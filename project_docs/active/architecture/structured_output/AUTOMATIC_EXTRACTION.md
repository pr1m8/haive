# Automatic Structured Output Extraction

**Version**: 1.0  
**Date**: August 7, 2025  
**Status**: Implemented

## Overview

Haive agents now support automatic extraction of structured output from LangGraph's AddableValuesDict. When you set `structured_output_model` on any agent, the framework automatically extracts and returns the Pydantic model instance.

## How It Works

### 1. Set Structured Output Model

```python
from haive.agents.simple.agent_v3 import SimpleAgentV3
from pydantic import BaseModel

class AnalysisResult(BaseModel):
    topic: str
    findings: List[str]
    confidence: float

agent = SimpleAgentV3(
    name="analyzer",
    engine=AugLLMConfig(),
    structured_output_model=AnalysisResult  # Just set this!
)
```

### 2. Execute Normally

```python
# Execute as usual
result = await agent.arun({"messages": [HumanMessage(content="Analyze X")]})

# result is now an AnalysisResult instance, not AddableValuesDict!
print(result.topic)
print(result.confidence)
```

### 3. Behind the Scenes

The automatic extraction happens in `ExecutionMixin._process_output`:

1. Checks if agent has `structured_output_model` set
2. Creates a `StructuredOutputHandler` for that model
3. Extracts the structured output from AddableValuesDict
4. Returns the Pydantic model instance directly

## Architecture Decision

### Why ExecutionMixin?

We chose to implement automatic extraction in `ExecutionMixin._process_output` because:

1. **Universal Coverage** - All agents inherit from ExecutionMixin
2. **Final Processing** - It's the last step before returning to user
3. **Transparent** - No changes needed to existing agent code
4. **Clean Abstraction** - Hides LangGraph internals from users

### Alternative Approaches Considered

1. **Agent State** - Not appropriate; state is for persistence
2. **Separate Mixin** - Would require explicit inclusion
3. **Post-processor** - Would add complexity

## Benefits

1. **Simplicity** - Users get Pydantic models directly
2. **Type Safety** - IDE autocomplete and type checking work
3. **No Manual Extraction** - No need to understand AddableValuesDict
4. **Backward Compatible** - Existing code continues to work

## Example: Complete Flow

```python
from typing import List
from pydantic import BaseModel, Field
from haive.agents.simple.agent_v3 import SimpleAgentV3
from haive.core.engine.aug_llm import AugLLMConfig

# 1. Define your output model
class ReportAnalysis(BaseModel):
    title: str = Field(description="Report title")
    summary: str = Field(description="Executive summary")
    key_points: List[str] = Field(description="Main points")
    risk_level: str = Field(description="low/medium/high")
    score: float = Field(ge=0, le=100)

# 2. Create agent with structured output
agent = SimpleAgentV3(
    name="report_analyzer",
    engine=AugLLMConfig(
        temperature=0.1,
        system_message="You are a report analysis expert."
    ),
    structured_output_model=ReportAnalysis  # Automatic extraction enabled!
)

# 3. Run the agent
result = await agent.arun({
    "messages": [HumanMessage(content="Analyze this quarterly report...")]
})

# 4. Use the result directly - it's a ReportAnalysis instance!
print(f"Title: {result.title}")
print(f"Risk Level: {result.risk_level}")
print(f"Score: {result.score:.1f}/100")

for i, point in enumerate(result.key_points, 1):
    print(f"{i}. {point}")
```

## Technical Details

### StructuredOutputHandler

The `StructuredOutputHandler` class provides the extraction logic:

- Searches multiple field name patterns
- Handles various result formats
- Provides fallback mechanisms
- Type-safe extraction

### Field Name Resolution

The handler searches for structured output in this order:

1. Model name as snake_case (e.g., `AnalysisResult` → `analysis_result`)
2. Common field names: `structured_output`, `output`, `result`
3. Any field containing the model type

### Error Handling

If extraction fails, the framework:

1. Logs a debug message (not warning, to avoid noise)
2. Falls back to normal output processing
3. Returns the original output

## Migration Guide

### Before (Manual Extraction)

```python
# Old way - manual extraction needed
result = await agent.arun(input_data)
handler = StructuredOutputHandler(AnalysisResult)
analysis = handler.extract(result)  # Manual step
```

### After (Automatic)

```python
# New way - automatic extraction
agent.structured_output_model = AnalysisResult
analysis = await agent.arun(input_data)  # Direct result!
```

## Best Practices

1. **Always Define Models** - Use clear, well-documented Pydantic models
2. **Set at Creation** - Set `structured_output_model` when creating the agent
3. **Type Hints** - Use type hints for better IDE support
4. **Validation** - Add Pydantic validators for business rules

## Troubleshooting

### Not Getting Structured Output?

1. Check that `structured_output_model` is set on the agent
2. Verify the model matches what the LLM is outputting
3. Enable debug logging to see extraction attempts
4. Check the agent's graph includes proper routing

### Debug Logging

```python
import logging
logging.getLogger("haive.agents.base.mixins.execution_mixin").setLevel(logging.DEBUG)
```

## Future Enhancements

1. **Streaming Support** - Extract structured output from streams
2. **Partial Extraction** - Handle incomplete outputs
3. **Multiple Models** - Support multiple output models
4. **Custom Fields** - Allow custom field name patterns
