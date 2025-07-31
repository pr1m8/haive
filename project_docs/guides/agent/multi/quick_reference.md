# Multi-Agent Quick Reference - Haive Framework

**Version**: 1.0
**Purpose**: Quick reference for multi-agent development
**Last Updated**: 2025-01-18

## 🚀 Quick Setup

```python
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState
from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.agent_node_v3 import create_agent_node_v3

# Create agents
planner = SimpleAgent(
    name="planner",
    engine=AugLLMConfig(),
    structured_output_model=YourOutputModel
)

# Initialize state
state = MultiAgentState(agents=[planner])

# Create and run nodes
node = create_agent_node_v3("planner")
result = node(state, config)
```

## 📋 Essential Patterns

### 1. Structured Output Agent

```python
from pydantic import BaseModel, Field

class AgentOutput(BaseModel):
    result: str
    confidence: float = Field(ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)

agent = SimpleAgent(
    name="processor",
    structured_output_model=AgentOutput
)
```

### 2. Custom State Schema

```python
class WorkflowState(MultiAgentState):
    # Input fields
    task: str = ""

    # Agent output fields (updated directly)
    result: str = ""
    confidence: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)
```

### 3. Sequential Execution

```python
# Create nodes
node1 = create_agent_node_v3("agent1")
node2 = create_agent_node_v3("agent2")

# Execute sequence
result1 = node1(state, config)  # Updates state fields
result2 = node2(state, config)  # Reads from state fields
```

## 🔧 Common Code Snippets

### Agent Creation

```python
# Basic agent
agent = SimpleAgent(
    name="processor",
    engine=AugLLMConfig(
        temperature=0.7,
        system_message="You are a helpful assistant."
    )
)

# Agent with structured output
agent = SimpleAgent(
    name="analyzer",
    engine=AugLLMConfig(),
    structured_output_model=AnalysisResult
)

# Agent with tools
from haive.agents.react import ReactAgent

agent = ReactAgent(
    name="researcher",
    engine=AugLLMConfig(),
    tools=[search_tool, calculator]
)
```

### State Management

```python
# Initialize state
state = MultiAgentState(
    agents=[agent1, agent2],
    task="Your task here"
)

# Get agent state
agent_state = state.get_agent_state("agent1")

# Update agent state
state.update_agent_state("agent1", {"status": "completed"})

# Direct field access
result = state.result  # Direct access to agent outputs
```

### Node Execution

```python
# Basic execution
node = create_agent_node_v3("agent_name")
result = node(state, config)

# With debug
result = node(state, {"debug": True})

# Async execution
result = await node(state, config)
```

## 🎯 Self-Discover Pattern

```python
# Step 1: Create sequential agents
selector = SimpleAgent(name="selector", structured_output_model=SelectedModules)
adapter = SimpleAgent(name="adapter", structured_output_model=AdaptedModules)
reasoner = SimpleAgent(name="reasoner", structured_output_model=ReasoningStructure)

# Step 2: Define state with all output fields
class SelfDiscoverState(MultiAgentState):
    # Selector outputs
    selected_modules: List[str] = Field(default_factory=list)
    rationale: str = ""

    # Adapter outputs
    adapted_modules: List[Dict[str, str]] = Field(default_factory=list)
    task_context: str = ""

    # Reasoner outputs
    reasoning_structure: Dict[str, Any] = Field(default_factory=dict)
    steps: List[str] = Field(default_factory=list)

# Step 3: Sequential execution
selector_node = create_agent_node_v3("selector")
adapter_node = create_agent_node_v3("adapter")
reasoner_node = create_agent_node_v3("reasoner")

result1 = selector_node(state, config)  # Updates: selected_modules, rationale
result2 = adapter_node(state, config)   # Reads: selected_modules, Updates: adapted_modules
result3 = reasoner_node(state, config)  # Reads: adapted_modules, Updates: reasoning_structure
```

## 📊 Debug and Monitoring

```python
# Enable debug mode
result = node(state, {"debug": True})

# Monitor state size
state_size = len(str(state.model_dump()))
print(f"State size: {state_size} characters")

# Display state info
state.display_agent_table()
state.display_debug_info()

# Check recompilation needs
if state.needs_any_recompile():
    agents = state.get_agents_needing_recompile()
    print(f"Recompile needed: {agents}")
```

## 🚨 Common Errors & Solutions

### 1. Agent Not Found

```python
# ❌ ERROR: Agent 'processor' not found
# ✅ FIX: Ensure agent is in state.agents dict
state = MultiAgentState(agents=[processor])
```

### 2. Field Not Updated

```python
# ❌ ERROR: state.result is empty
# ✅ FIX: Agent needs structured_output_model
agent = SimpleAgent(
    name="processor",
    structured_output_model=ProcessorOutput  # ← Required!
)
```

### 3. Import Errors

```bash
# ❌ ERROR: ModuleNotFoundError
# ✅ FIX: Always use poetry run
poetry run python your_script.py
```

### 4. Schema Validation

```python
# ❌ ERROR: Field 'result' not found
# ✅ FIX: State schema must have all agent output fields
class WorkflowState(MultiAgentState):
    result: str = ""  # ← Must match agent output fields
```

## 🔗 File Locations

### Core Files

- `packages/haive-core/src/haive/core/schema/prebuilt/multi_agent_state.py`
- `packages/haive-core/src/haive/core/graph/node/agent_node_v3.py`
- `packages/haive-agents/src/haive/agents/simple/agent.py`

### Documentation

- `project_docs/guides/agent/multi/README.md` - Main guide
- `project_docs/guides/agent/multi/systems_guide.md` - Technical details
- `project_docs/guides/agent/multi/examples/` - Working examples

### Tests

- `packages/haive-core/tests/node/test_self_discover_workflow.py`
- `packages/haive-core/tests/schema/test_multi_agent_state.py`

## 🎯 Best Practices

1. **Always use structured outputs** for agent communication
2. **Define complete state schemas** with all agent output fields
3. **Use poetry run** for all Python commands
4. **Test with real components** (no mocks)
5. **Enable debug mode** during development
6. **Monitor state size** for performance
7. **Handle errors gracefully** with try-catch blocks

## 📚 Learning Path

1. **Start with basic sequential** - [examples/basic_sequential.py](examples/basic_sequential.py)
2. **Try Self-Discover pattern** - [examples/self_discover_example.py](examples/self_discover_example.py)
3. **Read the full guide** - [README.md](README.md)
4. **Explore integration patterns** - [systems_guide.md](systems_guide.md)
5. **Build your own** - Use the patterns for custom workflows

---

**Remember**: Multi-agent systems in Haive are about **direct field updates** and **clean agent communication**. No complex nested structures - just type-safe, direct field access.
