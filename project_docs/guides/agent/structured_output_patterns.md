# Structured Output Patterns in Haive

**Version**: 1.0  
**Purpose**: Design patterns and best practices for structured output in agent workflows  
**Last Updated**: 2025-01-18

## 🎯 Overview

This guide presents proven patterns for implementing structured output in Haive agents, from simple conversions to complex multi-agent workflows with type-safe data flow.

## 🏗️ Core Patterns

### 1. Sequential Structuring Pattern

The most common pattern: Agent → StructuredOutputAgent

```python
from haive.agents.react import ReactAgent
from haive.agents.structured import StructuredOutputAgent
from pydantic import BaseModel, Field

# Define output structure
class AnalysisResult(BaseModel):
    summary: str
    confidence: float = Field(ge=0.0, le=1.0)
    key_findings: List[str]
    recommendations: List[str]

# Create analysis workflow
analyst = ReactAgent(
    name="analyst",
    engine=AugLLMConfig(),
    tools=[data_analysis_tool]
)

structurer = StructuredOutputAgent(
    name="analyst_structurer",
    output_model=AnalysisResult,
    custom_context="Extract all findings and recommendations"
)

# Execute sequentially
raw_analysis = analyst.run("Analyze customer churn data")
structured_result = structurer.run(raw_analysis)

# Type-safe access
print(f"Confidence: {structured_result.confidence}")
for finding in structured_result.key_findings:
    print(f"- {finding}")
```

### 2. Paired Agent Pattern

Using `with_structured_output()` for automatic pairing:

```python
# Create paired agents in one call
researcher, research_structurer = ReactAgent.with_structured_output(
    output_model=ResearchResult,
    name="researcher",
    engine=AugLLMConfig(),
    tools=[web_search, document_reader]
)

# Use in multi-agent state
class ResearchWorkflow(MultiAgentState):
    topic: str = ""
    # ResearchResult fields
    summary: str = ""
    sources: List[str] = Field(default_factory=list)
    confidence: float = 0.0

state = ResearchWorkflow(
    agents=[researcher, research_structurer],
    topic="AI safety research"
)

# Both agents work together automatically
```

### 3. Tool Structuring Pattern

Agents as structured tools for composition:

```python
# Create structured analysis tool
analysis_tool = DataAnalyst.as_structured_tool(
    output_model=AnalysisResult,
    name="analyze_data",
    description="Analyze data and return structured insights"
)

# Use in coordinator agent
coordinator = ReactAgent(
    name="project_manager",
    engine=AugLLMConfig(),
    tools=[analysis_tool, planning_tool, reporting_tool]
)

# Coordinator gets typed results from tools
result = coordinator.run("Analyze Q4 sales data")
# Tools return AnalysisResult instances
```

### 4. Conditional Structuring Pattern

Structure output only when needed:

```python
class SmartAgent(SimpleAgent):
    """Agent that structures output conditionally."""

    def run(self, input_text: str) -> Any:
        # Get raw output
        raw_output = super().run(input_text)

        # Check if structuring is needed
        if self._needs_structuring(input_text):
            return self.ensure_structured_output(
                raw_output,
                self.get_output_model(input_text),
                handle_errors=True
            )

        return raw_output

    def _needs_structuring(self, input_text: str) -> bool:
        """Determine if output should be structured."""
        keywords = ["analyze", "report", "summarize", "extract"]
        return any(keyword in input_text.lower() for keyword in keywords)

    def get_output_model(self, input_text: str) -> Type[BaseModel]:
        """Select appropriate output model based on input."""
        if "analyze" in input_text.lower():
            return AnalysisResult
        elif "report" in input_text.lower():
            return ReportOutput
        else:
            return GenericStructuredOutput
```

### 5. Multi-Model Pattern

Handle multiple output types in one workflow:

```python
from typing import Union

# Define multiple output models
class SuccessResult(BaseModel):
    status: Literal["success"] = "success"
    data: Dict[str, Any]
    message: str

class ErrorResult(BaseModel):
    status: Literal["error"] = "error"
    error_code: str
    error_message: str
    retry_after: Optional[int] = None

class WarningResult(BaseModel):
    status: Literal["warning"] = "warning"
    warnings: List[str]
    partial_data: Optional[Dict[str, Any]] = None

# Union type for all possible outputs
ProcessResult = Union[SuccessResult, ErrorResult, WarningResult]

# Create processor with union handling
processor = StructuredOutputAgent(
    name="result_processor",
    output_model=ProcessResult,  # Handles union types
    custom_context="Determine the appropriate status type"
)

# Process various outputs
outputs = [
    "Success! Found 42 matching records.",
    "Error: Database connection timeout (code: DB_TIMEOUT)",
    "Warning: Some records were skipped due to validation"
]

for output in outputs:
    result = processor.run(output)

    # Type narrowing
    if isinstance(result, SuccessResult):
        print(f"✅ {result.message}")
    elif isinstance(result, ErrorResult):
        print(f"❌ {result.error_code}: {result.error_message}")
    elif isinstance(result, WarningResult):
        print(f"⚠️ Warnings: {result.warnings}")
```

## 🔄 Advanced Patterns

### 1. Cascading Structure Pattern

Progressive refinement through multiple agents:

```python
# Level 1: Basic structure
basic_structurer = StructuredOutputAgent(
    name="basic_structurer",
    output_model=GenericStructuredOutput
)

# Level 2: Domain-specific structure
domain_structurer = StructuredOutputAgent(
    name="domain_structurer",
    output_model=DomainSpecificOutput,
    custom_context="Apply domain knowledge for medical terms"
)

# Level 3: Final validation and enrichment
final_structurer = StructuredOutputAgent(
    name="final_structurer",
    output_model=ValidatedOutput,
    custom_context="Ensure all required fields are complete"
)

# Cascade through levels
raw_output = analyst.run("Analyze patient data")
level1 = basic_structurer.run(raw_output)
level2 = domain_structurer.run(str(level1))
final = final_structurer.run(str(level2))
```

### 2. Parallel Structuring Pattern

Multiple structures from one source:

```python
import asyncio

async def parallel_structure(raw_output: str):
    """Extract multiple structures in parallel."""

    # Define extractors
    summary_extractor = StructuredOutputAgent(
        name="summary_extractor",
        output_model=SummaryOutput
    )

    metrics_extractor = StructuredOutputAgent(
        name="metrics_extractor",
        output_model=MetricsOutput
    )

    entities_extractor = StructuredOutputAgent(
        name="entities_extractor",
        output_model=EntitiesOutput
    )

    # Run in parallel
    summary_task = summary_extractor.arun(raw_output)
    metrics_task = metrics_extractor.arun(raw_output)
    entities_task = entities_extractor.arun(raw_output)

    summary, metrics, entities = await asyncio.gather(
        summary_task, metrics_task, entities_task
    )

    return {
        "summary": summary,
        "metrics": metrics,
        "entities": entities
    }
```

### 3. Schema Evolution Pattern

Handle changing output requirements:

```python
from pydantic import BaseModel, Field, root_validator

class VersionedOutput(BaseModel):
    """Base class for versioned outputs."""
    version: str = Field(default="1.0")

    @root_validator
    def migrate_if_needed(cls, values):
        """Migrate old schema to new format."""
        version = values.get("version", "1.0")

        if version == "1.0" and cls.__name__ == "OutputV2":
            # Migrate v1 to v2
            values["new_field"] = values.get("old_field", "default")
            values["version"] = "2.0"

        return values

class OutputV1(VersionedOutput):
    """Version 1 output schema."""
    summary: str
    score: float

class OutputV2(VersionedOutput):
    """Version 2 with additional fields."""
    summary: str
    score: float
    confidence: float = Field(default=0.5)
    metadata: Dict[str, Any] = Field(default_factory=dict)

# Automatic version handling
def get_output_model(version: str) -> Type[VersionedOutput]:
    """Get appropriate model version."""
    models = {
        "1.0": OutputV1,
        "2.0": OutputV2
    }
    return models.get(version, OutputV2)  # Default to latest
```

### 4. Context-Aware Structuring

Structure based on conversation context:

```python
class ContextAwareStructurer(StructuredOutputAgent):
    """Structurer that adapts based on context."""

    def get_custom_prompt(self, state: MessagesState) -> ChatPromptTemplate:
        """Generate context-aware prompt."""

        # Analyze conversation history
        last_human = state.get_last_human_message()
        has_technical = any(
            word in last_human.content.lower()
            for word in ["api", "database", "algorithm"]
        )

        if has_technical:
            context = "Focus on technical details and implementation"
        else:
            context = "Focus on business value and outcomes"

        return ChatPromptTemplate.from_template(f"""
        Extract structured information from the following text.
        Context: {context}

        Text: {{input}}

        Structure the output according to: {{format_instructions}}
        """)
```

### 5. Validation Pipeline Pattern

Ensure output quality through validation:

```python
from typing import Protocol

class OutputValidator(Protocol):
    """Protocol for output validators."""
    def validate(self, output: BaseModel) -> Tuple[bool, List[str]]:
        """Validate output and return (is_valid, errors)."""
        ...

class BusinessRuleValidator:
    """Validate against business rules."""

    def validate(self, output: AnalysisResult) -> Tuple[bool, List[str]]:
        errors = []

        if output.confidence < 0.7 and len(output.recommendations) > 0:
            errors.append("Low confidence but has recommendations")

        if not output.sources:
            errors.append("No sources provided")

        return len(errors) == 0, errors

class StructuredOutputPipeline:
    """Pipeline with validation stages."""

    def __init__(
        self,
        structurer: StructuredOutputAgent,
        validators: List[OutputValidator]
    ):
        self.structurer = structurer
        self.validators = validators

    def process(self, raw_output: str) -> Tuple[Optional[BaseModel], List[str]]:
        """Process with validation."""

        # Structure the output
        structured = self.structurer.run(raw_output)

        # Validate
        all_errors = []
        for validator in self.validators:
            is_valid, errors = validator.validate(structured)
            all_errors.extend(errors)

        if all_errors:
            return None, all_errors

        return structured, []
```

## 📋 Pattern Selection Guide

### When to Use Each Pattern

| Pattern          | Use When                             | Example                      |
| ---------------- | ------------------------------------ | ---------------------------- |
| Sequential       | Need to structure any agent's output | Analysis → Report            |
| Paired           | Want automatic structuring setup     | Research + Structure         |
| Tool             | Composing agents as tools            | Coordinator using analysts   |
| Conditional      | Structure only specific outputs      | Chat vs Analysis             |
| Multi-Model      | Multiple output types possible       | Success/Error/Warning        |
| Cascading        | Progressive refinement needed        | Raw → Basic → Detailed       |
| Parallel         | Multiple structures from one source  | Summary + Metrics + Entities |
| Schema Evolution | Output format changes over time      | API versioning               |
| Context-Aware    | Structure depends on context         | Technical vs Business        |
| Validation       | Quality assurance required           | Production systems           |

## 🎯 Best Practices

### 1. Design Output Models First

```python
# ✅ GOOD - Clear, focused models
class TaskResult(BaseModel):
    """Result of a single task execution."""
    task_id: str = Field(description="Unique task identifier")
    status: Literal["pending", "running", "completed", "failed"]
    result: Optional[str] = None
    error: Optional[str] = None
    duration_seconds: float = Field(ge=0)

# ❌ BAD - Vague, kitchen-sink model
class Result(BaseModel):
    data: Any
    extra: Dict
    stuff: List
```

### 2. Use Descriptive Field Names

```python
# ✅ GOOD - Self-documenting
class MetricsReport(BaseModel):
    total_revenue_usd: float
    conversion_rate_percentage: float
    average_order_value_usd: float
    customer_acquisition_cost_usd: float

# ❌ BAD - Ambiguous
class Metrics(BaseModel):
    revenue: float  # In what currency?
    rate: float     # What rate?
    aov: float      # What's aov?
    cac: float      # Unclear acronym
```

### 3. Always Provide Context

```python
# ✅ GOOD - Context helps extraction
structurer = StructuredOutputAgent(
    output_model=FinancialReport,
    custom_context="""
    Extract financial metrics with the following guidelines:
    - All monetary values should be in USD
    - Percentages should be 0-100, not decimals
    - Include source document references
    """
)

# ❌ BAD - No guidance
structurer = StructuredOutputAgent(output_model=FinancialReport)
```

### 4. Handle Edge Cases

```python
# ✅ GOOD - Robust handling
def structure_with_fallback(raw_output: str, model: Type[BaseModel]):
    """Structure with multiple fallback strategies."""

    # Try primary structurer
    try:
        structurer = StructuredOutputAgent(output_model=model)
        return structurer.run(raw_output)
    except Exception as e:
        logger.warning(f"Primary structuring failed: {e}")

    # Try with relaxed model
    try:
        relaxed_model = create_relaxed_version(model)
        structurer = StructuredOutputAgent(output_model=relaxed_model)
        result = structurer.run(raw_output)
        # Convert back to strict model with defaults
        return model(**result.dict())
    except Exception as e:
        logger.error(f"Fallback structuring failed: {e}")

    # Return minimal valid instance
    return create_minimal_instance(model)
```

### 5. Monitor and Improve

```python
# Track structuring success
class StructuringMetrics:
    def __init__(self):
        self.attempts = 0
        self.successes = 0
        self.failures = defaultdict(int)

    def record_attempt(self, model: Type[BaseModel], success: bool, error: Optional[str] = None):
        self.attempts += 1
        if success:
            self.successes += 1
        else:
            self.failures[error or "unknown"] += 1

    def get_success_rate(self) -> float:
        return self.successes / self.attempts if self.attempts > 0 else 0.0

    def get_common_errors(self) -> List[Tuple[str, int]]:
        return sorted(self.failures.items(), key=lambda x: x[1], reverse=True)
```

## 🔗 Integration with Haive Ecosystem

### With State Management

```python
# State automatically populated from structured output
class WorkflowState(MultiAgentState):
    # Matches AnalysisResult fields
    summary: str = ""
    confidence: float = 0.0
    key_findings: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)

# Structurer updates state directly
state.agents = [analyst, structurer]
# After execution, state fields are populated
```

### With Memory Systems

```python
# Store structured outputs in memory
memory = ConversationBufferMemory()

# Structured output for consistent storage
result = structurer.run(analysis)
memory.save_context(
    {"input": query},
    {"output": result.model_dump_json()}
)
```

### With Tool Systems

```python
# Tools can expect structured inputs
@tool
def process_analysis(analysis: AnalysisResult) -> str:
    """Process a structured analysis result."""
    if analysis.confidence > 0.8:
        return f"High confidence analysis: {analysis.summary}"
    else:
        return "Need more data for confident analysis"

# Agent uses tool with structured data
agent = ReactAgent(tools=[process_analysis])
```

## 📚 Further Reading

- [StructuredOutputAgent API](../../reference/api/structured_output_agent.md)
- [Handling Output Formats](handling_output_formats.md)
- [Multi-Agent Workflows](multi/README.md)
- [Pydantic Best Practices](/project_docs/active/standards/coding/PYDANTIC_PATTERNS.md)

---

**Remember**: Good structured output design makes your agents more reliable, maintainable, and composable. Always start with clear output models and use the appropriate pattern for your use case.
