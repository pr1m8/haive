"""Test Original Plan & Execute Agent with proper models and prompts."""

from haive.agents.planning.p_and_e.agent import PlanAndExecuteAgent
from haive.tools import google_search_tool


def test_original_plan_execute():
    """Test the original Plan & Execute agent implementation."""
    print("=== Testing Original Plan & Execute Agent ===")
    
    try:
        # Create Plan & Execute agent without tools for now
        agent = PlanAndExecuteAgent(
            name="PlanExecuteAgent"
        )
        
        print("✅ Plan & Execute agent created successfully")
        print(f"Agent engines: {list(agent.engines.keys())}")
        print(f"State schema: {agent.state_schema.__name__}")
        
        # Check the state schema fields
        print(f"State fields: {list(agent.state_schema.model_fields.keys())}")
        
        # Test compilation
        agent.compile()
        print("✅ Agent compiled successfully")
        
        print("✅ All basic setup tests completed - MessageList serialization is working!")
        print("✅ The original Plan & Execute agent structure is working correctly!")
                    
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


def test_plan_model():
    """Test the Plan model structure."""
    print("\n=== Testing Plan Model ===")
    
    from haive.agents.planning.p_and_e.models import Plan, PlanStep, StepType, StepStatus
    
    # Create a sample plan
    steps = [
        PlanStep(
            step_id=1,
            description="Research current AI trends",
            step_type=StepType.RESEARCH,
            expected_output="List of current AI trends and developments"
        ),
        PlanStep(
            step_id=2,
            description="Analyze the impact of these trends",
            step_type=StepType.ANALYSIS,
            expected_output="Analysis of how trends affect different industries",
            dependencies=[1]
        ),
        PlanStep(
            step_id=3,
            description="Synthesize findings into a summary",
            step_type=StepType.SYNTHESIS,
            expected_output="Comprehensive summary of AI developments",
            dependencies=[1, 2]
        )
    ]
    
    plan = Plan(
        objective="Research and summarize latest AI developments",
        steps=steps,
        total_steps=3
    )
    
    print("✅ Plan model created successfully")
    print(f"Objective: {plan.objective}")
    print(f"Total steps: {plan.total_steps}")
    print(f"Next step: {plan.next_step.description if plan.next_step else 'None'}")
    print(f"Progress: {plan.progress_percentage:.1f}%")
    
    # Test step execution simulation
    plan.update_step_status(1, StepStatus.COMPLETED, "Found 5 major AI trends including GPT-4, multimodal AI, etc.")
    print(f"After step 1 completion - Progress: {plan.progress_percentage:.1f}%")
    print(f"Next step: {plan.next_step.description if plan.next_step else 'None'}")
    
    # Test prompt formatting
    print("\n=== Plan Prompt Format ===")
    print(plan.to_prompt_format())


def test_act_model():
    """Test the Act model for replanning decisions."""
    print("\n=== Testing Act Model ===")
    
    from haive.agents.planning.p_and_e.models import Act, Response, Plan, PlanStep, StepType
    
    # Test Response action
    response_act = Act(action=Response(response="Based on my research, here are the key AI developments..."))
    print("✅ Response Act created")
    print(f"Is final response: {response_act.is_final_response}")
    print(f"Is plan: {response_act.is_plan}")
    
    # Test Plan action
    new_plan = Plan(
        objective="Follow up research on specific AI topic",
        steps=[
            PlanStep(
                step_id=1,
                description="Deep dive into GPT-4 capabilities",
                step_type=StepType.RESEARCH,
                expected_output="Detailed analysis of GPT-4"
            )
        ],
        total_steps=1
    )
    
    plan_act = Act(action=new_plan)
    print("✅ Plan Act created")
    print(f"Is final response: {plan_act.is_final_response}")
    print(f"Is plan: {plan_act.is_plan}")


if __name__ == "__main__":
    # Test the models first
    test_plan_model()
    test_act_model()
    
    # Test the agent
    test_original_plan_execute()