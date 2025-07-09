"""Test building meta state from any agent like LLMState pattern"""

from typing import Dict, Any, List
from pydantic import Field
from haive.core.schema.state_schema import StateSchema
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMEngine, AugLLMConfig

# Test creating meta state from any agent (like LLMState does with engine)
class TestAgentState(StateSchema):
    """Test state for any agent"""
    query: str = Field(default="")
    result: str = Field(default="")
    context: List[str] = Field(default_factory=list)

def test_meta_state_from_agent():
    """Test creating meta state from any agent"""
    
    # Create a simple agent
    engine = AugLLMEngine(AugLLMConfig(model="gpt-4"))
    agent = SimpleAgent(engine=engine, state_schema=TestAgentState)
    
    # The goal: create meta state that contains the agent + its state
    # WITHOUT flattening the agent's schema
    
    print(f"Agent state schema: {agent.state_schema}")
    print(f"Agent state fields: {agent.state_schema.model_fields.keys()}")
    
    # What we want: MetaState that has the agent + recompile fields
    # But preserves the agent's original state schema
    
    return agent

if __name__ == "__main__":
    agent = test_meta_state_from_agent()
    print("Agent created successfully")