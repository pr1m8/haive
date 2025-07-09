# tests/test_planning/test_p_and_e/test_models.py
"""Tests for Plan and Execute models."""

from datetime import datetime
from typing import List

import pytest

from haive.agents.planning.p_and_e.models import (
    Act,
    ExecutionResult,
    Plan,
    PlanStep,
    ReplanDecision,
    Response,
    StepStatus,
    StepType,
)


class TestPlanStep:
    """Test the PlanStep model."""

    def test_step_creation(self):
        """Test basic step creation."""
        step = PlanStep(
            step_id=1,
            description="Search for information",
            expected_output="Relevant information about the topic",
        )
        assert step.step_id == 1
        assert step.description == "Search for information"
        assert step.expected_output == "Relevant information about the topic"
        assert step.status == StepStatus.PENDING
        assert step.dependencies == []
        assert step.step_type == StepType.ACTION

    def test_step_with_dependencies(self):
        """Test step with dependencies."""
        step = PlanStep(
            step_id=3,
            description="Synthesize results",
            expected_output="Combined analysis of all findings",
            dependencies=[1, 2],
            step_type=StepType.SYNTHESIS,
        )
        assert step.dependencies == [1, 2]
        assert step.step_type == StepType.SYNTHESIS

    def test_step_validation(self):
        """Test step validation."""
        # Valid step
        step = PlanStep(
            step_id=1, description="Valid step", expected_output="Expected result"
        )
        assert step.step_id == 1
        assert step.expected_output == "Expected result"

    def test_step_computed_fields(self):
        """Test step computed fields."""
        # Test is_ready
        step = PlanStep(step_id=1, description="Test step", expected_output="Result")
        assert step.is_ready is True  # PENDING status means ready

        # Test execution_time
        assert step.execution_time is None

        # Simulate execution
        step.started_at = datetime.now()
        assert step.execution_time is None  # Not completed yet

        step.completed_at = datetime.now()
        assert step.execution_time is not None
        assert step.execution_time >= 0


class TestPlan:
    """Test the Plan model."""

    def test_plan_creation(self):
        """Test basic plan creation."""
        steps = [
            PlanStep(step_id=1, description="Step 1", expected_output="Step 1 output"),
            PlanStep(step_id=2, description="Step 2", expected_output="Step 2 output"),
        ]
        plan = Plan(objective="Complete a task", steps=steps, total_steps=2)

        assert plan.objective == "Complete a task"
        assert len(plan.steps) == 2
        # total_steps is automatically updated by model validator
        assert plan.total_steps == 2

    def test_plan_get_step(self):
        """Test getting step by ID."""
        steps = [
            PlanStep(
                step_id=1, description="Step 1", expected_output="Expected output"
            ),
            PlanStep(
                step_id=2, description="Step 2", expected_output="Expected output"
            ),
        ]
        plan = Plan(objective="Test", steps=steps, total_steps=2)

        step1 = plan.get_step(1)
        assert step1 is not None
        assert step1.description == "Step 1"

        step_none = plan.get_step(99)
        assert step_none is None

    def test_plan_summary(self):
        """Test plan summary generation."""
        plan = Plan(
            objective="Calculate population density",
            steps=[
                PlanStep(
                    step_id=1,
                    description="Get population",
                    expected_output="Population data",
                ),
                PlanStep(
                    step_id=2, description="Get area", expected_output="Area data"
                ),
                PlanStep(
                    step_id=3,
                    description="Calculate density",
                    expected_output="Density value",
                ),
            ],
            total_steps=3,
        )

        summary = plan.to_prompt_format()
        assert "Calculate population density" in summary
        assert "Total Steps: 3" in summary
        assert "Get population" in summary


class TestExecutionResult:
    """Test the ExecutionResult model."""

    def test_execution_result_success(self):
        """Test successful execution result."""
        result = ExecutionResult(
            step_id=1, success=True, output="Found information", execution_time=1.5
        )

        assert result.step_id == 1
        assert result.success is True
        assert result.output == "Found information"
        assert result.execution_time == 1.5
        assert result.error is None

    def test_execution_result_failure(self):
        """Test failed execution result."""
        result = ExecutionResult(
            step_id=2,
            success=False,
            output="",
            error="Tool not found",
            execution_time=0.1,
        )

        assert result.step_id == 2
        assert result.success is False
        assert result.error == "Tool not found"
        assert result.output == ""


class TestReplanDecision:
    """Test the ReplanDecision model."""

    def test_replan_continue(self):
        """Test replan decision to continue."""
        decision = ReplanDecision(decision="continue", reasoning="Plan is working well")

        assert decision.decision == "continue"
        assert decision.reasoning == "Plan is working well"
        assert decision.final_answer is None
        assert decision.replan_instructions is None

    def test_replan_with_new_plan(self):
        """Test replan decision with new plan."""
        decision = ReplanDecision(
            decision="replan",
            reasoning="Previous approach failed",
            replan_instructions="Try a different approach",
        )

        assert decision.decision == "replan"
        assert decision.reasoning == "Previous approach failed"
        assert decision.replan_instructions == "Try a different approach"


class TestResponse:
    """Test the Response model."""

    def test_response_creation(self):
        """Test basic response creation."""
        response = Response(response="The answer is 42")
        assert response.response == "The answer is 42"


class TestAct:
    """Test the Act model."""

    def test_act_with_response(self):
        """Test Act with Response action."""
        response = Response(response="Final answer")
        act = Act(action=response)

        assert isinstance(act.action, Response)
        assert act.action.response == "Final answer"

    def test_act_with_plan(self):
        """Test Act with Plan action."""
        plan = Plan(
            objective="New objective",
            steps=[
                PlanStep(
                    step_id=1, description="New step", expected_output="New result"
                )
            ],
            total_steps=1,
        )
        act = Act(action=plan)

        assert isinstance(act.action, Plan)
        assert act.action.objective == "New objective"

    def test_act_computed_properties(self):
        """Test Act computed properties."""
        # Test with Response
        response = Response(response="Final answer")
        act = Act(action=response)
        assert act.is_final_response is True
        assert act.is_plan is False

        # Test with Plan
        plan = Plan(
            objective="New objective",
            steps=[
                PlanStep(
                    step_id=1, description="New step", expected_output="New result"
                )
            ],
            total_steps=1,
        )
        act = Act(action=plan)
        assert act.is_final_response is False
        assert act.is_plan is True


class TestModelSerialization:
    """Test model serialization/deserialization."""

    def test_plan_step_serialization(self):
        """Test PlanStep model serialization."""
        step = PlanStep(
            step_id=1,
            description="Test step",
            expected_output="Test output",
            status=StepStatus.COMPLETED,
            dependencies=[],
            step_type=StepType.RESEARCH,
        )

        # Serialize
        data = step.model_dump()
        assert data["step_id"] == 1
        assert data["description"] == "Test step"
        assert data["expected_output"] == "Test output"
        assert data["status"] == "completed"
        assert data["step_type"] == "research"

        # Deserialize
        step2 = PlanStep(**data)
        assert step2.step_id == step.step_id
        assert step2.status == StepStatus.COMPLETED

    def test_plan_serialization(self):
        """Test Plan model serialization."""
        plan = Plan(
            objective="Test objective",
            steps=[
                PlanStep(step_id=1, description="Step 1", expected_output="Output 1"),
                PlanStep(step_id=2, description="Step 2", expected_output="Output 2"),
            ],
            total_steps=2,
        )

        # Serialize
        data = plan.model_dump()
        assert data["objective"] == "Test objective"
        assert len(data["steps"]) == 2

        # Deserialize
        plan2 = Plan(**data)
        assert plan2.objective == plan.objective
        assert len(plan2.steps) == 2
        assert plan2.steps[0].description == "Step 1"
