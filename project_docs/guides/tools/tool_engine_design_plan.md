# Tool Engine Design Plan & Architecture

**Research Date**: 2025-08-08  
**Status**: Design Phase  
**References**: @haive-core engine architecture analysis, @LangChain retriever tools

## Current State Analysis

### Existing ToolEngine Issues

- **Missing Abstract Methods**: `get_input_fields()` and `get_output_fields()` not implemented
- **Incomplete Interface**: Violates base Engine contract, cannot be properly instantiated
- **Limited Routing**: Basic auto-routing without sophisticated tool selection strategies

### Haive Engine Architecture Strengths

- **Configuration-Driven Factory Pattern**: Clean separation of config vs runtime
- **Type-Safe Field Definitions**: Schema-driven input/output specification
- **Excellent AugLLMConfig Foundation**: Comprehensive tool integration in LLM engine
- **LangChain Integration**: Seamless creation of LangChain runnables

## Proposed Tool Engine Architecture

### 1. Enhanced ToolEngine Base Structure

```python
class ToolEngine(InvokableEngine[ToolInputSchema, ToolOutputSchema]):
    """Enhanced tool engine with comprehensive routing and classification."""

    # Current fields (enhanced)
    tools: list[BaseTool | Tool | StructuredTool | BaseModel | RetrieverTool] | None
    toolkit: BaseToolkit | list[BaseToolkit] | None

    # NEW: Tool Classification & Routing
    tool_properties: dict[str, ToolProperties] = Field(default_factory=dict)
    routing_strategy: ToolRoutingStrategy = Field(default="auto_select")
    state_management: StateManagementConfig = Field(default_factory=StateManagementConfig)

    # NEW: Execution Configuration
    retry_policy: RetryPolicy | None = None
    parallel: bool = False
    interruptible: bool = True
    timeout: float | None = None

    # NEW: Integration Features
    structured_output_model: type[BaseModel] | None = None
    injected_state_fields: list[str] = Field(default_factory=list)
    retriever_configs: dict[str, RetrieverConfig] = Field(default_factory=dict)
```

### 2. Tool Properties Classification System

```python
class ToolProperties(BaseModel):
    """Classification and routing properties for tools."""

    # Core Classification
    tool_type: ToolType = Field(..., description="Primary tool category")
    execution_mode: ExecutionMode = Field(default="synchronous")

    # State Interaction
    reads_state: bool = Field(default=False, description="Tool reads from graph state")
    writes_state: bool = Field(default=False, description="Tool modifies graph state")
    state_dependencies: list[str] = Field(default_factory=list)

    # Execution Properties
    interruptible: bool = Field(default=True, description="Can be interrupted mid-execution")
    requires_confirmation: bool = Field(default=False, description="Needs user confirmation")
    has_side_effects: bool = Field(default=False, description="Modifies external systems")

    # Integration Properties
    supports_structured_output: bool = Field(default=False)
    supports_streaming: bool = Field(default=False)
    requires_auth: bool = Field(default=False)

    # Performance Properties
    expected_duration: float | None = Field(default=None, description="Expected runtime in seconds")
    compute_intensive: bool = Field(default=False)
    network_dependent: bool = Field(default=False)

class ToolType(str, Enum):
    """Tool type classification."""
    RETRIEVAL = "retrieval"           # Document/data retrieval
    COMPUTATION = "computation"       # Math, analysis, processing
    COMMUNICATION = "communication"   # API calls, messaging, notifications
    TRANSFORMATION = "transformation" # Data format conversion, manipulation
    VALIDATION = "validation"         # Input validation, verification
    COORDINATION = "coordination"     # Agent/workflow coordination
    MEMORY = "memory"                # State management, persistence
    SEARCH = "search"                # Web search, database query
    GENERATION = "generation"        # Content creation, synthesis

class ExecutionMode(str, Enum):
    """Tool execution mode."""
    SYNCHRONOUS = "synchronous"
    ASYNCHRONOUS = "asynchronous"
    STREAMING = "streaming"
    BATCH = "batch"
```

### 3. Tool Routing Strategy System

```python
class ToolRoutingStrategy(str, Enum):
    """Tool selection and routing strategies."""
    AUTO_SELECT = "auto_select"           # LLM decides based on description
    RULE_BASED = "rule_based"            # Predefined routing rules
    SIMILARITY_BASED = "similarity_based" # Semantic similarity routing
    PRIORITY_BASED = "priority_based"     # Tool priority ordering
    CONTEXT_AWARE = "context_aware"       # State-based routing
    LOAD_BALANCED = "load_balanced"       # Performance-based routing
    SEQUENTIAL = "sequential"             # Ordered execution
    PARALLEL = "parallel"                # Concurrent execution

class StateManagementConfig(BaseModel):
    """Configuration for state interaction."""

    # InjectedState Integration
    auto_inject_state: bool = Field(default=True)
    injected_state_keys: list[str] = Field(default_factory=list)

    # State Modification Rules
    state_modification_rules: dict[str, StateModificationRule] = Field(default_factory=dict)
    persistent_state_keys: list[str] = Field(default_factory=list)

    # Context Management
    context_window_size: int = Field(default=10, description="Number of previous results to maintain")
    auto_cleanup: bool = Field(default=True, description="Automatically clean up old state")

class StateModificationRule(BaseModel):
    """Rules for how tools can modify state."""
    allowed_keys: list[str] = Field(default_factory=list)
    required_keys: list[str] = Field(default_factory=list)
    validation_schema: type[BaseModel] | None = None
    merge_strategy: str = Field(default="overwrite")  # overwrite, merge, append
```

### 4. Enhanced Retriever Integration

```python
class EnhancedRetrieverConfig(BaseModel):
    """Enhanced configuration for retriever tools."""

    # Base Retriever Config
    retriever: BaseRetriever
    name: str
    description: str

    # Enhanced Features
    document_prompt: BasePromptTemplate | None = None
    document_separator: str = Field(default="\n\n")
    response_format: Literal['content', 'content_and_artifact'] = Field(default="content")

    # NEW: Advanced Features
    similarity_threshold: float | None = Field(default=None)
    max_results: int = Field(default=5)
    enable_reranking: bool = Field(default=False)
    metadata_filtering: dict[str, Any] = Field(default_factory=dict)

    # NEW: Integration with Tool Properties
    auto_classify: bool = Field(default=True, description="Auto-generate tool properties")
    custom_properties: ToolProperties | None = None

class RetrieverToolFactory:
    """Factory for creating enhanced retriever tools."""

    @staticmethod
    def create_retriever_tool(config: EnhancedRetrieverConfig) -> StructuredTool:
        """Create enhanced retriever tool with full property classification."""

        # Create base retriever tool
        base_tool = create_retriever_tool(
            retriever=config.retriever,
            name=config.name,
            description=config.description,
            document_prompt=config.document_prompt,
            document_separator=config.document_separator,
            response_format=config.response_format
        )

        # Auto-generate tool properties if enabled
        if config.auto_classify:
            properties = ToolProperties(
                tool_type=ToolType.RETRIEVAL,
                reads_state=True,  # Retriever tools typically read query state
                supports_structured_output=True,
                network_dependent=True,
                expected_duration=2.0,  # Typical retrieval time
                state_dependencies=["query", "context"]
            )
        else:
            properties = config.custom_properties or ToolProperties()

        # Enhance with metadata
        enhanced_tool = enhance_tool_with_properties(base_tool, properties)
        return enhanced_tool
```

### 5. Structured Output Tool Integration

```python
class StructuredOutputToolConfig(BaseModel):
    """Configuration for structured output tools."""

    # Base Configuration
    base_function: Callable
    output_model: type[BaseModel]

    # Tool Generation Options
    auto_generate_schema: bool = Field(default=True)
    include_field_descriptions: bool = Field(default=True)
    validate_output: bool = Field(default=True)

    # Integration Options
    inject_state: bool = Field(default=False)
    state_fields: list[str] = Field(default_factory=list)

    # Error Handling
    fallback_on_validation_error: bool = Field(default=True)
    validation_error_strategy: str = Field(default="return_error")

class StructuredOutputToolFactory:
    """Factory for creating structured output tools."""

    @staticmethod
    def from_function(
        func: Callable,
        output_model: type[BaseModel],
        config: StructuredOutputToolConfig | None = None
    ) -> StructuredTool:
        """Create structured output tool from function."""
        config = config or StructuredOutputToolConfig(
            base_function=func,
            output_model=output_model
        )

        # Analyze function signature
        sig = inspect.signature(func)
        has_docstring = bool(func.__doc__)
        has_type_hints = all(param.annotation != param.empty for param in sig.parameters.values())

        # Auto-generate properties
        properties = ToolProperties(
            tool_type=ToolType.TRANSFORMATION,  # Assume transformation for structured output
            supports_structured_output=True,
            reads_state=config.inject_state,
            state_dependencies=config.state_fields
        )

        # Create enhanced tool
        tool = create_structured_tool_from_function(func, output_model, config)
        return enhance_tool_with_properties(tool, properties)
```

### 6. Complete ToolEngine Implementation

```python
class EnhancedToolEngine(InvokableEngine[ToolInputSchema, ToolOutputSchema]):
    """Complete tool engine implementation following Haive patterns."""

    # Tool Configuration
    tools: list[BaseTool | Tool | StructuredTool | BaseModel] | None = None
    toolkit: BaseToolkit | list[BaseToolkit] | None = None
    retriever_configs: dict[str, EnhancedRetrieverConfig] = Field(default_factory=dict)

    # Routing & Classification
    tool_properties: dict[str, ToolProperties] = Field(default_factory=dict)
    routing_strategy: ToolRoutingStrategy = Field(default="auto_select")

    # Execution Configuration
    retry_policy: RetryPolicy | None = None
    parallel: bool = False
    timeout: float | None = None

    # Integration Features
    structured_output_model: type[BaseModel] | None = None
    state_management: StateManagementConfig = Field(default_factory=StateManagementConfig)

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Define input schema following Haive patterns."""
        return {
            "messages": (list[BaseMessage], Field(..., description="Input messages")),
            "state": (dict[str, Any], Field(default_factory=dict, description="Current state")),
            "tool_selection": (str | None, Field(default=None, description="Specific tool to use")),
            "context": (dict[str, Any], Field(default_factory=dict, description="Additional context"))
        }

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Define output schema following Haive patterns."""
        base_output = {
            "messages": (list[BaseMessage], Field(..., description="Output messages")),
            "tool_results": (list[dict[str, Any]], Field(default_factory=list, description="Tool execution results")),
            "state": (dict[str, Any], Field(default_factory=dict, description="Updated state")),
            "execution_metadata": (dict[str, Any], Field(default_factory=dict, description="Execution metadata"))
        }

        # Add structured output if configured
        if self.structured_output_model:
            model_name = self.structured_output_model.__name__.lower()
            base_output[f"{model_name}_result"] = (
                self.structured_output_model,
                Field(default=None, description=f"Structured {model_name} output")
            )

        return base_output

    def create_runnable(self, runnable_config: RunnableConfig | None = None) -> Any:
        """Create LangGraph ToolNode with enhanced capabilities."""

        # Compile all tools
        all_tools = self._compile_all_tools()

        # Apply tool properties and routing
        enhanced_tools = self._apply_tool_enhancements(all_tools)

        # Create LangGraph ToolNode with routing strategy
        if self.routing_strategy == ToolRoutingStrategy.AUTO_SELECT:
            return ToolNode(enhanced_tools)
        else:
            return CustomToolNode(enhanced_tools, self.routing_strategy, self.state_management)

    def _compile_all_tools(self) -> list[StructuredTool]:
        """Compile tools from all sources."""
        compiled_tools = []

        # Add direct tools
        if self.tools:
            compiled_tools.extend(self._process_tools(self.tools))

        # Add toolkit tools
        if self.toolkit:
            compiled_tools.extend(self._process_toolkits(self.toolkit))

        # Add retriever tools
        for config in self.retriever_configs.values():
            retriever_tool = RetrieverToolFactory.create_retriever_tool(config)
            compiled_tools.append(retriever_tool)

        return compiled_tools

    def _apply_tool_enhancements(self, tools: list[StructuredTool]) -> list[StructuredTool]:
        """Apply properties and routing enhancements to tools."""
        enhanced_tools = []

        for tool in tools:
            # Apply tool properties if available
            if tool.name in self.tool_properties:
                properties = self.tool_properties[tool.name]
                enhanced_tool = enhance_tool_with_properties(tool, properties)
            else:
                # Auto-generate properties if not provided
                properties = self._auto_generate_tool_properties(tool)
                enhanced_tool = enhance_tool_with_properties(tool, properties)

            enhanced_tools.append(enhanced_tool)

        return enhanced_tools

    def _auto_generate_tool_properties(self, tool: StructuredTool) -> ToolProperties:
        """Auto-generate tool properties from tool analysis."""

        # Analyze tool signature and behavior
        has_state_param = self._tool_has_state_parameter(tool)
        has_docstring = bool(tool.description)
        has_structured_schema = hasattr(tool, 'args_schema') and tool.args_schema

        # Classify based on name and description patterns
        tool_type = self._classify_tool_type(tool.name, tool.description)

        return ToolProperties(
            tool_type=tool_type,
            reads_state=has_state_param,
            supports_structured_output=has_structured_schema,
            interruptible=True,  # Default to interruptible
            has_side_effects=self._analyze_side_effects(tool),
        )
```

## Implementation Plan

### Phase 1: Core Infrastructure (Week 1)

1. **Fix Current ToolEngine**: Implement missing abstract methods
2. **Create Enhanced Base Classes**: ToolProperties, routing strategies, state management
3. **Build Tool Analysis System**: Auto-classification and property detection

### Phase 2: Integration Features (Week 2)

1. **Retriever Tool Factory**: Enhanced create_retriever_tool with properties
2. **Structured Output Tools**: Factory for function-to-tool conversion
3. **State Management Integration**: InjectedState patterns and state modification rules

### Phase 3: Advanced Routing (Week 3)

1. **Routing Strategy Implementation**: Rule-based, similarity-based, context-aware
2. **Performance Optimization**: Load balancing, parallel execution, timeout handling
3. **Tool Composition**: Complex multi-tool workflows and coordination

### Phase 4: Integration & Testing (Week 4)

1. **AugLLMConfig Integration**: Seamless tool engine integration with existing LLM config
2. **Agent Integration**: Tool engine support in SimpleAgent, ReactAgent, MultiAgent
3. **Comprehensive Testing**: Real component testing across all tool types and routing strategies

## Key Design Principles

### 1. Follow Haive Patterns

- **Configuration-driven factory pattern**
- **Type-safe field definitions with get_input_fields/get_output_fields**
- **Pydantic validation throughout**
- **LangChain runnable creation**

### 2. Comprehensive Tool Classification

- **Auto-detection of tool properties from signatures and docstrings**
- **Rich property system for routing and execution decisions**
- **Support for all tool interaction patterns (state, structured output, etc.)**

### 3. Flexible Routing System

- **Multiple routing strategies for different use cases**
- **Context-aware tool selection**
- **Performance-based load balancing**

### 4. Seamless Integration

- **Works with existing AugLLMConfig tool integration**
- **Supports agent-as-tool pattern**
- **Compatible with LangGraph workflows**

## Expected Benefits

1. **Complete Tool Engine**: Fixes current incomplete implementation
2. **Sophisticated Routing**: Multiple strategies beyond basic auto-routing
3. **Rich Tool Properties**: Comprehensive classification for intelligent selection
4. **Enhanced Retrievers**: Advanced retriever tool creation with full property support
5. **Structured Output Integration**: Seamless function-to-tool conversion with validation
6. **State Management**: Proper InjectedState support and state modification rules
7. **Performance Optimization**: Timeout, retry, parallel execution, load balancing
8. **Type Safety**: Full schema validation throughout the tool pipeline

This design maintains the elegant Haive architecture while providing the comprehensive tool management capabilities needed for sophisticated agent workflows.

## Tags

`#tool-engine` `#routing-strategies` `#tool-properties` `#retriever-integration` `#structured-output` `#state-management` `#langgraph-integration`
