# Inherit Engine Schemas Directly + Engine Type Overloading

**Date**: 2025-06-28  
**Focus**: Making nodes inherit engine schemas directly with engine-type-specific overloading

## The Inheritance Approach

### **Core Idea: Node = Engine + Execution Logic**
```python
# Instead of: Node generates schema from engine
# Use: Node IS the engine schema + execution wrapper

class EngineNodeConfig(NodeConfig):
    engine: Engine
    
    # Inherit engine's input/output schemas directly
    @property
    def input_schema(self) -> type[BaseModel]:
        return self.engine.input_schema  # Direct inheritance!
    
    @property  
    def output_schema(self) -> type[BaseModel]:
        return self.engine.output_schema  # Direct inheritance!
```

### **Engine Type Overloading Pattern**
```python
# Different node types for different engine types
class RetrieverNode(EngineNodeConfig):
    engine: RetrieverEngine  # Typed engine
    
    # Inherits RetrieverEngine.input_schema automatically
    # Can override for node-specific validation
    
class LLMNode(EngineNodeConfig):  
    engine: LLMEngine  # Typed engine
    
    # Inherits LLMEngine.input_schema automatically
    
class VectorStoreNode(EngineNodeConfig):
    engine: VectorStoreEngine  # Typed engine
```

## Implementation Strategy

### **1. Make Engines Have Required Schemas**
```python
# Enhance base Engine to require schemas
class Engine(ABC, BaseModel, Generic[TIn, TOut]):
    # Make these required, not optional
    input_schema: type[BaseModel] = Field(...)  # Required!
    output_schema: type[BaseModel] = Field(...)  # Required!
    
    def __init_subclass__(cls, **kwargs):
        """Ensure subclasses define schemas."""
        super().__init_subclass__(**kwargs)
        # Validate schemas are provided
        if not hasattr(cls, 'input_schema') or cls.input_schema is None:
            raise TypeError(f"{cls.__name__} must define input_schema")

# Engine types must define their schemas
class RetrieverEngine(Engine):
    class InputSchema(BaseModel):
        query: str = Field(..., description="Search query")
        k: int = Field(default=5, ge=1, le=100, description="Number of results")
        filter: Optional[Dict[str, Any]] = Field(default=None)
        
        @field_validator('query')
        @classmethod
        def validate_query(cls, v):
            if not v.strip():
                raise ValueError("Query cannot be empty")
            return v.strip()
    
    class OutputSchema(BaseModel):
        documents: List[Document] = Field(default_factory=list)
        scores: Optional[List[float]] = Field(default=None)
    
    input_schema: type[BaseModel] = InputSchema
    output_schema: type[BaseModel] = OutputSchema
```

### **2. Engine-Type-Specific Node Classes**
```python
class RetrieverNode(EngineNodeConfig):
    """Node specifically for retriever engines."""
    
    engine: RetrieverEngine  # Typed!
    node_type: NodeType = Field(default=NodeType.RETRIEVER)
    
    # Automatically inherits RetrieverEngine.InputSchema
    # Can add node-specific overrides
    
    @model_validator(mode='after')
    def validate_retriever_config(self):
        """Retriever-specific validation."""
        if self.engine.engine_type != EngineType.RETRIEVER:
            raise ValueError("RetrieverNode requires RetrieverEngine")
        return self
    
    def _extract_input(self, state) -> Dict[str, Any]:
        """Retriever-specific extraction logic."""
        # Use inherited input_schema for validation
        raw_input = super()._extract_input(state)
        
        # Validate using engine's InputSchema
        try:
            validated = self.engine.InputSchema(**raw_input)
            return validated.model_dump()
        except ValidationError as e:
            raise ValueError(f"Retriever input validation failed: {e}")

class LLMNode(EngineNodeConfig):
    """Node specifically for LLM engines."""
    
    engine: LLMEngine  # Typed!
    node_type: NodeType = Field(default=NodeType.LLM)
    
    @model_validator(mode='after') 
    def validate_llm_config(self):
        if self.engine.engine_type != EngineType.LLM:
            raise ValueError("LLMNode requires LLMEngine")
        return self
    
    def _extract_input(self, state) -> Dict[str, Any]:
        """LLM-specific extraction logic."""
        raw_input = super()._extract_input(state)
        
        # Validate using engine's InputSchema
        validated = self.engine.InputSchema(**raw_input)
        return validated.model_dump()
```

### **3. Factory Pattern for Node Creation**
```python
def create_engine_node(engine: Engine, name: str, **kwargs) -> EngineNodeConfig:
    """Factory that creates the right node type for the engine."""
    
    node_type_map = {
        EngineType.RETRIEVER: RetrieverNode,
        EngineType.LLM: LLMNode,
        EngineType.VECTOR_STORE: VectorStoreNode,
        EngineType.EMBEDDINGS: EmbeddingsNode,
        EngineType.AGENT: AgentNode,
    }
    
    node_class = node_type_map.get(engine.engine_type, EngineNodeConfig)
    return node_class(name=name, engine=engine, **kwargs)

# Usage
retriever_node = create_engine_node(my_retriever_engine, "retriever")
# Returns: RetrieverNode with inherited RetrieverEngine.InputSchema
```

### **4. Overloading for Node-Specific Behavior**
```python
class EnhancedRetrieverNode(RetrieverNode):
    """Retriever node with additional validation."""
    
    class EnhancedInputSchema(RetrieverEngine.InputSchema):
        """Inherit from engine schema and extend."""
        
        # Add node-specific fields
        max_retries: int = Field(default=3, ge=1, le=10)
        timeout: float = Field(default=30.0, gt=0)
        
        @field_validator('query')
        @classmethod
        def enhanced_query_validation(cls, v):
            # Call parent validation
            v = super().validate_query(v)
            
            # Add node-specific validation
            if len(v) > 1000:
                raise ValueError("Query too long for this node")
            return v
    
    # Override the inherited schema
    @property
    def input_schema(self) -> type[BaseModel]:
        return self.EnhancedInputSchema
```

### **5. Generic EngineNodeConfig as Fallback**
```python
class EngineNodeConfig(NodeConfig):
    """Generic engine node - inherits directly from engine."""
    
    engine: Engine  # Any engine type
    
    @property
    def input_schema(self) -> type[BaseModel]:
        """Inherit engine's input schema directly."""
        return self.engine.input_schema
    
    @property
    def output_schema(self) -> type[BaseModel]:
        """Inherit engine's output schema directly."""  
        return self.engine.output_schema
    
    def _extract_input(self, state) -> Dict[str, Any]:
        """Generic extraction using inherited schema."""
        raw_input = super()._extract_input(state)
        
        # Validate using inherited input schema
        try:
            validated = self.input_schema(**raw_input)
            return validated.model_dump()
        except ValidationError as e:
            raise ValueError(f"Input validation failed: {e}")
    
    def __call__(self, state, config=None):
        """Execute with inherited schema validation."""
        # Extract and validate using inherited schema
        validated_input = self._extract_input(state)
        
        # Execute engine
        result = self.engine.invoke(validated_input, config)
        
        # Validate output using inherited schema  
        try:
            validated_output = self.output_schema(**result)
            return self._wrap_result(validated_output.model_dump(), state)
        except ValidationError as e:
            logger.warning(f"Output validation failed: {e}")
            return self._wrap_result(result, state)  # Fallback
```

## Benefits of This Approach

### **1. True Inheritance**
```python
# Node IS the engine schema + execution logic
class RetrieverNode(EngineNodeConfig):
    engine: RetrieverEngine  # Automatically gets RetrieverEngine.InputSchema
```

### **2. Engine-Type-Specific Behavior**
```python
# Different node classes for different engine types
retriever_node = RetrieverNode(engine=retriever)  # Gets retriever-specific validation
llm_node = LLMNode(engine=llm)                    # Gets LLM-specific validation
```

### **3. Overloading for Customization**
```python
# Can extend inherited schemas
class CustomRetrieverNode(RetrieverNode):
    class CustomInputSchema(RetrieverEngine.InputSchema):
        # Add custom fields
        custom_field: str = "default"
```

### **4. Type Safety at Compile Time**
```python
# Typed engines ensure correct node types
def process_retriever(node: RetrieverNode):  # Type checker enforces this
    # node.engine is guaranteed to be RetrieverEngine
    # node.input_schema is guaranteed to be RetrieverEngine.InputSchema
```

### **5. Clean Factory Pattern**
```python
# Automatic node type selection
node = create_engine_node(engine, "my_node")  # Returns correct node type automatically
```

## Migration Path

### **Phase 1: Make Engine Schemas Required**
```python
# Enhance existing engines to have required schemas
class ExistingRetrieverEngine(Engine):
    input_schema = RetrieverInputSchema  # Add this
    output_schema = RetrieverOutputSchema  # Add this
```

### **Phase 2: Create Engine-Type-Specific Nodes**  
```python
# Create specialized node classes
class RetrieverNode(EngineNodeConfig): ...
class LLMNode(EngineNodeConfig): ...
```

### **Phase 3: Use Factory for New Code**
```python
# New code uses factory
node = create_engine_node(engine, name)
```

### **Phase 4: Migrate Existing Code**
```python
# Gradually migrate existing EngineNodeConfig usage
# old: EngineNodeConfig(engine=retriever)
# new: RetrieverNode(engine=retriever)
```

This approach makes nodes **truly inherit** from their engines while allowing **engine-type-specific overloading**!