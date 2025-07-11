"""Complete multi-agent test bringing together all concepts.

This test demonstrates:
- Multi-agent with conditional edges
- model_post_init usage
- Component composition
- Schema compatibility and adaptation
- Different agent types working together
"""

from typing import Any, Dict, List, Literal, Optional
from unittest.mock import MagicMock, Mock, patch

import pytest
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.base import EngineRetriever
from haive.core.graph.base_graph import END, START, BaseGraph
from haive.core.schema.composer import SchemaComposer
from haive.core.schema.state import MessagesState, ToolState
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field, field_validator, model_validator

from haive.agents.base.agent import Agent
from haive.agents.multi.base import MultiAgent, SequentialAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent


# Enhanced Multi-Agent with Conditional Routing
class ConditionalMultiAgent(MultiAgent):
    """Multi-agent that uses conditional edges for dynamic routing."""

    router_config: dict[str, Any] = Field(default_factory=dict)
    enable_conditional_routing: bool = Field(default=True)

    def model_post_init(self, __context):
        """Use model_post_init to set up routing and validate agents."""
        super().model_post_init(__context)

        # Validate agent compatibility
        self._validate_agent_compatibility()

        # Set up conditional routing configuration
        if self.enable_conditional_routing:
            self._setup_routing_config()

        # Pre-compute schema mappings for efficiency
        self._precompute_schema_mappings()

    def _validate_agent_compatibility(self):
        """Validate that agents can work together."""
        if len(self.agents) < 2:
            return

        for i in range(len(self.agents) - 1):
            current = self.agents[i]
            next_agent = self.agents[i + 1]

            # Check schema compatibility
            # In real implementation, would use AutoCompatibilitySystem
            logger.info(
                f"Validating compatibility: {current.name} -> {next_agent.name}"
            )

    def _setup_routing_config(self):
        """Set up configuration for conditional routing."""
        self.router_config = {
            "routes": {},
            "default_route": "sequential",
            "routing_function": self._route_based_on_state,
        }

        # Map agent capabilities to routes
        for agent in self.agents:
            if hasattr(agent, "engine") and hasattr(agent.engine, "tools"):
                self.router_config["routes"][f"needs_tools_{agent.name}"] = agent.name

    def _precompute_schema_mappings(self):
        """Pre-compute schema field mappings between agents."""
        self._schema_mappings = {}

        for i in range(len(self.agents) - 1):
            source = self.agents[i]
            target = self.agents[i + 1]

            # Store mapping info
            self._schema_mappings[f"{source.name}_to_{target.name}"] = {
                "source_outputs": getattr(source, "output_fields", []),
                "target_inputs": getattr(target, "input_fields", []),
            }

    def _route_based_on_state(self, state: dict) -> str:
        """Routing function for conditional edges."""
        # Example routing logic
        last_message = state.get("messages", [])[-1] if state.get("messages") else None

        if not last_message:
            return "sequential"

        content = getattr(last_message, "content", "")

        # Route based on content
        if "analyze" in content.lower():
            return "analyzer"
        if "search" in content.lower():
            return "searcher"
        return "sequential"

    def build_graph(self) -> BaseGraph:
        """Build graph with conditional edges."""
        graph = BaseGraph(state_schema=self.state_schema)

        # Add router node
        graph.add_node(
            "router",
            {
                "type": "CALLABLE",
                "callable": self._route_based_on_state,
                "description": "Route to appropriate agent",
            },
        )

        # Add agent nodes
        for agent in self.agents:
            graph.add_node(
                agent.name,
                {
                    "type": "AGENT",
                    "agent": agent,
                    "private_state_schema": self._agent_private_states.get(agent.name),
                },
            )

        # Start with router
        graph.add_edge(START, "router")

        # Add conditional edges from router
        routes = {agent.name: agent.name for agent in self.agents}
        routes["sequential"] = self.agents[0].name  # Default

        graph.add_conditional_edges("router", self._route_based_on_state, routes)

        # Connect agents sequentially as fallback
        for i in range(len(self.agents) - 1):
            graph.add_edge(self.agents[i].name, self.agents[i + 1].name)

        # End
        graph.add_edge(self.agents[-1].name, END)

        return graph


# Component-based Agent using composition
class ComponentAgent(Agent):
    """Agent built from reusable components."""

    components: dict[str, Any] = Field(default_factory=dict)
    component_config: dict[str, Any] = Field(default_factory=dict)

    @field_validator("components")
    def validate_components(self, v):
        """Validate that required components are present."""
        required = ["processor", "validator"]
        for req in required:
            if req not in v:
                raise ValueError(f"Missing required component: {req}")
        return v

    def model_post_init(self, __context):
        """Initialize components after model creation."""
        super().model_post_init(__context)

        # Set up component connections
        self._setup_component_connections()

        # Register components with graph
        self._register_components()

    def _setup_component_connections(self):
        """Set up how components connect to each other."""
        # Example: processor -> validator -> output
        self.component_config["flow"] = [
            ("processor", "validator"),
            ("validator", "output"),
        ]

    def _register_components(self):
        """Register components for use in graph."""
        for name, _component in self.components.items():
            # Could register in a component registry
            logger.info(f"Registered component: {name}")

    def build_graph(self) -> BaseGraph:
        """Build graph from components."""
        graph = BaseGraph(state_schema=self.state_schema)

        # Add component nodes
        for name, component in self.components.items():
            if callable(component):
                graph.add_node(name, {"type": "CALLABLE", "callable": component})
            else:
                graph.add_node(name, component)

        # Connect based on flow
        graph.add_edge(START, "processor")
        for source, target in self.component_config.get("flow", []):
            graph.add_edge(source, target)

        # Handle output node
        if "output" not in self.components:
            graph.add_edge("validator", END)
        else:
            graph.add_edge("output", END)

        return graph


# RAG Agent with proper schema
class EnhancedRAGAgent(Agent):
    """RAG agent with retriever engine and proper schema handling."""

    retriever_engine: EngineRetriever = Field(description="Retriever engine")
    llm_engine: AugLLMConfig | None = Field(
        default=None, description="Optional LLM for processing"
    )
    min_relevance_score: float = Field(default=0.7, ge=0, le=1)

    @model_validator(mode="after")
    def validate_engines(self):
        """Ensure engines are properly configured."""
        if not hasattr(self.retriever_engine, "search"):
            raise ValueError("Retriever engine must have search method")
        return self

    def model_post_init(self, __context):
        """Set up RAG-specific configuration."""
        super().model_post_init(__context)

        # Ensure state schema has necessary fields
        self._ensure_rag_fields()

    def _ensure_rag_fields(self):
        """Ensure state schema has RAG-specific fields."""
        # In real implementation, would modify state_schema
        required_fields = ["query", "documents", "context"]
        logger.info(f"Ensuring RAG fields: {required_fields}")

    def build_graph(self) -> BaseGraph:
        """Build RAG graph."""
        graph = BaseGraph(state_schema=self.state_schema)

        # Retrieval node
        graph.add_node(
            "retrieve",
            {
                "type": "ENGINE",
                "engine": "retriever",
                "input_fields": {"query": "query"},
                "output_fields": {"documents": "documents", "context": "context"},
            },
        )

        # Optional processing with LLM
        if self.llm_engine:
            graph.add_node(
                "process",
                {
                    "type": "ENGINE",
                    "engine": "llm",
                    "input_fields": {"query": "query", "context": "context"},
                    "output_fields": {"response": "response"},
                },
            )

            graph.add_edge(START, "retrieve")
            graph.add_edge("retrieve", "process")
            graph.add_edge("process", END)
        else:
            graph.add_edge(START, "retrieve")
            graph.add_edge("retrieve", END)

        return graph


# Test fixtures
@pytest.fixture
def mock_engines():
    """Create mock engines for testing."""
    # Query processor engine
    query_engine = Mock(spec=AugLLMConfig)
    query_engine.name = "query_processor"
    query_engine.get_input_fields.return_value = {
        "messages": (list[BaseMessage], Field(default_factory=list)),
        "query": (str, Field(default="")),
    }
    query_engine.get_output_fields.return_value = {
        "processed_query": (str, Field()),
        "intent": (str, Field()),
    }

    # Analyzer engine
    analyzer_engine = Mock(spec=AugLLMConfig)
    analyzer_engine.name = "analyzer"
    analyzer_engine.tools = []  # No tools
    analyzer_engine.get_input_fields.return_value = {
        "processed_query": (str, Field()),
        "intent": (str, Field()),
    }
    analyzer_engine.get_output_fields.return_value = {
        "analysis": (str, Field()),
        "confidence": (float, Field(default=0.0)),
    }

    # Retriever engine
    retriever_engine = Mock(spec=EngineRetriever)
    retriever_engine.name = "retriever"
    retriever_engine.search = Mock(
        return_value=[
            Document(page_content="Test doc 1", metadata={"score": 0.9}),
            Document(page_content="Test doc 2", metadata={"score": 0.8}),
        ]
    )

    return {
        "query": query_engine,
        "analyzer": analyzer_engine,
        "retriever": retriever_engine,
    }


# Test complete multi-agent system
class TestCompleteMultiAgent:
    """Test comprehensive multi-agent functionality."""

    def test_conditional_multi_agent_routing(self, mock_engines):
        """Test multi-agent with conditional routing."""
        with patch.multiple(
            "haive.agents.base.agent.Agent",
            setup_workflow=Mock(),
            _generate_state_schema=Mock(return_value=MessagesState),
        ):
            # Create agents
            query_agent = SimpleAgent(
                engine=mock_engines["query"], name="query_processor"
            )

            analyzer_agent = SimpleAgent(
                engine=mock_engines["analyzer"], name="analyzer"
            )

            # Create conditional multi-agent
            multi_agent = ConditionalMultiAgent(
                agents=[query_agent, analyzer_agent],
                name="conditional_system",
                enable_conditional_routing=True,
            )

            # Build graph
            graph = multi_agent.build_graph()

            # Verify conditional edges exist
            assert "router" in graph.nodes
            assert any(edge[0] == "router" for edge in graph.edges)

            # Test routing function
            test_state = {
                "messages": [HumanMessage(content="Please analyze this data")]
            }
            route = multi_agent._route_based_on_state(test_state)
            assert route == "analyzer"

    def test_component_agent_composition(self):
        """Test agent built from components."""

        # Create mock components
        def processor(state):
            return {"processed": True}

        def validator(state):
            if not state.get("processed"):
                raise ValueError("Not processed")
            return {"validated": True}

        with patch("haive.agents.base.agent.Agent.setup_workflow"):
            agent = ComponentAgent(
                components={"processor": processor, "validator": validator},
                name="component_system",
            )

            # Verify components registered
            assert "processor" in agent.components
            assert "validator" in agent.components

            # Build graph
            graph = agent.build_graph()

            # Verify component nodes
            assert "processor" in graph.nodes
            assert "validator" in graph.nodes

    def test_rag_agent_with_schema(self, mock_engines):
        """Test RAG agent with proper schema handling."""
        with patch("haive.agents.base.agent.Agent.setup_workflow"):
            rag_agent = EnhancedRAGAgent(
                retriever_engine=mock_engines["retriever"],
                llm_engine=mock_engines["analyzer"],
                name="rag_system",
                engines={
                    "retriever": mock_engines["retriever"],
                    "llm": mock_engines["analyzer"],
                },
            )

            # Build graph
            graph = rag_agent.build_graph()

            # Verify RAG-specific nodes
            assert "retrieve" in graph.nodes
            assert "process" in graph.nodes  # Since we have LLM

    def test_multi_agent_schema_flow(self, mock_engines):
        """Test schema compatibility in multi-agent flow."""
        with patch.multiple(
            "haive.agents.base.agent.Agent",
            setup_workflow=Mock(),
            _generate_state_schema=Mock(return_value=ToolState),
        ):
            # Create agents with different output schemas
            agents = []

            # Query agent outputs processed_query and intent
            query_agent = SimpleAgent(
                engine=mock_engines["query"], name="query_processor"
            )
            agents.append(query_agent)

            # Analyzer expects processed_query and intent (compatible!)
            analyzer_agent = SimpleAgent(
                engine=mock_engines["analyzer"], name="analyzer"
            )
            agents.append(analyzer_agent)

            # Create sequential multi-agent
            multi_agent = SequentialAgent(agents=agents, name="compatible_flow")

            # model_post_init should validate compatibility
            # In this case, schemas are compatible

            # Build graph
            graph = multi_agent.build_graph()

            # All agents should be connected
            assert len(graph.nodes) >= len(agents)


# Test model_post_init patterns
class TestModelPostInit:
    """Test proper use of model_post_init."""

    def test_model_post_init_validation(self):
        """Test that model_post_init validates configuration."""

        class ValidatingAgent(Agent):
            required_field: str
            optional_field: str = "default"

            def model_post_init(self, __context):
                super().model_post_init(__context)

                # Validate configuration
                if not self.required_field:
                    raise ValueError("required_field cannot be empty")

                # Set up derived fields
                self.derived_field = f"{self.required_field}_{self.optional_field}"

            def build_graph(self):
                return BaseGraph(state_schema=self.state_schema)

        with patch("haive.agents.base.agent.Agent.setup_workflow"):
            # Valid agent
            agent = ValidatingAgent(required_field="test", engines={"main": Mock()})
            assert agent.derived_field == "test_default"

            # Invalid agent
            with pytest.raises(ValueError):
                ValidatingAgent(required_field="", engines={"main": Mock()})

    def test_model_post_init_component_setup(self, mock_engines):
        """Test using model_post_init for component setup."""

        class ComponentSetupAgent(Agent):
            auto_setup_tools: bool = True

            def model_post_init(self, __context):
                super().model_post_init(__context)

                # Auto-setup based on configuration
                if self.auto_setup_tools and hasattr(self.engine, "tools"):
                    self._setup_tool_routing()

                # Pre-compute expensive operations
                self._precomputed_data = self._expensive_computation()

            def _setup_tool_routing(self):
                self.tool_routes = {}
                for tool in self.engine.tools:
                    self.tool_routes[tool.name] = "tool_node"

            def _expensive_computation(self):
                return {"computed": True}

            def build_graph(self):
                return BaseGraph(state_schema=self.state_schema)

        # Create engine with tools
        engine_with_tools = Mock(spec=AugLLMConfig)
        engine_with_tools.tools = [Mock(name="search_tool"), Mock(name="calc_tool")]

        with patch("haive.agents.base.agent.Agent.setup_workflow"):
            agent = ComponentSetupAgent(engine=engine_with_tools, auto_setup_tools=True)

            # Verify setup happened
            assert hasattr(agent, "tool_routes")
            assert "search_tool" in agent.tool_routes
            assert agent._precomputed_data["computed"]


# Integration test bringing it all together
def test_complete_multi_agent_system(mock_engines):
    """Test a complete multi-agent system with all features."""
    with patch.multiple(
        "haive.agents.base.agent.Agent",
        setup_workflow=Mock(),
        _generate_state_schema=Mock(return_value=ToolState),
    ):
        # 1. Create a RAG agent for retrieval
        rag_agent = EnhancedRAGAgent(
            retriever_engine=mock_engines["retriever"],
            name="retriever",
            engines={"retriever": mock_engines["retriever"]},
        )

        # 2. Create a query processing agent
        query_agent = SimpleAgent(engine=mock_engines["query"], name="query_processor")

        # 3. Create an analysis agent
        analyzer = SimpleAgent(engine=mock_engines["analyzer"], name="analyzer")

        # 4. Create a conditional multi-agent system
        system = ConditionalMultiAgent(
            agents=[rag_agent, query_agent, analyzer],
            name="complete_system",
            enable_conditional_routing=True,
        )

        # The system should:
        # - Use model_post_init to validate agent compatibility
        # - Set up conditional routing
        # - Pre-compute schema mappings
        # - Build a graph with conditional edges

        # Verify system setup
        assert len(system.agents) == 3
        assert system.enable_conditional_routing
        assert hasattr(system, "router_config")
        assert hasattr(system, "_schema_mappings")

        # Build the graph
        graph = system.build_graph()

        # Verify graph structure
        assert "router" in graph.nodes
        assert all(agent.name in graph.nodes for agent in system.agents)


# Run with: poetry run pytest packages/haive-agents/tests/test_multi_agent_complete.py -v
