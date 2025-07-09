# tests/test_planning/test_p_and_e/test_state.py
"""Tests for PlanExecuteState."""

from datetime import datetime

import pytest
from haive.core.schema.prebuilt.messages.messages_state import MessagesState
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from haive.agents.planning.p_and_e.models import Plan, PlanStep
from haive.agents.planning.p_and_e.state import PlanExecuteState


class TestPlanExecuteState:
    """Test the PlanExecuteState schema."""

    def test_state_inherits_from_messages_state(self):
        """Test that PlanExecuteState inherits from MessagesState."""
        assert issubclass(PlanExecuteState, MessagesState)

    def test_state_creation_empty(self):
        """Test creating empty state."""
        state = PlanExecuteState()

        assert len(state.messages) == 0
        assert state.plan is None
        assert state.final_answer is None
        assert state.started_at is not None  # Auto-initialized
        assert state.completed_at is None
        assert state.context is None

    def test_state_creation_with_messages(self):
        """Test creating state with messages."""
        messages = [HumanMessage(content="Hello"), AIMessage(content="Hi there")]
        state = PlanExecuteState(messages=messages)

        assert len(state.messages) == 2
        assert state.messages[0].content == "Hello"
        assert state.messages[1].content == "Hi there"

    def test_state_with_plan(self):
        """Test state with a plan."""
        plan = Plan(
            objective="Test objective",
            steps=[
                PlanStep(
                    step_id=1, description="Step 1", expected_output="Expected output"
                ),
                PlanStep(
                    step_id=2, description="Step 2", expected_output="Expected output"
                ),
            ],
            total_steps=2,
        )
        state = PlanExecuteState(plan=plan)

        assert state.plan is not None
        assert len(state.plan.steps) == 2
        assert state.plan.steps[0].description == "Step 1"

    def test_state_with_timestamps(self):
        """Test state with timestamps."""
        now = datetime.now()
        state = PlanExecuteState(started_at=now, completed_at=now)

        assert state.started_at == now
        assert state.completed_at == now

    def test_state_objective_from_messages(self):
        """Test objective extraction from messages."""
        messages = [
            SystemMessage(content="System prompt"),
            HumanMessage(content="What is 2+2?"),
            AIMessage(content="Let me calculate..."),
        ]
        state = PlanExecuteState(messages=messages)

        assert state.objective == "What is 2+2?"

    def test_state_objective_empty_messages(self):
        """Test objective with no messages."""
        state = PlanExecuteState()
        assert state.objective is None

    def test_state_objective_no_human_messages(self):
        """Test objective with no human messages."""
        messages = [SystemMessage(content="System prompt"), AIMessage(content="Hello")]
        state = PlanExecuteState(messages=messages)
        assert state.objective is None

    def test_state_plan_tracking(self):
        """Test plan tracking fields."""
        # No plan
        state = PlanExecuteState()
        assert state.plan is None
        assert state.current_step_id is None

        # With plan
        plan = Plan(
            objective="Test plan",
            steps=[
                PlanStep(
                    step_id=1, description="Step 1", expected_output="Expected output"
                ),
                PlanStep(
                    step_id=2, description="Step 2", expected_output="Expected output"
                ),
                PlanStep(
                    step_id=3, description="Step 3", expected_output="Expected output"
                ),
            ],
            total_steps=3,
        )
        state = PlanExecuteState(plan=plan, current_step_id=2)

        assert state.plan is not None
        assert state.current_step_id == 2
        assert len(state.plan.steps) == 3

    def test_state_execution_results(self):
        """Test execution_results field."""
        from haive.agents.planning.p_and_e.models import ExecutionResult

        # No results
        state = PlanExecuteState()
        assert state.execution_results == []

        # With execution results
        results = [
            ExecutionResult(
                step_id=1, success=True, output="Found info", execution_time=0.5
            ),
            ExecutionResult(
                step_id=2, success=True, output="Result: 42", execution_time=1.0
            ),
        ]
        state = PlanExecuteState(execution_results=results)

        assert len(state.execution_results) == 2
        assert state.execution_results[0].output == "Found info"
        assert state.execution_results[1].output == "Result: 42"

    def test_state_serialization(self):
        """Test state serialization/deserialization."""
        plan = Plan(
            objective="Test",
            steps=[
                PlanStep(
                    step_id=1,
                    description="Test step",
                    expected_output="Expected output",
                )
            ],
            total_steps=1,
        )
        state = PlanExecuteState(
            messages=[HumanMessage(content="Test")],
            plan=plan,
            final_answer="Answer",
            context="Test context",
        )

        # Serialize
        data = state.model_dump()
        assert "messages" in data
        assert "plan" in data
        assert "final_answer" in data
        assert "context" in data

        # Deserialize
        state2 = PlanExecuteState(**data)
        assert len(state2.messages) == 1
        assert state2.plan is not None
        assert state2.final_answer == "Answer"
        assert state2.context == "Test context"

    def test_state_message_handling(self):
        """Test that message handling from MessagesState works."""
        state = PlanExecuteState()

        # Add messages using the inherited MessageList functionality
        state.messages.append(HumanMessage(content="Question"))
        state.messages.append(AIMessage(content="Answer"))

        assert len(state.messages) == 2
        assert state.messages[0].content == "Question"
        assert state.messages[1].content == "Answer"

    def test_state_with_dict_messages(self):
        """Test state creation with dict messages (for persistence)."""
        messages = [
            {"type": "human", "content": "Hello"},
            {"type": "ai", "content": "Hi there"},
        ]
        state = PlanExecuteState(messages=messages)

        assert len(state.messages) == 2
        assert isinstance(state.messages[0], HumanMessage)
        assert isinstance(state.messages[1], AIMessage)
        assert state.messages[0].content == "Hello"
        assert state.messages[1].content == "Hi there"
