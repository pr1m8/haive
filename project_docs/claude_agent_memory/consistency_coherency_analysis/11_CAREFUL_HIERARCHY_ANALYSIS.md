# Careful Hierarchy Analysis - Component vs Agent

## Current State Analysis

### What We Have Now

- **Agent** = Current base class in `haive-agents/src/haive/agents/base/agent.py`
- Everything inherits from Agent (SimpleAgent, BaseRAGAgent, DocumentAgent, etc.)
- Agent extends InvokableEngine + multiple mixins
- Complex inheritance: `Agent(InvokableEngine, ExecutionMixin, StateMixin, PersistenceMixin, SerializationMixin, ABC)`

### Problems Identified

1. **Everything is "Agent"** even when it doesn't reason
2. **No clear distinction** between LLM reasoning vs deterministic processing
3. **Complex inheritance chain** makes it hard to understand capabilities
4. **Schema composition inconsistency** across different "agent" types

## Proposed Conceptual Model

### Component as Higher-Level Abstraction

- **Component** = "Anything that can be executed as part of a workflow"
- **Agent** = "Component that uses LLM for reasoning and decision-making"

### Key Insight

Not everything that can be executed needs to be called an "Agent". We can have:

- Components that retrieve data
- Components that process documents
- Components that load files
- Agents that reason with LLMs

## Careful Considerations

### 1. **Backward Compatibility is Critical**

- Existing code must continue to work
- Can't break `SimpleAgent(engine=llm_config)` pattern
- Can't break existing import statements
- Migration must be gradual and optional

### 2. **Naming Consistency**

- Users are familiar with "Agent" terminology
- Don't want to confuse with too many new concepts
- Need clear, intuitive naming that doesn't require relearning

### 3. **Implementation Complexity**

- Current Agent class has complex mixin inheritance
- Schema composition system is already sophisticated
- Can't disrupt existing patterns that work

### 4. **Gradual Evolution Strategy**

- Add new concepts alongside existing ones
- Provide migration path, not forced migration
- Allow both old and new patterns to coexist

## Proposed Approach: Additive, Not Disruptive

### Step 1: Add Component as New Base (Optional)

```python
# New base class (optional to use)
class Component(GraphNode):
    """Base for all executable workflow units"""
    # Provides common functionality

# Existing Agent class (unchanged)
class Agent(InvokableEngine, ...mixins):
    """Existing agent implementation - no changes"""
    # All existing functionality preserved
```

### Step 2: Create Specialized Components (New Options)

```python
# New specialized components (additions, not replacements)
class RetrieverComponent(Component):
    """For data retrieval tasks"""

class ProcessorComponent(Component):
    """For data processing tasks"""

# Existing agents (unchanged)
class SimpleAgent(Agent):
    """Existing simple agent - no changes"""
```

### Step 3: Provide Migration Helpers (Optional)

```python
# Migration helpers for those who want them
def migrate_to_component(old_agent_class):
    """Helper to convert agent to component if desired"""
    # Optional migration utility

# Compatibility functions
def is_reasoning_component(obj):
    """Check if component/agent has reasoning capability"""
    return isinstance(obj, Agent) or (
        isinstance(obj, Component) and
        obj.has_engine_type(EngineType.LLM)
    )
```

## Benefits of Careful Approach

### 1. **No Breaking Changes**

- All existing code continues to work
- Existing agents remain agents
- Existing import statements unchanged

### 2. **Gradual Adoption**

- New projects can use Component hierarchy
- Existing projects can migrate at their own pace
- Both patterns can coexist

### 3. **Clear Migration Path**

- Users can see benefits before committing
- Can migrate one piece at a time
- Can roll back if needed

### 4. **Improved Clarity Over Time**

- New code becomes clearer
- Old code still works
- Documentation can guide toward better patterns

## Schema Composition Strategy

### Keep Existing Patterns Working

```python
# Existing agent schema composition (unchanged)
class SimpleAgent(Agent):
    def _setup_schemas(self):
        # Current implementation preserved
        pass

# New component schema composition (additive)
class RetrieverComponent(Component):
    def _setup_schemas(self):
        # New, cleaner implementation
        pass
```

### Provide Unified Interface for Mixed Types

```python
# New utility for mixed component/agent workflows
def compose_mixed_schema(items):
    """Handle both old agents and new components"""
    agents = [item for item in items if isinstance(item, Agent)]
    components = [item for item in items if isinstance(item, Component)]

    # Use appropriate composer for each type
    # Provide unified result
```

## Questions Before Implementation

### 1. **Scope of Changes**

- How much of existing Agent functionality should Component have?
- Should Component be minimal or comprehensive?
- What's the minimum viable Component interface?

### 2. **Migration Strategy**

- Should we encourage migration or just provide the option?
- How do we handle mixed workflows (old agents + new components)?
- What's the timeline for deprecating old patterns (if ever)?

### 3. **Naming Decisions**

- Is "Component" the right name for the base class?
- Should specialized components be "RetrieverComponent" or "Retriever"?
- How do we make naming intuitive for users?

### 4. **Interface Design**

- Should Component have `execute()` method or something else?
- How do we handle the fact that Agent has `invoke()` method?
- Should both have similar interfaces for consistency?

## Recommendation

**Start small and careful:**

1. Create Component as additive base class
2. Create one specialized component type (e.g., RetrieverComponent)
3. Test with real use cases
4. Get feedback before expanding
5. Keep all existing Agent functionality unchanged
6. Provide clear documentation on when to use what

This approach minimizes risk while providing a path toward better architecture.
