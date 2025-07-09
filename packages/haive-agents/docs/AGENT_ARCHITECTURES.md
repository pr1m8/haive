# Agent Architectures in Haive

## Overview

This document outlines the different agent architecture patterns available in the Haive framework, focusing on proper use of generics, type safety, and the base agent infrastructure.

## Core Principles

### 1. No `__init__` with Pydantic

- Use **model validators**, **computed fields**, and **annotations**
- Leverage Pydantic's validation system instead of manual initialization
- Use `@model_validator(mode="after")` for post-initialization setup

### 2. Proper Generic Usage

- Inherit from `GenericAgent[TInput, TOutput, TState]`
- Use TypeVars with proper bounds: `TLLMEngine: AugLLMConfig`
- Leverage automatic schema derivation from base agent

### 3. Tool Route Management

- Use `ToolRouteMixin` for automatic tool routing
- Routes: `"pydantic_model"`, `"langchain_tool"`, `"function"`, `"retriever"`
- Tools are automatically analyzed and routed by type

## Agent Architecture Patterns

### 1. Base LLM Agent Pattern

```python
from haive.agents.base.generic_agent import GenericAgent
from haive.core.common.mixins.tool_route_mixin import ToolRouteMixin

class BaseLLMAgent[TInput: BaseModel, TOutput: BaseModel](
    GenericAgent[TInput, TOutput, MessagesState],
    ToolRouteMixin
):
    """Base pattern for LLM-based agents with tool routing."""

    # Primary LLM engine
    llm_engine: AugLLMConfig = Field(...)

    # Tools managed via ToolRouteMixin
    @model_validator(mode="after")
    def setup_llm_agent(self) -> "BaseLLMAgent":
        """Setup LLM agent with proper tool routing."""
        # Add LLM engine to engines dict
        self.engines["llm"] = self.llm_engine

        # Sync tool routes from any configured tools
        if hasattr(self, 'tools') and self.tools:
            self.sync_tool_routes_from_tools(self.tools)

        return self

    @computed_field
    @property
    def main_engine(self) -> AugLLMConfig:
        """Computed property for main engine."""
        return self.llm_engine
```

### 2. ReAct Agent Pattern

```python
class ReActAgent[TInput: BaseModel, TOutput: BaseModel](
    BaseLLMAgent[TInput, TOutput]
):
    """ReAct pattern with proper looping and tool execution."""

    # ReAct-specific configuration
    max_iterations: int = Field(default=10, description="Max reasoning iterations")
    stop_on_final_answer: bool = Field(default=True, description="Stop when final answer reached")

    def build_graph(self) -> BaseGraph:
        """Build ReAct graph with reasoning loop."""
        graph = BaseGraph(name=self.name)

        # Add reasoning node (LLM engine)
        reasoning_node = EngineNodeConfig(
            name="reasoning",
            engine=self.llm_engine
        )
        graph.add_node("reasoning", reasoning_node)

        # Add tool execution node if tools available
        if self.tool_routes:
            tool_node = ToolNodeConfig(
                name="tools",
                engine_name=self.llm_engine.name,
                allowed_routes=list(set(self.tool_routes.values()))
            )
            graph.add_node("tools", tool_node)

            # ReAct loop: reasoning -> tools -> reasoning
            graph.add_conditional_edges(
                "reasoning",
                self._should_use_tools,
                {True: "tools", False: END}
            )
            graph.add_edge("tools", "reasoning")
        else:
            graph.add_edge("reasoning", END)

        graph.add_edge(START, "reasoning")
        return graph

    def _should_use_tools(self, state) -> bool:
        """Determine if tools should be used based on last message."""
        # Implementation using base agent's tool checking logic
        return self._has_tool_calls(state)
```

### 3. RAG Agent Pattern

```python
class RAGAgent[TInput: BaseModel, TOutput: BaseModel](
    BaseLLMAgent[TInput, TOutput]
):
    """RAG pattern with retrieval and generation."""

    # Retrieval engine
    retriever_engine: BaseRetrieverConfig = Field(...)

    @model_validator(mode="after")
    def setup_rag_agent(self) -> "RAGAgent":
        """Setup RAG with both engines."""
        # Add both engines
        self.engines["retriever"] = self.retriever_engine
        self.engines["llm"] = self.llm_engine

        # Set up retriever as a tool
        self.set_tool_route("retrieve", "retriever", {
            "engine": "retriever",
            "description": "Retrieve relevant documents"
        })

        return self

    @classmethod
    def from_documents(
        cls,
        documents: List[Document],
        llm_config: LLMConfig,
        embedding_config: Optional[EmbeddingConfig] = None
    ) -> "RAGAgent":
        """Factory method using proper Pydantic patterns."""
        retriever_engine = BaseRetrieverConfig.from_documents(
            documents=documents,
            embedding_config=embedding_config
        )

        llm_engine = AugLLMConfig(
            llm_config=llm_config,
            prompt_template=RAG_ANSWER_STANDARD
        )

        return cls(
            retriever_engine=retriever_engine,
            llm_engine=llm_engine
        )
```

### 4. Agentic RAG Pattern (ReAct + Retrieval)

```python
class AgenticRAGAgent[TInput: BaseModel, TOutput: BaseModel](
    ReActAgent[TInput, TOutput]
):
    """Agentic RAG combining ReAct reasoning with retrieval tools."""

    # Additional retrieval capability
    retriever_engine: BaseRetrieverConfig = Field(...)

    @model_validator(mode="after")
    def setup_agentic_rag(self) -> "AgenticRAGAgent":
        """Setup agentic RAG with retrieval tools."""
        # Add retriever engine
        self.engines["retriever"] = self.retriever_engine

        # Create retrieval tools
        retrieval_tools = [
            self.retriever_engine.to_tool(
                name="retrieve_documents",
                description="Retrieve relevant documents for the query"
            ),
            self._create_search_tool(),
            self._create_context_tool()
        ]

        # Add tools with proper routing
        for tool in retrieval_tools:
            route = "retriever" if "retrieve" in tool.name else "function"
            self.add_routed_tool(tool, route)

        return self

    def _create_search_tool(self) -> BaseTool:
        """Create semantic search tool."""
        def search_documents(query: str) -> str:
            """Search documents semantically."""
            result = self.retriever_engine.invoke({"query": query})
            return f"Found {len(result.get('documents', []))} relevant documents"

        return StructuredTool.from_function(
            func=search_documents,
            name="search_documents",
            description="Search through available documents"
        )

    def _create_context_tool(self) -> BaseTool:
        """Create context analysis tool."""
        def analyze_context(context: str) -> str:
            """Analyze retrieved context for relevance."""
            # Use LLM engine to analyze context
            analysis_prompt = ChatPromptTemplate.from_template(
                "Analyze this context for relevance: {context}"
            )
            # Implementation would use self.llm_engine
            return "Context analysis complete"

        return StructuredTool.from_function(
            func=analyze_context,
            name="analyze_context",
            description="Analyze context for relevance and quality"
        )
```

## Multi-Agent Composition Patterns

### 1. Sequential Multi-Agent

```python
class MultiRAGWorkflow[TInput: BaseModel, TOutput: BaseModel](
    SequentialAgent[TInput, TOutput, RAGState]
):
    """Multi-agent RAG workflow with sequential processing."""

    @classmethod
    def create_workflow(
        cls,
        documents: List[Document],
        llm_config: LLMConfig,
        **kwargs
    ) -> "MultiRAGWorkflow":
        """Create multi-agent RAG workflow."""

        # Create specialized agents
        retrieval_agent = RAGAgent.from_documents(documents, llm_config)
        reasoning_agent = ReActAgent(llm_engine=AugLLMConfig(llm_config=llm_config))
        analysis_agent = AgenticRAGAgent.from_documents(documents, llm_config)

        return cls(
            agents=[retrieval_agent, reasoning_agent, analysis_agent],
            **kwargs
        )
```

### 2. Conditional Multi-Agent

```python
class AdaptiveRAGWorkflow[TInput: BaseModel, TOutput: BaseModel](
    ConditionalAgent[TInput, TOutput, RAGState]
):
    """Adaptive RAG that routes to different agents based on query type."""

    @model_validator(mode="after")
    def setup_routing(self) -> "AdaptiveRAGWorkflow":
        """Setup conditional routing based on query complexity."""

        def route_query(state) -> str:
            """Route based on query complexity."""
            query = state.get("query", "")
            if len(query.split()) > 20:
                return "complex_rag"
            elif "?" in query:
                return "simple_rag"
            else:
                return "agentic_rag"

        self.routing_function = route_query
        return self
```

## Best Practices

### 1. Engine Management

- Use `engines` dict, not single `engine` field
- Add engines in `@model_validator(mode="after")`
- Use computed properties for main engine access

### 2. Tool Integration

- Inherit from `ToolRouteMixin` for automatic routing
- Use `set_tool_route()` and `add_routed_tool()`
- Let the mixin analyze tool types automatically

### 3. Schema Composition

- Leverage `GenericAgent` auto-schema derivation
- Use proper TypeVar bounds for type safety
- Let base agent handle schema composition

### 4. Factory Methods

- Use `@classmethod` factory methods, not `__init__`
- Validate inputs and create engines in factory
- Return fully configured agent instances

### 5. State Management

- Define clear state schemas with proper inheritance
- Use base message state + domain-specific fields
- Let schema composer handle multi-agent state merging

This architecture provides type-safe, extensible, and composable agent patterns that leverage the full power of the Haive framework's infrastructure.
