# Planning and Execution Agent Patterns - Memory Guide

## Overview

This guide documents the key patterns and design approaches used in the Plan and Execute (p_and_e) agent architecture. These patterns demonstrate advanced agent design including structured outputs, multi-engine orchestration, and state management.

## Key Architectural Patterns

### 1. Multi-Engine Architecture

The p_and_e agent uses **three distinct engines** for different phases:

```python
# Planning Engine
self.engines["planner"] = AugLLMConfig(
    name="planner",
    structured_output_model=Plan,  # Structured output for plans
    structured_output_version="v2",
    prompt_template=planner_prompt,
)

# Execution Engine (with tools)
self.engines["executor"] = AugLLMConfig(
    name="executor", 
    prompt_template=executor_prompt,
    tools=self.tools,  # Tools available for execution
)

# Replanning Engine
self.engines["replanner"] = AugLLMConfig(
    name="replanner",
    structured_output_model=Act,  # Union type: Response | Plan
    structured_output_version="v2",
    prompt_template=replan_prompt,
)
```

**Key Insight**: Different phases of the agent workflow require different capabilities. Separating engines allows specialized configuration for each phase.

### 2. Structured Output Models (BaseModel Pattern)

The p_and_e agent demonstrates sophisticated use of Pydantic models for structured outputs:

#### Plan Model
```python
class Plan(BaseModel):
    """Complete execution plan with steps and metadata."""
    
    objective: str = Field(description="The main objective")
    steps: List[PlanStep] = Field(description="Ordered list of steps")
    total_steps: int = Field(description="Total number of steps")
    
    @computed_field
    @property
    def next_step(self) -> Optional[PlanStep]:
        """Get the next step ready for execution."""
        completed_ids = {s.step_id for s in self.completed_steps}
        for step in self.steps:
            if step.status == StepStatus.PENDING:
                if all(dep_id in completed_ids for dep_id in step.dependencies):
                    return step
        return None
```

#### Union Type for Decision Making
```python
class Response(BaseModel):
    """Response to user with final answer."""
    response: str = Field(description="Final response to user")

class Act(BaseModel):
    """Action to perform - either respond or continue with plan."""
    action: Union[Response, Plan] = Field(
        description="If you want to respond to user, use Response. "
        "If you need to further use tools, use Plan."
    )
```

**Key Insight**: Union types enable the agent to make decisions between different action types while maintaining type safety.

### 3. State Schema with Computed Fields

The state schema demonstrates advanced patterns for derived state:

```python
class PlanExecuteState(MessagesState):
    """Main state schema for Plan and Execute system."""
    
    # Core state
    plan: Optional[Plan] = Field(default=None)
    execution_results: List[ExecutionResult] = Field(default_factory=list)
    
    @computed_field
    @property
    def plan_status(self) -> str:
        """Get formatted plan status for executor."""
        if not self.plan:
            return "No plan available"
        
        lines = [
            f"Objective: {self.plan.objective}",
            f"Progress: {self.plan.progress_percentage:.1f}%",
            f"Completed: {len(self.plan.completed_steps)}",
        ]
        return "\n".join(lines)
    
    @computed_field
    @property
    def should_replan(self) -> bool:
        """Determine if replanning is needed."""
        if self.plan.has_failures and not self.plan.next_step:
            return True
        # Replan after every 3 steps for review
        completed_count = len(self.plan.completed_steps)
        if completed_count > 0 and completed_count % 3 == 0:
            return True
        return False
```

**Key Insight**: Computed fields provide a clean way to derive complex state without storing redundant data.

### 4. Prompt Engineering Patterns

The p_and_e agent uses sophisticated prompt templates:

```python
PLANNER_SYSTEM_MESSAGE = """You are an expert planning agent...

## Step Types:
- RESEARCH: Gathering information
- ANALYSIS: Processing data
- SYNTHESIS: Combining information
- VALIDATION: Verifying results
- ACTION: Performing tasks
- DECISION: Making choices

## Important Considerations:
- Number steps sequentially
- Each step should have clear expected output
- Consider potential failure points
"""

planner_prompt = ChatPromptTemplate.from_messages([
    ("system", PLANNER_SYSTEM_MESSAGE),
    MessagesPlaceholder(variable_name="messages", optional=True),
    ("human", "Create a detailed execution plan...")
])
```

**Key Insight**: Structured prompts with clear guidelines improve output quality and consistency.

### 5. Tool Integration Patterns

The p_and_e agent demonstrates clean tool integration:

```python
class PlanAndExecuteAgent(Agent):
    # Tools available to the agent
    tools: List[BaseTool] = Field(
        default_factory=list, 
        description="List of tools available to this agent"
    )
    
    def setup_agent(self) -> None:
        # Only executor engine gets tools
        self.engines["executor"] = AugLLMConfig(
            name="executor",
            tools=self.tools,  # Pass tools to executor
        )
```

**Key Insight**: Tools are assigned to specific engines based on their role in the workflow.

### 6. Conditional Routing with Graph Edges

The agent uses sophisticated routing logic:

```python
def check_plan_complete(state: PlanExecuteState) -> str:
    """Check if plan execution is complete or needs more steps."""
    if not state.plan:
        return "create_plan"
    
    if state.plan.is_complete:
        return "evaluate_progress"
    
    if state.plan.has_failures and not state.plan.next_step:
        return "evaluate_progress"
    
    # Periodic evaluation
    completed_count = len(state.plan.completed_steps)
    if completed_count > 0 and completed_count % 3 == 0:
        return "evaluate_progress"
    
    return "execute_step"

# In build_graph()
graph.add_conditional_edges(
    "execute_step",
    check_plan_complete,
    {
        "execute_step": "execute_step",
        "evaluate_progress": "evaluate_progress", 
        "create_plan": "create_plan",
    }
)
```

## Key Design Principles

### 1. Separation of Concerns
- **Planner**: Focuses on creating structured plans
- **Executor**: Handles tool usage and step execution
- **Replanner**: Makes strategic decisions about continuation

### 2. Type Safety Throughout
- All outputs are strongly typed with Pydantic models
- Union types enable flexible decision making
- Computed fields derive state without redundancy

### 3. Progressive Enhancement
- Start with basic state (MessagesState)
- Add domain-specific fields
- Use computed fields for derived values

### 4. Tool Routing Patterns
```python
# Tool types and their routing:
tool_routes = {
    "calculate": "langchain_tool",     # Goes to tool_node
    "search": "langchain_tool",         # Goes to tool_node  
    "analyze": "pydantic_model",        # Goes to parser_node
    "default": "main_engine"            # Stays in engine
}
```

### 5. State Management Best Practices
- Use `Field(default_factory=list)` for mutable defaults
- Implement validators for data consistency
- Use `@computed_field` for derived properties
- Keep state minimal and normalized

## Comparison with SimpleAgent

| Aspect | SimpleAgent | Plan & Execute Agent |
|--------|-------------|---------------------|
| Engines | Single engine | Multiple specialized engines |
| Output | Single structured output | Multiple output types (Plan, Act, Response) |
| Flow | Linear with optional tools | Complex orchestration with loops |
| State | Basic with tool routing | Rich state with execution tracking |
| Tools | All tools on single engine | Tools assigned to specific engines |

## Implementation Checklist

When building a SimpleAgent-based agent with these patterns:

1. **Define Your Models**
   - Create Pydantic models for all structured outputs
   - Use Union types for flexible decisions
   - Add computed fields for derived values

2. **Design Your State**
   - Extend from appropriate base (MessagesState, etc.)
   - Add domain-specific fields
   - Implement computed properties

3. **Configure Your Engines**
   - Assign structured_output_model
   - Set structured_output_version="v2"
   - Configure prompt templates

4. **Build Your Graph**
   - Use EngineNodeConfig for each engine
   - Add conditional routing where needed
   - Handle tool routing appropriately

5. **Handle Tool Types**
   - `langchain_tool`: Standard LangChain tools
   - `pydantic_model`: Structured outputs
   - `function`: Direct function calls

## Advanced Patterns

### Dynamic Schema Modification (from SimpleAgent)
```python
def _modify_engine_schema(self) -> None:
    """Modify engine's output schema to include structured fields."""
    composer = SchemaComposer(name=f"Enhanced{current_output_schema.__name__}")
    
    # Add enhanced messages field
    composer.add_standard_field("messages", use_enhanced=True)
    
    # Add structured output field
    composer.add_field(
        name=field_name,
        field_type=Optional[self.structured_output_model],
        default=None,
    )
    
    # Override engine's output schema
    self.engine.output_schema = composer.build()
```

### Validation Node Pattern (from SimpleAgent)
```python
validation_config = ValidationNodeConfigV2(
    name="validation",
    engine_name=self.engine.name,
    tool_node="tool_node",
    parser_node="parse_output",
    available_nodes=available_nodes,
)
```

## Summary

The p_and_e agent demonstrates sophisticated patterns for:
- Multi-phase agent workflows
- Structured decision making with Union types
- Advanced state management with computed fields
- Clean separation of concerns
- Type-safe tool integration

These patterns can be adapted for SimpleAgent implementations to create more sophisticated agent behaviors while maintaining the simplicity of the SimpleAgent interface.