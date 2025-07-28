"""Example demonstrating DynamicToolDiscoverySupervisor capabilities.

This example shows how the supervisor can:
1. Discover tools dynamically from multiple sources
2. Distribute tools to appropriate agents
3. Route tasks based on available tools and agent capabilities
"""

import asyncio
import os
import tempfile
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent
from haive.agents.supervisor.dynamic_tool_discovery_supervisor import (
    DynamicToolDiscoverySupervisor,
    ToolDiscoveryMode,
)


# Create some sample tools that can be discovered
@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions.

    Args:
        expression: Mathematical expression to evaluate

    Returns:
        Result of the calculation
    """
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {e!s}"


@tool
def text_analyzer(text: str) -> dict[str, Any]:
    """Analyze text for various metrics.

    Args:
        text: Text to analyze

    Returns:
        Dictionary with analysis results
    """
    words = text.split()
    return {
        "word_count": len(words),
        "character_count": len(text),
        "average_word_length": (
            sum(len(word) for word in words) / len(words) if words else 0
        ),
        "unique_words": len(set(words)),
    }


@tool
def web_search(query: str) -> str:
    """Simulate web search functionality.

    Args:
        query: Search query

    Returns:
        Simulated search results
    """
    return f"Search results for '{query}': Found 10 relevant articles about {query}"


async def basic_supervisor_example():
    """Basic example of DynamicToolDiscoverySupervisor."""
    # Configure LLM
    config = AugLLMConfig(temperature=0.1)

    # Create agents
    agents = {
        "analyzer": SimpleAgent(name="analyzer", engine=config),
        "executor": ReactAgent(name="executor", engine=config, tools=[]),
    }

    # Create supervisor with initial tools
    supervisor = DynamicToolDiscoverySupervisor(
        name="tool_supervisor",
        agents=agents,
        engine=config,
        tools_to_register=[
            {
                "name": "calculator",
                "description": "Calculate mathematical expressions",
                "func": calculator.func,
            }
        ],
    )

    # Run task that needs tool discovery
    await supervisor.arun(
        "I need to calculate 25 * 4 and analyze the word 'supervisor'"
    )

    # Check discovered tools


async def factory_method_example():
    """Example using factory method with discovery sources."""
    config = AugLLMConfig(temperature=0.1)

    # Create temporary directory with tool documentation
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create tool documentation
        tool_doc_path = os.path.join(temp_dir, "available_tools.md")
        with open(tool_doc_path, "w") as f:
            f.write(
                """# Available Tools Documentation

## Mathematical Tools

### Calculator
- Function: calculator(expression: str) -> float
- Description: Evaluates mathematical expressions
- Example: calculator("2 + 2") returns 4

### Statistics Calculator
- Function: stats_calc(numbers: List[float]) -> Dict
- Description: Calculate statistics (mean, median, std dev)
- Example: stats_calc([1, 2, 3, 4, 5]) returns statistics

## Text Processing Tools

### Text Analyzer
- Function: text_analyzer(text: str) -> Dict
- Description: Analyzes text for various metrics
- Returns: word count, character count, unique words

### Sentiment Analyzer
- Function: sentiment_analyze(text: str) -> str
- Description: Analyzes sentiment of text
- Returns: positive, negative, or neutral

## Web Tools

### Web Search
- Function: web_search(query: str) -> List[str]
- Description: Search the web for information
- Returns: List of relevant results

### URL Scraper
- Function: scrape_url(url: str) -> str
- Description: Extract content from a URL
- Returns: Cleaned text content
"""
            )

        # Create supervisor with discovery configuration
        supervisor = DynamicToolDiscoverySupervisor.create_with_discovery(
            name="discovery_supervisor",
            agents={
                "researcher": SimpleAgent(name="researcher", engine=config),
                "analyst": ReactAgent(name="analyst", engine=config, tools=[]),
                "reporter": SimpleAgent(name="reporter", engine=config),
            },
            engine=config,
            discovery_mode=ToolDiscoveryMode.HYBRID,
            rag_documents_path=temp_dir,
            component_discovery_config={
                "registry_path": "./components",
                "scan_packages": ["haive.tools"],
            },
        )

        # Run task requiring tool discovery
        await supervisor.arun(
            "Research the latest Python features, analyze their impact, and create a summary report"
        )

        # Show tool discovery process
        if supervisor.discovered_tools:
            for _tool_name in supervisor.discovered_tools:
                pass


async def multi_agent_tool_routing_example():
    """Example showing how supervisor routes based on tool availability."""
    config = AugLLMConfig(temperature=0.1)

    # Create specialized agents
    agent_configs = [
        {"type": "ReactAgent", "name": "math_specialist", "tools": [calculator]},
        {"type": "ReactAgent", "name": "text_specialist", "tools": [text_analyzer]},
        {"type": "SimpleAgent", "name": "general_assistant"},
    ]

    # Create supervisor with agents and tools
    supervisor = DynamicToolDiscoverySupervisor.create_with_agents_and_tools(
        name="routing_supervisor",
        agent_configs=agent_configs,
        engine=config,
        initial_tools=[web_search],
        discovery_mode=ToolDiscoveryMode.COMPONENT_DISCOVERY,
    )

    for _agent_name, agent in supervisor.agents.items():
        if hasattr(agent, "tools") and agent.tools:
            [t.name for t in agent.tools]

    # Test routing for different tasks
    tasks = [
        "Calculate the compound interest on $1000 at 5% for 10 years",
        "Analyze this text: 'The quick brown fox jumps over the lazy dog'",
        "Search for information about quantum computing",
    ]

    for task in tasks:

        # Simulate decision making
        from haive.agents.supervisor.types import SupervisorState

        state = SupervisorState(
            messages=[HumanMessage(content=task)], next_agent="", agent_outputs={}
        )

        await supervisor._make_decision(state)


async def dynamic_tool_loading_example():
    """Example showing dynamic tool loading during execution."""
    config = AugLLMConfig(temperature=0.1)

    # Start with minimal tools
    supervisor = DynamicToolDiscoverySupervisor(
        name="dynamic_loader",
        agents={"worker": ReactAgent(name="worker", engine=config, tools=[])},
        engine=config,
        discovery_mode=ToolDiscoveryMode.HYBRID,
    )

    # Simulate tool discovery
    discovery_tool = supervisor.tool_registry.get("discover_and_load_tools")

    # Discover tools for math
    discovery_tool.func("I need to perform complex mathematical calculations")

    # Discover tools for text
    discovery_tool.func("I need to analyze and process text documents")

    # Show final tool registry


async def performance_monitoring_example():
    """Example showing supervisor performance monitoring."""
    config = AugLLMConfig(temperature=0.1)

    # Create supervisor with multiple agents
    supervisor = DynamicToolDiscoverySupervisor(
        name="monitoring_supervisor",
        agents={
            "fast_agent": SimpleAgent(name="fast_agent", engine=config),
            "slow_agent": SimpleAgent(name="slow_agent", engine=config),
            "reliable_agent": ReactAgent(
                name="reliable_agent", engine=config, tools=[calculator]
            ),
        },
        engine=config,
        max_discovery_attempts=3,
    )

    # Run several tasks
    tasks = [
        "What is 2 + 2?",
        "Calculate 15 * 23",
        "Tell me a fact",
        "What's the weather like?",
        "Compute the factorial of 5",
    ]

    for _i, task in enumerate(tasks):
        await supervisor.arun(task)

    # Show routing history
    if hasattr(supervisor.state, "routing_history"):
        for _route in supervisor.state.get("routing_history", []):
            pass


async def main():
    """Run all examples."""
    await basic_supervisor_example()
    await factory_method_example()
    await multi_agent_tool_routing_example()
    await dynamic_tool_loading_example()
    await performance_monitoring_example()


if __name__ == "__main__":

    # Run examples
    asyncio.run(main())
