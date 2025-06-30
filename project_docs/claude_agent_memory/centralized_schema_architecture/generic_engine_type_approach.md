# Generic EngineNodeConfig with Engine Type Parameter

**Date**: 2025-06-28  
**Focus**: Making EngineNodeConfig generic off engine type instead of separate classes

## The Generic Approach

### **Core Concept: One Class, Generic Over Engine Type**
```python
from typing import Generic, TypeVar
from haive.core.engine.base import Engine, EngineType

E = TypeVar('E', bound=Engine)

class EngineNodeConfig(NodeConfig, Generic[E]):
    """Generic engine node that inherits schemas from its engine type."""
    
    engine: E  # Generic engine type
    
    @property
    def input_schema(self) -> type[BaseModel]:
        """Inherit input schema from engine."""
        return self.engine.input_schema
    
    @property  
    def output_schema(self) -> type[BaseModel]:
        """Inherit output schema from engine."""
        return self.engine.output_schema
    
    def _extract_input(self, state) -> Dict[str, Any]:
        """Extract and validate using engine's input schema."""
        raw_input = super()._extract_input(state)
        
        # Validate using inherited input schema
        try:
            validated = self.input_schema(**raw_input)
            return validated.model_dump()
        except ValidationError as e:
            raise ValueError(f"Input validation failed for {self.engine.engine_type.value}: {e}")
    
    def _validate_output(self, result: Any) -> Dict[str, Any]:
        """Validate result using engine's output schema."""
        try:
            validated = self.output_schema(**result)
            return validated.model_dump()
        except ValidationError as e:
            logger.warning(f"Output validation failed for {self.engine.engine_type.value}: {e}")
            return result  # Fallback to unvalidated
```

### **Type Aliases for Specific Engine Types**
```python
# Create type aliases for common engine types
RetrieverNode = EngineNodeConfig[RetrieverEngine]
LLMNode = EngineNodeConfig[LLMEngine] 
VectorStoreNode = EngineNodeConfig[VectorStoreEngine]
EmbeddingsNode = EngineNodeConfig[EmbeddingsEngine]
AgentNode = EngineNodeConfig[AgentEngine]

# Usage with full type safety
def create_retriever_node(engine: RetrieverEngine, name: str) -> RetrieverNode:
    return EngineNodeConfig[RetrieverEngine](name=name, engine=engine)

def create_llm_node(engine: LLMEngine, name: str) -> LLMNode:
    return EngineNodeConfig[LLMEngine](name=name, engine=engine)
```

### **Generic Factory Function**
```python
def create_engine_node(engine: E, name: str, **kwargs) -> EngineNodeConfig[E]:
    """Generic factory that preserves engine type."""
    return EngineNodeConfig[E](name=name, engine=engine, **kwargs)

# Usage maintains type information
retriever_engine: RetrieverEngine = ...
retriever_node: EngineNodeConfig[RetrieverEngine] = create_engine_node(retriever_engine, "retriever")

# Type checker knows:
# - retriever_node.engine is RetrieverEngine
# - retriever_node.input_schema is RetrieverEngine.InputSchema
# - retriever_node.output_schema is RetrieverEngine.OutputSchema
```

## Engine-Type-Specific Behavior with Method Overloading

### **Runtime Dispatch Based on Engine Type**
```python
class EngineNodeConfig(NodeConfig, Generic[E]):
    def _extract_input_specialized(self, state) -> Dict[str, Any]:
        """Engine-type-specific extraction logic."""
        
        # Dispatch based on engine type
        if self.engine.engine_type == EngineType.RETRIEVER:
            return self._extract_retriever_input(state)
        elif self.engine.engine_type == EngineType.LLM:
            return self._extract_llm_input(state)
        elif self.engine.engine_type == EngineType.VECTOR_STORE:
            return self._extract_vectorstore_input(state)
        else:
            return self._extract_generic_input(state)
    
    def _extract_retriever_input(self, state) -> Dict[str, Any]:
        """Retriever-specific extraction logic."""
        raw_input = super()._extract_input(state)
        
        # Retriever-specific processing
        if 'query' in raw_input:
            raw_input['query'] = str(raw_input['query']).strip()
        if 'k' in raw_input:
            raw_input['k'] = max(1, min(100, int(raw_input['k'])))
        
        # Validate with inherited schema
        validated = self.input_schema(**raw_input)
        return validated.model_dump()
    
    def _extract_llm_input(self, state) -> Dict[str, Any]:
        """LLM-specific extraction logic."""
        raw_input = super()._extract_input(state)
        
        # LLM-specific processing
        if 'messages' in raw_input and not raw_input['messages']:
            raise ValueError("LLM requires non-empty messages")
        
        # Validate with inherited schema
        validated = self.input_schema(**raw_input)
        return validated.model_dump()
```

### **Type Guards for Engine-Specific Access**
```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from haive.core.engine.retriever import RetrieverEngine
    from haive.core.engine.llm import LLMEngine

class EngineNodeConfig(NodeConfig, Generic[E]):
    def as_retriever_node(self) -> 'EngineNodeConfig[RetrieverEngine]':
        """Type guard for retriever nodes."""
        if self.engine.engine_type != EngineType.RETRIEVER:
            raise TypeError(f"Node has {self.engine.engine_type}, not RETRIEVER")
        return self  # type: ignore
    
    def as_llm_node(self) -> 'EngineNodeConfig[LLMEngine]':
        """Type guard for LLM nodes."""
        if self.engine.engine_type != EngineType.LLM:
            raise TypeError(f"Node has {self.engine.engine_type}, not LLM")
        return self  # type: ignore

# Usage
node: EngineNodeConfig[Engine] = get_some_node()

# Type-safe access to retriever-specific features
if node.engine.engine_type == EngineType.RETRIEVER:
    retriever_node = node.as_retriever_node()
    # retriever_node.engine is now typed as RetrieverEngine
    retriever_config = retriever_node.engine.retriever_config
```

## Enhanced Generic Implementation

### **Protocol-Based Engine Requirements**
```python
from typing import Protocol

class SchemaAwareEngine(Protocol):
    """Protocol for engines that provide input/output schemas."""
    input_schema: type[BaseModel]
    output_schema: type[BaseModel]
    engine_type: EngineType

E = TypeVar('E', bound=SchemaAwareEngine)

class EngineNodeConfig(NodeConfig, Generic[E]):
    """Generic node that works with any schema-aware engine."""
    
    engine: E
    
    @model_validator(mode='after')
    def validate_engine_has_schemas(self) -> 'EngineNodeConfig[E]':
        """Ensure engine has required schemas."""
        if not hasattr(self.engine, 'input_schema') or self.engine.input_schema is None:
            raise ValueError(f"Engine {self.engine.name} missing input_schema")
        if not hasattr(self.engine, 'output_schema') or self.engine.output_schema is None:
            raise ValueError(f"Engine {self.engine.name} missing output_schema")
        return self
```

### **Specialized Factory Functions**
```python
def create_retriever_node(
    engine: RetrieverEngine, 
    name: str,
    **kwargs
) -> EngineNodeConfig[RetrieverEngine]:
    """Create a typed retriever node."""
    node = EngineNodeConfig[RetrieverEngine](name=name, engine=engine, **kwargs)
    
    # Add retriever-specific configuration
    if not hasattr(node, 'extract_fields'):
        node.extract_fields = ['query', 'k', 'filter']
    
    return node

def create_llm_node(
    engine: LLMEngine,
    name: str, 
    **kwargs
) -> EngineNodeConfig[LLMEngine]:
    """Create a typed LLM node."""
    node = EngineNodeConfig[LLMEngine](name=name, engine=engine, **kwargs)
    
    # Add LLM-specific configuration
    if not hasattr(node, 'extract_fields'):
        node.extract_fields = ['messages', 'temperature', 'max_tokens']
    
    return node
```

## Benefits of Generic Approach

### **1. Single Class, Multiple Types**
```python
# One implementation handles all engine types
EngineNodeConfig[RetrieverEngine]  # Typed for retrievers
EngineNodeConfig[LLMEngine]        # Typed for LLMs  
EngineNodeConfig[VectorStoreEngine] # Typed for vector stores
```

### **2. Full Type Safety**
```python
retriever_node: EngineNodeConfig[RetrieverEngine] = create_retriever_node(engine, "name")
# Type checker knows retriever_node.engine is RetrieverEngine
# Type checker knows input_schema is RetrieverEngine.InputSchema
```

### **3. Engine-Specific Behavior via Dispatch**
```python
# Runtime behavior adapts to engine type
node._extract_input(state)  # Calls appropriate engine-specific method
```

### **4. Clean Type Aliases**
```python
# Easy to use aliases
RetrieverNode = EngineNodeConfig[RetrieverEngine]
LLMNode = EngineNodeConfig[LLMEngine]
```

### **5. Backward Compatibility**
```python
# Existing code still works
EngineNodeConfig(name="node", engine=some_engine)  # Generic[Engine]
```

## Usage Examples

```python
# Create typed nodes
retriever: RetrieverEngine = create_retriever_engine(...)
llm: LLMEngine = create_llm_engine(...)

retriever_node: RetrieverNode = create_retriever_node(retriever, "retriever")
llm_node: LLMNode = create_llm_node(llm, "llm")

# Type-safe graph building
graph = BaseGraph(name="MyGraph")
graph.add_node("retriever", retriever_node)  # Knows it's RetrieverNode
graph.add_node("llm", llm_node)              # Knows it's LLMNode

# Engine schemas automatically inherited
assert retriever_node.input_schema == retriever.input_schema
assert llm_node.output_schema == llm.output_schema
```

This approach gives us **one generic class** that adapts to **any engine type** while maintaining **full type safety**!