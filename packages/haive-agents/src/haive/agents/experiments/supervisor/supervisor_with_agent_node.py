"""
Supervisor with a single agent execution node.

Instead of creating tools for each agent, we have:
1. Tools that set the agent name in state
2. One node that reads agent name from state and executes that agent
"""

import asyncio
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema import StateSchema
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph import END
from pydantic import Field, model_validator

from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent


class SupervisorState(StateSchema):
    """State that tracks agent routing."""

    messages: List[Any] = Field(default_factory=list)
    selected_agent: Optional[str] = Field(default=None)  # Which agent to execute
    agent_task: Optional[str] = Field(default=None)  # Task for the agent
    agent_response: Optional[str] = Field(default=None)  # Response from agent
    available_agents: Dict[str, Any] = Field(default_factory=dict)  # Agent registry


class AgentExecutionNode:
    """Node that executes agents based on state."""

    def __init__(self, name: str = "agent_execution_node"):
        self.name = name

    async def __call__(self, state: SupervisorState) -> Dict[str, Any]:
        """Execute the selected agent from state."""
        # Check if we have an agent selected
        if not state.selected_agent:
            state.agent_response = "No agent selected"
            return {"state": state}

        # Get the agent from state
        agent = state.available_agents.get(state.selected_agent)
        if not agent:
            state.agent_response = (
                f"Agent '{state.selected_agent}' not found in registry"
            )
            state.selected_agent = None
            return {"state": state}

        # Get the task
        task = state.agent_task or "No task specified"

        try:
            # Create runnable from agent and invoke with messages
            # The agent should have an arun method or be a runnable
            if hasattr(agent, "arun"):
                # Async agent
                result = await agent.arun(task)
            elif hasattr(agent, "run"):
                # Sync agent
                result = agent.run(task)
            elif hasattr(agent, "invoke"):
                # LangChain runnable
                result = await agent.ainvoke({"messages": [HumanMessage(content=task)]})
                if isinstance(result, dict) and "messages" in result:
                    # Extract content from messages
                    last_msg = result["messages"][-1]
                    result = (
                        last_msg.content
                        if hasattr(last_msg, "content")
                        else str(last_msg)
                    )
            else:
                result = (
                    f"Agent {state.selected_agent} doesn't have a runnable interface"
                )

            state.agent_response = result

            # Add to message history
            state.messages.append(
                {
                    "role": "assistant",
                    "content": result,
                    "agent": state.selected_agent,
                    "timestamp": datetime.now().isoformat(),
                }
            )

        except Exception as e:
            state.agent_response = f"Error executing {state.selected_agent}: {str(e)}"

        # Clear selection for next iteration
        state.selected_agent = None
        state.agent_task = None

        return {"state": state}


class SupervisorWithAgentNode(ReactAgent):
    """
    Supervisor that uses a single agent execution node.

    Tools only set the agent selection in state.
    The agent node handles actual execution.
    """

    @model_validator(mode="after")
    def setup_supervisor(self):
        """Setup supervisor tools."""
        self._create_routing_tools()
        return self

    def _create_routing_tools(self):
        """Create tools that route to agents (just set state)."""
        if not self.engine:
            return

        tools = []

        @tool
        def select_math_agent(task: str) -> str:
            """Select the math agent to handle a mathematical task."""
            # This tool just marks the selection, doesn't execute
            return f"Selected math_agent for: {task}"

        @tool
        def select_search_agent(task: str) -> str:
            """Select the search agent to find information."""
            return f"Selected search_agent for: {task}"

        @tool
        def select_writer_agent(task: str) -> str:
            """Select the writer agent to create content."""
            return f"Selected writer_agent for: {task}"

        @tool
        def list_available_agents() -> List[str]:
            """List all available agents."""
            # In real implementation, this would check state.available_agents
            return ["math_agent", "search_agent", "writer_agent"]

        @tool
        def check_agent_status(agent_name: str) -> str:
            """Check if an agent is available."""
            # In real implementation, this would check state
            return f"Agent {agent_name} is available"

        tools.extend(
            [
                select_math_agent,
                select_search_agent,
                select_writer_agent,
                list_available_agents,
                check_agent_status,
            ]
        )

        self.engine.tools = tools

    def build_graph(self) -> BaseGraph:
        """Build graph with agent execution node."""
        graph = BaseGraph(name=self.name)

        # Supervisor node (uses tools to select agents)
        graph.add_node("supervisor", self._supervisor_node)

        # Agent execution node (executes selected agent)
        agent_node = AgentExecutionNode()
        graph.add_node("agent_node", agent_node)

        # Flow
        graph.set_entry_point("supervisor")

        # Conditional routing
        graph.add_conditional_edges(
            "supervisor",
            self._check_agent_selection,
            {"execute": "agent_node", "end": END},
        )

        # Loop back for multi-step tasks
        graph.add_edge("agent_node", "supervisor")

        return graph.compile()

    async def _supervisor_node(self, state: SupervisorState) -> Dict[str, Any]:
        """Supervisor analyzes task and selects agent."""
        # Get current task from messages
        if state.messages:
            last_msg = state.messages[-1]
            if isinstance(last_msg, dict):
                task = last_msg.get("content", "")
            else:
                task = str(last_msg)
        else:
            task = ""

        # Use LLM with tools to analyze and select
        prompt = f"""
You are a supervisor that routes tasks to specialized agents.

Task: {task}

Available agents:
- math_agent: Handles mathematical calculations
- search_agent: Finds information
- writer_agent: Creates written content

Use the select_[agent]_agent tools to route tasks.
The tool will set up the routing, then the agent will be executed.

Important: After using a select tool, set state.selected_agent and state.agent_task.
"""

        result = await self.engine.ainvoke({"messages": [HumanMessage(content=prompt)]})

        # Parse tool calls to set state
        # In a real implementation, this would parse the actual tool calls
        # For now, simple pattern matching
        response_text = str(result)

        if "select_math_agent" in response_text:
            state.selected_agent = "math_agent"
            state.agent_task = task
        elif "select_search_agent" in response_text:
            state.selected_agent = "search_agent"
            state.agent_task = task
        elif "select_writer_agent" in response_text:
            state.selected_agent = "writer_agent"
            state.agent_task = task

        return {"state": state}

    def _check_agent_selection(
        self, state: SupervisorState
    ) -> Literal["execute", "end"]:
        """Check if an agent was selected."""
        if state.selected_agent:
            return "execute"
        return "end"


# Demo
async def demo_agent_node_pattern():
    """Demonstrate the agent node pattern."""

    print("=== Agent Node Pattern Demo ===\n")

    # Create agents
    @tool
    def multiply(a: int, b: int) -> int:
        """Multiply two numbers."""
        return a * b

    math_engine = AugLLMConfig(
        name="math_engine",
        model="gpt-4",
        tools=[multiply],
        system_message="You are a math assistant.",
    ).create()

    math_agent = SimpleAgent(name="math_agent", engine=math_engine)

    search_engine = AugLLMConfig(
        name="search_engine",
        model="gpt-4",
        system_message="You are a search assistant. Simulate searching.",
    ).create()

    search_agent = SimpleAgent(name="search_agent", engine=search_engine)

    # Create supervisor
    supervisor_engine = AugLLMConfig(
        name="supervisor_engine",
        model="gpt-4",
        tools=[],  # Tools added by supervisor
        system_message="You are a task routing supervisor.",
    ).create()

    supervisor = SupervisorWithAgentNode(
        name="supervisor", engine=supervisor_engine, state_schema=SupervisorState
    )

    # Initialize state with agents
    initial_state = SupervisorState(
        available_agents={"math_agent": math_agent, "search_agent": search_agent}
    )

    # Test routing
    print("Test 1: Math task")
    initial_state.messages = [{"role": "user", "content": "Calculate 7 * 8"}]
    result = await supervisor.graph.ainvoke(initial_state)
    print(f"Result: {result.get('agent_response', 'No response')}\n")

    print("Test 2: Search task")
    initial_state.messages = [
        {"role": "user", "content": "Find information about Python"}
    ]
    result = await supervisor.graph.ainvoke(initial_state)
    print(f"Result: {result.get('agent_response', 'No response')}\n")

    print("✅ Key Pattern:")
    print("- Tools just set state.selected_agent")
    print("- Agent node reads state and executes the agent")
    print("- Agents can be added/removed from state.available_agents dynamically!")


if __name__ == "__main__":
    print("Agent Execution Node Pattern")
    print("One node executes any agent based on state routing\n")

    # Show the pattern
    print("Pattern flow:")
    print("1. Supervisor tools set state.selected_agent = 'agent_name'")
    print("2. Agent node reads state.selected_agent")
    print("3. Agent node gets agent from state.available_agents")
    print("4. Agent node creates runnable and invokes with task")
    print("5. Response goes back to state.agent_response")
