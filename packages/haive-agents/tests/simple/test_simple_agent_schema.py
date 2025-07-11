#!/usr/bin/env python

import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from agents.simple.factory import create_simple_agent
from agents.simple.state import SimpleAgentState

from haive.core.engine.aug_llm import AugLLMConfig


def test_simple_agent_schema():
    """Test a simple agent with the updated schema."""
    # Create a simple AugLLM engine
    aug_llm = AugLLMConfig(
        name="test_llm",
        system_prompt="You are a test assistant. Remember what the user tells you.",
    )

    try:
        # Create the agent using the factory function
        agent = create_simple_agent(
            engine=aug_llm,
            name="test_agent",
            system_prompt="You are a helpful assistant. Remember what the user tells you.",
        )
    except Exception:
        raise

    try:
        # Test the agent's schema
        state_schema = agent.state_schema
        assert (
            state_schema == SimpleAgentState
        ), f"Expected SimpleAgentState, got {state_schema}"
    except Exception:
        raise

    return True


if __name__ == "__main__":
    test_simple_agent_schema()
