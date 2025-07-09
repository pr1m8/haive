"""Graph Database RAG Agent package.

This package provides a sophisticated agent for natural language querying of Neo4j
graph databases. It converts user questions into Cypher queries, executes them,
and returns natural language answers.

The package includes:
    - **GraphDBRAGAgent**: Main agent class for graph database querying
    - **GraphDBRAGConfig**: Configuration class for the agent
    - **State classes**: Input, output, and workflow state management
    - **Models**: Structured output models for LLM responses
    - **Engines**: Pre-configured LLM engines for each workflow step

Quick Start:
    Basic usage with default configuration::

        >>> from haive.agents.rag.db_rag.graph_db import GraphDBRAGAgent
        >>>
        >>> # Create agent (uses environment variables for Neo4j)
        >>> agent = GraphDBRAGAgent()
        >>>
        >>> # Query the database
        >>> result = agent.invoke({"question": "What are the top rated movies?"})
        >>> print(result["answer"])

    Custom configuration::

        >>> from haive.agents.rag.db_rag.graph_db import GraphDBRAGAgent, GraphDBRAGConfig
        >>> from haive.agents.rag.db_rag.graph_db.config import GraphDBConfig
        >>>
        >>> # Configure for healthcare domain
        >>> config = GraphDBRAGConfig(
        ...     domain_name="healthcare",
        ...     domain_categories=["patient", "doctor", "medication", "condition"],
        ...     graph_db_config=GraphDBConfig(
        ...         graph_db_uri="bolt://localhost:7687",
        ...         graph_db_database="healthcare"
        ...     )
        ... )
        >>>
        >>> agent = GraphDBRAGAgent(config)

Environment Variables:
    The package uses these environment variables for Neo4j connection:

    - **NEO4J_URI**: Database URI (default: "bolt://localhost:7687")
    - **NEO4J_USER**: Username (default: "neo4j")
    - **NEO4J_PASSWORD**: Password (required)
    - **NEO4J_DATABASE**: Database name (default: "neo4j")

Example Workflow:
    The agent processes queries through these steps:

    1. **Domain Check**: Validates query relevance
    2. **Query Generation**: Natural language → Cypher
    3. **Validation**: Checks Cypher against schema
    4. **Correction**: Fixes any errors
    5. **Execution**: Runs query on Neo4j
    6. **Answer Generation**: Results → Natural language

Advanced Usage:
    Using with custom examples::

        >>> from haive.agents.rag.db_rag.graph_db.config import ExampleConfig
        >>>
        >>> config = GraphDBRAGConfig(
        ...     domain_name="movies",
        ...     example_config=ExampleConfig(
        ...         examples=[
        ...             {
        ...                 "question": "What movies did Tom Hanks act in?",
        ...                 "query": "MATCH (p:Person {name: 'Tom Hanks'})-[:ACTED_IN]->(m:Movie) RETURN m.title"
        ...             },
        ...             {
        ...                 "question": "Who directed The Matrix?",
        ...                 "query": "MATCH (p:Person)-[:DIRECTED]->(m:Movie {title: 'The Matrix'}) RETURN p.name"
        ...             }
        ...         ],
        ...         k=2  # Use 2 examples for few-shot learning
        ...     )
        ... )

    Streaming execution::

        >>> for chunk in agent.stream({"question": "List all actors"}):
        ...     if "generate_answer" in chunk:
        ...         print("Generating final answer...")
        ...     if "answer" in chunk:
        ...         print(f"Answer: {chunk['answer']}")

See Also:
    - Neo4j Documentation: https://neo4j.com/docs/
    - Cypher Query Language: https://neo4j.com/docs/cypher-manual/
    - LangGraph Documentation: https://python.langchain.com/docs/langgraph

Note:
    This package requires a running Neo4j instance and appropriate credentials.
    The agent works best with a well-structured graph schema and domain-specific
    examples for few-shot learning.
"""

# Import main components for easier access
from haive.agents.rag.db_rag.graph_db.agent import GraphDBRAGAgent
from haive.agents.rag.db_rag.graph_db.config import (
    ExampleConfig,
    GraphDBConfig,
    GraphDBRAGConfig,
)
from haive.agents.rag.db_rag.graph_db.models import (
    CypherQueryOutput,
    GuardrailsOutput,
    PropertyFilter,
    ValidateCypherOutput,
)
from haive.agents.rag.db_rag.graph_db.state import (
    InputState,
    OutputState,
    OverallState,
)

# Backward compatibility aliases
GraphDBAgent = GraphDBRAGAgent
"""Alias for backward compatibility. Use GraphDBRAGAgent instead."""

GraphDBAgentConfig = GraphDBRAGConfig
"""Alias for backward compatibility. Use GraphDBRAGConfig instead."""

# Define what should be imported with "from package import *"
__all__ = [
    # Main classes
    "GraphDBRAGAgent",
    "GraphDBRAGConfig",
    "GraphDBConfig",
    "ExampleConfig",
    # State classes
    "InputState",
    "OutputState",
    "OverallState",
    # Model classes
    "CypherQueryOutput",
    "ValidateCypherOutput",
    "GuardrailsOutput",
    "PropertyFilter",
    # Backward compatibility
    "GraphDBAgent",
    "GraphDBAgentConfig",
]

# Package metadata
__version__ = "1.0.0"
__author__ = "Haive Team"
__email__ = "support@haive.ai"
__description__ = "Graph Database RAG Agent for natural language Neo4j querying"

# Module-level docstring for help()
__doc__ = """
Graph Database RAG Agent Package

This package provides tools for querying Neo4j databases using natural language.
It includes automatic Cypher generation, validation, execution, and response
formatting.

Main Components:
    - GraphDBRAGAgent: The main agent class
    - GraphDBRAGConfig: Configuration options
    - State classes: Workflow state management
    - Models: Structured outputs for LLMs

Quick Example:
    >>> from haive.agents.rag.db_rag.graph_db import GraphDBRAGAgent
    >>> agent = GraphDBRAGAgent()
    >>> result = agent.invoke({"question": "Who directed The Matrix?"})
    >>> print(result["answer"])

For detailed documentation, see the individual module docstrings.
"""
