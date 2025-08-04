"""Test Simple Multi-Agent Pattern - Corrected imports.

This is a simplified test to verify multi-agent functionality works.
"""

from __future__ import annotations

import asyncio

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from haive.agents.multi import MultiAgent
from haive.agents.react import ReactAgent
from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig


# Test 1: Basic Sequential Pattern
async def test_sequential_pattern():
    """Test basic sequential multi-agent execution."""
    print("Testing Sequential Multi-Agent Pattern...")

    # Create agents
    analyzer = SimpleAgent(
        name="analyzer",
        engine=AugLLMConfig(temperature=0.3),
        system_message="You are an analyzer. Analyze the input briefly.",
    )

    summarizer = SimpleAgent(
        name="summarizer",
        engine=AugLLMConfig(temperature=0.5),
        system_message="You are a summarizer. Summarize the analysis briefly.",
    )

    # Create sequential multi-agent using MultiAgent with execution_mode
    multi = MultiAgent(
        name="sequential_test",
        agents=[analyzer, summarizer],
        execution_mode="sequence",
    )

    # Test execution
    result = await multi.arun("What are the benefits of renewable energy?")
    print(f"Sequential Result: {result}\n")
    return result


# Test 2: Parallel Pattern with Tools
async def test_parallel_with_tools():
    """Test parallel execution with tool-using agents."""
    print("Testing Parallel Multi-Agent Pattern with Tools...")

    @tool
    def calculate(expression: str) -> str:
        """Calculate a mathematical expression."""
        try:
            result = eval(expression)
            return f"Calculation result: {result}"
        except BaseException:
            return "Invalid expression"

    @tool
    def word_count(text: str) -> str:
        """Count words in text."""
        count = len(text.split())
        return f"Word count: {count}"

    # Create agents with tools
    math_agent = ReactAgent(
        name="math_expert",
        engine=AugLLMConfig(temperature=0.2),
        tools=[calculate],
        system_message="You are a math expert. Use the calculator tool when needed.",
    )

    text_agent = ReactAgent(
        name="text_analyst",
        engine=AugLLMConfig(temperature=0.3),
        tools=[word_count],
        system_message="You are a text analyst. Use the word count tool when needed.",
    )

    # Create parallel multi-agent
    multi = MultiAgent(
        name="parallel_test",
        agents=[math_agent, text_agent],
        execution_mode="parallel",
    )

    # Test execution
    result = await multi.arun(
        "Calculate 15 * 23 and count the words in this sentence.")
    print(f"Parallel Result: {result}\n")
    return result


# Test 3: Multi-Agent from Clean Implementation
async def test_clean_multi_agent():
    """Test the clean multi-agent implementation."""
    print("Testing Clean Multi-Agent Implementation...")

    # Import CleanMultiAgent if available
    try:
        from haive.agents.multi.clean_multi_agent import CleanMultiAgent

        # Create agents
        agent1 = SimpleAgent(
            name="researcher",
            engine=AugLLMConfig(temperature=0.5),
            system_message="You are a researcher. Find key points.",
        )

        agent2 = SimpleAgent(
            name="writer",
            engine=AugLLMConfig(temperature=0.7),
            system_message="You are a writer. Create a brief report.",
        )

        # Create clean multi-agent
        multi = CleanMultiAgent(
            name="clean_test",
            agents=[agent1, agent2],
        )

        result = await multi.arun(
            "Research and write about quantum computing basics.")
        print(f"Clean Multi-Agent Result: {result}\n")
        return result
    except ImportError as e:
        print(f"CleanMultiAgent not available: {e}")
        return None


# Test 4: Simple Structured Output Pattern
class AnalysisResult(BaseModel):
    """Structured analysis output."""

    topic: str
    key_points: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)


async def test_structured_output():
    """Test multi-agent with structured output."""
    print("Testing Multi-Agent with Structured Output...")

    # ReactAgent for analysis
    analyzer = ReactAgent(
        name="analyzer",
        engine=AugLLMConfig(temperature=0.3),
        system_message="Analyze topics and identify key points.",
    )

    # SimpleAgent for structured output
    formatter = SimpleAgent(
        name="formatter",
        engine=AugLLMConfig(temperature=0.2),
        structured_output_model=AnalysisResult,
        system_message="Format analysis into structured output.",
    )

    # Sequential execution
    multi = MultiAgent(
        name="structured_test",
        agents=[analyzer, formatter],
        execution_mode="sequence",
    )

    result = await multi.arun("Analyze the impact of AI on healthcare.")
    print(f"Structured Output Result: {result}\n")
    return result


# Main execution
async def main():
    """Run all tests."""
    print("🚀 Testing Multi-Agent Patterns\n")
    print("=" * 50)

    # Run tests
    try:
        # Test 1: Sequential
        await test_sequential_pattern()
        print("=" * 50)

        # Test 2: Parallel with tools
        await test_parallel_with_tools()
        print("=" * 50)

        # Test 3: Clean implementation
        await test_clean_multi_agent()
        print("=" * 50)

        # Test 4: Structured output
        await test_structured_output()
        print("=" * 50)

        print("✅ All tests completed!")

    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
