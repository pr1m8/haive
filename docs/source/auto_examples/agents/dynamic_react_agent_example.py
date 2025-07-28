#!/usr/bin/env python3
"""Example: DynamicReactAgent with Dynamic Tool Discovery.

This example demonstrates the DynamicReactAgent's ability to:
1. Start with basic tools
2. Discover and load new tools dynamically
3. Use both discovery agents and RAG-based tool finding
4. Show the "tool that exists to search for other tools" functionality

Run with: poetry run python examples/dynamic_react_agent_example.py
"""


import contextlib

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import tool

from haive.agents.react.dynamic_react_agent import DynamicReactAgent


@tool
def calculator(expression: str) -> float:
    """Calculate mathematical expression."""
    try:
        return eval(expression)
    except:
        return 0.0


@tool
def text_processor(text: str) -> str:
    """Process text by converting to uppercase."""
    return text.upper()


@tool
def word_counter(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def main():
    """Main demonstration of DynamicReactAgent capabilities."""
    # Example 1: Agent with pre-registered tools

    tools = [
        {
            "id": "calc",
            "name": "Calculator",
            "description": "Mathematical calculations",
            "component": calculator,
            "category": "math",
        },
        {
            "id": "text_proc",
            "name": "Text Processor",
            "description": "Text processing operations",
            "component": text_processor,
            "category": "text",
        },
    ]

    agent = DynamicReactAgent.create_with_tools(
        name="demo_agent",
        tools=tools,
        engine=AugLLMConfig(
            system_message="You are a helpful assistant with dynamic tool capabilities."
        ),
    )

    # Show that the agent has the discovery tool
    discovery_tools = [
        tool
        for tool in agent.engine.tools
        if hasattr(tool, "name") and "discover_and_load_tools" in tool.name
    ]

    if discovery_tools:
        pass

    # Example 2: Agent with discovery capabilities

    DynamicReactAgent.create_with_discovery(
        name="discovery_agent", document_path="@haive-tools", engine=AugLLMConfig()
    )

    # Example 3: Agent with RAG-based tool discovery

    documents = [
        "The calculator tool is useful for mathematical operations like addition, subtraction, multiplication, and division.",
        "Text processing tools can convert text to uppercase, lowercase, or perform other string manipulations.",
        "Word counting tools help analyze text by counting words, characters, or sentences.",
        "Web search tools can find information online and retrieve relevant results.",
        "File processing tools can read, write, and manipulate files in various formats.",
    ]

    DynamicReactAgent.create_with_rag_tooling(
        name="rag_agent", engine=AugLLMConfig(), rag_documents=documents
    )

    # Example 4: Demonstrate tool management

    # Create a state for testing
    from haive.agents.react.dynamic_react_agent import DynamicToolState

    state = DynamicToolState()

    # Add some tools to categories
    state.categorize_tool("calculator", "math")
    state.categorize_tool("text_processor", "text")
    state.categorize_tool("word_counter", "text")

    # Track usage
    state.track_tool_usage("calculator")
    state.track_tool_usage("calculator")
    state.track_tool_usage("text_processor")

    # Get tools by category
    state.get_tools_by_category("math")
    state.get_tools_by_category("text")

    # Example 5: Show the dynamic discovery tool in action

    # Test the discovery tool functionality
    discovery_tool = discovery_tools[0] if discovery_tools else None
    if discovery_tool:

        # Test discovery for different tasks
        test_queries = [
            "mathematical calculations",
            "text processing",
            "data visualization",
            "web scraping",
        ]

        for query in test_queries:
            with contextlib.suppress(Exception):
                discovery_tool.invoke({"task_description": query})


if __name__ == "__main__":
    main()
