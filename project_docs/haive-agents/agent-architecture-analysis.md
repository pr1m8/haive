# Haive Agent Architecture Analysis

**Date**: 2025-01-31
**Version**: 1.0
**Purpose**: Comprehensive analysis of the current agent architecture in Haive framework
**Last Updated**: 2025-01-31

## 🏗️ Architecture Overview

The Haive agent framework follows a sophisticated hierarchical architecture with multiple layers of abstraction:

### Core Hierarchy

```
Workflow (Pure orchestration, no LLM)
└── Agent (Workflow + Engine)
    ├── SimpleAgent (Basic agent pattern)
    ├── ReactAgent (Reasoning loop pattern)
    └── MultiAgent (Agent coordination)
        ├── EnhancedMultiAgent (V3 - Full features)
        └── EnhancedMultiAgentV4 (V4 - Clean API)
```

### Key Design Principles

1. **Engine-Centric Design**: Engines are the core abstraction, agents wrap engines
2. **Mixin-Based Composition**: Functionality added through mixins (RecompileMixin, DynamicToolRouteMixin, etc.)
3. **Hook-Based Extensibility**: Comprehensive lifecycle hooks for monitoring and customization
4. **Schema Composition**: Automatic schema generation from engines
5. **Type Safety**: Generic typing with defaults (e.g., Agent[AugLLMConfig])

## 📊 Component Analysis

### 1. Enhanced Base Agent (`enhanced_agent.py`)

The foundation of the entire agent system:

**Key Features**:

- Generic on engine type: `Agent[EngineT]`
- Automatic setup and initialization pipeline
- Schema composition via SchemaComposer
- Persistence and serialization support
- Full hooks integration

**Critical Methods**:

- `setup_agent()`: Abstract method for subclass-specific setup
- `build_graph()`: Abstract method for graph construction
- `compile()`: Graph compilation with caching
- Engine management (get_engine, set_engine)

**Setup Pipeline**:

1. Initialize hooks system
2. Call `setup_agent()` for field syncing
3. Generate schemas from engines
4. Setup persistence
5. Build initial graph

### 2. Hooks System (`hooks.py`)

Comprehensive event system for agent lifecycle:

**Event Categories**:

- **Lifecycle**: before/after_setup, before/after_build_graph
- **Execution**: before/after_run, before/after_arun
- **Node Execution**: before/after_node
- **Error Handling**: on_error, on_retry
- **State Management**: before/after_state_update
- **Specialized**: reflection, grading, structured output, message transformation

**Usage Pattern**:

```python
@agent.before_run
def log_start(context):
    logger.info(f"Starting {context.agent_name}")
```

### 3. Pre/Post Agent Mixin (`pre_post_agent_mixin.py`)

Generalizes pre/post processing patterns:

**Key Components**:

- Optional pre-processing agent
- Main agent processing
- Optional post-processing agent
- Message transformation between stages
- Hook integration for monitoring

**Factory Functions**:

- `create_reflection_agent()`: Adds reflection post-processing
- `create_graded_reflection_agent()`: Adds grading and reflection
- `create_structured_output_agent()`: Adds structured output processing

### 4. SimpleAgentV3 (`agent_v3.py`)

Enhanced implementation with full dynamic architecture:

**Key Features**:

- Default to AugLLMConfig engine
- RecompileMixin for auto-recompilation
- DynamicToolRouteMixin for tool management
- Debug mode enabled by default
- Structured output support
- Meta-agent embedding capabilities

**Convenience Fields** (sync to engine):

- temperature, max_tokens, model_name
- force_tool_use, structured_output_model
- system_message

**Dynamic Graph Building**:

- Adapts based on configuration (tools, structured output)
- Automatic node addition (agent_node, tool_node, parse_output, validation)
- Conditional routing based on message content

### 5. ReactAgentV4 (`agent_v4.py`)

Minimal ReactAgent implementing core ReAct pattern:

**Key Design**:

- Inherits from SimpleAgentV3
- Modifies graph to loop: tool_node → agent_node
- No fancy features, just the core pattern
- Clean implementation in ~65 lines

## 🔄 Multi-Agent Architecture

### EnhancedMultiAgent (V3)

Full-featured multi-agent coordination:

**Features**:

- Generic typing: `MultiAgent[AgentsT]`
- Performance tracking and adaptive routing
- Multiple execution modes (sequential, parallel, conditional, branch)
- Rich debugging and observability
- Agent performance metrics

**Key Methods**:

- `add_conditional_routing()`: Dynamic routing based on conditions
- `add_parallel_group()`: Parallel agent execution
- `update_performance()`: Track agent success rates
- `get_best_agent_for_task()`: Performance-based selection

### EnhancedMultiAgentV4

Clean API implementation with enhanced base agent pattern:

**Improvements**:

- Direct list initialization: `agents=[agent1, agent2, ...]`
- Proper implementation of `build_graph()` abstract method
- AgentNodeV3 integration for state projection
- Simple, intuitive API
- Build modes: auto, manual, lazy

**User-Friendly Methods**:

- `add_edge()`: Direct edge between agents
- `add_conditional_edge()`: Boolean condition routing
- `add_multi_conditional_edge()`: Multi-way routing
- `add_agent()`: Dynamic agent addition

## 🔌 AgentNodeV3 Architecture

Sophisticated state projection for multi-agent systems:

**Key Concepts**:

1. **Hierarchical State Management**: Projects container states to agent-specific schemas
2. **Direct Field Updates**: Structured output agents update state fields directly
3. **Type Safety**: Maintains schema validation throughout execution
4. **Dynamic Agent Lookup**: Resolves agents from state at runtime

**Execution Flow**:

1. **State Projection**: Container state → Agent-specific schema
2. **Agent Execution**: Agent processes projected state
3. **Output Integration**: Results → Container state updates

**Critical Methods**:

- `_project_state_for_agent()`: Extracts agent-specific state + shared fields
- `_process_agent_output()`: Handles structured vs message-based outputs
- `__call__()`: Main execution orchestration

## 📦 MultiAgentState Architecture

The state container that enables sophisticated multi-agent coordination:

### Key Features

1. **Hierarchical Agent Management**: Agents stored as first-class fields
2. **No Schema Flattening**: Each agent maintains its own schema independently
3. **Direct Field Updates**: Structured output agents update container fields directly
4. **State Isolation**: Each agent has isolated state in `agent_states` dict
5. **Recompilation Tracking**: Dynamic agent updates with graph recompilation support

### Architecture

**Storage Structure**:

```python
MultiAgentState:
├── agents: Dict[str, Agent]           # Agent instances (list converted to dict)
├── agent_states: Dict[str, Dict]      # Isolated state per agent
├── agent_outputs: Dict[str, Any]      # Legacy output storage
├── active_agent: Optional[str]        # Currently executing agent
├── agent_execution_order: List[str]   # Sequential execution order
└── agents_needing_recompile: Set[str] # Recompilation tracking
```

**Key Methods**:

- `get_agent_state()`: Get isolated state for specific agent
- `update_agent_state()`: Update agent's isolated state
- `set_active_agent()`: Mark agent as currently executing
- `mark_agent_for_recompile()`: Track recompilation needs
- `resolve_agent_recompile()`: Mark recompilation as complete

### Self-Discover Workflow Pattern

The MultiAgentState enables clean sequential workflows where agents read each other's outputs directly:

```python
# Agent 1 outputs to state fields
planner_node(state)  # Updates: planning_result, confidence

# Agent 2 reads those fields directly
executor_node(state)  # Reads: planning_result, Updates: execution_result

# Agent 3 reads all previous outputs
reviewer_node(state)  # Reads: planning_result, execution_result
```

### Engine Management

Engines from agents are synced to the parent state with namespacing:

- Agent engines: `{agent_name}.{engine_name}`
- Main engines: `{agent_name}.main`
- Global fallbacks: `main`, `{engine_name}`

### Debug Visualization

MultiAgentState provides rich debug visualization:

- `display_debug_info()`: Comprehensive tree view
- `create_agent_table()`: Status table for all agents
- Visual indicators for active, completed, pending agents

## 🎯 Key Differences Between V3 and V4

### EnhancedMultiAgent (V3)

- **Focus**: Feature-rich with performance tracking
- **Complexity**: High - many configuration options
- **Use Case**: Complex workflows needing adaptive routing
- **State**: EnhancedMultiAgentState or MultiAgentState
- **Strengths**: Performance metrics, adaptation, debugging

### EnhancedMultiAgentV4

- **Focus**: Clean API and proper base agent integration
- **Complexity**: Low - intuitive interface
- **Use Case**: Standard multi-agent workflows
- **State**: MultiAgentState (fixed)
- **Strengths**: Simple API, proper inheritance, easy to use

## 🧪 Test Strategy Recommendations

### 1. Basic Agent Tests

- Test SimpleAgentV3 with various configurations
- Verify dynamic graph building
- Test structured output integration
- Validate hook execution

### 2. Multi-Agent Coordination Tests

- Sequential execution with state sharing
- Parallel execution with convergence
- Conditional routing based on state
- Performance tracking and adaptation (V3)

### 3. State Projection Tests

- AgentNodeV3 state projection accuracy
- Structured output field updates
- Message-based backward compatibility
- Multi-level state hierarchies

### 4. Edge Cases

- Dynamic agent addition
- Recompilation triggers
- Error handling and recovery
- Complex routing patterns

## 🔮 Architecture Insights

### Strengths

1. **Flexibility**: Mixin-based design allows easy composition
2. **Observability**: Comprehensive hooks and debug support
3. **Type Safety**: Generic typing with sensible defaults
4. **Extensibility**: Easy to add new agent types
5. **State Management**: Sophisticated projection and isolation

### Potential Improvements

1. **Simplification**: Some abstractions could be simplified
2. **Documentation**: More inline examples needed
3. **Performance**: Hook system adds overhead
4. **Testing**: Need more integration tests
5. **Error Messages**: Could be more descriptive

## 📚 Recommended Usage Patterns

### Simple Agent

```python
agent = SimpleAgentV3(
    name="assistant",
    temperature=0.7,
    structured_output_model=MyModel
)
```

### Multi-Agent Sequential

```python
workflow = EnhancedMultiAgentV4(
    agents=[planner, executor, reviewer],
    execution_mode="sequential"
)
```

### Multi-Agent with Routing

```python
workflow = EnhancedMultiAgentV4(
    agents=[classifier, simple_handler, complex_handler],
    execution_mode="conditional"
)
workflow.add_conditional_edge(
    "classifier",
    lambda state: state["complexity"] > 0.5,
    "complex_handler",
    "simple_handler"
)
```

### Performance-Tracked Multi-Agent

```python
workflow = EnhancedMultiAgent(
    agents={"fast": fast_agent, "accurate": accurate_agent},
    performance_mode=True,
    adaptation_rate=0.2
)
```

## 🎓 Conclusion

The Haive agent architecture represents a sophisticated approach to agent design with:

- Clear separation of concerns (Workflow → Agent → MultiAgent)
- Flexible composition through mixins
- Comprehensive extensibility via hooks
- Strong type safety with generics
- Multiple abstraction levels for different use cases

**V3 vs V4 Choice**:

- Use V3 for complex workflows needing performance tracking
- Use V4 for clean, simple multi-agent coordination
- Both are production-ready with different strengths

The architecture successfully balances power and flexibility while maintaining reasonable complexity for the features provided.
