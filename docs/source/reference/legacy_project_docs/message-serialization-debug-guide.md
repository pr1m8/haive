# Comprehensive Debug Guide: Message Serialization Issues in Multi-Agent Systems

## Executive Summary

We're experiencing a `KeyError: 'tool_call_id'` when messages pass between agents in a sequential multi-agent system. The error occurs when `SimpleAgent` receives messages from `ReactAgent`, specifically when trying to reconstruct a `ToolMessage` that has lost its required `tool_call_id` field during state transfer.

## 1. Problem Statement

### Current Behavior

```
ReactAgent → Creates ToolMessage(tool_call_id="abc123") → Success
     ↓
State Transfer (serialization/deserialization)
     ↓
SimpleAgent → Receives dict without tool_call_id → KeyError
```

### Expected Behavior

Messages should maintain all required fields across agent boundaries, including `tool_call_id` for ToolMessages.

## 2. Architecture Overview

### Key Components

1. **ExecutionMixin** - Handles agent execution and input preparation
2. **Agent Base Class** - Manages schemas, engines, and persistence
3. **SchemaComposer** - Builds state schemas from engines
4. **AgentNode** - Executes agents in multi-agent graphs
5. **MultiAgent Base** - Orchestrates sequential/parallel agent execution

### Message Flow

```
User Input → ExecutionMixin._prepare_input() → Agent.invoke()
    → Graph Execution → AgentNode.__call__() → State Transfer
    → Next Agent → ExecutionMixin._prepare_input() → ERROR
```

## 3. Potential Issue Areas

### 3.1 ExecutionMixin Issues

#### A. Serialization Boundary Problems

**Issue**: The `_prepare_input` method may not properly preserve BaseMessage objects when converting between different input formats.

**Current Code Analysis**:

```python
# In _prepare_input()
if isinstance(input_data, BaseModel):
    data_dict = input_data.model_dump()  # <- This might lose fields!
```

**Debug Steps**:

1. Add logging before/after `model_dump()` calls
2. Check if `tool_call_id` exists in the original object but not in the dict
3. Verify `exclude_none` or other Pydantic config isn't dropping fields

#### B. Parent I/O Schema Mismatch

**Issue**: Child agents might not properly inherit or respect parent schema definitions.

**Debug Steps**:

1. Log `input_schema` and `output_schema` for each agent
2. Verify schema compatibility between sequential agents
3. Check if schemas are being auto-derived vs explicitly set

#### C. Message List Handling

**Issue**: The agent might be treating messages as individual items rather than preserving the list structure.

**Debug Steps**:

1. Log the type and structure of messages at each stage
2. Check if messages are being unpacked/repacked incorrectly
3. Verify list vs individual message handling

### 3.2 SchemaComposer & AugLLMConfig Issues

#### A. BaseMessage vs AnyMessage

**Issue**: Schema might be using strict `BaseMessage` typing when it should use `AnyMessage` for serialization compatibility.

**Current State**:

```python
# Strict typing
messages: List[BaseMessage]  # Requires objects

# Flexible typing
messages: List[AnyMessage]  # Accepts dicts OR objects
```

**Debug Steps**:

1. Check what type annotations are used in generated schemas
2. Test with `AnyMessage` to see if error persists
3. Verify LangChain's `convert_to_messages` behavior with different types

#### B. Shared Fields Updates

**Issue**: When multiple agents share a schema, field updates might not propagate correctly.

**Debug Steps**:

1. Log schema field definitions for each agent
2. Track field modifications during execution
3. Verify shared vs agent-specific fields

### 3.3 AgentNode Critical Issues

#### A. State Serialization for Checkpointing

**Issue**: The `_serialize_engine_for_state` exists but there's no equivalent for messages.

**Current Code**:

```python
def _serialize_engine_for_state(self, engine: Any) -> Dict[str, Any]:
    # Handles engines...

def _serialize_tool_for_state(self, tool: Any) -> Dict[str, Any]:
    # Handles tools...

# No _serialize_message_for_state!
```

**Debug Steps**:

1. Log message state before/after serialization
2. Check if custom message serialization is needed
3. Verify msgpack compatibility with ToolMessage fields

#### B. Message Extraction from State

**Issue**: When extracting messages from state, the conversion might lose fields.

**Current Code Analysis**:

```python
# In agent_node.py
if hasattr(state, 'messages'):
    state_dict['messages'] = actual_messages  # Are these preserved correctly?
```

**Debug Steps**:

1. Log message integrity at state extraction
2. Verify no intermediate conversions drop fields
3. Check if state dict properly maintains message objects

## 4. Debugging Strategy

### Phase 1: Isolate the Error Location

```python
# Add comprehensive logging at these points:

1. ReactAgent output:
   - Log the complete ToolMessage object
   - Log tool_call_id explicitly
   - Log serialized form

2. State Transfer:
   - Log state before leaving ReactAgent
   - Log state entering SimpleAgent
   - Compare message structures

3. SimpleAgent input:
   - Log raw input data
   - Log after _prepare_input
   - Log at point of error
```

### Phase 2: Trace the Serialization Path

```python
# Create a message tracker:
class MessageTracker:
    @staticmethod
    def log_message_state(location: str, messages: List[Any]):
        for i, msg in enumerate(messages):
            if isinstance(msg, ToolMessage):
                logger.info(f"{location} - ToolMessage {i}:")
                logger.info(f"  tool_call_id: {getattr(msg, 'tool_call_id', 'MISSING')}")
                logger.info(f"  type: {type(msg)}")
                logger.info(f"  __dict__: {msg.__dict__}")
            elif isinstance(msg, dict) and msg.get('type') == 'tool':
                logger.info(f"{location} - Tool dict {i}:")
                logger.info(f"  keys: {list(msg.keys())}")
                logger.info(f"  tool_call_id: {msg.get('tool_call_id', 'MISSING')}")
```

### Phase 3: Test Fixes Incrementally

#### Fix 1: Preserve BaseMessage Objects

```python
# In ExecutionMixin._prepare_input
if "messages" in input_data and all(isinstance(m, BaseMessage) for m in input_data["messages"]):
    # Don't convert, preserve as-is
    validation_data = {k: v for k, v in input_data.items() if k != "messages"}
    result = input_schema(**validation_data)
    result.messages = input_data["messages"]  # Preserve objects
    return result
```

#### Fix 2: Use AnyMessage Type

```python
# In schema generation
from langchain_core.messages import AnyMessage

class FlexibleMessageState(BaseModel):
    messages: List[AnyMessage] = Field(default_factory=list)
```

#### Fix 3: Custom Message Reducer

```python
def preserve_messages(left: List, right: List) -> List:
    """Custom reducer that preserves message objects."""
    result = left.copy() if left else []
    for msg in right:
        if isinstance(msg, BaseMessage):
            result.append(msg)  # Don't convert!
        else:
            # Only convert if necessary
            converted = convert_to_messages([msg])
            result.extend(converted)
    return result
```

## 5. Testing Protocol

### Test 1: Single Agent Message Preservation

```python
# Test if a single agent preserves ToolMessage
tool_msg = ToolMessage(content="test", tool_call_id="123")
agent = SimpleAgent(engine=engine)
result = agent.run({"messages": [tool_msg]})
assert result.messages[-1].tool_call_id == "123"
```

### Test 2: Multi-Agent Message Transfer

```python
# Test if messages survive agent transfer
agents = SequentialAgent(agents=[agent1, agent2])
result = agents.run(input_with_tool_message)
# Check if tool_call_id preserved
```

### Test 3: Checkpoint/Restore Cycle

```python
# Test if messages survive checkpointing
result1 = agent.run(input_data, thread_id="test")
result2 = agent.run({"messages": []}, thread_id="test")  # Should restore
# Verify tool_call_id in restored messages
```

## 6. Root Cause Hypotheses

### Hypothesis 1: Pydantic Serialization

- `model_dump()` might exclude optional fields
- `tool_call_id` might be marked as optional in ToolMessage schema
- Fix: Use `model_dump(exclude_none=False, exclude_unset=False)`

### Hypothesis 2: LangGraph Message Reducer

- The `add_messages` reducer calls `convert_to_messages`
- This conversion might not preserve all fields
- Fix: Use custom reducer or `operator.add`

### Hypothesis 3: State Transfer Serialization

- Messages are being serialized for msgpack compatibility
- The serialization loses Python object structure
- Fix: Implement proper message serialization protocol

### Hypothesis 4: Schema Type Mismatch

- Input schema expects `BaseMessage` objects
- State contains dict representations
- Type validation fails before proper conversion
- Fix: Use `AnyMessage` for internal state

## 7. Recommended Solutions

### Short-term Fix

1. Update `ExecutionMixin._prepare_input` to preserve BaseMessage objects
2. Add explicit tool_call_id logging at each stage
3. Use `exclude_none=False` in all `model_dump()` calls

### Medium-term Fix

1. Implement `MessageSerializer` protocol for consistent serialization
2. Update state schemas to use `AnyMessage` for flexibility
3. Add message integrity validation at agent boundaries

### Long-term Fix

1. Redesign state transfer to avoid unnecessary serialization
2. Implement checkpoint-aware message handling
3. Create comprehensive test suite for message preservation

## 8. Implementation Priority

1. **Immediate**: Add logging to pinpoint exact location of field loss
2. **High**: Fix `_prepare_input` to preserve BaseMessage objects
3. **Medium**: Implement proper message serialization
4. **Low**: Refactor to use AnyMessage throughout

## 9. Success Criteria

- ToolMessage with tool_call_id successfully transfers between agents
- Messages survive checkpoint/restore cycles
- No unnecessary conversions between BaseMessage and dict
- Clear error messages when message integrity is compromised
