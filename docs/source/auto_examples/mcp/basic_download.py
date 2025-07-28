#!/usr/bin/env python3
"""Basic example of downloading MCP servers.

This example shows the simplest way to download and install MCP servers.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.haive.mcp.downloader import GeneralMCPDownloader


async def download_basic_servers():
    """Download essential MCP servers."""
    # Create downloader with default configuration
    downloader = GeneralMCPDownloader()

    print("🚀 Downloading basic MCP servers...")
    print("-" * 50)

    # Download specific servers
    servers_to_install = ["filesystem", "sqlite"]

    result = await downloader.download_servers(
        server_names=servers_to_install, max_concurrent=2
    )

    # Show results
    print(f"\n✅ Successfully installed: {result['successful']}")
    print(f"❌ Failed: {result['failed']}")
    print(f"📊 Success rate: {result['success_rate']:.1f}%")

    # Show configuration file location
    print(f"\n📋 Configuration saved to: {result['config_file']}")

    # Show failed servers if any
    if result["failed_servers"]:
        print("\n❌ Failed installations:")
        for failure in result["failed_servers"]:
            print(f"  - {failure['server']}: {failure['error']}")

    return result


async def download_by_category():
    """Download servers by category."""
    downloader = GeneralMCPDownloader()

    print("\n🏷️  Downloading official servers...")
    print("-" * 50)

    # Download all official servers
    result = await downloader.download_servers(
        categories=["official"], max_concurrent=3
    )

    print(f"\n✅ Installed {result['successful']} official servers")

    return result


async def auto_discover_and_install():
    """Auto-discover and install servers."""
    downloader = GeneralMCPDownloader()

    print("\n🔍 Auto-discovering MCP servers...")
    print("-" * 50)

    # Discover and install up to 5 servers
    result = await downloader.auto_discover_and_download(limit=5)

    print(f"\n✅ Discovered and installed {result['successful']} servers")

    return result


async def main():
    """Run all examples."""
    print("MCP Server Download Examples")
    print("=" * 50)

    # Example 1: Download specific servers
    await download_basic_servers()

    # Example 2: Download by category
    # await download_by_category()

    # Example 3: Auto-discover
    # await auto_discover_and_install()

    print("\n✨ Examples complete!")


if __name__ == "__main__":
    asyncio.run(main())
