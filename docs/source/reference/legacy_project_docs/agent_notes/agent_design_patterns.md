# Agent Design Patterns in Haive

## Core Patterns

Haive supports various agent design patterns through its flexible graph architecture. Below are key patterns and when to use them.

## ReAct Pattern

The ReAct (Reasoning and Acting) pattern combines reasoning with tool actions in an iterative process.

### When to Use

- When the agent needs to perform multi-step reasoning
- When combining tool usage with intermediate thinking steps
- For complex problem solving requiring multiple tools

### Implementation

```python
from haive.agents.react_class.react_agent2.models import ReactState
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from langgraph.graph import END, START

# Create a react agent graph
graph = DynamicGraph(
    name="react_agent",
    state_schema=ReactState,
    components=[llm_engine, *tools]
)

# Define nodes
graph.add_node("agent", agent_node)
graph.add_node("tool_executor", tool_executor_node)

# Add routing logic
graph.add_conditional_edges(
    "agent",
    router_func,
    {
        "tools": "tool_executor",
        "final_answer": END
    }
)
graph.add_edge("tool_executor", "agent")
graph.add_edge(START, "agent")
```

## RAG Pattern

Retrieval Augmented Generation combines document retrieval with generation.

### When to Use

- When answers require factual knowledge beyond the LLM's training
- When responses need citations or evidence from documents
- For grounding responses in specific knowledge bases

### Implementation

```python
from haive.agents.rag.base.state import BaseRAGState
from haive.core.graph.dynamic_graph_builder import DynamicGraph

# Create a RAG agent graph
graph = DynamicGraph(
    name="rag_agent",
    state_schema=BaseRAGState,
    components=[retriever_engine, llm_engine]
)

# Define nodes
graph.add_node("retrieve", retriever_node)
graph.add_node("generate", generation_node)

# Define edges
graph.add_edge(START, "retrieve")
graph.add_edge("retrieve", "generate")
graph.add_edge("generate", END)
```

## Plan and Execute Pattern

The agent plans a sequence of steps, then executes each step.

### When to Use

- For complex tasks requiring structured planning
- When a task can be broken into distinct subtasks
- When errors in one step shouldn't affect the others

### Implementation

```python
from haive.agents.planning.plan_and_execute.models import PlanState
from haive.core.graph.dynamic_graph_builder import DynamicGraph

# Create plan and execute graph
graph = DynamicGraph(
    name="plan_execute_agent",
    state_schema=PlanState
)

# Define nodes
graph.add_node("planner", planner_node)
graph.add_node("executor", executor_node)
graph.add_node("checker", checker_node)

# Add edges with conditional routing
graph.add_edge(START, "planner")
graph.add_conditional_edges(
    "planner",
    plan_router,
    {
        "execute": "executor",
        "complete": END
    }
)
graph.add_conditional_edges(
    "executor",
    execution_router,
    {
        "next_step": "executor",
        "check": "checker",
        "complete": END
    }
)
graph.add_conditional_edges(
    "checker",
    checker_router,
    {
        "revise": "planner",
        "continue": "executor",
        "complete": END
    }
)
```

## Self-Critique Pattern

The agent evaluates its own responses and refines them.

### When to Use

- When output quality is critical
- For complex reasoning tasks requiring verification
- When implementing self-improvement loops

### Implementation

```python
from haive.agents.reasoning_and_critique.reflexion.models import ReflexionState
from haive.core.graph.dynamic_graph_builder import DynamicGraph

# Create self-critique graph
graph = DynamicGraph(
    name="self_critique_agent",
    state_schema=ReflexionState
)

# Define nodes
graph.add_node("generator", generator_node)
graph.add_node("critic", critic_node)
graph.add_node("refiner", refiner_node)

# Add edges
graph.add_edge(START, "generator")
graph.add_conditional_edges(
    "generator",
    critique_router,
    {
        "critique": "critic",
        "complete": END
    }
)
graph.add_edge("critic", "refiner")
graph.add_edge("refiner", "generator")
```

## Human-in-the-Loop Pattern

Integrates human feedback into the agent workflow.

### When to Use

- For high-stakes decisions requiring human approval
- When the agent might encounter edge cases
- For sensitive operations needing verification

### Implementation

```python
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from langgraph.graph import NodeInterrupt

# Define human review node
def human_review_node(state):
    if requires_review(state):
        raise NodeInterrupt({"state": state, "reason": "Human review required"})
    return {"status": "auto_approved"}

# Create human-in-the-loop graph
graph = DynamicGraph(
    name="human_in_the_loop_agent",
    state_schema=HumanReviewState
)

# Define nodes
graph.add_node("processor", processor_node)
graph.add_node("reviewer", human_review_node)
graph.add_node("finalizer", finalizer_node)

# Add edges
graph.add_edge(START, "processor")
graph.add_edge("processor", "reviewer")
graph.add_edge("reviewer", "finalizer")
graph.add_edge("finalizer", END)

# Resume after human review
response = graph.stream(Command(resume={"approved": True, "feedback": "Looks good"}))
```

## Multi-Agent Collaboration Pattern

Coordinates multiple specialized agents working together.

### When to Use

- When different subtasks require specialized expertise
- For complex workflows with distinct phases
- When implementing team-like collaboration

### Implementation

```python
from haive.core.graph.dynamic_graph_builder import DynamicGraph

# Create multi-agent graph
graph = DynamicGraph(
    name="multi_agent_system",
    state_schema=CollaborationState
)

# Define agents as nodes
graph.add_node("coordinator", coordinator_node)
graph.add_node("researcher", researcher_agent_node)
graph.add_node("writer", writer_agent_node)
graph.add_node("critic", critic_agent_node)

# Define workflow
graph.add_edge(START, "coordinator")
graph.add_conditional_edges(
    "coordinator",
    task_router,
    {
        "research": "researcher",
        "write": "writer",
        "review": "critic",
        "complete": END
    }
)
graph.add_edge("researcher", "coordinator")
graph.add_edge("writer", "coordinator")
graph.add_edge("critic", "coordinator")
```

## Tool Orchestration Pattern

Dynamically selects and uses the most appropriate tools.

### When to Use

- When the agent needs access to many tools
- For tasks requiring specialized tool selection
- When implementing complex tool usage policies

### Implementation

```python
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from haive.core.graph.tool_injector import create_tool_node

# Create tool orchestration graph
graph = DynamicGraph(
    name="tool_orchestrator",
    state_schema=ToolState,
    components=[llm_engine, *all_tools]
)

# Create specialized tool nodes
tool_node = create_tool_node(all_tools)

# Define nodes
graph.add_node("tool_selector", tool_selector_node)
graph.add_node("tool_executor", tool_node)
graph.add_node("result_processor", result_processor_node)

# Add edges
graph.add_edge(START, "tool_selector")
graph.add_conditional_edges(
    "tool_selector",
    tool_routing,
    {
        "execute": "tool_executor",
        "process": "result_processor",
        "complete": END
    }
)
graph.add_edge("tool_executor", "result_processor")
graph.add_edge("result_processor", "tool_selector")
```

## Combining Patterns

Patterns can be combined for more complex agents:

```python
# RAG + ReAct + Self-Critique combined pattern
graph = DynamicGraph(
    name="advanced_agent",
    state_schema=CombinedState
)

# Add nodes from multiple patterns
graph.add_node("retriever", retriever_node)
graph.add_node("reactor", react_agent_node)
graph.add_node("tool_executor", tool_node)
graph.add_node("critic", critic_node)
graph.add_node("refiner", refiner_node)

# Complex routing logic combining patterns
# [implementation details...]
```
