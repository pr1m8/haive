# Testing Philosophy - Haive Framework

**Version**: 1.0  
**Purpose**: Comprehensive testing standards for Haive development  
**Last Updated**: 2025-01-09

## 🎯 Core Testing Principles

### 1. ABSOLUTE NO MOCKS
- **Always use real components** - Real LLMs, real tools, real APIs
- **Never mock internal logic** - Test actual behavior, not simulated responses
- **Mock only external dependencies** - Third-party APIs, file systems, network calls

### 2. Test Behavior, Not Implementation
- **Focus on outcomes** - What the code does, not how it does it
- **Descriptive test names** - `test_agent_maintains_state_across_multiple_turns`
- **Clear assertions** - Test meaningful results, not internal state

### 3. Real Integration Testing
- **Use actual state files** - Save real conversation histories
- **Test with real engines** - Use configured LLM providers
- **Validate real workflows** - End-to-end agent interactions

## 🚫 Forbidden Testing Patterns

```python
# 🚨 ABSOLUTELY FORBIDDEN - Mock usage in any form
from unittest.mock import Mock, MagicMock, patch
mock_llm = Mock()                           # ❌ NO MOCKS EVER
@patch('haive.core.agent')                  # ❌ NO PATCHES EVER
with mock.patch() as mock_agent:            # ❌ NO MOCK CONTEXT MANAGERS
agent = MagicMock()                         # ❌ NO MAGIC MOCKS EVER

# 🚨 FORBIDDEN - Fake/stub implementations
class FakeLLM:                              # ❌ NO FAKE CLASSES
    def __call__(self): return "fake"

def mock_function():                        # ❌ NO MOCK FUNCTIONS
    return {"fake": "data"}

# 🚨 FORBIDDEN - Test doubles or substitutes
test_agent = TestDouble()                   # ❌ NO TEST DOUBLES
stub_response = Stub()                      # ❌ NO STUBS
fake_api = FakeAPI()                        # ❌ NO FAKE APIs
```

## ✅ Required Testing Patterns

### Real Component Testing
```python
def test_react_agent_with_real_llm_and_tools():
    """Test ReactAgent with actual LLM and real tools."""
    # Use REAL components only
    agent = ReactAgent(
        name="test_agent",
        model="gpt-4",                      # Real LLM
        tools=["calculator", "web_search"]  # Real tools
    )

    # Test with REAL input
    result = agent.process("Calculate 15 * 23 and search for Python tutorials")

    # Verify REAL behavior
    assert "345" in str(result.response)
    assert result.tool_calls_made > 0
    assert result.conversation_history is not None
    assert result.state_saved_to_file is True
```

### Real Integration Testing
```python
def test_agent_tool_integration_real_apis():
    """Test real agent with real tool integration."""
    calculator = Calculator()               # Real tool instance
    search_tool = WebSearchTool()          # Real search tool

    agent = ReactAgent(
        name="integration_test",
        model="gpt-4",
        tools=[calculator, search_tool]     # Real tools passed
    )

    result = agent.process("What's 50 * 30 and find current Python version")

    # Test real outcomes
    assert calculator in agent.active_tools
    assert search_tool in agent.active_tools
    assert "1500" in str(result.response)
```

### Real Error Handling
```python
def test_real_error_handling_with_invalid_tool():
    """Test how agent handles real tool errors."""
    agent = ReactAgent(name="error_test", model="gpt-4")

    # Cause real error by using non-existent tool
    result = agent.process("Use the nonexistent_tool to do something")

    # Test real error handling (not mocked)
    assert result.error_occurred is True
    assert "tool not found" in result.error_message.lower()
    assert result.recovery_attempted is True
```

## 📝 Test Structure Standards

### Descriptive Test Names
```python
# ✅ CORRECT - Clear, descriptive names
def test_simple_agent_maintains_conversation_state_across_multiple_turns():
    """Test that agent preserves context between interactions."""
    # Test implementation

def test_react_agent_with_math_tool_saves_state_history():
    """Test ReactAgent with real math tool and state persistence."""
    # Test implementation

def test_agent_handles_invalid_configuration_gracefully():
    """Test agent behavior with invalid config."""
    # Test implementation
```

### Test Organization
```python
import pytest
from haive.core.agent import ReactAgent

class TestReactAgent:
    """Test suite for ReactAgent functionality."""

    @pytest.fixture
    def configured_agent(self) -> ReactAgent:
        """Create a properly configured test agent."""
        return ReactAgent(
            name="test_agent",
            model="gpt-4",
            tools=["calculator"]
        )

    def test_agent_with_real_math_tool(self, configured_agent: ReactAgent):
        """Test agent with real math tool using actual LLM."""
        result = configured_agent.process("What is 15 * 23?")
        assert "345" in result.response
        assert configured_agent.conversation_history  # Real state saved
```

## 🔧 Testing Tools and Commands

### Running Tests
```bash
# Run tests for specific package
poetry run pytest packages/haive-agents/tests/

# Run all tests with coverage
poetry run pytest --cov=haive

# Run tests with verbose output
poetry run pytest -vv

# Run specific test file
poetry run pytest tests/test_react_agent.py

# Test with real components only (no mocks)
poetry run pytest -k "not mock" -v
```

### Test Configuration
```python
# conftest.py - Test configuration
import pytest
from haive.core.engine import AugLLMConfig

@pytest.fixture(scope="session")
def test_llm_config():
    """Provide real LLM configuration for tests."""
    return AugLLMConfig(
        model="gpt-4",
        temperature=0.1,  # Low temperature for consistent tests
        max_tokens=500
    )

@pytest.fixture
def real_calculator():
    """Provide real calculator tool."""
    from haive.tools.math import Calculator
    return Calculator()
```

## 📊 Quality Metrics

### Test Coverage Requirements
- **Unit Tests**: >90% line coverage
- **Integration Tests**: All critical workflows
- **End-to-End Tests**: Complete user scenarios
- **Error Handling**: All exception paths

### Test Quality Indicators
- **No mocks**: 100% real component usage
- **Descriptive names**: Clear test intent
- **Real data**: Actual state files and responses
- **Comprehensive assertions**: Meaningful validations

### Performance Testing
```python
def test_agent_response_time_under_load():
    """Test agent performance with concurrent requests."""
    agent = ReactAgent(name="perf_test", model="gpt-4")
    
    import asyncio
    import time
    
    async def send_request():
        return await agent.arun("Hello!")
    
    # Test concurrent requests
    start_time = time.time()
    tasks = [send_request() for _ in range(10)]
    results = await asyncio.gather(*tasks)
    end_time = time.time()
    
    # Verify performance
    assert len(results) == 10
    assert all(result for result in results)
    assert (end_time - start_time) < 30  # Should complete within 30s
```

## 🚨 Common Anti-Patterns to Avoid

### 1. Enhanced/Artificial Scenarios
```python
# ❌ WRONG - Enhanced/artificial scenarios
def test_enhanced_agent_with_super_powers():
    # Creates unrealistic test conditions
    pass
```

### 2. Bypassing Logic
```python
# ❌ WRONG - Cheating/bypassing logic
def test_agent_bypassing_validation():
    agent._skip_validation = True  # Circumvents real behavior
    pass
```

### 3. Artificial Success
```python
# ❌ WRONG - Artificial success scenarios
def test_agent_always_succeeds():
    # Test that doesn't actually test real behavior
    pass
```

## 🎯 Test Development Workflow

### 1. Test-Driven Development
```python
# Write test first
def test_new_agent_processes_user_input():
    """Test new agent processes user input correctly."""
    agent = NewAgent(name="test")
    result = agent.process("Hello world")
    assert result.response
    assert result.success

# Implement to make test pass
class NewAgent:
    def process(self, input_text: str) -> ProcessResult:
        # Implementation
        pass
```

### 2. Real Component Integration
```python
# Always use real components in tests
@pytest.fixture
def real_agent():
    """Create agent with real LLM and tools."""
    return ReactAgent(
        name="test_agent",
        model="gpt-4",  # Real model
        tools=[Calculator(), WebSearchTool()]  # Real tools
    )
```

### 3. State History Validation
```python
def test_agent_saves_real_state_history():
    """Test that agent saves actual conversation state."""
    agent = ReactAgent(name="state_test", model="gpt-4")
    
    # First interaction
    result1 = agent.process("My name is Alice")
    
    # Second interaction
    result2 = agent.process("What's my name?")
    
    # Verify real state persistence
    assert "alice" in result2.response.lower()
    assert len(agent.conversation_history) == 4  # 2 user + 2 assistant
    assert agent.state_file_exists()
```

## 🔄 Continuous Testing

### Pre-commit Testing
```bash
# Always run before committing
poetry run pytest --cov=haive --cov-fail-under=90
poetry run ruff check
poetry run mypy

# Integration test suite
poetry run pytest tests/integration/ -v
```

### CI/CD Testing
```yaml
# .github/workflows/test.yml
name: Test Suite
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run real component tests
        run: |
          poetry run pytest --cov=haive --cov-fail-under=90
          poetry run pytest tests/integration/ -v
```

---

**Remember**: Tests are the foundation of code quality. Real component testing ensures our agents work correctly in production environments.