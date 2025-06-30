# Pydantic Validators for Type Safety Enhancement

**Date**: 2025-06-28  
**Focus**: Using field_validator and model_validator to enhance existing engine reference system

## Current System + Pydantic Validators = Type Safety

### **Problem: Manual Type Checking**
```python
# Current: Manual type validation (messy)
def _validate_and_convert_type(self, value: Any, expected_type: type, field_name: str):
    if expected_type == str:
        return str(value)
    elif expected_type == int:
        try:
            return int(value)
        except (ValueError, TypeError):
            raise TypeError(f"Field {field_name} expected int, got {type(value)}")
    # ... lots of manual checking
```

### **Solution: Pydantic Validators (Clean)**
```python
# Better: Let Pydantic handle type validation automatically
class TypedInput(BaseModel):
    query: str
    k: int = 5
    
    @field_validator('k')
    @classmethod
    def validate_k(cls, v):
        if v < 1:
            raise ValueError('k must be positive')
        return v
```

## Enhanced EngineNodeConfig with Validators

### **1. Engine Compatibility Validation**
```python
class EngineNodeConfig(NodeConfig):
    engine: Engine | None = Field(default=None)
    engine_name: str | None = Field(default=None)
    
    @model_validator(mode='after')
    def validate_engine_reference(self) -> 'EngineNodeConfig':
        """Ensure we have either engine or engine_name."""
        if not self.engine and not self.engine_name:
            raise ValueError("Must provide either 'engine' or 'engine_name'")
        return self
    
    @field_validator('engine')
    @classmethod
    def validate_engine_has_contracts(cls, v: Engine | None):
        """Validate engine has required interface."""
        if v is None:
            return v
        
        if not hasattr(v, 'get_input_fields'):
            raise ValueError(f"Engine {v.name} missing get_input_fields method")
        if not hasattr(v, 'get_output_fields'):
            raise ValueError(f"Engine {v.name} missing get_output_fields method")
        
        return v
```

### **2. Dynamic Input Schema Generation**
```python
class EngineNodeConfig(NodeConfig):
    # Cache for generated input schema
    _input_schema: type[BaseModel] | None = Field(default=None, exclude=True)
    
    def get_input_schema(self, state=None) -> type[BaseModel]:
        """Generate Pydantic schema from engine input fields."""
        if self._input_schema:
            return self._input_schema
        
        # Get engine (using existing logic)
        engine = self._get_engine(state)
        if not engine:
            raise ValueError(f"Cannot get engine for node {self.name}")
        
        # Get engine input fields with types
        input_fields = engine.get_input_fields()  # {"query": (str, ""), "k": (int, 5)}
        
        # Build Pydantic field definitions
        field_definitions = {}
        validators = {}
        
        for field_name, (field_type, default_value) in input_fields.items():
            # Create Pydantic field
            if default_value is not None:
                field_definitions[field_name] = (field_type, Field(default=default_value))
            else:
                field_definitions[field_name] = (field_type, Field(...))  # Required
            
            # Add engine-specific validators
            validator = self._create_field_validator(field_name, field_type, engine.engine_type)
            if validator:
                validators[f'validate_{field_name}'] = validator
        
        # Create dynamic Pydantic model
        input_schema = create_model(
            f'{self.name}Input',
            **field_definitions,
            __validators__=validators
        )
        
        self._input_schema = input_schema
        return input_schema
    
    def _create_field_validator(self, field_name: str, field_type: type, engine_type: EngineType):
        """Create engine-specific field validators."""
        
        # Retriever-specific validation
        if engine_type == EngineType.RETRIEVER:
            if field_name == "query":
                @field_validator('query')
                @classmethod
                def validate_query(cls, v):
                    if not v or not v.strip():
                        raise ValueError("Query cannot be empty")
                    return v.strip()
                return validate_query
            
            elif field_name == "k":
                @field_validator('k')
                @classmethod
                def validate_k(cls, v):
                    if v < 1 or v > 100:
                        raise ValueError("k must be between 1 and 100")
                    return v
                return validate_k
        
        # LLM-specific validation  
        elif engine_type == EngineType.LLM:
            if field_name == "messages":
                @field_validator('messages')
                @classmethod
                def validate_messages(cls, v):
                    if not v:
                        raise ValueError("Messages list cannot be empty")
                    return v
                return validate_messages
        
        return None
```

### **3. Type-Safe Input Extraction**
```python
def __call__(self, state: StateLike, config: ConfigLike | None = None) -> Command | Send:
    """Execute with Pydantic validation."""
    
    # Get typed input schema
    input_schema = self.get_input_schema(state)
    
    # Extract raw data
    raw_input = self._extract_raw_input(state)
    
    # Validate with Pydantic (automatic type conversion + validation)
    try:
        validated_input = input_schema(**raw_input)
        typed_input = validated_input.model_dump()
    except ValidationError as e:
        logger.error(f"Input validation failed for {self.name}: {e}")
        return Command(
            update={"error": f"Input validation failed: {e}"},
            goto=self.command_goto
        )
    
    # Execute engine with validated input
    engine = self._get_engine(state)
    result = engine.invoke(typed_input, config)
    
    # Wrap result
    return self._wrap_smart_result(result, state, engine)
```

## Schema-Level Validation Enhancement

### **1. State Schema with Engine Contracts**
```python
class StateSchemaWithEngineValidation(StateSchema):
    """Enhanced state schema that validates engine compatibility."""
    
    @model_validator(mode='after')
    def validate_engine_compatibility(self) -> 'StateSchemaWithEngineValidation':
        """Validate all engines are compatible with state fields."""
        
        if not hasattr(self, 'engines'):
            return self
        
        state_fields = set(self.model_fields.keys())
        
        for engine_name, engine in self.engines.items():
            if hasattr(engine, 'get_input_fields'):
                required_fields = set(engine.get_input_fields().keys())
                missing_fields = required_fields - state_fields
                
                if missing_fields:
                    raise ValueError(
                        f"Engine {engine_name} requires fields not in state: {missing_fields}"
                    )
        
        return self
    
    @field_validator('engines')
    @classmethod  
    def validate_engines_dict(cls, v):
        """Validate engines dictionary."""
        if not isinstance(v, dict):
            raise TypeError("Engines must be a dictionary")
        
        for name, engine in v.items():
            if not hasattr(engine, 'get_input_fields'):
                raise ValueError(f"Engine {name} missing get_input_fields method")
        
        return v
```

### **2. Graph with Node Compatibility Validation**
```python
class TypedBaseGraph(BaseGraph):
    """Enhanced BaseGraph with automatic compatibility validation."""
    
    @model_validator(mode='after')
    def validate_node_compatibility(self) -> 'TypedBaseGraph':
        """Validate all nodes are compatible with state schema."""
        
        if not self.state_schema:
            return self
        
        for node_name, node in self.nodes.items():
            if node is None:
                continue
                
            # Validate engine nodes
            if hasattr(node, 'get_input_schema'):
                try:
                    # This will validate engine compatibility
                    node_input_schema = node.get_input_schema()
                    
                    # Check state has required fields
                    self._validate_state_provides_node_inputs(node_input_schema, node_name)
                    
                except Exception as e:
                    raise ValueError(f"Node {node_name} compatibility error: {e}")
        
        return self
    
    def _validate_state_provides_node_inputs(self, node_input_schema: type[BaseModel], node_name: str):
        """Validate state schema provides all fields needed by node."""
        
        state_fields = set(self.state_schema.model_fields.keys())
        required_fields = set(node_input_schema.model_fields.keys())
        
        missing_fields = required_fields - state_fields
        if missing_fields:
            raise ValueError(
                f"Node {node_name} requires fields not in state: {missing_fields}"
            )
```

## Agent-Level Validation

### **1. Agent with Automatic Schema Validation**
```python
class TypedAgent(Agent):
    """Agent with automatic engine-schema validation."""
    
    @model_validator(mode='after')
    def validate_agent_composition(self) -> 'TypedAgent':
        """Validate entire agent composition."""
        
        # 1. Validate engines are compatible with each other
        self._validate_engine_compatibility()
        
        # 2. Force schema regeneration with validation
        if self.set_schema:
            self._setup_schemas_with_validation()
        
        # 3. Validate graph compatibility (when built)
        if hasattr(self, '_graph_built') and self._graph_built:
            self._validate_graph_compatibility()
        
        return self
    
    def _setup_schemas_with_validation(self):
        """Enhanced schema setup with compatibility validation."""
        
        # Use enhanced SchemaComposer
        if self.engines:
            self.state_schema = TypedSchemaComposer.from_engines_with_validation(
                engines=list(self.engines.values()),
                name=f"{self.__class__.__name__}State"
            )
    
    def add_engine(self, name: str, engine: Engine):
        """Add engine with automatic validation."""
        
        # Validate engine interface
        if not hasattr(engine, 'get_input_fields'):
            raise ValueError(f"Engine {name} missing get_input_fields method")
        
        # Add to engines
        self.engines[name] = engine
        
        # Regenerate schema with validation
        if self.set_schema:
            self._setup_schemas_with_validation()
            
        # Validate compatibility if graph exists
        if self.graph:
            self._validate_graph_compatibility()
```

## Key Benefits of Pydantic Validators

### **1. Automatic Type Conversion**
```python
# Input: {"k": "5"}  (string)
# Pydantic: Automatically converts to int(5)
# No manual conversion needed!
```

### **2. Rich Error Messages**
```python
# ValidationError with detailed field-level errors
# Much better than manual error handling
```

### **3. Composition-Time Validation**
```python
# Errors caught when creating objects, not at runtime
agent = TypedAgent(engines=engines)  # Validates immediately
```

### **4. Field-Specific Logic**
```python
@field_validator('query')
@classmethod
def validate_query(cls, v):
    # Custom validation per field type
    return v.strip()
```

This approach uses **Pydantic's built-in validation system** to make the existing engine reference pattern **type-safe and robust**!