# NO MOCKS Testing Pattern

**Pattern**: Always use real components in tests
**Importance**: CRITICAL
**Established**: Core philosophy

## The Rule

**NEVER USE MOCKS IN HAIVE TESTS**

## Why

1. **Real behavior validation** - Mocks hide actual behavior
2. **Integration testing** - Real components expose integration issues
3. **Confidence** - If tests pass, production will work
4. **No surprises** - What you test is what runs

## Implementation

### ❌ FORBIDDEN

```python
from unittest.mock import Mock, MagicMock, patch

# NEVER DO THIS
mock_llm = Mock()
mock_llm.return_value = "fake response"

@patch('haive.core.agent')
def test_with_mock(mock_agent):
    pass  # NO!
```

### ✅ CORRECT

```python
from haive.core.engine.aug_llm import AugLLMConfig
from haive.agents.simple import SimpleAgent

def test_real_agent():
    """Test with REAL components."""
    # Real configuration
    config = AugLLMConfig(temperature=0.1)

    # Real agent
    agent = SimpleAgent(name="test", engine=config)

    # Real execution
    result = agent.run("Hello")

    # Real validation
    assert isinstance(result, str)
    assert len(result) > 0
```

## Common Patterns

### Testing with Real LLMs

```python
config = AugLLMConfig(
    temperature=0.1,  # Low for consistency
    max_tokens=100   # Limit for speed
)
```

### Testing with Real Tools

```python
@tool
def calculator(expression: str) -> str:
    """Real calculator tool."""
    return str(eval(expression))

agent = ReactAgent(
    name="test",
    engine=config,
    tools=[calculator]  # Real tool
)
```

### Testing State Persistence

```python
# Test real state saving
result1 = agent.run("My name is Alice")
result2 = agent.run("What's my name?")
assert "alice" in result2.lower()  # Real memory
```

## Related Memories

- @memory_index/by_task/testing/real_component_patterns.md
- @memory_index/by_agent/simple_agent/testing.md
- @memory_index/by_pattern/test_configuration.md

## Tags

#testing #no-mocks #philosophy #critical-rule
