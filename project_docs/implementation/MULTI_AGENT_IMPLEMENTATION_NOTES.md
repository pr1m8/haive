# Multi-Agent Implementation Notes - CRITICAL

**Date**: 2025-01-15
**Status**: Too many implementations, need clarity

## 🚨 The Problem

We have **TOO MANY** multi-agent implementations:

1. `/packages/haive-agents/src/haive/agents/multi/agent.py` (30KB) - Complex 804-line monster
2. `/packages/haive-agents/src/haive/agents/multi/base.py` (16KB) - Abstract base
3. `/packages/haive-agents/src/haive/agents/multi/enhanced_base.py` (27KB) - Enhanced with conditional edges
4. `/packages/haive-agents/src/haive/agents/multi/multi_agent_v2.py` (11KB) - Rebuilt version
5. `/packages/haive-agents/src/haive/agents/multi/compatibility_enhanced_base.py` (23KB) - Compatibility layer
6. `/packages/haive-agents/src/haive/agents/multi/configurable_base.py` (11KB) - Configurable version
7. `/packages/haive-agents/src/haive/agents/multi/experiments/proper_list_multi_agent.py` (18KB) - "Proper" version
8. `/packages/haive-agents/src/haive/agents/multi/experiments/list_multi_agent.py` (7KB) - List-based

**ALL created on July 11, 2025** (except experiments on July 15)

## ❌ What's Wrong With Each

### 1. `agent.py` (The 804-line monster)

- **Problem**: Over-engineered with too many coordination modes
- **Issues**: Complex state management, AgentSchemaComposer complexity
- **Status**: NOT imported by `__init__.py`

### 2. `base.py` (Currently imported)

- **Problem**: Abstract base that's actually imported
- **Issues**: Still uses complex patterns
- **Status**: This is what `__init__.py` imports

### 3. `enhanced_base.py`

- **Problem**: Even more complex with conditional edges
- **Issues**: Trying to do too much
- **Status**: Not used

### 4. `multi_agent_v2.py`

- **Problem**: Uses MultiAgentState but still complex
- **Issues**: Mentions AgentNodeV3 but doesn't use it properly
- **Status**: Not imported

### 5. `proper_list_multi_agent.py`

- **Problem**: Claims to use AgentNodeV3 properly but has issues
- **Issues**: Forces MultiAgentState, loses type safety
- **Status**: Experimental, not production

## 🎯 What We Actually Need

### Core Requirements:

1. **Simple sequential flow**: ReactAgent → SimpleAgent
2. **Type safety**: Each agent keeps its typed state schema
3. **Use AgentNodeV3**: For proper state projection
4. **Private state passing**: LangGraph pattern
5. **Clean API**: Simple to use

### The Correct Approach:

```python
from typing import List, Optional, Any
from pydantic import Field
from haive.agents.base.agent import Agent
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.graph.node.agent_node_v3 import create_agent_node_v3

class MultiAgent(Agent):
    """Multi-agent that uses private state passing and AgentNodeV3."""

    # These are FIELDS - agents passed in during creation
    agents: List[Agent] = Field(..., description="List of agents to coordinate")

    # Mode for execution
    mode: Literal["sequential", "conditional"] = Field(default="sequential")

    # For Plan & Execute pattern specifically
    planner: Optional[Agent] = Field(default=None)
    executor: Optional[Agent] = Field(default=None)
    replanner: Optional[Agent] = Field(default=None)

    def build_graph(self) -> BaseGraph:
        """Build graph using AgentNodeV3 for each agent."""
        # Minimal shared state or agent-specific states
        graph = BaseGraph()

        # Get agents list (from agents field or P&E fields)
        agent_list = self._get_agent_list()

        # Add each agent with AgentNodeV3
        for agent in agent_list:
            node = create_agent_node_v3(
                agent_name=agent.name,
                agent=agent,
                project_state=True,  # Key: project to agent's schema
            )
            graph.add_node(node)

        # Build edges based on mode
        self._build_edges(graph, agent_list)

        return graph.compile()

    def _get_agent_list(self) -> List[Agent]:
        """Get agents from either agents field or P&E fields."""
        if self.agents:
            return self.agents
        elif self.planner and self.executor:
            agents = [self.planner, self.executor]
            if self.replanner:
                agents.append(self.replanner)
            return agents
        else:
            raise ValueError("No agents configured")
```

## 📝 Key Principles Going Forward

1. **NO MORE VERSIONS** - Stop creating new implementations
2. **Use what exists** - AgentNodeV3, private state passing
3. **Keep it simple** - Sequential first, add complexity later
4. **Type safety** - Don't flatten schemas
5. **Clean up** - Delete or archive old implementations

## 🚀 Action Items

1. Pick ONE implementation to fix
2. Delete or archive the rest
3. Use AgentNodeV3 properly
4. Test with ReactAgent → SimpleAgent
5. Document the final approach

## 🎯 The Winner Should Be:

**Create a NEW, SIMPLE implementation** that:

- Uses Pydantic fields properly
- Leverages AgentNodeV3
- Supports private state passing
- Has minimal complexity
- Works with Plan & Execute pattern

**NOT** any of the existing 8+ implementations!
