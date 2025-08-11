# React Agents - ReAct Pattern Implementation

**Module**: `haive.agents.react`  
**Purpose**: ReAct (Reasoning and Acting) agents with iterative reasoning loops  
**Version**: Enhanced v3 with structured output and advanced features

## Overview

The react module provides ReAct (Reasoning and Acting) pattern implementations that enable agents to iteratively reason about problems, take actions using tools, and observe results until reaching a solution. This module includes both the original ReactAgent and the enhanced ReactAgentV3 with comprehensive structured output support.

**Key Capabilities:**

- Iterative reasoning loops with configurable iteration limits
- Tool usage in reasoning contexts with automatic recompilation
- Structured output with complete reasoning documentation
- Enhanced debugging and observability features
- Factory functions for quick agent creation
- Performance optimization configurations
- Integration with hooks system for monitoring

## Available Implementations

### ReactAgent (Original)

```python
from haive.agents.react import ReactAgent
from haive.core.engine.aug_llm import AugLLMConfig

agent = ReactAgent(
    name="react_agent",
    engine=AugLLMConfig(tools=[calculator, search_tool])
)
```

**Features:**

- Basic ReAct pattern implementation
- Extends SimpleAgent with reasoning loops
- Tool integration and state management
- Compatible with existing haive-core infrastructure

### ReactAgentV3 (Enhanced)

```python
from haive.agents.react import ReactAgentV3, create_react_agent
from pydantic import BaseModel, Field

class Analysis(BaseModel):
    reasoning_steps: List[str] = Field(description="Step-by-step reasoning")
    conclusion: str = Field(description="Final answer")

agent = ReactAgentV3(
    name="enhanced_react",
    engine=AugLLMConfig(
        tools=[calculator, research_tool],
        structured_output_model=Analysis
    ),
    max_iterations=8,
    debug=True
)
```

**Enhanced Features:**

- Full structured output support with Pydantic model validation
- Comprehensive reasoning trace documentation
- Dynamic tool addition with automatic graph recompilation
- Hooks system integration for monitoring and intervention
- Factory functions for rapid deployment
- Performance optimization configurations
- Enhanced error handling and recovery

## Factory Functions

### create_react_agent()

```python
from haive.agents.react import create_react_agent

agent = create_react_agent(
    name="research_assistant",
    tools=[web_search, calculator, database_lookup],
    structured_output_model=ResearchReport,
    max_iterations=10,
    temperature=0.6,
    debug=True
)
```

**Parameters:**

- `name`: Agent identifier
- `tools`: List of LangChain tools for acting phase
- `structured_output_model`: Optional Pydantic model for responses
- `max_iterations`: Maximum reasoning iterations (1-50)
- `temperature`: LLM creativity level (0.0-2.0)
- `max_tokens`: Token limit per iteration
- `debug`: Enable detailed reasoning traces
- `**engine_kwargs`: Additional AugLLMConfig parameters

### create_research_agent()

```python
from haive.agents.react import create_research_agent

researcher = create_research_agent(
    name="academic_researcher",
    research_tools=[scholarly_search, citation_lookup, data_analyzer],
    analysis_model=ResearchInvestigation,
    max_research_steps=12,
    debug=True
)
```

**Optimized for:**

- Academic and market research tasks
- Systematic information gathering
- Multi-source data validation
- Comprehensive analysis documentation

## ReAct Pattern Implementation

### Reasoning Loop Structure

```
1. **Think**: Analyze current situation and plan next steps
2. **Act**: Execute tools or gather information if needed
3. **Observe**: Process results and update understanding
4. **Evaluate**: Determine if problem is solved or continue
5. **Iterate**: Return to step 1 if max_iterations not reached
6. **Conclude**: Generate final answer (structured if configured)
```

### Graph Architecture

```
START → agent_node → validation_node
            ↑             ↓
            ←─── tool_node (loops back for continued reasoning)
            ↑             ↓
            ←─── parse_output (for structured output, then loops back)
                          ↓
                       END (when reasoning complete or max iterations)
```

## Structured Output Models

### Built-in Models

The module provides several pre-built structured output models for common use cases:

```python
# Comprehensive reasoning analysis
class ReasoningAnalysis(BaseModel):
    original_query: str
    reasoning_approach: str
    iteration_steps: List[str]
    tools_utilized: List[str]
    final_conclusion: str
    confidence_score: float
    total_iterations: int

# Technical problem solving
class TechnicalProblemSolution(BaseModel):
    problem_statement: str
    technical_analysis: List[str]
    solution_components: List[str]
    implementation_steps: List[str]
    risk_assessment: List[str]

# Research investigation
class ResearchInvestigation(BaseModel):
    research_question: str
    investigation_scope: str
    key_findings: List[str]
    supporting_evidence: List[str]
    executive_summary: str
```

## Performance Considerations

### Configuration Strategies

**Fast Execution (2-3 iterations):**

```python
fast_agent = ReactAgentV3(
    name="quick_solver",
    engine=AugLLMConfig(tools=[essential_tools], temperature=0.1, max_tokens=400),
    max_iterations=3,
    stop_on_first_tool_result=True,
    debug=False
)
```

**Thorough Analysis (8-12 iterations):**

```python
thorough_agent = ReactAgentV3(
    name="comprehensive_analyst",
    engine=AugLLMConfig(tools=[all_tools], temperature=0.5, max_tokens=1200),
    max_iterations=12,
    require_final_answer=True,
    debug=True
)
```

**Production Balanced (4-6 iterations):**

```python
production_agent = ReactAgentV3(
    name="production_solver",
    engine=AugLLMConfig(tools=[core_tools], temperature=0.3, max_tokens=800),
    max_iterations=6,
    debug=False
)
```

### Cost and Performance Metrics

- **Cost Factor**: ReAct agents are 3-5x more expensive than SimpleAgents due to iteration
- **Iteration Overhead**: Each iteration involves full LLM call + potential tool execution
- **Quality vs Speed**: More iterations generally improve solution quality
- **Token Accumulation**: Tool results accumulate across reasoning iterations

## Advanced Features

### Dynamic Tool Addition

```python
agent = ReactAgentV3(
    name="adaptive_agent",
    engine=AugLLMConfig(tools=[basic_calculator]),
    auto_recompile=True,
    max_iterations=8
)

# Add tools during execution
@tool
def advanced_analyzer(data: str) -> str:
    return f"Advanced analysis: {data}"

agent.add_tool(advanced_analyzer)  # Triggers automatic recompilation
```

### Hooks System Integration

```python
@agent.before_iteration
def log_iteration_start(context):
    logger.info(f"Starting iteration {context.iteration_count}")

@agent.after_tool_execution
def monitor_tool_usage(context):
    logger.info(f"Tool {context.tool_name}: {context.success}")

@agent.before_final_answer
def validate_completeness(context):
    if len(context.reasoning_trace) < 3:
        logger.warning("Solution may need more reasoning steps")
```

### Reasoning Trace Access

```python
result = agent.run("Complex problem requiring multiple steps")

# Access detailed reasoning process
reasoning_steps = agent.get_reasoning_trace()
tool_history = agent.get_tool_usage_history()

print(f"Completed {agent.iteration_count} iterations")
print(f"Reasoning steps: {len(reasoning_steps)}")
print(f"Tools used: {len(tool_history)} times")
```

## Integration Examples

### Multi-Agent Coordination

```python
# Research phase
research_agent = create_research_agent(
    name="researcher",
    research_tools=[web_search, database_query],
    analysis_model=ResearchInvestigation
)

# Analysis phase
analysis_agent = create_react_agent(
    name="analyst",
    tools=[calculator, data_analyzer],
    structured_output_model=TechnicalSolution
)

# Sequential execution
research_result = research_agent.run("Research renewable energy trends")
analysis_result = analysis_agent.run(f"Analyze this research: {research_result}")
```

### Agent-as-Tool Pattern

```python
# Convert ReactAgent to tool for use in other agents
research_tool = ReactAgentV3.as_tool(
    name="research_assistant",
    description="Perform comprehensive research and analysis",
    engine=AugLLMConfig(tools=[research_tools]),
    max_iterations=6
)

# Use in coordinator agent
coordinator = SimpleAgentV3(
    name="coordinator",
    engine=AugLLMConfig(tools=[research_tool, calculation_tool])
)
```

### Meta-Agent Embedding

```python
from haive.core.schema.prebuilt.meta_state import MetaStateSchema

# Embed ReactAgent in MetaStateSchema for advanced coordination
react_agent = ReactAgentV3(name="embedded_react", engine=config)
meta_state = MetaStateSchema.from_agent(
    agent=react_agent,
    initial_state={"research_mode": True},
    graph_context={"coordination_level": "advanced"}
)

# Execute with full tracking and state management
result = await meta_state.execute_agent(complex_task_data)
```

## Testing and Development

### Real Component Testing

```python
def test_react_agent_with_real_execution():
    """Test ReactAgentV3 with actual LLM and tools - no mocks."""
    agent = ReactAgentV3(
        name="test_agent",
        engine=AugLLMConfig(
            tools=[calculator, fact_lookup],
            llm_config=DeepSeekLLMConfig()
        ),
        max_iterations=5,
        debug=True
    )

    result = agent.run("Calculate the area of a circle with radius 10")

    # Verify real execution occurred
    assert agent.iteration_count > 0
    assert len(agent.get_reasoning_trace()) > 0
    assert "314" in str(result)  # π * 10²
```

### Structured Output Validation

```python
def test_structured_output_react():
    """Test structured output generation with reasoning documentation."""
    agent = ReactAgentV3(
        name="structured_test",
        engine=AugLLMConfig(
            tools=[research_tools],
            structured_output_model=ReasoningAnalysis
        ),
        max_iterations=6
    )

    analysis = agent.run("Analyze the impact of AI on education")

    # Validate structured output
    assert isinstance(analysis, ReasoningAnalysis)
    assert len(analysis.iteration_steps) > 0
    assert analysis.confidence_score >= 0.0
    assert analysis.confidence_score <= 1.0
```

## Migration Guide

### From ReactAgent to ReactAgentV3

```python
# Old ReactAgent
old_agent = ReactAgent(
    name="old_react",
    engine=AugLLMConfig(tools=[calculator])
)

# New ReactAgentV3 (drop-in replacement + enhancements)
new_agent = ReactAgentV3(
    name="enhanced_react",
    engine=AugLLMConfig(tools=[calculator]),
    max_iterations=10,  # Now configurable
    debug=True         # Enhanced debugging
)

# All existing functionality preserved
result = new_agent.run("Same input as before")
```

### Adding Structured Output

```python
# Define your output model
class CustomAnalysis(BaseModel):
    problem: str = Field(description="Problem statement")
    solution: str = Field(description="Complete solution")
    confidence: float = Field(ge=0.0, le=1.0, description="Solution confidence")

# Update agent configuration
enhanced_agent = ReactAgentV3(
    name="structured_react",
    engine=AugLLMConfig(
        tools=existing_tools,
        structured_output_model=CustomAnalysis  # Add this line
    ),
    max_iterations=8
)

# Results now return CustomAnalysis instances
analysis = enhanced_agent.run("Your problem here")
print(f"Confidence: {analysis.confidence}")
```

## Best Practices

### Iteration Management

- **Simple tasks**: 3-5 iterations
- **Complex analysis**: 8-12 iterations
- **Production systems**: 4-6 iterations for cost balance
- **Research tasks**: 10-15 iterations for thoroughness

### Tool Selection

- **Essential tools**: Include only necessary tools to reduce decision complexity
- **Specialized tools**: Add domain-specific tools for better reasoning quality
- **Dynamic addition**: Use `add_tool()` for adaptive behavior
- **Tool validation**: Ensure tools provide clear, actionable results

### Temperature Settings

- **Technical analysis**: 0.1-0.3 (focused, deterministic)
- **Creative problem solving**: 0.6-0.9 (flexible, innovative)
- **Balanced reasoning**: 0.3-0.5 (focused but adaptive)
- **Research tasks**: 0.2-0.4 (accurate, systematic)

### Production Deployment

- Set `debug=False` for production to reduce logging overhead
- Monitor iteration counts and costs with hooks system
- Use structured output for consistent API responses
- Implement timeout handling for long-running reasoning tasks
- Cache compiled graphs for repeated agent instantiation

## API Reference

For complete API documentation, see the auto-generated documentation:

- `ReactAgent`: Original ReAct implementation
- `ReactAgentV3`: Enhanced ReAct with structured output
- `create_react_agent()`: Factory function for standard configurations
- `create_research_agent()`: Factory function for research-optimized agents

## Examples

### Basic Usage

```python
from haive.agents.react import ReactAgentV3
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions."""
    return str(eval(expression))

agent = ReactAgentV3(
    name="math_solver",
    engine=AugLLMConfig(tools=[calculator]),
    max_iterations=5,
    debug=True
)

result = agent.run("What is 15% of 2500?")
```

### Advanced Structured Output

```python
from pydantic import BaseModel, Field
from typing import List

class ProblemSolution(BaseModel):
    problem_type: str = Field(description="Category of problem")
    reasoning_steps: List[str] = Field(description="Step-by-step reasoning")
    calculations: List[str] = Field(description="Mathematical calculations")
    final_answer: str = Field(description="Complete solution")
    verification: str = Field(description="Solution verification method")

agent = ReactAgentV3(
    name="problem_solver",
    engine=AugLLMConfig(
        tools=[calculator, fact_checker],
        structured_output_model=ProblemSolution
    ),
    max_iterations=8
)

solution = agent.run("A train travels 120km in 1.5 hours. How long to travel 300km?")
print(f"Problem type: {solution.problem_type}")
print(f"Steps: {len(solution.reasoning_steps)}")
print(f"Answer: {solution.final_answer}")
```

## See Also

- **haive.agents.simple**: SimpleAgent and SimpleAgentV3 for linear execution
- **haive.core.engine.aug_llm**: AugLLMConfig for engine configuration
- **haive.core.schema.prebuilt.meta_state**: MetaStateSchema for agent embedding
- **haive.agents.base**: Base Agent class with common functionality
