# Agent Configuration Guide - Haive Framework

**Version**: 1.0  
**Purpose**: Comprehensive guide for properly configuring agents and engines  
**Last Updated**: 2025-01-09

## 🚨 CRITICAL: Always Use `poetry run`

**ALL commands must use `poetry run` prefix:**

```bash
# CORRECT
poetry run python your_script.py
poetry run pytest packages/haive-agents/tests/ -v

# WRONG
python your_script.py
pytest packages/haive-agents/tests/ -v
```

## 🚨 CRITICAL: Research First, Configure Second

### Before Creating ANY Agent Configuration

```bash
# 1. Check existing agent examples
find packages/haive-agents/examples/ -name "*.py" | head -5

# 2. Look at existing agent implementations
find packages/haive-agents/src/ -name "agent.py" | head -5

# 3. Check engine configuration patterns
find packages/haive-core/src/ -name "*config*.py" | head -5

# 4. Look at test files for usage patterns
find packages/haive-agents/tests/ -name "test_*.py" | head -5

# 5. Test imports work with poetry run
poetry run python -c "from haive.agents.simple import SimpleAgent; print('✅ Import works')"
```

## 📋 Agent Types Overview

### Available Agent Types

1. **SimpleAgent** - Basic conversational agent with optional structured output
2. **ReactAgent** - Reasoning and acting agent with looping behavior
3. **BaseRAGAgent** - Retrieval-augmented generation agent
4. **MultiAgent** - Coordination of multiple agents

### Engine Types

1. **AugLLMConfig** - Primary engine for LLM interactions with tools
2. **VectorStoreConfig** - Vector store engine for RAG agents
3. **VectorStoreRetrieverConfig** - Retriever engine for RAG agents

## 🔧 AugLLMConfig - Primary Engine Configuration

### Research Existing Patterns First

```bash
# Check existing AugLLMConfig usage
grep -r "AugLLMConfig" packages/haive-agents/examples/ | head -5
grep -r "AugLLMConfig" packages/haive-agents/tests/ | head -5
```

### Basic AugLLMConfig Usage

```python
from haive.core.engine.aug_llm import AugLLMConfig

# ✅ CORRECT - Basic configuration
engine = AugLLMConfig()

# ✅ CORRECT - With common parameters
engine = AugLLMConfig(
    name="demo_llm",
    system_message="You are a helpful assistant.",
    temperature=0.7,
    model="gpt-4"
)

# ✅ CORRECT - With tools
from haive.core.tools import tool

@tool
def calculate(expression: str) -> float:
    """Calculate mathematical expression."""
    return eval(expression)

engine = AugLLMConfig(
    tools=[calculate],
    name="calculator_engine"
)
```

### Structured Output Configuration

```python
from pydantic import BaseModel, Field

class ProductAnalysis(BaseModel):
    """Product analysis result."""
    product_name: str = Field(description="Name of the product")
    rating: float = Field(description="Rating from 1-10")
    summary: str = Field(description="Brief summary")

# ✅ CORRECT - Structured output (v2 recommended)
engine = AugLLMConfig(
    structured_output_model=ProductAnalysis,
    structured_output_version="v2"  # Use v2 for better tool integration
)

# ❌ WRONG - Using v1 for new implementations
engine = AugLLMConfig(
    structured_output_model=ProductAnalysis,
    structured_output_version="v1"  # Deprecated
)
```

## 🤖 SimpleAgent Configuration

### Research Existing Patterns

```bash
# Check SimpleAgent usage patterns
find packages/haive-agents/ -name "*.py" | xargs grep -l "SimpleAgent" | head -5
```

### Basic SimpleAgent Setup

```python
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

# ✅ CORRECT - Basic agent
agent = SimpleAgent(
    name="simple_agent",
    engine=AugLLMConfig()
)

# ✅ CORRECT - Agent with structured output
agent = SimpleAgent(
    name="analyzer",
    engine=AugLLMConfig(),
    structured_output_model=ProductAnalysis
)

# ✅ CORRECT - Agent with tools
agent = SimpleAgent(
    name="tool_agent",
    engine=AugLLMConfig(),
    tools=[calculator_tool]
)
```

### SimpleAgent Convenience Fields

```python
# ✅ CORRECT - Using convenience fields
agent = SimpleAgent(
    name="configured_agent",
    engine=AugLLMConfig(),
    temperature=0.7,           # Convenience field
    model_name="gpt-4",        # Convenience field
    system_message="You are a helpful assistant"  # Convenience field
)

# ❌ WRONG - Configuring in engine AND agent
agent = SimpleAgent(
    name="bad_agent",
    engine=AugLLMConfig(temperature=0.5),  # ❌ Don't do this
    temperature=0.7,                       # ❌ And this
)
```

### SimpleAgent Factory Methods

```python
# ✅ CORRECT - Factory method patterns
agent = SimpleAgent.from_engine(
    engine=aug_llm_config,
    name="my_agent"
)

agent = SimpleAgent.create_with_tools(
    tools=[tool1, tool2],
    name="tool_agent"
)
```

## 🔄 ReactAgent Configuration

### Research Existing Patterns

```bash
# Check ReactAgent usage patterns
find packages/haive-agents/ -name "*.py" | xargs grep -l "ReactAgent" | head -5
```

### Basic ReactAgent Setup

```python
from haive.agents.react.agent import ReactAgent
from haive.core.engine.aug_llm import AugLLMConfig

# ✅ CORRECT - Basic ReactAgent
react_agent = ReactAgent(
    name="react_agent",
    engine=AugLLMConfig(tools=[calculator_tool])
)

# ✅ CORRECT - ReactAgent with configuration
react_agent = ReactAgent(
    name="reasoning_agent",
    engine=AugLLMConfig(),
    tools=[search_tool, calculator_tool],
    max_iterations=10,
    temperature=0.7
)
```

### ReactAgent Key Features

```python
# ReactAgent inherits ALL SimpleAgent patterns
# - Convenience fields
# - Factory methods
# - Structured output support
# - Tool integration

# ✅ CORRECT - ReactAgent with structured output
class ReasoningResult(BaseModel):
    reasoning: str = Field(description="Step-by-step reasoning")
    conclusion: str = Field(description="Final conclusion")

react_agent = ReactAgent(
    name="reasoning_agent",
    engine=AugLLMConfig(
        structured_output_model=ReasoningResult,
        structured_output_version="v2"
    )
)
```

## 📚 BaseRAGAgent Configuration

### Research Existing Patterns

```bash
# Check BaseRAGAgent usage patterns
find packages/haive-agents/ -name "*.py" | xargs grep -l "BaseRAGAgent" | head -5
find packages/haive-agents/ -name "*.py" | xargs grep -l "VectorStoreConfig" | head -5
```

### Basic BaseRAGAgent Setup

```python
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.core.engine.vectorstore import VectorStoreConfig
from haive.core.engine.retriever import VectorStoreRetrieverConfig

# ✅ CORRECT - From vector store config
rag_agent = BaseRAGAgent(
    name="rag_agent",
    engine=vector_store_config
)

# ✅ CORRECT - From retriever config
rag_agent = BaseRAGAgent(
    name="rag_agent",
    engine=retriever_config
)
```

### BaseRAGAgent Factory Methods

```python
# ✅ CORRECT - Factory methods
rag_agent = BaseRAGAgent.from_documents(
    documents=[doc1, doc2],
    embedding_model=embedding_config,
    name="my_rag_agent"
)

rag_agent = BaseRAGAgent.from_vectorstore(
    vector_store_config=vs_config,
    name="my_rag_agent"
)
```

### Vector Store Configuration

```python
from haive.core.engine.vectorstore import VectorStoreConfig

# ✅ CORRECT - Basic vector store
vector_store_config = VectorStoreConfig(
    name="my_vectorstore",
    embedding_model=embedding_config,
    documents=documents
)

# ✅ CORRECT - With retriever settings
retriever_config = VectorStoreRetrieverConfig(
    name="my_retriever",
    vector_store_config=vector_store_config,
    search_type="similarity",
    search_kwargs={"k": 5}
)
```

## 🎯 MultiAgent Configuration

### Research Existing Patterns

```bash
# Check MultiAgent usage patterns
find packages/haive-agents/ -name "*.py" | xargs grep -l "MultiAgent" | head -5
```

### MultiAgent Factory Method

```python
from haive.agents.multi.agent import MultiAgent
from haive.core.tools import tool

@tool
def add_tool(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

# ✅ CORRECT - Factory method with structured agents
agent_configs = [
    {
        "type": "simple",
        "name": "Planner",
        "structured_output_model": Plan,
        "structured_output_version": "v2",
    },
    {
        "type": "react",
        "name": "Calculator",
        "tools": [add_tool]
    },
]

multi_agent = MultiAgent.with_structured_agents(
    agent_configs=agent_configs,
    name="Planning and Calculation System"
)
```

## 🔧 Common Configuration Patterns

### Tool Integration Pattern

```python
from haive.core.tools import tool

@tool
def my_tool(query: str) -> str:
    """Tool description."""
    return f"Result for {query}"

# ✅ CORRECT - Add tools to engine
agent = SimpleAgent(
    name="tool_agent",
    engine=AugLLMConfig(tools=[my_tool])
)

# ✅ CORRECT - Add tools to agent (convenience)
agent = SimpleAgent(
    name="tool_agent",
    engine=AugLLMConfig(),
    tools=[my_tool]
)
```

### System Message Pattern

```python
# ✅ CORRECT - System message in engine
agent = SimpleAgent(
    name="specialized_agent",
    engine=AugLLMConfig(
        system_message="You are a specialized assistant for X task.",
        temperature=0.3,
        model="gpt-4"
    )
)

# ✅ CORRECT - System message as convenience field
agent = SimpleAgent(
    name="specialized_agent",
    engine=AugLLMConfig(),
    system_message="You are a specialized assistant for X task."
)
```

## 🚨 Common Mistakes to Avoid

### 1. Not Researching Existing Patterns

```python
# ❌ WRONG - Not checking existing examples
agent = SimpleAgent(
    name="my_agent",
    engine=CustomEngine()  # Reinventing the wheel
)

# ✅ CORRECT - Use existing patterns
agent = SimpleAgent(
    name="my_agent",
    engine=AugLLMConfig()  # Standard pattern
)
```

### 2. Incorrect Engine Type for Agent

```python
# ❌ WRONG - Using wrong engine type
rag_agent = BaseRAGAgent(
    name="rag_agent",
    engine=AugLLMConfig()  # Wrong engine type
)

# ✅ CORRECT - Use correct engine type
rag_agent = BaseRAGAgent(
    name="rag_agent",
    engine=VectorStoreConfig()  # Correct engine type
)
```

### 3. Double Configuration

```python
# ❌ WRONG - Configuring same field in multiple places
agent = SimpleAgent(
    name="agent",
    engine=AugLLMConfig(temperature=0.5),  # ❌ Here
    temperature=0.7,                       # ❌ And here
)

# ✅ CORRECT - Configure in one place
agent = SimpleAgent(
    name="agent",
    engine=AugLLMConfig(),
    temperature=0.7  # Use convenience field
)
```

### 4. Missing Engine Registration

```python
# ❌ WRONG - Manual engine registration
from haive.core.engine.base import EngineRegistry
registry = EngineRegistry.get_instance()
registry.register(engine)  # Don't do this manually

# ✅ CORRECT - Automatic registration
agent = SimpleAgent(
    name="agent",
    engine=AugLLMConfig()
)
# Engine is automatically registered
```

## 📋 Complete Configuration Examples

### Simple Conversational Agent

```python
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

agent = SimpleAgent(
    name="chat_agent",
    engine=AugLLMConfig(
        system_message="You are a helpful assistant.",
        temperature=0.7,
        model="gpt-4"
    )
)

# Usage
result = await agent.arun("Hello, how are you?")
```

### Tool-Enhanced Agent

```python
from haive.core.tools import tool

@tool
def get_weather(location: str) -> str:
    """Get weather for a location."""
    return f"Weather in {location}: Sunny, 75°F"

agent = SimpleAgent(
    name="weather_agent",
    engine=AugLLMConfig(
        tools=[get_weather],
        system_message="You are a weather assistant."
    )
)
```

### Structured Output Agent

```python
from pydantic import BaseModel, Field

class Analysis(BaseModel):
    sentiment: str = Field(description="Sentiment (positive/negative/neutral)")
    confidence: float = Field(description="Confidence score 0-1")
    summary: str = Field(description="Brief summary")

agent = SimpleAgent(
    name="analyzer",
    engine=AugLLMConfig(
        structured_output_model=Analysis,
        structured_output_version="v2"
    )
)
```

### RAG Agent with Documents

```python
from haive.agents.rag.base.agent import BaseRAGAgent

documents = [
    "Document content 1...",
    "Document content 2...",
]

rag_agent = BaseRAGAgent.from_documents(
    documents=documents,
    embedding_model=embedding_config,
    name="knowledge_agent"
)
```

## 🔍 Research Commands for Each Agent Type

### SimpleAgent Research

```bash
# Check existing SimpleAgent examples
find packages/haive-agents/examples/ -name "*.py" | xargs grep -l "SimpleAgent"

# Look at test patterns
find packages/haive-agents/tests/ -name "test_simple*"

# Check configuration patterns
grep -r "SimpleAgent(" packages/haive-agents/examples/ | head -5
```

### ReactAgent Research

```bash
# Check existing ReactAgent examples
find packages/haive-agents/examples/ -name "*.py" | xargs grep -l "ReactAgent"

# Look at test patterns
find packages/haive-agents/tests/ -name "test_react*"

# Check configuration patterns
grep -r "ReactAgent(" packages/haive-agents/examples/ | head -5
```

### BaseRAGAgent Research

```bash
# Check existing BaseRAGAgent examples
find packages/haive-agents/examples/ -name "*.py" | xargs grep -l "BaseRAGAgent"

# Look at test patterns
find packages/haive-agents/tests/ -name "test_*rag*"

# Check VectorStore patterns
grep -r "VectorStoreConfig" packages/haive-agents/examples/ | head -5
```

## 🛠️ Testing Your Configuration

### Basic Agent Test

```python
import asyncio
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

async def test_agent():
    agent = SimpleAgent(
        name="test_agent",
        engine=AugLLMConfig()
    )

    result = await agent.arun("Hello!")
    print(f"Result: {result}")

    # Test structured output
    if hasattr(agent, 'structured_output_model'):
        print(f"Structured output: {result}")

# Run test with poetry run
# poetry run python test_agent.py
asyncio.run(test_agent())
```

### Running Agent Tests

```bash
# ALWAYS use poetry run for testing
poetry run python your_agent_test.py

# Run existing tests
poetry run pytest packages/haive-agents/tests/ -v

# Test specific agent type
poetry run pytest packages/haive-agents/tests/test_simple.py -v

# Test imports work
poetry run python -c "from haive.agents.simple import SimpleAgent; print('✅ Import works')"
```

### Configuration Validation

```python
def validate_agent_config(agent):
    """Validate agent configuration."""
    assert agent.name is not None, "Agent must have a name"
    assert agent.engine is not None, "Agent must have an engine"

    # Check engine registration
    from haive.core.engine.base import EngineRegistry
    registry = EngineRegistry.get_instance()
    assert registry.find(agent.engine.name), "Engine should be registered"

    print("✅ Configuration valid!")
```

---

**Remember**: ALWAYS research existing patterns before creating new agent configurations. The examples/ and tests/ directories are your best resources for understanding proper usage patterns!
