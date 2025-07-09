"""Debug the Engine serialization problem in MultiAgent systems."""

from haive.agents.planning.p_and_e.state import PlanExecuteState
from haive.agents.simple.agent import SimpleAgent
from langchain_core.messages import HumanMessage

def test_simple_agent_alone():
    """Test if a simple agent works by itself."""
    print("=== Testing SimpleAgent Alone ===")
    
    try:
        agent = SimpleAgent(name="test_simple")
        result = agent.run("What is 2 + 2?")
        print(f"✅ SimpleAgent works: {result}")
        return True
    except Exception as e:
        print(f"❌ SimpleAgent failed: {e}")
        return False

def test_plan_execute_state_serialization():
    """Test the PlanExecuteState serialization."""
    print("\n=== Testing PlanExecuteState Serialization ===")
    
    try:
        # Create state
        state = PlanExecuteState(
            messages=[HumanMessage("Test")]
        )
        
        print(f"✅ State created: {type(state)}")
        
        # Test serialization
        serialized = state.model_dump()
        print(f"✅ Serialization successful")
        
        # Test deserialization  
        new_state = PlanExecuteState(**serialized)
        print(f"✅ Deserialization successful: {type(new_state)}")
        
        return True
    except Exception as e:
        print(f"❌ State serialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_multiagent_creation():
    """Test MultiAgentBase creation without running."""
    print("\n=== Testing MultiAgentBase Creation ===")
    
    try:
        from haive.agents.planning.proper_plan_execute import create_proper_plan_execute
        
        agent = create_proper_plan_execute()
        print(f"✅ MultiAgent created: {agent.name}")
        print(f"State schema: {agent.state_schema}")
        
        # Check if state schema has engine field
        if hasattr(agent.state_schema, 'model_fields'):
            engine_field = agent.state_schema.model_fields.get('engine')
            print(f"Engine field: {engine_field}")
            if engine_field:
                print(f"Engine field annotation: {engine_field.annotation}")
        
        return agent
    except Exception as e:
        print(f"❌ MultiAgent creation failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def show_engine_field_problem():
    """Show the exact problem with Engine field."""
    print("\n=== Analyzing Engine Field Problem ===")
    
    from haive.core.engine.base import Engine
    from haive.agents.planning.p_and_e.state import PlanExecuteState
    import inspect
    
    # Show Engine class
    print(f"Engine class: {Engine}")
    print(f"Engine is abstract: {inspect.isabstract(Engine)}")
    print(f"Engine abstract methods: {Engine.__abstractmethods__}")
    
    # Show PlanExecuteState engine field
    engine_field = PlanExecuteState.model_fields.get('engine')
    print(f"\nPlanExecuteState engine field: {engine_field}")
    if engine_field:
        print(f"Engine field type: {engine_field.annotation}")
        print(f"Engine field default: {engine_field.default}")
    
    # Show the field validator
    validators = PlanExecuteState.__pydantic_validators__
    print(f"\nValidators: {list(validators.keys())}")

def debug_langgraph_input_model():
    """Debug what LangGraph is doing with the input model."""
    print("\n=== Debugging LangGraph Input Model ===")
    
    try:
        from haive.agents.planning.proper_plan_execute import create_proper_plan_execute
        
        agent = create_proper_plan_execute()
        
        # Try to access the LangGraph app
        if hasattr(agent, '_app'):
            app = agent._app
            print(f"LangGraph app: {app}")
            
            if hasattr(app, 'input_model'):
                input_model = app.input_model
                print(f"Input model: {input_model}")
                
                if hasattr(input_model, 'model_fields'):
                    print(f"Input model fields: {list(input_model.model_fields.keys())}")
                    engine_field = input_model.model_fields.get('engine')
                    if engine_field:
                        print(f"Input model engine field: {engine_field}")
                        print(f"Input model engine annotation: {engine_field.annotation}")
        
    except Exception as e:
        print(f"Error in debug: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🔍 Debugging Engine Serialization Problem")
    print("=" * 60)
    
    # Test components individually
    simple_works = test_simple_agent_alone()
    state_works = test_plan_execute_state_serialization()
    
    # Test multiagent creation
    multiagent = test_multiagent_creation()
    
    # Show detailed analysis
    show_engine_field_problem()
    
    if multiagent:
        debug_langgraph_input_model()
    
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"✅ SimpleAgent works: {simple_works}")
    print(f"✅ State serialization works: {state_works}")
    print(f"✅ MultiAgent creation works: {multiagent is not None}")
    print("❌ But MultiAgent.run() fails due to Engine field type issue in LangGraph")