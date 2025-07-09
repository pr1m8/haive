# Dynamic Supervisor Agent

The Dynamic Supervisor Agent is a powerful coordination system that manages multiple specialized agents at runtime. It provides dynamic agent registration, intelligent task routing, and multi-step workflow orchestration through a ReAct (Reasoning + Acting) loop.

## Overview

The Dynamic Supervisor extends ReactAgent to provide:

- **Runtime Agent Management**: Add, remove, activate, and deactivate agents dynamically
- **Intelligent Task Routing**: Automatically route tasks to the most appropriate agent
- **Multi-Step Coordination**: Handle complex workflows requiring multiple agents
- **Tool-Based Execution**: Agents execute through handoff tools (no separate routing nodes)
- **State Persistence**: Full state serialization with agent exclusions for safety

## Architecture

```
┌─────────────────────────────────────────────────┐
│                Dynamic Supervisor               │
│  ┌─────────────────┐  ┌─────────────────────┐   │
│  │   ReactAgent    │  │  SupervisorState    │   │
│  │   (Base Loop)   │  │  (With Tools)       │   │
│  └─────────────────┘  └─────────────────────┘   │
│           │                       │             │
│           ▼                       ▼             │
│  ┌─────────────────┐  ┌─────────────────────┐   │
│  │  Dynamic Tools  │  │   Agent Registry    │   │
│  │  (Handoff Tools)│  │   (Runtime Mgmt)    │   │
│  └─────────────────┘  └─────────────────────┘   │
└─────────────────────────────────────────────────┘
                    │
                    ▼
        ┌─────────────────────────┐
        │    Specialized Agents   │
        │  ┌─────┐ ┌─────┐ ┌─────┐│
        │  │Agent│ │Agent│ │Agent││
        │  │  A  │ │  B  │ │  C  ││
        │  └─────┘ └─────┘ └─────┘│
        └─────────────────────────┘
```

## Key Components

### DynamicSupervisorAgent

The main supervisor class that coordinates agent execution.

```python
from haive.agents.dynamic_supervisor import DynamicSupervisorAgent
from haive.core.engine.aug_llm import AugLLMConfig

supervisor = DynamicSupervisorAgent(
    name="task_coordinator",
    engine=supervisor_engine,
    enable_agent_builder=False  # Optional: enable agent request capability
)
```

**Key Features:**

- Inherits from ReactAgent for looping behavior
- Uses SupervisorStateWithTools for dynamic tool generation
- Automatically syncs tools when agents are added/removed
- Supports both sync and async execution

### SupervisorStateWithTools

Enhanced state schema with dynamic agent management.

```python
from haive.agents.dynamic_supervisor.state import SupervisorStateWithTools

# Create and manage state
state = SupervisorStateWithTools()
state.add_agent("research", research_agent, "Research specialist")
state.activate_agent("research")
state.deactivate_agent("research")
state.remove_agent("research")
```

**State Fields:**

- `agents`: Dictionary of managed agents with metadata
- `last_executed_agent`: Track which agent last executed
- `agent_response`: Last agent response
- `execution_success`: Success/failure tracking
- `agent_choice_model`: Dynamic choice validation model

### Dynamic Tool Generation

Tools are generated automatically based on registered agents.

**Generated Tools:**

- `handoff_to_{agent_name}`: Execute specific agent
- `choose_agent`: Validate agent selection with current options

**Tool Features:**

- Execute agents directly (no separate routing node)
- Extract last message from agent responses
- Add engine metadata to HumanMessage responses
- Handle sync/async agent execution patterns

## Usage Examples

### Basic Setup

```python
import asyncio
from haive.agents.dynamic_supervisor import DynamicSupervisorAgent
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig, ModelType

# Create specialized agents
research_agent = SimpleAgent(
    name="research_agent",
    engine=AugLLMConfig(
        name="research_engine",
        llm_config=AzureLLMConfig(model=ModelType.GPT_4O_MINI),
        system_message="You are a research assistant."
    )
)

math_agent = SimpleAgent(
    name="math_agent",
    engine=AugLLMConfig(
        name="math_engine",
        llm_config=AzureLLMConfig(model=ModelType.GPT_4O_MINI),
        system_message="You are a math expert."
    )
)

# Create supervisor
supervisor = DynamicSupervisorAgent(
    name="coordinator",
    engine=AugLLMConfig(
        name="supervisor_engine",
        llm_config=AzureLLMConfig(model=ModelType.GPT_4O),
        force_tool_use=True
    )
)

# Initialize state with agents
state = supervisor.create_initial_state()
state.add_agent("research", research_agent, "Research expert")
state.add_agent("math", math_agent, "Math expert")

# Execute tasks
result = await supervisor.arun("What is the square root of 144?", state=state)
print(f"Executed by: {state.last_executed_agent}")
print(f"Response: {state.agent_response}")
```

### Dynamic Agent Management

```python
# Add agent at runtime
translator_agent = SimpleAgent(name="translator", engine=translator_engine)
state.add_agent("translator", translator_agent, "Translation expert")

# Use new agent
await supervisor.arun("Translate 'hello' to French", state=state)

# Deactivate agent temporarily
state.deactivate_agent("math")
await supervisor.arun("Calculate 5+5", state=state)  # Will use alternative

# Reactivate agent
state.activate_agent("math")
await supervisor.arun("Now calculate 5+5", state=state)  # Will use math agent

# Remove agent permanently
state.remove_agent("translator")
```

### Multi-Step Workflows

```python
# Complex task requiring multiple agents
task = """
Research the Fibonacci sequence, calculate the 10th number,
and write a Python function to generate it
"""

result = await supervisor.arun(task, state=state)

# Check execution history
for msg in state.messages:
    if hasattr(msg, 'additional_kwargs'):
        if msg.additional_kwargs.get('source') == 'agent_execution':
            agent = msg.additional_kwargs.get('agent_name')
            print(f"Agent {agent} executed: {msg.content[:100]}...")
```

## How It Works

### 1. Agent Registration

Agents are registered in the state's agent registry with metadata:

```python
state.add_agent(
    name="research",
    agent=research_agent,
    description="Research specialist",
    capabilities=["web_search", "analysis"],
    active=True
)
```

### 2. Dynamic Tool Generation

For each active agent, a handoff tool is created:

```python
@tool
def handoff_to_research(task_description: str) -> str:
    """Hand off a task to research agent."""
    # Get agent from registry
    agent = state.agents["research"].get_agent()

    # Execute agent with task
    result = agent.run(task_description)

    # Extract last message and add metadata
    response = extract_last_message(result)
    human_msg = HumanMessage(
        content=response,
        additional_kwargs={
            "agent_name": "research",
            "engine_name": agent.engine.name,
            "source": "agent_execution"
        }
    )
    state.messages.append(human_msg)

    return f"Agent research completed: {response}"
```

### 3. Supervisor Decision Making

The supervisor uses its LLM engine to:

1. Analyze the incoming task
2. Select the most appropriate agent
3. Call the corresponding handoff tool
4. Process the response and continue if needed

### 4. Message Flow

```
User Input → Supervisor → Tool Selection → Agent Execution → Response Processing → User Output
    ↑                                                                                    ↓
    └─────────────────── Continue if multi-step needed ←─────────────────────────────────┘
```

## Configuration

### DynamicSupervisorAgent Parameters

```python
DynamicSupervisorAgent(
    name="supervisor",                              # Supervisor identifier
    engine=supervisor_engine,                       # LLM engine for decision making
    enable_agent_builder=False,                     # Enable agent request tools
    state_schema_override=SupervisorStateWithTools, # Custom state schema
    auto_sync_tools=True,                          # Auto-sync tools on state changes
    **kwargs                                       # Additional ReactAgent parameters
)
```

### Engine Configuration

```python
# Supervisor engine - decision making
supervisor_engine = AugLLMConfig(
    name="supervisor_engine",
    llm_config=AzureLLMConfig(
        model=ModelType.GPT_4O,          # Use powerful model for coordination
        temperature=0.0                   # Deterministic routing decisions
    ),
    force_tool_use=True,                 # Always use tools for routing
    system_message=""                    # Set automatically by supervisor
)

# Agent engines - task execution
agent_engine = AugLLMConfig(
    name="specialist_engine",
    llm_config=AzureLLMConfig(
        model=ModelType.GPT_4O_MINI,     # Efficient model for tasks
        temperature=0.7                   # Allow creativity in responses
    ),
    system_message="You are a specialist in..."
)
```

## Message Attribution

Each agent execution adds metadata to messages:

```python
# HumanMessage from agent execution
{
    "content": "The square root of 144 is 12.",
    "additional_kwargs": {
        "agent_name": "math_agent",
        "engine_name": "math_engine",
        "source": "agent_execution"
    }
}
```

## Serialization

The implementation handles serialization by:

- Using `exclude=True` on agent fields in AgentInfo
- Storing only serializable metadata
- Reconstructing agents from registry when needed

```python
# Safe for msgpack serialization
serialized = msgpack.packb(state.model_dump())
deserialized_state = SupervisorStateWithTools(**msgpack.unpackb(serialized))
```

## Testing

Run the comprehensive test suite:

```bash
# All dynamic supervisor tests
poetry run pytest packages/haive-agents/tests/test_dynamic_supervisor/ -v

# Specific test file
poetry run pytest packages/haive-agents/tests/test_dynamic_supervisor/test_supervisor_real.py -v
```

## Best Practices

### 1. Agent Specialization

Create focused, specialized agents rather than general-purpose ones:

```python
# ✅ Good: Specialized agents
math_agent = SimpleAgent(system_message="You are a math expert. Solve calculations step by step.")
research_agent = SimpleAgent(system_message="You are a research assistant. Find and analyze information.")

# ❌ Bad: Overly broad agents
general_agent = SimpleAgent(system_message="You can do anything.")
```

### 2. Error Handling

Always check execution success:

```python
result = await supervisor.arun(task, state=state)
if not state.execution_success:
    print(f"Agent execution failed: {state.agent_response}")
```

### 3. State Management

Reuse state for related tasks to maintain context:

```python
# ✅ Good: Maintain context across related tasks
state = supervisor.create_initial_state()
await supervisor.arun("Research quantum computing", state=state)
await supervisor.arun("Summarize the key findings", state=state)

# ❌ Bad: New state loses context
state1 = supervisor.create_initial_state()
await supervisor.arun("Research quantum computing", state=state1)
state2 = supervisor.create_initial_state()  # Lost context!
```

## Key Differences from Experimental Version

- **ReactAgent Base**: Now inherits from ReactAgent for proper looping behavior
- **Enhanced State**: SupervisorStateWithTools with dynamic choice models
- **Better Message Handling**: Proper last-message extraction and metadata
- **Improved Engine Info**: Correct engine name extraction from agent engines
- **Production Ready**: Comprehensive testing and error handling

This implementation follows LangGraph patterns while maintaining the direct execution approach from our experiments.
