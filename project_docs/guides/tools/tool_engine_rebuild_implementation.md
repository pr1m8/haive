# ToolEngine Rebuild - Implementation Plan

**Date**: 2025-08-08  
**Purpose**: Complete rebuild with all discussed properties and tool types

## Implementation Structure

### 1. Core Types Module (`tool/types.py`)

```python
"""Universal tool type definitions for Haive framework."""
from __future__ import annotations

from enum import Enum
from typing import (
    Any, Callable, TypeAlias, Protocol, runtime_checkable,
    Union, Literal
)
from pydantic import BaseModel, Field, ConfigDict
from langchain_core.tools import BaseTool, StructuredTool
from langchain_core.tools.base import BaseToolkit

# Universal tool type - single source of truth
ToolLike: TypeAlias = Union[
    BaseTool,                    # LangChain tool instances
    StructuredTool,              # Structured tool instances
    type[BaseTool],              # Tool classes
    BaseModel,                   # Pydantic model instances (callable)
    type[BaseModel],             # Pydantic model classes
    Callable[..., Any],          # Raw functions
    BaseToolkit,                 # Tool collections
]

@runtime_checkable
class InterruptibleTool(Protocol):
    """Protocol for tools that support interruption."""

    @property
    def is_interruptible(self) -> bool:
        """Check if tool can be interrupted."""
        ...

    def interrupt(self) -> None:
        """Interrupt tool execution."""
        ...

@runtime_checkable
class StateAwareTool(Protocol):
    """Protocol for tools that interact with state."""

    @property
    def reads_state(self) -> bool:
        """Check if tool reads from state."""
        ...

    @property
    def writes_state(self) -> bool:
        """Check if tool writes to state."""
        ...

    @property
    def state_dependencies(self) -> list[str]:
        """Get state keys this tool depends on."""
        ...

class ToolType(str, Enum):
    """Tool implementation types."""
    LANGCHAIN_TOOL = "langchain_tool"
    PYDANTIC_MODEL = "pydantic_model"
    FUNCTION = "function"
    STRUCTURED_TOOL = "structured_tool"
    TOOLKIT = "toolkit"
    RETRIEVER_TOOL = "retriever_tool"
    VALIDATION_TOOL = "validation_tool"

class ToolCategory(str, Enum):
    """High-level tool categorization."""
    RETRIEVAL = "retrieval"
    COMPUTATION = "computation"
    COMMUNICATION = "communication"
    TRANSFORMATION = "transformation"
    VALIDATION = "validation"
    COORDINATION = "coordination"
    MEMORY = "memory"
    SEARCH = "search"
    GENERATION = "generation"
    UNKNOWN = "unknown"

class ToolCapability(str, Enum):
    """Fine-grained tool capabilities."""
    # Execution capabilities
    INTERRUPTIBLE = "interruptible"
    ASYNC_CAPABLE = "async_capable"
    STREAMING = "streaming"
    BATCH_CAPABLE = "batch_capable"

    # State interaction
    READS_STATE = "reads_state"
    WRITES_STATE = "writes_state"
    INJECTED_STATE = "injected_state"
    TO_STATE = "to_state"           # Tool that writes to state
    FROM_STATE = "from_state"       # Tool that reads from state

    # Output capabilities
    STRUCTURED_OUTPUT = "structured_output"
    VALIDATED_OUTPUT = "validated_output"

    # Special capabilities
    RETRIEVER = "retriever"
    VALIDATOR = "validator"
    TRANSFORMER = "transformer"
    ROUTED = "routed"              # Tool with custom routing

class ToolProperties(BaseModel):
    """Comprehensive tool properties."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # Core identification
    name: str
    tool_type: ToolType
    category: ToolCategory = Field(default=ToolCategory.UNKNOWN)

    # Capabilities
    capabilities: set[ToolCapability] = Field(default_factory=set)

    # State properties
    is_state_tool: bool = Field(default=False, description="Tool interacts with state")
    to_state_tool: bool = Field(default=False, description="Tool writes to state")
    from_state_tool: bool = Field(default=False, description="Tool reads from state")
    state_dependencies: list[str] = Field(default_factory=list)
    state_outputs: list[str] = Field(default_factory=list)

    # Execution properties
    is_interruptible: bool = Field(default=False)
    is_async: bool = Field(default=False)
    is_routed: bool = Field(default=False, description="Has custom routing")

    # Schema information
    input_schema: type[BaseModel] | None = None
    output_schema: type[BaseModel] | None = None
    structured_output_model: type[BaseModel] | None = None

    # Metadata
    description: str | None = None
    version: str = Field(default="1.0")
    tags: list[str] = Field(default_factory=list)

    # Quick checks using capabilities
    def has_capability(self, capability: ToolCapability) -> bool:
        """Check if tool has specific capability."""
        return capability in self.capabilities

    def is_retriever(self) -> bool:
        """Check if this is a retriever tool."""
        return self.has_capability(ToolCapability.RETRIEVER)

    def has_structured_output(self) -> bool:
        """Check if tool has structured output."""
        return self.has_capability(ToolCapability.STRUCTURED_OUTPUT)
```

### 2. Tool Analyzer (`tool/analyzer.py`)

```python
"""Tool analysis system using Haive utilities."""
import inspect
import asyncio
from typing import Any, get_type_hints, get_origin, get_args

from haive.core.common.utils.interrupt_utils import is_interruptible
from haive.core.common.utils.tool_schema_generator import (
    extract_input_schema, extract_output_schema
)

from .types import (
    ToolLike, ToolProperties, ToolType, ToolCategory,
    ToolCapability, InterruptibleTool, StateAwareTool
)

class ToolAnalyzer:
    """Analyzes tools to determine properties and capabilities."""

    def analyze(self, tool: ToolLike) -> ToolProperties:
        """Comprehensive tool analysis."""
        # Get basic info
        name = self._get_tool_name(tool)
        tool_type = self._determine_tool_type(tool)

        # Create properties
        properties = ToolProperties(
            name=name,
            tool_type=tool_type,
            category=self._determine_category(tool),
            description=self._get_description(tool)
        )

        # Analyze capabilities
        self._analyze_capabilities(tool, properties)

        # Analyze state interaction
        self._analyze_state_interaction(tool, properties)

        # Extract schemas
        properties.input_schema = self._safe_extract_schema(extract_input_schema, tool)
        properties.output_schema = self._safe_extract_schema(extract_output_schema, tool)

        # Check for structured output model
        properties.structured_output_model = self._extract_structured_output_model(tool)

        return properties

    def _determine_tool_type(self, tool: ToolLike) -> ToolType:
        """Determine the tool implementation type."""
        # Use existing patterns from ToolRouteMixin
        if hasattr(tool, "__bases__"):
            # Check MRO for BaseTool
            mro = inspect.getmro(tool)
            if any("BaseTool" in str(base) for base in mro):
                return ToolType.LANGCHAIN_TOOL

        # Check instances
        from langchain_core.tools import BaseTool, StructuredTool
        if isinstance(tool, StructuredTool):
            return ToolType.STRUCTURED_TOOL
        elif isinstance(tool, BaseTool):
            return ToolType.LANGCHAIN_TOOL

        # Check for Pydantic model with __call__
        if isinstance(tool, BaseModel) and hasattr(tool, "__call__"):
            return ToolType.PYDANTIC_MODEL

        # Check for toolkit
        from langchain_core.tools.base import BaseToolkit
        if isinstance(tool, BaseToolkit):
            return ToolType.TOOLKIT

        # Function
        if callable(tool):
            return ToolType.FUNCTION

        return ToolType.FUNCTION  # Default

    def _analyze_capabilities(self, tool: ToolLike, properties: ToolProperties) -> None:
        """Analyze tool capabilities."""
        capabilities = set()

        # Check interruptibility using existing util
        if is_interruptible(tool) or isinstance(tool, InterruptibleTool):
            capabilities.add(ToolCapability.INTERRUPTIBLE)
            properties.is_interruptible = True

        # Check async
        if self._is_async(tool):
            capabilities.add(ToolCapability.ASYNC_CAPABLE)
            properties.is_async = True

        # Check structured output
        if properties.output_schema or properties.structured_output_model:
            capabilities.add(ToolCapability.STRUCTURED_OUTPUT)

        # Check for retriever
        if self._is_retriever(tool):
            capabilities.add(ToolCapability.RETRIEVER)

        # Check for routed tool
        if hasattr(tool, "__tool_route__") or hasattr(tool, "route"):
            capabilities.add(ToolCapability.ROUTED)
            properties.is_routed = True

        properties.capabilities = capabilities

    def _analyze_state_interaction(self, tool: ToolLike, properties: ToolProperties) -> None:
        """Analyze how tool interacts with state."""
        # Check if implements StateAwareTool protocol
        if isinstance(tool, StateAwareTool):
            properties.is_state_tool = True
            if tool.reads_state:
                properties.from_state_tool = True
                properties.capabilities.add(ToolCapability.FROM_STATE)
                properties.capabilities.add(ToolCapability.READS_STATE)
            if tool.writes_state:
                properties.to_state_tool = True
                properties.capabilities.add(ToolCapability.TO_STATE)
                properties.capabilities.add(ToolCapability.WRITES_STATE)
            properties.state_dependencies = tool.state_dependencies
            return

        # Check for InjectedState
        if self._uses_injected_state(tool):
            properties.is_state_tool = True
            properties.from_state_tool = True
            properties.capabilities.add(ToolCapability.INJECTED_STATE)
            properties.capabilities.add(ToolCapability.READS_STATE)

        # Check parameter names
        if callable(tool):
            sig = inspect.signature(tool)
            param_names = set(sig.parameters.keys())

            # State reading indicators
            if param_names.intersection({"state", "context", "graph_state"}):
                properties.is_state_tool = True
                properties.from_state_tool = True
                properties.capabilities.add(ToolCapability.FROM_STATE)
                properties.capabilities.add(ToolCapability.READS_STATE)

            # Check return annotation for state writing
            if sig.return_annotation != sig.empty:
                if "state" in str(sig.return_annotation).lower():
                    properties.to_state_tool = True
                    properties.capabilities.add(ToolCapability.TO_STATE)
                    properties.capabilities.add(ToolCapability.WRITES_STATE)

    def _uses_injected_state(self, tool: ToolLike) -> bool:
        """Check for InjectedState annotation."""
        if not callable(tool):
            return False

        try:
            hints = get_type_hints(tool, include_extras=True)
            for param_type in hints.values():
                origin = get_origin(param_type)
                if origin is not None:
                    args = get_args(param_type)
                    if any("InjectedState" in str(arg) for arg in args):
                        return True
        except:
            pass
        return False

    def _is_async(self, tool: ToolLike) -> bool:
        """Check if tool is async."""
        if hasattr(tool, "__call__"):
            return asyncio.iscoroutinefunction(tool.__call__)
        return asyncio.iscoroutinefunction(tool) if callable(tool) else False

    def _is_retriever(self, tool: ToolLike) -> bool:
        """Check if tool is a retriever."""
        # Check name/description patterns
        name = self._get_tool_name(tool).lower()
        desc = self._get_description(tool).lower()

        retriever_patterns = ["retriev", "fetch", "search", "query", "lookup"]
        if any(pattern in name or pattern in desc for pattern in retriever_patterns):
            return True

        # Check for retriever base classes
        if hasattr(tool, "__class__"):
            return "retriever" in tool.__class__.__name__.lower()

        return False

    def _get_tool_name(self, tool: ToolLike) -> str:
        """Get tool name."""
        if hasattr(tool, "name"):
            return tool.name
        elif hasattr(tool, "__name__"):
            return tool.__name__
        return tool.__class__.__name__

    def _get_description(self, tool: ToolLike) -> str:
        """Get tool description."""
        if hasattr(tool, "description"):
            return tool.description or ""
        elif hasattr(tool, "__doc__"):
            return tool.__doc__ or ""
        return ""

    def _safe_extract_schema(self, extractor: Callable, tool: ToolLike) -> type[BaseModel] | None:
        """Safely extract schema using provided extractor."""
        try:
            return extractor(tool)
        except:
            return None

    def _extract_structured_output_model(self, tool: ToolLike) -> type[BaseModel] | None:
        """Extract structured output model if present."""
        # Check for explicit structured_output_model attribute
        if hasattr(tool, "structured_output_model"):
            return tool.structured_output_model

        # Check return type annotation
        if callable(tool):
            try:
                sig = inspect.signature(tool)
                if sig.return_annotation != sig.empty:
                    # Check if return type is a BaseModel
                    if isinstance(sig.return_annotation, type) and issubclass(sig.return_annotation, BaseModel):
                        return sig.return_annotation
            except:
                pass

        return None
```

### 3. Enhanced ToolEngine (`tool/engine.py`)

```python
"""Rebuilt ToolEngine with universal typing and advanced features."""
from __future__ import annotations

import logging
from typing import Any, Sequence
from collections import defaultdict

from pydantic import BaseModel, Field, ConfigDict, field_validator
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import StructuredTool, Tool
from langchain_core.tools.base import BaseTool, BaseToolkit
from langchain_core.messages import BaseMessage
from langgraph.prebuilt import ToolNode
from langgraph.types import RetryPolicy

from haive.core.engine.base import InvokableEngine
from haive.core.engine.base.types import EngineType

from .types import (
    ToolLike, ToolProperties, ToolType, ToolCategory,
    ToolCapability
)
from .analyzer import ToolAnalyzer

logger = logging.getLogger(__name__)

class ToolEngine(InvokableEngine[dict[str, Any], dict[str, Any]]):
    """Enhanced tool engine with universal typing and property analysis.

    This engine manages tools with comprehensive property analysis,
    capability-based routing, and state interaction tracking.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    engine_type: EngineType = EngineType.TOOL

    # Tool sources
    tools: Sequence[ToolLike] | None = Field(
        default=None,
        description="List of tools to manage"
    )
    toolkit: BaseToolkit | list[BaseToolkit] | None = Field(
        default=None,
        description="Toolkit(s) to use"
    )

    # Configuration
    retry_policy: RetryPolicy | None = None
    parallel: bool = Field(default=False)
    auto_route: bool = Field(default=True)
    messages_key: str = Field(default="messages")
    tool_choice: Literal["auto", "required", "none"] = Field(default="auto")
    return_source: bool = Field(default=True)

    # Advanced options
    timeout: float | None = None
    max_iterations: int | None = None

    # NEW: Tool analysis and properties
    enable_analysis: bool = Field(
        default=True,
        description="Enable automatic tool analysis"
    )
    _analyzer: ToolAnalyzer = Field(default_factory=ToolAnalyzer, exclude=True)
    _tool_properties: dict[str, ToolProperties] = Field(
        default_factory=dict,
        exclude=True,
        description="Analyzed tool properties"
    )
    _tool_instances: dict[str, ToolLike] = Field(
        default_factory=dict,
        exclude=True,
        description="Tool name to instance mapping"
    )

    def model_post_init(self, __context: Any) -> None:
        """Initialize and analyze tools after creation."""
        super().model_post_init(__context)
        if self.enable_analysis:
            self._analyze_all_tools()

    def _analyze_all_tools(self) -> None:
        """Analyze all configured tools."""
        all_tools = self._get_all_tools()

        for tool in all_tools:
            try:
                properties = self._analyzer.analyze(tool)
                self._tool_properties[properties.name] = properties
                self._tool_instances[properties.name] = tool

                logger.debug(
                    f"Analyzed tool '{properties.name}': "
                    f"type={properties.tool_type}, "
                    f"category={properties.category}, "
                    f"capabilities={properties.capabilities}"
                )
            except Exception as e:
                logger.warning(f"Failed to analyze tool: {e}")

    # Required abstract methods implementation

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Define input fields for tool engine."""
        return {
            "messages": (
                list[BaseMessage],
                Field(default_factory=list, description="Input messages")
            ),
            "state": (
                dict[str, Any],
                Field(default_factory=dict, description="Current state")
            ),
            "tool_choice": (
                str | list[str] | None,
                Field(default=None, description="Specific tool(s) to use")
            ),
            "required_capabilities": (
                list[ToolCapability] | None,
                Field(default=None, description="Required tool capabilities")
            )
        }

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Define output fields for tool engine."""
        return {
            "messages": (
                list[BaseMessage],
                Field(default_factory=list, description="Output messages with tool results")
            ),
            "tool_results": (
                list[dict[str, Any]],
                Field(default_factory=list, description="Tool execution results")
            ),
            "state": (
                dict[str, Any],
                Field(default_factory=dict, description="Updated state")
            ),
            "execution_metadata": (
                dict[str, Any],
                Field(default_factory=dict, description="Execution metadata")
            )
        }

    def create_runnable(self, runnable_config: RunnableConfig | None = None) -> Any:
        """Create enhanced ToolNode with property awareness."""
        params = self.apply_runnable_config(runnable_config)

        # Get all tools
        all_tools = self._get_all_tools()

        # Filter by capabilities if requested
        required_capabilities = params.get("required_capabilities")
        if required_capabilities:
            all_tools = self._filter_by_capabilities(all_tools, required_capabilities)

        # Create ToolNode
        kwargs = {
            "tools": all_tools,
            "retry_policy": params.get("retry_policy", self.retry_policy),
        }

        if self.timeout is not None:
            kwargs["timeout"] = params.get("timeout", self.timeout)
        if self.max_iterations is not None:
            kwargs["max_iterations"] = params.get("max_iterations", self.max_iterations)

        tool_node = ToolNode(**kwargs)

        # Wrap with property-aware handler if analysis is enabled
        if self.enable_analysis:
            return PropertyAwareToolNode(tool_node, self._tool_properties)

        return tool_node

    # Tool query methods

    def get_tools_by_capability(self, *capabilities: ToolCapability) -> list[str]:
        """Get tool names with specified capabilities."""
        matching = []
        for name, props in self._tool_properties.items():
            if all(cap in props.capabilities for cap in capabilities):
                matching.append(name)
        return matching

    def get_tools_by_category(self, category: ToolCategory) -> list[str]:
        """Get tool names in category."""
        return [
            name for name, props in self._tool_properties.items()
            if props.category == category
        ]

    def get_interruptible_tools(self) -> list[str]:
        """Get all interruptible tool names."""
        return [
            name for name, props in self._tool_properties.items()
            if props.is_interruptible
        ]

    def get_state_tools(self) -> list[str]:
        """Get all state-aware tool names."""
        return [
            name for name, props in self._tool_properties.items()
            if props.is_state_tool
        ]

    def get_tools_reading_state(self) -> list[str]:
        """Get tools that read from state."""
        return [
            name for name, props in self._tool_properties.items()
            if props.from_state_tool
        ]

    def get_tools_writing_state(self) -> list[str]:
        """Get tools that write to state."""
        return [
            name for name, props in self._tool_properties.items()
            if props.to_state_tool
        ]

    def get_tool_properties(self, tool_name: str) -> ToolProperties | None:
        """Get properties for specific tool."""
        return self._tool_properties.get(tool_name)

    # Helper methods

    def _filter_by_capabilities(
        self,
        tools: list[ToolLike],
        capabilities: list[ToolCapability]
    ) -> list[ToolLike]:
        """Filter tools by required capabilities."""
        filtered = []

        for tool in tools:
            # Find properties for this tool
            tool_name = self._analyzer._get_tool_name(tool)
            props = self._tool_properties.get(tool_name)

            if props and all(cap in props.capabilities for cap in capabilities):
                filtered.append(tool)

        return filtered

    def _get_all_tools(self) -> list[ToolLike]:
        """Get all tools from various sources."""
        all_tools = []

        # Add directly specified tools
        if self.tools:
            for tool in self.tools:
                # Process BaseModel tools
                if isinstance(tool, BaseModel) and not isinstance(
                    tool, (BaseTool, Tool, StructuredTool)
                ):
                    try:
                        structured_tool = self._convert_model_to_tool(tool)
                        if structured_tool:
                            all_tools.append(structured_tool)
                        else:
                            logger.warning(f"Could not convert model to tool: {type(tool).__name__}")
                    except Exception as e:
                        logger.warning(f"Error converting model to tool: {e}")
                else:
                    all_tools.append(tool)

        # Add tools from toolkits
        if self.toolkit:
            if isinstance(self.toolkit, list):
                for tk in self.toolkit:
                    if hasattr(tk, "get_tools"):
                        all_tools.extend(tk.get_tools())
                    elif isinstance(tk, BaseToolkit):
                        all_tools.extend(tk.tools)
            elif hasattr(self.toolkit, "get_tools"):
                all_tools.extend(self.toolkit.get_tools())
            elif isinstance(self.toolkit, BaseToolkit):
                all_tools.extend(self.toolkit.tools)

        return all_tools

    def _convert_model_to_tool(self, model: BaseModel) -> StructuredTool | None:
        """Convert Pydantic model to StructuredTool."""
        if not callable(model):
            return None

        call_method = model.__call__
        name = getattr(model, "name", model.__class__.__name__.lower())
        description = call_method.__doc__ or f"Tool for {name}"

        from langchain_core.tools import tool

        @tool(name=name, description=description)
        def model_tool(*args, **kwargs) -> Any:
            return call_method(*args, **kwargs)

        return model_tool

    # Class methods for type export

    @classmethod
    def get_tool_type(cls) -> type:
        """Get the universal ToolLike type for other components."""
        from .types import ToolLike
        return ToolLike

    @classmethod
    def get_analyzer(cls) -> ToolAnalyzer:
        """Get a tool analyzer instance."""
        return ToolAnalyzer()

    @classmethod
    def get_capability_enum(cls) -> type[ToolCapability]:
        """Get ToolCapability enum for other components."""
        from .types import ToolCapability
        return ToolCapability

class PropertyAwareToolNode:
    """Wrapper for ToolNode that uses tool properties."""

    def __init__(self, tool_node: ToolNode, properties: dict[str, ToolProperties]):
        self.tool_node = tool_node
        self.properties = properties

    def invoke(self, input_data: dict[str, Any], config: RunnableConfig | None = None) -> dict[str, Any]:
        """Invoke with property awareness."""
        # Could add property-based enhancements here
        result = self.tool_node.invoke(input_data, config)

        # Add execution metadata
        if "execution_metadata" not in result:
            result["execution_metadata"] = {}

        # Track which tools were used
        used_tools = []
        if "messages" in result:
            for msg in result["messages"]:
                if hasattr(msg, "tool_calls"):
                    for call in msg.tool_calls:
                        if call.get("name"):
                            used_tools.append(call["name"])

        # Add tool properties to metadata
        result["execution_metadata"]["used_tools"] = used_tools
        result["execution_metadata"]["tool_properties"] = {
            name: self.properties.get(name) for name in used_tools
            if name in self.properties
        }

        return result
```

### 4. Module Structure (`tool/__init__.py`)

```python
"""Enhanced tool engine with universal typing."""

from .engine import ToolEngine
from .types import (
    ToolLike,
    ToolType,
    ToolCategory,
    ToolCapability,
    ToolProperties,
    InterruptibleTool,
    StateAwareTool,
)
from .analyzer import ToolAnalyzer

__all__ = [
    # Engine
    "ToolEngine",

    # Types
    "ToolLike",
    "ToolType",
    "ToolCategory",
    "ToolCapability",
    "ToolProperties",

    # Protocols
    "InterruptibleTool",
    "StateAwareTool",

    # Analyzer
    "ToolAnalyzer",
]

# For backward compatibility and easy access
def get_tool_type():
    """Get the universal ToolLike type."""
    return ToolLike

def get_tool_analyzer():
    """Get a tool analyzer instance."""
    return ToolAnalyzer()
```

## Key Features Implemented

1. **Universal Type System**:
   - `ToolLike` as single source of truth
   - Comprehensive `ToolProperties` with all discussed fields
   - `ToolCapability` enum with state interaction types

2. **State Tool Properties**:
   - `is_state_tool` - General state interaction
   - `to_state_tool` - Writes to state
   - `from_state_tool` - Reads from state
   - `state_dependencies` and `state_outputs`

3. **Tool Analysis**:
   - Uses existing utilities (interrupt_utils, tool_schema_generator)
   - Detects all capabilities including InjectedState
   - Categorizes tools automatically

4. **Required Methods**:
   - Implements `get_input_fields()` properly
   - Implements `get_output_fields()` properly
   - Maintains all existing functionality

5. **Query Methods**:
   - Get tools by capability
   - Get interruptible tools
   - Get state-aware tools
   - Get tools reading/writing state

6. **Integration Ready**:
   - Exports types for ToolRouteMixin
   - Class methods for type access
   - Backward compatible with existing usage

This implementation provides the complete ToolEngine rebuild with all the properties and types we discussed!
