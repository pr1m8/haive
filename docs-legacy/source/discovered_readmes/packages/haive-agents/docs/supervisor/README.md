# Supervisor Documentation

This directory contains comprehensive documentation for all supervisor implementations in the haive-agents package. The documentation covers architecture, patterns, usage, and best practices.

## Documentation Structure

### Core Documentation

- **README.md** - This file, main documentation index
- **REORGANIZED_STRUCTURE.md** - Overview of the reorganized package structure
- **REORGANIZATION_SUMMARY.md** - Summary of reorganization changes

### Implementation Documentation

- **dynamic_supervisor_README.md** - Dynamic supervisor package documentation
- **README_DYNAMIC.md** - Dynamic supervisor implementation details
- **IMPLEMENTATION_PLAN.md** - Implementation strategy and roadmap
- **LANGGRAPH_ANALYSIS.md** - LangGraph integration patterns

### Testing and Development

- **TEST_GUIDE.md** - Testing guidelines and best practices
- **DYNAMIC_ROUTING_DESIGN.md** - Dynamic routing architecture

### Archives

- **archive/** - Archived debug files and old implementations
  - **debug/** - Debug files from development process

## Supervisor Implementations

### 1. Dynamic Supervisor Package

**Location**: `/src/haive/agents/dynamic_supervisor/`

The main production implementation providing:

- **Runtime agent management** - Add/remove agents dynamically
- **Tool-based execution** - Agents execute through tools
- **ReAct integration** - Inherits reasoning and acting capabilities
- **State management** - Maintains agent registry and execution state

**Key Features:**

- Extends ReactAgent for reasoning loop
- SupervisorStateWithTools for dynamic tool generation
- Handoff tools execute agents directly
- Automatic tool synchronization

### 2. Supervisor Package

**Location**: `/src/haive/agents/supervisor/`

Alternative implementations including:

- **Basic SupervisorAgent** - Traditional supervisor pattern
- **Integrated supervisor** - Integrated multi-agent coordination
- **Registry utilities** - Agent registry management
- **Routing logic** - Task routing and agent selection

### 3. React Agent

**Location**: `/src/haive/agents/react/`

Foundation for supervisor implementations:

- **ReAct pattern** - Reasoning and acting loop
- **Tool integration** - Seamless tool usage
- **State management** - Conversation state handling
- **SimpleAgent extension** - Inherits base functionality

## Architecture Patterns

### 1. Tool-Based Agent Execution

The main pattern uses tools that execute agents directly:

```python
@tool
def handoff_to_agent(task: str) -> str:
    \"\"\"Transfer task to specific agent.\"\"\"
    result = await agent.arun(task)
    return f"Agent response: {result}"
```

**Benefits:**

- Flexible runtime agent selection
- Clean separation of concerns
- Easy integration with ReAct loop
- Dynamic tool generation

### 2. Agent Execution Node Pattern

Alternative pattern using dedicated execution nodes:

```python
# Supervisor decides routing
state.agent_route = "math_agent"

# Agent execution node runs selected agent
async def _agent_execution_node(state):
    agent = registry.get_active_agent(state.agent_route)
    result = await agent.arun(state.current_task)
```

**Benefits:**

- Clear separation of routing and execution
- Flexible agent selection
- Simple state requirements
- Clean architecture

### 3. Dynamic Tool Generation

Pattern for creating tools from agent registry:

```python
# Tools generated from current agents
def _generate_handoff_tools(self):
    tools = []
    for agent_name, agent_info in self.registry.items():
        tool = create_handoff_tool(agent_name, agent_info)
        tools.append(tool)
    return tools
```

**Benefits:**

- Automatic tool updates
- Registry-driven tool creation
- Validated agent selection
- Clean tool lifecycle

## Usage Patterns

### Basic Supervisor Usage

```python
from haive.agents.dynamic_supervisor import create_dynamic_supervisor

# Create supervisor
supervisor = create_dynamic_supervisor(name="task_router")

# Add agents
state = supervisor.create_initial_state()
state.add_agent("math", math_agent, "Mathematics expert")
state.add_agent("search", search_agent, "Web search specialist")

# Route tasks
result = await supervisor.arun("Calculate 15 * 23", state=state)
```

### Dynamic Agent Activation

```python
# Start with minimal agents
state = supervisor.create_initial_state()
state.add_agent("general", general_agent, "General assistant")

# Add specialized agents as needed
if task_requires_math:
    state.add_agent("math", math_agent, "Mathematics expert")

if task_requires_search:
    state.add_agent("search", search_agent, "Web search specialist")
```

### Multi-Step Coordination

```python
# Supervisor coordinates multi-step workflows
result = await supervisor.arun(
    "Research the topic, analyze findings, and create a presentation",
    state=state
)
```

## Best Practices

### 1. Agent Design

- **Specialized agents** for specific tasks
- **Clear descriptions** for routing decisions
- **Robust error handling** in implementations
- **Appropriate tool selection** for each agent

### 2. Supervisor Configuration

- **Clear system messages** for routing logic
- **Appropriate model selection** for task complexity
- **Proper state management** for multi-turn interactions
- **Resource optimization** for cost efficiency

### 3. State Management

- **Minimal state** for performance
- **Clear state transitions** for debugging
- **Proper state persistence** for long conversations
- **State validation** for correctness

### 4. Error Handling

- **Graceful degradation** when agents fail
- **Retry logic** for transient failures
- **Fallback agents** for critical functions
- **Comprehensive logging** for debugging

## Testing Philosophy

### No-Mocks Approach

All supervisor tests use real components:

- **Real LLM integrations** - Actual API calls
- **Real agent implementations** - Full agent stack
- **Real state management** - Actual state persistence
- **Real tool execution** - Complete tool workflow

### Test Categories

1. **Unit tests** - Individual component testing
2. **Integration tests** - Multi-component workflows
3. **Component tests** - Specific supervisor components
4. **Experimental tests** - Pattern validation

### Test Structure

```python
def test_supervisor_with_real_components():
    \"\"\"Test supervisor with real LLM and agents.\"\"\"
    # Create real supervisor
    supervisor = DynamicSupervisorAgent(
        engine=AugLLMConfig(model="gpt-4")
    )

    # Create real agents
    math_agent = SimpleAgent(engine=math_engine)
    search_agent = SimpleAgent(engine=search_engine)

    # Test real coordination
    state = supervisor.create_initial_state()
    state.add_agent("math", math_agent, "Math expert")
    state.add_agent("search", search_agent, "Search expert")

    # Verify real behavior
    result = await supervisor.arun("Find and calculate something", state=state)
    assert result is not None
    assert len(result) > 0
```

## Performance Considerations

### 1. Agent Lifecycle

- **Lazy loading** - Only activate agents when needed
- **Resource pooling** - Share resources between agents
- **Caching strategies** - Cache agent results appropriately
- **Monitoring** - Track agent performance and usage

### 2. State Management

- **State size optimization** - Keep state minimal
- **State update batching** - Batch updates when possible
- **State persistence** - Use appropriate storage backends
- **State cleanup** - Regular cleanup of old state

### 3. Tool Management

- **Tool caching** - Cache tool results when appropriate
- **Tool optimization** - Optimize tool implementations
- **Tool synchronization** - Efficient state-tool sync
- **Tool monitoring** - Track tool usage and performance

## Common Use Cases

### 1. Task Routing

Route different types of tasks to specialized agents:

- **Question answering** → General agent
- **Calculations** → Math agent
- **Research** → Search agent
- **Code generation** → Code agent

### 2. Multi-Step Workflows

Coordinate complex multi-step processes:

- **Research → Analysis → Presentation**
- **Data Collection → Processing → Reporting**
- **Problem Analysis → Solution Design → Implementation**

### 3. Resource Management

Optimize resource usage in multi-agent systems:

- **Dynamic activation** - Activate agents on demand
- **Load balancing** - Distribute work across agents
- **Cost optimization** - Use appropriate models for tasks
- **Performance monitoring** - Track and optimize usage

### 4. Error Recovery

Handle failures gracefully:

- **Fallback agents** - Backup agents for critical functions
- **Retry logic** - Automatic retry for transient failures
- **Graceful degradation** - Reduced functionality when agents fail
- **Error reporting** - Comprehensive error tracking

## Development Guidelines

### 1. Adding New Patterns

When implementing new supervisor patterns:

1. Study existing patterns in `/patterns/` directory
2. Follow established architecture principles
3. Implement comprehensive tests
4. Document the pattern thoroughly
5. Provide usage examples

### 2. Modifying Existing Implementations

When modifying supervisor implementations:

1. Maintain backward compatibility
2. Update all related tests
3. Update documentation
4. Consider performance implications
5. Test with real components

### 3. Documentation Standards

All documentation should include:

- **Clear purpose** and scope
- **Architecture overview** with diagrams
- **Usage examples** with code
- **Best practices** and guidelines
- **Testing instructions**
- **Performance considerations**

## Related Resources

### Implementation Code

- [Dynamic Supervisor](../../src/haive/agents/dynamic_supervisor/) - Main implementation
- [Supervisor Package](../../src/haive/agents/supervisor/) - Alternative implementations
- [React Agent](../../src/haive/agents/react/) - Foundation implementation

### Examples and Tests

- [Examples](../../examples/supervisor/) - Usage examples and patterns
- [Tests](../../tests/supervisor/) - Comprehensive test suites
- [Test Documentation](../../tests/supervisor/README.md) - Testing guidelines

### External Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/) - Graph execution framework
- [LangChain Tools](https://python.langchain.com/docs/modules/agents/tools/) - Tool integration
- [Pydantic Documentation](https://docs.pydantic.dev/) - State management

## Contributing

When contributing to supervisor documentation:

1. Follow the existing documentation structure
2. Include comprehensive examples
3. Test all code examples
4. Update cross-references as needed
5. Maintain consistency with existing patterns

## Roadmap

### Planned Improvements

1. **Enhanced routing** - More sophisticated agent selection
2. **Performance optimization** - Faster state management
3. **Extended patterns** - New architectural patterns
4. **Better monitoring** - Enhanced observability
5. **Improved error handling** - More robust error recovery

### Future Patterns

1. **Hierarchical supervisors** - Multi-level coordination
2. **Federated agents** - Distributed agent management
3. **Adaptive routing** - Learning-based agent selection
4. **Resource-aware scheduling** - Optimize resource usage
5. **Stream processing** - Real-time agent coordination

For questions or contributions, please refer to the main project documentation or create an issue in the repository.
