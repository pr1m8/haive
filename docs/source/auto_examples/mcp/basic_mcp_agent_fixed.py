"""Example demonstrating basic MCP agent usage with type-checked integration.
Fixed version with correct imports.
"""

import asyncio
import logging

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import OpenAILLMConfig

from haive.mcp.agents import MCPAgent
from haive.mcp.config import MCPConfig, MCPServerConfig
from haive.mcp.discovery import MCPServerDiscovery

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def example_basic_mcp_agent():
    """Basic example of creating and using an MCP agent."""
    # Create an engine (adjust model as needed)
    engine = AugLLMConfig(
        llm_config=OpenAILLMConfig(model="gpt-4o-mini", temperature=0.1),
        name="mcp_engine",
    )

    # Create MCP configuration
    mcp_config = MCPConfig(
        enabled=True,
        servers={
            "filesystem": MCPServerConfig(
                name="filesystem",
                transport="stdio",
                command="npx",
                args=["-y", "@modelcontextprotocol/server-filesystem"],
                capabilities=["file_read", "file_write", "directory_list"],
                description="Local filesystem operations",
            )
        },
    )

    # Create MCP-enabled agent
    agent = MCPAgent(engine=engine, mcp_config=mcp_config, name="filesystem_assistant")

    # Initialize the agent
    await agent.setup()

    # Check MCP status
    status = agent.get_mcp_status()
    print(f"MCP Status: {status}")

    # Use the agent
    result = await agent.arun(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "List all Python files in the current directory",
                }
            ]
        }
    )

    print(f"Agent response: {result}")


async def example_dynamic_discovery():
    """Example using dynamic MCP server discovery."""
    # Create discovery instance
    discovery = MCPServerDiscovery()

    # Discover all available servers
    servers = await discovery.discover_all()
    print(f"Discovered {len(servers)} MCP servers")

    # Get discovery report
    report = discovery.get_discovery_report()
    print(f"Discovery report: {report}")

    # Create agent with discovered servers
    if servers:
        engine = AugLLMConfig(
            llm_config=OpenAILLMConfig(model="gpt-4o-mini", temperature=0.1),
            name="mcp_engine",
        )

        # Use discovered configuration
        mcp_config = discovery.create_mcp_config()

        agent = MCPAgent(
            engine=engine, mcp_config=mcp_config, name="discovered_mcp_agent"
        )

        await agent.setup()

        # List available capabilities
        capabilities = agent.get_available_capabilities()
        print(f"Available capabilities: {capabilities}")


async def example_multi_server_agent():
    """Example with multiple MCP servers."""
    engine = AugLLMConfig(
        llm_config=OpenAILLMConfig(model="gpt-4o-mini", temperature=0.1),
        name="mcp_engine",
    )

    # Create agent with multiple servers using convenience method
    agent = MCPAgent.create_with_mcp_servers(
        engine=engine,
        server_configs={
            "filesystem": {
                "transport": "stdio",
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem"],
                "capabilities": ["file_operations"],
            },
            "time": {
                "transport": "stdio",
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-time"],
                "capabilities": ["time_queries"],
            },
        },
        name="multi_mcp_agent",
    )

    await agent.setup()

    # Use agent with multiple capabilities
    result = await agent.arun(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What time is it? Also, create a file called 'timestamp.txt' with the current time.",
                }
            ]
        }
    )

    print(f"Multi-server result: {result}")


async def example_capability_based_tools():
    """Example finding tools by capability."""
    engine = AugLLMConfig(
        llm_config=OpenAILLMConfig(model="gpt-4o-mini", temperature=0.1),
        name="mcp_engine",
    )

    # Create agent
    agent = MCPAgent.create_with_mcp_servers(
        engine=engine,
        server_configs={
            "filesystem": {
                "transport": "stdio",
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem"],
                "capabilities": ["file_read", "file_write", "directory_list"],
            },
            "github": {
                "transport": "stdio",
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "capabilities": ["repo_access", "issue_management"],
                "env": {"GITHUB_TOKEN": "your_token_here"},  # Add real token
            },
        },
    )

    await agent.setup()

    # Find tools by capability
    file_tools = await agent.discover_tools_by_capability("file_read")
    print(f"Tools with file_read capability: {len(file_tools)}")

    repo_tools = await agent.discover_tools_by_capability("repo_access")
    print(f"Tools with repo_access capability: {len(repo_tools)}")


async def example_with_component_registry():
    """Example integrating with component registry."""
    # Discover servers
    discovery = MCPServerDiscovery()
    await discovery.discover_all()

    # Register with component registry
    await discovery.register_with_component_registry()

    # Now servers and tools are available through component registry
    try:
        from haive.core.utils.component_discovery import (
            ComponentType,
            create_component_registry,
        )

        registry = create_component_registry()

        # Search for MCP components
        mcp_components = registry.search_components(
            query="file operations", component_types=[ComponentType.MCP]
        )

        print(f"Found {len(mcp_components)} MCP components for file operations")

        # Get tools from MCP servers
        mcp_tools = registry.search_components(
            query="mcp", component_types=[ComponentType.TOOL]
        )

        print(f"Found {len(mcp_tools)} MCP tools")

    except ImportError:
        print("Component registry not available")


async def main():
    """Run all examples."""
    print("=== Basic MCP Agent Example ===")
    await example_basic_mcp_agent()

    print("\n=== Dynamic Discovery Example ===")
    await example_dynamic_discovery()

    print("\n=== Multi-Server Agent Example ===")
    await example_multi_server_agent()

    print("\n=== Capability-Based Tools Example ===")
    await example_capability_based_tools()

    print("\n=== Component Registry Integration Example ===")
    await example_with_component_registry()


if __name__ == "__main__":
    asyncio.run(main())
