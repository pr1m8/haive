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
    print("🚀 Starting Procedural MCP Server Addition Demo")
    print("=" * 50)

    # Create manager
    manager = MCPManager(
        auto_health_check=True, health_check_interval=15.0, max_retry_attempts=2
    )

    print(
        f"✅ Created MCPManager with health monitoring every {manager.health_check_interval}s"
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

    print(f"📋 Planning to add {len(servers_to_add)} MCP servers procedurally")
    print()

    # Add servers one by one
    successful_additions = []
    failed_additions = []

    for i, server_info in enumerate(servers_to_add, 1):
        name = server_info["name"]
        config = server_info["config"]

        print(f"🔄 [{i}/{len(servers_to_add)}] Adding server: {name}")
        print(f"   Category: {config.category}")
        print(f"   Transport: {config.transport}")
        print(f"   Command: {config.command} {' '.join(config.args or [])}")
        print(f"   Capabilities: {', '.join(config.capabilities)}")

        try:
            # Add server with immediate connection attempt
            result = await manager.add_server(name, config, connect_immediately=True)

            if result.success:
                print(f"   ✅ Successfully added! Status: {result.status}")
                print(
                    f"   🔧 Discovered {result.tools_count} tools: {', '.join(result.tools[:3])}{'...' if len(result.tools) > 3 else ''}"
                )
                if result.connection_time:
                    print(f"   ⏱️  Connection time: {result.connection_time:.2f}s")
                successful_additions.append(name)
            else:
                print(f"   ❌ Failed to add: {result.error_message}")
                print(f"   Status: {result.status}")
                failed_additions.append((name, result.error_message))

        except Exception as e:
            print(f"   💥 Exception occurred: {e}")
            failed_additions.append((name, str(e)))

        print()

        # Brief pause between additions (simulate real-world usage)
        if i < len(servers_to_add):
            print("   ⏳ Waiting 2 seconds before next addition...")
            await asyncio.sleep(2)
            print()

    # Summary report
    print("📊 Procedural Addition Summary")
    print("=" * 30)
    print(f"✅ Successful: {len(successful_additions)} servers")
    for name in successful_additions:
        print(f"   • {name}")

    print(f"❌ Failed: {len(failed_additions)} servers")
    for name, error in failed_additions:
        print(f"   • {name}: {error}")

    print()

    # Get overall status
    status = manager.get_all_server_status()
    print("🌐 Overall Manager Status")
    print("=" * 25)
    print(f"Total servers: {status['summary']['total_servers']}")
    print(f"Connected: {status['summary']['connected_servers']}")
    print(f"Failed: {status['summary']['failed_servers']}")
    print(f"Total tools available: {status['summary']['total_tools']}")

    # Show detailed server status
    if status["servers"]:
        print("\n📋 Detailed Server Status")
        print("-" * 25)
        for server_name, server_info in status["servers"].items():
            status_emoji = "✅" if server_info["status"] == "connected" else "❌"
            print(f"{status_emoji} {server_name}: {server_info['status']}")
            if server_info["tools"]:
                print(
                    f"   Tools: {', '.join(server_info['tools'][:3])}{'...' if len(server_info['tools']) > 3 else ''}"
                )

    # Demonstrate tool usage if any servers connected
    all_tools = await manager.get_all_tools()
    if all_tools:
        print(f"\n🔧 Available Tools ({len(all_tools)} total)")
        print("-" * 20)
        for tool in all_tools[:5]:  # Show first 5 tools
            print(f"• {tool.name}: {getattr(tool, 'description', 'No description')}")
        if len(all_tools) > 5:
            print(f"... and {len(all_tools) - 5} more tools")

        # Try calling a simple tool if available
        if len(all_tools) > 0:
            sample_tool = all_tools[0]
            print(f"\n🧪 Testing tool: {sample_tool.name}")
            try:
                # This would fail for most tools without proper arguments
                # but demonstrates the interface
                print(
                    f"   Tool signature: {getattr(sample_tool, 'args_schema', 'No schema available')}"
                )
            except Exception as e:
                print(f"   Tool inspection failed: {e}")

    # Demonstrate retry functionality
    if failed_additions:
        print(f"\n🔄 Attempting to retry {len(failed_additions)} failed servers...")
        retry_results = await manager.retry_failed_servers()

        successful_retries = [r for r in retry_results if r.success]
        print(f"   ✅ Retry successes: {len(successful_retries)}")
        for result in successful_retries:
            print(f"     • {result.server_name}: {result.tools_count} tools")

    # Health monitoring demonstration
    print("\n❤️  Health Monitoring")
    print("-" * 18)
    print(
        f"Auto health checks: {'enabled' if manager.auto_health_check else 'disabled'}"
    )
    print(f"Check interval: {manager.health_check_interval}s")

    if manager.auto_health_check:
        print("   Waiting 5 seconds to observe health monitoring...")
        await asyncio.sleep(5)

        # Check health status
        updated_status = manager.get_all_server_status()
        connected_count = updated_status["summary"]["connected_servers"]
        print(f"   Current connected servers: {connected_count}")

    # Final summary
    print("\n🎯 Demo Complete!")
    print("=" * 15)
    print("This demo showed:")
    print("• ✅ Procedural server addition (one by one)")
    print("• 🔧 Automatic tool discovery")
    print("• ❤️  Health monitoring")
    print("• 🔄 Retry logic for failed servers")
    print("• 📊 Status reporting and management")
    print("• 🧪 Tool enumeration and inspection")

    # Cleanup
    print("\n🧹 Shutting down manager...")
    await manager.shutdown()
    print("   Manager shutdown complete.")


async def demonstrate_dynamic_server_management():
    """Demonstrate dynamic server management capabilities."""
    print("\n" + "=" * 50)
    print("🔄 Dynamic Server Management Demo")
    print("=" * 50)

    manager = MCPManager(auto_health_check=False)  # Disable for this demo

    # Add a server
    config = MCPServerConfig(
        name="demo_server",
        transport=MCPTransport.STDIO,
        command="echo",
        args=["Hello MCP"],
        capabilities=["demo"],
    )

    print("➕ Adding demo server...")
    result = await manager.add_server("demo_server", config)
    print(f"   Result: {result.success}, Status: {result.status}")

    # Check status
    status = manager.get_server_status("demo_server")
    print(f"   Server status: {status}")

    # Remove server
    print("➖ Removing demo server...")
    removed = await manager.remove_server("demo_server")
    print(f"   Removed: {removed}")

    # Verify removal
    status_after = manager.get_server_status("demo_server")
    print(f"   Status after removal: {status_after}")

    await manager.shutdown()


if __name__ == "__main__":
    print("🎬 MCP Procedural Addition Demonstration")
    print("This script demonstrates adding MCP servers one by one")
    print("as requested: 'add all mcps procueduely one by obne'")
    print()

    try:
        # Run main demonstration
        asyncio.run(demonstrate_procedural_mcp_addition())

        # Run additional dynamic management demo
        asyncio.run(demonstrate_dynamic_server_management())

    except KeyboardInterrupt:
        print("\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n💥 Demo failed with error: {e}")
        logger.exception("Demo failed")

    print("\n👋 Demo finished!")
