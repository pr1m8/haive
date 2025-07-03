# Haive Core Persistence Module

The `haive.core.persistence` module provides comprehensive state persistence capabilities for Haive AI agents. It offers multiple backend implementations for storing and retrieving agent state, enabling stateful conversations and long-term memory across sessions.

## 🎯 **Overview**

This module integrates seamlessly with LangGraph's checkpointing system while adding Haive-specific enhancements such as:

- **Multiple Backend Support**: Memory, PostgreSQL, SQLite, and Supabase
- **Async/Sync Operations**: Full support for both synchronous and asynchronous workflows
- **Connection Pooling**: Optimized database connections for production use
- **Automatic Schema Management**: Tables and indexes created automatically
- **Long-term Memory**: Store integration for cross-thread persistent data
- **Error Handling**: Robust fallback mechanisms and retry logic

## 📦 **Available Backends**

### 🧠 **Memory Backend**

```python
from haive.core.persistence import MemoryCheckpointerConfig

config = MemoryCheckpointerConfig()
checkpointer = config.create_checkpointer()
```

- **Use Case**: Development, testing, temporary state
- **Persistence**: In-memory only (lost on restart)
- **Dependencies**: None (built-in)

### 🐘 **PostgreSQL Backend**

```python
from haive.core.persistence import PostgresCheckpointerConfig

config = PostgresCheckpointerConfig(
    connection_string="postgresql://user:pass@host:port/db"
)
checkpointer = config.create_checkpointer()
```

- **Use Case**: Production deployments, on-premise databases
- **Persistence**: Durable PostgreSQL storage
- **Dependencies**: `psycopg2-binary`, `psycopg-pool`

### ☁️ **Supabase Backend**

```python
from haive.core.persistence import SupabaseCheckpointerConfig

config = SupabaseCheckpointerConfig(
    connection_string=os.getenv("POSTGRES_CONNECTION_STRING"),
    user_id="user-123"
)
checkpointer, store = config.create_checkpointer_and_store()
```

- **Use Case**: Cloud deployments, managed PostgreSQL, multi-tenant apps
- **Persistence**: Cloud-hosted PostgreSQL via Supabase
- **Dependencies**: `psycopg2-binary`, `psycopg-pool`

## 🚀 **Quick Start Guide**

### 1. **Choose Your Backend**

```python
from haive.core.persistence import get_available_backends

# Check what's available
backends = get_available_backends()
print(f"Available backends: {backends}")
# Output: ['memory', 'postgres', 'supabase']
```

### 2. **Create Configuration**

```python
from haive.core.persistence import create_checkpointer_config

# Factory function approach
config = create_checkpointer_config(
    'postgres',
    connection_string="postgresql://user:pass@host:port/db"
)
```

### 3. **Create Checkpointer**

```python
# Synchronous
checkpointer = config.create_checkpointer()

# Asynchronous
async_checkpointer = await config.create_async_checkpointer()

# With long-term memory store
checkpointer, store = config.create_checkpointer_and_store()
```

### 4. **Use with LangGraph**

```python
from langgraph.graph import StateGraph

# Define your agent workflow
workflow = StateGraph(YourAgentState)
# ... define workflow ...

# Compile with persistence
app = workflow.compile(checkpointer=checkpointer)

# Run with thread configuration
thread_config = {"configurable": {"thread_id": "user-123-session-1"}}
result = app.invoke(initial_state, config=thread_config)
```

## 🏗️ **Database Schema**

The persistence module automatically creates the following tables:

### **Standard LangGraph Tables**

```sql
-- Main checkpoint storage
CREATE TABLE checkpoints (
    thread_id TEXT NOT NULL,
    checkpoint_ns TEXT NOT NULL DEFAULT '',
    checkpoint_id TEXT NOT NULL,
    parent_checkpoint_id TEXT,
    type TEXT,
    checkpoint JSONB NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}',
    PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id)
);

-- Large binary data storage
CREATE TABLE checkpoint_blobs (
    thread_id TEXT NOT NULL,
    checkpoint_ns TEXT NOT NULL DEFAULT '',
    channel TEXT NOT NULL,
    version TEXT NOT NULL,
    type TEXT NOT NULL,
    blob BYTEA,
    PRIMARY KEY (thread_id, checkpoint_ns, channel, version)
);

-- Pending write operations
CREATE TABLE checkpoint_writes (
    thread_id TEXT NOT NULL,
    checkpoint_ns TEXT NOT NULL DEFAULT '',
    checkpoint_id TEXT NOT NULL,
    task_id TEXT NOT NULL,
    idx INTEGER NOT NULL,
    channel TEXT NOT NULL,
    type TEXT,
    blob BYTEA NOT NULL,
    PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id, task_id, idx)
);
```

### **Store Tables** (for long-term memory)

```sql
-- Key-value store for cross-thread data
CREATE TABLE store (
    prefix TEXT[] NOT NULL,
    key TEXT NOT NULL,
    value JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (prefix, key)
);
```

## 🔌 **Installation Requirements**

### **Core Dependencies** (always required)

```bash
pip install langgraph pydantic
```

### **PostgreSQL Backend**

```bash
pip install psycopg2-binary psycopg-pool
```

### **Supabase Backend**

```bash
pip install psycopg2-binary psycopg-pool
# Optional: For REST API features
pip install supabase
```

## 🎯 **Connection String Formats**

### **PostgreSQL**

```
postgresql://username:password@host:port/database
postgresql://user:pass@localhost:5432/haive
```

### **Supabase PostgreSQL**

```
postgresql://postgres.PROJECT:PASSWORD@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

### **SQLite**

```
sqlite:///path/to/database.db
sqlite:///:memory:
```

## 🏛️ **Architecture**

```
haive.core.persistence/
├── __init__.py              # Main module exports and factory functions
├── base.py                  # Abstract base classes
├── types.py                 # Type definitions and enums
├── memory_config.py         # In-memory implementation
├── postgres_config.py       # PostgreSQL implementation
├── supabase_config.py       # Supabase cloud implementation
└── README.md               # This documentation
```

## 🧪 **Testing Your Setup**

```python
def test_persistence_setup():
    from haive.core.persistence import PostgresCheckpointerConfig

    config = PostgresCheckpointerConfig(
        connection_string="your-connection-string"
    )

    checkpointer = config.create_checkpointer()
    print(f"✅ Checkpointer: {type(checkpointer).__name__}")

    return True

test_persistence_setup()
```

## 📚 **API Reference**

### **Factory Functions**

- `get_available_backends()` → `list[str]`: List available backends
- `create_checkpointer_config(backend, **kwargs)` → `CheckpointerConfig`: Create config

### **Configuration Classes**

- `MemoryCheckpointerConfig`: In-memory persistence
- `PostgresCheckpointerConfig`: PostgreSQL persistence
- `SupabaseCheckpointerConfig`: Supabase cloud persistence

### **Key Methods**

- `create_checkpointer()` → `Checkpointer`: Create sync checkpointer
- `create_async_checkpointer()` → `AsyncCheckpointer`: Create async checkpointer
- `create_store()` → `Store`: Create sync store
- `create_checkpointer_and_store()` → `tuple`: Create both components

## 💡 **Best Practices**

1. **Production Setup**: Use PostgreSQL or Supabase for production
2. **Connection Pooling**: Configure appropriate pool sizes
3. **Error Handling**: Implement retry logic and fallbacks
4. **Security**: Use environment variables for connection strings
5. **Testing**: Always test persistence setup before deploying

---

_For more information, see the [Haive Documentation](https://github.com/pr1m8/haive) or individual module docs._
