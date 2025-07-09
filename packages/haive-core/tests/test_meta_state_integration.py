"""Tests for MetaStateSchema integration with the Haive agent system.

This test module validates that MetaStateSchema properly integrates with
existing agents and the broader Haive framework, ensuring that the meta
agent pattern works correctly with real agent implementations.
"""

from typing import Any, Dict, List
from unittest.mock import MagicMock, Mock

import pytest
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from pydantic import ValidationError

from haive.core.graph.node.meta_agent_node import MetaAgentNodeConfig
from haive.core.schema.prebuilt.meta_state import MetaStateSchema


class MockAgent:
    """Mock agent for testing purposes."""

    def __init__(self, name: str = "test_agent", should_fail: bool = False):
        self.name = name
        self.should_fail = should_fail
        self.engines = {"main": Mock()}
        self.engine = self.engines["main"]
        self.call_count = 0

    def run(self, input_data: Dict[str, Any], **config) -> Dict[str, Any]:
        """Mock run method."""
        self.call_count += 1

        if self.should_fail:
            raise RuntimeError("Mock agent failure")

        messages = input_data.get("messages", [])
        response = AIMessage(content=f"Response from {self.name}")

        return {
            "messages": messages + [response],
            "agent_response": f"Processed by {self.name}",
            "call_count": self.call_count,
        }

    def invoke(
        self, input_data: Dict[str, Any], config: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Mock invoke method."""
        return self.run(input_data, **(config or {}))


class TestMetaStateSchema:
    """Test cases for MetaStateSchema."""

    def test_basic_creation(self):
        """Test basic MetaStateSchema creation."""
        agent = MockAgent("test_agent")

        meta_state = MetaStateSchema(
            agent=agent,
            agent_input={"test": "data"},
            meta_context={"purpose": "testing"},
        )

        assert meta_state.agent is agent
        assert meta_state.agent_name == "test_agent"
        assert meta_state.agent_type == "MockAgent"
        assert meta_state.agent_input == {"test": "data"}
        assert meta_state.meta_context["purpose"] == "testing"
        assert meta_state.execution_status == "ready"

    def test_from_agent_factory(self):
        """Test creating MetaStateSchema from agent using factory method."""
        agent = MockAgent("factory_agent")

        meta_state = MetaStateSchema.from_agent(
            agent=agent,
            initial_input={"messages": [HumanMessage(content="Hello")]},
            meta_context={"created_via": "factory"},
        )

        assert meta_state.agent is agent
        assert meta_state.agent_name == "factory_agent"
        assert meta_state.agent_input["messages"][0].content == "Hello"
        assert meta_state.meta_context["created_via"] == "factory"

    def test_engine_synchronization(self):
        """Test that engines are synced from the embedded agent."""
        agent = MockAgent("engine_agent")
        agent.engines["custom"] = Mock(name="custom_engine")

        meta_state = MetaStateSchema(agent=agent)

        # Check that agent engines are synced with prefix
        assert "agent_main" in meta_state.engines
        assert "agent_custom" in meta_state.engines
        assert meta_state.engine is not None

    def test_agent_execution_success(self):
        """Test successful agent execution."""
        agent = MockAgent("exec_agent")

        meta_state = MetaStateSchema(
            agent=agent, agent_input={"messages": [HumanMessage(content="Test input")]}
        )

        # Execute agent
        result = meta_state.execute_agent()

        # Check execution results
        assert result["status"] == "success"
        assert meta_state.execution_status == "completed"
        assert meta_state.agent_output["agent_response"] == "Processed by exec_agent"
        assert len(meta_state.execution_history) == 1
        assert len(meta_state.messages) > 0  # Should have synced messages

    def test_agent_execution_failure(self):
        """Test agent execution failure handling."""
        agent = MockAgent("fail_agent", should_fail=True)

        meta_state = MetaStateSchema(agent=agent)

        # Execute agent (should fail)
        with pytest.raises(RuntimeError, match="Agent execution failed"):
            meta_state.execute_agent()

        # Check error state
        assert meta_state.execution_status == "error"
        assert meta_state.error_info is not None
        assert "Mock agent failure" in meta_state.error_info["error"]

    def test_input_preparation(self):
        """Test agent input preparation methods."""
        agent = MockAgent("input_agent")

        meta_state = MetaStateSchema(
            agent=agent,
            messages=[HumanMessage(content="Existing message")],
            agent_input={"custom": "data"},
            meta_context={"context": "info"},
        )

        # Test input preparation with different options
        input_data = meta_state.prepare_agent_input(
            additional_input={"extra": "field"},
            include_messages=True,
            include_context=True,
        )

        assert "messages" in input_data
        assert "meta_context" in input_data
        assert "custom" in input_data
        assert "extra" in input_data
        assert input_data["extra"] == "field"

    def test_state_cloning(self):
        """Test state cloning with different agents."""
        original_agent = MockAgent("original")
        new_agent = MockAgent("new")

        # Create original state with execution history
        meta_state = MetaStateSchema(agent=original_agent)
        meta_state.execute_agent()

        # Clone with new agent
        cloned_state = meta_state.clone_with_agent(new_agent, reset_history=True)

        assert cloned_state.agent is new_agent
        assert cloned_state.agent_name == "new"
        assert len(cloned_state.execution_history) == 0
        assert cloned_state.execution_status == "ready"

        # Original state should be unchanged
        assert meta_state.agent is original_agent
        assert len(meta_state.execution_history) == 1

    def test_execution_summary(self):
        """Test execution summary generation."""
        agent = MockAgent("summary_agent")
        meta_state = MetaStateSchema(agent=agent)

        # Execute multiple times
        meta_state.execute_agent()
        meta_state.execute_agent()

        summary = meta_state.get_execution_summary()

        assert summary["total_executions"] == 2
        assert summary["successful_executions"] == 2
        assert summary["failed_executions"] == 0
        assert summary["success_rate"] == 1.0
        assert summary["agent_name"] == "summary_agent"

    def test_get_agent_engine(self):
        """Test getting engines from the embedded agent."""
        agent = MockAgent("engine_test")
        agent.engines["special"] = Mock(name="special_engine")

        meta_state = MetaStateSchema(agent=agent)

        # Test getting main engine
        main_engine = meta_state.get_agent_engine("main")
        assert main_engine is not None

        # Test getting special engine
        special_engine = meta_state.get_agent_engine("special")
        assert special_engine is not None

        # Test non-existent engine
        none_engine = meta_state.get_agent_engine("nonexistent")
        assert none_engine is None


class TestMetaAgentNodeConfig:
    """Test cases for MetaAgentNodeConfig."""

    def test_node_creation(self):
        """Test creating MetaAgentNodeConfig."""
        node = MetaAgentNodeConfig(
            name="test_meta_node",
            input_preparation="auto",
            output_handling="merge",
            error_handling="capture",
        )

        assert node.name == "test_meta_node"
        assert node.input_preparation == "auto"
        assert node.output_handling == "merge"
        assert node.error_handling == "capture"

    def test_is_meta_state_validation(self):
        """Test meta state validation."""
        node = MetaAgentNodeConfig(name="test_node")

        # Test with valid meta state
        meta_state = MetaStateSchema(agent=MockAgent())
        assert node._is_meta_state(meta_state) is True

        # Test with invalid state
        invalid_state = {"not": "meta_state"}
        assert node._is_meta_state(invalid_state) is False

    def test_agent_extraction(self):
        """Test agent extraction from meta state."""
        agent = MockAgent("extracted_agent")
        node = MetaAgentNodeConfig(name="test_node")
        meta_state = MetaStateSchema(agent=agent)

        extracted_agent = node._extract_agent(meta_state)
        assert extracted_agent is agent

    def test_input_preparation_strategies(self):
        """Test different input preparation strategies."""
        node = MetaAgentNodeConfig(name="test_node")
        agent = MockAgent("prep_agent")

        meta_state = MetaStateSchema(
            agent=agent,
            messages=[HumanMessage(content="Test")],
            agent_input={"custom": "data"},
            meta_context={"info": "context"},
        )

        # Test auto preparation
        node.input_preparation = "auto"
        node.include_messages = True
        node.include_meta_context = True
        auto_input = node._prepare_agent_input(meta_state)
        assert "messages" in auto_input
        assert "custom" in auto_input
        assert "meta_context" in auto_input

        # Test agent_input only
        node.input_preparation = "agent_input"
        agent_input = node._prepare_agent_input(meta_state)
        assert agent_input == {"custom": "data"}

        # Test messages only
        node.input_preparation = "messages"
        messages_input = node._prepare_agent_input(meta_state)
        assert "messages" in messages_input
        assert len(messages_input) == 1

    def test_execution_flow(self):
        """Test the complete node execution flow."""
        agent = MockAgent("flow_agent")
        meta_state = MetaStateSchema(
            agent=agent, agent_input={"messages": [HumanMessage(content="Flow test")]}
        )

        node = MetaAgentNodeConfig(
            name="flow_node",
            input_preparation="auto",
            output_handling="merge",
            error_handling="capture",
        )

        # Execute the node
        result = node(meta_state)

        # Check that we get a Command or Send back
        assert hasattr(result, "update") or hasattr(result, "arg")

        # The result should contain updated state
        if hasattr(result, "update"):
            update_data = result.update
        else:
            update_data = result.arg

        assert update_data["execution_status"] == "completed"
        assert "agent_output" in update_data

    def test_error_handling_strategies(self):
        """Test different error handling strategies."""
        failing_agent = MockAgent("failing_agent", should_fail=True)
        meta_state = MetaStateSchema(agent=failing_agent)

        # Test capture error handling
        node = MetaAgentNodeConfig(name="error_node", error_handling="capture")

        result = node(meta_state)

        # Should get a result with error information
        if hasattr(result, "update"):
            update_data = result.update
        else:
            update_data = result.arg

        assert update_data["execution_status"] == "error"
        assert update_data["error_info"] is not None


class TestMetaStateIntegration:
    """Integration tests for meta state with real agent components."""

    def test_message_handling(self):
        """Test that messages are properly handled throughout the meta state."""
        agent = MockAgent("message_agent")

        # Create meta state with initial messages
        initial_messages = [HumanMessage(content="Initial message")]
        meta_state = MetaStateSchema(
            agent=agent,
            messages=initial_messages,
            agent_input={"messages": initial_messages},
        )

        # Execute agent
        meta_state.execute_agent()

        # Check that messages were updated
        assert len(meta_state.messages) > len(initial_messages)
        assert any(isinstance(msg, AIMessage) for msg in meta_state.messages)

    def test_engine_integration(self):
        """Test that engines are properly integrated in meta state."""
        agent = MockAgent("engine_integration_agent")
        agent.engine.name = "main_engine"
        agent.engines["secondary"] = Mock(name="secondary_engine")

        meta_state = MetaStateSchema(agent=agent)

        # Check engine synchronization
        assert meta_state.engine is not None
        assert "agent_main" in meta_state.engines
        assert "agent_secondary" in meta_state.engines

        # Check engine retrieval
        main_engine = meta_state.get_agent_engine("main")
        assert main_engine is agent.engine

        secondary_engine = meta_state.get_agent_engine("secondary")
        assert secondary_engine is agent.engines["secondary"]

    def test_reducer_functionality(self):
        """Test that reducers work correctly with meta state."""
        agent = MockAgent("reducer_agent")

        # Create meta state with initial data
        meta_state = MetaStateSchema(
            agent=agent,
            messages=[HumanMessage(content="Message 1")],
            execution_history=[{"test": "data1"}],
        )

        # Apply reducers by updating with new data
        new_data = {
            "messages": [HumanMessage(content="Message 2")],
            "execution_history": [{"test": "data2"}],
        }

        meta_state.apply_reducers(new_data)

        # Check that reducers were applied correctly
        assert len(meta_state.messages) == 2  # Messages should be added
        assert len(meta_state.execution_history) == 2  # History should be appended

    def test_shared_fields(self):
        """Test that shared fields work correctly in meta state."""
        # Create parent and child meta states
        parent_agent = MockAgent("parent_agent")
        child_agent = MockAgent("child_agent")

        parent_state = MetaStateSchema(
            agent=parent_agent, messages=[HumanMessage(content="Parent message")]
        )

        child_state = MetaStateSchema(
            agent=child_agent, messages=[HumanMessage(content="Child message")]
        )

        # Test field sharing behavior
        # This would typically be handled by the graph framework
        # but we can test the underlying state schema functionality

        assert parent_state.__shared_fields__ == [
            "messages",
            "agent_output",
            "execution_status",
        ]
        assert "messages" in parent_state.__shared_fields__

    def test_serialization_compatibility(self):
        """Test that meta state can be serialized and deserialized."""
        agent = MockAgent("serialization_agent")

        # Create meta state
        original_state = MetaStateSchema(
            agent=agent,
            agent_input={"test": "data"},
            meta_context={"serialization": "test"},
        )

        # Execute to add history
        original_state.execute_agent()

        # Serialize to dict
        state_dict = original_state.model_dump()

        # Check that important fields are preserved
        assert "agent_name" in state_dict
        assert "agent_type" in state_dict
        assert "execution_history" in state_dict
        assert "agent_output" in state_dict

        # Note: The actual agent object won't be serialized,
        # but the metadata about it should be preserved


if __name__ == "__main__":
    """Run the tests."""
    pytest.main([__file__, "-v"])
