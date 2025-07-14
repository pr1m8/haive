#!/usr/bin/env python3
"""Understand the exact serialization flow and where it breaks."""

import asyncio
from pydantic import BaseModel, Field
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.persistence.serializers import SecureSecretStrSerializer
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
import msgpack

def analyze_object(obj, name):
    """Analyze what's in an object for serialization."""
    print(f"\n=== Analyzing {name} ===")
    print(f"Type: {type(obj)}")
    
    if isinstance(obj, dict):
        print(f"Dict with {len(obj)} keys")
        for key, value in list(obj.items())[:5]:
            print(f"  {key}: {type(value).__name__}")
            if key == 'engine' and hasattr(value, '__class__'):
                print(f"    -> {value.__class__}")
    elif hasattr(obj, '__dict__'):
        print(f"Object with __dict__:")
        for key, value in list(obj.__dict__.items())[:10]:
            if not key.startswith('_'):
                print(f"  {key}: {type(value).__name__}")
                if key == 'engine' and hasattr(value, '__class__'):
                    print(f"    -> {value.__class__}")

async def test_serialization_flow():
    """Test the exact serialization flow."""
    
    print("=== Testing Serialization Flow ===\n")
    
    # Create agent
    config = AugLLMConfig(temperature=0.7)
    agent = SimpleAgent(name="test", engine=config)
    state = agent.state_schema()
    
    # 1. State object itself
    analyze_object(state, "State object")
    
    # 2. State.__dict__
    analyze_object(state.__dict__, "State.__dict__")
    
    # 3. State.model_dump()
    dumped = state.model_dump()
    analyze_object(dumped, "State.model_dump()")
    
    # 4. Test different serializers
    print("\n=== Testing Serializers ===")
    
    # Basic JsonPlusSerializer (what LangGraph uses by default)
    print("\n1. JsonPlusSerializer (default):")
    basic_serializer = JsonPlusSerializer()
    try:
        basic_serializer.dumps(state)
        print("   ✅ Can serialize state object directly")
    except Exception as e:
        print(f"   ❌ Cannot serialize state: {e}")
    
    try:
        basic_serializer.dumps(state.__dict__)
        print("   ✅ Can serialize state.__dict__")
    except Exception as e:
        print(f"   ❌ Cannot serialize state.__dict__: {e}")
    
    try:
        basic_serializer.dumps(dumped)
        print("   ✅ Can serialize model_dump()")
    except Exception as e:
        print(f"   ❌ Cannot serialize model_dump(): {e}")
    
    # SecureSecretStrSerializer
    print("\n2. SecureSecretStrSerializer:")
    secure_serializer = SecureSecretStrSerializer()
    try:
        secure_serializer.dumps(state)
        print("   ✅ Can serialize state object directly")
    except Exception as e:
        print(f"   ❌ Cannot serialize state: {e}")
    
    # 5. Find what needs to be fixed
    print("\n=== Issue Summary ===")
    print("The 'engine' field contains an AugLLMConfig object")
    print("This needs to be converted to a dict before serialization")
    print("But the execution mixin is trying to serialize before model_dump()")
    
    # Check if engines dict has the same issue
    if hasattr(state, 'engines') and state.engines:
        print(f"\nAlso checking 'engines' dict:")
        for name, engine in state.engines.items():
            print(f"  {name}: {type(engine).__name__}")

if __name__ == "__main__":
    asyncio.run(test_serialization_flow())