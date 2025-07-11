# SimpleAgent Patterns and Tool Integration Guide

## Overview

This guide documents the patterns used in SimpleAgent for building agents with structured outputs and tool integration. SimpleAgent provides a streamlined interface while supporting sophisticated features through engine modification.

## Core SimpleAgent Pattern

### 1. Engine Schema Modification

SimpleAgent's key innovation is **dynamic schema modification** to incorporate structured outputs:

```python
class SimpleAgent(Agent):
    """Simple agent that modifies its engine to include structured output schema."""

    # The key field - structured output model
    structured_output_model: type[BaseModel] | None = Field(
        default=None, description="Structured output model"
    )

    def _modify_engine_schema(self) -> None:
        """MODIFY the engine's output schema to include structured output fields."""

        # Create schema composer
        composer = SchemaComposer(name=f"Enhanced{current_output_schema.__name__}")

        # Add enhanced messages field
        composer.add_standard_field("messages", use_enhanced=True)

        # Add structured output field with smart naming
        field_name = (
            self.structured_output_model.__name__.lower()
            .replace("response", "")
            .replace("result", "")
            .strip()
        )
        if not field_name:
            field_name = "structured_result"

        composer.add_field(
            name=field_name,
            field_type=Optional[self.structured_output_model],
            default=None,
            description=f"Structured output of type {self.structured_output_model.__name__}"
        )

        # Override engine's output schema
        self.engine.output_schema = composer.build()
```

### 2. Tool Routing and Node Detection

SimpleAgent automatically detects what nodes are needed based on tools:

```python
def get_tool_routes(self) -> dict[str, str]:
    """Get tool routes from engine."""
    # Tool routes determine which node handles each tool
    return {
        "calculate": "langchain_tool",    # -> tool_node
        "search": "langchain_tool",        # -> tool_node
        "analyze": "pydantic_model",       # -> parser_node
        "validate": "engine",              # -> stays in engine
    }

def _needs_tool_node(self) -> bool:
    """Check if we need a tool node for langchain tools."""
    tool_routes = self.get_tool_routes()
    langchain_tools = [
        tool for tool, route in tool_routes.items()
        if route in ["langchain_tool", "function", "tool_node"]
    ]
    return len(langchain_tools) > 0

def _needs_parser_node(self) -> bool:
    """Check if we need a parser node for pydantic models."""
    # Parser node needed for:
    # 1. Structured output models
    # 2. Custom output parsers
    # 3. Pydantic tool models
    has_structured_output = bool(self.structured_output_model)
    has_output_parser = self.output_parser is not None

    tool_routes = self.get_tool_routes()
    pydantic_tools = [
        tool for tool, route in tool_routes.items()
        if route == "pydantic_model"
    ]

    return has_structured_output or has_output_parser or len(pydantic_tools) > 0
```

### 3. Graph Building with Validation Node

SimpleAgent uses a ValidationNodeConfigV2 for intelligent routing:

```python
def build_graph(self) -> BaseGraph:
    """Build the agent graph with proper state initialization."""
    graph = BaseGraph(name=self.name)

    # Track available nodes
    available_nodes = []

    # Add main agent node
    engine_node = EngineNodeConfig(name="agent_node", engine=self.engine)
    graph.add_node("agent_node", engine_node)
    available_nodes.append("agent_node")

    # Add tool node if needed
    if self._needs_tool_node():
        tool_config = ToolNodeConfig(
            name="tool_node",
            engine_name=self.engine.name,
        )
        graph.add_node("tool_node", tool_config)
        available_nodes.append("tool_node")

    # Add parser node if needed
    if self._needs_parser_node():
        parser_config = ParserNodeConfigV2(
            name="parse_output",
            engine_name=self.engine.name,
        )
        graph.add_node("parse_output", parser_config)
        available_nodes.append("parse_output")

    # Create validation node with available nodes
    validation_config = ValidationNodeConfigV2(
        name="validation",
        engine_name=self.engine.name,
        tool_node="tool_node",
        parser_node="parse_output",
        available_nodes=available_nodes,
    )
    graph.add_node("validation", validation_config)

    # Routing logic
    if self._has_force_tool_use():
        # Force tools - always go to validation
        graph.add_edge("agent_node", "validation")
    else:
        # Conditional routing based on tool calls
        graph.add_conditional_edges(
            "agent_node", has_tool_calls,
            {True: "validation", False: END}
        )

    # Store metadata for state initialization
    graph.metadata["available_nodes"] = available_nodes
    graph.metadata["tool_routes"] = self.get_tool_routes()

    return graph
```

## Tool Type Patterns

### 1. LangChain Tools

Standard LangChain BaseTool implementations:

```python
from langchain_core.tools import tool

@tool
def search_web(query: str) -> str:
    """Search the web for information."""
    return f"Results for: {query}"

# These route to "langchain_tool" -> tool_node
```

### 2. Pydantic Model Tools

Tools that return structured data:

```python
from pydantic import BaseModel

class AnalysisResult(BaseModel):
    summary: str
    confidence: float
    key_points: List[str]

def analyze_data(data: str) -> AnalysisResult:
    """Analyze data and return structured result."""
    return AnalysisResult(
        summary="Analysis complete",
        confidence=0.95,
        key_points=["Point 1", "Point 2"]
    )

# These route to "pydantic_model" -> parser_node
```

### 3. Engine-Internal Tools

Tools that stay within the engine:

```python
# Tools marked with route="engine" stay in the engine
# Useful for simple transformations or validations
```

## Structured Output Patterns

### 1. Simple Structured Output

```python
class TaskResult(BaseModel):
    completed: bool
    result: str
    confidence: float

agent = SimpleAgent(
    engine=AugLLMConfig(model="gpt-4"),
    structured_output_model=TaskResult
)
```

### 2. Complex Nested Outputs

```python
class Step(BaseModel):
    action: str
    reasoning: str

class PlanResult(BaseModel):
    objective: str
    steps: List[Step]
    estimated_time: int

agent = SimpleAgent(
    engine=AugLLMConfig(model="gpt-4"),
    structured_output_model=PlanResult
)
```

### 3. Union Type Outputs

```python
class Success(BaseModel):
    result: str

class Failure(BaseModel):
    error: str
    retry_suggestions: List[str]

class TaskOutcome(BaseModel):
    outcome: Union[Success, Failure]

agent = SimpleAgent(
    engine=AugLLMConfig(model="gpt-4"),
    structured_output_model=TaskOutcome
)
```

## Engine Registry Pattern

SimpleAgent automatically registers engines for node discovery:

```python
def _register_engine_in_registry(self) -> None:
    """Register the engine in EngineRegistry so other nodes can find it."""
    from haive.core.engine.base import EngineRegistry

    registry = EngineRegistry.get_instance()

    if not registry.find(self.engine.name):
        registry.register(self.engine)
        logger.info(f"Registered engine '{self.engine.name}'")
```

## State Initialization Pattern

SimpleAgent ensures proper state initialization with tool routes:

```python
def create_runnable(self, runnable_config=None) -> Any:
    """Override to ensure state is properly initialized."""
    compiled = super().create_runnable(runnable_config)

    # Ensure initial state has tool_routes and available_nodes
    initial_values = {}

    if "tool_routes" in self.graph.metadata:
        initial_values["tool_routes"] = self.graph.metadata["tool_routes"]

    if "available_nodes" in self.graph.metadata:
        initial_values["available_nodes"] = self.graph.metadata["available_nodes"]

    return compiled
```

## Convenience Patterns

### 1. Field Syncing

SimpleAgent provides convenience fields that sync to the engine:

```python
agent = SimpleAgent(
    temperature=0.7,        # Syncs to engine.temperature
    max_tokens=1000,        # Syncs to engine.max_tokens
    tools=[search, calc],   # Syncs to engine.tools
    structured_output_model=MyModel  # Triggers schema modification
)
```

### 2. Factory Methods

```python
# From engine
agent = SimpleAgent.from_engine(
    engine=my_configured_engine,
    name="My Agent"
)

# With tools
agent = SimpleAgent.create_with_tools(
    tools=[search_tool, calc_tool],
    name="Tool Agent"
)
```

## Best Practices

### 1. Structured Output Naming

SimpleAgent intelligently names output fields:

- `AnalysisResult` -> `analysis` field
- `ResponseModel` -> `model` field (strips "Response")
- `Result` -> `structured_result` field (fallback)

### 2. Tool Organization

```python
# Group tools by type for clarity
langchain_tools = [search_web, fetch_data]
pydantic_tools = [analyze_data, validate_result]

agent = SimpleAgent(
    tools=langchain_tools + pydantic_tools,
    structured_output_model=FinalResult
)
```

### 3. Prompt Engineering with Structured Output

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an analysis agent. Always structure your response."),
    ("human", "{query}")
])

agent = SimpleAgent(
    prompt_template=prompt,
    structured_output_model=AnalysisResult
)
```

## Common Patterns

### 1. Analysis Agent

```python
class Analysis(BaseModel):
    summary: str
    key_findings: List[str]
    confidence: float
    recommendations: List[str]

agent = SimpleAgent(
    engine=AugLLMConfig(
        model="gpt-4",
        temperature=0.3,
        system_message="You are an expert analyst."
    ),
    structured_output_model=Analysis,
    tools=[research_tool, calculate_stats]
)
```

### 2. Decision Agent

```python
class Decision(BaseModel):
    choice: Literal["approve", "reject", "review"]
    reasoning: str
    confidence: float

agent = SimpleAgent(
    structured_output_model=Decision,
    force_tool_use=True  # Always use validation
)
```

### 3. Multi-Step Agent

```python
class StepResult(BaseModel):
    step_number: int
    action_taken: str
    result: str
    next_step: Optional[str]

agent = SimpleAgent(
    structured_output_model=StepResult,
    tools=[execute_step, check_progress]
)
```

## Summary

SimpleAgent provides a clean interface for building agents with:

- Automatic schema modification for structured outputs
- Intelligent tool routing based on tool types
- Automatic node creation based on requirements
- Proper state initialization with metadata
- Convenience features for common patterns

The key insight is that SimpleAgent modifies its engine schema dynamically, allowing structured outputs to be seamlessly integrated into the agent's workflow without complex configuration.
