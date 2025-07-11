# tests/test_messages_state.py

from datetime import datetime
from typing import Any, Dict, List

import pytest
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langgraph.graph import add_messages

from haive.core.schema.prebuilt.messages.messages_state import (
    MessageList,
    MessageRound,
    MessagesState,
    ToolCallInfo,
)


class TestMessageListBasics:
    """Test basic functionality and list-like interface."""

    def test_empty_initialization(self):
        """Test creating empty MessageList."""
        state = MessageList()
        assert len(state) == 0
        assert state.message_count == 0
        assert state.last_message is None

    def test_string_initialization(self):
        """Test creating MessageList from string."""
        state = MessageList(root="Hello world")
        assert len(state) == 1
        assert isinstance(state[0], HumanMessage)
        assert state[0].content == "Hello world"

    def test_list_initialization(self):
        """Test creating MessageList from list of messages."""
        messages = [HumanMessage(content="Hello"), AIMessage(content="Hi there!")]
        state = MessageList(root=messages)
        assert len(state) == 2
        assert state[0].content == "Hello"
        assert state[1].content == "Hi there!"

    def test_mixed_string_message_initialization(self):
        """Test creating MessageList from mixed strings and messages."""
        mixed_input = [
            "Hello",  # String -> HumanMessage
            AIMessage(content="Hi there!"),
            "How are you?",  # String -> HumanMessage
        ]
        state = MessageList(root=mixed_input)
        assert len(state) == 3
        assert isinstance(state[0], HumanMessage)
        assert isinstance(state[1], AIMessage)
        assert isinstance(state[2], HumanMessage)

    def test_list_like_operations(self):
        """Test list-like operations with auto-conversion."""
        state = MessageList()

        # Test append with string
        state.append("Hello")
        assert len(state) == 1
        assert isinstance(state[0], HumanMessage)

        # Test append with message
        state.append(AIMessage(content="Hi"))
        assert len(state) == 2

        # Test extend with mixed types
        state.extend(["Another message", AIMessage(content="Another AI message")])
        assert len(state) == 4
        assert isinstance(state[2], HumanMessage)
        assert isinstance(state[3], AIMessage)

        # Test insert
        state.insert(1, "Inserted message")
        assert len(state) == 5
        assert state[1].content == "Inserted message"

    def test_iteration_and_indexing(self):
        """Test iteration and indexing."""
        messages = ["Message 1", "Message 2", "Message 3"]
        state = MessageList(root=messages)

        # Test iteration
        contents = [msg.content for msg in state]
        assert contents == ["Message 1", "Message 2", "Message 3"]

        # Test indexing
        assert state[0].content == "Message 1"
        assert state[-1].content == "Message 3"

        # Test slicing
        subset = state[1:3]
        assert len(subset) == 2
        assert subset[0].content == "Message 2"


class TestComputedProperties:
    """Test computed properties and caching."""

    def test_last_message_property(self):
        """Test last_message computed property."""
        state = MessagesState()
        assert state.last_message is None

        state.append("First message")
        assert state.last_message.content == "First message"

        state.append(AIMessage(content="Second message"))
        assert state.last_message.content == "Second message"
        assert isinstance(state.last_message, AIMessage)

    def test_message_type_properties(self):
        """Test message type-specific properties."""
        state = MessagesState(
            [
                SystemMessage(content="System message"),
                "Human message",
                AIMessage(content="AI message"),
                "Another human message",
            ]
        )

        assert state.last_human_message.content == "Another human message"
        assert state.last_ai_message.content == "AI message"
        assert state.system_message.content == "System message"
        assert state.first_real_human_message.content == "Human message"

    def test_real_vs_transformed_human_messages(self):
        """Test distinction between real and transformed human messages."""
        state = MessagesState(
            [
                "Real human message",
                HumanMessage(
                    content="Transformed", additional_kwargs={"engine_id": "llm-123"}
                ),
                HumanMessage(content="Another transformed", name="agent"),
                "Another real message",
            ]
        )

        real_messages = state.real_human_messages
        transformed_messages = state.transformed_human_messages

        assert len(real_messages) == 2
        assert len(transformed_messages) == 2
        assert real_messages[0].content == "Real human message"
        assert real_messages[1].content == "Another real message"

    def test_cache_invalidation(self):
        """Test that computed properties are invalidated when messages change."""
        state = MessagesState(["Initial message"])

        # Access property to cache it
        first_last = state.last_message
        assert first_last.content == "Initial message"

        # Modify state
        state.append("New message")

        # Property should be updated
        second_last = state.last_message
        assert second_last.content == "New message"
        assert second_last is not first_last


class TestToolCallManagement:
    """Test tool call management functionality."""

    # In the test file, update the create_ai_message_with_tool_calls method:
    def create_ai_message_with_tool_calls(self, tool_calls: List[Dict]) -> AIMessage:
        """Helper to create AI message with tool calls."""
        # Fix the tool call format
        formatted_calls = []
        for tc in tool_calls:
            formatted_call = {
                "name": tc.get("function", {}).get("name", ""),
                "args": tc.get("function", {}).get("arguments", {}),
                "id": tc.get("id", ""),
            }
            formatted_calls.append(formatted_call)

        return AIMessage(content="Using tools", tool_calls=formatted_calls)

    def create_tool_message(
        self, tool_call_id: str, content: str, is_error: bool = False
    ) -> ToolMessage:
        """Helper to create tool message."""
        kwargs = {"content": content, "tool_call_id": tool_call_id}
        if is_error:
            kwargs["additional_kwargs"] = {"is_error": True}
        return ToolMessage(**kwargs)

    def test_has_tool_calls_property(self):
        """Test has_tool_calls computed property."""
        state = MessagesState()
        assert not state.has_tool_calls

        # Add AI message without tool calls
        state.append(AIMessage(content="No tools"))
        assert not state.has_tool_calls

        # Add AI message with tool calls
        tool_calls = [{"id": "call_1", "function": {"name": "test_tool"}}]
        ai_msg = self.create_ai_message_with_tool_calls(tool_calls)
        state.append(ai_msg)
        assert state.has_tool_calls

    def test_tool_call_error_detection(self):
        """Test tool call error detection."""
        state = MessagesState(
            [
                self.create_ai_message_with_tool_calls(
                    [{"id": "call_1", "function": {"name": "test"}}]
                ),
                self.create_tool_message("call_1", "Success", is_error=False),
                self.create_ai_message_with_tool_calls(
                    [{"id": "call_2", "function": {"name": "test2"}}]
                ),
                self.create_tool_message("call_2", "Error occurred", is_error=True),
            ]
        )

        assert state.has_tool_errors
        error_messages = state.tool_call_errors
        assert len(error_messages) == 1
        assert error_messages[0].content == "Error occurred"

    def test_completed_tool_calls(self):
        """Test completed tool calls tracking."""
        tool_call_1 = {"id": "call_1", "function": {"name": "test_tool_1"}}
        tool_call_2 = {"id": "call_2", "function": {"name": "test_tool_2"}}

        state = MessagesState(
            [
                self.create_ai_message_with_tool_calls([tool_call_1, tool_call_2]),
                self.create_tool_message("call_1", "Success 1", is_error=False),
                self.create_tool_message("call_2", "Error 2", is_error=True),
            ]
        )

        completed = state.completed_tool_calls
        assert len(completed) == 2

        # Check successful tool call
        successful = [tc for tc in completed if tc.is_successful]
        failed = [tc for tc in completed if not tc.is_successful]

        assert len(successful) == 1
        assert len(failed) == 1
        assert successful[0].tool_call_id == "call_1"
        assert failed[0].tool_call_id == "call_2"

    def test_deduplicate_tool_calls(self):
        """Test tool call deduplication."""
        duplicate_tool_call = {"id": "call_1", "function": {"name": "test_tool"}}

        ai_msg1 = self.create_ai_message_with_tool_calls([duplicate_tool_call])
        ai_msg2 = self.create_ai_message_with_tool_calls([duplicate_tool_call])

        state = MessagesState([ai_msg1, ai_msg2])

        # Should have 2 identical tool calls initially
        all_tool_calls = []
        for msg in state:
            if isinstance(msg, AIMessage) and hasattr(msg, "tool_calls"):
                all_tool_calls.extend(msg.tool_calls)
        assert len(all_tool_calls) == 2

        # Deduplicate
        removed_count = state.deduplicate_tool_calls()
        assert removed_count == 1

        # Should have 1 tool call remaining
        all_tool_calls_after = []
        for msg in state:
            if isinstance(msg, AIMessage) and hasattr(msg, "tool_calls"):
                all_tool_calls_after.extend(msg.tool_calls)
        assert len(all_tool_calls_after) == 1

    def test_pending_tool_calls(self):
        """Test pending tool calls detection."""
        state = MessagesState(
            [
                self.create_ai_message_with_tool_calls(
                    [
                        {"id": "call_1", "function": {"name": "test1"}},
                        {"id": "call_2", "function": {"name": "test2"}},
                    ]
                ),
                self.create_tool_message("call_1", "Response for call_1"),
                # call_2 has no response
            ]
        )

        pending = state.get_pending_tool_calls()
        assert len(pending) == 1
        assert pending[0]["tool_call"]["id"] == "call_2"


class TestAdvancedFiltering:
    """Test advanced filtering capabilities."""

    def test_filter_by_type(self):
        """Test filtering by message type."""
        state = MessagesState(
            [
                SystemMessage(content="System"),
                "Human message",
                AIMessage(content="AI message"),
                ToolMessage(content="Tool response", tool_call_id="call_1"),
            ]
        )

        human_messages = state.filter_by_type(HumanMessage)
        ai_messages = state.filter_by_type(AIMessage)
        system_messages = state.filter_by_type(SystemMessage)

        assert len(human_messages) == 1
        assert len(ai_messages) == 1
        assert len(system_messages) == 1

        # Test multiple types
        ai_and_human = state.filter_by_type([AIMessage, HumanMessage])
        assert len(ai_and_human) == 2

    def test_filter_by_content_pattern(self):
        """Test filtering by content pattern."""
        state = MessagesState(
            [
                "Hello world",
                "Error: something went wrong",
                AIMessage(content="Success: operation completed"),
                "Another error occurred",
            ]
        )

        error_messages = state.filter_by_content_pattern(r"error", case_sensitive=False)
        success_messages = state.filter_by_content_pattern(r"Success")

        assert len(error_messages) == 2
        assert len(success_messages) == 1

    def test_filter_by_metadata(self):
        """Test filtering by metadata."""
        state = MessagesState(
            [
                HumanMessage(content="No metadata"),
                AIMessage(
                    content="With engine", additional_kwargs={"engine_id": "llm-123"}
                ),
                AIMessage(
                    content="Different engine",
                    additional_kwargs={"engine_id": "llm-456"},
                ),
                HumanMessage(
                    content="With agent", additional_kwargs={"source_agent": "agent1"}
                ),
            ]
        )

        engine_messages = state.filter_by_metadata("engine_id")
        specific_engine = state.filter_by_metadata("engine_id", "llm-123")
        agent_messages = state.filter_by_metadata("source_agent")

        assert len(engine_messages) == 2
        assert len(specific_engine) == 1
        assert len(agent_messages) == 1

    def test_filter_by_engine(self):
        """Test filtering by engine ID/name."""
        state = MessagesState(
            [
                AIMessage(
                    content="Engine 1", additional_kwargs={"engine_id": "llm-123"}
                ),
                AIMessage(
                    content="Engine 2", additional_kwargs={"engine_id": "llm-456"}
                ),
                AIMessage(
                    content="Named engine", additional_kwargs={"engine_name": "gpt4"}
                ),
            ]
        )

        engine_123_messages = state.filter_by_engine(engine_id="llm-123")
        named_engine_messages = state.filter_by_engine(engine_name="gpt4")

        assert len(engine_123_messages) == 1
        assert len(named_engine_messages) == 1

    def test_get_messages_since_last_human(self):
        """Test getting messages since last human message."""
        state = MessagesState(
            [
                "First human message",
                AIMessage(content="AI response 1"),
                ToolMessage(content="Tool response", tool_call_id="call_1"),
                "Second human message",  # This should be the "last human"
                AIMessage(content="AI response 2"),
                AIMessage(content="AI response 3"),
            ]
        )

        recent_with_human = state.get_messages_since_last_human(include_human=True)
        recent_without_human = state.get_messages_since_last_human(include_human=False)

        assert len(recent_with_human) == 3  # Human + 2 AI responses
        assert len(recent_without_human) == 2  # Just 2 AI responses
        assert recent_with_human[0].content == "Second human message"


class TestConversationRounds:
    """Test conversation round analysis."""

    def test_round_counting(self):
        """Test basic round counting."""
        state = MessagesState(
            [
                "Question 1",
                AIMessage(content="Answer 1"),
                "Question 2",
                AIMessage(content="Answer 2"),
                "Question 3",  # Incomplete round
            ]
        )

        assert state.round_count == 2  # Only completed rounds

    def test_conversation_rounds_property(self):
        """Test detailed conversation rounds."""
        state = MessagesState(
            [
                "Question 1",
                AIMessage(content="Answer 1"),
                "Question 2",
                AIMessage(
                    content="Answer 2",
                    tool_calls=[{"id": "call_1", "function": {"name": "test"}}],
                ),
                ToolMessage(content="Tool response", tool_call_id="call_1"),
            ]
        )

        rounds = state.conversation_rounds
        assert len(rounds) == 2

        first_round = rounds[0]
        assert first_round.round_number == 1
        assert first_round.human_message.content == "Question 1"
        assert len(first_round.ai_responses) == 1
        assert first_round.is_complete

        second_round = rounds[1]
        assert second_round.round_number == 2
        assert len(second_round.tool_calls) == 1
        assert len(second_round.tool_responses) == 1
        assert second_round.is_complete

    def test_incomplete_rounds(self):
        """Test handling of incomplete rounds."""
        state = MessagesState(
            [
                "Question 1",
                AIMessage(
                    content="Answer with tool",
                    tool_calls=[{"id": "call_1", "function": {"name": "test"}}],
                ),
                # Missing tool response
            ]
        )

        rounds = state.conversation_rounds
        assert len(rounds) == 1
        assert not rounds[0].is_complete  # Tool call without response


class TestMessageTransformations:
    """Test message transformation functionality."""

    def test_transform_ai_to_human(self):
        """Test transforming AI messages to Human messages."""
        state = MessagesState(
            [
                "Human message",
                AIMessage(content="AI message 1"),
                AIMessage(content="AI message 2", additional_kwargs={"test": "value"}),
            ]
        )

        state.transform_ai_to_human(preserve_metadata=True, engine_id="llm-123")

        # All should be human messages now
        human_count = len(state.filter_by_type(HumanMessage))
        ai_count = len(state.filter_by_type(AIMessage))

        assert human_count == 3
        assert ai_count == 0

        # Check metadata preservation
        last_msg = state.last_message
        assert last_msg.additional_kwargs.get("engine_id") == "llm-123"
        assert last_msg.additional_kwargs.get("test") == "value"

    def test_transform_for_reflection(self):
        """Test reflection transformation (role swapping)."""
        state = MessagesState(
            [
                SystemMessage(content="System message"),
                "Human message",
                AIMessage(content="AI message"),
            ]
        )

        state.transform_for_reflection(preserve_first=True)

        # First message (system) should be unchanged
        assert isinstance(state[0], SystemMessage)
        # Human should become AI
        assert isinstance(state[1], AIMessage)
        assert state[1].content == "Human message"
        # AI should become Human
        assert isinstance(state[2], HumanMessage)
        assert state[2].content == "AI message"

    def test_transform_for_agent_handoff(self):
        """Test agent handoff transformation."""
        state = MessagesState(
            [
                SystemMessage(content="System message"),
                "Human message",
                AIMessage(content="AI message"),
                ToolMessage(content="Tool message", tool_call_id="call_1"),
            ]
        )

        state.transform_for_agent_handoff(
            source_agent="agent1", exclude_system=True, exclude_tools=True
        )

        # Should exclude system and tool messages
        assert len(state) == 2
        # AI message should become Human with source agent
        transformed_ai = state.filter_by_metadata("source_agent", "agent1")
        assert len(transformed_ai) == 1
        assert transformed_ai[0].content == "AI message"


class TestUtilityMethods:
    """Test utility and helper methods."""

    def test_add_message_variants(self):
        """Test different ways to add messages."""
        state = MessagesState()

        # Add string
        state.add_message("String message")
        assert len(state) == 1
        assert isinstance(state[0], HumanMessage)

        # Add dict
        state.add_message({"role": "assistant", "content": "Dict message"})
        assert len(state) == 2
        assert isinstance(state[1], AIMessage)

        # Add BaseMessage
        state.add_message(SystemMessage(content="System message"))
        assert len(state) == 3
        assert isinstance(state[2], SystemMessage)

    def test_add_system_message(self):
        """Test adding system messages."""
        state = MessagesState(["Human message"])

        state.add_system_message("System message")

        # System message should be first
        assert isinstance(state[0], SystemMessage)
        assert state[0].content == "System message"
        assert len(state) == 2

    def test_add_engine_metadata(self):
        """Test adding engine metadata to AI messages."""
        state = MessagesState(
            [
                "Human message",
                AIMessage(content="AI message 1"),
                AIMessage(content="AI message 2"),
            ]
        )

        state.add_engine_metadata(engine_id="llm-123", engine_name="gpt4")

        # Only AI messages should have metadata
        ai_messages = state.filter_by_type(AIMessage)
        for msg in ai_messages:
            assert msg.additional_kwargs.get("engine_id") == "llm-123"
            assert msg.additional_kwargs.get("engine_name") == "gpt4"


class TestStaticConstructors:
    """Test static constructor methods."""

    def test_from_messages(self):
        """Test creating from messages list."""
        messages = [HumanMessage(content="Hello"), AIMessage(content="Hi")]
        state = MessagesState.from_messages(messages)

        assert len(state) == 2
        assert state[0].content == "Hello"

    def test_from_dict(self):
        """Test creating from dictionary."""
        data = {
            "messages": [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi"},
            ]
        }
        state = MessagesState.from_dict(data)

        assert len(state) == 2
        assert isinstance(state[0], HumanMessage)
        assert isinstance(state[1], AIMessage)

    def test_with_system_message(self):
        """Test creating with system message."""
        state = MessagesState.with_system_message("You are a helpful assistant")

        assert len(state) == 1
        assert isinstance(state[0], SystemMessage)
        assert state[0].content == "You are a helpful assistant"

    def test_from_string(self):
        """Test creating from single string."""
        state = MessagesState.from_string("Hello world")

        assert len(state) == 1
        assert isinstance(state[0], HumanMessage)
        assert state[0].content == "Hello world"


class TestFormatConversion:
    """Test format conversion methods."""

    def test_to_openai_format(self):
        """Test conversion to OpenAI format."""
        state = MessagesState(["Hello", AIMessage(content="Hi there")])

        openai_format = state.to_openai_format()

        assert len(openai_format) == 2
        assert openai_format[0]["role"] == "user"
        assert openai_format[1]["role"] == "assistant"

    def test_to_langchain_prompt(self):
        """Test conversion to LangChain prompt format."""
        state = MessagesState(["Hello", AIMessage(content="Hi there")])

        prompt = state.to_langchain_prompt()

        assert "User: Hello" in prompt
        assert "Assistant: Hi there" in prompt


class TestLangGraphCompatibility:
    """Test LangGraph reducer compatibility."""

    def test_add_messages_compatibility(self):
        """Test compatibility with add_messages reducer."""
        state1 = MessagesState(["Message 1"])
        state2 = MessagesState(["Message 2"])

        # Test addition
        combined = state1 + state2
        assert len(combined) == 2
        assert combined[0].content == "Message 1"
        assert combined[1].content == "Message 2"

    def test_model_dump_returns_root(self):
        """Test that model_dump returns the root list for LangGraph."""
        state = MessagesState(["Test message"])
        dumped = state.model_dump()

        assert isinstance(dumped, list)
        assert len(dumped) == 1
        assert dumped[0].content == "Test message"


# Performance and edge case tests
class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_state_properties(self):
        """Test properties on empty state."""
        state = MessagesState()

        assert state.last_message is None
        assert state.last_human_message is None
        assert state.last_ai_message is None
        assert state.system_message is None
        assert not state.has_tool_calls
        assert not state.has_tool_errors
        assert len(state.real_human_messages) == 0
        assert len(state.completed_tool_calls) == 0

    def test_malformed_tool_messages(self):
        """Test handling of malformed tool messages."""
        # Tool message without tool_call_id
        tool_msg = ToolMessage(content="Response")
        state = MessagesState([tool_msg])

        # Should not crash
        completed = state.completed_tool_calls
        assert len(completed) == 0

    def test_system_message_ordering(self):
        """Test system message ordering validation."""
        # System message after human should be reordered
        state = MessagesState(
            ["Human message", SystemMessage(content="System message")]
        )

        # System should be moved to front
        assert isinstance(state[0], SystemMessage)
        assert isinstance(state[1], HumanMessage)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
