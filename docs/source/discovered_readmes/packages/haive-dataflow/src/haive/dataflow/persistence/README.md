# Haive Persistence Module

Data persistence for the Haive framework, providing storage and retrieval mechanisms for conversations, states, and other application data.

## Overview

The persistence module provides functionality for storing and retrieving application data in various backend systems. It currently focuses on conversation persistence and uses Supabase as the primary storage backend.

## Module Structure

```
persistence/
├── __init__.py             # Package exports
├── conversations.py        # Conversation persistence
└── supabase_adapter.py     # Supabase integration for persistence
```

## Key Components

### Conversation Manager

The `ConversationManager` class in `conversations.py` provides functionality for:

- Creating and storing conversations
- Retrieving conversation history
- Adding messages to conversations
- Searching and filtering conversations
- Managing conversation metadata

### Supabase Adapter

The `SupabasePersistence` class in `supabase_adapter.py` provides:

- Connection management to Supabase
- Transaction handling
- Data transformation between application and database formats
- Error handling and retries

## Usage Examples

### Managing Conversations

```python
from haive.dataflow.persistence.conversations import ConversationManager, ConversationMetadata

# Create the conversation manager
manager = ConversationManager()

# Create a new conversation
conversation_id = await manager.create_conversation(
    user_id="user-123",
    metadata=ConversationMetadata(
        agent_id="agent-456",
        title="AI Ethics Discussion",
        tags=["ethics", "ai"]
    )
)

# Add a message to the conversation
message_id = await manager.add_message(
    conversation_id=conversation_id,
    content="What are the ethical implications of AI?",
    role="user",
    user_id="user-123"
)

# Retrieve conversation history
messages = await manager.get_messages(conversation_id)
for message in messages:
    print(f"{message.role}: {message.content}")

# Delete a conversation
await manager.delete_conversation(conversation_id)
```

### Using the Supabase Adapter Directly

```python
from haive.dataflow.persistence.supabase_adapter import SupabasePersistence

# Create the persistence adapter
persistence = SupabasePersistence()

# Store data
await persistence.store_item(
    table="my_table",
    data={"key": "value", "user_id": "user-123"},
    id_field="id"
)

# Retrieve data
items = await persistence.query_items(
    table="my_table",
    query_params={"user_id": "user-123"},
    limit=10,
    offset=0
)
```

## Data Models

### Conversation

- `id`: Unique identifier for the conversation
- `user_id`: ID of the user who owns the conversation
- `created_at`: Timestamp when the conversation was created
- `updated_at`: Timestamp when the conversation was last updated
- `metadata`: Additional metadata about the conversation

### Message

- `id`: Unique identifier for the message
- `conversation_id`: ID of the conversation the message belongs to
- `content`: Text content of the message
- `role`: Role of the message sender (user, assistant)
- `created_at`: Timestamp when the message was sent
- `metadata`: Additional metadata about the message

## Integration with LangGraph

The persistence system integrates with LangGraph for storing agent states and graph execution histories:

- State persistence during graph execution
- Checkpointing for long-running conversations
- History tracking for debugging and analysis
