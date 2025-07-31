# Multi-Agent Architecture Guide - Haive Framework

**Document Version**: 1.0
**Purpose**: Comprehensive guide to Haive's multi-agent system architecture
**Last Updated**: 2025-01-23
**Status**: Complete Analysis

## 🎯 Overview

This guide documents the complete multi-agent architecture in the Haive framework, covering all discovered implementations, state schemas, and integration patterns. The architecture enables sophisticated agent coordination through hierarchical state management and dynamic recompilation.

## 🏗️ Architecture Hierarchy

### Core Components Stack

```
EnhancedMultiAgent V3 (Coordinator)
├── AgentNodeV3Config (Execution Engine)
├── Multi-Agent State Schemas (State Management)
│   ├── MultiAgentState (Full-featured)
│   ├── FlexibleMultiAgentState (Minimal)
│   ├── MetaStateSchema (Single-agent embedding)
│   └── MultiAgentDynamicSupervisorState (Enhanced coordination)
└── Base Agent (Individual agents)
```

### Key Architectural Principles

1. **Hierarchical State Projection**: Container states project to agent-specific schemas without flattening
2. **Direct Field Updates**: Agents with structured output update container fields like engine nodes
3. **Self-Discover Pattern**: Sequential agents read each other's outputs directly from state fields
4. **Dynamic Recompilation**: Runtime agent addition/removal with graph rebuilding
5. **Engine Namespacing**: Agent engines synchronized with hierarchical naming

## 📦 Core Implementations

### 1. EnhancedMultiAgent V3 - Advanced Coordinator

**Location**: `packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_v3.py`

**Key Features**:
- Generic typing with `MultiAgent[AgentsT]` for type safety
- Performance tracking and adaptive routing
- Multi-engine coordination
- Rich debugging and visualization
- Production stability with advanced features

```python
class EnhancedMultiAgent(Agent, Generic[AgentsT]):
    """Enhanced MultiAgent V3 with full advanced features."""
    
    agents: AgentsT = Field(default_factory=dict)
    execution_mode: str = Field(default="infer")  # infer, sequential, parallel
    performance_mode: bool = Field(default=False)
    agent_performance: dict[str, dict[str, float]] = Field(default_factory=dict)
    
    # Execution modes: "infer", "sequential", "parallel", "supervisor"
    # Performance tracking for adaptive routing
    # Rich debug visualization
```

**Capabilities**:
- Automatic execution mode inference
- Performance-based agent selection
- Dynamic agent addition/removal
- Comprehensive execution tracking
- Rich debug output with timing analysis

### 2. AgentNodeV3Config - Core Execution Engine

**Location**: `packages/haive-core/src/haive/core/graph/node/agent_node_v3.py`

**Purpose**: Enables hierarchical state management and direct field updates in multi-agent workflows

```python
class AgentNodeV3Config(BaseNodeConfig[TInput, TOutput]):
    """Agent node configuration with hierarchical state projection support."""
    
    agent_name: str = Field(description="Name of agent to execute")
    agent: Agent | None = Field(default=None)
    project_state: bool = Field(default=True)  # Enable state projection
    shared_fields: list[str] = Field(default_factory=lambda: ["messages"])
```

**Critical Features**:
- **State Projection**: Projects container state to agent-specific schema
- **Direct Updates**: Agents with structured output update container fields directly
- **Self-Discover Support**: Enables agents to read previous agent outputs
- **Hierarchical Access**: Maintains type safety while allowing cross-agent communication

### 3. Enhanced Sequential Agent

**Location**: `packages/haive-agents/src/haive/agents/multi/enhanced_sequential_agent.py`

**Purpose**: Sequential pipeline execution with state passing

```python
class EnhancedSequentialAgent(Agent):
    """Sequential multi-agent with enhanced state management."""
    
    agents: list[Agent] = Field(default_factory=list)
    state_passing: bool = Field(default=True)
    execution_mode: str = Field(default="sequential")
```

## 🗄️ State Schema Architecture

### 1. MultiAgentState - Full-Featured Container

**Location**: `packages/haive-core/src/haive/core/schema/prebuilt/multi_agent_state.py`

**Inheritance**: `MultiAgentState(ToolState)` - Full tool/message/token management

**Key Features**:
- Hierarchical agent storage with isolated states
- Engine synchronization with namespacing
- Recompilation tracking and management
- Rich debug visualization
- Direct field updates for structured output agents

```python
class MultiAgentState(ToolState):
    """State schema for multi-agent systems with hierarchical management."""
    
    # Agent management
    agents: list[Agent] | dict[str, Agent] = Field(default_factory=dict)
    agent_states: dict[str, dict[str, Any]] = Field(default_factory=dict)
    
    # Execution tracking
    active_agent: str | None = Field(default=None)
    agent_outputs: dict[str, Any] = Field(default_factory=dict)
    agent_execution_order: list[str] = Field(default_factory=list)
    
    # Recompilation support
    agents_needing_recompile: set[str] = Field(default_factory=set)
    recompile_count: int = Field(default=0)
    recompile_history: list[dict[str, Any]] = Field(default_factory=list)
```

**Usage Pattern**:
```python
# Self-Discover workflow
state = MultiAgentState(agents={
    "selector": module_selector_agent,
    "adapter": module_adapter_agent, 
    "reasoner": reasoning_agent
})

# Sequential execution with direct field access
select_result = select_node(state, config)  # Updates: selected_modules
adapt_result = adapt_node(state, config)    # Reads: selected_modules, Updates: adapted_modules  
reason_result = reason_node(state, config)  # Reads: adapted_modules, Updates: final_reasoning
```

### 2. FlexibleMultiAgentState - Minimal Container

**Location**: `packages/haive-core/src/haive/core/schema/prebuilt/flexible_multi_agent_state.py`

**Inheritance**: `FlexibleMultiAgentState(StateSchema)` - No forced messages/tools

**Purpose**: Lightweight coordination without forcing specific fields

```python
class FlexibleMultiAgentState(StateSchema):
    """Flexible multi-agent state without forcing messages or tools."""
    
    agents: list[Agent] | dict[str, Agent] = Field(default_factory=dict)
    agent_states: dict[str, dict[str, Any]] = Field(default_factory=dict)
    shared_context: dict[str, Any] = Field(default_factory=dict)
    
    # Optional coordination fields
    current_agent: str | None = Field(default=None)
    completed_agents: list[str] = Field(default_factory=list)
    agent_outputs: dict[str, Any] = Field(default_factory=dict)
```

**Best For**:
- Minimal overhead multi-agent systems
- Custom coordination patterns
- Agents that don't need tools/messages
- Flexible shared context management

### 3. MetaStateSchema - Single-Agent Embedding

**Location**: `packages/haive-core/src/haive/core/schema/prebuilt/meta_state.py`

**Purpose**: Embed any agent for graph composition with recompilation support

```python
class MetaStateSchema(StateSchema, RecompileMixin):
    """State schema with embedded agent and graph composition support."""
    
    # Core agent embedding
    agent: Any | None = Field(default=None)
    agent_state: dict[str, Any] = Field(default_factory=dict)
    
    # Graph composition
    graph_context: dict[str, Any] = Field(default_factory=dict)
    execution_result: dict[str, Any] | None = Field(default=None)
    composition_metadata: dict[str, Any] = Field(default_factory=dict)
    
    # Execution tracking
    execution_status: str = Field(default="ready")
    agent_name: str | None = Field(default=None)
    agent_type: str | None = Field(default=None)
```

**Key Methods**:
```python
# Factory method for easy creation
meta_state = MetaStateSchema.from_agent(
    agent=simple_agent,
    initial_state={"ready": True},
    graph_context={"purpose": "analysis"}
)

# Async execution with tracking
result = await meta_state.execute_agent(input_data, update_state=True)

# Dynamic agent replacement
meta_state.update_agent(new_agent)  # Triggers recompilation
```

### 4. MultiAgentDynamicSupervisorState - Enhanced Coordination

**Location**: `packages/haive-agents/src/haive/agents/supervisor/multi_agent_dynamic_state.py`

**Purpose**: Combines dynamic supervisor with multi-agent coordination

```python
class MultiAgentDynamicSupervisorState(DynamicSupervisorState):
    """Enhanced state combining dynamic supervisor and multi-agent capabilities."""
    
    # Agent registry management
    agent_registry: AgentRegistryState = Field(default_factory=AgentRegistryState)
    
    # Multi-agent coordination  
    coordination: MultiAgentCoordinationState = Field(default_factory=MultiAgentCoordinationState)
    
    # Dynamic routing
    dynamic_tool_routes: dict[str, str] = Field(default_factory=dict)
    tool_usage_history: list[dict[str, Any]] = Field(default_factory=list)
```

**Advanced Features**:
- Dynamic agent registry management
- Choice model integration for agent selection
- Tool-to-agent mapping and routing
- Execution queue and coordination patterns
- Agent handoff tracking and management

## 🔄 Integration Patterns

### 1. Self-Discover Workflow Pattern

**Concept**: Sequential agents build on each other's outputs through direct field access

```python
# Agent Setup
class ModuleSelectorAgent(SimpleAgent):
    structured_output_model = SelectedModulesSchema

class ModuleAdapterAgent(SimpleAgent): 
    structured_output_model = AdaptedModulesSchema

class ReasoningAgent(SimpleAgent):
    structured_output_model = FinalReasoningSchema

# State Setup
state = MultiAgentState(agents={
    "selector": ModuleSelectorAgent(...),
    "adapter": ModuleAdapterAgent(...),
    "reasoner": ReasoningAgent(...)
})

# Execution Flow - each agent reads previous outputs directly
selector_node = create_agent_node_v3("selector")
adapter_node = create_agent_node_v3("adapter")  
reasoner_node = create_agent_node_v3("reasoner")

# Step 1: Select modules
result1 = selector_node(state, config)
# Result: state.selected_modules = {...}

# Step 2: Adapt modules (reads selected_modules from state)
result2 = adapter_node(state, config)  
# Result: state.adapted_modules = {...}

# Step 3: Generate reasoning (reads adapted_modules from state)
result3 = reasoner_node(state, config)
# Result: state.final_reasoning = {...}
```

### 2. ReactAgent → SimpleAgent Pattern

**Target Implementation**: The user mentioned this as a key pattern

```python
# ReactAgent for reasoning and tool use
react_agent = ReactAgent(
    name="reasoner",
    engine=AugLLMConfig(),
    tools=[research_tool, calculator, web_search]
)

# SimpleAgent for structured output
simple_agent = SimpleAgent(
    name="formatter", 
    engine=AugLLMConfig(),
    structured_output_model=FinalResultSchema
)

# Multi-agent coordination
state = MultiAgentState(agents={
    "reasoner": react_agent,
    "formatter": simple_agent
})

# Sequential execution
reasoning_result = await react_agent.arun("Analyze problem X")
structured_result = await simple_agent.arun(reasoning_result)
```

### 3. LangGraph Integration

```python
from langgraph.graph import StateGraph

# Build graph with multi-agent state
graph = StateGraph(MultiAgentState)

# Add agent nodes
graph.add_node("analyze", create_agent_node_v3("analyzer"))
graph.add_node("plan", create_agent_node_v3("planner")) 
graph.add_node("execute", create_agent_node_v3("executor"))
graph.add_node("review", create_agent_node_v3("reviewer"))

# Define execution flow
graph.add_edge("analyze", "plan")
graph.add_edge("plan", "execute") 
graph.add_edge("execute", "review")

# Compile and execute
app = graph.compile()
final_state = app.invoke(initial_state)
```

## 🎛️ State Management Patterns

### Hierarchical State Projection

**Key Concept**: AgentNodeV3 projects container states to agent-specific schemas

```python
# Container state (MultiAgentState)
container_state = MultiAgentState(
    agents={"planner": planner_agent},
    messages=[...],
    tools=[...],
    # Agent-specific fields populated by structured output
    planning_result=None,
    execution_steps=None
)

# Agent execution with projection
agent_node = create_agent_node_v3("planner", project_state=True)

# Projected state for agent (only relevant fields)
projected_state = PlannerState(
    messages=container_state.messages,  # Shared field
    context=container_state.shared_context,  # Shared field
    # Agent-specific fields excluded to avoid confusion
)

# Agent execution
result = agent_node(container_state, config)

# Direct field update (like engine nodes)
container_state.planning_result = result.planning_result
```

### State Transfer Rules

```python
# Configure cross-agent state transfers
state_transfers = {
    "planner->executor": {
        "plan": "execution_plan",
        "steps": "tasks", 
        "timeline": "schedule"
    },
    "executor->reviewer": {
        "results": "review_data",
        "metrics": "performance_data"
    }
}

# Apply transfers automatically
state.apply_state_transfer("planner", "executor")
```

### Engine Synchronization

```python
# Agents contribute engines to container with namespacing
state = MultiAgentState(agents={
    "planner": planner_agent,  # Has engine
    "executor": executor_agent  # Has engine  
})

# Results in container engines:
state.engines = {
    "planner.main": planner_agent.engine,
    "executor.main": executor_agent.engine,
    "main": planner_agent.engine,  # First agent's engine as default
}
```

## 🔧 Testing Patterns

### Real Component Testing

```python
def test_multi_agent_sequential_execution():
    """Test real multi-agent sequential execution."""
    # Create real agents
    planner = SimpleAgent(
        name="planner",
        engine=AugLLMConfig(temperature=0.1),
        structured_output_model=PlanSchema
    )
    
    executor = SimpleAgent(
        name="executor", 
        engine=AugLLMConfig(temperature=0.1),
        structured_output_model=ResultSchema
    )
    
    # Create state
    state = MultiAgentState(agents=[planner, executor])
    
    # Execute sequence
    plan_node = create_agent_node_v3("planner")
    exec_node = create_agent_node_v3("executor")
    
    # Real execution with actual LLMs
    plan_result = plan_node(state, config)
    exec_result = exec_node(state, config)
    
    # Verify real behavior
    assert hasattr(state, 'plan_result')
    assert hasattr(state, 'execution_result')
    assert state.agent_count == 2
```

### State Schema Testing

```python
def test_multi_agent_state_simple():
    """Test MultiAgentState without circular imports."""
    # Test basic functionality
    state = MultiAgentState()
    
    # Test agent state management
    state.update_agent_state("planner", {"plan": "Step 1", "status": "planning"})
    state.update_agent_state("executor", {"result": None, "status": "waiting"})
    
    # Test recompilation tracking
    state.mark_agent_for_recompile("planner", "Tools changed")
    state.resolve_agent_recompile("planner")
    
    # Test agent outputs
    state.record_agent_output("planner", {"plan": "Complete plan", "steps": 3})
    state.record_agent_output("executor", {"result": "Success", "data": [1, 2, 3]})
```

## 🎯 Implementation Recommendations

### 1. Start with MultiAgentState

For most use cases, start with `MultiAgentState` as it provides:
- Complete tool/message management
- Recompilation tracking
- Rich debugging capabilities
- Engine synchronization
- Hierarchical state management

### 2. Use AgentNodeV3 for Execution

Always use `create_agent_node_v3()` for agent execution in graphs:
- Enables state projection
- Supports direct field updates
- Handles recompilation
- Maintains type safety

### 3. Design for Self-Discover

Structure agents for direct field access:
- Use structured output models on agents
- Design state schema with agent-specific fields
- Let agents read previous outputs directly from state
- Avoid deep nesting in favor of flat field access

### 4. Plan for Recompilation

Always consider dynamic agent changes:
- Mark agents for recompilation when changed
- Use recompilation tracking
- Handle graph rebuilding gracefully
- Test recompilation scenarios

## 📚 Key Files Reference

### Core Implementation Files

1. **EnhancedMultiAgent V3**: `packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_v3.py`
2. **AgentNodeV3**: `packages/haive-core/src/haive/core/graph/node/agent_node_v3.py`
3. **MultiAgentState**: `packages/haive-core/src/haive/core/schema/prebuilt/multi_agent_state.py`
4. **FlexibleMultiAgentState**: `packages/haive-core/src/haive/core/schema/prebuilt/flexible_multi_agent_state.py`
5. **MetaStateSchema**: `packages/haive-core/src/haive/core/schema/prebuilt/meta_state.py`
6. **MultiAgentDynamicSupervisorState**: `packages/haive-agents/src/haive/agents/supervisor/multi_agent_dynamic_state.py`
7. **Enhanced Sequential Agent**: `packages/haive-agents/src/haive/agents/multi/enhanced_sequential_agent.py`

### Test Files

1. **MultiAgentState Test**: `packages/haive-agents/tests/multi/test_multi_agent_state_simple.py`
2. **Core Tests**: `packages/haive-core/tests/test_meta_agent_state_simple_v2.py`

## 🔮 Future Development

### Planned Enhancements

1. **ReactAgent → SimpleAgent Flow**: Target implementation pattern for reasoning + structured output
2. **Node Schema Composer**: Flexible I/O mapping for dynamic composition
3. **Field Visibility Mechanism**: Shared vs private field management
4. **Performance Optimization**: <1ms state projection overhead
5. **Advanced Coordination**: Complex DAG workflows and parallel patterns

### Architecture Evolution

The multi-agent system is designed for evolution:
- Schema composition hierarchy supports dynamic node creation
- Recompilation system enables runtime modifications
- Hierarchical state projection maintains type safety during changes
- Engine synchronization supports multi-LLM coordination

---

## 📝 Summary

The Haive multi-agent architecture provides a sophisticated foundation for complex agent coordination through:

1. **Hierarchical State Management**: No schema flattening, isolated agent states
2. **Direct Field Updates**: Structured output agents update container fields directly  
3. **Self-Discover Support**: Agents read each other's outputs from state fields
4. **Dynamic Recompilation**: Runtime agent changes with graph rebuilding
5. **Rich Debugging**: Comprehensive visualization and tracking
6. **Type Safety**: Generic typing and schema validation throughout

This architecture enables advanced workflows like Self-Discover while maintaining the flexibility for custom coordination patterns and the stability needed for production systems.

**Next Implementation Target**: ReactAgent → SimpleAgent sequential flow with structured output transfer and cross-agent data validation.