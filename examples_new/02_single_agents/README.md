# Single Agent Examples

Dive deeper into individual agent capabilities and patterns. These examples showcase different agent types and their unique strengths.

## Purpose

Explore the full range of single agent capabilities in Haive, from simple chat agents to sophisticated reasoning systems. Learn when to use different agent types and how to configure them effectively.

## Prerequisites

- Completed [Getting Started](../01_getting_started/) examples
- Understanding of basic agent concepts
- Familiarity with Python async/await (for some examples)

## Examples

### Core Agent Types

#### `simple_agent_advanced.py`

**Advanced SimpleAgent configuration**

- Complex prompt engineering
- Custom system messages
- Temperature and parameter tuning
- Memory management

#### `react_agent_demo.py`

**ReAct (Reasoning + Acting) pattern**

- Tool-using agent with reasoning
- Step-by-step problem solving
- Action planning and execution
- Error handling and recovery

#### `react_async.py`

**Asynchronous ReAct agent**

- Non-blocking agent execution
- Concurrent tool usage
- Performance optimization
- Async/await patterns

### Specialized Capabilities

#### `memory_agent.py`

**Agent with persistent memory**

- Long-term conversation memory
- Context preservation across sessions
- Memory retrieval and management
- User preference learning

#### `validation_agent.py`

**Self-validating agent responses**

- Output validation and correction
- Quality assurance patterns
- Confidence scoring
- Retry mechanisms

#### `structured_agent.py`

**Complex structured output patterns**

- Nested Pydantic models
- Data extraction and transformation
- Type validation and coercion
- Schema evolution

### Tool Integration

#### `tool_creation.py`

**Creating custom tools for agents**

- Define your own tool functions
- Tool parameter validation
- Error handling in tools
- Tool composition patterns

#### `dynamic_tools.py`

**Runtime tool management**

- Add/remove tools dynamically
- Conditional tool availability
- Tool selection strategies
- Performance considerations

## Key Patterns

### Agent Configuration

```python
# Advanced configuration pattern
config = AugLLMConfig(
    model="gpt-4",
    temperature=0.7,
    max_tokens=2000,
    system_message="You are an expert assistant."
)

agent = SimpleAgent(
    name="expert_agent",
    engine=config,
    memory=ConversationBufferMemory()
)
```

### Tool Creation

```python
@tool
def custom_calculator(expression: str) -> str:
    """Calculate mathematical expressions safely."""
    # Your tool implementation
    return str(eval(expression))

agent = ReactAgent(
    name="math_agent",
    engine=config,
    tools=[custom_calculator]
)
```

### Structured Output

```python
class AnalysisResult(BaseModel):
    summary: str = Field(description="Brief summary")
    confidence: float = Field(ge=0.0, le=1.0)
    recommendations: List[str]

config = AugLLMConfig(structured_output_model=AnalysisResult)
agent = SimpleAgent(name="analyst", engine=config)
```

## Running Examples

```bash
# Basic agent examples
poetry run python examples_new/02_single_agents/simple_agent_advanced.py
poetry run python examples_new/02_single_agents/react_agent_demo.py

# Async examples (require event loop)
poetry run python examples_new/02_single_agents/react_async.py

# Memory and validation
poetry run python examples_new/02_single_agents/memory_agent.py
poetry run python examples_new/02_single_agents/validation_agent.py
```

## Skill Level

**Intermediate** - Assumes basic understanding of:

- Agent fundamentals from Getting Started
- Python classes and functions
- Basic async/await concepts
- Pydantic models (for structured examples)

## Key Concepts

### Agent Types

- **SimpleAgent**: Best for straightforward tasks, conversation, content generation
- **ReactAgent**: Best for complex reasoning, tool usage, multi-step problems
- **Memory-Enhanced Agents**: Best for ongoing conversations, personalization

### Configuration Strategies

- **Temperature**: Lower (0.1-0.3) for factual tasks, higher (0.7-0.9) for creative tasks
- **System Messages**: Define agent personality and behavior
- **Memory**: Choose between conversation buffer, summary, or vector-based memory

### Tool Design Principles

- **Single Responsibility**: Each tool does one thing well
- **Clear Documentation**: Tools need good docstrings for agent understanding
- **Error Handling**: Tools should gracefully handle invalid inputs
- **Type Safety**: Use proper type hints and validation

## Performance Tips

1. **Model Selection**: GPT-3.5-turbo for speed, GPT-4 for quality
2. **Async Usage**: Use async agents for concurrent operations
3. **Memory Management**: Clear old conversations to maintain performance
4. **Tool Optimization**: Cache expensive tool operations

## Common Use Cases

### Content Creation

```python
writer = SimpleAgent(
    name="writer",
    engine=AugLLMConfig(temperature=0.8, max_tokens=1500)
)
```

### Data Analysis

```python
analyst = ReactAgent(
    name="analyst",
    engine=AugLLMConfig(temperature=0.2),
    tools=[data_loader, statistical_analyzer, chart_creator]
)
```

### Customer Support

```python
support = SimpleAgent(
    name="support",
    engine=AugLLMConfig(system_message="Helpful customer service agent"),
    memory=ConversationBufferMemory(max_token_limit=2000)
)
```

## Next Steps

Ready for more advanced patterns?

1. **[Multi-Agent Systems](../03_multi_agents/)** - Coordinate multiple agents
2. **[RAG Systems](../04_specialized/rag/)** - Retrieval-augmented generation
3. **[Game Playing](../04_specialized/games/)** - Interactive environments
4. **[Advanced Patterns](../05_advanced/)** - Custom architectures

## Troubleshooting

### Agent Not Using Tools

- Verify tool descriptions are clear
- Check tool function signatures
- Ensure tools are properly registered

### Memory Issues

- Monitor memory usage with large conversations
- Implement memory cleanup strategies
- Use summary memory for long interactions

### Async Problems

- Use `await` with async agent methods
- Handle exceptions in async contexts
- Consider using `asyncio.gather()` for concurrent operations

## Resources

- [Agent API Reference](../../docs/api/agents.md)
- [Tool Development Guide](../../docs/guides/tools.md)
- [Memory Systems](../../docs/guides/memory.md)
