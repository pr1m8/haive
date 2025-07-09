"""Test Clean Plan & Execute implementation following LangGraph patterns."""

from haive.agents.planning.clean_plan_execute import create_simple_plan_execute
from haive.tools import duckduckgo_search_tool


def test_clean_plan_execute():
    """Test the clean Plan & Execute implementation."""
    print("=== Testing Clean Plan & Execute Agent ===")
    
    try:
        # Create clean plan and execute agent
        agent = create_simple_plan_execute(tools=[duckduckgo_search_tool])
        
        print("✅ Clean Plan & Execute agent created successfully")
        print(f"Agent name: {agent.name}")
        print(f"State schema: {agent.state_schema.__name__}")
        print(f"Number of agents: {len(agent.agents)}")
        
        # List the agents
        for i, sub_agent in enumerate(agent.agents):
            print(f"  Agent {i}: {sub_agent.name} ({type(sub_agent).__name__})")
        
        # Test compilation
        agent.compile()
        print("✅ Agent compiled successfully")
        
        # Test simple execution
        print("\n=== Testing Simple Execution ===")
        result = agent.run("What is 2 + 2?")
        
        print("✅ Execution completed!")
        print(f"Result type: {type(result)}")
        
        # Check result structure
        if hasattr(result, 'response') and result.response:
            print(f"Final response: {result.response}")
        
        if hasattr(result, 'plan') and result.plan:
            print(f"Plan steps: {result.plan}")
            
        if hasattr(result, 'past_steps') and result.past_steps:
            print(f"Completed steps: {result.past_steps}")
            
        if hasattr(result, 'messages'):
            print(f"Messages count: {len(result.messages)}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


def test_models():
    """Test the simple models."""
    print("\n=== Testing Simple Models ===")
    
    from haive.agents.planning.clean_plan_execute import Plan, Act
    
    # Test Plan model
    plan = Plan(steps=[
        "Think about the problem",
        "Calculate 2 + 2", 
        "Provide the answer"
    ])
    print("✅ Plan model created")
    print(f"Plan steps: {plan.steps}")
    
    # Test Act model  
    continue_act = Act(action="continue", response="Execute step 1")
    print("✅ Continue Act created")
    print(f"Action: {continue_act.action}, Response: {continue_act.response}")
    
    final_act = Act(action="response", response="The answer is 4")
    print("✅ Final Act created") 
    print(f"Action: {final_act.action}, Response: {final_act.response}")


def test_state_schema():
    """Test the clean state schema."""
    print("\n=== Testing Clean State Schema ===")
    
    from haive.agents.planning.clean_plan_execute import PlanExecuteState
    from langchain_core.messages import HumanMessage, AIMessage
    
    # Create state
    state = PlanExecuteState(
        messages=[HumanMessage("What is 2 + 2?")],
        plan=["Calculate 2 + 2", "Provide answer"],
        past_steps=["Understood the question"],
        response=""
    )
    
    print("✅ State created successfully")
    print(f"Messages: {len(state.messages)}")
    print(f"Plan: {state.plan}")
    print(f"Past steps: {state.past_steps}")
    print(f"Response: {state.response}")
    
    # Test serialization (this validates our MessageList fix)
    serialized = state.model_dump()
    print("✅ State serialization successful")
    print(f"Serialized keys: {list(serialized.keys())}")
    print(f"Messages serialized as: {type(serialized['messages'])}")


if __name__ == "__main__":
    # Test models first
    test_models()
    test_state_schema()
    
    # Test the agent
    test_clean_plan_execute()