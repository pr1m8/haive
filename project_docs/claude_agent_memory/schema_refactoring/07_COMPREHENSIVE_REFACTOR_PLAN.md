# Comprehensive Schema System Refactoring Plan

## Overview

This plan addresses **ALL CRITICAL ISSUES** identified in the haive-core schema system:

- Monolithic schema classes and over-engineered compatibility
- Agent-graph-node config integration chaos
- Engine lookup pattern inconsistencies (3 different approaches)
- Mixin fragmentation and location inconsistencies
- Missing Pydantic type adaptation and model alias support
- Tool routing brittleness and hardcoded configurations

## Refactoring Strategy: Complete System Redesign

### **Core Approach: schema_test Module with Parallel Implementation**

1. **Build entirely new system** in `schema_test/` alongside existing code
2. **Adapter layer** provides 100% backwards compatibility
3. **Feature flag system** enables gradual migration
4. **Address ALL issues simultaneously** for cohesive architecture

## New Architecture Structure

```
packages/haive-core/src/haive/core/schema_test/
├── core/                          # Core component system
│   ├── interfaces/                # Standard contracts
│   │   ├── engine_provider.py     # Engine access interface
│   │   ├── tool_provider.py       # Tool access interface
│   │   ├── type_adapter.py        # Type conversion interface
│   │   ├── route_registry.py      # Route management interface
│   │   └── model_registry.py      # Pydantic model interface
│   ├── components/                # Single-responsibility components
│   │   ├── engine_manager.py      # Unified engine access
│   │   ├── tool_manager.py        # Unified tool management
│   │   ├── type_adapter.py        # Centralized type conversion
│   │   ├── route_manager.py       # Standardized routing
│   │   ├── model_registry.py      # Pydantic model handling
│   │   ├── field_manager.py       # Field definition and sharing
│   │   └── serialization.py       # JSON/dict conversion
│   ├── mixins/                    # Consistent mixin system
│   │   ├── engine_access.py       # Standard engine access mixin
│   │   ├── tool_routing.py        # Standard tool routing mixin
│   │   ├── type_conversion.py     # Standard type conversion mixin
│   │   ├── model_handling.py      # Pydantic model mixin
│   │   └── validation.py          # Standard validation mixin
│   └── schemas/                   # Clean schema implementations
│       ├── base_schema.py         # Minimal base with components
│       ├── message_schema.py      # Message handling
│       ├── tool_schema.py         # Tool-enabled schema
│       └── agent_schema.py        # Agent state schema
├── node_configs/                  # Unified node configuration
│   ├── base_config.py             # Standard node config base
│   ├── engine_config.py           # Engine execution config
│   ├── tool_config.py             # Tool execution config
│   ├── validation_config.py       # Validation config
│   └── parser_config.py           # Parser config
├── graph/                         # Graph integration utilities
│   ├── builder.py                 # Compile-time graph building
│   ├── executor.py                # Runtime execution context
│   ├── validator.py               # Graph validation utilities
│   └── routing.py                 # Route resolution utilities
├── adapters/                      # Legacy compatibility
│   ├── state_schema_adapter.py    # StateSchema compatibility
│   ├── composer_adapter.py        # SchemaComposer compatibility
│   ├── node_config_adapter.py     # Node config compatibility
│   └── agent_adapter.py           # Agent compatibility
├── migration/                     # Migration utilities
│   ├── detector.py                # Legacy pattern detection
│   ├── migrator.py                # Automated migration
│   └── validator.py               # Migration validation
└── compatibility/                 # Lightweight compatibility
    ├── converters.py              # Essential type conversions
    └── validators.py              # Compatibility validation
```

## Core Interface Definitions

### 1. **Engine Provider Interface (Standardized Access)**

```python
# core/interfaces/engine_provider.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List

class EngineProvider(ABC):
    """Standard contract for engine access - NO MORE CHAOS!"""

    @abstractmethod
    def get_engine(self, name: str) -> Any:
        """Get engine by name - FAIL FAST if not found."""
        pass

    @abstractmethod
    def get_primary_engine(self) -> Any:
        """Get the default engine."""
        pass

    @abstractmethod
    def list_engines(self) -> Dict[str, Any]:
        """Get all engines."""
        pass

    @abstractmethod
    def validate_reference(self, name: str) -> bool:
        """Validate engine reference at compile time."""
        pass

class EngineAccessor(ABC):
    """Objects that can access engines through provider."""

    @abstractmethod
    def get_engine_provider(self) -> EngineProvider:
        pass
```

### 2. **Type Adapter Interface (Unified Conversion)**

```python
# core/interfaces/type_adapter.py
from abc import ABC, abstractmethod
from typing import Any, Type, TypeVar, Dict, Optional
from pydantic import BaseModel

T = TypeVar('T')

class TypeAdapter(ABC):
    """Standard contract for type conversion."""

    @abstractmethod
    def can_convert(self, source_type: Type, target_type: Type) -> bool:
        """Check if conversion is supported."""
        pass

    @abstractmethod
    def convert(self, value: Any, target_type: Type[T]) -> T:
        """Convert value to target type."""
        pass

class TypeAdapterRegistry(ABC):
    """Registry for type adapters."""

    @abstractmethod
    def register_adapter(self, adapter: TypeAdapter) -> None:
        """Register a type adapter."""
        pass

    @abstractmethod
    def convert(self, value: Any, target_type: Type[T]) -> T:
        """Convert using registered adapters."""
        pass

    @abstractmethod
    def get_adapter(self, source_type: Type, target_type: Type) -> Optional[TypeAdapter]:
        """Get adapter for conversion."""
        pass
```

### 3. **Model Registry Interface (Pydantic Support)**

```python
# core/interfaces/model_registry.py
from abc import ABC, abstractmethod
from typing import Type, Dict, Any, List
from pydantic import BaseModel

class ModelRegistry(ABC):
    """Standard contract for Pydantic model handling."""

    @abstractmethod
    def register_model(self, model_class: Type[BaseModel], alias: Optional[str] = None) -> None:
        """Register model with optional alias."""
        pass

    @abstractmethod
    def get_model(self, name: str) -> Optional[Type[BaseModel]]:
        """Get model by name or alias."""
        pass

    @abstractmethod
    def create_instance(self, model_class: Type[BaseModel], data: Dict[str, Any]) -> BaseModel:
        """Create model instance handling aliases and preregistered fields."""
        pass

    @abstractmethod
    def get_field_aliases(self, model_class: Type[BaseModel]) -> Dict[str, str]:
        """Get field aliases for model."""
        pass

    @abstractmethod
    def list_models(self) -> List[str]:
        """List all registered model names."""
        pass
```

### 4. **Route Registry Interface (Standardized Routing)**

```python
# core/interfaces/route_registry.py
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from enum import Enum

class StandardRoute(Enum):
    """Standard route names - NO MORE INCONSISTENCY!"""
    PYDANTIC_MODEL = "pydantic_model"
    LANGCHAIN_TOOL = "langchain_tool"
    FUNCTION_CALL = "function_call"
    RETRIEVER = "retriever"
    PARSER = "parser"
    VALIDATOR = "validator"

class RouteRegistry(ABC):
    """Standard contract for route management."""

    @abstractmethod
    def register_route(self, tool_name: str, route: StandardRoute) -> None:
        """Register tool route."""
        pass

    @abstractmethod
    def get_route(self, tool_name: str) -> Optional[StandardRoute]:
        """Get route for tool."""
        pass

    @abstractmethod
    def validate_routes(self, routes: Dict[str, str]) -> List[str]:
        """Validate route configuration, return errors."""
        pass

    @abstractmethod
    def get_tools_for_route(self, route: StandardRoute) -> List[str]:
        """Get all tools using a route."""
        pass
```

## Component Implementations

### 1. **Unified Engine Manager**

```python
# core/components/engine_manager.py
from typing import Dict, Any, Optional
from ..interfaces.engine_provider import EngineProvider

class EngineManager(EngineProvider):
    """Unified engine access - SINGLE PATTERN FOR ALL NODES."""

    def __init__(self):
        self._engines: Dict[str, Any] = {}
        self._primary_engine: Optional[str] = None

    def get_engine(self, name: str) -> Any:
        """Get engine by name - FAIL FAST with clear error."""
        if name not in self._engines:
            available = list(self._engines.keys())
            raise EngineNotFoundError(
                f"Engine '{name}' not found. Available engines: {available}"
            )
        return self._engines[name]

    def get_primary_engine(self) -> Any:
        """Get primary engine - FAIL FAST if none set."""
        if not self._primary_engine:
            if not self._engines:
                raise NoEnginesError("No engines registered")
            # Use first engine as fallback
            self._primary_engine = next(iter(self._engines.keys()))

        return self.get_engine(self._primary_engine)

    def register_engine(self, name: str, engine: Any) -> None:
        """Register engine with validation."""
        if not name:
            raise ValueError("Engine name cannot be empty")

        self._engines[name] = engine

        # Set as primary if first engine
        if not self._primary_engine:
            self._primary_engine = name

    def validate_reference(self, name: str) -> bool:
        """Validate engine reference exists."""
        return name in self._engines

    def list_engines(self) -> Dict[str, Any]:
        """Get all engines."""
        return self._engines.copy()

class EngineNotFoundError(Exception):
    """Clear error when engine not found."""
    pass

class NoEnginesError(Exception):
    """Clear error when no engines available."""
    pass
```

### 2. **Centralized Type Adapter System**

```python
# core/components/type_adapter.py
from typing import Any, Type, TypeVar, Dict, List, Optional
from pydantic import BaseModel
import json
from ..interfaces.type_adapter import TypeAdapter, TypeAdapterRegistry

T = TypeVar('T')

class PydanticTypeAdapter(TypeAdapter):
    """Handles Pydantic model conversions with alias support."""

    def can_convert(self, source_type: Type, target_type: Type) -> bool:
        """Check if we can convert to Pydantic model."""
        try:
            return issubclass(target_type, BaseModel)
        except TypeError:
            return False

    def convert(self, value: Any, target_type: Type[T]) -> T:
        """Convert to Pydantic model handling aliases."""
        if isinstance(value, target_type):
            return value

        # Handle string JSON
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError as e:
                raise TypeConversionError(f"Invalid JSON: {e}")

        # Handle dict with model validation
        if isinstance(value, dict):
            try:
                return target_type.model_validate(value)
            except Exception as e:
                raise TypeConversionError(f"Pydantic validation failed: {e}")

        raise TypeConversionError(f"Cannot convert {type(value)} to {target_type}")

class JSONTypeAdapter(TypeAdapter):
    """Handles JSON string conversions."""

    def can_convert(self, source_type: Type, target_type: Type) -> bool:
        return source_type == str and target_type in [dict, list]

    def convert(self, value: Any, target_type: Type[T]) -> T:
        if isinstance(value, str):
            try:
                result = json.loads(value)
                if target_type == dict and isinstance(result, dict):
                    return result
                elif target_type == list and isinstance(result, list):
                    return result
            except json.JSONDecodeError as e:
                raise TypeConversionError(f"JSON decode failed: {e}")

        raise TypeConversionError(f"Cannot convert {type(value)} to {target_type}")

class UnifiedTypeAdapterRegistry(TypeAdapterRegistry):
    """Registry managing all type conversions."""

    def __init__(self):
        self._adapters: List[TypeAdapter] = []

        # Register default adapters
        self.register_adapter(PydanticTypeAdapter())
        self.register_adapter(JSONTypeAdapter())

    def register_adapter(self, adapter: TypeAdapter) -> None:
        """Register a type adapter."""
        self._adapters.append(adapter)

    def convert(self, value: Any, target_type: Type[T]) -> T:
        """Convert using best available adapter."""
        source_type = type(value)

        for adapter in self._adapters:
            if adapter.can_convert(source_type, target_type):
                try:
                    return adapter.convert(value, target_type)
                except TypeConversionError:
                    continue  # Try next adapter

        # No adapter found
        raise TypeConversionError(
            f"No adapter found for {source_type} -> {target_type}"
        )

    def get_adapter(self, source_type: Type, target_type: Type) -> Optional[TypeAdapter]:
        """Get adapter for conversion."""
        for adapter in self._adapters:
            if adapter.can_convert(source_type, target_type):
                return adapter
        return None

class TypeConversionError(Exception):
    """Clear error for type conversion failures."""
    pass
```

### 3. **Pydantic Model Registry with Alias Support**

```python
# core/components/model_registry.py
from typing import Type, Dict, Any, List, Optional
from pydantic import BaseModel
from ..interfaces.model_registry import ModelRegistry

class UnifiedModelRegistry(ModelRegistry):
    """Centralized Pydantic model handling with full alias support."""

    def __init__(self):
        self._models: Dict[str, Type[BaseModel]] = {}
        self._aliases: Dict[str, str] = {}  # alias -> canonical name
        self._field_aliases: Dict[str, Dict[str, str]] = {}  # model -> {alias: field}

    def register_model(self, model_class: Type[BaseModel], alias: Optional[str] = None) -> None:
        """Register model with full metadata extraction."""
        name = model_class.__name__
        self._models[name] = model_class

        # Register alias if provided
        if alias:
            self._aliases[alias] = name

        # Extract field aliases
        field_aliases = {}
        for field_name, field_info in model_class.model_fields.items():
            if field_info.alias:
                field_aliases[field_info.alias] = field_name

        if field_aliases:
            self._field_aliases[name] = field_aliases

    def get_model(self, name: str) -> Optional[Type[BaseModel]]:
        """Get model by name or alias."""
        # Try direct name first
        if name in self._models:
            return self._models[name]

        # Try alias
        if name in self._aliases:
            canonical_name = self._aliases[name]
            return self._models[canonical_name]

        return None

    def create_instance(self, model_class: Type[BaseModel], data: Dict[str, Any]) -> BaseModel:
        """Create model instance with alias handling."""
        model_name = model_class.__name__

        # Handle field aliases
        if model_name in self._field_aliases:
            processed_data = {}
            alias_map = self._field_aliases[model_name]

            for key, value in data.items():
                # Convert alias to field name if needed
                field_name = alias_map.get(key, key)
                processed_data[field_name] = value

            data = processed_data

        # Create instance with processed data
        return model_class.model_validate(data)

    def get_field_aliases(self, model_class: Type[BaseModel]) -> Dict[str, str]:
        """Get field aliases for model."""
        model_name = model_class.__name__
        return self._field_aliases.get(model_name, {})

    def list_models(self) -> List[str]:
        """List all registered model names."""
        return list(self._models.keys())
```

### 4. **Standardized Route Manager**

```python
# core/components/route_manager.py
from typing import Dict, List, Optional
from ..interfaces.route_registry import RouteRegistry, StandardRoute

class UnifiedRouteManager(RouteRegistry):
    """Centralized route management with validation."""

    def __init__(self):
        self._routes: Dict[str, StandardRoute] = {}
        self._reverse_routes: Dict[StandardRoute, List[str]] = {
            route: [] for route in StandardRoute
        }

    def register_route(self, tool_name: str, route: StandardRoute) -> None:
        """Register tool route with validation."""
        if not tool_name:
            raise ValueError("Tool name cannot be empty")

        # Remove from old route if exists
        if tool_name in self._routes:
            old_route = self._routes[tool_name]
            if tool_name in self._reverse_routes[old_route]:
                self._reverse_routes[old_route].remove(tool_name)

        # Add to new route
        self._routes[tool_name] = route
        self._reverse_routes[route].append(tool_name)

    def get_route(self, tool_name: str) -> Optional[StandardRoute]:
        """Get route for tool."""
        return self._routes.get(tool_name)

    def validate_routes(self, routes: Dict[str, str]) -> List[str]:
        """Validate route configuration."""
        errors = []

        for tool_name, route_str in routes.items():
            try:
                StandardRoute(route_str)
            except ValueError:
                valid_routes = [r.value for r in StandardRoute]
                errors.append(
                    f"Invalid route '{route_str}' for tool '{tool_name}'. "
                    f"Valid routes: {valid_routes}"
                )

        return errors

    def get_tools_for_route(self, route: StandardRoute) -> List[str]:
        """Get all tools using a route."""
        return self._reverse_routes[route].copy()

    def import_routes(self, routes: Dict[str, str]) -> None:
        """Import routes from dict with validation."""
        errors = self.validate_routes(routes)
        if errors:
            raise RouteValidationError(f"Route validation failed: {errors}")

        for tool_name, route_str in routes.items():
            route = StandardRoute(route_str)
            self.register_route(tool_name, route)

class RouteValidationError(Exception):
    """Clear error for route validation failures."""
    pass
```

## Unified Node Config System

### 1. **Base Node Config with All Mixins**

```python
# node_configs/base_config.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from ..core.mixins.engine_access import EngineAccessMixin
from ..core.mixins.tool_routing import ToolRoutingMixin
from ..core.mixins.type_conversion import TypeConversionMixin
from ..core.mixins.model_handling import ModelHandlingMixin

class BaseNodeConfig(
    EngineAccessMixin,
    ToolRoutingMixin,
    TypeConversionMixin,
    ModelHandlingMixin,
    ABC
):
    """Standard base for all node configs - CONSISTENT CAPABILITIES."""

    def __init__(
        self,
        engine_name: str,
        input_mapping: Optional[Dict[str, str]] = None,
        output_mapping: Optional[Dict[str, str]] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.engine_name = engine_name
        self.input_mapping = input_mapping or {}
        self.output_mapping = output_mapping or {}

    @abstractmethod
    def execute_node(self, context: 'ExecutionContext') -> Dict[str, Any]:
        """Execute the node logic - implemented by subclasses."""
        pass

    def __call__(self, state: Any, config: Optional[Dict] = None) -> Any:
        """Standard execution pattern for all nodes."""
        from ..graph.executor import ExecutionContext

        # Create execution context
        context = ExecutionContext(state=state, config=config)

        # Resolve engine (fail fast if not found)
        engine = self.resolve_engine(context)
        context.set_current_engine(engine)

        # Extract inputs using mapping
        inputs = self.extract_inputs(context, self.input_mapping)
        context.set_inputs(inputs)

        # Execute node-specific logic
        result = self.execute_node(context)

        # Map outputs
        outputs = self.map_outputs(result, self.output_mapping)

        return outputs
```

### 2. **Simplified Engine Node Config**

```python
# node_configs/engine_config.py
from typing import Any, Dict
from .base_config import BaseNodeConfig

class EngineNodeConfig(BaseNodeConfig):
    """Simplified engine execution - SINGLE RESPONSIBILITY."""

    def execute_node(self, context: 'ExecutionContext') -> Dict[str, Any]:
        """Execute engine with inputs."""
        engine = context.get_current_engine()
        inputs = context.get_inputs()

        # Execute engine
        try:
            if hasattr(engine, 'arun'):
                # Async engine
                import asyncio
                result = asyncio.run(engine.arun(inputs))
            elif hasattr(engine, 'run'):
                # Sync engine
                result = engine.run(inputs)
            else:
                # Direct callable
                result = engine(inputs)
        except Exception as e:
            raise EngineExecutionError(f"Engine execution failed: {e}")

        return {"result": result}

class EngineExecutionError(Exception):
    """Clear error for engine execution failures."""
    pass
```

### 3. **Unified Tool Node Config**

```python
# node_configs/tool_config.py
from typing import Any, Dict, List
from .base_config import BaseNodeConfig
from ..core.interfaces.route_registry import StandardRoute

class ToolNodeConfig(BaseNodeConfig):
    """Unified tool execution - CONSISTENT TOOL HANDLING."""

    def __init__(self, allowed_routes: List[StandardRoute] = None, **kwargs):
        super().__init__(**kwargs)
        self.allowed_routes = allowed_routes or [
            StandardRoute.LANGCHAIN_TOOL,
            StandardRoute.FUNCTION_CALL
        ]

    def execute_node(self, context: 'ExecutionContext') -> Dict[str, Any]:
        """Execute tools with unified interface."""
        engine = context.get_current_engine()
        inputs = context.get_inputs()

        # Get tools from engine using standard interface
        tools = self.get_tools_from_engine(engine)

        # Filter tools by allowed routes
        filtered_tools = self.filter_tools_by_routes(tools, self.allowed_routes)

        # Execute tool calls
        results = []
        tool_calls = inputs.get("tool_calls", [])

        for tool_call in tool_calls:
            tool_name = self.extract_tool_name(tool_call)
            tool = self.find_tool_by_name(filtered_tools, tool_name)

            if not tool:
                results.append({
                    "tool": tool_name,
                    "error": f"Tool '{tool_name}' not found",
                    "status": "error"
                })
                continue

            try:
                tool_input = self.extract_tool_input(tool_call)
                tool_result = self.execute_tool(tool, tool_input)
                results.append({
                    "tool": tool_name,
                    "result": tool_result,
                    "status": "success"
                })
            except Exception as e:
                results.append({
                    "tool": tool_name,
                    "error": str(e),
                    "status": "error"
                })

        return {"tool_results": results}
```

## Migration Strategy and Timeline

### **Phase 1: Foundation (Weeks 1-2)**

1. Create `schema_test/` module structure
2. Implement core interfaces and components
3. Build unified engine manager and type adapter system
4. Create standardized node config base classes

### **Phase 2: Node Config Unification (Weeks 3-4)**

1. Implement unified node configs using consistent patterns
2. Create mixin system for shared capabilities
3. Build route management and model registry
4. Comprehensive unit tests for all components

### **Phase 3: Adapter Layer (Weeks 5-6)**

1. Create adapters for StateSchema, SchemaComposer, node configs
2. Implement feature flag system for gradual migration
3. Build migration detection and automation tools
4. Comprehensive compatibility testing

### **Phase 4: Graph Integration (Weeks 7-8)**

1. Implement compile-time graph building and validation
2. Create execution context for runtime state management
3. Build graph routing and execution utilities
4. Integration testing with real agent workflows

### **Phase 5: Migration and Validation (Weeks 9-12)**

1. Internal migration of haive packages
2. Performance testing and optimization
3. Documentation and migration guides
4. Community feedback and issue resolution

## Success Metrics

### **Technical Metrics**

- **Zero engine lookup failures** in node execution
- **Consistent behavior** across all node types
- **100% API compatibility** through adapter layer
- **Sub-100ms** graph compilation time
- **Clear error messages** for all failure modes

### **Developer Experience**

- **Single pattern** for engine access across all nodes
- **Consistent mixin usage** for shared capabilities
- **Full Pydantic support** with aliases and preregistered fields
- **Centralized type conversion** with extensible adapters
- **Standardized route management** with compile-time validation

### **Reliability**

- **Fail-fast behavior** for misconfigurations
- **Predictable execution** regardless of state structure
- **Clear error boundaries** between components
- **No silent failures** in engine or tool access
- **Consistent multi-agent coordination** without namespace conflicts

## Conclusion

This comprehensive refactoring addresses **ALL CRITICAL ISSUES** simultaneously:

1. **Schema System**: Modular components replace monolithic classes
2. **Node Config Chaos**: Single, consistent pattern for all node types
3. **Engine Access**: Unified engine provider with fail-fast behavior
4. **Mixin Fragmentation**: Consistent mixin architecture across all components
5. **Type Adaptation**: Centralized, extensible conversion system
6. **Pydantic Support**: Full alias and preregistered field handling
7. **Tool Routing**: Standardized route management with validation
8. **Agent-Graph Integration**: Compile-time validation with runtime execution context

The `schema_test` approach ensures **zero breaking changes** while delivering a fundamentally better architecture that solves the root causes of the current system's brittleness and complexity.
