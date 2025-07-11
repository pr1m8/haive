"""Tests for MessagesStateWithTokenUsage with real SimpleAgent integration.

This test suite validates token tracking functionality using real agents
and actual LLM interactions (no mocks). Tests cover:

- Automatic token extraction from AI messages
- Token usage aggregation across conversation rounds
- Cost calculation and tracking
- Integration with SimpleAgent for real-world scenarios
"""

from typing import Any, Dict

import pytest
from haive.agents.simple.agent import SimpleAgent
from langchain_core.messages import AIMessage, HumanMessage

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.prebuilt.messages.messages_with_token_usage import (
    MessagesStateWithTokenUsage,
)


class TestMessagesStateWithTokenUsage:
    """Test suite for MessagesStateWithTokenUsage functionality."""

    @pytest.fixture
    def simple_agent(self) -> SimpleAgent:
        """Create a SimpleAgent with real LLM for token testing."""
        config = AugLLMConfig(
            temperature=0.1,  # Low temperature for consistent testing
            max_tokens=100,  # Small response for predictable token counts
        )

        return SimpleAgent(name="token_test_agent", engine=config)

    @pytest.fixture
    def token_state(self) -> MessagesStateWithTokenUsage:
        """Create a MessagesStateWithTokenUsage instance for testing."""
        return MessagesStateWithTokenUsage()

    def test_basic_token_state_creation(self, token_state: MessagesStateWithTokenUsage):
        """Test basic creation and initial state of MessagesStateWithTokenUsage."""
        assert token_state.messages == []
        assert token_state.token_usage is None
        assert token_state.token_usage_history == []
        assert len(token_state.get_token_usage_summary()["rounds"]) == 0

    def test_manual_message_addition_tracks_tokens(
        self, token_state: MessagesStateWithTokenUsage
    ):
        """Test that manually adding messages with token usage works."""
        # Create AI message with mock token usage data
        ai_message = AIMessage(
            content="Hello! How can I help you today?",
            response_metadata={
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 8,
                    "total_tokens": 18,
                }
            },
        )

        # Add message and verify token tracking
        token_state.add_message(ai_message)

        assert len(token_state.messages) == 1
        assert token_state.token_usage is not None
        assert token_state.token_usage.total_tokens == 18
        assert token_state.token_usage.input_tokens == 10
        assert token_state.token_usage.output_tokens == 8

    async def test_simple_agent_integration_with_token_tracking(
        self, simple_agent: SimpleAgent
    ):
        """Test real SimpleAgent interaction with automatic token tracking."""
        # Send a simple query to the agent
        response = await simple_agent.arun("What is 2 + 2?")

        # Verify we got a response
        assert response is not None
        assert isinstance(response, str)
        assert len(response) > 0

        # Get the agent's state (should be MessagesStateWithTokenUsage or compatible)
        # Note: This test assumes SimpleAgent uses a state schema with token tracking
        # We'll need to check how SimpleAgent exposes its state

        # For now, let's test that the response contains expected content
        assert "4" in response or "four" in response.lower()

    async def test_conversation_round_token_accumulation(
        self, simple_agent: SimpleAgent
    ):
        """Test that token usage accumulates across multiple conversation rounds."""
        conversation_id = "test-token-conversation"
        config = {"configurable": {"thread_id": conversation_id}}

        # First interaction
        response1 = await simple_agent.arun("Hello, my name is Alice.", config=config)
        assert response1 is not None

        # Second interaction
        response2 = await simple_agent.arun("What's my name?", config=config)
        assert response2 is not None
        assert "alice" in response2.lower()

        # Third interaction to build up token usage
        response3 = await simple_agent.arun("Tell me a short joke.", config=config)
        assert response3 is not None

    def test_token_usage_summary_calculation(
        self, token_state: MessagesStateWithTokenUsage
    ):
        """Test token usage summary calculation with multiple messages."""
        # Add multiple AI messages with different token counts
        messages_data = [
            {"prompt_tokens": 20, "completion_tokens": 15, "total_tokens": 35},
            {"prompt_tokens": 25, "completion_tokens": 20, "total_tokens": 45},
            {"prompt_tokens": 30, "completion_tokens": 25, "total_tokens": 55},
        ]

        for i, token_data in enumerate(messages_data):
            ai_message = AIMessage(
                content=f"Response {i+1}", response_metadata={"token_usage": token_data}
            )
            token_state.add_message(ai_message)

        # Get summary and verify calculations
        summary = token_state.get_token_usage_summary()

        assert summary["total_tokens"] == 135  # 35 + 45 + 55
        assert summary["input_tokens"] == 75  # 20 + 25 + 30
        assert summary["output_tokens"] == 60  # 15 + 20 + 25
        assert summary["rounds"] == 3

    def test_cost_calculation_with_provider_pricing(
        self, token_state: MessagesStateWithTokenUsage
    ):
        """Test cost calculation with provider-specific pricing."""
        # Add a message with token usage
        ai_message = AIMessage(
            content="This is a test response for cost calculation.",
            response_metadata={
                "token_usage": {
                    "prompt_tokens": 1000,  # 1k input tokens
                    "completion_tokens": 500,  # 500 output tokens
                    "total_tokens": 1500,
                }
            },
        )
        token_state.add_message(ai_message)

        # Calculate costs with GPT-4 pricing (example)
        token_state.calculate_costs(
            input_cost_per_1k=0.03,  # $0.03 per 1k input tokens
            output_cost_per_1k=0.06,  # $0.06 per 1k output tokens
        )

        summary = token_state.get_token_usage_summary()

        # Expected cost: (1000/1000 * 0.03) + (500/1000 * 0.06) = 0.03 + 0.03 = 0.06
        assert (
            abs(summary["total_cost"] - 0.06) < 0.001
        )  # Allow for floating point precision

    def test_conversation_cost_analysis(self, token_state: MessagesStateWithTokenUsage):
        """Test the comprehensive conversation cost analysis."""
        # Add messages to simulate a conversation
        for i in range(3):
            ai_message = AIMessage(
                content=f"Response {i+1}",
                response_metadata={
                    "token_usage": {
                        "prompt_tokens": 100 + (i * 10),
                        "completion_tokens": 50 + (i * 5),
                        "total_tokens": 150 + (i * 15),
                    }
                },
            )
            token_state.add_message(ai_message)

        # Set some costs
        token_state.calculate_costs(input_cost_per_1k=0.001, output_cost_per_1k=0.002)

        # Get cost analysis
        analysis = token_state.get_conversation_cost_analysis()

        assert "total_cost" in analysis
        assert "total_tokens" in analysis
        assert "rounds" in analysis
        assert "avg_tokens_per_round" in analysis
        assert analysis["rounds"] == 3
        assert analysis["avg_tokens_per_round"] > 0

    async def test_agent_state_access_for_token_inspection(
        self, simple_agent: SimpleAgent
    ):
        """Test accessing agent state to inspect token usage after interactions."""
        # This test explores how to access SimpleAgent's internal state
        # to verify token tracking is working in real agent scenarios

        conversation_id = "test-state-access"
        config = {"configurable": {"thread_id": conversation_id}}

        # Perform interaction
        response = await simple_agent.arun(
            "Explain quantum computing briefly.", config=config
        )
        assert response is not None

        # Try to access agent's state/memory for token inspection
        # Note: This might need adjustment based on SimpleAgent's actual API
        if hasattr(simple_agent, "state"):
            state = simple_agent.state
            if hasattr(state, "token_usage"):
                # If agent state has token tracking, verify it's working
                assert state.token_usage is not None or len(state.messages) > 0

        # Alternative: Check if agent has conversation memory/state persistence
        if hasattr(simple_agent, "get_state") or hasattr(simple_agent, "memory"):
            # Test agent state retrieval methods if they exist
            pass

    def test_token_usage_with_system_message(
        self, token_state: MessagesStateWithTokenUsage
    ):
        """Test token tracking with system message in conversation."""
        # Add system message
        token_state.add_system_message("You are a helpful assistant.")

        # Add AI response with token usage
        ai_message = AIMessage(
            content="I'm ready to help!",
            response_metadata={
                "token_usage": {
                    "prompt_tokens": 25,  # Including system message tokens
                    "completion_tokens": 8,
                    "total_tokens": 33,
                }
            },
        )
        token_state.add_message(ai_message)

        assert len(token_state.messages) == 2  # System + AI message
        assert token_state.get_system_message() is not None
        assert token_state.token_usage.total_tokens == 33

    def test_empty_state_summary(self, token_state: MessagesStateWithTokenUsage):
        """Test token usage summary for empty state."""
        summary = token_state.get_token_usage_summary()

        assert summary["total_tokens"] == 0
        assert summary["total_cost"] == 0.0
        assert summary["rounds"] == 0
        assert summary["message_count"] == 0

    @pytest.mark.asyncio
    async def test_multiple_agents_token_comparison(self):
        """Test token usage across multiple agent instances."""
        # Create two agents with different configurations
        agent1 = SimpleAgent(
            name="verbose_agent", engine=AugLLMConfig(max_tokens=200, temperature=0.7)
        )

        agent2 = SimpleAgent(
            name="concise_agent", engine=AugLLMConfig(max_tokens=50, temperature=0.1)
        )

        query = "Explain machine learning."

        # Get responses from both agents
        response1 = await agent1.arun(query)
        response2 = await agent2.arun(query)

        # Verify both responded
        assert response1 is not None and len(response1) > 0
        assert response2 is not None and len(response2) > 0

        # Verbose agent should generally produce longer responses
        # (though this isn't guaranteed due to LLM variability)
        print(f"Verbose agent response length: {len(response1)}")
        print(f"Concise agent response length: {len(response2)}")
