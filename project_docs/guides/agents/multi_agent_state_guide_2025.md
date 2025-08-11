# MultiAgentState Guide - Haive Framework

**Date**: August 7, 2025  
**Version**: 1.0  
**Purpose**: Comprehensive guide to MultiAgentState schema and patterns

## 🎯 Overview

MultiAgentState is the core state container for multi-agent workflows in Haive. It provides:
- **State isolation** between agents without schema flattening
- **Direct field updates** for structured output agents
- **Recompilation tracking** for dynamic workflows
- **Clean data flow** between sequential agents

## 📋 Core Architecture

### Class Definition

```python
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState
from haive.core.schema.tool_state import ToolState

class MultiAgentState(ToolState):
    """Container state for multi-agent workflows."""
    
    # Agent storage (list or dict)
    agents: list[Any] | dict[str, Any]
    
    # Isolated state for each agent
    agent_states: dict[str, dict[str, Any]]
    
    # Execution tracking
    active_agent: str | None
    agent_outputs: dict[str, Any]  # Legacy message pattern
    agent_execution_order: list[str]
    
    # Recompilation management
    agents_needing_recompile: set[str]
    recompile_count: int
    recompile_history: list[dict[str, Any]]
```

### Key Insight: No Schema Flattening

Unlike previous approaches that tried to merge all agent schemas, MultiAgentState:
- Keeps each agent's schema independent
- Projects state to agents as needed
- Maintains type safety without complex merging

## 🏗️ State Management Patterns

### 1. Direct Field Updates (Recommended)

Agents with `structured_output_model` update container fields directly:

```python
from pydantic import BaseModel

# Define structured outputs
class AnalysisResult(BaseModel):
    score: float
    findings: list[str]
    
class ReportResult(BaseModel):
    summary: str
    recommendations: list[str]

# Create agents with structured output
analyzer = SimpleAgentV3(
    name="analyzer",
    structured_output_model=AnalysisResult
)

reporter = SimpleAgentV3(
    name="reporter",
    structured_output_model=ReportResult
)

# Initialize state
state = MultiAgentState(agents=[analyzer, reporter])

# After analyzer runs, state has 'analyzer' field
# After reporter runs, state has 'reporter' field
# Both are typed and validated!
```

### 2. Agent State Isolation

Each agent maintains its own state:

```python
# Get agent-specific state
analyzer_state = state.get_agent_state("analyzer")

# Update agent state
state.update_agent_state("analyzer", {
    "last_run": datetime.now(),
    "iterations": 3
})

# Each agent's state is isolated
state.agent_states = {
    "analyzer": {"last_run": ..., "iterations": 3},
    "reporter": {"draft_count": 2}
}
```

### 3. Shared Fields

Configure fields shared between container and agents:

```python
# In AgentNodeV3Config
node_config = AgentNodeV3Config(
    agent_name="analyzer",
    shared_fields=["messages", "context", "tools"]
)

# These fields are copied to agent state during execution
```

## 💡 Usage Patterns

### Sequential Workflow with Data Flow

```python
# Real example from Self-Discover implementation
class StructureOutput(BaseModel):
    reasoning_modules: list[str]
    
class OperationalizeOutput(BaseModel):
    task_structure: dict[str, Any]
    
class ExecuteOutput(BaseModel):
    final_answer: str

# Create workflow
select_agent = SimpleAgentV3(
    name="select",
    structured_output_model=StructureOutput
)

adapt_agent = SimpleAgentV3(
    name="adapt",
    structured_output_model=OperationalizeOutput,
    prompt_template=ChatPromptTemplate.from_messages([
        ("system", "You are a reasoning adapter."),
        ("human", "Adapt these modules: {select.reasoning_modules}")
        # Direct access to previous agent's output!
    ])
)

implement_agent = SimpleAgentV3(
    name="implement",
    structured_output_model=ExecuteOutput,
    prompt_template=ChatPromptTemplate.from_messages([
        ("system", "You implement reasoning structures."),
        ("human", "Use structure: {adapt.task_structure}")
        # Direct access to adapt agent's output!
    ])
)

# Create workflow
workflow = EnhancedMultiAgentV4(
    agents=[select_agent, adapt_agent, implement_agent],
    execution_mode="sequential"
)

# Execute - data flows through fields
result = await workflow.arun({"task": "Solve complex problem"})
# result.final_answer is available!
```

### Parallel Analysis Pattern

```python
# Multiple agents analyze simultaneously
sentiment = SimpleAgentV3(
    name="sentiment",
    structured_output_model=SentimentResult
)

entities = SimpleAgentV3(
    name="entities", 
    structured_output_model=EntityResult
)

topics = SimpleAgentV3(
    name="topics",
    structured_output_model=TopicResult
)

# Create parallel analyzer
analyzer = EnhancedMultiAgentV4(
    agents=[sentiment, entities, topics],
    execution_mode="parallel"
)

# Execute
state = await analyzer.arun({"text": document})

# Access all results
print(f"Sentiment: {state.sentiment.score}")
print(f"Entities: {state.entities.names}")
print(f"Topics: {state.topics.main_topics}")
```

## 🔄 Recompilation Management

### Tracking Recompilation Needs

```python
# Mark agent for recompilation
state.mark_agent_for_recompile("analyzer", "Configuration changed")

# Check which agents need recompilation
needs_recompile = state.get_agents_needing_recompile()
print(f"Agents needing recompile: {needs_recompile}")

# Resolve after recompilation
state.resolve_agent_recompile("analyzer")

# View history
for event in state.recompile_history:
    print(f"{event['timestamp']}: {event['agent']} - {event['reason']}")
```

### Dynamic Agent Updates

```python
# Update agent configuration
new_analyzer = SimpleAgentV3(
    name="analyzer",
    temperature=0.2,  # Changed from 0.7
    tools=[new_tool]  # Added tool
)

# Update in state
state.agents["analyzer"] = new_analyzer
state.mark_agent_for_recompile("analyzer", "Added new tool")

# Workflow will recompile on next execution
```

## 🛠️ AgentNodeV3 Integration

### State Projection

AgentNodeV3 handles the magic of state projection:

```python
# In AgentNodeV3Config execution
def execute(self, state: MultiAgentState):
    # Get agent from state
    agent = state.get_agent(self.agent_name)
    
    # Project state to agent schema
    agent_state = self._project_state(state, agent)
    
    # Execute agent
    result = await agent.arun(agent_state)
    
    # Update container state
    if agent.structured_output_model:
        # Direct field update
        setattr(state, self.agent_name, result)
    else:
        # Legacy message pattern
        state.agent_outputs[self.agent_name] = result
```

### Shared Fields Configuration

```python
# Configure shared fields
config = AgentNodeV3Config(
    agent_name="processor",
    shared_fields=["messages", "context", "global_config"]
)

# These fields are copied from container to agent state
```

## 📊 Debugging and Monitoring

### Rich Debug Visualization

```python
# Display comprehensive debug info
state.display_debug_info("Workflow Status")

# Output shows:
# - Active agent
# - Execution order
# - Agent states tree
# - Recompilation needs
# - Agent outputs
```

### Create Agent Table

```python
# Get formatted table of agents
table = state.create_agent_table()
print(table)

# Shows:
# ┏━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━┓
# ┃ Agent    ┃ Type          ┃ Status  ┃
# ┡━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━┩
# │ analyzer │ SimpleAgentV3 │ Ready   │
# │ reporter │ SimpleAgentV3 │ Ready   │
# └──────────┴───────────────┴─────────┘
```

### Execution Tracking

```python
# Track execution order
print(f"Execution order: {state.agent_execution_order}")
# ['analyzer', 'reporter', 'formatter']

# Current active agent
print(f"Active: {state.active_agent}")

# Agent outputs (for message-based agents)
for agent, output in state.agent_outputs.items():
    print(f"{agent}: {output[:100]}...")
```

## 🎯 Best Practices

### 1. Use Structured Output

```python
# ✅ RECOMMENDED - Clean data flow
agent = SimpleAgentV3(
    name="processor",
    structured_output_model=ProcessResult
)

# ❌ AVOID - Message-based (legacy)
agent = SimpleAgentV3(
    name="processor"
    # No structured output - uses messages
)
```

### 2. Design Clear Data Flow

```python
# ✅ GOOD - Clear dependencies
Step1Output → Step2Input → Step3Input

# ❌ BAD - Circular dependencies
AgentA → AgentB → AgentC → AgentA
```

### 3. Initialize Agents Properly

```python
# ✅ CORRECT - List initialization
state = MultiAgentState(agents=[agent1, agent2, agent3])

# ✅ ALSO CORRECT - Dict initialization
state = MultiAgentState(agents={
    "analyzer": analyzer_agent,
    "reporter": reporter_agent
})

# ❌ WRONG - Empty initialization
state = MultiAgentState()
state.agents = [...]  # Don't do this
```

### 4. Handle Recompilation

```python
# Check before execution
if state.get_agents_needing_recompile():
    # Handle recompilation
    for agent_name in state.agents_needing_recompile:
        # Recompile agent...
        state.resolve_agent_recompile(agent_name)
```

## 🚨 Common Pitfalls

### 1. Accessing Non-Existent Fields

```python
# ❌ WRONG - Field might not exist yet
summary = state.analyzer.summary  # AttributeError!

# ✅ CORRECT - Check first
if hasattr(state, 'analyzer'):
    summary = state.analyzer.summary
```

### 2. Direct State Mutation

```python
# ❌ WRONG - Direct mutation
state.agent_states["analyzer"]["key"] = value

# ✅ CORRECT - Use methods
state.update_agent_state("analyzer", {"key": value})
```

### 3. Forgetting Agent Registration

```python
# ❌ WRONG - Agent not in state
node = create_agent_node_v3("missing_agent")
node(state)  # Error!

# ✅ CORRECT - Ensure agent exists
if "analyzer" in state.agents:
    node = create_agent_node_v3("analyzer")
```

## 🔗 Integration Examples

### With EnhancedMultiAgentV4

```python
# MultiAgentState is created automatically
workflow = EnhancedMultiAgentV4(
    agents=[agent1, agent2],
    execution_mode="sequential"
)

# Access the state
state = workflow.state  # MultiAgentState instance

# Monitor during execution
@workflow.after_node
def check_state(context):
    state = context.state
    print(f"Active: {state.active_agent}")
    print(f"Completed: {state.agent_execution_order}")
```

### With Custom Graphs

```python
# Create state manually
state = MultiAgentState(agents=[agent1, agent2])

# Build graph with agent nodes
graph = StateGraph(MultiAgentState)

# Add agent nodes
graph.add_node("agent1", create_agent_node_v3("agent1"))
graph.add_node("agent2", create_agent_node_v3("agent2"))

# Configure edges
graph.add_edge(START, "agent1")
graph.add_edge("agent1", "agent2")
graph.add_edge("agent2", END)

# Compile and run
chain = graph.compile()
result = await chain.ainvoke(state)
```

## 📅 What's New (August 2025)

- **No Schema Flattening**: Clean state isolation
- **Direct Field Updates**: Structured output pattern
- **AgentNodeV3 Integration**: Automatic state projection
- **Recompilation Tracking**: Dynamic workflow support
- **Rich Debug Visualization**: Comprehensive monitoring

## 🔗 Related Documentation

- [EnhancedMultiAgentV4 Guide](enhanced_multi_agent_v4_guide_2025.md)
- [MultiAgentState Source](../../packages/haive-core/src/haive/core/schema/prebuilt/multi_agent_state.py)
- [AgentNodeV3 Source](../../packages/haive-core/src/haive/core/graph/node/agent_node_v3.py)
- [Self-Discover Example](../../packages/haive-agents/examples/reasoning_and_critique/self_discover/)

---

**Last Updated**: August 7, 2025  
**Framework Version**: haive-core 0.2.0+