RAG Agents



Retrieval-Augmented Generation agents combine the power of LLMs with external knowledge sources.

.. note::



   This is the user guide for RAG agents. For API documentation, see :doc:`/api/haive/agents/rag/index.`
`

Overview



RAG agents in Haive provide intelligent document retrieval and question-answering capabilities:

- **BaseRAGAgent** - Foundation for all RAG implementations
- **HybridRAGAgent** - Combines multiple retrieval strategies
- **AdaptiveRAGAgent** - Dynamically adjusts retrieval based on query
- **GraphRAGAgent** - Uses knowledge graphs for enhanced retrieval

Quick Start



.. code-block:: python

    # Code example here

   from haive.agents.rag import BaseRAGAgent
   from haive.core.vectorstore import ChromaStore

   # Create vector store
   vectorstore = ChromaStore(collection_name="documents")

   # Create RAG agent
   rag_agent = BaseRAGAgent(

       name="knowledge_assistant",
       vectorstore=vectorstore,
       retriever_config={"k": 5}

   )

   # Ask questions
   response = await rag_agent.arun(

       "What are the key features of our product?"

   )

   RAG Agent Types



   .. grid:: 2


   .. grid-item-card:: BaseRAGAgent

      :text-align: center

      Foundation RAG implementation with customizable retrieval

   .. grid-item-card:: HybridRAGAgent

      :text-align: center

      Combines keyword and semantic search

   .. grid-item-card:: AdaptiveRAGAgent

      :text-align: center

      Dynamically adjusts retrieval strategy

   .. grid-item-card:: GraphRAGAgent

      :text-align: center

      Knowledge graph-enhanced retrieval

   Examples



   See our :doc`:`/guides/rag_agents guide for detailed examples and best practices.`
`

   .. toctree::


   :maxdepth: 2
   :hidden:

   base_rag
   hybrid_rag
   adaptive_rag
   graph_rag
`
