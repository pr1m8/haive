"""Test WebSocket schema behavior with SimpleAgent."""

import pytest
from haive.core.engine.aug_llm import AugLLMConfig

from haive.agents.simple.agent import SimpleAgent


def create_weather_tool():
    """Create a simple weather tool for testing."""

    def get_weather(location: str) -> str:
        """Get the current weather for a location."""
        return f"The weather in {location} is sunny and 72°F"

    return get_weather


class TestSimpleAgentSchema:
    """Test SimpleAgent schema generation with and without tools."""

    def test_simple_agent_without_tools(self):
        """Test SimpleAgent schema without tools."""
        agent = SimpleAgent(
            name="test_no_tools",
            engine=AugLLMConfig(
                model="gpt-3.5-turbo",
                prompt_template="You are a helpful assistant. Answer: {messages}",
            ),
            set_schema=True,
        )

        # Check schemas
        print(f"\nWithout tools:")
        print(f"Input schema fields: {list(agent.input_schema.model_fields.keys())}")
        print(f"State schema fields: {list(agent.state_schema.model_fields.keys())}")
        print(f"State schema base: {agent.state_schema.__bases__}")

        # Should have MessagesState
        assert "messages" in agent.input_schema.model_fields
        assert "messages" in agent.state_schema.model_fields
        assert len(agent.state_schema.model_fields) == 1  # Only messages

    def test_simple_agent_with_tools(self):
        """Test SimpleAgent schema with tools."""
        agent = SimpleAgent(
            name="test_with_tools",
            engine=AugLLMConfig(
                model="gpt-3.5-turbo",
                prompt_template="You are a helpful assistant. Answer: {messages}",
                tools=[create_weather_tool()],
            ),
            set_schema=True,
        )

        # Check schemas
        print(f"\nWith tools:")
        print(f"Input schema fields: {list(agent.input_schema.model_fields.keys())}")
        print(f"State schema fields: {list(agent.state_schema.model_fields.keys())}")
        print(f"State schema base: {agent.state_schema.__bases__}")

        # Should have ToolState with extra fields
        assert "messages" in agent.input_schema.model_fields
        assert "messages" in agent.state_schema.model_fields

        # Check if it has tool-related fields
        tool_fields = {
            "tools",
            "tool_routes",
            "name_attrs",
            "content",
            "output_schemas",
            "engine_route_config",
        }
        state_fields = set(agent.state_schema.model_fields.keys())

        # With tools, it should have ToolState fields
        assert tool_fields.issubset(
            state_fields
        ), f"Missing tool fields: {tool_fields - state_fields}"
        assert len(state_fields) > 1  # More than just messages

    def test_minimal_input_works_with_tools(self):
        """Test that minimal input still works even with ToolState schema."""
        agent = SimpleAgent(
            name="test_minimal_input",
            engine=AugLLMConfig(
                model="gpt-3.5-turbo",
                prompt_template="You are a helpful assistant. Answer: {messages}",
                tools=[create_weather_tool()],
            ),
            set_schema=True,
        )

        # Test with minimal input (just messages)
        minimal_input = {"messages": [{"role": "user", "content": "Hello"}]}

        # This should work even though schema has 7 fields
        try:
            result = agent.invoke(minimal_input)
            print(f"\nMinimal input test:")
            print(f"✓ Invoked successfully with minimal input")
            print(f"Result type: {type(result)}")
            print(
                f"Result keys: {list(result.keys()) if hasattr(result, 'keys') else 'N/A'}"
            )
        except Exception as e:
            pytest.fail(f"Minimal input failed: {e}")

    def test_schema_field_details(self):
        """Examine the actual field requirements in schemas."""
        agent_with_tools = SimpleAgent(
            name="test_field_details",
            engine=AugLLMConfig(model="gpt-3.5-turbo", tools=[create_weather_tool()]),
            set_schema=True,
        )

        print(f"\nField details for agent with tools:")
        print(f"State schema: {agent_with_tools.state_schema.__name__}")

        # Check which fields are required
        for (
            field_name,
            field_info,
        ) in agent_with_tools.state_schema.model_fields.items():
            is_required = field_info.is_required()
            default = field_info.default
            print(f"  {field_name}: required={is_required}, default={default}")

        # Check input schema
        print(f"\nInput schema: {agent_with_tools.input_schema.__name__}")
        for (
            field_name,
            field_info,
        ) in agent_with_tools.input_schema.model_fields.items():
            is_required = field_info.is_required()
            print(f"  {field_name}: required={is_required}")


if __name__ == "__main__":
    # Run tests directly
    test = TestSimpleAgentSchema()
    test.test_simple_agent_without_tools()
    test.test_simple_agent_with_tools()
    test.test_minimal_input_works_with_tools()
    test.test_schema_field_details()
