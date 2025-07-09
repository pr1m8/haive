"""Integration tests for the schema system with proper pytest format."""

import pytest


class TestSchemaIntegration:
    """Test schema system integration."""

    def test_direct_imports(self):
        """Test that schema components can be imported."""
        from haive.core.schema.prebuilt.messages.token_usage import TokenUsage
        from haive.core.schema.prebuilt.messages.token_usage_mixin import (
            TokenUsageMixin,
        )
        from haive.core.schema.prebuilt.messages_state import MessagesState
        from haive.core.schema.schema_composer import SchemaComposer
        from haive.core.schema.state_schema import StateSchema

        # Verify classes exist
        assert StateSchema is not None
        assert SchemaComposer is not None
        assert MessagesState is not None
        assert TokenUsage is not None
        assert TokenUsageMixin is not None

    def test_token_usage_calculation(self):
        """Test TokenUsage calculation works correctly."""
        from haive.core.schema.prebuilt.messages.token_usage import TokenUsage

        # Test basic calculation
        usage = TokenUsage(input_tokens=100, output_tokens=50)
        assert usage.input_tokens == 100
        assert usage.output_tokens == 50
        assert usage.total_tokens == 150

    def test_token_usage_mixin_basic(self):
        """Test TokenUsageMixin basic functionality."""
        from haive.core.schema.prebuilt.messages.token_usage_mixin import (
            TokenUsageMixin,
        )

        # Test mixin can be used as base class
        class TestState(TokenUsageMixin):
            test_field: str = "test"

        state = TestState()
        assert hasattr(state, "get_token_usage")
        assert hasattr(state, "track_message_tokens")

    def test_schema_composer_basic(self):
        """Test SchemaComposer basic functionality."""
        from haive.core.schema.schema_composer import SchemaComposer

        # Create instance
        composer = SchemaComposer("TestSchema")

        # Test methods exist
        assert hasattr(composer, "add_field")
        assert hasattr(composer, "build")

        # Test building works
        schema_class = composer.build()
        assert schema_class is not None

        # Test class has expected attributes
        assert hasattr(schema_class, "model_fields")
        assert hasattr(schema_class, "__name__")
        assert schema_class.__name__ == "TestSchema"

    def test_messages_state_basic(self):
        """Test MessagesState basic functionality."""
        from haive.core.schema.prebuilt.messages_state import MessagesState

        # Test methods exist
        assert hasattr(MessagesState, "add_message")
        assert hasattr(MessagesState, "get_last_message")

        # Test field exists in model
        assert "messages" in MessagesState.model_fields

    def test_multi_agent_state_import(self):
        """Test MultiAgentStateSchema can be imported."""
        from haive.core.schema.multi_agent_state_schema import MultiAgentStateSchema

        # Test it exists
        assert MultiAgentStateSchema is not None

        # Test it has expected fields
        assert hasattr(MultiAgentStateSchema, "model_fields")

    def test_modular_imports(self):
        """Test modular structure imports work."""
        # Test token usage module components
        from haive.core.schema.prebuilt.messages import MessagesStateWithTokenUsage
        from haive.core.schema.prebuilt.messages import TokenUsage as ModularTokenUsage
        from haive.core.schema.prebuilt.messages import TokenUsageMixin as ModularMixin

        # Verify they exist
        assert ModularTokenUsage is not None
        assert ModularMixin is not None
        assert MessagesStateWithTokenUsage is not None

    def test_token_usage_with_costs(self):
        """Test TokenUsage with cost calculation."""
        from haive.core.schema.prebuilt.messages.token_usage import TokenUsage

        # Test with costs
        usage = TokenUsage(
            input_tokens=100,
            output_tokens=50,
            input_token_cost=0.003,
            output_token_cost=0.015,
        )

        assert usage.total_tokens == 150
        assert usage.total_cost == 0.018  # 0.003 + 0.015

    def test_backward_compatibility(self):
        """Test backward compatibility patterns."""
        from haive.core.schema.schema_composer import SchemaComposer

        # Test class method still works
        schema_class = SchemaComposer.from_components([], name="BackCompatSchema")
        assert schema_class is not None

        # Test class has expected attributes
        assert hasattr(schema_class, "model_fields")
        assert hasattr(schema_class, "__name__")
        assert schema_class.__name__ == "BackCompatSchema"
