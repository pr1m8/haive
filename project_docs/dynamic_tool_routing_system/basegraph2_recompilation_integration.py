"""
BaseGraph2 Integration with Dynamic Tool Routing and Recompilation.

This demonstrates how to integrate dynamic tool routing with BaseGraph2's
recompilation tracking system.
"""

from typing import Dict, Any, Optional, List, Union, Set
from datetime import datetime
from pydantic import Field
import logging

from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.common.mixins.tool_route_mixin import ToolRouteMixin
from haive.agents.simple.agent import SimpleAgent
from haive.agents.react.agent import ReactAgent
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import tool
from langgraph.types import Send, Command

logger = logging.getLogger(__name__)

# ============================================================================
# EXTENDED BASEGRAPH WITH TOOL ROUTE TRACKING
# ============================================================================

class ToolRouteAwareBaseGraph(BaseGraph):
    """
    Extended BaseGraph that tracks tool route changes and triggers recompilation.
    """
    
    # Additional fields for tool route tracking
    tool_routes: Dict[str, str] = Field(
        default_factory=dict,
        description="Current tool routes in the graph"
    )
    _tool_route_hash: Optional[str] = Field(
        default=None, 
        exclude=True,
        description="Hash of tool routes at last compilation"
    )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._register_tool_route_observers()
    
    def _register_tool_route_observers(self):
        """Register observers for tool route changes in nodes."""
        # This would be called after nodes are added
        pass
    
    def update_tool_routes(self, new_routes: Dict[str, str]) -> None:
        """
        Update tool routes and check if recompilation is needed.
        
        Args:
            new_routes: New tool route mappings
        """
        old_routes = self.tool_routes.copy()
        self.tool_routes.update(new_routes)
        
        # Check if routes actually changed
        if old_routes != self.tool_routes:
            logger.info(f"Tool routes updated in graph '{self.name}'")
            self._mark_needs_recompile("Tool routes changed")
    
    def add_tool_route(self, tool_name: str, route: str) -> None:
        """Add or update a single tool route."""
        if tool_name not in self.tool_routes or self.tool_routes[tool_name] != route:
            self.tool_routes[tool_name] = route
            self._mark_needs_recompile(f"Tool route added/updated: {tool_name}")
    
    def remove_tool_route(self, tool_name: str) -> None:
        """Remove a tool route."""
        if tool_name in self.tool_routes:
            del self.tool_routes[tool_name]
            self._mark_needs_recompile(f"Tool route removed: {tool_name}")
    
    def _compute_state_hash(self) -> str:
        """Override to include tool routes in state hash."""
        # Get base hash from parent
        base_hash = super()._compute_state_hash()
        
        # Add tool routes to hash computation
        import hashlib
        tool_route_str = str(sorted(self.tool_routes.items()))
        combined = f"{base_hash}:{tool_route_str}"
        
        return hashlib.md5(combined.encode()).hexdigest()
    
    def mark_compiled(self) -> None:
        """Override to store tool route hash."""
        super().mark_compiled()
        self._tool_route_hash = self._compute_tool_route_hash()
    
    def _compute_tool_route_hash(self) -> str:
        """Compute hash of current tool routes."""
        import hashlib
        route_str = str(sorted(self.tool_routes.items()))
        return hashlib.md5(route_str.encode()).hexdigest()
    
    def get_compilation_info(self) -> Dict[str, Any]:
        """Override to include tool route information."""
        info = super().get_compilation_info()
        info.update({
            "tool_routes": self.tool_routes,
            "tool_route_count": len(self.tool_routes),
            "tool_route_hash": self._tool_route_hash
        })
        return info

# ============================================================================
# DYNAMIC NODE WITH TOOL ROUTE AWARENESS
# ============================================================================

class DynamicToolNode:
    """
    A node that can dynamically handle tool routing based on graph state.
    """
    
    def __init__(self, graph: ToolRouteAwareBaseGraph):
        self.graph = graph
        self.local_routes: Dict[str, str] = {}
    
    def __call__(self, state: Dict[str, Any]) -> Union[Dict[str, Any], Send, Command]:
        """
        Process state and handle dynamic tool routing.
        """
        # Check for tool route updates in state
        if "update_tool_routes" in state:
            new_routes = state["update_tool_routes"]
            self.graph.update_tool_routes(new_routes)
            
            # Signal recompilation if needed
            if self.graph.needs_recompile():
                logger.info("Tool routes changed - recompilation needed")
                return Command(
                    update={"needs_recompilation": True},
                    goto="recompilation_handler"
                )
        
        # Check for dynamic tool calls
        if "tool_call" in state:
            tool_name = state["tool_call"]["name"]
            
            # Look up route dynamically
            if tool_name in self.graph.tool_routes:
                route = self.graph.tool_routes[tool_name]
                
                # Use Send for dynamic routing to tool handler
                return Send(route, {
                    "tool_name": tool_name,
                    "args": state["tool_call"]["args"],
                    "state": state
                })
            else:
                return {"error": f"No route found for tool: {tool_name}"}
        
        return state

# ============================================================================
# AGENT WITH GRAPH INTEGRATION
# ============================================================================

class GraphIntegratedAgent(SimpleAgent):
    """
    Agent that integrates with ToolRouteAwareBaseGraph for dynamic updates.
    """
    
    def __init__(self, *args, graph: Optional[ToolRouteAwareBaseGraph] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.integrated_graph = graph
        
        # Register callback if graph provided
        if self.integrated_graph and hasattr(self.engine, 'add_tool'):
            self._register_tool_change_callback()
    
    def _register_tool_change_callback(self):
        """Register callback for tool changes."""
        # This would integrate with DynamicToolRouteMixin if used
        pass
    
    def add_tool_with_graph_update(self, tool_func: Any, route: str = "tool_node") -> None:
        """
        Add tool to agent and update graph's tool routes.
        """
        # Add to engine
        if hasattr(self.engine, 'add_tool'):
            self.engine.add_tool(tool_func, route)
            
            # Update graph if integrated
            if self.integrated_graph:
                tool_name = tool_func.name if hasattr(tool_func, 'name') else tool_func.__name__
                self.integrated_graph.add_tool_route(tool_name, f"{self.name}.{route}")
                
                logger.info(f"Added tool {tool_name} to agent {self.name} and updated graph")

# ============================================================================
# DEMONSTRATION WITH BASEGRAPH2
# ============================================================================

@tool
def web_search(query: str) -> str:
    """Search the web for information."""
    return f"Web results for: {query}"

@tool
def code_analyzer(code: str) -> Dict[str, Any]:
    """Analyze code and return insights."""
    return {
        "lines": len(code.split('\n')),
        "complexity": "medium",
        "suggestions": ["Add type hints", "Improve error handling"]
    }

def demonstrate_basegraph2_integration():
    """
    Demonstrate BaseGraph2 integration with dynamic tool routing.
    """
    print("=== BaseGraph2 Tool Route Integration Demo ===\n")
    
    # Create tool-route-aware graph
    graph = ToolRouteAwareBaseGraph(name="dynamic_tool_graph")
    
    # Create agents with initial tools
    simple_engine = AugLLMConfig(tools=[web_search])
    simple_agent = GraphIntegratedAgent(
        name="simple_agent",
        engine=simple_engine,
        graph=graph
    )
    
    # Add initial nodes to graph
    graph.add_node("start", lambda state: state)
    graph.add_node("tool_router", DynamicToolNode(graph))
    graph.add_node("agent_node", simple_agent.create_runnable())
    
    # Add edges
    graph.add_edge("start", "tool_router")
    graph.add_conditional_edges(
        "tool_router",
        lambda state: "agent_node" if "tool_call" not in state else "tool_handler",
        {
            "agent_node": "agent_node",
            "tool_handler": END  # Dynamic routing would handle this
        }
    )
    
    # Initial compilation state
    print("1. Initial state:")
    print(f"   Needs recompile: {graph.needs_recompile()}")
    print(f"   Tool routes: {graph.tool_routes}")
    
    # Mark as compiled
    graph.mark_compiled()
    print("\n2. After compilation:")
    info = graph.get_compilation_info()
    print(f"   Needs recompile: {info['needs_recompile']}")
    print(f"   Compiled at: {info['last_compiled_at']}")
    
    # Add tool dynamically
    print("\n3. Adding code_analyzer tool...")
    simple_agent.add_tool_with_graph_update(code_analyzer, "analysis_route")
    
    print(f"   Needs recompile: {graph.needs_recompile()}")
    print(f"   Tool routes: {graph.tool_routes}")
    
    # Demonstrate state-based tool route updates
    print("\n4. Updating tool routes via state...")
    state = {
        "update_tool_routes": {
            "web_search": "search_handler",
            "code_analyzer": "analyzer_handler"
        }
    }
    
    tool_router = graph.nodes["tool_router"]
    result = tool_router(state)
    
    print(f"   Result: {result}")
    print(f"   Graph needs recompile: {graph.needs_recompile()}")
    
    # Show final compilation info
    print("\n5. Final compilation info:")
    final_info = graph.get_compilation_info()
    for key, value in final_info.items():
        if key != "nodes":  # Skip nodes for brevity
            print(f"   {key}: {value}")

# ============================================================================
# ADVANCED PATTERN: MULTI-AGENT GRAPH WITH DYNAMIC TOOLS
# ============================================================================

def build_advanced_multi_agent_graph():
    """
    Build an advanced graph with multiple agents and dynamic tool routing.
    """
    # Create the graph
    graph = ToolRouteAwareBaseGraph(name="multi_agent_dynamic")
    
    # Create multiple agents
    agents = {}
    for i in range(3):
        engine = AugLLMConfig(tools=[], system_message=f"Agent {i}")
        agent = GraphIntegratedAgent(
            name=f"agent_{i}",
            engine=engine,
            graph=graph
        )
        agents[f"agent_{i}"] = agent
    
    # Dynamic agent selector using Send
    def agent_selector(state: Dict[str, Any]) -> Union[Send, Command]:
        """Select agent dynamically based on state."""
        # Check if specific agent requested
        if "target_agent" in state:
            agent_name = state["target_agent"]
            if agent_name in agents:
                return Send(f"{agent_name}_executor", state)
        
        # Check tool requirements
        if "required_tools" in state:
            required = set(state["required_tools"])
            
            # Find agent with most matching tools
            best_agent = None
            best_score = 0
            
            for name, agent in agents.items():
                if hasattr(agent.engine, 'tool_routes'):
                    agent_tools = set(agent.engine.tool_routes.keys())
                    score = len(required.intersection(agent_tools))
                    if score > best_score:
                        best_score = score
                        best_agent = name
            
            if best_agent:
                return Send(f"{best_agent}_executor", state)
        
        # Default to first agent
        return Send("agent_0_executor", state)
    
    # Add nodes
    graph.add_node("selector", agent_selector)
    
    # Add executor nodes for each agent
    for name, agent in agents.items():
        graph.add_node(f"{name}_executor", agent.create_runnable())
    
    # Set up flow
    graph.set_entry_point("selector")
    for name in agents:
        graph.add_edge(f"{name}_executor", END)
    
    return graph, agents

def demonstrate_advanced_pattern():
    """
    Demonstrate advanced multi-agent pattern with dynamic tools.
    """
    print("\n=== Advanced Multi-Agent Dynamic Tool Pattern ===\n")
    
    graph, agents = build_advanced_multi_agent_graph()
    
    # Add tools dynamically to different agents
    agents["agent_0"].add_tool_with_graph_update(web_search, "search_route")
    agents["agent_1"].add_tool_with_graph_update(code_analyzer, "analyze_route")
    
    print("1. Agent tool configuration:")
    for name, agent in agents.items():
        tools = []
        if hasattr(agent.engine, 'tool_routes'):
            tools = list(agent.engine.tool_routes.keys())
        print(f"   {name}: {tools}")
    
    print(f"\n2. Graph tool routes: {graph.tool_routes}")
    print(f"   Needs recompile: {graph.needs_recompile()}")
    
    # The graph would route to appropriate agents based on tool requirements
    print("\n3. Dynamic routing based on tool requirements:")
    print("   - State with web_search requirement -> routes to agent_0")
    print("   - State with code_analyzer requirement -> routes to agent_1")
    print("   - Send enables this without compile-time literals!")

if __name__ == "__main__":
    demonstrate_basegraph2_integration()
    demonstrate_advanced_pattern()