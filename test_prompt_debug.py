#!/usr/bin/env python3
"""Debug script to trace BasePromptTemplate serialization issue step by step."""

import os
import sys
import traceback

# Add the packages to Python path
sys.path.insert(0, '/home/will/Projects/haive/backend/haive/packages/haive-core/src')
sys.path.insert(0, '/home/will/Projects/haive/backend/haive/packages/haive-agents/src')

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.persistence.serializers import SecureSecretStrSerializer
from langchain_core.prompts import ChatPromptTemplate, BasePromptTemplate

def step_1_create_config():
    """Step 1: Create AugLLMConfig with prompt template."""
    print("=== STEP 1: Creating AugLLMConfig with ChatPromptTemplate ===")
    
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("human", "{input}")
    ])
    
    config = AugLLMConfig(
        name="test_config",
        prompt_template=chat_prompt
    )
    
    print(f"✅ Config created successfully")
    print(f"   prompt_template type: {type(config.prompt_template)}")
    print(f"   prompt_template: {repr(config.prompt_template)}")
    
    return config

def step_2_test_model_dump(config):
    """Step 2: Test model_dump serialization."""
    print("\n=== STEP 2: Testing model_dump() ===")
    
    try:
        dumped = config.model_dump()
        print(f"✅ model_dump() successful")
        print(f"   prompt_template type: {type(dumped.get('prompt_template'))}")
        prompt_template_data = dumped.get('prompt_template')
        if isinstance(prompt_template_data, dict):
            print(f"   prompt_template keys: {list(prompt_template_data.keys())}")
        else:
            print(f"   prompt_template: {repr(prompt_template_data)}")
        return dumped
    except Exception as e:
        print(f"❌ model_dump() failed: {e}")
        traceback.print_exc()
        return None

def step_3_test_serialization(config):
    """Step 3: Test SecureSecretStrSerializer."""
    print("\n=== STEP 3: Testing SecureSecretStrSerializer ===")
    
    serializer = SecureSecretStrSerializer()
    
    try:
        # Serialize
        serialized = serializer.dumps(config)
        print(f"✅ Serialization successful: {len(serialized)} bytes")
        
        # Deserialize
        deserialized = serializer.loads(serialized)
        print(f"✅ Deserialization successful")
        print(f"   Type: {type(deserialized)}")
        print(f"   prompt_template type: {type(deserialized.prompt_template) if hasattr(deserialized, 'prompt_template') else 'No prompt_template attr'}")
        
        if hasattr(deserialized, 'prompt_template') and deserialized.prompt_template:
            print(f"   prompt_template: {repr(deserialized.prompt_template)}")
        
        return deserialized
        
    except Exception as e:
        print(f"❌ Serialization failed: {e}")
        traceback.print_exc()
        return None

def step_4_test_recreate_from_dict(dumped_data):
    """Step 4: Test recreating AugLLMConfig from dumped dict."""
    print("\n=== STEP 4: Testing recreation from dict ===")
    
    if dumped_data is None:
        print("❌ No dumped data to test with")
        return None
    
    try:
        # Try to create AugLLMConfig from the dumped dict
        recreated = AugLLMConfig(**dumped_data)
        print(f"✅ Recreation from dict successful")
        print(f"   Type: {type(recreated)}")
        print(f"   prompt_template type: {type(recreated.prompt_template) if hasattr(recreated, 'prompt_template') else 'No prompt_template attr'}")
        
        if hasattr(recreated, 'prompt_template') and recreated.prompt_template:
            print(f"   prompt_template: {repr(recreated.prompt_template)}")
        
        return recreated
        
    except Exception as e:
        print(f"❌ Recreation from dict failed: {e}")
        traceback.print_exc()
        return None

def step_5_test_isinstance_checks(config):
    """Step 5: Test isinstance checks that might be failing."""
    print("\n=== STEP 5: Testing isinstance checks ===")
    
    if config is None or not hasattr(config, 'prompt_template'):
        print("❌ No config to test with")
        return
    
    prompt_template = config.prompt_template
    
    print(f"prompt_template is ChatPromptTemplate: {isinstance(prompt_template, ChatPromptTemplate)}")
    print(f"prompt_template is BasePromptTemplate: {isinstance(prompt_template, BasePromptTemplate)}")
    print(f"prompt_template is dict: {isinstance(prompt_template, dict)}")
    print(f"prompt_template type: {type(prompt_template)}")
    
    # Test some of the actual isinstance checks from the code
    if isinstance(prompt_template, ChatPromptTemplate):
        print("✅ ChatPromptTemplate isinstance check passes")
    else:
        print("❌ ChatPromptTemplate isinstance check fails")
    
    if hasattr(prompt_template, '__dict__'):
        print(f"   prompt_template attributes: {list(prompt_template.__dict__.keys()) if hasattr(prompt_template, '__dict__') else 'No __dict__'}")

def step_6_test_model_validator(config):
    """Step 6: Test if model validators are triggered."""
    print("\n=== STEP 6: Testing model validators ===")
    
    if config is None:
        print("❌ No config to test with")
        return
    
    try:
        # Try to trigger model validation by accessing properties
        print(f"Accessing name: {config.name}")
        print(f"Accessing prompt_template: {config.prompt_template}")
        
        # Try to trigger any lazy initialization
        if hasattr(config, '_validate_and_setup'):
            print("Calling _validate_and_setup...")
            config._validate_and_setup()
            
        print("✅ Model validator tests passed")
        
    except Exception as e:
        print(f"❌ Model validator test failed: {e}")
        traceback.print_exc()

def main():
    """Main debug workflow."""
    print("🔍 DEBUGGING PROMPT TEMPLATE SERIALIZATION ISSUE")
    
    # Step 1: Create config
    original_config = step_1_create_config()
    
    # Step 2: Test model_dump
    dumped_data = step_2_test_model_dump(original_config)
    
    # Step 3: Test serialization/deserialization
    deserialized_config = step_3_test_serialization(original_config)
    
    # Step 4: Test recreation from dict
    recreated_config = step_4_test_recreate_from_dict(dumped_data)
    
    # Step 5: Test isinstance checks on different configs
    print("\n=== ISINSTANCE CHECKS COMPARISON ===")
    print("Original config:")
    step_5_test_isinstance_checks(original_config)
    
    print("\nDeserialized config:")
    step_5_test_isinstance_checks(deserialized_config)
    
    print("\nRecreated from dict config:")
    step_5_test_isinstance_checks(recreated_config)
    
    # Step 6: Test model validators
    step_6_test_model_validator(deserialized_config)
    
    print("\n🎯 SUMMARY:")
    print(f"Original prompt_template type: {type(original_config.prompt_template) if original_config else 'Failed'}")
    print(f"Deserialized prompt_template type: {type(deserialized_config.prompt_template) if deserialized_config and hasattr(deserialized_config, 'prompt_template') else 'Failed/Missing'}")
    print(f"Recreated prompt_template type: {type(recreated_config.prompt_template) if recreated_config and hasattr(recreated_config, 'prompt_template') else 'Failed/Missing'}")

if __name__ == "__main__":
    main()