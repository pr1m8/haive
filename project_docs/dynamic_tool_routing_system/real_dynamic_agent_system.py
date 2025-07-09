"""
Real Dynamic Multi-Agent System with Tool Routing and Recompilation.

This example uses actual Haive agents (SimpleAgent, ReactAgent) to demonstrate
dynamic tool routing and recompilation signaling.
"""

from typing import List, Literal, Union, Dict, Any, Optional, Set
from pydantic import BaseModel, Field, computed_field
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, Send
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
import operator
from typing import Annotated
import logging
from datetime import datetime

# Real Haive imports
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent
from haive.agents.base.agent import Agent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.common.mixins.tool_route_mixin import ToolRouteMixin

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# ============================================================================
# TOOLS
# ============================================================================

@tool
def calculate(expression: str) -> float:
    """Calculate a mathematical expression."""
    try:
        # Safe eval with limited scope
        allowed_names = {
            k: v for k, v in math.__dict__.items() if not k.startswith("_")
        }
        allowed_names.update({"abs": abs, "round": round})
        return eval(expression, {"__builtins__": {}}, allowed_names)
    except:
        return 0.0

@tool  
def search(query: str) -> str:
    """Search for information."""
    return f"Search results for '{query}': Found 10 relevant documents about {query}"

@tool
def analyze(data: str) -> Dict[str, Any]:
    """Analyze data and return insights."""
    return {
        "insight": f"Analysis of '{data}'", 
        "confidence": 0.85,
        "key_points": ["Point 1", "Point 2", "Point 3"]
    }

@tool
def summarize(text: str, max_length: int = 100) -> str:
    """Summarize text to specified length."""
    return f"Summary (max {max_length} chars): {text[:max_length]}..."

# ============================================================================
# EXTENDED AGENT WITH RECOMPILATION TRACKING
# ============================================================================

class RecompilableAgent:
    """
    Mixin that adds recompilation tracking to agents.
    """
    
    def __init__(self, base_agent: Agent):
        self.base_agent = base_agent
        self._tool_route_hash: Optional[str] = None
        self._last_recompiled: Optional[datetime] = None
        self._pending_tool_additions: List[Dict[str, Any]] = []
        self._setup_recompilation_tracking()
    
    def __getattr__(self, name):
        """Delegate to base agent."""
        return getattr(self.base_agent, name)
        
    def _setup_recompilation_tracking(self):
        """Setup recompilation tracking for the agent."""
        if hasattr(self.base_agent.engine, 'tool_routes'):
            # Compute initial hash
            self._tool_route_hash = self._compute_tool_route_hash()
            
    def _compute_tool_route_hash(self) -> str:
        """Compute hash of current tool routes."""
        import hashlib
        if hasattr(self.base_agent.engine, 'tool_routes'):
            route_str = str(sorted(self.base_agent.engine.tool_routes.items()))
            return hashlib.md5(route_str.encode()).hexdigest()
        return ""
    
    def needs_recompilation(self) -> bool:
        """Check if agent's graph needs recompilation."""
        current_hash = self._compute_tool_route_hash()
        needs_recompile = current_hash != self._tool_route_hash
        
        if needs_recompile:
            logger.info(f"Agent {self.base_agent.name} needs recompilation - tool routes changed")
            
        return needs_recompile
    
    def add_tool_dynamically(self, tool_func: Any, route: str = None) -> None:
        """Add a tool dynamically to the agent."""
        logger.debug(f"Adding tool {tool_func.name} to agent {self.base_agent.name}")
        
        # Check current tool routes
        if hasattr(self.base_agent.engine, 'tool_routes'):
            logger.debug(f"Current tool routes: {self.base_agent.engine.tool_routes}")
        
        if hasattr(self.base_agent.engine, 'add_tool'):
            # Add to engine
            self.base_agent.engine.add_tool(tool_func, route)
            logger.info(f"Added tool {tool_func.name} to agent {self.base_agent.name}")
            
            # Check updated tool routes
            if hasattr(self.base_agent.engine, 'tool_routes'):
                logger.debug(f"Updated tool routes: {self.base_agent.engine.tool_routes}")
            
            # Mark for recompilation
            self._pending_tool_additions.append({
                "tool": tool_func,
                "route": route,
                "added_at": datetime.now()
            })
        else:
            logger.warning(f"Engine for agent {self.base_agent.name} does not support add_tool")
    
    def recompile_if_needed(self) -> bool:
        """Recompile the agent's graph if needed."""
        if self.needs_recompilation():
            logger.info(f"Recompiling agent {self.base_agent.name}")
            
            # Debug: Show what's about to be recompiled
            logger.debug(f"Agent {self.base_agent.name} pending additions: {self._pending_tool_additions}")
            
            # Check if agent has graph and build_graph method
            if hasattr(self.base_agent, 'build_graph'):
                logger.debug(f"Rebuilding graph for agent {self.base_agent.name}")
                
                # Rebuild the graph - this should include new tool nodes
                self.base_agent.graph = self.base_agent.build_graph()
                
                # Debug: Show graph structure after rebuild
                if hasattr(self.base_agent.graph, 'nodes'):
                    logger.debug(f"Graph nodes after rebuild: {list(self.base_agent.graph.nodes.keys())}")
                
                logger.info(f"Successfully recompiled agent {self.base_agent.name}")
            else:
                logger.warning(f"Agent {self.base_agent.name} doesn't have build_graph method")
            
            # Update tracking
            self._tool_route_hash = self._compute_tool_route_hash()
            self._last_recompiled = datetime.now()
            self._pending_tool_additions.clear()
            
            return True
        return False

# ============================================================================
# MULTI-AGENT STATE
# ============================================================================

class DynamicMultiAgentState(BaseModel):
    """State for multi-agent system with dynamic tool routing."""
    
    # Messages
    messages: Annotated[List[BaseMessage], operator.add] = Field(
        default_factory=list,
        description="Conversation messages"
    )
    
    # Agent management
    agents: Dict[str, Any] = Field(
        default_factory=dict,
        description="Available agents keyed by name"
    )
    selected_agent_names: Annotated[List[str], operator.add] = Field(
        default_factory=list,
        description="History of selected agents"
    )
    
    # Tool routing
    global_tool_routes: Dict[str, str] = Field(
        default_factory=dict,
        description="Global tool name to agent.route mapping"
    )
    pending_tool_additions: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Tools waiting to be added"
    )
    
    # Execution tracking
    execution_results: Dict[str, Any] = Field(
        default_factory=dict,
        description="Results from agent executions"
    )
    
    # Recompilation tracking
    agents_needing_recompile: Set[str] = Field(
        default_factory=set,
        description="Agent names that need recompilation"
    )
    recompilation_count: int = Field(
        default=0,
        description="Number of recompilations performed"
    )
    
    @computed_field
    @property
    def current_agent_name(self) -> Optional[str]:
        """Get the most recently selected agent name."""
        return self.selected_agent_names[-1] if self.selected_agent_names else None
    
    @computed_field
    @property
    def current_agent(self) -> Optional[Any]:
        """Get the current agent instance."""
        if self.current_agent_name:
            return self.agents.get(self.current_agent_name)
        return None
    
    @computed_field
    @property
    def all_available_tools(self) -> List[str]:
        """Get all available tool names across all agents."""
        tools = set()
        for agent in self.agents.values():
            if hasattr(agent.engine, 'tool_routes'):
                tools.update(agent.engine.tool_routes.keys())
        return sorted(list(tools))

# ============================================================================
# DYNAMIC ROUTING NODES
# ============================================================================

def agent_router(state: DynamicMultiAgentState) -> Union[Send, List[Send], Command]:
    """
    Route to appropriate agent(s) based on state.
    
    Uses Send for dynamic routing without compile-time literals.
    """
    # Check if we need to handle tool additions first
    if state.pending_tool_additions:
        logger.info("Routing to tool_manager for pending additions")
        return Send("tool_manager", state)
    
    # Check if any agents need recompilation
    if state.agents_needing_recompile:
        logger.info(f"Routing to recompilation_manager for agents: {state.agents_needing_recompile}")
        return Send("recompilation_manager", state)
    
    # Route to current agent if selected
    if state.current_agent_name and state.current_agent_name in state.agents:
        logger.info(f"Routing to agent_executor for {state.current_agent_name}")
        return Send("agent_executor", {
            "agent_name": state.current_agent_name,
            "state": state
        })
    
    # If no agent selected but we have messages, select based on content
    if state.messages and state.agents:
        # Simple heuristic: use ReactAgent for tool-heavy tasks, SimpleAgent otherwise
        last_message = state.messages[-1].content if state.messages else ""
        
        if any(word in last_message.lower() for word in ["calculate", "search", "analyze"]):
            agent_name = "react_agent" if "react_agent" in state.agents else list(state.agents.keys())[0]
        else:
            agent_name = "simple_agent" if "simple_agent" in state.agents else list(state.agents.keys())[0]
            
        logger.info(f"Auto-selecting agent: {agent_name}")
        return Command(
            update={"selected_agent_names": [agent_name]},
            goto="agent_router"
        )
    
    # Default: go to end
    return Command(goto=END)

def tool_manager(arg: Union[DynamicMultiAgentState, Dict[str, Any]]) -> Command:
    """
    Manage dynamic tool additions.
    
    Adds tools to agents and marks them for recompilation.
    """
    state = arg if isinstance(arg, DynamicMultiAgentState) else arg.get("state")
    
    logger.debug(f"Tool manager processing {len(state.pending_tool_additions)} pending additions")
    
    updates = {}
    agents_to_recompile = set()
    added_tools = []
    
    # Process pending tool additions
    for addition in state.pending_tool_additions:
        agent_name = addition["agent_name"]
        tool_func = addition["tool"]
        route = addition.get("route", "tool_node")
        
        logger.debug(f"Processing tool addition: {tool_func.name} -> {agent_name} with route {route}")
        
        if agent_name in state.agents:
            agent = state.agents[agent_name]
            
            # Debug: Show agent type and current state
            logger.debug(f"Agent {agent_name} type: {type(agent)}")
            base_agent = agent.base_agent if hasattr(agent, 'base_agent') else agent
            
            # Show current tools before addition
            if hasattr(base_agent.engine, 'tool_routes'):
                logger.debug(f"Agent {agent_name} current tools: {list(base_agent.engine.tool_routes.keys())}")
            
            # Add tool to agent if it's a RecompilableAgent
            if isinstance(agent, RecompilableAgent):
                agent.add_tool_dynamically(tool_func, route)
            elif hasattr(base_agent.engine, 'add_tool'):
                base_agent.engine.add_tool(tool_func, route)
                logger.info(f"Added tool {tool_func.name} directly to engine")
                
            agents_to_recompile.add(agent_name)
            
            # Update global tool routes
            tool_name = tool_func.name if hasattr(tool_func, 'name') else tool_func.__name__
            state.global_tool_routes[tool_name] = f"{agent_name}.{route}"
            added_tools.append(tool_name)
            
            logger.info(f"Added tool {tool_name} to agent {agent_name} with route {route}")
            
            # Debug: Show tools after addition
            if hasattr(base_agent.engine, 'tool_routes'):
                logger.debug(f"Agent {agent_name} tools after addition: {list(base_agent.engine.tool_routes.keys())}")
        else:
            logger.warning(f"Agent {agent_name} not found in state.agents")
    
    # Prepare updates
    updates["pending_tool_additions"] = []
    updates["agents_needing_recompile"] = list(agents_to_recompile)
    updates["messages"] = [
        AIMessage(content=f"Successfully added tools: {', '.join(added_tools)} to agents")
    ]
    
    logger.debug(f"Tool manager completed. Agents needing recompile: {agents_to_recompile}")
    
    # Route to recompilation manager
    return Command(
        update=updates,
        goto="recompilation_manager"
    )

def recompilation_manager(arg: Union[DynamicMultiAgentState, Dict[str, Any]]) -> Command:
    """
    Handle agent recompilation when tool routes change.
    """
    state = arg if isinstance(arg, DynamicMultiAgentState) else arg.get("state")
    
    logger.debug(f"Recompilation manager handling {len(state.agents_needing_recompile)} agents")
    
    recompiled = []
    failed = []
    
    for agent_name in state.agents_needing_recompile:
        logger.debug(f"Recompiling agent: {agent_name}")
        
        if agent_name in state.agents:
            agent = state.agents[agent_name]
            
            try:
                if isinstance(agent, RecompilableAgent):
                    logger.debug(f"Using RecompilableAgent.recompile_if_needed() for {agent_name}")
                    if agent.recompile_if_needed():
                        recompiled.append(agent_name)
                else:
                    # For regular agents, rebuild their graph
                    logger.debug(f"Manual recompilation for non-RecompilableAgent {agent_name}")
                    base_agent = agent.base_agent if hasattr(agent, 'base_agent') else agent
                    
                    # Show current graph structure before rebuild
                    if hasattr(base_agent, 'graph') and hasattr(base_agent.graph, 'nodes'):
                        logger.debug(f"Agent {agent_name} current graph nodes: {list(base_agent.graph.nodes.keys())}")
                    
                    base_agent.graph = base_agent.build_graph()
                    
                    # Show new graph structure after rebuild
                    if hasattr(base_agent, 'graph') and hasattr(base_agent.graph, 'nodes'):
                        logger.debug(f"Agent {agent_name} new graph nodes: {list(base_agent.graph.nodes.keys())}")
                    
                    recompiled.append(agent_name)
                    
            except Exception as e:
                logger.error(f"Failed to recompile agent {agent_name}: {e}")
                failed.append(agent_name)
        else:
            logger.warning(f"Agent {agent_name} not found in state.agents")
    
    updates = {
        "agents_needing_recompile": set(),
        "recompilation_count": state.recompilation_count + len(recompiled),
        "messages": [
            AIMessage(
                content=f"Recompilation complete. Success: {', '.join(recompiled)}. "
                f"Failed: {', '.join(failed) if failed else 'None'}"
            )
        ]
    }
    
    logger.debug(f"Recompilation manager completed. Recompiled: {recompiled}, Failed: {failed}")
    
    # Continue to agent execution
    return Command(
        update=updates,
        goto="agent_router"
    )

def agent_executor(arg: Dict[str, Any]) -> Command:
    """
    Execute a specific agent.
    
    Receives custom args from Send with agent_name and state.
    """
    agent_name = arg.get("agent_name")
    state = arg.get("state")
    
    if not isinstance(state, DynamicMultiAgentState):
        return Command(
            update={"messages": [AIMessage(content="Invalid state")]},
            goto=END
        )
    
    if agent_name not in state.agents:
        return Command(
            update={"messages": [AIMessage(content=f"Agent {agent_name} not found")]},
            goto=END
        )
    
    agent = state.agents[agent_name]
    
    try:
        # Get the last human message
        human_messages = [m for m in state.messages if isinstance(m, HumanMessage)]
        if not human_messages:
            return Command(
                update={"messages": [AIMessage(content="No input to process")]},
                goto=END
            )
        
        last_input = human_messages[-1].content
        
        # Create runnable and execute
        runnable = agent.create_runnable()
        
        # Execute based on agent type
        if hasattr(agent, 'arun'):
            import asyncio
            result = asyncio.run(agent.arun(last_input))
        else:
            result = runnable.invoke({"messages": [HumanMessage(content=last_input)]})
        
        # Extract response
        if isinstance(result, dict) and "messages" in result:
            response_messages = result["messages"]
        elif isinstance(result, str):
            response_messages = [AIMessage(content=result)]
        else:
            response_messages = [AIMessage(content=str(result))]
        
        updates = {
            "messages": response_messages,
            "execution_results": {
                agent_name: {
                    "timestamp": datetime.now().isoformat(),
                    "input": last_input,
                    "success": True
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Error executing agent {agent_name}: {e}")
        updates = {
            "messages": [AIMessage(content=f"Error executing {agent_name}: {str(e)}")],
            "execution_results": {
                agent_name: {
                    "timestamp": datetime.now().isoformat(),
                    "success": False,
                    "error": str(e)
                }
            }
        }
    
    return Command(update=updates, goto=END)

# ============================================================================
# GRAPH CONSTRUCTION
# ============================================================================

def build_dynamic_multi_agent_graph() -> StateGraph:
    """
    Build a graph that supports dynamic agent and tool management.
    """
    graph = StateGraph(DynamicMultiAgentState)
    
    # Add nodes
    graph.add_node("agent_router", agent_router)
    graph.add_node("tool_manager", tool_manager)
    graph.add_node("recompilation_manager", recompilation_manager)
    graph.add_node("agent_executor", agent_executor)
    
    # Single entry point - the router handles all decisions
    graph.add_edge(START, "agent_router")
    
    return graph

# ============================================================================
# DEMONSTRATION
# ============================================================================

def demonstrate_real_dynamic_agents():
    """
    Demonstrate dynamic tool routing with real Haive agents.
    """
    print("=== Real Dynamic Multi-Agent System Demo ===\n")
    
    # Create engines with initial tools
    simple_engine = AugLLMConfig(
        tools=[calculate],
        system_message="You are a helpful assistant that can calculate expressions."
    )
    
    react_engine = AugLLMConfig(
        tools=[search, analyze],
        system_message="You are a research assistant that can search and analyze information."
    )
    
    # Create real agents
    simple_agent = SimpleAgent(name="simple_agent", engine=simple_engine)
    react_agent = ReactAgent(name="react_agent", engine=react_engine)
    
    # Make them recompilable
    recompilable_simple = RecompilableAgent(simple_agent)
    recompilable_react = RecompilableAgent(react_agent)
    
    # Create initial state
    initial_state = DynamicMultiAgentState(
        agents={
            "simple_agent": recompilable_simple,
            "react_agent": recompilable_react
        },
        messages=[HumanMessage(content="Hello! What can you do?")]
    )
    
    # Build and compile graph
    graph = build_dynamic_multi_agent_graph()
    app = graph.compile()
    
    print("1. Initial agent configuration:")
    for name, agent in initial_state.agents.items():
        tools = []
        base_agent = agent.base_agent if hasattr(agent, 'base_agent') else agent
        if hasattr(base_agent.engine, 'tool_routes'):
            tools = list(base_agent.engine.tool_routes.keys())
        print(f"   - {name}: {tools}")
    
    # Run with initial configuration
    print("\n2. First run - auto-select agent...")
    result1 = app.invoke(initial_state)
    print(f"   Selected: {result1.get('selected_agent_names', [])}")
    print(f"   Response: {result1['messages'][-1].content if result1['messages'] else 'No response'}")
    
    # Add a tool dynamically to simple_agent
    print("\n3. Adding 'summarize' tool to simple_agent...")
    initial_state.pending_tool_additions = [{
        "agent_name": "simple_agent",
        "tool": summarize,
        "route": "tool_node"
    }]
    initial_state.messages.append(HumanMessage(content="Can you summarize this text: 'Dynamic tool routing is a powerful feature.'"))
    
    result2 = app.invoke(initial_state)
    print(f"   Recompilations: {result2['recompilation_count']}")
    print(f"   Response: {result2['messages'][-1].content if result2['messages'] else 'No response'}")
    
    # Add multiple tools to different agents
    print("\n4. Adding multiple tools to different agents...")
    initial_state.pending_tool_additions = [
        {
            "agent_name": "simple_agent",
            "tool": search,
            "route": "tool_node"
        },
        {
            "agent_name": "react_agent", 
            "tool": calculate,
            "route": "tool_node"
        }
    ]
    initial_state.messages.append(HumanMessage(content="Search for information about dynamic graphs and calculate 2+2"))
    initial_state.selected_agent_names = ["react_agent"]  # Explicitly select react agent
    
    result3 = app.invoke(initial_state)
    print(f"   Total recompilations: {result3['recompilation_count']}")
    print(f"   Global tool routes: {result3['global_tool_routes']}")
    
    # Show final tool configuration
    print("\n5. Final agent configuration:")
    for name, agent in result3['agents'].items():
        tools = []
        base_agent = agent.base_agent if hasattr(agent, 'base_agent') else agent
        if hasattr(base_agent.engine, 'tool_routes'):
            tools = list(base_agent.engine.tool_routes.keys())
        print(f"   - {name}: {tools}")

if __name__ == "__main__":
    import math  # For calculate tool
    demonstrate_real_dynamic_agents()