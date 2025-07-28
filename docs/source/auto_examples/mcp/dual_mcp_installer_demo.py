#!/usr/bin/env python3
"""Dual MCP Installer Demo

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
    """Demo Version 1: Safe Pattern-Based Installer"""
    print("\n" + "=" * 80)
    print("🛡️  VERSION 1: SAFE PATTERN-BASED INSTALLER")
    print("=" * 80)
    print("Uses predefined patterns for trusted, predictable installations")

    # Initialize config manager
    config_manager = MCPConfigManager()

    # Initialize safe installer
    safe_installer = SafePatternInstaller(config_manager)

    print("\n📊 Installer Status:")
    status = safe_installer.get_status_summary()
    print(f"   Available Patterns: {', '.join(status['available_patterns'])}")
    print(f"   Config Directory: {config_manager.config_dir}")

    # Demo 1: Install filesystem server with human approval
    print("\n🔧 Demo 1: Installing Filesystem Server (with approval)")
    filesystem_request = InstallationRequest(
        server_name="demo_filesystem",
        package_name="@modelcontextprotocol/server-filesystem",
        pattern_type="filesystem",
        custom_args=["/tmp"],
        require_approval=True,  # Human approval required
    )

    # Create installation tool
    filesystem_tool = safe_installer.create_installation_tool(filesystem_request)
    print(f"   Created tool: {filesystem_tool.name}")
    print(f"   Description: {filesystem_tool.description}")
    print(
        f"   Human approval: {'✅ Required' if filesystem_request.require_approval else '❌ Not required'}"
    )

    # Demo 2: Install calculator (no approval needed - math is safe)
    print("\n🔧 Demo 2: Installing Calculator Server (no approval)")
    calculator_request = InstallationRequest(
        server_name="demo_calculator",
        package_name="@modelcontextprotocol/server-math",
        pattern_type="web_api",
        require_approval=False,  # Math operations are safe
    )

    calculator_tool = safe_installer.create_installation_tool(calculator_request)
    print(f"   Created tool: {calculator_tool.name}")
    print(
        f"   Human approval: {'✅ Required' if calculator_request.require_approval else '❌ Not required'}"
    )

    # Demo 3: Show quick install tools
    print("\n🚀 Demo 3: Quick Install Tools")
    quick_tools = safe_installer.create_quick_install_tools()
    for tool in quick_tools:
        print(f"   - {tool.name}: {tool.description}")

    # Demo 4: Configuration export
    print("\n📋 Demo 4: Configuration Management")

    # Simulate a configured server
    sample_config = config_manager.export_claude_desktop_config("demo_filesystem")
    if sample_config:
        print("   Claude Desktop Config Preview:")
        import json

        print(f"   {json.dumps(sample_config, indent=6)}")
    else:
        print("   No configuration found (server not installed yet)")

    print("\n✅ Safe Pattern Installer Demo Complete")
    print("   • Uses only trusted, predefined patterns")
    print("   • Human approval optional (configurable per server)")
    print("   • 90%+ success rate for standard MCP servers")
    print("   • Automatic .env and config file management")

    return safe_installer


async def demo_advanced_code_installer():
    """Demo Version 2: Advanced Code Generation Installer"""
    print("\n" + "=" * 80)
    print("🧠 VERSION 2: ADVANCED CODE GENERATION INSTALLER")
    print("=" * 80)
    print("Uses LLM agents to generate custom installation code")

    # Initialize advanced installer
    advanced_installer = AdvancedCodeInstaller()

    print("\n📊 Installer Status:")
    status = advanced_installer.get_advanced_status()
    print(f"   Type: {status['installer_type']}")
    print(
        f"   Human Approval: {'✅ Always Required' if status['human_approval_required'] else '❌ Optional'}"
    )
    print(
        f"   LLM Agent: {'✅ Available' if status['llm_agent_available'] else '⚠️  Mock Mode'}"
    )

    # Demo 1: Standard MCP server (will fallback to safe)
    print("\n🔧 Demo 1: Standard MCP Server (Smart Fallback)")
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
    print(f"   Success: {success}")
    print(f"   Message: {message}")
    print(f"   Tools Created: {len(tools)}")

    # Demo 2: Python package (requires code generation)
    print("\n🔧 Demo 2: Python Package (Code Generation)")
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
    print(f"   Success: {success}")
    print(f"   Message Summary: {message.split('Next Steps:')[0]}...")
    print(f"   Tools Created: {len(tools)}")
    for i, tool in enumerate(tools, 1):
        print(f"      {i}. {tool.name}")

    # Demo 3: High-risk installation (git repository)
    print("\n🔧 Demo 3: High-Risk Installation (Git Repo)")
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
    print(f"   Success: {success}")
    print(
        f"   Message: {message.split('Next Steps:')[0] if 'Next Steps:' in message else message}"
    )
    print(f"   Tools Created: {len(tools)}")

    print("\n✅ Advanced Code Installer Demo Complete")
    print("   • Uses LLM agents for custom installation logic")
    print("   • Human approval ALWAYS required for generated code")
    print("   • Smart fallback to safe patterns when possible")
    print("   • Risk assessment and tolerance checking")

    return advanced_installer


async def demo_human_approval_integration():
    """Demo the human approval workflow using interrupt_tool_wrapper"""
    print("\n" + "=" * 80)
    print("👤 HUMAN APPROVAL INTEGRATION DEMO")
    print("=" * 80)
    print("Shows how interrupt_tool_wrapper.py integrates with both installers")

    print("\n🔧 How Human Approval Works:")
    print(
        """
📋 Process Flow:
   1. User requests MCP server installation
   2. Installer creates tool with add_human_in_the_loop() wrapper
   3. Tool execution pauses for human review
   4. Human can:
      - ✅ Accept: Execute as planned
      - ✏️  Edit: Modify parameters before execution  
      - 💬 Respond: Provide custom response instead
   5. Tool executes with approved/modified parameters

🛡️  Safety Features:
   - All generated code reviewed before execution
   - Dangerous patterns automatically blocked
   - Risk assessment shown to human reviewer
   - Edit capability allows parameter adjustment
   - Custom response allows complete override

⚙️  Configuration Options:
   - Per-server approval requirements
   - Risk tolerance levels
   - Pattern-based auto-approval for safe operations
   - Environment variable secure storage
"""
    )

    print("\n📄 Example .env File Structure:")
    print(
        """
# ~/.haive/mcp/.env
DEMO_FILESYSTEM_ROOT_PATH=/tmp
DEMO_DATABASE_DATABASE_URL=postgresql://user:pass@localhost:5432/db  
DEMO_WEB_API_API_KEY=your_secure_api_key_here
DEMO_WEB_API_BASE_URL=https://api.example.com
"""
    )

    print("\n📊 Claude Desktop Integration:")
    print(
        """
{
  "mcpServers": {
    "demo_filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
      "env": {
        "ROOT_PATH": "/tmp"
      }
    }
  }
}
"""
    )


async def main():
    """Run the complete dual installer demo"""
    print("🚀 DUAL MCP INSTALLER SYSTEM DEMO")
    print("Showcasing both Safe Pattern and Advanced Code Generation approaches")

    try:
        # Demo safe pattern installer
        safe_installer = await demo_safe_pattern_installer()

        # Demo advanced code installer
        advanced_installer = await demo_advanced_code_installer()

        # Demo human approval integration
        await demo_human_approval_integration()

        print("\n" + "=" * 80)
        print("🎯 SUMMARY: CHOOSE YOUR INSTALLER")
        print("=" * 80)

        print(
            """
🛡️  SAFE PATTERN INSTALLER (Recommended):
   ✅ Use for: Standard MCP servers, production environments
   ✅ Benefits: Predictable, fast, reliable, minimal oversight
   ✅ Patterns: NPM (@modelcontextprotocol/*), Python (mcp-server-*)
   ⚠️  Limitation: Only works with known patterns

🧠 ADVANCED CODE INSTALLER (Expert Mode):
   ✅ Use for: Custom servers, experimental packages, special requirements
   ✅ Benefits: Flexible, handles any installation type, LLM-powered
   ⚠️  Requires: Human oversight, code review, higher risk tolerance
   ⚠️  Limitation: Slower, requires expert judgment

🔧 INTEGRATION OPTIONS:
   1. Safe-first: Try safe patterns, fallback to advanced
   2. Advanced-only: Full LLM generation with human approval
   3. Hybrid: Different installers for different server types

📊 CONFIGURATION MANAGEMENT:
   • Unified .env file handling
   • Claude Desktop config export
   • Cross-installer server registry
   • Secure credential storage
"""
        )

    finally:
        # Cleanup
        if "safe_installer" in locals():
            safe_installer.cleanup()
        if "advanced_installer" in locals():
            advanced_installer.cleanup()

    print("\n✅ Demo Complete! Both installers ready for use.")


if __name__ == "__main__":
    asyncio.run(main())
