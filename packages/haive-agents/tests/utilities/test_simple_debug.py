#!/usr/bin/env python3
"""Simple debug test to isolate the issue."""

import sys

sys.path.insert(0, "/home/will/Projects/haive/backend/haive")

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from haive.agents.simple.agent_v2 import SimpleAgentV2


# Define test model
class TestResponse(BaseModel):
    """Simple test model."""

    message: str = Field(description="Test message")


# Simple prompt template
TEST_PROMPT = ChatPromptTemplate.from_messages(
    [("system", "You are a helpful assistant."), ("human", "Say hello: {query}")]
)


def test_simple_debug():
    """Debug test with simple model."""

    # Create agent with structured output
    agent = SimpleAgentV2(
        name="debug_agent",
        engine=AugLLMConfig(
            prompt_template=TEST_PROMPT,
            structured_output_model=TestResponse,
            structured_output_version="v2",
        ),
    )


    # Check state schema
    if hasattr(agent, "state_schema") and agent.state_schema:
        pass

    # Check output schema
    if hasattr(agent, "output_schema") and agent.output_schema:
        pass

    # Test run
    try:
        result = agent.run({"query": "world"}, debug=True)

        # Check for the field
        if "test_response" in result:
        else:
            pass")

        return result

    except Exception as e:
        import traceback

        traceback.print_exc()
        return None


if __name__ == "__main__":
    test_simple_debug()
