#!/usr/bin/env python3
"""Test that the fix resolves the serialization issue."""

import asyncio
from pydantic import BaseModel, Field
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

class TaskOutput(BaseModel):
    task: str = Field(..., description="Task")
    priority: str = Field(default="medium", description="Priority")

async def test_fix():
    """Test that the serialization issue is fixed."""
    
    print("=== Testing Serialization Fix ===\n")
    
    # Create agent with structured output
    config = AugLLMConfig(
        temperature=0.7,
        structured_output_model=TaskOutput,
        structured_output_version="v2"
    )
    
    agent = SimpleAgent(
        name="fixed_agent",
        engine=config
    )
    
    print("Testing agent execution with persistence...")
    
    try:
        # This should now work!
        result = await agent.arun(
            "Create a high priority task for testing the fix",
            config={"configurable": {"thread_id": "test-fix-123"}}
        )
        
        print(f"✅ SUCCESS! Agent executed without serialization errors")
        print(f"Result: {result}")
        print(f"Result type: {type(result)}")
        
        # If structured output is working, result should be TaskOutput
        if isinstance(result, TaskOutput):
            print(f"Task: {result.task}")
            print(f"Priority: {result.priority}")
            
    except Exception as e:
        print(f"❌ Still failed: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_fix())