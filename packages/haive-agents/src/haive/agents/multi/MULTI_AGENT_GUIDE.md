# Multi-Agent Systems Development Guide

This guide provides comprehensive documentation on creating multi-agent systems using the haive framework, with practical examples from the RAG workflow implementations.

## Table of Contents

1. [Overview](#overview)
2. [Core Concepts](#core-concepts)
3. [Creating Multi-Agent Systems](#creating-multi-agent-systems)
4. [Execution Modes](#execution-modes)
5. [State Management](#state-management)
6. [Building Custom Workflows](#building-custom-workflows)
7. [Practical Examples](#practical-examples)
8. [Best Practices](#best-practices)
9. [Debugging Tips](#debugging-tips)

## Overview

Multi-agent systems in haive allow you to orchestrate multiple specialized agents working together to solve complex tasks. Each agent focuses on a specific aspect of the problem, and the multi-agent system coordinates their execution.

## Core Concepts

### 1. MultiAgent Base Class

The `MultiAgent` class is the foundation for all multi-agent workflows:

```python
from haive.agents.multi.base import MultiAgent, ExecutionMode
from haive.agents.simple import SimpleAgent

class MyMultiAgent(MultiAgent):
    def __init__(self, **kwargs):
        # Define your agents
        agents = [...]

        super().__init__(
            agents=agents,
            execution_mode=ExecutionMode.SEQUENCE,
            state_schema=MyStateSchema,
            **kwargs
        )
```

### 2. Execution Modes

haive supports three execution modes:

- **SEQUENCE**: Agents execute one after another in order
- **PARALLEL**: Agents execute simultaneously
- **CONDITIONAL**: Agents execute based on conditions and routing logic

### 3. State Schema

State schemas define the data structure shared between agents:

```python
from haive.core.schema.prebuilt.rag_state import RAGState

class CustomRAGState(RAGState):
    """Extended state with custom fields"""
    custom_field: str = ""
    agent_outputs: Dict[str, Any] = {}
```

## Creating Multi-Agent Systems

### Step 1: Define Your State Schema

```python
from dataclasses import dataclass
from typing import List, Dict, Any
from haive.core.schema.prebuilt.rag_state import RAGState

class MyWorkflowState(RAGState):
    """State schema for my workflow"""
    # Add custom fields as needed
    processing_steps: List[str] = []
    intermediate_results: Dict[str, Any] = {}
    confidence_score: float = 0.0
```

### Step 2: Create Individual Agents

```python
from haive.agents.simple import SimpleAgent

# Agent 1: Query Analyzer
query_analyzer = SimpleAgent(
    name="query_analyzer",
    instructions="""
    Analyze the user query and extract key information.
    Identify the type of query and required processing steps.
    """,
    output_schema={
        "query_type": "str",
        "key_concepts": "List[str]",
        "complexity": "float"
    }
)

# Agent 2: Document Processor
doc_processor = SimpleAgent(
    name="document_processor",
    instructions="""
    Process retrieved documents based on the query analysis.
    Extract relevant information and prepare for answer generation.
    """,
    output_schema={
        "processed_docs": "List[str]",
        "relevance_scores": "List[float]"
    }
)

# Agent 3: Answer Generator
answer_generator = SimpleAgent(
    name="answer_generator",
    instructions="""
    Generate a comprehensive answer using processed documents.
    Ensure the answer addresses all aspects of the query.
    """,
    output_schema={
        "answer": "str",
        "confidence": "float",
        "sources": "List[str]"
    }
)
```

### Step 3: Create the Multi-Agent Workflow

```python
class MyMultiAgentWorkflow(MultiAgent):
    """Custom multi-agent workflow for document processing"""

    def __init__(self, **kwargs):
        agents = [query_analyzer, doc_processor, answer_generator]

        super().__init__(
            agents=agents,
            execution_mode=ExecutionMode.SEQUENCE,
            state_schema=MyWorkflowState,
            **kwargs
        )

    def build_custom_graph(self):
        """Optional: Build custom execution graph"""
        # Return None to use default graph based on execution mode
        return None
```

## Execution Modes

### Sequential Execution

```python
class SequentialWorkflow(MultiAgent):
    def __init__(self, **kwargs):
        agents = [agent1, agent2, agent3]

        super().__init__(
            agents=agents,
            execution_mode=ExecutionMode.SEQUENCE,
            state_schema=StateSchema,
            **kwargs
        )
```

**Use Case**: When each agent depends on the output of the previous one.

### Parallel Execution

```python
class ParallelWorkflow(MultiAgent):
    def __init__(self, **kwargs):
        # These agents will run simultaneously
        agents = [
            data_fetcher_1,
            data_fetcher_2,
            data_fetcher_3
        ]

        super().__init__(
            agents=agents,
            execution_mode=ExecutionMode.PARALLEL,
            state_schema=StateSchema,
            **kwargs
        )
```

**Use Case**: When agents can work independently and you want to maximize performance.

### Conditional Execution

```python
class ConditionalWorkflow(MultiAgent):
    def __init__(self, **kwargs):
        agents = [
            initial_assessor,
            route_a_agent,
            route_b_agent,
            final_processor
        ]

        super().__init__(
            agents=agents,
            execution_mode=ExecutionMode.CONDITIONAL,
            state_schema=StateSchema,
            **kwargs
        )

    def build_custom_graph(self):
        """Define custom routing logic"""
        # Implement conditional routing based on state
        # This is where you define which agents run based on conditions
        return None
```

**Use Case**: When the workflow path depends on intermediate results.

## State Management

### Using Schema Composer

The Schema Composer automatically manages state schemas:

```python
from haive.core.schema.schema_composer import SchemaComposer

class AutoManagedWorkflow(MultiAgent):
    def __init__(self, **kwargs):
        agents = [agent1, agent2, agent3]

        # SchemaComposer will automatically create a unified state schema
        super().__init__(
            agents=agents,
            execution_mode=ExecutionMode.SEQUENCE,
            # Don't specify state_schema - let SchemaComposer handle it
            **kwargs
        )
```

### Manual State Management

For more control, manually define your state:

```python
class ManualStateWorkflow(MultiAgent):
    def __init__(self, **kwargs):
        agents = [agent1, agent2, agent3]

        super().__init__(
            agents=agents,
            execution_mode=ExecutionMode.SEQUENCE,
            state_schema=CustomStateSchema,  # Explicitly set state schema
            **kwargs
        )
```

## Building Custom Workflows

### Example: FLARE (Forward-Looking Active REtrieval)

```python
class FLAREAgent(MultiAgent):
    """
    Forward-Looking Active REtrieval - generates text while actively
    predicting when retrieval would be beneficial.
    """

    def __init__(self, **kwargs):
        # Generation monitor agent
        generation_monitor = SimpleAgent(
            name="generation_monitor",
            instructions="""
            Monitor text generation for uncertainty indicators.
            Identify points where retrieval would be beneficial.
            """,
            output_schema={
                "uncertainty_detected": "bool",
                "retrieval_query": "Optional[str]"
            }
        )

        # Active retrieval agent
        active_retrieval = SimpleAgent(
            name="active_retrieval",
            instructions="""
            Perform targeted retrieval when uncertainty is detected.
            """,
            output_schema={
                "retrieved_documents": "List[str]"
            }
        )

        # Informed generation agent
        informed_generator = SimpleAgent(
            name="informed_generator",
            instructions="""
            Continue generation using retrieved information.
            """,
            output_schema={
                "generated_text": "str",
                "generation_complete": "bool"
            }
        )

        agents = [generation_monitor, active_retrieval, informed_generator]

        super().__init__(
            agents=agents,
            execution_mode=ExecutionMode.CONDITIONAL,
            state_schema=FLAREState,
            **kwargs
        )
```

### Example: Debate RAG System

```python
class DebateRAGAgent(MultiAgent):
    """
    Multiple agents debate different perspectives to reach consensus.
    """

    def __init__(self, debate_positions=None, **kwargs):
        if debate_positions is None:
            debate_positions = ["Affirmative", "Negative", "Neutral"]

        # Create position agents
        position_agents = []
        for position in debate_positions:
            agent = SimpleAgent(
                name=f"{position.lower()}_position",
                instructions=f"""
                Argue from the {position} perspective.
                Use evidence to support your position.
                """,
                output_schema={
                    "argument": "str",
                    "evidence": "List[str]"
                }
            )
            position_agents.append(agent)

        # Moderator agent
        moderator = SimpleAgent(
            name="debate_moderator",
            instructions="""
            Moderate the debate and identify key agreements/conflicts.
            """,
            output_schema={
                "summary": "str",
                "consensus_points": "List[str]"
            }
        )

        # Synthesis judge
        synthesis_judge = SimpleAgent(
            name="synthesis_judge",
            instructions="""
            Synthesize all perspectives into a final answer.
            """,
            output_schema={
                "final_answer": "str",
                "confidence": "float"
            }
        )

        agents = position_agents + [moderator, synthesis_judge]

        super().__init__(
            agents=agents,
            execution_mode=ExecutionMode.CONDITIONAL,
            state_schema=DebateRAGState,
            **kwargs
        )
```

## Practical Examples

### 1. Simple Sequential Workflow

```python
# Create a basic question-answering workflow
qa_workflow = SimpleRAGWithMemoryAgent(
    name="qa_workflow",
    max_rounds=1
)

# Use it
result = qa_workflow.invoke({
    "query": "What is the capital of France?",
    "conversation_history": []
})
```

### 2. Complex Multi-Strategy Workflow

```python
# Create a workflow that tries multiple strategies
multi_strategy = MultiQueryRAGAgent(
    name="multi_strategy_rag",
    fallback_strategies=["fusion", "step_back"],
    max_rounds=3
)

result = multi_strategy.invoke({
    "query": "Explain quantum computing applications in medicine"
})
```

### 3. Dynamic Adaptive Workflow

```python
# Create a workflow that adapts based on performance
adaptive_workflow = DynamicRAGAgent(
    name="adaptive_rag",
    initial_retrievers=["semantic", "keyword"],
    performance_threshold=0.7
)

result = adaptive_workflow.invoke({
    "query": "Complex technical question here"
})
```

## Best Practices

### 1. Agent Design

- **Single Responsibility**: Each agent should have one clear purpose
- **Clear Instructions**: Write detailed, specific instructions
- **Structured Output**: Use output schemas for predictable results

### 2. State Management

- **Minimal State**: Only include necessary information in state
- **Immutable Updates**: Always create new state objects, don't modify
- **Type Safety**: Use proper type hints and schemas

### 3. Error Handling

```python
class RobustWorkflow(MultiAgent):
    def __init__(self, **kwargs):
        # Add error handling agents
        error_handler = SimpleAgent(
            name="error_handler",
            instructions="Handle errors gracefully",
            output_schema={"error_handled": "bool"}
        )

        agents = [main_agent, error_handler]
        super().__init__(
            agents=agents,
            execution_mode=ExecutionMode.CONDITIONAL,
            **kwargs
        )
```

### 4. Performance Optimization

- Use **PARALLEL** execution when agents are independent
- Minimize state size to reduce overhead
- Cache expensive operations where possible

## Debugging Tips

### 1. Enable Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Your workflow will now show detailed execution logs
```

### 2. State Inspection

```python
class DebugWorkflow(MultiAgent):
    def invoke(self, input_data):
        result = super().invoke(input_data)

        # Inspect final state
        print(f"Final state: {result.state}")
        print(f"Agent outputs: {result.state.agent_outputs}")

        return result
```

### 3. Step-by-Step Execution

```python
# For debugging, switch to SEQUENCE mode temporarily
workflow = MyWorkflow(
    execution_mode=ExecutionMode.SEQUENCE,  # Easier to debug
    debug=True
)
```

## Advanced Patterns

### 1. Hierarchical Multi-Agent Systems

```python
class HierarchicalSystem(MultiAgent):
    def __init__(self, **kwargs):
        # Sub-workflow 1
        sub_workflow_1 = SimpleRAGWorkflow()

        # Sub-workflow 2
        sub_workflow_2 = AdvancedRAGWorkflow()

        # Coordinator
        coordinator = SimpleAgent(
            name="coordinator",
            instructions="Coordinate sub-workflows"
        )

        agents = [coordinator, sub_workflow_1, sub_workflow_2]
        super().__init__(agents=agents, **kwargs)
```

### 2. Dynamic Agent Creation

```python
class DynamicWorkflow(MultiAgent):
    def __init__(self, num_workers=3, **kwargs):
        # Dynamically create worker agents
        workers = []
        for i in range(num_workers):
            worker = SimpleAgent(
                name=f"worker_{i}",
                instructions=f"Process part {i} of the task"
            )
            workers.append(worker)

        super().__init__(
            agents=workers,
            execution_mode=ExecutionMode.PARALLEL,
            **kwargs
        )
```

### 3. Feedback Loops

```python
class FeedbackWorkflow(MultiAgent):
    def __init__(self, **kwargs):
        generator = SimpleAgent(name="generator")
        evaluator = SimpleAgent(name="evaluator")
        refiner = SimpleAgent(name="refiner")

        # Create a loop: generator -> evaluator -> refiner -> generator
        agents = [generator, evaluator, refiner]

        super().__init__(
            agents=agents,
            execution_mode=ExecutionMode.CONDITIONAL,
            max_iterations=3,  # Limit feedback loops
            **kwargs
        )
```

## Conclusion

Multi-agent systems in haive provide a powerful way to build complex AI workflows. By combining specialized agents with different execution modes and state management strategies, you can create sophisticated systems that tackle challenging problems effectively.

Remember to:

- Start simple and add complexity gradually
- Test each agent independently before combining
- Monitor performance and optimize as needed
- Use appropriate execution modes for your use case

For more examples, check out the implemented RAG workflows in the `multi_agent_rag` directory.
