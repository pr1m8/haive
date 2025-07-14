#!/usr/bin/env python3
"""Test script to reproduce BasePromptTemplate serialization issue."""

import os
import sys

# Add the packages to Python path
sys.path.insert(0, '/home/will/Projects/haive/backend/haive/packages/haive-core/src')
sys.path.insert(0, '/home/will/Projects/haive/backend/haive/packages/haive-agents/src')

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.persistence.serializers import SecureSecretStrSerializer
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

def test_prompt_template_serialization():
    """Test serializing AugLLMConfig with prompt templates."""
    
    # Create a simple chat prompt template
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("human", "{input}")
    ])
    
    # Create AugLLMConfig with prompt template
    config = AugLLMConfig(
        name="test_config",
        prompt_template=chat_prompt
    )
    
    print(f"Original prompt_template type: {type(config.prompt_template)}")
    print(f"Original prompt_template: {config.prompt_template}")
    
    # Test model_dump
    try:
        dumped = config.model_dump()
        print(f"model_dump() prompt_template type: {type(dumped.get('prompt_template'))}")
        print(f"model_dump() prompt_template: {dumped.get('prompt_template')}")
    except Exception as e:
        print(f"Error in model_dump(): {e}")
    
    # Test serializer
    serializer = SecureSecretStrSerializer()
    
    try:
        # Test serializing the config object
        serialized = serializer.dumps(config)
        print(f"Serialization successful: {len(serialized)} bytes")
        
        # Test deserializing
        deserialized = serializer.loads(serialized)
        print(f"Deserialization successful: {type(deserialized)}")
        print(f"Deserialized prompt_template type: {type(deserialized.prompt_template) if hasattr(deserialized, 'prompt_template') else 'No prompt_template attr'}")
        
    except Exception as e:
        print(f"Serialization error: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_prompt_template_serialization()