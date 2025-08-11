#!/usr/bin/env python3
"""ReactAgent Example - Agent with reasoning and tool usage.

This example demonstrates how to create a ReactAgent that can use tools
to solve problems through reasoning and action.
"""

import asyncio

from haive.agents.react import ReactAgent
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import tool


@tool
def calculator(expression: str) -> str:
    """Evaluate mathematical expressions safely.

    Args:
        expression: Mathematical expression to evaluate (e.g., "15 * 23")

    Returns:
        Result of the mathematical calculation
    """
    try:
        # Safe evaluation for basic math
        allowed_names = {
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
            "sum": sum,
            "pow": pow,
            "len": len,
        }
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


@tool
def word_counter(text: str) -> str:
    """Count words, characters, and lines in text.

    Args:
        text: Text to analyze

    Returns:
        Analysis of the text including word count, character count, etc.
    """
    words = len(text.split())
    chars = len(text)
    chars_no_spaces = len(text.replace(" ", ""))
    lines = len(text.split("\n"))

    return (
        f"Text Analysis:\n"
        f"- Words: {words}\n"
        f"- Characters: {chars}\n"
        f"- Characters (no spaces): {chars_no_spaces}\n"
        f"- Lines: {lines}"
    )


async def main():
    """Run the ReactAgent example."""
    # Create agent configuration
    config = AugLLMConfig(
        model="gpt-4",
        temperature=0.3,  # Lower temperature for more focused reasoning
        system_message="You are a helpful assistant that can use tools to solve problems.",
    )

    # Create tools
    tools = [calculator, word_counter]

    # Create the ReactAgent with tools
    agent = ReactAgent(name="reasoning_assistant", engine=config, tools=tools)

    # Example tasks that require tool usage
    tasks = [
        "Calculate the result of 15 * 23 + 47 and tell me if it's greater than 400",
        "Analyze this text: 'The quick brown fox jumps over the lazy dog' and tell me about its characteristics",
        "If I have 3 boxes with 12 items each, and I remove 8 items total, how many items do I have left?",
        "Count the words in this sentence and then calculate what 10% of that number would be",
    ]

    for _tool in tools:
        pass

    for _i, task in enumerate(tasks, 1):
        # Get agent response with reasoning
        await agent.arun(task, debug=True)

        # Add delay between tasks
        await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(main())
