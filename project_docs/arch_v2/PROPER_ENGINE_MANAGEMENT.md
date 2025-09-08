# Proper Engine Management Design

**Created**: 2025-01-07
**Purpose**: Design robust engine management system that actually works
**Status**: Addressing the real need

## 🎯 The Real Problem

You're right - we NEED engine management. The problem isn't that StateSchema manages engines, it's that it does it BADLY:

- No clear lifecycle management
- Circular dependencies
- Mixed responsibilities
- Poor injection patterns
- No proper registry

## 💡 The Solution: Proper Engine Management

### 1. Engine Lifecycle Manager

```python
class EngineManager:
    """Proper engine lifecycle management."""

    def __init__(self):
        self._engines: Dict[str, Engine] = {}
        self._factories: Dict[str, Callable] = {}
        self._initialized: Dict[str, bool] = {}
        self._dependencies: Dict[str, List[str]] = {}

    def register_engine(
        self,
        name: str,
        engine: Engine = None,
        factory: Callable = None,
        depends_on: List[str] = None
    ):
        """Register engine with proper dependency tracking."""
        if engine:
            self._engines[name] = engine
            self._initialized[name] = False
        elif factory:
            self._factories[name] = factory

        if depends_on:
            self._dependencies[name] = depends_on

    def initialize_engine(self, name: str) -> Engine:
        """Initialize engine with dependency resolution."""
        # Initialize dependencies first
        if name in self._dependencies:
            for dep in self._dependencies[name]:
                if not self._initialized.get(dep, False):
                    self.initialize_engine(dep)

        # Create if needed
        if name not in self._engines and name in self._factories:
            self._engines[name] = self._factories[name]()

        # Initialize
        engine = self._engines[name]
        if hasattr(engine, 'initialize'):
            engine.initialize()

        self._initialized[name] = True
        return engine

    def get_engine(self, name: str) -> Engine:
        """Get initialized engine."""
        if not self._initialized.get(name, False):
            return self.initialize_engine(name)
        return self._engines[name]

    def shutdown_engine(self, name: str):
        """Proper cleanup."""
        if name in self._engines and self._initialized.get(name):
            engine = self._engines[name]
            if hasattr(engine, 'cleanup'):
                engine.cleanup()
            self._initialized[name] = False
```

### 2. StateSchema with Proper Engine Support

```python
class ManagedStateSchema(BaseModel):
    """State with proper engine management."""

    # State data
    messages: List[BaseMessage] = Field(default_factory=list)
    context: Dict[str, Any] = Field(default_factory=dict)

    # Engine management (proper!)
    _engine_manager: EngineManager = None
    _engine_bindings: Dict[str, str] = {}

    def __init__(self, **data):
        super().__init__(**data)
        self._engine_manager = EngineManager()

    def bind_engine(self, field_name: str, engine_name: str):
        """Bind engine to field name for access."""
        self._engine_bindings[field_name] = engine_name

    def get_engine(self, field_name: str) -> Engine:
        """Get engine by field binding."""
        engine_name = self._engine_bindings.get(field_name)
        if engine_name:
            return self._engine_manager.get_engine(engine_name)
        return None

    @property
    def llm_engine(self) -> Engine:
        """Convenient property for main LLM."""
        return self.get_engine("llm")

    @property
    def prompt_engine(self) -> Engine:
        """Convenient property for prompts."""
        return self.get_engine("prompt")

    @property
    def tool_engine(self) -> Engine:
        """Convenient property for tools."""
        return self.get_engine("tools")
```

### 3. Enhanced Engine Types

```python
class PromptEngine(Engine):
    """Proper prompt engine with state injection."""

    def __init__(self, templates: Dict[str, str]):
        self.templates = templates
        self._compiled = {}

    def initialize(self):
        """Compile templates on init."""
        for name, template in self.templates.items():
            self._compiled[name] = self._compile_template(template)

    def format_with_state(self, template_name: str, state: StateSchema) -> str:
        """Format template with state context."""
        template = self._compiled[template_name]

        # Extract relevant state fields
        context = {
            "messages": state.messages,
            "context": state.context,
            **self._extract_custom_fields(state)
        }

        return template.format(**context)

    def create_runnable(self) -> Callable:
        """Create runnable that accepts state."""
        def run(state: StateSchema, template_name: str = "default"):
            return self.format_with_state(template_name, state)
        return run

class LLMEngine(Engine):
    """Enhanced LLM engine with proper integration."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._llm = None
        self._prompt_engine = None

    def set_prompt_engine(self, prompt_engine: PromptEngine):
        """Connect prompt engine."""
        self._prompt_engine = prompt_engine

    def initialize(self):
        """Initialize LLM."""
        from langchain_openai import ChatOpenAI
        self._llm = ChatOpenAI(**self.config)

    def invoke_with_state(self, state: StateSchema, template: str = None) -> str:
        """Invoke with automatic prompt formatting."""
        if template and self._prompt_engine:
            prompt = self._prompt_engine.format_with_state(template, state)
        else:
            # Use messages from state
            prompt = state.messages

        return self._llm.invoke(prompt)

    def create_runnable(self) -> Callable:
        """Create state-aware runnable."""
        def run(state: StateSchema):
            return self.invoke_with_state(state)
        return run
```

### 4. Engine Composition & Chaining

```python
class CompositeEngine(Engine):
    """Engine that composes multiple engines."""

    def __init__(self, engines: List[Tuple[str, Engine]], mode: str = "sequential"):
        self.engines = engines
        self.mode = mode
        self._manager = EngineManager()

        # Register all sub-engines
        for name, engine in engines:
            self._manager.register_engine(name, engine)

    def initialize(self):
        """Initialize all sub-engines."""
        for name, _ in self.engines:
            self._manager.initialize_engine(name)

    def create_runnable(self) -> Callable:
        """Create composite runnable."""
        if self.mode == "sequential":
            def run(state: StateSchema):
                result = state
                for name, _ in self.engines:
                    engine = self._manager.get_engine(name)
                    runnable = engine.create_runnable()
                    result = runnable(result)
                return result
            return run

        elif self.mode == "parallel":
            def run(state: StateSchema):
                results = {}
                for name, _ in self.engines:
                    engine = self._manager.get_engine(name)
                    runnable = engine.create_runnable()
                    results[name] = runnable(state)
                return results
            return run

class PipelineEngine(Engine):
    """Engine for building pipelines."""

    def __init__(self):
        self.stages: List[Tuple[str, Engine, Dict]] = []

    def add_stage(self, name: str, engine: Engine, config: Dict = None):
        """Add pipeline stage."""
        self.stages.append((name, engine, config or {}))
        return self  # Fluent interface

    def create_runnable(self) -> Callable:
        """Create pipeline runnable."""
        def run(state: StateSchema):
            for stage_name, engine, config in self.stages:
                # Update state with stage name
                state.context["current_stage"] = stage_name

                # Apply stage config
                if "inject_fields" in config:
                    for field, value in config["inject_fields"].items():
                        setattr(state, field, value)

                # Run engine
                runnable = engine.create_runnable()
                result = runnable(state)

                # Update state with result
                if "save_to" in config:
                    state.context[config["save_to"]] = result
                else:
                    state.context[f"{stage_name}_result"] = result

            return state
        return run
```

### 5. Engine Registry with Hot Reload

```python
class GlobalEngineRegistry:
    """Global registry with hot reload support."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self._engines: Dict[str, Engine] = {}
        self._configs: Dict[str, Dict] = {}
        self._watchers: List[Callable] = []

    def register_config(self, name: str, config: Dict):
        """Register engine configuration."""
        self._configs[name] = config

        # Notify watchers of config change
        for watcher in self._watchers:
            watcher(name, config)

    def create_engine(self, name: str, engine_type: str) -> Engine:
        """Create engine from config."""
        config = self._configs.get(name, {})

        if engine_type == "llm":
            engine = LLMEngine(config)
        elif engine_type == "prompt":
            engine = PromptEngine(config.get("templates", {}))
        elif engine_type == "pipeline":
            engine = PipelineEngine()
            for stage in config.get("stages", []):
                stage_engine = self.create_engine(stage["name"], stage["type"])
                engine.add_stage(stage["name"], stage_engine, stage.get("config"))
        else:
            raise ValueError(f"Unknown engine type: {engine_type}")

        self._engines[name] = engine
        return engine

    def watch_for_changes(self, callback: Callable):
        """Watch for config changes."""
        self._watchers.append(callback)

    def reload_engine(self, name: str):
        """Hot reload engine with new config."""
        if name in self._engines:
            # Cleanup old engine
            old_engine = self._engines[name]
            if hasattr(old_engine, 'cleanup'):
                old_engine.cleanup()

            # Create new engine
            config = self._configs[name]
            engine_type = config.get("type", "llm")
            self._engines[name] = self.create_engine(name, engine_type)
```

### 6. Usage Examples

```python
# Setup global registry
registry = GlobalEngineRegistry()

# Register configurations
registry.register_config("main_llm", {
    "type": "llm",
    "model": "gpt-4",
    "temperature": 0.7
})

registry.register_config("qa_prompt", {
    "type": "prompt",
    "templates": {
        "question": "Question: {question}\nContext: {context}\nAnswer:",
        "summary": "Summarize: {text}\nSummary:"
    }
})

registry.register_config("rag_pipeline", {
    "type": "pipeline",
    "stages": [
        {"name": "retrieve", "type": "retriever"},
        {"name": "prompt", "type": "prompt", "config": {"template": "question"}},
        {"name": "generate", "type": "llm"},
        {"name": "parse", "type": "parser"}
    ]
})

# Create state with proper engine management
state = ManagedStateSchema()

# Bind engines to state
state.bind_engine("llm", "main_llm")
state.bind_engine("prompt", "qa_prompt")
state.bind_engine("pipeline", "rag_pipeline")

# Use engines through state
llm = state.llm_engine
prompt = state.prompt_engine

# Or use pipeline
pipeline = state.get_engine("pipeline")
result = pipeline.create_runnable()(state)

# Hot reload support
def on_config_change(name: str, config: Dict):
    print(f"Config changed for {name}, reloading...")
    registry.reload_engine(name)

registry.watch_for_changes(on_config_change)
```

### 7. Advanced Patterns

```python
# Engine with state persistence
class StatefulEngine(Engine):
    """Engine that maintains state across calls."""

    def __init__(self):
        self._state_history: List[StateSchema] = []
        self._results_cache: Dict[str, Any] = {}

    def create_runnable(self) -> Callable:
        def run(state: StateSchema):
            # Cache key from state
            cache_key = self._get_cache_key(state)

            if cache_key in self._results_cache:
                return self._results_cache[cache_key]

            # Process and cache
            result = self._process(state)
            self._results_cache[cache_key] = result
            self._state_history.append(state)

            return result
        return run

# Engine with middleware
class MiddlewareEngine(Engine):
    """Engine with middleware support."""

    def __init__(self, base_engine: Engine):
        self.base_engine = base_engine
        self.middleware: List[Callable] = []

    def add_middleware(self, middleware: Callable):
        """Add middleware function."""
        self.middleware.append(middleware)

    def create_runnable(self) -> Callable:
        base_runnable = self.base_engine.create_runnable()

        def run(state: StateSchema):
            # Apply middleware in order
            for mw in self.middleware:
                state = mw(state)

            # Run base engine
            result = base_runnable(state)

            # Apply middleware to result
            for mw in reversed(self.middleware):
                if hasattr(mw, 'post_process'):
                    result = mw.post_process(result)

            return result
        return run
```

## 🎯 This Solves The Real Problems

1. **Proper Lifecycle**: Initialize, run, cleanup
2. **Dependency Management**: Engines can depend on each other
3. **State Integration**: Engines work WITH state, not against it
4. **Hot Reload**: Change configs without restart
5. **Composition**: Build complex engines from simple ones
6. **Caching**: Stateful engines for performance
7. **Middleware**: Add cross-cutting concerns

## 📊 Comparison

### Current (Bad) Engine Management

```python
# 74 methods doing everything badly
state.add_engine()
state.remove_engine()
state.setup_engines_and_tools()
state.sync_engine_fields()
# Circular dependencies everywhere
```

### Proper Engine Management

```python
# Clear separation of concerns
manager = EngineManager()
manager.register_engine("llm", factory=create_llm)
manager.initialize_engine("llm")

# State just binds to engines
state.bind_engine("llm", "llm")
llm = state.llm_engine  # Clean access
```

## 🚀 The Key Insight

We don't eliminate engine management - we do it PROPERLY:

- Engines are first-class citizens
- State and engines work together
- Clear lifecycle and dependencies
- Composable and reusable
- Hot reload for development

This is what StateSchema SHOULD have been doing with its 74 methods!
