#!/usr/bin/env python3
"""Reproduce the exact PydanticUndefined serialization issue."""

import os
import asyncio
from pydantic import BaseModel, Field
from pydantic_core import PydanticUndefined
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
import logging
import traceback

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Patch to catch the exact error
import msgpack
original_packb = msgpack.packb
call_count = 0

def patched_packb(o, **kwargs):
    """Catch PydanticUndefined in msgpack."""
    global call_count
    call_count += 1
    
    def find_undefined(obj, path=""):
        if obj is PydanticUndefined:
            print(f"\n❌ FOUND PydanticUndefined at path: {path}")
            print(f"   Call #{call_count} to msgpack.packb")
            print("   Stack trace (last 15 frames):")
            for line in traceback.format_stack()[-15:-1]:
                if '/haive/' in line:
                    print(f"   {line.strip()}")
            return True
        elif isinstance(obj, dict):
            for k, v in obj.items():
                if find_undefined(v, f"{path}.{k}" if path else k):
                    return True
        elif isinstance(obj, (list, tuple)):
            for i, v in enumerate(obj):
                if find_undefined(v, f"{path}[{i}]"):
                    return True
        return False
    
    if find_undefined(o):
        print(f"\n📍 Object being serialized has type: {type(o)}")
        if isinstance(o, dict) and 'messages' in o:
            print(f"   Looks like state dict with keys: {list(o.keys())[:10]}...")
    
    return original_packb(o, **kwargs)

msgpack.packb = patched_packb

class TaskOutput(BaseModel):
    """Structured output model."""
    task: str = Field(..., description="Task description")
    priority: str = Field(default="medium", description="Priority level")

async def test_exact_issue():
    """Reproduce the exact issue."""
    
    print("=== Reproducing PydanticUndefined Serialization Issue ===\n")
    
    # Create agent with structured output (like you have)
    config = AugLLMConfig(
        temperature=0.7,
        structured_output_model=TaskOutput,
        structured_output_version="v2"
    )
    
    agent = SimpleAgent(
        name="task_agent",
        engine=config
    )
    
    print(f"✅ Agent created with checkpointer: {type(agent.checkpointer).__name__ if agent.checkpointer else 'None'}")
    
    # Check initial state
    print("\n1. Checking initial state creation...")
    state = agent.state_schema()
    
    # Manual check for PydanticUndefined
    print("\n2. Checking state fields manually...")
    undefined_fields = []
    for field_name, field_info in state.__class__.model_fields.items():
        try:
            value = getattr(state, field_name)
            if value is PydanticUndefined:
                undefined_fields.append(field_name)
                print(f"   ❌ {field_name} = PydanticUndefined")
        except AttributeError:
            print(f"   ⚠️  {field_name} - AttributeError")
    
    if undefined_fields:
        print(f"\n⚠️  Found {len(undefined_fields)} PydanticUndefined fields BEFORE execution!")
    else:
        print("\n✅ No PydanticUndefined fields in initial state")
    
    # Now try to run with persistence
    print("\n3. Running agent with persistence enabled...")
    try:
        # Use thread_id to trigger checkpointing
        config = {"configurable": {"thread_id": "test-thread-123"}}
        
        # This should trigger the issue
        result = await agent.arun("Create a high priority task for testing the system", config=config)
        
        print(f"\n✅ Agent execution succeeded!")
        print(f"   Result: {result}")
        
    except Exception as e:
        print(f"\n❌ Agent execution failed!")
        print(f"   Error type: {type(e).__name__}")
        print(f"   Error message: {str(e)}")
        
        if "PydanticUndefined" in str(e) or "msgpack" in str(e):
            print("\n🎯 REPRODUCED THE ISSUE!")
            print("   This confirms PydanticUndefined is being serialized")
        
        # Don't print full traceback, we have our custom one
    
    print(f"\n📊 Total msgpack.packb calls: {call_count}")

async def test_workaround():
    """Test potential workarounds."""
    
    print("\n\n=== Testing Workarounds ===\n")
    
    # Workaround 1: Disable checkpointing
    print("1. Testing with checkpointing disabled...")
    config = AugLLMConfig(temperature=0.7, structured_output_model=TaskOutput)
    agent = SimpleAgent(name="test_no_checkpoint", engine=config)
    agent.checkpointer = None
    
    try:
        result = await agent.arun("Test without checkpointing")
        print("   ✅ Success without checkpointing!")
    except Exception as e:
        print(f"   ❌ Still failed: {e}")
    
    # Workaround 2: Force state initialization
    print("\n2. Testing with forced state initialization...")
    agent2 = SimpleAgent(name="test_forced_init", engine=config)
    
    # Force initialize state
    state = agent2.state_schema()
    _ = state.model_dump()  # Force all fields to initialize
    
    try:
        result = await agent2.arun("Test with forced init", config={"configurable": {"thread_id": "test2"}})
        print("   ✅ Success with forced initialization!")
    except Exception as e:
        print(f"   ❌ Still failed: {e}")

if __name__ == "__main__":
    print("Database URL:", "SET" if os.getenv("DATABASE_URL") else "NOT SET")
    asyncio.run(test_exact_issue())
    asyncio.run(test_workaround())