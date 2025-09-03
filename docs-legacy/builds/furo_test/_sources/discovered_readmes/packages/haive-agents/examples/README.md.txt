# Haive Agent Examples

This directory contains demonstration scripts showing how to use the new agent patterns created using `agent.py`, `SimpleAgentV3`, and `EnhancedMultiAgentV4` as foundations.

## Overview

These examples demonstrate:

- Sequential multi-agent workflows (ReactAgent → SimpleAgent)
- Structured output with Pydantic models
- Chat prompt templates with input variables
- Pre/post processing hooks
- Real component usage (no mocks)

## Examples

### 1. `working_sequential_demo.py` ✅ TESTED & WORKING

Demonstrates a simple ReactAgent → SimpleAgent sequential flow:

- ReactAgent with tools for market analysis
- SimpleAgent with structured output (FinalReport model)
- Prompt templates with input variables
- Real execution with Azure OpenAI

```bash
poetry run python packages/haive-agents/examples/working_sequential_demo.py
```

### 2. `basic_agent_test.py` ✅ TESTED & WORKING

Tests individual agents without multi-agent orchestration:

- SimpleAgentV3 with structured output
- ReactAgent with tools
- Manual sequential execution

```bash
poetry run python packages/haive-agents/examples/basic_agent_test.py
```

### 3. `simple_sequential_demo.py`

More complex demo with hooks and multiple workflows:

- React → Simple with structured output
- Multi-agent workflow with hooks
- Structured output chain

```bash
poetry run python packages/haive-agents/examples/simple_sequential_demo.py
```

### 4. `sequential_multi_agent_demo.py`

Comprehensive demo using pattern files:

- Multiple workflow patterns
- RAG agents with structured output
- Research workflows
- Reflection patterns

```bash
poetry run python packages/haive-agents/examples/sequential_multi_agent_demo.py
```

### 5. `reflection_hooks_demo.py`

Advanced patterns with reflection and hooks:

- Pre/post processing agents
- Reflection workflows
- Quality gates and iterative improvement
- Comprehensive hook monitoring

```bash
poetry run python packages/haive-agents/examples/reflection_hooks_demo.py
```

## Key Patterns Demonstrated

### 1. Sequential Agent Flow

```python
# ReactAgent for analysis
react_agent = ReactAgent(
    name="analyst",
    engine=AugLLMConfig(tools=[tool1, tool2])
)

# SimpleAgent for structured output
simple_agent = SimpleAgentV3(
    name="formatter",
    engine=AugLLMConfig(structured_output_model=OutputModel)
)

# Execute sequentially
analysis = await react_agent.arun("Analyze X")
report = await simple_agent.arun({"analysis": analysis})
```

### 2. Structured Output Models

```python
class FinalReport(BaseModel):
    title: str = Field(description="Report title")
    key_findings: List[str] = Field(description="Main findings")
    confidence: float = Field(ge=0.0, le=1.0)
```

### 3. Prompt Templates with Variables

```python
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "{system_message}"),
    ("human", "Analyze: {topic}\nContext: {context}")
])
```

### 4. Hook Patterns

```python
@workflow.before_agent_execution
def log_start(agent_name: str, state: dict):
    print(f"Starting {agent_name}")

@workflow.after_agent_execution
def log_end(agent_name: str, result: Any):
    print(f"Completed {agent_name}")
```

## Pattern Files Created

The following pattern files were created in `packages/haive-agents/src/haive/agents/patterns/`:

1. **`simple_rag_agent_pattern.py`** - RAG agents using SimpleAgentV3 as base
2. **`sequential_workflow_agent.py`** - Workflow patterns using EnhancedMultiAgentV4
3. **`react_structured_agent_variants.py`** - React → Structured patterns
4. **`hybrid_multi_agent_patterns.py`** - Advanced hybrid agent patterns

## Notes

- All examples use real LLM execution (Azure OpenAI)
- No mocks are used - everything is tested with real components
- The patterns directory needs proper imports to work with multi-agent demos
- SimpleAgentV3 and ReactAgent work well individually
- EnhancedMultiAgentV4 has some type validation issues that need resolution
