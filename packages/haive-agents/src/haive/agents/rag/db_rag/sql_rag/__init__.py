"""SQL RAG Agent Package.

This package provides a sophisticated SQL Retrieval-Augmented Generation (RAG) agent
that enables natural language querying of SQL databases. The agent converts user
questions into SQL queries, executes them safely, and returns natural language answers.

Key Features:
    - Natural language to SQL conversion
    - Multi-dialect support (PostgreSQL, MySQL, SQLite, MS SQL)
    - Query validation and correction
    - Hallucination detection
    - Answer quality grading
    - Comprehensive error handling

Quick Start:
    Basic usage::

        >>> from haive.agents.rag.db_rag.sql_rag import SQLRAGAgent, SQLRAGConfig
        >>>
        >>> # Configure agent
        >>> config = SQLRAGConfig(
        ...     domain_name="sales",
        ...     db_config={"db_uri": "sqlite:///sales.db"}
        ... )
        >>>
        >>> # Create and use agent
        >>> agent = SQLRAGAgent(config)
        >>> result = agent.invoke({"question": "What are total sales by region?"})
        >>> print(result["answer"])

Package Structure:
    - agent.py: Main SQLRAGAgent implementation
    - config.py: Configuration classes (SQLRAGConfig, SQLDatabaseConfig)
    - models.py: Pydantic models for structured outputs
    - state.py: State schemas for workflow management
    - prompts.py: LLM prompt templates
    - engines.py: Pre-configured LLM engines
    - utils.py: Helper utilities

Exports:
    - SQLRAGAgent: Main agent class
    - SQLRAGConfig: Agent configuration
    - SQLDatabaseConfig: Database configuration
    - SQLDatabaseAgent: Backward compatibility alias

Example:
    Advanced configuration::

        >>> from haive.agents.rag.db_rag.sql_rag import (
        ...     SQLRAGAgent,
        ...     SQLRAGConfig,
        ...     SQLDatabaseConfig
        ... )
        >>>
        >>> # Database configuration with specific tables
        >>> db_config = SQLDatabaseConfig(
        ...     db_type="postgresql",
        ...     db_host="analytics.company.com",
        ...     db_name="analytics",
        ...     db_user="analyst",
        ...     db_password="secure_pass",
        ...     include_tables=["sales", "customers", "products"],
        ...     sample_rows_in_table_info=5
        ... )
        >>>
        >>> # Agent configuration with custom settings
        >>> agent_config = SQLRAGConfig(
        ...     domain_name="analytics",
        ...     domain_categories=["sales", "customers", "inventory"],
        ...     db_config=db_config,
        ...     hallucination_check=True,
        ...     answer_grading=True,
        ...     max_iterations=3,
        ...     domain_examples={
        ...         "analytics": [
        ...             {
        ...                 "question": "Top customers by revenue",
        ...                 "query": "SELECT c.name, SUM(s.amount) as revenue FROM customers c JOIN sales s ON c.id = s.customer_id GROUP BY c.id ORDER BY revenue DESC LIMIT 10"
        ...             }
        ...         ]
        ...     }
        ... )
        >>>
        >>> # Create agent
        >>> agent = SQLRAGAgent(agent_config)
        >>>
        >>> # Complex query
        >>> result = agent.invoke({
        ...     "question": "Show me customers who haven't ordered in the last 90 days"
        ... })

Environment Variables:
    The package supports configuration through environment variables:

    - SQL_DB_TYPE: Database type (default: postgresql)
    - SQL_DB_HOST: Database host (default: localhost)
    - SQL_DB_PORT: Database port (default: 5432)
    - SQL_DB_NAME: Database name (default: postgres)
    - SQL_DB_USER: Database username (default: postgres)
    - SQL_DB_PASSWORD: Database password (default: postgres)
    - SQL_INCLUDE_TABLES: Comma-separated list of tables to include
    - SQL_EXCLUDE_TABLES: Comma-separated list of tables to exclude

See Also:
    - Documentation: https://docs.haive.ai/agents/sql-rag
    - Examples: https://github.com/haive/examples/sql-rag
    - API Reference: https://api.haive.ai/sql-rag
"""

from haive.agents.rag.db_rag.sql_rag.agent import SQLRAGAgent
from haive.agents.rag.db_rag.sql_rag.config import SQLDatabaseConfig, SQLRAGConfig

# For backward compatibility - some users might expect SQLDatabaseAgent
SQLDatabaseAgent = SQLRAGAgent

__all__ = [
    "SQLDatabaseAgent",  # Backward compatibility
    "SQLDatabaseConfig",
    "SQLRAGAgent",
    "SQLRAGConfig",
]

__version__ = "1.0.0"
__author__ = "Haive Team"
__email__ = "support@haive.ai"
