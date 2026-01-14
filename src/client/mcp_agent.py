import os
import sys
import json
import asyncio
from typing import List, Dict, Any, Optional
from pathlib import Path
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession
from google import genai
from google.genai import types

# Add src/client to path for imports
sys.path.insert(0, str(Path(__file__).parent))
import topic_mapping
TOPIC_TO_DATASET = topic_mapping.TOPIC_TO_DATASET

# Configuration
MAX_TURNS = int(os.getenv("MAX_TURNS", "10"))  # Max LLM invocations per query

class MCPAgent:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.model_id = os.getenv("LLM_MODEL", "gemini-2.0-flash")  # Use stable model
        
        # Get current date for temporal context
        from datetime import datetime
        current_date = datetime.now()
        current_year = current_date.year
        current_month = current_date.strftime("%Y-%m")
        
        # Build Knowledge Base string with dimension defaults
        kb_str = "\nKNOWN DATASETS WITH DIMENSION DEFAULTS:\n"
        for topic, info in TOPIC_TO_DATASET.items():
            dataset_id = info["dataset_id"]
            desc = info.get("description", "")
            dims = info.get("common_dimensions", {})
            kb_str += f"- Topic '{topic}' → Dataset '{dataset_id}' ({desc})\n"
            if dims:
                kb_str += f"  Default dimensions: {dims}\n"
            if info.get("regional_codes"):
                kb_str += f"  Regional codes: {list(info['regional_codes'].keys())}\n"
        
        self.system_instruction = f"""You are an expert assistant for querying Australian Bureau of Statistics (ABS) data.

TODAY'S DATE: {current_date.strftime("%B %d, %Y")} (Use this for temporal context)

CRITICAL WORKFLOW - ALWAYS FOLLOW THIS ORDER:
1. For known topics (inflation, population, employment, GDP, wages, retail, exports, imports, trade, commodity, migration, migrants, housing, building), use the dataset mappings directly (0 search calls)
2. Use get_dataset_structure FIRST to see all valid dimension codes
3. Construct filters using ONLY the codes from step 2
4. Use get_dataset_data with proper filters

{kb_str}

TEMPORAL HANDLING (CRITICAL):
- **DEFAULT TO LATEST DATA**: If user asks "population of Sydney" or "current inflation" WITHOUT specifying a year, DO NOT set start_period or end_period - this returns the MOST RECENT data available
- **"Latest", "Current", "Now"**: No time filters (gets most recent)
- **"This year"**: Set start_period="{current_year}-01", end_period="{current_month}"
- **"Last year"**: Set start_period="{current_year-1}-01", end_period="{current_year-1}-12"
- **Specific years** (e.g., "2023"): Set start_period="2023-01", end_period="2023-12"
- **"Last 12 months"**: Calculate from current month backwards

SDMX RULES FROM ABS DOCUMENTATION:
- All dimensions usually required (use defaults above or search if unknown)
- Dimension values must be CODES (e.g. "M", "3", "50"), never names
- Time period uses start_period/end_period parameters (YYYY-MM format)
- For regional queries, check regional_codes mapping above

SPECIAL INSTRUCTIONS:
- For EXPORTS: Use MERCH_EXP or BOP_GOODS datasets, search for commodity codes
- For IMPORTS: Use BOP_GOODS dataset
- For TRADE: Use ITGS (International Trade in Goods) dataset
- For commodities (iron ore, coal, etc): Search within export datasets using SITC codes

EXAMPLE WORKFLOWS:
✅ GOOD: "population of Sydney" → Use ABS_ANNUAL_ERP_ASGS2021, NO time filter → gets latest available
✅ GOOD: "inflation in 2023" → Use CPI_M, start_period="2023-01", end_period="2023-12"
✅ GOOD: "current GDP" → Use ANA_EXP, NO time filter → gets latest
❌ BAD: Always setting time filters (prevents getting latest data)
❌ BAD: Using dimension names instead of codes

ANSWER FORMAT:
- State the data point with its time period (e.g., "As of March 2024, ...")
- Be concise: 2-3 sentences with key numbers
- Always mention the date/period of the data
"""
        
        # Determine path to server script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up two levels from src/client to root, then down to src/abs_mcp_server/server.py
        self.server_script = os.path.join(current_dir, "..", "abs_mcp_server", "server.py")
        self.server_script = os.path.abspath(self.server_script)
        self.root_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))

    def _log_event(self, event_type: str, data: Any):
        """Logs events to a JSONL file for debugging."""
        import datetime
        timestamp = datetime.datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "event_type": event_type,
            "data": data
        }
        try:
            with open("query_trace.jsonl", "a") as f:
                f.write(json.dumps(log_entry) + "\n") # Serialize data properly
        except Exception as e:
            print(f"Failed to write log: {e}")


    def _clean_schema(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively cleans JSON schema to be compatible with Gemini.
        Removes 'additionalProperties', 'title', etc.
        Flattens 'anyOf' for Optional fields.
        """
        if not isinstance(schema, dict):
            return schema
            
        # Create copy to avoid mutating original
        clean = schema.copy()
        
        # Remove keys known to cause issues
        for key in ["additionalProperties", "title", "type_alias"]:
             if key in clean:
                 del clean[key]
        
        # Flatten anyOf: [{'type': 'string'}, {'type': 'null'}] -> {'type': 'string'}
        if "anyOf" in clean:
            options = clean["anyOf"]
            # specific fix for Optional[str] etc which appears as string | null
            valid_option = None
            for opt in options:
                if opt.get("type") != "null":
                    valid_option = opt
                    break
            
            if valid_option:
                # Merge the valid option into clean and remove anyOf
                # We recurse on valid_option first
                cleaned_valid = self._clean_schema(valid_option)
                clean.update(cleaned_valid)
                del clean["anyOf"]
                # If it was optional, we might strictly lose that info here, 
                # but for LLM tool calling, treating it as the base type is usually fine 
                # as long as we don't mark it required.
        
        # Recursive cleaning
        for key, value in clean.items():
            if isinstance(value, dict):
                clean[key] = self._clean_schema(value)
            elif isinstance(value, list):
                clean[key] = [self._clean_schema(item) if isinstance(item, dict) else item for item in value]
                
        return clean

    async def process_query(self, user_query: str):
        """
        Processes a query using Gemini and yields updates.
        """
        self._log_event("user_query_start", {"query": user_query})
        
        yield ("log", f"Drafting plan for query: '{user_query}'")

        # Server parameters
        # Try to locate .venv python
        venv_python = os.path.join(self.root_dir, ".venv", "bin", "python")
        if os.path.exists(venv_python):
            server_python = venv_python
            # log it for debugging
            self._log_event("server_startup", {"executable_used": "venv", "path": venv_python})
        else:
            server_python = sys.executable
            self._log_event("server_startup", {"executable_used": "sys.executable", "path": server_python})

        server_params = StdioServerParameters(
            command=server_python, 
            args=["-m", "abs_mcp_server.server"],
            env={**os.environ.copy(), "PYTHONPATH": os.path.join(self.root_dir, "src")},
            cwd=self.root_dir
        )

        try:
            # Create a client session
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    yield ("log", "Connected to MCP Server.")
                    
                    # Get available tools
                    tools_list = await session.list_tools()
                    tool_names = [t.name for t in tools_list.tools]
                    yield ("log", f"Discovered Tools: {tool_names}")
                    self._log_event("tools_discovered", {"tools": tool_names})
                    
                    # Convert MCP tools to Gemini tools format
                    gemini_funcs = []
                    for tool in tools_list.tools:
                        # Clean the schema
                        cleaned_schema = self._clean_schema(tool.inputSchema)
                        
                        gemini_funcs.append(types.FunctionDeclaration(
                            name=tool.name,
                            description=tool.description,
                            parameters=cleaned_schema
                        ))
                    
                    tool_config = types.Tool(function_declarations=gemini_funcs)

                    # Initialize Chat
                    # Create a fresh client for this async context to avoid "Event loop is closed" errors
                    client = genai.Client(api_key=self.api_key)
                    chat = client.aio.chats.create(
                        model=self.model_id,
                        config=types.GenerateContentConfig(
                            system_instruction=self.system_instruction,
                            tools=[tool_config]
                        )
                    )

                    # Send User Message
                    yield ("log", "Asking Gemini for next step...")
                    self._log_event("gemini_request", {"message": user_query})
                    response = await chat.send_message(user_query)
                    self._log_event("gemini_response", {"text": response.text, "function_calls": [{"name": fc.name, "args": fc.args} for part in response.candidates[0].content.parts for fc in [part.function_call] if fc] if response.candidates else []})

                    # Loop to handle tool calls with turn limit
                    turn_count = 0
                    max_turns = MAX_TURNS
                    
                    while turn_count < max_turns:
                        function_calls = []
                        # Check if response has text part to yield immediately?
                        # Gemini often returns text thinking + function call in one turn (gemini-2.0).
                        if response.text:
                             # We can yield it as a log or partial answer?
                             # Let's yield it as log for now to show "Thinking"
                             yield ("log", f"💭 **Model Thought**: {response.text}")

                        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                            for part in response.candidates[0].content.parts:
                                if part.function_call:
                                    function_calls.append(part.function_call)
                            
                        if not function_calls:
                            # If no function calls, this is the final answer
                            break
                        
                        # Increment turn count
                        turn_count += 1
                        yield ("log", f"🔄 Turn {turn_count}/{max_turns}")
                        
                        if turn_count >= max_turns:
                            yield ("log", f"⚠️ **Max turns reached ({max_turns}). Stopping to prevent runaway.**")
                            final_text = response.text or "Query stopped: Maximum iteration limit reached. Try simplifying your question."
                            yield ("answer", final_text)
                            self._log_event("max_turns_exceeded", {"turns": turn_count})
                            return
                            
                        # Execute all function calls
                        parts_to_send_back = []
                        
                        for fc in function_calls:
                            func_name = fc.name
                            func_args = fc.args
                            
                            yield ("log", f"🛠️ **Invoking Tool**: `{func_name}`")
                            yield ("log", f"**Arguments**:\n```json\n{json.dumps(dict(fc.args), indent=2)}\n```")
                            
                            try:
                                 # MCP call
                                 self._log_event("tool_call_start", {"name": func_name, "args": func_args})
                                 result = await session.call_tool(func_name, arguments=func_args)
                                 
                                 content_text = ""
                                 if isinstance(result.content, list):
                                     for c in result.content:
                                         if hasattr(c, 'text'):
                                             content_text += c.text
                                         else:
                                             content_text += str(c)
                                 else:
                                     content_text = str(result.content)
                                 
                                 display_output = content_text[:500] + "..." if len(content_text) > 500 else content_text
                                 if display_output and display_output != "undefined":
                                     yield ("log", f"**Tool Output**:\n```\n{display_output}\n```")
                                 self._log_event("tool_call_result", {"name": func_name, "output_preview": display_output, "full_output": content_text})
                                 
                                 parts_to_send_back.append(
                                     types.Part(
                                         function_response=types.FunctionResponse(
                                             name=func_name,
                                             response={"result": content_text}
                                        )
                                     )
                                 )

                            except Exception as e:
                                 error_msg = f"Error: {e}"
                                 yield ("log", f"❌ **Tool Error**: {error_msg}")
                                 self._log_event("tool_call_error", {"name": func_name, "error": str(e)})
                                 parts_to_send_back.append(
                                     types.Part(
                                         function_response=types.FunctionResponse(
                                             name=func_name,
                                             response={"error": error_msg}
                                         )
                                     )
                                 )
                        
                        # Feed back to Gemini
                        yield ("log", "Feeding tool results back to Gemini...")
                        self._log_event("gemini_tool_feedback", {"parts_count": len(parts_to_send_back)})
                        response = await chat.send_message(parts_to_send_back)
                        
                        # Log the subsequent response
                        fcs_log = []
                        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                            for part in response.candidates[0].content.parts:
                                if part.function_call:
                                    fcs_log.append({"name": part.function_call.name, "args": part.function_call.args})
                        
                        self._log_event("gemini_response_after_tool", {
                            "text": response.text if response.candidates else "", 
                            "function_calls": fcs_log
                        })

                    # Final response
                    try:
                        if response.text:
                            yield ("answer", response.text)
                            self._log_event("final_answer", {"text": response.text})
                        else:
                             # Check finish reason again
                             reason = "Unknown"
                             if response.candidates and response.candidates[0].finish_reason:
                                 reason = str(response.candidates[0].finish_reason)
                             
                             if "MALFORMED_FUNCTION_CALL" in reason:
                                 yield ("log", "⚠️ Model made a malformed call. Asking it to summarize what it has so far...")
                                 # Self-correction: ask the model to stop trying to use tools and just answer
                                 correction_prompt = "You made a malformed tool call. Please STOP calling tools. Just summarize the data you have collected so far into a final answer."
                                 response = await chat.send_message(correction_prompt)
                                 if response.text:
                                     yield ("answer", response.text)
                                     self._log_event("final_answer_recovered", {"text": response.text})
                                     return
                                     
                             yield ("answer", f"⚠️ No text generated. (Finish Reason: {reason})")
                    except Exception as e:
                        reason = "Unknown"
                        if response.candidates and response.candidates[0].finish_reason:
                            reason = str(response.candidates[0].finish_reason)
                        yield ("answer", f"⚠️ Response content inaccessible. Finish Reason: {reason}")
                        
        except Exception as e:
            # Log the full error to help debug
            import traceback
            traceback.print_exc()
            error_msg = f"❌ Execution Error: {e}"
            yield ("log", error_msg)
            self._log_event("execution_error", {"error": str(e), "traceback": traceback.format_exc()})
            # IMPORTANT: Yield an answer so the UI doesn't say "No response"
            yield ("answer", f"I encountered an error while processing your request:\n\n{error_msg}")
