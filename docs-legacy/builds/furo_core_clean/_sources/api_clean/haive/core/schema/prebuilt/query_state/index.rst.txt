
haive.core.schema.prebuilt.query_state
======================================

.. py:module:: haive.core.schema.prebuilt.query_state

.. autoapi-nested-parse::

   Query State Schema for Advanced RAG and Document Processing.

   This module provides comprehensive query state management for advanced RAG workflows,
   document processing, and multi-query scenarios. It builds on top of MessagesState
   and DocumentState to provide a unified query processing interface.

   The QueryState enables:
   - Multi-query processing and refinement
   - Query expansion and optimization
   - Retrieval strategy management
   - Context tracking and memory
   - Source citation and provenance
   - Time-weighted and filtered queries
   - Self-query and adaptive retrieval
   - Query result caching and optimization

   .. admonition:: Examples

      Basic query processing::
      
          from haive.core.schema.prebuilt.query_state import QueryState
      
          state = QueryState(
              original_query="What are the latest trends in AI?",
              query_type="research",
              retrieval_strategy="adaptive"
          )
      
      Advanced multi-query workflow::
      
          state = QueryState(
              original_query="Analyze Q4 2024 financial performance",
              refined_queries=[
                  "Q4 2024 revenue growth analysis",
                  "Fourth quarter 2024 profit margins",
                  "2024 Q4 market performance comparison"
              ],
              query_expansion_enabled=True,
              time_weighted_retrieval=True,
              source_filters=["financial_reports", "earnings_calls"]
          )
      
      Self-query with structured output::
      
          from haive.core.schema.prebuilt.query_state import QueryType, RetrievalStrategy
      
          state = QueryState(
              original_query="Find all documents about machine learning published after 2023",
              query_type=QueryType.STRUCTURED,
              retrieval_strategy=RetrievalStrategy.SELF_QUERY,
              structured_query_enabled=True,
              metadata_filters={"year": {"$gt": 2023}, "topic": "machine_learning"}
          )

   Author: Claude (Haive AI Agent Framework)
   Version: 1.0.0







Classes
-------

* :py:class:`QueryType` - Types of queries supported by the query processing system.* :py:class:`RetrievalStrategy` - Retrieval strategies for query processing.* :py:class:`QueryComplexity` - Query complexity levels for processing optimization.* :py:class:`QueryIntent` - Intent classification for query processing.* :py:class:`QueryProcessingConfig` - Configuration for query processing behavior.* :py:class:`QueryMetrics` - Metrics and analytics for query processing.* :py:class:`QueryResult` - Result container for query processing.* :py:class:`QueryState` - State schema for conversation management with LangChain integration.* :py:class:`QueryState` - Comprehensive query state for advanced RAG and document processing.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/schema/prebuilt/query_state/QueryType   /api_clean/haive/core/schema/prebuilt/query_state/RetrievalStrategy   /api_clean/haive/core/schema/prebuilt/query_state/QueryComplexity   /api_clean/haive/core/schema/prebuilt/query_state/QueryIntent   /api_clean/haive/core/schema/prebuilt/query_state/QueryProcessingConfig   /api_clean/haive/core/schema/prebuilt/query_state/QueryMetrics   /api_clean/haive/core/schema/prebuilt/query_state/QueryResult   /api_clean/haive/core/schema/prebuilt/query_state/QueryState   /api_clean/haive/core/schema/prebuilt/query_state/QueryState

Package Contents
----------------

.. rubric:: haive.core.schema.prebuilt.query_state.__all__

.. autosummary::
   :nosignatures:

   QueryComplexity   QueryIntent   QueryMetrics   QueryProcessingConfig   QueryProcessingState   QueryResult   QueryState   QueryType   RetrievalStrategy
.. automodule:: haive.core.schema.prebuilt.query_state
   :members:
   :show-inheritance:
