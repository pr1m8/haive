# Plan-and-Execute V3 Agent

Advanced implementation of the Plan-and-Execute methodology using Enhanced MultiAgent V3 architecture.

## Overview

The Plan-and-Execute V3 agent separates complex task execution into distinct phases:

1. **Planning**: Create detailed, structured execution plans
2. **Execution**: Execute individual steps with available tools
3. **Evaluation**: Assess progress and decide next actions
4. **Replanning**: Revise plans when necessary for better outcomes

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PlanExecuteV3Agent                           │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Enhanced MultiAgent V3                     │   │
│  │                                                         │   │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐         │   │
│  │  │ Planner  │───▶│ Executor │───▶│Evaluator │         │   │
│  │  │(Simple)  │    │ (React)  │    │ (Simple) │         │   │
│  │  └──────────┘    └──────────┘    └──────────┘         │   │
│  │       │                               │                │   │
│  │       │          ┌──────────┐         │                │   │
│  │       └─────────▶│Replanner │◀────────┘                │   │
│  │                  │ (Simple) │                          │   │
│  │                  └──────────┘                          │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Sub-Agents

- **Planner** (SimpleAgent): Creates structured execution plans with dependencies
- **Executor** (ReactAgent): Executes steps using available tools
- **Evaluator** (SimpleAgent): Assesses progress and makes continuation decisions
- **Replanner** (SimpleAgent): Creates revised plans when needed

### Structured Outputs

- **ExecutionPlan**: Detailed plan with steps, dependencies, and metadata
- **StepExecution**: Results from individual step execution
- **PlanEvaluation**: Progress assessment and decision (continue/replan/finalize)
- **RevisedPlan**: Improved plan incorporating lessons learned

## Features

- **Real Component Testing**: No mocks, uses actual LLMs and tools
- **Computed Fields**: State management with automatic field computation
- **Conditional Routing**: Smart routing between sub-agents based on state
- **Plan Revision**: Automatic replanning when execution encounters issues
- **Tool Integration**: Full tool support for step execution
- **Performance Tracking**: Built-in performance monitoring and metrics

## Usage

### Basic Usage

```python
from haive.agents.planning.plan_execute_v3 import PlanExecuteV3Agent
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import tool

# Create some tools
@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions."""
    return str(eval(expression))

@tool
def web_search(query: str) -> str:
    """Search the web for information."""
    # Implementation here
    return f"Search results for: {query}"

# Create agent
agent = PlanExecuteV3Agent(
    name="research_planner",
    config=AugLLMConfig(temperature=0.7),
    tools=[calculator, web_search]
)

# Execute task
result = await agent.arun(
    "Research renewable energy market trends and calculate the growth rate"
)

print(f"Final Answer: {result.final_answer}")
print(f"Steps Completed: {result.steps_completed}/{result.total_steps}")
print(f"Execution Time: {result.total_execution_time:.2f}s")
```

### Advanced Usage with Input Structure

```python
from haive.agents.planning.plan_execute_v3 import PlanExecuteV3Agent, PlanExecuteInput

# Structured input
input_data = PlanExecuteInput(
    objective="Analyze competitive landscape for AI startups",
    context="Focus on companies founded in the last 2 years with >$10M funding",
    max_steps=8,
    time_limit=300  # 5 minutes
)

# Execute with structured input
result = await agent.arun(input_data)

# Access detailed results
print(f"Objective: {result.objective}")
print(f"Key Findings:")
for finding in result.key_findings:
    print(f"  - {finding}")
print(f"Confidence: {result.confidence_score:.2%}")
```

### Custom State Management

```python
from haive.agents.planning.plan_execute_v3 import PlanExecuteV3State
from langchain_core.messages import HumanMessage

# Create custom initial state
state = PlanExecuteV3State(
    messages=[HumanMessage(content="Analyze market data")],
    context={"industry": "renewable_energy", "timeframe": "2023-2024"}
)

# Execute with existing state
result = await agent.arun("Continue analysis with latest data", state=state)
```

## Configuration

### Agent Parameters

- **name**: Agent identifier
- **config**: AugLLMConfig for LLM settings
- **tools**: List of available tools for execution
- **max_iterations**: Maximum planning iterations (default: 5)
- **max_steps_per_plan**: Maximum steps per plan (default: 10)

### LLM Configuration

```python
from haive.core.engine.aug_llm import AugLLMConfig

config = AugLLMConfig(
    model="gpt-4o",  # Use best model for planning
    temperature=0.3,  # Lower temperature for consistent planning
    max_tokens=2000,
    system_message="You are an expert at systematic planning and execution"
)
```

## State Schema

The `PlanExecuteV3State` extends `MessagesState` with computed fields:

### Core Fields

- **plan**: Current execution plan
- **step_executions**: History of step executions
- **evaluations**: History of plan evaluations
- **revision_count**: Number of plan revisions
- **final_answer**: Final result when complete

### Computed Fields

- **objective**: Extracted from plan or messages
- **current_step**: Formatted current step for executor
- **plan_status**: Formatted plan status overview
- **previous_results**: Formatted execution history
- **execution_summary**: Complete execution summary
- **should_evaluate**: Whether evaluation is needed
- **key_findings**: Extracted key findings from executions

## Examples

### Market Research Agent

```python
# Tools for market research
@tool
def stock_data(symbol: str) -> str:
    """Get stock data for a company."""
    return f"Stock data for {symbol}"

@tool
def news_search(query: str) -> str:
    """Search for recent news."""
    return f"News about: {query}"

# Create specialized market research agent
market_agent = PlanExecuteV3Agent(
    name="market_researcher",
    tools=[stock_data, news_search, calculator],
    max_steps_per_plan=12
)

# Research task
result = await market_agent.arun(
    "Analyze Tesla's market position and calculate its P/E ratio trends"
)
```

### Content Creation Agent

```python
@tool
def content_research(topic: str) -> str:
    """Research content on a topic."""
    return f"Content research for: {topic}"

@tool
def write_draft(outline: str) -> str:
    """Write content draft from outline."""
    return f"Draft content based on: {outline}"

# Content creation agent
content_agent = PlanExecuteV3Agent(
    name="content_creator",
    tools=[content_research, write_draft],
    config=AugLLMConfig(temperature=0.8)  # Higher creativity
)

result = await content_agent.arun(
    "Create a comprehensive blog post about sustainable technology trends"
)
```

## Error Handling

The agent includes robust error handling:

- **Step Failures**: Automatic evaluation and potential replanning
- **Tool Errors**: Graceful handling of tool execution failures
- **Plan Issues**: Automatic replanning when plans become infeasible
- **Timeout Handling**: Respect for execution time limits

## Performance

- **Parallel Execution**: Where possible within Enhanced MultiAgent V3
- **Smart Routing**: Conditional routing minimizes unnecessary steps
- **State Caching**: Efficient state management with computed fields
- **Tool Optimization**: Intelligent tool selection and usage

## Testing

```python
import pytest
from haive.agents.planning.plan_execute_v3 import PlanExecuteV3Agent

@pytest.mark.asyncio
async def test_plan_execute_v3_real_execution():
    """Test Plan-and-Execute V3 with real components."""
    agent = PlanExecuteV3Agent(tools=[calculator])

    result = await agent.arun("Calculate the compound interest on $1000 at 5% for 3 years")

    assert result.final_answer
    assert result.steps_completed > 0
    assert result.confidence_score > 0.5
    assert "1157.63" in result.final_answer  # Expected compound interest result
```

## Integration

### With Other Agents

```python
# Use Plan-and-Execute as a tool for other agents
plan_tool = PlanExecuteV3Agent.as_tool(
    name="complex_planner",
    description="Plan and execute complex multi-step tasks",
    tools=[calculator, web_search]
)

# Integrate into ReactAgent
coordinator = ReactAgent(
    name="coordinator",
    tools=[plan_tool, other_tools]
)
```

### With Custom State Schemas

```python
from haive.agents.planning.plan_execute_v3 import PlanExecuteV3State

class CustomPlanState(PlanExecuteV3State):
    """Extended state with custom fields."""

    project_id: str = Field(description="Project identifier")
    custom_context: Dict[str, Any] = Field(default_factory=dict)

    @computed_field
    @property
    def project_status(self) -> str:
        """Custom project status computation."""
        return f"Project {self.project_id}: {self.execution_summary}"
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed with `poetry install --all-extras`

2. **Tool Execution Failures**: Check tool implementations and error handling

3. **Plan Generation Issues**: Verify LLM configuration and system prompts

4. **State Management**: Ensure proper state schema usage and field validation

### Debug Mode

```python
# Enable debug mode for detailed logging
agent = PlanExecuteV3Agent(
    name="debug_agent",
    tools=tools
)
agent.multi_agent.debug_mode = True

# Execute with detailed logging
result = await agent.arun("Debug this complex task")
```

## Contributing

When extending Plan-and-Execute V3:

1. Follow existing patterns for structured outputs
2. Use computed fields for state management
3. Test with real components (no mocks)
4. Document new features comprehensively
5. Follow the established routing patterns

## See Also

- [Enhanced MultiAgent V3](../multi/enhanced_multi_agent_v3.py)
- [SimpleAgent V3](../simple/agent.py)
- [ReactAgent V3](../react/agent.py)
- [LLM Compiler V3](../llm_compiler_v3/README.md)
