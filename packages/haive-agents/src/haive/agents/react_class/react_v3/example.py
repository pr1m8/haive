#!/usr/bin/env python3
"""Test script for ReactAgent demonstrating various usage patterns.

This script shows how to:
1. Create ReactAgents with different tools
2. Use RetryPolicy with LangGraph
3. Schema composition with tool integration
4. Running agents with different input formats
"""

import logging
import sys
import time

import httpx
from haive.core.schema.schema_composer import SchemaComposer
from haive.core.utils.pydantic_utils import display_code, pretty_print
from langchain_core.messages import HumanMessage
from langchain_core.tools import StructuredTool, Tool
from langgraph.pregel import RetryPolicy
from pydantic import BaseModel, Field

from haive.agents.react_class.react_v3.agent import ReactAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger("react_agent_test")


# Define a simple tool
def get_current_weather(location: str) -> str:
    """Get the current weather in a given location."""
    # Simulate API delay
    time.sleep(0.5)

    # Simulate a weather response
    weathers = ["sunny", "partly cloudy", "cloudy", "rainy", "stormy"]
    temps = {
        "New York": 72,
        "San Francisco": 65,
        "Miami": 85,
        "Seattle": 55,
        "Chicago": 60,
    }

    temp = temps.get(location, 70)
    weather = weathers[hash(location + str(time.time())) % len(weathers)]

    return (
        f"The current weather in {location} is {weather} with a temperature of {temp}°F"
    )


# Define a structured tool
class Calculator(BaseModel):
    """Tool for performing simple calculations."""

    operation: str = Field(
        description="Math operation: 'add', 'subtract', 'multiply', 'divide'"
    )
    a: float = Field(description="First number")
    b: float = Field(description="Second number")


def calculate(args: Calculator) -> str:
    """Perform a calculation based on the operation and numbers."""
    op = args.operation.lower()
    if op == "add":
        result = args.a + args.b
        return f"{args.a} + {args.b} = {result}"
    if op == "subtract":
        result = args.a - args.b
        return f"{args.a} - {args.b} = {result}"
    if op == "multiply":
        result = args.a * args.b
        return f"{args.a} × {args.b} = {result}"
    if op == "divide":
        if args.b == 0:
            return "Error: Cannot divide by zero"
        result = args.a / args.b
        return f"{args.a} ÷ {args.b} = {result}"
    return f"Unknown operation: {op}"


# Define a flaky API tool to demonstrate retry
def search_api(query: str) -> str:
    """Search for information about a topic (simulates random failures)."""
    # Simulate random failures (30% chance)
    if hash(query + str(time.time())) % 10 < 3:
        raise httpx.HTTPError("API connection failed")

    # Simulate successful response
    return f"Search results for '{query}': Found multiple sources with relevant information."


def test_basic_react_agent():
    """Test a basic ReactAgent with simple tools."""
    logger.info("Testing basic ReactAgent with simple tools")

    # Create tools
    weather_tool = Tool.from_function(
        func=get_current_weather,
        name="get_weather",
        description="Get the current weather in a given location",
    )

    search_tool = Tool.from_function(
        func=search_api,
        name="search",
        description="Search for information about a topic",
    )

    # Create agent with tools
    agent = ReactAgent.from_tools(
        tools=[weather_tool, search_tool],
        system_prompt="You are a helpful assistant with access to tools for weather and search.",
    )

    # Print information about the agent

    # Run the agent
    query = "What's the weather in New York and can you also search for information about climate change?"

    result = agent.run(query)

    pretty_print(result, "Agent Result")

    return agent


def test_structured_tool_agent():
    """Test a ReactAgent with structured tools."""
    logger.info("Testing ReactAgent with structured tools")

    # Create a structured tool
    calculator_tool = StructuredTool.from_function(
        func=calculate,
        name="calculator",
        description="Perform mathematical calculations",
        args_schema=Calculator,
    )

    weather_tool = Tool.from_function(
        func=get_current_weather,
        name="get_weather",
        description="Get the current weather in a given location",
    )

    # Create agent with structured tool
    agent = ReactAgent.from_tools(
        tools=[calculator_tool, weather_tool],
        system_prompt="You are a helpful assistant that can perform calculations and check the weather.",
    )

    # Show schema information
    schema_composer = SchemaComposer.from_components(
        [agent.config.engine, *agent.config.tools]
    )
    schema_composer.build()

    # Display calculator tool schema
    display_code(Calculator, "Calculator Schema")

    # Run the agent with a calculation request
    query = "Can you add 24.5 and 17.8, and then tell me the weather in Seattle?"

    result = agent.run(query)

    pretty_print(result, "Agent Result")

    return agent


def test_retry_policy():
    """Test a ReactAgent with retry policies for flaky tools."""
    logger.info("Testing ReactAgent with retry policies")

    # Create a flaky tool
    search_tool = Tool.from_function(
        func=search_api,
        name="search",
        description="Search for information about a topic",
    )

    # Create custom retry policy for the search tool
    retry_policy = RetryPolicy(
        initial_interval=0.5,  # Start with 0.5s delay
        backoff_factor=2.0,  # Double the delay each retry
        max_interval=8.0,  # Cap at 8s
        max_attempts=5,  # Try up to 5 times
        jitter=True,  # Add randomness to delays
        retry_on=httpx.HTTPError,  # Only retry on HTTP errors
    )

    # Create agent with custom retry policy
    agent = ReactAgent.from_tools(
        tools=[search_tool],
        tool_retry=retry_policy,
        system_prompt="You are a helpful assistant that can search for information.",
    )

    # Print retry policy details

    # Print interval progression
    interval = retry_policy.initial_interval
    for _i in range(1, retry_policy.max_attempts):
        interval = min(
            interval * retry_policy.backoff_factor, retry_policy.max_interval
        )

    # Run the agent
    query = "Can you search for information about quantum computing?"

    result = agent.run(query)

    pretty_print(result, "Agent Result")

    return agent


def test_multi_turn_conversation():
    """Test a ReactAgent with a multi-turn conversation."""
    logger.info("Testing ReactAgent with multi-turn conversation")

    # Create tools
    weather_tool = Tool.from_function(
        func=get_current_weather,
        name="get_weather",
        description="Get the current weather in a given location",
    )

    calculator_tool = StructuredTool.from_function(
        func=calculate,
        name="calculator",
        description="Perform mathematical calculations",
        args_schema=Calculator,
    )

    # Create agent
    agent = ReactAgent.from_tools(
        tools=[weather_tool, calculator_tool],
        system_prompt="You are a helpful assistant that can perform calculations and check the weather.",
    )

    # Start a conversation
    messages = []

    # First turn
    query1 = "What's the weather in Miami?"

    messages.append(HumanMessage(content=query1))
    result1 = agent.run(messages)

    # Update messages with result
    messages = result1.get("messages", [])

    # Print intermediate result
    for msg in messages[-2:]:  # Show AI response and potential tool message
        type(msg).__name__

    # Second turn
    query2 = "Can you multiply 15 by 7?"

    messages.append(HumanMessage(content=query2))
    result2 = agent.run(messages)

    # Print final result
    pretty_print(result2, "Final Result")

    return agent, result2


def test_all():
    """Run all ReactAgent tests."""
    test_basic_react_agent()
    test_structured_tool_agent()
    test_retry_policy()
    test_multi_turn_conversation()


if __name__ == "__main__":
    test_all()
