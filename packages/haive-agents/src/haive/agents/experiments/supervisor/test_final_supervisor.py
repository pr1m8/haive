"""Final test of dynamic supervisor with minimal imports."""

import asyncio
import operator

# Direct imports to avoid haive module chain
import sys
from pathlib import Path
from typing import Annotated, Any, Dict, Literal, Sequence, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.graph import END, StateGraph

sys.path.insert(0, str(Path(__file__).parent))

from agent_info import AgentInfo
from test_utils import create_test_agents


# Define state for LangGraph
class DynamicSupervisorState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    agents: dict[str, AgentInfo]
    active_agents: set
    next_agent: str
    agent_task: str
    agent_response: str
    generated_tools: list


async def supervisor_reasoning_node(state: DynamicSupervisorState) -> dict[str, Any]:
    """Supervisor that reasons about which agent to use."""
    # Get the last user message
    user_message = None
    for msg in reversed(state["messages"]):
        if isinstance(msg, HumanMessage):
            user_message = msg.content
            break

    if not user_message:
        return {"messages": [AIMessage(content="No task provided.")]}

    # Analyze the task
    task_lower = user_message.lower()

    # Simple keyword-based routing (in real implementation, use LLM)
    if any(word in task_lower for word in ["search", "find", "look", "research"]):
        agent_choice = "search_agent"
        reasoning = "This task requires web search capabilities."
    elif any(
        word in task_lower
        for word in ["calculate", "math", "add", "multiply", "divide"]
    ):
        agent_choice = "math_agent"
        reasoning = "This task requires mathematical calculations."
    elif any(word in task_lower for word in ["plan", "organize", "strategy", "steps"]):
        agent_choice = "planning_agent"
        reasoning = "This task requires planning and organization."
    else:
        agent_choice = "search_agent"
        reasoning = "Defaulting to search for general queries."

    # Check if agent is active
    if agent_choice not in state.get("active_agents", set()):
        return {
            "messages": [
                AIMessage(
                    content=f"I would use {agent_choice}, but it's not currently active. Available agents: {state['active_agents']}"
                )
            ]
        }

    # Route to the chosen agent
    return {
        "messages": [AIMessage(content=f"{reasoning} Delegating to {agent_choice}.")],
        "next_agent": agent_choice,
        "agent_task": user_message,
    }


async def agent_execution_node(state: DynamicSupervisorState) -> dict[str, Any]:
    """Execute the selected agent - mirrors tool_node pattern."""
    agent_name = state.get("next_agent")
    task = state.get("agent_task")

    if not agent_name or not task:
        return {"agent_response": "No agent or task specified"}

    # Get agent from state (like tool_node gets tools)
    agent_info = state["agents"].get(agent_name)
    if not agent_info:
        return {"agent_response": f"Agent '{agent_name}' not found"}

    # Check if active
    if not agent_info.is_active():
        return {"agent_response": f"Agent '{agent_name}' is inactive"}

    # Get the actual agent
    agent = agent_info.get_agent()

    try:
        # Execute agent
        if hasattr(agent, "arun"):
            result = await agent.arun(task)
        elif hasattr(agent, "invoke"):
            result = agent.invoke({"messages": [HumanMessage(content=task)]})
        else:
            result = f"Agent {agent_name} has no execution method"

        # Clear routing and return result
        return {
            "agent_response": str(result),
            "messages": [
                AIMessage(content=f"{agent_name} completed: {str(result)[:200]}...")
            ],
            "next_agent": "",
            "agent_task": "",
        }

    except Exception as e:
        import traceback

        traceback.print_exc()
        return {
            "agent_response": f"Error executing {agent_name}: {e!s}",
            "messages": [AIMessage(content=f"Error with {agent_name}: {e!s}")],
            "next_agent": "",
            "agent_task": "",
        }


def route_supervisor(state: DynamicSupervisorState) -> Literal["execute", "end"]:
    """Route based on supervisor decision."""
    if state.get("next_agent") and state.get("agent_task"):
        return "execute"
    return "end"


async def test_dynamic_supervisor():
    """Test the complete dynamic supervisor."""
    # Create test agents
    agents_dict = await create_test_agents()

    for _name, _info in agents_dict.items():
        pass

    # Build the supervisor graph
    workflow = StateGraph(DynamicSupervisorState)

    # Add the 3 core nodes
    workflow.add_node("supervisor", supervisor_reasoning_node)
    workflow.add_node("execute", agent_execution_node)

    # Set up routing
    workflow.set_entry_point("supervisor")
    workflow.add_conditional_edges(
        "supervisor", route_supervisor, {"execute": "execute", "end": END}
    )
    workflow.add_edge("execute", END)

    # Compile
    app = workflow.compile()

    # Test 1: Math calculation
    state1 = {
        "messages": [HumanMessage(content="Please calculate 25 + 15 for me")],
        "agents": agents_dict,
        "active_agents": {"search_agent", "math_agent"},
        "next_agent": "",
        "agent_task": "",
        "agent_response": "",
        "generated_tools": [],
    }

    await app.ainvoke(state1)

    # Test 2: Search task
    state2 = {
        "messages": [
            HumanMessage(content="Search for information about Python decorators")
        ],
        "agents": agents_dict,
        "active_agents": {"search_agent", "math_agent"},
        "next_agent": "",
        "agent_task": "",
        "agent_response": "",
        "generated_tools": [],
    }

    result2 = await app.ainvoke(state2)
    if result2.get("agent_response"):
        pass

    # Test 3: Dynamic agent addition
    # Activate the planning agent
    agents_dict["planning_agent"].activate()

    state3 = {
        "messages": [
            HumanMessage(content="Create a plan for learning machine learning")
        ],
        "agents": agents_dict,
        "active_agents": {
            "search_agent",
            "math_agent",
            "planning_agent",
        },  # Now active!
        "next_agent": "",
        "agent_task": "",
        "agent_response": "",
        "generated_tools": [],
    }

    await app.ainvoke(state3)

    # Test 4: Inactive agent handling
    state4 = {
        "messages": [HumanMessage(content="Please organize my day")],
        "agents": agents_dict,
        "active_agents": {
            "search_agent",
            "math_agent",
        },  # planning_agent not in active set
        "next_agent": "",
        "agent_task": "",
        "agent_response": "",
        "generated_tools": [],
    }

    await app.ainvoke(state4)


if __name__ == "__main__":
    asyncio.run(test_dynamic_supervisor())
