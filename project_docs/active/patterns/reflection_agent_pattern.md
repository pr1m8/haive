# Reflection/Reflexion Agent Pattern

**Version**: 1.0
**Purpose**: Building reflection agents using message transformer nodes
**Last Updated**: 2025-01-16

## 🎯 Overview

The Reflection pattern enables agents to analyze and improve their own outputs through structured self-critique. This is implemented using:

1. **Message Transformer Nodes** - Transform agent outputs
2. **Structured Output Models** - Critique, Improvement, ReflectionResult
3. **Sequential Multi-Agent Pattern** - Base agent → Reflection processor

## 🏗️ Architecture

### Core Components

1. **Base Agent**: Produces initial output
2. **Reflection Processor**: Analyzes output and provides structured feedback
3. **Improvement Agent**: (Optional) Applies feedback to improve output
4. **Message Transformer**: Modifies messages based on reflection

### Reflection Models (from structured_output.models)

```python
class Critique(BaseModel):
    """Structured critique of an output."""
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    overall_quality: float  # 0.0 to 1.0
    needs_revision: bool

class Improvement(BaseModel):
    """Structured improvement suggestions."""
    original_issue: str
    proposed_solution: str
    implementation_steps: List[str]
    expected_impact: str
    priority: str  # high, medium, low

class ReflectionResult(BaseModel):
    """Complete reflection analysis."""
    summary: str
    critique: Critique
    improvements: List[Improvement]
    action_items: List[str]
    confidence: float
```

## 💻 Implementation Patterns

### 1. Basic Reflection Agent

```python
from haive.agents.simple.agent import SimpleAgent
from haive.agents.structured_output.agent import StructuredOutputAgent
from haive.agents.structured_output.models import (
    Critique, Improvement, ReflectionResult
)
from haive.agents.multi.proper_base import ProperMultiAgent
from haive.core.engine.aug_llm import AugLLMConfig

class ReflectionAgent(ProperMultiAgent):
    """Agent that reflects on its own outputs."""

    @classmethod
    def create(
        cls,
        base_agent: Agent,
        name: str = None,
        max_iterations: int = 3,
        quality_threshold: float = 0.8
    ) -> "ReflectionAgent":
        """Create a reflection agent that improves outputs iteratively.

        Args:
            base_agent: The agent whose outputs to reflect on
            name: Name for the reflection agent
            max_iterations: Maximum reflection iterations
            quality_threshold: Quality score to stop reflecting

        Returns:
            Configured ReflectionAgent
        """
        # Create reflection processor
        reflection_processor = StructuredOutputAgent.create_reflection_processor(
            reflection_models=[Critique, Improvement, ReflectionResult],
            name=f"{base_agent.name}_reflection"
        )

        # Create improvement agent
        improvement_agent = SimpleAgent(
            name=f"{base_agent.name}_improver",
            engine=AugLLMConfig(
                system_message="""You are an improvement agent.
                Take the original output and the reflection feedback,
                then produce an improved version addressing the issues raised.""",
                temperature=0.3
            )
        )

        # Return multi-agent with reflection loop
        return cls(
            name=name or f"{base_agent.name}_with_reflection",
            agents=[base_agent, reflection_processor, improvement_agent],
            execution_mode="sequential",
            # Add reflection control to state
            state_schema=type(
                "ReflectionState",
                (MessagesStateWithTokenUsage,),
                {
                    "__annotations__": {
                        "reflection_count": int,
                        "quality_scores": List[float],
                        "max_iterations": int,
                        "quality_threshold": float
                    },
                    "reflection_count": Field(default=0),
                    "quality_scores": Field(default_factory=list),
                    "max_iterations": Field(default=max_iterations),
                    "quality_threshold": Field(default=quality_threshold)
                }
            )
        )
```

### 2. Message Transformer Pattern

```python
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from typing import List, Callable

class MessageTransformerNode:
    """Node that transforms messages based on reflection results."""

    def __init__(
        self,
        transform_fn: Callable[[List[BaseMessage]], List[BaseMessage]],
        name: str = "message_transformer"
    ):
        self.transform_fn = transform_fn
        self.name = name

    def __call__(self, state: dict) -> dict:
        """Transform messages in state."""
        messages = state.get("messages", [])
        transformed = self.transform_fn(messages)
        return {"messages": transformed}

# Example transformer that adds reflection context
def add_reflection_context(messages: List[BaseMessage]) -> List[BaseMessage]:
    """Add reflection analysis to messages."""
    enhanced = []

    for msg in messages:
        enhanced.append(msg)

        # If AI message, check for reflection
        if isinstance(msg, AIMessage):
            # Look for subsequent tool messages with reflection
            reflection = find_reflection_for_message(msg, messages)
            if reflection:
                # Add reflection as context
                enhanced.append(HumanMessage(
                    content=f"Reflection on previous response:\n{reflection}"
                ))

    return enhanced
```

### 3. Reflexion Pattern (Multi-Step)

```python
class ReflexionAgent(ProperMultiAgent):
    """Implements the Reflexion pattern with memory of past attempts."""

    @classmethod
    def create(
        cls,
        task_agent: Agent,
        evaluator_agent: Agent = None,
        max_attempts: int = 3,
        name: str = None
    ) -> "ReflexionAgent":
        """Create a Reflexion agent that learns from past attempts.

        The Reflexion pattern:
        1. Attempt task
        2. Evaluate result
        3. Generate reflection on what went wrong
        4. Retry with accumulated reflections

        Args:
            task_agent: Agent that attempts the task
            evaluator_agent: Agent that evaluates success (optional)
            max_attempts: Maximum attempts before giving up
            name: Name for the reflexion agent
        """
        # Create evaluator if not provided
        if not evaluator_agent:
            evaluator_agent = StructuredOutputAgent.create_validation_processor(
                validation_models=[ValidationResult, QualityCheck],
                name="task_evaluator"
            )

        # Create reflection generator
        reflection_agent = StructuredOutputAgent.create_reflection_processor(
            reflection_models=[ReflectionResult],
            name="reflection_generator",
            system_message="""Analyze the task attempt and evaluation.
            Generate insights about what went wrong and how to improve.
            Focus on actionable feedback for the next attempt."""
        )

        # Create state with reflexion memory
        reflexion_state = type(
            "ReflexionState",
            (MessagesStateWithTokenUsage,),
            {
                "__annotations__": {
                    "attempt_count": int,
                    "max_attempts": int,
                    "reflections": List[str],
                    "attempt_results": List[dict],
                    "task_complete": bool
                },
                "attempt_count": Field(default=0),
                "max_attempts": Field(default=max_attempts),
                "reflections": Field(default_factory=list),
                "attempt_results": Field(default_factory=list),
                "task_complete": Field(default=False)
            }
        )

        return cls(
            name=name or "reflexion_agent",
            agents=[task_agent, evaluator_agent, reflection_agent],
            execution_mode="conditional",  # Custom logic for reflexion loop
            state_schema=reflexion_state
        )
```

### 4. Self-Critique Pattern

```python
class SelfCritiqueAgent(ProperMultiAgent):
    """Agent that critiques its own outputs before finalizing."""

    @classmethod
    def create(
        cls,
        base_agent: Agent,
        critique_models: List[Type[BaseModel]] = None,
        name: str = None
    ) -> "SelfCritiqueAgent":
        """Create self-critiquing agent.

        Args:
            base_agent: Agent to add self-critique to
            critique_models: Models for critique (defaults to Critique)
            name: Name for the agent
        """
        if not critique_models:
            critique_models = [Critique]

        # Create critique processor
        critique_agent = StructuredOutputAgent(
            name=f"{base_agent.name}_critic",
            engine=AugLLMConfig(
                system_message="""You are a critical reviewer.
                Analyze the provided content and give honest, constructive feedback.
                Be specific about strengths and weaknesses.""",
                temperature=0.2
            ),
            output_models=critique_models
        )

        # Create final processor that incorporates critique
        final_agent = SimpleAgent(
            name=f"{base_agent.name}_final",
            engine=AugLLMConfig(
                system_message="""You are a finalizer agent.
                Take the original output and its critique, then produce
                a final version that addresses any valid criticisms while
                maintaining the strengths identified.""",
                temperature=0.3
            )
        )

        return cls(
            name=name or f"{base_agent.name}_self_critique",
            agents=[base_agent, critique_agent, final_agent],
            execution_mode="sequential"
        )
```

## 🎨 Advanced Patterns

### 1. Iterative Reflection Loop

```python
def create_iterative_reflection_graph(
    base_agent: Agent,
    max_iterations: int = 3,
    quality_threshold: float = 0.8
) -> StateGraph:
    """Create a graph with iterative reflection loop."""
    from haive.core.graph import StateGraph, END

    # Create graph
    graph = StateGraph(ReflectionState)

    # Add nodes
    graph.add_node("generate", base_agent)
    graph.add_node("reflect", reflection_processor)
    graph.add_node("improve", improvement_agent)
    graph.add_node("check_quality", quality_checker)

    # Add edges
    graph.add_edge("generate", "reflect")
    graph.add_edge("reflect", "check_quality")

    # Conditional edge based on quality
    graph.add_conditional_edges(
        "check_quality",
        lambda state: "improve" if should_improve(state) else "end",
        {
            "improve": "improve",
            "end": END
        }
    )

    # Loop back from improve to reflect
    graph.add_edge("improve", "reflect")

    # Set entry point
    graph.set_entry_point("generate")

    return graph

def should_improve(state: ReflectionState) -> str:
    """Determine if improvement is needed."""
    if state.reflection_count >= state.max_iterations:
        return "end"

    latest_quality = state.quality_scores[-1] if state.quality_scores else 0.0
    if latest_quality >= state.quality_threshold:
        return "end"

    return "improve"
```

### 2. Multi-Perspective Reflection

```python
class MultiPerspectiveReflection(ProperMultiAgent):
    """Reflect from multiple perspectives."""

    @classmethod
    def create(
        cls,
        base_agent: Agent,
        perspectives: List[str] = None,
        name: str = None
    ) -> "MultiPerspectiveReflection":
        """Create multi-perspective reflection.

        Args:
            base_agent: Agent to reflect on
            perspectives: List of perspectives to use
            name: Name for the agent
        """
        if not perspectives:
            perspectives = [
                "technical_accuracy",
                "clarity_and_communication",
                "completeness",
                "practical_applicability"
            ]

        # Create reflection agent for each perspective
        reflection_agents = []
        for perspective in perspectives:
            agent = StructuredOutputAgent.create_reflection_processor(
                reflection_models=[Critique, Improvement],
                name=f"{perspective}_reflector",
                system_message=f"""You are a {perspective} expert.
                Analyze the content specifically from the perspective of {perspective}.
                Provide targeted feedback on this aspect."""
            )
            reflection_agents.append(agent)

        # Create synthesis agent
        synthesis_agent = SimpleAgent(
            name="reflection_synthesizer",
            engine=AugLLMConfig(
                system_message="""Synthesize all perspective reflections into
                a cohesive improvement plan. Prioritize the most critical issues
                across all perspectives."""
            )
        )

        # All reflectors in parallel, then synthesis
        all_agents = [base_agent] + reflection_agents + [synthesis_agent]

        return cls(
            name=name or "multi_perspective_reflection",
            agents=all_agents,
            execution_mode="branch",  # Custom branching logic
            # Reflectors run in parallel after base_agent
        )
```

## 🚀 Usage Examples

### Basic Reflection

```python
# Create base agent
writer = SimpleAgent(
    name="writer",
    engine=AugLLMConfig(
        system_message="You are a technical writer."
    )
)

# Add reflection capability
reflective_writer = ReflectionAgent.create(
    base_agent=writer,
    max_iterations=2,
    quality_threshold=0.85
)

# Run with automatic reflection
result = await reflective_writer.arun(
    "Write a technical explanation of quantum computing"
)
```

### Reflexion Pattern

```python
# Create task agent
coder = ReactAgent(
    name="coder",
    tools=[python_repl_tool],
    engine=AugLLMConfig()
)

# Create reflexion agent
reflexion_coder = ReflexionAgent.create(
    task_agent=coder,
    max_attempts=3
)

# Run with learning from failures
result = await reflexion_coder.arun(
    "Write a function to solve the traveling salesman problem"
)

# Agent will attempt, evaluate, reflect, and retry with insights
```

## 🎯 Best Practices

### 1. Clear Reflection Criteria

```python
# ✅ GOOD - Specific reflection criteria
reflection_agent = StructuredOutputAgent.create_reflection_processor(
    reflection_models=[Critique],
    system_message="""Evaluate based on:
    1. Technical accuracy
    2. Code efficiency
    3. Error handling
    4. Documentation quality
    Provide specific examples for each point."""
)

# ❌ BAD - Vague reflection
reflection_agent = SimpleAgent(
    engine=AugLLMConfig(
        system_message="Reflect on the output"
    )
)
```

### 2. Actionable Feedback

```python
# ✅ GOOD - Actionable improvements
class ActionableImprovement(BaseModel):
    issue: str = Field(description="Specific issue identified")
    location: str = Field(description="Where in the output")
    suggestion: str = Field(description="How to fix it")
    example: str = Field(description="Example of improvement")
```

### 3. Reflection Memory

```python
# ✅ GOOD - Maintain reflection history
state = ReflectionState(
    reflections=[],  # Store all reflections
    improvements_applied=[],  # Track what was fixed
    quality_progression=[]  # Monitor improvement
)
```

## 🚨 Common Pitfalls

### 1. Infinite Reflection Loops

```python
# ❌ WRONG - No termination condition
while True:
    output = generate()
    reflection = reflect(output)
    output = improve(output, reflection)

# ✅ CORRECT - Clear termination
for i in range(max_iterations):
    output = generate()
    reflection = reflect(output)
    if reflection.overall_quality >= threshold:
        break
    output = improve(output, reflection)
```

### 2. Ignoring Reflection

```python
# ❌ WRONG - Generate reflection but don't use it
reflection = reflect(output)
return output  # Reflection wasted!

# ✅ CORRECT - Apply reflection insights
reflection = reflect(output)
if reflection.needs_revision:
    output = improve(output, reflection)
return output
```

### 3. Over-Reflection

```python
# ❌ WRONG - Reflecting on perfect outputs
if True:  # Always reflect
    reflection = reflect(output)

# ✅ CORRECT - Reflect when beneficial
if confidence < threshold or user_requested:
    reflection = reflect(output)
```

## 📊 Performance Considerations

1. **Token Usage**: Reflection doubles or triples token usage
2. **Latency**: Each reflection cycle adds processing time
3. **Memory**: Storing reflection history consumes memory
4. **Quality vs Speed**: Balance iteration count with quality needs

## 🔗 Integration with Message Transformer

```python
# Message transformer for reflection context
def reflection_transformer(messages: List[BaseMessage]) -> List[BaseMessage]:
    """Add reflection insights to conversation."""
    enhanced = []

    for i, msg in enumerate(messages):
        enhanced.append(msg)

        # Find reflection for this message
        if isinstance(msg, AIMessage):
            for j in range(i+1, len(messages)):
                if (isinstance(messages[j], ToolMessage) and
                    messages[j].name in ["Critique", "ReflectionResult"]):
                    # Add reflection as context
                    reflection_data = json.loads(messages[j].content)
                    enhanced.append(HumanMessage(
                        content=f"Previous attempt feedback: {reflection_data}"
                    ))
                    break

    return enhanced

# Use in graph
graph.add_node("transform_messages", MessageTransformerNode(
    transform_fn=reflection_transformer
))
```

## 📝 Summary

The Reflection/Reflexion pattern enables:

1. **Self-Improvement**: Agents analyze and improve their outputs
2. **Structured Critique**: Using Pydantic models for consistent feedback
3. **Iterative Refinement**: Multiple improvement cycles
4. **Learning from Failure**: Reflexion pattern with memory
5. **Multi-Perspective Analysis**: Different viewpoints on output

Key components:

- Message Transformer Nodes
- Structured Output Models
- Sequential/Conditional Execution
- State Management for Iterations

Next steps would involve testing these patterns with real scenarios and optimizing the reflection criteria for specific use cases.
