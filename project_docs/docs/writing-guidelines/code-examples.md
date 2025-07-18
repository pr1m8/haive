# Code Examples Guide

How to write effective, clear, and useful code examples for Haive documentation.

## 🎯 Purpose of Code Examples

Code examples should:

- **Demonstrate real usage** - Solve actual problems users face
- **Work as written** - Copy-paste should work without modification
- **Teach concepts** - Show best practices and patterns
- **Build confidence** - Help users succeed quickly

## 📋 Example Types

### 1. **Quick Start Examples**

Show the simplest possible usage:

```python
from haive.agents.simple import SimpleAgent

# Create a basic agent
agent = SimpleAgent(name="helper")

# Use the agent
result = agent.invoke({"input": "Hello, world!"})
print(result["output"])
```

**Guidelines:**

- Minimal setup required
- Single clear purpose
- Immediate visible result
- No complex configuration

### 2. **Complete Working Examples**

Full examples that demonstrate real workflows:

```python
from haive.agents.simple import SimpleAgent
from haive.tools import WebSearchTool, CalculatorTool
from haive.core.types import HumanMessage

# Configure tools
tools = [
    WebSearchTool(api_key="your_api_key"),
    CalculatorTool()
]

# Create agent with tools
agent = SimpleAgent(
    name="research_assistant",
    tools=tools,
    temperature=0.7
)

# Example conversation
messages = [
    HumanMessage(content="What's the population of Tokyo and calculate the density if the area is 2,194 km²?")
]

# Execute
result = agent.invoke({"messages": messages})

# Access results
final_message = result["messages"][-1]
print(f"Assistant: {final_message.content}")

# Check what tools were used
tools_used = result.get("tools_used", [])
print(f"Tools used: {tools_used}")
```

**Guidelines:**

- Complete imports and setup
- Real-world scenario
- Show error handling where relevant
- Explain each major step

### 3. **Configuration Examples**

Show different ways to configure components:

```python
# Basic configuration
basic_config = AgentConfig(
    temperature=0.7,
    max_tokens=1000
)

# Advanced configuration
advanced_config = AgentConfig(
    temperature=0.3,
    max_tokens=2000,
    tools=["web_search", "calculator", "file_reader"],
    timeout=60,
    retry_count=3,
    streaming=True
)

# From file configuration
config = AgentConfig.from_file("config/my_agent.yaml")

# Environment-based configuration
config = AgentConfig.from_env(prefix="HAIVE_AGENT_")
```

**Guidelines:**

- Show progression from simple to complex
- Explain when to use each approach
- Include common configurations
- Reference external config files

### 4. **Error Handling Examples**

Demonstrate proper error handling:

```python
from haive.agents.simple import SimpleAgent
from haive.core.exceptions import ValidationError, ExecutionError

agent = SimpleAgent(name="helper")

try:
    result = agent.invoke({
        "messages": [HumanMessage(content="Hello")]
    })

except ValidationError as e:
    print(f"Input validation failed: {e}")
    # Handle invalid input

except ExecutionError as e:
    print(f"Agent execution failed: {e}")
    # Handle execution failure

except Exception as e:
    print(f"Unexpected error: {e}")
    # Handle unexpected errors
```

**Guidelines:**

- Show specific exception types
- Demonstrate recovery strategies
- Include logging where appropriate
- Explain when errors occur

## 🎨 Writing Style

### Code Style

Follow Haive project conventions:

```python
# Good: Clear variable names
agent = SimpleAgent(name="research_assistant")
search_results = agent.invoke(query_data)

# Bad: Unclear abbreviations
a = SimpleAgent(name="ra")
res = a.invoke(qd)
```

### Comments

Use comments to explain the why, not the what:

```python
# Configure agent for conservative responses
agent = SimpleAgent(
    name="fact_checker",
    temperature=0.1,  # Low temperature for factual accuracy
    max_tokens=500    # Limit response length
)

# Use structured input for better results
input_data = {
    "messages": [HumanMessage(content=query)],
    "context": {"domain": "science", "accuracy_required": True}
}
```

### Documentation Strings

Include docstrings for complex examples:

```python
def create_research_agent(api_keys: dict) -> SimpleAgent:
    """Create a research agent with web search capabilities.

    Args:
        api_keys: Dictionary containing API keys for external services.
            Must include 'search_api_key' and optionally 'llm_api_key'.

    Returns:
        Configured SimpleAgent ready for research tasks.

    Example:
        >>> keys = {"search_api_key": "your_key"}
        >>> agent = create_research_agent(keys)
        >>> result = agent.invoke({"input": "Latest AI research"})
    """
    tools = [WebSearchTool(api_key=api_keys["search_api_key"])]

    return SimpleAgent(
        name="researcher",
        tools=tools,
        temperature=0.3
    )
```

## 📝 Content Organization

### Example Structure

Organize examples with clear sections:

````markdown
## Creating a Simple Agent

Brief explanation of what this example demonstrates.

### Basic Usage

```python
# Minimal example
```
````

### With Configuration

```python
# Extended example with configuration
```

### Complete Example

```python
# Full working example
```

### Expected Output

```
Expected output from the example
```

### Next Steps

What to try after this example.

````

### Progressive Complexity
Build examples from simple to complex:

1. **Hello World** - Absolute minimum
2. **Basic Features** - Core functionality
3. **Common Patterns** - Typical usage
4. **Advanced Features** - Full capabilities
5. **Real Applications** - Production-like examples

## 🧪 Testing Examples

### Verification Process
All examples must be:

1. **Runnable** - Execute without errors
2. **Complete** - Include all necessary imports
3. **Current** - Work with latest versions
4. **Realistic** - Solve real problems

### Test Script Template
```python
"""
Test script for documentation examples.
Run this to verify all examples work.
"""
import sys
from pathlib import Path

def test_basic_agent_creation():
    """Test the basic agent creation example."""
    from haive.agents.simple import SimpleAgent

    # Example from docs
    agent = SimpleAgent(name="helper")
    result = agent.invoke({"input": "Hello, world!"})

    # Verify it works
    assert "output" in result
    assert isinstance(result["output"], str)
    print("✅ Basic agent creation works")

def test_agent_with_tools():
    """Test the agent with tools example."""
    # Test code here
    pass

if __name__ == "__main__":
    test_basic_agent_creation()
    test_agent_with_tools()
    print("🎉 All examples pass!")
````

## 🎯 Example Categories

### By Complexity Level

#### **Beginner Examples**

- Single function calls
- Basic configuration
- Simple inputs and outputs
- No error handling

```python
# Beginner: Basic agent usage
agent = SimpleAgent(name="helper")
result = agent.invoke({"input": "Hello"})
```

#### **Intermediate Examples**

- Multiple components
- Configuration options
- Basic error handling
- Common patterns

```python
# Intermediate: Agent with configuration
config = AgentConfig(temperature=0.7, tools=["web_search"])
agent = SimpleAgent(name="assistant", config=config)

try:
    result = agent.invoke({"input": "Research topic"})
except ExecutionError as e:
    print(f"Error: {e}")
```

#### **Advanced Examples**

- Complex workflows
- Custom components
- Comprehensive error handling
- Production patterns

```python
# Advanced: Custom agent with monitoring
class MonitoredAgent(SimpleAgent):
    def invoke(self, input_data):
        start_time = time.time()
        try:
            result = super().invoke(input_data)
            self.log_success(time.time() - start_time)
            return result
        except Exception as e:
            self.log_error(e, time.time() - start_time)
            raise
```

### By Use Case

#### **Getting Started**

- First agent creation
- Basic configuration
- Simple interactions

#### **Tool Integration**

- Adding tools to agents
- Tool configuration
- Tool result handling

#### **Advanced Workflows**

- Multi-step processes
- State management
- Complex routing

#### **Production Deployment**

- Error handling
- Monitoring
- Performance optimization

## ✅ Quality Checklist

### Before Publishing

- [ ] Example runs without errors
- [ ] All imports are included
- [ ] Variables are clearly named
- [ ] Comments explain non-obvious parts
- [ ] Output is shown where helpful
- [ ] Error cases are handled
- [ ] Example serves a clear purpose

### Content Quality

- [ ] Solves a real user problem
- [ ] Follows project conventions
- [ ] Uses current API versions
- [ ] Includes necessary context
- [ ] Shows best practices
- [ ] Scales appropriately

---

**Remember**: Good code examples are often the difference between a user succeeding with your framework or giving up. Invest time in making them excellent.
