#!/usr/bin/env python

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from agents.simple.factory import create_simple_agent
from agents.simple.state import SimpleAgentState
from haive.core.engine.aug_llm import AugLLMConfig


def test_simple_agent_schema():
    """Test a simple agent with the updated schema."""
    print("Step 1: Creating AugLLM config")
    # Create a simple AugLLM engine
    aug_llm = AugLLMConfig(
        name="test_llm",
        system_prompt="You are a test assistant. Remember what the user tells you.",
    )

    print("Step 2: Creating agent")
    try:
        # Create the agent using the factory function
        agent = create_simple_agent(
            engine=aug_llm,
            name="test_agent",
            system_prompt="You are a helpful assistant. Remember what the user tells you.",
        )
        print("Agent created successfully")
    except Exception as e:
        print(f"Error creating agent: {e}")
        raise

    print("Step 3: Checking state schema")
    try:
        # Test the agent's schema
        state_schema = agent.state_schema
        print(f"Agent state schema: {state_schema}")
        print(f"SimpleAgentState: {SimpleAgentState}")
        assert (
            state_schema == SimpleAgentState
        ), f"Expected SimpleAgentState, got {state_schema}"
        print("Schema validation passed")
    except Exception as e:
        print(f"Error validating schema: {e}")
        raise

    print("Test succeeded")
    return True


if __name__ == "__main__":
    test_simple_agent_schema()
