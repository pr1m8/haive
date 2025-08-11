# EnhancedMultiAgentV4 Usage Patterns and Node Architecture

## Overview

EnhancedMultiAgentV4 is the primary multi-agent orchestration pattern in Haive. It extends the base Agent class and implements the `build_graph()` method, enabling sophisticated multi-agent workflows with various execution modes.

## Key Features

1. **Enhanced Base Agent Pattern**: Properly extends Agent class
2. **Direct List Initialization**: Simple API with `agents=[agent1, agent2, ...]`
3. **Multiple Execution Modes**: Sequential, parallel, conditional, manual
4. **AgentNodeV3 Integration**: Advanced state projection for agent isolation
5. **MultiAgentState Management**: Type-safe state handling across agents
6. **Dynamic Graph Building**: Auto, manual, and lazy build modes

## Basic Usage Patterns

### 1. Sequential Pattern (ReactAgent → SimpleAgent)

```python
from haive.agents.multi.enhanced_multi_agent_v4 import EnhancedMultiAgentV4
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import tool
from pydantic import BaseModel, Field

# Create tools for ReactAgent
@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions."""
    return f"Result: {eval(expression)}"

# Define structured output for SimpleAgent
class AnalysisReport(BaseModel):
    summary: str = Field(description="Summary of findings")
    recommendations: list[str] = Field(description="Key recommendations")

# Create agents
reasoner = ReactAgent(
    name="reasoner",
    engine=AugLLMConfig(temperature=0.1),
    tools=[calculator],
    system_message="You are a reasoning agent. Use tools to analyze."
)

formatter = SimpleAgent(
    name="formatter",
    engine=AugLLMConfig(temperature=0.1),
    structured_output_model=AnalysisReport,
    system_message="Format the analysis into a structured report."
)

# Create sequential workflow
workflow = EnhancedMultiAgentV4(
    name="analysis_workflow",
    agents=[reasoner, formatter],  # Direct list initialization
    execution_mode="sequential"    # reasoner → formatter
)

# Execute
result = await workflow.arun({
    "messages": [{"role": "user", "content": "Calculate 15 * 23 and analyze"}]
})
```

### 2. Parallel Execution Pattern

```python
# Create multiple analysis agents
tech_analyst = SimpleAgent(
    name="tech_analyst",
    engine=AugLLMConfig(),
    system_message="Analyze technical aspects."
)

business_analyst = SimpleAgent(
    name="business_analyst",
    engine=AugLLMConfig(),
    system_message="Analyze business aspects."
)

user_analyst = SimpleAgent(
    name="user_analyst",
    engine=AugLLMConfig(),
    system_message="Analyze user experience aspects."
)

# Create parallel workflow
workflow = EnhancedMultiAgentV4(
    name="parallel_analysis",
    agents=[tech_analyst, business_analyst, user_analyst],
    execution_mode="parallel"  # All run simultaneously
)

# Execute parallel analysis
result = await workflow.arun({
    "messages": [{"role": "user", "content": "Analyze this product idea"}]
})
```

### 3. Conditional Routing Pattern

```python
# Create classifier and processing agents
classifier = SimpleAgent(
    name="classifier",
    engine=AugLLMConfig(),
    system_message="Classify as 'simple' or 'complex'."
)

simple_processor = SimpleAgent(
    name="simple_processor",
    engine=AugLLMConfig(),
    system_message="Handle simple requests."
)

complex_processor = ReactAgent(
    name="complex_processor",
    engine=AugLLMConfig(),
    tools=[calculator],
    system_message="Handle complex requests with tools."
)

# Create conditional workflow
workflow = EnhancedMultiAgentV4(
    name="adaptive_processor",
    agents=[classifier, simple_processor, complex_processor],
    execution_mode="conditional",
    build_mode="manual"  # We'll add routing manually
)

# Define routing condition
def route_by_complexity(state) -> bool:
    """Route based on classifier output."""
    messages = state.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and "complex" in str(msg.content).lower():
            return True
    return False

# Add conditional routing
workflow.add_conditional_edge(
    from_agent="classifier",
    condition=route_by_complexity,
    true_agent="complex_processor",
    false_agent="simple_processor"
)

# Build and execute
workflow.build()
result = await workflow.arun({"messages": [{"role": "user", "content": "..."}]})
```

### 4. Dynamic Agent Addition

```python
# Start with initial agent
workflow = EnhancedMultiAgentV4(
    name="dynamic_team",
    agents=[SimpleAgent(name="coordinator", engine=AugLLMConfig())],
    execution_mode="manual",
    build_mode="auto"  # Auto-rebuild on changes
)

# Later, add specialist dynamically
specialist = SimpleAgent(
    name="specialist",
    engine=AugLLMConfig(),
    system_message="You are a domain specialist."
)

workflow.add_agent(specialist)
workflow.add_edge("coordinator", "specialist")

# Continue execution with expanded team
result = await workflow.arun({"messages": [...]})
```

## Node Architecture

### AgentNodeV3 - Hierarchical State Projection

The core of multi-agent execution is AgentNodeV3, which provides:

1. **State Projection**: Projects MultiAgentState to agent-specific schemas
2. **Direct Field Updates**: Structured output agents update fields directly
3. **Type Safety**: Maintains schema validation throughout execution
4. **Dynamic Agent Lookup**: Resolves agents from state at runtime

```python
# AgentNodeV3 is created automatically for each agent
from haive.core.graph.node.agent_node_v3 import create_agent_node_v3

# This happens internally in EnhancedMultiAgentV4
node_config = create_agent_node_v3(
    agent_name="analyzer",
    agent=analyzer_agent
)
```

### CallableNodeConfig - Wrap Functions as Nodes

For simple logic, you can wrap functions as nodes:

```python
from haive.core.graph.node.callable_node import CallableNodeConfig

def check_threshold(messages: list, threshold: int = 100) -> bool:
    total_length = sum(len(msg.content) for msg in messages)
    return total_length > threshold

node = CallableNodeConfig(
    name="check_threshold",
    callable_func=check_threshold,
    goto_on_true="summarize",
    goto_on_false="continue"
)
```

### GenericEngineNodeConfig - Type-Safe Engine Nodes

For engine-based processing with type safety:

```python
from haive.core.graph.node.engine_node_generic import GenericEngineNodeConfig

# Define input/output schemas
class QueryInput(BaseModel):
    query: str
    context: Optional[str] = None

class QueryOutput(BaseModel):
    answer: str
    confidence: float

# Create type-safe engine node
node = GenericEngineNodeConfig[QueryInput, QueryOutput](
    name="query_processor",
    engine=my_engine,
    input_schema=QueryInput,
    output_schema=QueryOutput
)
```

## Testing Patterns

```python
import pytest
from haive.agents.multi.enhanced_multi_agent_v4 import EnhancedMultiAgentV4
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

@pytest.mark.asyncio
async def test_sequential_workflow():
    """Test sequential multi-agent execution."""
    # Create agents
    agent1 = SimpleAgent(
        name="agent1",
        engine=AugLLMConfig(temperature=0.1),
        system_message="First agent in pipeline."
    )

    agent2 = SimpleAgent(
        name="agent2",
        engine=AugLLMConfig(temperature=0.1),
        system_message="Second agent in pipeline."
    )

    # Create workflow
    workflow = EnhancedMultiAgentV4(
        name="test_workflow",
        agents=[agent1, agent2],
        execution_mode="sequential"
    )

    # Execute with real LLMs (no mocks!)
    result = await workflow.arun({
        "messages": [{"role": "user", "content": "Test message"}]
    })

    assert result is not None
    # Verify both agents participated
    assert len(workflow.agent_dict) == 2
```

## Key Implementation Details

1. **State Schema**: Always uses MultiAgentState for agent coordination
2. **Agent Conversion**: Converts list to dict internally for efficient lookup
3. **Graph Building**: Happens based on build_mode (auto/manual/lazy)
4. **Node Creation**: Each agent gets an AgentNodeV3 for proper state handling
5. **Execution Modes**:
   - Sequential: Chain agents one after another
   - Parallel: Execute all agents simultaneously
   - Conditional: Route based on conditions
   - Manual: Full control over edge creation

## Best Practices

1. **Use Descriptive Names**: Give agents clear, descriptive names
2. **Define Clear System Messages**: Each agent should have a specific purpose
3. **Use Structured Output**: For data flow between agents
4. **Test with Real LLMs**: Follow no-mocks testing philosophy
5. **Start Simple**: Begin with sequential, then add complexity

## Common Patterns

1. **Analysis → Formatting**: ReactAgent analyzes, SimpleAgent formats
2. **Classification → Processing**: Classify complexity, route to appropriate processor
3. **Parallel Analysis → Synthesis**: Multiple analysts, single synthesizer
4. **Dynamic Team Building**: Start with coordinator, add specialists as needed
5. **Error Handling**: Add error handler agents with conditional routing

## Integration with Other Components

- **MetaStateSchema**: For meta-capable agents
- **BaseGraph**: Graph construction and compilation
- **StateGraph**: Execution runtime
- **Tools**: ReactAgent can use any LangChain tools
- **Structured Output**: Pydantic models for cross-agent data flow
