#!/usr/bin/env python3
"""Demonstration of procedural MCP server addition.

This script demonstrates how to use the MCPManager to add MCP servers
one by one during runtime, as requested: "add all mcps procueduely one by obne".

The script shows:
    - Step-by-step server addition
    - Health monitoring
    - Tool discovery
    - Error handling
    - Status reporting

Run with:
    poetry run python examples/procedural_mcp_addition.py
"""

import asyncio
import logging
from pathlib import Path

from haive.mcp.config import MCPServerConfig, MCPTransport
from haive.mcp.manager import MCPManager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def demonstrate_procedural_mcp_addition():
    """Demonstrate adding MCP servers one by one procedurally."""
    # Create manager
    manager = MCPManager(
        auto_health_check=True, health_check_interval=15.0, max_retry_attempts=2
    )

    # Define servers to add procedurally
    servers_to_add = [
        {
            "name": "filesystem",
            "config": MCPServerConfig(
                name="filesystem",
                transport=MCPTransport.STDIO,
                command="npx",
                args=["-y", "@modelcontextprotocol/server-filesystem"],
                env={"FILESYSTEM_ROOT": str(Path.home() / "tmp")},
                capabilities=[
                    "read_file",
                    "write_file",
                    "list_directory",
                    "create_directory",
                ],
                category="filesystem",
                description="Local filesystem operations via MCP",
            ),
        },
        {
            "name": "github",
            "config": MCPServerConfig(
                name="github",
                transport=MCPTransport.STDIO,
                command="npx",
                args=["-y", "@modelcontextprotocol/server-github"],
                env={"GITHUB_TOKEN": "your_github_token_here"},
                capabilities=["repo_access", "issue_management", "pr_operations"],
                category="development",
                description="GitHub repository operations via MCP",
            ),
        },
        {
            "name": "sqlite",
            "config": MCPServerConfig(
                name="sqlite",
                transport=MCPTransport.STDIO,
                command="npx",
                args=["-y", "@modelcontextprotocol/server-sqlite"],
                capabilities=["database_query", "schema_inspect", "data_analysis"],
                category="database",
                description="SQLite database operations via MCP",
            ),
        },
        {
            "name": "brave_search",
            "config": MCPServerConfig(
                name="brave_search",
                transport=MCPTransport.STDIO,
                command="npx",
                args=["-y", "@modelcontextprotocol/server-brave-search"],
                env={"BRAVE_API_KEY": "your_brave_api_key_here"},
                capabilities=["web_search", "search_results", "content_discovery"],
                category="search",
                description="Web search via Brave Search API",
            ),
        },
        {
            "name": "puppeteer",
            "config": MCPServerConfig(
                name="puppeteer",
                transport=MCPTransport.STDIO,
                command="npx",
                args=["-y", "@modelcontextprotocol/server-puppeteer"],
                capabilities=[
                    "web_scraping",
                    "screenshot",
                    "pdf_generation",
                    "automation",
                ],
                category="web",
                description="Web automation and scraping via Puppeteer",
            ),
        },
    ]

    # Add servers one by one
    successful_additions = []
    failed_additions = []

    for i, server_info in enumerate(servers_to_add, 1):
        name = server_info["name"]
        config = server_info["config"]

        try:
            # Add server with immediate connection attempt
            result = await manager.add_server(name, config, connect_immediately=True)

            if result.success:
                if result.connection_time:
                    pass
                successful_additions.append(name)
            else:
                failed_additions.append((name, result.error_message))

        except Exception as e:
            failed_additions.append((name, str(e)))

        # Brief pause between additions (simulate real-world usage)
        if i < len(servers_to_add):
            await asyncio.sleep(2)

    # Summary report
    for name in successful_additions:
        pass

    for name, _error in failed_additions:
        pass

    # Get overall status
    status = manager.get_all_server_status()

    # Show detailed server status
    if status["servers"]:
        for _server_name, server_info in status["servers"].items():
            "✅" if server_info["status"] == "connected" else "❌"
            if server_info["tools"]:
                pass

    # Demonstrate tool usage if any servers connected
    all_tools = await manager.get_all_tools()
    if all_tools:
        for _tool in all_tools[:5]:  # Show first 5 tools
            pass
        if len(all_tools) > 5:
            pass

        # Try calling a simple tool if available
        if len(all_tools) > 0:
            all_tools[0]
            try:
                # This would fail for most tools without proper arguments
                # but demonstrates the interface
                pass
            except Exception:
                pass

    # Demonstrate retry functionality
    if failed_additions:
        retry_results = await manager.retry_failed_servers()

        successful_retries = [r for r in retry_results if r.success]
        for result in successful_retries:
            pass

    # Health monitoring demonstration

    if manager.auto_health_check:
        await asyncio.sleep(5)

        # Check health status
        updated_status = manager.get_all_server_status()
        updated_status["summary"]["connected_servers"]

    # Final summary

    # Cleanup
    await manager.shutdown()


async def demonstrate_dynamic_server_management():
    """Demonstrate dynamic server management capabilities."""
    manager = MCPManager(auto_health_check=False)  # Disable for this demo

    # Add a server
    config = MCPServerConfig(
        name="demo_server",
        transport=MCPTransport.STDIO,
        command="echo",
        args=["Hello MCP"],
        capabilities=["demo"],
    )

    await manager.add_server("demo_server", config)

    # Check status
    manager.get_server_status("demo_server")

    # Remove server
    await manager.remove_server("demo_server")

    # Verify removal
    manager.get_server_status("demo_server")

    await manager.shutdown()


if __name__ == "__main__":
    try:
        # Run main demonstration
        asyncio.run(demonstrate_procedural_mcp_addition())

        # Run additional dynamic management demo
        asyncio.run(demonstrate_dynamic_server_management())

    except KeyboardInterrupt:
        pass
    except Exception:
        logger.exception("Demo failed")
