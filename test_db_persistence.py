#!/usr/bin/env python3
"""Test database persistence and retrieve data by thread ID."""

import os
import uuid
import json
import psycopg2
from datetime import datetime
from haive.agents.conversation.collaberative.agent import CollaborativeConversation
from haive.agents.simple.agent import SimpleAgent
from haive.core.models.llm.base import AugLLMConfig

def create_test_conversation():
    """Create a test conversation and return the thread ID."""
    print("=== Testing Database Persistence ===\n")
    
    # Generate a unique thread ID
    thread_id = f"test-thread-{uuid.uuid4()}"
    print(f"📌 Thread ID: {thread_id}\n")
    
    # Create agents
    agents = {
        "Alice": SimpleAgent(
            name="Alice",
            engine=AugLLMConfig(
                system_message="You are Alice, a creative thinker.",
                deployment_name="gpt-4o-mini"
            )
        ),
        "Bob": SimpleAgent(
            name="Bob",
            engine=AugLLMConfig(
                system_message="You are Bob, a practical analyst.",
                deployment_name="gpt-4o-mini"
            )
        )
    }
    
    # Create conversation with checkpointing enabled
    conversation = CollaborativeConversation.create_brainstorming_session(
        participants=agents,
        topic="Test persistence: Database features",
        sections=["Overview", "Implementation"],
        output_format="outline",
        max_rounds=1,
        persistence=True,  # Enable persistence
        thread_id=thread_id
    )
    
    # Run conversation
    print("Running conversation...")
    result = conversation.invoke(
        {"messages": []},
        config={"configurable": {"thread_id": thread_id}}
    )
    
    print(f"\n✅ Conversation completed with {len(result.get('messages', []))} messages")
    print(f"📊 Document sections: {list(result.get('document_sections', {}).keys())}")
    
    return thread_id

def query_database(thread_id):
    """Query the database to retrieve data for the given thread ID."""
    print(f"\n=== Querying Database for Thread {thread_id} ===\n")
    
    conn_string = os.getenv("POSTGRES_CONNECTION_STRING")
    if not conn_string:
        print("❌ POSTGRES_CONNECTION_STRING not found")
        return
    
    try:
        with psycopg2.connect(conn_string) as conn:
            with conn.cursor() as cursor:
                # 1. Check threads table
                print("1. Checking threads table:")
                cursor.execute("""
                    SELECT thread_id, created_at, last_access, metadata
                    FROM threads
                    WHERE thread_id = %s
                """, (thread_id,))
                
                thread_data = cursor.fetchone()
                if thread_data:
                    print(f"   ✅ Thread found!")
                    print(f"   - Created: {thread_data[1]}")
                    print(f"   - Last Access: {thread_data[2]}")
                    print(f"   - Metadata: {thread_data[3]}")
                else:
                    print(f"   ❌ Thread not found in threads table")
                
                # 2. Check checkpoints table
                print("\n2. Checking checkpoints table:")
                cursor.execute("""
                    SELECT COUNT(*) as checkpoint_count,
                           MIN(checkpoint_id) as first_checkpoint,
                           MAX(checkpoint_id) as last_checkpoint
                    FROM checkpoints
                    WHERE thread_id = %s
                """, (thread_id,))
                
                checkpoint_info = cursor.fetchone()
                if checkpoint_info and checkpoint_info[0] > 0:
                    print(f"   ✅ Found {checkpoint_info[0]} checkpoints")
                    print(f"   - First: {checkpoint_info[1]}")
                    print(f"   - Last: {checkpoint_info[2]}")
                    
                    # Get latest checkpoint data
                    cursor.execute("""
                        SELECT checkpoint_id, parent_checkpoint_id, 
                               checkpoint, created_at
                        FROM checkpoints
                        WHERE thread_id = %s
                        ORDER BY checkpoint_id DESC
                        LIMIT 1
                    """, (thread_id,))
                    
                    latest = cursor.fetchone()
                    if latest:
                        print(f"\n   Latest checkpoint details:")
                        print(f"   - ID: {latest[0]}")
                        print(f"   - Parent: {latest[1]}")
                        print(f"   - Created: {latest[3]}")
                        
                        # Parse checkpoint data
                        checkpoint_data = latest[2]
                        if checkpoint_data:
                            print(f"\n   Checkpoint data keys: {list(checkpoint_data.keys())}")
                            
                            # Extract conversation state
                            if 'channel_values' in checkpoint_data:
                                values = checkpoint_data['channel_values']
                                print(f"\n   Conversation state:")
                                print(f"   - Messages: {len(values.get('messages', []))}")
                                print(f"   - Topic: {values.get('topic', 'N/A')}")
                                print(f"   - Speakers: {values.get('speakers', [])}")
                                print(f"   - Turn count: {values.get('turn_count', 0)}")
                                print(f"   - Current section: {values.get('current_section', 'N/A')}")
                                
                                # Show document sections if available
                                if 'document_sections' in values:
                                    print(f"\n   Document sections:")
                                    for section, content in values['document_sections'].items():
                                        if content:
                                            print(f"   - {section}: {len(content)} chars")
                else:
                    print(f"   ❌ No checkpoints found")
                
                # 3. List recent threads
                print("\n3. Recent threads in database:")
                cursor.execute("""
                    SELECT thread_id, created_at, last_access
                    FROM threads
                    ORDER BY last_access DESC
                    LIMIT 5
                """)
                
                recent_threads = cursor.fetchall()
                for thread in recent_threads:
                    print(f"   - {thread[0][:50]}... (created: {thread[1].strftime('%Y-%m-%d %H:%M')})")
                    
    except Exception as e:
        print(f"❌ Database error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Run test conversation
    thread_id = create_test_conversation()
    
    # Query database
    query_database(thread_id)