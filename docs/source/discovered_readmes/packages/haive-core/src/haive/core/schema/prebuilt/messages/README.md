# Haive MessagesState System

This package provides a comprehensive system for managing conversation state in Haive agents, with advanced features for message processing, tool call handling, and conversation analysis.

## Overview

The MessagesState system serves as the foundation for conversation-based agents in the Haive framework, providing seamless integration with LangGraph for agent workflows. It offers robust functionality for working with LangChain message types, message filtering, transformation, and conversation management.

This package provides two implementations:

1. **Classic MessagesState**: The original implementation with core functionality
2. **Enhanced MessagesState**: A more powerful implementation with advanced features

Both implementations share a compatible API, allowing for gradual migration and feature adoption.

## Key Features

- **Message Management**: Comprehensive handling of different message types (Human, AI, System, Tool)
- **Conversation Structure**: Automatic message ordering and system message handling
- **Tool Integration**: Robust tool call handling, deduplication, and error tracking
- **Conversation Analysis**: Round tracking, completion detection, and detailed analytics
- **Message Transformation**: Utilities for agent-to-agent communication and synthetic conversations
- **LangGraph Integration**: Proper reducers and message handling for graph-based agents

## Installation

The MessagesState system is included with the Haive Core package:

```bash
pip install haive-core
```

## Usage

### Basic Usage

```python
from haive.core.schema.prebuilt.messages import MessagesState
from langchain_core.messages import HumanMessage, AIMessage

# Create a new state
state = MessagesState()

# Add a system message
state.add_system_message("You are a helpful assistant.")

# Add conversation messages
state.add_message(HumanMessage(content="Hello, can you help me?"))
state.add_message(AIMessage(content="Of course! What can I help you with?"))

# Access messages
last_msg = state.get_last_message()
human_msg = state.get_last_human_message()
ai_msg = state.get_last_ai_message()

# Use in LangGraph
from langgraph.graph import StateGraph, START, END

# Create a graph with the state
graph = StateGraph(MessagesState)

# Add nodes and edges
graph.add_node("process", process_fn)
graph.add_edge(START, "process")
graph.add_edge("process", END)

# Compile and run
compiled = graph.compile()
result = compiled.invoke({"messages": []})
```

### Advanced Features

```python
from haive.core.schema.prebuilt.messages import MessagesState

state = MessagesState()
# ... add messages ...

# Get conversation rounds
rounds = state.get_conversation_rounds()
print(f"Conversation has {len(rounds)} rounds")

# Deduplicate tool calls
removed = state.deduplicate_tool_calls()
print(f"Removed {removed} duplicate tool calls")

# Get detailed tool call information
tool_calls = state.get_completed_tool_calls()
for tc in tool_calls:
    print(f"Tool call {tc.tool_call_id}: {'✓' if tc.is_successful else '✗'}")

# Transform messages for agent handoff
state.transform_ai_to_human(preserve_metadata=True)
```

### Enhanced Implementation

For maximum flexibility, use the enhanced implementation directly:

```python
from haive.core.schema.prebuilt.messages import EnhancedMessagesState, MessageList

# Create state with MessageList
state = EnhancedMessagesState()
# ... add messages ...

# Access computed properties
print(f"Message count: {state.message_count}")
print(f"Round count: {state.round_count}")
print(f"Has tool errors: {state.has_tool_errors}")

# Use advanced filtering
ai_messages = state.messages.filter_by_type(AIMessage)
pattern_matches = state.messages.filter_by_content_pattern("error")
```

## Documentation

For more information, see:

- [Migration Guide](MIGRATION.md): Details on migrating between implementations
- [API Reference](https://docs.haive.ai/reference/core/schema/prebuilt/messages): Complete API documentation
- [Examples](https://docs.haive.ai/examples/messages_state): Detailed usage examples

## Architecture

The MessagesState system is organized as follows:

```
haive/core/schema/prebuilt/messages/
├── __init__.py              # Public exports and imports
├── utils.py                 # Shared utility functions and classes
├── compatibility.py         # Compatibility layer for backward compatibility
├── messages_state.py        # Enhanced implementation
├── MIGRATION.md             # Migration guide
└── README.md                # Package documentation
```

## Contributing

When extending the MessagesState system, please follow these guidelines:

1. Maintain backward compatibility with the classic API
2. Add new features through the compatibility layer when possible
3. Document new features thoroughly with examples
4. Add unit tests for all new functionality
5. Update the migration guide for significant changes

## License

This package is part of the Haive Core framework and is licensed under the same terms as the main project.
