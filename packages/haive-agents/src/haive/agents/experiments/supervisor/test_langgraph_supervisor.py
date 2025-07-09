"""Test supervisor using LangGraph directly (avoiding Haive BaseGraph bug)."""

import asyncio
import operator
from typing import Annotated, Any, Dict, Literal, Sequence, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.graph import END, StateGraph

# Import our working components
from haive.agents.experiments.supervisor.agent_info import AgentInfo
from haive.agents.experiments.supervisor.test_utils import create_test_agents


# Define state using TypedDict for LangGraph
class SupervisorGraphState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    agents: Dict[str, AgentInfo]
    active_agents: set
    next_agent: str
    agent_task: str
    agent_response: str


async def supervisor_node(state: SupervisorGraphState) -> Dict[str, Any]:
    """Supervisor node that analyzes task and routes to appropriate agent."""
    # Get last user message
    user_message = None
    for msg in reversed(state["messages"]):
        if isinstance(msg, HumanMessage):
            user_message = msg.content
            break

    if not user_message:
        return {"messages": [AIMessage(content="No task provided.")]}

    # Simple routing logic
    task_lower = user_message.lower()

    # Determine which agent to use
    if any(word in task_lower for word in ["search", "find", "look up", "research"]):
        chosen_agent = "search_agent"
        reasoning = "This task requires web search capabilities."
    elif any(
        word in task_lower for word in ["calculate", "math", "add", "multiply", "sum"]
    ):
        chosen_agent = "math_agent"
        reasoning = "This task requires mathematical calculations."
    elif any(word in task_lower for word in ["plan", "organize", "steps", "strategy"]):
        chosen_agent = "planning_agent"
        reasoning = "This task requires planning and organization."
    else:
        # Default to search if unclear
        chosen_agent = "search_agent"
        reasoning = "Defaulting to search agent for general queries."

    # Check if agent is active
    if chosen_agent not in state.get("active_agents", set()):
        return {
            "messages": [
                AIMessage(
                    content=f"Agent '{chosen_agent}' is not currently active. Please choose another task."
                )
            ]
        }

    # Set routing in state
    return {
        "messages": [AIMessage(content=f"{reasoning} Routing to {chosen_agent}.")],
        "next_agent": chosen_agent,
        "agent_task": user_message,
    }


async def agent_execution_node(state: SupervisorGraphState) -> Dict[str, Any]:
    """Execute the selected agent."""
    agent_name = state.get("next_agent")
    task = state.get("agent_task")

    if not agent_name or not task:
        return {"agent_response": "No agent or task specified"}

    # Get agent from state
    agent_info = state["agents"].get(agent_name)
    if not agent_info:
        return {"agent_response": f"Agent '{agent_name}' not found"}

    # Check if active
    if not agent_info.is_active():
        return {"agent_response": f"Agent '{agent_name}' is inactive"}

    # Get actual agent
    agent = agent_info.get_agent()

    try:
        # Execute agent
        print(f"   Executing {agent_name} with task: {task}")

        if hasattr(agent, "arun"):
            result = await agent.arun(task)
        elif hasattr(agent, "invoke"):
            result = agent.invoke({"input": task})
        else:
            result = f"Agent {agent_name} has no execution method"

        return {
            "agent_response": str(result),
            "messages": [
                AIMessage(
                    content=f"Agent {agent_name} completed: {str(result)[:100]}..."
                )
            ],
            "next_agent": "",
            "agent_task": "",
        }

    except Exception as e:
        return {
            "agent_response": f"Error executing {agent_name}: {str(e)}",
            "messages": [AIMessage(content=f"Error: {str(e)}")],
            "next_agent": "",
            "agent_task": "",
        }


def route_supervisor(state: SupervisorGraphState) -> Literal["agent_execution", "end"]:
    """Route based on supervisor's decision."""
    if state.get("next_agent") and state.get("agent_task"):
        return "agent_execution"
    return "end"


async def test_langgraph_supervisor():
    """Test the supervisor using LangGraph directly."""
    print("\n=== Testing LangGraph Dynamic Supervisor ===\n")

    # Create test agents
    agents_dict = await create_test_agents()

    print("1. Created agents:")
    for name, info in agents_dict.items():
        print(f"   - {name}: {info.description} (active: {info.active})")

    # Build graph
    print("\n2. Building graph...")
    workflow = StateGraph(SupervisorGraphState)

    # Add nodes
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("agent_execution", agent_execution_node)

    # Add edges
    workflow.set_entry_point("supervisor")
    workflow.add_conditional_edges(
        "supervisor",
        route_supervisor,
        {"agent_execution": "agent_execution", "end": END},
    )
    workflow.add_edge("agent_execution", END)

    # Compile
    app = workflow.compile()
    print("   ✅ Graph compiled successfully!")

    # Test 1: Math task
    print("\n3. Testing math task...")
    initial_state = {
        "messages": [HumanMessage(content="Calculate 25 + 15")],
        "agents": agents_dict,
        "active_agents": {"search_agent", "math_agent"},
        "next_agent": "",
        "agent_task": "",
        "agent_response": "",
    }

    result = await app.ainvoke(initial_state)

    print(f"   Messages: {len(result['messages'])}")
    for i, msg in enumerate(result["messages"]):
        print(f"   [{i}] {msg.content[:100]}")

    if result.get("agent_response"):
        print(f"   Agent response: {result['agent_response']}")

    # Test 2: Search task
    print("\n4. Testing search task...")
    search_state = {
        "messages": [
            HumanMessage(
                content="Search for information about Python async programming"
            )
        ],
        "agents": agents_dict,
        "active_agents": {"search_agent", "math_agent"},
        "next_agent": "",
        "agent_task": "",
        "agent_response": "",
    }

    result2 = await app.ainvoke(search_state)

    print(f"   Messages: {len(result2['messages'])}")
    if result2.get("agent_response"):
        print(f"   Agent response preview: {result2['agent_response'][:100]}...")

    # Test 3: Inactive agent
    print("\n5. Testing inactive agent...")
    plan_state = {
        "messages": [HumanMessage(content="Create a plan for building a web app")],
        "agents": agents_dict,
        "active_agents": {"search_agent", "math_agent"},  # planning_agent not active
        "next_agent": "",
        "agent_task": "",
        "agent_response": "",
    }

    result3 = await app.ainvoke(plan_state)

    print(f"   Messages: {len(result3['messages'])}")
    print(f"   Last message: {result3['messages'][-1].content}")

    print("\n✅ LangGraph supervisor test complete!")


if __name__ == "__main__":
    asyncio.run(test_langgraph_supervisor())
