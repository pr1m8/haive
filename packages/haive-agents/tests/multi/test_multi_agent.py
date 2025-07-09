#!/usr/bin/env python
# test_multi_agent.py

"""Test example for using the improved MultiAgent class.

This script demonstrates how to create and use multiple agents together
using the MultiAgent class with the enhanced AgentSchemaComposer.
"""

import logging

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.logging.rich_logger import LogLevel, get_logger
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field

from haive.agents.multi.agent import MultiAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent

# Configure logger
logger = get_logger("test_multi_agent")
logger.set_level(LogLevel.DEBUG)


# Define a tool for demonstration
from langchain_core.tools import tool


@tool
def add(a: int, b: int) -> int:
    """Returns the sum of two numbers."""
    return a + b


# Define an output model
class Plan(BaseModel):
    """A simple planning model with steps."""

    steps: list[str] = Field(description="list of steps")


def create_test_agents():
    """Create test agents for the multi-agent system."""
    # Create a ReactAgent with a tool
    tool_aug = AugLLMConfig(tools=[add], name="react_llm")
    react_agent = ReactAgent(engine=tool_aug, name="ReactAgent")

    # Create a SimpleAgent with structured output
    plan_aug = AugLLMConfig(
        structured_output_model=Plan, structured_output_version="v2", name="plan_llm"
    )
    simple_agent = SimpleAgent(engine=plan_aug, name="SimpleAgent")

    return react_agent, simple_agent


def test_sequential():
    """Test sequential multi-agent execution."""
    logger.info("=== Testing Sequential Multi-Agent ===")

    # Create the agents
    react_agent, simple_agent = create_test_agents()

    # Create sequential multi-agent
    multi = MultiAgent.sequential(
        agents=[react_agent, simple_agent],
        name="SequentialDemo",
        separation_strategy="smart",
        use_agent_nodes=True,
        use_engine_io_mappings=True,
    )

    # Print schema info
    print_schema_info(multi)

    # Run the multi-agent
    input_data = {
        "messages": [HumanMessage(content="Calculate 5+7 and then make a plan")]
    }
    result = multi.run(input_data)

    # Show result
    logger.info("Result from sequential multi-agent:")
    if hasattr(result, "agent_outputs"):
        for agent_name, output in result.agent_outputs.items():
            logger.info(f"  {agent_name} output: {output}")
    else:
        logger.info(f"  {result}")

    return multi, result


def test_supervisor():
    """Test supervisor multi-agent execution."""
    logger.info("=== Testing Supervisor Multi-Agent ===")

    # Create the agents
    react_agent, simple_agent = create_test_agents()

    # Create supervisor multi-agent
    multi = MultiAgent.supervised(
        agents=[simple_agent],
        coordinator=react_agent,
        name="SupervisorDemo",
        separation_strategy="smart",
        use_agent_nodes=True,
        use_engine_io_mappings=True,
    )

    # Print schema info
    print_schema_info(multi)

    # Run the multi-agent
    input_data = {
        "messages": [HumanMessage(content="Calculate 5+7 and then make a plan")]
    }
    result = multi.run(input_data)

    # Show result
    logger.info("Result from supervisor multi-agent:")
    if hasattr(result, "agent_outputs"):
        for agent_name, output in result.agent_outputs.items():
            logger.info(f"  {agent_name} output: {output}")
    else:
        logger.info(f"  {result}")

    return multi, result


def print_schema_info(multi_agent: MultiAgent):
    """Print information about the schema and engine IO mappings."""
    logger.info(f"Multi-Agent: {multi_agent.name}")
    logger.info(f"State Schema: {multi_agent.state_schema.__name__}")

    # Check if schema has engine IO mappings
    if hasattr(multi_agent.state_schema, "__engine_io_mappings__"):
        mappings = getattr(multi_agent.state_schema, "__engine_io_mappings__", {})
        logger.info(f"Engine IO Mappings: {len(mappings)}")

        # Print mappings
        for engine_name, mapping in mappings.items():
            logger.info(f"  Engine: {engine_name}")
            logger.info(f"    Inputs: {mapping.get('inputs', [])}")
            logger.info(f"    Outputs: {mapping.get('outputs', [])}")
    else:
        logger.info("No engine IO mappings found!")

    # Print engines
    if hasattr(multi_agent.state_schema, "engines"):
        engines = getattr(multi_agent.state_schema, "engines", {})
        logger.info(f"Engines: {len(engines)}")
        for name in engines:
            logger.info(f"  {name}")
    else:
        logger.info("No engines found in schema!")


def main():
    """Run the multi-agent tests."""
    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Run tests
    test_sequential()
    test_supervisor()

    logger.info("All tests completed successfully!")


if __name__ == "__main__":
    main()
