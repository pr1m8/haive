"""Reflection example using the structured output post-hook pattern.

This combines the reflection pattern from the project docs with our
simple post-processing hook for extracting structured output.
"""

import asyncio
from typing import List

from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# Import our post-processing hook
from structured_output_post_hook import extract_structured_output


# Reflection models (based on project_docs/active/patterns/reflection_agent_pattern.md)
class Critique(BaseModel):
    """Structured critique of an output."""

    strengths: list[str] = Field(description="Identified strengths")
    weaknesses: list[str] = Field(description="Identified weaknesses")
    suggestions: list[str] = Field(description="Specific improvement suggestions")
    overall_quality: float = Field(
        ge=0.0, le=1.0, description="Quality score 0.0 to 1.0"
    )
    needs_revision: bool = Field(description="Whether revision is needed")


class ReflectionResult(BaseModel):
    """Complete reflection analysis."""

    summary: str = Field(description="Summary of the reflection analysis")
    critique: Critique = Field(description="Detailed critique")
    action_items: list[str] = Field(description="Specific action items for improvement")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in the analysis")


async def create_reflection_agent_with_structured_output():
    """Create a reflection agent using structured output post-hook pattern."""
    # Create reflection prompt
    reflection_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a reflection agent that analyzes and critiques responses.

        Your role is to:
        1. Identify strengths and weaknesses in the provided response
        2. Suggest specific improvements
        3. Provide an overall quality assessment
        4. Determine if revision is needed

        Be constructive and specific in your feedback.""",
            ),
            (
                "human",
                """Please analyze and provide structured feedback on this response:

Original Query: {query}
Response to Analyze: {response}

Provide a comprehensive reflection on the quality, accuracy, and completeness of this response.""",
            ),
        ]
    )

    # Create reflection agent with structured output
    reflection_agent = SimpleAgent(
        name="reflection_analyzer",
        engine=AugLLMConfig(
            prompt_template=reflection_prompt,
            structured_output_model=ReflectionResult,
            structured_output_version="v2",
            temperature=0.3,  # Lower temp for consistent analysis
        ),
    )

    return reflection_agent


async def example_basic_reflection():
    """Example: Basic response reflection with structured analysis."""

    # Create reflection agent
    reflector = await create_reflection_agent_with_structured_output()

    # Original query and response to analyze
    original_query = "Explain quantum computing"
    original_response = """
    Quantum computing uses quantum mechanics to process information.
    It's faster than regular computers and uses qubits instead of bits.
    This makes it good for solving complex problems.
    """

    # Run reflection analysis
    result = await reflector.arun(
        {"query": original_query, "response": original_response}
    )

    # Extract structured reflection using our post-hook
    reflection = extract_structured_output(result, ReflectionResult)

    if reflection:

        for strength in reflection.critique.strengths:
            pass")

        for weakness in reflection.critique.weaknesses:
            pass")

        for suggestion in reflection.critique.suggestions:
            pass")

        for action in reflection.action_items:
            pass")
    else:
        pass")


async def create_improvement_agent():
    """Create an improvement agent that applies reflection feedback."""
    improvement_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an improvement agent that creates better versions of responses.

        You will receive:
        1. An original query
        2. An original response
        3. Structured feedback about the response

        Your task is to create an improved version that addresses the feedback while
        maintaining the strengths identified.""",
            ),
            (
                "human",
                """Please improve this response based on the feedback provided:

Original Query: {query}
Original Response: {response}

Feedback Summary: {feedback_summary}
Identified Weaknesses: {weaknesses}
Improvement Suggestions: {suggestions}

Provide an improved version of the response that addresses these issues.""",
            ),
        ]
    )

    return SimpleAgent(
        name="improvement_agent",
        engine=AugLLMConfig(
            prompt_template=improvement_prompt,
            temperature=0.5,  # Moderate creativity for improvements
        ),
    )


async def example_reflection_with_improvement():
    """Example: Full reflection loop with improvement."""

    # Create agents
    reflector = await create_reflection_agent_with_structured_output()
    improver = await create_improvement_agent()

    # Original content
    query = "What are the benefits of renewable energy?"
    original_response = """
    Renewable energy is good for the environment. It comes from sources
    like solar and wind that don't run out. It's clean and helps reduce pollution.
    """


    # Step 1: Reflect on original response
    reflection_result = await reflector.arun(
        {"query": query, "response": original_response}
    )

    reflection = extract_structured_output(reflection_result, ReflectionResult)

    if reflection:

        # Step 2: Apply improvements if needed
        if reflection.critique.needs_revision:

            improved_result = await improver.arun(
                {
                    "query": query,
                    "response": original_response,
                    "feedback_summary": reflection.summary,
                    "weaknesses": "; ".join(reflection.critique.weaknesses),
                    "suggestions": "; ".join(reflection.critique.suggestions),
                }
            )

            # Extract improved response (it's a dict with messages)
            if isinstance(improved_result, dict) and "messages" in improved_result:
                messages = improved_result["messages"]
                for msg in reversed(messages):
                    if hasattr(msg, "content") and msg.content:
                        improved_response = msg.content
                        break
                else:
                    improved_response = "Could not extract improved response"
            else:
                improved_response = str(improved_result)


            # Optional: Reflect on the improvement

            second_reflection_result = await reflector.arun(
                {"query": query, "response": improved_response}
            )

            second_reflection = extract_structured_output(
                second_reflection_result, ReflectionResult
            )

            if second_reflection:

                improvement = (
                    second_reflection.critique.overall_quality
                    - reflection.critique.overall_quality
                )
        else:
            pass")


async def example_iterative_reflection():
    """Example: Iterative reflection until quality threshold is met."""

    # Create agents
    reflector = await create_reflection_agent_with_structured_output()
    improver = await create_improvement_agent()

    # Configuration
    max_iterations = 3
    quality_threshold = 0.8

    # Starting content
    query = "Explain machine learning algorithms"
    current_response = "Machine learning is when computers learn from data."


    iteration = 0
    quality_scores = []

    while iteration < max_iterations:
        iteration += 1

        # Reflect on current response
        reflection_result = await reflector.arun(
            {"query": query, "response": current_response}
        )

        reflection = extract_structured_output(reflection_result, ReflectionResult)

        if reflection:
            quality = reflection.critique.overall_quality
            quality_scores.append(quality)


            # Check if we've reached the threshold
            if quality >= quality_threshold:
                break

            # Check if quality is declining
            if len(quality_scores) > 1 and quality < quality_scores[-2]:
                break

            # Apply improvements
            if reflection.critique.needs_revision:

                improved_result = await improver.arun(
                    {
                        "query": query,
                        "response": current_response,
                        "feedback_summary": reflection.summary,
                        "weaknesses": "; ".join(reflection.critique.weaknesses),
                        "suggestions": "; ".join(reflection.critique.suggestions),
                    }
                )

                # Extract improved response
                if isinstance(improved_result, dict) and "messages" in improved_result:
                    messages = improved_result["messages"]
                    for msg in reversed(messages):
                        if hasattr(msg, "content") and msg.content:
                            current_response = msg.content
                            break
                else:
                    current_response = str(improved_result)
        else:
            break



async def main():
    """Run all reflection examples."""
    await example_basic_reflection()
    await example_reflection_with_improvement()
    await example_iterative_reflection()


if __name__ == "__main__":
    asyncio.run(main())
