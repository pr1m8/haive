# Agent Architecture Evolution Plan

**Date**: 2025-01-09  
**Phase**: Advanced Architecture Development  
**Goal**: Implement generic agent classification, dynamic graph modification, and structured output redesign

## Current State Analysis

### Completed ✅

- Generic engine typing system with schema composer intelligence
- State schema with engine I/O mixin separation
- SimpleAgent and ReactAgent using v2 nodes
- Engine addition methods for dynamic expansion

### Architecture Insights

- ReactAgent inherits v2 nodes from SimpleAgent (correct pattern)
- Tool-routed nodes vs engine nodes distinction is crucial
- Schema composer needs to work with node configs, not just state schemas

## Phase 1: Agent Classification Framework

### 1.1 Base Agent Taxonomy

```python
# Agent type hierarchy
class AgentType(Enum):
    LLM_BASED = "llm_based"        # SimpleAgent, ReactAgent
    WORKFLOW = "workflow"          # Pure orchestration
    MULTI_AGENT = "multi_agent"    # Agent orchestration
    META = "meta"                  # Graph modification

class AgentCapability(Enum):
    STRUCTURED_OUTPUT = "structured_output"
    TOOL_ROUTING = "tool_routing"
    DYNAMIC_GRAPH = "dynamic_graph"
    MESSAGE_TRANSFORM = "message_transform"
```

### 1.2 Generic Agent Base

```python
class GenericAgent(Agent, Generic[TEngine, TCapabilities]):
    """Generic agent with type-safe capabilities."""
    agent_type: AgentType
    capabilities: Set[AgentCapability]
    tool_routed_nodes: List[str] = Field(default_factory=list)
```

## Phase 2: Schema Composer + Node Config Integration

### 2.1 Node Config Schema Composition

```python
# Schema composer works with node configs
composer.add_node_config(tool_node_config)  # Extracts I/O fields
composer.add_node_config(validation_node_config)  # Adds validation fields
composer.add_callable_node(my_function)  # Creates node from function
```

### 2.2 Callable Node Factory

```python
@node_from_callable
def custom_processor(state: MyState) -> Command:
    # Custom processing logic
    return Command(update={"processed": True})

# Auto-generates node config with I/O inference
```

## Phase 3: Structured Output Redesign

### 3.1 Current Problem

```python
# Current: SimpleAgent with structured_output_model
agent = SimpleAgent(
    engine=llm_engine,
    structured_output_model=TaskResult
)
```

### 3.2 Proposed Solution: Sequential Multi-Agent Pattern

```python
# New: Sequential multi-agent with adapter
structured_agent = SequentialAgent([
    SimpleAgent(engine=llm_engine),
    AdapterAgent(
        input_schema=SimpleAgentOutput,
        output_schema=TaskResult,
        transform_template=prompt_template
    )
])
```

### 3.3 Generalized Pattern

- Any structured output becomes sequential multi-agent
- Adapter handles schema transformation
- Template-based or function-based adaptation

## Phase 4: Output Processing Consolidation

### 4.1 Unified Output Processing

```python
class OutputProcessor(Generic[TInput, TOutput]):
    """Unified output processing interface."""

    def process_message(self, message: BaseMessage) -> BaseMessage
    def parse_structured(self, content: str) -> TOutput
    def transform_schema(self, input_data: TInput) -> TOutput
```

### 4.2 Message Transformation Nodes

```python
# Consolidate: parse_output, output_parser, message_transformer
class MessageTransformNode(BaseNodeConfig):
    processor: OutputProcessor
    field_mapping: Dict[str, str]  # output_field -> state_field
```

## Phase 5: Dynamic Graph Modification

### 5.1 Meta-State Tracking

```python
class MetaState(StateSchema):
    graph_version: int = Field(default=1)
    pending_modifications: List[GraphModification] = Field(default_factory=list)
    recompile_needed: bool = Field(default=False)
    checkpoint_before_recompile: Optional[str] = Field(default=None)
```

### 5.2 Graph Modification Operations

```python
class GraphModification(BaseModel):
    operation: Literal["add_node", "remove_node", "add_edge", "modify_branch"]
    node_config: Optional[BaseNodeConfig] = None
    edge_config: Optional[EdgeConfig] = None
    checkpoint_safe: bool = True  # Can resume from checkpoint
```

### 5.3 Recompilation Flow

```python
# Detection -> Checkpoint -> Modify -> Recompile -> Resume
if state.recompile_needed:
    checkpoint_id = agent.create_checkpoint()
    agent.apply_modifications(state.pending_modifications)
    agent.recompile_graph()
    agent.resume_from_checkpoint(checkpoint_id)
```

## Phase 6: Token-based Message State

### 6.1 Replace Prebuilt Messages

```python
# Current: Generic messages state
messages: List[BaseMessage]

# New: Token-aware message state
class TokenMessageState(StateSchema):
    messages: List[BaseMessage]
    token_count: int = Field(default=0)
    token_limit: Optional[int] = Field(default=None)
    truncation_strategy: TokenTruncationStrategy = Field(default="sliding_window")
```

### 6.2 Token Management

```python
def add_message_with_tokens(state: TokenMessageState, message: BaseMessage):
    """Add message while managing token limits."""
    token_cost = estimate_tokens(message)
    if state.token_count + token_cost > state.token_limit:
        state.messages = truncate_messages(state.messages, state.truncation_strategy)
    state.messages.append(message)
    state.token_count += token_cost
```

## Implementation Priority

### Phase 1 (Immediate)

1. **Agent classification framework** - Define AgentType and capabilities
2. **Tool-routed nodes tracking** - Add tool_routed_nodes field
3. **Generic agent base** - Create GenericAgent with typing

### Phase 2 (Short-term)

1. **Schema composer + node configs** - Extend composer to work with nodes
2. **Callable node factory** - @node_from_callable decorator
3. **Structured output redesign** - Sequential multi-agent pattern

### Phase 3 (Medium-term)

1. **Output processing consolidation** - Unified OutputProcessor
2. **Message transformation** - Consolidate parsing nodes
3. **Token-based messages** - Replace prebuilt message state

### Phase 4 (Long-term)

1. **Meta-state implementation** - Graph modification tracking
2. **Dynamic recompilation** - Safe checkpoint/resume flow
3. **Advanced capabilities** - Dynamic edge modification, branch changes

## Success Criteria

- [ ] Clear agent type classification system
- [ ] Schema composer works with node configs
- [ ] Structured output uses sequential multi-agent pattern
- [ ] Unified output processing interface
- [ ] Token-aware message management
- [ ] Dynamic graph modification with safe recompilation
- [ ] Backward compatibility maintained
- [ ] Performance impact minimal

## Key Design Principles

1. **Composition over inheritance** - Use capabilities and mixins
2. **Type safety** - Generics and proper typing throughout
3. **Extensibility** - Easy to add new agent types and capabilities
4. **Safety** - Checkpointing before dangerous operations
5. **Performance** - Token management and efficient recompilation
6. **Clarity** - Clear distinction between agent types and node types

This plan builds on our v2 node foundation and creates a sophisticated, extensible agent architecture that can handle complex workflows, dynamic modification, and type-safe composition.
