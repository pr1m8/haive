"""
Examples demonstrating the use of the enhanced MessagesState system.

This file contains complete examples of common usage patterns, demonstrating
both the classic API and the enhanced features.
"""

from typing import Dict, List, Optional, Union

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)

# The examples below use try/except to handle the case where the enhanced
# features are not available, making them safe to run in any environment


def basic_usage_example():
    """Demonstrates basic usage of MessagesState."""
    from haive.core.schema.prebuilt.messages import MessagesState

    # Create a new state
    state = MessagesState()

    # Add a system message
    state.add_system_message("You are a helpful assistant.")

    # Add conversation messages
    state.add_message(HumanMessage(content="Hello, can you help me?"))
    state.add_message(AIMessage(content="Of course! What can I help you with?"))
    state.add_message(HumanMessage(content="I need help with Python."))
    state.add_message(
        AIMessage(
            content="I'd be happy to help with Python. What specific question do you have?"
        )
    )

    # Access messages
    print(f"Last message: {state.get_last_message().content}")
    print(f"Last human message: {state.get_last_human_message().content}")
    print(f"Last AI message: {state.get_last_ai_message().content}")

    # Format conversion
    openai_format = state.to_openai_format()
    print(f"OpenAI format has {len(openai_format)} messages")

    return state


def tool_usage_example():
    """Demonstrates tool usage with MessagesState."""
    from haive.core.schema.prebuilt.messages import MessagesState

    # Create a new state
    state = MessagesState()

    # Add a system message
    state.add_system_message("You are a helpful assistant with tool access.")

    # Add conversation with tool usage
    state.add_message(HumanMessage(content="What's the weather in New York?"))

    # AI message with tool calls
    ai_msg = AIMessage(
        content="I'll check the weather for you.",
        tool_calls=[
            {
                "id": "call_abc123",
                "name": "get_weather",
                "args": {"location": "New York"},
            }
        ],
    )
    state.add_message(ai_msg)

    # Tool response
    tool_msg = ToolMessage(
        content='{"temperature": 72, "condition": "sunny"}', tool_call_id="call_abc123"
    )
    state.add_message(tool_msg)

    # AI response after tool
    state.add_message(
        AIMessage(content="The weather in New York is currently 72°F and sunny.")
    )

    # Check for tool calls
    print(f"Has tool calls: {state.has_tool_calls()}")

    # Get tool calls from a specific message
    tool_calls = state.get_tool_calls(ai_msg)
    print(f"Tool calls: {tool_calls}")

    return state


def enhanced_features_example():
    """Demonstrates enhanced features of MessagesState."""
    from haive.core.schema.prebuilt.messages import MessagesState

    # Create state with conversation including tools
    state = tool_usage_example()

    try:
        # Get conversation rounds
        print("\nConversation Rounds:")
        rounds = state.get_conversation_rounds()
        for i, round_info in enumerate(rounds):
            print(f"Round {i+1}:")
            print(f"  Human: {round_info.human_message.content}")
            print(f"  AI responses: {len(round_info.ai_responses)}")
            print(f"  Tool calls: {len(round_info.tool_calls)}")
            print(f"  Tool responses: {len(round_info.tool_responses)}")
            print(f"  Complete: {round_info.is_complete}")
            print(f"  Has errors: {round_info.has_errors}")

        # Get completed tool calls
        print("\nCompleted Tool Calls:")
        completed_calls = state.get_completed_tool_calls()
        for call in completed_calls:
            print(f"  Tool: {call.tool_call.get('name')}")
            print(f"  Args: {call.tool_call.get('args')}")
            print(f"  Success: {call.is_successful}")

        # Check if messages are from real humans
        print("\nMessage Sources:")
        for msg in state.messages:
            if isinstance(msg, HumanMessage):
                is_real = state.is_real_human_message(msg)
                print(
                    f"  '{msg.content[:20]}...' is from a {'real human' if is_real else 'transformed source'}"
                )

    except NotImplementedError as e:
        print(f"Enhanced features not available: {e}")

    return state


def agent_handoff_example():
    """Demonstrates agent-to-agent handoff with message transformation."""
    from haive.core.schema.prebuilt.messages import MessagesState

    # First agent's state
    agent1 = MessagesState()
    agent1.add_system_message("You are Agent 1, an expert in data analysis.")
    agent1.add_message(HumanMessage(content="Analyze this dataset"))
    agent1.add_message(
        AIMessage(
            content="I found these patterns in the data: high correlation between X and Y"
        )
    )

    print("Agent 1 conversation:")
    for msg in agent1.messages:
        print(f"  [{msg.type}] {msg.content[:40]}...")

    # Second agent's state
    agent2 = MessagesState()
    agent2.add_system_message("You are Agent 2, an expert in visualization.")

    # Transform and transfer messages
    try:
        # Transform AI messages to human messages for handoff
        agent1.transform_ai_to_human(
            preserve_metadata=True, engine_id="agent1", engine_name="DataAnalysisAgent"
        )

        print("\nAgent 1 conversation after transformation:")
        for msg in agent1.messages:
            print(f"  [{msg.type}] {msg.content[:40]}...")

        # Copy transformed messages to agent2 (skipping system message)
        for msg in agent1.messages:
            if not isinstance(msg, SystemMessage):
                agent2.add_message(msg)

        print("\nAgent 2 conversation after handoff:")
        for msg in agent2.messages:
            print(f"  [{msg.type}] {msg.content[:40]}...")

            # Check metadata on transferred messages
            if hasattr(msg, "additional_kwargs") and msg.additional_kwargs:
                print(f"  Metadata: {msg.additional_kwargs}")

    except NotImplementedError as e:
        print(f"Enhanced features not available: {e}")

    return agent1, agent2


def enhanced_implementation_example():
    """Demonstrates using the enhanced implementation directly."""
    try:
        from haive.core.schema.prebuilt.messages import (
            EnhancedMessagesState,
            MessageList,
        )

        # Create new state with the enhanced implementation
        state = EnhancedMessagesState()

        # Add messages
        state.add_system_message("You are a helpful assistant.")
        state.add_message(HumanMessage(content="Hello!"))
        state.add_message(AIMessage(content="Hi there! How can I help you?"))
        state.add_message(HumanMessage(content="Tell me about Python."))
        state.add_message(
            AIMessage(
                content="Python is a programming language known for its readability."
            )
        )

        # Access computed properties
        print("\nEnhanced State Properties:")
        print(f"  Message count: {state.message_count}")
        print(f"  Round count: {state.round_count}")
        print(f"  Has tool calls: {state.has_tool_calls}")
        print(f"  Has tool errors: {state.has_tool_errors}")

        # Use the message list directly
        print("\nMessage List Operations:")
        print(f"  First human: '{state.messages.first_real_human_message.content}'")

        # Use filtering
        human_messages = state.messages.filter_by_type(HumanMessage)
        print(f"  Human messages: {len(human_messages)}")

        # Use transformation
        state.transform_for_reflection()
        print("\nAfter Reflection Transformation:")
        for msg in state.messages:
            print(f"  [{msg.type}] {msg.content[:40]}...")

        return state

    except (ImportError, AttributeError):
        print("Enhanced implementation (EnhancedMessagesState) not available")
        return None


if __name__ == "__main__":
    print("=== Basic Usage Example ===")
    basic_usage_example()

    print("\n=== Tool Usage Example ===")
    tool_usage_example()

    print("\n=== Enhanced Features Example ===")
    enhanced_features_example()

    print("\n=== Agent Handoff Example ===")
    agent_handoff_example()

    print("\n=== Enhanced Implementation Example ===")
    enhanced_implementation_example()
