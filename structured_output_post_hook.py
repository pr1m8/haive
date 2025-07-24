"""Simple post-processing hook for extracting structured output from agents.

This is the generic pattern for getting structured output from SimpleAgent
with structured_output_model configuration.
"""

import asyncio
from typing import Any, List, Optional, Type, TypeVar

from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# Type variable for any Pydantic model
T = TypeVar("T", bound=BaseModel)


def extract_structured_output[T: BaseModel](agent_result: dict, model_class: type[T]) -> T | None:
    """Generic post-processing hook to extract structured output from agent results.

    This is a simple utility function that extracts the structured output
    from a SimpleAgent's result when configured with structured_output_model.

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


# Example usage with different models


class TodoList(BaseModel):
    """A todo list with items."""

    title: str = Field(description="Title of the todo list")
    items: list[str] = Field(description="List of todo items", min_items=3, max_items=8)
    priority: str = Field(description="Overall priority", pattern="^(high|medium|low)$")
    estimated_hours: float = Field(description="Total estimated hours")


class AnalysisResult(BaseModel):
    """Result of an analysis."""

    topic: str = Field(description="What was analyzed")
    findings: list[str] = Field(description="Key findings", min_items=2, max_items=5)
    confidence: float = Field(description="Confidence score", ge=0.0, le=1.0)
    recommendation: str = Field(description="Main recommendation")


async def example_todo_list():
    """Example: Using SimpleAgent with TodoList structured output."""

    # Create prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful task planner."),
            ("human", "Create a todo list for: {task}"),
        ]
    )

    # Create agent with structured output
    agent = SimpleAgent(
        name="todo_planner",
        engine=AugLLMConfig(
            prompt_template=prompt,
            structured_output_model=TodoList,
            structured_output_version="v2",
        ),
    )

    # Run agent
    result = await agent.arun({"task": "prepare for a presentation"})

    # Extract structured output using the post-processing hook
    todo_list = extract_structured_output(result, TodoList)

    if todo_list:
        for i, item in enumerate(todo_list.items, 1):
            pass
    else:
        pass")


async def example_analysis():
    """Example: Using SimpleAgent with AnalysisResult structured output."""

    # Create prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a data analyst. Analyze the given situation and provide structured findings.",
            ),
            ("human", "Analyze this: {situation}"),
        ]
    )

    # Create agent with structured output
    agent = SimpleAgent(
        name="analyst",
        engine=AugLLMConfig(
            prompt_template=prompt,
            structured_output_model=AnalysisResult,
            structured_output_version="v2",
            temperature=0.5,
        ),
    )

    # Run agent
    result = await agent.arun(
        {
            "situation": "Our website traffic dropped 40% last week but sales only dropped 10%"
        }
    )

    # Extract structured output using the post-processing hook
    analysis = extract_structured_output(result, AnalysisResult)

    if analysis:
        for finding in analysis.findings:
            pass")
    else:
        pass")


# Generic helper for any agent with structured output
async def run_agent_with_structured_output[T: BaseModel](
    agent: SimpleAgent, input_data: Any, output_model: type[T], debug: bool = False
) -> T | None:
    """Run an agent and extract its structured output.

    This is a convenience function that combines agent execution
    with the post-processing hook.

    Args:
        agent: The SimpleAgent to run
        input_data: Input data for the agent
        output_model: The expected output model class
        debug: Whether to run in debug mode

    Returns:
        The structured output, or None if extraction fails
    """
    # Run the agent
    result = await agent.arun(input_data, debug=debug)

    # Extract and return the structured output
    return extract_structured_output(result, output_model)


async def example_generic_helper():
    """Example: Using the generic helper function."""

    # Create an agent
    agent = SimpleAgent(
        name="planner",
        engine=AugLLMConfig(
            structured_output_model=TodoList, structured_output_version="v2"
        ),
    )

    # Use the generic helper
    todo_list = await run_agent_with_structured_output(
        agent=agent, input_data="Plan a weekend camping trip", output_model=TodoList
    )

    if todo_list:
        pass")
    else:
        pass")


async def main():
    """Run all examples."""
    await example_todo_list()
    await example_analysis()
    await example_generic_helper()


if __name__ == "__main__":
    asyncio.run(main())
