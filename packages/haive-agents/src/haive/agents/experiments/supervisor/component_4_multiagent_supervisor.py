"""Component 4: Dynamic Supervisor using MultiAgentBase approach.

This implementation uses MultiAgentBase to orchestrate a supervisor agent
with dynamic agent execution capabilities.
"""

import asyncio
from typing import Any, Dict, Literal

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from haive.core.schema.agent_schema_composer import BuildMode
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END
from pydantic import Field

# Import our components
from haive.agents.experiments.supervisor.component_2_tools import (
    SupervisorStateWithTools,
)
from haive.agents.experiments.supervisor.component_3_agent_execution import (
    create_agent_execution_node,
)
from haive.agents.multi.enhanced_base import MultiAgentBase
from haive.agents.simple.agent import SimpleAgent

# Create supervisor prompt
SUPERVISOR_PROMPT = """You are an intelligent task supervisor that routes tasks to specialized agents.

Available agents:
{agent_descriptions}

Your job is to:
1. Analyze the user's task
2. Decide which agent is best suited to handle it
3. Set next_agent and agent_task in your response
4. Or decide to END if the task is complete

Always respond with your reasoning first, then your decision.
"""


def create_supervisor_engine(state: SupervisorStateWithTools) -> AugLLMConfig:
    """Create supervisor engine with dynamic agent descriptions."""
    # Build agent descriptions from state
    agent_descriptions = []
    for name, info in state.agents.items():
        if info.active:
            agent_descriptions.append(f"- {name}: {info.description}")

    descriptions_text = (
        "\n".join(agent_descriptions) if agent_descriptions else "No agents available"
    )

    # Create supervisor engine with tools from state
    return AugLLMConfig(
        name="supervisor_engine",
        llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.3),
        tools=state.get_all_tools(),  # Use tools from state
        system_message=SUPERVISOR_PROMPT.format(agent_descriptions=descriptions_text),
    )


def route_supervisor(
    state: SupervisorStateWithTools,
) -> Literal["agent_execution", "END"]:
    """Route based on supervisor's decision in state."""
    # Check if supervisor set an agent to execute
    if state.next_agent and state.agent_task:
        return "agent_execution"

    # Check for explicit END signal
    if state.next_agent == "END":
        return "END"

    # Default to END if no routing
    return "END"


async def supervisor_node(state: SupervisorStateWithTools) -> dict[str, Any]:
    """Supervisor node that uses dynamic tools from state."""
    # Get last user message
    user_message = None
    for msg in reversed(state.messages):
        if msg.role == "user":
            user_message = msg.content
            break

    if not user_message:
        return {"messages": [AIMessage(content="No task provided.")]}

    # Create supervisor agent with current state tools
    supervisor = SimpleAgent(name="supervisor", engine=create_supervisor_engine(state))

    # Run supervisor with the task
    result = await supervisor.arun(user_message)

    # The supervisor should have used tools to set routing in state
    # Add supervisor's reasoning to messages
    return {"messages": [AIMessage(content=result)]}


def create_dynamic_supervisor_system() -> MultiAgentBase:
    """Create the complete dynamic supervisor system using MultiAgentBase."""
    # Create agent execution node
    agent_execution_node = create_agent_execution_node()

    # Create supervisor as a workflow node (not an agent)
    # This allows us to use state-based tools dynamically

    system = MultiAgentBase(
        agents=[],  # No pre-defined agents - supervisor is a workflow node
        workflow_nodes={
            "supervisor": supervisor_node,
            "agent_execution": agent_execution_node,
        },
        branches=[
            # Supervisor routes to agent_execution or END
            (
                "supervisor",
                route_supervisor,
                {"agent_execution": "agent_execution", "END": END},
            )
        ],
        # After agent execution, go back to supervisor
        entry_points=["supervisor"],
        finish_points=["agent_execution"],  # Agent execution goes back to supervisor
        state_schema_override=SupervisorStateWithTools,
        schema_build_mode=BuildMode.SEQUENCE,
        name="Dynamic Supervisor System",
    )

    return system


async def test_multiagent_supervisor():
    """Test the MultiAgentBase supervisor implementation."""
    try:
        from .test_utils import create_test_agents
    except ImportError:
        from test_utils import create_test_agents

    # Create test agents
    agents_dict = await create_test_agents()

    # Create the supervisor system
    system = create_dynamic_supervisor_system()

    # Build and compile the graph
    graph = system.build_graph()
    compiled = graph.compile()

    # Create initial state with agents
    initial_state = {
        "messages": [
            HumanMessage(content="Search for information about Haive framework")
        ],
        "agents": agents_dict,
        "active_agents": {"search_agent", "math_agent"},  # planning_agent is inactive
    }

    # Run the system

    result = await compiled.ainvoke(initial_state)

    if result.get("agent_response"):
        pass

    # Test with a math task
    initial_state["messages"] = [HumanMessage(content="Calculate 15 + 27")]

    result = await compiled.ainvoke(initial_state)


# Add a simpler test for just the routing
async def test_routing_logic():
    """Test just the routing logic without full system."""
    from haive.agents.experiments.supervisor.component_1_state_foundation import (
        create_test_simple_agent,
    )

    # Create minimal state
    state = SupervisorStateWithTools()

    # Add test agents
    search_agent = await create_test_simple_agent("search", "Web search specialist")
    state.add_agent("search_agent", search_agent, "Web search specialist")

    # Test routing with no task
    route_supervisor(state)

    # Test routing with task set
    state.next_agent = "search_agent"
    state.agent_task = "Search for Python tutorials"
    route_supervisor(state)

    # Test explicit END
    state.next_agent = "END"
    state.agent_task = ""
    route_supervisor(state)


if __name__ == "__main__":
    # Run routing test first (simpler)
    asyncio.run(test_routing_logic())

    # Then run full system test
    asyncio.run(test_multiagent_supervisor())
