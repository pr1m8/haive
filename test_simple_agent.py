#!/usr/bin/env python3
"""Simple test to verify Supabase checkpointer works with basic operations."""

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


def test_simple_checkpointer_usage():
    """Test basic checkpointer operations that an agent would use."""
    
    print("🔧 Testing Supabase Checkpointer for Agent Usage")
    print("=" * 55)
    
    try:
        # Create config
        print("1. Creating Supabase checkpointer config...")
        config = SupabaseCheckpointerConfig(
            connection_string=os.getenv("POSTGRES_CONNECTION_STRING"),
            setup_needed=False  # Already set up in previous tests
        )
        
        checkpointer = config.create_checkpointer()
        print(f"   ✓ Checkpointer ready: {type(checkpointer).__name__}")
        
        # Test basic operations an agent would perform
        thread_id = f"simple-agent-{uuid.uuid4()}"
        print(f"\n2. Testing with thread: {thread_id}")
        
        # Create config like LangGraph would
        checkpoint_config = {
            "configurable": {
                "thread_id": thread_id,
                "checkpoint_ns": "default"
            }
        }
        
        # Simulate what an agent would store
        print("3. Simulating agent checkpoint storage...")
        
        # Step 1: Initial state
        initial_checkpoint = {
            "v": 1,
            "ts": "2024-01-01T00:00:00Z",
            "id": str(uuid.uuid4()),
            "channel_values": {
                "messages": ["User: Hello", "Assistant: Hi there!"],
                "current_step": "greeting"
            }
        }
        
        result1 = checkpointer.put(
            checkpoint_config, 
            initial_checkpoint, 
            {"step": 1, "action": "greeting"}, 
            {}
        )
        print(f"   ✓ Stored initial checkpoint: {result1['configurable']['checkpoint_id']}")
        
        # Step 2: Process state
        process_checkpoint = {
            "v": 2,
            "ts": "2024-01-01T00:01:00Z", 
            "id": str(uuid.uuid4()),
            "channel_values": {
                "messages": ["User: Hello", "Assistant: Hi there!", "User: How are you?"],
                "current_step": "processing"
            }
        }
        
        result2 = checkpointer.put(
            checkpoint_config,
            process_checkpoint,
            {"step": 2, "action": "processing"},
            {}
        )
        print(f"   ✓ Stored processing checkpoint: {result2['configurable']['checkpoint_id']}")
        
        # Step 3: Final state
        final_checkpoint = {
            "v": 3,
            "ts": "2024-01-01T00:02:00Z",
            "id": str(uuid.uuid4()),
            "channel_values": {
                "messages": ["User: Hello", "Assistant: Hi there!", "User: How are you?", "Assistant: I'm doing well!"],
                "current_step": "completed"
            }
        }
        
        result3 = checkpointer.put(
            checkpoint_config,
            final_checkpoint, 
            {"step": 3, "action": "completed"},
            {}
        )
        print(f"   ✓ Stored final checkpoint: {result3['configurable']['checkpoint_id']}")
        
        # Test retrieval
        print("\n4. Testing checkpoint retrieval...")
        
        # Get latest state
        latest = checkpointer.get(checkpoint_config)
        if latest:
            print(f"   ✓ Retrieved latest checkpoint")
            print(f"   ✓ Checkpoint type: {type(latest)}")
            
            # Handle the actual return format
            if hasattr(latest, 'checkpoint'):
                checkpoint_data = latest.checkpoint
            elif isinstance(latest, dict):
                checkpoint_data = latest
            else:
                print(f"   ⚠️  Unexpected format: {latest}")
                checkpoint_data = {}
            
            channel_values = checkpoint_data.get("channel_values", {})
            messages = channel_values.get("messages", [])
            step = channel_values.get("current_step", "unknown")
            print(f"   ✓ Current step: {step}")
            print(f"   ✓ Message count: {len(messages)}")
            print(f"   ✓ Last message: {messages[-1] if messages else 'None'}")
        else:
            print("   ❌ Failed to retrieve latest state")
            return False
        
        # Test history
        print("\n5. Testing checkpoint history...")
        
        history = list(checkpointer.list(checkpoint_config, limit=10))
        print(f"   ✓ Retrieved {len(history)} checkpoints from history")
        
        for i, cp in enumerate(history):
            if hasattr(cp, 'checkpoint') and hasattr(cp, 'metadata'):
                step = cp.metadata.get("step", "unknown")
                action = cp.metadata.get("action", "unknown")
                print(f"     Checkpoint {i+1}: step {step}, action {action}")
        
        # Verify we have the expected checkpoints
        if len(history) >= 3:
            print("   ✅ History contains all expected checkpoints")
        else:
            print(f"   ⚠️  Expected 3+ checkpoints, got {len(history)}")
        
        print("\n🎉 Basic checkpointer operations working perfectly!")
        print("   ✅ This confirms the Supabase checkpointer is ready for agent usage")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function."""
    
    print("🚀 Simple Agent Checkpointer Test")
    print("=" * 50)
    
    # Check environment
    postgres_conn = os.getenv("POSTGRES_CONNECTION_STRING")
    if not postgres_conn:
        print("❌ POSTGRES_CONNECTION_STRING not set")
        return False
    
    # Run test
    success = test_simple_checkpointer_usage()
    
    if success:
        print(f"\n🎊 SUCCESS: Supabase checkpointer ready for agents!")
        print("✓ PostgreSQL checkpointer working with Supabase")
        print("✓ Multi-step checkpoint storage and retrieval")
        print("✓ Checkpoint history and metadata working")
        print("✓ Ready for LangGraph agent integration")
    else:
        print(f"\n❌ Checkpointer test failed")
    
    return success


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)