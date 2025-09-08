# Haive Framework Refactoring Roadmap

**Created**: 2025-01-06
**Purpose**: Actionable roadmap for addressing technical debt
**Status**: Ready for Implementation

## 🎯 Executive Summary

The Haive framework suffers from severe technical debt concentrated in 4 major monolithic classes. This roadmap provides a phased approach to refactor these components while maintaining backward compatibility and system stability.

## 🚨 Priority Matrix

| Component    | Size (LoC) | Impact   | Effort    | Priority |
| ------------ | ---------- | -------- | --------- | -------- |
| StateSchema  | 500+       | Critical | High      | **P1**   |
| AugLLMConfig | 2601       | Critical | Very High | **P1**   |
| Node System  | 45 files   | High     | Medium    | **P2**   |
| DynamicGraph | 1985       | Medium   | Medium    | **P3**   |

## 📅 Phase 1: Foundation (Weeks 1-4)

### Goal: Create facades and stop the bleeding

### 1.1 StateSchema Facade

```python
# Create a simple interface over the complex StateSchema
class StateManager:
    """Simple interface for state management"""
    def get_field(self, name: str) -> Any
    def set_field(self, name: str, value: Any) -> None
    def is_dirty(self, name: str) -> bool
    def get_changes(self) -> dict
```

**Actions:**

- [ ] Create `StateManager` facade class
- [ ] Add deprecation warnings to direct StateSchema methods
- [ ] Update documentation to use StateManager
- [ ] Add comprehensive tests for StateManager

### 1.2 AugLLMConfig Simplification

```python
# Create focused interfaces
class LLMSettings:
    """Just LLM configuration"""
    model: str
    temperature: float
    max_tokens: int

class PromptManager:
    """Just prompt handling"""
    def format_prompt(template: str, variables: dict) -> str

class ToolManager:
    """Just tool management"""
    def add_tool(tool: Tool) -> None
    def get_tools() -> list[Tool]
```

**Actions:**

- [ ] Create simplified configuration classes
- [ ] Add factory methods for common configurations
- [ ] Document migration path from AugLLMConfig
- [ ] Create compatibility layer

### 1.3 Node Consolidation Plan

**Actions:**

- [ ] Identify core node types (max 6)
- [ ] Map all existing nodes to core types
- [ ] Create migration guide for \_v2, \_v3 variants
- [ ] Mark deprecated nodes

### 1.4 Stop Adding Debt

**Policy Changes:**

- [ ] No new methods in classes > 500 lines
- [ ] All new features through facades
- [ ] Mandatory design review for new components
- [ ] Test coverage requirement: 80%

## 📅 Phase 2: Decomposition (Weeks 5-12)

### Goal: Break apart monoliths incrementally

### 2.1 StateSchema Decomposition

```python
# Separate concerns
class StateData(BaseModel):
    """Pure data storage"""
    fields: dict[str, Any]

class FieldManager:
    """Field operations"""
    def add_field(name: str, type: Type) -> None
    def remove_field(name: str) -> None
    def validate_field(name: str, value: Any) -> bool

class DirtyTracker:
    """Change tracking"""
    def mark_dirty(field: str) -> None
    def get_dirty_fields() -> set[str]
    def reset() -> None

class StateOrchestrator:
    """Coordinates the components"""
    data: StateData
    fields: FieldManager
    tracker: DirtyTracker
```

**Implementation Steps:**

1. **Week 5-6**: Extract StateData
   - [ ] Create pure data class
   - [ ] Move data storage logic
   - [ ] Update tests

2. **Week 7-8**: Extract FieldManager
   - [ ] Create field management class
   - [ ] Move field operations
   - [ ] Update schema composition

3. **Week 9-10**: Extract DirtyTracker
   - [ ] Create tracking class
   - [ ] Move dirty field logic
   - [ ] Add change events

4. **Week 11-12**: Create StateOrchestrator
   - [ ] Coordinate components
   - [ ] Maintain compatibility
   - [ ] Comprehensive testing

### 2.2 AugLLMConfig Breakdown

```python
# Target architecture
class LLMConfiguration:
    settings: LLMSettings
    prompts: PromptManager
    tools: ToolManager
    output: OutputHandler

    @classmethod
    def from_legacy(cls, config: AugLLMConfig):
        """Migration helper"""
```

**Implementation Steps:**

1. **Week 5-7**: Extract Settings
   - [ ] Create LLMSettings class
   - [ ] Move configuration logic
   - [ ] Add validation

2. **Week 8-9**: Extract PromptManager
   - [ ] Create prompt handling
   - [ ] Move template logic
   - [ ] Add prompt registry

3. **Week 10-11**: Extract ToolManager
   - [ ] Create tool management
   - [ ] Move routing logic
   - [ ] Add tool discovery

4. **Week 12**: Integration
   - [ ] Create new configuration class
   - [ ] Add migration helpers
   - [ ] Update documentation

## 📅 Phase 3: Node System Reform (Weeks 13-16)

### Goal: Consolidate to focused node types

### 3.1 Core Node Types

```python
class ExecutionNode:
    """Executes callables/agents/engines"""

class TransformNode:
    """Transforms data/state/messages"""

class RouterNode:
    """Makes routing decisions"""

class ValidationNode:
    """Validates data/schemas"""

class CoordinatorNode:
    """Coordinates multiple nodes"""
```

### 3.2 Migration Plan

1. **Week 13**: Define interfaces
2. **Week 14**: Implement core nodes
3. **Week 15**: Create adapters for existing nodes
4. **Week 16**: Update documentation

### 3.3 Cleanup

- [ ] Remove test files from source
- [ ] Remove example files from source
- [ ] Consolidate validation variants
- [ ] Delete deprecated versions

## 📅 Phase 4: Graph Builder Simplification (Weeks 17-20)

### Goal: Separate concerns in graph building

### 4.1 Target Architecture

```python
class GraphStructure:
    """Just the data structure"""
    nodes: dict[str, Node]
    edges: list[Edge]

class GraphBuilder:
    """Just builds structure"""
    def add_node(node: Node) -> None
    def add_edge(source: str, target: str) -> None

class GraphCompiler:
    """Just compiles to LangGraph"""
    def compile(structure: GraphStructure) -> CompiledGraph

class GraphVisualizer:
    """Just visualization"""
    def visualize(structure: GraphStructure) -> None
```

### 4.2 Implementation

1. **Week 17**: Extract GraphStructure
2. **Week 18**: Separate builders
3. **Week 19**: Extract compiler
4. **Week 20**: Remove pattern system

## 📊 Success Metrics

### Code Quality Metrics

- [ ] No class > 300 lines
- [ ] Cyclomatic complexity < 10
- [ ] Test coverage > 80%
- [ ] No circular dependencies

### Performance Metrics

- [ ] Test suite < 5 seconds
- [ ] Import time < 1 second
- [ ] Memory usage reduced by 30%

### Developer Experience

- [ ] Onboarding time < 1 day
- [ ] Clear documentation for all patterns
- [ ] No version variants (\_v2, \_v3)

## 🛠️ Implementation Guidelines

### 1. Incremental Approach

- Always maintain backward compatibility
- Use deprecation warnings
- Provide migration helpers
- Keep old code until Phase 5

### 2. Testing Strategy

```python
# Test both old and new
def test_state_management():
    # Test legacy
    old_state = StateSchema()
    assert old_state.works()

    # Test new
    new_state = StateManager()
    assert new_state.works()

    # Test compatibility
    assert can_migrate(old_state, new_state)
```

### 3. Documentation Requirements

- Update examples immediately
- Create migration guides
- Document deprecations clearly
- Add inline code comments

### 4. Review Process

- Design review before implementation
- Code review by 2+ developers
- Performance testing required
- Documentation review

## 🚀 Quick Wins (Can Start Immediately)

### 1. Add Facades (1 day each)

```python
# Simple wrappers to hide complexity
class SimpleAgent:
    def __init__(self, name: str):
        self._config = AugLLMConfig()  # Hide complexity

    def run(self, input: str) -> str:
        # Simple interface
```

### 2. Consolidate Imports (2 days)

```python
# haive/core/__init__.py
from haive.core.simple import (
    SimpleAgent,
    SimpleState,
    SimpleNode,
    SimpleGraph
)

__all__ = ['SimpleAgent', 'SimpleState', 'SimpleNode', 'SimpleGraph']
```

### 3. Remove Test Files from Source (1 hour)

```bash
# Move all test files to proper test directories
find packages/*/src -name "*test*.py" -exec mv {} ../tests/ \;
```

### 4. Create Deprecation Helpers (1 day)

```python
def deprecated(message: str):
    """Decorator for deprecation warnings"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(message, DeprecationWarning)
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

## 📋 Checklist for Each Refactoring

- [ ] Design documented and reviewed
- [ ] Tests written for new code
- [ ] Migration guide created
- [ ] Deprecation warnings added
- [ ] Documentation updated
- [ ] Performance benchmarked
- [ ] Code reviewed
- [ ] Integration tested

## 🎯 Expected Outcomes

### After Phase 1 (Month 1)

- Development velocity improved by 20%
- New features easier to add
- Clear patterns established

### After Phase 2 (Month 3)

- Monoliths broken apart
- Testing time reduced by 50%
- Onboarding simplified

### After Phase 3 (Month 4)

- Node system consolidated
- Maintenance burden reduced
- Clear architecture

### After Phase 4 (Month 5)

- All major debt addressed
- System maintainable
- Ready for growth

## 🔗 Resources

### Documentation

- [Architecture Hub](./ARCHITECTURE_HUB.md)
- [Technical Debt Summary](./technical_debt.md)
- [StateSchema Redesign](./STATE_SCHEMA_REDESIGN.md)
- [Engine Redesign](./ENGINE_REDESIGN.md)

### Examples

- [Facade Pattern Example](./examples/facade_pattern.py)
- [Migration Helper Example](./examples/migration_helper.py)
- [Test Both Patterns](./examples/test_compatibility.py)

---

**Remember**: The goal is not perfection but continuous improvement. Start with quick wins, maintain compatibility, and refactor incrementally. Every small improvement counts!
