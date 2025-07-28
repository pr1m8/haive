#!/usr/bin/env python3
"""Example: AI-enhanced coding workflow with intelligent MCP server selection.

This example demonstrates how an AI agent can use the intelligent MCP server
selection tools to automatically configure itself for various coding tasks.
The agent analyzes tasks and dynamically selects the most appropriate servers.

Usage:
    python ai_enhanced_coding.py
"""

import asyncio
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import LLMConfig

from haive.mcp.agents import MCPAgent

# Import the haive MCP tools
from haive.mcp.tools import MCPAssistant, MCPServerSelector


class AIEnhancedCodingAgent:
    """An AI agent that enhances its capabilities based on coding tasks."""

    def __init__(self):
        """Initialize the enhanced coding agent."""
        self.assistant = MCPAssistant(cache_enabled=True)
        self.selector = MCPServerSelector()
        self.current_config = None
        self.current_agent = None

        # Create base engine configuration
        self.base_engine = AugLLMConfig(
            llm_config=LLMConfig(provider="openai", model="gpt-4o-mini"),
            name="ai_enhanced_engine",
        )

    async def analyze_and_configure(self, task_description: str) -> dict[str, Any]:
        """Analyze a task and automatically configure MCP servers.

        Args:
            task_description: Natural language description of the coding task

        Returns:
            Dictionary with configuration details and analysis
        """
        print(f"🔍 Analyzing task: '{task_description}'")
        print("=" * 60)

        # Use AI assistant for smart configuration
        smart_config = await self.assistant.auto_configure_for_task(
            task_description,
            prefer_simple_setup=True,
            max_servers=4,
            include_fallbacks=True,
        )

        # Display analysis results
        print("💭 Task Analysis:")
        print(f"   Detected pattern: {smart_config.reasoning}")
        print(f"   Setup complexity: {smart_config.setup_complexity}")
        print(f"   Primary servers: {len(smart_config.primary_servers)}")

        if smart_config.warnings:
            print("⚠️  Warnings:")
            for warning in smart_config.warnings:
                print(f"   - {warning}")

        # Validate the configuration
        validation = await self.assistant.validate_configuration(smart_config.config)

        print("\n✅ Configuration Validation:")
        print(f"   Valid: {'Yes' if validation['valid'] else 'No'}")
        print(f"   Setup time: ~{validation['estimated_setup_time']}s")

        if validation["required_env_vars"]:
            print(
                f"   Required env vars: {', '.join(set(validation['required_env_vars']))}"
            )

        if not validation["valid"]:
            print("❌ Issues found:")
            for issue in validation["issues"]:
                print(f"   - {issue}")

        # Store current configuration
        self.current_config = smart_config

        return {
            "config": smart_config,
            "validation": validation,
            "reasoning": self.assistant.get_selection_reasoning(),
        }

    async def create_enhanced_agent(self) -> MCPAgent:
        """Create an MCP agent with the current configuration."""
        if not self.current_config:
            raise ValueError(
                "No configuration available. Run analyze_and_configure first."
            )

        print("\n🤖 Creating enhanced agent...")

        # Create MCP-enabled agent
        agent = MCPAgent(
            engine=self.base_engine,
            mcp_config=self.current_config.config,
            name="ai_enhanced_coding_agent",
        )

        # Initialize the agent
        await agent.setup()

        # Check status
        status = agent.get_mcp_status()
        print(f"   Connected servers: {', '.join(status['connected_servers'])}")
        print(f"   Available tools: {status['tool_count']}")

        self.current_agent = agent
        return agent

    async def demonstrate_capabilities(self):
        """Demonstrate the agent's enhanced capabilities."""
        if not self.current_agent:
            raise ValueError("No agent available. Create agent first.")

        print("\n🚀 Demonstrating enhanced capabilities...")

        # Get available capabilities
        status = self.current_agent.get_mcp_status()

        print("📊 Available Resources:")
        print(f"   MCP Tools: {status['tool_count']}")
        print(f"   Connected Servers: {len(status['connected_servers'])}")

        for server in status["connected_servers"]:
            print(f"   - {server}")

        # Example: Try to use available tools
        print("\n🔧 Available MCP Tools:")
        for tool_name in status["available_tools"][:5]:  # Show first 5
            print(f"   - {tool_name}")

        if len(status["available_tools"]) > 5:
            print(f"   ... and {len(status['available_tools']) - 5} more")

    def explain_server_choice(self, server_name: str):
        """Explain why a server was recommended."""
        explanation = self.assistant.explain_recommendation(server_name)

        print(f"\n📖 Explanation for {server_name}:")
        print(f"   Profile: {explanation.get('profile', {})}")
        print(f"   Setup time: ~{explanation['estimated_setup_time']}s")
        print(f"   Use cases: {', '.join(explanation['common_use_cases'])}")

        if explanation["setup_requirements"]:
            print(
                f"   Setup requirements: {', '.join(explanation['setup_requirements'])}"
            )

        if explanation["fallback_options"]:
            print(f"   Fallback options: {', '.join(explanation['fallback_options'])}")

    async def switch_task_context(self, new_task: str):
        """Switch to a new task context with different server configuration."""
        print("\n🔄 Switching to new task context...")

        # Analyze new task
        await self.analyze_and_configure(new_task)

        # Create new agent if configuration changed
        new_agent = await self.create_enhanced_agent()

        print(f"✅ Successfully switched to new configuration for: '{new_task}'")
        return new_agent


async def demonstrate_scenarios():
    """Demonstrate various coding scenarios with intelligent server selection."""
    agent = AIEnhancedCodingAgent()

    # Scenario 1: Code Security Analysis
    print("🎯 SCENARIO 1: Code Security Analysis")
    print("=" * 80)

    security_task = "Analyze a GitHub repository for security vulnerabilities and code quality issues"

    analysis1 = await agent.analyze_and_configure(security_task)
    await agent.create_enhanced_agent()
    await agent.demonstrate_capabilities()

    # Explain key server choices
    if analysis1["config"].primary_servers:
        for server in analysis1["config"].primary_servers[:2]:
            agent.explain_server_choice(server)

    print("\n" + "=" * 80)

    # Scenario 2: Data Analysis and Research
    print("🎯 SCENARIO 2: Data Analysis and Research")
    print("=" * 80)

    research_task = (
        "Research academic papers about machine learning and analyze datasets"
    )

    await agent.switch_task_context(research_task)
    await agent.demonstrate_capabilities()

    print("\n" + "=" * 80)

    # Scenario 3: Web Development with API Integration
    print("🎯 SCENARIO 3: Web Development with API Integration")
    print("=" * 80)

    web_task = "Build a web application that fetches data from external APIs and manages user files"

    await agent.switch_task_context(web_task)
    await agent.demonstrate_capabilities()

    print("\n" + "=" * 80)

    # Scenario 4: Content Creation and Management
    print("🎯 SCENARIO 4: Content Creation and Management")
    print("=" * 80)

    content_task = "Generate images and manage content in a documentation system with calendar integration"

    await agent.switch_task_context(content_task)
    await agent.demonstrate_capabilities()


async def demonstrate_filtering():
    """Demonstrate advanced filtering capabilities."""
    print("\n🔍 ADVANCED FILTERING DEMO")
    print("=" * 50)

    selector = MCPServerSelector()

    # Show available prefixes
    prefixes = selector.get_available_prefixes()
    print(f"📦 Available prefixes ({len(prefixes)}):")
    for prefix in prefixes[:10]:  # Show first 10
        count = len(selector.filter_by_prefix(prefix))
        print(f"   {prefix} ({count} servers)")

    if len(prefixes) > 10:
        print(f"   ... and {len(prefixes) - 10} more")

    # Show filtering by official servers
    official_servers = selector.filter_by_prefix("modelcontextprotocol/")
    print(f"\n🏢 Official ModelContextProtocol servers ({len(official_servers)}):")

    for server in official_servers[:8]:  # Show first 8
        metadata = server.get("metadata", {})
        name = metadata.get("name", "Unknown")
        category = metadata.get("category", "Unknown")
        print(f"   {name.split('/')[-1]} ({category})")

    # Show task-based recommendations
    print("\n🎯 Task-based Recommendations:")

    sample_tasks = [
        "work with files and directories",
        "access GitHub repositories",
        "search the web for information",
        "manage database queries",
        "handle calendar and scheduling",
    ]

    for task in sample_tasks:
        recommendations = selector.recommend_for_task(task, max_servers=2)
        if recommendations:
            top_rec = recommendations[0]
            print(f"   '{task}' → {top_rec.server_name} (score: {top_rec.score:.1f})")


async def main():
    """Main demonstration function."""
    print("🚀 AI-Enhanced Coding with Intelligent MCP Server Selection")
    print("=" * 80)
    print("This demo shows how AI agents can automatically select and configure")
    print("MCP servers based on task analysis for enhanced coding capabilities.")
    print("=" * 80)

    try:
        # First demonstrate the filtering capabilities
        await demonstrate_filtering()

        print("\n\n")

        # Then demonstrate the full scenarios
        await demonstrate_scenarios()

        print("\n✅ Demo completed successfully!")
        print("\nKey benefits demonstrated:")
        print("  • Automatic server selection based on task analysis")
        print("  • Intelligent configuration with validation")
        print("  • Dynamic capability switching for different tasks")
        print("  • Fallback strategies for robust operation")
        print("  • Detailed reasoning and explanations")

    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("Note: This demo requires the full haive-mcp package to be installed")
        print("and may need environment variables for some MCP servers.")


if __name__ == "__main__":
    asyncio.run(main())
