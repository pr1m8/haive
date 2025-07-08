DB RAG
======

Database-backed Retrieval Augmented Generation agents for SQL and Graph databases.

Module path: ``haive.agents.rag.db_rag``

Overview
--------

The DB RAG module provides agents that combine database querying with language models:

- **SQL RAG**: Query SQL databases and generate natural language responses
- **Graph DB**: Query graph databases with natural language

Architecture
------------

.. code-block:: text

   User Query → Query Constructor → Database → Result Parser → LLM → Response

Submodules
----------

SQL RAG Agent
~~~~~~~~~~~~~

For querying relational databases:

.. code-block:: python

   from haive.agents.rag.db_rag.sql_rag import SQLRAGAgent
   
   sql_agent = SQLRAGAgent(
       name="sql_assistant",
       engine=llm_engine,
       connection_string="postgresql://user:pass@localhost/db",
       schema_description="E-commerce database with orders, products, customers"
   )
   
   result = await sql_agent.arun({
       "query": "What were the top selling products last month?"
   })

Features:
- Natural language to SQL conversion
- Schema-aware query generation
- Result interpretation and summarization
- Error handling and query validation

Graph DB Agent
~~~~~~~~~~~~~~

For querying graph databases:

.. code-block:: python

   from haive.agents.rag.db_rag.graph_db import GraphDBAgent
   
   graph_agent = GraphDBAgent(
       name="graph_assistant",
       engine=llm_engine,
       connection_string="bolt://localhost:7687",
       database="neo4j"
   )
   
   result = await graph_agent.arun({
       "query": "Find all connections between user A and user B"
   })

Features:
- Natural language to Cypher/Gremlin
- Path finding and pattern matching
- Relationship exploration
- Graph visualization support

Configuration
-------------

.. code-block:: python

   from haive.agents.rag.db_rag.base import DatabaseConfig
   
   config = DatabaseConfig(
       connection_string="...",
       schema_sampling=True,
       max_results=100,
       timeout=30,
       use_reflection=True
   )

Security Considerations
-----------------------

- **Never hardcode credentials** - Use environment variables or secrets management
- **Query validation** - All generated queries are validated before execution
- **Read-only mode** - Option to restrict to SELECT/MATCH queries only
- **Schema permissions** - Limit access to sensitive tables/collections

Module Documentation
--------------------

.. automodule:: haive.agents.rag.db_rag
   :members:
   :undoc-members:
   :show-inheritance:

Submodules
----------

.. autosummary::
   :toctree: generated
   :maxdepth: 1
   
   haive.agents.rag.db_rag.base
   haive.agents.rag.db_rag.sql_rag
   haive.agents.rag.db_rag.graph_db

See Also
--------

- :doc:`/api/haive/agents/rag/index` - RAG agents overview
- :doc:`/guides/rag_agents` - RAG implementation guide