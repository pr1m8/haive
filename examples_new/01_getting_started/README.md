# Getting Started Examples

Welcome to the Haive framework! These examples will help you understand the basics and get up and running quickly.

## Purpose

This directory contains beginner-friendly examples that introduce core concepts of the Haive framework. Start here if you're new to Haive or want to understand the fundamentals.

## Prerequisites

- Python 3.10+
- Poetry installed (`pip install poetry`)
- Basic Python knowledge
- Haive framework installed (`poetry install` from project root)

## Examples

### 1. `hello_world.py`

**Your first Haive agent!**

- Create a simple agent that responds to greetings
- Learn basic agent configuration
- Understand the simplest agent pattern

### 2. `basic_chat.py`

**Interactive chat with an agent**

- Build a conversational agent
- Handle multiple turns of conversation
- Learn about message handling

### 3. `agent_with_tools.py`

**Enhance agents with tools**

- Add calculator and web search capabilities
- Understand tool integration
- See how agents can perform actions

### 4. `structured_output.py`

**Get structured responses**

- Define output schemas with Pydantic
- Extract specific information reliably
- Learn type-safe agent responses

## Quick Start

```bash
# Run your first agent
poetry run python examples_new/01_getting_started/hello_world.py

# Try the interactive chat
poetry run python examples_new/01_getting_started/basic_chat.py

# See tools in action
poetry run python examples_new/01_getting_started/agent_with_tools.py
```

## Key Concepts Covered

- **Agent Creation**: How to instantiate basic agents
- **Configuration**: Using AugLLMConfig for agent settings
- **Message Handling**: Working with chat messages
- **Tool Integration**: Adding capabilities to agents
- **Structured Output**: Getting predictable, typed responses

## Common Patterns

```python
# Basic agent pattern
from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

agent = SimpleAgent(
    name="my_agent",
    engine=AugLLMConfig(temperature=0.7)
)

result = agent.run("Hello!")
```

## Next Steps

Once you're comfortable with these basics:

1. **[Single Agents](../02_single_agents/)** - Explore different agent types and capabilities
2. **[Multi Agents](../03_multi_agents/)** - Learn agent coordination and workflows
3. **[Specialized Examples](../04_specialized/)** - See domain-specific applications

## Troubleshooting

### Import Errors

Make sure you're using `poetry run`:

```bash
poetry run python examples_new/01_getting_started/hello_world.py
```

### API Key Issues

Set your OpenAI API key:

```bash
export OPENAI_API_KEY="your-key-here"
```

### Performance

These examples use real LLMs. Response times depend on:

- Model selection (GPT-4 is slower than GPT-3.5)
- Network latency
- API rate limits

## Resources

- [Haive Documentation](https://haive.readthedocs.io)
- [Main README](../../README.md)
- [CLAUDE.md](../../CLAUDE.md) - Development guide
