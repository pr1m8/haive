"""Test building meta state from any agent like LLMState pattern."""

from typing import Any, Dict, List

from haive.core.engine.aug_llm import AugLLMConfig, AugLLMEngine
from haive.core.schema.state_schema import StateSchema
from pydantic import Field

from haive.agents.simple.agent import SimpleAgent


# Test creating meta state from any agent (like LLMState does with engine)
class TestAgentState(StateSchema):
    """Test state for any agent."""

    query: str = Field(default="")
    result: str = Field(default="")
    context: list[str] = Field(default_factory=list)


def test_meta_state_from_agent():
    """Test creating meta state from any agent."""
    # Create a simple agent
    engine = AugLLMEngine(AugLLMConfig(model="gpt-4"))
    agent = SimpleAgent(engine=engine, state_schema=TestAgentState)

    # The goal: create meta state that contains the agent + its state
    # WITHOUT flattening the agent's schema

    # What we want: MetaState that has the agent + recompile fields
    # But preserves the agent's original state schema

    return agent


if __name__ == "__main__":
    agent = test_meta_state_from_agent()
