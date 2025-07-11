"""Clean 3-node supervisor: supervisor -> (execute_agent | add_agent | END).

Simple, clear routing:
- execute_agent: Takes agent name + payload, runs the agent
- add_agent: Creates and registers a new agent
- END: Finishes the conversation
"""

import asyncio
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema import StateSchema
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.graph import END
from pydantic import BaseModel, Field

from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent


class SupervisorState(StateSchema):
    """State for the 3-node supervisor."""

    messages: list[Any] = Field(default_factory=list)

    # Agent execution
    agent_to_execute: str | None = Field(default=None)
    execution_payload: str | None = Field(default=None)
    agent_response: str | None = Field(default=None)

    # Agent creation
    agent_to_add: dict[str, Any] | None = Field(default=None)

    # Agent registry (stored in state)
    available_agents: dict[str, Any] = Field(default_factory=dict)
    agent_metadata: dict[str, dict[str, Any]] = Field(default_factory=dict)


class ExecuteAgentNode:
    """Node that executes any agent by name."""

    async def __call__(self, state: SupervisorState) -> dict[str, Any]:
        """Execute the specified agent with the payload."""
        agent_name = state.agent_to_execute
        payload = state.execution_payload

        if not agent_name:
            state.agent_response = "No agent specified for execution"
            return {"state": state}

        if agent_name not in state.available_agents:
            state.agent_response = f"Agent '{agent_name}' not found. Available: {list(state.available_agents.keys())}"
            state.agent_to_execute = None
            state.execution_payload = None
            return {"state": state}

        agent = state.available_agents[agent_name]
        task = payload or "No task specified"

        try:
            # Execute the agent
            if hasattr(agent, "arun"):
                result = await agent.arun(task)
            elif hasattr(agent, "invoke"):
                result = await agent.ainvoke({"messages": [HumanMessage(content=task)]})
                # Extract content if result has messages
                if isinstance(result, dict) and "messages" in result:
                    last_msg = result["messages"][-1]
                    result = getattr(last_msg, "content", str(last_msg))
            else:
                result = f"Agent {agent_name} has no runnable interface"

            state.agent_response = f"{agent_name}: {result}"

            # Add to conversation
            state.messages.append(
                {
                    "role": "assistant",
                    "content": state.agent_response,
                    "agent": agent_name,
                    "timestamp": datetime.now().isoformat(),
                }
            )

            # Update usage metadata
            if agent_name in state.agent_metadata:
                state.agent_metadata[agent_name]["usage_count"] = (
                    state.agent_metadata[agent_name].get("usage_count", 0) + 1
                )
                state.agent_metadata[agent_name]["last_used"] = datetime.now()

        except Exception as e:
            state.agent_response = f"Error executing {agent_name}: {e!s}"

        # Clear execution state
        state.agent_to_execute = None
        state.execution_payload = None

        return {"state": state}


class AddAgentNode:
    """Node that creates and adds new agents."""

    async def __call__(self, state: SupervisorState) -> dict[str, Any]:
        """Create and register a new agent."""
        agent_spec = state.agent_to_add

        if not agent_spec:
            return {"state": state}

        try:
            # Extract agent specification
            name = agent_spec.get("name")
            agent_type = agent_spec.get("type", "simple")
            description = agent_spec.get("description", "")
            system_message = agent_spec.get("system_message", "")
            tools = agent_spec.get("tools", [])

            if not name:
                state.agent_response = "Agent name is required"
                state.agent_to_add = None
                return {"state": state}

            if name in state.available_agents:
                state.agent_response = f"Agent '{name}' already exists"
                state.agent_to_add = None
                return {"state": state}

            # Create engine for the agent
            engine = AugLLMConfig(
                name=f"{name}_engine",
                model="gpt-4",
                tools=tools,
                system_message=system_message or f"You are {name}, {description}",
            ).create()

            # Create agent based on type
            if agent_type == "react":
                from haive.agents.react.agent import ReactAgent

                agent = ReactAgent(name=name, engine=engine)
            else:
                agent = SimpleAgent(name=name, engine=engine)

            # Register in state
            state.available_agents[name] = agent
            state.agent_metadata[name] = {
                "description": description,
                "type": agent_type,
                "created_at": datetime.now(),
                "usage_count": 0,
                "last_used": None,
            }

            state.agent_response = (
                f"Created and registered agent '{name}' ({agent_type}): {description}"
            )

            # Add to conversation
            state.messages.append(
                {
                    "role": "assistant",
                    "content": state.agent_response,
                    "action": "agent_created",
                    "timestamp": datetime.now().isoformat(),
                }
            )

        except Exception as e:
            state.agent_response = f"Error creating agent: {e!s}"

        # Clear creation state
        state.agent_to_add = None

        return {"state": state}


class ThreeNodeSupervisor(ReactAgent):
    """Clean supervisor with exactly 3 destinations:
    supervisor -> execute_agent | add_agent | END.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._setup_tools()

    def _setup_tools(self):
        """Create the supervisor's tools."""
        if not self.engine:
            return

        @tool
        def execute_agent(agent_name: str, task: str) -> str:
            """Execute a specific agent with a task. Sets up execution for the next node."""
            return f"Will execute {agent_name} with task: {task}"

        @tool
        def add_new_agent(
            name: str,
            description: str,
            agent_type: str = "simple",
            system_message: str = "",
        ) -> str:
            """Add a new agent to the system. Sets up creation for the next node."""
            return f"Will create {agent_type} agent '{name}': {description}"

        @tool
        def list_agents() -> list[str]:
            """List all available agents and their descriptions."""
            # This would access state in real implementation
            return ["Use this tool to see available agents"]

        @tool
        def agent_status(agent_name: str) -> str:
            """Get status and metadata for a specific agent."""
            return f"Status check for {agent_name}"

        @tool
        def finish_conversation() -> str:
            """End the conversation."""
            return "Conversation will end"

        self.engine.tools = [
            execute_agent,
            add_new_agent,
            list_agents,
            agent_status,
            finish_conversation,
        ]

    def build_graph(self) -> BaseGraph:
        """Build the clean 3-node graph."""
        graph = BaseGraph(name=self.name)

        # The 3 nodes
        graph.add_node("supervisor", self._supervisor_node)
        graph.add_node("execute_agent", ExecuteAgentNode())
        graph.add_node("add_agent", AddAgentNode())

        # Entry point
        graph.set_entry_point("supervisor")

        # Supervisor routes to one of 3 destinations
        graph.add_conditional_edges(
            "supervisor",
            self._route_supervisor,
            {"execute": "execute_agent", "add": "add_agent", "end": END},
        )

        # Both execution nodes loop back to supervisor
        graph.add_edge("execute_agent", "supervisor")
        graph.add_edge("add_agent", "supervisor")

        return graph.compile()

    async def _supervisor_node(self, state: SupervisorState) -> dict[str, Any]:
        """Supervisor node that uses tools to set up routing."""
        # Get current input
        if state.messages:
            last_msg = state.messages[-1]
            if isinstance(last_msg, dict):
                user_input = last_msg.get("content", "")
            else:
                user_input = str(last_msg)
        else:
            user_input = ""

        # Create context prompt
        agent_list = (
            list(state.available_agents.keys())
            if state.available_agents
            else ["No agents registered"]
        )

        prompt = f"""
You are a supervisor managing agents. Current user request: {user_input}

Available agents: {agent_list}

Your tools:
- execute_agent(agent_name, task): Execute an existing agent
- add_new_agent(name, description, type, system_message): Create a new agent
- list_agents(): See all available agents
- agent_status(name): Check agent metadata
- finish_conversation(): End the conversation

Important: After using a tool, set the appropriate state fields:
- execute_agent -> set state.agent_to_execute and state.execution_payload
- add_new_agent -> set state.agent_to_add with agent spec
- finish_conversation -> no state changes needed
"""

        # Invoke LLM with tools
        result = await self.engine.ainvoke({"messages": [HumanMessage(content=prompt)]})

        # Parse result to set state (simplified - in real implementation would parse tool calls)
        result_str = str(result)

        if "execute_agent" in result_str:
            # Extract agent name and task (simplified parsing)
            # In real implementation, would parse actual tool calls
            if "math" in user_input.lower():
                state.agent_to_execute = (
                    "math_agent" if "math_agent" in state.available_agents else None
                )
            elif "search" in user_input.lower():
                state.agent_to_execute = (
                    "search_agent" if "search_agent" in state.available_agents else None
                )
            state.execution_payload = user_input

        elif "add_new_agent" in result_str:
            # Set agent creation spec
            if "math" in user_input.lower():
                state.agent_to_add = {
                    "name": "math_agent",
                    "type": "simple",
                    "description": "Mathematical calculations",
                    "system_message": "You are a math assistant",
                }
            elif "search" in user_input.lower():
                state.agent_to_add = {
                    "name": "search_agent",
                    "type": "simple",
                    "description": "Information search",
                    "system_message": "You are a search assistant",
                }

        return {"state": state}

    def _route_supervisor(
        self, state: SupervisorState
    ) -> Literal["execute", "add", "end"]:
        """Route to one of the 3 destinations."""
        if state.agent_to_execute:
            return "execute"
        if state.agent_to_add:
            return "add"
        return "end"


# Demo the clean 3-node pattern
async def demo_three_node_supervisor():
    """Demonstrate the 3-node supervisor pattern."""
    # Create supervisor
    supervisor_engine = AugLLMConfig(
        name="supervisor_engine",
        model="gpt-4",
        tools=[],  # Tools added by supervisor
        system_message="You are a task routing supervisor with 3 actions: execute, add, or end.",
    ).create()

    ThreeNodeSupervisor(
        name="three_node_supervisor",
        engine=supervisor_engine,
        state_schema=SupervisorState,
    )

    # Test the routing
    initial_state = SupervisorState()

    # Test 1: Try to execute non-existent agent (should route to add)
    initial_state.messages = [{"role": "user", "content": "Calculate 5 + 3"}]

    # Simulate supervisor decision
    initial_state.agent_to_add = {
        "name": "math_agent",
        "type": "simple",
        "description": "Math calculations",
        "system_message": "You are a math assistant",
    }

    # Execute add_agent node
    add_node = AddAgentNode()
    await add_node(initial_state)

    # Test 2: Now execute the created agent
    initial_state.agent_to_execute = "math_agent"
    initial_state.execution_payload = "Calculate 5 + 3"

    execute_node = ExecuteAgentNode()
    await execute_node(initial_state)


if __name__ == "__main__":

    # Show the routing logic

    asyncio.run(demo_three_node_supervisor())
