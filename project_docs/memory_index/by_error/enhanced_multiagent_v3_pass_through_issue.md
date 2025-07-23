# Enhanced MultiAgent V3 Pass-Through Issue

**Date**: 2025-01-21
**Issue**: Agents in Enhanced MultiAgent V3 are being treated as pass-through instead of executing
**Status**: Under Investigation

## 🚨 Problem Description

When using Enhanced MultiAgent V3 with sequential execution mode, the sub-agents are not being executed. Instead, they're being treated as pass-through nodes.

### Error Symptoms

```
WARNING Node [yellow]planner[/yellow]: No callable found, using pass-through
WARNING Node [yellow]worker[/yellow]: No callable found, using pass-through
WARNING Node [yellow]solver[/yellow]: No callable found, using pass-through
```

### Code Pattern That Fails

```python
# Creating agents
planner = SimpleAgent(name="planner", engine=config)
worker = ReactAgent(name="worker", engine=config, tools=tools)
solver = SimpleAgent(name="solver", engine=config)

# Creating Enhanced MultiAgent V3
multi_agent = EnhancedMultiAgent(
    name="coordinator",
    agents={
        "planner": planner,
        "worker": worker,
        "solver": solver
    },
    execution_mode="sequential",
    state_schema=StateSchema
)

# Execution - agents don't run, just pass-through
result = await multi_agent.arun(initial_state)
```

## 🔍 Investigation Findings

### 1. Agent Callability

Agents are not directly callable:

```python
callable(agent) == False
hasattr(agent, '__call__') == False
hasattr(agent, 'arun') == True  # But this isn't what graph expects
```

### 2. BaseGraph2 Node Detection

The graph looks for callables in this order:

1. Direct callable: `callable(node)`
2. Metadata callable: `node.metadata["callable"]`
3. `__call__` method: `callable(node.__call__)`

Agents don't match any of these patterns.

### 3. Enhanced MultiAgent V3 Implementation

The `add_intelligent_agent_routing` method adds agents directly:

```python
for agent_name, agent in agents.items():
    node_name = f"{prefix}{agent_name}"
    self.add_node(node_name, agent)  # Agent passed directly
```

## 🤔 Potential Solutions

### 1. Wrap Agents in AgentNodeConfig

Older implementations use:

```python
from haive.core.graph.node.agent_node import AgentNodeConfig
graph.add_node(node_name, AgentNodeConfig(name=node_name, agent=agent))
```

### 2. Make Agents Callable

Add a `__call__` method to Agent base class that delegates to execution.

### 3. Use Different Node Type

There might be a specific node type for agents in Enhanced MultiAgent V3.

### 4. Check Plan-and-Execute V3

The user mentioned Plan-and-Execute V3 infrastructure was working. Need to verify if it has the same issue or uses a different approach.

## 📋 Next Steps

1. Check if Plan-and-Execute V3 actually works or has same issue
2. Look for examples of working Enhanced MultiAgent V3 usage
3. Check if there's a specific way agents should be configured
4. Consider using AgentNodeConfig wrapper
5. Look for alternative execution patterns

## 🔗 Related Issues

- Plan-and-Execute V3 agent node execution issue (TODO #12)
- ReWOO V3 agent node execution issue (TODO #17)

## 💡 User Guidance

The user mentioned:

- "you shoudlnt habve to write node funcitnos like this itll auto go into state"
- This suggests Enhanced MultiAgent V3 should handle execution automatically
- But current implementation isn't working as expected

## 📚 References

- `/packages/haive-core/src/haive/core/graph/state_graph/base_graph2.py` - Node detection logic
- `/packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_v3.py` - Multi-agent implementation
- `/packages/haive-core/src/haive/core/graph/node/agent_node.py` - AgentNodeConfig

---

**Note**: This issue affects both Plan-and-Execute V3 and ReWOO V3 implementations. Resolution needed before continuing with advanced agent patterns.
