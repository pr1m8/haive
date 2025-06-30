# Conversational Agents Documentation

## Overview
This document covers conversational agents in the Haive framework - agents designed for natural language interactions and dialogue management.

## Available Conversational Agents

### 1. SimpleAgent
**Location**: `/packages/haive-agents/src/haive/agents/simple/`

A basic conversational agent that provides straightforward LLM interactions.

**Key Features**:
- Direct LLM communication
- Simple state management
- Minimal configuration required

**Usage Example**:
```python
from haive.agents.simple import SimpleAgent

agent = SimpleAgent(
    name="assistant",
    model="gpt-4",
    system_prompt="You are a helpful assistant."
)

response = await agent.chat("Hello, how are you?")
```

### 2. ConversationAgent
**Location**: `/packages/haive-agents/src/haive/agents/conversation/`

An advanced conversational agent with memory and context management.

**Key Features**:
- Conversation history tracking
- Context window management
- Memory persistence options
- Multi-turn dialogue support

**Usage Example**:
```python
from haive.agents.conversation import ConversationAgent

agent = ConversationAgent(
    name="chat_assistant",
    model="gpt-4",
    memory_type="buffer",
    max_history=10
)

# Multi-turn conversation
response1 = await agent.chat("What's the weather like?")
response2 = await agent.chat("What about tomorrow?")  # Maintains context
```

### 3. PersonaAgent
**Location**: `/packages/haive-agents/src/haive/agents/persona/`

A conversational agent with customizable personality and behavioral traits.

**Key Features**:
- Persona configuration
- Consistent personality traits
- Role-playing capabilities
- Emotional state tracking

**Usage Example**:
```python
from haive.agents.persona import PersonaAgent

agent = PersonaAgent(
    name="expert",
    model="gpt-4",
    persona={
        "role": "technical expert",
        "traits": ["analytical", "precise", "helpful"],
        "expertise": ["software", "AI", "data science"]
    }
)
```

## Common Patterns

### Memory Management
```python
# Configure memory for conversation agents
agent = ConversationAgent(
    memory_config={
        "type": "buffer",
        "max_tokens": 2000,
        "summarize_on_overflow": True
    }
)
```

### Context Injection
```python
# Add context to conversations
agent.add_context({
    "user_preferences": user_data,
    "session_info": session_data
})
```

### Stream Responses
```python
# Stream responses for real-time interaction
async for chunk in agent.stream_chat("Tell me a story"):
    print(chunk, end="", flush=True)
```

## Configuration Options

### Base Configuration
All conversational agents support:
- `name`: Agent identifier
- `model`: LLM model to use
- `temperature`: Response randomness (0-1)
- `max_tokens`: Maximum response length
- `system_prompt`: Base instructions

### Advanced Configuration
- `memory_type`: ["buffer", "summary", "vector", "none"]
- `context_window`: Maximum context size
- `response_format`: ["text", "json", "markdown"]
- `streaming`: Enable/disable streaming

## Best Practices

1. **Memory Management**
   - Use appropriate memory types for your use case
   - Clear memory periodically for long-running agents
   - Implement summarization for extended conversations

2. **Context Handling**
   - Keep context relevant and concise
   - Update context based on conversation flow
   - Use structured context for better results

3. **Error Handling**
   - Implement fallback responses
   - Handle rate limits gracefully
   - Log conversation metrics

## Integration Examples

### With Tools
```python
from haive.tools import WebSearchTool

agent = ConversationAgent(
    tools=[WebSearchTool()],
    tool_choice="auto"
)
```

### With Streaming
```python
async def handle_stream():
    async for chunk in agent.stream_chat(query):
        await websocket.send(chunk)
```

### With Persistence
```python
# Save conversation state
state = agent.save_state()
await database.save(state)

# Restore conversation
agent.load_state(saved_state)
```

## See Also
- [CLAUDE_AGENTS.md](./CLAUDE_AGENTS.md) - Main agents documentation
- [CLAUDE_AGENTS_TASK.md](./CLAUDE_AGENTS_TASK.md) - Task-oriented agents
- [CLAUDE_AGENT_TEMPLATE.md](./CLAUDE_AGENT_TEMPLATE.md) - Agent development template