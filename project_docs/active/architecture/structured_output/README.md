# Structured Output Documentation

This directory contains comprehensive documentation for handling structured output in Haive agents when using LangGraph.

## Contents

1. **[AUTOMATIC_EXTRACTION.md](AUTOMATIC_EXTRACTION.md)** 🆕
   - How automatic structured output extraction works
   - Architecture decisions and implementation details
   - Migration guide and best practices

2. **[WHY_ADDABLEVALUESDICT.md](WHY_ADDABLEVALUESDICT.md)**
   - Deep dive into why LangGraph returns AddableValuesDict
   - Understanding the graph-based computation model
   - Benefits and design rationale

3. **[STRUCTURED_OUTPUT_ANALYSIS.md](STRUCTURED_OUTPUT_ANALYSIS.md)**
   - Detailed execution flow analysis
   - How structured output works with multi-node graphs
   - Trace analysis and findings

4. **[STRUCTURED_OUTPUT_SOLUTION_SUMMARY.md](STRUCTURED_OUTPUT_SOLUTION_SUMMARY.md)**
   - Practical solutions and recommendations
   - Performance comparison of different approaches
   - Quick reference guide

## Quick Start

### Automatic Extraction (Recommended) 🆕

Simply set `structured_output_model` on your agent:

```python
from haive.agents.simple.agent_v3 import SimpleAgentV3
from haive.core.engine.aug_llm import AugLLMConfig

agent = SimpleAgentV3(
    name="my_agent",
    engine=AugLLMConfig(),
    structured_output_model=YourOutputModel  # Automatic extraction!
)

# Get Pydantic model directly
result = await agent.arun(input)  # result is YourOutputModel instance!
```

### Manual Extraction

For more control, use StructuredOutputHandler:

```python
from haive.agents.base.structured_output_handler import StructuredOutputHandler

# Create handler
handler = StructuredOutputHandler(YourOutputModel)

# Extract structured output
result = await agent.arun(input)
output = handler.extract(result)
```

## Related Code

- Implementation: `packages/haive-agents/src/haive/agents/base/structured_output_handler.py`
- Examples: `packages/haive-agents/examples/multi_agent_v4/structured_output_best_practices.py`
