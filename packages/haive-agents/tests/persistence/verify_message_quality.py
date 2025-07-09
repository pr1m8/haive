#!/usr/bin/env python3
"""Verify message quality and logical flow."""

import json
import os
import sys
from datetime import datetime

sys.path.insert(0, "/home/will/Projects/haive/backend/haive/packages/haive-core/src")
sys.path.insert(0, "/home/will/Projects/haive/backend/haive/packages/haive-agents/src")


def test_message_flow():
    """Test that messages flow logically and sound right."""
    print("🔍 Testing Message Quality and Flow")
    print("=" * 70)

    from langchain_core.messages import HumanMessage

    from haive.agents.simple.agent import SimpleAgent

    timestamp = datetime.now().strftime("%H%M%S")
    thread_id = f"flow_test_{timestamp}"

    # Create agent with specific personality
    agent = SimpleAgent(
        name=f"FlowTest_{timestamp}",
        system_message="""You are a helpful AI assistant named Alex. 
        You have a friendly, professional tone.
        You remember previous conversations and refer back to them naturally.
        Always be concise but complete in your responses.""",
        persistence=True,
    )
    agent.compile()

    config = {"configurable": {"thread_id": thread_id}}

    # Conversation flow test
    conversations = [
        ("Hello! My name is John and I'm working on a Python project.", "greeting"),
        ("I need help with database connections.", "topic_introduction"),
        (
            "Specifically, I'm having issues with PostgreSQL prepared statements.",
            "specific_problem",
        ),
        ("What did I tell you my name was?", "memory_check"),
        ("Can you summarize what we've discussed so far?", "summary_request"),
    ]

    all_messages = []

    for i, (user_msg, test_type) in enumerate(conversations):
        print(f"\n📤 Message {i+1} ({test_type}): {user_msg}")

        result = agent.invoke({"messages": [HumanMessage(content=user_msg)]}, config)

        # Extract response
        if hasattr(result, "messages"):
            response = result.messages[-1].content
        else:
            response = "No response"

        all_messages.append((user_msg, response))
        print(f"📥 Response: {response[:200]}...")

        # Check quality based on test type
        if test_type == "greeting":
            if "hello" in response.lower() or "hi" in response.lower():
                print("   ✅ Appropriate greeting")
            else:
                print("   ❌ Missing greeting")

        elif test_type == "memory_check":
            if "john" in response.lower():
                print("   ✅ Remembers user's name")
            else:
                print("   ❌ Doesn't remember name")

        elif test_type == "summary_request":
            keywords = ["python", "database", "postgresql", "prepared statements"]
            found = sum(1 for k in keywords if k in response.lower())
            if found >= 2:
                print(f"   ✅ Good summary (mentioned {found}/4 key topics)")
            else:
                print(f"   ❌ Poor summary (only mentioned {found}/4 key topics)")

    # Save conversation for review
    output_file = f"conversation_flow_{timestamp}.json"
    with open(output_file, "w") as f:
        json.dump(
            {
                "thread_id": thread_id,
                "messages": all_messages,
                "timestamp": datetime.now().isoformat(),
            },
            f,
            indent=2,
        )

    print(f"\n📁 Conversation saved to: {output_file}")

    return thread_id


def check_ssl_connection_issue():
    """Check SSL connection configuration."""
    print("\n\n🔍 Checking SSL Connection Configuration")
    print("=" * 70)

    conn_string = os.environ.get("POSTGRES_CONNECTION_STRING")
    if conn_string:
        print(f"Connection string: {conn_string[:50]}...")

        # Check if SSL mode is specified
        if "sslmode=" in conn_string:
            import re

            match = re.search(r"sslmode=(\w+)", conn_string)
            if match:
                sslmode = match.group(1)
                print(f"SSL mode: {sslmode}")

                if sslmode == "require":
                    print(
                        "   ℹ️  SSL is required - this can cause issues with connection stability"
                    )
                    print("   💡 Consider adding: ?sslmode=require&keepalives_idle=600")
        else:
            print("   ⚠️  No SSL mode specified")

    # Check connection pool settings
    print("\n📊 Connection Pool Settings:")

    try:
        from haive.core.persistence.store.connection import ConnectionManager

        print("   ✅ ConnectionManager available")

        # Check for keepalive settings in configs
        from haive.agents.conversation.base.agent import BaseConversationAgent

        test_agent = BaseConversationAgent(name="test")

        if hasattr(test_agent, "persistence") and hasattr(
            test_agent.persistence, "connection_kwargs"
        ):
            kwargs = test_agent.persistence.connection_kwargs
            print(f"   Connection kwargs: {kwargs}")

            if "keepalives_idle" in kwargs:
                print(
                    f"   ✅ Keepalive settings configured: {kwargs.get('keepalives_idle')}s"
                )
            else:
                print("   ❌ No keepalive settings")

    except Exception as e:
        print(f"   ❌ Error checking settings: {e}")


def main():
    """Run message quality tests."""
    # Test message flow
    thread_id = test_message_flow()

    # Check SSL configuration
    check_ssl_connection_issue()

    print("\n" + "=" * 70)
    print("✅ Message quality test complete!")


if __name__ == "__main__":
    main()
