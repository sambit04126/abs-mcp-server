
import asyncio
import os
import sys
from dotenv import load_dotenv

# Add src to path so we can import client
sys.path.append(os.path.abspath("src"))

from client.mcp_agent import MCPAgent

# Load env for Google API Key
load_dotenv()

async def run_test():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY not found in environment.")
        return

    print("🤖 Initializing MCP Agent with Gemini...")
    agent = MCPAgent(api_key=api_key)
    
    query = "What is the current population of Perth?"
    print(f"\n❓ Query: {query}\n")
    print("--- MCP Transaction Log ---")

    try:
        async for event_type, content in agent.process_query(query):
            if event_type == "log":
                # Print logs with a prefix to show activity
                print(f"[LOG] {content}")
            elif event_type == "answer":
                print(f"\n✅ FINAL ANSWER:\n{content}")
    except Exception as e:
        print(f"\n❌ Exception during MCP execution: {e}")

if __name__ == "__main__":
    asyncio.run(run_test())
