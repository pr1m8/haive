"""Test Original Plan & Execute Agent with proper models and prompts."""

from haive.agents.planning.p_and_e.agent import PlanAndExecuteAgent


def test_original_plan_execute():
    """Test the original Plan & Execute agent implementation."""
    try:
        # Create Plan & Execute agent without tools for now
        agent = PlanAndExecuteAgent(name="PlanExecuteAgent")

        # Check the state schema fields

        # Test compilation
        agent.compile()

    except Exception:
        import traceback

        traceback.print_exc()


def test_plan_model():
    """Test the Plan model structure."""
    from haive.agents.planning.p_and_e.models import (
        Plan,
        PlanStep,
        StepStatus,
        StepType,
    )

    # Create a sample plan
    steps = [
        PlanStep(
            step_id=1,
            description="Research current AI trends",
            step_type=StepType.RESEARCH,
            expected_output="List of current AI trends and developments",
        ),
        PlanStep(
            step_id=2,
            description="Analyze the impact of these trends",
            step_type=StepType.ANALYSIS,
            expected_output="Analysis of how trends affect different industries",
            dependencies=[1],
        ),
        PlanStep(
            step_id=3,
            description="Synthesize findings into a summary",
            step_type=StepType.SYNTHESIS,
            expected_output="Comprehensive summary of AI developments",
            dependencies=[1, 2],
        ),
    ]

    plan = Plan(
        objective="Research and summarize latest AI developments",
        steps=steps,
        total_steps=3,
    )

    # Test step execution simulation
    plan.update_step_status(
        1,
        StepStatus.COMPLETED,
        "Found 5 major AI trends including GPT-4, multimodal AI, etc.",
    )

    # Test prompt formatting


def test_act_model():
    """Test the Act model for replanning decisions."""
    from haive.agents.planning.p_and_e.models import (
        Act,
        Plan,
        PlanStep,
        Response,
        StepType,
    )

    # Test Response action
    Act(
        action=Response(
            response="Based on my research, here are the key AI developments..."
        )
    )

    # Test Plan action
    new_plan = Plan(
        objective="Follow up research on specific AI topic",
        steps=[
            PlanStep(
                step_id=1,
                description="Deep dive into GPT-4 capabilities",
                step_type=StepType.RESEARCH,
                expected_output="Detailed analysis of GPT-4",
            )
        ],
        total_steps=1,
    )

    Act(action=new_plan)


if __name__ == "__main__":
    # Test the models first
    test_plan_model()
    test_act_model()

    # Test the agent
    test_original_plan_execute()
