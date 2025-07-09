# MessagesState Migration Guide

This guide explains how to migrate from the classic `MessagesState` to the enhanced version with minimal disruption.

## Overview

The enhanced `MessagesState` implementation provides significant new features while maintaining backward compatibility:

- Conversation round tracking and analysis
- Tool call deduplication and error handling
- Message transformation utilities
- Advanced filtering and analysis
- Performance optimizations with caching

## Migration Paths

### Path 1: Direct Replacement (No Code Changes)

The simplest approach is to update your imports without changing any code:

```python
# Old code
from haive.core.schema.prebuilt.messages_state import MessagesState

# New code (compatible with old API)
from haive.core.schema.prebuilt.messages import MessagesState
```

This works because the enhanced implementation provides a compatibility layer that maintains the same API as the classic version.

### Path 2: Leveraging Enhanced Features

To use the new features while still using the familiar MessagesState API:

```python
from haive.core.schema.prebuilt.messages import MessagesState

# Create state as usual
state = MessagesState()
state.add_message(HumanMessage(content="Hello"))
state.add_message(AIMessage(content="Hi there!"))

# Use new features
# 1. Deduplicate tool calls
duplicate_count = state.deduplicate_tool_calls()
print(f"Removed {duplicate_count} duplicate tool calls")

# 2. Get conversation rounds
rounds = state.get_conversation_rounds()
print(f"Conversation has {len(rounds)} rounds")

# 3. Check for real human messages vs transformed ones
for msg in state.messages:
    if isinstance(msg, HumanMessage):
        is_real = state.is_real_human_message(msg)
        print(f"Message: {msg.content[:20]}... is {'real' if is_real else 'transformed'}")

# 4. Get detailed tool call information
tool_calls = state.get_completed_tool_calls()
for tc in tool_calls:
    print(f"Tool call: {tc.tool_call_id} was {'successful' if tc.is_successful else 'failed'}")
```

### Path 3: Full Migration to Enhanced Implementation

For maximum flexibility and all features, use the enhanced implementation directly:

```python
from haive.core.schema.prebuilt.messages import EnhancedMessagesState, MessageList

# Create new state (same API as classic, plus enhanced features)
state = EnhancedMessagesState()

# Add messages as usual
state.add_message(HumanMessage(content="Hello"))
state.add_message(AIMessage(content="Hi there!"))

# Use advanced computed properties
print(f"Message count: {state.message_count}")
print(f"Round count: {state.round_count}")
print(f"Has tool errors: {state.has_tool_errors}")

# Use message transformation features
state.transform_ai_to_human(preserve_metadata=True)

# Use advanced filtering
ai_messages = state.filter_by_type(AIMessage)
error_messages = state.filter_by_metadata("is_error", True)
```

## Feature Comparison

| Feature                  | Classic MessagesState | Enhanced MessagesState |
| ------------------------ | --------------------- | ---------------------- |
| Basic message management | ✅                    | ✅                     |
| Message filtering        | ✅                    | ✅ (Enhanced)          |
| Tool call handling       | ✅                    | ✅ (Enhanced)          |
| Conversation rounds      | ❌                    | ✅                     |
| Tool call deduplication  | ❌                    | ✅                     |
| Message transformation   | ❌                    | ✅                     |
| Message round tracking   | ❌                    | ✅                     |
| Cached properties        | ❌                    | ✅                     |
| Advanced filtering       | ❌                    | ✅                     |

## Advanced Examples

### Example 1: Agent-to-Agent Communication

```python
from haive.core.schema.prebuilt.messages import MessagesState

# First agent's state
agent1_state = MessagesState()
agent1_state.add_system_message("You are Agent 1, an expert in data analysis.")
agent1_state.add_message(HumanMessage(content="Analyze this dataset"))
agent1_state.add_message(AIMessage(content="I found these patterns..."))

# Transfer to second agent (with transformation)
agent2_state = MessagesState()
agent2_state.add_system_message("You are Agent 2, an expert in visualization.")

# Transform AI messages from agent1 to human messages for agent2
# This maintains conversation flow while changing perspective
agent1_adapter = MessagesStateAdapter(agent1_state)
agent1_adapter.transform_ai_to_human(preserve_metadata=True, engine_id="agent1")

# Copy transformed messages to agent2
for msg in agent1_state.messages:
    if not isinstance(msg, SystemMessage):  # Skip system message
        agent2_state.add_message(msg)

# Now agent2 sees agent1's AI responses as human messages
```

### Example 2: Conversation Round Analysis

```python
from haive.core.schema.prebuilt.messages import MessagesState

state = MessagesState()
# ... add messages ...

# Get detailed round information
rounds = state.get_conversation_rounds()

# Analyze rounds for quality
for round_info in rounds:
    print(f"Round {round_info.round_number}:")
    print(f"  Human: {round_info.human_message.content[:50]}...")
    print(f"  AI responses: {len(round_info.ai_responses)}")
    print(f"  Tool calls: {len(round_info.tool_calls)}")
    print(f"  Has errors: {round_info.has_errors}")
    print(f"  Is complete: {round_info.is_complete}")
```

## Handling Missing Dependencies

If you're using the enhanced features but the compatibility package is not installed, you'll see clear error messages:

```
NotImplementedError: Enhanced features not available. Install the enhanced MessagesState package.
```

To resolve this, ensure you've properly installed the package and its dependencies.

## Performance Considerations

The enhanced implementation uses caching for computed properties, which can improve performance in many cases. However, if you're making frequent modifications to the messages list, be aware that caches are invalidated on each change.

For very large message histories, the MessageList implementation provides better performance than the classic implementation.

## Common Issues

1. **Import Errors**: If you see import errors, check that the enhanced package is installed correctly.

2. **Type Errors**: The enhanced implementation uses more precise typing, which might catch issues that were previously overlooked.

3. **Behavior Differences**: While the core API is compatible, some edge cases might behave slightly differently. Test thoroughly when migrating.

4. **Missing Features**: If you're trying to use a feature that results in a NotImplementedError, make sure you're using the correct import path.

## FAQ

### Q: Will the classic MessagesState be deprecated?

A: No, both implementations will be maintained. The classic implementation now includes adapter methods to use enhanced features when available.

### Q: Do I need to migrate all my code at once?

A: No, you can migrate gradually. Start by updating imports, then leverage enhanced features as needed.

### Q: What if I need a feature that's only in the enhanced version?

A: You can use the adapter pattern to access enhanced features from the classic implementation, or fully migrate to the enhanced version.

### Q: Is there a performance impact?

A: The enhanced implementation is generally more efficient for complex operations and large message histories, but might have slightly higher overhead for simple operations.
