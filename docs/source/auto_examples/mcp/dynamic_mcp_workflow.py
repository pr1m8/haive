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
    print("\n" + "=" * 60)
    print("🔔 APPROVAL REQUEST")
    print("=" * 60)
    print(f"Server: {request.recommendation.server_name}")
    print(f"Reason: {request.recommendation.reason}")
    print(f"Capabilities: {', '.join(request.recommendation.capabilities)}")
    print(f"Confidence: {request.recommendation.confidence:.2f}")

    if request.recommendation.alternative_servers:
        print(f"Alternatives: {', '.join(request.recommendation.alternative_servers)}")

    print("\nConfiguration:")
    print(f"  Transport: {request.recommendation.config.transport}")
    print(f"  Command: {request.recommendation.config.command}")
    print(f"  Args: {' '.join(request.recommendation.config.args or [])}")

    # In a real implementation, this would wait for actual user input
    # For demo, we'll auto-approve after showing the request
    print("\n⚡ Auto-approving for demonstration...")
    await asyncio.sleep(2)

    return True  # Approve


async def main():
    """Run the dynamic MCP workflow example."""

    print("🚀 Dynamic MCP Server Discovery and Installation Demo")
    print("=" * 60)

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
    print("\n📋 Initializing intelligent MCP agent...")
    await agent.setup()

    # Example 1: Request that needs web search capability
    print("\n\n📌 Example 1: Web Search Request")
    print("-" * 40)

    result1 = await agent.arun(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Search the web for the latest Python 3.13 features and summarize them",
                }
            ]
        }
    )

    print(f"\nAgent Response: {result1}")

    # Check installed servers
    status = await agent.mcp_manager.get_all_server_status()
    print(f"\n✅ Servers after Example 1: {list(status['servers'].keys())}")

    # Example 2: Request that needs filesystem access
    print("\n\n📌 Example 2: Filesystem Request")
    print("-" * 40)

    result2 = await agent.arun(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Create a file called 'python_features.md' with the search results",
                }
            ]
        }
    )

    print(f"\nAgent Response: {result2}")

    # Check installed servers again
    status = await agent.mcp_manager.get_all_server_status()
    print(f"\n✅ Servers after Example 2: {list(status['servers'].keys())}")

    # Example 3: Database request
    print("\n\n📌 Example 3: Database Request")
    print("-" * 40)

    result3 = await agent.arun(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "I need to connect to a PostgreSQL database and query user data",
                }
            ]
        }
    )

    print(f"\nAgent Response: {result3}")

    # Final status report
    print("\n\n📊 Final Status Report")
    print("=" * 60)

    final_status = agent.mcp_manager.get_all_server_status()
    print(f"Total servers: {final_status['summary']['total_servers']}")
    print(f"Connected: {final_status['summary']['connected_servers']}")
    print(f"Failed: {final_status['summary']['failed_servers']}")
    print(f"Total tools available: {final_status['summary']['total_tools']}")

    print("\n🔧 Available servers and their tools:")
    for server_name, server_info in final_status["servers"].items():
        print(f"\n  {server_name}:")
        print(f"    Status: {server_info['status']}")
        print(
            f"    Tools: {', '.join(server_info['tools']) if server_info['tools'] else 'None'}"
        )

    # Show recommendation history
    print("\n\n📜 Recommendation History:")
    for i, rec in enumerate(agent.get_recommendation_history(), 1):
        print(f"\n  {i}. {rec.server_name}")
        print(f"     Reason: {rec.reason}")
        print(f"     Confidence: {rec.confidence:.2f}")

    # Cleanup
    print("\n\n🧹 Shutting down MCP manager...")
    await agent.mcp_manager.shutdown()

    print("\n✨ Demo complete!")


async def advanced_example():
    """Advanced example with manual tool discovery and hot-reload."""

    print("\n\n🔬 Advanced Dynamic MCP Example")
    print("=" * 60)

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
    print("\n🔍 Manually discovering database servers...")

    discovery_result = await agent.arun(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Use the discover_mcp_servers tool to find database servers",
                }
            ]
        }
    )

    print(f"\nDiscovery result: {discovery_result}")

    # Install a specific server
    print("\n📦 Installing PostgreSQL server...")

    install_result = await agent.arun(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Use the install_mcp_server tool to install modelcontextprotocol/server-postgres",
                }
            ]
        }
    )

    print(f"\nInstallation result: {install_result}")

    # Hot-reload demonstration
    print("\n🔄 Demonstrating hot-reload...")

    # Get tools before
    tools_before = await agent.mcp_manager.get_all_tools()
    print(f"Tools before reload: {len(tools_before)}")

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
    tools_after = await agent.mcp_manager.get_all_tools(refresh=True)
    print(f"Tools after reload: {len(tools_after)}")

    # List all capabilities
    print("\n📋 Listing all MCP capabilities...")

    status_result = await agent.arun(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Use the list_mcp_status tool to show all available capabilities",
                }
            ]
        }
    )

    print(f"\nFull status: {status_result}")

    await agent.mcp_manager.shutdown()


if __name__ == "__main__":
    # Run basic example
    asyncio.run(main())

    # Uncomment to run advanced example
    # asyncio.run(advanced_example())
