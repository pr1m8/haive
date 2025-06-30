# Engine Reference Pattern - The Key to Type Safety

**Date**: 2025-06-28  
**Focus**: Understanding how engine_name references work and where type safety breaks

## The Engine Reference System (Already Exists!)

### **How Engine References Work**
```python
# EngineNodeConfig can reference engines in two ways:
class EngineNodeConfig(NodeConfig):
    engine: Engine | None = Field(default=None)           # Direct reference
    engine_name: str | None = Field(default=None)         # Name reference

def _get_engine(self, state: StateLike | None = None) -> Engine | None:
    # Priority 1: Direct engine reference
    if self.engine:
        return self.engine
    
    # Priority 2: Get from state's engines dict using engine_name
    if self.engine_name and state:
        if hasattr(state, "engines"):
            engines_dict = getattr(state, "engines", {})
            if self.engine_name in engines_dict:
                engine = engines_dict[self.engine_name]
                self.engine = engine  # Cache it!
                return engine
```

### **The State Schema Engine Registry**
```python
# State schemas already have engine storage!
class StateSchema:
    engines: dict[str, Engine] = Field(default_factory=dict)  # Engine registry!
    
    def get_class_engine(self, name: str) -> Engine | None:
        """Get engine by name from class-level storage."""
        
    def get_all_class_engines(self) -> dict[str, Engine]:
        """Get all engines stored at class level."""
```

## Where Type Safety Actually Breaks

### **The Real Issue: Lazy Engine Resolution**

**Problem 1: Engine Retrieved Too Late**
```python
def _extract_smart_input(self, state, engine):
    # Engine is already resolved here - TOO LATE!
    
    # Strategy 3: Engine-defined inputs
    engine_inputs = self._get_engine_inputs(engine)
    if engine_inputs:
        return self._extract_typed_input(state, engine_inputs, engine.engine_type)
        
def _get_engine_inputs(self, engine: Engine) -> list[str] | None:
    if hasattr(engine, "get_input_fields"):
        return list(engine.get_input_fields().keys())  # LOSES TYPES!
    return None
```

**Problem 2: Type Information Available But Not Used**
```python
# Engine HAS type information
engine.get_input_fields() → {"query": (str, ""), "k": (int, 5)}

# But node only uses field names
engine_inputs = list(engine.get_input_fields().keys())  # ["query", "k"]

# Type info (str, int) is THROWN AWAY!
```

### **The Fix: Use Engine Reference for Type Information**

**Enhanced Engine Input Extraction**
```python
def _get_engine_inputs_with_types(self, engine: Engine) -> dict[str, tuple[type, Any]] | None:
    """Get input fields WITH type information."""
    if hasattr(engine, "get_input_fields"):
        return engine.get_input_fields()  # Keep the types!
    return None

def _extract_typed_input_enhanced(self, state, engine):
    """Extract input with actual type validation."""
    
    # Get engine inputs WITH types
    engine_fields = self._get_engine_inputs_with_types(engine)
    if not engine_fields:
        return self._extract_default_input(state, engine.engine_type)
    
    # Extract with type validation
    extracted = {}
    for field_name, (field_type, default_value) in engine_fields.items():
        raw_value = self._get_state_value(state, field_name, default_value)
        
        # TYPE VALIDATION HERE!
        validated_value = self._validate_and_convert_type(raw_value, field_type, field_name)
        extracted[field_name] = validated_value
    
    return extracted

def _validate_and_convert_type(self, value: Any, expected_type: type, field_name: str) -> Any:
    """Validate and convert value to expected type."""
    if value is None:
        return None
        
    # Type validation with conversion attempts
    if expected_type == str:
        return str(value)
    elif expected_type == int:
        try:
            return int(value)
        except (ValueError, TypeError):
            raise TypeError(f"Field {field_name} expected int, got {type(value)}")
    elif expected_type == float:
        try:
            return float(value)
        except (ValueError, TypeError):
            raise TypeError(f"Field {field_name} expected float, got {type(value)}")
    # ... more type handling
    
    return value
```

### **Schema-Level Engine Reference Enhancement**

**Engine Compatibility Pre-Check**
```python
def _get_schema_inputs_with_types(self, state, engine_name: str) -> dict[str, tuple[type, Any]] | None:
    """Get engine inputs from schema WITH type information."""
    
    # Current method gets just field names
    if hasattr(state, "__engine_io_mappings__") and engine_name:
        field_names = getattr(state, "__engine_io_mappings__", {}).get(engine_name, {}).get("inputs")
        if field_names:
            # NEW: Get engine from state.engines to get types
            if hasattr(state, "engines") and engine_name in state.engines:
                engine = state.engines[engine_name]
                if hasattr(engine, "get_input_fields"):
                    all_fields = engine.get_input_fields()
                    # Return only the mapped fields with their types
                    return {name: all_fields[name] for name in field_names if name in all_fields}
    
    return None
```

### **Node Configuration Enhancement**

**Type-Aware Field Mapping**
```python
class EngineNodeConfig(NodeConfig):
    # Keep existing fields
    engine: Engine | None = Field(default=None)
    engine_name: str | None = Field(default=None)
    
    # ADD: Cache engine type information
    _engine_field_types: dict[str, tuple[type, Any]] = Field(default_factory=dict, exclude=True)
    
    def _cache_engine_types(self):
        """Cache engine type information for validation."""
        engine = self._get_engine()
        if engine and hasattr(engine, 'get_input_fields'):
            self._engine_field_types = engine.get_input_fields()
    
    def get_required_input_types(self) -> dict[str, type]:
        """Get required input field types for validation."""
        if not self._engine_field_types:
            self._cache_engine_types()
        return {name: field_type for name, (field_type, _) in self._engine_field_types.items()}
    
    def validate_state_has_required_fields(self, state_schema: type[BaseModel]) -> bool:
        """Validate that state schema has all required fields with correct types."""
        required_types = self.get_required_input_types()
        state_fields = state_schema.model_fields
        
        for field_name, required_type in required_types.items():
            if field_name not in state_fields:
                logger.error(f"Missing required field: {field_name}")
                return False
            
            state_field_type = state_fields[field_name].annotation
            if not self._is_type_compatible(state_field_type, required_type):
                logger.error(f"Type mismatch for {field_name}: state has {state_field_type}, engine needs {required_type}")
                return False
        
        return True
```

## The Key Insight

**The engine reference system is already there and working!** The issue is:

1. **Engine types are available** via `engine.get_input_fields()`
2. **Engine lookup works** via `engine_name` → `state.engines[name]`  
3. **Type information is discarded** instead of being used for validation

## The Enhancement Strategy

### **Use Engine References for Type Safety**
1. **Resolve engine earlier** to get type information during setup
2. **Cache engine field types** in node configuration
3. **Validate state compatibility** before execution
4. **Use typed extraction** during runtime

### **Schema Enhancement**
1. **Store engine type mappings** in `__engine_io_mappings__`
2. **Include type information** not just field names
3. **Validate engine compatibility** during schema composition

The engine reference pattern is **already solid** - we just need to **use it for type safety** instead of just field name lookup!