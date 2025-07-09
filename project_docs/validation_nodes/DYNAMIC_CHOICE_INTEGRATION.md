# Dynamic Choice Model and Validation Nodes

## Current State: No Integration

**Important**: None of the current validation nodes use `DynamicChoiceModel`. They operate on different principles:

- **Validation Nodes**: Process tool calls from AIMessages and route based on tool types
- **DynamicChoiceModel**: Creates runtime Pydantic models for constrained string choices

## Where DynamicChoiceModel IS Used

### 1. Dynamic Supervisor Agent
```python
# In supervisor agents for agent selection
from haive.core.common.models.dynamic_choice_model import DynamicChoiceModel

class DynamicSupervisorState(BaseModel):
    agent_choice_builder: DynamicChoiceModel = Field(
        default_factory=lambda: DynamicChoiceModel(
            options=["agent1", "agent2"],
            include_end=True
        )
    )
    
    @property
    def AgentChoice(self) -> Type[BaseModel]:
        """Get current agent choice model"""
        return self.agent_choice_builder.current_model
```

### 2. Game States (Clue, Mastermind)
```python
# For dynamic player/action choices in games
class ClueGameState(BaseModel):
    player_choice_model: DynamicChoiceModel[str] = Field(
        default_factory=lambda: DynamicChoiceModel(
            options=[],  # Populated with player names
            include_end=False
        )
    )
```

### 3. StructuredOutputMixin
```python
# For dynamic tool configuration
class StructuredOutputMixin:
    def with_structured_output(self, model: Type[BaseModel], ...):
        # Configures structured output models
        # Could potentially use DynamicChoiceModel for tool selection
```

## How Validation Nodes Work Instead

### Tool Route Detection
```python
# UnifiedValidationNode uses engine.tool_routes
def _get_tool_route(self, tool_name: str, engine: Any) -> str:
    # Check static tool routes dictionary
    tool_routes = getattr(engine, "tool_routes", {})
    if tool_name in tool_routes:
        return tool_routes[tool_name]
    
    # Returns: "pydantic_model", "langchain_tool", "function", etc.
```

### Fixed Routing Destinations
```python
# Validation nodes have fixed destination nodes
class UnifiedValidationNodeConfig(BaseNodeConfig):
    tool_node: str = "tool_node"  # Fixed name
    parse_output_node: str = "parse_output"  # Fixed name
    agent_node: str = "agent_node"  # Fixed name
```

## Potential Future Integration

### Concept: Dynamic Validation Router
```python
# CONCEPTUAL - Not implemented
class DynamicValidationNode(UnifiedValidationNodeConfig):
    """Validation node with dynamic routing choices"""
    
    route_choice_builder: DynamicChoiceModel = Field(
        default_factory=lambda: DynamicChoiceModel(
            options=["tool_node", "parse_output", "agent_node"],
            include_end=True
        )
    )
    
    def add_route_option(self, node_name: str):
        """Dynamically add a routing destination"""
        self.route_choice_builder.add_option(node_name)
    
    def _determine_destination(self, tool_type: str) -> str:
        """Use dynamic choice model for routing"""
        RouteChoice = self.route_choice_builder.current_model
        # Would need logic to map tool_type to valid route choices
```

### Use Cases for Dynamic Integration

1. **Multi-Tool-Node Systems**: Different tool nodes for different tool types
2. **Adaptive Routing**: Change routing based on conversation context
3. **Plugin Architecture**: Dynamically add new tool processors
4. **A/B Testing**: Route to different implementations dynamically

## Why Current Design Doesn't Need It

1. **Static Graph Structure**: LangGraph compiles graphs with fixed nodes
2. **Tool Routes Are Deterministic**: Tool type → destination mapping is clear
3. **Simplicity**: Fixed routing is easier to understand and debug
4. **Performance**: No runtime model generation overhead

## Key Insight

Validation nodes and DynamicChoiceModel serve different purposes:

- **Validation Nodes**: Infrastructure for processing tool calls
- **DynamicChoiceModel**: User-facing choice constraints for LLMs

They operate at different layers of the system and don't naturally overlap in current implementations.