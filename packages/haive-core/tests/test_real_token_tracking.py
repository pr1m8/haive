"""Test real token tracking with actual SimpleAgent interactions.

This test verifies that token tracking works end-to-end with real LLM calls.
"""

import asyncio

from haive.agents.simple.agent import SimpleAgent
from langchain_core.messages import AIMessage

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.prebuilt.llm_state import LLMState
from haive.core.schema.prebuilt.messages.messages_with_token_usage import (
    MessagesStateWithTokenUsage,
)


async def test_simple_agent_real_token_tracking():
    """Test that SimpleAgent actually tracks tokens with real LLM calls."""
    print("🧪 Testing real token tracking with SimpleAgent...")

    # Create SimpleAgent with real LLM
    config = AugLLMConfig(
        temperature=0.1,
        max_tokens=50,  # Keep it small for testing
    )

    agent = SimpleAgent(name="token_tracker_test", engine=config)

    print(f"   Agent created: {agent.name}")
    print(f"   Engine: {agent.engine}")

    # Make a real LLM call
    response = await agent.arun("What is 2 + 2? Answer briefly.")

    print(f"   Response: {response}")
    print(f"   Response type: {type(response)}")

    # Try to access agent state/memory to check token tracking
    # This might vary based on SimpleAgent implementation

    if hasattr(agent, "state"):
        state = agent.state
        print(f"   Agent state type: {type(state)}")
        print(f"   State has token_usage: {hasattr(state, 'token_usage')}")

        if hasattr(state, "token_usage"):
            print(f"   Token usage: {state.token_usage}")
            print(f"   Token usage history: {state.token_usage_history}")

        if hasattr(state, "messages"):
            print(f"   Messages count: {len(state.messages)}")
            for i, msg in enumerate(state.messages):
                print(f"     Message {i}: {type(msg)} - {msg.content[:50]}...")
                if hasattr(msg, "response_metadata"):
                    print(f"       Response metadata: {msg.response_metadata}")

    # Check if agent has conversation memory
    if hasattr(agent, "memory"):
        print(f"   Agent memory: {agent.memory}")

    # Check if agent stores conversation history
    if hasattr(agent, "conversation_history"):
        print(f"   Conversation history: {agent.conversation_history}")


def test_llm_state_with_real_engine():
    """Test LLMState with real engine configuration."""
    print("\n🧪 Testing LLMState with real engine...")

    engine = AugLLMConfig(name="llm_state_test", temperature=0.1, max_tokens=100)

    llm_state = LLMState(engine=engine)

    print(f"   LLMState created with engine: {llm_state.engine}")
    print(f"   Has token_usage field: {hasattr(llm_state, 'token_usage')}")
    print(f"   Has messages field: {hasattr(llm_state, 'messages')}")
    print(f"   Has tools field: {hasattr(llm_state, 'tools')}")

    # Test with a real AI message that might have token usage
    ai_message = AIMessage(
        content="The answer is 4.",
        response_metadata={
            "usage": {"prompt_tokens": 15, "completion_tokens": 5, "total_tokens": 20}
        },
    )

    print(f"   Adding message with token usage...")
    llm_state.add_message(ai_message)

    print(f"   Messages count: {len(llm_state.messages)}")
    print(f"   Token usage: {llm_state.token_usage}")
    print(f"   Token usage history: {llm_state.token_usage_history}")

    # Test LLMState specific features
    print(f"   Context length: {llm_state.context_length}")
    print(f"   Token usage percentage: {llm_state.token_usage_percentage}")
    print(f"   Is approaching token limit: {llm_state.is_approaching_token_limit}")
    print(f"   Remaining tokens: {llm_state.remaining_tokens}")


def test_messages_state_with_token_usage_direct():
    """Test MessagesStateWithTokenUsage directly."""
    print("\n🧪 Testing MessagesStateWithTokenUsage directly...")

    state = MessagesStateWithTokenUsage()

    print(f"   Initial token usage: {state.token_usage}")
    print(f"   Initial token usage history: {state.token_usage_history}")

    # Add multiple messages with token usage
    messages = [
        AIMessage(
            content="Response 1",
            response_metadata={
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 5,
                    "total_tokens": 15,
                }
            },
        ),
        AIMessage(
            content="Response 2",
            response_metadata={
                "usage": {
                    "prompt_tokens": 20,
                    "completion_tokens": 10,
                    "total_tokens": 30,
                }
            },
        ),
        AIMessage(
            content="Response 3",
            response_metadata={
                "usage": {
                    "prompt_tokens": 30,
                    "completion_tokens": 15,
                    "total_tokens": 45,
                }
            },
        ),
    ]

    for i, msg in enumerate(messages):
        print(f"   Adding message {i+1}...")
        state.add_message(msg)
        print(f"     Token usage after message {i+1}: {state.token_usage}")

    print(f"   Final token usage: {state.token_usage}")
    print(f"   Token usage history length: {len(state.token_usage_history)}")

    # Test summary
    summary = state.get_token_usage_summary()
    print(f"   Token usage summary: {summary}")

    # Test cost calculation
    state.calculate_costs(input_cost_per_1k=0.001, output_cost_per_1k=0.002)
    print(f"   After cost calculation: {state.token_usage}")


async def main():
    """Run all token tracking tests."""
    print("🚀 Testing Real Token Tracking\n")

    try:
        await test_simple_agent_real_token_tracking()
        test_llm_state_with_real_engine()
        test_messages_state_with_token_usage_direct()

        print("\n🎉 All token tracking tests completed!")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
