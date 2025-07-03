# Enhance Existing Infrastructure - Claude Discovery Agent

**Date**: 2025-06-28  
**Focus**: Build on what's already there instead of rebuilding from scratch

## What We Already Have (That's Actually Good!)

### **1. NodeConfig Already Has Smart Field Extraction**

```python
# Lines 204-233 in base_config.py - ALREADY EXISTS!
def _extract_input(self, state: Any) -> Dict[str, Any]:
    """Extract input from state based on configuration."""

    if self.extract_fields is None:
        # Smart conversion already implemented
        if isinstance(state, BaseModel):
            return state.model_dump()
        elif isinstance(state, dict):
            return state
        # ... more smart handling

    # Support for both list and dict mapping - ALREADY THERE!
    if isinstance(self.extract_fields, list):
        # Extract listed fields
    elif isinstance(self.extract_fields, dict):
        # Map state fields to input fields
```

**This is already intelligent! We just need to enhance it.**

### **2. EngineNodeConfig Already Has Type-Aware Extraction**

```python
# Lines 331-373 in engine_node.py - ALREADY EXISTS!
def _extract_smart_input(self, state: StateLike, engine: Engine) -> Any:
    """Extract input using the most appropriate strategy."""

    # Strategy 1: Explicit mapping
    if self.input_fields:
        return self._extract_mapped_input(...)

    # Strategy 2: Schema-defined inputs
    schema_inputs = self._get_schema_inputs(state, engine.name)
    if schema_inputs:
        return self._extract_typed_input(state, schema_inputs, engine.engine_type)

    # Strategy 3: Engine-defined inputs
    engine_inputs = self._get_engine_inputs(engine)
    if engine_inputs:
        return self._extract_typed_input(state, engine_inputs, engine.engine_type)

# Type-specific extractors ALREADY EXIST!
extractors = {
    EngineType.RETRIEVER: self._extract_retriever_fields,
    EngineType.LLM: self._extract_llm_fields,
    EngineType.VECTOR_STORE: self._extract_vectorstore_fields,
    EngineType.EMBEDDINGS: self._extract_embeddings_fields,
    EngineType.AGENT: self._extract_agent_fields,
}
```

**This is already sophisticated! We just need to make it work better.**

### **3. NodeConfig Already Has Dynamic Routing Infrastructure**

```python
# Lines 192-247 in base_config.py - ALREADY EXISTS!
def _should_use_dynamic_routing(self) -> bool:
    """Check if dynamic routing should be used."""
    return self.routing_enabled and self.routing_strategy is not None

def _wrap_with_routing(self, result: Any, route: Union[str, List[str]], state: Any):
    """Wrap result with appropriate command type."""
    # Smart routing logic already there!
```

## What We Need to Enhance (Not Rebuild)

### **1. Enhance Schema-Defined Input Detection**

```python
# ENHANCE existing _get_schema_inputs method
def _get_schema_inputs(self, state: StateLike, engine_name: str) -> list[str] | None:
    """Get engine inputs from schema - ENHANCE THIS."""

    # Current implementation (lines 632-642)
    if not hasattr(state, "__engine_io_mappings__") or not engine_name:
        return None
    return getattr(state, "__engine_io_mappings__", {}).get(engine_name, {}).get("inputs")

    # ENHANCE: Add compatibility checking
    if not hasattr(state, "__engine_io_mappings__"):
        # NEW: Try to derive from engine compatibility
        return self._derive_schema_inputs_from_engine_compatibility(state, engine_name)

    # ENHANCE: Add fallback strategies
    mappings = getattr(state, "__engine_io_mappings__", {})
    if engine_name not in mappings:
        # NEW: Try engine type matching
        return self._find_compatible_engine_inputs(state, engine_name)
```

### **2. Enhance Engine Compatibility Detection**

```python
# ADD to existing EngineNodeConfig
def _get_engine_compatibility_info(self) -> Optional[EngineCompatibilityInfo]:
    """Get compatibility info from engine - NEW METHOD."""
    if not self.engine:
        return None

    # Build on existing get_input_fields/get_output_fields
    if hasattr(self.engine, 'get_input_fields') and hasattr(self.engine, 'get_output_fields'):
        return EngineCompatibilityInfo(
            required_inputs=set(self.engine.get_input_fields().keys()),
            provided_outputs=set(self.engine.get_output_fields().keys()),
            engine_type=getattr(self.engine, 'engine_type', None),
            input_types={k: v[0] for k, v in self.engine.get_input_fields().items()},
            output_types={k: v[0] for k, v in self.engine.get_output_fields().items()}
        )
    return None

def validate_state_compatibility(self, state_schema: type[BaseModel]) -> CompatibilityResult:
    """Validate compatibility with state schema - NEW METHOD."""
    compat_info = self._get_engine_compatibility_info()
    if not compat_info:
        return CompatibilityResult(compatible=True, reason="No engine compatibility info")

    # Check if state has required fields
    state_fields = set(state_schema.model_fields.keys())
    missing_fields = compat_info.required_inputs - state_fields

    if missing_fields:
        return CompatibilityResult(
            compatible=False,
            reason=f"Missing required fields: {missing_fields}"
        )

    return CompatibilityResult(compatible=True)
```

### **3. Enhance SchemaComposer with Engine Awareness**

```python
# ADD to existing SchemaComposer
@classmethod
def from_components_with_compatibility_checking(
    cls,
    components: list[Any],
    name: str = "ComposedState"
) -> type[BaseModel]:
    """Enhance existing from_components with compatibility checking."""

    composer = cls(name=name)
    compatibility_issues = []

    for component in components:
        # Use existing field extraction
        try:
            composer.add_fields_from_component(component)
        except Exception as e:
            compatibility_issues.append(f"Component {component}: {e}")

        # NEW: Add compatibility validation
        if hasattr(component, '_get_engine_compatibility_info'):
            compat_info = component._get_engine_compatibility_info()
            if compat_info:
                composer._track_engine_compatibility(component.name, compat_info)

    # NEW: Validate all components are compatible
    if compatibility_issues:
        logger.warning(f"Compatibility issues found: {compatibility_issues}")

    schema = composer.build()

    # NEW: Add engine I/O mappings to schema
    if hasattr(composer, '_engine_compatibilities'):
        schema.__engine_io_mappings__ = composer._build_io_mappings()

    return schema
```

### **4. Enhance BaseGraph with Smart Node Addition**

```python
# ADD to existing BaseGraph
def add_node_with_compatibility_checking(self, name: str, node: Any) -> bool:
    """Enhance existing add_node with optional compatibility checking."""

    # Use existing add_node for basic functionality
    try:
        # NEW: Pre-validation if node supports it
        if hasattr(node, 'validate_state_compatibility') and self.state_schema:
            result = node.validate_state_compatibility(self.state_schema)
            if not result.compatible:
                logger.warning(f"Node {name} compatibility issue: {result.reason}")
                # Could either fail or continue with warning

        # Use existing add_node method
        self.add_node(name, node)

        # NEW: Update schema if possible
        self._update_schema_for_new_node(name, node)

        return True

    except Exception as e:
        logger.error(f"Failed to add node {name}: {e}")
        return False

def _update_schema_for_new_node(self, name: str, node: Any):
    """Update graph's state schema to include new node's requirements."""
    # Only if we have schema awareness
    if not self.state_schema or not hasattr(node, '_get_engine_compatibility_info'):
        return

    # Get node's requirements
    compat_info = node._get_engine_compatibility_info()
    if not compat_info:
        return

    # Re-compose schema (build on existing SchemaComposer)
    # This would use the enhanced SchemaComposer above
```

### **5. Enhance Agent Schema Setup**

```python
# ENHANCE existing _setup_schemas in Agent
def _setup_schemas(self) -> None:
    """Generate schemas from available engines with enhanced compatibility."""

    # Keep all existing logic, just enhance the composer calls
    if engine_list:
        # REPLACE: Basic SchemaComposer call
        # self.state_schema = SchemaComposer.from_components(...)

        # WITH: Enhanced compatibility-aware version
        self.state_schema = SchemaComposer.from_components_with_compatibility_checking(
            components=engine_list,
            name=f"{self.__class__.__name__}State"
        )

        # NEW: Validate all engines are compatible
        self._validate_engine_compatibility()

def _validate_engine_compatibility(self):
    """Validate that all engines in this agent are compatible."""
    engine_nodes = []

    # Find all engine-based nodes (would be created in build_graph)
    for engine_name, engine in self.engines.items():
        # Create temporary node to check compatibility
        temp_node = EngineNodeConfig(name=f"{engine_name}_node", engine=engine)
        if hasattr(temp_node, 'validate_state_compatibility'):
            result = temp_node.validate_state_compatibility(self.state_schema)
            if not result.compatible:
                logger.warning(f"Engine {engine_name} compatibility issue: {result.reason}")
```

## Key Insight

**We're not rebuilding - we're enhancing the smart infrastructure that's already there:**

✅ **NodeConfig** already has intelligent field extraction - enhance it  
✅ **EngineNodeConfig** already has type-aware processing - enhance it  
✅ **SchemaComposer** already composes from components - enhance it  
✅ **BaseGraph** already manages nodes - enhance it  
✅ **Agent** already sets up schemas - enhance it

## Enhancement Strategy

1. **Add compatibility info extraction** to existing methods
2. **Add validation methods** to existing classes
3. **Enhance existing composer calls** with compatibility checking
4. **Add smart defaults** that work with existing infrastructure
5. **Keep all existing behavior** while adding new capabilities

This approach **builds on the good infrastructure that's already there** instead of starting over!
