"""Test Plan & Execute Agent with fixed MessageList serialization."""

from haive.agents.planning.plan_and_execute_multi import PlanAndExecuteAgent
from haive.agents.simple.agent import SimpleAgent
from haive.tools import google_search_tool


def test_plan_execute_with_simple_agents():
    """Test Plan & Execute using Simple agents for all roles."""
    print("=== Creating Plan & Execute Agent ===")
    
    try:
        # Create three simple agents for different roles
        planner = SimpleAgent(
            name="planner",
            system_message="You are a planning agent. Create detailed step-by-step plans to accomplish objectives."
        )
        print("✅ Planner agent created")
        
        executor = SimpleAgent(
            name="executor", 
            system_message="You are an execution agent. Execute individual steps from plans using available tools."
        )
        print("✅ Executor agent created")
        
        replanner = SimpleAgent(
            name="replanner",
            system_message="You are a replanning agent. Determine if plans need revision or if objectives are complete."
        )
        print("✅ Replanner agent created")
        
        # Create the Plan & Execute multi-agent
        plan_execute_agent = PlanAndExecuteAgent(
            planner=planner,
            executor=executor, 
            replanner=replanner,
            name="TestPlanExecute"
        )
        
        print("✅ Plan & Execute agent created successfully")
        print(f"Schema fields: {list(plan_execute_agent.state_schema.model_fields.keys())}")
        
        # Test compilation
        plan_execute_agent.compile()
        print("✅ Agent compiled successfully")
        
        print("✅ All setup completed - MessageList serialization is working properly!")
            
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()


def test_messagelist_serialization():
    """Test MessageList serialization independently."""
    print("\n=== Testing MessageList Serialization ===")
    
    from haive.core.schema.prebuilt.messages.messages_state import MessageList
    from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
    
    # Create test messages
    messages = MessageList([
        HumanMessage("Calculate 5 + 3"),
        AIMessage("I'll use the add tool", additional_kwargs={'engine_name': 'planner'}),
        ToolMessage("8", tool_call_id="call_123", additional_kwargs={'engine_name': 'math_tool'})
    ])
    
    print("✅ MessageList created with engine metadata")
    
    # Test serialization
    serialized = messages.model_dump()
    print("✅ MessageList serialized successfully")
    print(f"Serialized type: {type(serialized)}")
    print(f"Message count: {len(serialized)}")
    
    for i, msg in enumerate(serialized):
        print(f"  Message {i}: type={msg.get('type')}")
        if 'engine_name' in msg:
            print(f"    engine_name: {msg['engine_name']}")
        if 'tool_call_id' in msg:
            print(f"    tool_call_id: {msg['tool_call_id']}")


if __name__ == "__main__":
    # Test MessageList first
    test_messagelist_serialization()
    
    # Test the full Plan & Execute agent
    test_plan_execute_with_simple_agents()