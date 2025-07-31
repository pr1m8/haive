# Field Mapping Guide - Haive Framework

**Version**: 1.0  
**Date**: 2025-01-21  
**Status**: Available Now - Production Ready  

## 🎯 **Overview**

Field mapping in Haive allows you to transform data between different field names while preserving types. This is useful for connecting agents and engines that use different field names for the same data.

**Key Capability**: Map `agent.result` → `state.potato` with full type safety!

## 🚀 **Quick Start - Available Now**

### Basic Field Mapping (EngineNode Level)

```python
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.engine.aug_llm import AugLLMConfig

# Create engine with field mapping
engine = AugLLMConfig(name="my_engine")

# Create node with output field mapping
node_config = EngineNodeConfig(
    name="processor",
    engine=engine,
    output_fields={"result": "potato"}  # Maps engine output "result" → state "potato"
)
```

### Multi-Field Mapping

```python
# Map multiple fields
node_config = EngineNodeConfig(
    name="analyzer",
    engine=engine,
    input_fields={"query": "question", "context": "background"},  # Input mapping
    output_fields={"result": "answer", "confidence": "score"}     # Output mapping
)
```

## 📋 **Field Mapping Formats**

### 1. List Format (Identity Mapping)
```python
# Use specific fields as-is (no renaming)
input_fields = ["messages", "query"]      # Extract only these fields
output_fields = ["result", "metadata"]    # Output only these fields
```

### 2. Dict Format (Rename Mapping) 
```python
# Rename fields during mapping
input_fields = {
    "user_query": "query",        # state.user_query → engine.query
    "context_data": "context"     # state.context_data → engine.context
}

output_fields = {
    "result": "final_answer",     # engine.result → state.final_answer
    "confidence": "score"         # engine.confidence → state.score
}
```

## 🔧 **Real-World Examples**

### Example 1: RAG Agent with Custom Fields

```python
from haive.agents.rag.base import BaseRAGAgent
from haive.core.graph.node.engine_node import EngineNodeConfig

# Create RAG agent that outputs to custom field
class CustomRAGAgent(BaseRAGAgent):
    def build_graph(self):
        graph = super().build_graph()
        
        # Override retriever node to use custom output field
        retriever_node = EngineNodeConfig(
            name="retriever",
            engine=self.engines["retriever"],
            output_fields={"retrieved_documents": "research_data"}  # Custom mapping
        )
        
        graph.add_node("retriever", retriever_node)
        return graph
```

### Example 2: Multi-Agent Field Coordination

```python
from haive.agents.multi.enhanced_multi_agent_v3 import EnhancedMultiAgent

# Agent 1: Research → findings
research_agent = SimpleAgent(name="researcher")

# Agent 2: Analysis expects "data" field
analysis_agent = SimpleAgent(name="analyzer")

# Create coordinated workflow with field mapping
class CoordinatedWorkflow(EnhancedMultiAgent):
    def build_graph(self):
        graph = super().build_graph()
        
        # Add field mapping between agents
        research_node = EngineNodeConfig(
            name="researcher",
            agent=research_agent,
            output_fields={"findings": "data"}  # Map findings → data for next agent
        )
        
        graph.add_node("researcher", research_node)
        return graph
```

### Example 3: SimpleAgent with Custom Output

```python
from haive.agents.simple import SimpleAgent

# Create SimpleAgent with custom output field
agent = SimpleAgent(
    name="formatter",
    engine=AugLLMConfig(temperature=0.3)
)

# In your graph building, use field mapping
node_config = EngineNodeConfig(
    name="formatter",
    agent=agent,
    output_fields={"response": "formatted_output"}  # Custom field name
)
```

## 🏗️ **Implementation Patterns**

### Pattern 1: Agent Factory with Field Mapping

```python
def create_mapped_agent(
    agent_class,
    name: str,
    engine_config,
    input_mapping: dict = None,
    output_mapping: dict = None
):
    """Factory to create agents with field mapping."""
    agent = agent_class(name=name, engine=engine_config)
    
    # Apply field mapping at node level
    node_config = EngineNodeConfig(
        name=name,
        agent=agent,
        input_fields=input_mapping,
        output_fields=output_mapping
    )
    
    return agent, node_config

# Usage
agent, node = create_mapped_agent(
    SimpleAgent,
    "processor",
    AugLLMConfig(),
    output_mapping={"result": "potato"}
)
```

### Pattern 2: Workflow with Field Transitions

```python
class MappedWorkflow(EnhancedMultiAgent):
    """Workflow with automatic field mapping between agents."""
    
    def __init__(self, agents, field_mappings=None):
        super().__init__(agents=agents)
        self.field_mappings = field_mappings or {}
    
    def build_graph(self):
        graph = super().build_graph()
        
        # Apply field mappings to each agent node
        for i, (agent_name, agent) in enumerate(self.agents.items()):
            if agent_name in self.field_mappings:
                mapping = self.field_mappings[agent_name]
                
                node_config = EngineNodeConfig(
                    name=agent_name,
                    agent=agent,
                    input_fields=mapping.get("input", None),
                    output_fields=mapping.get("output", None)
                )
                
                graph.add_node(agent_name, node_config)
        
        return graph

# Usage
workflow = MappedWorkflow(
    agents=[research_agent, analysis_agent],
    field_mappings={
        "research_agent": {"output": {"findings": "data"}},
        "analysis_agent": {"output": {"result": "final_report"}}
    }
)
```

### Pattern 3: State Schema with Field Mapping

```python
from haive.core.schema.state_schema import StateSchema
from pydantic import Field

class MappedWorkflowState(StateSchema):
    """State schema that supports field mapping."""
    
    # Original fields
    query: str = Field(...)
    context: str = Field(default="")
    
    # Mapped fields (different names for same data)
    question: str = Field(default="")  # Maps from query
    background: str = Field(default="")  # Maps from context
    
    # Output fields
    result: str = Field(default="")
    potato: str = Field(default="")  # Custom output field
    
    def sync_mapped_fields(self):
        """Sync mapped fields after updates."""
        self.question = self.query
        self.background = self.context
```

## 📊 **Current Limitations**

### What's Available Now
- ✅ Basic field renaming (`"result" → "potato"`)
- ✅ Multiple field mapping 
- ✅ Input and output mapping
- ✅ Type preservation (dict values preserve types)
- ✅ Agent node integration

### What's Not Yet Available
- ❌ Path-based extraction (`"messages[-1].content"`)
- ❌ Transform pipelines (`["uppercase", "strip"]`)
- ❌ Complex nested field mapping
- ❌ Conditional field mapping
- ❌ Multi-agent field coordination (automatic)

## 🚀 **Advanced Usage (Future)**

### Planned: Path-Based Extraction
```python
# Future capability
field_mappings = [
    FieldMapping(
        source_path="messages[-1].content",  # Extract from last message
        target_path="potato",               # Map to simple field
        transform=["strip", "uppercase"]    # Apply transforms
    )
]
```

### Planned: Multi-Agent Coordination
```python
# Future capability
workflow = EnhancedMultiAgent.create(
    agents=[agent1, agent2],
    field_transfers={
        ("agent1", "agent2"): {"findings": "context"}  # Auto field transfer
    }
)
```

## 🎯 **Best Practices**

### 1. Use Descriptive Field Names
```python
# ✅ Good - Clear purpose
output_fields = {
    "analysis_result": "final_analysis",
    "confidence_score": "reliability"
}

# ❌ Bad - Unclear purpose  
output_fields = {"result": "data", "score": "num"}
```

### 2. Document Field Mappings
```python
class DocumentedAgent(SimpleAgent):
    """Agent with documented field mappings.
    
    Field Mappings:
        Input: query → question (user's question)
        Output: result → formatted_answer (processed response)
    """
    
    def build_graph(self):
        # Use documented mapping
        node = EngineNodeConfig(
            name=self.name,
            agent=self,
            input_fields={"query": "question"},
            output_fields={"result": "formatted_answer"}
        )
```

### 3. Test Field Mappings
```python
def test_field_mapping():
    """Test that field mapping works correctly."""
    agent = SimpleAgent(engine=AugLLMConfig())
    
    node = EngineNodeConfig(
        name="test",
        agent=agent,
        output_fields={"result": "potato"}
    )
    
    # Test with mock state
    result = node(test_state)
    assert hasattr(result, "potato")  # Mapped field exists
    assert result.potato == expected_value  # Correct value
```

## 🔗 **Related Documentation**

- [Multi-Agent Workflow Guide](multi_agent_workflows.md) - Building complex workflows
- [SimpleRAG Guide](simple_rag_complete.md) - RAG with field mapping
- [Node Configuration Guide](../haive-core/nodes/configuration_guide.md) - Node setup
- [State Schema Guide](../haive-core/schemas/state_schema_guide.md) - State management

## 💡 **Quick Reference**

### Create Field Mapping
```python
from haive.core.graph.node.engine_node import EngineNodeConfig

# Simple mapping
node = EngineNodeConfig(
    engine=my_engine,
    output_fields={"result": "potato"}
)

# Multiple mappings
node = EngineNodeConfig(
    engine=my_engine,
    input_fields={"user_query": "query"},
    output_fields={"result": "answer", "confidence": "score"}
)
```

### Use in Multi-Agent
```python
class MappedMultiAgent(EnhancedMultiAgent):
    def build_graph(self):
        graph = super().build_graph()
        
        # Apply mapping to specific agent
        mapped_node = EngineNodeConfig(
            name="agent1",
            agent=self.agents["agent1"],
            output_fields={"result": "potato"}
        )
        
        graph.add_node("agent1", mapped_node)
        return graph
```

---

**Field mapping is available now!** Use `output_fields={"result": "potato"}` in EngineNodeConfig to start mapping fields immediately.