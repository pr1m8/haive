# Multi-Agent Reflection API Reference

**Version**: 1.0  
**Last Updated**: 2025-01-21

## 📚 Table of Contents

- [MultiAgentReflection](#multiagentreflection)
- [Models](#models)
- [Factory Functions](#factory-functions)
- [Exceptions](#exceptions)
- [Type Definitions](#type-definitions)

## MultiAgentReflection

### Class Definition

```python
class MultiAgentReflection:
    """Multi-agent reflection system using sequential coordination."""
```

### Constructor

```python
def __init__(
    self,
    name: str = "reflection_system",
    engine_config: Optional[AugLLMConfig] = None,
    tools: Optional[List[Tool]] = None,
    include_improvement: bool = False,
    reflection_temperature: float = 0.3,
    main_temperature: float = 0.7
) -> None
```

**Parameters:**

- `name` (str): Name for the multi-agent system. Default: "reflection_system"
- `engine_config` (Optional[AugLLMConfig]): Base engine configuration. If None, uses default AugLLMConfig
- `tools` (Optional[List[Tool]]): Tools available to the main ReactAgent. Default: None
- `include_improvement` (bool): Whether to include an improvement agent. Default: False
- `reflection_temperature` (float): Temperature for reflection agents (lower for consistency). Default: 0.3
- `main_temperature` (float): Temperature for main agent. Default: 0.7

**Raises:**

- `ValidationError`: If engine_config is invalid
- `ImportError`: If required dependencies are missing

**Example:**

```python
from haive.agents.reflection import MultiAgentReflection
from haive.core.engine.aug_llm import AugLLMConfig

config = AugLLMConfig(temperature=0.1, max_tokens=1000)
reflection_system = MultiAgentReflection(
    name="my_reflection",
    engine_config=config,
    include_improvement=True,
    reflection_temperature=0.2
)
```

### Methods

#### reflect_on_task

```python
async def reflect_on_task(
    self,
    task: str,
    debug: bool = False
) -> ReflectionResult
```

Perform reflection on a task using the multi-agent system.

**Parameters:**

- `task` (str): The task to process and reflect on
- `debug` (bool): Whether to enable debug output. Default: False

**Returns:**

- `ReflectionResult`: Complete reflection result with original response, grade, and optional improvement

**Raises:**

- `ValueError`: If task is empty or invalid
- `RuntimeError`: If agent execution fails
- `ValidationError`: If reflection grade validation fails

**Example:**

```python
result = await reflection_system.reflect_on_task(
    "Explain machine learning to a 10-year-old",
    debug=True
)

print(f"Quality Score: {result.reflection_grade.quality_score}/10")
print(f"Improvements: {result.reflection_grade.improvements}")
```

### Properties

#### main_agent

```python
@property
def main_agent(self) -> ReactAgent
```

The ReactAgent responsible for initial task processing.

**Returns:**

- `ReactAgent`: The main processing agent

#### reflection_agent

```python
@property
def reflection_agent(self) -> SimpleAgent
```

The SimpleAgent responsible for reflection and grading.

**Returns:**

- `SimpleAgent`: The reflection agent with structured output

#### improvement_agent

```python
@property
def improvement_agent(self) -> Optional[SimpleAgent]
```

The optional SimpleAgent for creating improved responses.

**Returns:**

- `Optional[SimpleAgent]`: The improvement agent if include_improvement=True, None otherwise

#### multi_agent

```python
@property
def multi_agent(self) -> EnhancedMultiAgent
```

The EnhancedMultiAgent coordinating the reflection workflow.

**Returns:**

- `EnhancedMultiAgent`: The multi-agent coordinator

### Private Methods

#### \_transform_messages_for_reflection

```python
def _transform_messages_for_reflection(
    self,
    messages: List[BaseMessage]
) -> List[BaseMessage]
```

Transform messages for reflection analysis (AI→Human conversion).

#### \_create_reflection_prompt

```python
def _create_reflection_prompt(
    self,
    original_task: str,
    agent_response: str,
    transformed_conversation: List[BaseMessage]
) -> str
```

Create the reflection prompt with transformed conversation context.

#### \_create_improvement_prompt

```python
def _create_improvement_prompt(
    self,
    original_task: str,
    original_response: str,
    reflection_grade: ReflectionGrade
) -> str
```

Create prompt for improvement based on reflection analysis.

#### \_extract_insights

```python
def _extract_insights(self, reflection_grade: ReflectionGrade) -> str
```

Extract key insights from the reflection grade for summary.

## Models

### ReflectionGrade

```python
class ReflectionGrade(BaseModel):
    """Structured output for reflection grading."""
```

**Fields:**

- `quality_score: int` - Quality rating from 1-10 (required)
- `reasoning_clarity: int` - How clear the reasoning is, 1-10 (required)
- `action_appropriateness: int` - How appropriate actions were, 1-10 (required)
- `improvements: List[str]` - Specific areas for improvement (default: [])
- `strengths: List[str]` - What was done well (default: [])
- `overall_assessment: str` - Overall assessment of performance (required)

**Validation:**

- All scores must be between 1 and 10 (inclusive)
- `overall_assessment` must be non-empty

**Example:**

```python
grade = ReflectionGrade(
    quality_score=8,
    reasoning_clarity=9,
    action_appropriateness=7,
    improvements=["Add more examples", "Simplify technical terms"],
    strengths=["Clear structure", "Good analogies"],
    overall_assessment="Well-structured explanation with room for simplification"
)
```

### ReflectionResult

```python
class ReflectionResult(BaseModel):
    """Result from the reflection multi-agent."""
```

**Fields:**

- `initial_response: str` - Original agent response (required)
- `reflection_grade: ReflectionGrade` - Graded reflection (required)
- `improved_response: Optional[str]` - Optional improved response (default: None)
- `reflection_insights: str` - Key insights from reflection (required)

**Example:**

```python
result = ReflectionResult(
    initial_response="Machine learning is...",
    reflection_grade=grade,
    improved_response="Machine learning is like teaching...",
    reflection_insights="Quality: 8/10 | Reasoning: 9/10 | Action: 7/10"
)
```

## Factory Functions

### create_simple_reflection_system

```python
def create_simple_reflection_system(
    tools: Optional[List[Tool]] = None,
    engine_config: Optional[AugLLMConfig] = None
) -> MultiAgentReflection
```

Create a simple reflection system with ReactAgent + ReflectionAgent.

**Parameters:**

- `tools` (Optional[List[Tool]]): Tools for the ReactAgent. Default: None
- `engine_config` (Optional[AugLLMConfig]): Base engine configuration. Default: None

**Returns:**

- `MultiAgentReflection`: Configured reflection system without improvement

**Example:**

```python
from haive.agents.reflection import create_simple_reflection_system
from langchain_core.tools import Tool

def calculator(expr: str) -> str:
    return str(eval(expr))

calc_tool = Tool(name="calculator", description="Calculate expressions", func=calculator)

system = create_simple_reflection_system(
    tools=[calc_tool],
    engine_config=AugLLMConfig(temperature=0.1)
)
```

### create_full_reflection_system

```python
def create_full_reflection_system(
    tools: Optional[List[Tool]] = None,
    engine_config: Optional[AugLLMConfig] = None
) -> MultiAgentReflection
```

Create a full reflection system with ReactAgent + ReflectionAgent + ImprovementAgent.

**Parameters:**

- `tools` (Optional[List[Tool]]): Tools for the ReactAgent. Default: None
- `engine_config` (Optional[AugLLMConfig]): Base engine configuration. Default: None

**Returns:**

- `MultiAgentReflection`: Configured reflection system with improvement capability

**Example:**

```python
from haive.agents.reflection import create_full_reflection_system

full_system = create_full_reflection_system(
    tools=[calc_tool],
    engine_config=AugLLMConfig(temperature=0.1)
)

result = await full_system.reflect_on_task("Complex calculation task")
if result.improved_response:
    print("Improvement generated!")
```

## Exceptions

### Common Exceptions

#### ValidationError

Raised when Pydantic model validation fails.

```python
try:
    grade = ReflectionGrade(quality_score=15)  # Invalid: > 10
except ValidationError as e:
    print(f"Validation error: {e}")
```

#### RuntimeError

Raised when agent execution fails.

```python
try:
    result = await reflection_system.reflect_on_task("")  # Empty task
except RuntimeError as e:
    print(f"Execution error: {e}")
```

#### ImportError

Raised when required dependencies are missing.

```python
try:
    from haive.agents.reflection import MultiAgentReflection
except ImportError as e:
    print(f"Missing dependency: {e}")
```

## Type Definitions

### Common Types

```python
from typing import List, Optional, Dict, Any
from langchain_core.tools import Tool
from langchain_core.messages import BaseMessage
from haive.core.engine.aug_llm import AugLLMConfig

# Tool type for ReactAgent
ToolList = List[Tool]

# Engine configuration
EngineConfig = AugLLMConfig

# Message transformation
MessageList = List[BaseMessage]

# Reflection context
ReflectionContext = Dict[str, Any]
```

### Agent Types

```python
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent
from haive.agents.multi.enhanced_multi_agent_v3 import EnhancedMultiAgent

# Main agent types used in reflection
MainAgent = ReactAgent
ReflectionAgent = SimpleAgent
CoordinatorAgent = EnhancedMultiAgent
```

## Usage Patterns

### Basic Pattern

```python
# 1. Create system
system = create_simple_reflection_system()

# 2. Reflect on task
result = await system.reflect_on_task("Your task here")

# 3. Access results
print(f"Score: {result.reflection_grade.quality_score}")
```

### Advanced Pattern

```python
# 1. Custom configuration
config = AugLLMConfig(
    temperature=0.1,
    max_tokens=1500,
    model="gpt-4o"
)

# 2. With tools
tools = [calculator_tool, search_tool]

# 3. Full system
system = create_full_reflection_system(
    tools=tools,
    engine_config=config
)

# 4. Detailed reflection
result = await system.reflect_on_task(
    "Complex multi-step problem",
    debug=True
)

# 5. Process results
if result.reflection_grade.quality_score < 8:
    print("Improvement available!")
    print(result.improved_response)
```

### Error Handling Pattern

```python
try:
    result = await system.reflect_on_task(task, debug=True)

    # Validate quality
    if result.reflection_grade.quality_score >= 8:
        return result.initial_response
    else:
        return result.improved_response or result.initial_response

except ValidationError as e:
    logger.error(f"Model validation failed: {e}")
    return None

except RuntimeError as e:
    logger.error(f"Agent execution failed: {e}")
    return None
```

---

**Note**: This API reference covers the core functionality. For implementation details and examples, see the [README](README.md) and test files.
