# Procedural Implementation Plan for Multi-Agent State Design

## Executive Summary

A step-by-step plan to implement and test different state mixing strategies for multi-agent systems, starting with the meta-agent state pattern.

## Phase 1: Foundation (Current State Analysis)

### Step 1.1: Document Current Issues

- [ ] Schema composition creates namespace conflicts
- [ ] Type safety is lost during state transitions
- [ ] No clear state ownership model
- [ ] Agent nodes expect specific types but receive generic state

### Step 1.2: Define Requirements

- [ ] Type safety throughout execution
- [ ] Clear state ownership and access patterns
- [ ] Support for both shared and private state
- [ ] Easy agent addition/removal
- [ ] Debugging and introspection capabilities

## Phase 2: Meta-Agent State Implementation

### Step 2.1: Basic Meta-Agent State

```python
class MetaAgentState(StateSchema):
    """A state that contains itself and agent states."""

    # Self-referential meta fields
    meta: Dict[str, Any] = Field(
        default_factory=dict,
        description="Meta information about the state itself"
    )

    # Shared communication channel
    messages: List[BaseMessage] = Field(default_factory=list)

    # Agent containers (start simple)
    agents: Dict[str, Agent] = Field(
        default_factory=dict,
        description="Agent instances"
    )

    # Agent states
    agent_states: Dict[str, StateSchema] = Field(
        default_factory=dict,
        description="Current state for each agent"
    )

    # Execution control
    current_agent: Optional[str] = None
    execution_history: List[Dict[str, Any]] = Field(default_factory=list)
```

### Step 2.2: State Projection Methods

```python
def get_agent_view(self, agent_name: str) -> StateSchema:
    """Get the state view for a specific agent."""
    # Returns the agent's specific state + shared fields

def update_from_agent(self, agent_name: str, result: StateSchema) -> None:
    """Update state from agent execution result."""
    # Merges agent result back into meta state
```

### Step 2.3: Test Basic Flow

1. Create meta state with 2 agents
2. Project state to agent 1
3. Execute agent 1
4. Merge results back
5. Project state to agent 2
6. Verify state consistency

## Phase 3: Schema Mixing Strategies

### Step 3.1: Additive Mixing

```python
class AdditiveMixer:
    """Adds fields from all agents without conflict resolution."""

    def mix_schemas(self, schemas: List[Type[StateSchema]]) -> Type[StateSchema]:
        # Combine all fields, error on conflicts
```

### Step 3.2: Namespaced Mixing

```python
class NamespacedMixer:
    """Prefixes fields with agent names."""

    def mix_schemas(self, schemas: List[Type[StateSchema]]) -> Type[StateSchema]:
        # agent1_task, agent2_task, etc.
```

### Step 3.3: Hierarchical Mixing

```python
class HierarchicalMixer:
    """Creates nested structure."""

    def mix_schemas(self, schemas: List[Type[StateSchema]]) -> Type[StateSchema]:
        # shared.messages, agent1.task, agent2.result
```

### Step 3.4: Smart Mixing

```python
class SmartMixer:
    """Intelligently merges based on field semantics."""

    def mix_schemas(self, schemas: List[Type[StateSchema]]) -> Type[StateSchema]:
        # Detects common fields, creates shared section
        # Keeps unique fields separate
```

## Phase 4: Integration with Agent Node V2

### Step 4.1: Enhanced Agent Node

```python
class MetaAwareAgentNode(AgentNodeConfig):
    """Agent node that understands meta state."""

    def __call__(self, state: MetaAgentState, config: Optional[ConfigLike]) -> Command:
        # 1. Extract agent view from meta state
        # 2. Execute agent with projected state
        # 3. Merge results back to meta state
        # 4. Return Command with updated meta state
```

### Step 4.2: Coordinator Node Updates

- Update coordinator to work with meta state
- Handle state transitions between agents
- Manage execution flow

## Phase 5: Testing Protocol

### Test 1: Type Safety Verification

```python
def test_type_safety():
    # Create typed agents
    planner = PlannerAgent(state_schema=PlannerState)
    executor = ExecutorAgent(state_schema=ExecutorState)

    # Create meta state
    meta_state = MetaAgentState()
    meta_state.register_agent(planner)
    meta_state.register_agent(executor)

    # Verify type hints work
    planner_view = meta_state.get_agent_view("planner")
    assert isinstance(planner_view, PlannerState)
```

### Test 2: State Flow Test

```python
def test_state_flow():
    # Test complete flow through multiple agents
    # Verify state consistency
    # Check no data loss
```

### Test 3: Performance Test

```python
def test_performance():
    # Measure state projection overhead
    # Check memory usage
    # Time state updates
```

## Phase 6: Decision Matrix

| Criteria    | Meta-Agent | Namespaced | Hierarchical | Smart Mix |
| ----------- | ---------- | ---------- | ------------ | --------- |
| Type Safety | ✅✅✅     | ✅✅       | ✅✅         | ✅        |
| Flexibility | ✅✅       | ✅         | ✅✅         | ✅✅✅    |
| Performance | ✅✅       | ✅✅✅     | ✅✅         | ✅        |
| Debugging   | ✅✅✅     | ✅         | ✅✅         | ✅✅      |
| Complexity  | Medium     | Low        | Medium       | High      |

## Implementation Order

### Week 1: Foundation

1. **Day 1-2**: Implement basic MetaAgentState
2. **Day 3-4**: Add projection/merge methods
3. **Day 5**: Basic testing

### Week 2: Schema Mixing

1. **Day 1**: Implement mixing strategies
2. **Day 2-3**: Test each strategy
3. **Day 4-5**: Performance optimization

### Week 3: Integration

1. **Day 1-2**: Update AgentNodeV2
2. **Day 3**: Update coordinator
3. **Day 4-5**: Full system testing

## Success Criteria

1. **Type Safety**: No runtime type errors
2. **Performance**: < 1ms overhead per state transition
3. **Usability**: Adding new agent requires < 10 lines of code
4. **Correctness**: All state transitions are validated
5. **Debugging**: Clear state visualization in logs

## Risk Mitigation

1. **Risk**: Circular dependencies in meta state
   - **Mitigation**: Use lazy evaluation and careful design

2. **Risk**: Performance degradation with many agents
   - **Mitigation**: Implement state diffing and caching

3. **Risk**: Complex debugging with nested states
   - **Mitigation**: Rich logging and state visualization tools

## Next Immediate Steps

1. Create `MetaAgentState` class
2. Implement basic projection logic
3. Test with 2 simple agents
4. Measure performance baseline
5. Iterate based on results
