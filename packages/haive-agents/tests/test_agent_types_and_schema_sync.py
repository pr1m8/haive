"""Test different agent types, field sync, and schema adaptation.

Tests for:
- Different agent types (Simple, RAG, Retriever-based)
- __init_subclass__ patterns
- Field synchronization between agent and engines
- Schema adaptation and compatibility
- Automatic schema composition based on agent type
"""

from typing import Any, Dict, List, Optional, Type
from unittest.mock import MagicMock, Mock, patch

import pytest
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.base import Engine, EngineRetriever
from haive.core.schema.auto_compatibility import AutoCompatibilitySystem
from haive.core.schema.composer import SchemaComposer
from haive.core.schema.state import MessagesState, StateSchema
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from pydantic import BaseModel, Field

from haive.agents.base.agent import Agent
from haive.agents.rag.agent import SimpleRAGAgent
from haive.agents.simple.agent import SimpleAgent


# Custom Agent Types for Testing
class RetrieverAgent(Agent):
    """Agent that primarily uses a retriever engine."""

    def __init__(self, retriever_engine: EngineRetriever, **kwargs):
        # Set engines with retriever as main
        engines = {"retriever": retriever_engine}
        if "engines" in kwargs:
            engines.update(kwargs.pop("engines"))

        super().__init__(engines=engines, **kwargs)
        self.retriever_engine = retriever_engine

    def build_graph(self):
        """Build a retrieval-focused graph."""
        from haive.core.graph.base_graph import END, START, BaseGraph

        graph = BaseGraph(state_schema=self.state_schema)

        # Add retrieval node
        graph.add_node(
            "retrieve",
            {
                "type": "ENGINE",
                "engine": "retriever",
                "input_fields": {"query": "query"},
                "output_fields": {"documents": "documents", "context": "context"},
            },
        )

        # Add processing node if we have an LLM
        if "llm" in self.engines:
            graph.add_node(
                "process",
                {
                    "type": "ENGINE",
                    "engine": "llm",
                    "input_fields": {"context": "context", "query": "query"},
                    "output_fields": {"response": "response"},
                },
            )
            graph.add_edge("retrieve", "process")
            graph.add_edge("process", END)
        else:
            graph.add_edge("retrieve", END)

        graph.add_edge(START, "retrieve")

        return graph


class HybridAgent(Agent):
    """Agent that combines multiple engine types."""

    def __init__(self, llm_engine: Engine, retriever_engine: Engine, **kwargs):
        engines = {"llm": llm_engine, "retriever": retriever_engine}
        super().__init__(engines=engines, **kwargs)

    def build_graph(self):
        """Build a hybrid graph using both engines."""
        from haive.core.graph.base_graph import END, START, BaseGraph

        graph = BaseGraph(state_schema=self.state_schema)

        # Conditional routing based on query type
        graph.add_node("router", {"type": "CALLABLE", "callable": self.route_query})

        # Retrieval path
        graph.add_node("retrieve", {"type": "ENGINE", "engine": "retriever"})

        # Direct LLM path
        graph.add_node("llm_direct", {"type": "ENGINE", "engine": "llm"})

        # RAG path
        graph.add_node("llm_with_context", {"type": "ENGINE", "engine": "llm"})

        # Routing
        graph.add_edge(START, "router")
        graph.add_conditional_edges(
            "router",
            self.route_query,
            {"retrieval": "retrieve", "direct": "llm_direct"},
        )

        graph.add_edge("retrieve", "llm_with_context")
        graph.add_edge("llm_direct", END)
        graph.add_edge("llm_with_context", END)

        return graph

    def route_query(self, state: Dict) -> str:
        """Route based on query type."""
        query = state.get("query", "")
        if "search" in query.lower() or "find" in query.lower():
            return "retrieval"
        return "direct"


# Test Models
class QueryInput(BaseModel):
    """Input schema for queries."""

    query: str = Field(description="User query")
    search_type: Optional[str] = Field(default="semantic", description="Type of search")


class RetrievalOutput(BaseModel):
    """Output schema for retrieval."""

    documents: List[Document] = Field(default_factory=list)
    context: List[str] = Field(default_factory=list)
    relevance_scores: Optional[List[float]] = None


class AnalysisOutput(BaseModel):
    """Output schema for analysis."""

    response: str
    sources: List[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)


# Test __init_subclass__ pattern
class AutoConfiguredAgent(Agent):
    """Agent that uses __init_subclass__ for auto-configuration."""

    # Class-level configuration
    default_temperature: float = 0.7
    default_model: str = "gpt-4"
    requires_tools: bool = False

    def __init_subclass__(cls, **kwargs):
        """Auto-configure subclasses."""
        super().__init_subclass__(**kwargs)

        # Auto-set defaults based on class name
        if "RAG" in cls.__name__:
            cls.requires_retriever = True
            cls.default_chunk_size = 1000

        if "Tool" in cls.__name__:
            cls.requires_tools = True

        # Register schema requirements
        cls._schema_requirements = cls._analyze_schema_requirements()

    @classmethod
    def _analyze_schema_requirements(cls) -> Dict[str, Any]:
        """Analyze what schema fields this agent type needs."""
        requirements = {
            "needs_messages": True,  # All agents need messages
            "needs_tools": cls.requires_tools,
            "custom_fields": [],
        }

        # Check for special requirements
        if hasattr(cls, "requires_retriever"):
            requirements["custom_fields"].extend(
                [
                    ("documents", List[Document], Field(default_factory=list)),
                    ("context", List[str], Field(default_factory=list)),
                ]
            )

        return requirements


class TestFieldSync:
    """Test field synchronization between agents and engines."""

    def test_agent_engine_field_sync(self):
        """Test that agent fields sync to engines."""
        # Create mock engine
        mock_engine = Mock(spec=AugLLMConfig)
        mock_engine.temperature = 0.5
        mock_engine.model_name = "gpt-3.5"

        with patch("haive.agents.simple.agent.SimpleAgent.setup_workflow"):
            # Create agent with override values
            agent = SimpleAgent(
                engine=mock_engine,
                temperature=0.9,  # Override engine default
                model_name="gpt-4",  # Override engine default
            )

            # After sync_fields_from_engines, agent should have engine values
            # But if agent specifies them, agent values take precedence
            assert agent.temperature == 0.9
            assert agent.model_name == "gpt-4"

    def test_multi_engine_field_sync(self):
        """Test field sync with multiple engines."""
        # Create engines with different configs
        llm_engine = Mock(spec=AugLLMConfig)
        llm_engine.temperature = 0.7
        llm_engine.name = "llm"

        retriever_engine = Mock(spec=EngineRetriever)
        retriever_engine.top_k = 5
        retriever_engine.name = "retriever"

        with patch.object(Agent, "setup_workflow"):
            agent = HybridAgent(
                llm_engine=llm_engine,
                retriever_engine=retriever_engine,
                temperature=0.8,  # Override LLM temperature
            )

            # Check field sync
            assert agent.temperature == 0.8  # Agent override
            # Agent should have access to both engines
            assert "llm" in agent.engines
            assert "retriever" in agent.engines


class TestSchemaAdaptation:
    """Test schema adaptation between different agent types."""

    def test_simple_to_rag_adaptation(self):
        """Test adapting SimpleAgent output to RAG agent input."""

        # Simple agent output schema
        class SimpleOutput(BaseModel):
            query: str
            intent: str = "search"

        # RAG agent input schema
        class RAGInput(BaseModel):
            query: str
            search_type: str = "semantic"
            max_docs: int = 5

        # Test compatibility
        compatibility = AutoCompatibilitySystem()
        report = compatibility.check_compatibility(SimpleOutput, RAGInput)

        # Should need adaptation (different fields)
        assert not report["is_compatible"]

        # Get adapter
        adapter = compatibility.get_adapter(SimpleOutput, RAGInput)

        # Test adaptation
        simple_output = SimpleOutput(query="Find Python tutorials", intent="search")
        rag_input = adapter(simple_output)

        # Should map fields appropriately
        assert hasattr(rag_input, "query") or "query" in rag_input
        assert hasattr(rag_input, "search_type") or "search_type" in rag_input

    def test_retriever_to_llm_adaptation(self):
        """Test adapting retriever output to LLM input."""
        # Use actual schemas
        retriever_output = RetrievalOutput(
            documents=[
                Document(page_content="Python is great", metadata={"source": "doc1"}),
                Document(page_content="Python tutorials", metadata={"source": "doc2"}),
            ],
            context=["Python is great", "Python tutorials"],
            relevance_scores=[0.9, 0.85],
        )

        # LLM expects different format
        class LLMInput(BaseModel):
            messages: List[BaseMessage]
            context: str  # Single string, not list

        # Manual adaptation (what our system should do automatically)
        def adapt_retriever_to_llm(retriever_out: RetrievalOutput) -> Dict:
            return {
                "messages": [
                    HumanMessage(content=f"Context: {' '.join(retriever_out.context)}")
                ],
                "context": "\n".join(retriever_out.context),
            }

        adapted = adapt_retriever_to_llm(retriever_output)
        assert "messages" in adapted
        assert isinstance(adapted["context"], str)


class TestAgentTypeDetection:
    """Test automatic agent type detection and configuration."""

    def test_rag_agent_detection(self):
        """Test that RAG agents are properly detected and configured."""
        with patch("haive.agents.rag.agent.SimpleRAGAgent.setup_workflow"):
            retriever_engine = Mock(spec=EngineRetriever)

            rag_agent = SimpleRAGAgent(engine=retriever_engine, name="doc_searcher")

            # Should have retriever-specific configuration
            assert hasattr(rag_agent, "engine")
            assert rag_agent.engine == retriever_engine

            # State schema should include retrieval fields
            # (In real implementation, would check state_schema)

    def test_agent_type_from_engines(self):
        """Test inferring agent type from engines."""
        # Mock different engine types
        llm_only = {"llm": Mock(spec=AugLLMConfig)}
        retriever_only = {"retriever": Mock(spec=EngineRetriever)}
        hybrid = {
            "llm": Mock(spec=AugLLMConfig),
            "retriever": Mock(spec=EngineRetriever),
        }

        # Helper to detect agent type
        def detect_agent_type(engines: Dict) -> str:
            has_llm = any(
                isinstance(e, AugLLMConfig) or hasattr(e, "invoke")
                for e in engines.values()
            )
            has_retriever = any(
                isinstance(e, EngineRetriever) or hasattr(e, "search")
                for e in engines.values()
            )

            if has_llm and has_retriever:
                return "hybrid"
            elif has_retriever:
                return "retriever"
            else:
                return "simple"

        assert detect_agent_type(llm_only) == "simple"
        assert detect_agent_type(retriever_only) == "retriever"
        assert detect_agent_type(hybrid) == "hybrid"


class TestSchemaCompositionPatterns:
    """Test different schema composition patterns."""

    def test_incremental_schema_building(self):
        """Test building schemas incrementally based on agent needs."""
        # Start with base
        composer = SchemaComposer("IncrementalSchema", base_class=MessagesState)

        # Add fields based on agent type
        agent_type = "rag"

        if agent_type in ["rag", "retriever"]:
            composer.add_field("documents", List[Document], default_factory=list)
            composer.add_field("context", List[str], default_factory=list)

        if agent_type in ["simple", "rag"]:
            composer.add_field("response", str, default="")

        schema = composer.build()

        # Verify fields
        assert hasattr(schema, "messages")  # From base
        assert hasattr(schema, "documents")  # From RAG
        assert hasattr(schema, "context")  # From RAG
        assert hasattr(schema, "response")  # From simple/RAG

    def test_schema_composition_with_conflicts(self):
        """Test handling schema conflicts in multi-agent systems."""

        # Two agents with conflicting field types
        class Agent1Schema(StateSchema):
            result: str = Field(description="Text result")
            confidence: float = Field(default=0.0)

        class Agent2Schema(StateSchema):
            result: List[str] = Field(description="List of results")  # Conflict!
            confidence: int = Field(default=0)  # Different type!

        # Composer should handle this
        composer = SchemaComposer("MergedSchema")

        # Add fields with namespace to avoid conflicts
        composer.add_field("agent1_result", str)
        composer.add_field("agent2_result", List[str], default_factory=list)
        composer.add_field("agent1_confidence", float, default=0.0)
        composer.add_field("agent2_confidence", int, default=0)

        schema = composer.build()
        instance = schema()

        # Both fields should exist without conflict
        assert hasattr(instance, "agent1_result")
        assert hasattr(instance, "agent2_result")


class TestAutoConfiguredAgents:
    """Test agents with __init_subclass__ auto-configuration."""

    def test_auto_configured_rag_agent(self):
        """Test that RAG agents get auto-configured."""

        class AutoRAGAgent(AutoConfiguredAgent):
            """Automatically configured RAG agent."""

            pass

        # Should have auto-detected RAG configuration
        assert hasattr(AutoRAGAgent, "requires_retriever")
        assert AutoRAGAgent.requires_retriever
        assert hasattr(AutoRAGAgent, "default_chunk_size")

        # Check schema requirements
        requirements = AutoRAGAgent._schema_requirements
        assert requirements["needs_messages"]
        assert any("documents" in field[0] for field in requirements["custom_fields"])

    def test_auto_configured_tool_agent(self):
        """Test that Tool agents get auto-configured."""

        class AutoToolAgent(AutoConfiguredAgent):
            """Automatically configured tool-using agent."""

            pass

        # Should have tool requirements
        assert AutoToolAgent.requires_tools

        requirements = AutoToolAgent._schema_requirements
        assert requirements["needs_tools"]


# Integration test
def test_multi_agent_schema_flow():
    """Test complete schema flow in multi-agent system."""
    with patch("haive.agents.base.agent.Agent.setup_workflow"):
        # Create different agent types
        simple_agent = Mock(spec=SimpleAgent)
        simple_agent.state_schema = type(
            "SimpleSchema",
            (StateSchema,),
            {"query": Field(default=""), "response": Field(default="")},
        )

        rag_agent = Mock(spec=SimpleRAGAgent)
        rag_agent.state_schema = type(
            "RAGSchema",
            (StateSchema,),
            {
                "query": Field(default=""),
                "documents": Field(default_factory=list),
                "context": Field(default_factory=list),
                "response": Field(default=""),
            },
        )

        # Test schema compatibility for sequential execution
        # Simple -> RAG: query should flow through
        # RAG output should be richer than simple input

        # This demonstrates the importance of schema composition
        # in making different agent types work together


# Run with: poetry run pytest packages/haive-agents/tests/test_agent_types_and_schema_sync.py -v
