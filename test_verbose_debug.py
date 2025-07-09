#!/usr/bin/env python3
"""
Debug with verbose logging to trace the issue.
"""

import sys
import logging
sys.path.insert(0, '/home/will/Projects/haive/backend/haive')

# Enable DEBUG logging
logging.basicConfig(level=logging.DEBUG)

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from haive.agents.simple.agent_v2 import SimpleAgentV2
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.field_utils import get_field_info_from_model

# Define test model
class TestResponse(BaseModel):
    """Simple test model."""
    message: str = Field(description="Test message")

# Simple prompt
TEST_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "Say hello: {query}")
])

def test_verbose_debug():
    """Debug with verbose logging."""
    print("=== Verbose Debug Test ===")
    
    # Test field naming utility
    field_info = get_field_info_from_model(TestResponse)
    print(f"Field info from model: {field_info}")
    
    # Enable specific loggers
    logging.getLogger('haive.core.schema.field_extractor').setLevel(logging.INFO)
    logging.getLogger('haive.core.schema.schema_composer').setLevel(logging.INFO)
    
    # Create agent
    agent = SimpleAgentV2(
        name="debug_agent",
        engine=AugLLMConfig(
            prompt_template=TEST_PROMPT,
            structured_output_model=TestResponse,
            structured_output_version='v2'
        )
    )
    
    print(f"\nAgent state schema fields: {list(agent.state_schema.model_fields.keys())}")
    print(f"Agent output schema fields: {list(agent.output_schema.model_fields.keys())}")
    
    return agent

if __name__ == "__main__":
    agent = test_verbose_debug()