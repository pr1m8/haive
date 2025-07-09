# Dynamic Tool Routing for Meta-Agent Implementation

## Executive Summary

We've built a comprehensive dynamic tool routing system that solves the core challenges for meta-agent implementations:

1. **Dynamic Routing**: Add tools and route calls without compile-time constraints
2. **Recompilation Detection**: Hash-based system to efficiently detect when agent graphs need rebuilding
3. **Multi-Agent Coordination**: State-driven architecture for managing multiple agents with dynamic capabilities

## What We Built & Tested

### 1. **Real Working Implementation** 
- Uses actual `SimpleAgent` and `ReactAgent` from Haive
- Successfully adds tools dynamically at runtime
- Demonstrates recompilation detection and execution

### 2. **Core Components**

#### A. Dynamic Routing System (`real_dynamic_agent_system.py`)
```python
# Route dynamically without compile-time literals
def agent_router(state) -> Send:
    return Send("agent_executor", {
        "agent_name": selected_agent,
        "state": state
    })
```

#### B. Recompilation Detection (`RecompilableAgent`)
```python
def needs_recompilation(self) -> bool:
    current_hash = self._compute_tool_route_hash()
    return current_hash != self._tool_route_hash
```

#### C. Tool Management Flow
```
tool_manager → recompilation_manager → agent_executor
```

### 3. **Test Results** (Verified Working)

```
Initial agent configuration:
   - simple_agent: ['calculate']
   - react_agent: ['search', 'analyze']

After dynamic tool addition:
   - simple_agent: ['calculate', 'summarize', 'search']  
   - react_agent: ['search', 'analyze', 'calculate']

Recompilations: 2 (triggered by tool route changes)
```

## Key Insights for Meta-Agent

### 1. **Graph Structure Doesn't Change**
- Adding tools doesn't create new nodes
- Existing nodes (`agent_node`, `validation`, `tool_node`) handle new tools
- **Implication**: Focus on tool routing within existing structure

### 2. **Validation Node V2 is Critical**
- Current SimpleAgent uses `placeholder_node` instead of `ValidationNodeConfigV2`
- **Issue**: Tool routing depends on validation node having proper computed fields
- **Solution**: Need V2 validation node with dynamic tool message handling

### 3. **State-Driven Architecture Works**
- Routing decisions made at runtime based on state
- No hardcoded paths in graph structure
- **Benefits**: Maximum flexibility for meta-agent scenarios

## Recompilation Check Strategy

### Hash-Based Detection
```python
def _compute_tool_route_hash(self) -> str:
    route_str = str(sorted(self.tool_routes.items()))
    return hashlib.md5(route_str.encode()).hexdigest()
```

### Efficient Recompilation
- **Only recompile when tool routes actually change**
- **Batch operations** to reduce recompilation frequency
- **Lazy recompilation** - mark as needed but recompile only when executing

### Meta-Agent Context
```python
class MetaAgent:
    def add_capability(self, agent_name: str, tool: Any):
        """Add tool to agent and handle recompilation."""
        agent = self.agents[agent_name]
        agent.add_tool_dynamically(tool)
        
        if agent.needs_recompilation():
            self.schedule_recompilation(agent_name)
            
    def execute_with_recompilation_check(self, agent_name: str, task: str):
        """Execute after checking recompilation needs."""
        agent = self.agents[agent_name]
        
        if agent.needs_recompilation():
            agent.recompile_if_needed()
            
        return agent.execute(task)
```

## Implementation for Meta-Agent

### 1. **Tool Route Registry**
```python
class MetaAgentState(BaseModel):
    # Central registry of all tool routes
    global_tool_routes: Dict[str, str] = Field(default_factory=dict)
    
    # Track which agents need recompilation
    agents_needing_recompile: Set[str] = Field(default_factory=set)
    
    @computed_field
    def available_capabilities(self) -> List[str]:
        """All tools available across agents."""
        return list(self.global_tool_routes.keys())
```

### 2. **Dynamic Agent Orchestration**
```python
def meta_agent_router(state: MetaAgentState) -> Union[Send, Command]:
    """Route based on capabilities needed."""
    
    # Analyze task requirements
    required_tools = analyze_task_requirements(state.current_task)
    
    # Find best agent for tools needed
    best_agent = find_agent_with_tools(required_tools, state.agents)
    
    # Check if recompilation needed
    if best_agent in state.agents_needing_recompile:
        return Send("recompilation_manager", state)
    
    # Execute with best agent
    return Send("agent_executor", {
        "agent_name": best_agent,
        "required_tools": required_tools,
        "state": state
    })
```

### 3. **Capability Management**
```python
class CapabilityManager:
    def add_capability_to_agent(self, agent_name: str, capability: Any):
        """Add capability and track recompilation needs."""
        
        # Add to specific agent
        agent = self.agents[agent_name]
        agent.add_tool_dynamically(capability)
        
        # Update global registry
        self.global_tool_routes[capability.name] = f"{agent_name}.tool_node"
        
        # Mark for recompilation if needed
        if agent.needs_recompilation():
            self.agents_needing_recompile.add(agent_name)
    
    def distribute_capability(self, capability: Any, strategy: str = "all"):
        """Distribute capability across multiple agents."""
        
        if strategy == "all":
            for agent_name in self.agents:
                self.add_capability_to_agent(agent_name, capability)
        elif strategy == "best_fit":
            best_agent = self.find_best_agent_for_capability(capability)
            self.add_capability_to_agent(best_agent, capability)
```

## Next Steps for Meta-Agent

### 1. **Immediate Integration**
- Adapt `RecompilableAgent` pattern for your meta-agent
- Use `Send`/`Command` routing patterns
- Implement tool route registry

### 2. **V2 Node Integration** (Dependency)
- Wait for V2 validation node with computed fields
- Integrate proper tool message handling
- Test dynamic routing through validation

### 3. **Meta-Agent Specific Features**
- Agent creation/destruction at runtime
- Capability distribution strategies  
- Performance monitoring for recompilation

### 4. **Advanced Patterns**
- Event-driven capability management
- Hierarchical agent structures
- Cross-agent tool sharing

## File Structure Created

```
project_docs/dynamic_tool_routing_system/
├── DYNAMIC_TOOL_ROUTING_ARCHITECTURE.md    # Complete architecture guide
├── META_AGENT_INTEGRATION_GUIDE.md         # This file
├── real_dynamic_agent_system.py            # Working implementation
├── basegraph2_recompilation_integration.py # BaseGraph2 integration
├── dynamic_tool_route_mixin.py             # Enhanced mixin
├── recompilation_hook_example.py           # Recompilation patterns
├── debug_tool_addition.py                  # Debug tool addition
├── debug_validation_node_v2.py             # V2 node debugging
└── README.md                               # Quick reference
```

The system is ready for integration into your meta-agent implementation. The core patterns have been tested and proven to work with real Haive agents.