# Multi-Agent Systems Guide - Haive Framework

**Version**: 1.0
**Purpose**: Comprehensive guide for building multi-agent systems in Haive
**Last Updated**: 2025-01-18

## 🎯 Overview

This guide covers everything you need to know about building sophisticated multi-agent systems in Haive. We'll explore the architecture, provide practical examples, and demonstrate advanced patterns like Self-Discover workflows.

## 🏗️ Architecture

### Core Components

```
MultiAgentState (Container)
├── agents: Dict[str, Agent]           # Agent instances
├── agent_states: Dict[str, Dict]      # Isolated agent states
├── messages: List[BaseMessage]        # Shared conversation
├── tools: List[Tool]                  # Shared tools
├── engines: Dict[str, Engine]         # Shared engines
└── [dynamic fields from agents]       # Direct field updates
```

### Key Features

1. **🏗️ Hierarchical State Management** - No schema flattening
2. **🔄 Direct Field Updates** - Agents update container fields directly
3. **🧠 Self-Discover Workflows** - Sequential agents reading each other's outputs
4. **⚡ Type Safety** - Full validation throughout execution

## 📚 Documentation Structure

### Core Concepts

- **[Architecture Overview](architecture.md)** - System design and patterns
- **[State Management](state_management.md)** - Container and projection patterns
- **[Direct Field Updates](direct_field_updates.md)** - How agents communicate

### Implementation Guides

- **[Quick Start](quick_start.md)** - Basic setup and first workflows
- **[Sequential Workflows](sequential_workflows.md)** - Step-by-step agent execution
- **[Parallel Processing](parallel_processing.md)** - Concurrent agent execution
- **[Self-Discover Patterns](self_discover.md)** - Advanced reasoning workflows

### Advanced Topics

- **[Dynamic Composition](dynamic_composition.md)** - Runtime agent addition
- **[Error Handling](error_handling.md)** - Robust workflow management
- **[Performance Optimization](performance.md)** - Scale and efficiency
- **[Integration Patterns](integration.md)** - FastAPI, Streamlit, etc.

### Examples

- **[Basic Examples](examples/basic/)** - Simple multi-agent workflows
- **[Self-Discover Examples](examples/self_discover/)** - Reasoning workflows
- **[Integration Examples](examples/integration/)** - Real-world applications

## 🚀 Quick Start

### Basic Multi-Agent Setup

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
result2 = exec_node(state, config)  # Reads planning fields directly
```

## 🎯 Core Patterns

### 1. Direct Field Updates

```python
# Traditional approach (complex)
plan = state.agent_outputs["planner"]["plan"]

# Haive approach (direct)
plan = state.plan  # Direct field access
```

### 2. Self-Discover Workflows

```python
# Sequential execution with direct field access
selector_node = create_agent_node_v3("selector")
adapter_node = create_agent_node_v3("adapter")
reasoner_node = create_agent_node_v3("reasoner")

result1 = selector_node(state, config)  # Updates: selected_modules, rationale
result2 = adapter_node(state, config)   # Reads: selected_modules, Updates: adapted_modules
result3 = reasoner_node(state, config)  # Reads: adapted_modules, Updates: reasoning_structure
```

### 3. LangGraph Integration

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

# Compile and execute
app = graph.compile()
final_state = app.invoke(state)
```

## 🔧 Working Examples

### Example 1: Content Analysis Pipeline

```python
from typing import List
from pydantic import BaseModel, Field

# Define structured outputs
class ContentAnalysis(BaseModel):
    clarity_score: float = Field(ge=0.0, le=10.0)
    engagement_score: float = Field(ge=0.0, le=10.0)
    key_themes: List[str]
    improvements: List[str]

class ContentSummary(BaseModel):
    summary: str
    word_count: int
    readability_level: str

# Create agents
analyzer = SimpleAgent(
    name="analyzer",
    engine=AugLLMConfig(),
    structured_output_model=ContentAnalysis
)

summarizer = SimpleAgent(
    name="summarizer",
    engine=AugLLMConfig(),
    structured_output_model=ContentSummary
)

# Custom state schema
class ContentPipelineState(MultiAgentState):
    # Input
    content: str = ""

    # Analyzer outputs
    clarity_score: float = 0.0
    engagement_score: float = 0.0
    key_themes: List[str] = Field(default_factory=list)
    improvements: List[str] = Field(default_factory=list)

    # Summarizer outputs
    summary: str = ""
    word_count: int = 0
    readability_level: str = ""

# Execute pipeline
state = ContentPipelineState(
    agents=[analyzer, summarizer],
    content="Your content here..."
)

# Sequential execution
analyzer_node = create_agent_node_v3("analyzer")
summarizer_node = create_agent_node_v3("summarizer")

result1 = analyzer_node(state, config)  # Updates analysis fields
result2 = summarizer_node(state, config)  # Updates summary fields

# Access results directly
print(f"Clarity Score: {state.clarity_score}")
print(f"Summary: {state.summary}")
```

### Example 2: Self-Discover Research Workflow

```python
class ResearchState(MultiAgentState):
    # Input
    research_question: str = ""
    available_sources: List[str] = Field(default_factory=list)

    # Research planner outputs
    research_plan: List[str] = Field(default_factory=list)
    key_concepts: List[str] = Field(default_factory=list)

    # Information gatherer outputs
    gathered_info: List[Dict[str, Any]] = Field(default_factory=list)
    source_credibility: Dict[str, float] = Field(default_factory=dict)

    # Synthesizer outputs
    synthesis: str = ""
    conclusions: List[str] = Field(default_factory=list)
    confidence_level: float = 0.0

# Create specialized agents
research_planner = SimpleAgent(
    name="research_planner",
    engine=AugLLMConfig(),
    structured_output_model=ResearchPlan
)

info_gatherer = SimpleAgent(
    name="info_gatherer",
    engine=AugLLMConfig(),
    structured_output_model=GatheredInfo
)

synthesizer = SimpleAgent(
    name="synthesizer",
    engine=AugLLMConfig(),
    structured_output_model=Synthesis
)

# Execute research workflow
state = ResearchState(
    agents=[research_planner, info_gatherer, synthesizer],
    research_question="How effective are renewable energy policies?",
    available_sources=["academic_papers", "government_reports", "industry_data"]
)

# Sequential Self-Discover execution
plan_node = create_agent_node_v3("research_planner")
gather_node = create_agent_node_v3("info_gatherer")
synthesize_node = create_agent_node_v3("synthesizer")

result1 = plan_node(state, config)     # Creates research plan
result2 = gather_node(state, config)   # Gathers info based on plan
result3 = synthesize_node(state, config)  # Synthesizes findings

# Final research output
print(f"Research Plan: {state.research_plan}")
print(f"Synthesis: {state.synthesis}")
print(f"Confidence: {state.confidence_level}")
```

## 🎯 Best Practices

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

## 🔗 Related Documentation

### Core Framework

- **[Agent Building Guide](../building_guide.md)** - General agent development
- **[Multi-Agent Architecture](../../active/architecture/multi_agent_meta_agent_memory_hub.md)** - Technical architecture
- **[Testing Philosophy](../../active/standards/testing/philosophy.md)** - No mocks approach

### Implementation Files

- **[MultiAgentState](../../../packages/haive-core/src/haive/core/schema/prebuilt/multi_agent_state.py)** - Container state schema
- **[AgentNodeV3](../../../packages/haive-core/src/haive/core/graph/node/agent_node_v3.py)** - Execution nodes
- **[Multi-Agent Systems Guide](../../../packages/haive-core/docs/multi_agent_systems.md)** - Complete technical guide

### Test Examples

- **[Self-Discover Test](../../../packages/haive-core/tests/node/test_self_discover_workflow.py)** - Working example
- **[Multi-Agent Tests](../../../packages/haive-core/tests/schema/test_multi_agent_state.py)** - Unit tests

## 🎯 Next Steps

1. **Read the [Quick Start](quick_start.md)** - Get your first multi-agent workflow running
2. **Try the [Self-Discover Examples](examples/self_discover/)** - Advanced reasoning patterns
3. **Explore [Integration Patterns](integration.md)** - Real-world applications
4. **Build your own** - Use the patterns to create custom workflows

---

**Note**: This guide is actively maintained and updated with new patterns and examples. All examples are tested with real components (no mocks).
