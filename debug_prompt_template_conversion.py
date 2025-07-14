#!/usr/bin/env python3
"""
COMPREHENSIVE DEBUG SCRIPT FOR PROMPT TEMPLATE CONVERSION
This script traces EVERY step where ChatPromptTemplate gets converted to dict
and where BasePromptTemplate instantiation is attempted.
"""

import logging
import sys
import traceback
import json
from typing import Any, Dict
import pdb

# Add packages to path
sys.path.insert(0, '/home/will/Projects/haive/backend/haive/packages/haive-core/src')
sys.path.insert(0, '/home/will/Projects/haive/backend/haive/packages/haive-agents/src')

# Set up EXTREMELY verbose logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)

# Enable debug for ALL haive modules
for module in [
    'haive.core.engine',
    'haive.core.schema', 
    'haive.core.persistence',
    'haive.agents.base',
    'haive.agents.simple',
    'langchain_core',
    'pydantic'
]:
    logging.getLogger(module).setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

def add_prompt_template_breakpoint():
    """Add breakpoint when BasePromptTemplate is encountered."""
    original_init = None
    
    def debug_init(self, *args, **kwargs):
        logger.error(f"🚨 BREAKPOINT: BasePromptTemplate.__init__ called!")
        logger.error(f"   Args: {args}")
        logger.error(f"   Kwargs: {kwargs}")
        logger.error(f"   Class: {self.__class__}")
        
        # Print full stack trace
        stack = traceback.extract_stack()
        logger.error(f"   FULL CALL STACK:")
        for i, frame in enumerate(stack):
            logger.error(f"     [{i}] {frame.filename}:{frame.lineno} in {frame.name}")
            logger.error(f"         {frame.line}")
        
        # Trigger debugger
        pdb.set_trace()
        
        # Call original init
        return original_init(self, *args, **kwargs)
    
    # Patch BasePromptTemplate.__init__
    from langchain_core.prompts import BasePromptTemplate
    original_init = BasePromptTemplate.__init__
    BasePromptTemplate.__init__ = debug_init
    
    logger.error("✅ Added BasePromptTemplate.__init__ breakpoint")

def trace_model_dump_calls():
    """Trace all model_dump calls that convert objects to dicts."""
    original_model_dump = None
    
    def debug_model_dump(self, *args, **kwargs):
        if hasattr(self, 'prompt_template') or 'prompt_template' in str(type(self)):
            logger.error(f"🔍 MODEL_DUMP CALL on object with prompt_template!")
            logger.error(f"   Object type: {type(self)}")
            logger.error(f"   Args: {args}")
            logger.error(f"   Kwargs: {kwargs}")
            
            if hasattr(self, 'prompt_template'):
                logger.error(f"   prompt_template type: {type(self.prompt_template)}")
                logger.error(f"   prompt_template: {self.prompt_template}")
            
            # Print stack trace
            stack = traceback.extract_stack()
            logger.error(f"   CALL STACK:")
            for frame in stack[-8:]:  # Last 8 frames
                logger.error(f"     {frame.filename}:{frame.lineno} in {frame.name}")
                logger.error(f"       {frame.line}")
            
            # Call original and check result
            result = original_model_dump(self, *args, **kwargs)
            
            if isinstance(result, dict) and 'prompt_template' in result:
                logger.error(f"   RESULT prompt_template type: {type(result['prompt_template'])}")
                logger.error(f"   RESULT prompt_template: {result['prompt_template']}")
                
                # Breakpoint for dict conversion
                if isinstance(result['prompt_template'], dict):
                    logger.error(f"🚨 PROMPT TEMPLATE CONVERTED TO DICT!")
                    pdb.set_trace()
            
            return result
        else:
            return original_model_dump(self, *args, **kwargs)
    
    # Patch BaseModel.model_dump
    from pydantic import BaseModel
    original_model_dump = BaseModel.model_dump
    BaseModel.model_dump = debug_model_dump
    
    logger.error("✅ Added model_dump tracing")

def trace_pydantic_validation():
    """Trace Pydantic validation that might trigger BasePromptTemplate creation."""
    original_validate_python = None
    
    def debug_validate_python(self, obj, *args, **kwargs):
        if 'BasePromptTemplate' in str(self) or 'prompt_template' in str(obj):
            logger.error(f"🔍 PYDANTIC VALIDATION of prompt_template!")
            logger.error(f"   Validator: {self}")
            logger.error(f"   Object type: {type(obj)}")
            logger.error(f"   Object: {obj}")
            
            # Check if obj is the problematic dict
            if isinstance(obj, dict) and all(k in obj for k in ['name', 'input_variables', 'optional_variables']):
                logger.error(f"🚨 FOUND THE PROBLEMATIC DICT!")
                logger.error(f"   Dict keys: {list(obj.keys())}")
                logger.error(f"   Dict values: {obj}")
                
                # Print stack trace
                stack = traceback.extract_stack()
                logger.error(f"   FULL VALIDATION STACK:")
                for i, frame in enumerate(stack):
                    logger.error(f"     [{i}] {frame.filename}:{frame.lineno} in {frame.name}")
                    logger.error(f"         {frame.line}")
                
                # Breakpoint before the error
                pdb.set_trace()
        
        return original_validate_python(self, obj, *args, **kwargs)
    
    # Patch TypeAdapter.validate_python
    from pydantic import TypeAdapter
    original_validate_python = TypeAdapter.validate_python
    TypeAdapter.validate_python = debug_validate_python
    
    logger.error("✅ Added Pydantic validation tracing")

def trace_serialization():
    """Trace serialization operations."""
    original_dumps = None
    
    def debug_dumps(self, obj):
        if hasattr(obj, 'prompt_template') or (isinstance(obj, dict) and 'prompt_template' in obj):
            logger.error(f"🔍 SERIALIZATION of object with prompt_template!")
            logger.error(f"   Object type: {type(obj)}")
            
            if hasattr(obj, 'prompt_template'):
                logger.error(f"   prompt_template type: {type(obj.prompt_template)}")
            elif isinstance(obj, dict) and 'prompt_template' in obj:
                logger.error(f"   prompt_template type in dict: {type(obj['prompt_template'])}")
            
            # Stack trace
            stack = traceback.extract_stack()
            logger.error(f"   SERIALIZATION STACK:")
            for frame in stack[-6:]:
                logger.error(f"     {frame.filename}:{frame.lineno} in {frame.name}")
                logger.error(f"       {frame.line}")
        
        return original_dumps(self, obj)
    
    # Patch SecureSecretStrSerializer.dumps
    from haive.core.persistence.serializers import SecureSecretStrSerializer
    original_dumps = SecureSecretStrSerializer.dumps
    SecureSecretStrSerializer.dumps = debug_dumps
    
    logger.error("✅ Added serialization tracing")

def main():
    """Run the comprehensive debug test."""
    logger.error("🚀 STARTING COMPREHENSIVE PROMPT TEMPLATE DEBUG")
    
    # Add all our debugging hooks
    add_prompt_template_breakpoint()
    trace_model_dump_calls()
    trace_pydantic_validation()
    trace_serialization()
    
    logger.error("🔧 All debug hooks installed")
    
    # Import after patching
    from typing import List
    from langchain_core.prompts import ChatPromptTemplate
    from pydantic import BaseModel, Field
    from haive.agents.simple.agent_v2 import SimpleAgentV2
    from haive.core.engine.aug_llm import AugLLMConfig
    
    # Create the same prompt template as in test_basic.py
    logger.error("📝 Creating RAG_QUERY_REFINEMENT template")
    RAG_QUERY_REFINEMENT = ChatPromptTemplate.from_messages([
        ("system", "You are an expert query optimization specialist..."),
        ("human", "Analyze and refine: {query} with context: {context}")
    ]).partial(context="")
    
    logger.error(f"✅ Created template: {type(RAG_QUERY_REFINEMENT)}")
    
    # Create the response model
    class QueryRefinementResponse(BaseModel):
        original_query: str = Field(description="The original user query")
        refined_query: str = Field(description="The refined query")
        analysis: str = Field(description="Analysis of improvements")
    
    logger.error("📊 Created QueryRefinementResponse model")
    
    # Step 1: Create AugLLMConfig (this might trigger conversion)
    logger.error("🏗️ STEP 1: Creating AugLLMConfig")
    try:
        config = AugLLMConfig(
            prompt_template=RAG_QUERY_REFINEMENT,
            structured_output_model=QueryRefinementResponse,
            structured_output_version='v2'
        )
        logger.error(f"✅ AugLLMConfig created: {type(config)}")
        logger.error(f"   Config prompt_template type: {type(config.prompt_template)}")
    except Exception as e:
        logger.error(f"❌ AugLLMConfig creation failed: {e}")
        traceback.print_exc()
        return
    
    # Step 2: Create SimpleAgentV2 (this might trigger conversion)
    logger.error("🤖 STEP 2: Creating SimpleAgentV2")
    try:
        agent = SimpleAgentV2(engine=config)
        logger.error(f"✅ Agent created: {type(agent)}")
    except Exception as e:
        logger.error(f"❌ Agent creation failed: {e}")
        traceback.print_exc()
        return
    
    # Step 3: Run the agent (this is where the error occurs)
    logger.error("🎯 STEP 3: Running agent (WHERE ERROR OCCURS)")
    try:
        result = agent.run({"query": "what is the tallest building in france"}, debug=True)
        logger.error(f"✅ Agent run successful: {result}")
    except Exception as e:
        logger.error(f"❌ AGENT RUN FAILED: {e}")
        logger.error(f"❌ ERROR TYPE: {type(e)}")
        
        # Print full traceback
        logger.error("❌ FULL TRACEBACK:")
        traceback.print_exc()
        
        # Find the exact error location
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logger.error("🎯 EXACT ERROR FRAMES:")
        for frame_info in traceback.extract_tb(exc_traceback):
            if any(keyword in str(frame_info.line).lower() for keyword in ['baseprompttemplate', 'prompt_template', 'validate_python']):
                logger.error(f"📍 CRITICAL FRAME:")
                logger.error(f"   File: {frame_info.filename}")
                logger.error(f"   Line: {frame_info.lineno}")
                logger.error(f"   Function: {frame_info.name}")
                logger.error(f"   Code: {frame_info.line}")

if __name__ == "__main__":
    main()