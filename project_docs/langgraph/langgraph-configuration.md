# LangGraph: Configuration Management

## Overview

LangGraph's configuration system enables flexible runtime customization of agent workflows through two distinct phases: schema definition during graph creation and value provisioning during graph execution. This document analyzes the technical relationship between these phases and their implications for the Haive framework node system redesign.

## Core Conceptual Framework

### 1. Configuration Schema Definition (Creation Phase)

During graph creation, LangGraph allows developers to define a configuration schema:

```python  
class ConfigSchema(TypedDict):  
    model: Optional[str]  
    system_message: Optional[str]  

workflow = StateGraph(  
    AgentState,  
    config_schema=ConfigSchema  # Schema declaration  
)  
```

Key characteristics:  
- **Type Safety**: Enforces structural validation of runtime configs  
- **Discoverability**: Exposes available parameters via `graph.config_specs`  
- **Documentation**: Serves as machine-readable API contract  
- **Default Management**: Optional field definitions enable fallback values  

### 2. Runtime Configuration (Invocation Phase)

During graph invocation, specific configuration values are provided:

```python  
graph.invoke(  
    {"messages": [...]},  
    {"configurable": {"model": "gpt-4", "system_message": "..."}}  # Value injection  
)  
```

Execution features:  
- **Dynamic Overrides**: Swap components without graph recompilation  
- **Contextual Adaptation**: Adjust behavior per-invocation basis  
- **Multi-Tenancy**: Maintain isolated configurations for different users/sessions  
- **Hot Reloading**: Modify operational parameters during runtime  

## Architectural Comparison

| Aspect                | Creation Phase ConfigSchema          | Invocation Phase Configurable         |  
|-----------------------|---------------------------------------|----------------------------------------|  
| **Purpose**           | Define configurable interface        | Provide runtime values                 |  
| **Validation**        | Structural type checking             | Value compatibility checks             |  
| **Persistence**       | Baked into graph artifact            | Ephemeral per-execution context        |  
| **Access Pattern**    | Centralized schema definition        | Distributed value injection            |  
| **Modifiability**     | Requires graph recompilation         | Dynamic at invocation time             |  

## Implementation Patterns

### 1. Schema-Driven Development

```python  
class AgentConfig(TypedDict):  
    llm: Literal["claude3", "gpt-4"]  
    temperature: Annotated[float, Field(ge=0, le=1)]  
    retries: Annotated[int, Field(ge=0)]  

builder = StateGraph(AgentState, config_schema=AgentConfig)  
```

Benefits:  
- Enables IDE autocompletion for config fields  
- Generates OpenAPI-compatible documentation  
- Facilitates configuration versioning  

### 2. Runtime Configuration Strategies

```python  
# Multi-configuration manager  
config_store = {  
    "basic": {"model": "claude3", "temperature": 0.5},  
    "premium": {"model": "gpt-4", "temperature": 0.2}  
}  

def route_config(user_tier: str):  
    return {"configurable": config_store[user_tier]}  

graph.invoke(inputs, route_config("premium"))  
```

## Application to Haive Node System

For Haive's node system redesign, we should implement the following configuration patterns:

### 1. Engine Configuration Targeting

The node system should support precise engine targeting through a consistent configuration system:

```python
def create_engine_node(
    engine: Engine,
    config_mapping: Optional[Dict[str, str]] = None,
    command_goto: Optional[str] = None
) -> Callable:
    """Create a node function with configuration targeting."""
    
    def engine_node(state: Dict[str, Any]) -> Any:
        # Extract runtime config
        runtime_config = state.get("__runnable_config__")
        
        # Apply engine-specific configuration targeting
        if runtime_config and "configurable" in runtime_config:
            # Apply direct engine targeting by ID
            if "engine_configs" in runtime_config["configurable"]:
                engine_configs = runtime_config["configurable"]["engine_configs"]
                if engine.id in engine_configs:
                    # Apply targeted configuration
                    engine_specific_config = engine_configs[engine.id]
                    # Use config with engine
                    # ...
        
        # Execute engine with configuration
        # ...
    
    return engine_node
```

### 2. Schema-Based Configuration

Use schema definitions to drive configuration behavior:

```python
class LLMNodeConfig(BaseModel):
    """Configuration schema for LLM nodes."""
    temperature: float = Field(default=0.7, ge=0, le=1)
    max_tokens: Optional[int] = Field(default=None, ge=0)
    system_message: Optional[str] = Field(default=None)

# Use in node creation
def create_llm_node(
    llm_engine: Engine,
    config_schema: Type[BaseModel] = LLMNodeConfig,
    command_goto: Optional[str] = None
) -> Callable:
    """Create an LLM node with schema-based configuration."""
    # Implementation using config_schema
    pass
```

### 3. Configuration Inheritance

Support configuration inheritance from parent to child graphs:

```python
def create_subgraph_node(
    subgraph: StateGraph,
    shared_fields: Optional[List[str]] = None,
    inherit_config: bool = True,
    command_goto: Optional[str] = None
) -> Callable:
    """Create a subgraph node with configuration inheritance."""
    
    def subgraph_node(state: Dict[str, Any]) -> Any:
        # Extract runtime config
        runtime_config = state.get("__runnable_config__")
        
        # Create subgraph state with shared fields
        subgraph_state = {}
        if shared_fields:
            for field in shared_fields:
                if field in state:
                    subgraph_state[field] = state[field]
        
        # Pass configuration to subgraph if enabled
        if inherit_config and runtime_config:
            # Execute subgraph with parent config
            result = subgraph.invoke(subgraph_state, runtime_config)
        else:
            # Execute without config inheritance
            result = subgraph.invoke(subgraph_state)
        
        # Process result
        # ...
    
    return subgraph_node
```

### 4. Default Configuration

Provide default configuration with override capabilities:

```python
class DynamicGraph:
    """Enhanced graph builder with default configuration."""
    
    def __init__(
        self,
        state_schema: Optional[Type[StateSchema]] = None,
        components: Optional[List[Engine]] = None,
        default_config: Optional[Dict[str, Any]] = None
    ):
        self.state_schema = state_schema
        self.components = components or []
        self.default_config = default_config or {}
        
        # Setup continues...
    
    def set_default_config(self, config: Dict[str, Any]) -> None:
        """Set default configuration for graph invocation."""
        self.default_config = config
    
    def invoke(self, input_data: Any, runtime_config: Optional[Dict[str, Any]] = None) -> Any:
        """Invoke graph with merged configuration."""
        # Merge default and runtime configs
        if runtime_config:
            config = self._merge_configs(self.default_config, runtime_config)
        else:
            config = self.default_config
        
        # Invoke graph with merged config
        return self.graph.invoke(input_data, config)
```

## Conclusion

LangGraph's dual-phase configuration approach offers a powerful model for flexible agent workflows. By adopting similar patterns in Haive's node system redesign, we can create a more dynamic, configurable framework that supports:

1. **Engine-Level Configuration**: Precisely target specific engines with runtime parameters
2. **Schema-Driven Validation**: Ensure configuration values meet defined constraints
3. **Configuration Inheritance**: Cleanly propagate configuration through graph hierarchies
4. **Default Behaviors**: Provide sensible defaults while enabling runtime overrides

These patterns will enable Haive to support sophisticated multi-tenant architectures and dynamic behavior adjustment without compromising type safety or system integrity.
