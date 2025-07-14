#!/usr/bin/env python3
"""Test different approaches to fix the serialization issue."""

import asyncio
from pydantic import BaseModel, Field
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

class TaskOutput(BaseModel):
    task: str = Field(..., description="Task")
    priority: str = Field(default="medium", description="Priority")

async def test_fix_approaches():
    """Test different ways to fix the issue."""
    
    print("=== Testing Fix Approaches ===\n")
    
    # Create agent
    config = AugLLMConfig(
        temperature=0.7,
        structured_output_model=TaskOutput,
        structured_output_version="v2"
    )
    
    agent = SimpleAgent(
        name="test_agent",
        engine=config
    )
    
    print("1. Original issue - with persistence:")
    try:
        result = await agent.arun(
            "Create a task", 
            config={"configurable": {"thread_id": "test-123"}}
        )
        print(f"   ✅ Success: {result}")
    except Exception as e:
        print(f"   ❌ Failed: {type(e).__name__}: {str(e)[:100]}...")
    
    print("\n2. Fix approach 1 - Disable checkpointing:")
    agent2 = SimpleAgent(name="test2", engine=config)
    agent2.checkpointer = None
    try:
        result = await agent2.arun("Create a task")
        print(f"   ✅ Success: {result}")
    except Exception as e:
        print(f"   ❌ Failed: {type(e).__name__}: {str(e)[:100]}...")
    
    print("\n3. Fix approach 2 - Pre-convert state:")
    agent3 = SimpleAgent(name="test3", engine=config)
    
    # Force state to convert engines to dicts
    state = agent3.state_schema()
    
    # Manually convert engine fields
    if hasattr(state, 'engine') and hasattr(state.engine, 'model_dump'):
        state.engine = state.engine.model_dump()
    
    if hasattr(state, 'engines'):
        for key, eng in state.engines.items():
            if hasattr(eng, 'model_dump'):
                state.engines[key] = eng.model_dump()
    
    try:
        result = await agent3.arun(
            "Create a task",
            config={"configurable": {"thread_id": "test-456"}}
        )
        print(f"   ✅ Success: {result}")
    except Exception as e:
        print(f"   ❌ Failed: {type(e).__name__}: {str(e)[:100]}...")
    
    print("\n4. Fix approach 3 - Check if issue is in _prepare_input:")
    # Let's see what _prepare_input does
    from haive.agents.base.mixins.execution_mixin import ExecutionMixin
    mixin = ExecutionMixin()
    
    # Create fresh agent
    agent4 = SimpleAgent(name="test4", engine=config)
    
    # Get initial state
    initial_state = agent4.state_schema()
    print(f"\n   Initial state engine type: {type(initial_state.engine)}")
    
    # What does _prepare_input return?
    prepared = mixin._prepare_input(agent4, "test input")
    print(f"   Prepared input type: {type(prepared)}")
    
    if hasattr(prepared, 'engine'):
        print(f"   Prepared engine type: {type(prepared.engine)}")
    
    # The real fix might be to ensure model_dump is called BEFORE serialization

if __name__ == "__main__":
    asyncio.run(test_fix_approaches())