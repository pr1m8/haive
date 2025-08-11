"""Example demonstrating dynamic MCP server discovery and installation workflow.

This example shows how to use the IntelligentMCPAgent to:
1. Automatically discover needed MCP servers based on user requests
2. Get HITL approval for installations
3. Install and configure servers dynamically
4. Use newly available tools without restart
"""

import asyncio
import logging

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import LLMConfig
from haive.mcp.agents import IntelligentMCPAgent
from haive.mcp.agents.intelligent_mcp_agent import HITLApprovalRequest

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Custom approval callback for demonstration
async def interactive_approval_callback(request: HITLApprovalRequest) -> bool:
    """Interactive approval callback that prompts user."""
    if request.recommendation.alternative_servers:
        pass

    # In a real implementation, this would wait for actual user input
    # For demo, we'll auto-approve after showing the request
    await asyncio.sleep(2)

    return True  # Approve


async def main():
    """Run the dynamic MCP workflow example."""
    # Create engine configuration
    engine = AugLLMConfig(
        llm_config=LLMConfig(provider="openai", model="gpt-4o-mini"),
        name="intelligent_mcp_engine",
    )

    # Create intelligent agent with custom approval callback
    agent = IntelligentMCPAgent(
        engine=engine,
        name="dynamic_mcp_assistant",
        auto_discover=True,
        require_approval=True,
        approval_callback=interactive_approval_callback,
    )

    # Initialize the agent
    await agent.setup()

    # Example 1: Request that needs web search capability

    await agent.arun(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Search the web for the latest Python 3.13 features and summarize them",
                }
            ]
        }
    )

    # Check installed servers
    await agent.mcp_manager.get_all_server_status()

    # Example 2: Request that needs filesystem access

    await agent.arun(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Create a file called 'python_features.md' with the search results",
                }
            ]
        }
    )

    # Check installed servers again
    await agent.mcp_manager.get_all_server_status()

    # Example 3: Database request

    await agent.arun(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "I need to connect to a PostgreSQL database and query user data",
                }
            ]
        }
    )

    # Final status report

    final_status = agent.mcp_manager.get_all_server_status()

    for _server_name, _server_info in final_status["servers"].items():
        pass

    # Show recommendation history
    for _i, _rec in enumerate(agent.get_recommendation_history(), 1):
        pass

    # Cleanup
    await agent.mcp_manager.shutdown()


async def advanced_example():
    """Advanced example with manual tool discovery and hot-reload."""
    # Create engine
    engine = AugLLMConfig(llm_config=LLMConfig(provider="openai", model="gpt-4o-mini"))

    # Create agent with manual discovery (no auto-discover)
    agent = IntelligentMCPAgent(
        engine=engine,
        name="manual_discovery_agent",
        auto_discover=False,  # Manual control
        require_approval=False,  # No approval needed
    )

    await agent.setup()

    # Manually discover servers for a capability

    await agent.arun(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Use the discover_mcp_servers tool to find database servers",
                }
            ]
        }
    )

    # Install a specific server

    await agent.arun(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Use the install_mcp_server tool to install modelcontextprotocol/server-postgres",
                }
            ]
        }
    )

    # Hot-reload demonstration

    # Get tools before
    await agent.mcp_manager.get_all_tools()

    # Reload the server
    await agent.arun(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Use the reload_mcp_server tool to reload the postgres server",
                }
            ]
        }
    )

    # Get tools after (with refresh)
    await agent.mcp_manager.get_all_tools(refresh=True)

    # List all capabilities

    await agent.arun(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Use the list_mcp_status tool to show all available capabilities",
                }
            ]
        }
    )

    await agent.mcp_manager.shutdown()


if __name__ == "__main__":
    # Run basic example
    asyncio.run(main())

    # Uncomment to run advanced example
    # asyncio.run(advanced_example())
