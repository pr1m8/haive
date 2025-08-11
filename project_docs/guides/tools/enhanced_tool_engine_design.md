# Enhanced ToolEngine Design & Architecture

**Date**: 2025-08-08  
**Status**: Design Phase  
**Current State**: ToolEngine is implemented and working - we're adding enhancements

## Current ToolEngine Analysis

The ToolEngine is **fully functional** with:

- ✅ Complete abstract method implementation
- ✅ LangGraph ToolNode integration
- ✅ Basic tool execution and routing
- ✅ Retry policies and parallel execution
- ✅ Message handling

What we're adding:

- 🔧 Universal tool typing system
- 🔧 Tool classification and properties
- 🔧 Advanced routing strategies
- 🔧 State-aware tool management
- 🔧 Interruptible execution patterns

## Enhanced ToolEngine Architecture

### 1. Core Type System (New Module: `tool/types.py`)

```python
# packages/haive-core/src/haive/core/engine/tool/types.py
from enum import Enum
from typing import TypeAlias, Union, Callable, Any, Literal
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool, StructuredTool
from langchain_core.tools.base import BaseToolkit

# Universal tool type definition
ToolType: TypeAlias = Union[
    BaseTool,                    # LangChain tool instances
    StructuredTool,              # Structured tool instances
    type[BaseTool],              # Tool classes
    type[BaseModel],             # Pydantic models as tools
    BaseModel,                   # Pydantic model instances
    Callable[..., Any],          # Functions as tools
    BaseToolkit,                 # Tool collections
]

class ToolCategory(str, Enum):
    """High-level tool categorization."""
    RETRIEVAL = "retrieval"           # Document/data retrieval
    COMPUTATION = "computation"       # Math, analysis, processing
    COMMUNICATION = "communication"   # API calls, messaging
    TRANSFORMATION = "transformation" # Data conversion, manipulation
    VALIDATION = "validation"         # Input validation, verification
    COORDINATION = "coordination"     # Agent/workflow coordination
    MEMORY = "memory"                # State management, persistence
    SEARCH = "search"                # Web search, database query
    GENERATION = "generation"        # Content creation, synthesis
    UNKNOWN = "unknown"              # Uncategorized

class ToolCapability(str, Enum):
    """Specific tool capabilities."""
    # Execution capabilities
    INTERRUPTIBLE = "interruptible"
    ASYNC_CAPABLE = "async_capable"
    STREAMABLE = "streamable"
    BATCH_CAPABLE = "batch_capable"

    # State interaction
    STATE_READER = "state_reader"
    STATE_WRITER = "state_writer"
    INJECTED_STATE = "injected_state"

    # Output capabilities
    STRUCTURED_OUTPUT = "structured_output"
    VALIDATED_OUTPUT = "validated_output"

    # Special capabilities
    RETRIEVER = "retriever"
    REQUIRES_AUTH = "requires_auth"
    NETWORK_DEPENDENT = "network_dependent"
    COMPUTE_INTENSIVE = "compute_intensive"

class ExecutionMode(str, Enum):
    """Tool execution mode."""
    SYNCHRONOUS = "synchronous"
    ASYNCHRONOUS = "asynchronous"
    STREAMING = "streaming"
    BATCH = "batch"

class ToolProperties(BaseModel):
    """Comprehensive tool properties."""

    # Core classification
    category: ToolCategory = Field(default=ToolCategory.UNKNOWN)
    capabilities: set[ToolCapability] = Field(default_factory=set)
    execution_mode: ExecutionMode = Field(default=ExecutionMode.SYNCHRONOUS)

    # State interaction
    state_dependencies: list[str] = Field(
        default_factory=list,
        description="State keys this tool depends on"
    )
    state_outputs: list[str] = Field(
        default_factory=list,
        description="State keys this tool writes to"
    )

    # Performance hints
    expected_duration: float | None = Field(
        default=None,
        description="Expected execution time in seconds"
    )
    timeout: float | None = Field(
        default=None,
        description="Maximum execution time"
    )

    # Schema information
    input_schema: type[BaseModel] | None = None
    output_schema: type[BaseModel] | None = None

    # Metadata
    version: str = Field(default="1.0")
    description: str | None = None
    tags: list[str] = Field(default_factory=list)

    # Quick property checks
    @property
    def is_interruptible(self) -> bool:
        return ToolCapability.INTERRUPTIBLE in self.capabilities

    @property
    def reads_state(self) -> bool:
        return ToolCapability.STATE_READER in self.capabilities

    @property
    def writes_state(self) -> bool:
        return ToolCapability.STATE_WRITER in self.capabilities

    @property
    def has_structured_output(self) -> bool:
        return ToolCapability.STRUCTURED_OUTPUT in self.capabilities

class RoutingStrategy(str, Enum):
    """Tool routing strategies."""
    AUTO = "auto"                          # LLM decides
    CAPABILITY_BASED = "capability_based"  # Route by capabilities
    CATEGORY_BASED = "category_based"      # Route by category
    SEMANTIC = "semantic"                  # Semantic similarity
    RULE_BASED = "rule_based"             # Predefined rules
    LOAD_BALANCED = "load_balanced"        # Performance-based
    PRIORITY = "priority"                  # Priority ordering
    SEQUENTIAL = "sequential"              # Fixed order
    PARALLEL = "parallel"                  # All at once
```

### 2. Tool Analyzer (New Module: `tool/analyzer.py`)

```python
# packages/haive-core/src/haive/core/engine/tool/analyzer.py
import inspect
import ast
from typing import Any, get_args, get_origin
from pydantic import BaseModel
from langchain_core.tools import BaseTool, StructuredTool

from .types import (
    ToolProperties, ToolCategory, ToolCapability,
    ExecutionMode, ToolType
)

class ToolAnalyzer:
    """Analyzes tools to determine their properties and capabilities."""

    def analyze(self, tool: ToolType) -> ToolProperties:
        """Analyze a tool and return its properties."""
        properties = ToolProperties()

        # Determine category
        properties.category = self._determine_category(tool)

        # Analyze capabilities
        properties.capabilities = self._analyze_capabilities(tool)

        # Determine execution mode
        properties.execution_mode = self._determine_execution_mode(tool)

        # Extract schemas
        properties.input_schema = self._extract_input_schema(tool)
        properties.output_schema = self._extract_output_schema(tool)

        # Analyze state dependencies
        state_info = self._analyze_state_interaction(tool)
        properties.state_dependencies = state_info["dependencies"]
        properties.state_outputs = state_info["outputs"]

        # Performance hints
        properties.expected_duration = self._estimate_duration(tool)

        # Extract metadata
        properties.description = self._extract_description(tool)
        properties.tags = self._extract_tags(tool)

        return properties

    def _determine_category(self, tool: ToolType) -> ToolCategory:
        """Determine tool category from name, description, and type."""
        # Check explicit markers
        if hasattr(tool, "__tool_category__"):
            return tool.__tool_category__

        # Get tool name and description
        name = self._get_tool_name(tool).lower()
        desc = self._get_tool_description(tool).lower()

        # Category detection patterns
        patterns = {
            ToolCategory.RETRIEVAL: ["retriev", "fetch", "search", "query", "lookup"],
            ToolCategory.COMPUTATION: ["calculat", "comput", "math", "analyz", "process"],
            ToolCategory.COMMUNICATION: ["send", "email", "notify", "api", "webhook"],
            ToolCategory.TRANSFORMATION: ["convert", "transform", "parse", "format"],
            ToolCategory.VALIDATION: ["validat", "check", "verify", "test"],
            ToolCategory.MEMORY: ["remember", "store", "save", "persist"],
            ToolCategory.SEARCH: ["search", "find", "google", "bing", "web"],
            ToolCategory.GENERATION: ["generat", "create", "write", "compose"],
        }

        # Check patterns
        for category, keywords in patterns.items():
            if any(kw in name or kw in desc for kw in keywords):
                return category

        return ToolCategory.UNKNOWN

    def _analyze_capabilities(self, tool: ToolType) -> set[ToolCapability]:
        """Analyze tool capabilities."""
        capabilities = set()

        # Check if interruptible
        if self._is_interruptible(tool):
            capabilities.add(ToolCapability.INTERRUPTIBLE)

        # Check async capability
        if self._is_async_capable(tool):
            capabilities.add(ToolCapability.ASYNC_CAPABLE)

        # Check state interaction
        if self._reads_state(tool):
            capabilities.add(ToolCapability.STATE_READER)
        if self._writes_state(tool):
            capabilities.add(ToolCapability.STATE_WRITER)
        if self._uses_injected_state(tool):
            capabilities.add(ToolCapability.INJECTED_STATE)

        # Check output capabilities
        if self._has_structured_output(tool):
            capabilities.add(ToolCapability.STRUCTURED_OUTPUT)

        # Check special capabilities
        if self._is_retriever(tool):
            capabilities.add(ToolCapability.RETRIEVER)

        # Check explicit capability markers
        if hasattr(tool, "__tool_capabilities__"):
            capabilities.update(tool.__tool_capabilities__)

        return capabilities

    def _is_interruptible(self, tool: ToolType) -> bool:
        """Check if tool supports interruption."""
        # Use fixed interrupt_utils
        from haive.core.common.utils.interrupt_utils import is_interruptible

        # Multiple checks
        if is_interruptible(tool):
            return True

        # Check for interrupt marker
        if hasattr(tool, "__interruptible__"):
            return bool(tool.__interruptible__)

        # Check for pause_for_human in source
        try:
            source = inspect.getsource(tool if not isinstance(tool, type) else tool.__call__)
            return "pause_for_human" in source
        except:
            pass

        return False

    def _reads_state(self, tool: ToolType) -> bool:
        """Check if tool reads from state."""
        # Check for InjectedState parameter
        if self._uses_injected_state(tool):
            return True

        # Check parameter names
        if callable(tool):
            try:
                sig = inspect.signature(tool)
                state_params = {"state", "context", "graph_state", "agent_state"}
                return bool(state_params.intersection(sig.parameters.keys()))
            except:
                pass

        return False

    def _uses_injected_state(self, tool: ToolType) -> bool:
        """Check if tool uses InjectedState annotation."""
        if not callable(tool):
            return False

        try:
            sig = inspect.signature(tool)
            for param in sig.parameters.values():
                if param.annotation != param.empty:
                    # Check for InjectedState in annotation
                    if "InjectedState" in str(param.annotation):
                        return True
                    # Check for Annotated[dict, InjectedState]
                    origin = get_origin(param.annotation)
                    if origin is not None:
                        args = get_args(param.annotation)
                        if any("InjectedState" in str(arg) for arg in args):
                            return True
        except:
            pass

        return False

    def _has_structured_output(self, tool: ToolType) -> bool:
        """Check if tool has structured output."""
        # Check for output schema
        if self._extract_output_schema(tool) is not None:
            return True

        # Check return type annotation
        if callable(tool):
            try:
                sig = inspect.signature(tool)
                if sig.return_annotation != sig.empty:
                    # Check if return type is a BaseModel
                    if isinstance(sig.return_annotation, type) and issubclass(sig.return_annotation, BaseModel):
                        return True
            except:
                pass

        return False

    def _extract_input_schema(self, tool: ToolType) -> type[BaseModel] | None:
        """Extract input schema from tool."""
        # Use existing utility
        from haive.core.common.utils.tool_schema_generator import extract_input_schema

        try:
            return extract_input_schema(tool)
        except:
            return None

    def _extract_output_schema(self, tool: ToolType) -> type[BaseModel] | None:
        """Extract output schema from tool."""
        from haive.core.common.utils.tool_schema_generator import extract_output_schema

        try:
            return extract_output_schema(tool)
        except:
            return None

    def _get_tool_name(self, tool: ToolType) -> str:
        """Get tool name."""
        if hasattr(tool, "name"):
            return tool.name
        elif hasattr(tool, "__name__"):
            return tool.__name__
        return tool.__class__.__name__

    def _get_tool_description(self, tool: ToolType) -> str:
        """Get tool description."""
        if hasattr(tool, "description"):
            return tool.description or ""
        elif hasattr(tool, "__doc__"):
            return tool.__doc__ or ""
        return ""
```

### 3. Enhanced ToolEngine Implementation

```python
# packages/haive-core/src/haive/core/engine/tool/base.py (enhanced)
from typing import Any, Literal
from pydantic import Field
from langgraph.prebuilt import ToolNode

from .types import (
    ToolType, ToolProperties, ToolCategory,
    ToolCapability, RoutingStrategy
)
from .analyzer import ToolAnalyzer

class ToolEngine(InvokableEngine[dict[str, Any], dict[str, Any]]):
    """Enhanced tool engine with universal typing and advanced routing."""

    # Existing fields
    tools: list[ToolType] | None = None
    toolkit: BaseToolkit | list[BaseToolkit] | None = None

    # NEW: Enhanced configuration
    routing_strategy: RoutingStrategy = Field(
        default=RoutingStrategy.AUTO,
        description="Tool selection strategy"
    )

    # NEW: Tool analysis cache
    _tool_properties: dict[str, ToolProperties] = {}
    _analyzer: ToolAnalyzer = Field(default_factory=ToolAnalyzer)

    def model_post_init(self, __context: Any) -> None:
        """Analyze tools after initialization."""
        super().model_post_init(__context)
        self._analyze_all_tools()

    def _analyze_all_tools(self) -> None:
        """Analyze all configured tools."""
        all_tools = self._get_all_tools()

        for tool in all_tools:
            tool_name = self._get_tool_name(tool)
            properties = self._analyzer.analyze(tool)
            self._tool_properties[tool_name] = properties

    def get_tools_by_capability(self, capability: ToolCapability) -> list[ToolType]:
        """Get tools with specific capability."""
        matching_tools = []
        all_tools = self._get_all_tools()

        for tool in all_tools:
            tool_name = self._get_tool_name(tool)
            properties = self._tool_properties.get(tool_name)
            if properties and capability in properties.capabilities:
                matching_tools.append(tool)

        return matching_tools

    def get_tools_by_category(self, category: ToolCategory) -> list[ToolType]:
        """Get tools in specific category."""
        matching_tools = []
        all_tools = self._get_all_tools()

        for tool in all_tools:
            tool_name = self._get_tool_name(tool)
            properties = self._tool_properties.get(tool_name)
            if properties and properties.category == category:
                matching_tools.append(tool)

        return matching_tools

    def get_tool_properties(self, tool_name: str) -> ToolProperties | None:
        """Get properties for a specific tool."""
        return self._tool_properties.get(tool_name)

    def create_runnable(self, runnable_config: RunnableConfig | None = None) -> Any:
        """Create enhanced ToolNode with routing."""
        tools_list = self._prepare_tools()

        # Apply routing strategy
        if self.routing_strategy != RoutingStrategy.AUTO:
            tools_list = self._apply_routing_strategy(tools_list)

        # Create ToolNode with enhanced configuration
        tool_node = ToolNode(
            tools=tools_list,
            messages_key=self.messages_key,
            handle_tool_errors=self.handle_tool_errors,
            **self.tool_kwargs
        )

        # Add retry policy if configured
        if self.retry_policy:
            tool_node = self._add_retry_policy(tool_node)

        return tool_node

    def _apply_routing_strategy(self, tools: list[ToolType]) -> list[ToolType]:
        """Apply routing strategy to tool list."""
        if self.routing_strategy == RoutingStrategy.PRIORITY:
            # Sort by priority (could be based on performance, reliability, etc.)
            return self._sort_by_priority(tools)
        elif self.routing_strategy == RoutingStrategy.CATEGORY_BASED:
            # Group by category for better organization
            return self._group_by_category(tools)
        elif self.routing_strategy == RoutingStrategy.CAPABILITY_BASED:
            # Sort by capabilities for better matching
            return self._sort_by_capabilities(tools)

        return tools

    # Export types for other components
    @classmethod
    def get_tool_type_alias(cls) -> type:
        """Get the ToolType TypeAlias for use in other components."""
        return ToolType

    @classmethod
    def get_analyzer(cls) -> ToolAnalyzer:
        """Get a tool analyzer instance."""
        return ToolAnalyzer()
```

### 4. Integration Helpers

```python
# packages/haive-core/src/haive/core/engine/tool/__init__.py
"""Tool engine with universal typing system."""

from .base import ToolEngine
from .types import (
    ToolType,
    ToolProperties,
    ToolCategory,
    ToolCapability,
    ExecutionMode,
    RoutingStrategy,
)
from .analyzer import ToolAnalyzer

# Convenience imports for other components
__all__ = [
    "ToolEngine",
    "ToolType",
    "ToolProperties",
    "ToolCategory",
    "ToolCapability",
    "ExecutionMode",
    "RoutingStrategy",
    "ToolAnalyzer",
]

# For backward compatibility
def get_tool_type():
    """Get the universal ToolType for imports."""
    return ToolType
```

## Implementation Strategy

### Phase 1: Core Types

1. Create `types.py` with all enums and models
2. Implement `ToolAnalyzer` with capability detection
3. Test analyzer with various tool types

### Phase 2: Enhance ToolEngine

1. Add tool analysis on initialization
2. Implement capability and category queries
3. Add routing strategy support
4. Cache analyzed properties

### Phase 3: Integration Points

1. Export types for ToolRouteMixin usage
2. Create convenience methods for type access
3. Ensure backward compatibility

## Benefits

1. **Universal Type System**: Single ToolType used everywhere
2. **Rich Property Analysis**: Automatic capability detection
3. **Advanced Routing**: Multiple strategies beyond auto
4. **State Awareness**: Track state dependencies
5. **Performance Hints**: Duration estimates and timeouts
6. **Extensible**: Easy to add new capabilities

## Usage Example

```python
# Create enhanced tool engine
engine = ToolEngine(
    tools=[retriever_tool, calculator, web_search],
    routing_strategy=RoutingStrategy.CAPABILITY_BASED
)

# Query tools by capability
interruptible_tools = engine.get_tools_by_capability(ToolCapability.INTERRUPTIBLE)
state_readers = engine.get_tools_by_capability(ToolCapability.STATE_READER)

# Get tool properties
calc_props = engine.get_tool_properties("calculator")
print(f"Calculator category: {calc_props.category}")
print(f"Calculator capabilities: {calc_props.capabilities}")

# Other components can import and use
from haive.core.engine.tool import ToolType, ToolAnalyzer

# ToolRouteMixin can now use these types
analyzer = ToolAnalyzer()
properties = analyzer.analyze(some_tool)
```

This enhanced ToolEngine becomes the foundation for universal tool typing across the entire Haive framework!
