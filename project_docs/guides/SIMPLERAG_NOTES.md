# SimpleRAG Notes - Key Learnings and Patterns

**Version**: 1.0
**Purpose**: Notes on SimpleRAG implementation patterns and common mistakes
**Last Updated**: 2025-01-20

## 🎯 Core Understanding: SimpleRAG is a Class Inheriting from MultiAgent

**CRITICAL**: SimpleRAG is a **CLASS** that **inherits** from **MultiAgent**.

```python
class SimpleRAG(MultiAgent):
    """SimpleRAG inheriting from MultiAgent with sequential BaseRAGAgent + SimpleAgent."""

    # Configuration fields
    retriever_config: BaseRetrieverConfig | VectorStoreConfig = Field(
        ..., description="Configuration for the retriever agent"
    )
    llm_config: AugLLMConfig = Field(
        ..., description="Configuration for the generator agent"
    )

    @model_validator(mode="before")
    @classmethod
    def create_agents(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Create the retriever and generator agents."""
        if not isinstance(values, dict):
            return values

        # Get configs
        retriever_config = values.get("retriever_config")
        llm_config = values.get("llm_config")

        if retriever_config and llm_config:
            # Create retriever agent
            retriever = BaseRAGAgent(name="retriever", engine=retriever_config)

            # Create generator agent with ChatPromptTemplate and structured output
            generator_config = llm_config.model_copy()
            generator_config.prompt_template = RAG_CHAT_TEMPLATE
            generator_config.structured_output_model = RAGAnswer

            generator = SimpleAgent(name="generator", engine=generator_config)

            # Set agents and execution mode
            values["agents"] = [retriever, generator]
            values["execution_mode"] = "sequential"

        return values
```

## ❌ Common Mistakes Made

### 1. Creating a Function Instead of Class

```python
# ❌ WRONG - Don't create a function
def SimpleRAG(...) -> MultiAgent:
    # Create agents and return MultiAgent

# ✅ CORRECT - Create a class inheriting from MultiAgent
class SimpleRAG(MultiAgent):
    # Proper Pydantic fields and model_validator
```

### 2. Overriding **init** Instead of Using model_validator

```python
# ❌ WRONG - Don't override __init__
class SimpleRAG(MultiAgent):
    def __init__(self, ...):
        # Override __init__ breaks Pydantic validation

# ✅ CORRECT - Use model_validator
class SimpleRAG(MultiAgent):
    @model_validator(mode="before")
    @classmethod
    def create_agents(cls, values): ...
```

### 3. Missing Pydantic Patterns

```python
# ❌ WRONG - Overriding __init__ in Pydantic models
class RAGAnswer(BaseModel):
    def __init__(self, ...):  # Breaks Pydantic validation

# ✅ CORRECT - Use Field validation
class RAGAnswer(BaseModel):
    answer: str = Field(...)
    sources: List[str] = Field(default_factory=list)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
```

## ✅ Key Patterns That Work

### 1. MultiAgent Creation from List

The MultiAgent class accepts a list of agents in the constructor:

```python
# From MultiAgent clean.py - normalize_agents_and_name validator
agents = [agent1, agent2, agent3]
multi_agent = MultiAgent(agents=agents)

# This gets normalized to:
# {
#   "agent1_name": agent1,
#   "agent2_name": agent2,
#   "agent3_name": agent3
# }
```

### 2. ChatPromptTemplate Usage

```python
from langchain_core.prompts import ChatPromptTemplate

RAG_CHAT_TEMPLATE = ChatPromptTemplate.from_messages([
    ("system", "System instructions..."),
    ("human", "Context:\n{context}\n\nQuestion: {query}\n\nPlease provide...")
])

# Use in agent config
generator_config.prompt_template = RAG_CHAT_TEMPLATE
```

### 3. Structured Output Models

```python
class RAGAnswer(BaseModel):
    answer: str = Field(..., description="The main answer")
    sources: List[str] = Field(default_factory=list, description="Source references")
    confidence: float = Field(default=0.5, ge=0.0, le=1.0, description="Confidence score")
    reasoning: str = Field(default="", description="Reasoning process")

# Use in agent config
generator_config.structured_output_model = RAGAnswer
```

## 🏗️ SimpleRAG Architecture

```
SimpleRAG Function
├── Creates BaseRAGAgent (retriever)
├── Creates SimpleAgent (generator)
│   ├── Uses ChatPromptTemplate
│   └── Uses RAGAnswer structured output
└── Returns MultiAgent([retriever, generator], mode="sequential")
```

### Execution Flow

1. **Input**: Query and vector store configuration
2. **BaseRAGAgent**: Retrieves relevant documents
3. **SimpleAgent**: Generates structured answer using retrieved context
4. **Output**: RAGAnswer with answer, sources, confidence, reasoning

## 🔧 Component Structure

### File Organization

```
packages/haive-agents/src/haive/agents/rag/simple/
├── simple_rag.py                    # Main function
├── answer_generator/
│   ├── __init__.py                  # Exports
│   ├── models.py                    # RAGAnswer model
│   └── prompts.py                   # RAG_CHAT_TEMPLATE
└── __init__.py                      # Package exports
```

### Dependencies

```python
from haive.agents.multi.clean import MultiAgent  # Core multi-agent
from haive.agents.rag.base.agent import BaseRAGAgent  # Retriever
from haive.agents.simple.agent import SimpleAgent     # Generator
from haive.core.engine.aug_llm import AugLLMConfig   # LLM config
from langchain_core.prompts import ChatPromptTemplate # Prompts
```

## 📚 Learning from MultiAgent Clean

### Key Insights from clean.py

1. **agents Field**: MultiAgent has `agents: dict[str, Agent]` field
2. **List Normalization**: List of agents gets converted to dict by name
3. **Execution Modes**: "sequential", "parallel", "conditional", "infer"
4. **State Management**: Uses MultiAgentState by default
5. **Simple Creation**: `MultiAgent(agents=[...])` just works

### MultiAgent Constructor Pattern

```python
# From normalize_agents_and_name validator:
if isinstance(agents, list):
    # Convert list to dict using agent names
    agent_dict = {}
    for i, agent in enumerate(agents):
        if hasattr(agent, "name") and agent.name:
            agent_dict[agent.name] = agent
        else:
            agent_dict[f"agent_{i}"] = agent
    values["agents"] = agent_dict
```

## 🚨 Things That Confused Me

### 1. Class vs Function Confusion

- **Thought**: SimpleRAG should be a class like other agents
- **Reality**: SimpleRAG is just a factory function that creates MultiAgent

### 2. Inheritance Confusion

- **Thought**: Should extend MultiAgent with custom logic
- **Reality**: MultiAgent already handles everything, just pass agents list

### 3. Pydantic Override Confusion

- **Thought**: Need to override **init** for custom behavior
- **Reality**: Use Field validation and model_validator, never override **init**

### 4. Complex Architecture Confusion

- **Thought**: Need sophisticated state management and routing
- **Reality**: Sequential execution is just `MultiAgent(agents=[a, b], mode="sequential")`

## ✅ Final Working Pattern

```python
class SimpleRAG(MultiAgent):
    """SimpleRAG inheriting from MultiAgent with sequential BaseRAGAgent + SimpleAgent.

    This creates a sequential workflow:
    1. BaseRAGAgent retrieves relevant documents
    2. SimpleAgent generates structured answer from context
    """

    # Configuration fields
    retriever_config: BaseRetrieverConfig | VectorStoreConfig = Field(
        ..., description="Configuration for document retrieval"
    )
    llm_config: AugLLMConfig = Field(
        ..., description="Configuration for answer generation"
    )

    @model_validator(mode="before")
    @classmethod
    def create_agents(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Create the retriever and generator agents automatically."""
        if not isinstance(values, dict):
            return values

        # Get configs
        retriever_config = values.get("retriever_config")
        llm_config = values.get("llm_config")

        if retriever_config and llm_config:
            # Create retriever agent
            retriever = BaseRAGAgent(name="retriever", engine=retriever_config)

            # Create generator with prompt template and structured output
            generator_config = llm_config.model_copy()
            generator_config.prompt_template = RAG_CHAT_TEMPLATE
            generator_config.structured_output_model = RAGAnswer

            generator = SimpleAgent(name="generator", engine=generator_config)

            # Set agents and execution mode for MultiAgent
            values["agents"] = [retriever, generator]
            values["execution_mode"] = "sequential"

        return values

# Usage:
simple_rag = SimpleRAG(
    retriever_config=my_retriever_config,
    llm_config=my_llm_config
)
```

## 🎯 Key Takeaways

1. **Inheritance over Composition**: SimpleRAG inherits from MultiAgent, don't create functions
2. **Read the Code**: Always read clean implementations first
3. **Class with Proper Patterns**: Use Pydantic fields and model_validator, not **init**
4. **Use Existing Patterns**: MultiAgent already handles multi-agent workflows
5. **Pydantic Best Practices**: Field validation, model_validator, no **init** overrides
6. **ChatPromptTemplate**: Proper way to format prompts with variables
7. **Structured Output**: Essential for agent communication and type safety

## 🔗 Related Files

- `/packages/haive-agents/src/haive/agents/multi/clean.py` - MultiAgent implementation
- `/packages/haive-agents/src/haive/agents/rag/simple/simple_rag.py` - Final implementation
- `/project_docs/guides/agent/multi/` - Multi-agent documentation
- `/project_docs/guides/agent/chat_prompt_template_examples.md` - Prompt examples

---

**Remember**: SimpleRAG is a **CLASS** that **inherits** from MultiAgent. Use proper Pydantic patterns with Field validation and model_validator, never override **init**!
