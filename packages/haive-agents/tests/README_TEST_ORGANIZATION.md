# Haive Agents Test Organization

This directory contains comprehensive tests for the Haive agents package, organized by functionality.

## Directory Structure

### `/conversation/`

Tests for conversation agent types:

- Collaborative conversations
- Debate systems
- Round robin discussions
- Social media agent interactions

### `/rag/`

Tests for RAG (Retrieval Augmented Generation) agents:

- Base RAG agent functionality
- Simple RAG agent workflows
- Document retrieval and processing
- Answer generation pipelines

### `/multi/`

Tests for multi-agent systems:

- Sequential agent coordination
- Parallel agent execution
- Agent communication patterns
- State transfer between agents

### `/persistence/`

Tests for persistence functionality:

- Database integration tests
- PostgreSQL checkpoint storage
- Message persistence verification
- Thread continuation tests

### `/utilities/`

Test utilities and helper functions:

- Database debugging tools
- Checkpoint metadata viewers
- Message quality verification
- Prepared statement error checking

### `/resources/`

Test resources and data:

- State history files
- Test result outputs
- Sample conversations
- Agent configuration data

## Test Categories

### Core Agent Tests

- `test_all_agents_comprehensive.py` - Tests all agent types with persistence
- `test_simple_agent.py` - Basic agent functionality
- `test_react_agent.py` - ReAct pattern agents

### Integration Tests

- `test_db_persistence.py` - Database persistence integration
- `test_rag_and_conversations.py` - RAG and conversation agent integration

### Persistence Tests

- `final_persistence_test.py` - Comprehensive persistence verification
- `verify_message_storage.py` - Message storage verification
- `verify_message_quality.py` - Message quality checks

## Running Tests

```bash
# Run all agent tests
poetry run pytest packages/haive-agents/tests/

# Run specific test categories
poetry run pytest packages/haive-agents/tests/conversation/
poetry run pytest packages/haive-agents/tests/rag/
poetry run pytest packages/haive-agents/tests/persistence/

# Run comprehensive agent test
poetry run pytest packages/haive-agents/tests/test_all_agents_comprehensive.py
```

## Test Configuration

Tests use the shared `conftest.py` for common fixtures and setup. All tests that require persistence will automatically detect the `POSTGRES_CONNECTION_STRING` environment variable.

## Recent Fixes

- ✅ Fixed prepared statement conflicts with PostgreSQL
- ✅ Organized scattered test files into proper module structure
- ✅ Added SSL connection resilience for Supabase
- ✅ Verified message quality and conversation flow
- ✅ Implemented comprehensive agent testing framework
