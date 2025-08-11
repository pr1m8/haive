#!/usr/bin/env python3
"""Basic Agent Test - Test individual agents with structured output."""

import asyncio

from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent_v3 import SimpleAgentV3
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from pydantic import BaseModel, Field


# Structured output models
class AnalysisResult(BaseModel):
    """Structured analysis output."""

    topic: str = Field(description="Topic analyzed")
    key_points: list[str] = Field(description="Key points identified")
    summary: str = Field(description="Brief summary")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score")


async def test_simple_agent_v3():
    """Test SimpleAgentV3 with structured output."""
    # Create agent with structured output
    agent = SimpleAgentV3(
        name="analyzer",
        engine=AugLLMConfig(
            temperature=0.3,
            system_message="You are an expert analyst. Provide structured analysis.",
            structured_output_model=AnalysisResult,
        ),
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "{system_message}"),
                ("human", "Analyze this topic: {topic}\nContext: {context}"),
            ]
        ),
        debug=True,
    )

    # Test execution
    try:
        result = await agent.arun(
            {
                "topic": "The impact of AI on software development",
                "context": "Focus on productivity, code quality, and developer experience",
                "messages": [{"role": "user", "content": "Analyze this topic"}],
            }
        )

        if isinstance(result, dict):
            for _key, _value in result.items():
                pass
        elif isinstance(result, AnalysisResult):
            pass
        else:
            pass

    except Exception:
        import traceback

        traceback.print_exc()


async def test_react_agent():
    """Test ReactAgent with tools."""

    # Create tools
    @tool
    def calculate(expression: str) -> str:
        """Calculate mathematical expressions."""
        try:
            result = eval(expression)
            return f"The result of {expression} is {result}"
        except:
            return f"Could not calculate {expression}"

    @tool
    def get_info(topic: str) -> str:
        """Get information about a topic."""
        info_db = {
            "python": "Python is a high-level programming language known for simplicity.",
            "ai": "AI refers to machines performing tasks that require human intelligence.",
            "react": "React is a JavaScript library for building user interfaces.",
        }
        return info_db.get(topic.lower(), f"No information found about {topic}")

    # Create ReactAgent
    agent = ReactAgent(
        name="assistant",
        engine=AugLLMConfig(
            temperature=0.5,
            system_message="You are a helpful assistant. Use tools to answer questions.",
            tools=[calculate, get_info],
        ),
    )

    # Test execution
    try:
        # Test 1: Math calculation
        await agent.arun("What is 25 * 4 + 10?")

        # Test 2: Information retrieval
        await agent.arun("Tell me about Python")

    except Exception:
        import traceback

        traceback.print_exc()


async def test_sequential_manual():
    """Test sequential execution manually (without MultiAgent)."""
    # Agent 1: Analyzer
    analyzer = SimpleAgentV3(
        name="analyzer",
        engine=AugLLMConfig(
            temperature=0.4,
            system_message="You are an analyzer. Break down problems into components.",
        ),
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "{system_message}"),
                ("human", "Analyze this problem: {problem}"),
            ]
        ),
    )

    # Agent 2: Solution Designer with structured output
    class Solution(BaseModel):
        approach: str = Field(description="Solution approach")
        steps: list[str] = Field(description="Implementation steps")
        benefits: list[str] = Field(description="Expected benefits")

    designer = SimpleAgentV3(
        name="designer",
        engine=AugLLMConfig(
            temperature=0.5,
            system_message="You are a solution designer. Create practical solutions.",
            structured_output_model=Solution,
        ),
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "{system_message}"),
                ("human", "Based on this analysis:\n{analysis}\n\nDesign a solution."),
            ]
        ),
    )

    # Execute sequentially
    try:
        problem = "How to improve code review efficiency in large teams"

        # Step 1: Analyze
        analysis_result = await analyzer.arun(
            {"problem": problem, "messages": [{"role": "user", "content": problem}]}
        )

        # Step 2: Design solution
        solution_result = await designer.arun(
            {
                "analysis": str(analysis_result),
                "messages": [{"role": "user", "content": "Design solution"}],
            }
        )

        if isinstance(solution_result, dict):
            pass
        else:
            pass

    except Exception:
        import traceback

        traceback.print_exc()


async def main():
    """Run all tests."""
    await test_simple_agent_v3()
    await test_react_agent()
    await test_sequential_manual()


if __name__ == "__main__":
    asyncio.run(main())
