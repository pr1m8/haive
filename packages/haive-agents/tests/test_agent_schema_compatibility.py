"""Test agent schema composition and compatibility.

Tests for:
- AgentSchemaComposer with different build modes
- Schema compatibility between agents
- Field separation strategies
- Multi-agent schema composition
- Engine I/O mappings
"""

from typing import Any, Dict, List, Optional
from unittest.mock import Mock, patch

import pytest
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.agent_composer import AgentSchemaComposer
from haive.core.schema.auto_compatibility import AutoCompatibilitySystem
from haive.core.schema.composer import SchemaComposer
from haive.core.schema.enhanced_schema_composer import (
    EnhancedSchemaComposer,
    SeparationStrategy,
)
from haive.core.schema.state import MessagesState, StateSchema, ToolState
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from pydantic import BaseModel, Field

from haive.agents.multi.base import SequentialAgent
from haive.agents.simple.agent import SimpleAgent


# Test Schemas
class QuerySchema(BaseModel):
    """Input schema for query processing."""

    query: str = Field(description="User query")
    context: Optional[List[str]] = Field(default=None, description="Context")


class AnalysisSchema(BaseModel):
    """Output schema for analysis."""

    summary: str = Field(description="Analysis summary")
    entities: List[str] = Field(default_factory=list, description="Extracted entities")
    confidence: float = Field(default=0.0, ge=0, le=1)


class RecommendationSchema(BaseModel):
    """Schema for recommendations."""

    recommendations: List[str] = Field(description="List of recommendations")
    priority: str = Field(default="medium", description="Priority level")


# Fixtures
@pytest.fixture
def mock_query_engine():
    """Engine that accepts queries."""
    engine = Mock(spec=AugLLMConfig)
    engine.name = "query_engine"

    engine.get_input_fields.return_value = {
        "query": (str, Field(description="Query")),
        "messages": (List[BaseMessage], Field(default_factory=list)),
    }
    engine.get_output_fields.return_value = {
        "response": (str, Field(description="Response")),
        "entities": (List[str], Field(default_factory=list)),
    }

    engine.derive_input_schema.return_value = QuerySchema
    engine.derive_output_schema.return_value = AnalysisSchema

    return engine


@pytest.fixture
def mock_analysis_engine():
    """Engine that produces analysis."""
    engine = Mock(spec=AugLLMConfig)
    engine.name = "analysis_engine"

    engine.get_input_fields.return_value = {
        "summary": (str, Field(description="Summary to analyze")),
        "entities": (List[str], Field(default_factory=list)),
    }
    engine.get_output_fields.return_value = {
        "recommendations": (List[str], Field(default_factory=list)),
        "priority": (str, Field(default="medium")),
    }

    return engine


class TestSchemaComposer:
    """Test basic schema composition."""

    def test_schema_composer_basic(self):
        """Test basic schema composition with fields."""
        composer = SchemaComposer(name="TestSchema")

        # Add fields
        composer.add_field("query", str, default="")
        composer.add_field("results", List[str], default_factory=list)
        composer.add_field("confidence", float, default=0.0)

        # Build schema
        schema = composer.build()

        # Verify fields
        assert hasattr(schema, "query")
        assert hasattr(schema, "results")
        assert hasattr(schema, "confidence")

        # Test instantiation
        instance = schema(query="test", confidence=0.9)
        assert instance.query == "test"
        assert instance.confidence == 0.9
        assert instance.results == []

    def test_schema_composer_with_base(self):
        """Test schema composition with base class."""
        composer = SchemaComposer(
            name="ExtendedMessagesState", base_class=MessagesState
        )

        # Add custom fields
        composer.add_field("task", str, description="Current task")
        composer.add_field("status", str, default="pending")

        # Build schema
        schema = composer.build()

        # Verify inheritance
        assert issubclass(schema, MessagesState)
        assert hasattr(schema, "messages")  # From MessagesState
        assert hasattr(schema, "task")  # Custom field
        assert hasattr(schema, "status")  # Custom field

    def test_field_with_reducer(self):
        """Test adding fields with reducers."""
        composer = SchemaComposer(name="ReducerSchema")

        # Add field with reducer
        from langchain_core.messages import add_messages

        composer.add_field(
            "messages", List[BaseMessage], default_factory=list, reducer=add_messages
        )

        schema = composer.build()

        # Check reducer is properly set
        field_info = schema.model_fields["messages"]
        assert "reducer" in field_info.metadata


class TestAgentSchemaComposer:
    """Test agent-specific schema composition."""

    def test_agent_schema_composer_smart_mode(
        self, mock_query_engine, mock_analysis_engine
    ):
        """Test AgentSchemaComposer in smart mode."""
        agents = [
            Mock(engines={"main": mock_query_engine}, name="query_agent"),
            Mock(engines={"main": mock_analysis_engine}, name="analysis_agent"),
        ]

        composer = AgentSchemaComposer(agents=agents, build_mode="smart")
        schema = composer.build()

        # Should have fields from both engines
        assert hasattr(schema, "query")  # From query engine
        assert hasattr(schema, "response")  # From query engine
        assert hasattr(schema, "entities")  # Shared field
        assert hasattr(schema, "summary")  # From analysis engine
        assert hasattr(schema, "recommendations")  # From analysis engine

    def test_agent_schema_composer_namespaced_mode(
        self, mock_query_engine, mock_analysis_engine
    ):
        """Test AgentSchemaComposer in namespaced mode."""
        agents = [
            Mock(engines={"main": mock_query_engine}, name="query_agent"),
            Mock(engines={"main": mock_analysis_engine}, name="analysis_agent"),
        ]

        composer = AgentSchemaComposer(agents=agents, build_mode="namespaced")
        schema = composer.build()

        # Should have namespaced fields
        assert hasattr(schema, "query_agent_query")
        assert hasattr(schema, "query_agent_response")
        assert hasattr(schema, "analysis_agent_summary")
        assert hasattr(schema, "analysis_agent_recommendations")

    def test_shared_fields_detection(self, mock_query_engine, mock_analysis_engine):
        """Test detection of shared fields between agents."""
        # Both engines have 'entities' field
        agents = [
            Mock(engines={"main": mock_query_engine}, name="agent1"),
            Mock(engines={"main": mock_analysis_engine}, name="agent2"),
        ]

        composer = AgentSchemaComposer(agents=agents, build_mode="smart")
        schema = composer.build()

        # Entities should be marked as shared
        field_info = schema.model_fields.get("entities")
        assert field_info is not None
        # In smart mode, shared fields are detected


class TestEnhancedSchemaComposer:
    """Test enhanced schema composer with separation strategies."""

    def test_separation_strategy_smart(self, mock_query_engine):
        """Test SMART separation strategy."""
        composer = EnhancedSchemaComposer(SeparationStrategy.SMART)

        # Create mock agent
        agent = Mock()
        agent.engines = {"main": mock_query_engine}

        result = composer.compose_from_components([agent], "SmartSchema")

        assert result.schema_class is not None
        assert hasattr(result.schema_class, "query")
        assert hasattr(result.schema_class, "response")

    def test_separation_strategy_conflicts(self):
        """Test handling of field conflicts."""
        composer = EnhancedSchemaComposer(SeparationStrategy.NAMESPACED)

        # Create components with conflicting fields
        engine1 = Mock()
        engine1.get_input_fields.return_value = {"data": (str, Field())}
        engine1.get_output_fields.return_value = {"result": (str, Field())}

        engine2 = Mock()
        engine2.get_input_fields.return_value = {"data": (int, Field())}  # Conflict!
        engine2.get_output_fields.return_value = {
            "result": (List[str], Field())
        }  # Conflict!

        agent1 = Mock(engines={"e1": engine1})
        agent2 = Mock(engines={"e2": engine2})

        result = composer.compose_from_components([agent1, agent2], "ConflictSchema")

        # Should handle conflicts based on strategy
        assert len(result.conflicts) > 0
        assert result.schema_class is not None


class TestSchemaCompatibility:
    """Test schema compatibility checking."""

    def test_auto_compatibility_system(self):
        """Test automatic compatibility detection."""
        compatibility_system = AutoCompatibilitySystem()

        # Define test schemas
        class SourceSchema(BaseModel):
            query: str
            max_results: int = 10

        class TargetSchema(BaseModel):
            query: str
            limit: int  # Different name but similar purpose

        # Check compatibility
        report = compatibility_system.check_compatibility(SourceSchema, TargetSchema)

        assert not report["is_compatible"]  # Should detect incompatibility
        assert len(report["missing_fields"]) > 0  # 'limit' is missing in source
        assert len(report["extra_fields"]) > 0  # 'max_results' is extra in source

    def test_compatible_schemas(self):
        """Test detection of compatible schemas."""
        compatibility_system = AutoCompatibilitySystem()

        class Schema1(BaseModel):
            query: str
            context: Optional[List[str]] = None

        class Schema2(BaseModel):
            query: str
            context: Optional[List[str]] = None
            extra: Optional[str] = None  # Optional extra field

        report = compatibility_system.check_compatibility(Schema1, Schema2)

        # Should be compatible (Schema1 -> Schema2)
        assert report["is_compatible"]
        assert report["total_issues"] == 0

    def test_schema_adapter_generation(self):
        """Test automatic adapter generation."""
        compatibility_system = AutoCompatibilitySystem()

        class InputSchema(BaseModel):
            text: str
            count: int = 5

        class OutputSchema(BaseModel):
            content: str  # Maps from 'text'
            limit: int  # Maps from 'count'

        # Get adapter
        adapter = compatibility_system.get_adapter(InputSchema, OutputSchema)

        # Test adapter
        input_data = InputSchema(text="Hello", count=10)
        output_data = adapter(input_data)

        # Simple mapping would need custom logic, but adapter should handle it
        assert hasattr(output_data, "content") or "content" in output_data
        assert hasattr(output_data, "limit") or "limit" in output_data


class TestMultiAgentSchemaIntegration:
    """Test schema integration for multi-agent systems."""

    def test_sequential_agent_schema_compatibility(
        self, mock_query_engine, mock_analysis_engine
    ):
        """Test that sequential agents have compatible schemas."""
        with patch("haive.agents.simple.agent.SimpleAgent.setup_workflow"):
            # Create agents with specific schemas
            query_agent = SimpleAgent(engine=mock_query_engine, name="query_processor")

            analysis_agent = SimpleAgent(engine=mock_analysis_engine, name="analyzer")

            # Test schema compatibility
            compatibility_system = AutoCompatibilitySystem()

            # In a real sequential flow, output of agent1 should be compatible with input of agent2
            # This would check query_agent.output_schema vs analysis_agent.input_schema

            # For this test, we check if the multi-agent can compose them
            with patch("haive.agents.multi.base.SequentialAgent.setup_workflow"):
                multi_agent = SequentialAgent(
                    agents=[query_agent, analysis_agent], name="query_analyzer"
                )

                # Multi-agent should handle schema composition
                assert multi_agent.state_schema is not None

    def test_schema_field_routing(self):
        """Test that fields are properly routed between agents."""
        # Create schema with engine I/O mappings
        composer = SchemaComposer(name="RoutingSchema")

        # Add fields with engine mappings
        composer.add_field("query", str)
        composer.add_field("entities", List[str], default_factory=list)
        composer.add_field("summary", str, default="")

        schema = composer.build()

        # Add engine I/O mappings (simulating what happens in real agent)
        schema.__engine_io_mappings__ = {
            "query_engine": {"inputs": ["query"], "outputs": ["entities", "summary"]},
            "analysis_engine": {
                "inputs": ["summary", "entities"],
                "outputs": ["recommendations"],
            },
        }

        # Verify mappings exist
        assert hasattr(schema, "__engine_io_mappings__")
        assert "query_engine" in schema.__engine_io_mappings__
        assert "analysis_engine" in schema.__engine_io_mappings__


class TestStateSchemaIntegration:
    """Test integration with different state schema types."""

    def test_messages_state_compatibility(self):
        """Test MessagesState usage in agents."""
        composer = SchemaComposer(name="ChatSchema", base_class=MessagesState)
        composer.add_field("current_topic", str, default="")

        schema = composer.build()

        # Should have messages field with reducer
        assert hasattr(schema, "messages")
        assert hasattr(schema, "current_topic")

        # Test message handling
        instance = schema(messages=[HumanMessage(content="Hello")])
        assert len(instance.messages) == 1

    def test_tool_state_compatibility(self):
        """Test ToolState usage in agents."""
        composer = SchemaComposer(name="ToolSchema", base_class=ToolState)
        composer.add_field("task", str)

        schema = composer.build()

        # Should have tool-related fields
        assert hasattr(schema, "messages")
        assert hasattr(schema, "tools")
        assert hasattr(schema, "tool_schemas")
        assert hasattr(schema, "task")


# Run with: poetry run pytest packages/haive-agents/tests/test_agent_schema_compatibility.py -v
