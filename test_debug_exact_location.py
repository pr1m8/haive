#!/usr/bin/env python3
"""Debug script to find EXACT location of remaining serialization issues."""

import os
import sys
import traceback
import logging

# Add the packages to Python path
sys.path.insert(0, '/home/will/Projects/haive/backend/haive/packages/haive-core/src')
sys.path.insert(0, '/home/will/Projects/haive/backend/haive/packages/haive-agents/src')

# Enable all debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def run_react_agent_with_debug():
    """Run ReactAgent test with full debug tracing."""
    
    print("🔍 STARTING EXACT LOCATION DEBUG")
    
    try:
        # Import and run the exact same test
        from haive.agents.react.agent import ReactAgent
        from haive.core.engine.aug_llm import AugLLMConfig
        from langchain_core.tools import tool
        
        print("✅ Imports successful")
        
        # Create the tool
        @tool
        def calc_add(a: int, b: int) -> int:
            """Add two numbers."""
            return a + b
        
        print("✅ Tool created")
        
        # Create engine config
        engine_config = AugLLMConfig(tools=[calc_add])
        print("✅ Engine config created")
        
        # Create ReactAgent
        agent = ReactAgent(
            name="debug_agent",
            engine=engine_config
        )
        print("✅ ReactAgent created")
        
        # Try to run the agent - this is where the error should occur
        print("🎯 About to run agent - setting up debug hooks...")
        
        # Patch the agent execution to catch exact error location
        original_run = agent.run
        original_arun = agent.arun
        
        def debug_run(*args, **kwargs):
            print(f"🔍 DEBUG: agent.run called with args={args}, kwargs={kwargs}")
            try:
                return original_run(*args, **kwargs)
            except Exception as e:
                print(f"❌ ERROR in agent.run: {e}")
                print(f"❌ ERROR type: {type(e)}")
                print("❌ FULL TRACEBACK:")
                traceback.print_exc()
                raise
        
        def debug_arun(*args, **kwargs):
            print(f"🔍 DEBUG: agent.arun called with args={args}, kwargs={kwargs}")
            try:
                return original_arun(*args, **kwargs)
            except Exception as e:
                print(f"❌ ERROR in agent.arun: {e}")
                print(f"❌ ERROR type: {type(e)}")
                print("❌ FULL TRACEBACK:")
                traceback.print_exc()
                raise
        
        agent.run = debug_run
        agent.arun = debug_arun
        
        # Now try to run
        print("🚀 Executing agent.run('What is 2 + 2?')")
        result = agent.run("What is 2 + 2?")
        print(f"✅ SUCCESS: {result}")
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        print(f"❌ ERROR TYPE: {type(e)}")
        print("❌ DETAILED TRACEBACK:")
        
        # Get the full traceback
        tb = traceback.format_exc()
        print(tb)
        
        # Try to pinpoint the exact line
        import traceback as tb_module
        exc_type, exc_value, exc_traceback = sys.exc_info()
        
        print("\n🎯 EXACT ERROR LOCATION ANALYSIS:")
        for frame_info in traceback.extract_tb(exc_traceback):
            print(f"📍 File: {frame_info.filename}")
            print(f"   Line: {frame_info.lineno}")
            print(f"   Function: {frame_info.name}")
            print(f"   Code: {frame_info.line}")
            print()

if __name__ == "__main__":
    run_react_agent_with_debug()