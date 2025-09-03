#!/usr/bin/env python3
"""Example demonstrating the Haive Dataflow MCP Server.

This example shows how to:
1. Start the dataflow MCP server
2. Connect to it from a client
3. Use the exposed tools to query registry, discover components, and create agents
4. Access resources for registry information
"""

import asyncio
import logging
from pathlib import Path

# MCP client imports
from mcp.client import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def run_dataflow_mcp_example():
    """Run example interactions with the Dataflow MCP server."""
    # Server path - adjust based on your setup
    server_script = (
        Path(__file__).parent.parent
        / "src"
        / "haive"
        / "mcp"
        / "servers"
        / "dataflow_mcp_server.py"
    )

    # Create server parameters for stdio transport
    server_params = StdioServerParameters(command="python", args=[str(server_script)])

    # Connect to the server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()

            logger.info("Connected to Haive Dataflow MCP Server")

            # List available tools
            tools = await session.list_tools()
            logger.info(f"\nAvailable tools: {len(tools)}")
            for tool in tools:
                logger.info(f"  - {tool.name}: {tool.description}")

            # List available resources
            resources = await session.list_resources()
            logger.info(f"\nAvailable resources: {len(resources)}")
            for resource in resources:
                logger.info(f"  - {resource.uri}: {resource.name}")

            # Example 1: Query the registry
            logger.info("\n=== Example 1: Query Registry ===")
            result = await session.call_tool(
                "query_registry", arguments={"entity_type": "agent", "limit": 5}
            )
            logger.info(f"Found {len(result)} agents in registry:")
            for entity in result:
                logger.info(f"  - {entity.get('name')}: {entity.get('description')}")

            # Example 2: Discover components
            logger.info("\n=== Example 2: Discover Components ===")
            discovery_result = await session.call_tool(
                "discover_components",
                arguments={"component_type": "all", "auto_register": False},
            )
            logger.info("Discovery results:")
            logger.info(f"  - Agents: {len(discovery_result.get('agents', []))}")
            logger.info(f"  - Tools: {len(discovery_result.get('tools', []))}")
            logger.info(f"  - Total: {discovery_result.get('total', 0)}")

            # Example 3: Create an agent
            logger.info("\n=== Example 3: Create Agent ===")
            agent_result = await session.call_tool(
                "create_agent",
                arguments={
                    "request": {
                        "name": "research_assistant",
                        "model": "gpt-4o-mini",
                        "tools": ["web_search", "calculator"],
                        "system_prompt": "You are a helpful research assistant.",
                        "temperature": 0.7,
                    }
                },
            )
            if agent_result.get("success"):
                logger.info(f"Created agent: {agent_result.get('agent_id')}")
                logger.info(f"Message: {agent_result.get('message')}")
            else:
                logger.error(f"Failed to create agent: {agent_result.get('error')}")

            # Example 4: Execute a tool
            logger.info("\n=== Example 4: Execute Tool ===")
            exec_result = await session.call_tool(
                "execute_tool",
                arguments={
                    "tool_name": "calculator",
                    "input_data": {"expression": "2 + 2"},
                },
            )
            logger.info(f"Tool execution result: {exec_result}")

            # Example 5: Access resources
            logger.info("\n=== Example 5: Access Resources ===")

            # Get registry entities
            registry_resource = await session.read_resource("registry://entities")
            logger.info("Registry entities by type:")
            entities = registry_resource.get("entities", {})
            for entity_type, items in entities.items():
                logger.info(f"  - {entity_type}: {len(items)} items")

            # Get registry statistics
            stats_resource = await session.read_resource("registry://statistics")
            logger.info("\nRegistry statistics:")
            logger.info(
                f"  - Total entities: {stats_resource.get('total_entities', 0)}"
            )
            logger.info(f"  - By type: {stats_resource.get('by_type', {})}")

            # Example 6: Use prompts
            logger.info("\n=== Example 6: Use Prompts ===")

            # List available prompts
            prompts = await session.list_prompts()
            logger.info(f"Available prompts: {len(prompts)}")
            for prompt in prompts:
                logger.info(f"  - {prompt.name}: {prompt.description}")

            # Get a specific prompt
            if prompts:
                prompt_result = await session.get_prompt(
                    prompts[0].name,
                    arguments={
                        "requirement": "I need to process and analyze documents"
                    },
                )
                logger.info("\nGenerated prompt:")
                for msg in prompt_result.messages:
                    logger.info(f"  [{msg.role}]: {msg.content[:100]}...")


async def demonstrate_mcp_integration():
    """Demonstrate MCP integration with AugLLMConfig."""
    logger.info("\n=== MCP Integration with AugLLMConfig ===")

    try:
        from haive.mcp.integration.aug_llm_mcp_extension import (
            MCPServerConfig,
            create_mcp_enabled_aug_config,
        )

        # Create MCP-enabled configuration
        config = await create_mcp_enabled_aug_config(
            name="mcp_research_agent",
            model="gpt-4o-mini",
            mcp_servers={
                "dataflow": MCPServerConfig(
                    name="dataflow",
                    transport="stdio",
                    command="python",
                    args=[
                        str(
                            Path(__file__).parent.parent
                            / "src"
                            / "haive"
                            / "mcp"
                            / "servers"
                            / "dataflow_mcp_server.py"
                        )
                    ],
                )
            },
            system_message="You are a helpful AI assistant with access to Haive components.",
            tools=["web_search"],  # Additional non-MCP tools
            temperature=0.7,
        )

        logger.info(f"Created MCP-enabled config: {config.name}")
        logger.info(
            f"MCP tools discovered: {len([t for t in config.tools if t.startswith('dataflow_')])}"
        )
        logger.info(f"MCP resources loaded: {len(config.mcp_resources or [])}")
        logger.info(f"MCP prompts available: {len(config.mcp_prompts or {})}")

        # The enhanced system prompt includes MCP information
        logger.info("\nEnhanced system prompt preview:")
        logger.info(config.system_message[:200] + "...")

    except ImportError as e:
        logger.warning(f"Could not demonstrate AugLLMConfig integration: {e}")


async def main():
    """Run all examples."""
    logger.info("Starting Haive Dataflow MCP Examples")

    # Run basic MCP client examples
    await run_dataflow_mcp_example()

    # Demonstrate integration
    await demonstrate_mcp_integration()

    logger.info("\nExamples completed!")


if __name__ == "__main__":
    asyncio.run(main())
