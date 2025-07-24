# New Multi-Agent System Design Plan

**Version**: 1.0
**Purpose**: Comprehensive plan for building a new multi-agent system using enhanced base agent
**Last Updated**: 2025-01-23

## 🎯 Design Goals

### Core Objectives

1. **Enhanced Base Agent Integration**: Use the improved base agent with all mixins
2. **MultiAgentState Integration**: Leverage hierarchical state management
3. **Simple Agent Lists**: Define agents as lists with optional build modes
4. **Conditional Edges**: Support branches and conditional execution paths
5. **Modern Architecture**: Clean, type-safe, and extensible design

### Key Features

- Sequential execution with conditional branching
- Parallel execution capabilities
- Dynamic agent composition
- Rich debugging and visualization
- Graph compilation and execution
- State management with projection
- Tool and engine synchronization

## 🏗️ Architecture Design

### Class Hierarchy

```
MultiAgent (Base)
├── Enhanced base agent integration
├── MultiAgentState management
├── Graph compilation and execution
├── Agent list processing
└── Build mode handling

SequentialMultiAgent (MultiAgent)
├── Sequential execution logic
├── Conditional edge support
├── Branch condition evaluation
└── State passing between agents

ParallelMultiAgent (MultiAgent) [Future]
├── Parallel execution logic
├── Result aggregation
└── Synchronization handling

ConditionalMultiAgent (MultiAgent) [Future]
├── Complex branching logic
├── Decision tree execution
└── Dynamic path selection
```

### State Management

```
MultiAgentState
├── agents: Dict[str, Agent] (from list conversion)
├── agent_states: Dict[str, Dict] (isolated states)
├── execution_graph: CompiledGraph (LangGraph)
├── build_mode: str (auto, manual, lazy)
├── conditional_edges: List[ConditionalEdge]
└── execution_results: Dict[str, Any]
```

## 📋 Implementation Plan

### Phase 1: Base MultiAgent Class

```python
class MultiAgent(Agent):
    """Base multi-agent coordinator using enhanced base agent."""

    # Agent management
    agents: List[Agent] = Field(default_factory=list)
    build_mode: Literal["auto", "manual", "lazy"] = Field(default="auto")

    # Graph management
    execution_graph: CompiledGraph | None = Field(default=None)
    state_schema: Type[MultiAgentState] = Field(default=MultiAgentState)

    # Execution tracking
    execution_mode: str = Field(default="sequential")
    conditional_edges: List[ConditionalEdge] = Field(default_factory=list)

    # Rich debugging
    debug_mode: bool = Field(default=False)
    visualization_enabled: bool = Field(default=True)
```

### Phase 2: Sequential Implementation

```python
class SequentialMultiAgent(MultiAgent):
    """Sequential multi-agent with conditional branching."""

    execution_mode: str = Field(default="sequential", frozen=True)

    # Sequential-specific options
    stop_on_error: bool = Field(default=False)
    state_passing: bool = Field(default=True)
    enable_branches: bool = Field(default=True)

    def add_conditional_edge(
        self,
        from_agent: str,
        condition: Callable,
        true_agent: str,
        false_agent: str | None = None
    ):
        """Add conditional edge between agents."""

    def build_sequential_graph(self) -> CompiledGraph:
        """Build LangGraph for sequential execution."""
```

### Phase 3: Integration Components

```python
@dataclass
class ConditionalEdge:
    """Configuration for conditional execution paths."""
    from_agent: str
    condition: Callable[[MultiAgentState], bool]
    true_path: str
    false_path: str | None = None
    condition_name: str = "unnamed_condition"

class BuildMode:
    """Build mode configurations."""
    AUTO = "auto"      # Build graph automatically on first run
    MANUAL = "manual"  # Require explicit build() call
    LAZY = "lazy"      # Build only when needed
```

## 🚀 Usage Examples

### Example 1: Simple Sequential Workflow

```python
from haive.agents.simple.agent import SimpleAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.multi.sequential import SequentialMultiAgent
from haive.core.engine.aug_llm import AugLLMConfig

# Create individual agents
planner = ReactAgent(
    name="planner",
    engine=AugLLMConfig(temperature=0.3),
    tools=["web_search", "calculator"],
    structured_output_model=PlanSchema
)

analyzer = SimpleAgent(
    name="analyzer",
    engine=AugLLMConfig(temperature=0.1),
    structured_output_model=AnalysisSchema
)

writer = SimpleAgent(
    name="writer",
    engine=AugLLMConfig(temperature=0.8),
    structured_output_model=ReportSchema
)

# Create sequential multi-agent
workflow = SequentialMultiAgent(
    name="research_workflow",
    agents=[planner, analyzer, writer],
    build_mode="auto",
    debug_mode=True
)

# Execute workflow
result = await workflow.arun({
    "task": "Research and write a report on AI trends",
    "requirements": ["detailed analysis", "executive summary"]
})

print(f"Final report: {result.report}")
```

### Example 2: Conditional Branching

```python
# Create agents for different paths
simple_task_agent = SimpleAgent(
    name="simple_processor",
    engine=AugLLMConfig(),
    structured_output_model=SimpleResultSchema
)

complex_task_agent = ReactAgent(
    name="complex_processor",
    engine=AugLLMConfig(),
    tools=["research_tool", "analysis_tool"],
    structured_output_model=ComplexResultSchema
)

reviewer = SimpleAgent(
    name="reviewer",
    engine=AugLLMConfig(),
    structured_output_model=ReviewSchema
)

# Create conditional workflow
def task_complexity_condition(state: MultiAgentState) -> bool:
    """Determine if task is complex based on classifier output."""
    return state.task_classification.complexity_score > 0.7

workflow = SequentialMultiAgent(
    name="adaptive_workflow",
    agents=[simple_task_agent, complex_task_agent, reviewer],
    build_mode="manual"
)

# Add conditional branching
workflow.add_conditional_edge(
    from_agent="classifier",
    condition=task_complexity_condition,
    true_agent="complex_processor",
    false_agent="simple_processor"
)

# Both paths converge to reviewer
workflow.add_edge("simple_processor", "reviewer")
workflow.add_edge("complex_processor", "reviewer")

# Build and execute
workflow.build()
result = await workflow.arun({"task": "Analyze market trends"})
```

### Example 3: ReactAgent → SimpleAgent Pattern

```python
# The key pattern mentioned by user
react_reasoning_agent = ReactAgent(
    name="reasoner",
    engine=AugLLMConfig(temperature=0.7),
    tools=["calculator", "web_search", "file_reader"],
    # No structured output - uses messages/reasoning
)

simple_formatter_agent = SimpleAgent(
    name="formatter",
    engine=AugLLMConfig(temperature=0.1),
    structured_output_model=FinalOutputSchema,
    # Reads reasoning from previous agent's output
)

# Sequential workflow
reasoning_workflow = SequentialMultiAgent(
    name="react_to_simple_workflow",
    agents=[react_reasoning_agent, simple_formatter_agent],
    state_passing=True,  # Pass state between agents
    debug_mode=True
)

# Execute with reasoning → formatting
result = await reasoning_workflow.arun({
    "query": "Calculate compound interest and format as financial report",
    "principal": 10000,
    "rate": 0.05,
    "years": 10
})

# Result contains structured output from SimpleAgent
print(f"Formatted report: {result.financial_report}")
print(f"Reasoning used: {result.reasoning_trace}")
```

### Example 4: Advanced Multi-Path Workflow

```python
# Create specialized agents
classifier = SimpleAgent(
    name="classifier",
    engine=AugLLMConfig(),
    structured_output_model=TaskClassificationSchema
)

research_agent = ReactAgent(
    name="researcher",
    engine=AugLLMConfig(),
    tools=["web_search", "document_reader"],
    structured_output_model=ResearchSchema
)

calculation_agent = ReactAgent(
    name="calculator",
    engine=AugLLMConfig(),
    tools=["calculator", "data_analysis"],
    structured_output_model=CalculationSchema
)

creative_agent = SimpleAgent(
    name="creative_writer",
    engine=AugLLMConfig(temperature=0.9),
    structured_output_model=CreativeOutputSchema
)

synthesizer = SimpleAgent(
    name="synthesizer",
    engine=AugLLMConfig(temperature=0.3),
    structured_output_model=FinalSynthesisSchema
)

# Multi-path workflow
workflow = SequentialMultiAgent(
    name="intelligent_routing_workflow",
    agents=[classifier, research_agent, calculation_agent, creative_agent, synthesizer],
    build_mode="manual",
    debug_mode=True
)

# Define routing conditions
def needs_research(state: MultiAgentState) -> bool:
    return "research" in state.task_classification.required_capabilities

def needs_calculation(state: MultiAgentState) -> bool:
    return "math" in state.task_classification.required_capabilities

def needs_creativity(state: MultiAgentState) -> bool:
    return "creative" in state.task_classification.required_capabilities

# Add conditional routing
workflow.add_conditional_edge("classifier", needs_research, "researcher", "synthesizer")
workflow.add_conditional_edge("classifier", needs_calculation, "calculator", "synthesizer")
workflow.add_conditional_edge("classifier", needs_creativity, "creative_writer", "synthesizer")

# All paths converge to synthesizer
workflow.add_edge("researcher", "synthesizer")
workflow.add_edge("calculator", "synthesizer")
workflow.add_edge("creative_writer", "synthesizer")

# Build and execute
workflow.build()
result = await workflow.arun({
    "task": "Create a business plan with market research and financial projections"
})
```

## 🛠️ Technical Implementation Details

### Agent List Processing

```python
def _process_agent_list(self, agents: List[Agent]) -> Dict[str, Agent]:
    """Convert agent list to dict and validate."""
    agent_dict = {}
    for agent in agents:
        if not hasattr(agent, 'name') or not agent.name:
            raise ValueError(f"Agent {agent} must have a name")

        if agent.name in agent_dict:
            raise ValueError(f"Duplicate agent name: {agent.name}")

        agent_dict[agent.name] = agent

    return agent_dict
```

### Build Mode Implementation

```python
def _handle_build_mode(self):
    """Handle different build modes."""
    if self.build_mode == "auto":
        if not self.execution_graph:
            self.build()
    elif self.build_mode == "manual":
        if not self.execution_graph:
            raise RuntimeError("Graph not built. Call build() first.")
    elif self.build_mode == "lazy":
        if not self.execution_graph:
            self.build()  # Build on first access
```

### State Schema Generation

```python
def _create_dynamic_state_schema(self) -> Type[MultiAgentState]:
    """Create state schema with agent-specific fields."""

    # Start with base MultiAgentState
    base_fields = MultiAgentState.model_fields.copy()

    # Add agent-specific fields from structured output
    for agent_name, agent in self.agents.items():
        if hasattr(agent, 'structured_output_model') and agent.structured_output_model:
            model_fields = agent.structured_output_model.model_fields
            for field_name, field_info in model_fields.items():
                # Add with agent prefix to avoid conflicts
                prefixed_name = f"{agent_name}_{field_name}"
                base_fields[prefixed_name] = field_info

    # Create dynamic state class
    return create_model(
        f"{self.name}State",
        **base_fields,
        __base__=MultiAgentState
    )
```

### Graph Compilation

```python
def build(self) -> CompiledGraph:
    """Build LangGraph from agent configuration."""
    from langgraph.graph import StateGraph

    # Create graph with dynamic state schema
    state_schema = self._create_dynamic_state_schema()
    graph = StateGraph(state_schema)

    # Add agent nodes
    for agent_name, agent in self.agents.items():
        node_func = self._create_agent_node(agent_name, agent)
        graph.add_node(agent_name, node_func)

    # Add edges (sequential by default)
    self._add_edges_to_graph(graph)

    # Add conditional edges
    self._add_conditional_edges_to_graph(graph)

    # Compile graph
    self.execution_graph = graph.compile()
    return self.execution_graph
```

## 🧪 Testing Strategy

### Unit Tests

```python
def test_sequential_multi_agent_creation():
    """Test basic sequential multi-agent creation."""
    agents = [
        SimpleAgent(name="agent1", engine=AugLLMConfig()),
        SimpleAgent(name="agent2", engine=AugLLMConfig())
    ]

    workflow = SequentialMultiAgent(
        name="test_workflow",
        agents=agents
    )

    assert len(workflow.agents) == 2
    assert "agent1" in workflow.agents
    assert "agent2" in workflow.agents

def test_conditional_edge_addition():
    """Test adding conditional edges."""
    workflow = SequentialMultiAgent(name="test", agents=[])

    def test_condition(state):
        return True

    workflow.add_conditional_edge(
        from_agent="agent1",
        condition=test_condition,
        true_agent="agent2",
        false_agent="agent3"
    )

    assert len(workflow.conditional_edges) == 1
```

### Integration Tests

```python
@pytest.mark.asyncio
async def test_react_to_simple_workflow():
    """Test ReactAgent → SimpleAgent pattern."""

    # Create real agents
    react_agent = ReactAgent(
        name="reasoner",
        engine=AugLLMConfig(temperature=0.1),
        tools=["calculator"]
    )

    simple_agent = SimpleAgent(
        name="formatter",
        engine=AugLLMConfig(temperature=0.1),
        structured_output_model=TestOutputSchema
    )

    # Create workflow
    workflow = SequentialMultiAgent(
        name="react_simple_test",
        agents=[react_agent, simple_agent]
    )

    # Execute with real LLMs
    result = await workflow.arun({
        "query": "Calculate 15 * 23 and format the result"
    })

    # Verify structured output
    assert hasattr(result, 'calculation_result')
    assert "345" in str(result.calculation_result)
```

## 📊 File Structure

```
packages/haive-agents/src/haive/agents/multi/
├── __init__.py
├── base_multi_agent.py          # Base MultiAgent class
├── sequential_multi_agent.py    # Sequential implementation
├── conditional_edge.py          # Conditional edge utilities
├── build_modes.py              # Build mode configurations
└── examples/
    ├── simple_sequential.py     # Basic sequential example
    ├── react_to_simple.py      # ReactAgent → SimpleAgent
    ├── conditional_workflow.py  # Branching example
    └── advanced_routing.py     # Multi-path workflow

packages/haive-agents/tests/multi/
├── test_base_multi_agent.py
├── test_sequential_multi_agent.py
├── test_conditional_edges.py
└── test_integration_workflows.py
```

## 🎯 Success Criteria

### Must Have

1. ✅ Enhanced base agent integration
2. ✅ MultiAgentState compatibility
3. ✅ Agent list → dict conversion
4. ✅ Sequential execution with state passing
5. ✅ Basic conditional edges
6. ✅ Graph compilation and execution
7. ✅ ReactAgent → SimpleAgent pattern support

### Should Have

1. Rich debugging and visualization
2. Multiple build modes (auto, manual, lazy)
3. Error handling and recovery
4. Performance monitoring
5. State projection and isolation
6. Tool synchronization

### Could Have

1. Parallel execution capabilities
2. Complex branching logic
3. Dynamic agent composition
4. Advanced visualization
5. Performance optimization
6. Caching and memoization

## 🚀 Implementation Order

1. **Phase 1**: Base MultiAgent class with enhanced agent integration
2. **Phase 2**: SequentialMultiAgent with basic execution
3. **Phase 3**: Conditional edge system and branching
4. **Phase 4**: Build modes and graph compilation
5. **Phase 5**: Rich debugging and visualization
6. **Phase 6**: Testing and examples
7. **Phase 7**: Documentation and optimization

---

This plan provides a comprehensive roadmap for building a modern, flexible multi-agent system that leverages all the enhanced capabilities while maintaining simplicity and usability. Ready to start implementation?
