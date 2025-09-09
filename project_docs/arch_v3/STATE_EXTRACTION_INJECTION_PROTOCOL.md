# State Extraction & Injection Protocol Design

**Created**: 2025-09-08
**Purpose**: Design proper state extraction, injection, and wrapping protocols
**Status**: Active Design
**Problem**: State randomly grabbed from dicts with no contracts

## 🔥 The Current State Chaos

### What Happens Now (The Horror)

```python
# Node receives complete GraphState (could be 100+ fields)
def node_function(state: dict):  # No type!
    # Random field grabbing
    messages = state.get("messages", [])  # Hope it exists!
    context = state.get("context", {})    # Maybe?
    tools = state.get("tools")           # Who knows?

    # Pass partial state to engine
    engine_input = {
        "messages": messages,
        "temperature": state.get("temperature", 0.7)  # Random default
    }

    # Engine does its own extraction
    result = engine.run(engine_input)

    # Shove result back somehow
    state["result"] = result
    return state  # Hope nothing broke
```

### The Problems

1. **No Contracts**: Nodes don't declare what state they need
2. **Type Loss**: Everything becomes dict
3. **Random Access**: `state.get()` everywhere with random defaults
4. **No Validation**: Invalid state passes through
5. **Field Conflicts**: Multiple components write to same fields
6. **No Transformation**: Raw state passed around

## 🎯 Proposed Solution: State Extraction & Injection Protocols

### Core Protocols

```python
from typing import Protocol, TypeVar, Generic, Type
from pydantic import BaseModel

StateT = TypeVar('StateT', bound=BaseModel)
ExtractedT = TypeVar('ExtractedT', bound=BaseModel)
InjectedT = TypeVar('InjectedT', bound=BaseModel)

class StateExtractor(Protocol[StateT, ExtractedT]):
    """Protocol for extracting specific fields from state."""

    def get_required_fields(self) -> list[str]:
        """Declare which fields this component needs."""
        ...

    def extract(self, state: StateT) -> ExtractedT:
        """Extract and transform required fields from state."""
        ...

    def validate_extraction(self, extracted: ExtractedT) -> bool:
        """Validate extracted state meets requirements."""
        ...

class StateInjector(Protocol[InjectedT, StateT]):
    """Protocol for injecting results back into state."""

    def get_injection_fields(self) -> list[str]:
        """Declare which fields this component will modify."""
        ...

    def inject(self, result: InjectedT, state: StateT) -> StateT:
        """Inject results back into state with proper merging."""
        ...

    def validate_injection(self, state: StateT) -> bool:
        """Validate state after injection."""
        ...

class StateTransformer(Protocol[StateT, ExtractedT, InjectedT]):
    """Combined extraction and injection with transformation."""

    def transform_in(self, state: StateT) -> ExtractedT:
        """Transform state for component consumption."""
        ...

    def transform_out(self, result: InjectedT, state: StateT) -> StateT:
        """Transform result and merge back into state."""
        ...
```

## 🔧 Implementation Patterns

### 1. Typed State Requirements

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class NodeStateRequirements(BaseModel):
    """What a node needs from state."""
    messages: List[BaseMessage] = Field(..., description="Conversation history")
    context: dict = Field(default_factory=dict, description="Execution context")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)

class NodeStateOutput(BaseModel):
    """What a node produces."""
    response: str = Field(..., description="Node response")
    metadata: dict = Field(default_factory=dict)
    next_node: Optional[str] = Field(None, description="Routing decision")

class TypedNode(BaseNode):
    """Node with explicit state contracts."""

    input_schema: Type[BaseModel] = NodeStateRequirements
    output_schema: Type[BaseModel] = NodeStateOutput

    def extract_state(self, state: StateSchema) -> NodeStateRequirements:
        """Type-safe extraction."""
        return self.input_schema(
            messages=state.messages,
            context=state.context,
            temperature=state.get("temperature", 0.7)
        )

    def inject_result(self, result: NodeStateOutput, state: StateSchema) -> StateSchema:
        """Type-safe injection."""
        state.messages.append(AIMessage(content=result.response))
        state.metadata.update(result.metadata)
        if result.next_node:
            state.next = result.next_node
        return state

    async def execute(self, state: StateSchema) -> StateSchema:
        """Execute with type safety."""
        # Extract what we need
        extracted = self.extract_state(state)

        # Process with types
        result = await self.process(extracted)

        # Inject back
        return self.inject_result(result, state)
```

### 2. State Wrapper Pattern

```python
class StateWrapper(Generic[StateT]):
    """Wrapper that provides controlled access to state."""

    def __init__(self, state: StateT, access_control: dict[str, set[str]]):
        """Initialize with state and access control.

        Args:
            state: The wrapped state
            access_control: Dict mapping component names to allowed fields
        """
        self._state = state
        self._access_control = access_control
        self._access_log = []  # Track who accessed what
        self._mutation_log = []  # Track who changed what

    def extract_for(self, component: str, schema: Type[BaseModel]) -> BaseModel:
        """Extract state for specific component."""
        allowed_fields = self._access_control.get(component, set())

        # Build extraction dict
        extracted = {}
        for field in schema.model_fields:
            if field in allowed_fields:
                if hasattr(self._state, field):
                    extracted[field] = getattr(self._state, field)
                    self._access_log.append({
                        "component": component,
                        "field": field,
                        "operation": "read"
                    })

        # Create typed result
        return schema(**extracted)

    def inject_from(self, component: str, result: BaseModel) -> None:
        """Inject result from specific component."""
        allowed_fields = self._access_control.get(component, set())

        for field, value in result.model_dump().items():
            if field in allowed_fields:
                old_value = getattr(self._state, field, None)
                setattr(self._state, field, value)
                self._mutation_log.append({
                    "component": component,
                    "field": field,
                    "old_value": old_value,
                    "new_value": value,
                    "operation": "write"
                })
            else:
                raise PermissionError(
                    f"Component {component} not allowed to write field {field}"
                )

    def get_state(self) -> StateT:
        """Get the wrapped state."""
        return self._state

    def get_access_report(self) -> dict:
        """Get access and mutation report."""
        return {
            "accesses": self._access_log,
            "mutations": self._mutation_log
        }
```

### 3. State Projection Pattern

```python
class StateProjection(Generic[StateT, ProjectedT]):
    """Project full state to component-specific view."""

    def __init__(self, projection_map: dict[str, str]):
        """Initialize with field mapping.

        Args:
            projection_map: Maps state fields to projected fields
            Example: {"messages": "conversation", "context": "metadata"}
        """
        self.projection_map = projection_map

    def project(self, state: StateT, target_schema: Type[ProjectedT]) -> ProjectedT:
        """Project state to target schema."""
        projected_data = {}

        for state_field, proj_field in self.projection_map.items():
            if hasattr(state, state_field) and proj_field in target_schema.model_fields:
                value = getattr(state, state_field)
                projected_data[proj_field] = value

        return target_schema(**projected_data)

    def unproject(self, projected: ProjectedT, state: StateT) -> StateT:
        """Merge projected data back to state."""
        for state_field, proj_field in self.projection_map.items():
            if hasattr(projected, proj_field):
                value = getattr(projected, proj_field)
                setattr(state, state_field, value)

        return state
```

### 4. State Lens Pattern (Functional Approach)

```python
from typing import Callable

class StateLens(Generic[StateT, FocusT]):
    """Functional lens for focusing on state subparts."""

    def __init__(
        self,
        getter: Callable[[StateT], FocusT],
        setter: Callable[[StateT, FocusT], StateT]
    ):
        """Initialize with getter and setter.

        Args:
            getter: Function to extract focused part
            setter: Function to update focused part
        """
        self.get = getter
        self.set = setter

    def modify(self, f: Callable[[FocusT], FocusT]) -> Callable[[StateT], StateT]:
        """Create function that modifies focused part."""
        def modifier(state: StateT) -> StateT:
            current = self.get(state)
            modified = f(current)
            return self.set(state, modified)
        return modifier

    def compose(self, other: 'StateLens[FocusT, Any]') -> 'StateLens[StateT, Any]':
        """Compose lenses for nested access."""
        return StateLens(
            getter=lambda s: other.get(self.get(s)),
            setter=lambda s, v: self.set(s, other.set(self.get(s), v))
        )

# Example usage
messages_lens = StateLens(
    getter=lambda state: state.messages,
    setter=lambda state, msgs: setattr(state, 'messages', msgs) or state
)

last_message_lens = StateLens(
    getter=lambda msgs: msgs[-1] if msgs else None,
    setter=lambda msgs, msg: msgs[:-1] + [msg] if msgs else [msg]
)

# Compose for nested access
last_message_of_state = messages_lens.compose(last_message_lens)
```

## 🏗️ Integration with Existing System

### 1. Enhanced Node with State Contracts

```python
class ContractNode(BaseNode):
    """Node with explicit state contracts."""

    # Declare state requirements
    state_requirements: Type[BaseModel]
    state_output: Type[BaseModel]

    # Extraction and injection strategies
    extractor: StateExtractor
    injector: StateInjector

    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)
        self.extractor = self._create_extractor()
        self.injector = self._create_injector()

    def _create_extractor(self) -> StateExtractor:
        """Create appropriate extractor for this node."""
        return TypedExtractor(self.state_requirements)

    def _create_injector(self) -> StateInjector:
        """Create appropriate injector for this node."""
        return TypedInjector(self.state_output)

    async def execute(self, state: StateSchema) -> StateSchema:
        """Execute with proper extraction/injection."""
        # Extract what we need
        extracted = self.extractor.extract(state)

        # Validate extraction
        if not self.extractor.validate_extraction(extracted):
            raise ValueError(f"Invalid state extraction for {self.name}")

        # Process
        result = await self.process(extracted)

        # Inject back
        updated_state = self.injector.inject(result, state)

        # Validate injection
        if not self.injector.validate_injection(updated_state):
            raise ValueError(f"Invalid state injection from {self.name}")

        return updated_state
```

### 2. Engine with State Transformation

```python
class StateAwareEngine(Engine):
    """Engine that properly handles state transformation."""

    input_transformer: StateTransformer
    output_transformer: StateTransformer

    def __init__(self, config: EngineConfig, **kwargs):
        super().__init__(config, **kwargs)
        self.input_transformer = self._create_input_transformer()
        self.output_transformer = self._create_output_transformer()

    async def execute_with_state(self, state: StateSchema) -> StateSchema:
        """Execute with proper state transformation."""
        # Transform state to engine input
        engine_input = self.input_transformer.transform_in(state)

        # Execute engine
        result = await self.execute(engine_input)

        # Transform and merge back
        return self.output_transformer.transform_out(result, state)
```

### 3. Graph with State Flow Control

```python
class StateControlledGraph(BaseGraph):
    """Graph with controlled state flow."""

    def __init__(self, state_schema: Type[StateSchema]):
        super().__init__(state_schema)
        self.access_control = {}  # Node -> allowed fields
        self.state_flow = {}  # Node -> node state transfer rules

    def add_node_with_contracts(
        self,
        name: str,
        node: ContractNode,
        readable_fields: set[str],
        writable_fields: set[str]
    ):
        """Add node with explicit field access."""
        self.add_node(name, node)
        self.access_control[name] = {
            "read": readable_fields,
            "write": writable_fields
        }

    def add_edge_with_transform(
        self,
        from_node: str,
        to_node: str,
        transformer: Optional[StateTransformer] = None
    ):
        """Add edge with optional state transformation."""
        self.add_edge(from_node, to_node)
        if transformer:
            self.state_flow[f"{from_node}->{to_node}"] = transformer

    async def execute_node(self, node_name: str, state: StateSchema) -> StateSchema:
        """Execute node with controlled state access."""
        node = self.nodes[node_name]
        access = self.access_control.get(node_name, {})

        # Wrap state for controlled access
        wrapped = StateWrapper(state, {node_name: access})

        # Execute with wrapped state
        result = await node.execute(wrapped)

        # Get access report
        report = wrapped.get_access_report()
        self.log_state_access(node_name, report)

        return wrapped.get_state()
```

## 🎯 Benefits of This Approach

### 1. Type Safety

- Every component declares its input/output schemas
- Compile-time checking of state access
- No more random `state.get()` calls

### 2. Explicit Contracts

- Nodes declare what fields they need
- Clear read/write permissions
- Validated extraction and injection

### 3. Debugging & Monitoring

- Track which component accessed which fields
- Audit trail of state mutations
- Clear data flow visibility

### 4. Performance

- Only extract needed fields
- Avoid copying entire state
- Lazy evaluation possible

### 5. Composability

- Lenses compose for nested access
- Transformers chain together
- Projections can be stacked

## 📋 Migration Strategy

### Phase 1: Add Contracts to New Components

```python
# New nodes use contracts
class MyNode(ContractNode):
    state_requirements = MyInputSchema
    state_output = MyOutputSchema
```

### Phase 2: Wrap Existing Components

```python
# Wrap old nodes
class LegacyNodeWrapper(ContractNode):
    def __init__(self, legacy_node):
        self.legacy_node = legacy_node
        # Infer contracts from usage
```

### Phase 3: Gradual Migration

```python
# Update components incrementally
# Old and new can coexist during transition
```

## 🚨 Critical Design Decisions

### 1. Extraction Strategy

- **Option A**: Explicit field lists (current)
- **Option B**: Schema-based automatic
- **Option C**: Annotation-based (`@extracts`, `@injects`)

### 2. Validation Approach

- **Option A**: Pydantic validation (type-based)
- **Option B**: Custom validators per component
- **Option C**: Graph-level validation rules

### 3. State Wrapper Implementation

- **Option A**: Proxy objects with access control
- **Option B**: Immutable state with transformations
- **Option C**: Copy-on-write semantics

### 4. Performance Optimization

- **Option A**: Lazy extraction (on-demand)
- **Option B**: Pre-compute projections
- **Option C**: Cache transformed states

## 🔄 Example: Complete Flow

```python
# 1. Define schemas
class AgentInput(BaseModel):
    messages: List[BaseMessage]
    temperature: float = 0.7

class AgentOutput(BaseModel):
    response: str
    confidence: float

# 2. Create node with contracts
class SmartAgentNode(ContractNode):
    state_requirements = AgentInput
    state_output = AgentOutput

    async def process(self, input: AgentInput) -> AgentOutput:
        # Type-safe processing
        response = await self.llm.generate(
            messages=input.messages,
            temperature=input.temperature
        )
        return AgentOutput(
            response=response.content,
            confidence=0.95
        )

# 3. Use in graph
graph = StateControlledGraph(ConversationState)
graph.add_node_with_contracts(
    "agent",
    SmartAgentNode(),
    readable_fields={"messages", "temperature", "context"},
    writable_fields={"messages", "agent_response", "confidence"}
)

# 4. Execute with controlled state flow
state = ConversationState(messages=[...])
result = await graph.execute(state)
# State access is controlled, typed, and audited!
```

## 🔑 Key Takeaways

1. **No more dict diving** - Explicit contracts for state access
2. **Type safety throughout** - Schemas for input/output
3. **Controlled mutations** - Know who changes what
4. **Composable patterns** - Lenses, projections, transformers
5. **Gradual migration** - Old and new can coexist

This approach would reduce complexity from 82🔥 to <20🔥 by making state flow explicit, typed, and controlled!
