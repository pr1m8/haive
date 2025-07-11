"""Test to verify if SimpleAgent's engine schema modification is actually necessary.

This test creates SimpleAgent instances with structured output models and verifies
that they work correctly both with and without the engine schema modification.
"""

from typing import Optional
from unittest.mock import patch

import pytest
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field

from haive.agents.simple.agent import SimpleAgent


# Test models for structured output
class TaskResult(BaseModel):
    """Test model for structured output."""

    completed: bool = Field(description="Whether the task is completed")
    result: str = Field(description="The result of the task")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in the result")


class AnalysisOutput(BaseModel):
    """Test model for analysis output."""

    summary: str = Field(description="Summary of the analysis")
    key_points: list[str] = Field(description="Key points identified")
    confidence_score: float = Field(
        ge=0.0, le=1.0, description="Confidence in analysis"
    )


@pytest.fixture
def llm_config():
    """Mock LLM config for testing."""
    return AzureLLMConfig(
        model="gpt-4",
        api_version="2024-02-15-preview",
        azure_endpoint="https://test.openai.azure.com/",
        api_key="test_key",
    )


@pytest.fixture
def v1_engine_config(llm_config):
    """AugLLM config with v1 structured output."""
    return AugLLMConfig(
        name="test_v1_engine",
        llm_config=llm_config,
        structured_output_model=TaskResult,
        structured_output_version="v1",
    )


@pytest.fixture
def v2_engine_config(llm_config):
    """AugLLM config with v2 structured output."""
    return AugLLMConfig(
        name="test_v2_engine",
        llm_config=llm_config,
        structured_output_model=TaskResult,
        structured_output_version="v2",
    )


class TestEngineModificationNecessity:
    """Test whether SimpleAgent's engine schema modification is necessary."""

    def test_v1_without_modification_has_structured_fields(self, v1_engine_config):
        """Test that v1 engine naturally includes structured output fields."""
        # Get the engine's natural output schema (before any modification)
        natural_schema = v1_engine_config.derive_output_schema()
        natural_fields = natural_schema.model_fields.keys()

        # V1 should naturally include the structured output fields
        assert (
            "completed" in natural_fields
        ), "V1 should include 'completed' field naturally"
        assert "result" in natural_fields, "V1 should include 'result' field naturally"
        assert (
            "confidence" in natural_fields
        ), "V1 should include 'confidence' field naturally"
        assert "messages" in natural_fields, "V1 should include 'messages' field"

    def test_v2_without_modification_has_messages_only(self, v2_engine_config):
        """Test that v2 engine only has messages field (no structured fields)."""
        # Get the engine's natural output schema (before any modification)
        natural_schema = v2_engine_config.derive_output_schema()
        natural_fields = natural_schema.model_fields.keys()

        # V2 should only have messages field
        assert "messages" in natural_fields, "V2 should include 'messages' field"
        assert (
            "completed" not in natural_fields
        ), "V2 should NOT include structured fields naturally"
        assert (
            "result" not in natural_fields
        ), "V2 should NOT include structured fields naturally"
        assert (
            "confidence" not in natural_fields
        ), "V2 should NOT include structured fields naturally"

    def test_parser_finds_structured_model_directly(
        self, v1_engine_config, v2_engine_config
    ):
        """Test that parser can find structured output model via direct lookup."""
        # Both v1 and v2 should have the structured output model accessible
        assert hasattr(
            v1_engine_config, "structured_output_model"
        ), "V1 engine should have structured_output_model"
        assert (
            v1_engine_config.structured_output_model == TaskResult
        ), "V1 should have correct model"

        assert hasattr(
            v2_engine_config, "structured_output_model"
        ), "V2 engine should have structured_output_model"
        assert (
            v2_engine_config.structured_output_model == TaskResult
        ), "V2 should have correct model"

    def test_v2_has_model_in_pydantic_tools(self, v2_engine_config):
        """Test that v2 engine has structured output model in pydantic_tools."""
        # V2 should include the model as a tool
        assert hasattr(
            v2_engine_config, "pydantic_tools"
        ), "V2 engine should have pydantic_tools"
        assert (
            TaskResult in v2_engine_config.pydantic_tools
        ), "TaskResult should be in pydantic_tools"

    def test_simple_agent_with_modification_disabled(self, v1_engine_config):
        """Test SimpleAgent creation with engine modification disabled."""
        # Patch the _modify_engine_schema method to do nothing
        with patch.object(SimpleAgent, "_modify_engine_schema") as mock_modify:
            agent = SimpleAgent(
                name="test_agent_no_modification",
                engine=v1_engine_config,
                structured_output_model=TaskResult,
            )

            # Verify the method was called (but we prevented it from executing)
            mock_modify.assert_called_once()

            # Agent should still be created successfully
            assert agent.name == "test_agent_no_modification"
            assert agent.engine == v1_engine_config
            assert agent.structured_output_model == TaskResult

    def test_simple_agent_v2_with_modification_disabled(self, v2_engine_config):
        """Test SimpleAgent with v2 engine and modification disabled."""
        with patch.object(SimpleAgent, "_modify_engine_schema") as mock_modify:
            agent = SimpleAgent(
                name="test_agent_v2_no_modification",
                engine=v2_engine_config,
                structured_output_model=TaskResult,
            )

            # Verify setup completed
            mock_modify.assert_called_once()
            assert agent.engine == v2_engine_config

            # The engine should still have the structured output model available for parser
            assert hasattr(agent.engine, "structured_output_model")
            assert agent.engine.structured_output_model == TaskResult

    def test_parser_node_creation_without_modification(self, v1_engine_config):
        """Test that parser node can be created without engine modification."""
        from haive.core.graph.node.parser_node_config import ParserNodeConfig

        # Mock agent that doesn't modify engine
        with patch.object(SimpleAgent, "_modify_engine_schema"):
            agent = SimpleAgent(
                name="test_parser_node",
                engine=v1_engine_config,
                structured_output_model=TaskResult,
            )

            # Create parser node config
            parser_config = ParserNodeConfig(
                name="test_parser", engine_name=agent.engine.name
            )

            # Parser should be able to find the structured output model
            assert parser_config.engine_name == agent.engine.name

            # The engine should have the structured output model accessible
            mock_state = type(
                "MockState", (), {"engines": {agent.engine.name: agent.engine}}
            )()

            engine = parser_config._get_engine_from_state(mock_state)
            assert engine == agent.engine

            # Should be able to find the tool
            tool_class = parser_config._find_tool_in_engine(engine, "TaskResult")
            assert tool_class == TaskResult

    def test_engine_schema_comparison_with_and_without_modification(
        self, v1_engine_config
    ):
        """Compare engine schemas with and without modification to see the difference."""
        # Get original schema before any modification
        original_schema = v1_engine_config.derive_output_schema()
        original_fields = set(original_schema.model_fields.keys())

        # Create agent with modification (normal behavior)
        agent_with_mod = SimpleAgent(
            name="agent_with_modification",
            engine=v1_engine_config,
            structured_output_model=TaskResult,
        )

        # Get modified schema
        modified_schema = agent_with_mod.engine.derive_output_schema()
        modified_fields = set(modified_schema.model_fields.keys())

        # Check what fields were added by modification
        added_fields = modified_fields - original_fields

        # The modification should add a field for the structured output model
        assert len(added_fields) > 0, "Modification should add fields"

        # Should add a field with the model name (lowercased, cleaned)
        expected_field_name = "taskresult"  # Based on SimpleAgent's field naming logic
        assert any(
            expected_field_name in field.lower() for field in added_fields
        ), f"Should add field for TaskResult, got: {added_fields}"

    def test_state_schema_composition_without_engine_modification(
        self, v1_engine_config
    ):
        """Test that agent state schema can be composed without engine modification."""
        from haive.core.schema.schema_composer import SchemaComposer

        # Create schema composer with unmodified engine
        composer = SchemaComposer(name="TestState")
        composer.add_fields_from_components([v1_engine_config])

        # Build state schema
        state_schema = composer.build()
        state_fields = state_schema.model_fields.keys()

        # Should include the natural fields from v1 engine
        assert (
            "completed" in state_fields
        ), "State should include structured fields from v1 engine"
        assert "result" in state_fields
        assert "confidence" in state_fields
        assert "messages" in state_fields

    @pytest.mark.parametrize(
        "engine_config_fixture", ["v1_engine_config", "v2_engine_config"]
    )
    def test_both_versions_work_without_modification(
        self, request, engine_config_fixture
    ):
        """Test that both v1 and v2 work without engine modification."""
        engine_config = request.getfixturevalue(engine_config_fixture)

        with patch.object(SimpleAgent, "_modify_engine_schema") as mock_modify:
            agent = SimpleAgent(
                name=f"test_agent_{engine_config_fixture}",
                engine=engine_config,
                structured_output_model=TaskResult,
            )

            # Verify modification was bypassed
            mock_modify.assert_called_once()

            # Agent should be fully functional
            assert agent.engine == engine_config
            assert agent.structured_output_model == TaskResult

            # Should be able to build graph
            graph = agent.build_graph()
            assert graph is not None
            assert len(graph.nodes) > 0

            # Parser node should be created if needed
            if agent._needs_parser_node():
                assert "parse_output" in graph.nodes or any(
                    "parse" in name for name in graph.nodes
                )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
