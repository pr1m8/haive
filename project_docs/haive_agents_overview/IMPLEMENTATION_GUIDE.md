# Agent Implementation Guide

## Overview

This guide provides step-by-step instructions for implementing new agents in the haive-agents package, including best practices and common patterns.

## Quick Start: Creating a New Agent

### 1. Basic Agent Template

```python
from typing import Any, Dict
from pydantic import BaseModel, Field
from haive.agents.base.agent import Agent
from haive.core.engine.agent.agent import register_agent
from haive.core.graph.GraphBuilder import DynamicGraph
from langgraph.graph import END, START
from langgraph.types import Command

# Define State Schema
class MyAgentState(BaseModel):
    """State schema for MyAgent"""
    input_data: str
    processed_data: str = ""
    result: Any = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

# Define Config Schema
class MyAgentConfig(BaseModel):
    """Configuration for MyAgent"""
    model_name: str = "gpt-4"
    temperature: float = 0.7
    max_retries: int = 3

# Register and Implement Agent
@register_agent(MyAgentConfig)
class MyAgent(Agent[MyAgentConfig]):
    """Custom agent implementation"""
    
    def __init__(self, config: MyAgentConfig, name: str = "MyAgent"):
        super().__init__(config=config, name=name)
        self.state_schema = MyAgentState
    
    def process_data(self, state: MyAgentState) -> Command:
        """Process the input data"""
        # Your processing logic here
        processed = f"Processed: {state.input_data}"
        return Command(update={"processed_data": processed})
    
    def generate_result(self, state: MyAgentState) -> Command:
        """Generate final result"""
        # Your generation logic here
        result = {"status": "success", "data": state.processed_data}
        return Command(update={"result": result})
    
    def setup_workflow(self):
        """Define the agent workflow"""
        gb = DynamicGraph(state_schema=self.state_schema)
        
        # Add nodes
        gb.add_node("process", self.process_data)
        gb.add_node("generate", self.generate_result)
        
        # Add edges
        gb.add_edge(START, "process")
        gb.add_edge("process", "generate")
        gb.add_edge("generate", END)
        
        # Build graph
        self.graph = gb.build()
```

### 2. Using the Agent

```python
# Create agent instance
config = MyAgentConfig(model_name="gpt-4", temperature=0.5)
agent = MyAgent(config=config, name="Data Processor")

# Invoke agent
result = agent.invoke({"input_data": "Hello, World!"})
print(result)
```

## Advanced Patterns

### 1. Sequential Agent Implementation

```python
from haive.agents.multi.base import SequentialAgent

class MySequentialAgent(SequentialAgent):
    """Agent that executes sub-agents in sequence"""
    
    @classmethod
    def create_pipeline(cls, config: Dict[str, Any]):
        # Create sub-agents
        agent1 = ProcessingAgent(config["processor_config"])
        agent2 = AnalysisAgent(config["analyzer_config"])
        agent3 = ReportAgent(config["reporter_config"])
        
        # Return sequential agent
        return cls(
            agents=[agent1, agent2, agent3],
            name="Analysis Pipeline"
        )
```

### 2. Conditional Agent Implementation

```python
from haive.agents.multi.base import ConditionalAgent

class MyConditionalAgent(ConditionalAgent):
    """Agent with conditional routing"""
    
    def route_decision(self, state):
        """Determine which path to take"""
        if state.query_type == "simple":
            return "simple_path"
        elif state.query_type == "complex":
            return "complex_path"
        else:
            return "default_path"
    
    def setup_workflow(self):
        gb = DynamicGraph(state_schema=self.state_schema)
        
        # Add router node
        gb.add_node("router", self.route_decision)
        
        # Add path nodes
        gb.add_node("simple_handler", self.handle_simple)
        gb.add_node("complex_handler", self.handle_complex)
        gb.add_node("default_handler", self.handle_default)
        
        # Add conditional edges
        gb.add_edge(START, "router")
        gb.add_conditional_edges(
            "router",
            self.route_decision,
            {
                "simple_path": "simple_handler",
                "complex_path": "complex_handler",
                "default_path": "default_handler"
            }
        )
        
        # Connect to end
        gb.add_edge("simple_handler", END)
        gb.add_edge("complex_handler", END)
        gb.add_edge("default_handler", END)
        
        self.graph = gb.build()
```

### 3. RAG Agent Implementation

```python
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.rag.base.config import BaseRAGConfig

class MyCustomRAGAgent(BaseRAGAgent):
    """Custom RAG implementation"""
    
    def retrieve(self, state):
        """Custom retrieval logic"""
        # Add pre-processing
        processed_query = self.preprocess_query(state.query)
        
        # Call parent retrieve
        documents = super().retrieve(state)
        
        # Add post-processing
        filtered_docs = self.filter_documents(documents)
        
        return Command(update={"retrieved_documents": filtered_docs})
    
    def generate_answer(self, state):
        """Custom answer generation"""
        # Add custom prompt
        custom_prompt = self.build_custom_prompt(state)
        
        # Generate answer
        answer = self.llm.invoke(custom_prompt)
        
        # Add metadata
        metadata = self.extract_metadata(answer)
        
        return Command(update={
            "answer": answer,
            "metadata": metadata
        })
```

## Engine Integration

### 1. LLM Engine Integration

```python
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig

class LLMAgent(Agent):
    def __init__(self, config):
        super().__init__(config)
        
        # Configure LLM
        self.llm_config = AugLLMConfig(
            llm_config=AzureLLMConfig(
                deployment_name="gpt-4",
                temperature=0.7
            ),
            prompt_template=self.get_prompt_template()
        )
        
        # Create engine
        self.llm_engine = self.llm_config.create_engine()
```

### 2. Document Engine Integration

```python
from haive.core.engine.document import DocumentEngine, DocumentEngineConfig

class DocumentProcessorAgent(Agent):
    def __init__(self, config):
        super().__init__(config)
        
        # Configure document engine
        self.doc_config = DocumentEngineConfig(
            chunking_strategy="semantic",
            chunk_size=1000,
            chunk_overlap=200
        )
        
        # Create engine
        self.doc_engine = DocumentEngine(self.doc_config)
```

### 3. Retriever Engine Integration

```python
from haive.core.engine.retriever import RetrieverEngineConfig

class RetrieverAgent(Agent):
    def __init__(self, config):
        super().__init__(config)
        
        # Configure retriever
        self.retriever_config = RetrieverEngineConfig(
            vector_store_type="faiss",
            embedding_model="text-embedding-ada-002",
            top_k=10
        )
        
        # Create retriever
        self.retriever = self.retriever_config.create_retriever()
```

## State Management Best Practices

### 1. State Schema Design

```python
class WellDesignedState(BaseModel):
    """Example of well-designed state"""
    
    # Required fields with clear types
    query: str
    user_id: str
    
    # Optional fields with defaults
    context: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    # Computed fields
    processed: bool = False
    timestamp: float = Field(default_factory=time.time)
    
    # Validation
    @field_validator('query')
    def validate_query(cls, v):
        if not v.strip():
            raise ValueError("Query cannot be empty")
        return v.strip()
```

### 2. State Updates

```python
def update_state_safely(self, state):
    """Safe state update pattern"""
    try:
        # Perform operation
        result = self.process_data(state.data)
        
        # Update state
        return Command(update={
            "result": result,
            "processed": True,
            "error": None
        })
    except Exception as e:
        # Handle error
        return Command(update={
            "error": str(e),
            "processed": False
        })
```

## Error Handling

### 1. Retry Logic

```python
def with_retry(self, func, state, max_retries=3):
    """Retry pattern for operations"""
    for attempt in range(max_retries):
        try:
            return func(state)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            self.logger.warning(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2 ** attempt)  # Exponential backoff
```

### 2. Graceful Degradation

```python
def retrieve_with_fallback(self, state):
    """Fallback pattern for retrieval"""
    try:
        # Try primary retrieval
        docs = self.primary_retriever.invoke(state.query)
        if docs:
            return Command(update={"documents": docs})
    except Exception as e:
        self.logger.error(f"Primary retrieval failed: {e}")
    
    try:
        # Fallback to secondary
        docs = self.secondary_retriever.invoke(state.query)
        return Command(update={"documents": docs})
    except Exception as e:
        self.logger.error(f"Secondary retrieval failed: {e}")
        
    # Final fallback
    return Command(update={
        "documents": [],
        "error": "All retrieval methods failed"
    })
```

## Testing Your Agent

### 1. Unit Test Template

```python
import pytest
from your_module import MyAgent, MyAgentConfig

class TestMyAgent:
    @pytest.fixture
    def agent(self):
        config = MyAgentConfig(temperature=0.5)
        return MyAgent(config)
    
    def test_process_data(self, agent):
        # Create test state
        state = agent.state_schema(input_data="test")
        
        # Call method
        result = agent.process_data(state)
        
        # Assert
        assert result.update["processed_data"] == "Processed: test"
    
    def test_full_workflow(self, agent):
        # Test complete workflow
        result = agent.invoke({"input_data": "test"})
        
        assert result["result"]["status"] == "success"
        assert "data" in result["result"]
```

### 2. Integration Test Template

```python
@pytest.mark.integration
class TestMyAgentIntegration:
    def test_with_real_llm(self):
        # Use real configurations
        config = MyAgentConfig(
            model_name="gpt-3.5-turbo",
            temperature=0.7
        )
        agent = MyAgent(config)
        
        # Test with real data
        result = agent.invoke({
            "input_data": "Analyze this text..."
        })
        
        assert result["result"] is not None
```

## Performance Optimization

### 1. Parallel Processing

```python
from concurrent.futures import ThreadPoolExecutor

def process_batch(self, items):
    """Process items in parallel"""
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(self.process_item, item)
            for item in items
        ]
        
        results = []
        for future in futures:
            try:
                results.append(future.result())
            except Exception as e:
                self.logger.error(f"Processing failed: {e}")
                results.append(None)
    
    return results
```

### 2. Caching

```python
from functools import lru_cache

class CachedAgent(Agent):
    @lru_cache(maxsize=100)
    def expensive_operation(self, query: str):
        """Cache expensive operations"""
        return self.llm.invoke(query)
```

## Deployment Considerations

### 1. Configuration Management

```python
class ProductionConfig(BaseModel):
    """Production-ready configuration"""
    
    # Environment-based settings
    api_key: str = Field(default_factory=lambda: os.getenv("API_KEY"))
    endpoint: str = Field(default_factory=lambda: os.getenv("ENDPOINT"))
    
    # Resource limits
    max_concurrent_requests: int = 10
    timeout_seconds: int = 30
    
    # Feature flags
    enable_caching: bool = True
    enable_retry: bool = True
```

### 2. Logging and Monitoring

```python
import logging
from datetime import datetime

class MonitoredAgent(Agent):
    def __init__(self, config):
        super().__init__(config)
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def invoke(self, inputs):
        """Invoke with monitoring"""
        start_time = datetime.now()
        request_id = str(uuid.uuid4())
        
        self.logger.info(f"Request {request_id} started")
        
        try:
            result = super().invoke(inputs)
            duration = (datetime.now() - start_time).total_seconds()
            
            self.logger.info(
                f"Request {request_id} completed in {duration}s"
            )
            
            return result
        except Exception as e:
            self.logger.error(
                f"Request {request_id} failed: {e}",
                exc_info=True
            )
            raise
```

## Common Pitfalls and Solutions

### 1. State Mutation
**Problem**: Directly modifying state objects
**Solution**: Always return new state via Command

### 2. Missing Error Handling
**Problem**: Unhandled exceptions crash workflow
**Solution**: Wrap operations in try-except blocks

### 3. Memory Leaks
**Problem**: Accumulating data in agent instance
**Solution**: Store data in state, not instance

### 4. Blocking Operations
**Problem**: Synchronous operations block execution
**Solution**: Use async operations or thread pools

### 5. Hard-coded Values
**Problem**: Configuration mixed with logic
**Solution**: Use config classes and environment variables