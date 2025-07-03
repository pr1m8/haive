#!/usr/bin/env python3
"""Detailed test to examine conversation agent inputs, outputs, and persistence behavior."""

import json
import logging
from haive.agents.conversation.collaberative.agent import CollaborativeConversation

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_conversation_persistence_detailed():
    """Test conversation agents with detailed examination of inputs, outputs, and persistence."""
    
    print("=== Detailed Conversation Persistence Test ===\n")
    
    # Test 1: Run conversation with persistence and examine the flow
    print("1. Creating conversation with persistence=True...")
    
    session = CollaborativeConversation.create_brainstorming_session(
        topic="AI-powered productivity tools",
        participants=["ProductManager", "Developer"], 
        sections=["Problem Analysis", "Solution Ideas"],
        max_rounds=2,  # Allow for more interaction
        persistence=True
    )
    
    print(f"   Persistence config type: {type(session.persistence).__name__}")
    print(f"   Checkpointer type: {type(session.checkpointer).__name__}")
    print()
    
    # Test 2: Run conversation and capture detailed results
    thread_id = "detailed_test_001"
    config = {"configurable": {"thread_id": thread_id, "recursion_limit": 100}}
    
    print("2. Running conversation...")
    print(f"   Thread ID: {thread_id}")
    print(f"   Input config: {config}")
    print()
    
    result = session.run({}, config=config)
    
    print("3. Examining conversation result:")
    print(f"   Result type: {type(result).__name__}")
    
    # Extract and display key information from result
    if hasattr(result, 'messages'):
        print(f"   Total messages: {len(result.messages)}")
        print("   Message types:")
        for i, msg in enumerate(result.messages):
            msg_type = type(msg).__name__ 
            speaker = getattr(msg, 'name', 'System')
            content_preview = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
            print(f"     {i+1}. {msg_type} from {speaker}: {content_preview}")
    
    # Check other result attributes
    for attr in ['round_number', 'turn_count', 'conversation_ended', 'speakers', 'topic']:
        if hasattr(result, attr):
            print(f"   {attr}: {getattr(result, attr)}")
    print()
    
    # Test 3: Verify persistence by checking database state
    print("4. Verifying persistence in database:")
    
    if hasattr(session.checkpointer, 'conn') and session.checkpointer.conn:
        try:
            with session.checkpointer.conn.connection() as conn:
                with conn.cursor() as cursor:
                    # Get thread info
                    cursor.execute(
                        "SELECT thread_id, created_at, last_access, metadata FROM threads WHERE thread_id = %s",
                        (thread_id,)
                    )
                    thread_info = cursor.fetchone()
                    
                    if thread_info:
                        print(f"   ✅ Thread registered: {thread_info[0]}")
                        print(f"      Created: {thread_info[1]}")
                        print(f"      Last access: {thread_info[2]}")
                        
                        # Try to parse metadata if it exists
                        try:
                            metadata = json.loads(thread_info[3]) if thread_info[3] else {}
                            print(f"      Metadata: {metadata}")
                        except:
                            print(f"      Metadata (raw): {thread_info[3]}")
                    
                    # Get checkpoint info
                    cursor.execute(
                        "SELECT checkpoint_id, created_at FROM checkpoints WHERE thread_id = %s ORDER BY created_at",
                        (thread_id,)
                    )
                    checkpoints = cursor.fetchall()
                    
                    print(f"   ✅ Found {len(checkpoints)} checkpoints:")
                    for i, (cp_id, created_at) in enumerate(checkpoints[:5]):  # Show first 5
                        print(f"      {i+1}. {cp_id} at {created_at}")
                    if len(checkpoints) > 5:
                        print(f"      ... and {len(checkpoints) - 5} more")
                        
        except Exception as e:
            print(f"   ❌ Database verification failed: {e}")
    else:
        print("   ❌ No database connection available")
    print()
    
    # Test 4: Try to retrieve a specific checkpoint
    print("5. Testing checkpoint retrieval:")
    
    try:
        checkpoint_config = {"configurable": {"thread_id": thread_id}}
        retrieved_checkpoint = session.checkpointer.get(checkpoint_config)
        
        if retrieved_checkpoint:
            print("   ✅ Retrieved checkpoint successfully")
            print(f"   Checkpoint keys: {list(retrieved_checkpoint.keys())}")
            
            # Look at channel_values which contains the actual state
            if 'channel_values' in retrieved_checkpoint:
                channel_values = retrieved_checkpoint['channel_values']
                print(f"   Channel values type: {type(channel_values)}")
                
                if isinstance(channel_values, dict):
                    print("   State fields:")
                    for key, value in channel_values.items():
                        if key == 'messages':
                            print(f"     {key}: {len(value)} messages" if isinstance(value, list) else f"     {key}: {type(value)}")
                        else:
                            print(f"     {key}: {value}")
                elif hasattr(channel_values, '__dict__'):
                    print("   State attributes:")
                    for key, value in channel_values.__dict__.items():
                        if key == 'messages':
                            print(f"     {key}: {len(value)} messages" if isinstance(value, list) else f"     {key}: {type(value)}")
                        else:
                            print(f"     {key}: {value}")
        else:
            print("   ❌ No checkpoint retrieved")
            
    except Exception as e:
        print(f"   ❌ Checkpoint retrieval failed: {e}")
    print()
    
    # Test 5: Try to resume conversation from persisted state
    print("6. Testing conversation resumption:")
    
    try:
        # Create a new session but try to continue from the same thread
        resume_session = CollaborativeConversation.create_brainstorming_session(
            topic="Resumed conversation - AI productivity tools",
            participants=["ProductManager", "Developer"],
            sections=["Implementation Plan"],  # New section 
            max_rounds=1,
            persistence=True
        )
        
        # Try to run with the same thread_id to see if it resumes
        resume_config = {"configurable": {"thread_id": thread_id, "recursion_limit": 100}}
        
        print(f"   Resuming with thread_id: {thread_id}")
        resume_result = resume_session.run({}, config=resume_config)
        
        print("   ✅ Conversation resumed successfully")
        print(f"   Resume result type: {type(resume_result).__name__}")
        
        if hasattr(resume_result, 'messages'):
            print(f"   Total messages after resume: {len(resume_result.messages)}")
            
            # Show the last few messages to see continuation
            print("   Last few messages:")
            for msg in resume_result.messages[-3:]:
                msg_type = type(msg).__name__
                speaker = getattr(msg, 'name', 'System')
                content_preview = msg.content[:80] + "..." if len(msg.content) > 80 else msg.content
                print(f"     {msg_type} from {speaker}: {content_preview}")
                
    except Exception as e:
        print(f"   ❌ Conversation resumption failed: {e}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_conversation_persistence_detailed()