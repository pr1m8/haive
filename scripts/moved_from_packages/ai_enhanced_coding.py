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
        # Use AI assistant for smart configuration
        smart_config = await self.assistant.auto_configure_for_task(
            task_description,
            prefer_simple_setup=True,
            max_servers=4,
            include_fallbacks=True,
        )

        # Display analysis results

        if smart_config.warnings:
            for _warning in smart_config.warnings:
                pass

        # Validate the configuration
        validation = await self.assistant.validate_configuration(smart_config.config)

        if validation["required_env_vars"]:
            pass

        if not validation["valid"]:
            for _issue in validation["issues"]:
                pass

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

        # Create MCP-enabled agent
        agent = MCPAgent(
            engine=self.base_engine,
            mcp_config=self.current_config.config,
            name="ai_enhanced_coding_agent",
        )

        # Initialize the agent
        await agent.setup()

        # Check status
        agent.get_mcp_status()

        self.current_agent = agent
        return agent

    async def demonstrate_capabilities(self):
        """Demonstrate the agent's enhanced capabilities."""
        if not self.current_agent:
            raise ValueError("No agent available. Create agent first.")

        # Get available capabilities
        status = self.current_agent.get_mcp_status()

        for _server in status["connected_servers"]:
            pass

        # Example: Try to use available tools
        for _tool_name in status["available_tools"][:5]:  # Show first 5
            pass

        if len(status["available_tools"]) > 5:
            pass

    def explain_server_choice(self, server_name: str):
        """Explain why a server was recommended."""
        explanation = self.assistant.explain_recommendation(server_name)

        if explanation["setup_requirements"]:
            pass

        if explanation["fallback_options"]:
            pass

    async def switch_task_context(self, new_task: str):
        """Switch to a new task context with different server configuration."""
        # Analyze new task
        await self.analyze_and_configure(new_task)

        # Create new agent if configuration changed
        new_agent = await self.create_enhanced_agent()

        return new_agent


async def demonstrate_scenarios():
    """Demonstrate various coding scenarios with intelligent server selection."""
    agent = AIEnhancedCodingAgent()

    # Scenario 1: Code Security Analysis

    security_task = "Analyze a GitHub repository for security vulnerabilities and code quality issues"

    analysis1 = await agent.analyze_and_configure(security_task)
    await agent.create_enhanced_agent()
    await agent.demonstrate_capabilities()

    # Explain key server choices
    if analysis1["config"].primary_servers:
        for server in analysis1["config"].primary_servers[:2]:
            agent.explain_server_choice(server)

    # Scenario 2: Data Analysis and Research

    research_task = (
        "Research academic papers about machine learning and analyze datasets"
    )

    await agent.switch_task_context(research_task)
    await agent.demonstrate_capabilities()

    # Scenario 3: Web Development with API Integration

    web_task = "Build a web application that fetches data from external APIs and manages user files"

    await agent.switch_task_context(web_task)
    await agent.demonstrate_capabilities()

    # Scenario 4: Content Creation and Management

    content_task = "Generate images and manage content in a documentation system with calendar integration"

    await agent.switch_task_context(content_task)
    await agent.demonstrate_capabilities()


async def demonstrate_filtering():
    """Demonstrate advanced filtering capabilities."""
    selector = MCPServerSelector()

    # Show available prefixes
    prefixes = selector.get_available_prefixes()
    for prefix in prefixes[:10]:  # Show first 10
        len(selector.filter_by_prefix(prefix))

    if len(prefixes) > 10:
        pass

    # Show filtering by official servers
    official_servers = selector.filter_by_prefix("modelcontextprotocol/")

    for server in official_servers[:8]:  # Show first 8
        metadata = server.get("metadata", {})
        metadata.get("name", "Unknown")
        metadata.get("category", "Unknown")

    # Show task-based recommendations

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
            recommendations[0]


async def main():
    """Main demonstration function."""
    try:
        # First demonstrate the filtering capabilities
        await demonstrate_filtering()

        # Then demonstrate the full scenarios
        await demonstrate_scenarios()

    except Exception:
        pass


if __name__ == "__main__":
    asyncio.run(main())
