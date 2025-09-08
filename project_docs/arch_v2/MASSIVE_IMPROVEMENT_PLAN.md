# Haive Framework: Massive Practical Design Improvement Plan

**Created**: 2025-01-07
**Purpose**: Comprehensive, actionable plan to fix the architectural crisis
**Scope**: Complete framework redesign while maintaining backwards compatibility
**Timeline**: 12-week implementation plan

## 🎯 Executive Summary

The Haive framework is collapsing under 10x code bloat, circular dependencies, and 7 god objects. This plan provides a practical, step-by-step approach to:

1. **Reduce codebase by 89%** (2,747 → 300 files)
2. **Eliminate circular dependencies** completely
3. **Break up monoliths** (74+ methods → 10 methods)
4. **Create clean architecture** with proper separation
5. **Maintain backwards compatibility** during migration

## 📊 Current State Assessment

### Critical Metrics

- **2,747 Python files** (should be ~300)
- **7 God Objects** with 50-112 methods each
- **105 MultiAgent variants** doing the same thing
- **119 agent.py files** with massive duplication
- **12 archive directories** of failed attempts

### Root Causes

1. No separation of concerns
2. Everything depends on everything
3. Classes trying to do too much
4. No clear architectural boundaries
5. Accumulation of workarounds

## 🏗️ The Master Plan

### Phase 1: Stop the Bleeding (Week 1)

#### 1.1 Freeze New Features

```python
# .github/ARCHITECTURE_FREEZE.md
NO NEW FEATURES UNTIL REFACTORING COMPLETE
- No new agent variants
- No new state schema fields
- No new engine types
- Only critical bug fixes
```

#### 1.2 Create Architecture Decision Records

```markdown
# ADR-001: Separation of Concerns

Status: Accepted
Context: StateSchema has 74 methods mixing 10 responsibilities
Decision: Split into single-responsibility components
Consequences: Breaking change requiring migration
```

#### 1.3 Set Up Metrics Dashboard

```python
# scripts/architecture_metrics.py
def measure_complexity():
    metrics = {
        "total_files": count_python_files(),
        "god_objects": find_classes_over_50_methods(),
        "circular_deps": find_circular_dependencies(),
        "duplicate_code": find_duplicates(),
    }
    return metrics

# Run weekly to track progress
```

### Phase 2: Create Clean Foundation (Weeks 2-3)

#### 2.1 New Namespace Structure

```python
haive/
├── simple/                 # New clean implementation
│   ├── __init__.py
│   ├── state.py           # Pure state (100 lines)
│   ├── engine.py          # Engine pattern (150 lines)
│   ├── agent.py           # Simple agent (100 lines)
│   ├── react.py           # React agent (150 lines)
│   ├── multi.py           # Multi-agent (200 lines)
│   └── graph.py           # Graph builder (200 lines)
├── core/                  # Existing (keep for compatibility)
└── agents/                # Existing (keep for compatibility)
```

#### 2.2 Core Abstractions

```python
# haive/simple/state.py
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class State(BaseModel):
    """Pure state container - NO business logic."""
    messages: List[Dict[str, str]] = Field(default_factory=list)
    context: Dict[str, Any] = Field(default_factory=dict)

    # That's it! No engines, no methods beyond Pydantic

# haive/simple/engine.py
from abc import ABC, abstractmethod
from typing import Any, Callable

class Engine(ABC):
    """Minimal engine interface."""

    @abstractmethod
    def create_runnable(self) -> Callable:
        """Create executable component."""
        pass

class EngineRegistry:
    """Central engine management."""

    def __init__(self):
        self._engines: Dict[str, Engine] = {}

    def register(self, name: str, engine: Engine):
        self._engines[name] = engine

    def get(self, name: str) -> Engine:
        return self._engines[name]

# haive/simple/agent.py
class Agent:
    """Minimal agent - 100 lines max."""

    def __init__(self, name: str, engine: Engine):
        self.name = name
        self.engine = engine
        self._runnable = None

    def run(self, input_data: Any) -> Any:
        if not self._runnable:
            self._runnable = self.engine.create_runnable()
        return self._runnable(input_data)
```

### Phase 3: Implement Core Patterns (Weeks 4-5)

#### 3.1 Clean Dependency Injection

```python
# haive/simple/injection.py
class Injector:
    """Clean dependency injection."""

    def __init__(self, registry: EngineRegistry):
        self.registry = registry

    def inject_engines(self, target: Any, engine_map: Dict[str, str]):
        """Inject engines into target."""
        for attr_name, engine_name in engine_map.items():
            engine = self.registry.get(engine_name)
            setattr(target, f"_{attr_name}", engine)

# Usage
state = State()
injector = Injector(registry)
injector.inject_engines(state, {
    "llm": "main_llm",
    "prompt": "qa_prompt",
    "tools": "tool_engine"
})
```

#### 3.2 Prompt Engine Pattern

```python
# haive/simple/prompt.py
class PromptEngine(Engine):
    """Clean prompt engine."""

    def __init__(self, template: str):
        self.template = template

    def create_runnable(self) -> Callable:
        return lambda ctx: self.template.format(**ctx)

# Usage
prompt_engine = PromptEngine("Q: {question}\nA:")
registry.register("qa_prompt", prompt_engine)
```

#### 3.3 React Loop Pattern

```python
# haive/simple/react.py
class ReactAgent(Agent):
    """React with simple loop."""

    def __init__(self, name: str, engine: Engine, tools: List[Any]):
        super().__init__(name, engine)
        self.tools = tools
        self.max_iterations = 10

    def run(self, input_data: Any) -> Any:
        for i in range(self.max_iterations):
            # Think
            thought = self._runnable(input_data)

            # Act (use tool if needed)
            if self._needs_tool(thought):
                tool_result = self._use_tool(thought)
                input_data = {"thought": thought, "observation": tool_result}
            else:
                return thought

        return "Max iterations reached"
```

### Phase 4: Create Facades (Weeks 6-7)

#### 4.1 StateSchema Facade

```python
# haive/facades/state_facade.py
class StateSchemaFacade:
    """Facade over the 74-method StateSchema."""

    def __init__(self, legacy_state: StateSchema):
        self._legacy = legacy_state
        self._simple = State()

    def get_messages(self) -> List:
        return self._simple.messages

    def add_message(self, msg: str):
        self._simple.messages.append(msg)

    def get_engine(self, name: str) -> Engine:
        # Delegate to registry instead of StateSchema
        return registry.get(name)

    # Hide the other 71 methods!
```

#### 4.2 AugLLMConfig Facade

```python
# haive/facades/llm_facade.py
class LLMConfigFacade:
    """Facade over 98-method AugLLMConfig."""

    def __init__(self, legacy_config: AugLLMConfig):
        self._legacy = legacy_config

    def create_llm(self) -> Callable:
        """Simple LLM creation."""
        return self._legacy.create_runnable()

    def with_tools(self, tools: List) -> 'LLMConfigFacade':
        """Add tools simply."""
        self._legacy.tools = tools
        return self

    # Hide the other 95 methods!
```

#### 4.3 BaseGraph Facade

```python
# haive/facades/graph_facade.py
class GraphFacade:
    """Facade over 112-method BaseGraph."""

    def __init__(self):
        self._nodes = {}
        self._edges = []

    def add_node(self, name: str, func: Callable):
        self._nodes[name] = func

    def add_edge(self, from_node: str, to_node: str):
        self._edges.append((from_node, to_node))

    def compile(self) -> Callable:
        # Simple compilation without "intelligent" routing
        return self._build_simple_graph()

    # No more guessing execution order from names!
```

### Phase 5: Migration Strategy (Weeks 8-9)

#### 5.1 Adapter Pattern

```python
# haive/adapters/legacy_adapter.py
class LegacyAdapter:
    """Adapt old code to new patterns."""

    @staticmethod
    def adapt_state(old_state: StateSchema) -> State:
        """Convert old StateSchema to clean State."""
        new_state = State()
        new_state.messages = old_state.messages
        new_state.context = getattr(old_state, 'context', {})
        return new_state

    @staticmethod
    def adapt_agent(old_agent: OldAgent) -> Agent:
        """Convert old agent to simple agent."""
        engine = LegacyAdapter.adapt_engine(old_agent.engine)
        return Agent(old_agent.name, engine)
```

#### 5.2 Gradual Migration

```python
# haive/__init__.py
# Support both old and new imports

# Old way (keep working)
from haive.core.schema import StateSchema
from haive.agents.simple import SimpleAgent as OldSimpleAgent

# New way (preferred)
from haive.simple import State, Agent, ReactAgent

# Deprecation warnings
def __getattr__(name):
    if name == "StateSchema":
        warnings.warn(
            "StateSchema is deprecated. Use haive.simple.State",
            DeprecationWarning,
            stacklevel=2
        )
        return StateSchema
```

### Phase 6: Consolidation (Weeks 10-11)

#### 6.1 Merge MultiAgent Variants

```python
# haive/simple/multi.py
class MultiAgent(Agent):
    """ONE MultiAgent to rule them all."""

    def __init__(self, agents: List[Agent], mode: str = "sequential"):
        self.agents = agents
        self.mode = mode

    def run(self, input_data: Any) -> Any:
        if self.mode == "sequential":
            result = input_data
            for agent in self.agents:
                result = agent.run(result)
            return result
        elif self.mode == "parallel":
            return [agent.run(input_data) for agent in self.agents]
        else:
            raise ValueError(f"Unknown mode: {self.mode}")

# That's it! Not 105 variants!
```

#### 6.2 Archive Cleanup

```bash
#!/bin/bash
# scripts/archive_cleanup.sh

# Move all archives to single location
mkdir -p deprecated/archives
find packages -type d -name "archive" -exec mv {} deprecated/archives/ \;

# Create migration guide
cat > deprecated/MIGRATION.md << EOF
# Migration from Deprecated Code

## Archives
All archived code has been moved here.
DO NOT ADD NEW CODE TO ARCHIVES.

## Migration Path
Old: haive.agents.multi.archive.v4.MultiAgentV4
New: haive.simple.MultiAgent

[Migration examples...]
EOF
```

### Phase 7: Testing & Validation (Week 12)

#### 7.1 Regression Tests

```python
# tests/test_backwards_compat.py
def test_old_api_still_works():
    """Ensure old code doesn't break."""
    # Old way
    old_state = StateSchema()
    old_state.add_engine("llm", some_engine)

    # Should still work (with deprecation warning)
    assert old_state.get_engine("llm") is not None

def test_new_api_works():
    """Test new clean API."""
    # New way
    state = State()
    registry.register("llm", some_engine)

    # Clean and simple
    assert registry.get("llm") is not None
```

#### 7.2 Performance Benchmarks

```python
# benchmarks/performance.py
def benchmark_old_vs_new():
    # Old way: Load 2,747 files
    start = time.time()
    from haive.core import StateSchema
    old_time = time.time() - start

    # New way: Load ~30 files
    start = time.time()
    from haive.simple import State
    new_time = time.time() - start

    print(f"Old: {old_time:.2f}s, New: {new_time:.2f}s")
    print(f"Improvement: {old_time/new_time:.1f}x faster")
```

## 📊 Success Metrics

### Week 1 Baseline

```yaml
total_files: 2,747
god_objects: 7
max_methods: 112 (BaseGraph)
circular_deps: 47
multiagent_variants: 105
```

### Week 12 Target

```yaml
total_files: 300 (-89%)
god_objects: 0 (-100%)
max_methods: 15 (-87%)
circular_deps: 0 (-100%)
multiagent_variants: 1 (-99%)
```

## 🚀 Implementation Schedule

### Week 1: Foundation

- [ ] Freeze features
- [ ] Create ADRs
- [ ] Set up metrics
- [ ] Team alignment

### Weeks 2-3: Clean Core

- [ ] Create haive.simple namespace
- [ ] Implement State, Engine, Agent
- [ ] Basic dependency injection

### Weeks 4-5: Core Patterns

- [ ] PromptEngine
- [ ] ReactAgent loop
- [ ] MultiAgent consolidation

### Weeks 6-7: Facades

- [ ] StateSchema facade
- [ ] AugLLMConfig facade
- [ ] BaseGraph facade

### Weeks 8-9: Migration

- [ ] Adapters for old code
- [ ] Deprecation warnings
- [ ] Documentation

### Weeks 10-11: Consolidation

- [ ] Merge duplicates
- [ ] Clean archives
- [ ] Optimize imports

### Week 12: Validation

- [ ] Full regression tests
- [ ] Performance benchmarks
- [ ] Documentation review
- [ ] Release preparation

## 🎯 Key Principles

### 1. Simplicity First

```python
# ❌ WRONG
class ComplexThing:
    # 74 methods, 2000 lines

# ✅ RIGHT
class SimpleThing:
    # 10 methods, 100 lines
```

### 2. Single Responsibility

```python
# ❌ WRONG
class DoesEverything:
    def manage_state(): ...
    def handle_engines(): ...
    def route_tools(): ...

# ✅ RIGHT
class State: # Just state
class EngineRegistry: # Just engines
class Router: # Just routing
```

### 3. Explicit Over Magic

```python
# ❌ WRONG
def _infer_from_naming_patterns(agents):
    # Guess execution order from names

# ✅ RIGHT
def set_execution_order(agents: List[str]):
    # Explicit order
```

### 4. Composition Over Inheritance

```python
# ❌ WRONG
class SuperComplexBase:
    # 7 mixins, 43 methods

# ✅ RIGHT
class Simple:
    def __init__(self, engine: Engine):
        self.engine = engine  # Compose!
```

## 🛡️ Risk Mitigation

### Backwards Compatibility

- Keep old namespace working
- Add deprecation warnings
- Provide migration tools
- Extensive regression tests

### Team Resistance

- Show performance improvements
- Demonstrate simpler code
- Quick wins first
- Incremental migration

### Technical Debt

- Don't try to fix everything
- Focus on core problems
- Facade pattern for legacy
- Archive don't delete

## 📈 Expected Outcomes

### Developer Experience

- **10x faster imports** (2,747 → 300 files)
- **90% less code to understand**
- **Clear architectural boundaries**
- **Simple, testable components**

### System Performance

- **Faster startup** (less code to load)
- **Lower memory usage** (fewer objects)
- **Better caching** (smaller modules)
- **Reduced latency** (simpler paths)

### Business Impact

- **Faster feature development**
- **Easier onboarding**
- **Reduced bugs**
- **Maintainable codebase**

## 🎯 Success Criteria

The refactoring is successful when:

1. ✅ New agents can be created in <50 lines
2. ✅ No class has >20 methods
3. ✅ No circular dependencies
4. ✅ All tests pass
5. ✅ 90% code reduction achieved
6. ✅ Documentation is clear
7. ✅ Team is using new patterns

## 📝 Conclusion

This plan transforms Haive from a 2,747-file monster into a clean, 300-file framework. The key is:

1. **Stop making it worse** (freeze)
2. **Build clean alternative** (haive.simple)
3. **Hide complexity** (facades)
4. **Migrate gradually** (adapters)
5. **Measure success** (metrics)

With 12 weeks of focused effort, we can deliver a framework that's 10x simpler, faster, and more maintainable.

---

_"The best code is no code. The second best is simple code. Haive currently has neither."_
