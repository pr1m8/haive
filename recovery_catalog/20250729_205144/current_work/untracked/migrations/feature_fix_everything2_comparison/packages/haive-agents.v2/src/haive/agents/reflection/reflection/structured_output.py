"""Structured output reflection agents and examples.

This module provides reflection agents that use structured output models
combined with a post-processing hook pattern for extracting results.
"""

import asyncio
from typing import Any, TypeVar

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

from haive.agents.simple.agent import SimpleAgent

from .models import ReflectionResult

# Type variable for any Pydantic model
T = TypeVar("T", bound=BaseModel)


def extract_structured_output(
    agent_result: dict[str, Any], model_class: type[T]
) -> T | None:
    """Generic post-processing hook to extract structured output from agent results.

    Args:
        agent_result: The dict returned by agent.arun()
        model_class: The Pydantic model class to extract

    Returns:
        Instance of the model class, or None if not found
    """
    # Check if result has messages
    if not isinstance(agent_result, dict) or "messages" not in agent_result:
        return None

    messages = agent_result["messages"]

    # Look through messages in reverse order (most recent first)
    for msg in reversed(messages):
        # Check if it's an AI message with tool calls
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tool_call in msg.tool_calls:
                if isinstance(tool_call, dict):
                    # Check if this tool call matches our model
                    if tool_call.get("name") == model_class.__name__:
                        import json

                        # Extract and parse the arguments
                        args = tool_call.get("args", {})
                        if isinstance(args, str):
                            args = json.loads(args)

                        # Create and return the model instance
                        try:
                            return model_class(**args)
                        except Exception:
                            continue

                    # Handle OpenAI function format
                    elif "function" in tool_call:
                        func = tool_call["function"]
                        if func.get("name") == model_class.__name__:
                            args = func.get("arguments", {})
                            if isinstance(args, str):
                                args = json.loads(args)

                            try:
                                return model_class(**args)
                            except Exception:
                                continue

    return None


class StructuredReflectionAgent:
    """Agent that performs reflection with structured output extraction."""

    def __init__(
        self,
        name: str = "reflection_agent",
        system_prompt: str | None = None,
        temperature: float = 0.3,
    ):
        """Initialize the structured reflection agent.

        Args:
            name: Name for the agent
            system_prompt: Custom system prompt (optional)
            temperature: Temperature for LLM generation
        """
        self.name = name

        # Default reflection prompt
        if not system_prompt:
            system_prompt = """You are a reflection agent that analyzes and critiques responses.
        
Your role is to:
1. Identify strengths and weaknesses in the provided response
2. Suggest specific improvements
3. Provide an overall quality assessment
4. Determine if revision is needed

Be constructive and specific in your feedback."""

        # Create reflection prompt template
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                (
                    "human",
                    """Please analyze and provide structured feedback on this response:

Original Query: {query}
Response to Analyze: {response}

Provide a comprehensive reflection on the quality, accuracy, and completeness of this response.""",
                ),
            ]
        )

        # Create the underlying SimpleAgent with structured output
        self.agent = SimpleAgent(
            name=name,
            engine=AugLLMConfig(
                prompt_template=self.prompt_template,
                structured_output_model=ReflectionResult,
                structured_output_version="v2",
                temperature=temperature,
            ),
        )

    async def reflect(self, query: str, response: str) -> ReflectionResult | None:
        """Perform reflection analysis on a response.

        Args:
            query: The original query
            response: The response to analyze

        Returns:
            ReflectionResult with structured analysis, or None if extraction fails
        """
        # Run the agent
        result = await self.agent.arun({"query": query, "response": response})

        # Extract structured output using post-processing hook
        return extract_structured_output(result, ReflectionResult)


class StructuredImprovementAgent:
    """Agent that improves responses based on reflection feedback."""

    def __init__(self, name: str = "improvement_agent", temperature: float = 0.5):
        """Initialize the improvement agent.

        Args:
            name: Name for the agent
            temperature: Temperature for LLM generation
        """
        self.name = name

        # Create improvement prompt template
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

        # Create the underlying SimpleAgent
        self.agent = SimpleAgent(
            name=name,
            engine=AugLLMConfig(
                prompt_template=improvement_prompt, temperature=temperature
            ),
        )

    async def improve(
        self, query: str, response: str, reflection: ReflectionResult
    ) -> str:
        """Improve a response based on reflection feedback.

        Args:
            query: The original query
            response: The response to improve
            reflection: The reflection analysis

        Returns:
            Improved response text
        """
        # Run the improvement agent
        result = await self.agent.arun(
            {
                "query": query,
                "response": response,
                "feedback_summary": reflection.summary,
                "weaknesses": "; ".join(reflection.critique.weaknesses),
                "suggestions": "; ".join(reflection.critique.suggestions),
            }
        )

        # Extract improved response from messages
        if isinstance(result, dict) and "messages" in result:
            messages = result["messages"]
            for msg in reversed(messages):
                if hasattr(msg, "content") and msg.content:
                    return msg.content

        return str(result)


class ReflectionLoop:
    """Manages iterative reflection and improvement process."""

    def __init__(
        self,
        reflector: StructuredReflectionAgent,
        improver: StructuredImprovementAgent,
        max_iterations: int = 3,
        quality_threshold: float = 0.8,
    ):
        """Initialize the reflection loop.

        Args:
            reflector: The reflection agent
            improver: The improvement agent
            max_iterations: Maximum iterations before stopping
            quality_threshold: Quality score to stop iterating
        """
        self.reflector = reflector
        self.improver = improver
        self.max_iterations = max_iterations
        self.quality_threshold = quality_threshold

    async def iterate(self, query: str, initial_response: str) -> dict[str, Any]:
        """Run iterative reflection and improvement.

        Args:
            query: The original query
            initial_response: Starting response to improve

        Returns:
            Dictionary with final response, iterations, and quality progression
        """
        current_response = initial_response
        iteration = 0
        quality_scores = []
        reflections = []

        while iteration < self.max_iterations:
            iteration += 1

            # Reflect on current response
            reflection = await self.reflector.reflect(query, current_response)

            if not reflection:
                break

            reflections.append(reflection)
            quality = reflection.critique.overall_quality
            quality_scores.append(quality)

            # Check if we've reached the threshold
            if quality >= self.quality_threshold:
                break

            # Check if quality is declining
            if len(quality_scores) > 1 and quality < quality_scores[-2]:
                break

            # Apply improvements if needed
            if reflection.critique.needs_revision:
                current_response = await self.improver.improve(
                    query, current_response, reflection
                )
            else:
                break

        return {
            "final_response": current_response,
            "iterations": iteration,
            "quality_scores": quality_scores,
            "reflections": reflections,
            "improved": (
                len(quality_scores) > 0 and quality_scores[-1] > quality_scores[0]
                if quality_scores
                else False
            ),
        }


# Factory functions for easy creation
def create_reflection_agent(
    name: str = "reflector", temperature: float = 0.3, **kwargs
) -> StructuredReflectionAgent:
    """Create a structured reflection agent."""
    return StructuredReflectionAgent(name=name, temperature=temperature, **kwargs)


def create_improvement_agent(
    name: str = "improver", temperature: float = 0.5, **kwargs
) -> StructuredImprovementAgent:
    """Create a structured improvement agent."""
    return StructuredImprovementAgent(name=name, temperature=temperature, **kwargs)


def create_reflection_loop(
    max_iterations: int = 3,
    quality_threshold: float = 0.8,
    reflector_name: str = "reflector",
    improver_name: str = "improver",
) -> ReflectionLoop:
    """Create a complete reflection loop system."""
    reflector = create_reflection_agent(name=reflector_name)
    improver = create_improvement_agent(name=improver_name)

    return ReflectionLoop(
        reflector=reflector,
        improver=improver,
        max_iterations=max_iterations,
        quality_threshold=quality_threshold,
    )


# Example usage functions
async def example_basic_reflection():
    """Example: Basic response reflection with structured analysis."""
    print("\n=== Basic Reflection Example ===\n")

    # Create reflection agent
    reflector = create_reflection_agent()

    # Original query and response to analyze
    query = "Explain quantum computing"
    response = """
    Quantum computing uses quantum mechanics to process information. 
    It's faster than regular computers and uses qubits instead of bits.
    This makes it good for solving complex problems.
    """

    print(f"Query: {query}")
    print(f"Response: {response}")

    # Run reflection analysis
    reflection = await reflector.reflect(query, response)

    if reflection:
        print("\n✅ Reflection Analysis:")
        print(f"Summary: {reflection.summary}")
        print(f"Overall Quality: {reflection.critique.overall_quality:.2f}")
        print(f"Needs Revision: {reflection.critique.needs_revision}")
        print(f"Confidence: {reflection.confidence:.2f}")

        print("\nStrengths:")
        for strength in reflection.critique.strengths:
            print(f"  • {strength}")

        print("\nWeaknesses:")
        for weakness in reflection.critique.weaknesses:
            print(f"  • {weakness}")

        print("\nSuggestions:")
        for suggestion in reflection.critique.suggestions:
            print(f"  • {suggestion}")

        print("\nAction Items:")
        for action in reflection.action_items:
            print(f"  • {action}")
    else:
        print("❌ Failed to extract reflection analysis")


async def example_reflection_with_improvement():
    """Example: Full reflection loop with improvement."""
    print("\n\n=== Reflection + Improvement Example ===\n")

    # Create agents
    reflector = create_reflection_agent()
    improver = create_improvement_agent()

    # Original content
    query = "What are the benefits of renewable energy?"
    original_response = """
    Renewable energy is good for the environment. It comes from sources
    like solar and wind that don't run out. It's clean and helps reduce pollution.
    """

    print(f"Query: {query}")
    print(f"Original Response: {original_response}")

    # Step 1: Reflect on original response
    reflection = await reflector.reflect(query, original_response)

    if reflection:
        print("\n📊 Reflection Analysis:")
        print(f"Quality Score: {reflection.critique.overall_quality:.2f}")
        print(f"Needs Revision: {reflection.critique.needs_revision}")

        # Step 2: Apply improvements if needed
        if reflection.critique.needs_revision:
            print("\n🔧 Applying improvements...")

            improved_response = await improver.improve(
                query, original_response, reflection
            )

            print("\n✨ Improved Response:")
            print(improved_response)

            # Optional: Reflect on the improvement
            print("\n🔍 Re-analyzing improved response.")

            second_reflection = await reflector.reflect(query, improved_response)

            if second_reflection:
                print(
                    f"New Quality Score: {second_reflection.critique.overall_quality:.2f}"
                )
                print(
                    f"Still Needs Revision: {second_reflection.critique.needs_revision}"
                )

                improvement = (
                    second_reflection.critique.overall_quality
                    - reflection.critique.overall_quality
                )
                print(f"Quality Improvement: {improvement:+.2f}")
        else:
            print("\n✅ No revision needed - original response is good!")


async def example_iterative_reflection():
    """Example: Iterative reflection until quality threshold is met."""
    print("\n\n=== Iterative Reflection Example ===\n")

    # Create reflection loop
    loop = create_reflection_loop(max_iterations=3, quality_threshold=0.8)

    # Starting content
    query = "Explain machine learning algorithms"
    initial_response = "Machine learning is when computers learn from data."

    print(f"Query: {query}")
    print(f"Starting Response: {initial_response}")
    print(f"Target Quality: {loop.quality_threshold}")
    print(f"Max Iterations: {loop.max_iterations}")

    # Run iterative improvement
    result = await loop.iterate(query, initial_response)

    print("\n📈 Final Results:")
    print(f"Iterations completed: {result['iterations']}")
    print(
        f"Quality progression: {' → '.join(f'{q:.2f}' for q in result['quality_scores'])}"
    )
    print(f"Improved: {result['improved']}")
    print("\nFinal Response:")
    print(result["final_response"])


async def main():
    """Run all structured reflection examples."""
    await example_basic_reflection()
    await example_reflection_with_improvement()
    await example_iterative_reflection()


if __name__ == "__main__":
    asyncio.run(main())
