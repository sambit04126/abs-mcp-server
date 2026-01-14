import streamlit as st
import asyncio
import os
from dotenv import load_dotenv
from mcp_agent import MCPAgent

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="ABS Chat", 
    page_icon="📊", 
    layout="centered"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    st.session_state.agent = None

# Get API key
api_key = os.getenv("GOOGLE_API_KEY", "")

# Initialize agent
if api_key and st.session_state.agent is None:
    try:
        st.session_state.agent = MCPAgent(api_key=api_key)
    except Exception as e:
        st.error(f"❌ Failed to initialize: {e}")

# ============================================================================
# HEADER
# ============================================================================
# Title row with connection status
st.markdown(
    """
    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;'>
        <div>
            <h1 style='margin: 0; padding: 0;'>💬 ABS Chat</h1>
        </div>
    </div>
    """, 
    unsafe_allow_html=True
)

# Connection status badge (top right corner)
if api_key:
    st.success("✅ Connected")
else:
    st.error("❌ Not Connected - Set GOOGLE_API_KEY in .env")

st.markdown("---")

# Example Questions (collapsible)
with st.expander("💡 Example questions you can ask", expanded=False):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📊 Basic (Single numbers):**")
        st.markdown("• Current inflation rate (CPI)")
        st.markdown("• Latest unemployment rate")
        st.markdown("• Population of Australia")
        st.markdown("• Total registered births")
        st.markdown("• Annual deaths summary")
        st.markdown("• Average weekly earnings")
        st.markdown("• Total GDP")
        st.markdown("• Retail turnover last month")
        st.markdown("• Net overseas migration")
        st.markdown("• Building approvals total")
    
    with col2:
        st.markdown("**📈 Intermediate (Trends & Specifics):**")
        st.markdown("• Inflation change over last 5 years")
        st.markdown("• Birth rate trends last 10 years")
        st.markdown("• GDP growth rate quarterly trend")
        st.markdown("• Unemployment trend since 2020")
        st.markdown("• Population of Sydney vs 5 years ago")
        st.markdown("• Retail trade in Food vs Clothing")
        st.markdown("• Mining industry employment trends")
        st.markdown("• Wage Price Index annual growth")
        st.markdown("• House price index changes")
        st.markdown("• Export values last 12 months")
    
    with col3:
        st.markdown("**🌍 Advanced (Comparisons & Complex):**")
        st.markdown("• Compare unemployment: NSW vs Victoria")
        st.markdown("• CPI vs Wage Growth comparison")
        st.markdown("• Population growth: Brisbane vs Perth")
        st.markdown("• Retail trade: NSW vs QLD trend")
        st.markdown("• Mining vs Construction wages")
        st.markdown("• Exports vs Imports (Trade Balance)")
        st.markdown("• Migration: Arrivals vs Departures")
        st.markdown("• GDP contribution by State")
        st.markdown("• Housing finance: Owner vs Investor")
        st.markdown("• Male vs Female participation rate")

# ============================================================================
# CHAT MESSAGES
# ============================================================================
chat_container = st.container()

with chat_container:
    if not st.session_state.messages:
        # Clean, simple welcome
        st.info("👋 **Ready to help!** Start by asking a question below.", icon="💬")
    else:
        # Display all messages
        for msg in st.session_state.messages:
            # User question
            with st.chat_message("user"):
                st.markdown(f"**{msg['query']}**")
            
            # Assistant response with trace
            with st.chat_message("assistant"):
                # Collapsible execution trace
                if msg.get("logs"):
                    with st.expander("🔍 View execution trace", expanded=False):
                        for log in msg["logs"]:
                            st.markdown(log, unsafe_allow_html=True)
                
                # Answer
                st.markdown(msg["answer"])

# ============================================================================
# INPUT (Always at bottom)
# ============================================================================
st.markdown("---")

# Use a placeholder for processing indicator
if "processing" not in st.session_state:
    st.session_state.processing = False

# Only show input form when not processing
if not st.session_state.processing:
    with st.form(key="query_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_input = st.text_input(
                "Ask your question",
                placeholder="e.g., What is the current inflation rate?",
                label_visibility="collapsed",
                key="user_query_input"
            )
        
        with col2:
            submit_clicked = st.form_submit_button("Send 🚀", type="primary", use_container_width=True)
else:
    st.info("⏳ Processing your query...")
    user_input = None
    submit_clicked = False

# ============================================================================
# PROCESS QUERY
# ============================================================================
if submit_clicked and user_input:
    if not api_key:
        st.error("❌ Please set GOOGLE_API_KEY in .env file")
    elif st.session_state.agent is None:
        st.error("❌ Agent not initialized")
    else:
        # Set processing flag and rerun to hide input
        st.session_state.processing = True
        
        # Add placeholder message
        st.session_state.messages.append({
            "query": user_input,
            "answer": "⏳ Processing...",
            "logs": []
        })
        st.rerun()

# If we're processing, actually run the query
if st.session_state.processing and len(st.session_state.messages) > 0:
    last_msg = st.session_state.messages[-1]
    
    # Only process if it's still a placeholder
    if last_msg["answer"] == "⏳ Processing...":
        user_query = last_msg["query"]
        
        # Process query
        async def run_interaction():
            final_answer = ""
            interaction_logs = []
            
            async for event_type, content in st.session_state.agent.process_query(user_query):
                if event_type == "log":
                    if content and content != "undefined":
                        interaction_logs.append(content)
                elif event_type == "answer":
                    final_answer = content
            
            return final_answer, interaction_logs

        try:
            # Run with timeout
            async def run_with_timeout():
                return await asyncio.wait_for(
                    run_interaction(), 
                    timeout=30.0
                )
            
            response, logs = asyncio.run(run_with_timeout())
            
            if not response:
                response = "⚠️ I couldn't generate a response. Please try rephrasing your question."
            
            # Update the message
            st.session_state.messages[-1] = {
                "query": user_query,
                "answer": response,
                "logs": logs
            }
            
        except asyncio.TimeoutError:
            st.session_state.messages[-1] = {
                "query": user_query,
                "answer": "⏱️ **Query timeout:** This query is taking longer than expected (>30 seconds). Please try a more specific query or try again later.",
                "logs": []
            }
            
        except Exception as e:
            st.session_state.messages[-1] = {
                "query": user_query,
                "answer": f"❌ Error: {e}",
                "logs": []
            }
        
        # Clear processing flag and rerun
        st.session_state.processing = False
        st.rerun()
