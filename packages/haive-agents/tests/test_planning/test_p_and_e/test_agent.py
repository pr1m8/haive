# tests/test_planning/test_p_and_e/test_agent.py
"""Tests for PlanAndExecuteAgent without mocks."""

import pytest
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool

from haive.agents.planning.p_and_e.agent import PlanAndExecuteAgent
from haive.agents.planning.p_and_e.models import Act, Plan, PlanStep, Response
from haive.agents.planning.p_and_e.state import PlanExecuteState
from haive.agents.simple.agent import SimpleAgent


# Test tools
@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Search results for '{query}': Found relevant information"


@tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        result = eval(expression)
        return f"Calculation result: {result}"
    except:
        return "Error: Invalid expression"


class TestPlanAndExecuteAgent:
    """Test the PlanAndExecuteAgent."""

    def test_agent_initialization(self):
        """Test agent initializes with default engines."""
        agent = PlanAndExecuteAgent(name="test_agent")

        # Check agent properties
        assert agent.name == "test_agent"
        # When use_prebuilt_base=True, the schema is composed from PlanExecuteState
        assert agent.state_schema.__name__ == "PlanAndExecuteAgentState"
        assert agent.use_prebuilt_base is True

        # Check engines are created
        assert "planner" in agent.engines
        assert "executor" in agent.engines
        assert "replanner" in agent.engines

        # Check engine types
        assert isinstance(agent.engines["planner"], AugLLMConfig)
        assert isinstance(agent.engines["executor"], AugLLMConfig)
        assert isinstance(agent.engines["replanner"], AugLLMConfig)

    def test_agent_schema_has_engine_fields(self):
        """Test that the composed schema includes engine fields."""
        agent = PlanAndExecuteAgent(name="test_agent")

        # Get the state schema fields
        fields = agent.state_schema.model_fields

        # Check that engine management fields are present
        assert "engine" in fields
        assert "engines" in fields

        # Check other expected fields from PlanExecuteState
        assert "messages" in fields
        assert "plan" in fields
        assert "final_answer" in fields
        assert "context" in fields

    def test_planner_engine_configuration(self):
        """Test planner engine has correct configuration."""
        agent = PlanAndExecuteAgent(name="test_agent")
        planner = agent.engines["planner"]

        assert planner.structured_output_model == Plan
        assert planner.structured_output_version == "v2"
        assert planner.prompt_template is not None
        assert "context" in planner.partial_variables

    def test_executor_engine_configuration(self):
        """Test executor engine has correct configuration."""
        agent = PlanAndExecuteAgent(name="test_agent")
        executor = agent.engines["executor"]

        assert executor.prompt_template is not None
        assert "plan_status" in executor.partial_variables
        assert "current_step" in executor.partial_variables
        assert "previous_results" in executor.partial_variables

    def test_replanner_engine_configuration(self):
        """Test replanner engine has correct configuration."""
        agent = PlanAndExecuteAgent(name="test_agent")
        replanner = agent.engines["replanner"]

        assert replanner.structured_output_model == Act
        assert replanner.structured_output_version == "v2"
        assert replanner.prompt_template is not None
        assert "objective" in replanner.partial_variables

    def test_agent_with_tools(self):
        """Test agent can be created with tools."""
        agent = PlanAndExecuteAgent(
            name="test_agent_with_tools", tools=[search, calculate]
        )

        # Check tools are accessible (would be used by executors)
        assert hasattr(agent, "tools")
        assert len(agent.tools) == 2

    def test_graph_structure(self):
        """Test the agent builds the correct graph structure."""
        agent = PlanAndExecuteAgent(name="test_agent")

        # The graph should be built during initialization
        assert agent.graph is not None

        # Check graph has expected nodes
        # Note: We'd need to access internal graph structure to verify nodes
        # For now, just verify graph exists and is compiled
        assert hasattr(agent, "_app")
        assert agent._app is not None


class TestSimpleAgentWithPlannerEngine:
    """Test SimpleAgent with planner engine configuration."""

    def test_simple_agent_with_planner(self):
        """Test creating SimpleAgent with planner engine."""
        from haive.agents.planning.p_and_e.prompts import planner_prompt

        planner_aug = AugLLMConfig(
            name="planner",
            structured_output_model=Plan,
            structured_output_version="v2",
            prompt_template=planner_prompt,
            temperature=0.1,
        )

        agent = SimpleAgent(engine=planner_aug)

        # Check agent configuration
        assert agent.engine == planner_aug
        assert agent.engine.structured_output_model == Plan

        # Check state schema fields
        fields = agent.state_schema.model_fields

        # Should have engine management fields
        assert "engine" in fields
        assert "engines" in fields

        # Should have standard fields
        assert "messages" in fields
        assert "plan" in fields  # From structured output model

    def test_simple_agent_state_creation(self):
        """Test creating state instance from SimpleAgent schema."""
        from haive.agents.planning.p_and_e.prompts import planner_prompt

        planner_aug = AugLLMConfig(
            name="planner",
            structured_output_model=Plan,
            structured_output_version="v2",
            prompt_template=planner_prompt,
            temperature=0.1,
        )

        agent = SimpleAgent(engine=planner_aug)

        # Create state instance
        state = agent.state_schema()

        # Check state has expected fields
        assert hasattr(state, "messages")
        assert hasattr(state, "engine")
        assert hasattr(state, "engines")
        assert hasattr(state, "plan")

        # Check default values
        assert len(state.messages) == 0
        assert state.engine is None
        assert isinstance(state.engines, dict)
        assert state.plan is None

    def test_simple_agent_output_field(self):
        """Test that structured output creates appropriate field."""
        from haive.agents.planning.p_and_e.prompts import planner_prompt

        planner_aug = AugLLMConfig(
            name="planner",
            structured_output_model=Plan,
            structured_output_version="v2",
            prompt_template=planner_prompt,
            temperature=0.1,
        )

        agent = SimpleAgent(engine=planner_aug)

        # The 'plan' field should be added based on structured output
        fields = agent.state_schema.model_fields
        plan_field = fields.get("plan")

        assert plan_field is not None
        assert "Plan" in str(plan_field.annotation)
        assert plan_field.default is None
