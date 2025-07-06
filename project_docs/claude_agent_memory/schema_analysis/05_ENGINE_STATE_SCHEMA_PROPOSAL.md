# Engine State Schema Proposal - Simplification

**Memory Tag**: [MEM-101-E]  
**Parent**: [MEM-101] Schema Analysis  
**Purpose**: Proposal for simplified engine-based schema system  
**Date**: 2025-01-06

## 🎯 Problem Statement

Current issues with the schema system:

- Massive file sizes with complex inheritance
- Multiple ways to define engines (confusing)
- Schema generation is overly complex
- Too much magic happening behind the scenes
- Hard to understand what's going on

## 💡 Proposed Solution: EngineStateSchema

### Core Concept

Instead of complex schema composition, create a simple engine-focused schema that:

- Has ONE clear way to define the main engine
- Automatically handles common patterns
- Reduces inheritance depth
- Makes engine access explicit and simple

## 🏗️ Proposed Implementation

### 1. Simple EngineStateSchema Base

```python
class EngineStateSchema(StateSchema):
    """Simplified schema focused on single-engine patterns."""

    # THE engine - one clear place
    engine: Optional[Engine] = Field(
        default=None,
        description="The main engine for this agent"
    )

    # Common fields most agents need
    messages: List[BaseMessage] = Field(default_factory=list)

    @model_validator(mode="after")
    def setup_engine_access(self):
        """Make engine accessible in standard ways."""
        if self.engine:
            # For EngineNodeConfig compatibility
            if not hasattr(self, "engines"):
                self.engines = {}

            # Add main engine with standard names
            self.engines["main"] = self.engine
            self.engines[self.engine.name] = self.engine

            # Also set engine type variants
            engine_type = getattr(self.engine, "engine_type", "llm")
            self.engines[engine_type] = self.engine

        return self
```

### 2. Simplified Agent Base

```python
class SimplifiedAgent(Agent):
    """Cleaner agent base with less magic."""

    # Just one engine field
    engine: Engine = Field(
        ...,
        description="The main engine"
    )

    # Use EngineStateSchema by default
    state_schema: Type[StateSchema] = EngineStateSchema

    def setup_agent(self):
        """Minimal setup - just sync engine to state."""
        # Put engine in state schema if needed
        if hasattr(self.state_schema, "engine"):
            self.state_schema.engine = self.engine
```

### 3. LLM-Specific Schema

```python
class LLMStateSchema(EngineStateSchema):
    """Schema specifically for LLM agents."""

    # LLM-specific fields
    system_message: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None

    # Tools handled simply
    tools: List[Any] = Field(default_factory=list)
    tool_results: Dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def sync_llm_settings(self):
        """Sync settings to engine if it's an LLM."""
        if self.engine and hasattr(self.engine, "temperature"):
            if self.temperature is not None:
                self.engine.temperature = self.temperature
            if self.max_tokens is not None:
                self.engine.max_tokens = self.max_tokens
        return self
```

### 4. Multi-Engine Schema (When Needed)

```python
class MultiEngineStateSchema(EngineStateSchema):
    """Only use when you REALLY need multiple engines."""

    # Additional engines beyond main
    retriever: Optional[Engine] = None
    reranker: Optional[Engine] = None

    @model_validator(mode="after")
    def setup_all_engines(self):
        """Add all engines to engines dict."""
        super().setup_engine_access()

        if self.retriever:
            self.engines["retriever"] = self.retriever

        if self.reranker:
            self.engines["reranker"] = self.reranker

        return self
```

## 🎯 Benefits

### 1. **Clarity**

- ONE place for the main engine
- Clear when to use multi-engine
- Explicit over implicit

### 2. **Simplicity**

- Less inheritance depth
- Smaller, focused classes
- Easy to understand

### 3. **Compatibility**

- Still works with EngineNodeConfig
- Maintains engines dict for nodes
- But simpler mental model

### 4. **Performance**

- Less dynamic schema generation
- Fewer validation passes
- Smaller memory footprint

## 🔄 Migration Path

### From Current System

```python
# Old way - complex
class MyAgent(Agent):
    engines = {"llm": engine1, "tool": engine2}
    # Complex schema generation...

# New way - simple
class MyAgent(SimplifiedAgent):
    engine = my_llm_engine
    state_schema = LLMStateSchema
```

### For Multi-Agent

```python
# When you need multiple agents, be explicit
class TeamState(MultiAgentStateSchema):
    # Clear that this is multi-agent
    agent1: SimplifiedAgent
    agent2: SimplifiedAgent

    # Shared state
    shared_context: str = ""
```

## 📊 Comparison

| Aspect            | Current System  | Proposed System |
| ----------------- | --------------- | --------------- |
| Engine Definition | Multiple ways   | One clear way   |
| Schema Generation | Dynamic/Complex | Simple/Explicit |
| File Size         | Huge            | Small, focused  |
| Inheritance       | Deep            | Shallow         |
| Mental Model      | Complex         | Simple          |

## 🚀 Example Usage

### Simple LLM Agent

```python
class ChatAgent(SimplifiedAgent):
    """Just works out of the box."""

    engine: AugLLMConfig = Field(
        default_factory=lambda: AugLLMConfig(
            model="gpt-4",
            temperature=0.7
        )
    )

    state_schema = LLMStateSchema

    def build_graph(self):
        # Simple, clear graph
        graph = BaseGraph()
        graph.add_node("llm", EngineNodeConfig(
            engine_name="main"  # Always findable
        ))
        return graph
```

### With Tools

```python
class ToolAgent(SimplifiedAgent):
    engine: AugLLMConfig = Field(
        default_factory=lambda: AugLLMConfig(
            model="gpt-4",
            tools=[calculator, web_search]
        )
    )

    state_schema = LLMStateSchema  # Tools handled by schema
```

## 🤔 Open Questions

1. Should we keep SchemaComposer for advanced use cases?
2. How to handle backward compatibility?
3. Should engine type (LLM, Retriever) be more explicit?
4. Where should tool routing live - schema or engine?

## 📝 Next Steps

1. Prototype EngineStateSchema
2. Test with existing agents
3. Measure complexity reduction
4. Get feedback on API design
5. Plan migration strategy

---

**Status**: Proposal for discussion
**Goal**: Reduce complexity while maintaining functionality
