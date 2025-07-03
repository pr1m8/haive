# Computed Field Approach - Zero Breaking Changes

**Date**: 2025-06-28  
**Focus**: Using computed_field to get engine schemas from existing engine/engine_name pattern

## The Non-Breaking Enhancement

### **Use Existing Engine Resolution + Computed Fields**

```python
from pydantic import computed_field

class EngineNodeConfig(NodeConfig):
    # Keep ALL existing fields exactly as they are
    engine: Engine | None = Field(default=None)
    engine_name: str | None = Field(default=None)

    # Keep existing _get_engine method exactly as is
    def _get_engine(self, state: StateLike | None = None) -> Engine | None:
        # Existing implementation stays unchanged
        # Priority 1: Direct engine reference
        if self.engine:
            return self.engine
        # Priority 2: Get from state's engines dict using engine_name
        if self.engine_name and state:
            # ... existing logic

    # ADD: Computed fields that use existing engine resolution
    @computed_field
    @property
    def input_schema(self) -> type[BaseModel] | None:
        """Get input schema from engine if available."""
        if self.engine and hasattr(self.engine, 'input_schema'):
            return self.engine.input_schema
        return None

    @computed_field
    @property
    def output_schema(self) -> type[BaseModel] | None:
        """Get output schema from engine if available."""
        if self.engine and hasattr(self.engine, 'output_schema'):
            return self.engine.output_schema
        return None

    @computed_field
    @property
    def engine_input_fields(self) -> dict[str, tuple[type, Any]] | None:
        """Get input field types from engine."""
        if self.engine and hasattr(self.engine, 'get_input_fields'):
            return self.engine.get_input_fields()
        return None

    @computed_field
    @property
    def engine_output_fields(self) -> dict[str, tuple[type, Any]] | None:
        """Get output field types from engine."""
        if self.engine and hasattr(self.engine, 'get_output_fields'):
            return self.engine.get_output_fields()
        return None
```

### **State-Aware Computed Fields**

```python
class EngineNodeConfig(NodeConfig):
    def get_input_schema_from_state(self, state: StateLike) -> type[BaseModel] | None:
        """Get input schema using state to resolve engine_name."""
        engine = self._get_engine(state)  # Use existing resolution
        if engine and hasattr(engine, 'input_schema'):
            return engine.input_schema
        return None

    def get_input_fields_from_state(self, state: StateLike) -> dict[str, tuple[type, Any]] | None:
        """Get input field types using state to resolve engine_name."""
        engine = self._get_engine(state)  # Use existing resolution
        if engine and hasattr(engine, 'get_input_fields'):
            return engine.get_input_fields()
        return None

    def validate_input_with_engine_schema(self, raw_input: dict, state: StateLike) -> dict[str, Any]:
        """Validate input using engine's schema if available."""
        # Try to get engine schema
        input_schema = self.get_input_schema_from_state(state)
        if input_schema:
            try:
                validated = input_schema(**raw_input)
                return validated.model_dump()
            except ValidationError as e:
                logger.warning(f"Engine schema validation failed: {e}")
                # Fall back to existing behavior

        # Fallback to existing extraction logic
        return raw_input
```

### **Enhanced Existing Methods (Non-Breaking)**

```python
class EngineNodeConfig(NodeConfig):
    def _extract_smart_input(self, state: StateLike, engine: Engine) -> Any:
        """ENHANCE existing method to use engine schemas when available."""

        # NEW: Try engine schema validation first
        if hasattr(engine, 'input_schema') and engine.input_schema:
            try:
                # Extract raw input using existing logic
                if self.input_fields:
                    raw_input = self._extract_mapped_input(
                        state, self._normalize_mapping(self.input_fields)
                    )
                else:
                    # Use existing extraction strategies
                    schema_inputs = self._get_schema_inputs(state, engine.name)
                    if schema_inputs:
                        raw_input = self._extract_typed_input(state, schema_inputs, engine.engine_type)
                    else:
                        engine_inputs = self._get_engine_inputs(engine)
                        if engine_inputs:
                            raw_input = self._extract_typed_input(state, engine_inputs, engine.engine_type)
                        else:
                            raw_input = self._extract_default_input(state, engine.engine_type)

                # NEW: Validate with engine schema if available
                validated = engine.input_schema(**raw_input)
                logger.debug(f"✅ Engine schema validation successful for {engine.name}")
                return validated.model_dump()

            except ValidationError as e:
                logger.warning(f"Engine schema validation failed for {engine.name}: {e}")
                # Fall through to existing logic
            except Exception as e:
                logger.debug(f"Schema validation error: {e}")
                # Fall through to existing logic

        # EXISTING: All original logic stays as fallback
        if self.input_fields:
            logger.debug("Using explicit input field mapping")
            return self._extract_mapped_input(
                state, self._normalize_mapping(self.input_fields)
            )

        # ... rest of existing method unchanged
```

### **Schema Composer Enhancement**

```python
class SchemaComposer:
    @classmethod
    def from_components_with_engine_schemas(
        cls,
        components: list[Any],
        name: str = "ComposedState"
    ) -> type[BaseModel]:
        """Enhanced version that uses engine schemas when available."""

        composer = cls(name=name)

        for component in components:
            # NEW: Check if component has computed schema fields
            if hasattr(component, 'input_schema') and component.input_schema:
                # Use engine's input schema
                composer.add_fields_from_model(component.input_schema)
                logger.debug(f"Added fields from {component.name} input schema")

            elif hasattr(component, 'engine_input_fields') and component.engine_input_fields:
                # Use engine's field definitions
                for field_name, (field_type, default) in component.engine_input_fields.items():
                    composer.add_field(field_name, field_type, default)
                logger.debug(f"Added engine fields from {component.name}")

            else:
                # EXISTING: Fall back to existing logic
                composer.add_fields_from_component(component)

        return composer.build()
```

### **Agent Enhancement (Non-Breaking)**

```python
class Agent:
    def _setup_schemas(self) -> None:
        """ENHANCE existing method to use engine schemas when available."""

        # Keep all existing logic exactly the same
        engine_list = []
        agent_list = []

        if self.engine:
            engine_list.append(self.engine)

        for name, component in self.engines.items():
            if isinstance(component, str):
                continue
            if isinstance(component, Agent):
                agent_list.append(component)
            else:
                engine_list.append(component)

        # EXISTING: All current schema creation logic
        if not self.state_schema:
            if agent_list:
                # Use AgentSchemaComposer for agents
                self.state_schema = AgentSchemaComposer.from_agents(...)
            elif engine_list:
                # ENHANCED: Try engine-schema-aware composition first
                try:
                    self.state_schema = SchemaComposer.from_components_with_engine_schemas(
                        components=engine_list,
                        name=f"{self.__class__.__name__}State"
                    )
                    logger.debug("Used engine schemas for state composition")
                except Exception as e:
                    logger.debug(f"Engine schema composition failed: {e}, falling back")
                    # EXISTING: Fall back to original logic
                    self.state_schema = SchemaComposer.from_components(
                        components=engine_list,
                        name=f"{self.__class__.__name__}State"
                    )

        # EXISTING: All other logic unchanged
        self._auto_derive_io_schemas()
```

### **Usage - Zero Breaking Changes**

```python
# Existing code works exactly as before
node = EngineNodeConfig(name="my_node", engine=my_engine)

# NEW: Can now access computed schema fields
if node.input_schema:
    print(f"Node has input schema: {node.input_schema}")

if node.engine_input_fields:
    print(f"Engine input fields: {node.engine_input_fields}")

# Existing engine_name resolution still works
node_with_name = EngineNodeConfig(name="my_node", engine_name="retriever")
# When used with state containing engines, computed fields work
schema = node_with_name.get_input_schema_from_state(state)
```

## Benefits

### **1. Zero Breaking Changes**

- All existing fields stay exactly the same
- All existing methods keep their original behavior
- Computed fields are additive only

### **2. Gradual Enhancement**

- New code can use computed schema fields
- Existing code continues to work
- Enhanced methods try new approach, fall back to old

### **3. Engine Name Resolution Works**

```python
# This pattern already works and gets enhanced
node = EngineNodeConfig(engine_name="my_retriever")
# When executed with state containing engines["my_retriever"]
# Computed fields and enhanced methods use the resolved engine
```

### **4. Backward Compatible Schema Composition**

```python
# Existing schema composition works
schema = SchemaComposer.from_components(engines)

# Enhanced version tries engine schemas first, falls back
schema = SchemaComposer.from_components_with_engine_schemas(engines)
```

### **5. Optional Type Safety**

```python
# If engines have schemas: type-safe validation
# If engines don't have schemas: existing behavior
# No forcing of breaking changes
```

This approach enhances the existing system **without breaking anything** while adding **optional type safety** through computed fields!
