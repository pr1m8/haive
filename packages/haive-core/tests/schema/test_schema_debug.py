#!/usr/bin/env python3
"""Debug schema generation specifically."""

import sys

sys.path.insert(0, "/home/will/Projects/haive/backend/haive")

from haive.agents.simple.agent_v2 import SimpleAgentV2
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.field_utils import get_field_info_from_model


# Define test model
class TestResponse(BaseModel):
    """Simple test model."""

    message: str = Field(description="Test message")


# Simple prompt
TEST_PROMPT = ChatPromptTemplate.from_messages(
    [("system", "You are a helpful assistant."), ("human", "Say hello: {query}")]
)


def test_schema_debug():
    """Debug schema generation."""

    # Test field naming utility
    field_info = get_field_info_from_model(TestResponse)

    # Create agent
    agent = SimpleAgentV2(
        name="debug_agent",
        engine=AugLLMConfig(
            prompt_template=TEST_PROMPT,
            structured_output_model=TestResponse,
            structured_output_version="v2",
        ),
    )


    # Check engine's output schema
    if hasattr(agent.engine, "output_schema") and agent.engine.output_schema:
    else:
        pass

    # Check agent's state schema
    if hasattr(agent, "state_schema") and agent.state_schema:
    else:
        pass

    # Check agent's output schema
    if hasattr(agent, "output_schema") and agent.output_schema:
    else:
        pass

    return agent


if __name__ == "__main__":
    agent = test_schema_debug()
