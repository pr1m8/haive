# Docstring Standards

Comprehensive guide for writing Google-style docstrings in the Haive project.

## 📋 Overview

Haive uses **Google-style docstrings** for all Python code documentation. These docstrings are automatically parsed by Sphinx to generate API documentation.

## 🎯 Basic Format

### Module Docstrings
```python
"""Short description of the module.

Longer description explaining the module's purpose, main concepts,
and how it fits into the larger system.

The module provides functionality for:
    - First main feature
    - Second main feature
    - Third main feature

Example:
    Basic usage example::

        from haive.agents.simple import SimpleAgent
        
        agent = SimpleAgent(name="my_agent")
        result = agent.invoke({"input": "Hello, world!"})

Note:
    Important notes about the module, dependencies, or usage.

See Also:
    :mod:`related.module`: Description of related module
    :class:`RelatedClass`: Description of related class
"""
```

### Class Docstrings
```python
class SimpleAgent(Agent):
    """A simple agent that processes input through a single workflow.

    The SimpleAgent provides a straightforward way to create agents with
    minimal configuration. It automatically handles state management and
    provides sensible defaults for common use cases.

    Args:
        name: The agent's name for identification and logging.
        config: Optional configuration object for customizing behavior.
        engine: Optional LLM engine. Defaults to OpenAI GPT-4.
        tools: Optional list of tools to make available to the agent.

    Attributes:
        name: The agent's name.
        state_schema: The Pydantic schema for agent state.
        graph: The underlying LangGraph state graph.

    Example:
        Creating and using a simple agent::

            agent = SimpleAgent(
                name="assistant",
                tools=[web_search_tool, calculator_tool]
            )
            
            result = agent.invoke({
                "messages": [HumanMessage(content="What's 2+2?")]
            })
            
            print(result["messages"][-1].content)

    Note:
        This agent is best for simple, single-step workflows. For more
        complex multi-step processes, consider using ChainAgent or
        MultiAgent.

    Raises:
        ValueError: If the name is empty or contains invalid characters.
        ConfigurationError: If the configuration is invalid.
    """
```

### Method Docstrings
```python
def invoke(self, input_data: dict) -> dict:
    """Execute the agent with the given input.

    Processes the input through the agent's workflow and returns the
    result. This is the primary method for running the agent.

    Args:
        input_data: Dictionary containing the input data. Must include
            any fields required by the agent's state schema.

    Returns:
        Dictionary containing the agent's output, including processed
        messages, tool results, and any additional state information.

    Raises:
        ValidationError: If input_data doesn't match the expected schema.
        ExecutionError: If the agent encounters an error during execution.
        ToolError: If a tool call fails and cannot be recovered.

    Example:
        Basic invocation::

            result = agent.invoke({
                "messages": [HumanMessage(content="Hello!")],
                "user_id": "user123"
            })
            
            # Access the response
            response = result["messages"][-1].content
            
        With tool usage::

            result = agent.invoke({
                "messages": [HumanMessage(content="What's the weather?")],
                "location": "San Francisco"
            })

    Note:
        This method is synchronous. For async execution, use `ainvoke()`.
    """
```

### Function Docstrings
```python
def create_agent_from_config(config_path: str) -> Agent:
    """Create an agent instance from a configuration file.

    Loads the configuration from the specified file and instantiates
    the appropriate agent type based on the configuration.

    Args:
        config_path: Path to the YAML or JSON configuration file.

    Returns:
        Configured agent instance ready for use.

    Raises:
        FileNotFoundError: If the configuration file doesn't exist.
        ConfigurationError: If the configuration is invalid or incomplete.
        ImportError: If the specified agent type cannot be imported.

    Example:
        Loading from YAML::

            agent = create_agent_from_config("config/my_agent.yaml")
            result = agent.invoke({"input": "test"})

        Loading from JSON::

            agent = create_agent_from_config("config/my_agent.json")
    """
```

## 📝 Section Details

### Required Sections

#### **Args**
- List all parameters with types and descriptions
- Use present tense: "The input data" not "The input data that will be processed"
- Be specific about expected formats and constraints

```python
Args:
    name: The agent's unique identifier. Must be alphanumeric.
    config: Configuration object. If None, uses default settings.
    timeout: Maximum execution time in seconds. Defaults to 30.
    tools: List of tool instances to make available to the agent.
        Each tool must implement the Tool protocol.
```

#### **Returns**
- Describe the return value type and contents
- Explain the structure for complex return types
- Mention important attributes or methods

```python
Returns:
    AgentResult containing the execution results. The result includes:
        - messages: List of processed messages
        - metadata: Execution metadata and timing
        - state: Final agent state after execution
```

#### **Raises**
- List all exceptions that might be raised
- Explain when each exception occurs
- Include both direct raises and propagated exceptions

```python
Raises:
    ValueError: If name is empty or contains invalid characters.
    ConfigurationError: If the configuration is invalid or incomplete.
    TimeoutError: If execution exceeds the specified timeout.
    ToolError: If a required tool is not available or fails.
```

### Optional Sections

#### **Example**
- Provide working code examples
- Show realistic usage scenarios
- Include expected outputs when helpful

```python
Example:
    Basic usage::

        agent = SimpleAgent(name="helper")
        result = agent.invoke({"input": "Hello"})
        
    With custom configuration::

        config = AgentConfig(temperature=0.7, max_tokens=100)
        agent = SimpleAgent(name="helper", config=config)
        result = agent.invoke({"input": "Hello"})
        print(result["output"])  # "Hello! How can I help you?"
```

#### **Note**
- Important information about usage
- Warnings about common pitfalls
- Performance considerations

```python
Note:
    This method loads the entire dataset into memory. For large
    datasets, consider using the streaming version instead.
    
    The agent maintains conversation history automatically.
    Clear it manually if needed using `agent.clear_history()`.
```

#### **See Also**
- Related classes, functions, or modules
- External resources or documentation
- Alternative approaches

```python
See Also:
    :class:`ChainAgent`: For multi-step workflows
    :func:`create_agent_from_config`: For configuration-based creation
    :mod:`haive.tools`: Available tools and utilities
```

#### **Attributes** (for classes)
- Public attributes that users should know about
- Properties that provide important information
- Don't document private attributes

```python
Attributes:
    name: The agent's unique identifier.
    state_schema: Pydantic schema for validating agent state.
    is_configured: True if the agent has been properly configured.
    tool_count: Number of available tools.
```

## 🎨 Style Guidelines

### Language and Tone
- **Present tense**: "Returns the result" not "Will return the result"
- **Active voice**: "Processes the input" not "The input is processed"
- **Imperative for Args**: "The input data" not "This is the input data"
- **Be specific**: "List of tool instances" not "Tools"

### Formatting
- **First line**: Short, concise summary (one line)
- **Blank line**: After first line if there's more content
- **Paragraphs**: Separate with blank lines
- **Code blocks**: Use double colons `::` for code examples
- **References**: Use Sphinx cross-references `:class:`, `:func:`, etc.

### Content Guidelines
- **Be comprehensive**: Include all important information
- **Be concise**: Don't repeat information unnecessarily
- **Be accurate**: Ensure all information is correct and up-to-date
- **Be helpful**: Focus on what users need to know

## ✅ Common Patterns

### Configuration Classes
```python
class AgentConfig(BaseModel):
    """Configuration for agent behavior and capabilities.

    This configuration class provides fine-grained control over agent
    behavior, including LLM parameters, tool availability, and execution
    constraints.

    Attributes:
        temperature: Randomness in LLM responses (0.0-1.0). Default 0.7.
        max_tokens: Maximum tokens in generated responses. Default 1000.
        tools: List of tool names to make available to the agent.
        timeout: Maximum execution time in seconds. Default 30.
        retry_count: Number of retries on failure. Default 3.

    Example:
        Creating a conservative configuration::

            config = AgentConfig(
                temperature=0.1,
                max_tokens=500,
                tools=["web_search", "calculator"],
                timeout=60
            )

        Using with an agent::

            agent = SimpleAgent(name="assistant", config=config)
    """
```

### State Classes
```python
class AgentState(StateSchema):
    """State schema for tracking agent execution.

    This schema defines the structure of data that flows through
    the agent's execution graph. All state modifications must
    conform to this schema.

    Attributes:
        messages: Conversation history and current messages.
        user_id: Identifier for the current user session.
        metadata: Additional execution metadata and context.
        tools_used: List of tools invoked during execution.

    Note:
        This schema uses Pydantic v2 features. All fields are
        validated during state transitions.
    """
```

### Factory Functions
```python
def create_simple_agent(name: str, **kwargs) -> SimpleAgent:
    """Factory function for creating a SimpleAgent with sensible defaults.

    This convenience function sets up a SimpleAgent with commonly-used
    configurations and sensible defaults, reducing boilerplate code.

    Args:
        name: The agent's unique identifier.
        **kwargs: Additional configuration options passed to the agent.
            Common options include 'tools', 'temperature', and 'timeout'.

    Returns:
        Configured SimpleAgent instance ready for use.

    Example:
        Quick agent creation::

            agent = create_simple_agent("helper")
            
        With customization::

            agent = create_simple_agent(
                "research_assistant",
                tools=["web_search", "calculator"],
                temperature=0.3
            )
    """
```

## ❌ Common Mistakes

### Don't Do This
```python
def process(data):
    """Process data."""  # Too brief, no Args/Returns
    
def calculate(x, y, operation="add"):
    """Does math stuff.
    
    x: first number
    y: second number  # Wrong format for Args
    operation: what to do
    """
    
class MyAgent:
    """Agent class."""  # No description of purpose or usage
```

### Do This Instead
```python
def process(data: dict) -> ProcessResult:
    """Process input data through the configured pipeline.

    Args:
        data: Input data dictionary containing required fields.

    Returns:
        ProcessResult containing the processed data and metadata.

    Raises:
        ValidationError: If data doesn't match the expected schema.
    """
    
def calculate(x: float, y: float, operation: str = "add") -> float:
    """Perform mathematical operations on two numbers.

    Args:
        x: First operand.
        y: Second operand.
        operation: Operation to perform. Options: "add", "subtract",
            "multiply", "divide". Defaults to "add".

    Returns:
        Result of the mathematical operation.

    Raises:
        ValueError: If operation is not supported.
        ZeroDivisionError: If dividing by zero.

    Example:
        Basic arithmetic::

            result = calculate(5, 3, "add")  # Returns 8
            result = calculate(10, 2, "divide")  # Returns 5.0
    """
    
class MyAgent(Agent):
    """Custom agent for specialized task processing.

    This agent extends the base Agent class to provide specialized
    functionality for handling complex, multi-step workflows with
    custom validation and error handling.

    Args:
        name: Unique identifier for the agent.
        config: Configuration object for customizing behavior.

    Example:
        Creating and using the agent::

            agent = MyAgent(name="processor")
            result = agent.invoke({"input": "data"})
    """
```

---

**Remember**: Good docstrings are an investment in code maintainability and user experience. They should answer the questions users have when they encounter your code.