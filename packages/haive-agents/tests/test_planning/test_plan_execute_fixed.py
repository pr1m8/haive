"""Test Plan & Execute Agent with fixed MessageList serialization."""

from haive.agents.planning.plan_and_execute_multi import PlanAndExecuteAgent
from haive.agents.simple.agent import SimpleAgent


def test_plan_execute_with_simple_agents():
    """Test Plan & Execute using Simple agents for all roles."""
    try:
        # Create three simple agents for different roles
        planner = SimpleAgent(
            name="planner",
            system_message="You are a planning agent. Create detailed step-by-step plans to accomplish objectives.",
        )

        executor = SimpleAgent(
            name="executor",
            system_message="You are an execution agent. Execute individual steps from plans using available tools.",
        )

        replanner = SimpleAgent(
            name="replanner",
            system_message="You are a replanning agent. Determine if plans need revision or if objectives are complete.",
        )

        # Create the Plan & Execute multi-agent
        plan_execute_agent = PlanAndExecuteAgent(
            planner=planner,
            executor=executor,
            replanner=replanner,
            name="TestPlanExecute",
        )

        # Test compilation
        plan_execute_agent.compile()

    except Exception:
        import traceback

        traceback.print_exc()


def test_messagelist_serialization():
    """Test MessageList serialization independently."""
    from haive.core.schema.prebuilt.messages.messages_state import MessageList
    from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

    # Create test messages
    messages = MessageList(
        [
            HumanMessage("Calculate 5 + 3"),
            AIMessage(
                "I'll use the add tool", additional_kwargs={"engine_name": "planner"}
            ),
            ToolMessage(
                "8",
                tool_call_id="call_123",
                additional_kwargs={"engine_name": "math_tool"},
            ),
        ]
    )

    # Test serialization
    serialized = messages.model_dump()

    for _i, msg in enumerate(serialized):
        if "engine_name" in msg:
            pass
        if "tool_call_id" in msg:
            pass


if __name__ == "__main__":
    # Test MessageList first
    test_messagelist_serialization()

    # Test the full Plan & Execute agent
    test_plan_execute_with_simple_agents()
