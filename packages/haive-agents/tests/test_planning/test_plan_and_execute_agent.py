"""Tests for Plan and Execute Agent implementation."""

import asyncio

import pytest
from haive.core.llm import AugLLMConfig
from haive.tools.tools.search_tools import tavily_search

from haive.agents.planning.p_and_e.state import Plan, PlanExecuteState, PlanStep
from haive.agents.planning.plan_and_execute import (
    PlanAndExecuteAgent,
    create_plan_and_execute_agent,
)


class TestPlanAndExecuteAgent:
    """Test suite for Plan and Execute Agent."""

    @pytest.fixture
    def base_config(self):
        """Base configuration for agents."""
        return AugLLMConfig(model="gpt-4", temperature=0.7)

    @pytest.fixture
    def plan_execute_agent(self, base_config):
        """Create a plan and execute agent."""
        return create_plan_and_execute_agent(
            planner_config=base_config,
            executor_config=base_config,
            replanner_config=base_config,
            max_replanning_attempts=2,
        )

    def test_agent_creation(self, base_config):
        """Test creating a plan and execute agent."""
        agent = PlanAndExecuteAgent(
            planner_config=base_config,
            executor_config=base_config,
            replanner_config=base_config,
        )

        assert agent.planner is not None
        assert agent.executor is not None
        assert agent.replanner is not None
        assert len(agent.agents) == 3
        assert tavily_search in agent.executor_tools

    def test_agent_without_replanner(self, base_config):
        """Test creating agent without replanner."""
        agent = PlanAndExecuteAgent(
            planner_config=base_config, executor_config=base_config
        )

        assert agent.planner is not None
        assert agent.executor is not None
        assert agent.replanner is None
        assert len(agent.agents) == 2

    def test_custom_executor_tools(self, base_config):
        """Test custom executor tools."""
        custom_tools = ["tool1", "tool2"]
        agent = PlanAndExecuteAgent(
            planner_config=base_config,
            executor_config=base_config,
            executor_tools=custom_tools,
        )

        assert agent.executor_tools == custom_tools

    def test_routing_from_planner(self, plan_execute_agent):
        """Test routing logic from planner."""
        # Test with valid plan
        state = PlanExecuteState(
            plan=Plan(
                task="Test task",
                steps=[
                    PlanStep(
                        step_number=1, description="Step 1", expected_output="Output 1"
                    )
                ],
                total_steps=1,
            )
        )

        route = plan_execute_agent._route_from_planner(state)
        assert route == "executor"

        # Test without plan
        state_no_plan = PlanExecuteState()
        route = plan_execute_agent._route_from_planner(state_no_plan)
        assert route == "__end__"

    def test_routing_from_executor(self, plan_execute_agent):
        """Test routing logic from executor."""
        # Test with incomplete plan
        state = PlanExecuteState(
            plan=Plan(
                task="Test task",
                steps=[
                    PlanStep(
                        step_number=1,
                        description="Step 1",
                        expected_output="Output 1",
                        status="completed",
                    ),
                    PlanStep(
                        step_number=2, description="Step 2", expected_output="Output 2"
                    ),
                ],
                total_steps=2,
            )
        )

        route = plan_execute_agent._route_from_executor(state)
        assert route in ["executor", "replanner"]

        # Test with completed plan
        for step in state.plan.steps:
            step.status = "completed"

        route = plan_execute_agent._route_from_executor(state)
        assert route == "__end__"

    def test_routing_from_replanner(self, plan_execute_agent):
        """Test routing logic from replanner."""
        from haive.core.base import BaseMessage

        # Test CONTINUE response
        state = PlanExecuteState(
            messages=[BaseMessage(role="assistant", content="CONTINUE with execution")]
        )

        route = plan_execute_agent._route_from_replanner(state)
        assert route == "executor"

        # Test new plan response
        new_plan_content = """{
            "task": "Updated task",
            "steps": [
                {
                    "step_number": 1,
                    "description": "New step 1",
                    "expected_output": "New output 1"
                }
            ],
            "total_steps": 1
        }"""

        state = PlanExecuteState(
            messages=[BaseMessage(role="assistant", content=new_plan_content)]
        )

        route = plan_execute_agent._route_from_replanner(state)
        assert route == "executor"
        assert state.plan is not None
        assert state.plan.total_steps == 1
        assert state.replanning_count == 1

    def test_create_function(self, base_config):
        """Test the create_plan_and_execute_agent function."""
        # Test with configs
        agent = create_plan_and_execute_agent(
            planner_config=base_config,
            executor_config=base_config,
            replanner_config=base_config,
        )

        assert isinstance(agent, PlanAndExecuteAgent)
        assert agent.planner is not None
        assert agent.executor is not None
        assert agent.replanner is not None

        # Test with dicts
        config_dict = {"model": "gpt-4", "temperature": 0.5}

        agent = create_plan_and_execute_agent(
            planner_config=config_dict, executor_config=config_dict
        )

        assert isinstance(agent, PlanAndExecuteAgent)
        assert agent.planner is not None
        assert agent.executor is not None

    def test_graph_structure(self, plan_execute_agent):
        """Test the graph structure is properly built."""
        # Build the graph
        graph = plan_execute_agent.build_graph()

        # The graph should be compiled and ready
        assert graph is not None

        # Check that branches were properly added
        assert len(plan_execute_agent.branches) == 3  # planner, executor, replanner

    @pytest.mark.asyncio
    async def test_state_schema_composition(self, plan_execute_agent):
        """Test that state schema is properly composed."""
        # The state schema should be PlanExecuteState
        assert plan_execute_agent.state_schema_override == PlanExecuteState

        # After setup, the composed schema should include fields from all agents
        plan_execute_agent.setup_agent()

        # Verify the schema includes expected fields
        schema_fields = plan_execute_agent.state_schema.__fields__.keys()
        assert "messages" in schema_fields
        assert "plan" in schema_fields
        assert "status" in schema_fields
