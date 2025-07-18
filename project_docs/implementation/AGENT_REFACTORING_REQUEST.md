# Agent Refactoring and Visualization Implementation Request

## Overview

Refactor agent classes in `haive-agents` to use modern agent architecture, implement comprehensive visualization capabilities, and create test cases that generate visual documentation assets for the docs.

## Current State Analysis

### Key Issues Identified

1. **Inconsistent Agent Classes**: Some agents use old `agent config` + `agent class` pattern vs newer unified approach
2. **Missing Visualizations**: Agents lack comprehensive graph visualization and state history tracking
3. **Documentation Assets**: Need automated generation of agent graphs, state traces, and execution outputs for docs
4. **Test Coverage**: Missing test cases in `haive-agents/tests/` that demonstrate agent capabilities
5. **API Differences**: `haive-agents/base/agent` vs `haive-core/engines/agent` have different methods but similar visualization/run capabilities

### File Locations to Examine

```
packages/haive-agents/src/haive/agents/
├── base/
│   ├── agent.py                    # Current base agent class
│   └── __init__.py
├── simple/
│   ├── agent.py                    # SimpleAgent implementation
│   └── example.py
├── react/
│   ├── agent.py                    # ReactAgent implementation
│   └── example.py
├── conversation/
│   ├── debate/agent.py             # DebateConversation agent
│   └── collaberative/agent.py      # CollaborativeConversation
├── rag/
│   ├── base/agent.py               # BaseRAGAgent
│   ├── adaptive_rag/agent.py       # AdaptiveRAGAgent
│   └── simple/agent.py             # SimpleRAGAgent
└── multi/
    └── agent.py                    # MultiAgent

packages/haive-core/src/haive/core/
├── engine/
│   └── agent.py                    # Core agent engine (different API)
└── graph/
    └── visualization.py            # Existing visualization utilities

packages/haive-agents/tests/
├── conftest.py                     # Shared test fixtures
└── (need to create comprehensive test structure)
```

## Requirements

### 1. Agent Architecture Refactoring

#### Primary Objectives

- [ ] Standardize all agents to use consistent API pattern
- [ ] Ensure all agents support visualization methods
- [ ] Implement state history tracking for all agent types
- [ ] Create unified base class with visualization capabilities

#### Specific Tasks

**Analyze Current Agent Patterns**:

```python
# Document current patterns found in:
# 1. haive-agents/base/agent.py
# 2. haive-core/engines/agent.py
# 3. Identify which agents use old vs new patterns
```

**Standardize Agent Interface**:

```python
class StandardAgentInterface:
    """Standard interface all agents should implement."""

    # Core execution methods
    async def arun(self, input_data: Any) -> Any: ...
    async def astream(self, input_data: Any) -> AsyncIterator[Any]: ...

    # Visualization methods
    def visualize_graph(self, output_path: str, format: str = "png") -> None: ...
    def get_execution_trace(self) -> Dict[str, Any]: ...
    def save_state_history(self, output_path: str) -> None: ...

    # State management
    def get_current_state(self) -> Dict[str, Any]: ...
    def load_state_history(self, file_path: str) -> None: ...
```

### 2. Visualization Implementation

#### Graph Visualization Requirements

- [ ] Generate graph images for all agent types showing:
  - State flow diagrams
  - Tool interaction graphs (for ReAct agents)
  - Multi-agent communication flows
  - RAG retrieval pipelines
  - Conversation turn structures

#### Output Requirements

```
docs/source/_static/agent_graphs/
├── simple_agent_graph.png
├── react_agent_graph.png
├── rag_agent_graph.png
├── debate_agent_graph.png
├── multi_agent_graph.png
└── {agent_name}_graph.png

docs/source/_static/agent_traces/
├── simple_agent_trace.json
├── react_agent_execution.json
├── rag_retrieval_trace.json
└── {agent_name}_state_history.json
```

#### Implementation Pattern

```python
class VisualizableAgent:
    """Mixin for agent visualization capabilities."""

    def visualize_graph(self,
                       output_path: str,
                       format: str = "png",
                       include_state: bool = True,
                       include_tools: bool = True) -> None:
        """Generate agent graph visualization.

        Args:
            output_path: Where to save the visualization
            format: Output format (png, svg, html)
            include_state: Whether to show state transitions
            include_tools: Whether to show tool interactions
        """
        pass

    def get_execution_trace(self) -> Dict[str, Any]:
        """Get detailed execution trace for documentation.

        Returns:
            Detailed trace including:
            - Input/output pairs
            - State transitions
            - Tool calls and results
            - Timing information
            - Token usage
        """
        pass

    def save_state_history(self, output_path: str) -> None:
        """Save complete state history for docs generation."""
        pass
```

### 3. Test Implementation

#### Test Structure to Create

```
packages/haive-agents/tests/
├── conftest.py                         # Shared fixtures
├── test_visualization/                 # Visualization tests
│   ├── test_graph_generation.py       # Graph generation tests
│   ├── test_state_tracking.py         # State history tests
│   └── test_trace_export.py           # Trace export tests
├── test_agents/                       # Agent-specific tests
│   ├── test_simple_agent.py           # SimpleAgent tests + viz
│   ├── test_react_agent.py            # ReactAgent tests + viz
│   ├── test_rag_agents.py             # RAG agent tests + viz
│   ├── test_conversation_agents.py    # Conversation agent tests + viz
│   └── test_multi_agent.py            # MultiAgent tests + viz
├── integration/                       # Integration tests
│   ├── test_agent_engine_integration.py
│   └── test_full_workflow_with_viz.py
└── fixtures/                          # Test data
    ├── sample_conversations.json
    ├── mock_tool_responses.json
    └── expected_graph_structures.json
```

#### Test Requirements

Each test should:

- [ ] **Test core functionality** of the agent
- [ ] **Generate visualization assets** during test execution
- [ ] **Save execution traces** for documentation
- [ ] **Validate graph structure** and content
- [ ] **Create example outputs** for docs

#### Example Test Pattern

```python
class TestSimpleAgentWithVisualization:
    """Test SimpleAgent with comprehensive visualization."""

    async def test_simple_agent_conversation_with_visualization(self):
        """Test agent conversation and generate docs assets."""
        # Arrange
        agent = SimpleAgent(name="doc_demo_agent")
        output_dir = Path("docs/source/_static/agent_graphs")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Act - Run agent with tracking
        response = await agent.arun("Explain quantum computing simply")

        # Generate visualization assets
        agent.visualize_graph(
            output_path=str(output_dir / "simple_agent_graph.png"),
            format="png"
        )

        # Save execution trace
        trace = agent.get_execution_trace()
        with open(output_dir / "simple_agent_trace.json", "w") as f:
            json.dump(trace, f, indent=2)

        # Assert
        assert response is not None
        assert (output_dir / "simple_agent_graph.png").exists()
        assert len(trace["steps"]) > 0
```

### 4. Documentation Integration

#### Sphinx Integration Requirements

- [ ] Create custom Sphinx directive for agent visualization
- [ ] Auto-generate agent gallery from test outputs
- [ ] Include execution traces in API documentation
- [ ] Create interactive agent examples

#### Custom Sphinx Directive

```python
# docs/source/_extensions/agent_viz.py
class AgentVisualizationDirective(SphinxDirective):
    """Directive to embed agent visualizations in docs."""

    def run(self):
        agent_name = self.arguments[0]

        # Include graph image
        graph_path = f"_static/agent_graphs/{agent_name}_graph.png"

        # Include execution trace
        trace_path = f"_static/agent_traces/{agent_name}_trace.json"

        # Generate documentation content
        return [
            # Graph image
            # Execution trace
            # Interactive example
        ]
```

#### Documentation Structure

```rst
.. agent-visualization:: simple_agent
   :show-graph: true
   :show-trace: true
   :show-example: true

.. agent-visualization:: react_agent
   :show-tools: true
   :show-reasoning: true
```

### 5. Implementation Steps

#### Phase 1: Analysis and Planning

1. **Audit current agent implementations**
   - Document API differences between `haive-agents/base/agent` and `haive-core/engines/agent`
   - Identify which agents use old vs new patterns
   - Create compatibility matrix

2. **Design unified interface**
   - Create standard agent base class with visualization
   - Design state tracking system
   - Plan graph generation architecture

#### Phase 2: Core Implementation

1. **Implement visualization base class**
   - Create `VisualizableAgent` mixin
   - Implement graph generation using existing `haive.core.graph.visualization`
   - Add state history tracking

2. **Refactor existing agents**
   - Update each agent to inherit from new base
   - Ensure API consistency
   - Add visualization capabilities

#### Phase 3: Testing and Documentation

1. **Create comprehensive test suite**
   - Implement test cases that generate visualization assets
   - Add integration tests for agent combinations
   - Create performance benchmarks

2. **Generate documentation assets**
   - Run tests to create all visualization files
   - Implement Sphinx directives
   - Create agent gallery and examples

### 6. Specific Agent Requirements

#### SimpleAgent

- **Graph**: Linear state flow with message processing
- **Trace**: Input → Processing → Output with token counts
- **Special Features**: Conversation memory visualization

#### ReactAgent

- **Graph**: Cyclic reasoning loop with tool interactions
- **Trace**: Thought → Action → Observation cycles
- **Special Features**: Tool usage patterns, reasoning chain

#### RAGAgent (all variants)

- **Graph**: Retrieval → Rerank → Generate pipeline
- **Trace**: Query → Documents → Context → Response
- **Special Features**: Document relevance scores, retrieval metrics

#### ConversationAgents (Debate, Collaborative, etc.)

- **Graph**: Multi-participant interaction flows
- **Trace**: Turn-by-turn conversation state
- **Special Features**: Participant roles, conversation phases

#### MultiAgent

- **Graph**: Agent coordination and communication
- **Trace**: Inter-agent message passing and state sharing
- **Special Features**: Coordination strategies, load balancing

### 7. Success Criteria

- [ ] All agents implement consistent visualization API
- [ ] Test suite generates complete set of documentation assets
- [ ] Sphinx documentation auto-includes agent visualizations
- [ ] Agent graphs accurately represent execution flow
- [ ] State traces provide debugging and learning value
- [ ] Performance impact of visualization is minimal
- [ ] Documentation is automatically updated when agents change

### 8. Reference Documentation

**Existing Code to Study**:

- `packages/haive-core/src/haive/core/graph/visualization.py` - Existing visualization utilities
- `packages/haive-agents/src/haive/agents/conversation/debate/agent.py` - Well-documented agent example
- `packages/haive-agents/src/haive/agents/rag/adaptive_rag/agent.py` - Complex agent with multiple strategies

**Visualization Libraries to Use**:

- `graphviz` - For static graph generation
- `mermaid` - For interactive diagrams in docs
- `plotly` - For interactive state visualizations
- `networkx` - For graph analysis and layout

**Documentation Tools Available**:

- `sphinx-gallery` - For executable examples
- `sphinxcontrib-mermaid` - For diagram integration
- `sphinx-design` - For enhanced UI components

## Deliverables

1. **Refactored Agent Classes**: All agents using consistent API with visualization
2. **Comprehensive Test Suite**: Tests that generate documentation assets
3. **Visualization Assets**: Complete set of agent graphs and traces
4. **Documentation Integration**: Automatic inclusion of visualizations in docs
5. **Implementation Guide**: Documentation for adding visualization to new agents

## Timeline Estimate

- **Phase 1 (Analysis)**: 2-3 days
- **Phase 2 (Implementation)**: 5-7 days
- **Phase 3 (Testing/Docs)**: 3-4 days
- **Total**: 10-14 days

This request provides a comprehensive plan for modernizing the agent architecture while creating rich documentation assets that will significantly improve the user experience and developer onboarding.
