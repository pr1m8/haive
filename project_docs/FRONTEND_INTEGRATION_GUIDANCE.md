# Frontend Integration Guidance for Haive Agents

## Current Backend Architecture

### WebSocket Endpoint

- **URL Pattern**: `/api/ws/chat/{agent_name}`
- **Location**: `packages/haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:35`

### Current Message Protocol (Backend)

The existing haive-dataflow WebSocket uses these message types:

- `message` - User input
- `response` - Agent response
- `status` - Status updates
- `error` - Error messages
- `state` - Intermediate state
- `state_complete` - Final state

### Agent Output Structure

Haive agents produce structured output with:

- **Messages**: LangChain message format (HumanMessage, AIMessage, etc.)
- **Graph Structure**: Multi-node execution (agent_node → validation → parse_output)
- **Structured Data**: Pydantic models for typed outputs
- **Tool Calls**: Native LangChain tool calling format

### Available Agents (30+ types)

- `SimpleAgent` - Basic structured output
- `ReactAgent` - Reasoning and action
- `ConversationAgent` - Multi-turn chat
- `PlanningAgent` - Task planning
- `ResearchAgent` - Information gathering
- And 25+ more specialized agents

## Integration Requirements

### Message Format Adaptation

The frontend expects:

```json
{
  "type": "message_start|thinking|tool_call|tool_result|content|artifact|message",
  "content": "...",
  "tool_calls": [...],
  "artifacts": [...]
}
```

### Backend Message Streaming

The backend streams:

- LangChain message objects
- State updates through graph nodes
- Tool execution results
- Structured output parsing

### Authentication

- Supabase-based persistence with RLS policies
- User isolation via `user_id` parameter
- Thread management in `agent_threads` table

## Recommended Approach

**Frontend adapts to backend** - modify assistant-ui to handle:

1. LangChain message format
2. Graph-based state updates
3. Native tool calling protocol
4. Supabase thread/checkpoint system

### Key Files to Reference

- WebSocket handler: `agent_routes.py:35`
- Agent examples: `packages/haive-agents/src/haive/agents/`
- Persistence: `packages/haive-core/src/haive/core/persistence/supabase_config.py`
- Database schema: Uses existing Supabase tables with RLS

### Next Steps

1. Use existing `/api/ws/chat/{agent_name}` endpoint
2. Adapt frontend to consume LangChain message stream
3. Handle multi-node graph execution flow
4. Integrate with Supabase authentication system