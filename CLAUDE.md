# CLAUDE.md - Haive Agent Framework

**Purpose**: Central memory hub for Haive development
**Version**: 4.0
**Last Updated**: 2025-01-15

## 🎯 Project Context

- **Directory**: `/home/will/Projects/haive/backend/haive`
- **Branch**: `feature/fix_everything`
- **Structure**: Monorepo with Git submodules (7 packages)
- **Core Rules**:
  - Always use `poetry run` prefix for ALL Python commands
  - Real components only - NO MOCKS EVER in tests
  - Always use explicit imports: `from haive.core.*`
  - Be EXTREMELY careful with submodules - each is its own repo

## 📚 Essential Documentation

### 🧠 Memory Index System

- **@memory_index/README.md** - Central memory index for all discoveries
- **@memory_index/quick_reference.md** - Most-used patterns and fixes
- **@memory_index/by_date/** - Chronological memory tracking
- **@project_docs/README.md** - Main project documentation hub

### Standards & Guides (Import for details)

- @project_docs/active/standards/coding/COMMAND_EXECUTION_GUIDE.md
- @project_docs/active/standards/coding/PYDANTIC_PATTERNS.md
- @project_docs/active/standards/testing/philosophy.md
- @project_docs/active/standards/git/workflow.md
- @project_docs/guides/TOOL_ROUTING_REFACTOR.md - **NEW** Routing changes for structured output

### Architecture & Patterns

- @project_docs/active/architecture/multi_agent_meta_agent_memory_hub.md
- @project_docs/active/architecture/meta_state_pattern.md
- @project_docs/active/architecture/agent_as_tool_pattern.md
- **Generalized Hook System** - Enhanced base agent with pre/post processing hooks

## 🚀 Current Focus

- **Active Work**: MultiAgent Sequential Pattern (ReactAgent → SimpleAgent)
- **Issues**: @project_docs/sessions/active/current_issues.md
- **Recent Achievements**: See @memory_index/by_date/2025-01-23/

## 🎯 Recent Completed Work (2025-01-29)

### BaseModel Tool Routing & Mixin Fixes ✅ **COMPLETED**

**Problem Solved**: Comprehensive fix for BaseModel tool routing and mixin integration issues.

**Key Fixes**:

- **StructuredOutputMixin**: Fixed to use `"parse_output"` route instead of deprecated `"structured_output"`
- **AugLLMConfig add_tool()**: Fixed to always sync routes, resolving `with_structured_output()` not setting routes
- **ValidationNodeV2**: Enhanced to handle all three BaseModel routes properly
- **Tool Routing System**: Complete validation of routing patterns

**Routes Now Working**:

- `structured_output_model` → `"parse_output"` route
- BaseModel without `__call__` → `"pydantic_model"` route (error case)
- BaseModel with `__call__` → `"pydantic_tool"` route (executable tool)
- BaseModel instances → `"function"` route

**Testing**: All BaseModel patterns validated with real components, no mocks used.

**Documentation**: Updated `@project_docs/guides/TOOL_ROUTING_REFACTOR.md` with complete details.

## 🔥 Git Safety Protocol (CRITICAL)

### Essential Safety Commands

```bash
# BEFORE ANY WORK
git status && git diff

# BEFORE COMMITTING
git diff --cached && trunk check --all && poetry run pytest
git add specific_file.py && git commit -m "feat: clear description"

# SUBMODULE SAFETY
cd packages/haive-{package} && git status && git branch -vv
git branch backup-$(date +%Y%m%d-%H%M%S)  # Create backup

# RECOVERY
git reflog  # Find lost commits
git branch recovery-branch HEAD@{n}
```

**Key Rules**: Never force push submodules, always create backups, check status before work.

## 🛠️ Most Used Commands

```bash
# Development (ALWAYS with poetry run)
poetry run python script.py
poetry run pytest packages/haive-agents/tests/ -v
poetry run python -c "from haive.core import *; print('Imports OK')"

# Quality Checks
trunk check --all
trunk check --fix --all
poetry run mypy packages/
poetry run ruff check

# Research Before Coding
find packages/ -name "*.py" | xargs grep -l "YourPattern" | head -5
```

## 📦 Project Structure - Namespaced Polyrepo

This is a **namespaced polyrepo** - multiple repositories managed as submodules:

```
packages/                          # Each package is its own Git repository!
├── haive-core/     # github.com/pr1m8/haive-core (foundation)
├── haive-agents/   # github.com/pr1m8/haive-agents (agent implementations)
├── haive-tools/    # github.com/pr1m8/haive-tools (tool implementations)
├── haive-games/    # github.com/pr1m8/haive-games (game environments)
├── haive-mcp/      # github.com/pr1m8/haive-mcp (MCP integration)
├── haive-prebuilt/ # github.com/pr1m8/haive-prebuilt (pre-configured)
└── haive-dataflow/ # github.com/pr1m8/haive-dataflow (data processing)

project_docs/       # Documentation in main repo only
├── active/         # Current standards & architecture
├── sessions/       # Working memory
└── {package}/      # Package-specific docs
```

### ⚠️ Polyrepo Implications:

1. **Each package has its own**:
   - Git history
   - Branches
   - Tags
   - Issues/PRs
   - CI/CD

2. **Working with submodules**:

   ```bash
   # Update all submodules
   git submodule update --init --recursive

   # Work in a submodule
   cd packages/haive-agents
   git checkout -b my-feature
   # Make changes, commit, push
   cd ../..
   git add packages/haive-agents
   git commit -m "Update haive-agents submodule"
   ```

3. **CRITICAL**: Changes in submodules must be:
   - Committed in the submodule first
   - Pushed to the submodule's remote
   - Then referenced in main repo

## 🎯 Critical Development Rules

1. **NO MOCKS EVER**: Test with real LLMs, real tools, real components
2. **Poetry Run Everything**: Never run Python directly
3. **Research First**: Check existing patterns before implementing
4. **Explicit Imports**: `from haive.core.engine import X` not `from engine import X`
5. **Pydantic Patterns**: Never override `__init__`, use Field validation
6. **Git Safety**: Always check diff before commits
7. **Use TodoWrite**: For planning and tracking
8. **System vs Human Messages**: System message in AugLLMConfig, human message in ChatPromptTemplate
9. **Agent Composition**: Use MultiAgent for combining agents, not complex inheritance
10. **Keep It Simple**: One line compositions like `MultiAgent([Agent1, Agent2], mode="sequential")`

## 📝 Quick Code Reference

### Essential Imports

```python
# Core
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.prebuilt.messages_state import MessagesState
from haive.core.schema.prebuilt.meta_state import MetaStateSchema

# Agents - Use V3 versions for enhanced features
from haive.agents.simple.agent_v3 import SimpleAgentV3
from haive.agents.react.agent import ReactAgent
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.rag.simple.answer_agent import AnswerAgent
from haive.agents.multi.enhanced_multi_agent_v4 import EnhancedMultiAgentV4

# Tools
from langchain_core.tools import Tool, tool
from langchain_core.messages import HumanMessage, AIMessage
```

### Agent Configuration Patterns

```python
# AugLLMConfig - System message goes HERE, not in prompt template
config = AugLLMConfig()  # Uses defaults
config = AugLLMConfig(
    temperature=0.7,
    max_tokens=1000,
    system_message="You are a helpful assistant"  # System message in AugLLMConfig
)

# SimpleAgentV3 - Use V3 for enhanced features
from haive.agents.simple.agent_v3 import SimpleAgentV3

agent = SimpleAgentV3(
    name="my_agent",
    engine=config,
    prompt_template=ChatPromptTemplate.from_messages([
        ("system", "System message from AugLLMConfig"),
        ("human", "User message template with {variables}")
    ])
)

# ReactAgent with tools
@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions."""
    return str(eval(expression))

agent = ReactAgent(
    name="react_agent",
    engine=config,
    tools=[calculator]
)

# RAG Pattern - SIMPLE composition
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.rag.simple.answer_agent import AnswerAgent
from haive.agents.multi.enhanced_multi_agent_v4 import EnhancedMultiAgentV4

# Simple RAG = BaseRAGAgent + AnswerAgent in sequence
SimpleRAGAgent = EnhancedMultiAgentV4([BaseRAGAgent, AnswerAgent], mode="sequential")
```

### More Agent Examples

#### 1. Research Assistant Agent

```python
@tool
def web_search(query: str) -> str:
    """Search the web for information."""
    # Implementation here
    return f"Search results for: {query}"

@tool
def document_summarizer(text: str) -> str:
    """Summarize long documents."""
    # Implementation here
    return f"Summary of: {text[:100]}..."

research_agent = ReactAgent(
    name="research_assistant",
    engine=AugLLMConfig(
        temperature=0.3,
        system_message="You are a thorough research assistant. Always cite sources."
    ),
    tools=[web_search, document_summarizer]
)

# Usage
result = research_agent.run("Research the latest developments in AI safety")
```

#### 2. Code Review Agent with Structured Output

```python
class CodeReviewResult(BaseModel):
    """Structured code review output."""
    overall_rating: int = Field(ge=1, le=10, description="Code quality rating")
    issues: List[str] = Field(description="List of issues found")
    suggestions: List[str] = Field(description="Improvement suggestions")
    security_concerns: List[str] = Field(default_factory=list)

code_reviewer = SimpleAgentV3(
    name="code_reviewer",
    engine=AugLLMConfig(
        temperature=0.2,
        structured_output_model=CodeReviewResult,
        system_message="You are an expert code reviewer focusing on quality, security, and best practices."
    ),
    prompt_template=ChatPromptTemplate.from_messages([
        ("system", "Review the following code and provide structured feedback."),
        ("human", "Code to review:\n\n{code}\n\nLanguage: {language}")
    ])
)

# Usage
review = code_reviewer.run({
    "code": "def unsafe_function(user_input): exec(user_input)",
    "language": "Python"
})
```

#### 3. Customer Service Agent

```python
class CustomerResponse(BaseModel):
    """Structured customer service response."""
    response: str = Field(description="Response to customer")
    sentiment: str = Field(description="Customer sentiment: positive/negative/neutral")
    urgency: str = Field(description="Urgency level: low/medium/high")
    follow_up_needed: bool = Field(description="Whether follow-up is required")

@tool
def lookup_order(order_id: str) -> str:
    """Look up customer order information."""
    return f"Order {order_id} details: Status: Shipped, Date: 2025-01-20"

@tool
def check_inventory(product_id: str) -> str:
    """Check product inventory."""
    return f"Product {product_id}: 15 units in stock"

customer_service_agent = ReactAgent(
    name="customer_service",
    engine=AugLLMConfig(
        temperature=0.6,
        structured_output_model=CustomerResponse,
        system_message="You are a helpful customer service representative. Be empathetic and solution-focused."
    ),
    tools=[lookup_order, check_inventory]
)

# Usage
response = customer_service_agent.run("My order #12345 hasn't arrived yet and I'm worried")
```

#### 4. Content Creation Workflow

```python
# Multi-agent content creation pipeline
content_planner = SimpleAgentV3(
    name="content_planner",
    engine=AugLLMConfig(
        temperature=0.7,
        system_message="You create detailed content plans and outlines."
    )
)

content_writer = SimpleAgentV3(
    name="content_writer",
    engine=AugLLMConfig(
        temperature=0.8,
        system_message="You write engaging, high-quality content based on plans."
    )
)

content_editor = SimpleAgentV3(
    name="content_editor",
    engine=AugLLMConfig(
        temperature=0.3,
        system_message="You edit and refine content for clarity and quality."
    )
)

# Compose into workflow
ContentCreationWorkflow = EnhancedMultiAgentV4([
    content_planner,
    content_writer,
    content_editor
], mode="sequential")

# Usage
final_content = ContentCreationWorkflow.run("Create a blog post about AI in healthcare")
```

### Memory Management Patterns

#### 1. Agent with Persistent Memory

```python
from haive.core.memory import ConversationBufferMemory, VectorStoreMemory

# Agent with conversation memory
memory_agent = SimpleAgentV3(
    name="memory_agent",
    engine=AugLLMConfig(temperature=0.7),
    memory=ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        max_token_limit=2000
    )
)

# Usage with memory
result1 = memory_agent.run("My name is Alice and I like Python programming")
result2 = memory_agent.run("What do you remember about me?")  # Will remember Alice + Python
```

#### 2. RAG Agent with Vector Memory

```python
from haive.core.memory.vector_store import ChromaVectorStore

# Create vector store for long-term memory
vector_memory = VectorStoreMemory(
    vector_store=ChromaVectorStore(
        collection_name="agent_memory",
        persist_directory="./memory_data"
    ),
    memory_key="relevant_context",
    input_key="query"
)

# Agent with vector-based memory
smart_agent = SimpleAgentV3(
    name="smart_agent",
    engine=AugLLMConfig(temperature=0.6),
    memory=vector_memory
)

# Usage - agent remembers across sessions
smart_agent.run("I work at TechCorp as a data scientist")
smart_agent.run("My favorite tools are pandas and scikit-learn")
# Later session
result = smart_agent.run("What do you know about my work?")  # Retrieves relevant memories
```

#### 3. Multi-Agent with Shared Memory

```python
from haive.core.memory import SharedMemory

# Shared memory between agents
shared_memory = SharedMemory(
    memory_type="redis",  # or "in_memory", "file"
    connection_params={"host": "localhost", "port": 6379}
)

# Multiple agents sharing memory
researcher = ReactAgent(
    name="researcher",
    engine=AugLLMConfig(),
    tools=[web_search],
    memory=shared_memory
)

writer = SimpleAgentV3(
    name="writer",
    engine=AugLLMConfig(),
    memory=shared_memory
)

# Usage - agents share context
researcher.run("Research AI trends for 2025")
writer.run("Write an article based on the research")  # Access researcher's findings
```

#### 4. Memory with Custom Retrieval

```python
class CustomMemoryRetriever:
    """Custom memory retrieval strategy."""

    def retrieve_relevant_memories(self, query: str, k: int = 5) -> List[str]:
        """Retrieve memories relevant to query."""
        # Custom logic for memory retrieval
        return ["relevant memory 1", "relevant memory 2"]

    def store_memory(self, content: str, metadata: dict = None):
        """Store new memory with metadata."""
        # Custom storage logic
        pass

custom_memory = CustomMemoryRetriever()

# Agent with custom memory strategy
specialized_agent = SimpleAgentV3(
    name="specialized_agent",
    engine=AugLLMConfig(),
    memory=custom_memory
)
```

#### 5. Memory-First Routing Agent

```python
from haive.agents.memory.routing_agent import MemoryRoutingAgent

# Agent that routes based on memory context
routing_agent = MemoryRoutingAgent(
    name="memory_router",
    engine=AugLLMConfig(),
    agents={
        "technical": ReactAgent(name="tech", tools=[code_analyzer]),
        "creative": SimpleAgentV3(name="creative", engine=creative_config),
        "research": ReactAgent(name="research", tools=[web_search])
    },
    routing_strategy="memory_similarity",  # Route based on memory similarity
    memory=vector_memory
)

# Usage - routes to appropriate agent based on memory
routing_agent.run("Fix this Python bug")  # Routes to technical agent
routing_agent.run("Write a poem")        # Routes to creative agent
```

#### 6. Hierarchical Memory System

```python
class HierarchicalMemory:
    """Multi-level memory system."""

    def __init__(self):
        self.short_term = ConversationBufferMemory(max_token_limit=1000)
        self.working_memory = ConversationBufferMemory(max_token_limit=5000)
        self.long_term = VectorStoreMemory(vector_store=ChromaVectorStore())

    def get_context(self, query: str) -> str:
        """Get context from all memory levels."""
        recent = self.short_term.get_relevant_context(query)
        working = self.working_memory.get_relevant_context(query)
        long_term = self.long_term.get_relevant_context(query)

        return f"Recent: {recent}\nWorking: {working}\nLong-term: {long_term}"

hierarchical_memory = HierarchicalMemory()

# Agent with hierarchical memory
advanced_agent = SimpleAgentV3(
    name="advanced_agent",
    engine=AugLLMConfig(),
    memory=hierarchical_memory
)
```

## 🏗️ How to Write Agents - CORRECT Patterns

### 1. System vs Human Message Pattern

```python
# ✅ CORRECT - System message in AugLLMConfig, Human message in ChatPromptTemplate
class AnswerAgent(SimpleAgentV3):
    engine: AugLLMConfig = Field(
        default_factory=lambda: AugLLMConfig(
            temperature=0.7,
            system_message="You are a helpful assistant."  # System message HERE
        )
    )

    prompt_template: ChatPromptTemplate = Field(
        default_factory=lambda: ChatPromptTemplate.from_messages([
            ("system", "System message from AugLLMConfig"),
            ("human", "User question: {query}\nContext: {context}")  # Human template HERE
        ])
    )

# ❌ WRONG - Everything in one template
prompt_template = ChatPromptTemplate.from_template(
    "System: You are helpful\nHuman: {query}"  # DON'T DO THIS
)
```

### 2. Agent Composition Pattern - Pydantic Classes

```python
# ✅ CORRECT - Pydantic class extending EnhancedMultiAgentV4
class SimpleRAGAgent(EnhancedMultiAgentV4):
    """Simple RAG = BaseRAGAgent + AnswerAgent in sequence."""

    agents: List = Field(
        default_factory=lambda: [
            BaseRAGAgent(name="retriever"),
            AnswerAgent(name="answerer")
        ]
    )

    execution_mode: str = Field(default="sequential")

# ✅ CORRECT - Collective RAG with multiple sources
class CollectiveRAGAgent(EnhancedMultiAgentV4):
    """Collective RAG = Multiple SimpleRAGAgent + SynthesisAgent."""

    agents: List = Field(
        default_factory=lambda: [
            SimpleRAGAgent(name="rag_source_1"),
            SimpleRAGAgent(name="rag_source_2"),
            SimpleRAGAgent(name="rag_source_3"),
            SynthesisAgent(name="synthesizer")
        ]
    )

    execution_mode: str = Field(default="parallel_then_sequential")

# ❌ WRONG - Complex inheritance and post_init
class ComplexRAGAgent(Agent):
    def model_post_init(self):
        # Don't build complex custom classes
        super().model_post_init()
        self.agents = [...]  # Overcomplicating
```

### 3. Base Agent Pattern - Generic Engines

```python
# ✅ CORRECT - Base agent with generic engine that works by default
class BaseRAGAgent(RetrieverMixin, Agent):
    engine: BaseRetrieverConfig | VectorStoreConfig = Field(
        default_factory=lambda: VectorStoreConfig(
            name="default_vectorstore",
            provider="InMemory",
            embedding_config=HuggingFaceEmbeddingConfig()  # Works by default
        )
    )

# ✅ CORRECT - Simple agent extension
class AnswerAgent(SimpleAgentV3):
    """SimpleAgentV3 with specific RAG configuration."""

    engine: AugLLMConfig = Field(
        default_factory=lambda: AugLLMConfig(
            temperature=0.7,
            system_message="You are a helpful assistant."
        )
    )

    prompt_template: ChatPromptTemplate = Field(...)

# ❌ WRONG - Building everything from scratch
class MyComplexAgent(Agent):
    def __init__(self):
        # Don't reinvent the wheel
        pass
```

### 4. Testing Pattern (NO MOCKS)

```python
# ✅ CORRECT - Real components, real execution
def test_simple_rag_agent():
    """Test with REAL components."""
    # Create instance - uses default HuggingFace embeddings
    rag_agent = SimpleRAGAgent(name="test_rag")

    # Real execution
    result = rag_agent.run("What is machine learning?")
    assert isinstance(result, str)
    assert len(result) > 0

    # Verify structure
    assert len(rag_agent.agents) == 2
    assert rag_agent.execution_mode == "sequential"

# ❌ WRONG - Mocks and fake responses
def test_with_mocks():
    mock_llm = Mock()
    mock_llm.return_value = "fake response"  # NOT REAL TESTING
```

## 🎯 Structured Output with Pydantic

### Basic Pattern

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class AnalysisResult(BaseModel):
    """Structured output model."""
    sentiment: str = Field(description="Overall sentiment")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score")
    key_themes: List[str] = Field(description="Main themes found")

# Use in agent
class AnalysisAgent(SimpleAgentV3):
    engine: AugLLMConfig = Field(
        default_factory=lambda: AugLLMConfig(
            temperature=0.3,
            structured_output_model=AnalysisResult,  # Pydantic model HERE
            system_message="You are an expert analyst."
        )
    )
```

### Multi-Agent Structured Workflow

```python
# Define output models for each step
class Plan(BaseModel):
    questions: List[str] = Field(description="Research questions")
    search_terms: List[str] = Field(description="Search terms")

class Findings(BaseModel):
    results: List[str] = Field(description="Key findings")
    sources: List[str] = Field(description="Source references")

class Report(BaseModel):
    summary: str = Field(max_length=500, description="Executive summary")
    recommendations: List[str] = Field(description="Action items")

# Create workflow
StructuredWorkflow = EnhancedMultiAgentV4([
    SimpleAgentV3(engine=AugLLMConfig(structured_output_model=Plan)),
    SimpleAgentV3(engine=AugLLMConfig(structured_output_model=Findings)),
    SimpleAgentV3(engine=AugLLMConfig(structured_output_model=Report))
], mode="sequential")
```

## 📁 Branch Examples & Implementation Locations

### Current RAG Implementation

**Branch**: `feature/fix_everything`

**Files**:

- `packages/haive-agents/src/haive/agents/rag/base/agent.py` - BaseRAGAgent with HuggingFace embeddings
- `packages/haive-agents/src/haive/agents/rag/simple/answer_agent.py` - AnswerAgent with document prompt
- `packages/haive-agents/src/haive/agents/rag/simple/agent.py` - SimpleRAGAgent Pydantic class

**Usage**:

```python
# Import the Pydantic class
from haive.agents.rag.simple.agent import SimpleRAGAgent

# Create instance - uses default HuggingFace embeddings
rag_agent = SimpleRAGAgent(name="my_rag")

# Execute RAG workflow
result = rag_agent.run("What is machine learning?")
print(result)
```

### Enhanced Agent Architecture

**Branch**: `feature/fix_everything`

**Key Files**:

- `packages/haive-agents/src/haive/agents/simple/agent_v3.py` - SimpleAgentV3 with hooks
- `packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_v4.py` - Multi-agent orchestration
- `packages/haive-core/src/haive/core/schema/prebuilt/meta_state.py` - MetaStateSchema

**Pattern**:

```python
# Enhanced agents with recompilation, hooks, dynamic tools
from haive.agents.simple.agent_v3 import SimpleAgentV3

agent = SimpleAgentV3(
    name="enhanced_agent",
    engine=AugLLMConfig(system_message="System message here"),
    prompt_template=ChatPromptTemplate.from_messages([
        ("system", "From AugLLMConfig"),
        ("human", "Template with {variables}")
    ])
)
```

### Multi-Agent Patterns

**Branch**: `feature/fix_everything`

**Files**:

- `packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_v4.py` - Core multi-agent
- `packages/haive-agents/src/haive/agents/rag/simple_rag_agent_v4.py` - RAG V4 example
- `packages/haive-agents/src/haive/agents/rag/collective_rag_agent_v4.py` - Collective RAG

**Simple Composition**:

```python
# Sequential: Agent A → Agent B → Agent C
MyWorkflow = EnhancedMultiAgentV4([AgentA, AgentB, AgentC], mode="sequential")
```

### Generalized Hook System

**New in Enhanced Base Agent**: All agents now support comprehensive hook system for monitoring, pre/post processing, reflection, and structured output workflows.

**Key Features**:

- Pre/post processing agents with message transformation
- Reflection and grading hooks
- Structured output hooks
- Multi-stage workflow monitoring
- Factory patterns for common use cases

**Files**:

- `packages/haive-agents/src/haive/agents/base/hooks.py` - Hook system core
- `packages/haive-agents/src/haive/agents/base/pre_post_agent_mixin.py` - Pre/post processing mixin
- `packages/haive-agents/examples/generalized_hooks_example.py` - Comprehensive examples

**Basic Hook Usage**:

```python
from haive.agents.simple.agent_v3 import SimpleAgentV3
from haive.core.engine.aug_llm import AugLLMConfig

agent = SimpleAgentV3(name="writer", engine=AugLLMConfig())

# Add hooks using decorators
@agent.before_run
def log_start(context):
    print(f"Starting {context.agent_name}")

@agent.after_run
def log_end(context):
    print(f"Completed {context.agent_name}")

@agent.before_reflection
def track_reflection(context):
    print("Starting reflection analysis")

# Execute with hook monitoring
result = await agent.arun("Write a story")
```

**Pre/Post Processing Pattern**:

```python
# Create main agent
main_agent = SimpleAgentV3(name="writer", engine=config)

# Create reflection agent
reflection_agent = SimpleAgentV3(name="critic", engine=reflection_config)

# Set up post-processing with message transformation
main_agent.post_agent = reflection_agent
main_agent.use_post_transform = True
main_agent.post_transform_type = "reflection"

# Execute with automatic pre/post processing
result = await main_agent.arun("Write and improve a story")
```

**Factory Pattern for Reflection**:

```python
from haive.agents.base.pre_post_agent_mixin import create_reflection_agent

# Create agent with reflection capabilities
enhanced_agent = create_reflection_agent(
    main_agent=SimpleAgentV3(name="writer", engine=config)
)

result = await enhanced_agent.arun("Complex writing task")
```

**Multi-Stage Workflow Monitoring**:

```python
from haive.agents.base.hooks import create_multi_stage_hook

# Track complex workflows
stages = ["analysis", "grading", "reflection", "improvement"]
hook = create_multi_stage_hook(stages)

agent.add_hook(HookEvent.PRE_PROCESS, hook)
agent.add_hook(HookEvent.POST_PROCESS, hook)

# Execute with comprehensive monitoring
result = await agent.arun("Complex analytical task")

# Parallel then sequential: [A, B, C] → D
MyWorkflow = EnhancedMultiAgentV4([AgentA, AgentB, AgentC, AgentD], mode="parallel_then_sequential")
```

### Documentation & Memory

**Branch**: `feature/fix_everything`

**Key Docs**:

- `CLAUDE.md` - This file - central memory and patterns
- `project_docs/active/architecture/multi_agent_meta_agent_memory_hub.md` - Multi-agent architecture
- `project_docs/active/architecture/meta_state_pattern.md` - MetaStateSchema guide
- `project_docs/active/standards/testing/philosophy.md` - No-mocks testing

**Memory References**:

```python
# Use @ to reference memory documents
# @project_docs/active/architecture/multi_agent_meta_agent_memory_hub.md
# @project_docs/active/standards/testing/philosophy.md
```

### Testing Pattern (NO MOCKS)

```python
def test_agent_real_execution():
    """Test with REAL components."""
    config = AugLLMConfig()
    agent = SimpleAgent(engine=config)

    result = agent.run("Hello")
    assert isinstance(result, str)
    assert len(result) > 0
```

## 🧠 Development Workflow

### Essential Steps

1. **Research First**: `find packages/ -name "*.py" | xargs grep -l "YourPattern"`
2. **Plan with TodoWrite**: Break down tasks into steps
3. **Build & Test Incrementally**: Create minimal → test → add feature → test
4. **Use Real Components**: No mocks, test with actual LLMs and tools

### Test-Driven Pattern

```python
# 1. Write test first
def test_my_agent_creation():
    agent = MyAgent()
    assert agent is not None

# 2. Make it pass
class MyAgent:
    def __init__(self):
        pass

# 3. Add feature test
def test_my_agent_execution():
    agent = MyAgent(config=AugLLMConfig())
    result = agent.run("Hello")
    assert isinstance(result, str)

# Continue incrementally...
```

## 🔗 Package Import Hierarchy

```
# ALLOWED:
- Core → standard library, third-party
- Agents → core, standard library, third-party
- Tools → core, standard library, third-party
- Games → core, agents, tools, third-party

# FORBIDDEN:
- Core → agents/tools/games (circular!)
```

## 🎨 Coding Style & Standards

### Python Code Style

```python
# ✅ CORRECT - Descriptive names, type hints, early returns
def process_agent_response(
    agent_response: str,
    validation_config: ValidationConfig
) -> ProcessedResponse:
    """Process agent response with validation.

    Args:
        agent_response: Raw response from agent
        validation_config: Configuration for validation rules

    Returns:
        ProcessedResponse with validation results

    Raises:
        ValidationError: If response fails validation
    """
    if not agent_response:
        raise ValidationError("Empty response")

    if not validation_config.enabled:
        return ProcessedResponse(content=agent_response, validated=False)

    # Process with validation
    validated_content = validate_response(agent_response, validation_config)
    return ProcessedResponse(
        content=validated_content,
        validated=True,
        validation_score=validated_content.score
    )

# ❌ WRONG - Poor naming, no types, nested logic
def process(resp, config):
    if resp:
        if config:
            if config.enabled:
                return validate_response(resp, config)
            else:
                return resp
        else:
            return resp
    else:
        return None
```

### Pydantic Model Patterns

```python
# ✅ CORRECT - Proper Pydantic usage
class AgentConfig(BaseModel):
    """Configuration for agent behavior."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid"
    )

    name: str = Field(..., min_length=1, max_length=50)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=None, ge=1)
    tools: List[str] = Field(default_factory=list)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate agent name format."""
        if not v.replace("_", "").isalnum():
            raise ValueError("Name must be alphanumeric with underscores")
        return v

# Usage - Pydantic handles initialization automatically
config = AgentConfig(name="my_agent", temperature=0.8)
# Pydantic validates all fields and creates the instance
```

### Error Handling Patterns

```python
# ✅ CORRECT - Structured error handling
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def execute_agent_safely(
    agent: Agent,
    input_data: str
) -> Optional[AgentResponse]:
    """Execute agent with comprehensive error handling."""
    try:
        logger.info(f"Executing agent {agent.name} with input length {len(input_data)}")

        response = agent.run(input_data)

        if not response:
            logger.warning(f"Agent {agent.name} returned empty response")
            return None

        logger.info(f"Agent {agent.name} completed successfully")
        return response

    except ValidationError as e:
        logger.error(f"Validation error in agent {agent.name}: {e}")
        raise AgentValidationError(f"Agent validation failed: {e}")

    except Exception as e:
        logger.error(f"Unexpected error in agent {agent.name}: {e}")
        raise AgentExecutionError(f"Agent execution failed: {e}")

# ❌ WRONG - Silent failures, print statements
def bad_execute(agent, input_data):
    try:
        result = agent.run(input_data)
        print(f"Got result: {result}")  # Use logger!
        return result
    except:
        print("Something went wrong")   # No error context!
        return None                     # Silent failure!
```

### Testing Patterns (NO MOCKS)

```python
# ✅ CORRECT - Real component testing with descriptive names
def test_simple_agent_handles_basic_conversation_with_real_llm():
    """Test SimpleAgent maintains conversation context with real LLM."""
    config = AugLLMConfig(temperature=0.1)  # Low for consistency
    agent = SimpleAgent(name="test_conversation", engine=config)

    # First exchange
    response1 = agent.run("My name is Alice")
    assert isinstance(response1, str)
    assert len(response1) > 0

    # Second exchange - should remember context
    response2 = agent.run("What's my name?")
    assert "alice" in response2.lower()

    # Verify state persistence
    assert len(agent.conversation_history) >= 4  # 2 user + 2 assistant

def test_react_agent_with_real_calculator_tool_integration():
    """Test ReactAgent uses real calculator tool correctly."""
    @tool
    def calculator(expression: str) -> str:
        """Real calculator tool."""
        return str(eval(expression))

    config = AugLLMConfig(temperature=0.1)
    agent = ReactAgent(
        name="test_calculator",
        engine=config,
        tools=[calculator]
    )

    result = agent.run("What is 15 * 23?")
    assert "345" in str(result)
    assert agent.tool_calls_made > 0

# ❌ WRONG - Mocks, vague names, no real testing
def test_agent():  # Vague name!
    mock_llm = Mock()  # NO MOCKS!
    mock_llm.return_value = "fake response"
    agent = SimpleAgent(llm=mock_llm)
    result = agent.run("test")
    assert result == "fake response"  # Tests nothing real!
```

## 🚨 Common Pitfalls to Avoid

1. **Running Python without poetry run** → ImportError
2. **Using mocks in tests** → False confidence
3. **Generic imports** → Use explicit haive.core.\*
4. **Overriding Pydantic **init\*\*\*\* → Breaks validation
5. **Using print() instead of logger** → Poor debugging
6. **git add .** → Stage files individually
7. **Building without testing** → Large broken changes
8. **Not asking for help** → Stuck for hours on solvable problems
9. **Skipping research phase** → Reinventing existing patterns
10. **Testing at the end** → Hard to debug failures
11. **Deleting test files** → Loss of valuable documentation

## 📊 MCP Integration (Recommended)

### Quick Setup for Common Tools

```bash
# PostgreSQL - Database operations
claude mcp add haive-db -s user -- npx -y @modelcontextprotocol/server-postgres "postgresql://localhost/haive"

# Filesystem - Enhanced file operations
claude mcp add haive-files -s user -- npx -y @modelcontextprotocol/server-filesystem /home/will/Projects/haive

# GitHub - Repository management
claude mcp add haive-github -s user -e GITHUB_TOKEN=$GITHUB_TOKEN -- npx -y @modelcontextprotocol/server-github

# List configured servers
claude mcp list
```

See: @project_docs/claude_documentation/MCP_SETUP.md for complete setup guide with 8+ servers

## 🆘 When to Ask for Help

### Don't Stay Stuck - Ask Specific Questions

```python
# ✅ GOOD - Specific questions with context
"I'm implementing a ReactAgent with tools but getting ImportError on langchain_core.tools.
I've checked that langchain is installed with poetry show. What should I check next?"

"My agent test passes but the agent isn't actually using the tools I provided.
Here's my test code: [code]. What's the pattern for testing tool usage?"

"I'm following the MetaStateSchema pattern but getting a Pydantic validation error
when trying to embed my agent. The error is: [error]. How do I fix this?"

# ❌ BAD - Vague questions
"My code doesn't work"
"I'm getting an error"
"How do I make an agent?"
```

### When to Ask vs When to Research

```python
# ✅ RESEARCH FIRST - Common patterns
find packages/ -name "*.py" | xargs grep -l "similar_problem"
# Look at existing agent implementations
# Check test files for patterns

# ✅ ASK FOR HELP - After research doesn't work
"I found 3 similar implementations [X, Y, Z] but none handle my specific case of [description].
What's the best approach for [specific problem]?"

# ✅ ASK FOR HELP - Time-sensitive issues
"I'm getting a blocking error that's preventing all tests from running: [error]"

# ✅ ASK FOR HELP - Architecture decisions
"Should I extend SimpleAgent or create a new agent type for [use case]?"
```

### Debugging Workflow

```bash
# 1. Check the basics
poetry run python -c "import haive.core; print('Core imports OK')"
poetry run python -c "import haive.agents; print('Agents imports OK')"
git status && git diff

# 2. Run minimal test
poetry run python -c "
from haive.core.engine.aug_llm import AugLLMConfig
from haive.agents.simple.agent import SimpleAgent
config = AugLLMConfig()
agent = SimpleAgent(engine=config)
print('Basic agent creation works')
"

# 3. If still stuck, ask for help with:
# - What you're trying to do
# - What you've tried
# - Exact error message
# - Minimal reproduction code
```

## 🔍 Quick Debugging

### Runtime Agent Debugging

```python
# ✅ ALWAYS use debug=True when developing/testing agents
agent = SimpleAgent(name="test_agent", engine=config)
result = agent.run("Hello", debug=True)  # Shows detailed execution info

# For ReactAgent with tools
agent = ReactAgent(name="debug_agent", engine=config, tools=[calculator])
result = agent.run("Calculate 15 * 23", debug=True)  # Shows tool calls, reasoning steps

# For async agents
result = await agent.arun("Hello", debug=True)  # Async version with debug info

# ✅ ALWAYS logically check outputs
print(f"Agent result: {result}")
print(f"Result type: {type(result)}")
print(f"Result length: {len(str(result))}")

# Check if result makes sense
if "345" in str(result):
    print("✅ Calculation appears correct")
else:
    print("❌ Expected calculation result not found")

# For structured outputs, check fields
if hasattr(result, 'content'):
    print(f"Content: {result.content}")
if hasattr(result, 'metadata'):
    print(f"Metadata: {result.metadata}")
```

### Environment Debugging

```bash
# Check imports work
poetry run python -c "from haive.core import *; from haive.agents import *"

# Verify environment
poetry env info
which python  # Should show .venv path

# Fix common issues
poetry install --all-extras
poetry cache clear pypi --all
```

### Documentation Build Debugging

```bash
# Build docs (check for errors)
nox -s docs

# Quick build test
poetry run sphinx-build -b html docs/source docs/build/html -W --keep-going

# Check for syntax errors in examples
find packages -name "*.py" -exec python -m py_compile {} \; 2>&1 | grep -E "Error|Sorry"

# Find files with invalid names (spaces, parentheses)
find . -name "*\ *" -o -name "*(*" -o -name "*)*"

# View docs locally
python -m http.server 8003 --directory docs/build/html/
# Then open http://localhost:8003
```

📚 **Documentation Memories**:

- @memory_index/by_task/documentation/ - All documentation-related memories
- @memory_index/by_error/build_errors/ - Build error solutions
- @memory_index/quick_reference.md - Common patterns and fixes

## 🧪 Testing: NO MOCKS + Proper Structure

### 🚨 IMPORTANT: Keep Test Files As Documentation

**DO NOT DELETE TEST FILES** - They serve as living documentation of:

- How the system should behave
- Real usage patterns and examples
- Edge cases and error handling
- Integration between components

Test files are valuable references for understanding the codebase!

### Test File Organization

```
packages/haive-{package}/
├── src/haive/{package}/
│   └── my_module.py           # Your source code
└── tests/
    └── test_my_module.py      # Test for that module

# ALWAYS: Test files go in packages/haive-*/tests/
# NEVER: Create test files in root or random locations
# ALWAYS: Keep test files after creation - they're documentation!

# For nested modules, mirror the source structure:
packages/haive-agents/
├── src/haive/agents/
│   └── reasoning_and_critique/
│       └── self_discover/
│           └── agent.py
└── tests/
    └── reasoning_and_critique/
        └── self_discover/
            └── test_agent.py   # Mirror the directory structure
```

### Running Tests

```bash
# Run all tests in a package
poetry run pytest packages/haive-agents/tests/ -v

# Run specific test subdirectory
poetry run pytest packages/haive-agents/tests/multi/ -v
poetry run pytest packages/haive-agents/tests/rag/ -v

# Run single test file
poetry run pytest packages/haive-agents/tests/multi/test_simple_multi_agent.py -v

# Run specific test function
poetry run pytest packages/haive-agents/tests/multi/test_simple_multi_agent.py::test_sequential_execution -v

# Run with coverage
poetry run pytest packages/haive-agents/tests/ --cov=haive.agents --cov-report=html

# Run tests matching pattern
poetry run pytest -k "test_react" -v
```

## 📂 File Organization Standards

### Project File Structure

```
haive/
├── packages/              # All package code
│   ├── haive-core/
│   │   ├── src/          # Source code
│   │   └── tests/        # Test files organized by module
│   │       ├── graph/    # Graph-related tests
│   │       ├── memory/   # Memory system tests
│   │       ├── schema/   # Schema tests
│   │       └── persistence/ # Persistence tests
│   ├── haive-agents/
│   │   ├── src/
│   │   └── tests/
│   │       ├── multi/    # Multi-agent tests
│   │       ├── rag/      # RAG agent tests
│   │       ├── planning/ # Planning agent tests
│   │       ├── research/ # Research agent tests
│   │       └── reasoning/ # Reasoning agent tests
│   └── ...
├── scripts/              # Utility scripts
│   ├── maintenance/      # Maintenance and fix scripts
│   │   ├── docs/        # Documentation build scripts
│   │   └── agents/      # Agent enhancement scripts
│   └── debug/           # Debug utilities
├── project_docs/         # Documentation
│   ├── active/          # Current standards
│   ├── summaries/       # Implementation summaries
│   ├── guides/          # User guides
│   ├── build-reports/   # Build and test reports
│   ├── issues/          # Issue tracking
│   └── plans/           # Architecture plans
├── examples/            # Example scripts
└── docs/                # Sphinx documentation

# Files that MUST stay in root:
- CLAUDE.md              # This file - central memory
- README.md              # Project readme
- pyproject.toml         # Poetry configuration
- noxfile.py            # Nox automation
- .gitignore            # Git ignore rules
```

### Creating New Files

```bash
# ALWAYS check if similar file exists first
find packages/ -name "*similar_pattern*" -type f

# Create test file in correct location
# For agent tests:
touch packages/haive-agents/tests/category/test_new_feature.py

# For core tests:
touch packages/haive-core/tests/module/test_new_component.py

# For scripts:
touch scripts/maintenance/category/new_script.py

# For documentation:
touch project_docs/category/new_doc.md
```

### Moving Files to Proper Locations

```bash
# If you accidentally create a test in root:
mv test_something.py packages/haive-agents/tests/appropriate_category/

# If you create a debug script in root:
mv fix_something.py scripts/debug/

# If you create documentation in root:
mv SOMETHING_SUMMARY.md project_docs/summaries/
```

## 📚 Documentation Standards

### Required Patterns

- **Google-style docstrings** on all public functions/classes
- **Type hints** on all parameters and returns
- **Examples** in docstrings for complex functions
- **@ references** for memory documents: `@project_docs/path/to/doc.md`

### Docstring Template

```python
def my_function(param: str, config: Optional[Config] = None) -> Result:
    """Brief description of what this does.

    Args:
        param: Description of parameter.
        config: Optional configuration.

    Returns:
        Result object with processed data.

    Examples:
        >>> result = my_function("test")
        >>> print(result.data)
    """
```

### Package README Structure

````markdown
# Package Name

Brief description.

## Installation

`poetry add package-name`

## Quick Start

```python
# Basic usage example
```
````

## Features

- Key feature list

## Documentation

- Links to guides and API docs

```

---

**Remember**: This file loads at every session. Keep frequently-used info here, import the rest!
```
