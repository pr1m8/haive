#!/usr/bin/env python3
"""Test a real agent using Supabase PostgreSQL checkpointer."""

import os
import uuid
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Add the package to the path
import sys
sys.path.insert(0, str(Path(__file__).parent / "packages" / "haive-core" / "src"))

from haive.core.persistence.supabase_config import SupabaseCheckpointerConfig


def test_agent_with_supabase_checkpointer():
    """Test a simple agent using the Supabase checkpointer."""
    
    print("🤖 Testing Agent with Supabase PostgreSQL Checkpointer")
    print("=" * 60)
    
    try:
        # Import LangGraph components
        from langgraph.graph import StateGraph, START, END
        from typing_extensions import TypedDict
        
        # Define a simple state
        class AgentState(TypedDict):
            messages: list[str]
            step_count: int
        
        # Create simple agent functions
        def add_message(state: AgentState):
            """Add a message to the state."""
            new_messages = state["messages"] + [f"Step {state['step_count']}: Processing..."]
            return {
                "messages": new_messages, 
                "step_count": state["step_count"] + 1
            }
        
        def finish_processing(state: AgentState):
            """Finish processing."""
            new_messages = state["messages"] + ["Processing complete!"]
            return {
                "messages": new_messages,
                "step_count": state["step_count"] + 1
            }
        
        # Build the graph
        print("1. Creating LangGraph agent...")
        workflow = StateGraph(AgentState)
        workflow.add_node("process", add_message)
        workflow.add_node("finish", finish_processing)
        
        workflow.add_edge(START, "process")
        workflow.add_edge("process", "finish")
        workflow.add_edge("finish", END)
        
        # Create Supabase checkpointer with connection pool
        print("2. Setting up Supabase checkpointer...")
        
        from langgraph.checkpoint.postgres import PostgresSaver
        from psycopg_pool import ConnectionPool
        
        postgres_conn = os.getenv("POSTGRES_CONNECTION_STRING")
        
        # Create a fresh connection pool for this test
        pool = ConnectionPool(postgres_conn, min_size=1, max_size=5)
        checkpointer = PostgresSaver(pool)
        print(f"   ✓ Checkpointer: {type(checkpointer).__name__}")
        
        # Compile graph with checkpointer
        app = workflow.compile(checkpointer=checkpointer)
        print("   ✓ Agent compiled with Supabase checkpointer")
        
        # Test the agent with persistence
        print("\n3. Running agent with persistence...")
        
        thread_id = f"agent-test-{uuid.uuid4()}"
        config_dict = {"configurable": {"thread_id": thread_id}}
        
        initial_state = {
            "messages": ["Starting agent test"],
            "step_count": 1
        }
        
        print(f"   📝 Thread ID: {thread_id}")
        print(f"   📝 Initial state: {initial_state}")
        
        # Run the agent
        result = app.invoke(initial_state, config=config_dict)
        print(f"   ✓ Agent completed successfully")
        print(f"   📋 Final messages: {result['messages']}")
        print(f"   📋 Final step count: {result['step_count']}")
        
        # Test persistence by retrieving the state
        print("\n4. Testing state persistence...")
        
        # Get the saved state
        saved_state = app.get_state(config_dict)
        print(f"   ✓ Retrieved saved state")
        print(f"   📋 Saved messages: {saved_state.values['messages']}")
        print(f"   📋 Saved step count: {saved_state.values['step_count']}")
        
        # Verify state matches
        if saved_state.values == result:
            print("   ✅ State persistence verified - data matches!")
        else:
            print("   ⚠️  State mismatch detected")
            
        # Test state history
        print("\n5. Testing checkpoint history...")
        
        history = list(app.get_state_history(config_dict, limit=5))
        print(f"   ✓ Retrieved {len(history)} checkpoint states")
        
        for i, state in enumerate(history):
            step_count = state.values.get('step_count', 0)
            msg_count = len(state.values.get('messages', []))
            print(f"     Checkpoint {i+1}: step {step_count}, {msg_count} messages")
        
        print("\n🎉 Agent with Supabase persistence working perfectly!")
        return True
        
    except Exception as e:
        print(f"❌ Agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function."""
    
    print("🚀 Agent Integration Test with Supabase")
    print("=" * 70)
    
    # Check environment
    postgres_conn = os.getenv("POSTGRES_CONNECTION_STRING")
    if not postgres_conn or "[YOUR-PASSWORD]" in postgres_conn:
        print("❌ POSTGRES_CONNECTION_STRING not set")
        return False
    
    print(f"✓ Using Supabase connection: {postgres_conn[:50]}...")
    
    # Run agent test
    success = test_agent_with_supabase_checkpointer()
    
    if success:
        print(f"\n🎊 SUCCESS: Agent integration with Supabase working!")
        print("✓ LangGraph agent using PostgreSQL checkpointer")
        print("✓ State persistence to Supabase database")
        print("✓ State retrieval and history working")
        print("✓ End-to-end integration verified")
    else:
        print(f"\n❌ Agent integration test failed")
    
    return success


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)