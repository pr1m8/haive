# SimpleAgent User Guide

The `SimpleAgent` is the foundational conversational agent in the Haive framework. It provides basic chat functionality with memory and can be extended with tools and structured outputs.

## Quick Start

### Basic Usage

```python
import asyncio
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

async def main():
    # Create agent configuration
    config = AugLLMConfig(
        name="my_agent",
        temperature=0.7
    )
    
    # Create the SimpleAgent
    agent = SimpleAgent(
        name="my_agent",
        engine=config
    )
    
    # Use the agent
    response = agent.run("Hello! Please introduce yourself.")
    print(f"Agent: {response}")

asyncio.run(main())
```

## Key Features

### 🧠 **Conversation Memory**
- Automatically maintains conversation history
- Provides context across multiple interactions
- Memory persists throughout the agent's lifecycle

### ⚡ **Simple API**
- Clean `.run()` method for synchronous usage
- Async support with `.arun()` 
- No complex setup required

### 🔧 **Configurable**
- Customizable LLM settings (temperature, model, etc.)
- Flexible prompt templates
- Extensible architecture

## Working Example

Here's a complete working example you can run:

```python
#!/usr/bin/env python3
"""SimpleAgent Demo - A working example"""

import asyncio
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

async def demo_conversation():
    """Demonstrate a multi-turn conversation."""
    
    # Create agent
    config = AugLLMConfig(name="demo_agent", temperature=0.7)
    agent = SimpleAgent(name="demo_agent", engine=config)
    
    # Multi-turn conversation
    responses = []
    
    # Turn 1: Introduction
    response1 = agent.run("Hello! Please introduce yourself.")
    responses.append(("Human", "Hello! Please introduce yourself."))
    responses.append(("Agent", response1))
    
    # Turn 2: Question with context
    response2 = agent.run("What's your favorite color?")
    responses.append(("Human", "What's your favorite color?"))
    responses.append(("Agent", response2))
    
    # Turn 3: Follow-up that uses memory
    response3 = agent.run("Why did you choose that color?")
    responses.append(("Human", "Why did you choose that color?"))
    responses.append(("Agent", response3))
    
    # Display conversation
    print("🤖 SimpleAgent Conversation Demo")
    print("=" * 50)
    for speaker, message in responses:
        print(f"{speaker}: {message}")
        print()
    
    return responses

if __name__ == "__main__":
    asyncio.run(demo_conversation())
```

## Configuration Options

### Basic Configuration

```python
from haive.core.engine.aug_llm import AugLLMConfig

# Basic configuration
config = AugLLMConfig(
    name="my_agent",
    temperature=0.7,        # Controls randomness (0.0-2.0)
    max_tokens=1000,        # Maximum response length
)
```

### Advanced Configuration

```python
# Advanced configuration with custom prompts
config = AugLLMConfig(
    name="advanced_agent",
    temperature=0.5,
    max_tokens=2000,
    system_message="You are a helpful research assistant specializing in scientific topics.",
)
```

## Agent Architecture

The SimpleAgent is built on Haive's graph-based architecture:

```
┌─────────────────┐
│   Human Input   │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐    ┌─────────────────┐
│  Message State  │───▶│   LLM Engine    │
└─────────────────┘    └─────────┬───────┘
          ▲                      │
          │                      ▼
          │            ┌─────────────────┐
          └────────────│  Agent Response │
                       └─────────────────┘
```

### Internal Components

- **Message State**: Maintains conversation history
- **LLM Engine**: Processes inputs and generates responses  
- **Graph Executor**: Orchestrates the conversation flow

## Common Use Cases

### 1. Customer Support Chat

```python
config = AugLLMConfig(
    name="support_agent",
    temperature=0.3,  # Lower for more consistent responses
    system_message="""You are a helpful customer support agent. 
    Be polite, professional, and try to solve customer problems."""
)

support_agent = SimpleAgent(name="support_agent", engine=config)
response = support_agent.run("I'm having trouble with my order")
```

### 2. Educational Tutor

```python
config = AugLLMConfig(
    name="tutor_agent", 
    temperature=0.5,
    system_message="""You are a patient tutor. Explain concepts clearly 
    and ask follow-up questions to ensure understanding."""
)

tutor = SimpleAgent(name="tutor_agent", engine=config)
response = tutor.run("Can you explain photosynthesis?")
```

### 3. Creative Writing Assistant

```python
config = AugLLMConfig(
    name="writer_agent",
    temperature=0.8,  # Higher for more creativity
    system_message="""You are a creative writing assistant. Help users 
    brainstorm ideas and improve their writing."""
)

writer = SimpleAgent(name="writer_agent", engine=config)
response = writer.run("Help me write a story about a robot")
```

## Best Practices

### ✅ Do

- **Set appropriate temperature**: 0.0-0.3 for factual tasks, 0.7-1.0 for creative tasks
- **Use descriptive agent names**: Helps with debugging and monitoring
- **Keep conversations focused**: SimpleAgent works best for straightforward interactions
- **Handle errors gracefully**: Wrap agent calls in try-catch blocks

### ❌ Don't

- **Use for complex tool interactions**: Consider ReactAgent instead
- **Expect perfect factual accuracy**: Always verify important information
- **Store sensitive data in conversation**: Be mindful of privacy
- **Ignore token limits**: Monitor conversation length for long sessions

## Troubleshooting

### Common Issues

**Issue**: Agent responses are too random/inconsistent
```python
# Solution: Lower the temperature
config = AugLLMConfig(name="agent", temperature=0.2)
```

**Issue**: Agent doesn't remember previous conversation
```python
# Solution: Ensure you're using the same agent instance
agent = SimpleAgent(name="my_agent", engine=config)
response1 = agent.run("My name is Alice")
response2 = agent.run("What's my name?")  # Should remember Alice
```

**Issue**: Responses are too long
```python
# Solution: Set max_tokens limit
config = AugLLMConfig(name="agent", max_tokens=100)
```

## Next Steps

Once you're comfortable with SimpleAgent, explore:

- **[ReactAgent](react_agent_guide.md)**: For tool-using agents
- **[Multi-Agent Systems](multi_agent_guide.md)**: For coordinated agent workflows  
- **[RAG Agents](rag_agent_guide.md)**: For knowledge-based agents

## API Reference

### `SimpleAgent`

#### Constructor
```python
SimpleAgent(name: str, engine: AugLLMConfig)
```

#### Methods

**`.run(message: str) -> str`**
- Synchronous conversation method
- Returns agent's response as string

**`.arun(message: str) -> str`**  
- Asynchronous conversation method
- Returns agent's response as string

**`.reset_state()`**
- Clears conversation history
- Starts fresh conversation

---

*This guide provides everything you need to get started with SimpleAgent. For more advanced usage patterns, see the [Advanced Agent Patterns](advanced_patterns.md) guide.*