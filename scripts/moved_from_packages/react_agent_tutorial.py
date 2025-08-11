#!/usr/bin/env python3
"""ReactAgent Tutorial - Agents with Tools and Reasoning.

Difficulty: ⭐⭐ Beginner-Intermediate
Estimated Time: 10 minutes
Learning Objectives:
  • Create tool-enabled agents
  • Understand reasoning loops
  • Build custom tools
  • Handle complex problem-solving

Next Steps:
  → Try structured_output_guide.py for data extraction
  → Explore multi_agent_coordination.py for team workflows
"""

import asyncio
from datetime import datetime

from haive.agents.react import ReactAgent
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import tool


# Custom tools for the agent
@tool
def calculator(expression: str) -> str:
    """Evaluate mathematical expressions safely.

    Args:
        expression: Mathematical expression to evaluate (e.g., "2 + 3 * 4")

    Returns:
        Result of the calculation as a string
    """
    try:
        # Safe evaluation of basic math expressions
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error: {e!s}"


@tool
def get_current_time() -> str:
    """Get the current date and time.

    Returns:
        Current date and time as a formatted string
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def text_analyzer(text: str) -> str:
    """Analyze text and provide statistics.

    Args:
        text: Text to analyze

    Returns:
        Analysis results including word count, character count, etc.
    """
    words = text.split()
    sentences = text.split(".")

    return f"""Text Analysis Results:
• Characters: {len(text)}
• Words: {len(words)}
• Sentences: {len([s for s in sentences if s.strip()])}
• Average words per sentence: {len(words) / max(len([s for s in sentences if s.strip()]), 1):.1f}
• First 50 chars: {text[:50]}..."""


async def main():
    """Run the ReactAgent tutorial."""
    # Step 1: Create agent configuration
    config = AugLLMConfig(
        temperature=0.1,  # Lower temperature for more precise reasoning
        system_message="""You are a helpful assistant with access to tools.
Use the available tools to help answer questions and solve problems.
Think step by step and explain your reasoning.""",
    )

    # Step 2: Create the ReactAgent with tools
    agent = ReactAgent(
        name="tutorial_react_agent",
        engine=config,
        tools=[calculator, get_current_time, text_analyzer],
    )

    # Step 3: Run problem-solving examples

    # Example problems that require tool usage
    problems = [
        "What's the current time and what is 25 * 37?",
        "I have a paragraph: 'Artificial intelligence is transforming how we work and live. It enables automation of complex tasks.' Can you analyze this text and tell me about it?",
        "If I invest $1000 at 5% annual interest, how much will I have after 10 years using compound interest formula?",
    ]

    for _i, problem in enumerate(problems, 1):
        # Get agent response with tool usage
        await agent.arun(problem)

        # Show tool usage summary
        if hasattr(agent, "last_tool_calls"):
            pass

        # Small pause between problems
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
