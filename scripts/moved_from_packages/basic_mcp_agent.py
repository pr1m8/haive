"""Example demonstrating basic MCP agent usage with type-checked integration."""

import asyncio
import logging

from haive.core.engine import create_engine
from haive.mcp.agents import MCPAgent
from haive.mcp.config import MCPConfig, MCPServerConfig
from haive.mcp.discovery import MCPServerDiscovery

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def example_basic_mcp_agent():
    """Basic example of creating and using an MCP agent."""
    # Create an engine (adjust model as needed)
    engine = create_engine(model="gpt-4o-mini")

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
    agent.get_mcp_status()

    # Use the agent
    await agent.arun(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "List all Python files in the current directory",
                }
            ]
        }
    )


async def example_dynamic_discovery():
    """Example using dynamic MCP server discovery."""
    # Create discovery instance
    discovery = MCPServerDiscovery()

    # Discover all available servers
    servers = await discovery.discover_all()

    # Get discovery report
    discovery.get_discovery_report()

    # Create agent with discovered servers
    if servers:
        engine = create_engine(model="gpt-4o-mini")

        # Use discovered configuration
        mcp_config = discovery.create_mcp_config()

        agent = MCPAgent(
            engine=engine, mcp_config=mcp_config, name="discovered_mcp_agent"
        )

        await agent.setup()

        # List available capabilities
        agent.get_available_capabilities()


async def example_multi_server_agent():
    """Example with multiple MCP servers."""
    engine = create_engine(model="gpt-4o-mini")

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
    await agent.arun(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What time is it? Also, create a file called 'timestamp.txt' with the current time.",
                }
            ]
        }
    )


async def example_capability_based_tools():
    """Example finding tools by capability."""
    engine = create_engine(model="gpt-4o-mini")

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
    await agent.discover_tools_by_capability("file_read")

    await agent.discover_tools_by_capability("repo_access")


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
        registry.search_components(
            query="file operations", component_types=[ComponentType.MCP]
        )

        # Get tools from MCP servers
        registry.search_components(query="mcp", component_types=[ComponentType.TOOL])

    except ImportError:
        pass


async def main():
    """Run all examples."""
    await example_basic_mcp_agent()

    await example_dynamic_discovery()

    await example_multi_server_agent()

    await example_capability_based_tools()

    await example_with_component_registry()


if __name__ == "__main__":
    asyncio.run(main())
