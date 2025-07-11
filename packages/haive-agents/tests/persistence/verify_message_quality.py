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

        result = agent.invoke({"messages": [HumanMessage(content=user_msg)]}, config)

        # Extract response
        response = result.messages[-1].content if hasattr(result, "messages") else "No response"

        all_messages.append((user_msg, response))

        # Check quality based on test type
        if test_type == "greeting":
            if "hello" in response.lower() or "hi" in response.lower():
                pass")
            else:
                pass")

        elif test_type == "memory_check":
            if "john" in response.lower():
                pass")
            else:
                pass")

        elif test_type == "summary_request":
            keywords = ["python", "database", "postgresql", "prepared statements"]
            found = sum(1 for k in keywords if k in response.lower())
            if found >= 2:
                pass")
            else:
                pass")

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


    return thread_id


def check_ssl_connection_issue():
    """Check SSL connection configuration."""

    conn_string = os.environ.get("POSTGRES_CONNECTION_STRING")
    if conn_string:

        # Check if SSL mode is specified
        if "sslmode=" in conn_string:
            import re

            match = re.search(r"sslmode=(\w+)", conn_string)
            if match:
                sslmode = match.group(1)

                if sslmode == "require":
        else:
            passed")

    # Check connection pool settings

    try:


        # Check for keepalive settings in configs
        from haive.agents.conversation.base.agent import BaseConversationAgent

        test_agent = BaseConversationAgent(name="test")

        if hasattr(test_agent, "persistence") and hasattr(
            test_agent.persistence, "connection_kwargs"
        ):
            kwargs = test_agent.persistence.connection_kwargs

            if "keepalives_idle" in kwargs:
                pass
            else:
                pass")

    except Exception as e:
        pass")


def main():
    """Run message quality tests."""
    # Test message flow
    test_message_flow()

    # Check SSL configuration
    check_ssl_connection_issue()



if __name__ == "__main__":
    main()
