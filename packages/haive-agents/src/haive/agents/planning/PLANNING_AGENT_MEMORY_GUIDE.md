# Planning Agent Memory Guide

**Version**: 1.0  
**Purpose**: Comprehensive guide for building planning agents with various patterns  
**Last Updated**: 2025-01-09

## 🎯 Planning Pattern Overview

### Available Planning Patterns

1. **Sequential Planning** (Plan & Execute)
   - Linear step execution
   - Simple dependencies
   - Good for straightforward tasks

2. **DAG Planning** (LLM Compiler)
   - Directed Acyclic Graph structure
   - Parallel execution support
   - Complex dependency management

3. **Evidence-Based Planning** (ReWOO)
   - Evidence collection and referencing
   - Reasoning with gathered evidence
   - Good for research tasks

4. **Adaptive Planning** (FLARE)
   - Dynamic plan adjustment
   - Retrieval-augmented generation
   - Self-correcting behavior

5. **Recursive Planning**
   - Hierarchical decomposition
   - Sub-plan generation
   - Complex problem solving

## 📋 Planning Agent Design Checklist

### 1. Define Your Planning Pattern

```python
# Questions to answer:
- What type of problems will this agent solve?
- Does it need parallel execution?
- Will plans need to adapt during execution?
- Is evidence gathering important?
- Are sub-plans/recursion needed?
```

### 2. Choose Step Types

```python
from haive.agents.planning.models.base import (
    StepType,
    ActionStep,
    ResearchStep,
    RecursiveStep,
    ConditionalStep,
    ParallelStep
)

# Common combinations:
# Research Agent: ResearchStep + ActionStep + SynthesisStep
# Task Agent: ActionStep + ValidationStep + ConditionalStep
# Complex Agent: RecursiveStep + ParallelStep + all types
```

### 3. Design State Schema

```python
from haive.core.schema.prebuilt.tool_state import ToolState
from pydantic import Field, computed_field, field_validator, model_validator
from typing import List, Optional, Dict, Any, TypeVar, Generic

class PlanningAgentState(ToolState):
    """State for planning agent extending ToolState.

    Leverages ToolState for:
    - Tool management and routing
    - Message history with token tracking
    - Tool validation and categorization
    """

    # Core planning fields
    objective: str = Field(description="Main objective")
    plan: Optional[BasePlan] = Field(default=None, description="Current plan")

    # Execution tracking
    completed_steps: List[str] = Field(default_factory=list)
    step_results: Dict[str, Any] = Field(default_factory=dict)

    # Planning-specific fields
    max_steps: int = Field(default=10, description="Maximum steps allowed", ge=1, le=100)
    allow_replanning: bool = Field(default=True)
    replan_count: int = Field(default=0, ge=0)

    # Pattern-specific fields
    evidence: Dict[str, str] = Field(default_factory=dict)  # For ReWOO
    adaptation_context: Dict[str, Any] = Field(default_factory=dict)  # For FLARE
    sub_plans: Dict[str, BasePlan] = Field(default_factory=dict)  # For recursive

    @field_validator('max_steps')
    @classmethod
    def validate_max_steps(cls, v: int) -> int:
        """Ensure reasonable step limits."""
        if v < 1:
            raise ValueError("max_steps must be at least 1")
        if v > 100:
            raise ValueError("max_steps cannot exceed 100 for safety")
        return v

    @model_validator(mode="after")
    def setup_planning_state(self) -> "PlanningAgentState":
        """Setup planning-specific state after parent initialization."""
        # Parent validators from ToolState run first
        # This gives us tool management, routing, etc.

        # Initialize plan tools if plan exists
        if self.plan:
            self._sync_plan_tools()

        return self

    def _sync_plan_tools(self) -> None:
        """Sync tools referenced in plan with state tools."""
        if not self.plan:
            return

        # Check all steps for tool references
        for step in self.plan.steps:
            if hasattr(step, 'tool_name') and step.tool_name:
                # Ensure tool is available
                if not self.get_tool_by_name(step.tool_name):
                    logger.warning(f"Step {step.id} references unknown tool: {step.tool_name}")

    @computed_field
    @property
    def is_complete(self) -> bool:
        """Check if objective is achieved."""
        return self.plan is not None and self.plan.is_complete

    @computed_field
    @property
    def next_actions(self) -> List[BaseStep]:
        """Get next executable steps."""
        if not self.plan:
            return []
        return self.plan.update_ready_steps()

    @computed_field
    @property
    def progress_summary(self) -> Dict[str, Any]:
        """Get comprehensive progress summary."""
        return {
            "objective": self.objective,
            "total_steps": len(self.plan.steps) if self.plan else 0,
            "completed_steps": len(self.completed_steps),
            "replan_count": self.replan_count,
            "has_tools": len(self.tools) > 0,
            "tool_categories": list(set(self.tool_routes.values())) if hasattr(self, 'tool_routes') else []
        }


# Type variable for generic planning states
TPlanningState = TypeVar('TPlanningState', bound=PlanningAgentState)
```

### 4. Define Structured Output Models

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Union

# For plan generation
class PlanOutput(BaseModel):
    """Structured output for plan generation."""

    objective_analysis: str = Field(
        description="Analysis of the objective and approach"
    )

    steps: List[StepDefinition] = Field(
        description="Steps to execute"
    )

    success_criteria: str = Field(
        description="How to determine success"
    )

    potential_issues: List[str] = Field(
        default_factory=list,
        description="Potential problems to watch for"
    )

class StepDefinition(BaseModel):
    """Definition for a single step."""

    name: str = Field(description="Step name")
    description: str = Field(description="What to do")
    step_type: StepType = Field(description="Type of step")
    dependencies: List[str] = Field(default_factory=list)

    # Type-specific fields
    tool_name: Optional[str] = None  # For ACTION steps
    query: Optional[str] = None  # For RESEARCH steps
    condition: Optional[str] = None  # For CONDITIONAL steps

# For step execution
class StepResult(BaseModel):
    """Result from executing a step."""

    success: bool = Field(description="Whether step succeeded")
    output: Any = Field(description="Step output")
    error: Optional[str] = Field(default=None)

    # Additional context
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    evidence: Optional[List[str]] = None
    next_steps: Optional[List[str]] = None

# For replanning decisions
class ReplanDecision(BaseModel):
    """Decision on whether to replan."""

    should_replan: bool = Field(description="Whether to replan")
    reason: str = Field(description="Reasoning")

    # If replanning
    keep_steps: List[str] = Field(
        default_factory=list,
        description="Step IDs to keep"
    )
    modify_steps: Dict[str, str] = Field(
        default_factory=dict,
        description="Steps to modify and how"
    )
    new_constraints: Optional[Dict[str, Any]] = None
```

### 5. Design Prompts

```python
# Plan Generation Prompt
PLAN_GENERATION_PROMPT = """
You are a planning agent tasked with creating an execution plan.

Objective: {objective}

Context:
{context}

Available Tools:
{tools}

Create a detailed plan to achieve the objective. Consider:
1. What information needs to be gathered
2. What actions need to be taken
3. Dependencies between steps
4. Potential failure points
5. Success criteria

Output your plan with clear, actionable steps.
"""

# Step Execution Prompt
STEP_EXECUTION_PROMPT = """
Execute the following step in the plan:

Step: {step_name}
Description: {step_description}
Type: {step_type}

Previous Results:
{previous_results}

Available Tools:
{available_tools}

Execute this step and provide the result.
"""

# Replan Decision Prompt
REPLAN_DECISION_PROMPT = """
Evaluate the current plan execution:

Original Objective: {objective}
Current Plan Progress: {progress}
Failed Steps: {failures}
Completed Steps: {completed}

Should we:
1. Continue with the current plan
2. Modify the plan
3. Create a new plan
4. Provide final answer with current results

Analyze and decide the best course of action.
"""
```

### 6. Tool Selection

```python
# Common tools for planning agents
tools = [
    # Information gathering
    web_search_tool,
    document_retrieval_tool,
    database_query_tool,

    # Analysis
    data_analysis_tool,
    summarization_tool,
    comparison_tool,

    # Action
    api_call_tool,
    file_operation_tool,
    notification_tool,

    # Validation
    fact_check_tool,
    result_validation_tool
]

# Tool routing configuration
tool_routes = {
    "web_search": "research_engine",
    "analyze": "analysis_engine",
    "execute": "action_engine",
    "validate": "validation_engine"
}
```

## 🏗️ Implementation Patterns

### Pattern 1: Simple Sequential Planner

```python
from haive.agents.simple import SimpleAgent
from haive.agents.planning.models.base import SequentialPlan, ActionStep

class SequentialPlannerAgent(SimpleAgent):
    """Simple sequential planning agent."""

    def __init__(self, **kwargs):
        super().__init__(
            structured_output_model=PlanOutput,
            **kwargs
        )

    def build_graph(self) -> BaseGraph:
        graph = BaseGraph()

        # Plan generation node
        graph.add_node("generate_plan", self.generate_plan_node)

        # Execution loop
        graph.add_node("execute_step", self.execute_step_node)
        graph.add_node("check_complete", self.check_complete_node)

        # Edges
        graph.add_edge(START, "generate_plan")
        graph.add_edge("generate_plan", "execute_step")
        graph.add_edge("execute_step", "check_complete")
        graph.add_conditional_edges(
            "check_complete",
            self.should_continue,
            {
                True: "execute_step",
                False: END
            }
        )

        return graph
```

### Pattern 2: DAG Planner (LLM Compiler Style)

```python
class DAGPlannerAgent(SimpleAgent):
    """DAG-based planning with parallel execution."""

    def build_graph(self) -> BaseGraph:
        graph = BaseGraph()

        # Planning phase
        graph.add_node("analyze_objective", self.analyze_objective_node)
        graph.add_node("generate_dag", self.generate_dag_node)

        # Execution phase
        graph.add_node("schedule_steps", self.schedule_steps_node)
        graph.add_node("execute_parallel", self.execute_parallel_node)
        graph.add_node("join_results", self.join_results_node)

        # Adaptation phase
        graph.add_node("evaluate_progress", self.evaluate_progress_node)

        # Complex routing
        graph.add_edge(START, "analyze_objective")
        graph.add_edge("analyze_objective", "generate_dag")
        graph.add_edge("generate_dag", "schedule_steps")
        graph.add_edge("schedule_steps", "execute_parallel")
        graph.add_edge("execute_parallel", "join_results")
        graph.add_edge("join_results", "evaluate_progress")

        graph.add_conditional_edges(
            "evaluate_progress",
            self.determine_next_action,
            {
                "continue": "schedule_steps",
                "adapt": "generate_dag",
                "complete": END
            }
        )

        return graph
```

### Pattern 3: Evidence-Based Planner (ReWOO Style)

````python
from haive.agents.planning.rewoo.state import ReWOOState
from haive.agents.planning.rewoo.models import ReWOOPlan, Evidence

class ReWOOPlannerAgent(SimpleAgent):
    """Evidence-based planner using ReWOO pattern."""

    def __init__(self, **kwargs):
        super().__init__(
            state_schema=ReWOOState,  # Use ReWOO state with ToolState
            structured_output_model=ReWOOPlan,
            **kwargs
        )

    def build_graph(self) -> BaseGraph:
        graph = BaseGraph()

        # Planning phase
        graph.add_node("analyze_objective", self.analyze_objective_node)
        graph.add_node("create_evidence_plan", self.create_evidence_plan_node)

        # Evidence collection phase
        graph.add_node("collect_evidence", self.collect_evidence_node)
        graph.add_node("validate_evidence", self.validate_evidence_node)

        # Reasoning phase
        graph.add_node("reason_with_evidence", self.reason_with_evidence_node)

        # Flow
        graph.add_edge(START, "analyze_objective")
        graph.add_edge("analyze_objective", "create_evidence_plan")
        graph.add_edge("create_evidence_plan", "collect_evidence")
        graph.add_edge("collect_evidence", "validate_evidence")

        graph.add_conditional_edges(
            "validate_evidence",
            self.check_evidence_complete,
            {
                True: "reason_with_evidence",
                False: "collect_evidence"
            }
        )

        graph.add_edge("reason_with_evidence", END)

        return graph


### Pattern 4: Adaptive Planner (FLARE Style)

```python
class AdaptivePlannerAgent(SimpleAgent):
    """Self-adapting planner with retrieval augmentation."""

    def __init__(self, **kwargs):
        # Multiple engines for different capabilities
        super().__init__(
            engines={
                "planner": planning_engine,
                "retriever": retrieval_engine,
                "executor": execution_engine
            },
            **kwargs
        )

    def build_graph(self) -> BaseGraph:
        graph = BaseGraph()

        # Initial planning
        graph.add_node("initial_plan", self.initial_plan_node)

        # Execution with adaptation
        graph.add_node("execute_adaptive", self.execute_adaptive_node)
        graph.add_node("check_confidence", self.check_confidence_node)
        graph.add_node("retrieve_info", self.retrieve_info_node)
        graph.add_node("adapt_plan", self.adapt_plan_node)

        # Routing with adaptation triggers
        graph.add_edge(START, "initial_plan")
        graph.add_edge("initial_plan", "execute_adaptive")
        graph.add_edge("execute_adaptive", "check_confidence")

        graph.add_conditional_edges(
            "check_confidence",
            self.confidence_routing,
            {
                "high": END,
                "medium": "execute_adaptive",
                "low": "retrieve_info"
            }
        )

        graph.add_edge("retrieve_info", "adapt_plan")
        graph.add_edge("adapt_plan", "execute_adaptive")

        return graph
````

## 🧪 Testing Planning Agents

### Test Scenarios

```python
# 1. Simple linear task
test_simple = {
    "objective": "Research and summarize recent AI developments",
    "expected_steps": ["search", "read", "analyze", "summarize"]
}

# 2. Complex parallel task
test_parallel = {
    "objective": "Compare products across multiple vendors",
    "expected_parallel": ["vendor_a", "vendor_b", "vendor_c"],
    "expected_join": "comparison"
}

# 3. Adaptive scenario
test_adaptive = {
    "objective": "Find solution to technical problem",
    "initial_confidence": "low",
    "expected_adaptations": 2
}

# 4. Recursive scenario
test_recursive = {
    "objective": "Plan a complex project with sub-tasks",
    "expected_depth": 3
}
```

### Validation Patterns

```python
from pydantic import ValidationError

def validate_plan(plan: BasePlan) -> bool:
    """Validate plan structure and logic."""
    try:
        # Pydantic validation
        plan.model_validate(plan.model_dump())
    except ValidationError as e:
        raise ValueError(f"Plan validation failed: {e}")

    # Check for cycles in DAG plans
    if isinstance(plan, DAGPlan):
        assert plan.validate_dag(), "Plan contains cycles"

    # Check dependencies
    step_ids = {s.id for s in plan.steps}
    for step in plan.steps:
        for dep in step.dependencies:
            assert dep.step_id in step_ids, f"Invalid dependency: {dep.step_id}"

    # Check execution order
    batches = plan.get_execution_order()
    assert len(batches) > 0, "No executable steps"

    # Validate tool availability for steps
    if hasattr(plan, 'state') and hasattr(plan.state, 'tools'):
        for step in plan.steps:
            if hasattr(step, 'tool_name') and step.tool_name:
                assert any(t.name == step.tool_name for t in plan.state.tools if hasattr(t, 'name')), \
                    f"Step {step.id} references unavailable tool: {step.tool_name}"

    return True


def validate_state_consistency(state: PlanningAgentState) -> bool:
    """Validate state consistency."""
    # Use Pydantic's validation
    try:
        state.model_validate(state.model_dump())
    except ValidationError as e:
        raise ValueError(f"State validation failed: {e}")

    # Check plan-state consistency
    if state.plan:
        # Completed steps should exist in plan
        plan_step_ids = {s.id for s in state.plan.steps}
        for step_id in state.completed_steps:
            assert step_id in plan_step_ids, f"Completed step {step_id} not in plan"

    # Check tool consistency (inherited from ToolState)
    # This is handled by ToolState validators

    return True
```

## 📊 Performance Considerations

### Resource Management

```python
# Set resource limits
class ResourceAwarePlan(BasePlan):
    max_tokens: int = Field(default=10000)
    max_api_calls: int = Field(default=50)
    max_time_seconds: int = Field(default=300)

    def can_add_step(self, step: BaseStep) -> bool:
        """Check if we have resources for another step."""
        estimated_tokens = sum(s.metadata.tokens_used or 0 for s in self.steps)
        return estimated_tokens < self.max_tokens
```

### Optimization Strategies

1. **Batch Operations**: Group similar operations
2. **Caching**: Cache retrieval results
3. **Early Termination**: Stop when objective is met
4. **Progressive Planning**: Plan in stages
5. **Parallel Execution**: Use ParallelStep when possible

## 🔍 Debugging Tips

### Common Issues

1. **Circular Dependencies**
   - Use DAG validation
   - Visualize with Mermaid diagrams

2. **Resource Exhaustion**
   - Set hard limits
   - Monitor token usage

3. **Infinite Loops**
   - Set max iterations
   - Add termination conditions

4. **Poor Plan Quality**
   - Improve prompts
   - Add examples
   - Use structured output validation

### Debug Helpers

```python
# Visualize plan
print(plan.to_mermaid())

# Track execution
for step in plan.steps:
    print(f"{step.id}: {step.status} - {step.metadata.execution_time}s")

# Analyze failures
for failed in plan.failed_steps:
    print(f"Failed: {failed.name} - {failed.metadata.last_error}")
```

## 🎯 Best Practices

1. **Use Existing State Patterns**: Extend ToolState or other prebuilt states instead of creating from scratch
2. **Leverage Pydantic Validation**: Use Field validators, model validators, and proper typing
3. **Never Override `__init__`**: Use Pydantic's validation system instead
4. **Start Simple**: Begin with SequentialPlan, add complexity as needed
5. **Use Structured Output**: Always use Pydantic models for plan generation
6. **Validate Early**: Check plans before execution using Pydantic validation
7. **Monitor Progress**: Track execution metrics (ToolState provides this)
8. **Handle Failures**: Always have fallback strategies
9. **Test Thoroughly**: Test each planning pattern separately
10. **Document Patterns**: Keep examples of successful plans

### Common Mistakes to Avoid

```python
# ❌ WRONG - Don't reinvent the wheel
class MyPlanningState(StateSchema):
    tools: List[Any] = Field(default_factory=list)
    tool_routes: Dict[str, str] = Field(default_factory=dict)
    # ... reimplementing tool management

# ✅ CORRECT - Extend existing states
class MyPlanningState(ToolState):
    # Inherit tool management, just add planning-specific fields
    plan: Optional[BasePlan] = Field(default=None)
    objective: str = Field(...)

# ❌ WRONG - Manual init override
class BadState(BaseModel):
    def __init__(self, **data):
        super().__init__(**data)
        self.setup_tools()  # This breaks Pydantic!

# ✅ CORRECT - Use validators
class GoodState(BaseModel):
    @model_validator(mode="after")
    def setup_state(self) -> "GoodState":
        self._setup_tools()
        return self
```

---

Remember: Good planning is about decomposition, dependency management, and adaptability. Start with clear objectives and build plans that can handle real-world complexity. Always build on existing patterns rather than reinventing the wheel!
