Engine System
=============

The engine system provides the core infrastructure for integrating LLMs, documents, embeddings, and tools into the Haive framework.

Module path: ``haive.core.engine``

Overview
--------

Engines are the bridge between Haive agents and various AI capabilities:

.. grid:: 1 2 2 3
   :gutter: 3

   .. grid-item-card:: **Base Engine**
      :link: base
      :link-type: doc
      
      Abstract base class for all engines
      
   .. grid-item-card:: **Aug LLM Engine**
      :link: aug_llm
      :link-type: doc
      
      Augmented LLM with tools & schemas
      
   .. grid-item-card:: **Document Engine**
      :link: document
      :link-type: doc
      
      Document processing & loaders
      
   .. grid-item-card:: **Agent Engine**
      :link: agent
      :link-type: doc
      
      Agent-specific engine utilities
      
   .. grid-item-card:: **Embedding Engine**
      :link: embedding
      :link-type: doc
      
      Text embedding generation
      
   .. grid-item-card:: **Retriever Engine**
      :link: retriever
      :link-type: doc
      
      Document retrieval systems
      
   .. grid-item-card:: **Vectorstore Engine**
      :link: vectorstore
      :link-type: doc
      
      Vector database integration
      
   .. grid-item-card:: **Tool Engine**
      :link: tool
      :link-type: doc
      
      Tool registration & execution

Engine Architecture
-------------------

.. code-block:: text

   BaseEngine (Abstract)
   ├── AugLLMEngine      # LLM + Tools + Structured Output
   ├── DocumentEngine    # Document loading & processing
   ├── EmbeddingEngine   # Text → Vector embeddings
   ├── RetrieverEngine   # Similarity search & retrieval
   ├── VectorstoreEngine # Vector DB operations
   └── ToolEngine        # Tool management

Quick Start
-----------

**Creating an Augmented LLM Engine:**

.. code-block:: python

   from haive.core.engine.aug_llm import AugLLMEngine, AugLLMEngineConfig
   from haive.core.tools import tool
   
   # Define tools
   @tool
   def calculate(expression: str) -> float:
       """Calculate a mathematical expression."""
       return eval(expression)
   
   # Create engine with tools
   config = AugLLMEngineConfig(
       model="gpt-4o",
       temperature=0.7,
       tools=[calculate]
   )
   
   engine = AugLLMEngine(config)
   
   # Use in agent
   result = await engine.arun({
       "messages": [{"role": "user", "content": "What is 2 + 2?"}]
   })

**Document Processing:**

.. code-block:: python

   from haive.core.engine.document import DocumentEngine
   
   doc_engine = DocumentEngine()
   
   # Load documents
   documents = await doc_engine.load_documents(
       source="path/to/docs",
       file_types=[".pdf", ".md", ".txt"]
   )
   
   # Split into chunks
   chunks = await doc_engine.split_documents(
       documents,
       chunk_size=1000,
       overlap=200
   )

**Embedding Generation:**

.. code-block:: python

   from haive.core.engine.embedding import EmbeddingEngine
   
   embed_engine = EmbeddingEngine(
       model="text-embedding-3-small"
   )
   
   # Generate embeddings
   embeddings = await embed_engine.embed_documents(
       texts=["Hello world", "Haive framework"]
   )

**Vector Store Integration:**

.. code-block:: python

   from haive.core.engine.vectorstore import VectorstoreEngine
   from haive.core.engine.retriever import RetrieverEngine
   
   # Create vector store
   vectorstore = VectorstoreEngine(
       provider="chroma",
       collection_name="my_docs"
   )
   
   # Add documents
   await vectorstore.add_documents(documents, embeddings)
   
   # Create retriever
   retriever = RetrieverEngine(
       vectorstore=vectorstore,
       search_type="similarity",
       k=5
   )
   
   # Search
   results = await retriever.retrieve("What is Haive?")

Engine Composition
------------------

Engines can be composed for complex workflows:

.. code-block:: python

   from haive.agents.rag import BaseRAGAgent
   
   # RAG agent uses multiple engines
   rag_agent = BaseRAGAgent(
       name="rag_assistant",
       llm_engine=aug_llm_engine,
       embedding_engine=embed_engine,
       retriever_engine=retriever_engine,
       document_engine=doc_engine
   )

Best Practices
--------------

1. **Engine Reuse**: Create engines once and share across agents
2. **Configuration**: Use environment variables for API keys
3. **Error Handling**: Engines provide structured error responses
4. **Async First**: All engine operations are async
5. **Type Safety**: Engines use Pydantic models for I/O

.. toctree::
   :maxdepth: 2
   :caption: Engine Types
   :hidden:
   
   base
   aug_llm
   document
   agent
   embedding
   retriever
   vectorstore
   tool

See Also
--------

- :doc:`/api/haive/core/models/index` - Model configurations
- :doc:`/guides/engine_system` - Engine system guide
- :doc:`/api/haive/core/schema/index` - Schema system