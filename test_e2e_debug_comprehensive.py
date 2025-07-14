#!/usr/bin/env python3
"""
Comprehensive end-to-end test with detailed logging at every step.
This will trace the exact location where BasePromptTemplate serialization fails.
"""

import logging
import sys
import traceback
from typing import Any, Dict

# Add the packages to Python path
sys.path.insert(0, '/home/will/Projects/haive/backend/haive/packages/haive-core/src')
sys.path.insert(0, '/home/will/Projects/haive/backend/haive/packages/haive-agents/src')

# Set up comprehensive logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Enable debug logging for specific modules
logging.getLogger('haive.core.schema').setLevel(logging.DEBUG)
logging.getLogger('haive.core.persistence').setLevel(logging.DEBUG)
logging.getLogger('haive.agents.base.mixins').setLevel(logging.DEBUG)
logging.getLogger('haive.core.engine').setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

def log_object_details(obj: Any, name: str, step: str):
    """Log detailed information about an object."""
    logger.info(f"\n=== {step}: {name} ===")
    logger.info(f"Type: {type(obj)}")
    
    if hasattr(obj, '__dict__'):
        logger.info(f"Attributes: {list(obj.__dict__.keys())}")
    
    if hasattr(obj, 'prompt_template'):
        prompt_template = obj.prompt_template
        logger.info(f"prompt_template type: {type(prompt_template)}")
        logger.info(f"prompt_template: {repr(prompt_template)}")
        
        # Check if it's a LangChain Serializable
        if hasattr(prompt_template, '__class__') and hasattr(prompt_template.__class__, '__mro__'):
            for cls in prompt_template.__class__.__mro__:
                if 'Serializable' in cls.__name__:
                    logger.info(f"✅ Found Serializable in MRO: {cls}")
                    break
            else:
                logger.warning(f"❌ No Serializable found in MRO: {prompt_template.__class__.__mro__}")
    
    if hasattr(obj, 'model_dump'):
        try:
            dumped = obj.model_dump()
            logger.info(f"model_dump() successful")
            if 'prompt_template' in dumped:
                logger.info(f"model_dump prompt_template type: {type(dumped['prompt_template'])}")
                logger.info(f"model_dump prompt_template: {dumped['prompt_template']}")
        except Exception as e:
            logger.error(f"model_dump() failed: {e}")

def test_schema_composer():
    """Test SchemaComposer step by step."""
    logger.info("\n🔍 TESTING SCHEMA COMPOSER")
    
    try:
        from haive.core.engine.aug_llm import AugLLMConfig
        from haive.core.schema.composer import SchemaComposer
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.tools import tool
        
        # Create a simple tool
        @tool
        def calc_add(a: int, b: int) -> str:
            """Add two numbers."""
            return str(a + b)
        
        # Create ChatPromptTemplate
        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant."),
            ("human", "{input}")
        ])
        
        log_object_details(chat_prompt, "ChatPromptTemplate", "STEP 1: Create ChatPromptTemplate")
        
        # Create AugLLMConfig
        config = AugLLMConfig(
            prompt_template=chat_prompt,
            tools=[calc_add]
        )
        
        log_object_details(config, "AugLLMConfig", "STEP 2: Create AugLLMConfig")
        
        # Test SchemaComposer
        logger.info("\n🔍 STEP 3: SchemaComposer.from_components")
        schema_class = SchemaComposer.from_components(config)
        logger.info(f"✅ Schema created: {schema_class}")
        
        # Create schema instance
        logger.info("\n🔍 STEP 4: Create schema instance")
        schema_instance = schema_class()
        log_object_details(schema_instance, "Schema Instance", "STEP 4: Schema Instance Created")
        
        return config, schema_class, schema_instance
        
    except Exception as e:
        logger.error(f"❌ Schema Composer test failed: {e}")
        traceback.print_exc()
        return None, None, None

def test_serialization(config, schema_instance):
    """Test serialization step by step."""
    logger.info("\n🔍 TESTING SERIALIZATION")
    
    try:
        from haive.core.persistence.serializers import SecureSecretStrSerializer
        
        # Test serializing the config directly
        logger.info("\n🔍 STEP 5: Serialize AugLLMConfig directly")
        serializer = SecureSecretStrSerializer()
        
        config_serialized = serializer.dumps(config)
        logger.info(f"✅ Config serialized: {len(config_serialized)} bytes")
        
        # Test deserializing the config
        logger.info("\n🔍 STEP 6: Deserialize AugLLMConfig")
        config_deserialized = serializer.loads(config_serialized)
        log_object_details(config_deserialized, "Deserialized Config", "STEP 6: Config Deserialized")
        
        # Test serializing the schema instance
        logger.info("\n🔍 STEP 7: Serialize schema instance")
        schema_serialized = serializer.dumps(schema_instance)
        logger.info(f"✅ Schema serialized: {len(schema_serialized)} bytes")
        
        # Test deserializing the schema
        logger.info("\n🔍 STEP 8: Deserialize schema instance")
        schema_deserialized = serializer.loads(schema_serialized)
        log_object_details(schema_deserialized, "Deserialized Schema", "STEP 8: Schema Deserialized")
        
        return config_deserialized, schema_deserialized
        
    except Exception as e:
        logger.error(f"❌ Serialization test failed: {e}")
        traceback.print_exc()
        return None, None

def test_agent_creation():
    """Test agent creation and execution step by step."""
    logger.info("\n🔍 TESTING AGENT CREATION AND EXECUTION")
    
    try:
        from haive.agents.react.agent import ReactAgent
        from haive.core.engine.aug_llm import AugLLMConfig
        from langchain_core.tools import tool
        
        @tool
        def calc_add(a: int, b: int) -> str:
            """Add two numbers."""
            return str(a + b)
        
        # Create engine config
        logger.info("\n🔍 STEP 9: Create AugLLMConfig for agent")
        engine_config = AugLLMConfig(tools=[calc_add])
        log_object_details(engine_config, "Agent Engine Config", "STEP 9: Agent Engine Created")
        
        # Create ReactAgent
        logger.info("\n🔍 STEP 10: Create ReactAgent")
        agent = ReactAgent(
            name="debug_agent",
            engine=engine_config
        )
        logger.info(f"✅ Agent created: {agent}")
        
        # Check agent state schema
        logger.info("\n🔍 STEP 11: Check agent state schema")
        if hasattr(agent, 'state_schema'):
            logger.info(f"Agent state schema: {agent.state_schema}")
            logger.info(f"State schema fields: {agent.state_schema.model_fields.keys()}")
        
        # Try to create initial state
        logger.info("\n🔍 STEP 12: Create initial state")
        initial_state = agent.state_schema()
        log_object_details(initial_state, "Initial State", "STEP 12: Initial State Created")
        
        return agent, initial_state
        
    except Exception as e:
        logger.error(f"❌ Agent creation test failed: {e}")
        traceback.print_exc()
        return None, None

def test_execution_mixin(agent):
    """Test execution mixin step by step."""
    logger.info("\n🔍 TESTING EXECUTION MIXIN")
    
    try:
        # Test _prepare_input
        logger.info("\n🔍 STEP 13: Test _prepare_input")
        prepared_input = agent._prepare_input("What is 2 + 2?")
        logger.info(f"✅ Prepared input: {type(prepared_input)}")
        log_object_details(prepared_input, "Prepared Input", "STEP 13: Input Prepared")
        
        # Check if prepared input has engine field
        if hasattr(prepared_input, 'engine'):
            log_object_details(prepared_input.engine, "Prepared Input Engine", "STEP 13a: Engine in Prepared Input")
        
        return prepared_input
        
    except Exception as e:
        logger.error(f"❌ Execution mixin test failed: {e}")
        traceback.print_exc()
        return None

def test_state_reconstruction():
    """Test state reconstruction from dict."""
    logger.info("\n🔍 TESTING STATE RECONSTRUCTION FROM DICT")
    
    try:
        from haive.core.engine.aug_llm import AugLLMConfig
        from langchain_core.prompts import ChatPromptTemplate
        
        # Create a dict that simulates serialized state
        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant."),
            ("human", "{input}")
        ])
        
        config = AugLLMConfig(prompt_template=chat_prompt)
        
        # Simulate what happens in serialization
        logger.info("\n🔍 STEP 14: model_dump() to create dict")
        config_dict = config.model_dump()
        logger.info(f"Config dict prompt_template type: {type(config_dict['prompt_template'])}")
        logger.info(f"Config dict prompt_template: {config_dict['prompt_template']}")
        
        # Try to reconstruct AugLLMConfig from dict
        logger.info("\n🔍 STEP 15: Reconstruct AugLLMConfig from dict")
        reconstructed_config = AugLLMConfig(**config_dict)
        log_object_details(reconstructed_config, "Reconstructed Config", "STEP 15: Config Reconstructed")
        
        return reconstructed_config
        
    except Exception as e:
        logger.error(f"❌ State reconstruction test failed: {e}")
        traceback.print_exc()
        return None

def main():
    """Run comprehensive end-to-end test."""
    logger.info("🚀 STARTING COMPREHENSIVE END-TO-END DEBUG TEST")
    
    # Test 1: Schema Composer
    config, schema_class, schema_instance = test_schema_composer()
    if not config:
        logger.error("❌ Schema Composer test failed, stopping")
        return
    
    # Test 2: Serialization
    config_deserialized, schema_deserialized = test_serialization(config, schema_instance)
    
    # Test 3: Agent Creation
    agent, initial_state = test_agent_creation()
    if not agent:
        logger.error("❌ Agent creation test failed, stopping")
        return
    
    # Test 4: Execution Mixin
    prepared_input = test_execution_mixin(agent)
    
    # Test 5: State Reconstruction
    reconstructed_config = test_state_reconstruction()
    
    # Test 6: Try to run the agent (this is where the error should occur)
    logger.info("\n🔍 STEP 16: FINAL TEST - Run agent (where error occurs)")
    try:
        result = agent.run("What is 2 + 2?", debug=True)
        logger.info(f"✅ SUCCESS: Agent ran successfully: {result}")
    except Exception as e:
        logger.error(f"❌ FINAL ERROR: {e}")
        logger.error(f"❌ ERROR TYPE: {type(e)}")
        logger.error("❌ FULL TRACEBACK:")
        traceback.print_exc()
        
        # Try to get more specific information about where it failed
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logger.error("\n🎯 EXACT ERROR LOCATION:")
        for frame_info in traceback.extract_tb(exc_traceback):
            if 'BasePromptTemplate' in str(frame_info.line) or 'prompt_template' in str(frame_info.filename).lower():
                logger.error(f"📍 CRITICAL FRAME:")
                logger.error(f"   File: {frame_info.filename}")
                logger.error(f"   Line: {frame_info.lineno}")
                logger.error(f"   Function: {frame_info.name}")
                logger.error(f"   Code: {frame_info.line}")

if __name__ == "__main__":
    main()