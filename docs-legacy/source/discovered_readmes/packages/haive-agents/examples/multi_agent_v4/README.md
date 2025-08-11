# EnhancedMultiAgentV4 Examples

This directory contains practical examples demonstrating various multi-agent workflow patterns using EnhancedMultiAgentV4.

## Examples

### 1. Sequential Analysis Pipeline (`sequential_analysis_pipeline.py`)

Demonstrates a ReactAgent → SimpleAgent sequential workflow where:

- ReactAgent performs data analysis using calculation tools
- SimpleAgent formats results with structured output
- Data flows cleanly between agents
- Tools are isolated to specific agents

**Key Pattern**: Sequential execution with structured output transfer

### 2. Parallel Document Analysis (`parallel_document_analysis.py`)

Shows parallel execution of multiple specialized agents:

- Sentiment analyzer with sentiment scoring tools
- Entity extractor with pattern matching tools
- Topic analyzer with statistical tools
- All agents run simultaneously for faster processing
- Results are formatted with structured outputs

**Key Pattern**: Parallel execution with tool specialization

### 3. Conditional Support Router (`conditional_support_router.py`)

Implements intelligent query routing based on classification:

- Classifier agent categorizes incoming queries
- Routes to technical, billing, or product specialists
- Each specialist has domain-specific tools
- Structured outputs for consistent responses

**Key Pattern**: Conditional routing with specialized handlers

### 4. Complex Data Flow (`complex_data_flow.py`)

Demonstrates sophisticated multi-stage workflow:

- Research → Analysis → Strategy → Validation → Summary
- Each agent builds on previous agents' structured outputs
- Direct field access in prompts (e.g., `{researcher.findings}`)
- Mix of tool-using and reasoning-only agents

**Key Pattern**: Complex data flow with structured state passing

## Running the Examples

Each example can be run independently:

```bash
# Run sequential pipeline
poetry run python sequential_analysis_pipeline.py

# Run parallel analysis
poetry run python parallel_document_analysis.py

# Run conditional router
poetry run python conditional_support_router.py

# Run complex data flow
poetry run python complex_data_flow.py
```

## Key Concepts Demonstrated

### 1. Tool Isolation

Each agent has only the tools it needs:

- No shared tool instances between agents
- Domain-specific tool sets
- Clear separation of concerns

### 2. Structured Output Flow

Agents with `structured_output_model` create typed fields on the state:

- Next agents can reference these fields directly
- Type-safe data flow between agents
- Clean, validated outputs

### 3. Execution Modes

- **Sequential**: One agent after another
- **Parallel**: Multiple agents simultaneously
- **Conditional**: Dynamic routing based on conditions
- **Manual**: Full control over execution flow

### 4. State Management

- Each agent has isolated state in `agent_states`
- Structured outputs become state fields
- Direct field access in prompts
- No schema flattening issues

## Common Patterns

### Creating Agents with Tools

```python
agent = ReactAgentV4(
    name="analyzer",
    engine=AugLLMConfig(temperature=0.3),
    tools=[tool1, tool2],  # Agent-specific tools
    structured_output_model=OutputModel  # Optional
)
```

### Sequential Workflow

```python
workflow = EnhancedMultiAgentV4(
    agents=[agent1, agent2, agent3],
    execution_mode="sequential"
)
```

### Accessing Previous Agent Outputs

```python
agent2 = SimpleAgentV3(
    name="processor",
    prompt_template=ChatPromptTemplate.from_messages([
        ("system", "Process the analysis results."),
        ("human", "Previous findings: {agent1.findings}")
    ])
)
```

### Conditional Routing

```python
workflow.add_multi_conditional_edge(
    from_agent="classifier",
    condition=routing_function,
    routes={
        "category1": "agent1",
        "category2": "agent2"
    }
)
```

## Best Practices

1. **Use Structured Outputs**: Enable clean data flow
2. **Isolate Tools**: Each agent gets only needed tools
3. **Name Agents Clearly**: Helps with debugging
4. **Start Simple**: Build complexity gradually
5. **Test with Real LLMs**: No mocks, actual behavior

## Troubleshooting

### Import Errors

Always use `poetry run`:

```bash
poetry run python example.py
```

### Missing Agents

Ensure all agents are in the workflow:

```python
workflow = EnhancedMultiAgentV4(
    agents=[agent1, agent2],  # All agents here
    execution_mode="sequential"
)
```

### Tool Conflicts

Never share tool instances:

```python
# ❌ WRONG
shared_tool = calculator()
agent1 = ReactAgent(tools=[shared_tool])
agent2 = ReactAgent(tools=[shared_tool])

# ✅ CORRECT
agent1 = ReactAgent(tools=[calculator])
agent2 = ReactAgent(tools=[word_counter])
```

---

**Date**: August 7, 2025  
**Framework Version**: haive-agents 0.2.0+
