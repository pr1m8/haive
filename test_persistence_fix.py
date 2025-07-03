#!/usr/bin/env python3
"""Test script to verify persistence fix for conversation agents."""

import logging
from haive.agents.conversation.collaberative.agent import CollaborativeConversation

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_persistence_fix():
    """Test that conversation agents properly use persistence when persistence=True."""
    
    print("=== Testing Persistence Fix ===\n")
    
    # Test 1: Create conversation with persistence=True 
    print("Creating collaborative conversation with persistence=True...")
    session = CollaborativeConversation.create_brainstorming_session(
        topic="Database Persistence Test",
        participants=["Alice", "Bob"],
        sections=["Overview", "Testing"],
        max_rounds=1,
        persistence=True  # This should enable actual database persistence
    )
    
    # Display what persistence configuration was set up
    print(f"Session persistence config: {session.persistence}")
    print(f"Session checkpointer type: {type(session.checkpointer).__name__ if session.checkpointer else 'None'}")
    
    # Run a very short conversation
    thread_id = "test_persistence_fix_001"
    config = {"configurable": {"thread_id": thread_id, "recursion_limit": 50}}
    
    print(f"\nRunning conversation with thread_id: {thread_id}")
    result = session.run({}, config=config)
    
    print(f"Conversation completed. Round number: {getattr(result, 'round_number', 'Unknown')}")
    
    # Test 2: Try to retrieve state from the same thread_id to verify persistence
    print(f"\nAttempting to retrieve state for thread_id: {thread_id}")
    
    # Create another session with the same persistence config
    session2 = CollaborativeConversation.create_brainstorming_session(
        topic="Database Persistence Test - Session 2",
        participants=["Charlie", "Dave"],
        sections=["Continuation"],
        max_rounds=1,
        persistence=True
    )
    
    # Try to get checkpoint
    if session2.checkpointer:
        try:
            checkpoint_config = {"configurable": {"thread_id": thread_id}}
            checkpoint = session2.checkpointer.get(checkpoint_config)
            if checkpoint:
                print("✅ SUCCESS: Found checkpoint data in persistence store!")
                print(f"   Checkpoint keys: {list(checkpoint.keys()) if isinstance(checkpoint, dict) else 'Not a dict'}")
            else:
                print("❌ FAILED: No checkpoint found in persistence store")
        except Exception as e:
            print(f"❌ ERROR: Exception when retrieving checkpoint: {e}")
    else:
        print("❌ FAILED: No checkpointer available")
    
    # Test 3: Query database directly to verify thread and checkpoint tables
    print("\n=== Database Verification ===")
    try:
        # Try to access the checkpointer's connection to query the database
        if hasattr(session.checkpointer, 'conn'):
            pool = session.checkpointer.conn
            if pool:
                print("Querying database directly...")
                with pool.connection() as conn:
                    with conn.cursor() as cursor:
                        # Check threads table
                        cursor.execute("SELECT thread_id, created_at FROM threads WHERE thread_id = %s", (thread_id,))
                        thread_result = cursor.fetchone()
                        if thread_result:
                            print(f"✅ Thread found in database: {thread_result[0]} created at {thread_result[1]}")
                        else:
                            print("❌ Thread not found in database")
                        
                        # Check checkpoints table
                        cursor.execute("SELECT COUNT(*) FROM checkpoints WHERE thread_id = %s", (thread_id,))
                        checkpoint_count = cursor.fetchone()[0]
                        print(f"   Checkpoints for this thread: {checkpoint_count}")
                        
                        if checkpoint_count > 0:
                            print("✅ SUCCESS: Checkpoints are being saved to database!")
                        else:
                            print("❌ FAILED: No checkpoints saved to database")
        else:
            print("❌ No database connection available for verification")
            
    except Exception as e:
        print(f"❌ Database verification failed: {e}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_persistence_fix()