"""Test complete supervisor without MultiAgentBase (due to import bug)."""

import asyncio
from typing import Any, Dict, Literal

from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END

# Import our working components
from haive.agents.experiments.supervisor.component_2_tools import (
    SupervisorStateWithTools,
)
from haive.agents.experiments.supervisor.component_3_agent_execution import (
    create_agent_execution_node,
)
from haive.agents.experiments.supervisor.test_utils import create_test_agents


async def supervisor_node(state: SupervisorStateWithTools) -> Dict[str, Any]:
    """Supervisor node that analyzes task and routes to appropriate agent."""
    # Get last user message
    user_message = None
    for msg in reversed(state.messages):
        if hasattr(msg, "content") and isinstance(msg, HumanMessage):
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
    if chosen_agent not in state.active_agents:
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


def route_supervisor(
    state: SupervisorStateWithTools,
) -> Literal["agent_execution", "END"]:
    """Route based on supervisor's decision."""
    if state.next_agent and state.agent_task:
        return "agent_execution"
    return "END"


async def test_complete_supervisor():
    """Test the complete dynamic supervisor system."""
    print("\n=== Testing Complete Dynamic Supervisor ===\n")

    # Create test agents
    agents_dict = await create_test_agents()

    # Create initial state
    initial_state = SupervisorStateWithTools(
        messages=[HumanMessage(content="Calculate 25 + 15")],
        agents=agents_dict,
        active_agents={"search_agent", "math_agent"},  # planning_agent is inactive
    )

    print("1. Initial setup:")
    print(f"   Agents: {list(initial_state.agents.keys())}")
    print(f"   Active: {initial_state.active_agents}")
    print(f"   Tools generated: {initial_state.generated_tools}")

    # Create nodes
    agent_execution_node = create_agent_execution_node()

    # Build graph
    print("\n2. Building graph...")
    graph = BaseGraph(state_schema=SupervisorStateWithTools)

    # Add nodes
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("agent_execution", agent_execution_node)

    # Add edges
    graph.set_entry_point("supervisor")
    graph.add_conditional_edges(
        "supervisor",
        route_supervisor,
        {"agent_execution": "agent_execution", "END": END},
    )
    graph.add_edge("agent_execution", END)

    # Compile
    compiled = graph.compile()
    print("   ✅ Graph compiled successfully!")

    # Test 1: Math task
    print("\n3. Testing math task...")
    result = await compiled.ainvoke(initial_state.model_dump())

    print(f"   Messages: {len(result.get('messages', []))}")
    for i, msg in enumerate(result.get("messages", [])):
        content = msg.get("content", "") if isinstance(msg, dict) else msg.content
        print(f"   [{i}] {content[:100]}")

    if result.get("agent_response"):
        print(f"   Agent response: {result['agent_response']}")

    # Test 2: Search task
    print("\n4. Testing search task...")
    search_state = SupervisorStateWithTools(
        messages=[
            HumanMessage(
                content="Search for information about Python async programming"
            )
        ],
        agents=agents_dict,
        active_agents={"search_agent", "math_agent"},
    )

    result2 = await compiled.ainvoke(search_state.model_dump())

    print(f"   Messages: {len(result2.get('messages', []))}")
    if result2.get("agent_response"):
        print(f"   Agent response: {result2['agent_response'][:100]}...")

    # Test 3: Inactive agent
    print("\n5. Testing inactive agent...")
    plan_state = SupervisorStateWithTools(
        messages=[HumanMessage(content="Create a plan for building a web app")],
        agents=agents_dict,
        active_agents={"search_agent", "math_agent"},  # planning_agent not active
    )

    result3 = await compiled.ainvoke(plan_state.model_dump())

    print(f"   Messages: {len(result3.get('messages', []))}")
    last_msg = result3.get("messages", [])[-1]
    content = (
        last_msg.get("content", "") if isinstance(last_msg, dict) else last_msg.content
    )
    print(f"   Last message: {content}")

    print("\n✅ Complete supervisor test finished!")


if __name__ == "__main__":
    asyncio.run(test_complete_supervisor())
