# Typed State-Engine-Node Integration Architecture

**Created**: 2025-09-08
**Purpose**: Integrate state extraction/injection with Engine decomposition and Node consolidation using proper typing
**Status**: Active Design
**Goal**: Type-safe, contract-based component interaction

## 🎯 The Vision: Fully Typed Component Flow

```python
# What we want:
StateT → ExtractorT → EngineInputT → EngineOutputT → InjectorT → StateT

# With compile-time type checking at every boundary!
```

## 📐 Core Type System Design

### 1. Generic Type Variables

```python
from typing import TypeVar, Generic, Protocol
from pydantic import BaseModel

# State types
StateT = TypeVar('StateT', bound='BaseState')
PartialStateT = TypeVar('PartialStateT', bound=BaseModel)

# Engine types
EngineInputT = TypeVar('EngineInputT', bound=BaseModel)
EngineOutputT = TypeVar('EngineOutputT', bound=BaseModel)
EngineConfigT = TypeVar('EngineConfigT', bound='BaseEngineConfig')

# Node types
NodeInputT = TypeVar('NodeInputT', bound=BaseModel)
NodeOutputT = TypeVar('NodeOutputT', bound=BaseModel)
NodeStateT = TypeVar('NodeStateT', bound='BaseState')

# Message types
MessageT = TypeVar('MessageT', bound='BaseMessage')
ConversationT = TypeVar('ConversationT', bound=list[MessageT])
```

### 2. Base State Protocol with Typing

```python
class BaseState(BaseModel, Generic[PartialStateT]):
    """Base state with typed extraction/injection."""

    @classmethod
    def extract_for[T: BaseModel](cls, component: type[T]) -> T:
        """Extract typed subset for component."""
        ...

    def inject_from[T: BaseModel](self, result: T, component: type) -> 'BaseState':
        """Inject typed result from component."""
        ...

    def project_to[T: BaseState](self, target_type: type[T]) -> T:
        """Project to different state type."""
        ...

class ConversationState(BaseState):
    """Typed conversation state."""
    messages: list[BaseMessage]
    context: dict[str, Any]
    metadata: dict[str, Any]

    def extract_messages(self) -> list[BaseMessage]:
        """Type-safe message extraction."""
        return self.messages

    def extract_for_llm(self) -> 'LLMInput':
        """Extract and transform for LLM engine."""
        return LLMInput(
            messages=self.messages,
            temperature=self.context.get('temperature', 0.7)
        )
```

## 🔧 Engine Decomposition with Proper Typing

### 1. Typed Engine Configs (Decomposed from AugLLMConfig)

```python
# Pure LLM Config
class LLMConfig(BaseModel, Generic[MessageT]):
    """Pure LLM configuration with message type."""
    model: str
    temperature: float
    max_tokens: int | None

    def validate_messages(self, messages: list[MessageT]) -> list[MessageT]:
        """Type-safe message validation."""
        return messages

# Tool Config with proper types
class ToolConfig(BaseModel, Generic[ToolT]):
    """Tool configuration with tool type."""
    tools: list[ToolT]
    tool_routes: dict[str, str]

    def get_tool[T](self, name: str, tool_type: type[T]) -> T | None:
        """Get typed tool by name."""
        for tool in self.tools:
            if tool.name == name and isinstance(tool, tool_type):
                return tool
        return None

# Structured Output Config
class StructuredOutputConfig(BaseModel, Generic[OutputT]):
    """Structured output with output type."""
    output_model: type[OutputT]
    validation_mode: Literal['strict', 'lenient']

    def validate_output(self, output: Any) -> OutputT:
        """Validate and return typed output."""
        return self.output_model.model_validate(output)
```

### 2. Typed Engine Interfaces

```python
class TypedEngine(Protocol[EngineInputT, EngineOutputT, EngineConfigT]):
    """Fully typed engine protocol."""

    config: EngineConfigT

    def validate_input(self, input: Any) -> EngineInputT:
        """Validate input to engine type."""
        ...

    def execute(self, input: EngineInputT) -> EngineOutputT:
        """Execute with typed input/output."""
        ...

    async def aexecute(self, input: EngineInputT) -> EngineOutputT:
        """Async execute with typed input/output."""
        ...

class LLMEngine(TypedEngine[LLMInput, LLMOutput, LLMConfig]):
    """Concrete LLM engine with full typing."""

    def __init__(self, config: LLMConfig):
        self.config = config

    def validate_input(self, input: Any) -> LLMInput:
        """Validate to LLMInput."""
        if isinstance(input, LLMInput):
            return input
        elif isinstance(input, dict):
            return LLMInput.model_validate(input)
        else:
            raise TypeError(f"Cannot convert {type(input)} to LLMInput")

    async def aexecute(self, input: LLMInput) -> LLMOutput:
        """Execute LLM with typed IO."""
        # Actual LLM call
        response = await self._call_llm(
            messages=input.messages,
            **self.config.model_dump()
        )
        return LLMOutput(
            content=response.content,
            metadata=response.metadata
        )

class ToolEngine(TypedEngine[ToolInput, ToolOutput, ToolConfig]):
    """Tool engine with proper typing."""

    def __init__(self, config: ToolConfig[ToolT]):
        self.config = config

    async def aexecute(self, input: ToolInput) -> ToolOutput:
        """Execute tool with type safety."""
        tool = self.config.get_tool(input.tool_name, Tool)
        if not tool:
            raise ValueError(f"Tool {input.tool_name} not found")

        result = await tool.arun(input.tool_input)
        return ToolOutput(
            tool_name=input.tool_name,
            result=result
        )
```

## 🔌 Node Consolidation with State Contracts

### 1. The 4 Core Typed Nodes

```python
class ExecutionNode(Generic[NodeInputT, NodeOutputT, EngineT]):
    """Pure execution node with engine type."""

    input_schema: type[NodeInputT]
    output_schema: type[NodeOutputT]
    engine: EngineT

    def extract_from_state(self, state: StateT) -> NodeInputT:
        """Extract typed input from state."""
        return state.extract_for(self.input_schema)

    def inject_to_state(self, output: NodeOutputT, state: StateT) -> StateT:
        """Inject typed output to state."""
        return state.inject_from(output, self.__class__)

    async def execute(self, state: StateT) -> StateT:
        """Execute with full type flow."""
        # Extract
        node_input = self.extract_from_state(state)

        # Transform for engine
        engine_input = self.transform_to_engine_input(node_input)

        # Execute engine
        engine_output = await self.engine.aexecute(engine_input)

        # Transform from engine
        node_output = self.transform_from_engine_output(engine_output)

        # Inject
        return self.inject_to_state(node_output, state)

    @abstractmethod
    def transform_to_engine_input(self, input: NodeInputT) -> EngineInputT:
        """Transform node input to engine input."""
        ...

    @abstractmethod
    def transform_from_engine_output(self, output: EngineOutputT) -> NodeOutputT:
        """Transform engine output to node output."""
        ...

class ValidationNode(Generic[ValidatedT]):
    """Validation node with validated type."""

    validation_schema: type[ValidatedT]
    validation_rules: list[Callable[[ValidatedT], bool]]

    def validate(self, state: StateT) -> tuple[bool, ValidatedT | None]:
        """Validate state to typed schema."""
        try:
            validated = state.extract_for(self.validation_schema)

            for rule in self.validation_rules:
                if not rule(validated):
                    return False, None

            return True, validated
        except Exception:
            return False, None

class RoutingNode(Generic[RouteInputT]):
    """Routing node with route input type."""

    route_schema: type[RouteInputT]
    routes: dict[str, Callable[[RouteInputT], bool]]

    def determine_route(self, state: StateT) -> str:
        """Determine route with typed input."""
        route_input = state.extract_for(self.route_schema)

        for route_name, condition in self.routes.items():
            if condition(route_input):
                return route_name

        return "default"

class TerminalNode(Generic[FinalT]):
    """Terminal node with final output type."""

    output_schema: type[FinalT]

    def finalize(self, state: StateT) -> FinalT:
        """Finalize to typed output."""
        return state.extract_for(self.output_schema)
```

### 2. Concrete Typed Node Examples

```python
# Define specific types
class ChatInput(BaseModel):
    messages: list[BaseMessage]
    temperature: float = 0.7

class ChatOutput(BaseModel):
    response: str
    confidence: float

class ChatNode(ExecutionNode[ChatInput, ChatOutput, LLMEngine]):
    """Concrete chat node with full typing."""

    input_schema = ChatInput
    output_schema = ChatOutput

    def __init__(self, name: str, llm_config: LLMConfig):
        self.name = name
        self.engine = LLMEngine(llm_config)

    def transform_to_engine_input(self, input: ChatInput) -> LLMInput:
        """Transform chat input to LLM input."""
        return LLMInput(
            messages=input.messages,
            temperature=input.temperature
        )

    def transform_from_engine_output(self, output: LLMOutput) -> ChatOutput:
        """Transform LLM output to chat output."""
        return ChatOutput(
            response=output.content,
            confidence=output.metadata.get('confidence', 0.9)
        )
```

## 🔄 State Flow with Full Typing

### 1. Typed State Extractor

```python
class TypedStateExtractor(Generic[StateT, ExtractedT]):
    """Extract typed subset from state."""

    def __init__(
        self,
        source_type: type[StateT],
        target_type: type[ExtractedT],
        field_mapping: dict[str, str]
    ):
        self.source_type = source_type
        self.target_type = target_type
        self.field_mapping = field_mapping

    def extract(self, state: StateT) -> ExtractedT:
        """Extract with type safety."""
        extracted_data = {}

        for source_field, target_field in self.field_mapping.items():
            if hasattr(state, source_field):
                value = getattr(state, source_field)
                extracted_data[target_field] = value

        return self.target_type.model_validate(extracted_data)

    def extract_partial(self, state: StateT, fields: set[str]) -> dict[str, Any]:
        """Extract partial state as dict."""
        return {
            field: getattr(state, field)
            for field in fields
            if hasattr(state, field)
        }
```

### 2. Typed State Injector

```python
class TypedStateInjector(Generic[InjectedT, StateT]):
    """Inject typed result into state."""

    def __init__(
        self,
        source_type: type[InjectedT],
        target_type: type[StateT],
        merge_strategy: Literal['replace', 'append', 'merge']
    ):
        self.source_type = source_type
        self.target_type = target_type
        self.merge_strategy = merge_strategy

    def inject(self, result: InjectedT, state: StateT) -> StateT:
        """Inject with type safety."""
        state_dict = state.model_dump()
        result_dict = result.model_dump()

        if self.merge_strategy == 'replace':
            state_dict.update(result_dict)
        elif self.merge_strategy == 'append':
            for key, value in result_dict.items():
                if key in state_dict and isinstance(state_dict[key], list):
                    state_dict[key].append(value)
                else:
                    state_dict[key] = value
        elif self.merge_strategy == 'merge':
            # Deep merge logic
            state_dict = self._deep_merge(state_dict, result_dict)

        return self.target_type.model_validate(state_dict)
```

### 3. Complete Typed Flow

```python
class TypedGraphFlow(Generic[InitialStateT, FinalStateT]):
    """Graph with fully typed state flow."""

    def __init__(
        self,
        initial_state_type: type[InitialStateT],
        final_state_type: type[FinalStateT]
    ):
        self.initial_state_type = initial_state_type
        self.final_state_type = final_state_type
        self.nodes: dict[str, TypedNode] = {}
        self.edges: dict[str, list[str]] = {}
        self.transformers: dict[str, StateTransformer] = {}

    def add_typed_node[
        NodeT: TypedNode
    ](
        self,
        name: str,
        node: NodeT,
        extractor: TypedStateExtractor,
        injector: TypedStateInjector
    ) -> None:
        """Add node with typed extraction/injection."""
        self.nodes[name] = node
        node.extractor = extractor
        node.injector = injector

    async def execute(self, initial_state: InitialStateT) -> FinalStateT:
        """Execute with full type flow."""
        current_state: Any = initial_state

        for node_name in self.get_execution_order():
            node = self.nodes[node_name]

            # Type-safe execution
            current_state = await node.execute(current_state)

            # Validate state type after each step
            if not isinstance(current_state, BaseState):
                raise TypeError(f"Node {node_name} returned invalid state type")

        # Final type validation
        if not isinstance(current_state, self.final_state_type):
            # Try to convert
            current_state = current_state.project_to(self.final_state_type)

        return current_state
```

## 🎯 Putting It All Together

### Complete Example with Full Typing

```python
# 1. Define all types
class ConversationInput(BaseModel):
    user_message: str
    history: list[BaseMessage]
    context: dict[str, Any]

class ConversationState(BaseState):
    messages: list[BaseMessage]
    context: dict[str, Any]
    current_response: str | None = None
    confidence: float = 0.0

class AgentInput(BaseModel):
    messages: list[BaseMessage]
    temperature: float

class AgentOutput(BaseModel):
    response: str
    confidence: float
    metadata: dict[str, Any]

# 2. Create typed engines
llm_config = LLMConfig[BaseMessage](
    model="gpt-4",
    temperature=0.7,
    max_tokens=1000
)

llm_engine = LLMEngine(llm_config)

# 3. Create typed nodes
class AgentNode(ExecutionNode[AgentInput, AgentOutput, LLMEngine]):
    input_schema = AgentInput
    output_schema = AgentOutput

    def transform_to_engine_input(self, input: AgentInput) -> LLMInput:
        return LLMInput(
            messages=input.messages,
            temperature=input.temperature
        )

    def transform_from_engine_output(self, output: LLMOutput) -> AgentOutput:
        return AgentOutput(
            response=output.content,
            confidence=0.95,
            metadata=output.metadata
        )

agent_node = AgentNode(
    name="agent",
    engine=llm_engine
)

# 4. Set up extractors and injectors
extractor = TypedStateExtractor(
    source_type=ConversationState,
    target_type=AgentInput,
    field_mapping={
        "messages": "messages",
        "context.temperature": "temperature"
    }
)

injector = TypedStateInjector(
    source_type=AgentOutput,
    target_type=ConversationState,
    merge_strategy='merge'
)

# 5. Create typed graph
graph = TypedGraphFlow[
    ConversationState,
    ConversationState
](
    initial_state_type=ConversationState,
    final_state_type=ConversationState
)

graph.add_typed_node(
    "agent",
    agent_node,
    extractor,
    injector
)

# 6. Execute with full type safety
initial_state = ConversationState(
    messages=[UserMessage(content="Hello")],
    context={"temperature": 0.8}
)

final_state = await graph.execute(initial_state)
# Type checker knows final_state is ConversationState!
```

## 🔥 Benefits of This Approach

### 1. **Compile-Time Type Safety**

- Every boundary has type checking
- IDE autocomplete works everywhere
- Catch errors before runtime

### 2. **Clear Contracts**

- Each component declares its types
- No ambiguity about what goes where
- Self-documenting code

### 3. **Modular Composition**

- Engines are properly decomposed
- Nodes have single responsibilities
- State flows are explicit

### 4. **Performance**

- Type validation happens once
- No runtime type checking needed
- Optimized state extraction

### 5. **Debugging**

- Clear type errors at boundaries
- Traceable state transformations
- Explicit data flow

## 📊 Complexity Reduction

### Before (82🔥)

- Untyped dicts everywhere
- No contracts between components
- AugLLMConfig doing everything
- 12+ node types with mixed concerns
- Random state mutation

### After (<20🔥)

- Full typing throughout
- Clear extraction/injection contracts
- 6 focused engine configs
- 4 single-purpose nodes
- Controlled state flow

## 🚀 Migration Strategy

### Phase 1: Add Types to New Components

```python
# New components use full typing
class MyNode(ExecutionNode[InputT, OutputT, EngineT]):
    ...
```

### Phase 2: Wrap Existing Components

```python
# Adapter for old components
class LegacyNodeAdapter(ExecutionNode):
    def __init__(self, legacy_node):
        self.legacy = legacy_node
        # Infer types from usage
```

### Phase 3: Gradual Type Addition

```python
# Add types incrementally
# Old and new coexist
```

## 🔑 Key Insights

1. **Types are Documentation**: The types tell you exactly what each component needs and produces
2. **Boundaries are Contracts**: Every component boundary has explicit type contracts
3. **State is Controlled**: No more random state mutation - everything goes through typed extractors/injectors
4. **Engines are Focused**: Each engine does one thing with clear types
5. **Nodes are Simple**: Each node type has a single, well-typed responsibility

This architecture would transform the chaotic 82🔥 system into a clean, typed, <20🔥 system!
