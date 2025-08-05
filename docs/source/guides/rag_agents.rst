RAG (Retrieval-Augmented Generation) Agents
===========================================

This guide covers the extensive RAG agent implementations available in Haive, including various strategies, architectures, and use cases.

Overview
--------

RAG agents combine retrieval mechanisms with language models to provide context-aware responses. Haive offers 20+ specialized RAG implementations covering different retrieval strategies, grading mechanisms, and architectural patterns.

Core RAG Concepts
-----------------

Basic RAG Flow
~~~~~~~~~~~~~~

1. **Query Processing*: Transform user query for optimal retrieval
2. **Document Retrieval*: Fetch relevant documents from vector stores
3. **Document Grading*: Evaluate relevance of retrieved documents
4. **Answer Generation*: Generate response using retrieved context
5. **Hallucination Check*: Validate answer against source documents

Available RAG Agents
--------------------

Simple RAG Agents
~~~~~~~~~~~~~~~~~

**SimpleRAGAgent*

   - Location: ``haive.agents.rag.simple``
   - Basic retrieval and generation
   - Best for: Quick prototypes and simple Q&A

.. code-block:: python

    # Code example here

    from haive.agents.rag.simple import SimpleRAGAgent

    agent = SimpleRAGAgent(
    name="simple_rag",
    vector_store=vector_store,
    model="gpt-4"
    )

    async def example():
        result = await agent.query("What is RAG?")



**LLMRAGAgent*

    - Location: ``haive.agents.rag.llm_rag``
    - Direct LLM integration without complex routing
    - Best for: When you have high-quality embeddings

    Advanced Query Processing
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    **HyDERAGAgent* (Hypothetical Document Embeddings)

    - Location: ``haive.agents.rag.hyde``
    - Generates hypothetical documents to improve retrieval
    - Best for: Abstract or conceptual queries

.. code-block:: python

    # Code example here

    from haive.agents.rag.hyde import HyDERAGAgent

    agent = HyDERAGAgent(
    name="hyde_rag",
    vector_store=vector_store,
    hypothesis_model="gpt-4"
    )


**MultiQueryRAGAgent*

    - Location: ``haive.agents.rag.multi_query``
    - Generates multiple query variations
    - Best for: Ambiguous or multi-faceted queries

    **StepBackRAGAgent*

    - Location: ``haive.agents.rag.step_back``
    - Creates abstracted queries for better context
    - Best for: Specific questions needing broader context

    Document Grading & Validation
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **CorrectiveRAGAgent*

    - Location: ``haive.agents.rag.corrective``
    - Implements document grading and re-retrieval
    - Best for: High-accuracy requirements

.. code-block:: python

    # Code example here

    from haive.agents.rag.corrective import CorrectiveRAGAgent

    agent = CorrectiveRAGAgent(
    name="corrective_rag",
    vector_store=vector_store,
    grading_threshold=0.7,
    max_retries=3
    )


**SelfRAGAgent*

    - Location: ``haive.agents.rag.self_reflective``
    - Self-reflection and critique mechanisms
    - Best for: Complex reasoning tasks

    **HallucinationGradingAgent*

    - Location: ``haive.agents.rag.hallucination_grading``
    - Validates answers against source documents
    - Best for: Factual accuracy critical applications

    Specialized Architectures
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    **AdaptiveRAGAgent*

    - Location: ``haive.agents.rag.adaptive``
    - Dynamically adjusts retrieval strategy
    - Best for: Diverse query types

.. code-block:: python

    # Code example here

    from haive.agents.rag.adaptive import AdaptiveRAGAgent

    agent = AdaptiveRAGAgent(
    name="adaptive_rag",
    strategies=["simple", "hyde", "multi_query"],
    auto_select=True
    )


**FusionRAGAgent*

    - Location: ``haive.agents.rag.fusion``
    - Combines multiple retrieval methods
    - Best for: Maximum recall requirements

    **SpeculativeRAGAgent*

    - Location: ``haive.agents.rag.speculative``
    - Parallel retrieval with speculation
    - Best for: Low-latency requirements

    Database-Specific RAG
    ~~~~~~~~~~~~~~~~~~~~~

    **SQLRAGAgent*

    - Location: ``haive.agents.rag.db_rag.sql_rag``
    - Text-to-SQL with retrieval augmentation
    - Best for: Structured data queries

.. code-block:: python

    # Code example here

    from haive.agents.rag.db_rag.sql_rag import SQLRAGAgent

    agent = SQLRAGAgent(
    name="sql_rag",
    database_url="postgresql://...",
    schema_description="sales database"
    )


**GraphRAGAgent*

    - Location: ``haive.agents.rag.db_rag.graph_db``
    - Graph database retrieval
    - Best for: Relationship-heavy queries

    Multi-Agent RAG Systems
    ~~~~~~~~~~~~~~~~~~~~~~~

    **MultiAgentRAG*

    - Location: ``haive.agents.rag.multi_agent_rag``
    - Orchestrates multiple specialized RAG agents
    - Best for: Complex workflows

.. code-block:: python

    # Code example here

    from haive.agents.rag.multi_agent_rag import MultiAgentRAG

    system = MultiAgentRAG(
    agents={
    "researcher": ResearchRAGAgent(),
    "validator": ValidationRAGAgent(),
    "synthesizer": SynthesisRAGAgent()
    }
    )

    Configuration Patterns

----------------------

    Basic Configuration
    ~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Code example here

    from haive.agents.rag.base import RAGConfig

    config = RAGConfig(
    # Retrieval settings
    vector_store_type="chroma",
    embedding_model="text-embedding-3-small",
    chunk_size=500,
    chunk_overlap=50,
    top_k=5,

    # Generation settings
    llm_model="gpt-4",
    temperature=0.7,
    max_tokens=1000,

    # Grading settings
    relevance_threshold=0.7,
    enable_reranking=True,

    # Memory settings
    enable_memory=True,
    memory_type="conversation_buffer"
    )

    Advanced Configuration

~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Code example here

    from haive.agents.rag.multi_strategy import MultiStrategyConfig

    config = MultiStrategyConfig(
    strategies={
    "factual": {
    "retrieval": "dense",
    "grading": "strict",
    "generation": "precise"
    },
    "creative": {
    "retrieval": "hybrid",
    "grading": "lenient",
    "generation": "creative"
    }
    },
    strategy_selector="auto",  # or "manual"
    fallback_strategy="factual"
    )

    Common Patterns

---------------

    Query Enhancement
    ~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Code example here

    # Query decomposition
    from haive.agents.rag.query_decomposition import QueryDecomposer

    decomposer = QueryDecomposer()
    async def example():
        sub_queries = await decomposer.decompose(

    "Compare advantages and disadvantages of solar vs wind energy"
    )
    # Result: ["advantages of solar energy", "disadvantages of solar energy", ...]

    Document Processing

~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Code example here

    # Custom document grading
    from haive.agents.rag.common.document_graders import ComprehensiveGrader

    grader = ComprehensiveGrader(
    relevance_weight=0.4,
    completeness_weight=0.3,
    accuracy_weight=0.3
    )

    async def example():
        score = await grader.grade(document, query)


    Hallucination Prevention

~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Code example here

    # Hallucination checking
    from haive.agents.rag.common.hallucination_graders import HallucinationGrader

    grader = HallucinationGrader()
    async def example():
        is_grounded = await grader.check(

    answer=generated_answer,
    sources=retrieved_documents
    )

    Performance Optimization

------------------------

    Caching Strategies
    ~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Code example here

    from haive.agents.rag.base import RAGAgent
    from haive.core.cache import SemanticCache

    cache = SemanticCache(similarity_threshold=0.95)

    agent = RAGAgent(
    name="cached_rag",
    cache=cache,
    cache_ttl=3600  # 1 hour
    )

    Batch Processing

~~~~~~~~~~~~~~~~

.. code-block:: python

    # Code example here

    # Process multiple queries efficiently
    queries = ["Query 1", "Query 2", "Query 3"]

    async def example():
        results = await agent.batch_query(

    queries=queries,
    batch_size=10,
    parallel=True
    )

    Streaming Responses

~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Code example here

    # Stream responses for real-time applications
    async for chunk in agent.stream_query("Complex question"):
    print(chunk, end="", flush=True)

    Integration Examples

--------------------

    With Memory Systems
    ~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Code example here

    from haive.agents.rag.memory_aware import MemoryAwareRAGAgent

    agent = MemoryAwareRAGAgent(
    name="memory_rag",
    memory_type="conversation_summary",
    memory_window=10,
    include_memory_in_context=True
    )

    With Tool Usage

~~~~~~~~~~~~~~~

.. code-block:: python

    # Code example here

    from haive.agents.rag.adaptive_tools import ToolAugmentedRAGAgent
    from haive.tools import WebSearchTool, CalculatorTool

    agent = ToolAugmentedRAGAgent(
    name="tool_rag",
    tools=[WebSearchTool(), CalculatorTool()],
    tool_selection="auto"
    )

    With Structured Output

~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Code example here

    from haive.agents.rag.typed import TypedRAGAgent
    from pydantic import BaseModel

    class AnalysisResult(BaseModel):
        pass
    summary: str
    key_points: List[str]
    confidence: float

    agent = TypedRAGAgent(
    name="typed_rag",
    output_schema=AnalysisResult
    )

    Best Practices

--------------

    1. **Choose the Right Agent*

    - Start with SimpleRAGAgent for prototypes
    - Use CorrectiveRAGAgent for accuracy-critical tasks
    - Deploy AdaptiveRAGAgent for diverse query types

    2. **Optimize Retrieval*

    - Tune chunk size based on your content
    - Use hybrid search for better recall
    - Implement semantic caching for common queries

    3. **Ensure Quality*

    - Always enable document grading for production
    - Implement hallucination checks for factual content
    - Monitor retrieval and generation metrics

    4. **Scale Efficiently*

    - Use batch processing for multiple queries
    - Implement connection pooling for databases
    - Cache embeddings for frequently accessed documents

    Troubleshooting
    ---------------

    Common Issues
    ~~~~~~~~~~~~~

    **Low Retrieval Quality*

    - Increase ``top_k`` parameter
    - Try different embedding models
    - Implement query enhancement (HyDE, multi-query)

    **Hallucinations*

    - Enable strict document grading
    - Reduce generation temperature
    - Implement fact-checking post-processing

    **Performance Issues*

    - Enable caching
    - Use smaller embedding models
    - Implement async processing

    **Context Limits*

    - Implement document summarization
    - Use relevance-based truncation
    - Consider multi-turn interactions

    Monitoring & Debugging
    ~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Code example here

    # Enable detailed logging
    import logging

    logging.getLogger("haive.agents.rag").setLevel(logging.DEBUG)

    # Track metrics
    from haive.monitoring import RAGMonitor

    monitor = RAGMonitor()
    agent = SimpleRAGAgent(monitor=monitor)

    # Get performance metrics
    metrics = monitor.get_metrics()
    print(f"Avg retrieval time: {metrics.avg_retrieval_time}s")
    print(f"Avg generation time: {metrics.avg_generation_time}s")

    Advanced Topics

---------------

    Custom RAG Implementation
    ~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Code example here

    from haive.agents.rag.base import BaseRAGAgent

    class CustomRAGAgent(BaseRAGAgent):
        pass
    async def retrieve(self, query: str) -> List[Document]:
    # Custom retrieval logic
    pass

    async def grade(self, docs: List[Document], query: str) -> List[Document]:
    # Custom grading logic
    pass

    async def generate(self, query: str, context: List[Document]) -> str:
    # Custom generation logic
    pass

    Factory Pattern Usage

~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Code example here

    from haive.agents.rag.factories import CompatibleRAGFactory

    factory = CompatibleRAGFactory()

    # Create agent from configuration
    agent = factory.create_agent({
    "type": "corrective",
    "vector_store": "chroma",
    "model": "gpt-4",
    "grading_enabled": True
    })

    Multi-Modal RAG

~~~~~~~~~~~~~~~

.. code-block:: python

    # Code example here

    from haive.agents.rag.multimodal import MultiModalRAGAgent

    agent = MultiModalRAGAgent(
    name="mm_rag",
    supported_modalities=["text", "image", "table"],
    embedding_models={
    "text": "text-embedding-3",
    "image": "clip-vit-base"
    }
    )

    See Also

--------

    - **RAG API Reference*: ``/docs/source/api/agents/rag.rst``
    - **Vector Store Configuration*: ``/docs/source/guides/vector_stores.rst``
    - **Embedding Models Guide*: ``/docs/source/guides/embeddings.rst``
    - **RAG Examples*: ``/examples/rag/``
