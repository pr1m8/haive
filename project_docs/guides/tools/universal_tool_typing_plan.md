# Universal Tool Typing System - Implementation Plan

**Date**: 2025-08-08  
**Status**: Design & Implementation Mapping  
**Goal**: Extend existing ToolRouteMixin and utilities for comprehensive tool typing

## Leverage Existing Infrastructure

### 1. Current Assets We'll Build On

#### ToolRouteMixin (Primary Foundation)

```python
# Already provides:
- Tool analysis and categorization
- Metadata tracking (including is_executable)
- Dynamic route management
- Tool type determination

# We'll extend with:
- is_interruptible capability
- state_interaction properties (reads_state, writes_state)
- structured_output support detection
- performance characteristics
```

#### Existing Utilities to Enhance

- `interrupt_utils.py` - Fix and extend `is_interruptible()`
- `tool_schema_generator.py` - Add output model detection
- `naming.py` - Already handles tool naming perfectly

### 2. New Mixins to Create

#### InterruptibleToolMixin

```python
class InterruptibleToolMixin:
    """Mixin for tools that support interruption."""

    # Leverages existing interrupt_utils
    @property
    def is_interruptible(self) -> bool:
        """Check if tool supports interruption."""
        from haive.core.common.utils.interrupt_utils import is_interruptible
        return is_interruptible(self)

    @property
    def interrupt_points(self) -> list[str]:
        """Get interrupt points in tool execution."""
        # Use AST analysis from interrupt_utils
        return self._analyze_interrupt_points()
```

#### StateAwareToolMixin

```python
class StateAwareToolMixin:
    """Mixin for tools that interact with state."""

    # Properties we'll add to tool metadata
    reads_state: bool = False
    writes_state: bool = False
    state_dependencies: list[str] = Field(default_factory=list)
    required_state_keys: list[str] = Field(default_factory=list)

    def analyze_state_interaction(self) -> dict[str, Any]:
        """Analyze tool's state interaction patterns."""
        # Use tool_schema_generator to detect InjectedState usage
        from haive.core.common.utils.tool_schema_generator import extract_input_schema
        schema = extract_input_schema(self)

        # Check for InjectedState annotations
        has_injected_state = self._check_for_injected_state(schema)

        return {
            "reads_state": self.reads_state or has_injected_state,
            "writes_state": self.writes_state,
            "state_dependencies": self.state_dependencies,
            "uses_injected_state": has_injected_state
        }
```

#### StructuredOutputToolMixin

```python
class StructuredOutputToolMixin:
    """Mixin for tools with structured output."""

    # Leverage existing StructuredOutputMixin patterns
    structured_output_model: type[BaseModel] | None = None
    output_validation: bool = True

    def get_output_schema(self) -> type[BaseModel] | None:
        """Get structured output schema if available."""
        # Use tool_schema_generator
        from haive.core.common.utils.tool_schema_generator import extract_output_schema
        return extract_output_schema(self) or self.structured_output_model
```

### 3. Enhanced ToolRouteMixin Extension

```python
class EnhancedToolRouteMixin(ToolRouteMixin):
    """Extended tool routing with universal typing."""

    def _analyze_tool(self, tool: Any, name: str | None = None) -> dict[str, Any]:
        """Enhanced tool analysis with capability detection."""
        # First, use parent's analysis
        metadata = super()._analyze_tool(tool, name)

        # Add universal typing checks
        metadata.update({
            # Interruption capability
            "is_interruptible": self._check_interruptible(tool),

            # State interaction
            "reads_state": self._check_reads_state(tool),
            "writes_state": self._check_writes_state(tool),
            "state_dependencies": self._extract_state_deps(tool),

            # Structured output
            "has_structured_output": self._check_structured_output(tool),
            "output_model": self._extract_output_model(tool),

            # Performance hints
            "is_async": self._check_async_capability(tool),
            "expected_duration": self._estimate_duration(tool),
            "requires_network": self._check_network_requirement(tool),

            # Enhanced categorization
            "tool_category": self._categorize_tool(tool, metadata)
        })

        return metadata

    def _check_interruptible(self, tool: Any) -> bool:
        """Check if tool supports interruption."""
        # Fix and use interrupt_utils.is_interruptible
        from haive.core.common.utils.interrupt_utils import is_interruptible

        # Check multiple patterns:
        # 1. Uses pause_for_human
        if is_interruptible(tool):
            return True

        # 2. Has interrupt annotation/decorator
        if hasattr(tool, '__interrupt_enabled__'):
            return True

        # 3. Implements InterruptibleToolMixin
        if isinstance(tool, InterruptibleToolMixin):
            return True

        return False

    def _check_reads_state(self, tool: Any) -> bool:
        """Check if tool reads from state."""
        # Use schema analysis
        from haive.core.common.utils.tool_schema_generator import extract_input_schema

        try:
            schema = extract_input_schema(tool)
            # Check for InjectedState parameter
            if schema and hasattr(schema, '__annotations__'):
                for field, annotation in schema.__annotations__.items():
                    if 'InjectedState' in str(annotation):
                        return True
        except:
            pass

        # Check for state-related parameter names
        if callable(tool):
            import inspect
            sig = inspect.signature(tool)
            state_params = {'state', 'context', 'graph_state', 'agent_state'}
            return bool(state_params.intersection(sig.parameters.keys()))

        return False
```

### 4. Universal Tool Type Enum Extension

```python
class UniversalToolType(str, Enum):
    """Extended tool categorization."""

    # From existing ToolType
    LANGCHAIN_TOOL = "langchain_tool"
    PYDANTIC_MODEL = "pydantic_model"
    FUNCTION = "function"

    # New universal categories
    RETRIEVER = "retriever"
    VALIDATOR = "validator"
    TRANSFORMER = "transformer"
    COORDINATOR = "coordinator"
    MEMORY = "memory"
    SEARCH = "search"
    COMPUTATION = "computation"
    COMMUNICATION = "communication"
    GENERATION = "generation"

class ToolCapabilities(BaseModel):
    """Universal tool capability definition."""

    # Core type
    tool_type: UniversalToolType

    # Execution capabilities
    is_executable: bool = True
    is_interruptible: bool = False
    is_async: bool = False
    supports_streaming: bool = False
    supports_batch: bool = False

    # State interaction
    reads_state: bool = False
    writes_state: bool = False
    state_dependencies: list[str] = Field(default_factory=list)
    uses_injected_state: bool = False

    # Output capabilities
    has_structured_output: bool = False
    output_model: type[BaseModel] | None = None
    supports_validation: bool = False

    # Performance characteristics
    expected_duration: float | None = None
    requires_network: bool = False
    requires_auth: bool = False
    compute_intensive: bool = False

    # Metadata
    version: str = "1.0"
    tags: list[str] = Field(default_factory=list)
```

### 5. Integration Points & Field Impacts

#### Fields to Add/Modify in ToolRouteMixin

```python
# In tool_metadata dict:
tool_metadata = {
    "tool_type": str,  # Existing
    "is_executable": bool,  # Existing

    # NEW universal fields
    "capabilities": ToolCapabilities,  # Comprehensive capability object
    "is_interruptible": bool,
    "state_interaction": {
        "reads": bool,
        "writes": bool,
        "dependencies": list[str]
    },
    "output_schema": type[BaseModel] | None,
    "performance_hints": {
        "async": bool,
        "duration": float | None,
        "network": bool
    }
}
```

#### Integration with Existing Systems

1. **ToolList (via ToolListMixin)**
   - Enhance `get_by_tool_type()` to support universal types
   - Add `get_by_capability()` for capability-based filtering
   - Update `categorize_tools()` with universal categories

2. **Tool Schema Generator**
   - Extend to detect more patterns (InjectedState, async, etc.)
   - Add output model extraction
   - Improve docstring parsing for capability hints

3. **Interrupt Utils**
   - Fix the bug in `is_interruptible()`
   - Add more detection patterns
   - Support decorator-based interruption

### 6. Usage Examples

```python
# Enhanced tool with universal typing
@tool
class DataRetrieverTool(InterruptibleToolMixin, StateAwareToolMixin):
    """Retriever tool with full capability declaration."""

    # Capability declarations
    reads_state = True
    state_dependencies = ["query", "filters"]
    structured_output_model = SearchResults

    def __call__(self, query: str, state: Annotated[dict, InjectedState]) -> SearchResults:
        """Execute retrieval with state context."""
        # Tool implementation
        pass

# Tool analysis via enhanced mixin
class MyAgent(Agent, EnhancedToolRouteMixin):
    tools = [DataRetrieverTool(), calculator, web_search]

    def setup_agent(self):
        # Automatic capability detection
        for tool_name, metadata in self.tool_metadata.items():
            capabilities = metadata["capabilities"]
            print(f"{tool_name}: {capabilities.tool_type}")
            print(f"  Interruptible: {capabilities.is_interruptible}")
            print(f"  State-aware: {capabilities.reads_state}")
            print(f"  Output model: {capabilities.output_model}")
```

### 7. Implementation Priority

1. **Phase 1: Core Infrastructure**
   - Fix `is_interruptible()` bug
   - Create ToolCapabilities model
   - Extend ToolRouteMixin with universal analysis

2. **Phase 2: Capability Mixins**
   - InterruptibleToolMixin
   - StateAwareToolMixin
   - StructuredOutputToolMixin

3. **Phase 3: Integration**
   - Update ToolList methods
   - Enhance schema generators
   - Add capability-based routing

4. **Phase 4: Testing & Documentation**
   - Test all capability detection patterns
   - Document universal typing system
   - Create migration guide

## Benefits

1. **Leverages Existing Infrastructure** - Builds on proven ToolRouteMixin
2. **Universal Type System** - Consistent capability detection across all tools
3. **Automatic Detection** - Smart analysis without manual declaration
4. **Backward Compatible** - Works with existing tool definitions
5. **Performance Optimized** - Capability metadata enables smart routing
6. **Type Safe** - Full Pydantic validation and type checking

This approach maximizes reuse of existing excellent infrastructure while adding the universal typing capabilities needed for sophisticated tool management.
