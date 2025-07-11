# tests/test_planning/test_p_and_e/test_integration.py
"""Integration tests for Plan and Execute agent."""

import pytest
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

from haive.agents.planning.p_and_e.agent import PlanAndExecuteAgent
from haive.agents.planning.p_and_e.models import Plan, PlanStep
from haive.agents.planning.p_and_e.state import PlanExecuteState
from haive.agents.simple.agent import SimpleAgent


# Test tools that return predictable results
@tool
def get_weather(location: str) -> str:
    """Get weather for a location."""
    return f"The weather in {location} is sunny and 75°F"


@tool
def get_population(city: str) -> str:
    """Get population of a city."""
    populations = {
        "tokyo": "13.96 million",
        "new york": "8.34 million",
        "london": "9.00 million",
    }
    return f"The population of {city.lower()} is {populations.get(city.lower(), 'unknown')}"


@tool
def calculate_area(length: float, width: float) -> str:
    """Calculate area given length and width."""
    area = length * width
    return f"The area is {area} square units"


class TestPlanAndExecuteIntegration:
    """Integration tests for PlanAndExecuteAgent."""

    @pytest.mark.skip(reason="Requires LLM connection")
    def test_agent_simple_execution(self):
        """Test agent executing a simple task."""
        PlanAndExecuteAgent(name="test_agent", tools=[get_weather])

        PlanExecuteState(
            messages=[HumanMessage(content="What's the weather in Tokyo?")]
        )

        # This would run the full agent
        # assert result.final_answer is not None

    def test_state_initialization_flow(self):
        """Test the flow of state initialization and updates."""
        # Create initial state
        initial_state = PlanExecuteState(
            messages=[
                HumanMessage(content="Calculate the area of Tokyo if it's 2194 km²")
            ]
        )

        assert initial_state.objective == "Calculate the area of Tokyo if it's 2194 km²"
        assert initial_state.plan is None

        # Simulate plan creation
        plan = Plan(
            objective="Calculate Tokyo's area",
            steps=[
                PlanStep(
                    step_id=1,
                    description="Understand that Tokyo's area is already given",
                    expected_output="Expected output",
                ),
                PlanStep(
                    step_id=2,
                    description="Present the answer",
                    expected_output="Expected output",
                ),
            ],
        )

        state_with_plan = PlanExecuteState(
            messages=initial_state.messages, plan=plan, current_step_id=1
        )

        assert state_with_plan.plan is not None
        assert len(state_with_plan.plan.steps) == 2
        assert state_with_plan.current_step_id == 1

    def test_schema_field_integration(self):
        """Test that all schema fields work together properly."""
        from datetime import datetime

        # Create a complex state
        plan = Plan(
            objective="Complete task",
            steps=[
                PlanStep(
                    step_id=1, description="Step 1", expected_output="Expected output"
                ),
                PlanStep(
                    step_id=2, description="Step 2", expected_output="Expected output"
                ),
            ],
        )

        state = PlanExecuteState(
            messages=[
                HumanMessage(content="Do something"),
                AIMessage(content="I'll help with that"),
            ],
            plan=plan,
            context="Test context",
            started_at=datetime.now(),
        )

        # Test fields work with the data
        assert state.objective == "Do something"
        assert state.context == "Test context"
        assert len(state.plan.steps) == 2

        # Test serialization works
        data = state.model_dump()
        restored = PlanExecuteState(**data)

        assert len(restored.messages) == 2
        assert restored.plan is not None
        assert restored.context == "Test context"


class TestSchemaComposition:
    """Test schema composition behavior."""

    def test_plan_execute_agent_schema_composition(self):
        """Test that PlanAndExecuteAgent properly composes schemas."""
        agent = PlanAndExecuteAgent(name="test_agent")

        # Get schema instance
        schema_instance = agent.state_schema()

        # Check all expected fields are present and accessible
        expected_fields = [
            "messages",  # From MessagesState
            "plan",  # From PlanExecuteState
            "final_answer",  # From PlanExecuteState
            "context",  # From PlanExecuteState
            "engine",  # From schema composition
            "engines",  # From schema composition
        ]

        for field in expected_fields:
            assert hasattr(schema_instance, field), f"Missing field: {field}"

        # Check computed properties work
        assert schema_instance.objective == ""  # No messages
        assert schema_instance.plan_progress == "No plan created yet"
        assert schema_instance.execution_results == "No steps executed yet"

    def test_simple_agent_planner_composition(self):
        """Test SimpleAgent with planner engine composition."""
        from haive.agents.planning.p_and_e.prompts import planner_prompt

        planner_config = AugLLMConfig(
            name="test_planner",
            structured_output_model=Plan,
            structured_output_version="v2",
            prompt_template=planner_prompt,
            temperature=0.1,
        )

        agent = SimpleAgent(name="planner_agent", engine=planner_config)

        # Check the composed schema
        schema = agent.state_schema
        fields = schema.model_fields

        # Should have plan field from structured output
        assert "plan" in fields

        # Should have engine management fields
        assert "engine" in fields
        assert "engines" in fields

        # Should have messages field
        assert "messages" in fields

        # Create instance and verify it works
        instance = schema()
        instance.messages.append(HumanMessage(content="Test"))
        assert len(instance.messages) == 1
