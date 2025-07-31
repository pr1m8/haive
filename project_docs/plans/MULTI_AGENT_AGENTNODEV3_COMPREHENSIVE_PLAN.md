# Comprehensive Multi-Agent Implementation Plan with AgentNodeV3

**Version**: 1.0  
**Date**: 2025-01-15  
**Purpose**: Complete plan for implementing multi-agent system using AgentNodeV3, state schemas, and hierarchical state management

## 📋 Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [AgentNodeV3 Understanding](#2-agentnodev3-understanding)
3. [State Schema Architecture](#3-state-schema-architecture)
4. [Multi-Agent Implementation Plan](#4-multi-agent-implementation-plan)
5. [Hierarchical State Management](#5-hierarchical-state-management)
6. [Reference Fields & State Projection](#6-reference-fields--state-projection)
7. [DO's and DON'Ts](#7-dos-and-donts)
8. [Test Plan (No Mocks)](#8-test-plan-no-mocks)
9. [Implementation Steps](#9-implementation-steps)

## 1. Core Concepts

### 1.1 What We're Building

A clean multi-agent system that:

- Uses **AgentNodeV3** for proper state projection
- Supports **hierarchical state** without schema flattening
- Enables **private state passing** between agents
- Maintains **type safety** for each agent's schema
- Works with **real LLMs** (no mocks)

### 1.2 Key Components

```
MultiAgent (Base Class)
├── SequentialAgent - Agents run in order
├── BranchingAgent - Conditional routing
├── ParallelAgent - Concurrent execution
└── Custom patterns via composition
```

## 2. AgentNodeV3 Understanding

### 2.1 What AgentNodeV3 Does

```python
# AgentNodeV3 provides:
# 1. State projection from container → agent schema
# 2. Private data passing between nodes
# 3. Hierarchical state updates
# 4. Recompilation tracking

node = create_agent_node_v3(
    agent_name="planner",          # Key in agents dict
    agent=planner_agent,           # Actual agent instance
    project_state=True,            # Project to agent's schema
    shared_fields=["messages"],    # Fields from container
    extract_from_container=True,   # If using container pattern
    update_container_state=True,   # Update back to container
)
```

### 2.2 State Flow Through AgentNodeV3

```
Container State → AgentNodeV3 → Agent Input State → Agent Execution → Agent Output State → Container Update
     (Any)         (Projects)      (Typed Schema)                        (Typed Output)      (Merged Back)
```

## 3. State Schema Architecture

### 3.1 Schema Hierarchy

```python
# Level 1: Overall Multi-Agent State (Minimal)
class MultiAgentState(TypedDict):
    current_agent: Optional[str]
    completed_agents: List[str]
    error: Optional[str]

# Level 2: Agent-Specific States (Typed)
class PlannerState(StateSchema):
    task: str
    plan: Plan
    confidence: float

class ExecutorState(StateSchema):
    plan: Plan
    current_step: str
    results: Dict[str, Any]

# Level 3: Private Transfer States
class PlannerOutput(BaseModel):
    plan: Plan
    reasoning: List[str]
    next_action: str

class ExecutorInput(BaseModel):
    plan: Plan
    previous_results: Optional[Dict[str, Any]]
```

### 3.2 State Composition Strategy

**DON'T**: Flatten all agent schemas into one
**DO**: Keep agent schemas separate, use projection

```python
# BAD - Schema flattening
class FlatMultiAgentState(StateSchema):
    # Mixing all agent fields - loses type safety
    planner_plan: Plan
    executor_results: Dict
    formatter_output: str

# GOOD - Hierarchical with projection
class MultiAgentContainer(StateSchema):
    agents: Dict[str, Agent]
    agent_states: Dict[str, Dict[str, Any]]  # Isolated states
    shared_context: Dict[str, Any]  # Only truly shared data
```

## 4. Multi-Agent Implementation Plan

### 4.1 Base MultiAgent Class

```python
from typing import List, Dict, Union, Optional, Any
from abc import abstractmethod
from pydantic import Field, field_validator, PrivateAttr
from haive.agents.base.agent import Agent
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.graph.node.agent_node_v3 import create_agent_node_v3

AgentOrList = Union[Agent, List[Agent]]

class MultiAgent(Agent):
    """Base multi-agent with hierarchical state management."""

    # Agents storage
    agents: Union[List[AgentOrList], Dict[str, AgentOrList]] = Field(...)

    # State management strategy
    state_strategy: Literal["minimal", "container", "custom"] = Field(default="minimal")

    # Shared fields that all agents can access
    shared_fields: List[str] = Field(default_factory=lambda: [])

    # Private state passing rules
    state_transfer_map: Dict[str, Dict[str, str]] = Field(
        default_factory=dict,
        description="Maps agent outputs to next agent inputs"
    )

    # Internal registries
    _agent_registry: Dict[str, Agent] = PrivateAttr(default_factory=dict)
    _agent_groups: Dict[str, List[str]] = PrivateAttr(default_factory=dict)

    def build_graph(self) -> BaseGraph:
        """Build graph with proper state management."""
        # Choose state schema based on strategy
        if self.state_strategy == "minimal":
            graph = BaseGraph(state_schema=MultiAgentState)
        elif self.state_strategy == "container":
            graph = BaseGraph(state_schema=MultiAgentContainer)
        else:
            graph = BaseGraph(state_schema=self.state_schema)

        # Add agents with AgentNodeV3
        self._add_agent_nodes(graph)

        # Build edges (subclass implements)
        self._build_edges(graph)

        return graph.compile()

    def _add_agent_nodes(self, graph: BaseGraph):
        """Add each agent as AgentNodeV3 with proper configuration."""
        for agent_name, agent in self._agent_registry.items():
            # Determine node configuration based on state strategy
            if self.state_strategy == "minimal":
                # Private state passing - no container
                node = create_agent_node_v3(
                    agent_name=agent_name,
                    agent=agent,
                    name=f"agent_{agent_name}",
                    extract_from_container=False,
                    project_state=True,
                    shared_fields=[],  # No shared fields in minimal
                )
            elif self.state_strategy == "container":
                # Container pattern with projection
                node = create_agent_node_v3(
                    agent_name=agent_name,
                    agent=agent,
                    name=f"agent_{agent_name}",
                    extract_from_container=True,
                    project_state=True,
                    shared_fields=self.shared_fields,
                    update_container_state=True,
                )

            graph.add_node(node)
```

### 4.2 SequentialAgent Implementation

```python
class SequentialAgent(MultiAgent):
    """Sequential execution with optional parallel groups."""

    def _build_edges(self, graph: BaseGraph):
        """Build sequential flow with group support."""
        sequence = self._get_execution_sequence()

        prev_node = START

        for item in sequence:
            if isinstance(item, list):
                # Parallel group
                group_id = f"group_{id(item)}"

                # Add aggregator
                graph.add_node(f"aggregate_{group_id}", self._create_aggregator(item))

                # Connect all in group to aggregator
                for agent_name in item:
                    graph.add_edge(prev_node, f"agent_{agent_name}")
                    graph.add_edge(f"agent_{agent_name}", f"aggregate_{group_id}")

                prev_node = f"aggregate_{group_id}"
            else:
                # Single agent
                graph.add_edge(prev_node, f"agent_{item}")
                prev_node = f"agent_{item}"

        graph.add_edge(prev_node, END)
```

### 4.3 BranchingAgent Implementation

```python
class BranchingAgent(MultiAgent):
    """Conditional routing between agents."""

    # Routing configuration
    routes: Dict[str, ConditionalRoute] = Field(default_factory=dict)

    def _build_edges(self, graph: BaseGraph):
        """Build conditional routing."""
        # Add conditional edges for each route
        for source, route in self.routes.items():
            graph.add_conditional_edges(
                f"agent_{source}",
                route.condition,
                {dest: f"agent_{dest}" for dest in route.destinations} |
                {END: END} if route.can_end else {}
            )
```

## 5. Hierarchical State Management

### 5.1 State Hierarchy Patterns

```python
# Pattern 1: Minimal Shared State
class MinimalMultiAgentState(TypedDict):
    """Only coordination metadata - agents pass private data."""
    current_agent: Optional[str]
    final_result: Optional[Any]

# Pattern 2: Container with Isolated States
class ContainerMultiAgentState(StateSchema):
    """Container pattern - each agent has isolated state."""
    agents: Dict[str, Agent]
    agent_states: Dict[str, Dict[str, Any]]
    shared_context: Dict[str, Any]

    def get_agent_state(self, agent_name: str) -> Dict[str, Any]:
        return self.agent_states.get(agent_name, {})

    def update_agent_state(self, agent_name: str, updates: Dict[str, Any]):
        self.agent_states[agent_name] = {
            **self.agent_states.get(agent_name, {}),
            **updates
        }

# Pattern 3: Reference Fields
class ReferenceMultiAgentState(StateSchema):
    """State with reference fields for cross-agent data."""
    agents: Dict[str, Agent]

    # Reference fields point to other agent outputs
    planner_output_ref: Optional[str] = Field(
        default=None,
        description="Reference to planner's output location"
    )

    def resolve_reference(self, ref: str) -> Any:
        """Resolve a reference to actual data."""
        # Implementation for reference resolution
        pass
```

### 5.2 State Projection Rules

```python
# AgentNodeV3 projection configuration
projection_rules = {
    "planner": {
        "shared_fields": ["task", "context"],
        "private_fields": ["plan", "reasoning"],
        "output_mapping": {
            "plan": "executor.input_plan",
            "reasoning": "analyzer.reasoning_context"
        }
    },
    "executor": {
        "shared_fields": ["context"],
        "input_mapping": {
            "input_plan": "plan",  # Maps from planner output
        }
    }
}
```

## 6. Reference Fields & State Projection

### 6.1 Reference Field Pattern

```python
class AgentStateWithReferences(StateSchema):
    """State that references other agent outputs."""

    # Direct data
    local_data: Dict[str, Any] = Field(default_factory=dict)

    # References to other agent data
    references: Dict[str, str] = Field(
        default_factory=dict,
        description="References to other agent outputs"
    )

    def add_reference(self, key: str, source_agent: str, source_field: str):
        """Add a reference to another agent's output."""
        self.references[key] = f"{source_agent}.{source_field}"

    def resolve_reference(self, key: str, container_state: Any) -> Any:
        """Resolve reference to actual data."""
        if key not in self.references:
            return None

        ref = self.references[key]
        agent_name, field = ref.split(".", 1)

        # Get from container state
        agent_state = container_state.agent_states.get(agent_name, {})
        return agent_state.get(field)
```

### 6.2 AgentNodeV3 Projection Configuration

```python
# Configure how AgentNodeV3 projects state
def configure_agent_projection(agent: Agent) -> Dict[str, Any]:
    """Configure state projection for an agent."""
    return {
        # Fields to extract from container
        "shared_fields": ["messages", "context"],

        # How to map container fields to agent input
        "field_mapping": {
            "shared_context.task": "task_description",
            "previous_agent_output": "input_data"
        },

        # What to include in agent's view
        "include_metadata": True,

        # How to update container after execution
        "update_strategy": "merge",  # or "replace"
    }
```

## 7. DO's and DON'Ts

### 7.1 DO's ✅

1. **DO use AgentNodeV3** for all agent nodes
2. **DO maintain type safety** with proper schemas
3. **DO use private state passing** for agent communication
4. **DO test with real LLMs** (no mocks)
5. **DO keep shared state minimal**
6. **DO use proper Pydantic patterns** (no `__init__`)
7. **DO leverage state projection** instead of flattening
8. **DO handle errors gracefully** with state updates

### 7.2 DON'Ts ❌

1. **DON'T flatten agent schemas** into one mega-schema
2. **DON'T use mocks** in tests
3. **DON'T override `__init__`** in Pydantic models
4. **DON'T share everything** - use private state passing
5. **DON'T create complex state hierarchies** - keep it simple
6. **DON'T bypass AgentNodeV3** projection
7. **DON'T mix agent-specific logic** in MultiAgent base
8. **DON'T forget recompilation tracking**

## 8. Test Plan (No Mocks)

### 8.1 Test Structure

```
tests/
├── test_multi_agent_base.py      # Base functionality
├── test_sequential_agent.py      # Sequential execution
├── test_branching_agent.py       # Conditional routing
├── test_state_projection.py      # AgentNodeV3 projection
├── test_hierarchical_state.py    # State management
└── integration/
    ├── test_react_simple_flow.py # Real agent integration
    ├── test_plan_execute.py      # P&E pattern
    └── test_complex_routing.py   # Complex flows
```

### 8.2 Base Test Cases

```python
import pytest
from haive.agents.simple import SimpleAgent
from haive.agents.react import ReactAgent
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage

class TestMultiAgentBase:
    """Test multi-agent base functionality with real components."""

    @pytest.fixture
    def planner_agent(self):
        """Create real planner agent."""
        return SimpleAgent(
            name="planner",
            engine=AugLLMConfig(
                system_message="You are a planning agent. Create step-by-step plans.",
                structured_output_model=Plan,
                structured_output_version="v2"
            )
        )

    @pytest.fixture
    def executor_agent(self):
        """Create real executor agent."""
        return ReactAgent(
            name="executor",
            engine=AugLLMConfig(
                system_message="You are an execution agent. Execute the given plan.",
                tools=[...]  # Real tools
            )
        )

    async def test_sequential_execution_real_llm(self, planner_agent, executor_agent):
        """Test sequential execution with real LLMs."""
        # Create sequential multi-agent
        multi = SequentialAgent(agents=[planner_agent, executor_agent])

        # Execute with real input
        result = await multi.ainvoke({
            "task": "Create a plan for learning Python"
        })

        # Verify real execution
        assert result is not None
        assert "final_result" in result

        # Verify both agents executed
        assert result.get("completed_agents") == ["planner", "executor"]

    async def test_state_projection_maintains_types(self):
        """Test that AgentNodeV3 maintains type safety."""
        # Create agents with specific schemas
        agent1 = SimpleAgent(
            name="agent1",
            engine=AugLLMConfig(),
            state_schema=Agent1State  # Custom typed state
        )

        agent2 = SimpleAgent(
            name="agent2",
            engine=AugLLMConfig(),
            state_schema=Agent2State  # Different typed state
        )

        multi = SequentialAgent(agents=[agent1, agent2])

        # Each agent should receive its typed state
        # Verify through execution
        result = await multi.ainvoke({"input": "test"})

        # Check internal state tracking
        # Agent states should maintain their schemas
```

### 8.3 Integration Tests

```python
class TestReactSimpleIntegration:
    """Test ReactAgent → SimpleAgent flow with real execution."""

    async def test_react_simple_sequential_flow(self):
        """Test reasoning → formatting flow."""
        # Create agents
        react = ReactAgent(
            name="reasoner",
            engine=AugLLMConfig(
                system_message="Analyze and reason about the task"
            ),
            tools=[WebSearchTool(), CalculatorTool()]
        )

        simple = SimpleAgent(
            name="formatter",
            engine=AugLLMConfig(
                system_message="Format the reasoning into a report",
                structured_output_model=FormattedReport
            )
        )

        # Create sequential flow
        multi = SequentialAgent(
            agents=[react, simple],
            state_strategy="minimal"  # Use private state passing
        )

        # Execute
        result = await multi.ainvoke({
            "task": "Research the latest AI developments"
        })

        # Verify flow
        assert isinstance(result["final_result"], FormattedReport)
        assert result["completed_agents"] == ["reasoner", "formatter"]

    async def test_private_state_passing(self):
        """Test private data flows between agents."""
        # Create agents that pass private data
        analyzer = SimpleAgent(
            name="analyzer",
            engine=AugLLMConfig(),
            output_schema=AnalysisOutput  # Typed output
        )

        synthesizer = SimpleAgent(
            name="synthesizer",
            engine=AugLLMConfig(),
            input_schema=AnalysisOutput  # Expects analyzer's output
        )

        multi = SequentialAgent(agents=[analyzer, synthesizer])

        # The output of analyzer should flow to synthesizer
        result = await multi.ainvoke({"data": "analyze this"})

        # Verify private state passed correctly
        assert result["completed_agents"] == ["analyzer", "synthesizer"]
```

### 8.4 Error Handling Tests

```python
async def test_agent_error_handling():
    """Test error handling in multi-agent flow."""
    # Create agent that might fail
    faulty_agent = SimpleAgent(
        name="faulty",
        engine=AugLLMConfig(max_tokens=1)  # Too small, might fail
    )

    recovery_agent = SimpleAgent(
        name="recovery",
        engine=AugLLMConfig()
    )

    # Create branching flow with error handling
    multi = BranchingAgent(
        agents=[faulty_agent, recovery_agent],
        routes={
            "faulty": ConditionalRoute(
                condition=lambda s: "recovery" if s.get("error") else END,
                destinations=["recovery", END]
            )
        }
    )

    result = await multi.ainvoke({"input": "test"})

    # Should handle error gracefully
    assert "error" not in result or result["completed_agents"][-1] == "recovery"
```

## 9. Implementation Steps

### 9.1 Phase 1: Core Infrastructure (Week 1)

1. **Clean up existing implementations**
   - Archive old multi-agent files
   - Keep only the new clean design

2. **Implement base MultiAgent class**
   - Proper state management options
   - AgentNodeV3 integration
   - State projection setup

3. **Implement SequentialAgent**
   - Basic sequential flow
   - Parallel group support
   - Test with real agents

### 9.2 Phase 2: Advanced Patterns (Week 2)

4. **Implement BranchingAgent**
   - Conditional routing
   - Error handling branches
   - Complex flow support

5. **Add state management strategies**
   - Minimal state
   - Container pattern
   - Reference fields

6. **Create test suite**
   - Unit tests (real LLMs)
   - Integration tests
   - Error scenarios

### 9.3 Phase 3: Production Ready (Week 3)

7. **Performance optimization**
   - State projection efficiency
   - Parallel execution tuning
   - Memory management

8. **Documentation**
   - API documentation
   - Usage examples
   - Best practices guide

9. **Real-world examples**
   - Plan & Execute implementation
   - Research pipeline
   - Multi-stage analysis

### 9.4 Testing Checklist

- [ ] All tests use real LLMs (no mocks)
- [ ] State projection maintains type safety
- [ ] Private state passing works correctly
- [ ] Error handling is robust
- [ ] Performance is acceptable
- [ ] Memory usage is reasonable
- [ ] Recompilation tracking works
- [ ] Complex flows execute correctly

## 10. Success Criteria

1. **Clean Architecture**: Single, well-designed multi-agent system
2. **Type Safety**: Each agent maintains its typed schema
3. **Real Testing**: 100% real component testing (no mocks)
4. **Performance**: <100ms overhead for multi-agent coordination
5. **Usability**: <10 lines to create common patterns
6. **Reliability**: Graceful error handling and recovery

---

**Remember**: Keep it simple, use AgentNodeV3 properly, maintain type safety, and test with real components!
