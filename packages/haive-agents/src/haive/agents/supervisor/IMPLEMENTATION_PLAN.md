# Haive Supervisor Implementation Plan

## Overview

This document outlines the detailed implementation plan for integrating LangGraph's supervisor pattern into the Haive framework, leveraging existing Haive infrastructure while providing enhanced dynamic routing capabilities.

## Key Design Decisions

### 1. Single Node Dynamic Routing Approach

Instead of LangGraph's multi-node handoff pattern, we'll implement a single supervisor node that uses `DynamicChoiceModel` for intelligent routing:

```python
# Traditional LangGraph approach (multiple handoff tools)
handoff_to_research = create_handoff_tool("research_agent")
handoff_to_math = create_handoff_tool("math_agent")

# Haive approach (single dynamic routing node)
supervisor_node = SupervisorNode(
    routing_model=DynamicChoiceModel(options=registered_agents),
    decision_engine=AugLLM(prompt="Route to best agent for: {task}")
)
```

### 2. Leveraging DynamicChoiceModel

The `DynamicChoiceModel` at `/haive/core/common/models/dynamic_choice_model.py` provides:

- Runtime agent addition/removal
- Automatic schema generation
- Choice validation
- Protocol-based flexibility

### 3. Integration with Haive's Node System

Using `NodeFactory` and `EngineNodeConfig` from `/haive/core/graph/node/`:

- Consistent with Haive patterns
- Leverages existing engine infrastructure
- Maintains compatibility with BaseGraph

## Implementation Components

### 1. SupervisorAgent Class

**File**: `supervisor/agent.py`

```python
class SupervisorAgent(Agent):
    """Haive-native supervisor with dynamic routing capabilities."""

    # Configuration
    routing_model: DynamicChoiceModel[str]
    registered_agents: dict[str, Agent]
    routing_engine: AugLLMConfig
    output_mode: Literal["full_history", "last_message"] = "last_message"

    def build_graph(self) -> BaseGraph:
        """Build supervisor graph with single routing node."""

    def register_agent(self, agent: Agent) -> None:
        """Add agent to registry and update routing model."""

    def create_routing_node(self) -> NodeFunction:
        """Create dynamic routing node using NodeFactory."""
```

**Key Features**:

- Inherits full Agent capabilities (mixins, persistence, serialization)
- Dynamic agent registry with runtime modification
- Single routing node approach for efficiency
- Integration with Haive's graph building patterns

### 2. AgentRegistry

**File**: `supervisor/registry.py`

```python
class AgentRegistry:
    """Manages agent lifecycle and routing model synchronization."""

    def __init__(self, routing_model: DynamicChoiceModel[str]):
        self.agents: dict[str, Agent] = {}
        self.routing_model = routing_model

    def register(self, agent: Agent) -> None:
        """Register agent and update routing model."""

    def unregister(self, name: str) -> bool:
        """Remove agent and update routing model."""

    def get_available_agents(self) -> list[str]:
        """Get current agent names for routing."""
```

### 3. DynamicRoutingEngine

**File**: `supervisor/routing.py`

```python
class DynamicRoutingEngine:
    """Handles routing decisions using DynamicChoiceModel and LLM."""

    def __init__(self,
                 routing_model: DynamicChoiceModel[str],
                 decision_engine: AugLLMConfig):
        self.routing_model = routing_model
        self.decision_engine = decision_engine

    async def route_request(self, state: Any) -> str:
        """Determine target agent for request."""

    def create_routing_prompt(self, available_agents: list[str]) -> str:
        """Generate prompt for routing decision."""
```

### 4. HandoffToolManager

**File**: `supervisor/handoff.py`

```python
class HandoffToolManager:
    """Manages agent handoff tools and message preservation."""

    def create_handoff_tool(self, target_agent: str) -> BaseTool:
        """Create handoff tool for specific agent."""

    def preserve_message_context(self,
                                source_state: Any,
                                target_agent: str) -> Any:
        """Maintain conversation context during handoffs."""
```

## Implementation Phases

### Phase 1: Core Infrastructure (Week 1)

- [ ] Implement `SupervisorAgent` base class
- [ ] Create `AgentRegistry` with `DynamicChoiceModel` integration
- [ ] Basic graph building with single routing node
- [ ] Unit tests for core components

### Phase 2: Routing Engine (Week 2)

- [ ] Implement `DynamicRoutingEngine`
- [ ] Integration with `NodeFactory` patterns
- [ ] Routing decision logic
- [ ] State preservation mechanisms

### Phase 3: Handoff System (Week 3)

- [ ] Implement `HandoffToolManager`
- [ ] Message context preservation
- [ ] Agent state isolation
- [ ] Error handling and recovery

### Phase 4: Advanced Features (Week 4)

- [ ] Parallel agent execution support
- [ ] Agent capability detection
- [ ] Performance optimization
- [ ] Comprehensive documentation

### Phase 5: Testing & Examples (Week 5)

- [ ] Integration tests
- [ ] Example implementations
- [ ] Performance benchmarks
- [ ] Documentation completion

## Technical Considerations

### Graph Building Strategy

```python
def build_graph(self) -> BaseGraph:
    """Build supervisor graph with dynamic routing."""
    graph = BaseGraph(self.state_schema)

    # Create supervisor node using NodeFactory
    supervisor_node = NodeFactory.create_node_function(
        config=self.routing_engine,
        command_goto="route_to_agent"
    )

    # Add registered agents as nodes
    for name, agent in self.registered_agents.items():
        agent_node = NodeFactory.create_node_function(
            config=agent.main_engine,
            command_goto="supervisor"
        )
        graph.add_node(name, agent_node)

    # Dynamic routing logic
    graph.add_conditional_edges(
        "supervisor",
        self._routing_function,
        self.routing_model.option_names
    )

    return graph
```

### State Management

- Use Haive's `StateMixin` for state handling
- Preserve message history across agent boundaries
- Maintain tool_call_id relationships
- Support both full and filtered message modes

### Error Handling

- Agent unavailability graceful handling
- Routing failures with fallback mechanisms
- State corruption detection and recovery
- Comprehensive logging for debugging

## Integration Points

### With Existing Haive Components

1. **Agent Base Class**: Full inheritance of capabilities
2. **Schema Composer**: Automatic schema merging
3. **Engine System**: NodeFactory integration
4. **Persistence**: Leverage existing mixins
5. **Configuration**: Use Haive config patterns

### With DynamicChoiceModel

1. **Runtime Updates**: Agent addition/removal
2. **Schema Generation**: Automatic routing schemas
3. **Validation**: Choice validation before routing
4. **Flexibility**: Support various agent types

## Success Criteria

### Functional Requirements

- [x] Dynamic agent registration/deregistration
- [ ] Intelligent routing based on context
- [ ] Message preservation across handoffs
- [ ] Integration with existing Haive patterns
- [ ] Performance parity with standard agents

### Non-Functional Requirements

- [ ] Comprehensive test coverage (>90%)
- [ ] Clear documentation and examples
- [ ] Performance benchmarks
- [ ] Memory efficiency
- [ ] Scalability to 10+ agents

## Next Steps

1. **Start Implementation**: Begin with `SupervisorAgent` base class
2. **Prototype Routing**: Create basic routing with `DynamicChoiceModel`
3. **Test Integration**: Ensure compatibility with existing agents
4. **Iterate**: Refine based on testing and feedback
5. **Document**: Create comprehensive usage guides

This plan provides a clear roadmap for implementing a sophisticated supervisor system that leverages the best of both LangGraph patterns and Haive's infrastructure while adding unique dynamic routing capabilities.
