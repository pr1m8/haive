# ToolEngine V2 - Complete Rebuild Design

**Date**: 2025-08-08  
**Purpose**: Complete rebuild of ToolEngine with universal typing from the ground up  
**Status**: Architecture Design

## Design Philosophy

Start fresh with a clean, well-typed ToolEngine that:

1. Serves as the single source of truth for tool types
2. Provides rich tool analysis and classification
3. Enables sophisticated routing and execution strategies
4. Integrates seamlessly with existing Haive patterns

## Core Architecture

### 1. Foundation Types (`tool/types.py`)

```python
"""Universal tool type system for Haive framework."""
from __future__ import annotations

from enum import Enum, auto
from typing import (
    Any, Callable, TypeAlias, Protocol, runtime_checkable,
    Literal, TypeVar, Generic, Union
)
from pydantic import BaseModel, Field, ConfigDict
from langchain_core.tools import BaseTool, StructuredTool
from langchain_core.tools.base import BaseToolkit
from langchain_core.messages import BaseMessage

# Type variables
TInput = TypeVar('TInput')
TOutput = TypeVar('TOutput')

# Universal tool type - THE source of truth
ToolLike: TypeAlias = Union[
    BaseTool,                         # LangChain tool instances
    StructuredTool,                   # Structured tool instances
    type[BaseTool],                   # Tool classes
    BaseModel,                        # Pydantic model instances (callable)
    type[BaseModel],                  # Pydantic model classes
    Callable[..., Any],               # Raw functions
    BaseToolkit,                      # Tool collections
    "ToolProtocol",                   # Our protocol
]

@runtime_checkable
class ToolProtocol(Protocol):
    """Protocol for tool-like objects."""

    @property
    def name(self) -> str:
        """Tool name."""
        ...

    @property
    def description(self) -> str | None:
        """Tool description."""
        ...

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Execute the tool."""
        ...

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
    ANALYSIS = "analysis"
    UNKNOWN = "unknown"

class ToolCapability(str, Enum):
    """Tool capabilities for advanced routing."""
    # Execution modes
    ASYNC = "async"
    SYNC = "sync"
    STREAMING = "streaming"
    BATCH = "batch"

    # Interruption
    INTERRUPTIBLE = "interruptible"
    PAUSABLE = "pausable"

    # State interaction
    READS_STATE = "reads_state"
    WRITES_STATE = "writes_state"
    INJECTED_STATE = "injected_state"
    STATELESS = "stateless"

    # I/O characteristics
    STRUCTURED_INPUT = "structured_input"
    STRUCTURED_OUTPUT = "structured_output"
    VALIDATED_OUTPUT = "validated_output"

    # Resource requirements
    NETWORK_REQUIRED = "network_required"
    AUTH_REQUIRED = "auth_required"
    COMPUTE_INTENSIVE = "compute_intensive"
    MEMORY_INTENSIVE = "memory_intensive"

    # Special types
    RETRIEVER = "retriever"
    VALIDATOR = "validator"
    TRANSFORMER = "transformer"

class ExecutionMode(str, Enum):
    """How the tool executes."""
    BLOCKING = "blocking"
    NON_BLOCKING = "non_blocking"
    BACKGROUND = "background"
    SCHEDULED = "scheduled"

class RoutingStrategy(str, Enum):
    """Tool selection strategies."""
    AUTO = "auto"                              # LLM decides
    CAPABILITY_MATCH = "capability_match"      # Match required capabilities
    CATEGORY_FIRST = "category_first"          # Category-based selection
    SEMANTIC_SIMILARITY = "semantic_similarity" # Embedding-based
    RULE_ENGINE = "rule_engine"                # Rule-based routing
    LOAD_BALANCED = "load_balanced"            # Performance-based
    PRIORITY_QUEUE = "priority_queue"          # Priority ordering
    ROUND_ROBIN = "round_robin"                # Rotate through tools
    LEAST_RECENTLY_USED = "least_recently_used" # LRU selection

class ToolMetadata(BaseModel):
    """Rich metadata for tools."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # Identification
    name: str
    category: ToolCategory
    description: str | None = None
    version: str = "1.0"

    # Capabilities
    capabilities: set[ToolCapability] = Field(default_factory=set)
    execution_mode: ExecutionMode = Field(default=ExecutionMode.BLOCKING)

    # Performance hints
    avg_execution_time: float | None = None  # seconds
    timeout: float | None = None             # seconds
    max_retries: int = 3
    success_rate: float | None = None        # 0.0 - 1.0

    # Resource requirements
    requires_auth: bool = False
    auth_type: str | None = None
    rate_limit: int | None = None           # requests per minute

    # State interaction
    state_inputs: list[str] = Field(default_factory=list)
    state_outputs: list[str] = Field(default_factory=list)
    state_schema: type[BaseModel] | None = None

    # Schema information
    input_schema: type[BaseModel] | None = None
    output_schema: type[BaseModel] | None = None
    error_schema: type[BaseModel] | None = None

    # Usage tracking
    usage_count: int = 0
    error_count: int = 0
    last_used: float | None = None

    # Tags and custom data
    tags: list[str] = Field(default_factory=list)
    custom_properties: dict[str, Any] = Field(default_factory=dict)
```

### 2. Tool Analysis System (`tool/analyzer.py`)

```python
"""Advanced tool analysis system."""
import ast
import inspect
import asyncio
from typing import Any, get_type_hints, get_origin, get_args
from datetime import datetime

from .types import (
    ToolLike, ToolMetadata, ToolCategory, ToolCapability,
    ExecutionMode, ToolProtocol
)

class ToolAnalyzer:
    """Comprehensive tool analyzer."""

    def __init__(self,
                 enable_ast_analysis: bool = True,
                 enable_runtime_analysis: bool = False):
        self.enable_ast_analysis = enable_ast_analysis
        self.enable_runtime_analysis = enable_runtime_analysis
        self._analysis_cache: dict[str, ToolMetadata] = {}

    def analyze(self, tool: ToolLike, force: bool = False) -> ToolMetadata:
        """Perform comprehensive tool analysis."""
        tool_id = self._get_tool_id(tool)

        # Check cache
        if not force and tool_id in self._analysis_cache:
            return self._analysis_cache[tool_id]

        # Create base metadata
        metadata = ToolMetadata(
            name=self._get_name(tool),
            category=self._determine_category(tool),
            description=self._get_description(tool)
        )

        # Analyze capabilities
        metadata.capabilities = self._analyze_capabilities(tool)

        # Determine execution mode
        metadata.execution_mode = self._determine_execution_mode(tool)

        # Extract schemas
        metadata.input_schema = self._extract_input_schema(tool)
        metadata.output_schema = self._extract_output_schema(tool)

        # Analyze state interaction
        state_analysis = self._analyze_state_interaction(tool)
        metadata.state_inputs = state_analysis["inputs"]
        metadata.state_outputs = state_analysis["outputs"]

        # Performance analysis (if enabled)
        if self.enable_runtime_analysis:
            perf_data = self._analyze_performance(tool)
            metadata.avg_execution_time = perf_data.get("avg_time")
            metadata.success_rate = perf_data.get("success_rate")

        # Cache result
        self._analysis_cache[tool_id] = metadata

        return metadata

    def _analyze_capabilities(self, tool: ToolLike) -> set[ToolCapability]:
        """Deep capability analysis."""
        capabilities = set()

        # Check async capability
        if self._is_async(tool):
            capabilities.add(ToolCapability.ASYNC)
        else:
            capabilities.add(ToolCapability.SYNC)

        # Check interruption support
        if self._is_interruptible(tool):
            capabilities.add(ToolCapability.INTERRUPTIBLE)

        # State interaction
        state_caps = self._analyze_state_capabilities(tool)
        capabilities.update(state_caps)

        # I/O capabilities
        if self._has_structured_input(tool):
            capabilities.add(ToolCapability.STRUCTURED_INPUT)
        if self._has_structured_output(tool):
            capabilities.add(ToolCapability.STRUCTURED_OUTPUT)

        # Resource requirements
        if self._requires_network(tool):
            capabilities.add(ToolCapability.NETWORK_REQUIRED)

        # Special capabilities
        if self._is_retriever(tool):
            capabilities.add(ToolCapability.RETRIEVER)

        return capabilities

    def _is_async(self, tool: ToolLike) -> bool:
        """Check if tool is async."""
        if hasattr(tool, '__call__'):
            return asyncio.iscoroutinefunction(tool.__call__)
        if callable(tool):
            return asyncio.iscoroutinefunction(tool)
        return False

    def _is_interruptible(self, tool: ToolLike) -> bool:
        """Enhanced interruption detection."""
        # Method 1: Check for explicit marker
        if hasattr(tool, '__interruptible__'):
            return bool(tool.__interruptible__)

        # Method 2: Check for capability declaration
        if hasattr(tool, '__tool_capabilities__'):
            return ToolCapability.INTERRUPTIBLE in tool.__tool_capabilities__

        # Method 3: AST analysis for pause patterns
        if self.enable_ast_analysis:
            try:
                source = inspect.getsource(tool if callable(tool) else tool.__call__)
                tree = ast.parse(source)

                # Look for pause_for_human or interrupt patterns
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        if hasattr(node.func, 'id') and 'pause' in node.func.id:
                            return True
                        if hasattr(node.func, 'attr') and 'interrupt' in node.func.attr:
                            return True
            except:
                pass

        # Method 4: Check if implements interruptible protocol
        return hasattr(tool, 'interrupt') or hasattr(tool, 'pause')

    def _analyze_state_capabilities(self, tool: ToolLike) -> set[ToolCapability]:
        """Analyze state interaction capabilities."""
        caps = set()

        # Check for InjectedState usage
        if self._uses_injected_state(tool):
            caps.add(ToolCapability.INJECTED_STATE)
            caps.add(ToolCapability.READS_STATE)

        # Check parameter names
        if callable(tool):
            try:
                sig = inspect.signature(tool)
                param_names = set(sig.parameters.keys())

                # Read indicators
                read_indicators = {'state', 'context', 'graph_state', 'agent_state'}
                if param_names.intersection(read_indicators):
                    caps.add(ToolCapability.READS_STATE)

                # Write indicators (usually in return type or docstring)
                if self._writes_to_state(tool):
                    caps.add(ToolCapability.WRITES_STATE)

                # If no state interaction
                if not caps:
                    caps.add(ToolCapability.STATELESS)

            except:
                pass

        return caps

    def _uses_injected_state(self, tool: ToolLike) -> bool:
        """Check for InjectedState annotation."""
        if not callable(tool):
            return False

        try:
            hints = get_type_hints(tool, include_extras=True)

            for param_type in hints.values():
                # Check for Annotated[X, InjectedState]
                origin = get_origin(param_type)
                if origin is not None:
                    args = get_args(param_type)
                    if any('InjectedState' in str(arg) for arg in args):
                        return True
        except:
            pass

        return False
```

### 3. New ToolEngine V2 (`tool/engine_v2.py`)

```python
"""ToolEngine V2 - Complete rebuild with universal typing."""
from __future__ import annotations

import asyncio
from typing import Any, Sequence
from collections import defaultdict
from datetime import datetime

from pydantic import Field, ConfigDict
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import ToolNode

from haive.core.engine.base import InvokableEngine
from .types import (
    ToolLike, ToolMetadata, ToolCategory, ToolCapability,
    RoutingStrategy, ExecutionMode
)
from .analyzer import ToolAnalyzer
from .router import ToolRouter
from .executor import ToolExecutor

class ToolEngineV2(InvokableEngine[dict[str, Any], dict[str, Any]]):
    """Rebuilt ToolEngine with universal typing and advanced capabilities."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # Tool configuration
    tools: Sequence[ToolLike] = Field(
        default_factory=list,
        description="Tools managed by this engine"
    )

    # Routing configuration
    routing_strategy: RoutingStrategy = Field(
        default=RoutingStrategy.AUTO,
        description="Tool selection strategy"
    )
    routing_config: dict[str, Any] = Field(
        default_factory=dict,
        description="Configuration for routing strategy"
    )

    # Execution configuration
    parallel_execution: bool = Field(
        default=False,
        description="Enable parallel tool execution"
    )
    max_parallel: int = Field(
        default=5,
        description="Maximum parallel executions"
    )
    timeout_default: float = Field(
        default=30.0,
        description="Default timeout for tools"
    )
    retry_config: dict[str, Any] = Field(
        default_factory=lambda: {"max_attempts": 3, "backoff_factor": 2.0}
    )

    # State management
    state_sync: bool = Field(
        default=True,
        description="Synchronize state between tools"
    )
    state_schema: type[BaseModel] | None = Field(
        default=None,
        description="Schema for state validation"
    )

    # Advanced features
    enable_caching: bool = Field(
        default=True,
        description="Cache tool results"
    )
    enable_monitoring: bool = Field(
        default=True,
        description="Track tool performance"
    )
    enable_validation: bool = Field(
        default=True,
        description="Validate tool I/O"
    )

    # Internal components
    _analyzer: ToolAnalyzer = Field(default_factory=ToolAnalyzer)
    _router: ToolRouter | None = None
    _executor: ToolExecutor | None = None
    _metadata_registry: dict[str, ToolMetadata] = Field(default_factory=dict)
    _performance_data: dict[str, dict] = Field(default_factory=lambda: defaultdict(dict))

    def model_post_init(self, __context: Any) -> None:
        """Initialize engine components."""
        super().model_post_init(__context)

        # Analyze all tools
        self._analyze_tools()

        # Initialize router
        self._router = ToolRouter(
            strategy=self.routing_strategy,
            config=self.routing_config,
            metadata_registry=self._metadata_registry
        )

        # Initialize executor
        self._executor = ToolExecutor(
            parallel=self.parallel_execution,
            max_parallel=self.max_parallel,
            timeout_default=self.timeout_default,
            retry_config=self.retry_config,
            enable_monitoring=self.enable_monitoring
        )

    def _analyze_tools(self) -> None:
        """Analyze all tools and build metadata registry."""
        for tool in self.tools:
            metadata = self._analyzer.analyze(tool)
            self._metadata_registry[metadata.name] = metadata

            # Store tool instance reference
            if hasattr(self, '_tool_instances'):
                self._tool_instances[metadata.name] = tool
            else:
                self._tool_instances = {metadata.name: tool}

    # Core Engine Implementation

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Define input schema."""
        fields = {
            "messages": (list[BaseMessage], Field(default_factory=list)),
            "tool_choice": (str | list[str] | None, Field(default=None)),
            "required_capabilities": (list[ToolCapability] | None, Field(default=None)),
            "context": (dict[str, Any], Field(default_factory=dict))
        }

        if self.state_schema:
            fields["state"] = (self.state_schema, Field(...))

        return fields

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Define output schema."""
        fields = {
            "messages": (list[BaseMessage], Field(default_factory=list)),
            "tool_results": (list[dict[str, Any]], Field(default_factory=list)),
            "execution_metadata": (dict[str, Any], Field(default_factory=dict))
        }

        if self.state_schema:
            fields["state"] = (self.state_schema, Field(...))

        return fields

    def create_runnable(self, runnable_config: RunnableConfig | None = None) -> Any:
        """Create enhanced ToolNode."""
        # Select tools based on routing strategy
        selected_tools = self._router.select_tools(
            available_tools=list(self._tool_instances.values()),
            context=runnable_config.get("configurable", {}) if runnable_config else {}
        )

        # Create ToolNode with selected tools
        tool_node = ToolNode(
            tools=selected_tools,
            handle_tool_errors=True
        )

        # Wrap with executor for advanced features
        return self._executor.wrap_tool_node(tool_node)

    # Query Methods

    def get_tools_by_capability(self, *capabilities: ToolCapability) -> list[str]:
        """Get tool names with all specified capabilities."""
        matching_tools = []

        for name, metadata in self._metadata_registry.items():
            if all(cap in metadata.capabilities for cap in capabilities):
                matching_tools.append(name)

        return matching_tools

    def get_tools_by_category(self, category: ToolCategory) -> list[str]:
        """Get tool names in category."""
        return [
            name for name, metadata in self._metadata_registry.items()
            if metadata.category == category
        ]

    def get_tool_metadata(self, tool_name: str) -> ToolMetadata | None:
        """Get metadata for specific tool."""
        return self._metadata_registry.get(tool_name)

    def get_interruptible_tools(self) -> list[str]:
        """Get all interruptible tool names."""
        return self.get_tools_by_capability(ToolCapability.INTERRUPTIBLE)

    def get_state_aware_tools(self) -> list[str]:
        """Get tools that interact with state."""
        state_tools = []

        for name, metadata in self._metadata_registry.items():
            caps = metadata.capabilities
            if any(cap in caps for cap in [
                ToolCapability.READS_STATE,
                ToolCapability.WRITES_STATE,
                ToolCapability.INJECTED_STATE
            ]):
                state_tools.append(name)

        return state_tools

    # Performance Tracking

    def get_performance_stats(self, tool_name: str) -> dict[str, Any]:
        """Get performance statistics for a tool."""
        metadata = self._metadata_registry.get(tool_name)
        perf_data = self._performance_data.get(tool_name, {})

        return {
            "usage_count": metadata.usage_count if metadata else 0,
            "error_count": metadata.error_count if metadata else 0,
            "success_rate": metadata.success_rate if metadata else None,
            "avg_execution_time": metadata.avg_execution_time if metadata else None,
            "last_used": metadata.last_used if metadata else None,
            **perf_data
        }

    # Class Methods for Type Export

    @classmethod
    def get_tool_type(cls) -> type:
        """Get the universal ToolLike type."""
        from .types import ToolLike
        return ToolLike

    @classmethod
    def get_analyzer(cls) -> ToolAnalyzer:
        """Get a tool analyzer instance."""
        return ToolAnalyzer()

    @classmethod
    def get_capability_enum(cls) -> type[ToolCapability]:
        """Get the ToolCapability enum."""
        from .types import ToolCapability
        return ToolCapability

    @classmethod
    def get_category_enum(cls) -> type[ToolCategory]:
        """Get the ToolCategory enum."""
        from .types import ToolCategory
        return ToolCategory
```

### 4. Tool Router (`tool/router.py`)

```python
"""Advanced tool routing system."""
from typing import Any, Sequence
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from .types import ToolLike, ToolMetadata, RoutingStrategy, ToolCapability

class ToolRouter:
    """Routes to appropriate tools based on strategy."""

    def __init__(self,
                 strategy: RoutingStrategy,
                 config: dict[str, Any],
                 metadata_registry: dict[str, ToolMetadata]):
        self.strategy = strategy
        self.config = config
        self.metadata_registry = metadata_registry

        # Strategy-specific initialization
        if strategy == RoutingStrategy.SEMANTIC_SIMILARITY:
            self._init_embeddings()
        elif strategy == RoutingStrategy.RULE_ENGINE:
            self._init_rules()

    def select_tools(self,
                    available_tools: Sequence[ToolLike],
                    context: dict[str, Any]) -> list[ToolLike]:
        """Select tools based on routing strategy."""

        if self.strategy == RoutingStrategy.AUTO:
            return list(available_tools)  # Return all for LLM selection

        elif self.strategy == RoutingStrategy.CAPABILITY_MATCH:
            required_caps = context.get("required_capabilities", [])
            return self._match_by_capabilities(available_tools, required_caps)

        elif self.strategy == RoutingStrategy.CATEGORY_FIRST:
            preferred_category = context.get("preferred_category")
            return self._route_by_category(available_tools, preferred_category)

        elif self.strategy == RoutingStrategy.SEMANTIC_SIMILARITY:
            query = context.get("query", "")
            return self._route_by_similarity(available_tools, query)

        elif self.strategy == RoutingStrategy.PRIORITY_QUEUE:
            return self._route_by_priority(available_tools)

        elif self.strategy == RoutingStrategy.LOAD_BALANCED:
            return self._route_by_load(available_tools)

        # Default fallback
        return list(available_tools)

    def _match_by_capabilities(self,
                              tools: Sequence[ToolLike],
                              required: list[ToolCapability]) -> list[ToolLike]:
        """Match tools that have all required capabilities."""
        if not required:
            return list(tools)

        matched = []
        for tool in tools:
            tool_name = self._get_tool_name(tool)
            metadata = self.metadata_registry.get(tool_name)

            if metadata and all(cap in metadata.capabilities for cap in required):
                matched.append(tool)

        return matched

    def _route_by_category(self,
                          tools: Sequence[ToolLike],
                          category: str | None) -> list[ToolLike]:
        """Route by category preference."""
        if not category:
            return list(tools)

        categorized = defaultdict(list)
        for tool in tools:
            tool_name = self._get_tool_name(tool)
            metadata = self.metadata_registry.get(tool_name)
            if metadata:
                categorized[metadata.category].append(tool)

        # Return preferred category first, then others
        result = categorized.get(category, [])
        for cat, cat_tools in categorized.items():
            if cat != category:
                result.extend(cat_tools)

        return result
```

### 5. Tool Executor (`tool/executor.py`)

```python
"""Advanced tool execution with monitoring and optimization."""
import asyncio
import time
from typing import Any
from concurrent.futures import ThreadPoolExecutor

from .types import ToolMetadata

class ToolExecutor:
    """Handles tool execution with advanced features."""

    def __init__(self,
                 parallel: bool = False,
                 max_parallel: int = 5,
                 timeout_default: float = 30.0,
                 retry_config: dict[str, Any] = None,
                 enable_monitoring: bool = True):
        self.parallel = parallel
        self.max_parallel = max_parallel
        self.timeout_default = timeout_default
        self.retry_config = retry_config or {}
        self.enable_monitoring = enable_monitoring

        if parallel:
            self.executor = ThreadPoolExecutor(max_workers=max_parallel)

    def wrap_tool_node(self, tool_node: Any) -> Any:
        """Wrap ToolNode with execution enhancements."""
        # Add monitoring, retries, timeouts, etc.
        return EnhancedToolNode(
            tool_node=tool_node,
            executor=self,
            enable_monitoring=self.enable_monitoring
        )

    async def execute_with_monitoring(self,
                                    tool: Any,
                                    args: dict[str, Any],
                                    metadata: ToolMetadata) -> dict[str, Any]:
        """Execute tool with performance monitoring."""
        start_time = time.time()
        error = None
        result = None

        try:
            # Execute with timeout
            if asyncio.iscoroutinefunction(tool):
                result = await asyncio.wait_for(
                    tool(**args),
                    timeout=metadata.timeout or self.timeout_default
                )
            else:
                result = await asyncio.wait_for(
                    asyncio.to_thread(tool, **args),
                    timeout=metadata.timeout or self.timeout_default
                )

        except asyncio.TimeoutError:
            error = "Timeout"
        except Exception as e:
            error = str(e)

        # Update metadata
        execution_time = time.time() - start_time
        metadata.usage_count += 1
        if error:
            metadata.error_count += 1
        metadata.last_used = time.time()

        # Update running averages
        if metadata.avg_execution_time:
            metadata.avg_execution_time = (
                metadata.avg_execution_time * 0.9 + execution_time * 0.1
            )
        else:
            metadata.avg_execution_time = execution_time

        return {
            "result": result,
            "error": error,
            "execution_time": execution_time,
            "metadata": metadata
        }
```

## Integration Plan

### Phase 1: Core Implementation

1. Create `types.py` with all type definitions
2. Implement `ToolAnalyzer` with comprehensive analysis
3. Build core `ToolEngineV2` class
4. Implement `ToolRouter` with multiple strategies
5. Create `ToolExecutor` for advanced execution

### Phase 2: Integration Points

1. Update imports to export types
2. Create migration helpers
3. Update ToolRouteMixin to use ToolEngineV2 types
4. Ensure backward compatibility

### Phase 3: Advanced Features

1. Implement caching system
2. Add performance monitoring
3. Create validation framework
4. Build interrupt handling system

## Key Differences from V1

1. **Complete Type System**: Rich type hierarchy with protocols
2. **Advanced Analysis**: Deep capability detection with caching
3. **Sophisticated Routing**: Multiple strategies beyond auto
4. **Performance Tracking**: Built-in monitoring and optimization
5. **State Management**: First-class state interaction support
6. **Modular Design**: Separate router and executor components

## Migration Path

```python
# Old ToolEngine usage
engine = ToolEngine(tools=[...])

# New ToolEngineV2 usage - backward compatible
engine = ToolEngineV2(tools=[...])  # Works the same

# With new features
engine = ToolEngineV2(
    tools=[...],
    routing_strategy=RoutingStrategy.CAPABILITY_MATCH,
    enable_monitoring=True,
    state_schema=MyStateSchema
)

# Query capabilities
interruptible = engine.get_interruptible_tools()
retrievers = engine.get_tools_by_category(ToolCategory.RETRIEVAL)
```

This complete rebuild provides a clean, well-typed foundation for all tool management in Haive!
