# Dynamic Tool Routing with Recompilation POC

This directory contains a proof-of-concept implementation demonstrating how to add dynamic tool routing capabilities to Haive agents with automatic recompilation detection.

## Files Overview

### 1. `real_dynamic_agent_system.py`

**Real implementation using actual Haive agents**

- Uses `SimpleAgent` and `ReactAgent` from haive-agents
- Demonstrates `Send` and `Command` for dynamic routing without compile-time literals
- Shows how to add tools dynamically to agents
- Implements recompilation tracking for agent graphs

**Key Features:**

- `RecompilableAgent` class that extends base agents
- Dynamic tool addition with `add_tool_dynamically()`
- Hash-based change detection for tool routes
- Multi-agent coordination with dynamic routing

### 2. `basegraph2_recompilation_integration.py`

**Integration with BaseGraph2's recompilation system**

- Extends `BaseGraph2` with tool route tracking
- Demonstrates integration with existing recompilation infrastructure
- Shows how to create tool-route-aware nodes

**Key Features:**

- `ToolRouteAwareBaseGraph` class
- Tool route hash computation
- Dynamic node routing with `DynamicToolNode`
- Graph-integrated agents

### 3. `dynamic_tool_route_mixin.py`

**Extended mixin for dynamic tool routing**

- Extends `ToolRouteMixin` with change callbacks
- Provides observer pattern for tool route changes
- Supports batch updates and pending change tracking

**Key Features:**

- Change callbacks for tool route modifications
- Batch update operations
- Pending change tracking and notifications

### 4. `recompilation_hook_example.py`

**Recompilation hook system demonstration**

- Shows how to implement hash-based change detection
- Demonstrates callback-based recompilation notifications
- Provides patterns for lazy recompilation

## Key Concepts

### Dynamic Routing with Send/Command

Instead of using compile-time literals:

```python
# Traditional approach (requires literals)
def router(state) -> Literal["node1", "node2"]:
    return "node1"

# Dynamic approach (no literals needed)
def router(state) -> Union[Send, Command]:
    return Send("agent_executor", {"agent_name": "dynamic_agent"})
```

### Tool Route Management

```python
# Add tool dynamically
agent.add_tool_dynamically(new_tool, "custom_route")

# Graph automatically detects change and marks for recompilation
if graph.needs_recompile():
    graph.recompile()
```

### Recompilation Detection

```python
# Hash-based change detection
def _compute_tool_route_hash(self) -> str:
    route_str = str(sorted(self.tool_routes.items()))
    return hashlib.md5(route_str.encode()).hexdigest()

# Automatic recompilation check
def needs_recompilation(self) -> bool:
    current_hash = self._compute_tool_route_hash()
    return current_hash != self._tool_route_hash
```

## Usage Patterns

### 1. Dynamic Agent Selection

```python
def agent_router(state) -> Send:
    # Select agent based on runtime conditions
    agent_name = select_best_agent(state)
    return Send("agent_executor", {
        "agent_name": agent_name,
        "state": state
    })
```

### 2. Tool Addition with Recompilation

```python
# Add tool to agent
agent.add_tool_dynamically(new_tool, "tool_route")

# Check if recompilation needed
if agent.needs_recompilation():
    agent.recompile_if_needed()
```

### 3. Multi-Agent Coordination

```python
# Route to multiple agents in parallel
def multi_agent_router(state) -> List[Send]:
    return [
        Send("agent_1", {"task": "analyze"}),
        Send("agent_2", {"task": "search"}),
        Send("agent_3", {"task": "summarize"})
    ]
```

## Benefits

1. **No Compile-Time Literals**: Dynamic routing without `Literal` type constraints
2. **Automatic Recompilation**: Detects when graphs need rebuilding
3. **Efficient Updates**: Hash-based change detection prevents unnecessary recompilation
4. **Flexible Architecture**: Supports adding tools and agents at runtime
5. **Real Integration**: Uses actual Haive agents and BaseGraph2

## Running the Examples

```bash
# Run the main demonstration
python real_dynamic_agent_system.py

# Run BaseGraph2 integration example
python basegraph2_recompilation_integration.py

# Run recompilation hook example
python recompilation_hook_example.py
```

## Integration with Existing Code

To integrate this pattern into existing Haive code:

1. **Extend your agents** with `RecompilableAgent` pattern
2. **Use ToolRouteAwareBaseGraph** instead of regular BaseGraph
3. **Implement dynamic routing** with `Send` and `Command`
4. **Add recompilation checks** before agent execution

This approach allows you to add tools and modify routing dynamically while maintaining graph integrity and performance through intelligent recompilation detection.
