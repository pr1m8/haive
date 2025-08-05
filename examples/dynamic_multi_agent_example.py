"""Dynamic Multi-Agent System with Tool Routing and Recompilation.

This example demonstrates how to:
1. Use Send/Command for dynamic agent routing
2. Add tools dynamically to agents and signal recompilation
3. Handle tool_route annotations dynamically
"""

from __future__ import annotations

import logging
import operator
from typing import Annotated, Any

from langchain_core.tools import tool
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, Send
from pydantic import BaseModel, Field, computed_field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# MOCK CLASSES (to avoid imports during test)
# ============================================================================


class MockAgent:
    """Mock agent for demonstration."""

    def __init__(self, name: str, tools: list | None = None):
        self.name = name
        self.tools = tools or []
        self.tool_routes = {}
        self._recompile_needed = False

    def add_tool(self, tool_func, route: str):
        """Add a tool dynamically."""
        tool_name = tool_func.name if hasattr(tool_func, "name") else tool_func.__name__
        self.tools.append(tool_func)
        self.tool_routes[tool_name] = route
        self._recompile_needed = True
        logger.info(f"Added tool {tool_name} with route {route} to agent {self.name}")

    def needs_recompile(self):
        return self._recompile_needed

    def mark_compiled(self):
        self._recompile_needed = False

    def create_runnable(self):
        """Create a runnable that respects tool routes."""

        def runnable(state):
            # This would be the actual agent logic
            return {
                "agent_name": self.name,
                "processed": True,
                "tool_routes": self.tool_routes,
            }

        return runnable


# ============================================================================
# TOOLS
# ============================================================================


@tool
def calculate(expression: str) -> float:
    """Calculate a mathematical expression."""
    return eval(expression)


@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Search results for: {query}"


@tool
def analyze(data: str) -> dict[str, Any]:
    """Analyze data and return insights."""
    return {"insight": f"Analysis of {data}", "confidence": 0.85}


# ============================================================================
# STATE DEFINITION
# ============================================================================


class MultiAgentState(BaseModel):
    """State for multi-agent system with dynamic tool routing."""

    # Agent management
    agents: dict[str, MockAgent] = Field(default_factory=dict)
    selected_agents: Annotated[list[str], operator.add] = Field(default_factory=list)

    # Tool routing
    global_tool_routes: dict[str, str] = Field(default_factory=dict)
    pending_tool_additions: list[dict[str, Any]] = Field(default_factory=list)

    # Execution state
    messages: Annotated[list[str], operator.add] = Field(default_factory=list)
    results: dict[str, Any] = Field(default_factory=dict)

    # Recompilation tracking
    agents_needing_recompile: Set[str] = Field(default_factory=set)
    graph_needs_recompile: bool = Field(default=False)

    @computed_field
    @property
    def selected_agent(self) -> str | None:
        """Get the most recently selected agent."""
        return self.selected_agents[-1] if self.selected_agents else None

    @computed_field
    @property
    def available_tools(self) -> list[str]:
        """Get all available tools across all agents."""
        tools = set()
        for agent in self.agents.values():
            tools.update(agent.tool_routes.keys())
        return list(tools)


# ============================================================================
# DYNAMIC ROUTING NODES
# ============================================================================


def agent_router(state: MultiAgentState) -> Send | list[Send] | Command:
    """Route to appropriate agent(s) based on state.

    This demonstrates how to use Send for dynamic routing without
    needing Literal types at compile time.
    """
    # Check if we need to handle tool additions first
    if state.pending_tool_additions:
        return Send("tool_manager", state)

    # Check if any agents need recompilation
    if state.agents_needing_recompile:
        return Send("recompilation_manager", state)

    # Route to selected agent
    if state.selected_agent and state.selected_agent in state.agents:
        # Use Send for dynamic routing - no Literal needed!
        return Send(
            "agent_executor",
            {"agent_name": state.selected_agent, "state": state},
        )

    # Or route to multiple agents in parallel
    if len(state.agents) > 1:
        # Send to multiple agents dynamically
        sends = []
        for agent_name in state.agents:
            sends.append(
                Send("agent_executor", {"agent_name": agent_name, "state": state}),
            )
        return sends

    # Default: go to end
    return Command(goto=END)


def tool_manager(arg: dict[str, Any]) -> Command:
    """Manage dynamic tool additions.

    This node handles adding tools to agents and marking them for
    recompilation.
    """
    state = arg if isinstance(arg, MultiAgentState) else arg.get("state")

    updates = {}
    agents_to_recompile = set()

    # Process pending tool additions
    for addition in state.pending_tool_additions:
        agent_name = addition["agent_name"]
        tool_func = addition["tool"]
        route = addition["route"]

        if agent_name in state.agents:
            agent = state.agents[agent_name]
            agent.add_tool(tool_func, route)
            agents_to_recompile.add(agent_name)

            # Update global tool routes
            tool_name = tool_func.name if hasattr(tool_func, "name") else tool_func.__name__
            state.global_tool_routes[tool_name] = f"{agent_name}.{route}"

    # Clear pending additions
    updates["pending_tool_additions"] = []
    updates["agents_needing_recompile"] = list(agents_to_recompile)
    updates["messages"] = [f"Added {len(state.pending_tool_additions)} tools"]

    # Route to recompilation manager
    return Command(update=updates, goto="recompilation_manager")


def recompilation_manager(arg: dict[str, Any]) -> Command:
    """Handle agent recompilation when tool routes change."""
    state = arg if isinstance(arg, MultiAgentState) else arg.get("state")

    recompiled = []
    for agent_name in state.agents_needing_recompile:
        if agent_name in state.agents:
            agent = state.agents[agent_name]
            if agent.needs_recompile():
                # In real implementation, this would rebuild the agent's graph
                logger.info(f"Recompiling agent {agent_name}")
                agent.mark_compiled()
                recompiled.append(agent_name)

    updates = {
        "agents_needing_recompile": [],
        "messages": [f"Recompiled agents: {', '.join(recompiled)}"],
    }

    # Continue to agent execution
    return Command(update=updates, goto="agent_router")


def agent_executor(arg: dict[str, Any]) -> Command:
    """Execute a specific agent.

    This receives custom args from Send, not just state.
    """
    agent_name = arg.get("agent_name")
    state = arg.get("state")

    if agent_name not in state.agents:
        return Command(update={"messages": [f"Agent {agent_name} not found"]}, goto=END)

    agent = state.agents[agent_name]
    runnable = agent.create_runnable()
    result = runnable(state)

    updates = {
        "results": {agent_name: result},
        "messages": [f"Executed agent {agent_name}"],
    }

    return Command(update=updates, goto=END)


def control_node(state: MultiAgentState) -> Command:
    """Main control node that orchestrates the flow.

    This demonstrates using Command for dynamic flow control.
    """
    # Dynamically determine next step
    if not state.agents:
        return Command(update={"messages": ["No agents available"]}, goto=END)

    # Check various conditions and route accordingly
    if state.pending_tool_additions:
        # Tools need to be added
        return Command(goto="agent_router")
    if state.selected_agent:
        # Specific agent selected
        return Command(goto="agent_router")
    # Need to select an agent
    return Command(update={"selected_agents": ["simple_agent"]}, goto="agent_router")


# ============================================================================
# GRAPH CONSTRUCTION
# ============================================================================


def build_dynamic_graph() -> StateGraph:
    """Build a graph that supports dynamic agent and tool management."""
    graph = StateGraph(MultiAgentState)

    # Add nodes - note we don't need to specify all possible agent nodes
    graph.add_node("control", control_node)
    graph.add_node("agent_router", agent_router)
    graph.add_node("tool_manager", tool_manager)
    graph.add_node("recompilation_manager", recompilation_manager)
    graph.add_node("agent_executor", agent_executor)

    # Add edges
    graph.add_edge(START, "control")
    # No need for literal types - nodes handle routing dynamically

    return graph


# ============================================================================
# USAGE EXAMPLE
# ============================================================================


def demonstrate_dynamic_tool_routing():
    """Demonstrate dynamic tool addition and routing."""
    # Create initial agents
    simple_agent = MockAgent("simple_agent", [calculate])
    react_agent = MockAgent("react_agent", [search])

    # Create initial state
    initial_state = MultiAgentState(
        agents={"simple_agent": simple_agent, "react_agent": react_agent},
    )

    # Build graph
    graph = build_dynamic_graph()
    app = graph.compile()

    for _name, _agent in initial_state.agents.items():
        pass

    # Run with initial configuration
    app.invoke(initial_state)

    # Now add a tool dynamically
    initial_state.pending_tool_additions = [
        {"agent_name": "simple_agent", "tool": analyze, "route": "analysis_route"},
    ]

    # Run again - this will trigger tool addition and recompilation
    app.invoke(initial_state)

    # Add multiple tools to different agents
    initial_state.pending_tool_additions = [
        {"agent_name": "simple_agent", "tool": search, "route": "search_route"},
        {"agent_name": "react_agent", "tool": analyze, "route": "react_analysis"},
    ]

    app.invoke(initial_state)

    # Demonstrate dynamic agent selection
    initial_state.selected_agents = ["react_agent"]
    initial_state.pending_tool_additions = []

    app.invoke(initial_state)


# ============================================================================
# KEY INSIGHTS
# ============================================================================
"""
Key Insights from this implementation:

1. **Dynamic Routing with Send**:
   - Send allows routing to nodes without compile-time literals
   - Can pass custom arguments, not just state
   - Enables map-reduce patterns and parallel execution

2. **Command for Flow Control**:
   - Command.goto accepts strings dynamically
   - No need for Literal types at runtime
   - Can update state and route in one operation

3. **Tool Route Management**:
   - Tools can be added to agents dynamically
   - Recompilation is triggered by state flags
   - Global tool route tracking enables cross-agent tool discovery

4. **Recompilation Pattern**:
   - Agents track their own recompilation needs
   - Central recompilation manager handles updates
   - Graph structure remains stable while agent internals change

5. **State-Driven Architecture**:
   - State contains all routing information
   - Nodes make decisions based on current state
   - No hardcoded paths or agent names in graph structure
"""

if __name__ == "__main__":
    demonstrate_dynamic_tool_routing()
