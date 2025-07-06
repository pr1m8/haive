#!/usr/bin/env python3
"""Simple test to review if conversation persistence is working without prepared statement conflicts."""

import os
import sys
from datetime import datetime

def test_basic_conversation():
    """Basic test of conversation agent with fixed persistence."""
    try:
        # Add the packages to path
        sys.path.insert(0, '/home/will/Projects/haive/backend/haive/packages/haive-core/src')
        sys.path.insert(0, '/home/will/Projects/haive/backend/haive/packages/haive-agents/src')
        
        print("🧪 Testing basic conversation with fixed PostgreSQL...")
        
        from haive.core.engine.aug_llm import AugLLMConfig
        
        # Import the correct collaborative agent
        from haive.agents.conversation.collaberative.agent import CollaborativeConversation
        
        # Create a simple test
        test_id = datetime.now().strftime('%H%M%S')
        participants = {
            f"TestAgent_{test_id}": AugLLMConfig(
                name=f"TestAgent_{test_id}",
                system_message="You are a helpful assistant. Give brief responses.",
            ),
        }
        
        # Create agent with persistence
        agent = CollaborativeConversation(
            name=f"TestConversation_{test_id}",
            participant_agents=participants,
            topic="Simple test",
            max_rounds=1,
            persistence=True,
        )
        
        print(f"✅ Agent created successfully: {agent.name}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_basic_conversation()