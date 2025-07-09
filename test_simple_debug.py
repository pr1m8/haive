#!/usr/bin/env python3
"""
Simple debug test to isolate the issue.
"""

import sys
sys.path.insert(0, '/home/will/Projects/haive/backend/haive')

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from haive.agents.simple.agent_v2 import SimpleAgentV2
from haive.core.engine.aug_llm import AugLLMConfig

# Define test model
class TestResponse(BaseModel):
    """Simple test model."""
    message: str = Field(description="Test message")

# Simple prompt template
TEST_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "Say hello: {query}")
])

def test_simple_debug():
    """Debug test with simple model."""
    print("=== Simple Debug Test ===")
    
    # Create agent with structured output
    agent = SimpleAgentV2(
        name="debug_agent",
        engine=AugLLMConfig(
            prompt_template=TEST_PROMPT,
            structured_output_model=TestResponse,
            structured_output_version='v2'
        )
    )
    
    print(f"Agent: {agent.name}")
    print(f"Engine: {agent.engine.name}")
    print(f"Expected field name: test_response")
    
    # Check state schema
    if hasattr(agent, 'state_schema') and agent.state_schema:
        print(f"State schema fields: {list(agent.state_schema.model_fields.keys())}")
    
    # Check output schema
    if hasattr(agent, 'output_schema') and agent.output_schema:
        print(f"Output schema fields: {list(agent.output_schema.model_fields.keys())}")
    
    # Test run
    try:
        result = agent.run({"query": "world"}, debug=True)
        print(f"\n✅ SUCCESS: Agent execution completed")
        print(f"Result keys: {list(result.keys())}")
        
        # Check for the field
        if 'test_response' in result:
            print(f"✅ SUCCESS: Found 'test_response' in result")
            print(f"Value: {result['test_response']}")
        else:
            print(f"❌ FAILURE: 'test_response' not found in result")
            
        return result
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_simple_debug()