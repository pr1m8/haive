# Dynamic Tool Routing Architecture for Meta-Agent Systems

## Overview

This document describes a comprehensive system for dynamic tool routing in multi-agent environments, specifically designed for meta-agent implementations that need to add tools and modify routing at runtime without full graph recompilation.

## Core Problem Solved

**Challenge**: How to add tools dynamically to agents and route tool calls to the appropriate handlers without:

1. Requiring compile-time `Literal` type specifications
2. Full graph recompilation for every tool addition
3. Hardcoded routing paths in the graph structure

**Solution**: A dynamic routing system using LangGraph's `Send` and `Command` primitives with hash-based recompilation detection.

## Architecture Components

### 1. Dynamic Routing with Send/Command

#### Traditional Approach (Problematic)

```python
def router(state) -> Literal["node1", "node2", "node3"]:
    # Requires knowing all possible destinations at compile time
    return "node1"
```

#### Dynamic Approach (Our Solution)

```python
def agent_router(state) -> Union[Send, Command, List[Send]]:
    # Runtime decision making
    if state.pending_tool_additions:
        return Send("tool_manager", state)

    # Dynamic agent selection
    agent_name = select_agent_based_on_context(state)
    return Send("agent_executor", {
        "agent_name": agent_name,
        "state": state
    })
```

**Key Benefits**:

- No compile-time literals needed
- Can route to any node dynamically
- Supports parallel execution with `List[Send]`
- Custom payloads via `Send(node_name, custom_data)`

### 2. Recompilation Detection System

#### Hash-Based Change Detection

```python
def _compute_tool_route_hash(self) -> str:
    """Compute hash of current tool routes."""
    route_str = str(sorted(self.tool_routes.items()))
    return hashlib.md5(route_str.encode()).hexdigest()

def needs_recompilation(self) -> bool:
    """Check if recompilation needed."""
    current_hash = self._compute_tool_route_hash()
    return current_hash != self._tool_route_hash
```

#### Recompilation Triggers

- Tool route additions/removals
- Agent configuration changes
- Graph structure modifications
- State schema updates

### 3. Tool Route Management

#### Engine-Level Tool Addition

```python
# Tools are added to the engine
engine.add_tool(new_tool, route="tool_node")

# Tool routes are tracked
engine.tool_routes = {
    "calculate": "langchain_tool",
    "search": "langchain_tool",
    "new_tool": "tool_node"
}
```

#### Graph-Level Route Tracking

```python
# Graph maintains global view of tool routes
graph.tool_routes = {
    "calculate": "agent1.tool_node",
    "search": "agent2.tool_node",
    "analyze": "agent1.validation_node"
}
```

### 4. Multi-Agent State Management

#### Centralized State

```python
class DynamicMultiAgentState(BaseModel):
    # Agent management
    agents: Dict[str, Any] = Field(default_factory=dict)
    selected_agent_names: List[str] = Field(default_factory=list)

    # Tool routing
    global_tool_routes: Dict[str, str] = Field(default_factory=dict)
    pending_tool_additions: List[Dict[str, Any]] = Field(default_factory=list)

    # Recompilation tracking
    agents_needing_recompile: Set[str] = Field(default_factory=set)
    recompilation_count: int = Field(default=0)
```

#### Dynamic Agent Selection

```python
@computed_field
def current_agent_name(self) -> Optional[str]:
    """Get most recently selected agent."""
    return self.selected_agent_names[-1] if self.selected_agent_names else None
```

### 5. Node Flow Architecture

#### Core Flow Pattern

```
START → agent_router → [tool_manager] → [recompilation_manager] → agent_executor → END
```

#### Node Responsibilities

1. **agent_router**: Dynamic routing decision maker
   - Checks for pending tool additions
   - Routes to appropriate managers or executors
   - Uses `Send` for dynamic routing

2. **tool_manager**: Tool addition processor
   - Processes pending tool additions
   - Updates agent engines with new tools
   - Marks agents for recompilation

3. **recompilation_manager**: Recompilation handler
   - Checks which agents need recompilation
   - Rebuilds agent graphs when needed
   - Tracks recompilation statistics

4. **agent_executor**: Agent execution handler
   - Receives custom payloads via `Send`
   - Executes specific agents with context
   - Handles agent-specific error cases

## Implementation Patterns

### 1. Recompilable Agent Wrapper

```python
class RecompilableAgent:
    def __init__(self, base_agent: Agent):
        self.base_agent = base_agent
        self._tool_route_hash = self._compute_tool_route_hash()

    def add_tool_dynamically(self, tool_func, route=None):
        """Add tool and mark for recompilation."""
        self.base_agent.engine.add_tool(tool_func, route)
        # Hash automatically detects change

    def needs_recompilation(self) -> bool:
        """Check if graph needs rebuilding."""
        return self._compute_tool_route_hash() != self._tool_route_hash
```

### 2. Dynamic Node Configuration

```python
class DynamicToolNode:
    def __init__(self, graph: BaseGraph):
        self.graph = graph

    def __call__(self, state) -> Union[Send, Command]:
        """Handle dynamic tool routing."""
        if "tool_call" in state:
            tool_name = state["tool_call"]["name"]
            route = self.graph.tool_routes.get(tool_name)

            if route:
                return Send(route, {
                    "tool_name": tool_name,
                    "args": state["tool_call"]["args"],
                    "state": state
                })
```

### 3. Batch Tool Operations

```python
def batch_add_tools(self, tool_additions: List[Dict]):
    """Add multiple tools efficiently."""
    for addition in tool_additions:
        agent = self.agents[addition["agent_name"]]
        agent.add_tool_dynamically(addition["tool"], addition["route"])

    # Single recompilation check after all additions
    if any(agent.needs_recompilation() for agent in self.agents.values()):
        self.recompile_all_needed()
```

## Key Insights for Meta-Agent Implementation

### 1. Graph Structure Stability

- **Agent graphs don't change structure** when tools are added
- SimpleAgent always has: `agent_node → validation → tool_node`
- Tools are handled by existing nodes, not new nodes

### 2. Validation Node V2 Integration

- **Current Issue**: SimpleAgent uses `placeholder_node` instead of `ValidationNodeConfigV2`
- **Solution Needed**: Proper V2 validation node with computed fields for tool messages
- **Impact**: Dynamic tool routing depends on validation node having access to updated tool routes

### 3. State-Driven Routing

- **Key Pattern**: State contains routing information, not graph structure
- **Benefits**:
  - Routing decisions made at runtime
  - No compile-time dependencies
  - Easy to modify routing logic

### 4. Recompilation Optimization

- **Hash-based detection** prevents unnecessary recompilations
- **Batch operations** reduce recompilation frequency
- **Lazy recompilation** delays until actually needed

## Recommendations for Meta-Agent

### 1. Tool Route State Management

```python
class MetaAgentState(BaseModel):
    # Central tool route registry
    tool_routes: Dict[str, str] = Field(default_factory=dict)

    # Dynamic tool additions
    @computed_field
    def available_tools(self) -> List[str]:
        """Get all available tools across agents."""
        return list(self.tool_routes.keys())
```

### 2. Agent Factory Pattern

```python
class AgentFactory:
    def create_agent_with_tools(self, agent_type: str, tools: List[Any]) -> Agent:
        """Create agent with initial tools."""
        # Create base agent
        # Add tools dynamically
        # Return recompilable wrapper
```

### 3. Dynamic Command System

```python
def meta_agent_router(state: MetaAgentState) -> Command:
    """Route based on current system state."""

    # Check system conditions
    if state.needs_tool_management:
        return Command(goto="tool_management_flow")

    if state.needs_agent_creation:
        return Command(goto="agent_creation_flow")

    # Dynamic agent selection
    selected_agent = self.select_best_agent(state)
    return Command(
        update={"selected_agent": selected_agent},
        goto="agent_execution_flow"
    )
```

### 4. Event-Driven Architecture

```python
class ToolAdditionEvent:
    agent_name: str
    tool: Any
    route: str
    timestamp: datetime

class MetaAgentEventHandler:
    def handle_tool_addition(self, event: ToolAdditionEvent):
        # Add tool to agent
        # Update global routes
        # Signal recompilation if needed
```

## Implementation Roadmap

### Phase 1: Core Dynamic Routing

1. Implement `Send`/`Command` based routing
2. Create recompilation detection system
3. Build tool route management

### Phase 2: V2 Node Integration

1. Fix validation node to use `ValidationNodeConfigV2`
2. Implement computed fields for tool messages
3. Test dynamic tool routing through validation

### Phase 3: Meta-Agent Integration

1. Adapt patterns for meta-agent use case
2. Implement agent factory patterns
3. Add event-driven tool management

### Phase 4: Optimization

1. Batch operations for performance
2. Lazy recompilation strategies
3. Monitoring and debugging tools

## Conclusion

This architecture provides a robust foundation for dynamic tool routing in meta-agent systems. The key innovations are:

1. **Dynamic routing** without compile-time constraints
2. **Efficient recompilation** based on actual changes
3. **State-driven architecture** for maximum flexibility
4. **Extensible patterns** for complex meta-agent scenarios

The system is designed to scale from simple tool additions to complex multi-agent orchestration while maintaining performance and reliability.
