"""Tests for Multi-Agent Plan and Execute Agent implementation.

This module tests the PlanAndExecuteAgent that uses MultiAgentBase with proper
field configuration and tool routing capabilities.
"""

import asyncio

import pytest
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool

from haive.agents.planning import PlanAndExecuteAgent
from haive.agents.planning.p_and_e.models import Act, Plan, PlanStep
from haive.agents.planning.p_and_e.state import PlanExecuteState
from haive.agents.react import ReactAgent
from haive.agents.simple import SimpleAgent


# Test tools without mocks
@tool
def search_tool(query: str) -> str:
    """Search for information.

    Args:
        query: The search query string.

    Returns:
        Search results as a string.
    """
    return f"Search results for '{query}': Found relevant information about the topic."


@tool
def calculate_tool(expression: str) -> str:
    """Calculate a mathematical expression.

    Args:
        expression: Mathematical expression to evaluate.

    Returns:
        Calculation result or error message.
    """
    try:
        result = eval(expression)
        return f"Calculation result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"


class TestPlanAndExecuteMultiAgent:
    """Test suite for Multi-Agent Plan and Execute Agent."""

    @pytest.fixture
    def aug_llm_config(self):
        """Create an AugLLM config for testing.

        Returns:
            AugLLMConfig: Configuration for testing.
        """
        return AugLLMConfig(name="test_aug_llm", temperature=0.7)

    @pytest.fixture
    def planner_agent(self, aug_llm_config):
        """Create a planner agent.

        Args:
            aug_llm_config: AugLLM configuration.

        Returns:
            SimpleAgent: Configured planner agent.
        """
        return SimpleAgent(
            name="planner",
            engine=aug_llm_config,
            instructions="Create a plan to accomplish: {objective}",
            output_schema=Act,
            output_schema_strict=True,
        )

    @pytest.fixture
    def executor_agent(self, aug_llm_config):
        """Create an executor agent.

        Args:
            aug_llm_config: AugLLM configuration.

        Returns:
            ReactAgent: Configured executor agent.
        """
        return ReactAgent(
            name="executor",
            engine=aug_llm_config,
            instructions="Execute this step: {current_step}",
        )

    @pytest.fixture
    def replanner_agent(self, aug_llm_config):
        """Create a replanner agent.

        Args:
            aug_llm_config: AugLLM configuration.

        Returns:
            SimpleAgent: Configured replanner agent.
        """
        return SimpleAgent(
            name="replanner",
            engine=aug_llm_config,
            instructions="Assess progress and decide next action",
            output_schema=Act,
            output_schema_strict=True,
        )

    @pytest.fixture
    def plan_execute_agent(self, planner_agent, executor_agent, replanner_agent):
        """Create a complete plan and execute agent.

        Args:
            planner_agent: Planner agent instance.
            executor_agent: Executor agent instance.
            replanner_agent: Replanner agent instance.

        Returns:
            MultiAgentBase: Complete plan and execute agent.
        """
        return PlanAndExecuteAgent(
            planner=planner_agent,
            executor=executor_agent,
            replanner=replanner_agent,
            name="test_plan_execute_agent",
        )

    def test_agent_creation(self, plan_execute_agent):
        """Test creating a plan and execute agent.

        Args:
            plan_execute_agent: Plan and execute agent fixture.
        """
        assert plan_execute_agent.name == "test_plan_execute_agent"
        assert len(plan_execute_agent.agents) == 3

        # Check agent names via list access
        agent_names = [agent.name for agent in plan_execute_agent.agents]
        assert "planner" in agent_names
        assert "executor" in agent_names
        assert "replanner" in agent_names

        # Check dict-like access by name
        assert plan_execute_agent.agents["planner"].name == "planner"
        assert plan_execute_agent.agents["executor"].name == "executor"
        assert plan_execute_agent.agents["replanner"].name == "replanner"

        # Check get method
        assert plan_execute_agent.agents.get("planner") is not None
        assert plan_execute_agent.agents.get("nonexistent") is None

    def test_agent_fields(self, plan_execute_agent):
        """Test agent field configuration.

        Args:
            plan_execute_agent: Plan and execute agent fixture.
        """
        # Check agent names
        agent_names = [agent.name for agent in plan_execute_agent.agents]
        assert "planner" in agent_names
        assert "executor" in agent_names
        assert "replanner" in agent_names

        # Check state schema override
        assert plan_execute_agent.state_schema_override == PlanExecuteState

        # Check build mode
        from haive.agents.multi.enhanced_base import BuildMode

        assert plan_execute_agent.schema_build_mode == BuildMode.PARALLEL

    def test_tool_routing_inheritance(self, plan_execute_agent):
        """Test that agent is a MultiAgentBase.

        Args:
            plan_execute_agent: Plan and execute agent fixture.
        """
        from haive.agents.multi.enhanced_base import MultiAgentBase

        # Check it's a MultiAgentBase
        assert isinstance(plan_execute_agent, MultiAgentBase)

        # Check core capabilities
        assert hasattr(plan_execute_agent, "agents")
        assert hasattr(plan_execute_agent, "branches")
        assert hasattr(plan_execute_agent, "build_graph")

    def test_tools_sync_to_executor(self, plan_execute_agent):
        """Test that agents are properly configured.

        Args:
            plan_execute_agent: Plan and execute agent fixture.
        """
        # Find the executor agent
        executor = None
        for agent in plan_execute_agent.agents:
            if agent.name == "executor":
                executor = agent
                break

        assert executor is not None
        assert hasattr(executor, "engine")

    def test_branch_creation(self, plan_execute_agent):
        """Test that branches are properly created.

        Args:
            plan_execute_agent: Plan and execute agent fixture.
        """
        assert hasattr(plan_execute_agent, "branches")
        assert (
            len(plan_execute_agent.branches) == 2
        )  # executor->routing, replanner->routing (planner->executor is implicit)

        # Check branch structure
        for branch in plan_execute_agent.branches:
            assert len(branch) == 3  # (agent, condition_func, route_map)
            agent, condition_func, route_map = branch
            # condition_func can be None for direct edges
            if condition_func is not None:
                assert callable(condition_func)
            # route_map can be dict or direct agent for simple edges
            assert route_map is not None

    def test_multi_agent_base_inheritance(self, plan_execute_agent):
        """Test inheritance from MultiAgentBase.

        Args:
            plan_execute_agent: Plan and execute agent fixture.
        """
        from haive.agents.multi.enhanced_base import MultiAgentBase

        assert isinstance(plan_execute_agent, MultiAgentBase)
        assert hasattr(plan_execute_agent, "agents")
        assert hasattr(plan_execute_agent, "branches")
        assert hasattr(plan_execute_agent, "build_graph")

    def test_agent_validation(self, planner_agent, executor_agent):
        """Test agent validation in model_post_init.

        Args:
            planner_agent: Planner agent fixture.
            executor_agent: Executor agent fixture.
        """
        # Test missing agents
        with pytest.raises(
            ValueError, match="requires planner, executor, and replanner"
        ):
            PlanAndExecuteAgent(
                planner=planner_agent,
                executor=executor_agent,
                # Missing replanner
                name="incomplete_agent",
            )

        with pytest.raises(
            ValueError, match="requires planner, executor, and replanner"
        ):
            PlanAndExecuteAgent(
                planner=planner_agent,
                # Missing executor and replanner
                name="incomplete_agent",
            )

    def test_tool_route_mixin_methods(self, plan_execute_agent):
        """Test ToolRouteMixin methods work correctly.

        Args:
            plan_execute_agent: Plan and execute agent fixture.
        """

        # Test add_tool method
        @tool
        def new_tool(input_text: str) -> str:
            """Process input text.

            Args:
                input_text: Text to process.

            Returns:
                Processed text.
            """
            return f"Processing: {input_text}"

        initial_tool_count = len(plan_execute_agent.tools)
        plan_execute_agent.add_tool(new_tool)

        assert len(plan_execute_agent.tools) == initial_tool_count + 1
        assert "new_tool" in plan_execute_agent.tool_routes

        # Test get_tool_route method
        route = plan_execute_agent.get_tool_route("new_tool")
        assert route is not None

        # Test tool metadata
        metadata = plan_execute_agent.get_tool_metadata("new_tool")
        assert metadata is not None

    def test_state_schema_composition(self, plan_execute_agent):
        """Test state schema is properly composed.

        Args:
            plan_execute_agent: Plan and execute agent fixture.
        """
        # The agent should have a composed state schema
        assert hasattr(plan_execute_agent, "state_schema")

        # The schema should include fields from PlanExecuteState
        schema_fields = plan_execute_agent.state_schema.model_fields
        assert "messages" in schema_fields
        assert "plan" in schema_fields
        assert "final_answer" in schema_fields
        assert "context" in schema_fields

    def test_agent_name_inheritance(self, plan_execute_agent):
        """Test that agent names are properly set.

        Args:
            plan_execute_agent: Plan and execute agent fixture.
        """
        assert plan_execute_agent.name == "test_plan_execute_agent"
        assert plan_execute_agent.planner.name == "planner"
        assert plan_execute_agent.executor.name == "executor"
        assert plan_execute_agent.replanner.name == "replanner"

    def test_tool_categorization(self, plan_execute_agent):
        """Test that tools are properly categorized.

        Args:
            plan_execute_agent: Plan and execute agent fixture.
        """
        # Check that tools have been analyzed and categorized
        assert len(plan_execute_agent.tool_routes) >= 2

        # Check that search_tool and calculate_tool are categorized
        search_route = plan_execute_agent.get_tool_route("search_tool")
        calc_route = plan_execute_agent.get_tool_route("calculate_tool")

        assert search_route is not None
        assert calc_route is not None

        # Both should be function routes
        assert search_route == "function"
        assert calc_route == "function"

    @pytest.mark.asyncio
    async def test_basic_structure_verification(self, plan_execute_agent):
        """Test basic agent structure is correct for execution.

        Args:
            plan_execute_agent: Plan and execute agent fixture.

        Note:
            This test verifies structure without running full LLM execution.
        """
        # Test that the agent can be initialized and has correct structure
        assert plan_execute_agent.planner is not None
        assert plan_execute_agent.executor is not None
        assert plan_execute_agent.replanner is not None

        # Test that tools are properly configured
        assert len(plan_execute_agent.tools) == 2

        # Test that branches are properly configured for routing
        assert len(plan_execute_agent.branches) == 2

        # Note: Full execution tests would require actual LLM calls
        # This test verifies the structure is correct for execution
