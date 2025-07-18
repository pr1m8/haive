# Task-Oriented Agents Documentation

## Overview

Task-oriented agents in Haive are designed to accomplish specific goals through planning, execution, and verification cycles. These agents excel at breaking down complex tasks and executing them systematically.

## Available Task Agents

### 1. ReactAgent

**Location**: `/packages/haive-agents/src/haive/agents/react/`

ReAct (Reasoning + Acting) agent that interleaves thought, action, and observation.

**Key Features**:

- Explicit reasoning steps
- Tool usage with observations
- Self-correction capabilities
- Structured thought process

**Usage Example**:

```python
from haive.agents.react import ReactAgent
from haive.tools import PythonREPLTool, WebSearchTool

agent = ReactAgent(
    name="research_assistant",
    tools=[PythonREPLTool(), WebSearchTool()],
    max_iterations=5
)

result = await agent.execute(
    "Research the latest AI developments and create a summary report"
)
```

### 2. PlanAndExecuteAgent

**Location**: `/packages/haive-agents/src/haive/agents/plan_and_execute/`

Agent that creates a plan before execution and follows it systematically.

**Key Features**:

- Upfront planning phase
- Step-by-step execution
- Plan revision capabilities
- Progress tracking

**Usage Example**:

```python
from haive.agents.plan_and_execute import PlanAndExecuteAgent

agent = PlanAndExecuteAgent(
    name="project_manager",
    planner_model="gpt-4",
    executor_model="gpt-3.5-turbo"
)

result = await agent.execute({
    "task": "Set up a new Python project with testing and CI/CD",
    "requirements": ["pytest", "github actions", "pre-commit"]
})
```

### 3. ChainAgent

**Location**: `/packages/haive-agents/src/haive/agents/chain/`

Agent that chains multiple sub-agents or tasks in sequence.

**Key Features**:

- Sequential task execution
- Inter-agent communication
- Pipeline configuration
- Result aggregation

**Usage Example**:

```python
from haive.agents.chain import ChainAgent
from haive.agents import ResearchAgent, WriterAgent, ReviewerAgent

agent = ChainAgent(
    name="content_pipeline",
    agents=[
        ResearchAgent(),
        WriterAgent(),
        ReviewerAgent()
    ]
)

article = await agent.execute("Write an article about quantum computing")
```

### 4. MultiAgent

**Location**: `/packages/haive-agents/src/haive/agents/multi/`

Orchestrates multiple agents working in parallel or coordination.

**Key Features**:

- Parallel agent execution
- Agent coordination
- Resource management
- Result synthesis

**Usage Example**:

```python
from haive.agents.multi import MultiAgent

agent = MultiAgent(
    name="analysis_team",
    agents={
        "data_analyst": DataAnalysisAgent(),
        "visualizer": VisualizationAgent(),
        "reporter": ReportAgent()
    },
    coordination="parallel"
)
```

### 5. CodeExecutorAgent

**Location**: `/packages/haive-agents/src/haive/agents/code_executor/`

Specialized agent for code generation and execution tasks.

**Key Features**:

- Code generation
- Safe execution environment
- Error handling and debugging
- Multiple language support

**Usage Example**:

```python
from haive.agents.code_executor import CodeExecutorAgent

agent = CodeExecutorAgent(
    name="code_assistant",
    languages=["python", "javascript"],
    sandbox=True
)

result = await agent.execute(
    "Create a function to calculate fibonacci numbers with memoization"
)
```

## Task Execution Patterns

### Planning Pattern

```python
# Explicit planning before execution
agent = PlanAndExecuteAgent(
    planning_prompt="Break down this task into clear steps",
    revision_enabled=True
)
```

### Iteration Pattern

```python
# Iterative refinement
agent = ReactAgent(
    max_iterations=10,
    early_stopping=True,
    success_criteria="All tests pass"
)
```

### Pipeline Pattern

```python
# Multi-stage processing
pipeline = ChainAgent([
    ("extract", DataExtractor()),
    ("transform", DataTransformer()),
    ("load", DataLoader())
])
```

## Configuration Options

### Execution Control

- `max_iterations`: Maximum execution cycles
- `timeout`: Task timeout in seconds
- `retry_on_failure`: Automatic retry configuration
- `checkpoint_frequency`: Save progress intervals

### Resource Management

- `max_concurrent_tools`: Tool usage limits
- `memory_limit`: Memory usage constraints
- `api_rate_limits`: External API throttling

### Output Configuration

- `output_format`: Structure of results
- `include_reasoning`: Include thought process
- `verbosity`: Logging detail level

## Advanced Features

### Custom Success Criteria

```python
def custom_validator(result):
    return result.accuracy > 0.95

agent = ReactAgent(
    success_validator=custom_validator
)
```

### Progress Callbacks

```python
async def on_step_complete(step, result):
    await notify_progress(step, result)

agent = PlanAndExecuteAgent(
    callbacks={"on_step": on_step_complete}
)
```

### State Persistence

```python
# Save execution state
checkpoint = agent.save_checkpoint()

# Resume from checkpoint
agent.load_checkpoint(checkpoint)
result = await agent.resume()
```

## Best Practices

1. **Task Decomposition**
   - Break complex tasks into manageable steps
   - Define clear success criteria
   - Use appropriate agent types for task complexity

2. **Error Handling**
   - Implement retry logic for transient failures
   - Provide fallback strategies
   - Log detailed error information

3. **Resource Optimization**
   - Choose appropriate models for each step
   - Implement caching where possible
   - Monitor token usage and costs

4. **Testing**
   - Test individual agent components
   - Validate task plans before execution
   - Use sandbox environments for code execution

## Integration Examples

### With Monitoring

```python
from haive.monitoring import TaskMonitor

monitor = TaskMonitor()
agent = ReactAgent(monitor=monitor)

# Track execution metrics
result = await agent.execute(task)
metrics = monitor.get_metrics()
```

### With Validation

```python
from haive.validators import OutputValidator

agent = CodeExecutorAgent(
    output_validator=OutputValidator(
        schema={"type": "object", "required": ["code", "tests"]}
    )
)
```

## See Also

- [CLAUDE_AGENTS.md](./CLAUDE_AGENTS.md) - Main agents documentation
- [CLAUDE_AGENTS_CONVERSATIONAL.md](./CLAUDE_AGENTS_CONVERSATIONAL.md) - Conversational agents
- [CLAUDE_AGENT_TEMPLATE.md](./CLAUDE_AGENT_TEMPLATE.md) - Agent development template
