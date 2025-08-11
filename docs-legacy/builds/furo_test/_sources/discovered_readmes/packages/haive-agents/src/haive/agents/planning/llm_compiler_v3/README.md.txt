# LLM Compiler V3 Agent

**Enhanced MultiAgent V3 implementation of the LLM Compiler pattern**

## Overview

LLM Compiler V3 is a modernized implementation of the LLM Compiler pattern using Enhanced MultiAgent V3 architecture. It enables efficient parallel execution of tasks by automatically decomposing complex queries into a DAG of parallelizable subtasks.

### Key Features

- **Parallel Task Execution**: Automatically identifies and executes independent tasks in parallel
- **Dependency Management**: Handles complex task dependencies with automatic resolution
- **Smart Replanning**: Automatically replans when tasks fail or results are insufficient
- **Enhanced MultiAgent V3**: Built on the latest multi-agent framework for consistency and maintainability
- **Tool Integration**: Seamlessly integrates with any LangChain-compatible tools
- **Structured Output**: Uses Pydantic models for type-safe data flow
- **Performance Optimization**: Tracks execution efficiency and optimization opportunities

## Architecture

The LLM Compiler V3 Agent uses four specialized sub-agents:

1. **Planner Agent** (`SimpleAgent` with structured output)
   - Decomposes queries into parallelizable task DAGs
   - Optimizes for maximum parallelization while respecting dependencies
   - Creates comprehensive execution plans

2. **Task Fetcher Agent** (`ReactAgent`)
   - Manages task coordination and scheduling
   - Handles dependency resolution and execution ordering
   - Coordinates parallel execution within resource limits

3. **Parallel Executor Agent** (`ReactAgent` with tools)
   - Executes individual tasks using appropriate tools
   - Manages tool invocation and error handling
   - Provides detailed execution results

4. **Joiner Agent** (`SimpleAgent` with structured output)
   - Synthesizes results from all executed tasks
   - Creates final comprehensive answers
   - Decides between final response or replanning

## Installation

This module is part of the `haive-agents` package:

```bash
pip install haive-agents
```

## Quick Start

### Basic Usage

```python
from haive.agents.planning.llm_compiler_v3 import LLMCompilerV3Agent
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_community.tools import DuckDuckGoSearchRun

# Create tools
search_tool = DuckDuckGoSearchRun()
calculator_tool = # ... your calculator tool

# Create agent
agent = LLMCompilerV3Agent(
    name="research_compiler",
    tools=[search_tool, calculator_tool]
)

# Execute complex query
result = await agent.arun(
    "Find the latest AI research papers from 2024 and calculate the average number of citations"
)

print(f"Final Answer: {result.final_answer}")
print(f"Tasks Executed: {result.tasks_executed}")
print(f"Success Rate: {result.success_rate:.2%}")
print(f"Total Time: {result.total_execution_time:.2f}s")
```

### Advanced Configuration

```python
from haive.agents.planning.llm_compiler_v3 import (
    LLMCompilerV3Agent,
    LLMCompilerV3Config,
    ExecutionMode
)

# Custom configuration
config = LLMCompilerV3Config(
    name="advanced_compiler",
    execution_mode=ExecutionMode.PARALLEL,
    max_parallel_tasks=5,
    task_timeout=180.0,
    enable_auto_replan=True,
    max_replan_attempts=3,
    parallel_efficiency_target=0.85
)

# Create agent with configuration
agent = LLMCompilerV3Agent(
    name="advanced_compiler",
    config=config,
    tools=my_tools
)

# Execute with preferences
result = await agent.arun(
    query="Complex multi-step research task",
    context={"domain": "AI research", "focus": "recent developments"},
    execution_preferences={
        "max_parallel": 8,
        "timeout": 300
    }
)
```

### Synchronous Usage

```python
# For non-async environments
result = agent.run(
    "Search for recent developments in quantum computing and summarize the key breakthroughs"
)
```

## Examples

### Research and Analysis

```python
async def research_example():
    agent = LLMCompilerV3Agent(
        tools=[web_search, calculator, pdf_reader, summarizer]
    )

    result = await agent.arun("""
    Research the top 5 AI conferences in 2024, find their acceptance rates,
    calculate the average acceptance rate, and summarize the most common research topics.
    """)

    return result

# The agent will automatically:
# 1. Search for AI conferences in parallel
# 2. Extract acceptance rates for each
# 3. Calculate averages while searching continues
# 4. Analyze research topics in parallel
# 5. Synthesize comprehensive final answer
```

### Data Processing Pipeline

```python
async def data_processing_example():
    agent = LLMCompilerV3Agent(
        tools=[data_loader, data_cleaner, analyzer, visualizer]
    )

    result = await agent.arun("""
    Load the sales data from Q4 2024, clean any inconsistencies,
    analyze monthly trends, and create summary visualizations.
    """)

    # Automatic parallelization:
    # - Data loading and initial analysis in parallel
    # - Cleaning and trend analysis as soon as data loads
    # - Visualization generation parallel to statistical analysis
```

## Key Components

### Models

- **CompilerTask**: Individual task in the execution DAG
- **CompilerPlan**: Complete execution plan with dependencies
- **ParallelExecutionResult**: Result from task execution
- **CompilerInput/Output**: Structured input and output models

### Configuration

- **LLMCompilerV3Config**: Comprehensive configuration options
- **ExecutionMode**: Parallel, sequential, or hybrid execution
- **Tool management**: Priority, exclusion, and timeout settings
- **Performance tuning**: Efficiency targets and optimization settings

### State Management

- **LLMCompilerStateSchema**: Complete execution state tracking
- **Dependency resolution**: Automatic task argument resolution
- **Progress monitoring**: Real-time execution progress
- **Error handling**: Graceful failure recovery and replanning

## Performance Features

### Parallel Execution Optimization

- **Dependency Analysis**: Automatic identification of parallelizable tasks
- **Resource Management**: Configurable parallel execution limits
- **Load Balancing**: Smart task scheduling based on priority and dependencies
- **Efficiency Tracking**: Real-time monitoring of parallel execution efficiency

### Smart Replanning

- **Failure Detection**: Automatic detection of execution issues
- **Adaptive Replanning**: Intelligent replanning based on partial results
- **Context Preservation**: Maintains successful results during replanning
- **Iterative Improvement**: Learns from failures to create better plans

### Tool Management

- **Tool Prioritization**: Configurable tool preferences and priorities
- **Timeout Handling**: Individual and global timeout management
- **Error Recovery**: Graceful handling of tool failures
- **Result Caching**: Optional caching for expensive tool operations

## Comparison with LLM Compiler V1

| Feature           | V1 (Original)            | V3 (Enhanced MultiAgent)   |
| ----------------- | ------------------------ | -------------------------- |
| Architecture      | Custom nodes + LangGraph | Enhanced MultiAgent V3     |
| Code Complexity   | ~500+ lines              | ~300 lines                 |
| Maintainability   | Custom implementation    | Standardized framework     |
| Agent Consistency | Different patterns       | Unified agent approach     |
| Debugging         | Complex state tracking   | Built-in debugging         |
| Extensibility     | Custom modifications     | Framework-based extensions |
| Testing           | Mock-heavy               | Real component testing     |

## Advanced Usage

### Custom Tool Integration

```python
from langchain_core.tools import tool

@tool
def custom_analysis_tool(data: str, method: str) -> str:
    \"\"\"Perform custom analysis on data.\"\"\"
    # Your analysis logic
    return analysis_result

agent = LLMCompilerV3Agent(
    tools=[custom_analysis_tool, other_tools],
    config=LLMCompilerV3Config(
        tool_priorities={"custom_analysis_tool": 10}  # High priority
    )
)
```

### Execution Monitoring

```python
# Enable detailed monitoring
config = LLMCompilerV3Config(
    enable_detailed_logging=True,
    log_task_timings=True,
    enable_execution_tracing=True
)

agent = LLMCompilerV3Agent(config=config, tools=tools)
result = await agent.arun(query)

# Access detailed execution information
print(f"Parallel Efficiency: {result.parallel_efficiency:.2%}")
print(f"Task Breakdown:")
for task_result in result.execution_results:
    print(f"  {task_result.task_id}: {task_result.execution_time:.2f}s")
```

### Error Handling and Recovery

```python
try:
    result = await agent.arun(complex_query)

    if result.success_rate < 0.8:
        print(f"Warning: Only {result.success_rate:.2%} of tasks succeeded")
        failed_tasks = result.get_failed_tasks()
        for failed in failed_tasks:
            print(f"Failed: {failed.task_id} - {failed.error_message}")

except Exception as e:
    print(f"Execution failed: {e}")
```

## Testing

The LLM Compiler V3 Agent follows the haive-agents testing philosophy of **no mocks** - all tests use real LLM components:

```python
import pytest
from haive.agents.planning.llm_compiler_v3 import LLMCompilerV3Agent

@pytest.mark.asyncio
async def test_llm_compiler_v3_real_execution():
    \"\"\"Test with real LLM and tools.\"\"\"
    agent = LLMCompilerV3Agent(tools=[calculator_tool, search_tool])

    result = await agent.arun(
        "Calculate 15 * 23 and search for the latest AI news"
    )

    assert result.tasks_executed >= 2
    assert "345" in result.final_answer  # Calculator result
    assert "AI" in result.final_answer.lower()  # Search result
    assert result.success_rate > 0.5
```

## Migration from LLM Compiler V1

### Key Changes

1. **Simplified Architecture**: No custom nodes or complex LangGraph structures
2. **Standardized Patterns**: Uses Enhanced MultiAgent V3 for consistency
3. **Better Error Handling**: Built-in replanning and error recovery
4. **Improved Maintainability**: Cleaner code with standard patterns
5. **Enhanced Testing**: Real component testing without mocks

### Migration Steps

1. Replace `LLMCompilerAgent` with `LLMCompilerV3Agent`
2. Update configuration to use `LLMCompilerV3Config`
3. Adapt tools to LangChain-compatible format
4. Update result handling to use `CompilerOutput` model
5. Test with real components instead of mocks

## API Reference

For detailed API documentation, see the [API Reference](../../../docs/api/planning/llm_compiler_v3/index.rst).

## Contributing

Contributions are welcome! Please follow the haive-agents development standards:

- Use real component testing (no mocks)
- Follow Enhanced MultiAgent V3 patterns
- Include comprehensive documentation
- Add examples for new features

## See Also

- [Enhanced MultiAgent V3](../../multi/enhanced_multi_agent_v3.py)
- [Plan-and-Execute V3](../plan_execute_v3/)
- [ReWOO V3](../rewoo_v3/)
- [Advanced Agent Rebuilding Guide](../../../../project_docs/active/implementation/ADVANCED_AGENT_REBUILDING_GUIDE.md)
