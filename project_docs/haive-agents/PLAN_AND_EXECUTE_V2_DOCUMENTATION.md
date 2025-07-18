# Plan and Execute Agent v2 Documentation

**Version**: 2.0  
**Purpose**: Complete guide to the Plan and Execute Agent v2 implementation  
**Last Updated**: 2025-01-16

## 🎯 Overview

The Plan and Execute Agent v2 is a sophisticated multi-agent system that breaks down complex tasks into manageable steps. It uses a sequential three-agent pattern: **Planner → Executor → Replanner**, with each agent specialized for its role.

## 🏗️ Architecture

### Core Pattern: Sequential Multi-Agent

```
User Query → Planner → Executor → Replanner → Loop/Response
     ↓           ↓         ↓          ↓
   Input      Create    Execute    Evaluate
             Plan      Steps      & Decide
```

### Agent Roles

1. **Planner** (SimpleAgent)
   - Creates structured plans with numbered steps
   - Uses `Plan` structured output model
   - Temperature: 0.7 (creative planning)

2. **Executor** (ReactAgent)
   - Executes individual steps using tools
   - Uses `ExecutionResult` structured output model
   - Temperature: 0.3 (focused execution)
   - Has access to tools (search, calculator, etc.)

3. **Replanner** (SimpleAgent)
   - Decides whether to continue or provide final response
   - Uses `Act` structured output model (Response | Plan)
   - Temperature: 0.5 (balanced decision-making)

## 📋 State Schema

### PlanAndExecuteState

```python
class PlanAndExecuteState(MultiAgentState):
    """State for Plan and Execute Agent v2."""

    # P&E specific fields
    input: str = Field(..., description="Original user query")
    plan: Optional[Plan] = Field(default=None, description="Current plan")
    past_steps: List[Step] = Field(default_factory=list, description="Completed steps")
    response: Optional[str] = Field(default=None, description="Current response")
    final_response: Optional[str] = Field(default=None, description="Final response")

    # Inherited from MultiAgentState:
    # - agents: Dict[str, Agent] (planner, executor, replanner)
    # - agent_states: Dict[str, Dict[str, Any]]
    # - agent_outputs: Dict[str, Any]
    # - execution tracking fields
    # - recompilation fields

    def update_past_steps(self, step: Step) -> None:
        """Add completed step to past_steps."""
        if step.is_complete():
            self.past_steps.append(step)
            if self.plan:
                self.plan.update_status()

    def get_next_step(self) -> Optional[Step]:
        """Get the next incomplete step."""
        if not self.plan:
            return None
        return self.plan.get_next_step()

    def is_plan_complete(self) -> bool:
        """Check if the plan is complete."""
        return self.plan is not None and self.plan.status == "complete"
```

## 📦 Data Models

### Plan Model

```python
class Plan(BaseModel):
    """A plan containing steps to execute."""

    description: str = Field(..., description="Overall description of the plan")
    steps: List[Step] = Field(default_factory=list, description="List of steps")
    status: Literal["not_started", "in_progress", "complete"] = Field(
        default="not_started", description="Overall status"
    )

    def update_status(self) -> None:
        """Update plan status based on step completion."""
        if all(step.is_complete() for step in self.steps):
            self.status = "complete"
        elif any(step.status == "in_progress" for step in self.steps):
            self.status = "in_progress"
        else:
            self.status = "not_started"
```

### Step Model

```python
class Step(BaseModel):
    """A step in the plan."""

    id: int = Field(..., description="Unique identifier")
    description: str = Field(..., description="What this step does")
    status: Literal["not_started", "in_progress", "complete"] = Field(
        default="not_started", description="Current status"
    )
    result: Optional[str] = Field(default=None, description="Execution result")

    def add_result(self, result: str) -> None:
        """Add result and mark step as complete."""
        self.result = result
        self.status = "complete"
```

### Action Models

```python
class Response(BaseModel):
    """Final response to user."""
    response: str = Field(..., description="The final response")

class Act(BaseModel):
    """Action to take - either respond or create new plan."""
    action: Response | Plan = Field(
        ..., description="Use Response for final answer, Plan for more steps"
    )

class ExecutionResult(BaseModel):
    """Result of executing a step."""
    step_id: Optional[int] = Field(default=None, description="Step ID executed")
    result: str = Field(..., description="Execution result")
    step_completed: bool = Field(default=False, description="Whether step is complete")
```

## 🚀 Usage Examples

### Basic Usage

```python
from haive.agents.planning.plan_and_execute.v2.agent import PlanAndExecuteAgent
from haive.tools.tools.search_tools import tavily_search_tool

# Create P&E agent
agent = PlanAndExecuteAgent.create_default(
    tools=[tavily_search_tool],
    name="research_agent"
)

# Execute complex task
result = await agent.arun("Research the latest developments in quantum computing")
```

### With Multiple Tools

```python
from haive.tools.tools.search_tools import tavily_search_tool
from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions."""
    return str(eval(expression))

# Create agent with multiple tools
agent = PlanAndExecuteAgent.create_default(
    tools=[tavily_search_tool, calculator],
    name="research_and_analyze"
)

# Execute task requiring both search and calculation
result = await agent.arun(
    "Find the current market cap of Tesla and calculate what a 10% increase would be"
)
```

### Custom Configuration

```python
# Create with custom configuration
agent = PlanAndExecuteAgent.create_default(
    tools=[tavily_search_tool],
    name="custom_pe_agent",
    execution_mode="sequential",
    parallel_wait_for_all=True
)

# Access agent components
planner = agent.get_agent("planner")
executor = agent.get_agent("executor")
replanner = agent.get_agent("replanner")
```

## 🔄 Execution Flow

### Phase 1: Planning

1. **Input**: User query received
2. **Planner Agent**: Creates structured plan
3. **Output**: `Plan` object with numbered steps

```python
# Example planner output
{
    "description": "Research quantum computing developments",
    "steps": [
        {"id": 1, "description": "Search for recent quantum computing news"},
        {"id": 2, "description": "Identify key breakthrough technologies"},
        {"id": 3, "description": "Summarize findings with key insights"}
    ],
    "status": "not_started"
}
```

### Phase 2: Execution

1. **Executor Agent**: Takes next incomplete step
2. **Tool Usage**: Uses available tools to execute step
3. **Result**: `ExecutionResult` with step completion

```python
# Example executor output
{
    "step_id": 1,
    "result": "Found 5 recent articles on quantum computing breakthroughs...",
    "step_completed": True
}
```

### Phase 3: Replanning

1. **Replanner Agent**: Evaluates progress
2. **Decision**: Continue with more steps OR provide final response
3. **Output**: `Act` object with Response or new Plan

```python
# Example replanner output (continue)
{
    "action": {
        "description": "Continue with analysis",
        "steps": [
            {"id": 4, "description": "Analyze technical implications"}
        ]
    }
}

# Example replanner output (final response)
{
    "action": {
        "response": "Based on research, key quantum computing developments include..."
    }
}
```

## 📊 State Management

### Agent State Isolation

Each agent maintains its own isolated state within the MultiAgentState:

```python
# Access agent-specific state
planner_state = state.get_agent_state("planner")
executor_state = state.get_agent_state("executor")
replanner_state = state.get_agent_state("replanner")

# Update agent state
state.update_agent_state("planner", {"current_step": 1})
state.update_agent_state("executor", {"tools_used": ["search"]})
```

### Shared State Management

The PlanAndExecuteState provides shared context:

```python
# Shared across all agents
state.input = "Original user query"
state.plan = current_plan
state.past_steps = completed_steps
state.response = current_response
```

### Execution Tracking

```python
# Track execution order
state.agent_execution_order = ["planner", "executor", "replanner"]

# Record agent outputs
state.record_agent_output("planner", plan_result)
state.record_agent_output("executor", execution_result)
state.record_agent_output("replanner", decision_result)
```

## 🛠️ Agent Helper Methods

### PlanAndExecuteAgent Methods

```python
def should_continue_execution(self, state: PlanAndExecuteState) -> bool:
    """Check if execution should continue based on state."""
    if not state.plan:
        return False

    # Check if all steps are complete
    if all(step.status == "complete" for step in state.plan.steps):
        return False

    # Check if we have a final response
    if state.response and "final response" in state.response.lower():
        return False

    return True

def get_next_action(self, state: PlanAndExecuteState) -> str:
    """Determine next action based on current state."""
    if not state.plan:
        return "planner"

    # Check if we have incomplete steps
    next_step = state.get_next_step()
    if next_step and next_step.status in ["not_started", "in_progress"]:
        return "executor"

    # Check if we need to replan
    if self.should_continue_execution(state):
        return "replanner"

    return "end"
```

### Result Processing

```python
def process_execution_result(self, state: PlanAndExecuteState, result: ExecutionResult) -> PlanAndExecuteState:
    """Process execution result and update state."""
    if result.step_id:
        # Find and update the step
        for step in state.plan.steps:
            if step.id == result.step_id:
                step.add_result(result.result)
                break

    # Update response
    state.response = result.result

    # Add to past steps if complete
    if result.step_completed:
        completed_step = state.get_next_step()
        if completed_step:
            state.update_past_steps(completed_step)

    return state

def process_replan_result(self, state: PlanAndExecuteState, result: Act) -> PlanAndExecuteState:
    """Process replanning result and update state."""
    if isinstance(result.action, Response):
        # Final response - we're done
        state.response = result.action.response
        state.final_response = result.action.response
    elif isinstance(result.action, Plan):
        # New plan - update steps
        state.plan = result.action
        state.plan.update_status()

    return state
```

## 🧪 Testing

### Unit Tests

```python
def test_plan_and_execute_agent_creation():
    """Test creating P&E agent with default configuration."""
    agent = PlanAndExecuteAgent.create_default(
        tools=[Calculator()],
        name="test_pe_agent"
    )

    assert agent.name == "test_pe_agent"
    assert agent.execution_mode == "sequential"
    assert len(agent.agents) == 3

    agent_names = list(agent.agents.keys())
    assert "planner" in agent_names
    assert "executor" in agent_names
    assert "replanner" in agent_names
```

### Integration Tests

```python
@pytest.mark.asyncio
async def test_plan_and_execute_agent_real_execution():
    """Test P&E agent with real LLM execution."""
    agent = PlanAndExecuteAgent.create_default(
        tools=[Calculator()],
        name="test_pe_execution"
    )

    result = await agent.arun("Calculate 15 * 23")

    assert isinstance(result, str)
    assert len(result) > 0
    assert "345" in result or "15 * 23" in result
```

### State Tests

```python
def test_plan_and_execute_agent_methods():
    """Test P&E agent helper methods."""
    agent = PlanAndExecuteAgent.create_default(
        tools=[Calculator()],
        name="test_pe_methods"
    )

    test_state = PlanAndExecuteState(
        input="Test task",
        agents=agent.agents
    )

    # Test should_continue_execution with no plan
    assert not agent.should_continue_execution(test_state)

    # Test get_next_action with no plan
    assert agent.get_next_action(test_state) == "planner"
```

## 📈 Performance Considerations

### Execution Efficiency

- **Sequential Processing**: Each agent runs sequentially, not in parallel
- **State Persistence**: State is maintained across agent executions
- **Tool Reuse**: Executor agent reuses tools efficiently

### Memory Management

- **Isolated States**: Each agent's state is isolated
- **Shared Context**: Common data is shared through PlanAndExecuteState
- **Step History**: Completed steps are tracked for context

### Scalability

- **Tool Flexibility**: Supports any number of tools
- **Dynamic Planning**: Can adapt plans based on execution results
- **Recompilation**: Supports dynamic agent updates

## 🎯 Best Practices

### 1. Tool Selection

```python
# ✅ CORRECT - Use appropriate tools for the task
research_tools = [tavily_search_tool, web_scraper_tool]
math_tools = [calculator, statistics_tool]
file_tools = [file_reader, csv_analyzer]

# Create specialized agents
research_agent = PlanAndExecuteAgent.create_default(tools=research_tools)
analysis_agent = PlanAndExecuteAgent.create_default(tools=math_tools)
```

### 2. Query Formulation

```python
# ✅ CORRECT - Clear, specific queries
await agent.arun("Research Tesla's Q4 2024 earnings and calculate the year-over-year growth")

# ❌ WRONG - Vague queries
await agent.arun("Tell me about Tesla")
```

### 3. State Management

```python
# ✅ CORRECT - Use state methods
state.update_past_steps(completed_step)
state.record_agent_output("planner", result)

# ❌ WRONG - Direct state manipulation
state.past_steps.append(step)  # Bypasses validation
```

### 4. Error Handling

```python
# ✅ CORRECT - Handle execution errors
try:
    result = await agent.arun(query)
except Exception as e:
    logger.error(f"P&E execution failed: {e}")
    # Handle error appropriately
```

## 🚨 Common Issues

### 1. Tool Configuration

```python
# ❌ WRONG - Tools in engine config
executor_agent = ReactAgent(
    engine=AugLLMConfig(tools=[tool])  # Don't put tools here
)

# ✅ CORRECT - Tools in agent config
executor_agent = ReactAgent(
    engine=AugLLMConfig(),
    tools=[tool]  # Tools go here
)
```

### 2. State Schema Compatibility

```python
# ❌ WRONG - Not inheriting from MultiAgentState
class BadState(StateSchema):
    agents: Dict[str, Agent] = Field(...)  # Missing management logic

# ✅ CORRECT - Inherit from MultiAgentState
class GoodState(MultiAgentState):
    custom_field: str = Field(...)  # Adds to existing management
```

### 3. Agent Execution Order

```python
# ❌ WRONG - Wrong execution order
agent.agents = {"executor": executor, "planner": planner}  # Executor first

# ✅ CORRECT - Proper execution order
agent.agents = {"planner": planner, "executor": executor, "replanner": replanner}
```

## 🔗 Related Documentation

- [MultiAgentState Documentation](../active/architecture/multiagent_state_documentation.md)
- [ProperMultiAgent Documentation](../active/architecture/proper_multi_agent_documentation.md)
- [Agent-as-Tool Pattern](../active/architecture/agent_as_tool_pattern.md)

## 📝 Summary

The Plan and Execute Agent v2 provides:

1. **Structured Planning**: Breaks complex tasks into manageable steps
2. **Tool Integration**: Executor agent can use any available tools
3. **Dynamic Replanning**: Adapts plans based on execution results
4. **State Management**: Full state tracking with MultiAgentState
5. **Sequential Execution**: Coordinated three-agent workflow
6. **Type Safety**: Proper Pydantic models for all data structures

It's ideal for complex, multi-step tasks that require both planning and execution capabilities, making it perfect for research, analysis, and problem-solving workflows.

---

**Example Usage**:

```python
agent = PlanAndExecuteAgent.create_default(tools=[search_tool])
result = await agent.arun("Research AI trends and provide analysis")
```
