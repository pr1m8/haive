# Engine Decomposition Implementation Plan

**Domain**: Engine Decomposition  
**Estimated Days**: 8-10 days  
**Target LOC**: 6,000 LOC (from 12,000 LOC - 50% reduction)  
**Dependencies**: [Contracts](../contracts/PROTOCOL_CONTRACTS_PLAN.md)

## 🎯 Overview

Break apart the monolithic `AugLLMConfig` (2,600 LOC) into specialized, focused configuration components. This is the highest-impact transformation that will unlock clean architecture throughout the system.

## 📊 Current State Analysis

### The Monolith Problem

**File**: `packages/haive-core/src/haive/core/engine/aug_llm/config.py`

- **2,647 lines of code** in single file
- **58 methods** handling everything from LLM config to tool management
- **Multiple responsibilities**: LLM settings, tool routing, structured output, validation, caching
- **15+ mixins** creating complex inheritance chains
- **Circular imports** with nodes, agents, and schema modules

### Current File Analysis

```bash
# Current engine structure (12,000 total LOC)
packages/haive-core/src/haive/core/engine/
├── aug_llm/
│   ├── config.py              # 2,647 LOC - THE MONSTER
│   ├── engine.py              # 1,200 LOC - Execution logic
│   └── __init__.py            # 50 LOC - Exports
├── tool/
│   ├── tool_engine.py         # 1,800 LOC - Tool management
│   ├── validation.py          # 900 LOC - Tool validation
│   └── routing.py            # 1,200 LOC - Tool routing
└── common/
    ├── base.py               # 800 LOC - Base engine
    ├── mixins.py            # 1,500 LOC - Multiple mixins
    └── utilities.py          # 900 LOC - Utilities
```

### Key Problems Identified

1. **Responsibility Overload**: Single class handles 8+ distinct concerns
2. **Import Cycles**: Engine → Node → Agent → Engine
3. **Testing Nightmare**: 2,600 LOC file is untestable in isolation
4. **Performance Issues**: Massive object instantiation overhead
5. **Maintenance Hell**: Any change requires understanding entire system

## 🏗️ Target Architecture

### Decomposed Structure (6,000 total LOC)

```
packages/haive-core/src/haive/core/engine/
├── configs/                          # Specialized configurations
│   ├── __init__.py                  # Config exports (50 LOC)
│   ├── llm_config.py                # Pure LLM configuration (300 LOC)
│   ├── tool_config.py               # Tool management config (400 LOC)
│   ├── structured_config.py         # Structured output config (200 LOC)
│   ├── validation_config.py         # Validation rules config (150 LOC)
│   ├── caching_config.py            # Caching configuration (100 LOC)
│   └── composite_config.py          # Config composition (200 LOC)
├── providers/                        # LLM provider implementations
│   ├── __init__.py                  # Provider exports (30 LOC)
│   ├── openai_provider.py           # OpenAI implementation (400 LOC)
│   ├── anthropic_provider.py        # Anthropic implementation (350 LOC)
│   ├── azure_provider.py            # Azure implementation (300 LOC)
│   └── base_provider.py             # Provider protocol (150 LOC)
├── execution/                        # Execution engines
│   ├── __init__.py                  # Execution exports (30 LOC)
│   ├── llm_engine.py               # Pure LLM execution (500 LOC)
│   ├── tool_engine.py              # Tool execution (600 LOC)
│   ├── composite_engine.py         # Combined execution (400 LOC)
│   └── async_engine.py             # Async execution wrapper (300 LOC)
├── routing/                          # Tool routing logic
│   ├── __init__.py                  # Routing exports (30 LOC)
│   ├── route_detector.py           # Route detection (250 LOC)
│   ├── route_registry.py           # Route management (200 LOC)
│   └── route_validator.py          # Route validation (150 LOC)
└── legacy/                          # Backward compatibility
    ├── __init__.py                  # Legacy exports (30 LOC)
    ├── aug_llm_facade.py           # AugLLMConfig facade (500 LOC)
    └── migration_guide.md           # Migration documentation
```

**Total**: 24 files, ~6,000 LOC (50% reduction)

## 📋 Detailed Implementation Steps

### Step 1: Extract LLM Configuration (Days 1-2)

#### 1.1 Create Pure LLM Config

**File**: `configs/llm_config.py`

```python
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from enum import Enum

class LLMProvider(str, Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    AZURE_OPENAI = "azure_openai"
    OLLAMA = "ollama"

class LLMConfig(BaseModel):
    """Pure LLM configuration without tool coupling."""

    # Core LLM settings
    provider: LLMProvider = Field(default=LLMProvider.OPENAI)
    model: str = Field(default="gpt-4")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=None, ge=1)
    top_p: float = Field(default=1.0, ge=0.0, le=1.0)
    frequency_penalty: float = Field(default=0.0, ge=-2.0, le=2.0)
    presence_penalty: float = Field(default=0.0, ge=-2.0, le=2.0)

    # Provider-specific settings
    provider_settings: Dict[str, Any] = Field(default_factory=dict)

    # System message
    system_message: Optional[str] = Field(default=None)

    # Request settings
    timeout_seconds: int = Field(default=60, gt=0)
    max_retries: int = Field(default=3, ge=0)

    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        extra = "forbid"

    def to_provider_params(self) -> Dict[str, Any]:
        """Convert to provider-specific parameters."""
        base_params = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
        }

        # Add provider-specific params
        if self.provider == LLMProvider.OPENAI:
            base_params.update({
                "frequency_penalty": self.frequency_penalty,
                "presence_penalty": self.presence_penalty,
            })

        # Merge provider settings
        base_params.update(self.provider_settings)
        return base_params
```

#### 1.2 Create Tool Configuration

**File**: `configs/tool_config.py`

```python
from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field
from haive.core.contracts.engine.tool_protocol import ToolProtocol, ToolMetadata

ToolType = Union[ToolProtocol, Any]  # Any for backward compatibility

class ToolConfig(BaseModel):
    """Tool management configuration."""

    # Tool registry
    tools: List[ToolType] = Field(default_factory=list)
    tool_routes: Dict[str, str] = Field(default_factory=dict)
    tool_metadata: Dict[str, ToolMetadata] = Field(default_factory=dict)

    # Execution settings
    tool_timeout_seconds: int = Field(default=30, gt=0)
    max_tool_calls: int = Field(default=10, gt=0)
    allow_parallel_tools: bool = Field(default=False)

    # Validation settings
    validate_tool_inputs: bool = Field(default=True)
    validate_tool_outputs: bool = Field(default=True)
    strict_tool_routing: bool = Field(default=True)

    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True  # Allow ToolProtocol objects
        extra = "forbid"

    def add_tool(self, tool: ToolType, name: Optional[str] = None, route: Optional[str] = None) -> None:
        """Add tool with automatic route detection."""
        tool_name = name or getattr(tool, 'name', str(tool))

        if tool not in self.tools:
            self.tools.append(tool)

        # Auto-detect route if not provided
        if route is None:
            route = self._detect_tool_route(tool)

        self.tool_routes[tool_name] = route
        self.tool_metadata[tool_name] = self._extract_tool_metadata(tool)

    def remove_tool(self, name: str) -> None:
        """Remove tool by name."""
        # Find and remove tool
        tool_to_remove = None
        for tool in self.tools:
            if getattr(tool, 'name', str(tool)) == name:
                tool_to_remove = tool
                break

        if tool_to_remove:
            self.tools.remove(tool_to_remove)
            self.tool_routes.pop(name, None)
            self.tool_metadata.pop(name, None)

    def get_tool_names(self) -> List[str]:
        """Get all registered tool names."""
        return list(self.tool_routes.keys())

    def _detect_tool_route(self, tool: ToolType) -> str:
        """Detect appropriate route for tool."""
        # Import here to avoid circular imports
        from haive.core.engine.routing.route_detector import detect_tool_route
        return detect_tool_route(tool)

    def _extract_tool_metadata(self, tool: ToolType) -> ToolMetadata:
        """Extract metadata from tool."""
        # Import here to avoid circular imports
        from haive.core.engine.routing.route_detector import extract_tool_metadata
        return extract_tool_metadata(tool)
```

### Step 2: Extract Structured Output Configuration (Day 3)

#### 2.1 Structured Output Config

**File**: `configs/structured_config.py`

```python
from typing import Optional, Type, Dict, Any, Union
from pydantic import BaseModel, Field

StructuredModelType = Union[Type[BaseModel], BaseModel, None]

class StructuredConfig(BaseModel):
    """Configuration for structured output generation."""

    # Core structured output settings
    structured_output_model: StructuredModelType = Field(default=None)
    output_format: str = Field(default="json", pattern=r"^(json|yaml|xml)$")
    strict_mode: bool = Field(default=True)

    # Validation settings
    validate_output: bool = Field(default=True)
    retry_on_validation_error: bool = Field(default=True)
    max_validation_retries: int = Field(default=3, ge=0)

    # Schema generation
    include_schema_in_prompt: bool = Field(default=True)
    schema_format: str = Field(default="json_schema")

    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True
        extra = "forbid"

    def get_structured_model_name(self) -> Optional[str]:
        """Get the name of structured model."""
        if self.structured_output_model is None:
            return None

        if isinstance(self.structured_output_model, type):
            return self.structured_output_model.__name__
        else:
            return self.structured_output_model.__class__.__name__

    def generate_schema(self) -> Optional[Dict[str, Any]]:
        """Generate JSON schema for structured model."""
        if self.structured_output_model is None:
            return None

        if isinstance(self.structured_output_model, type):
            return self.structured_output_model.model_json_schema()
        else:
            return self.structured_output_model.__class__.model_json_schema()

    def validate_structured_output(self, output: Any) -> Any:
        """Validate output against structured model."""
        if self.structured_output_model is None:
            return output

        if not self.validate_output:
            return output

        # Perform validation
        if isinstance(self.structured_output_model, type):
            return self.structured_output_model.model_validate(output)
        else:
            return self.structured_output_model.__class__.model_validate(output)
```

### Step 3: Create Composite Configuration (Day 4)

#### 3.1 Composite Config

**File**: `configs/composite_config.py`

```python
from typing import Optional
from pydantic import BaseModel, Field
from .llm_config import LLMConfig
from .tool_config import ToolConfig
from .structured_config import StructuredConfig
from .validation_config import ValidationConfig
from .caching_config import CachingConfig

class CompositeEngineConfig(BaseModel):
    """Composite configuration combining all engine aspects."""

    # Component configurations
    llm: LLMConfig = Field(default_factory=LLMConfig)
    tools: ToolConfig = Field(default_factory=ToolConfig)
    structured: StructuredConfig = Field(default_factory=StructuredConfig)
    validation: ValidationConfig = Field(default_factory=ValidationConfig)
    caching: CachingConfig = Field(default_factory=CachingConfig)

    # Global settings
    name: str = Field(default="composite_engine")
    debug: bool = Field(default=False)

    class Config:
        """Pydantic configuration."""
        extra = "forbid"

    def configure_llm(self, **kwargs) -> None:
        """Configure LLM settings."""
        for key, value in kwargs.items():
            if hasattr(self.llm, key):
                setattr(self.llm, key, value)

    def configure_tools(self, **kwargs) -> None:
        """Configure tool settings."""
        for key, value in kwargs.items():
            if hasattr(self.tools, key):
                setattr(self.tools, key, value)

    def configure_structured(self, **kwargs) -> None:
        """Configure structured output settings."""
        for key, value in kwargs.items():
            if hasattr(self.structured, key):
                setattr(self.structured, key, value)

    def add_tool(self, tool, name: Optional[str] = None, route: Optional[str] = None) -> None:
        """Add tool to configuration."""
        self.tools.add_tool(tool, name, route)

    def with_structured_output(self, model_class):
        """Set structured output model."""
        self.structured.structured_output_model = model_class
        return self

    def to_legacy_format(self) -> dict:
        """Convert to AugLLMConfig-compatible format."""
        return {
            # LLM settings
            "model": self.llm.model,
            "temperature": self.llm.temperature,
            "max_tokens": self.llm.max_tokens,
            "system_message": self.llm.system_message,

            # Tool settings
            "tools": self.tools.tools,
            "tool_routes": self.tools.tool_routes,

            # Structured output
            "structured_output_model": self.structured.structured_output_model,

            # Other settings
            "debug": self.debug,
        }
```

### Step 4: Create Execution Engines (Days 5-6)

#### 4.1 LLM Execution Engine

**File**: `execution/llm_engine.py`

```python
from typing import Any, Dict, List, Optional
from haive.core.contracts.engine.engine_protocol import EngineProtocol
from ..configs.llm_config import LLMConfig
from ..providers.base_provider import LLMProvider

class LLMExecutionEngine(EngineProtocol[LLMConfig, Dict[str, Any], str]):
    """Pure LLM execution without tool coupling."""

    def __init__(self, config: LLMConfig):
        self._config = config
        self._provider = self._create_provider()

    @property
    def config(self) -> LLMConfig:
        """Get current configuration."""
        return self._config

    def configure(self, **kwargs) -> None:
        """Update configuration."""
        for key, value in kwargs.items():
            if hasattr(self._config, key):
                setattr(self._config, key, value)

        # Recreate provider if needed
        self._provider = self._create_provider()

    async def arun(self, state: Dict[str, Any]) -> str:
        """Execute LLM with given state."""
        messages = state.get("messages", [])

        # Add system message if configured
        if self._config.system_message:
            system_msg = {"role": "system", "content": self._config.system_message}
            messages = [system_msg] + messages

        # Execute with provider
        response = await self._provider.agenerate(
            messages=messages,
            **self._config.to_provider_params()
        )

        return response.content

    def run(self, state: Dict[str, Any]) -> str:
        """Execute LLM synchronously."""
        import asyncio
        return asyncio.run(self.arun(state))

    def _create_provider(self) -> LLMProvider:
        """Create appropriate provider based on config."""
        from ..providers import get_provider
        return get_provider(self._config.provider, self._config.provider_settings)
```

#### 4.2 Tool Execution Engine

**File**: `execution/tool_engine.py`

```python
from typing import Any, Dict, List
from haive.core.contracts.engine.engine_protocol import EngineProtocol, ToolExecutionResult
from ..configs.tool_config import ToolConfig
from ..routing.route_registry import RouteRegistry

class ToolExecutionEngine(EngineProtocol[ToolConfig, Dict[str, Any], List[ToolExecutionResult]]):
    """Dedicated tool execution engine."""

    def __init__(self, config: ToolConfig):
        self._config = config
        self._route_registry = RouteRegistry()
        self._sync_routes()

    @property
    def config(self) -> ToolConfig:
        """Get current configuration."""
        return self._config

    def configure(self, **kwargs) -> None:
        """Update configuration."""
        for key, value in kwargs.items():
            if hasattr(self._config, key):
                setattr(self._config, key, value)
        self._sync_routes()

    def add_tool(self, tool: Any, name: Optional[str] = None) -> None:
        """Add tool to engine."""
        self._config.add_tool(tool, name)
        self._sync_routes()

    def remove_tool(self, name: str) -> None:
        """Remove tool from engine."""
        self._config.remove_tool(name)
        self._sync_routes()

    async def arun(self, state: Dict[str, Any]) -> List[ToolExecutionResult]:
        """Execute tools based on state."""
        tool_calls = state.get("tool_calls", [])
        results = []

        for call in tool_calls:
            result = await self._execute_single_tool(call)
            results.append(result)

        return results

    def run(self, state: Dict[str, Any]) -> List[ToolExecutionResult]:
        """Execute tools synchronously."""
        import asyncio
        return asyncio.run(self.arun(state))

    async def _execute_single_tool(self, tool_call: Dict[str, Any]) -> ToolExecutionResult:
        """Execute a single tool call."""
        import time

        tool_name = tool_call["name"]
        tool_input = tool_call.get("input", {})

        start_time = time.time()

        try:
            # Get route and execute
            route = self._config.tool_routes.get(tool_name)
            output = await self._route_registry.execute_route(route, tool_name, tool_input)

            execution_time_ms = int((time.time() - start_time) * 1000)

            return ToolExecutionResult(
                tool_name=tool_name,
                input=tool_input,
                output=output,
                execution_time_ms=execution_time_ms,
                success=True,
                error=None
            )

        except Exception as e:
            execution_time_ms = int((time.time() - start_time) * 1000)

            return ToolExecutionResult(
                tool_name=tool_name,
                input=tool_input,
                output=None,
                execution_time_ms=execution_time_ms,
                success=False,
                error=str(e)
            )

    def _sync_routes(self) -> None:
        """Synchronize routes with registry."""
        self._route_registry.clear()

        for tool_name, route in self._config.tool_routes.items():
            tool = self._find_tool_by_name(tool_name)
            if tool:
                self._route_registry.register_route(route, tool_name, tool)

    def _find_tool_by_name(self, name: str) -> Any:
        """Find tool by name."""
        for tool in self._config.tools:
            tool_name = getattr(tool, 'name', str(tool))
            if tool_name == name:
                return tool
        return None
```

### Step 5: Create Backward Compatibility Layer (Day 7)

#### 5.1 AugLLMConfig Facade

**File**: `legacy/aug_llm_facade.py`

```python
from typing import Any, Dict, List, Optional
from ..configs.composite_config import CompositeEngineConfig
from ..execution.composite_engine import CompositeExecutionEngine

class AugLLMConfig:
    """Backward compatibility facade for AugLLMConfig.

    This class provides the same interface as the original AugLLMConfig
    but delegates to the new decomposed architecture.
    """

    def __init__(self, **kwargs):
        """Initialize with legacy parameters."""
        # Create composite config
        self._config = CompositeEngineConfig()

        # Map legacy parameters to new structure
        self._map_legacy_params(kwargs)

        # Create execution engine
        self._engine = CompositeExecutionEngine(self._config)

    def _map_legacy_params(self, params: Dict[str, Any]) -> None:
        """Map legacy parameters to new configuration structure."""

        # LLM parameters
        llm_params = {}
        for key in ["model", "temperature", "max_tokens", "system_message", "provider"]:
            if key in params:
                llm_params[key] = params[key]

        if llm_params:
            self._config.configure_llm(**llm_params)

        # Tool parameters
        if "tools" in params:
            for tool in params["tools"]:
                self._config.add_tool(tool)

        # Structured output
        if "structured_output_model" in params:
            self._config.configure_structured(
                structured_output_model=params["structured_output_model"]
            )

        # Debug mode
        if "debug" in params:
            self._config.debug = params["debug"]

    # Legacy property accessors
    @property
    def model(self) -> str:
        return self._config.llm.model

    @model.setter
    def model(self, value: str) -> None:
        self._config.llm.model = value

    @property
    def temperature(self) -> float:
        return self._config.llm.temperature

    @temperature.setter
    def temperature(self, value: float) -> None:
        self._config.llm.temperature = value

    @property
    def tools(self) -> List[Any]:
        return self._config.tools.tools

    @property
    def tool_routes(self) -> Dict[str, str]:
        return self._config.tools.tool_routes

    # Legacy methods
    def add_tool(self, tool: Any, name: Optional[str] = None, route: Optional[str] = None) -> "AugLLMConfig":
        """Add tool (legacy interface)."""
        self._config.add_tool(tool, name, route)
        return self

    def with_structured_output(self, model_class: Any) -> "AugLLMConfig":
        """Set structured output model (legacy interface)."""
        self._config.with_structured_output(model_class)
        return self

    async def arun(self, state: Dict[str, Any]) -> Any:
        """Execute engine (legacy interface)."""
        return await self._engine.arun(state)

    def run(self, state: Dict[str, Any]) -> Any:
        """Execute engine synchronously (legacy interface)."""
        return self._engine.run(state)

    # Additional legacy methods as needed...
```

### Step 6: Integration & Testing (Days 8-10)

#### 6.1 Comprehensive Testing Strategy

**Unit Tests**: Test each config class in isolation

```python
# tests/engine/configs/test_llm_config.py
import pytest
from haive.core.engine.configs.llm_config import LLMConfig, LLMProvider

class TestLLMConfig:
    def test_default_configuration(self):
        """Test default LLM configuration."""
        config = LLMConfig()
        assert config.provider == LLMProvider.OPENAI
        assert config.model == "gpt-4"
        assert config.temperature == 0.7
        assert config.system_message is None

    def test_provider_params_generation(self):
        """Test provider parameter generation."""
        config = LLMConfig(
            model="gpt-4-turbo",
            temperature=0.5,
            max_tokens=1000
        )

        params = config.to_provider_params()
        assert params["model"] == "gpt-4-turbo"
        assert params["temperature"] == 0.5
        assert params["max_tokens"] == 1000

    def test_validation(self):
        """Test configuration validation."""
        with pytest.raises(ValueError):
            LLMConfig(temperature=3.0)  # Too high

        with pytest.raises(ValueError):
            LLMConfig(max_tokens=0)  # Too low
```

**Integration Tests**: Test component interactions

```python
# tests/engine/integration/test_composite_config.py
import pytest
from haive.core.engine.configs.composite_config import CompositeEngineConfig

class TestCompositeConfig:
    def test_component_interaction(self):
        """Test interaction between config components."""
        config = CompositeEngineConfig()

        # Configure LLM
        config.configure_llm(model="gpt-4", temperature=0.8)
        assert config.llm.model == "gpt-4"
        assert config.llm.temperature == 0.8

        # Add tool
        def dummy_tool(x): return x
        config.add_tool(dummy_tool, name="test_tool")
        assert "test_tool" in config.tools.tool_routes

    def test_legacy_compatibility(self):
        """Test backward compatibility with legacy format."""
        config = CompositeEngineConfig()
        config.configure_llm(model="gpt-4")

        legacy_format = config.to_legacy_format()
        assert legacy_format["model"] == "gpt-4"
        assert "tools" in legacy_format
```

**System Tests**: Test full execution flow

```python
# tests/engine/system/test_engine_execution.py
import pytest
from haive.core.engine.execution.composite_engine import CompositeExecutionEngine
from haive.core.engine.configs.composite_config import CompositeEngineConfig

@pytest.mark.asyncio
class TestEngineExecution:
    async def test_llm_only_execution(self):
        """Test pure LLM execution."""
        config = CompositeEngineConfig()
        config.configure_llm(model="gpt-3.5-turbo", temperature=0.1)

        engine = CompositeExecutionEngine(config)

        state = {
            "messages": [
                {"role": "user", "content": "Hello, world!"}
            ]
        }

        result = await engine.arun(state)
        assert isinstance(result, str)
        assert len(result) > 0

    async def test_tool_execution(self):
        """Test tool execution flow."""
        def calculator(expression: str) -> str:
            return str(eval(expression))

        config = CompositeEngineConfig()
        config.add_tool(calculator, name="calc")

        engine = CompositeExecutionEngine(config)

        state = {
            "tool_calls": [
                {"name": "calc", "input": {"expression": "2 + 2"}}
            ]
        }

        results = await engine.arun(state)
        assert len(results) == 1
        assert results[0]["output"] == "4"
```

## 🧪 Testing Strategy

### 1. Property-Based Testing (Hypothesis)

```python
from hypothesis import given, strategies as st

@given(
    temperature=st.floats(min_value=0.0, max_value=2.0),
    max_tokens=st.integers(min_value=1, max_value=4000)
)
def test_llm_config_properties(temperature, max_tokens):
    """Property-based testing for LLM config."""
    config = LLMConfig(temperature=temperature, max_tokens=max_tokens)

    # Properties that should always hold
    assert 0.0 <= config.temperature <= 2.0
    assert config.max_tokens >= 1

    params = config.to_provider_params()
    assert params["temperature"] == temperature
    assert params["max_tokens"] == max_tokens
```

### 2. Golden Tests

Create known-good configuration outputs and validate against them:

```python
# tests/engine/golden/test_golden_configs.py
def test_golden_llm_config():
    """Test against golden LLM configuration."""
    config = LLMConfig(model="gpt-4", temperature=0.7)

    expected = {
        "model": "gpt-4",
        "temperature": 0.7,
        "max_tokens": None,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
    }

    assert config.to_provider_params() == expected
```

### 3. Performance Testing

```python
import time
import pytest

def test_config_instantiation_performance():
    """Test configuration instantiation performance."""
    start_time = time.time()

    for _ in range(1000):
        config = CompositeEngineConfig()

    end_time = time.time()
    avg_time_ms = (end_time - start_time) * 1000 / 1000

    # Should be fast - target <1ms per instantiation
    assert avg_time_ms < 1.0
```

## 📊 Success Metrics

### Technical Metrics

- [ ] **50% LOC reduction** (12,000 → 6,000 LOC)
- [ ] **Zero circular imports** between engine components
- [ ] **100% test coverage** for all new config classes
- [ ] **<1ms config instantiation** time (vs current ~50ms)
- [ ] **Single responsibility** - each config handles one concern

### Quality Metrics

- [ ] **All existing functionality preserved** through facade layer
- [ ] **Clean dependency graph** with proper separation
- [ ] **Performance improvements** in engine startup
- [ ] **Maintainable code** with focused, testable components

### Developer Experience

- [ ] **Migration guide** for existing code
- [ ] **Clear examples** for each configuration type
- [ ] **Comprehensive documentation** for all components
- [ ] **IDE support** with proper type hints

## 🔗 Integration Points

### With Contracts Domain

- All configs implement appropriate protocols
- Engine execution follows `EngineProtocol` interface
- Tool management via `ToolProtocol` contracts

### With Node Domain

- Execution engines used by graph nodes
- Configuration passed through node execution
- Tool routing coordinates with node validation

### With Agent Domain

- Agents use composite configurations
- Agent-specific config profiles
- Backward compatibility for existing agent code

### With Schema Domain

- Configuration schemas for validation
- State schemas for execution
- Message schemas for LLM communication

## 🚨 Common Pitfalls

### 1. Leaky Abstractions

**Problem**: Configuration details bleeding into execution logic
**Solution**: Strict interface adherence and protocol testing

### 2. Circular Dependencies

**Problem**: New components importing each other
**Solution**: Use protocols and dependency injection

### 3. Performance Regression

**Problem**: Multiple small objects slower than monolith
**Solution**: Object pooling and lazy initialization

### 4. Backward Compatibility Breaks

**Problem**: Existing code breaks during transition
**Solution**: Comprehensive facade layer and gradual migration

## 🔄 Rollback Strategy

### If Performance Issues Arise

1. **Isolate problem component**: Each config is independent
2. **Revert to monolith**: Keep original AugLLMConfig as fallback
3. **Gradual rollback**: Revert one component at a time
4. **Performance profiling**: Identify and fix bottlenecks

### Risk Mitigation

- Maintain original AugLLMConfig alongside new system
- Feature flags to switch between implementations
- Comprehensive performance benchmarking
- Gradual migration with rollback points

---

**Next Steps**:

1. Start with LLMConfig extraction (lowest risk)
2. Add comprehensive testing for each component
3. Build facade layer for backward compatibility
4. Validate performance improvements
