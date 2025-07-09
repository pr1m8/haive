"""Test dynamic supervisor with real agents (no mocks)."""

import pytest
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.messages import HumanMessage

from haive.agents.dynamic_supervisor import (
    AgentInfo,
    DynamicSupervisorAgent,
    SupervisorState,
    SupervisorStateWithTools,
)
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent


def create_test_agents():
    """Create real agent instances of different types for testing."""

    # SimpleAgent for basic tasks
    simple_engine = AugLLMConfig(
        name="simple_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        system_message="You are a helpful assistant. Answer questions clearly and concisely.",
    )
    simple_agent = SimpleAgent(
        name="simple_agent",
        engine=simple_engine,
        description="General purpose assistant for simple tasks",
    )

    # ReactAgent for reasoning tasks
    react_engine = AugLLMConfig(
        name="react_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        system_message="You are a reasoning agent. Think step by step to solve problems.",
    )
    react_agent = ReactAgent(
        name="react_agent",
        engine=react_engine,
        description="Reasoning and problem-solving specialist",
    )

    # Another SimpleAgent for specialized tasks
    specialist_engine = AugLLMConfig(
        name="specialist_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        system_message="You are a code analysis expert. Analyze and explain code clearly.",
    )
    specialist_agent = SimpleAgent(
        name="specialist_agent",
        engine=specialist_engine,
        description="Code analysis and explanation specialist",
    )

    return simple_agent, react_agent, specialist_agent


class TestDynamicSupervisorWithRealAgents:
    """Test supervisor with real agent instances."""

    def test_supervisor_creation_with_engine(self):
        """Test creating supervisor with real engine."""
        supervisor_engine = AugLLMConfig(
            name="supervisor_engine",
            llm_config=AzureLLMConfig(model="gpt-4o"),
            system_message="You are a task supervisor. Route tasks to appropriate agents.",
        )

        supervisor = DynamicSupervisorAgent(
            name="test_supervisor", engine=supervisor_engine
        )

        assert supervisor.name == "test_supervisor"
        assert supervisor.engine is not None
        assert hasattr(supervisor, "state_schema")

    def test_add_real_agents_to_state(self):
        """Test adding real agents to supervisor state."""
        state = SupervisorStateWithTools()
        simple_agent, react_agent, _ = create_test_agents()

        # Add agents of different types
        state.add_agent("simple", simple_agent, "Simple task handler")
        state.add_agent("react", react_agent, "Reasoning specialist")

        # Verify agents were added
        assert len(state.agents) == 2
        assert "simple" in state.agents
        assert "react" in state.agents

        # Verify tools were generated
        assert "handoff_to_simple" in state.generated_tools
        assert "handoff_to_react" in state.generated_tools
        assert "choose_agent" in state.generated_tools

    def test_handoff_tool_execution(self):
        """Test that handoff tools can execute real agents."""
        state = SupervisorStateWithTools()
        simple_agent, _, _ = create_test_agents()

        # Add agent and get tools
        state.add_agent("simple", simple_agent, simple_agent.description)
        tools = state.get_all_tools()

        # Find handoff tool
        handoff_tool = next(t for t in tools if t.name == "handoff_to_simple")
        assert handoff_tool is not None

        # We can't actually execute without API keys, but verify structure
        assert callable(handoff_tool.func)
        assert "simple" in handoff_tool.description.lower()

    def test_dynamic_agent_management(self):
        """Test adding and removing agents dynamically."""
        state = SupervisorStateWithTools()
        simple_agent, react_agent, specialist_agent = create_test_agents()

        # Start with 2 agents
        state.add_agent("simple", simple_agent, simple_agent.description)
        state.add_agent("react", react_agent, react_agent.description)

        initial_tools = state.generated_tools.copy()
        assert len(state.agents) == 2
        assert len([t for t in initial_tools if t.startswith("handoff_")]) == 2

        # Add third agent
        state.add_agent("specialist", specialist_agent, specialist_agent.description)

        assert len(state.agents) == 3
        assert "handoff_to_specialist" in state.generated_tools

        # Remove an agent
        state.remove_agent("react")

        assert len(state.agents) == 2
        assert "react" not in state.agents
        assert "handoff_to_react" not in state.generated_tools

    def test_agent_activation_deactivation(self):
        """Test activating and deactivating agents."""
        state = SupervisorStateWithTools()
        search_agent, math_agent, _ = create_test_agents()

        # Add active agent
        state.add_agent("search", search_agent, "Search specialist", active=True)
        assert "search" in state.active_agents

        # Add inactive agent
        state.add_agent("math", math_agent, "Math expert", active=False)
        assert "math" not in state.active_agents

        # Activate math agent
        state.activate_agent("math")
        assert "math" in state.active_agents

        # Deactivate search agent
        state.deactivate_agent("search")
        assert "search" not in state.active_agents

    def test_supervisor_with_initial_agents(self):
        """Test supervisor with pre-configured agents."""
        supervisor_engine = AugLLMConfig(
            name="supervisor_engine",
            llm_config=AzureLLMConfig(model="gpt-4o"),
            force_tool_use=True,
        )

        supervisor = DynamicSupervisorAgent(
            name="coordinator", engine=supervisor_engine
        )

        # Create initial state with agents
        state = supervisor.create_initial_state()
        search_agent, math_agent, _ = create_test_agents()

        state.add_agent("search", search_agent, "Search expert")
        state.add_agent("math", math_agent, "Math expert")

        # Get tools - should include handoff tools
        tools = state.get_all_tools()
        tool_names = [t.name for t in tools]

        assert "handoff_to_search" in tool_names
        assert "handoff_to_math" in tool_names
        assert "choose_agent" in tool_names

    @pytest.mark.asyncio
    async def test_supervisor_graph_build(self):
        """Test that supervisor builds valid graph."""
        supervisor_engine = AugLLMConfig(
            name="supervisor_engine", llm_config=AzureLLMConfig(model="gpt-4o")
        )

        supervisor = DynamicSupervisorAgent(
            name="test_supervisor", engine=supervisor_engine
        )

        # Graph should be built during initialization
        assert supervisor.graph is not None
        assert hasattr(supervisor.graph, "nodes")

        # Should use SimpleAgent graph (no modifications)
        # Main node is the agent_node from SimpleAgent
        assert "agent_node" in supervisor.graph.nodes


class TestSupervisorStateSerialization:
    """Test state serialization with real agents."""

    def test_agent_exclusion_from_serialization(self):
        """Test that agents are properly excluded from serialization."""
        import ormsgpack

        state = SupervisorState()
        search_agent, _, _ = create_test_agents()

        # Add real agent
        state.add_agent("search", search_agent, "Search expert")

        # Serialize state
        state_dict = state.model_dump()

        # Agent should be excluded
        assert "search" in state_dict["agents"]
        agent_data = state_dict["agents"]["search"]
        assert "agent" not in agent_data  # Excluded!
        assert agent_data["name"] == "search"
        assert agent_data["description"] == "Search expert"

        # Should serialize without error
        serialized = ormsgpack.packb(state_dict)
        assert isinstance(serialized, bytes)

        # Can deserialize
        deserialized = ormsgpack.unpackb(serialized)
        assert deserialized["agents"]["search"]["name"] == "search"
