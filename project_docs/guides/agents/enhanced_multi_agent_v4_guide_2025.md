# EnhancedMultiAgentV4 Guide - Haive Framework

**Date**: August 7, 2025  
**Version**: 1.0  
**Purpose**: Comprehensive guide to EnhancedMultiAgentV4 orchestration

## 🚀 Overview

EnhancedMultiAgentV4 is the state-of-the-art multi-agent orchestrator in Haive that enables:
- Sequential, parallel, and conditional agent execution
- Clean list-based initialization
- Dynamic agent composition
- Structured data flow between agents
- Full integration with enhanced agent architecture

## 📋 Quick Start

### Basic Sequential Workflow

```python
from haive.agents.multi.enhanced_multi_agent_v4 import EnhancedMultiAgentV4
from haive.agents.react.agent_v4 import ReactAgentV4
from haive.agents.simple.agent_v3 import SimpleAgentV3
from pydantic import BaseModel

# Define structured output
class AnalysisResult(BaseModel):
    summary: str
    key_points: list[str]
    confidence: float

# Create agents
analyzer = ReactAgentV4(
    name="analyzer",
    tools=[research_tool, calculator]
)

formatter = SimpleAgentV3(
    name="formatter",
    structured_output_model=AnalysisResult
)

# Create workflow - just pass a list!
workflow = EnhancedMultiAgentV4(
    name="analysis_workflow",
    agents=[analyzer, formatter],  # Simple list initialization
    execution_mode="sequential"
)

# Execute
result = await workflow.arun({
    "task": "Analyze market trends for AI in 2025"
})
# result.summary, result.key_points, result.confidence available!
```

## 🏗️ Architecture

### Class Hierarchy

```
Agent (base with enhanced features)
└── EnhancedMultiAgentV4
    ├── Implements build_graph()
    ├── Uses AgentNodeV3 for state projection
    └── Integrates all enhanced agent features
```

### Key Components

1. **MultiAgentState** - Container for all agent states
2. **AgentNodeV3** - Handles state projection to individual agents
3. **Execution Modes** - Different orchestration patterns
4. **Build Modes** - Control when graph is constructed

## 🎯 Execution Modes

### 1. Sequential Mode

Agents execute one after another in order.

```python
# Create sequential pipeline
pipeline = EnhancedMultiAgentV4(
    agents=[preprocessor, analyzer, postprocessor],
    execution_mode="sequential"
)

# Executes: preprocessor → analyzer → postprocessor
result = await pipeline.arun({"data": raw_data})
```

### 2. Parallel Mode

All agents execute simultaneously.

```python
# Create parallel analysis
parallel_analyzer = EnhancedMultiAgentV4(
    agents=[sentiment_agent, entity_agent, topic_agent],
    execution_mode="parallel"
)

# All three agents analyze concurrently
results = await parallel_analyzer.arun({"text": document})
```

### 3. Conditional Mode

Route to different agents based on conditions.

```python
# Create conditional workflow
router_workflow = EnhancedMultiAgentV4(
    agents=[classifier, simple_handler, complex_handler],
    execution_mode="conditional",
    build_mode="manual"  # Need to add edges manually
)

# Add conditional routing
router_workflow.add_conditional_edge(
    from_agent="classifier",
    condition=lambda state: state.get("complexity", 0) > 0.7,
    true_agent="complex_handler",
    false_agent="simple_handler"
)

router_workflow.build()
result = await router_workflow.arun({"query": user_input})
```

### 4. Manual Mode

Full control over edge configuration.

```python
# Create with manual mode
custom_workflow = EnhancedMultiAgentV4(
    agents=[agent1, agent2, agent3, agent4],
    execution_mode="manual"
)

# Add custom edges
custom_workflow.add_edge("agent1", "agent2")
custom_workflow.add_edge("agent1", "agent3")  # Parallel branch
custom_workflow.add_edge("agent2", "agent4")
custom_workflow.add_edge("agent3", "agent4")
custom_workflow.add_edge("agent4", END)

custom_workflow.build()
```

## 🔄 State Management

### MultiAgentState Structure

```python
class MultiAgentState(StateSchema):
    messages: List[BaseMessage] = []
    agent_states: Dict[str, Dict[str, Any]] = {}
    shared_tools: List[BaseTool] = []
    shared_engines: Dict[str, Any] = {}
```

### State Projection

Each agent receives its own view of the state:

```python
# In AgentNodeV3, state is projected:
agent_state = state.agent_states.get(agent_name, {})
# Agent sees only its state, not the full MultiAgentState
```

### Structured Output Updates

Agents with structured output directly update container fields:

```python
# If agent has structured_output_model
if hasattr(agent, 'structured_output_model'):
    # Output is added as a field to MultiAgentState
    setattr(state, agent_name, structured_output)
```

## 💡 Advanced Patterns

### 1. Multi-Way Conditional Routing

```python
# Create router workflow
support_router = EnhancedMultiAgentV4(
    agents=[
        classifier,
        billing_agent,
        technical_agent,
        general_agent,
        escalation_agent
    ],
    execution_mode="manual"
)

# Define routing function
def route_support(state):
    category = state.get("category", "general")
    urgency = state.get("urgency", 0)
    
    if urgency > 0.9:
        return "escalation"
    return category

# Add multi-way routing
support_router.add_multi_conditional_edge(
    from_agent="classifier",
    condition=route_support,
    routes={
        "billing": "billing_agent",
        "technical": "technical_agent",
        "general": "general_agent",
        "escalation": "escalation_agent"
    },
    default="general_agent"
)
```

### 2. Dynamic Agent Addition

```python
# Start with base workflow
workflow = EnhancedMultiAgentV4(
    agents=[initial_agent],
    execution_mode="sequential",
    build_mode="auto"  # Auto-rebuild on changes
)

# Dynamically add agents based on needs
if needs_validation:
    validator = SimpleAgentV3(name="validator")
    workflow.add_agent(validator)  # Graph rebuilds automatically

if needs_formatting:
    formatter = SimpleAgentV3(
        name="formatter",
        structured_output_model=OutputFormat
    )
    workflow.add_agent(formatter)
```

### 3. Nested Multi-Agent Workflows

```python
# Create sub-workflows
research_team = EnhancedMultiAgentV4(
    name="research_team",
    agents=[web_researcher, academic_researcher, data_analyst],
    execution_mode="parallel"
)

writing_team = EnhancedMultiAgentV4(
    name="writing_team",
    agents=[content_writer, editor, fact_checker],
    execution_mode="sequential"
)

# Create master workflow
master_workflow = EnhancedMultiAgentV4(
    name="content_pipeline",
    agents=[research_team, writing_team],
    execution_mode="sequential"
)
```

### 4. Feedback Loops

```python
# Create iterative improvement workflow
improvement_workflow = EnhancedMultiAgentV4(
    agents=[writer, critic, improver],
    execution_mode="manual"
)

# Add feedback loop
improvement_workflow.add_edge("writer", "critic")
improvement_workflow.add_edge("critic", "improver")
improvement_workflow.add_conditional_edge(
    from_agent="improver",
    condition=lambda state: state.get("quality_score", 0) < 0.8,
    true_agent="writer",  # Loop back if quality low
    false_agent=END      # Exit if quality good
)
```

## 🧪 Testing Patterns

### Basic Multi-Agent Test

```python
import pytest
from haive.agents.multi.enhanced_multi_agent_v4 import EnhancedMultiAgentV4
from haive.agents.simple.agent_v3 import SimpleAgentV3

@pytest.mark.asyncio
async def test_sequential_workflow():
    """Test sequential multi-agent execution."""
    # Create agents with real LLMs (no mocks!)
    agent1 = SimpleAgentV3(name="agent1", temperature=0.1)
    agent2 = SimpleAgentV3(name="agent2", temperature=0.1)
    
    # Create workflow
    workflow = EnhancedMultiAgentV4(
        agents=[agent1, agent2],
        execution_mode="sequential"
    )
    
    # Execute
    result = await workflow.arun({
        "task": "Process this sequentially"
    })
    
    # Verify execution
    assert result is not None
    assert workflow.state.agent_states["agent1"]
    assert workflow.state.agent_states["agent2"]
```

### Testing with Structured Output

```python
@pytest.mark.asyncio
async def test_structured_output_flow():
    """Test data flow with structured output."""
    # Define models
    class Analysis(BaseModel):
        score: float
        findings: list[str]
    
    class Report(BaseModel):
        summary: str
        recommendations: list[str]
    
    # Create agents
    analyzer = SimpleAgentV3(
        name="analyzer",
        structured_output_model=Analysis
    )
    reporter = SimpleAgentV3(
        name="reporter",
        structured_output_model=Report
    )
    
    # Create workflow
    workflow = EnhancedMultiAgentV4(
        agents=[analyzer, reporter],
        execution_mode="sequential"
    )
    
    # Execute
    result = await workflow.arun({"data": "Test data"})
    
    # Verify structured output
    assert hasattr(workflow.state, "analyzer")
    assert isinstance(workflow.state.analyzer, Analysis)
    assert hasattr(workflow.state, "reporter")
    assert isinstance(workflow.state.reporter, Report)
```

## 🛠️ Build Modes

### Auto Build (Default)

```python
# Graph builds immediately
workflow = EnhancedMultiAgentV4(
    agents=[agent1, agent2],
    build_mode="auto"  # Default
)
# Ready to use immediately
```

### Manual Build

```python
# Defer graph building
workflow = EnhancedMultiAgentV4(
    agents=[agent1, agent2],
    build_mode="manual"
)

# Configure edges
workflow.add_edge("agent1", "agent2")

# Build when ready
workflow.build()
```

### Lazy Build

```python
# Build on first execution
workflow = EnhancedMultiAgentV4(
    agents=[agent1, agent2],
    build_mode="lazy"
)

# Graph builds here automatically
result = await workflow.arun({"task": "First run"})
```

## 📊 Monitoring and Debugging

### Display Workflow Info

```python
# Get human-readable workflow info
info = workflow.display_info()
print(info)
# Shows:
# - Workflow name
# - Execution mode
# - Agent list with types
# - Build status
```

### Access Individual Agents

```python
# Get agent by name
agent = workflow.get_agent("analyzer")

# Get all agent names
names = workflow.get_agent_names()

# Check if agent exists
if "validator" in workflow.agents:
    validator = workflow.agents["validator"]
```

### Monitor Execution

```python
# Add hooks for monitoring
@workflow.before_node
def log_agent_start(context):
    print(f"Starting agent: {context.node_name}")

@workflow.after_node
def log_agent_complete(context):
    print(f"Completed agent: {context.node_name}")
    if hasattr(context.state, context.node_name):
        print(f"Output: {getattr(context.state, context.node_name)}")
```

## 🚀 Performance Considerations

1. **Parallel Execution**: Use parallel mode for independent agents
2. **Lazy Building**: Use lazy mode for dynamic workflows
3. **State Size**: Monitor agent_states size in long workflows
4. **Recompilation**: Minimize dynamic agent additions in tight loops

## 🎯 Best Practices

1. **Use Structured Output**: Enable clean data flow between agents
2. **Name Agents Clearly**: Descriptive names help debugging
3. **Start Simple**: Begin with sequential, add complexity as needed
4. **Test with Real LLMs**: Never use mocks, test actual behavior
5. **Monitor State**: Use hooks to track execution flow
6. **Handle Errors**: Add error handling agents for robustness

## 🚨 Common Pitfalls

1. **Duplicate Agent Names**
   ```python
   # ❌ WRONG
   agents = [
       SimpleAgentV3(name="agent"),
       SimpleAgentV3(name="agent")  # Duplicate!
   ]
   
   # ✅ CORRECT - Auto-renamed to agent_1
   # Or use unique names
   ```

2. **Forgetting to Build**
   ```python
   # ❌ WRONG
   workflow = EnhancedMultiAgentV4(
       agents=[...],
       build_mode="manual"
   )
   await workflow.arun(...)  # Error! Not built
   
   # ✅ CORRECT
   workflow.build()
   await workflow.arun(...)
   ```

3. **Mixing Execution Modes**
   ```python
   # ❌ WRONG
   workflow = EnhancedMultiAgentV4(
       execution_mode="sequential"
   )
   workflow.add_conditional_edge(...)  # Won't work!
   
   # ✅ CORRECT
   workflow = EnhancedMultiAgentV4(
       execution_mode="conditional"
   )
   ```

## 📅 What's New (August 2025)

- **Direct List Initialization**: Just pass `agents=[...]`
- **AgentNodeV3 Integration**: Proper state projection
- **Structured Output Fields**: Direct state field updates
- **Enhanced Base Integration**: All mixin features available
- **Dynamic Recompilation**: Auto-rebuild on changes
- **Multi-Way Routing**: Complex conditional patterns

## 🔗 Related Documentation

- [Enhanced Agents Guide](enhanced_agents_guide_2025.md)
- [SimpleAgentV3 Guide](enhanced_agents_guide_2025.md#simpleagentv3---the-workhorse)
- [ReactAgentV4 Guide](enhanced_agents_guide_2025.md#reactagentv4---reasoning-loops)
- [MultiAgentState](../../packages/haive-core/src/haive/core/schema/multi_agent_state.py)
- [AgentNodeV3](../../packages/haive-core/src/haive/core/engine/rate_limited_engine.py)

---

**Last Updated**: August 7, 2025  
**Framework Version**: haive-agents 0.2.0+