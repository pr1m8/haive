# Multi-Agent State Design Variants

## Overview

Exploring different approaches for mixing agent schemas in multi-agent systems.

## Order of Operations

### Phase 1: Define Core Concepts

1. **Agent State**: Individual agent's typed state
2. **Meta State**: Coordination and control state
3. **Master State**: The combined state for the entire system
4. **State Transitions**: How state flows between agents

### Phase 2: Design Variants

## Variant A: Meta-Agent Container Pattern

```python
class MetaAgentState(StateSchema):
    """Meta state that contains agent states as typed fields."""

    # Meta coordination fields
    messages: List[BaseMessage]
    current_agent: str
    execution_path: List[str]

    # Agent states as first-class typed fields
    planner_state: Optional[PlannerState] = None
    executor_state: Optional[ExecutorState] = None
    reviewer_state: Optional[ReviewerState] = None

    # Shared context all agents can access
    shared_context: Dict[str, Any]

    # Meta tracking
    agent_history: List[Dict[str, Any]]
```

**Pros:**

- Type safety maintained
- Clear ownership of fields
- Easy debugging

**Cons:**

- Must know all agents at compile time
- Adding agents requires schema changes

## Variant B: Dynamic Agent Registry Pattern

```python
class DynamicMetaState(StateSchema):
    """Meta state with dynamic agent registration."""

    # Core shared state
    messages: List[BaseMessage]

    # Dynamic agent registry
    agent_registry: Dict[str, Type[StateSchema]]  # agent_name -> schema type
    agent_states: Dict[str, StateSchema]          # agent_name -> state instance

    # Execution control
    active_agents: List[str]
    current_agent: Optional[str]

    # State transfer rules
    transfer_mappings: Dict[str, Dict[str, str]]  # source_agent -> {field_mappings}
```

**Pros:**

- Dynamic agent addition
- Flexible state management
- Runtime type checking

**Cons:**

- Less compile-time safety
- More complex validation

## Variant C: Hierarchical Composition Pattern

```python
class HierarchicalState(StateSchema):
    """State with hierarchical composition."""

    class SharedState(BaseModel):
        """Fields shared by all agents."""
        messages: List[BaseMessage]
        context: Dict[str, Any]
        metadata: Dict[str, Any]

    class PrivateStates(BaseModel):
        """Container for agent-specific states."""
        # Dynamically composed from agent schemas
        pass

    # Composed fields
    shared: SharedState
    private: PrivateStates

    # Control flow
    flow_state: Dict[str, Any]
```

## Variant D: Schema Mixin Pattern

```python
# Define mixable components
class MessagesMixin(BaseModel):
    messages: List[BaseMessage]

class PlannerMixin(BaseModel):
    task: str
    plan: Optional[str]
    plan_steps: List[str]

class ExecutorMixin(BaseModel):
    execution_result: Optional[str]
    completed_steps: List[str]

# Compose via multiple inheritance
class SequentialMultiAgentState(
    StateSchema,
    MessagesMixin,
    PlannerMixin,
    ExecutorMixin
):
    """Composed state using mixins."""
    # Add coordination fields
    current_agent: str
    agent_outputs: Dict[str, Any]
```

**Pros:**

- Reusable components
- Clear composition
- Type safe

**Cons:**

- Can lead to complex inheritance
- Field conflicts need resolution

## Variant E: Projection-Based Pattern

```python
class ProjectionState(StateSchema):
    """Master state with projection capabilities."""

    # All fields in flat structure
    _fields: Dict[str, Any]

    # Schema registry
    _schemas: Dict[str, Type[BaseModel]]

    def project_to(self, agent_name: str) -> BaseModel:
        """Project state to agent-specific schema."""
        schema = self._schemas[agent_name]
        relevant_fields = self._get_relevant_fields(schema)
        return schema(**relevant_fields)

    def merge_from(self, agent_name: str, result: BaseModel) -> None:
        """Merge agent result back."""
        for field, value in result.dict().items():
            self._fields[f"{agent_name}_{field}"] = value
```

## Phase 3: Testing Strategy

### 1. **Type Safety Test**

- Can we maintain type hints through the entire flow?
- Do IDEs provide proper autocomplete?

### 2. **Runtime Validation Test**

- Does Pydantic validation work correctly?
- Can we catch schema mismatches early?

### 3. **State Transfer Test**

- How do we pass data between agents?
- Is the mapping explicit or implicit?

### 4. **Performance Test**

- Cost of state projection/copying
- Memory usage with large states

### 5. **Developer Experience Test**

- How easy is it to add a new agent?
- How clear are error messages?

## Phase 4: Implementation Order

1. **Start with Variant A** (Meta-Agent Container)
   - Simplest to understand
   - Good for fixed agent sets
   - Test basic concepts

2. **Then try Variant D** (Schema Mixin)
   - Tests composition approach
   - Good for reusable components

3. **Finally Variant B** (Dynamic Registry)
   - Most flexible
   - Best for dynamic systems

## Key Questions to Answer

1. **Field Ownership**: Who owns shared fields like `messages`?
2. **Update Semantics**: How do we handle concurrent updates?
3. **Validation Points**: When do we validate state transitions?
4. **Schema Evolution**: How do we version schemas?
5. **Error Recovery**: What happens when state is invalid?

## Next Steps

1. Implement minimal version of each variant
2. Create test scenarios for each
3. Measure type safety, performance, and usability
4. Choose best approach or hybrid

## Design Principles

1. **Explicit over Implicit**: Clear state ownership
2. **Type Safety First**: Maintain types through entire flow
3. **Fail Fast**: Validate early and often
4. **Composable**: Easy to extend and modify
5. **Debuggable**: Clear state visualization
