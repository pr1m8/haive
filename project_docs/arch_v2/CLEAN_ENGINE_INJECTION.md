# Clean Engine Injection Pattern for StateSchema

**Created**: 2025-01-07
**Purpose**: Design clean patterns for injecting engines into StateSchema
**Status**: Proposed solution

## 🎯 The Problem

Currently StateSchema has a messy engine management system:

- Mixed `engine` (singular) and `engines` (dict) fields
- 74 methods including engine management
- Circular dependencies between Engine ↔ StateSchema
- No clean injection pattern

## 💡 The Solution: Clean Dependency Injection

### 1. Engine Registry Pattern

```python
class EngineRegistry:
    """Central registry for all engines."""

    def __init__(self):
        self._engines: Dict[str, Engine] = {}
        self._factories: Dict[str, Callable] = {}

    def register(self, name: str, engine: Engine) -> None:
        """Register an engine instance."""
        self._engines[name] = engine

    def register_factory(self, name: str, factory: Callable) -> None:
        """Register an engine factory for lazy creation."""
        self._factories[name] = factory

    def get(self, name: str) -> Engine:
        """Get or create engine by name."""
        if name in self._engines:
            return self._engines[name]

        if name in self._factories:
            engine = self._factories[name]()
            self._engines[name] = engine
            return engine

        raise KeyError(f"Engine '{name}' not found")
```

### 2. Clean StateSchema (No Engine Management)

```python
class StateSchema(BaseModel):
    """Pure state definition - NO engine management."""

    # State fields only
    messages: List[BaseMessage] = Field(default_factory=list)
    context: Dict[str, Any] = Field(default_factory=dict)

    # NO engine fields!
    # NO engine methods!
```

### 3. Engine Injector Pattern

```python
class EngineInjector:
    """Handles engine injection into state schemas."""

    def __init__(self, registry: EngineRegistry):
        self.registry = registry

    def inject(self, state: StateSchema, engine_map: Dict[str, str]) -> None:
        """Inject engines into state as needed."""
        for field_name, engine_name in engine_map.items():
            engine = self.registry.get(engine_name)
            setattr(state, f"_{field_name}_engine", engine)

    def create_enhanced_state(
        self,
        state_class: Type[StateSchema],
        engines: Dict[str, Engine]
    ) -> StateSchema:
        """Create state with engine capabilities."""

        # Create base state
        state = state_class()

        # Attach engines as private attributes
        for name, engine in engines.items():
            setattr(state, f"_engine_{name}", engine)

        # Add accessor methods dynamically
        def get_engine(self, name: str) -> Engine:
            return getattr(self, f"_engine_{name}", None)

        state.get_engine = types.MethodType(get_engine, state)

        return state
```

### 4. Prompt Engine Integration

```python
class PromptEngine(Engine):
    """Clean prompt engine."""

    def __init__(self, template: str, variables: List[str]):
        self.template = template
        self.variables = variables

    def format(self, **kwargs) -> str:
        """Format the prompt with variables."""
        return self.template.format(**kwargs)

    def create_runnable(self) -> Callable:
        """Create runnable for the engine pattern."""
        return lambda x: self.format(**x)
```

### 5. Usage Pattern

```python
# 1. Setup engines in registry
registry = EngineRegistry()

# Register prompt engine
prompt_engine = PromptEngine(
    template="Question: {question}\nContext: {context}\nAnswer:",
    variables=["question", "context"]
)
registry.register("qa_prompt", prompt_engine)

# Register LLM engine
llm_engine = AugLLMConfig(temperature=0.7)
registry.register("main_llm", llm_engine)

# Register tool engine
tool_engine = ToolEngine(tools=[calculator, web_search])
registry.register("tools", tool_engine)

# 2. Create clean state (no engines)
class MyAgentState(StateSchema):
    messages: List[BaseMessage] = Field(default_factory=list)
    question: str = Field(default="")
    context: str = Field(default="")

# 3. Inject engines when needed
injector = EngineInjector(registry)

state = MyAgentState()
injector.inject(state, {
    "prompt": "qa_prompt",
    "llm": "main_llm",
    "tools": "tools"
})

# 4. Use injected engines
prompt = state._prompt_engine.format(
    question=state.question,
    context=state.context
)
result = state._llm_engine.invoke(prompt)
```

## 🏗️ Advanced Patterns

### 1. Engine Composition

```python
class CompositeEngine(Engine):
    """Compose multiple engines."""

    def __init__(self, engines: List[Engine]):
        self.engines = engines

    def create_runnable(self) -> Callable:
        """Chain engines together."""
        def run(input_data):
            result = input_data
            for engine in self.engines:
                runnable = engine.create_runnable()
                result = runnable(result)
            return result
        return run

# Usage
composite = CompositeEngine([
    prompt_engine,
    llm_engine,
    parser_engine
])
registry.register("full_pipeline", composite)
```

### 2. Lazy Engine Loading

```python
class LazyEngineProxy:
    """Proxy for lazy engine loading."""

    def __init__(self, engine_name: str, registry: EngineRegistry):
        self.engine_name = engine_name
        self.registry = registry
        self._engine = None

    def __getattr__(self, name):
        """Lazy load engine on first access."""
        if self._engine is None:
            self._engine = self.registry.get(self.engine_name)
        return getattr(self._engine, name)

# Usage
state._llm_engine = LazyEngineProxy("main_llm", registry)
# Engine only loaded when actually used
result = state._llm_engine.invoke(prompt)  # Loads here
```

### 3. Engine Lifecycle Management

```python
class ManagedEngine(Engine):
    """Engine with lifecycle management."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._runnable = None
        self._initialized = False

    def initialize(self) -> None:
        """Initialize engine resources."""
        if not self._initialized:
            self._runnable = self._create_runnable_from_config()
            self._initialized = True

    def cleanup(self) -> None:
        """Clean up engine resources."""
        if self._initialized:
            if hasattr(self._runnable, 'close'):
                self._runnable.close()
            self._runnable = None
            self._initialized = False

    def create_runnable(self) -> Callable:
        """Get or create runnable."""
        if not self._initialized:
            self.initialize()
        return self._runnable

# Context manager support
@contextmanager
def managed_state(state_class, engines):
    """Manage engine lifecycle with state."""
    state = state_class()
    injector = EngineInjector(registry)
    injector.inject(state, engines)

    # Initialize all engines
    for engine in engines.values():
        if hasattr(engine, 'initialize'):
            engine.initialize()

    try:
        yield state
    finally:
        # Cleanup all engines
        for engine in engines.values():
            if hasattr(engine, 'cleanup'):
                engine.cleanup()
```

## 🎯 Benefits

### 1. Clean Separation of Concerns

- **StateSchema**: Pure state definition (data only)
- **Engine**: Configuration and execution
- **EngineRegistry**: Central management
- **EngineInjector**: Clean injection pattern

### 2. No Circular Dependencies

```
StateSchema (pure data)
    ↓
EngineInjector (one-way injection)
    ↓
Engine (independent components)
```

### 3. Testability

```python
def test_state_without_engines():
    """Test state logic without engine complexity."""
    state = MyAgentState(
        messages=[HumanMessage(content="test")],
        context="test context"
    )
    assert len(state.messages) == 1
    # No engine complexity to mock!

def test_with_mock_engines():
    """Test with simple mock engines."""
    mock_engine = Mock()
    mock_engine.invoke.return_value = "response"

    state = MyAgentState()
    state._llm_engine = mock_engine

    result = state._llm_engine.invoke("test")
    assert result == "response"
```

### 4. Flexibility

```python
# Different engine configurations for different environments

# Development
dev_registry = EngineRegistry()
dev_registry.register("llm", MockLLMEngine())

# Production
prod_registry = EngineRegistry()
prod_registry.register("llm", AugLLMConfig(
    model="gpt-4",
    temperature=0.3
))

# Same state, different engines
state = MyAgentState()
injector = EngineInjector(
    prod_registry if IS_PRODUCTION else dev_registry
)
```

## 📊 Comparison

### Current Approach (Messy)

```python
class StateSchema:
    # 74 methods!
    # Circular dependencies!
    engine: Optional[Engine]
    engines: Dict[str, Engine]

    def add_engine(self, name, engine): ...
    def get_engine(self, name): ...
    def remove_engine(self, name): ...
    def list_engines(self): ...
    def setup_engines_and_tools(self): ...
    def sync_engine_fields(self): ...
    # ... 68 more methods
```

### Clean Approach

```python
class StateSchema:
    # Pure state - maybe 10 methods
    messages: List[BaseMessage]
    context: Dict[str, Any]

class EngineInjector:
    # Single responsibility - injection
    def inject(self, state, engines): ...

class EngineRegistry:
    # Single responsibility - registry
    def register(self, name, engine): ...
    def get(self, name): ...
```

## 🚀 Migration Strategy

### Phase 1: Add Clean Components

```python
# Add alongside existing code
from haive.core.clean import (
    CleanStateSchema,
    EngineRegistry,
    EngineInjector
)
```

### Phase 2: Adapter Pattern

```python
class StateSchemaAdapter:
    """Adapt old StateSchema to clean pattern."""

    def __init__(self, old_state: StateSchema):
        self.old_state = old_state
        self.registry = EngineRegistry()

        # Extract engines from old state
        if old_state.engine:
            self.registry.register("main", old_state.engine)
        for name, engine in old_state.engines.items():
            self.registry.register(name, engine)

    def to_clean_state(self) -> CleanStateSchema:
        """Convert to clean state."""
        clean = CleanStateSchema()
        # Copy pure state fields
        clean.messages = self.old_state.messages
        clean.context = self.old_state.context
        return clean
```

### Phase 3: Gradual Migration

```python
# New code uses clean pattern
state = CleanStateSchema()
injector.inject(state, {"llm": "main_llm"})

# Old code still works
old_state = StateSchema()
old_state.add_engine("llm", engine)
```

## 🎯 Summary

The clean engine injection pattern:

1. **Separates concerns** - State is just data
2. **Eliminates circular dependencies** - One-way flow
3. **Improves testability** - No mocking complexity
4. **Increases flexibility** - Easy to swap engines
5. **Reduces complexity** - From 74 methods to ~10

This pattern turns the 2,323-line StateSchema monolith into:

- ~100 lines for CleanStateSchema
- ~50 lines for EngineRegistry
- ~50 lines for EngineInjector
- **Total: ~200 lines instead of 2,323!**

---

_"Dependency injection is about inverting control. StateSchema trying to control everything is the opposite of good DI."_
