"""Comprehensive Test Suite for Plan and Execute Multi-Agent System.

This test suite covers:
1. Basic Plan and Execute workflow
2. Computed fields accessibility in PlanExecuteState
3. Routing between planner, executor, and replanner agents
4. Convenience function create_plan_execute_multi_agent()
5. Error handling and edge cases
6. Custom branches and workflow customization
"""

from datetime import datetime
from typing import Any, Dict, List
from unittest.mock import AsyncMock, MagicMock

import pytest
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.agent_schema_composer import BuildMode
from langgraph.graph import END, START

from haive.agents.base.agent import Agent
from haive.agents.multi.enhanced_base import (
    MultiAgentBase,
    create_plan_execute_multi_agent,
)
from haive.agents.planning.p_and_e.models import (
    Act,
    ExecutionResult,
    Plan,
    PlanStep,
    Response,
)
from haive.agents.planning.p_and_e.state import PlanExecuteState
from haive.agents.simple.agent import SimpleAgent


class TestPlanExecuteState:
    """Test the PlanExecuteState computed fields and functionality."""

    def test_computed_fields_basic(self):
        """Test that computed fields are accessible and return expected values."""
        # Create a basic plan
        plan = Plan(
            objective="Test objective",
            total_steps=3,
            steps=[
                PlanStep(
                    step_id=1,
                    description="Step 1",
                    expected_output="Output 1",
                    status="pending",
                ),
                PlanStep(
                    step_id=2,
                    description="Step 2",
                    expected_output="Output 2",
                    status="pending",
                ),
                PlanStep(
                    step_id=3,
                    description="Step 3",
                    expected_output="Output 3",
                    status="pending",
                ),
            ],
        )

        # Create state with the plan
        state = PlanExecuteState(
            plan=plan,
            current_step_id=1,
            execution_results=[],
            messages=[{"type": "human", "content": "Test objective"}],
        )

        # Test computed fields
        assert state.plan_status is not None
        assert "Test objective" in state.plan_status
        assert "Total Steps: 3" in state.plan_status
        assert "Progress: 0.0%" in state.plan_status

        assert state.current_step is not None
        assert "Step 1" in state.current_step

        assert state.previous_results == "No previous results"
        assert state.objective == "Test objective"
        assert state.should_replan is False
        assert state.execution_time is None

    def test_computed_fields_with_progress(self):
        """Test computed fields with execution progress."""
        # Create a plan with mixed progress
        plan = Plan(
            objective="Test objective",
            total_steps=3,
            steps=[
                PlanStep(
                    step_id=1,
                    description="Step 1",
                    expected_output="Output 1",
                    status="completed",
                    result="Done",
                ),
                PlanStep(
                    step_id=2,
                    description="Step 2",
                    expected_output="Output 2",
                    status="in_progress",
                ),
                PlanStep(
                    step_id=3,
                    description="Step 3",
                    expected_output="Output 3",
                    status="pending",
                ),
            ],
        )

        # Create execution results
        execution_results = [
            ExecutionResult(
                step_id=1,
                success=True,
                output="Step 1 completed successfully",
                execution_time=2.5,
            )
        ]

        state = PlanExecuteState(
            plan=plan,
            current_step_id=2,
            execution_results=execution_results,
            messages=[{"type": "human", "content": "Test objective"}],
        )

        # Test computed fields with progress
        assert "Progress: 33.3%" in state.plan_status
        assert "Completed: 1" in state.plan_status
        assert "Step 2" in state.current_step
        assert "Step 1 completed successfully" in state.previous_results
        assert state.should_replan is False

    def test_computed_fields_should_replan(self):
        """Test should_replan computed field logic."""
        # Test replan after 3 completed steps
        plan = Plan(
            objective="Test objective",
            total_steps=4,
            steps=[
                PlanStep(
                    step_id=1,
                    description="Step 1",
                    expected_output="Output 1",
                    status="completed",
                ),
                PlanStep(
                    step_id=2,
                    description="Step 2",
                    expected_output="Output 2",
                    status="completed",
                ),
                PlanStep(
                    step_id=3,
                    description="Step 3",
                    expected_output="Output 3",
                    status="completed",
                ),
                PlanStep(
                    step_id=4,
                    description="Step 4",
                    expected_output="Output 4",
                    status="pending",
                ),
            ],
        )

        state = PlanExecuteState(
            plan=plan, messages=[{"type": "human", "content": "Test objective"}]
        )

        assert state.should_replan is True

        # Test replan when no plan
        state_no_plan = PlanExecuteState(
            messages=[{"type": "human", "content": "Test objective"}]
        )
        assert state_no_plan.should_replan is True

    def test_execution_time_calculation(self):
        """Test execution time calculation."""
        start_time = datetime.now()
        end_time = datetime.now()

        state = PlanExecuteState(
            started_at=start_time,
            completed_at=end_time,
            messages=[{"type": "human", "content": "Test objective"}],
        )

        # Should be a small positive number
        assert state.execution_time is not None
        assert state.execution_time >= 0


class TestPlanExecuteMultiAgent:
    """Test the complete Plan and Execute multi-agent system."""

    @pytest.fixture
    def llm_config(self):
        """Create a basic LLM configuration."""
        return AugLLMConfig()

    @pytest.fixture
    def planner_agent(self, llm_config):
        """Create a planner agent."""
        return SimpleAgent(name="planner", engine=llm_config)

    @pytest.fixture
    def executor_agent(self, llm_config):
        """Create an executor agent."""
        return SimpleAgent(name="executor", engine=llm_config)

    @pytest.fixture
    def replanner_agent(self, llm_config):
        """Create a replanner agent."""
        return SimpleAgent(name="replanner", engine=llm_config)

    def test_create_plan_execute_multi_agent_basic(
        self, planner_agent, executor_agent, replanner_agent
    ):
        """Test basic creation of Plan and Execute multi-agent system."""
        # Create using convenience function
        plan_execute_system = create_plan_execute_multi_agent(
            planner_agent=planner_agent,
            executor_agent=executor_agent,
            replanner_agent=replanner_agent,
        )

        assert isinstance(plan_execute_system, MultiAgentBase)
        assert len(plan_execute_system.agents) == 3
        assert plan_execute_system.state_schema_override == PlanExecuteState
        assert plan_execute_system.schema_build_mode == BuildMode.PARALLEL
        assert plan_execute_system.branches is not None
        assert len(plan_execute_system.branches) >= 2  # At least routing branches

    def test_create_plan_execute_multi_agent_with_options(
        self, planner_agent, executor_agent, replanner_agent
    ):
        """Test creation with custom options."""
        plan_execute_system = create_plan_execute_multi_agent(
            planner_agent=planner_agent,
            executor_agent=executor_agent,
            replanner_agent=replanner_agent,
            name="Custom Plan Execute System",
            schema_build_mode=BuildMode.PARALLEL,
        )

        assert plan_execute_system.name == "Custom Plan Execute System"
        assert plan_execute_system.schema_build_mode == BuildMode.PARALLEL

    def test_plan_execute_routing_logic(
        self, planner_agent, executor_agent, replanner_agent
    ):
        """Test the routing logic between agents."""
        # Create the system
        plan_execute_system = create_plan_execute_multi_agent(
            planner_agent=planner_agent,
            executor_agent=executor_agent,
            replanner_agent=replanner_agent,
        )

        # Test that the system has branches configured
        assert plan_execute_system.branches is not None
        assert len(plan_execute_system.branches) == 2  # Should have routing branches

        # Test branches structure
        for branch in plan_execute_system.branches:
            assert isinstance(branch, tuple)
            assert len(branch) == 3  # (source, condition, destinations)
            source, condition, destinations = branch
            assert callable(condition)
            assert isinstance(destinations, dict)

        # Test routing functions with different states

        # Get the routing functions from the branches
        executor_branch = None
        replanner_branch = None

        for branch in plan_execute_system.branches:
            source, condition, destinations = branch
            if source == executor_agent:
                executor_branch = condition
            elif source == replanner_agent:
                replanner_branch = condition

        assert executor_branch is not None
        assert replanner_branch is not None

        # Test route after execution - complete plan
        complete_plan = Plan(
            objective="Test",
            total_steps=1,
            steps=[
                PlanStep(
                    step_id=1,
                    description="Step 1",
                    expected_output="Output 1",
                    status="completed",
                )
            ],
        )
        complete_state = PlanExecuteState(
            plan=complete_plan, messages=[{"type": "human", "content": "Test"}]
        )
        # Plan is already complete since step status is "completed"

        route = executor_branch(complete_state)
        assert route == "replanner"

        # Test route after execution - continue
        continue_plan = Plan(
            objective="Test",
            total_steps=2,
            steps=[
                PlanStep(
                    step_id=1,
                    description="Step 1",
                    expected_output="Output 1",
                    status="completed",
                ),
                PlanStep(
                    step_id=2,
                    description="Step 2",
                    expected_output="Output 2",
                    status="pending",
                ),
            ],
        )
        continue_state = PlanExecuteState(
            plan=continue_plan, messages=[{"type": "human", "content": "Test"}]
        )

        route = executor_branch(continue_state)
        assert route == "executor"

        # Test route after replan - complete
        final_state = PlanExecuteState(
            final_answer="Task completed successfully",
            messages=[{"type": "human", "content": "Test"}],
        )

        route = replanner_branch(final_state)
        assert route == END

    def test_plan_execute_workflow_nodes(
        self, planner_agent, executor_agent, replanner_agent
    ):
        """Test workflow node functions."""
        plan_execute_system = create_plan_execute_multi_agent(
            planner_agent=planner_agent,
            executor_agent=executor_agent,
            replanner_agent=replanner_agent,
        )

        # Test that the system has the proper configuration
        assert plan_execute_system.state_schema_override == PlanExecuteState
        assert len(plan_execute_system.agents) == 3

        # Test that branches are properly configured
        assert plan_execute_system.branches is not None
        assert len(plan_execute_system.branches) == 2

        # Test schema composition works
        test_state = PlanExecuteState(messages=[{"type": "human", "content": "Test"}])

        # Test computed fields are accessible
        assert test_state.objective == "Test"
        assert test_state.plan_status == "No plan available"
        assert test_state.current_step is None
        assert test_state.previous_results == "No previous results"
        assert test_state.should_replan is True

    def test_plan_execute_error_handling(
        self, planner_agent, executor_agent, replanner_agent
    ):
        """Test error handling in Plan and Execute workflow."""
        plan_execute_system = create_plan_execute_multi_agent(
            planner_agent=planner_agent,
            executor_agent=executor_agent,
            replanner_agent=replanner_agent,
        )

        # Test that error handling works at the system level
        # The routing functions should handle edge cases gracefully

        # Test routing with no plan
        empty_state = PlanExecuteState(messages=[{"type": "human", "content": "Test"}])

        # Get routing functions from branches
        executor_branch = None

        for branch in plan_execute_system.branches:
            source, condition, destinations = branch
            if source == executor_agent:
                executor_branch = condition
            elif source == replanner_agent:
                pass

        # Should handle no plan gracefully
        route = executor_branch(empty_state)
        assert route == "replanner"  # Should route to replanner when no plan

        # Test routing with invalid state
        invalid_state = PlanExecuteState(
            plan=Plan(objective="Test", total_steps=0, steps=[]),
            messages=[{"type": "human", "content": "Test"}],
        )

        route = executor_branch(invalid_state)
        assert route in ["executor", "replanner"]  # Should handle gracefully

    def test_plan_execute_with_custom_branches(
        self, planner_agent, executor_agent, replanner_agent
    ):
        """Test Plan and Execute with custom branches."""

        def custom_condition(state):
            return "custom_route"

        custom_branches = [
            (
                executor_agent,
                custom_condition,
                {"custom_route": replanner_agent, "default": END},
            )
        ]

        plan_execute_system = create_custom_plan_execute_multi_agent(
            planner=planner_agent,
            executor=executor_agent,
            replanner=replanner_agent,
            custom_branches=custom_branches,
        )

        # Should use custom branches instead of default
        assert plan_execute_system.branches == custom_branches
        assert len(plan_execute_system.branches) == 1

    def test_plan_execute_schema_composition(
        self, planner_agent, executor_agent, replanner_agent
    ):
        """Test schema composition in Plan and Execute system."""
        plan_execute_system = create_plan_execute_multi_agent(
            planner_agent=planner_agent,
            executor_agent=executor_agent,
            replanner_agent=replanner_agent,
        )

        # Should compose schemas from all agents
        assert plan_execute_system.state_schema_override == PlanExecuteState

        # Test that computed fields are accessible
        test_state = PlanExecuteState(
            messages=[{"type": "human", "content": "Test objective"}]
        )

        # These should not raise errors
        assert test_state.objective == "Test objective"
        assert test_state.plan_status == "No plan available"
        assert test_state.current_step is None
        assert test_state.previous_results == "No previous results"
        assert test_state.should_replan is True


class TestPlanExecuteIntegration:
    """Integration tests for the complete Plan and Execute system."""

    @pytest.fixture
    def llm_config(self):
        """Create a basic LLM configuration."""
        return AugLLMConfig()

    def test_plan_execute_integration_setup(self, llm_config):
        """Test integration of Plan and Execute system with real agents."""
        # Create real agents
        planner = SimpleAgent(name="planner", engine=llm_config)
        executor = SimpleAgent(name="executor", engine=llm_config)
        replanner = SimpleAgent(name="replanner", engine=llm_config)

        # Create the system
        plan_execute_system = create_plan_execute_multi_agent(
            planner_agent=planner, executor_agent=executor, replanner_agent=replanner
        )

        # Test that system is properly configured
        assert len(plan_execute_system.agents) == 3
        assert plan_execute_system.state_schema_override == PlanExecuteState
        assert plan_execute_system.branches is not None

        # Test routing functions work with real state
        test_state = PlanExecuteState(
            plan=Plan(
                objective="Test task",
                total_steps=1,
                steps=[
                    PlanStep(
                        step_id=1,
                        description="Test step",
                        expected_output="Test output",
                        status="pending",
                    )
                ],
            ),
            messages=[{"type": "human", "content": "Test task"}],
        )

        # Get routing functions from branches
        executor_branch = None
        for branch in plan_execute_system.branches:
            source, condition, destinations = branch
            if source == executor:
                executor_branch = condition
                break

        # Test routing function works
        assert executor_branch is not None
        route_result = executor_branch(test_state)
        assert route_result in ["executor", "replanner"]


# Additional convenience functions for testing
def create_sequential_plan_execute_multi_agent(
    planner: Agent, executor: Agent, replanner: Agent, **kwargs
) -> MultiAgentBase:
    """Create a simple sequential Plan and Execute system.

    Args:
        planner: Planning agent
        executor: Execution agent
        replanner: Replanning agent
        **kwargs: Additional arguments

    Returns:
        MultiAgentBase: Sequential Plan and Execute system
    """
    return MultiAgentBase(
        agents=[planner, executor, replanner],
        state_schema_override=PlanExecuteState,
        schema_build_mode=BuildMode.SEQUENCE,
        **kwargs
    )


def create_custom_plan_execute_multi_agent(
    planner: Agent,
    executor: Agent,
    replanner: Agent,
    custom_branches: list[tuple],
    **kwargs
) -> MultiAgentBase:
    """Create a Plan and Execute system with custom branches.

    Args:
        planner: Planning agent
        executor: Execution agent
        replanner: Replanning agent
        custom_branches: Custom routing branches
        **kwargs: Additional arguments

    Returns:
        MultiAgentBase: Custom Plan and Execute system
    """
    return MultiAgentBase(
        agents=[planner, executor, replanner],
        branches=custom_branches,
        state_schema_override=PlanExecuteState,
        schema_build_mode=BuildMode.SEQUENCE,
        **kwargs
    )
