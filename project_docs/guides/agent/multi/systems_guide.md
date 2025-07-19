# Multi-Agent Systems in Haive

## Overview

Haive provides sophisticated multi-agent systems that enable complex workflows through hierarchical state management, direct field updates, and seamless agent coordination. The system is built around two core components:

- **MultiAgentState**: Container state schema for managing multiple agents
- **AgentNodeV3**: Execution nodes that enable direct field updates and Self-Discover workflows

## Key Features

### 🏗️ Hierarchical State Management

Unlike traditional approaches that flatten agent schemas, Haive maintains each agent's schema independently while providing coordinated execution:

```python
# Each agent maintains its own schema
planner_state = state.get_agent_state("planner")  # {"plan": [...], "confidence": 0.9}
executor_state = state.get_agent_state("executor")  # {"status": "ready", "resources": [...]}

# Shared resources available to all agents
state.messages  # Shared conversation history
state.tools     # Shared tool registry
state.engines   # Shared engine pool
```

### 🔄 Direct Field Updates

Agents with structured output schemas update container fields directly, enabling clean cross-agent communication:

```python
# Traditional approach (complex)
plan = state.agent_outputs["planner"]["plan"]

# Haive approach (direct)
plan = state.plan  # Direct field access
```

### 🧠 Self-Discover Workflows

Sequential agents can read each other's outputs directly from state fields:

```python
# Agent 1 outputs structured data
planner_result = PlanningResult(plan=["Step 1", "Step 2"], priority="high")
# Updates: state.plan, state.priority

# Agent 2 reads directly from state
executor_input = {"plan": state.plan, "priority": state.priority}
# Clean, type-safe field access
```

## Architecture

### Container-Based Approach

```
MultiAgentState (Container)
├── agents: Dict[str, Agent]           # Agent instances
├── agent_states: Dict[str, Dict]      # Isolated agent states
├── messages: List[BaseMessage]        # Shared conversation
├── tools: List[Tool]                  # Shared tools
├── engines: Dict[str, Engine]         # Shared engines
└── [dynamic fields from agents]       # Direct field updates
```

### Execution Flow

1. **State Projection**: Container state → Agent-specific schema
2. **Agent Execution**: Agent processes projected state
3. **Output Integration**: Results → Container state updates
4. **Field Updates**: Structured outputs update container fields directly

## Quick Start

### Basic Setup

```python
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState
from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

# Create agents with structured output
planner = SimpleAgent(
    name="planner",
    engine=AugLLMConfig(),
    structured_output_model=PlanningResult
)

executor = SimpleAgent(
    name="executor",
    engine=AugLLMConfig(),
    structured_output_model=ExecutionResult
)

# Initialize state
state = MultiAgentState(agents=[planner, executor])
```

### Sequential Execution

```python
from haive.core.graph.node.agent_node_v3 import create_agent_node_v3

# Create nodes
plan_node = create_agent_node_v3("planner")
exec_node = create_agent_node_v3("executor")

# Execute sequence
result1 = plan_node(state, config)  # Updates planning fields
result2 = exec_node(state, config)  # Reads planning fields, outputs execution fields
```

### LangGraph Integration

```python
from langgraph.graph import StateGraph

# Build graph
graph = StateGraph(MultiAgentState)
graph.add_node("plan", create_agent_node_v3("planner"))
graph.add_node("execute", create_agent_node_v3("executor"))
graph.add_node("review", create_agent_node_v3("reviewer"))

# Define flow
graph.add_edge("plan", "execute")
graph.add_edge("execute", "review")

# Compile and run
app = graph.compile()
final_state = app.invoke(state)
```

## Advanced Usage

### Self-Discover Workflow

```python
from typing import List, Dict, Any
from pydantic import BaseModel, Field

# Define structured outputs
class SelectedModules(BaseModel):
    selected_modules: List[str]
    rationale: str
    confidence: float = Field(ge=0.0, le=1.0)

class AdaptedModules(BaseModel):
    adapted_modules: List[Dict[str, str]]
    task_context: str
    adaptation_notes: str

class ReasoningStructure(BaseModel):
    reasoning_structure: Dict[str, Any]
    steps: List[str]
    methodology: str

# Create agents with structured outputs
selector = SimpleAgent(
    name="selector",
    engine=AugLLMConfig(),
    structured_output_model=SelectedModules
)

adapter = SimpleAgent(
    name="adapter", 
    engine=AugLLMConfig(),
    structured_output_model=AdaptedModules
)

reasoner = SimpleAgent(
    name="reasoner",
    engine=AugLLMConfig(),
    structured_output_model=ReasoningStructure
)

# Setup state with all required fields
class SelfDiscoverState(MultiAgentState):
    # Input fields
    task_description: str = ""
    available_modules: List[str] = Field(default_factory=list)
    
    # Output fields (directly updated by agents)
    selected_modules: List[str] = Field(default_factory=list)
    rationale: str = ""
    confidence: float = 0.0
    
    adapted_modules: List[Dict[str, str]] = Field(default_factory=list)
    task_context: str = ""
    adaptation_notes: str = ""
    
    reasoning_structure: Dict[str, Any] = Field(default_factory=dict)
    steps: List[str] = Field(default_factory=list)
    methodology: str = ""

# Initialize state
state = SelfDiscoverState(
    agents=[selector, adapter, reasoner],
    task_description="How can we reduce plastic waste in oceans?",
    available_modules=["systems_thinking", "root_cause_analysis", "solution_design"]
)

# Execute Self-Discover workflow
selector_node = create_agent_node_v3("selector")
adapter_node = create_agent_node_v3("adapter")
reasoner_node = create_agent_node_v3("reasoner")

# Sequential execution with direct field access
result1 = selector_node(state, config)  # Updates: selected_modules, rationale, confidence
result2 = adapter_node(state, config)   # Reads: selected_modules, Updates: adapted_modules
result3 = reasoner_node(state, config)  # Reads: adapted_modules, Updates: reasoning_structure

# Final state has all results directly accessible
print(f"Selected modules: {state.selected_modules}")
print(f"Reasoning structure: {state.reasoning_structure}")
print(f"Final methodology: {state.methodology}")
```

### Dynamic Agent Composition

```python
# Add agents at runtime
new_agent = SimpleAgent(name="validator", engine=AugLLMConfig())
state.agents["validator"] = new_agent

# Mark for recompilation
state.mark_agent_for_recompile("validator", "Added new agent")

# Check recompilation needs
if state.needs_any_recompile():
    agents_to_recompile = state.get_agents_needing_recompile()
    print(f"Recompiling: {agents_to_recompile}")
```

### Parallel Processing

```python
from haive.core.graph.node.agent_node_v3 import create_agent_node_v3

# Create parallel processing nodes
analyzer_node = create_agent_node_v3("analyzer")
summarizer_node = create_agent_node_v3("summarizer")
classifier_node = create_agent_node_v3("classifier")

# Execute in parallel (same input)
import asyncio

async def parallel_execution():
    tasks = [
        analyzer_node(state, config),
        summarizer_node(state, config),
        classifier_node(state, config)
    ]
    results = await asyncio.gather(*tasks)
    return results

# Results from all agents
results = asyncio.run(parallel_execution())
```

## Best Practices

### 1. Use Structured Outputs

```python
# ✅ GOOD - Structured output enables direct field updates
class AnalysisResult(BaseModel):
    analysis: str
    confidence: float
    recommendations: List[str]

agent = SimpleAgent(
    name="analyzer",
    structured_output_model=AnalysisResult
)

# Result updates state fields directly
# state.analysis, state.confidence, state.recommendations
```

### 2. Design Clean State Schemas

```python
# ✅ GOOD - Clear field organization
class WorkflowState(MultiAgentState):
    # Input fields
    task_description: str
    requirements: List[str]
    
    # Agent output fields
    analysis_result: str = ""
    plan: List[str] = Field(default_factory=list)
    execution_status: str = ""
    
    # Metadata
    workflow_id: str = ""
    started_at: datetime = Field(default_factory=datetime.now)
```

### 3. Handle Errors Gracefully

```python
# ✅ GOOD - Comprehensive error handling
try:
    result = agent_node(state, config)
    
    # Apply updates safely
    for key, value in result.update.items():
        if hasattr(state, key) and key != "agent_states":
            setattr(state, key, value)
            
except AgentExecutionError as e:
    logger.error(f"Agent execution failed: {e}")
    # Handle agent-specific errors
    
except ValidationError as e:
    logger.error(f"State validation failed: {e}")
    # Handle schema validation errors
```

### 4. Use Debug Mode for Development

```python
# ✅ GOOD - Enable debug for development
result = agent_node(state, {"debug": True})

# Shows detailed execution info:
# - State projection details
# - Agent input/output
# - Field updates
# - Execution timing
```

## Performance Considerations

### State Size Management

```python
# Monitor state size
state_size = len(str(state.model_dump()))
print(f"State size: {state_size} characters")

# Clean up old data
state.agent_outputs.clear()  # Clear legacy outputs
state.recompile_history = state.recompile_history[-10:]  # Keep last 10
```

### Memory Usage

```python
# Use shared fields efficiently
config = AgentNodeV3Config(
    agent_name="processor",
    shared_fields=["messages"],  # Only share what's needed
    update_container_state=False  # Skip state updates if not needed
)
```

### Execution Optimization

```python
# Batch agent executions
async def batch_execution(agents, state, config):
    tasks = []
    for agent_name in agents:
        node = create_agent_node_v3(agent_name)
        tasks.append(node(state, config))
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
```

## Troubleshooting

### Common Issues

1. **Agent Not Found**: Check agent is in `state.agents` dict
2. **Field Not Updated**: Verify agent has `structured_output_model` 
3. **Import Errors**: Use `poetry run` for all Python commands
4. **Schema Validation**: Ensure state schema has all required fields

### Debug Tools

```python
# State inspection
state.display_agent_table()    # Show agent overview
state.display_debug_info()     # Show detailed state info
state.create_agent_table()     # Rich table visualization

# Agent node debugging
result = agent_node(state, {"debug": True})  # Detailed execution info
```

### Performance Monitoring

```python
import time

# Measure execution time
start_time = time.time()
result = agent_node(state, config)
execution_time = time.time() - start_time

print(f"Agent execution took {execution_time:.2f} seconds")

# Monitor token usage
print(f"Total tokens: {state.get_token_usage_summary()}")
```

## Integration Examples

### FastAPI Integration

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class WorkflowRequest(BaseModel):
    task_description: str
    agents: List[str]

@app.post("/execute_workflow")
async def execute_workflow(request: WorkflowRequest):
    # Initialize state
    state = MultiAgentState(
        agents=get_agents(request.agents),
        task_description=request.task_description
    )
    
    # Execute workflow
    result = await run_multi_agent_workflow(state)
    
    return {
        "status": "completed",
        "results": result.model_dump(),
        "execution_time": result.execution_time
    }
```

### Streamlit Integration

```python
import streamlit as st
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState

st.title("Multi-Agent Workflow")

# User inputs
task = st.text_input("Task Description")
selected_agents = st.multiselect("Select Agents", ["planner", "executor", "reviewer"])

if st.button("Execute Workflow"):
    # Initialize state
    state = MultiAgentState(
        agents=get_agents(selected_agents),
        task_description=task
    )
    
    # Execute with progress
    with st.spinner("Executing workflow..."):
        result = execute_multi_agent_workflow(state)
    
    # Display results
    st.success("Workflow completed!")
    st.json(result.model_dump())
```

## API Reference

### Core Classes

- [`MultiAgentState`](../../../../packages/haive-core/src/haive/core/schema/prebuilt/multi_agent_state.py): Container state schema
- [`AgentNodeV3Config`](../../../../packages/haive-core/src/haive/core/graph/node/agent_node_v3.py): Agent execution configuration
- [`create_agent_node_v3`](../../../../packages/haive-core/src/haive/core/graph/node/agent_node_v3.py): Factory function

### Key Methods

- `state.get_agent_state(name)`: Get agent's isolated state
- `state.update_agent_state(name, updates)`: Update agent state
- `state.mark_agent_for_recompile(name, reason)`: Mark for recompilation
- `node(state, config)`: Execute agent node

### Configuration Options

- `shared_fields`: Fields to share from container to agent
- `output_mode`: How to handle outputs ("merge", "replace", "isolate")
- `project_state`: Whether to project state to agent schema
- `track_recompilation`: Whether to track recompilation needs

## Contributing

To contribute to multi-agent systems:

1. Follow the [Testing Philosophy](../../../active/standards/testing/philosophy.md) - NO MOCKS
2. Use [Google-style docstrings](../../../active/standards/documentation/google_style.md)
3. Test with real agents and real LLMs
4. Add comprehensive examples to docstrings
5. Update this documentation with new patterns

## See Also

- [Agent Development Guide](../../../active/implementation/agent_development/)
- [State Management Patterns](../../../active/architecture/schemas/)
- [LangGraph Integration](../../../active/implementation/langgraph_integration/)
- [Performance Optimization](../../../active/analysis/performance/)