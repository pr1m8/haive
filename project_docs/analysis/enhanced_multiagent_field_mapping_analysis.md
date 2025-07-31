# EnhancedMultiAgent V3 Field Mapping Analysis

**Date**: 2025-01-21  
**Status**: Complete Analysis with Action Plan  

## 🔍 **Executive Summary**

After analyzing EnhancedMultiAgent V3, AgentNode V3, and SimpleAgent configurations, I've identified key issues and solutions for dynamic field mapping and engine configuration.

## 🎯 **Key Findings**

### 1. EnhancedMultiAgent V3 Field Handling

**Current State:**
- Uses AgentNodeV3 for execution which supports field projections
- Has `shared_fields` concept for cross-agent data sharing
- Supports both dict and list agent configurations
- Handles structured output from agents

**Issues:**
- No direct field remapping at the MultiAgent level
- Relies on AgentNodeV3 for field transformations
- Limited support for "output field X as field Y" patterns

### 2. AgentNode V3 Configuration Analysis

**Projection System:**
```python
# AgentNodeV3 projects state for each agent:
def _project_state_for_agent(self, state, agent):
    # 1. Start with agent's isolated state
    agent_state = agent_states.get(agent_name, {})
    
    # 2. Add shared fields from container
    for field in shared_fields:
        if hasattr(state, field):
            projected[field] = getattr(state, field)
    
    # 3. Agent sees combined view
    return projected
```

**Field Mapping Support:**
- `input_fields`: Can be list (direct) or dict (mapped)
- `output_fields`: Can be list (direct) or dict (mapped)
- `structured_output`: Direct field updates when agent has output_schema

### 3. SimpleAgent Engine Configuration

**Current Implementation:**
```python
# SimpleAgent correctly uses AugLLMConfig
engine: AugLLMConfig = Field(...)

# Validator ensures it's always AugLLMConfig
@field_validator("engine", mode="before")
def ensure_aug_llm_config(cls, v):
    if v is None:
        return AugLLMConfig()
    # ... validation logic
```

**Status**: ✅ Working correctly - SimpleAgent uses proper engine configuration

### 4. Dynamic Field Mapping Capabilities

**Current Options:**

1. **EngineNode Level** (Basic):
   ```python
   # Map output fields
   output_fields = {"result": "potato"}  # agent.result → state.potato
   ```

2. **AgentNode Level** (Intermediate):
   ```python
   # Structured output mapping
   agent.output_schema = OutputModel  # Fields map directly to state
   ```

3. **NodeSchemaComposer** (Advanced - Not Yet Implemented):
   ```python
   # Complex transformations
   field_mappings = [
       FieldMapping(
           source_path="messages[-1].content",
           target_path="potato",
           transform=["strip", "uppercase"]
       )
   ]
   ```

## 📊 **Problem Analysis**

### Issue 1: Field Name Conflicts
**Problem**: Multiple agents might output to same field  
**Example**: Both agents output "result" → overwrites occur  
**Current Workaround**: Use agent-specific field names or `agent_outputs` dict  

### Issue 2: Limited Field Transformation
**Problem**: Can't easily map "agent.output.nested.field" → "state.simple_field"  
**Current Limitation**: Only supports top-level field mapping  
**Needed**: Path-based extraction with transformations  

### Issue 3: Type Preservation During Mapping
**Problem**: Field mapping doesn't guarantee type preservation  
**Risk**: `str` field mapped to `int` field causes runtime errors  
**Solution**: Type-aware mapping system  

### Issue 4: Multi-Agent State Coordination
**Problem**: Complex to coordinate state between sequential agents  
**Example**: Agent1.findings → Agent2.context requires manual setup  
**Needed**: Declarative state transfer rules  

## 🛠️ **Recommended Solutions**

### Solution 1: Implement NodeSchemaComposer

Create the missing NodeSchemaComposer for advanced field mapping:

```python
from typing import Any, Optional, List, Type
from dataclasses import dataclass
from pydantic import BaseModel

@dataclass
class FieldMapping:
    """Define how to map fields between schemas."""
    source_path: str  # "messages[-1].content" or "result.data"
    target_path: str  # "potato" or "output.processed"
    transform: Optional[List[str]] = None  # ["strip", "uppercase"]
    default: Any = None
    type_hint: Optional[Type] = None  # Preserve type info

class NodeSchemaComposer:
    """Compose node schemas with flexible field mapping."""
    
    def __init__(
        self,
        input_schema: Type[BaseModel],
        output_schema: Type[BaseModel],
        field_mappings: List[FieldMapping]
    ):
        self.input_schema = input_schema
        self.output_schema = output_schema
        self.field_mappings = field_mappings
    
    def extract_value(self, data: dict, path: str) -> Any:
        """Extract value from nested path."""
        # Implementation: support dot notation and array indices
        # "messages[-1].content" → data["messages"][-1]["content"]
        pass
    
    def apply_transforms(self, value: Any, transforms: List[str]) -> Any:
        """Apply transformation pipeline."""
        for transform in transforms:
            if transform == "strip" and isinstance(value, str):
                value = value.strip()
            elif transform == "uppercase" and isinstance(value, str):
                value = value.upper()
            # Add more transforms
        return value
    
    def map_fields(self, input_data: dict) -> dict:
        """Map fields from input to output schema."""
        output_data = {}
        
        for mapping in self.field_mappings:
            # Extract value
            value = self.extract_value(input_data, mapping.source_path)
            
            # Apply transforms
            if mapping.transform:
                value = self.apply_transforms(value, mapping.transform)
            
            # Set in output
            self.set_nested_value(output_data, mapping.target_path, value)
        
        return output_data
```

### Solution 2: Enhanced AgentNode Configuration

Extend AgentNode to support advanced mapping:

```python
class EnhancedAgentNode(AgentNodeV3):
    """AgentNode with advanced field mapping."""
    
    field_mappings: Optional[List[FieldMapping]] = None
    
    def invoke(self, state: StateType) -> StateType:
        # Regular agent execution
        result = super().invoke(state)
        
        # Apply field mappings if configured
        if self.field_mappings:
            composer = NodeSchemaComposer(
                input_schema=type(result),
                output_schema=type(state),
                field_mappings=self.field_mappings
            )
            mapped_data = composer.map_fields(result.model_dump())
            
            # Update state with mapped fields
            for key, value in mapped_data.items():
                setattr(state, key, value)
        
        return state
```

### Solution 3: MultiAgent Field Coordination

Add field coordination to EnhancedMultiAgent:

```python
class EnhancedMultiAgentV4(EnhancedMultiAgent):
    """MultiAgent with field coordination support."""
    
    # Define how fields transfer between agents
    field_transfers: Optional[Dict[Tuple[str, str], Dict[str, str]]] = None
    # Example: {("agent1", "agent2"): {"findings": "context"}}
    
    async def execute_sequential(self, input_data: Any) -> Any:
        """Execute with field transfers."""
        current_data = input_data
        
        for i, (agent_name, agent) in enumerate(self.agents.items()):
            # Execute agent
            result = await agent.arun(current_data)
            
            # Apply field transfers to next agent
            if i < len(self.agents) - 1:
                next_agent_name = list(self.agents.keys())[i + 1]
                transfer_key = (agent_name, next_agent_name)
                
                if transfer_key in self.field_transfers:
                    transfers = self.field_transfers[transfer_key]
                    # Map fields for next agent
                    transferred_data = {}
                    for source, target in transfers.items():
                        if hasattr(result, source):
                            transferred_data[target] = getattr(result, source)
                    
                    # Merge with result
                    if isinstance(result, dict):
                        result.update(transferred_data)
                    else:
                        for k, v in transferred_data.items():
                            setattr(result, k, v)
            
            current_data = result
        
        return current_data
```

### Solution 4: Declarative Field Mapping

Create a declarative API for field mapping:

```python
# Easy field mapping API
workflow = EnhancedMultiAgent.create(
    agents=[research_agent, analysis_agent, report_agent],
    execution_mode="sequential",
    field_mappings=[
        # Map research_agent.findings → analysis_agent.data
        FieldMap(from_agent="research_agent", from_field="findings",
                 to_agent="analysis_agent", to_field="data"),
        
        # Map analysis_agent.result → report_agent.content with transform
        FieldMap(from_agent="analysis_agent", from_field="result",
                 to_agent="report_agent", to_field="content",
                 transform=["strip", "format_markdown"]),
        
        # Map nested field with default
        FieldMap(from_agent="analysis_agent", 
                 from_field="metadata.confidence",
                 to_agent="report_agent", 
                 to_field="confidence_score",
                 default=0.5)
    ]
)
```

## 📋 **Implementation Plan**

### Phase 1: Core Infrastructure (Priority: High)
1. **Implement NodeSchemaComposer** 
   - Path-based field extraction
   - Transform pipeline
   - Type preservation
   - Default values

2. **Test Field Mapping**
   - Unit tests for path extraction
   - Transform pipeline tests
   - Type safety validation
   - Integration tests

### Phase 2: Agent Integration (Priority: High)
1. **Enhance AgentNode**
   - Add field_mappings support
   - Integrate NodeSchemaComposer
   - Maintain backward compatibility

2. **Update EnhancedMultiAgent**
   - Add field transfer support
   - Implement declarative API
   - Update documentation

### Phase 3: Advanced Features (Priority: Medium)
1. **Complex Transformations**
   - Custom transform functions
   - Conditional mappings
   - Aggregation support

2. **Performance Optimization**
   - Cache compiled mappings
   - Optimize path extraction
   - Parallel mapping execution

### Phase 4: Developer Experience (Priority: Medium)
1. **Validation Tools**
   - Schema compatibility checker
   - Mapping validator
   - Type mismatch warnings

2. **Documentation**
   - Field mapping guide
   - Common patterns
   - Migration guide

## 🎯 **Quick Wins Available Now**

### 1. Use Existing Dict Mapping

```python
# Available now in EngineNode
engine_config = EngineNodeConfig(
    output_fields={"result": "potato"}  # Maps result → potato
)
```

### 2. Use Structured Output

```python
# Define output schema for direct mapping
class AgentOutput(BaseModel):
    potato: str  # Will map to state.potato
    confidence: float

agent = SimpleAgent(
    engine=config,
    output_schema=AgentOutput
)
```

### 3. Manual Field Coordination

```python
# Current workaround for multi-agent
async def coordinate_agents(input_data):
    # Agent 1
    result1 = await agent1.arun(input_data)
    
    # Manual field mapping
    agent2_input = {
        "context": result1.get("findings"),  # Map findings → context
        "query": input_data.get("query")
    }
    
    # Agent 2
    result2 = await agent2.arun(agent2_input)
    return result2
```

## 🚀 **Next Steps**

1. **Immediate**: Use existing dict mapping for simple cases
2. **Short-term**: Implement NodeSchemaComposer for advanced mapping
3. **Medium-term**: Enhance MultiAgent with declarative field transfers
4. **Long-term**: Full type-safe field transformation system

## 📊 **Summary**

The current system has basic field mapping capabilities but lacks:
- Advanced path-based extraction
- Transform pipelines  
- Type-safe mapping
- Declarative multi-agent coordination

The proposed solutions will enable:
- `"result" → "potato"` with type preservation
- Complex nested field extraction
- Transform pipelines
- Declarative agent coordination

All while maintaining backward compatibility and improving developer experience.