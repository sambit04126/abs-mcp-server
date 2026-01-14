import pytest
from unittest.mock import Mock, AsyncMock, patch
from client.mcp_agent import MCPAgent

@pytest.mark.asyncio
async def test_agent_process_query():
    # Mock OpenAI client
    with patch("client.mcp_agent.AsyncOpenAI") as MockOpenAI:
        mock_client = MockOpenAI.return_value
        
        # Setup mock response for first call (tool call)
        mock_msg_1 = Mock()
        mock_msg_1.tool_calls = [
            Mock(
                id="call_123",
                function=Mock(
                    name="search_datasets",
                    arguments='{"keyword": "census"}',
                )
            )
        ]
        mock_msg_1.content = None

        # Setup mock response for second call (final answer)
        mock_msg_2 = Mock()
        mock_msg_2.tool_calls = []
        mock_msg_2.content = "The population is 2 million."

        # Configure chat.completions.create to return these in sequence
        mock_client.chat.completions.create = AsyncMock(side_effect=[
            Mock(choices=[Mock(message=mock_msg_1)]),
            Mock(choices=[Mock(message=mock_msg_2)])
        ])

        # Mock MCP Session
        with patch("client.mcp_agent.stdio_client") as mock_stdio:
            mock_stdio.return_value.__aenter__.return_value = (Mock(), Mock())
            
            with patch("client.mcp_agent.ClientSession") as MockSession:
                session_instance = MockSession.return_value
                session_instance.__aenter__.return_value = session_instance
                session_instance.initialize = AsyncMock()
                
                # Mock list_tools
                mock_tool = Mock()
                mock_tool.name = "search_datasets"
                mock_tool.description = "Search"
                mock_tool.inputSchema = {}
                session_instance.list_tools = AsyncMock(return_value=Mock(tools=[mock_tool]))
                
                # Mock call_tool
                session_instance.call_tool = AsyncMock(return_value=Mock(content=[{"id": "123", "name": "Census"}]))

                # Instantiate Agent
                agent = MCPAgent(api_key="fake-key")
                
                # Run Query
                response = await agent.process_query("What is the population?")
                
                assert response == "The population is 2 million."
                assert session_instance.initialize.called
                assert session_instance.list_tools.called
                assert session_instance.call_tool.called_with("search_datasets", arguments={"keyword": "census"})
