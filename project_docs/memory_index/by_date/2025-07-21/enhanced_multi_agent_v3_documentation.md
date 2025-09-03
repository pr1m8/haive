# Enhanced MultiAgent V3 - Complete Documentation

**Version**: 1.0
**Created**: 2025-07-21
**Status**: Production Ready
**Author**: Claude Code Session

## 🎯 Overview

Enhanced MultiAgent V3 is the most advanced multi-agent coordination system in Haive, combining production stability with cutting-edge features. It follows the V3 pattern established by SimpleAgent V3 and ReactAgent V3, providing type-safe, performance-optimized, and highly observable multi-agent workflows.

## 📚 Table of Contents

1. [Core Concepts](#core-concepts)
2. [Architecture](#architecture)
3. [Installation & Setup](#installation--setup)
4. [Quick Start](#quick-start)
5. [Execution Patterns](#execution-patterns)
6. [Advanced Features](#advanced-features)
7. [Configuration Guide](#configuration-guide)
8. [Performance & Monitoring](#performance--monitoring)
9. [Testing](#testing)
10. [Troubleshooting](#troubleshooting)
11. [Migration Guide](#migration-guide)
12. [API Reference](#api-reference)

## 🧠 Core Concepts

### Multi-Agent Coordination

Enhanced MultiAgent V3 coordinates multiple agents in sophisticated workflows, supporting:

- **Sequential execution** - Agents run in order
- **Parallel execution** - Agents run concurrently
- **Conditional routing** - Dynamic agent selection
- **Branch workflows** - Complex multi-stage patterns

### Generic Typing

Full type safety with generic agent collections:

```python
# Type-safe dict of agents
MultiAgent[Dict[str, SimpleAgent]]

# Type-safe list of agents
MultiAgent[List[ReactAgent]]
```

### Performance Intelligence

Adaptive routing based on agent performance metrics:

- Success rates
- Execution duration
- Efficiency scores
- Historical performance

## 🏗️ Architecture

### Class Hierarchy

```
Agent (base)
└── EnhancedMultiAgent[AgentsT] (Generic)
    ├── ExecutionMixin
    ├── StateMixin
    ├── PersistenceMixin
    └── SerializationMixin
```

### State Management

```
EnhancedMultiAgentState
├── Core Fields (backward compatible)
│   ├── messages: List[BaseMessage]
│   └── current_agent: str
├── Execution Tracking
│   ├── execution_history: List[AgentExecutionRecord]
│   └── execution_flow: ExecutionFlow
├── Performance Tracking
│   ├── agent_performance: Dict[str, Dict[str, Any]]
│   └── performance_summary: Dict[str, Any]
└── Routing & Coordination
    ├── routing_state: Dict[str, Any]
    ├── parallel_coordination: Dict[str, Any]
    └── conditional_state: Dict[str, Any]
```

### Graph Integration

Uses BaseGraph intelligent routing with custom branch configurations:

- Automatic sequence inference
- Custom routing patterns
- Entry point management
- Terminal node handling

## 🚀 Installation & Setup

### Prerequisites

```bash
# Ensure you have the enhanced base agents
poetry run python -c "from haive.agents.simple.enhanced_agent_v3 import EnhancedSimpleAgent; print('✅ Ready')"
```

### Import

```python
from haive.agents.multi.enhanced_multi_agent_v3 import EnhancedMultiAgent
from haive.agents.simple.enhanced_agent_v3 import EnhancedSimpleAgent
from haive.core.schema.prebuilt.enhanced_multi_agent_state import EnhancedMultiAgentState
```

## 🎬 Quick Start

### Basic Sequential Workflow

```python
from haive.agents.multi.enhanced_multi_agent_v3 import EnhancedMultiAgent
from haive.agents.simple.enhanced_agent_v3 import EnhancedSimpleAgent

# Create individual agents
analyzer = EnhancedSimpleAgent(
    name="analyzer",
    temperature=0.3,
    system_message="You analyze data and provide insights."
)
summarizer = EnhancedSimpleAgent(
    name="summarizer",
    temperature=0.5,
    system_message="You create concise summaries."
)

# Create multi-agent workflow
workflow = EnhancedMultiAgent(
    name="analysis_workflow",
    agents=[analyzer, summarizer],
    execution_mode="sequential"
)

# Execute
compiled = workflow.compile()
result = compiled.invoke({
    "messages": [{"role": "user", "content": "Analyze quarterly sales data"}]
})
```

### Enhanced Features Workflow

```python
# Create with advanced features
advanced_workflow = EnhancedMultiAgent(
    name="adaptive_team",
    agents={
        "researcher": research_agent,
        "analyzer": analysis_agent,
        "writer": writing_agent
    },
    execution_mode="branch",
    performance_mode=True,      # Enable performance tracking
    debug_mode=True,           # Rich debugging
    multi_engine_mode=True,    # Multiple engines
    advanced_routing=True,     # Sophisticated routing
    adaptation_rate=0.2        # Learning rate
)
```

## 🔄 Execution Patterns

### 1. Sequential Execution

Agents execute in order, each receiving output from the previous:

```python
sequential_multi = EnhancedMultiAgent(
    name="sequential_workflow",
    agents=[preprocessor, analyzer, formatter],
    execution_mode="sequential"
)

# Flow: preprocessor → analyzer → formatter
```

**Use Cases:**

- Data processing pipelines
- Content creation workflows
- Analysis → Summary → Report chains

### 2. Parallel Execution

Multiple agents execute simultaneously:

```python
parallel_multi = EnhancedMultiAgent(
    name="expert_panel",
    agents=[tech_expert, business_expert, user_expert],
    execution_mode="parallel"
)

# All experts analyze simultaneously
```

**Use Cases:**

- Multi-perspective analysis
- Concurrent processing
- Expert panel evaluations

### 3. Conditional Routing

Dynamic agent selection based on input characteristics:

```python
conditional_multi = EnhancedMultiAgent(
    name="smart_router",
    agents=[classifier, billing_agent, technical_agent, general_agent],
    entry_point="classifier",
    execution_mode="conditional",
    advanced_routing=True
)

# Add routing logic
def route_by_category(state):
    content = str(state["messages"][-1].content).lower()
    if "billing" in content:
        return "billing_agent"
    elif "technical" in content:
        return "technical_agent"
    else:
        return "general_agent"

conditional_multi.add_conditional_routing(
    "classifier",
    route_by_category,
    {
        "billing_agent": "billing_agent",
        "technical_agent": "technical_agent",
        "general_agent": "general_agent"
    }
)
```

**Use Cases:**

- Customer service routing
- Content categorization
- Request triage systems

### 4. Branch Workflows

Complex multi-stage patterns combining sequential and parallel:

```python
branch_multi = EnhancedMultiAgent(
    name="complex_workflow",
    agents=[validator, processor1, processor2, aggregator],
    entry_point="validator",
    execution_mode="branch",
    advanced_routing=True
)

# Configure: validator → (processor1, processor2) → aggregator
branch_multi.add_edge("validator", "processor1")
branch_multi.add_parallel_group(["processor1", "processor2"], next_agent="aggregator")
```

**Use Cases:**

- Complex document processing
- Multi-stage validation
- Parallel processing with convergence

## 🎛️ Advanced Features

### Performance Tracking

Monitor and optimize agent performance:

```python
# Enable performance mode
perf_multi = EnhancedMultiAgent(
    name="adaptive_system",
    agents={"fast": fast_agent, "accurate": slow_agent},
    performance_mode=True,
    adaptation_rate=0.3  # How quickly to adapt (0.0-1.0)
)

# Performance updates happen automatically
# Manual updates:
perf_multi.update_performance("fast", success=True, duration=0.5)
perf_multi.update_performance("accurate", success=True, duration=2.0)

# Get best agent for task
best_agent = perf_multi.get_best_agent_for_task()
print(f"Best performer: {best_agent}")

# Analyze performance
analysis = perf_multi.analyze_agent_performance()
print(f"Fast agent efficiency: {analysis['agents']['fast']['efficiency_score']}")
```

### Rich Debugging

Comprehensive observability and debugging:

```python
debug_multi = EnhancedMultiAgent(
    name="debug_workflow",
    agents=[agent1, agent2],
    debug_mode=True
)

# Display capabilities
debug_multi.display_capabilities()

# Get detailed summary
summary = debug_multi.get_capabilities_summary()
print(f"Features enabled: {summary['features']}")
```

### Multi-Engine Coordination

Use different engines for different agents:

```python
multi_engine = EnhancedMultiAgent(
    name="multi_engine_team",
    agents={
        "creative": creative_agent,  # High temperature
        "analytical": analytical_agent,  # Low temperature
        "coordinator": coordinator_agent  # Medium temperature
    },
    multi_engine_mode=True
)
```

### Generic Typing Support

Full type safety with agent collections:

```python
from typing import Dict

# Type-safe agent dictionary
agents: Dict[str, EnhancedSimpleAgent] = {
    "researcher": EnhancedSimpleAgent(name="researcher"),
    "writer": EnhancedSimpleAgent(name="writer")
}

# Type-safe multi-agent
typed_multi: EnhancedMultiAgent[Dict[str, EnhancedSimpleAgent]] = EnhancedMultiAgent(
    name="typed_workflow",
    agents=agents,
    performance_mode=True
)
```

## ⚙️ Configuration Guide

### Basic Configuration

```python
basic_config = EnhancedMultiAgent(
    name="basic_workflow",           # Required: workflow identifier
    agents=[agent1, agent2],         # Required: agent collection
    execution_mode="sequential"      # How to execute agents
)
```

### Advanced Configuration

```python
advanced_config = EnhancedMultiAgent(
    name="advanced_workflow",
    agents={"role1": agent1, "role2": agent2},

    # Execution Configuration
    execution_mode="branch",         # infer/sequential/parallel/conditional/branch
    entry_point="role1",            # Starting agent
    infer_sequence=True,            # Auto-infer execution order
    max_iterations=10,              # Max conditional iterations

    # Enhanced Features
    multi_engine_mode=True,         # Multiple engine support
    advanced_routing=True,          # Sophisticated routing
    performance_mode=True,          # Performance tracking
    debug_mode=True,               # Rich debugging

    # Performance Tuning
    adaptation_rate=0.2,           # Learning rate (0.0-1.0)

    # Persistence (optional)
    persistence_config={
        "store_type": "postgres",
        "connection_string": "postgresql://..."
    }
)
```

### State Schema Configuration

```python
# Automatic schema selection
workflow = EnhancedMultiAgent(
    name="auto_schema",
    agents=[agent1, agent2],
    performance_mode=True  # Automatically uses EnhancedMultiAgentState
)

# Manual schema specification
workflow = EnhancedMultiAgent(
    name="manual_schema",
    agents=[agent1, agent2],
    state_schema=EnhancedMultiAgentState
)
```

## 📊 Performance & Monitoring

### Performance Metrics

Each agent tracks:

- **Success Rate**: Percentage of successful executions
- **Average Duration**: Mean execution time
- **Task Count**: Total number of tasks
- **Efficiency Score**: Success rate / duration ratio

### Monitoring Tools

```python
# Get performance analysis
analysis = multi_agent.analyze_agent_performance()

# Overall statistics
print(f"Average success rate: {analysis['overall']['average_success_rate']}")
print(f"Total tasks completed: {analysis['overall']['total_tasks']}")
print(f"Best performing agent: {analysis['overall']['best_agent']}")

# Per-agent metrics
for agent_name, metrics in analysis['agents'].items():
    print(f"{agent_name}:")
    print(f"  Success rate: {metrics['success_rate']}")
    print(f"  Average duration: {metrics['avg_duration']}s")
    print(f"  Efficiency score: {metrics['efficiency_score']}")
```

### Adaptive Routing

The system automatically learns which agents perform best:

```python
# Adaptation rate controls learning speed
# 0.0 = no learning, 1.0 = immediate adaptation
multi_agent = EnhancedMultiAgent(
    agents={"fast": fast_agent, "accurate": slow_agent},
    performance_mode=True,
    adaptation_rate=0.1  # Gradual learning
)

# System will automatically prefer better performing agents
best_agent = multi_agent.get_best_agent_for_task()
```

## 🧪 Testing

### Test Organization

```
packages/haive-agents/tests/multi/
├── test_enhanced_multi_agent_v3.py                    # Basic functionality
└── test_enhanced_multi_agent_v3_comprehensive.py     # All execution patterns
```

### Running Tests

```bash
# Basic functionality tests
poetry run python packages/haive-agents/tests/multi/test_enhanced_multi_agent_v3.py

# Comprehensive execution pattern tests
poetry run python packages/haive-agents/tests/multi/test_enhanced_multi_agent_v3_comprehensive.py

# All multi-agent tests
poetry run pytest packages/haive-agents/tests/multi/ -v
```

### Test Coverage

**Basic Tests (5/5 passing):**

- Creation and Basic Functionality
- Capabilities and Analysis
- Routing Configuration
- Execution and Performance
- Factory Methods

**Comprehensive Tests (6/6 passing):**

- Sequential Execution Pattern
- Parallel Execution Pattern
- Conditional Execution Pattern
- Branch Execution Pattern
- Performance Tracking
- State Management

### Writing Custom Tests

```python
def test_custom_workflow():
    """Test custom multi-agent workflow."""
    # Create multi-agent
    workflow = EnhancedMultiAgent(
        name="test_workflow",
        agents=[agent1, agent2],
        execution_mode="sequential",
        performance_mode=True,
        debug_mode=True
    )

    # Compile and test
    compiled = workflow.compile()
    result = compiled.invoke({
        "messages": [{"role": "user", "content": "Test input"}]
    })

    # Validate results
    assert result is not None
    assert "messages" in result
    assert len(result["messages"]) > 0

    # Check performance tracking
    assert len(workflow.agent_performance) > 0
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Import Errors

```python
# ❌ Wrong
from haive.agents.multi import EnhancedMultiAgent

# ✅ Correct
from haive.agents.multi.enhanced_multi_agent_v3 import EnhancedMultiAgent
```

#### 2. State Schema Validation Errors

```python
# Issue: Message format validation
# Solution: Use proper BaseMessage format

from langchain_core.messages import HumanMessage

# ❌ Wrong
result = compiled.invoke({
    "messages": [{"role": "user", "content": "Hello"}]  # Dict format
})

# ✅ Correct
result = compiled.invoke({
    "messages": [HumanMessage(content="Hello")]  # BaseMessage format
})
```

#### 3. Routing Configuration Errors

```python
# Issue: Agent not found in routing
# Solution: Ensure all referenced agents exist

workflow = EnhancedMultiAgent(
    agents=[agent1, agent2],  # Only these agents exist
    entry_point="agent1"      # ✅ Valid - exists in agents
)

workflow.add_edge("agent1", "agent3")  # ❌ Error - agent3 doesn't exist
```

#### 4. Performance Mode Not Working

```python
# Issue: Performance tracking not enabled
# Solution: Enable performance_mode

# ❌ Wrong - no performance tracking
workflow = EnhancedMultiAgent(agents=[agent1, agent2])

# ✅ Correct - performance tracking enabled
workflow = EnhancedMultiAgent(
    agents=[agent1, agent2],
    performance_mode=True
)
```

### Debug Mode

Enable debug mode for detailed logging:

```python
workflow = EnhancedMultiAgent(
    name="debug_workflow",
    agents=[agent1, agent2],
    debug_mode=True  # Enables detailed logging
)

# Check capabilities
workflow.display_capabilities()

# Get detailed summary
summary = workflow.get_capabilities_summary()
```

### Logging

Monitor execution with logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Now see detailed execution logs
result = compiled.invoke(input_data)
```

## 🔄 Migration Guide

### From Basic MultiAgent

```python
# Old basic MultiAgent
from haive.agents.multi.clean import MultiAgent

old_multi = MultiAgent(
    name="old_workflow",
    agents=[agent1, agent2]
)

# New Enhanced MultiAgent V3
from haive.agents.multi.enhanced_multi_agent_v3 import EnhancedMultiAgent

new_multi = EnhancedMultiAgent(
    name="new_workflow",
    agents=[agent1, agent2],
    # All existing functionality preserved
    # Plus new V3 features available
    performance_mode=True,
    debug_mode=True
)
```

### From SimpleAgent/ReactAgent to MultiAgent

```python
# Single agent
single_agent = SimpleAgent(name="processor")

# Convert to multi-agent for orchestration
multi_agent = EnhancedMultiAgent(
    name="processor_workflow",
    agents=[single_agent],
    execution_mode="sequential"
)

# Or create workflow with multiple agents
multi_agent = EnhancedMultiAgent(
    name="complex_workflow",
    agents=[preprocessor, single_agent, postprocessor],
    execution_mode="sequential"
)
```

### Upgrading Agent Types

```python
# Upgrade to enhanced agents for better integration
from haive.agents.simple.enhanced_agent_v3 import EnhancedSimpleAgent

# Old
basic_agent = SimpleAgent(name="agent")

# New - better V3 integration
enhanced_agent = EnhancedSimpleAgent(
    name="agent",
    temperature=0.7,
    performance_mode=True
)

# Use in V3 MultiAgent
workflow = EnhancedMultiAgent(
    agents=[enhanced_agent],
    performance_mode=True  # Now works optimally
)
```

## 📖 API Reference

### EnhancedMultiAgent Class

#### Constructor

```python
EnhancedMultiAgent(
    name: str,                                    # Required: workflow name
    agents: AgentsT,                             # Required: agent collection
    execution_mode: str = "infer",               # Execution pattern
    entry_point: Optional[str] = None,           # Starting agent
    infer_sequence: bool = True,                 # Auto-infer sequence
    multi_engine_mode: bool = False,             # Multiple engines
    advanced_routing: bool = False,              # Sophisticated routing
    performance_mode: bool = False,              # Performance tracking
    debug_mode: bool = False,                    # Rich debugging
    adaptation_rate: float = 0.1,               # Learning rate
    max_iterations: int = 10,                    # Max conditional iterations
    persistence_config: Optional[Dict] = None,   # Persistence settings
    state_schema: Optional[Type] = None,         # State schema override
    **kwargs                                     # Additional Agent parameters
)
```

#### Core Methods

```python
# Compilation and execution
compile() -> CompiledStateGraph
run(input_data: str) -> str
arun(input_data: str) -> str  # Async version

# Agent management
get_agent_names() -> List[str]
get_agent(name: str) -> Optional[Agent]

# Routing configuration
add_conditional_routing(source: str, condition_fn: Callable, routes: Dict[str, str])
add_parallel_group(agent_names: List[str], next_agent: Optional[str] = None)
add_edge(source_agent: str, target_agent: str)

# Performance tracking
update_performance(agent_name: str, success: bool, duration: float)
get_best_agent_for_task(task_type: str = "general") -> str
analyze_agent_performance() -> Dict[str, Any]

# Capabilities and debugging
display_capabilities()
get_capabilities_summary() -> Dict[str, Any]

# Factory methods
@classmethod
create(agents: Union[List, Dict], name: str = "multi_agent", **kwargs) -> "EnhancedMultiAgent"
```

### EnhancedMultiAgentState Class

#### Core Fields

```python
# Backward compatible
messages: List[BaseMessage]
current_agent: Optional[str]

# Execution tracking
execution_history: List[AgentExecutionRecord]
execution_flow: Optional[ExecutionFlow]
total_executions: int

# Performance tracking
agent_performance: Dict[str, Dict[str, Any]]
performance_summary: Dict[str, Any]

# Routing and coordination
routing_state: Dict[str, Any]
parallel_coordination: Dict[str, Any]
conditional_state: Dict[str, Any]
next_agent: Optional[str]
available_agents: List[str]

# Context and data
shared_context: Dict[str, Any]
private_context: Dict[str, Dict[str, Any]]
workflow_metadata: Dict[str, Any]

# Debugging and observability
debug_info: Dict[str, Any]
execution_trace: List[str]
error_log: List[Dict[str, Any]]

# Status tracking
execution_status: str  # ready/running/completed/error
completion_status: Dict[str, bool]
overall_success: bool
```

#### State Methods

```python
# Execution management
start_execution(execution_mode: str, available_agents: List[str])
record_agent_execution(agent_name: str, duration: float, success: bool, ...)
complete_execution(success: bool = True, error_message: str = None)

# Performance tracking
update_agent_performance(agent_name: str, success_rate: float, avg_duration: float, task_count: int)
get_performance_summary() -> Dict[str, Any]

# Routing and coordination
record_routing_decision(source_agent: str, target_agent: str, decision_criteria: str, ...)
start_parallel_group(agent_names: List[str])
complete_parallel_agent(agent_name: str) -> bool
record_conditional_branch(condition: str, result: Any, chosen_agent: str)

# Summaries and analysis
get_execution_summary() -> Dict[str, Any]
```

### AgentExecutionRecord Model

```python
agent_name: str                    # Name of executing agent
start_time: float                  # Execution start timestamp
end_time: Optional[float]          # Execution end timestamp
duration: Optional[float]          # Execution duration in seconds
success: bool                      # Whether execution succeeded
input_data: Dict[str, Any]         # Input provided to agent
output_data: Dict[str, Any]        # Output from agent
error_message: Optional[str]       # Error message if failed
metadata: Dict[str, Any]           # Additional metadata
```

### ExecutionFlow Model

```python
execution_mode: str                       # Execution mode used
total_duration: Optional[float]           # Total execution duration
agent_executions: List[AgentExecutionRecord]  # Individual executions
routing_decisions: List[Dict[str, Any]]   # Routing decisions made
parallel_groups: List[List[str]]          # Parallel execution groups
conditional_branches: List[Dict[str, Any]]  # Conditional decisions
success: bool                             # Overall success status
error_message: Optional[str]              # Error message if failed
```

## 🎯 Best Practices

### 1. Agent Design

- Use descriptive agent names that reflect their roles
- Configure appropriate temperatures for agent purposes
- Provide clear system messages for each agent
- Use EnhancedSimpleAgent V3 for optimal integration

### 2. Workflow Design

- Start with simple sequential patterns, then add complexity
- Use conditional routing for decision-based workflows
- Use parallel execution for independent tasks
- Use branch workflows for complex multi-stage processes

### 3. Performance Optimization

- Enable performance_mode for production workflows
- Monitor agent performance regularly
- Adjust adaptation_rate based on workflow stability needs
- Use debug_mode during development and testing

### 4. Error Handling

- Always handle potential execution failures
- Use try-catch blocks around compile() and invoke()
- Monitor error_log in state for debugging
- Implement fallback strategies for critical workflows

### 5. Testing Strategy

- Test each execution pattern thoroughly
- Use real agents in tests (no mocks)
- Test performance tracking functionality
- Validate routing decisions with different inputs

## 🔗 Related Documentation

- [Enhanced SimpleAgent V3](enhanced_simple_agent_v3_documentation.md)
- [Enhanced ReactAgent V3](enhanced_react_agent_v3_documentation.md)
- [BaseGraph Documentation](../haive-core/base_graph_documentation.md)
- [State Schema Guide](../haive-core/state_schema_guide.md)
- [Performance Monitoring](performance_monitoring_guide.md)

## 📝 Changelog

### Version 1.0 (2025-07-21)

- Initial release of Enhanced MultiAgent V3
- All execution patterns implemented and tested
- Performance tracking and adaptive routing
- Rich debugging and observability
- Comprehensive test coverage
- Production-ready implementation

---

**Last Updated**: 2025-07-21
**Status**: Production Ready ✅
**Test Coverage**: 11/11 tests passing ✅
