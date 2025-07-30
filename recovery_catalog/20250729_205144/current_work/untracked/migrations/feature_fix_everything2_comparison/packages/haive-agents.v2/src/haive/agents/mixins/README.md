# Agent Mixins

Core mixins that provide reusable functionality to Haive agents through composition.

## Overview

Mixins enable modular agent architecture by providing specific capabilities that can be combined across different agent types. Each mixin handles a distinct aspect of agent functionality.

## Key Components

### PersistenceMixin (`persistence_mixin.py`)

**Automatic Supabase integration for conversation persistence.**

**Recent Changes (2025-06-30)**:

- ✅ **Auto-Supabase Detection**: Now automatically detects and uses Supabase when `POSTGRES_CONNECTION_STRING` environment variable is set
- ✅ **Seamless Fallback**: Falls back to individual PostgreSQL environment variables if connection string not found
- ✅ **Zero Configuration**: Works out-of-the-box with Supabase connections

**Usage**:

```python
# Set environment variable (agents auto-detect this)
export POSTGRES_CONNECTION_STRING="postgresql://postgres.{project}:{password}@aws-0-{region}.pooler.supabase.com:6543/postgres"

# Agent automatically uses Supabase
from haive.agents.simple.agent import SimpleAgent
agent = SimpleAgent()  # Persistence configured automatically
```

### ExecutionMixin (`execution_mixin.py`)

**Core execution logic with improved recursion limit handling.**

**Recent Changes (2025-06-30)**:

- ✅ **Fixed Recursion Limit Display**: Debug messages now correctly show recursion limit values
- ✅ **Proper Config Location**: Looks for recursion_limit in `config.configurable.recursion_limit` (correct location)
- ✅ **Default Values**: Ensures recursion_limit defaults to 100 if not specified

**Configuration**:

```python
# Recursion limit properly detected and displayed
config = {
    'configurable': {
        'thread_id': 'conversation-id',
        'recursion_limit': 100  # Now correctly displayed in debug output
    }
}
```

## Installation

This module is part of the `haive-agents` package. Install it using:

```bash
pip install haive-agents
```

## Usage Examples

### Basic Agent with Auto-Persistence

```python
from haive.agents.simple.agent import SimpleAgent
from langchain_core.messages import HumanMessage

# Agent automatically detects Supabase from environment
agent = SimpleAgent(name="My Agent")

# Conversations automatically persisted
result = agent.run(
    {'messages': [HumanMessage(content="Hello!")]},
    config={'configurable': {'thread_id': 'conversation-1'}}
)

# Verify Supabase is being used
if hasattr(agent, 'persistence') and "supabase.com" in str(agent.persistence.connection_string):
    print("✅ Using Supabase persistence!")
```

### Custom Configuration

```python
# Override defaults if needed
config = {
    'configurable': {
        'thread_id': f'user-{user_id}-session-{session_id}',
        'recursion_limit': 150  # Override default of 100
    }
}

result = agent.run(messages, config=config)
```

## Troubleshooting

### Common Issues

**Prepared Statement Errors**:

- Error: `prepared statement "_pg3_X" already exists`
- **Impact**: ⚠️ Does NOT prevent data persistence
- **Solution**: These errors can be safely ignored

**Missing Supabase Detection**:

- **Cause**: `POSTGRES_CONNECTION_STRING` environment variable not set
- **Solution**: `export POSTGRES_CONNECTION_STRING="your-supabase-connection"`

**Recursion Limit Issues**:

- **Fixed**: Debug messages now show correct recursion limit values
- **Default**: 100 (configurable via `config.configurable.recursion_limit`)

## API Reference

For detailed API documentation, see the [API Reference](../../../docs/source/api/mixins/index.rst).

## See Also

- [Supabase Integration Guide](../../../../project_docs/SUPABASE_INTEGRATION.md)
- [Agent Base Classes](../README.md)
- [PostgreSQL Configuration](../../../haive-core/docs/POSTGRESQL_CONFIG.md)
