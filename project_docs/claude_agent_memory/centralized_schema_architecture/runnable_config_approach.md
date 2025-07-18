# RunnableConfig-Based Engine Configuration

**Date**: 2025-06-28
**Focus**: Using RunnableConfig pattern for engine configuration instead of separate config fields

## Current RunnableConfig Infrastructure

### **What Already Exists**

```python
# From runnable.py - Already implemented!
class RunnableConfigManager:
    @staticmethod
    def create(thread_id=None, user_id=None, **kwargs) -> RunnableConfig:
        """Create standardized RunnableConfig."""
        configurable = {
            "thread_id": thread_id or str(uuid.uuid4()),
            "engine_configs": {}  # Already has engine_configs!
        }
        return {"configurable": configurable}

    @staticmethod
    def add_engine_config(config, engine_name, **engine_params):
        """Add engine-specific configuration."""
        # This pattern already exists!
```

### **Current EngineNodeConfig Usage**

```python
# Lines 729-753 in engine_node.py - Already using this pattern!
def _build_merged_config(self, runtime_config, engine):
    """Build merged configuration."""
    config = dict(runtime_config or {})
    config.setdefault("configurable", {})

    # Apply node-level overrides
    config["configurable"].update(self.config_overrides)

    # Apply engine-specific overrides
    engine_id = getattr(engine, "id", None)
    if engine_id and self.config_overrides:
        config["configurable"].setdefault("engine_configs", {})
        config["configurable"]["engine_configs"].setdefault(engine_id, {})
        config["configurable"]["engine_configs"][engine_id].update(self.config_overrides)
```

## The Enhanced Approach

### **1. Remove Engine-Specific Config Fields from NodeConfig**

```python
class EngineNodeConfig(NodeConfig):
    # REMOVE these fields (they belong in RunnableConfig now):
    # temperature: float | None = Field(default=None)
    # max_tokens: int | None = Field(default=None)
    # model_name: str | None = Field(default=None)
    # tools: list[Any] | None = Field(default=None)

    # KEEP only core node fields:
    engine: Engine | None = Field(default=None)
    engine_name: str | None = Field(default=None)

    # Enhanced config building
    def build_engine_config(self, base_config: RunnableConfig | None = None) -> RunnableConfig:
        """Build RunnableConfig with engine-specific parameters."""

        # Start with base config or create new
        if base_config:
            config = copy.deepcopy(base_config)
        else:
            config = RunnableConfigManager.create()

        # Get engine for configuration
        engine = self._get_engine_for_config()
        if not engine:
            return config

        # Add engine-specific config using engine ID/name
        engine_key = getattr(engine, 'id', None) or getattr(engine, 'name', 'default')

        # Build engine parameters from engine's configurable fields
        engine_params = self._extract_engine_configurable_params(engine)

        if engine_params:
            config = RunnableConfigManager.add_engine_config(
                config,
                engine_key,
                **engine_params
            )

        return config

    def _extract_engine_configurable_params(self, engine: Engine) -> dict[str, Any]:
        """Extract configurable parameters from engine."""
        params = {}

        # LLM-specific parameters
        if hasattr(engine, 'engine_type') and engine.engine_type == EngineType.LLM:
            if hasattr(engine, 'temperature') and engine.temperature is not None:
                params['temperature'] = engine.temperature
            if hasattr(engine, 'max_tokens') and engine.max_tokens is not None:
                params['max_tokens'] = engine.max_tokens
            if hasattr(engine, 'model') and engine.model is not None:
                params['model'] = engine.model

        # Retriever-specific parameters
        elif hasattr(engine, 'engine_type') and engine.engine_type == EngineType.RETRIEVER:
            if hasattr(engine, 'k') and engine.k is not None:
                params['k'] = engine.k
            if hasattr(engine, 'search_type') and engine.search_type is not None:
                params['search_type'] = engine.search_type
            if hasattr(engine, 'score_threshold') and engine.score_threshold is not None:
                params['score_threshold'] = engine.score_threshold

        return params
```

### **2. Enhanced RunnableConfigManager**

```python
class RunnableConfigManager:
    # Existing methods stay the same...

    @staticmethod
    def add_engine_config(
        config: RunnableConfig,
        engine_name: str,
        **engine_params
    ) -> RunnableConfig:
        """Add engine-specific configuration parameters."""
        config = copy.deepcopy(config)

        # Ensure structure exists
        config.setdefault("configurable", {})
        config["configurable"].setdefault("engine_configs", {})

        # Add engine parameters
        config["configurable"]["engine_configs"][engine_name] = engine_params

        return config

    @staticmethod
    def get_engine_config(config: RunnableConfig, engine_name: str) -> dict[str, Any]:
        """Extract engine-specific configuration."""
        return (
            config.get("configurable", {})
            .get("engine_configs", {})
            .get(engine_name, {})
        )

    @staticmethod
    def merge_engine_configs(
        base_config: RunnableConfig,
        runtime_config: RunnableConfig
    ) -> RunnableConfig:
        """Merge engine configurations from multiple sources."""
        merged = copy.deepcopy(base_config)

        runtime_engine_configs = (
            runtime_config.get("configurable", {})
            .get("engine_configs", {})
        )

        for engine_name, params in runtime_engine_configs.items():
            merged = RunnableConfigManager.add_engine_config(
                merged, engine_name, **params
            )

        return merged

    @staticmethod
    def create_for_engine_type(
        engine_type: EngineType,
        thread_id: str | None = None,
        **engine_params
    ) -> RunnableConfig:
        """Create config optimized for specific engine type."""
        config = RunnableConfigManager.create(thread_id=thread_id)

        # Add engine-type-specific defaults
        if engine_type == EngineType.LLM:
            defaults = {
                "temperature": 0.7,
                "max_tokens": 1000,
                "stream": False
            }
            defaults.update(engine_params)
            config = RunnableConfigManager.add_engine_config(
                config, "default_llm", **defaults
            )

        elif engine_type == EngineType.RETRIEVER:
            defaults = {
                "k": 5,
                "search_type": "similarity",
                "score_threshold": 0.0
            }
            defaults.update(engine_params)
            config = RunnableConfigManager.add_engine_config(
                config, "default_retriever", **defaults
            )

        return config
```

### **3. Engine-Aware Execution**

```python
class EngineNodeConfig(NodeConfig):
    def __call__(self, state, config=None):
        """Execute with enhanced config management."""

        # Build engine-specific config
        engine_config = self.build_engine_config(config)

        # Get engine
        engine = self._get_engine(state)
        if not engine:
            raise ValueError(f"No engine available for {self.name}")

        # Extract input with computed field validation
        validated_input = self._extract_and_validate_input(state, engine)

        # Execute with engine-aware config
        result = engine.invoke(validated_input, engine_config)

        # Wrap result
        return self._wrap_smart_result(result, state, engine)

    def _extract_and_validate_input(self, state, engine):
        """Extract and validate input using computed field schemas."""
        # Use existing smart extraction
        raw_input = self._extract_smart_input(state, engine)

        # Try engine schema validation if available
        if hasattr(engine, 'input_schema') and engine.input_schema:
            try:
                validated = engine.input_schema(**raw_input)
                return validated.model_dump()
            except ValidationError as e:
                logger.warning(f"Engine schema validation failed: {e}")

        return raw_input
```

### **4. Agent-Level Config Management**

```python
class Agent:
    def create_runnable(self, runnable_config=None):
        """Enhanced runnable creation with engine configs."""

        # Build base config from agent engines
        agent_config = self._build_agent_config(runnable_config)

        # Compile graph with enhanced config
        compiled = super().create_runnable(agent_config)

        return compiled

    def _build_agent_config(self, base_config=None):
        """Build agent config with all engine configurations."""
        if base_config:
            config = copy.deepcopy(base_config)
        else:
            config = RunnableConfigManager.create()

        # Add each engine's configuration
        for engine_name, engine in self.engines.items():
            engine_params = self._extract_engine_runtime_params(engine)
            if engine_params:
                config = RunnableConfigManager.add_engine_config(
                    config, engine_name, **engine_params
                )

        return config

    def _extract_engine_runtime_params(self, engine):
        """Extract runtime parameters from engine."""
        params = {}

        # Extract based on engine type
        if hasattr(engine, 'engine_type'):
            if engine.engine_type == EngineType.LLM:
                for param in ['temperature', 'max_tokens', 'model', 'stream']:
                    if hasattr(engine, param):
                        value = getattr(engine, param)
                        if value is not None:
                            params[param] = value

            elif engine.engine_type == EngineType.RETRIEVER:
                for param in ['k', 'search_type', 'score_threshold']:
                    if hasattr(engine, param):
                        value = getattr(engine, param)
                        if value is not None:
                            params[param] = value

        return params
```

### **5. Factory Functions for Clean Usage**

```python
def create_llm_node_with_config(
    engine: LLMEngine,
    name: str,
    temperature: float = 0.7,
    max_tokens: int = 1000,
    **kwargs
) -> EngineNodeConfig:
    """Create LLM node with configuration."""

    # Create base config for this engine type
    base_config = RunnableConfigManager.create_for_engine_type(
        EngineType.LLM,
        temperature=temperature,
        max_tokens=max_tokens,
        **kwargs
    )

    # Create node
    node = EngineNodeConfig(name=name, engine=engine)

    # Store config on node for later use
    node._base_config = base_config

    return node

def create_retriever_node_with_config(
    engine: RetrieverEngine,
    name: str,
    k: int = 5,
    search_type: str = "similarity",
    **kwargs
) -> EngineNodeConfig:
    """Create retriever node with configuration."""

    base_config = RunnableConfigManager.create_for_engine_type(
        EngineType.RETRIEVER,
        k=k,
        search_type=search_type,
        **kwargs
    )

    node = EngineNodeConfig(name=name, engine=engine)
    node._base_config = base_config

    return node
```

## Benefits of RunnableConfig Approach

### **1. Clean Separation of Concerns**

```python
# Node handles execution logic
node = EngineNodeConfig(name="llm", engine=llm_engine)

# Config handles runtime parameters
config = RunnableConfigManager.create_for_engine_type(
    EngineType.LLM,
    temperature=0.8,
    max_tokens=500
)
```

### **2. Runtime Configuration Override**

```python
# Base configuration
base_config = agent.create_base_config()

# Runtime override
runtime_config = RunnableConfigManager.add_engine_config(
    base_config,
    "my_llm",
    temperature=0.9  # Override for this execution
)

result = agent.run(input_data, config=runtime_config)
```

### **3. LangGraph Standard Pattern**

```python
# Follows LangGraph conventions
compiled_graph = graph.compile(
    checkpointer=checkpointer,
    store=store
)

result = compiled_graph.invoke(
    input_data,
    config=runnable_config  # Standard LangGraph pattern
)
```

### **4. Engine-Type-Specific Defaults**

```python
# Different defaults per engine type
llm_config = RunnableConfigManager.create_for_engine_type(
    EngineType.LLM,  # Gets LLM defaults
    temperature=0.7
)

retriever_config = RunnableConfigManager.create_for_engine_type(
    EngineType.RETRIEVER,  # Gets retriever defaults
    k=10
)
```

This approach leverages the **existing RunnableConfig infrastructure** and **removes configuration mixing** from node classes while providing **engine-type-specific configuration management**!
