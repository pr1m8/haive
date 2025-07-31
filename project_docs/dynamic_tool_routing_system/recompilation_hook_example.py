"""Recompilation Hook Example for BaseGraph2.

This demonstrates how to extend BaseGraph2 to automatically detect
when tool routes change and signal recompilation needs.
"""

import logging
from collections.abc import Callable
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)

# ============================================================================
# RECOMPILATION-AWARE BASE GRAPH
# ============================================================================


class RecompilationAwareGraph:
    """Extended graph that tracks tool route changes and signals recompilation.

    This would be mixed into BaseGraph2 or used as a wrapper.
    """

    def __init__(self, name: str = "recompilation_aware_graph"):
        self.name = name
        self.nodes = {}
        self.edges = []
        self.tool_routes: dict[str, str] = {}
        self._tool_route_hash: str | None = None
        self._needs_recompile: bool = False
        self._recompile_callbacks: list[Callable] = []
        self._last_compiled_at: datetime | None = None

    def _compute_tool_route_hash(self) -> str:
        """Compute hash of current tool routes."""
        import hashlib

        route_str = str(sorted(self.tool_routes.items()))
        return hashlib.md5(route_str.encode()).hexdigest()

    def check_tool_routes_changed(self) -> bool:
        """Check if tool routes have changed since last compilation."""
        current_hash = self._compute_tool_route_hash()
        changed = current_hash != self._tool_route_hash
        if changed:
            logger.info(
                f"Tool routes changed - old hash: {self._tool_route_hash}, new hash: {current_hash}"
            )
        return changed

    def update_tool_routes(self, routes: dict[str, str]) -> None:
        """Update tool routes and check if recompilation is needed.

        Args:
            routes: New tool routes mapping
        """
        old_routes = self.tool_routes.copy()
        self.tool_routes.update(routes)

        if self.check_tool_routes_changed():
            self._needs_recompile = True
            self._notify_recompile_needed(
                "tool_routes_changed",
                {"old_routes": old_routes, "new_routes": self.tool_routes},
            )

    def add_tool_route(self, tool_name: str, route: str) -> None:
        """Add a single tool route."""
        if tool_name not in self.tool_routes or self.tool_routes[tool_name] != route:
            self.tool_routes[tool_name] = route
            if self.check_tool_routes_changed():
                self._needs_recompile = True
                self._notify_recompile_needed(
                    "tool_route_added", {"tool_name": tool_name, "route": route}
                )

    def remove_tool_route(self, tool_name: str) -> None:
        """Remove a tool route."""
        if tool_name in self.tool_routes:
            old_route = self.tool_routes.pop(tool_name)
            self._needs_recompile = True
            self._notify_recompile_needed(
                "tool_route_removed", {"tool_name": tool_name, "old_route": old_route}
            )

    def register_recompile_callback(
        self, callback: Callable[[str, dict], None]
    ) -> None:
        """Register a callback for recompilation events."""
        self._recompile_callbacks.append(callback)

    def _notify_recompile_needed(self, reason: str, details: dict[str, Any]) -> None:
        """Notify all callbacks that recompilation is needed."""
        for callback in self._recompile_callbacks:
            try:
                callback(reason, details)
            except Exception as e:
                logger.exception(f"Error in recompile callback: {e}")

    def needs_recompile(self) -> bool:
        """Check if graph needs recompilation."""
        return self._needs_recompile or self.check_tool_routes_changed()

    def mark_compiled(self) -> None:
        """Mark the graph as compiled."""
        self._needs_recompile = False
        self._tool_route_hash = self._compute_tool_route_hash()
        self._last_compiled_at = datetime.now()
        logger.info(f"Graph marked as compiled at {self._last_compiled_at}")

    def get_compilation_info(self) -> dict[str, Any]:
        """Get information about compilation state."""
        return {
            "needs_recompile": self.needs_recompile(),
            "last_compiled_at": self._last_compiled_at,
            "tool_route_hash": self._tool_route_hash,
            "current_tool_routes": self.tool_routes,
            "tool_routes_changed": self.check_tool_routes_changed(),
        }


# ============================================================================
# INTEGRATION WITH VALIDATION NODE
# ============================================================================


class ToolRouteAwareValidationNode:
    """Validation node that can dynamically update tool routes in the graph.

    This shows how nodes can signal recompilation needs.
    """

    def __init__(self, graph: RecompilationAwareGraph):
        self.graph = graph
        self.local_tool_routes: dict[str, str] = {}

    def add_tool_dynamically(self, tool_name: str, route: str) -> None:
        """Add a tool and update graph's tool routes.

        This will trigger recompilation if needed.
        """
        self.local_tool_routes[tool_name] = route
        self.graph.add_tool_route(tool_name, route)

    def __call__(self, state: dict[str, Any]) -> dict[str, Any] | Any:
        """Process state and handle tool routing.

        Can dynamically add tools based on state.
        """
        # Check if state contains new tool definitions
        if "dynamic_tools" in state:
            for tool_def in state["dynamic_tools"]:
                self.add_tool_dynamically(tool_def["name"], tool_def["route"])

        # Check if state requests tool route updates
        if "update_tool_routes" in state:
            self.graph.update_tool_routes(state["update_tool_routes"])

        # Normal validation logic here
        return state


# ============================================================================
# USAGE PATTERN FOR AGENTS
# ============================================================================


class DynamicToolAgent:
    """Agent that can add tools dynamically and trigger graph recompilation."""

    def __init__(self, name: str, graph: RecompilationAwareGraph):
        self.name = name
        self.graph = graph
        self.tools = {}

        # Register for recompilation events
        self.graph.register_recompile_callback(self._handle_recompile_event)

    def _handle_recompile_event(self, reason: str, details: dict[str, Any]) -> None:
        """Handle recompilation events from the graph."""
        logger.info(f"Agent {self.name} notified of recompilation: {reason}")
        if reason == "tool_routes_changed":
            # Update internal tool routing based on graph changes
            self._update_internal_routes(details["new_routes"])

    def _update_internal_routes(self, new_routes: dict[str, str]) -> None:
        """Update agent's internal routing based on graph routes."""
        # Agent-specific logic to handle route updates

    def add_tool(self, tool_name: str, tool_func: Callable, route: str) -> None:
        """Add a tool to the agent and update graph routes.

        This will trigger recompilation if the route is new or changed.
        """
        self.tools[tool_name] = tool_func
        self.graph.add_tool_route(tool_name, f"{self.name}.{route}")

    def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        """Execute agent logic."""
        # Check if recompilation is needed before execution
        if self.graph.needs_recompile():
            logger.warning(
                f"Agent {self.name} executing but graph needs recompilation!"
            )
            # In production, this might trigger automatic recompilation

        # Normal agent execution
        return {"agent": self.name, "executed": True}


# ============================================================================
# DEMONSTRATION
# ============================================================================


def demonstrate_recompilation_hooks():
    """Demonstrate the recompilation hook system."""
    # Create recompilation-aware graph
    graph = RecompilationAwareGraph("demo_graph")

    # Create validation node
    validation_node = ToolRouteAwareValidationNode(graph)

    # Create agents
    agent1 = DynamicToolAgent("agent1", graph)
    agent2 = DynamicToolAgent("agent2", graph)

    # Initial state

    # Mark as compiled
    graph.mark_compiled()

    # Add a tool to agent1
    agent1.add_tool("calculator", lambda x: x, "calc_route")

    # Add multiple tools
    agent2.add_tool("search", lambda q: f"results for {q}", "search_route")
    agent1.add_tool("analyzer", lambda d: {"analysis": d}, "analyze_route")

    # Get compilation info
    info = graph.get_compilation_info()
    for _key, _value in info.items():
        pass

    # Simulate recompilation
    graph.mark_compiled()

    # Dynamic tool addition through state
    state = {
        "dynamic_tools": [
            {"name": "formatter", "route": "format_route"},
            {"name": "validator", "route": "validate_route"},
        ]
    }
    validation_node(state)


# ============================================================================
# KEY PATTERNS
# ============================================================================

"""
Key Patterns for Dynamic Tool Routing with Recompilation:

1. **Hash-Based Change Detection**:
   - Compute hash of tool routes configuration
   - Compare with last compiled hash to detect changes
   - Trigger recompilation only when actually needed

2. **Callback-Based Notifications**:
   - Nodes and agents register callbacks for recompilation events
   - Graph notifies all observers when routes change
   - Enables coordinated updates across the system

3. **State-Driven Tool Addition**:
   - Tools can be added through state updates
   - Validation nodes detect and process tool additions
   - Graph automatically tracks route changes

4. **Lazy Recompilation**:
   - Mark recompilation needed but don't force immediate recompile
   - Allow batching of multiple changes
   - Recompile only when actually executing

5. **Agent-Graph Integration**:
   - Agents update graph's tool routes when adding tools
   - Graph notifies agents when routes change
   - Bidirectional communication ensures consistency
"""

if __name__ == "__main__":
    demonstrate_recompilation_hooks()
