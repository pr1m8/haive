# StructuredOutputAgent Guide

**Version**: 1.0
**Purpose**: Complete guide to using StructuredOutputAgent for type-safe agent outputs
**Last Updated**: 2025-01-18

## 🎯 Overview

StructuredOutputAgent is a specialized agent that converts unstructured text into validated Pydantic models. It's designed to work seamlessly in multi-agent workflows, providing type-safe data extraction and transformation.

## 🏗️ Architecture

```
Input (Any Format) → StructuredOutputAgent → Pydantic Model Output
                           ↓
                    Tool-based extraction (v2)
                           ↓
                    Validated, typed data
```

### Key Features

- **Universal Input Handling**: Accepts strings, messages, dicts, or any format
- **Tool-Based Extraction**: Always uses reliable v2 extraction
- **Type Safety**: Outputs validated Pydantic models
- **Multi-Agent Ready**: Designed for sequential workflows
- **Custom Context**: Configurable extraction instructions
- **Error Handling**: Graceful fallbacks for failed extractions

## 📋 Basic Usage

### Simple Example

```python
from haive.agents.structured import StructuredOutputAgent
from pydantic import BaseModel, Field
from typing import List

# Define your output structure
class ProjectSummary(BaseModel):
    title: str = Field(description="Project title")
    status: str = Field(description="Current status")
    progress: float = Field(ge=0.0, le=100.0)
    blockers: List[str] = Field(default_factory=list)
    next_steps: List[str] = Field(default_factory=list)

# Create the agent
structurer = StructuredOutputAgent(
    name="project_structurer",
    output_model=ProjectSummary,
    custom_context="Extract project management details"
)

# Convert unstructured text
unstructured = """
The DataSync project is currently in development phase with about 75% completion.
We're blocked by API rate limits and pending security review. Next steps include
finalizing the authentication module and beginning integration testing.
"""

result = structurer.run(unstructured)

print(f"Title: {result.title}")
print(f"Progress: {result.progress}%")
print(f"Blockers: {result.blockers}")
```

### Using Built-in Models

```python
from haive.agents.structured import (
    GenericStructuredOutput,
    AnalysisOutput,
    TaskOutput
)

# Generic extraction
generic_structurer = StructuredOutputAgent(
    name="generic",
    output_model=GenericStructuredOutput
)

# Analysis-specific
analysis_structurer = StructuredOutputAgent(
    name="analyzer",
    output_model=AnalysisOutput,
    custom_context="Focus on evidence and confidence levels"
)

# Task management
task_structurer = StructuredOutputAgent(
    name="task_manager",
    output_model=TaskOutput
)
```

## 🔄 Multi-Agent Workflows

### Sequential Pattern

The most common pattern: Any Agent → StructuredOutputAgent

```python
from haive.agents.react import ReactAgent
from haive.agents.simple import SimpleAgent
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState

# Define workflow state
class AnalysisWorkflow(MultiAgentState):
    # Input
    query: str = ""

    # Output fields (match your model)
    summary: str = ""
    findings: List[str] = Field(default_factory=list)
    confidence_score: float = 0.0
    recommendations: List[str] = Field(default_factory=list)

# Create agents
analyst = ReactAgent(
    name="analyst",
    engine=AugLLMConfig(),
    tools=[data_tool, search_tool]
)

structurer = StructuredOutputAgent(
    name="analysis_structurer",
    output_model=AnalysisOutput
)

# Setup workflow
state = AnalysisWorkflow(
    agents=[analyst, structurer],
    query="Analyze customer satisfaction trends"
)

# Execute (using nodes)
from haive.core.graph.node.agent_node_v3 import create_agent_node_v3

analyst_node = create_agent_node_v3("analyst")
structurer_node = create_agent_node_v3("analysis_structurer")

# Run sequentially
result1 = analyst_node(state, config)
result2 = structurer_node(state, config)

# State now has structured fields populated
print(f"Summary: {state.summary}")
print(f"Confidence: {state.confidence_score}")
```

### With SimpleAgent

```python
# SimpleAgent with custom logic
processor = SimpleAgent(
    name="data_processor",
    engine=AugLLMConfig(
        system_message="Process and analyze data comprehensively"
    )
)

# Structure the output
structurer = StructuredOutputAgent(
    name="processor_structurer",
    output_model=ProcessingResult,
    custom_context="Extract all metrics and insights"
)

# Chain execution
raw_result = processor.run("Process Q4 sales data")
structured = structurer.run(raw_result)
```

## 🎨 Custom Output Models

### Best Practices for Model Design

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Literal
from datetime import datetime

class ComprehensiveReport(BaseModel):
    """Well-designed output model with validation."""

    # Metadata
    report_id: str = Field(description="Unique report identifier")
    generated_at: datetime = Field(default_factory=datetime.now)
    report_type: Literal["analysis", "summary", "detailed"] = "analysis"

    # Core content
    executive_summary: str = Field(
        ...,
        min_length=50,
        max_length=500,
        description="Brief executive summary"
    )

    # Structured data
    key_metrics: Dict[str, float] = Field(
        default_factory=dict,
        description="Numerical metrics extracted"
    )

    findings: List[str] = Field(
        default_factory=list,
        min_items=1,
        description="Key findings from analysis"
    )

    # Optional fields
    confidence_level: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Confidence in findings (0-1)"
    )

    data_sources: List[str] = Field(
        default_factory=list,
        description="Data sources used"
    )

    # Validation
    @validator('key_metrics')
    def validate_metrics(cls, v):
        """Ensure metrics are reasonable."""
        for key, value in v.items():
            if value < 0:
                raise ValueError(f"Metric {key} cannot be negative")
        return v

    @validator('findings')
    def validate_findings(cls, v):
        """Ensure findings are substantial."""
        cleaned = [f.strip() for f in v if f.strip()]
        if not cleaned:
            raise ValueError("At least one finding required")
        return cleaned
```

### Using the Custom Model

```python
# Create specialized structurer
report_structurer = StructuredOutputAgent(
    name="report_structurer",
    output_model=ComprehensiveReport,
    custom_context="""
    Extract a comprehensive report with:
    - Executive summary (50-500 chars)
    - All numerical metrics as key_metrics
    - At least one finding
    - Confidence level if mentioned
    - Any data sources referenced
    """
)

# Process complex input
complex_input = """
Based on analysis of 10,000 customer records from our CRM and survey data:

Executive Summary: Customer satisfaction has increased by 15% QoQ, driven
primarily by improved response times and product quality enhancements.

Key Metrics:
- Satisfaction Score: 4.2/5.0 (up from 3.65)
- Response Time: 2.4 hours average (down from 5.8)
- Retention Rate: 89% (up from 82%)
- NPS: 67 (up from 45)

Our findings indicate:
1. Faster response times correlate strongly with satisfaction
2. Product quality improvements had the highest impact
3. Mobile app users show 20% higher satisfaction

Confidence in these findings is high (approximately 0.85) given the
large sample size and consistent patterns across segments.
"""

report = report_structurer.run(complex_input)

# Access structured data
print(f"Report ID: {report.report_id}")
print(f"Summary: {report.executive_summary}")
print(f"Metrics: {report.key_metrics}")
print(f"Confidence: {report.confidence_level}")
```

## 🔧 Advanced Features

### Custom Prompts

```python
from langchain_core.prompts import ChatPromptTemplate

# Create custom extraction prompt
custom_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a specialized data extractor for financial reports.
    Focus on:
    - Monetary values (always in USD)
    - Percentage changes (as decimals)
    - Time periods (in standard format)
    - Risk factors (categorized by severity)
    """),
    ("user", "{input}"),
    ("user", "Extract into format: {format_instructions}")
])

# Use with agent
financial_structurer = StructuredOutputAgent(
    name="financial_structurer",
    output_model=FinancialReport,
    custom_prompt=custom_prompt
)
```

### Handling Different Input Types

```python
# The agent handles various input formats automatically

# String input
result1 = structurer.run("Summary: Good progress. Status: Active")

# AIMessage input
from langchain_core.messages import AIMessage
msg = AIMessage(content="Analysis complete with high confidence")
result2 = structurer.run(msg)

# Dict input
data = {"output": "Project on track", "metrics": {"progress": 0.75}}
result3 = structurer.run(data)

# Already structured (passthrough)
existing = MyModel(field1="value1", field2="value2")
result4 = structurer.run(existing)  # Returns as-is
```

### Error Handling

```python
class RobustStructuredAgent(StructuredOutputAgent):
    """Extended agent with robust error handling."""

    def run(self, input_data: Any) -> BaseModel:
        """Run with fallback strategies."""

        try:
            # Try normal extraction
            return super().run(input_data)

        except Exception as e:
            logger.warning(f"Primary extraction failed: {e}")

            # Try with relaxed prompt
            self.custom_context = "Extract whatever information is available"
            try:
                return super().run(input_data)

            except Exception as e2:
                logger.error(f"Fallback extraction failed: {e2}")

                # Return minimal valid instance
                return self.output_model(
                    **self._get_minimal_fields()
                )

    def _get_minimal_fields(self) -> dict:
        """Get minimal required fields for model."""
        required = {}
        for field_name, field in self.output_model.__fields__.items():
            if field.required:
                # Provide sensible defaults
                if field.type_ == str:
                    required[field_name] = "Unknown"
                elif field.type_ == float:
                    required[field_name] = 0.0
                elif field.type_ == list:
                    required[field_name] = []
        return required
```

## 🎯 Configuration Options

### Engine Configuration

```python
from haive.core.engine.aug_llm import AugLLMConfig

# Configure for accurate extraction
config = AugLLMConfig(
    temperature=0.1,  # Low temperature for consistency
    max_tokens=2000,  # Enough for complex structures
    system_message="You are a precise data extraction specialist."
)

structurer = StructuredOutputAgent(
    name="precise_structurer",
    output_model=DetailedOutput,
    engine=config
)
```

### Context Customization

```python
# Different contexts for different scenarios

# Technical extraction
tech_structurer = StructuredOutputAgent(
    output_model=TechnicalSpec,
    custom_context="""
    Extract technical specifications including:
    - All version numbers
    - API endpoints
    - Configuration parameters
    - Performance metrics
    Use exact values, don't approximate.
    """
)

# Business extraction
business_structurer = StructuredOutputAgent(
    output_model=BusinessMetrics,
    custom_context="""
    Extract business metrics focusing on:
    - Financial figures (with currency)
    - Growth percentages
    - Market segments
    - Strategic initiatives
    Round to reasonable precision.
    """
)
```

## 📊 Performance Considerations

### Optimization Tips

1. **Model Complexity**: Simpler models extract more reliably
2. **Context Length**: Keep custom context concise and focused
3. **Temperature**: Use low temperature (0.1-0.3) for consistency
4. **Caching**: Cache structurer instances when possible

```python
# Cached structurer for repeated use
from functools import lru_cache

@lru_cache(maxsize=10)
def get_structurer(model_name: str) -> StructuredOutputAgent:
    """Get cached structurer instance."""
    models = {
        "analysis": AnalysisOutput,
        "task": TaskOutput,
        "report": ReportOutput
    }

    return StructuredOutputAgent(
        name=f"{model_name}_structurer",
        output_model=models[model_name]
    )

# Reuse same instance
structurer = get_structurer("analysis")
```

### Batch Processing

```python
async def batch_structure(
    texts: List[str],
    output_model: Type[BaseModel]
) -> List[BaseModel]:
    """Structure multiple texts efficiently."""

    structurer = StructuredOutputAgent(
        name="batch_structurer",
        output_model=output_model
    )

    # Process in parallel
    tasks = [structurer.arun(text) for text in texts]
    results = await asyncio.gather(*tasks)

    return results
```

## 🚨 Common Issues and Solutions

### Issue 1: Incomplete Extraction

```python
# Problem: Not all fields extracted
# Solution: Provide explicit guidance

structurer = StructuredOutputAgent(
    output_model=CompleteOutput,
    custom_context="""
    Extract ALL of the following (use 'Unknown' if not found):
    - Title (required)
    - Description (required)
    - Status (required)
    - Priority (default to 'medium')
    - Tags (empty list if none)
    """
)
```

### Issue 2: Type Conversion Errors

```python
# Problem: String numbers not converting
# Solution: Add validators to model

class RobustModel(BaseModel):
    count: int
    percentage: float

    @validator('count', pre=True)
    def parse_count(cls, v):
        if isinstance(v, str):
            # Handle "5 items" -> 5
            return int(''.join(filter(str.isdigit, v)))
        return v

    @validator('percentage', pre=True)
    def parse_percentage(cls, v):
        if isinstance(v, str):
            # Handle "25%" -> 0.25
            v = v.replace('%', '')
            return float(v) / 100 if float(v) > 1 else float(v)
        return v
```

### Issue 3: Complex Nested Structures

```python
# Problem: Deeply nested data hard to extract
# Solution: Step-wise extraction

# First level
class ContactInfo(BaseModel):
    email: str
    phone: Optional[str]

class Address(BaseModel):
    street: str
    city: str
    country: str

# Main model
class Company(BaseModel):
    name: str
    contact: ContactInfo
    address: Address

# Extract with clear structure
structurer = StructuredOutputAgent(
    output_model=Company,
    custom_context="""
    Extract company information with nested structure:
    - Company name
    - Contact info (email, phone)
    - Address (street, city, country)

    Look for these in sections or paragraphs.
    """
)
```

## 🔗 Integration Examples

### With LangGraph

```python
from langgraph.graph import StateGraph, END

# Define graph with structuring step
workflow = StateGraph(AnalysisWorkflow)

# Add nodes
workflow.add_node("analyze", analyst_node)
workflow.add_node("structure", structurer_node)
workflow.add_node("validate", validator_node)

# Connect nodes
workflow.add_edge("analyze", "structure")
workflow.add_edge("structure", "validate")
workflow.add_edge("validate", END)

# Compile and run
graph = workflow.compile()
result = graph.invoke({"query": "Analyze trends"})
```

### With Memory

```python
from langchain.memory import ConversationSummaryMemory

# Structure before storing
memory = ConversationSummaryMemory()

# After agent execution
raw_output = agent.run(query)
structured = structurer.run(raw_output)

# Store structured data
memory.save_context(
    {"input": query},
    {"output": structured.model_dump_json()}
)
```

### With Tools

```python
# Create tool that returns structured data
structured_analysis_tool = ReactAgent.as_structured_tool(
    output_model=AnalysisResult,
    name="analyze_with_structure",
    description="Analyze data and return structured results"
)

# Use in another agent
coordinator = SimpleAgent(
    name="coordinator",
    tools=[structured_analysis_tool]
)
```

## 📚 API Reference

### StructuredOutputAgent

```python
class StructuredOutputAgent(SimpleAgent):
    """Agent for converting unstructured text to structured output."""

    # Required fields
    structured_output_model: Type[BaseModel]

    # Optional fields
    output_model: Type[BaseModel] = GenericStructuredOutput
    custom_context: Optional[str] = None
    custom_prompt: Optional[ChatPromptTemplate] = None

    # Always v2 (tool-based)
    structured_output_version: Literal["v2"] = "v2"
```

### Helper Functions

```python
# Create with defaults
from haive.agents.structured.agent import create_structured_agent

agent = create_structured_agent(
    output_model=MyModel,
    name="my_structurer",
    custom_context="Extract all fields"
)
```

### Built-in Models

```python
# Generic catch-all
GenericStructuredOutput(
    main_content: str,
    key_points: List[str],
    action_items: List[str],
    metadata: Dict[str, Any],
    confidence: Optional[float]
)

# Analysis-focused
AnalysisOutput(
    summary: str,
    findings: List[str],
    evidence: List[str],
    recommendations: List[str],
    confidence_score: float
)

# Task management
TaskOutput(
    task_id: str,
    title: str,
    description: str,
    status: str,
    priority: str,
    assignee: Optional[str],
    due_date: Optional[str],
    dependencies: List[str]
)
```

## 🎯 Best Practices Summary

1. **Always define clear output models** with proper validation
2. **Use descriptive field names** and descriptions
3. **Provide custom context** for better extraction
4. **Handle errors gracefully** with fallbacks
5. **Test with various input formats** before production
6. **Use low temperature** for consistent results
7. **Cache structurer instances** for performance
8. **Monitor extraction success** and iterate on prompts

## 📚 Related Documentation

- [Handling Output Formats](handling_output_formats.md)
- [Structured Output Patterns](structured_output_patterns.md)
- [Multi-Agent Workflows](multi/README.md)
- [Building Agents Guide](building_guide.md)

---

**Remember**: StructuredOutputAgent is your bridge between unstructured AI outputs and type-safe application logic. Use it to make your agent workflows more reliable and maintainable.
