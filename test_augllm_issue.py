#!/usr/bin/env python3
"""Test that AugLLMConfig is the actual serialization issue."""

import asyncio
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.persistence.serializers import SecureSecretStrSerializer
import msgpack

async def test_augllm_serialization():
    """Test AugLLMConfig serialization specifically."""
    
    print("=== Testing AugLLMConfig Serialization ===\n")
    
    # Create agent
    config = AugLLMConfig(temperature=0.7)
    agent = SimpleAgent(name="test", engine=config)
    
    # Get state
    state = agent.state_schema()
    
    print(f"1. State has engine field: {hasattr(state, 'engine')}")
    print(f"   Engine value type: {type(state.engine)}")
    print(f"   Engine is AugLLMConfig: {isinstance(state.engine, AugLLMConfig)}")
    
    # Test direct msgpack
    print("\n2. Testing direct msgpack on AugLLMConfig...")
    try:
        msgpack.packb(config)
        print("   ✅ Direct msgpack succeeded (unexpected!)")
    except Exception as e:
        print(f"   ❌ Direct msgpack failed: {type(e).__name__}: {e}")
    
    # Test with model_dump
    print("\n3. Testing msgpack on dumped state...")
    dumped = state.model_dump()
    
    # Check what's in the engine field
    if 'engine' in dumped:
        print(f"   Engine in dump: {type(dumped['engine'])}")
        print(f"   Is dict: {isinstance(dumped['engine'], dict)}")
        if isinstance(dumped['engine'], dict):
            print(f"   Engine keys: {list(dumped['engine'].keys())[:5]}...")
    
    try:
        msgpack.packb(dumped)
        print("   ✅ msgpack on dumped state succeeded")
    except Exception as e:
        print(f"   ❌ msgpack on dumped state failed: {e}")
    
    # Test with SecureSecretStrSerializer
    print("\n4. Testing with SecureSecretStrSerializer...")
    serializer = SecureSecretStrSerializer()
    
    # Try the state directly
    try:
        serialized = serializer.dumps(state)
        print("   ✅ Serializer handled state object")
    except Exception as e:
        print(f"   ❌ Serializer failed on state: {e}")
    
    # The key issue: model_dump might not be called before serialization
    print("\n5. Testing state dict directly (no model_dump)...")
    
    # This is what might be happening
    state_dict = state.__dict__.copy()
    print(f"   State dict has engine: {'engine' in state_dict}")
    if 'engine' in state_dict:
        print(f"   Engine type in __dict__: {type(state_dict['engine'])}")
    
    try:
        msgpack.packb(state_dict)
        print("   ✅ msgpack on state.__dict__ succeeded")
    except Exception as e:
        print(f"   ❌ msgpack on state.__dict__ failed: {e}")
        if "AugLLMConfig" in str(e):
            print("\n   🎯 FOUND THE ISSUE!")
            print("   The state.__dict__ contains the actual AugLLMConfig object")
            print("   This happens when the state is serialized before model_dump()")

if __name__ == "__main__":
    asyncio.run(test_augllm_serialization())