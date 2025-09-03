# Building Agents in Haive - Complete Guide

Welcome to the comprehensive guide for building agents in the Haive framework. This documentation covers everything from basic agent concepts to advanced multi-agent orchestration patterns.

## Table of Contents

- [Introduction](#introduction)
- [Architecture Overview](#architecture-overview)
- [Getting Started](#getting-started)
- [Agent Types](#agent-types)
  - [SimpleAgent V3](#simpleagent-v3)
  - [ReactAgent V3](#reactagent-v3)
  - [EnhancedMultiAgent V4](#enhancedmultiagent-v4)
- [Building Your First Agent](#building-your-first-agent)
- [Advanced Patterns](#advanced-patterns)
- [Best Practices](#best-practices)
- [API Reference](#api-reference)

## Introduction

The Haive Agent Framework provides a sophisticated, hierarchical architecture for building AI agents with LangChain integration. The framework emphasizes:

- **Type Safety**: Comprehensive type hints and Pydantic validation
- **Modularity**: Clean separation of concerns through mixins
- **Flexibility**: Multiple agent types for different use cases
- **Production Ready**: Built-in debugging, monitoring, and error handling

## Architecture Overview

The Haive framework follows a hierarchical architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                      Workflow Layer                          │
│         (Pure orchestration without LLM)                     │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                      Agent Layer                             │
│         (Workflow + Engine + build_graph())                  │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐    │
│  │SimpleAgentV3│  │ReactAgentV3 │  │EnhancedMultiAgent│    │
│  │             │  │             │  │       V4         │    │
│  └─────────────┘  └─────────────┘  └──────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

1. **Enhanced Base Agent** (`haive.agents.base.enhanced_agent.Agent`)
   - Abstract base class requiring `build_graph()` implementation
   - Integrates multiple mixins for comprehensive functionality
   - Generic engine support: `Agent[EngineT]`

2. **Mixins** provide specific capabilities:
   - `ExecutionMixin`: Sync/async execution
   - `StateMixin`: State management
   - `PersistenceMixin`: State persistence
   - `StructuredOutputMixin`: Pydantic model outputs
   - `PrePostAgentMixin`: Pre/post processing hooks

3. **Hooks System** for lifecycle management:
   - Before/after execution hooks
   - State update monitoring
   - Error handling hooks
   - Graph building hooks

## Getting Started

### Installation

```bash
# Install haive-agents package
poetry add haive-agents

# Install required dependencies
poetry add langchain-core langchain-openai pydantic
```

### Basic Setup

```python
from haive.agents.simple.agent_v3 import SimpleAgentV3
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import tool

# Create a simple agent
agent = SimpleAgentV3(
    name="my_assistant",
    engine=AugLLMConfig(
        temperature=0.7,
        model="gpt-4"
    ),
    debug=True  # Enable comprehensive logging
)

# Execute the agent
result = agent.run("Hello! How can you help me?")
print(result)
```

## Agent Types

### SimpleAgent V3

The **SimpleAgentV3** is the foundational agent implementation with comprehensive features:

#### Key Features

- **Enhanced dynamic architecture** with automatic recompilation
- **Hooks integration** for lifecycle monitoring
- **Structured output support** with Pydantic models
- **Debug-first approach** (`debug=True` by default)
- **Agent-as-tool pattern** support

#### Basic Example

```python
from haive.agents.simple.agent_v3 import SimpleAgentV3
from haive.core.engine.aug_llm import AugLLMConfig

# Create a simple conversational agent
agent = SimpleAgentV3(
    name="chat_assistant",
    engine=AugLLMConfig(
        temperature=0.7,
        max_tokens=500,
        system_message="You are a helpful assistant"
    )
)

# Add lifecycle hooks
@agent.before_run
def log_input(context):
    print(f"Processing: {context.input_data}")

@agent.after_run
def log_output(context):
    print(f"Generated: {context.output_data[:100]}...")

# Run the agent
response = agent.run("Explain quantum computing in simple terms")
```

#### With Structured Output

```python
from pydantic import BaseModel, Field
from typing import List

class AnalysisResult(BaseModel):
    summary: str = Field(description="Brief summary of the analysis")
    key_points: List[str] = Field(description="Main points discovered")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score")

# Create agent with structured output
agent = SimpleAgentV3(
    name="analyzer",
    engine=AugLLMConfig(
        structured_output_model=AnalysisResult,
        temperature=0.3  # Lower temperature for consistency
    )
)

# Execute and get structured result
result = agent.run("Analyze the benefits of renewable energy")
assert isinstance(result, AnalysisResult)
print(f"Summary: {result.summary}")
print(f"Confidence: {result.confidence}")
```

#### With Tools

```python
from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

@tool
def weather_api(location: str) -> str:
    """Get weather information for a location."""
    # Mock implementation
    return f"The weather in {location} is sunny, 72°F"

# Create agent with tools
agent = SimpleAgentV3(
    name="assistant_with_tools",
    engine=AugLLMConfig(
        tools=[calculator, weather_api],
        temperature=0.7
    )
)

# Agent will automatically use tools when needed
result = agent.run("What's 15 * 23? Also, what's the weather in New York?")
```

### ReactAgent V3

The **ReactAgentV3** implements the ReAct (Reasoning and Acting) pattern for complex problem-solving:

#### Key Features

- **Iterative reasoning loops** with configurable max iterations
- **Tool integration** for gathering information
- **Reasoning trace** tracking
- **Structured output** support
- **Inherits all SimpleAgentV3 features**

#### Basic Example

```python
from haive.agents.react.agent_v3 import ReactAgentV3
from langchain_core.tools import tool

@tool
def web_search(query: str) -> str:
    """Search the web for information."""
    # Mock implementation
    return f"Search results for '{query}': [relevant information here]"

@tool
def calculator(expression: str) -> str:
    """Perform calculations."""
    return str(eval(expression))

# Create ReactAgent
agent = ReactAgentV3(
    name="research_assistant",
    engine=AugLLMConfig(
        tools=[web_search, calculator],
        temperature=0.7,
        max_tokens=1000
    ),
    max_iterations=5,  # Limit reasoning loops
    debug=True
)

# Execute complex reasoning task
result = agent.run(
    "Find the current population of Tokyo and calculate how many buses "
    "would be needed if each bus holds 50 people"
)
```

#### With Structured Output

```python
from pydantic import BaseModel, Field
from typing import List

class ResearchReport(BaseModel):
    question: str = Field(description="Original research question")
    methodology: List[str] = Field(description="Steps taken to research")
    findings: List[str] = Field(description="Key discoveries")
    calculations: List[str] = Field(description="Calculations performed")
    conclusion: str = Field(description="Final answer with reasoning")
    confidence: float = Field(ge=0.0, le=1.0)

# Create research agent with structured output
agent = ReactAgentV3(
    name="structured_researcher",
    engine=AugLLMConfig(
        tools=[web_search, calculator],
        structured_output_model=ResearchReport,
        temperature=0.3
    ),
    max_iterations=8,
    require_final_answer=True
)

# Get structured research report
report = agent.run("Analyze global renewable energy adoption trends")
print(f"Methodology: {report.methodology}")
print(f"Confidence: {report.confidence}")
```

#### Factory Functions

```python
from haive.agents.react.agent_v3 import create_react_agent, create_research_agent

# Quick agent creation
agent = create_react_agent(
    name="my_react_agent",
    tools=[web_search, calculator],
    max_iterations=6,
    temperature=0.6,
    debug=True
)

# Specialized research agent
research_agent = create_research_agent(
    name="researcher",
    research_tools=[web_search, database_tool],
    analysis_model=ResearchReport,
    max_research_steps=10
)
```

### EnhancedMultiAgent V4

The **EnhancedMultiAgentV4** provides sophisticated multi-agent orchestration:

#### Key Features

- **Direct list initialization** for simplicity
- **Multiple execution modes**: sequential, parallel, conditional, manual
- **AgentNodeV3 integration** for state projection
- **MultiAgentState** for hierarchical state management
- **Dynamic agent addition** with auto-recompilation

#### Sequential Workflow

```python
from haive.agents.multi.enhanced_multi_agent_v4 import EnhancedMultiAgentV4
from haive.agents.simple.agent_v3 import SimpleAgentV3
from haive.agents.react.agent_v3 import ReactAgentV3

# Create individual agents
analyzer = ReactAgentV3(
    name="analyzer",
    engine=AugLLMConfig(tools=[research_tool]),
    max_iterations=5
)

processor = SimpleAgentV3(
    name="processor",
    engine=AugLLMConfig(
        structured_output_model=ProcessedData,
        temperature=0.3
    )
)

formatter = SimpleAgentV3(
    name="formatter",
    engine=AugLLMConfig(
        system_message="You format data into beautiful reports"
    )
)

# Create sequential workflow
workflow = EnhancedMultiAgentV4(
    name="analysis_pipeline",
    agents=[analyzer, processor, formatter],
    execution_mode="sequential"
)

# Execute workflow
result = await workflow.arun({
    "task": "Analyze market trends for electric vehicles"
})
```

#### Parallel Execution

```python
# Create agents for parallel analysis
technical_analyst = SimpleAgentV3(
    name="technical",
    engine=AugLLMConfig(
        structured_output_model=TechnicalAnalysis
    )
)

financial_analyst = SimpleAgentV3(
    name="financial",
    engine=AugLLMConfig(
        structured_output_model=FinancialAnalysis
    )
)

market_analyst = SimpleAgentV3(
    name="market",
    engine=AugLLMConfig(
        structured_output_model=MarketAnalysis
    )
)

# Create parallel workflow
parallel_workflow = EnhancedMultiAgentV4(
    name="comprehensive_analysis",
    agents=[technical_analyst, financial_analyst, market_analyst],
    execution_mode="parallel"
)

# All agents execute simultaneously
results = await parallel_workflow.arun({
    "company": "Tesla",
    "period": "Q4 2023"
})
```

#### Conditional Routing

```python
# Create classifier and specialized agents
classifier = SimpleAgentV3(
    name="classifier",
    engine=AugLLMConfig(
        structured_output_model=Classification,
        temperature=0.1
    )
)

simple_processor = SimpleAgentV3(
    name="simple_processor",
    engine=AugLLMConfig()
)

complex_processor = ReactAgentV3(
    name="complex_processor",
    engine=AugLLMConfig(tools=[calculator, analyzer]),
    max_iterations=10
)

# Create conditional workflow
conditional_workflow = EnhancedMultiAgentV4(
    name="smart_routing",
    agents=[classifier, simple_processor, complex_processor],
    execution_mode="conditional"
)

# Add routing logic
def route_by_complexity(state):
    """Route based on task complexity."""
    complexity = state.get("complexity", 0)
    return "complex_processor" if complexity > 0.7 else "simple_processor"

conditional_workflow.add_conditional_edge(
    from_agent="classifier",
    condition=route_by_complexity,
    routes={
        "simple_processor": "simple_processor",
        "complex_processor": "complex_processor"
    }
)

# Execute with routing
result = await conditional_workflow.arun({
    "task": "Process this data based on complexity"
})
```

#### Manual Graph Building

```python
# Create workflow with manual control
manual_workflow = EnhancedMultiAgentV4(
    name="custom_flow",
    agents=[agent1, agent2, agent3, agent4],
    execution_mode="manual",
    build_mode="manual"
)

# Build custom execution flow
manual_workflow.add_edge("agent1", "agent2")
manual_workflow.add_edge("agent1", "agent3")  # Parallel branch

# Add conditional routing
manual_workflow.add_conditional_edge(
    from_agent="agent2",
    condition=lambda state: state.get("needs_validation"),
    true_agent="agent4",
    false_agent=END
)

manual_workflow.add_edge("agent3", "agent4")
manual_workflow.add_edge("agent4", END)

# Build and execute
manual_workflow.build()
result = await manual_workflow.arun({"input": "data"})
```

## Building Your First Agent

### Step 1: Choose Your Agent Type

- **SimpleAgentV3**: For straightforward tasks, conversations, and single-purpose agents
- **ReactAgentV3**: For complex reasoning, research, and multi-step problem solving
- **EnhancedMultiAgentV4**: For orchestrating multiple agents in workflows

### Step 2: Configure the Engine

```python
from haive.core.engine.aug_llm import AugLLMConfig

# Basic configuration
engine = AugLLMConfig(
    model="gpt-4",              # or "gpt-3.5-turbo", "claude-3", etc.
    temperature=0.7,            # 0.0 = deterministic, 1.0 = creative
    max_tokens=1000,            # Maximum response length
    system_message="...",       # System prompt
    tools=[...],                # Optional tools
    structured_output_model=... # Optional Pydantic model
)
```

### Step 3: Add Tools (Optional)

```python
from langchain_core.tools import tool

@tool
def my_custom_tool(param: str) -> str:
    """Tool description for the LLM."""
    # Implementation
    return result

# Add to engine
engine = AugLLMConfig(tools=[my_custom_tool])
```

### Step 4: Define Structured Output (Optional)

```python
from pydantic import BaseModel, Field

class MyOutput(BaseModel):
    field1: str = Field(description="Description for LLM")
    field2: int = Field(ge=0, description="Non-negative integer")

# Add to engine
engine = AugLLMConfig(structured_output_model=MyOutput)
```

### Step 5: Create and Execute

```python
# Create agent
agent = SimpleAgentV3(
    name="my_agent",
    engine=engine,
    debug=True
)

# Add hooks for monitoring
@agent.before_run
def monitor_start(context):
    print(f"Starting: {context.agent_name}")

# Execute
result = agent.run("Your input here")
```

## Advanced Patterns

### 1. Agent as Tool Pattern

Convert any agent into a reusable tool:

```python
# Create specialized agent
expert_agent = SimpleAgentV3(
    name="domain_expert",
    engine=AugLLMConfig(
        system_message="You are an expert in quantum physics",
        temperature=0.3
    )
)

# Convert to tool
expert_tool = expert_agent.as_tool(
    name="quantum_expert",
    description="Consult quantum physics expert"
)

# Use in another agent
coordinator = ReactAgentV3(
    name="coordinator",
    engine=AugLLMConfig(tools=[expert_tool, other_tools]),
)
```

### 2. Self-Discover Pattern (Production Ready!)

Systematic 4-stage reasoning methodology for complex problem-solving:

```python
from haive.agents.reasoning_and_critique.self_discover import SelfDiscoverWorkflow
from haive.agents.reasoning_and_critique.self_discover.selector.agent import SelectorAgent
from haive.agents.reasoning_and_critique.self_discover.adapter.agent import AdapterAgent
from haive.agents.reasoning_and_critique.self_discover.structurer.agent import StructurerAgent
from haive.agents.reasoning_and_critique.self_discover.executor.agent import ExecutorAgent

# ✅ Option 1: Use complete workflow (Recommended)
async def solve_complex_problem():
    workflow = SelfDiscoverWorkflow()

    result = await workflow.solve_task("""
    Our startup needs to choose a growth strategy:
    (A) Market expansion ($500K, 6 months)
    (B) Product features ($300K, 4 months)
    (C) Customer success ($200K, 3 months)

    Budget: $400K, Goal: 40% growth this year
    Current metrics: 85% retention, $1.2K CAC, 8% churn

    What should we prioritize and why?
    """)

    # Returns 12/12 quality scores in production
    workflow.analyze_self_discover_result(result)
    return result

# ✅ Option 2: Custom 4-stage coordination
async def custom_self_discover():
    # Create 4-stage pipeline: Select → Adapt → Structure → Execute
    selector = SelectorAgent(name="selector", engine=AugLLMConfig(temperature=0.3))
    adapter = AdapterAgent(name="adapter", engine=AugLLMConfig(temperature=0.4))
    structurer = StructurerAgent(name="structurer", engine=AugLLMConfig(temperature=0.2))
    executor = ExecutorAgent(name="executor", engine=AugLLMConfig(temperature=0.6))

    # Sequential workflow
    self_discover = EnhancedMultiAgentV4(
        name="custom_self_discover",
        agents=[selector, adapter, structurer, executor],
        execution_mode="sequential"
    )

    result = await self_discover.arun({
        "messages": [HumanMessage(content="Design a recommendation system...")]
    })

    return result

# ✅ Option 3: Hybrid with reflection
async def self_discover_with_reflection():
    workflow = SelfDiscoverWorkflow()

    reflection_agent = SimpleAgentV3(
        name="reflector",
        engine=AugLLMConfig(
            temperature=0.3,
            system_message="Analyze reasoning quality and suggest improvements"
        )
    )

    # Combine Self-Discover + Reflection
    hybrid = EnhancedMultiAgentV4(
        name="enhanced_reasoning",
        agents=[workflow, reflection_agent],
        execution_mode="sequential"
    )

    return await hybrid.arun({"task": "Complex strategic analysis..."})

# Production validated: 12/12 quality scores, real Azure OpenAI execution
```

**Self-Discover Benefits** (Production Validated):

- ✅ **Systematic Reasoning**: 4-stage methodology (Select → Adapt → Structure → Execute)
- ✅ **Quality Validated**: 12/12 scores across 4 demo scenarios
- ✅ **Traceable Process**: Clear reasoning traces and module selection
- ✅ **Production Ready**: Real LLM execution, no mocks

### 3. Dynamic Recompilation

Agents that adapt at runtime:

```python
# Create agent with auto-recompilation
adaptive_agent = SimpleAgentV3(
    name="adaptive",
    engine=AugLLMConfig(tools=[initial_tool]),
    auto_recompile=True
)

# Add tools dynamically
@tool
def new_capability(input: str) -> str:
    """New tool added at runtime."""
    return f"Processing: {input}"

# Agent automatically recompiles
adaptive_agent.add_tool(new_capability)

# Continue execution with new capability
result = adaptive_agent.run("Use the new capability")
```

### 4. Meta-Agent Pattern

Agents embedded in MetaStateSchema:

```python
from haive.core.schema.prebuilt.meta_state import MetaStateSchema

# Create agent
agent = SimpleAgentV3(
    name="worker",
    engine=AugLLMConfig()
)

# Make meta-capable
meta_state = MetaStateSchema.from_agent(
    agent=agent,
    initial_state={"ready": True},
    graph_context={"purpose": "analysis"}
)

# Execute with tracking
result = await meta_state.execute_agent(
    input_data={"query": "Analyze this"},
    update_state=True
)

# Check execution summary
summary = meta_state.get_execution_summary()
```

## Best Practices

### 1. Error Handling

```python
try:
    result = agent.run(input_data)
except ValidationError as e:
    # Handle structured output validation errors
    logger.error(f"Output validation failed: {e}")
except ToolExecutionError as e:
    # Handle tool execution failures
    logger.error(f"Tool execution failed: {e}")
except Exception as e:
    # General error handling
    logger.exception(f"Agent execution failed: {e}")
```

### 2. Debugging and Monitoring

```python
# Enable comprehensive debugging
agent = SimpleAgentV3(
    name="debugged_agent",
    engine=engine,
    debug=True,  # Detailed logging
    hooks_enabled=True  # Lifecycle monitoring
)

# Add monitoring hooks
@agent.before_run
def log_start(context):
    logger.info(f"Starting: {context.input_data}")

@agent.after_run
def log_complete(context):
    logger.info(f"Completed in {context.execution_time}ms")

@agent.on_error
def log_error(context):
    logger.error(f"Error: {context.error}")
```

### 3. Performance Optimization

```python
# Configure for production
agent = SimpleAgentV3(
    name="production_agent",
    engine=AugLLMConfig(
        temperature=0.3,      # Lower for consistency
        max_tokens=500,       # Limit token usage
        timeout=30            # Set timeout
    ),
    debug=False,              # Disable debug logging
    change_tracking_enabled=False  # Disable if not needed
)

# For ReactAgent, limit iterations
react_agent = ReactAgentV3(
    name="efficient_react",
    engine=engine,
    max_iterations=5,         # Balance thoroughness vs cost
    stop_on_first_tool_result=True  # For simple lookups
)
```

### 4. Testing Agents

```python
import pytest
from unittest.mock import Mock

# Note: Haive philosophy is NO MOCKS for real testing
# This is just for isolated unit tests

def test_agent_creation():
    """Test agent can be created."""
    agent = SimpleAgentV3(
        name="test_agent",
        engine=AugLLMConfig()
    )
    assert agent.name == "test_agent"
    assert agent.debug is True  # Default

def test_agent_execution():
    """Test agent executes successfully."""
    agent = SimpleAgentV3(
        name="test_agent",
        engine=AugLLMConfig(
            temperature=0.1  # Deterministic for testing
        )
    )
    result = agent.run("Hello")
    assert isinstance(result, str)
    assert len(result) > 0
```

## API Reference

### SimpleAgentV3

```python
class SimpleAgentV3(Agent[AugLLMConfig]):
    """Enhanced simple agent with dynamic architecture."""

    # Core configuration
    name: str
    engine: AugLLMConfig

    # Enhanced features
    debug: bool = True
    auto_recompile: bool = True
    hooks_enabled: bool = True

    # Convenience fields (sync to engine)
    temperature: float | None
    max_tokens: int | None
    model_name: str | None
    system_message: str | None
    structured_output_model: type[BaseModel] | None

    # Methods
    def run(input_data: Any) -> Any
    async def arun(input_data: Any) -> Any
    def add_tool(tool: BaseTool) -> None

    # Class methods
    @classmethod
    def as_tool(name: str, description: str) -> BaseTool

    # Hooks
    @before_run
    @after_run
    @on_error
```

### ReactAgentV3

```python
class ReactAgentV3(SimpleAgentV3):
    """ReAct pattern agent with reasoning loops."""

    # ReAct configuration
    max_iterations: int = 10
    stop_on_first_tool_result: bool = False
    require_final_answer: bool = True

    # State tracking
    iteration_count: int
    reasoning_trace: list[str]
    tool_results_history: list[dict]

    # Methods
    def get_reasoning_trace() -> list[str]
    def get_tool_usage_history() -> list[dict]
    def set_max_iterations(max: int) -> None
```

### EnhancedMultiAgentV4

```python
class EnhancedMultiAgentV4(Agent):
    """Multi-agent orchestration with flexible execution."""

    # Configuration
    agents: list[Agent]
    execution_mode: Literal["sequential", "parallel", "conditional", "manual"]
    build_mode: Literal["auto", "manual", "lazy"]
    state_schema: type = MultiAgentState

    # Graph building
    def build_graph() -> BaseGraph
    def add_edge(from_agent: str, to_agent: str) -> None
    def add_conditional_edge(...) -> None

    # Agent management
    def add_agent(agent: Agent) -> None
    def get_agent(name: str) -> Agent | None
    def get_agent_names() -> list[str]
```

### AugLLMConfig

```python
class AugLLMConfig(BaseModel):
    """LLM engine configuration."""

    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int | None = None
    system_message: str | None = None
    tools: list[BaseTool] = []
    structured_output_model: type[BaseModel] | None = None
    timeout: int = 300
    retry_attempts: int = 3
```

## Next Steps

1. **Explore Examples**: Check the `/examples` directory for working code
2. **Read Architecture Docs**: Deep dive into specific components
3. **Join Community**: Contribute and get help from other developers
4. **Build Something**: Start with a simple agent and expand

## Contributing

We welcome contributions! Please see our [Contributing Guide](../CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
