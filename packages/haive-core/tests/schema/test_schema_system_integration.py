"""Integration tests for the complete schema system."""

from typing import Optional

import pytest

from haive.core.schema import (
    MessagesState,
    MessagesStateWithTokenUsage,
    MultiAgentStateSchema,
    SchemaComposer,
    StateSchema,
    TokenUsage,
    TokenUsageMixin,
)


class TestSchemaSystemIntegration:
    """Test the complete schema system integration."""

    def test_core_imports(self):
        """Test that all core imports work."""
        # Verify classes exist
        assert StateSchema is not None
        assert SchemaComposer is not None
        assert MessagesState is not None
        assert MultiAgentStateSchema is not None
        assert TokenUsage is not None
        assert TokenUsageMixin is not None
        assert MessagesStateWithTokenUsage is not None

    def test_state_schema_basic_functionality(self):
        """Test StateSchema basic functionality."""
        # Create instance
        state = StateSchema()

        # Test engine fields exist
        assert hasattr(state, "engine")
        assert hasattr(state, "engines")
        assert hasattr(state, "llm")
        assert hasattr(state, "main_engine")

        # Test engines is a dict
        assert isinstance(state.engines, dict)

        # Test convenience properties
        assert state.llm is None  # No engines set
        assert state.main_engine is None  # No engines set

    def test_schema_composer_basic_functionality(self):
        """Test SchemaComposer basic functionality."""
        # Create instance
        composer = SchemaComposer("TestSchema")

        # Test methods exist
        assert hasattr(composer, "add_engine")
        assert hasattr(composer, "add_engine_management")
        assert hasattr(composer, "build")

        # Test building works
        schema_class = composer.build()
        assert schema_class is not None

        # Test instance creation
        instance = schema_class()
        assert instance is not None

    def test_messages_state_functionality(self):
        """Test MessagesState functionality."""
        # Create instance
        messages_state = MessagesState()

        # Test methods exist
        assert hasattr(messages_state, "add_message")
        assert hasattr(messages_state, "get_last_message")
        assert hasattr(messages_state, "messages")

        # Test messages field
        assert isinstance(messages_state.messages, list)
        assert len(messages_state.messages) == 0

    def test_token_usage_functionality(self):
        """Test token usage functionality."""
        # Test TokenUsage creation
        usage = TokenUsage(input_tokens=100, output_tokens=50)
        assert usage.input_tokens == 100
        assert usage.output_tokens == 50
        assert usage.total_tokens == 150

    def test_token_usage_mixin(self):
        """Test TokenUsageMixin functionality."""

        # Create test class with mixin
        class TestState(TokenUsageMixin):
            test_field: str = "test"

        # Create instance
        state = TestState()

        # Test mixin methods exist
        assert hasattr(state, "get_token_usage")
        assert hasattr(state, "track_message_tokens")

    def test_messages_state_with_token_usage(self):
        """Test MessagesStateWithTokenUsage functionality."""
        # Create instance
        token_state = MessagesStateWithTokenUsage()

        # Test has both message and token functionality
        assert hasattr(token_state, "add_message")
        assert hasattr(token_state, "messages")
        assert hasattr(token_state, "get_token_usage_summary")

        # Test fields
        assert isinstance(token_state.messages, list)

    def test_backward_compatibility(self):
        """Test that existing patterns still work."""
        # Test class method still works
        schema_class = SchemaComposer.from_components([], name="TestSchema")
        assert schema_class is not None

        # Test instance creation
        instance = schema_class()
        assert instance is not None

    def test_engine_management_integration(self):
        """Test engine management integration."""
        # Create composer
        composer = SchemaComposer("TestSchema")

        # Test engine management methods
        assert hasattr(composer, "add_engine")
        assert hasattr(composer, "add_engine_management")

        # Build schema
        schema_class = composer.build()
        instance = schema_class()

        # Test engine fields exist
        assert hasattr(instance, "engine")
        assert hasattr(instance, "engines")
        assert hasattr(instance, "llm")
        assert hasattr(instance, "main_engine")

    def test_modular_structure(self):
        """Test that modular structure imports work."""
        # Test we can import from various locations
        from haive.core.schema.prebuilt.messages import TokenUsage as ModularTokenUsage
        from haive.core.schema.prebuilt.messages import TokenUsageMixin as ModularMixin

        # Verify they're the same classes
        assert ModularTokenUsage is TokenUsage
        assert ModularMixin is TokenUsageMixin

    def test_multi_agent_state_schema(self):
        """Test MultiAgentStateSchema functionality."""
        # Create instance
        multi_agent_state = MultiAgentStateSchema()

        # Test it's a valid schema
        assert multi_agent_state is not None

        # Test it has engine management
        assert hasattr(multi_agent_state, "engines")
