#!/usr/bin/env python3
"""Dual MCP Installer Demo.

Shows both Version 1 (Safe Pattern) and Version 2 (Advanced Code Generation) installers.
Both support human approval via interrupt_tool_wrapper.py integration.
"""

import asyncio

# Import our new installer system
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from haive.mcp.installers import (
    AdvancedCodeInstaller,
    MCPConfigManager,
    SafePatternInstaller,
)
from haive.mcp.installers.advanced_code_installer import CodeGenerationRequest
from haive.mcp.installers.safe_pattern_installer import InstallationRequest


async def demo_safe_pattern_installer():
    """Demo Version 1: Safe Pattern-Based Installer."""
    # Initialize config manager
    config_manager = MCPConfigManager()

    # Initialize safe installer
    safe_installer = SafePatternInstaller(config_manager)

    safe_installer.get_status_summary()

    # Demo 1: Install filesystem server with human approval
    filesystem_request = InstallationRequest(
        server_name="demo_filesystem",
        package_name="@modelcontextprotocol/server-filesystem",
        pattern_type="filesystem",
        custom_args=["/tmp"],
        require_approval=True,  # Human approval required
    )

    # Create installation tool
    safe_installer.create_installation_tool(filesystem_request)

    # Demo 2: Install calculator (no approval needed - math is safe)
    calculator_request = InstallationRequest(
        server_name="demo_calculator",
        package_name="@modelcontextprotocol/server-math",
        pattern_type="web_api",
        require_approval=False,  # Math operations are safe
    )

    safe_installer.create_installation_tool(calculator_request)

    # Demo 3: Show quick install tools
    quick_tools = safe_installer.create_quick_install_tools()
    for _tool in quick_tools:
        pass

    # Demo 4: Configuration export

    # Simulate a configured server
    sample_config = config_manager.export_claude_desktop_config("demo_filesystem")
    if sample_config:
        pass

    else:
        pass

    return safe_installer


async def demo_advanced_code_installer():
    """Demo Version 2: Advanced Code Generation Installer."""
    # Initialize advanced installer
    advanced_installer = AdvancedCodeInstaller()

    advanced_installer.get_advanced_status()

    # Demo 1: Standard MCP server (will fallback to safe)
    standard_request = CodeGenerationRequest(
        server_name="advanced_filesystem",
        server_description="Official MCP filesystem server for file operations",
        package_info={
            "name": "@modelcontextprotocol/server-filesystem",
            "repo": "https://github.com/modelcontextprotocol/servers",
            "type": "npm",
        },
        risk_tolerance="low",
    )

    success, message, tools = await advanced_installer.install_server_advanced(
        standard_request
    )

    # Demo 2: Python package (requires code generation)
    python_request = CodeGenerationRequest(
        server_name="custom_python_server",
        server_description="Custom Python-based MCP server for data processing",
        package_info={
            "name": "mcp-data-processor",
            "type": "python",
            "repo": "https://github.com/example/mcp-data-processor",
        },
        custom_requirements="Requires pandas and numpy dependencies",
        risk_tolerance="medium",
    )

    success, message, tools = await advanced_installer.install_server_advanced(
        python_request
    )
    for _i, _tool in enumerate(tools, 1):
        pass

    # Demo 3: High-risk installation (git repository)
    git_request = CodeGenerationRequest(
        server_name="experimental_server",
        server_description="Experimental MCP server from third-party repository",
        package_info={
            "name": "experimental-mcp-server",
            "repo": "https://github.com/thirdparty/experimental-mcp",
            "type": "git",
        },
        risk_tolerance="low",  # Low tolerance with high risk
    )

    success, message, tools = await advanced_installer.install_server_advanced(
        git_request
    )

    return advanced_installer


async def demo_human_approval_integration():
    """Demo the human approval workflow using interrupt_tool_wrapper."""


async def main():
    """Run the complete dual installer demo."""
    try:
        # Demo safe pattern installer
        safe_installer = await demo_safe_pattern_installer()

        # Demo advanced code installer
        advanced_installer = await demo_advanced_code_installer()

        # Demo human approval integration
        await demo_human_approval_integration()

    finally:
        # Cleanup
        if "safe_installer" in locals():
            safe_installer.cleanup()
        if "advanced_installer" in locals():
            advanced_installer.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
