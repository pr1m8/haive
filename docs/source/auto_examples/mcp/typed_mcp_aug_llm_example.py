#!/usr/bin/env python3
"""Example demonstrating type-safe MCP integration with AugLLMConfig.

This example shows how to use the MCPAugLLMConfig class which provides
full type checking for MCP configurations while integrating seamlessly
with the existing AugLLMConfig functionality.
"""

import asyncio
import logging
from pathlib import Path

# Agent imports for demonstration
from haive.agents import ReactAgent

# Haive imports with proper typing
from haive.core.engine.aug_llm import MCPAugLLMConfig, create_mcp_aug_llm_config
from haive.core.models.llm.base import LLMConfig
from pydantic import BaseModel, Field

# MCP imports with full types
from haive.mcp.config import MCPConfig, MCPServerConfig, MCPTransport

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Example structured output model
class AnalysisResult(BaseModel):
    """Structured output for file analysis."""

    file_count: int = Field(..., description="Number of files analyzed")
    total_size: int = Field(..., description="Total size in bytes")
    file_types: list[str] = Field(
        default_factory=list, description="Unique file types found"
    )
    summary: str = Field(..., description="Brief summary of findings")


async def example_basic_mcp_config():
    """Demonstrate basic type-safe MCP configuration."""
    logger.info("\n=== Basic Type-Safe MCP Configuration ===")

    # Create properly typed MCP server configuration
    filesystem_server = MCPServerConfig(
        name="filesystem",
        enabled=True,
        transport=MCPTransport.STDIO,
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem"],
        env={"ALLOWED_PATHS": "/tmp"},
        capabilities=["file_read", "file_write", "directory_list"],
        category="storage",
        description="Local filesystem operations",
        timeout=30,
        retry_attempts=3,
    )

    # Create MCP configuration with full typing
    mcp_config = MCPConfig(
        enabled=True,
        servers={"filesystem": filesystem_server},
        auto_discover=False,
        lazy_init=False,
        global_timeout=60,
        max_concurrent_servers=5,
    )

    # Create MCPAugLLMConfig with all types properly checked
    config = MCPAugLLMConfig(
        name="file_analyzer",
        llm_config=LLMConfig(
            provider="openai", model="gpt-4o-mini", temperature=0.3, max_tokens=1000
        ),
        system_message="You are a file system analysis expert.",
        mcp_config=mcp_config,
        structured_output_model=AnalysisResult,
        structured_output_version="v2",  # Use tool-based output
        tools=["calculator"],  # Can still add non-MCP tools
        auto_discover_mcp_tools=True,
        inject_mcp_resources=True,
        use_mcp_prompts=True,
    )

    # Initialize MCP
    await config.setup()

    # Debug the configuration
    config.debug_mcp_state()

    # Show type information
    logger.info("\nType Information:")
    logger.info(f"  Config type: {type(config).__name__}")
    logger.info(f"  MCP config type: {type(config.mcp_config).__name__}")
    logger.info(f"  Has {len(config.get_mcp_tools())} MCP tools")
    logger.info(f"  Has {len(config.get_all_tools())} total tools")

    # Cleanup
    config.cleanup()


async def example_multiple_servers():
    """Demonstrate configuration with multiple MCP servers."""
    logger.info("\n=== Multiple MCP Servers with Type Safety ===")

    # Define multiple server configurations
    servers = {
        "filesystem": MCPServerConfig(
            name="filesystem",
            transport=MCPTransport.STDIO,
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem"],
            capabilities=["file_operations"],
            category="storage",
        ),
        "github": MCPServerConfig(
            name="github",
            transport=MCPTransport.STDIO,
            command="npx",
            args=["-y", "@modelcontextprotocol/server-github"],
            env={"GITHUB_TOKEN": "your_token_here"},
            capabilities=["repo_access", "issue_management"],
            category="development",
        ),
        "postgres": MCPServerConfig(
            name="postgres",
            transport=MCPTransport.STDIO,
            command="npx",
            args=["-y", "@modelcontextprotocol/server-postgres"],
            env={"DATABASE_URL": "postgresql://localhost/testdb"},
            capabilities=["database_query"],
            category="database",
        ),
    }

    # Create configuration
    config = MCPAugLLMConfig(
        name="multi_server_agent",
        llm_config=LLMConfig(provider="openai", model="gpt-4o-mini"),
        mcp_config=MCPConfig(
            enabled=True,
            servers=servers,
            categories=["storage", "development"],  # Filter by category
            required_capabilities=["file_operations"],  # Require specific capabilities
        ),
        system_message="AI assistant with access to files, GitHub, and database.",
    )

    await config.setup()

    # Show tools organized by server
    logger.info("\nTools by MCP Server:")
    for tool in config.get_mcp_tools():
        server_name = tool.name.split("_")[0]
        logger.info(f"  {server_name}: {tool.name}")

    # Access tool by name with type safety
    tool_name = "filesystem_read_file"
    tool = config.get_tool_by_name(tool_name)
    if tool:
        logger.info(f"\nFound tool '{tool_name}': {type(tool).__name__}")

    config.cleanup()


async def example_with_agent():
    """Demonstrate using MCPAugLLMConfig with an agent."""
    logger.info("\n=== Using MCPAugLLMConfig with ReactAgent ===")

    # Use factory function for convenience
    config = await create_mcp_aug_llm_config(
        name="agent_assistant",
        model="gpt-4o-mini",
        mcp_servers={
            "filesystem": {
                "transport": "stdio",
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem"],
                "env": {"ALLOWED_PATHS": "/tmp"},
            }
        },
        system_message="You are a helpful AI assistant with filesystem access.",
        temperature=0.7,
        structured_output_model=AnalysisResult,
    )

    # Create agent with MCP-enabled config
    agent = ReactAgent(engine=config, name="mcp_react_agent")

    # Initialize agent
    await agent.setup()

    logger.info(f"\nAgent ready with {len(config.get_all_tools())} tools")
    logger.info("Available MCP operations:")
    for tool in config.get_mcp_tools()[:5]:  # Show first 5
        logger.info(f"  - {tool.name}: {tool.description}")

    # The agent can now use MCP tools alongside regular tools
    # Example usage (would need actual implementation):
    # result = await agent.arun({
    #     "messages": [{
    #         "role": "user",
    #         "content": "List files in /tmp and analyze them"
    #     }]
    # })

    # Cleanup
    config.cleanup()


async def example_custom_server():
    """Demonstrate configuration with custom MCP server."""
    logger.info("\n=== Custom MCP Server Configuration ===")

    # Path to custom server
    custom_server_path = (
        Path(__file__).parent.parent
        / "src"
        / "haive"
        / "mcp"
        / "servers"
        / "dataflow_mcp_server.py"
    )

    # Configure custom server with full typing
    custom_server = MCPServerConfig(
        name="haive_dataflow",
        transport=MCPTransport.STDIO,
        command="python",
        args=[str(custom_server_path)],
        capabilities=[
            "registry_query",
            "component_discovery",
            "agent_creation",
            "tool_execution",
        ],
        category="haive",
        description="Haive dataflow system integration",
        timeout=60,
        health_check_interval=30,
    )

    # Create config with custom server
    config = MCPAugLLMConfig(
        name="haive_integration",
        llm_config=LLMConfig(provider="openai", model="gpt-4o-mini"),
        mcp_config=MCPConfig(
            enabled=True, servers={"dataflow": custom_server}, enable_health_checks=True
        ),
        system_message="AI assistant integrated with Haive's dataflow system.",
    )

    await config.setup()

    # Show discovered resources
    resources = config.get_mcp_resources()
    if resources:
        logger.info(f"\nDiscovered {len(resources)} MCP resources:")
        for resource in resources[:3]:
            logger.info(f"  - {resource.uri}: {resource.name} ({resource.mime_type})")

    # Show available prompts
    prompts = config.get_mcp_prompts()
    if prompts:
        logger.info(f"\nAvailable MCP prompts: {list(prompts.keys())}")

    config.cleanup()


async def example_type_checking_benefits():
    """Demonstrate type checking benefits with MCPAugLLMConfig."""
    logger.info("\n=== Type Checking Benefits ===")

    # This would cause type errors if uncommented:
    # config = MCPAugLLMConfig(
    #     mcp_config="invalid"  # Type error: expected MCPConfig
    # )

    # config = MCPAugLLMConfig(
    #     mcp_config=MCPConfig(
    #         servers={
    #             "test": "invalid"  # Type error: expected MCPServerConfig
    #         }
    #     )
    # )

    # Proper typed configuration
    config = MCPAugLLMConfig(
        name="typed_config",
        llm_config=LLMConfig(provider="openai", model="gpt-4"),
        mcp_config=MCPConfig(
            enabled=True,
            servers={
                "test": MCPServerConfig(
                    name="test",
                    transport=MCPTransport.STDIO,  # Type-safe enum
                    command="test",
                    args=["arg1", "arg2"],  # Type: list[str]
                    timeout=30,  # Type: int
                    enabled=True,  # Type: bool
                )
            },
            max_concurrent_servers=5,  # Type: int
            categories=["test", "demo"],  # Type: list[str]
        ),
    )

    # Type-safe method calls
    config.get_all_tools()  # Returns List[str]

    logger.info("Type checking ensures:")
    logger.info("  - Correct configuration structure")
    logger.info("  - Valid parameter types")
    logger.info("  - IDE autocomplete support")
    logger.info("  - Early error detection")
    logger.info("\nConfiguration validated successfully!")


async def main():
    """Run all examples."""
    logger.info("=== Type-Safe MCP Integration Examples ===")

    await example_basic_mcp_config()
    await example_multiple_servers()
    await example_with_agent()
    await example_custom_server()
    await example_type_checking_benefits()

    logger.info("\n=== All Examples Complete ===")


if __name__ == "__main__":
    asyncio.run(main())
