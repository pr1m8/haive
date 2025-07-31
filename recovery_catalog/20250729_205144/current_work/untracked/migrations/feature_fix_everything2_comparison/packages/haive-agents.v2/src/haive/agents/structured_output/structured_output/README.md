# Structured Output Agent

Agent that produces structured, typed outputs using Pydantic models.

## Overview

The Structured Output Agent extends SimpleAgent to provide:

- Type-safe output generation using Pydantic models
- Automatic validation of generated outputs
- Clean integration with multi-agent workflows
- Support for complex nested structures

## Key Features

- **Pydantic Model Support**: Define output schemas with full validation
- **Type Safety**: Ensures outputs match expected structure
- **Validation**: Automatic validation with helpful error messages
- **Flexibility**: Support for simple and complex data structures
- **Multi-Agent Ready**: Perfect for cross-agent data flow

## Usage Examples

### Basic Structured Output

```python
from haive.agents.structured_output import StructuredOutputAgent
from pydantic import BaseModel, Field
from typing import List

class AnalysisResult(BaseModel):
    """Structured analysis output."""
    summary: str = Field(description="Brief summary of findings")
    confidence: float = Field(ge=0, le=1, description="Confidence score")
    key_points: List[str] = Field(description="Key findings")
    recommendation: str = Field(description="Recommended action")

# Create agent with structured output
agent = StructuredOutputAgent(
    name="analyzer",
    engine=AugLLMConfig(),
    output_model=AnalysisResult
)

# Get structured result
result = await agent.arun("Analyze the Q4 sales data and provide recommendations")
# result is AnalysisResult instance with validated fields
print(f"Summary: {result.summary}")
print(f"Confidence: {result.confidence}")
```

### Complex Nested Structures

```python
from datetime import datetime
from typing import List, Optional

class TaskItem(BaseModel):
    """Individual task."""
    title: str
    priority: str = Field(pattern="^(high|medium|low)$")
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = None

class ProjectPlan(BaseModel):
    """Complete project plan."""
    project_name: str
    description: str
    tasks: List[TaskItem]
    estimated_hours: float
    risks: List[str]

agent = StructuredOutputAgent(
    name="project_planner",
    engine=AugLLMConfig(
        system_message="You are a project planning expert"
    ),
    output_model=ProjectPlan
)

plan = await agent.arun("Create a project plan for building a mobile app")
# plan is fully validated ProjectPlan instance
```

### Multi-Agent Structured Flow

```python
# Research agent produces structured findings
class ResearchFindings(BaseModel):
    sources: List[str]
    facts: List[str]
    confidence_level: float

research_agent = StructuredOutputAgent(
    name="researcher",
    output_model=ResearchFindings
)

# Writer agent consumes structured input
class Article(BaseModel):
    title: str
    introduction: str
    body: List[str]
    conclusion: str
    citations: List[str]

writer_agent = StructuredOutputAgent(
    name="writer",
    output_model=Article
)

# Chain agents with structured data flow
findings = await research_agent.arun("Research renewable energy trends")
article = await writer_agent.arun(
    f"Write an article based on: {findings.model_dump_json()}"
)
```

## Configuration

### Output Model Definition

```python
class MyOutput(BaseModel):
    # Use Field for validation and documentation
    name: str = Field(..., min_length=1, max_length=100)

    # Numeric constraints
    score: float = Field(ge=0, le=100)

    # Enums and patterns
    status: str = Field(pattern="^(active|inactive|pending)$")

    # Complex types
    tags: List[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    # Model config
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )
```

### Agent Configuration

```python
agent = StructuredOutputAgent(
    name="structured_agent",
    engine=AugLLMConfig(
        temperature=0.1,  # Lower temperature for consistent structure
        system_message="""Generate structured outputs that match the schema.
        Be precise and ensure all required fields are populated correctly."""
    ),
    output_model=MyOutput,
    retry_on_validation_error=True,  # Retry if validation fails
    max_retries=3  # Maximum validation retries
)
```

## Best Practices

1. **Clear Field Descriptions**: Use Field descriptions to guide the LLM
2. **Appropriate Constraints**: Set reasonable validation constraints
3. **Error Handling**: Handle validation errors gracefully
4. **Schema Documentation**: Document models thoroughly for clarity
5. **Testing**: Test with various inputs to ensure robustness

## Error Handling

```python
from pydantic import ValidationError

try:
    result = await agent.arun("Generate analysis")
except ValidationError as e:
    print(f"Output validation failed: {e}")
    # Handle specific field errors
    for error in e.errors():
        print(f"Field {error['loc']}: {error['msg']}")
```

## Testing

```bash
# Run structured output tests
poetry run pytest packages/haive-agents/tests/structured_output/ -v

# Test specific models
poetry run pytest packages/haive-agents/tests/structured_output/test_models.py -v
```

## Common Use Cases

- **Data Extraction**: Extract structured data from unstructured text
- **Report Generation**: Create consistent, structured reports
- **API Responses**: Generate type-safe API response objects
- **Multi-Agent Coordination**: Pass structured data between agents
- **Form Processing**: Convert natural language to form data

## See Also

- [SimpleAgent](../simple/README.md) - Base agent class
- [MultiAgent](../multi/README.md) - Multi-agent coordination
- [Pydantic Documentation](https://docs.pydantic.dev/) - Model validation
