# Dynamic Supervisor Agent

The `DynamicSupervisorAgent` provides a powerful, LangGraph-style supervisor implementation with enhanced Haive-specific capabilities for dynamic agent management, adaptive response handling, and comprehensive performance monitoring.

## Overview

The Dynamic Supervisor extends the traditional supervisor pattern by enabling:

- **Runtime Agent Management**: Add/remove agents without system restart
- **Adaptive Response Handling**: Modify agent responses based on configuration
- **Performance Monitoring**: Track execution metrics and optimize routing
- **Enhanced State Management**: Comprehensive state tracking with execution history
- **Flexible Coordination**: Support for sequential and parallel execution patterns

## Key Features

### 🔄 Dynamic Agent Management

```python
from haive.agents.supervisor import DynamicSupervisorAgent
from haive.agents.react import ReactAgent

# Create supervisor
supervisor = DynamicSupervisorAgent(
    name="dynamic_supervisor",
    auto_rebuild_graph=True,
    enable_parallel_execution=False
)

# Add agents at runtime
research_agent = ReactAgent(name="researcher")
await supervisor.register_agent(
    research_agent,
    capability_description="Handles research and fact-finding tasks",
    execution_config={
        "priority": 3,
        "execution_timeout": 180.0,
        "max_retries": 2
    }
)

# Remove agents dynamically
await supervisor.unregister_agent("researcher")

# Update agent configuration
await supervisor.update_agent_config("researcher", {
    "priority": 4,
    "execution_timeout": 120.0
})
```

### 📊 Enhanced State Management

The `DynamicSupervisorState` provides comprehensive tracking:

```python
from haive.agents.supervisor import DynamicSupervisorState

# State includes:
# - Agent execution history with performance metrics
# - Routing decisions with reasoning
# - Dynamic configuration management
# - Performance statistics and monitoring
# - Task context and conversation metadata
```

### 🎯 Intelligent Routing with Reasoning

```python
# Supervisor makes decisions with detailed reasoning
decision = SupervisorDecision(
    target_agent="research_agent",
    reasoning="User query requires fact-finding and web research capabilities",
    confidence=0.85,
    available_agents=["research_agent", "writing_agent", "math_agent"],
    alternatives=[
        {"agent": "writing_agent", "score": 0.3},
        {"agent": "math_agent", "score": 0.1}
    ]
)
```

### 🔧 Response Adaptation

```python
# Configure response adaptation per agent
await supervisor.register_agent(
    agent,
    execution_config={
        "output_mode": "last_message",  # or "full_history"
        "state_adapters": {
            "response_filter": {"remove_markdown": True},
            "length_limiter": {"max_length": 200}
        },
        "custom_params": {
            "adaptation_level": "high",
            "filter_sensitive": True
        }
    }
)
```

## Architecture

### Core Components

1. **DynamicSupervisorAgent**: Main supervisor class
2. **DynamicSupervisorState**: Enhanced state schema
3. **AgentExecutionConfig**: Per-agent configuration
4. **AgentExecutionResult**: Execution tracking
5. **SupervisorDecision**: Decision tracking with reasoning

### Execution Flow

```
User Input → Supervisor Analysis → Agent Selection → Agent Execution → Response Adaptation → Output
     ↑                                    ↓
Performance Monitoring ← State Update ← Execution Tracking
```

### Graph Structure

```
START → Supervisor → Coordinator → Agent Nodes → Adapter → Supervisor
                         ↓
                       END
```

## Usage Examples

### Basic Dynamic Supervisor

```python
import asyncio
from haive.agents.supervisor import DynamicSupervisorAgent
from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage

async def basic_example():
    # Create supervisor
    supervisor = DynamicSupervisorAgent(
        name="basic_supervisor",
        engine=AugLLMConfig(),
        auto_rebuild_graph=True
    )

    # Add agents
    writing_agent = SimpleAgent(name="writer", engine=AugLLMConfig())
    math_agent = SimpleAgent(name="calculator", engine=AugLLMConfig())

    await supervisor.register_agent(
        writing_agent,
        "Handles writing and content creation"
    )
    await supervisor.register_agent(
        math_agent,
        "Handles mathematical calculations"
    )

    # Use supervisor
    result = await supervisor.ainvoke({
        "messages": [HumanMessage(content="Write a poem about mathematics")]
    })

    print(result)

asyncio.run(basic_example())
```

### Advanced Configuration

```python
async def advanced_example():
    supervisor = DynamicSupervisorAgent(
        name="advanced_supervisor",
        engine=AugLLMConfig(),
        auto_rebuild_graph=True,
        enable_parallel_execution=True,
        max_execution_history=200
    )

    # Add agent with detailed configuration
    specialist_agent = ReactAgent(
        name="specialist",
        engine=AugLLMConfig()
    )

    await supervisor.register_agent(
        specialist_agent,
        capability_description="Specialized problem solving with tools",
        execution_config={
            "priority": 5,
            "execution_timeout": 300.0,
            "max_retries": 3,
            "output_mode": "full_history",
            "handoff_back": True,
            "custom_params": {
                "use_advanced_reasoning": True,
                "enable_self_reflection": True
            },
            "state_adapters": {
                "quality_filter": {"min_quality_score": 0.8},
                "format_optimizer": {"optimize_for_readability": True}
            }
        }
    )

    # Monitor performance
    supervisor.print_supervisor_dashboard()

    # Get detailed performance metrics
    performance = supervisor.get_performance_summary()
    print(f"Success rate: {performance['success_rate']:.2%}")

asyncio.run(advanced_example())
```

### Runtime Agent Management

```python
async def runtime_management_example():
    supervisor = DynamicSupervisorAgent(name="runtime_supervisor")

    # Start with minimal setup
    base_agent = SimpleAgent(name="base", engine=AugLLMConfig())
    await supervisor.register_agent(base_agent, "Basic operations")

    # Dynamically add specialized agents based on needs
    async def add_specialist_if_needed(task_type: str):
        if task_type == "research" and not supervisor.agent_registry.is_agent_registered("researcher"):
            research_agent = ReactAgent(name="researcher", engine=AugLLMConfig())
            await supervisor.register_agent(
                research_agent,
                "Advanced research capabilities",
                execution_config={"priority": 4}
            )
        elif task_type == "coding" and not supervisor.agent_registry.is_agent_registered("coder"):
            code_agent = SimpleAgent(name="coder", engine=AugLLMConfig())
            await supervisor.register_agent(
                code_agent,
                "Programming and development tasks",
                execution_config={"priority": 3}
            )

    # Add agents based on incoming requests
    await add_specialist_if_needed("research")
    await add_specialist_if_needed("coding")

    # Remove agents when no longer needed
    await supervisor.unregister_agent("base")

asyncio.run(runtime_management_example())
```

## Performance Monitoring

### Built-in Metrics

- **Execution Count**: Total and per-agent execution counts
- **Success Rate**: Overall and per-agent success rates
- **Response Time**: Average execution duration
- **Error Tracking**: Failure counts and retry statistics
- **Usage Patterns**: Most/least used agents

### Dashboard Visualization

```python
# Print comprehensive dashboard
supervisor.print_supervisor_dashboard()

# Get programmatic access to metrics
metrics = supervisor.get_performance_summary()
```

### Performance Optimization

The supervisor automatically optimizes routing based on:

- Agent success rates
- Average response times
- Priority configurations
- Current load and availability

## Configuration Options

### Supervisor Configuration

| Parameter                   | Type | Default | Description                                  |
| --------------------------- | ---- | ------- | -------------------------------------------- |
| `auto_rebuild_graph`        | bool | True    | Automatically rebuild graph on agent changes |
| `enable_parallel_execution` | bool | False   | Enable parallel agent execution              |
| `max_execution_history`     | int  | 100     | Maximum execution records to maintain        |

### Agent Execution Configuration

| Parameter           | Type  | Default        | Description                              |
| ------------------- | ----- | -------------- | ---------------------------------------- |
| `priority`          | int   | 1              | Agent priority (higher = more preferred) |
| `execution_timeout` | float | 300.0          | Timeout in seconds                       |
| `max_retries`       | int   | 3              | Maximum retry attempts                   |
| `output_mode`       | str   | "full_history" | "full_history" or "last_message"         |
| `handoff_back`      | bool  | True           | Include handoff back messages            |
| `custom_params`     | dict  | {}             | Custom agent parameters                  |
| `state_adapters`    | dict  | {}             | Response adaptation rules                |

## Error Handling

The dynamic supervisor provides robust error handling:

- **Timeout Management**: Configurable timeouts per agent
- **Retry Logic**: Automatic retries with exponential backoff
- **Graceful Degradation**: Fallback to alternative agents
- **Error Recovery**: State cleanup and recovery procedures

## Best Practices

### 1. Agent Design

- Keep agents focused on specific capabilities
- Use descriptive capability descriptions
- Set appropriate timeouts and priorities

### 2. Performance Optimization

- Monitor agent performance regularly
- Adjust priorities based on usage patterns
- Remove unused agents to reduce overhead

### 3. State Management

- Clean up old execution history periodically
- Use appropriate state adapters for response filtering
- Monitor memory usage in long-running sessions

### 4. Error Handling

- Set realistic timeout values
- Configure appropriate retry counts
- Implement proper error logging

## Integration with Existing Haive Architecture

The Dynamic Supervisor seamlessly integrates with:

- **Haive Core**: Uses standard Agent base class and state schemas
- **LangGraph**: Compatible with LangGraph patterns and conventions
- **Persistence**: Supports Supabase auto-persistence
- **Tools**: Works with all Haive tool integrations
- **Memory**: Compatible with memory management systems

## Comparison with Standard Supervisor

| Feature                | Standard Supervisor | Dynamic Supervisor         |
| ---------------------- | ------------------- | -------------------------- |
| Agent Management       | Static registration | Runtime add/remove         |
| State Tracking         | Basic state         | Comprehensive tracking     |
| Performance Monitoring | Limited             | Full metrics and dashboard |
| Response Adaptation    | None                | Configurable adapters      |
| Graph Rebuilding       | Manual              | Automatic                  |
| Parallel Execution     | No                  | Optional                   |
| Decision Reasoning     | Basic               | Detailed with alternatives |

## Migration Guide

### From Standard Supervisor

```python
# Old approach
from haive.agents.supervisor import SupervisorAgent

supervisor = SupervisorAgent(name="supervisor")
supervisor.register_agent(agent)

# New approach
from haive.agents.supervisor import DynamicSupervisorAgent

supervisor = DynamicSupervisorAgent(name="supervisor")
await supervisor.register_agent(agent, "Agent description")
```

### Key Differences

1. **Async Registration**: Use `await` for agent registration/deregistration
2. **Enhanced Configuration**: Provide execution configuration during registration
3. **State Schema**: Use `DynamicSupervisorState` for enhanced tracking
4. **Performance Monitoring**: Access built-in performance metrics

## Troubleshooting

### Common Issues

1. **Graph Rebuild Failures**: Ensure all agents are properly configured
2. **Timeout Errors**: Adjust execution timeouts for slow agents
3. **Memory Usage**: Clean up execution history in long sessions
4. **Performance Degradation**: Monitor and optimize agent priorities

### Debug Mode

```python
# Enable detailed logging
import logging
logging.getLogger("haive.agents.supervisor").setLevel(logging.DEBUG)

# Use dashboard for monitoring
supervisor.print_supervisor_dashboard()

# Check performance metrics
performance = supervisor.get_performance_summary()
```

## Future Enhancements

Planned improvements include:

- **Machine Learning Optimization**: AI-driven routing optimization
- **Load Balancing**: Advanced load distribution algorithms
- **Health Monitoring**: Agent health checks and automatic recovery
- **Cost Optimization**: Token usage tracking and optimization
- **Advanced Adaptation**: More sophisticated response adaptation rules
