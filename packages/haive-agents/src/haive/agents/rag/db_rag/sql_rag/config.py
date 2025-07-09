"""Configuration module for SQL RAG Agent.

This module provides configuration classes for setting up SQL database connections
and agent behavior. It supports multiple database types and includes extensive
customization options for the agent workflow.

Example:
    Basic PostgreSQL configuration::

        >>> from haive.agents.rag.db_rag.sql_rag.config import SQLRAGConfig, SQLDatabaseConfig
        >>>
        >>> # Configure database connection
        >>> db_config = SQLDatabaseConfig(
        ...     db_type="postgresql",
        ...     db_host="localhost",
        ...     db_name="sales_db",
        ...     db_user="admin",
        ...     db_password="secure_password",
        ...     include_tables=["orders", "customers", "products"]
        ... )
        >>>
        >>> # Configure agent
        >>> agent_config = SQLRAGConfig(
        ...     domain_name="sales",
        ...     db_config=db_config,
        ...     hallucination_check=True,
        ...     max_iterations=3
        ... )

Note:
    Database credentials can be provided through environment variables
    for security. See SQLDatabaseConfig for supported variables.
"""

import inspect
import os
from typing import Any

from dotenv import load_dotenv
from haive.core.engine.agent.agent import AgentConfig
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from langchain_community.utilities import SQLDatabase
from pydantic import BaseModel, Field, field_validator

from haive.agents.rag.db_rag.sql_rag.engines import default_sql_engines
from haive.agents.rag.db_rag.sql_rag.state import InputState, OutputState, OverallState

load_dotenv(".env")


class SQLDatabaseConfig(BaseModel):
    """Configuration for SQL database connections.

    This class handles connection details for various SQL database types
    including PostgreSQL, MySQL, SQLite, and MS SQL Server. Credentials
    can be provided directly or through environment variables.

    Attributes:
        db_type (str): Database type - postgresql, mysql, sqlite, mssql.
        db_uri (Optional[str]): Complete connection URI if provided directly.
        db_user (str): Database username (env: SQL_DB_USER).
        db_password (str): Database password (env: SQL_DB_PASSWORD).
        db_host (str): Database host (env: SQL_DB_HOST).
        db_port (str): Database port (env: SQL_DB_PORT).
        db_name (str): Database name (env: SQL_DB_NAME).
        include_tables (Optional[List[str]]): Tables to include (None = all).
        exclude_tables (List[str]): Tables to exclude from queries.
        sample_rows_in_table_info (int): Sample rows to show in schema.
        custom_query (Optional[str]): Custom query for schema retrieval.

    Example:
        Using environment variables::

            >>> # Set environment variables:
            >>> # SQL_DB_TYPE=postgresql
            >>> # SQL_DB_HOST=localhost
            >>> # SQL_DB_NAME=mydb
            >>> # SQL_DB_USER=user
            >>> # SQL_DB_PASSWORD=pass
            >>>
            >>> config = SQLDatabaseConfig()
            >>> db = config.get_sql_db()
            ✅ Connected to postgresql database

        Direct configuration::

            >>> config = SQLDatabaseConfig(
            ...     db_type="mysql",
            ...     db_host="mysql.example.com",
            ...     db_port="3306",
            ...     db_name="analytics",
            ...     db_user="analyst",
            ...     db_password="secure_pass",
            ...     include_tables=["sales", "customers"]
            ... )

        Using connection URI::

            >>> config = SQLDatabaseConfig(
            ...     db_uri="sqlite:///path/to/database.db"
            ... )

    Note:
        For SQLite databases, db_name should be the file path.
        For other databases, ensure the appropriate driver is installed:
        - PostgreSQL: psycopg2
        - MySQL: pymysql
        - MS SQL: pyodbc
    """

    db_type: str = Field(
        default=os.getenv("SQL_DB_TYPE", "postgresql"),
        description="Type of SQL database (postgresql, mysql, sqlite, etc.)",
    )
    db_uri: str | None = Field(
        default=None, description="The database connection URI (if provided directly)"
    )
    db_user: str = Field(
        default=os.getenv("SQL_DB_USER", "postgres"),
        description="The database username",
    )
    db_password: str = Field(
        default=os.getenv("SQL_DB_PASSWORD", "postgres"),
        description="The database password",
    )
    db_host: str = Field(
        default=os.getenv("SQL_DB_HOST", "localhost"), description="The database host"
    )
    db_port: str = Field(
        default=os.getenv("SQL_DB_PORT", "5432"), description="The database port"
    )
    db_name: str = Field(
        default=os.getenv("SQL_DB_NAME", "postgres"), description="The database name"
    )
    include_tables: list[str] | None = Field(
        default_factory=lambda: (
            os.getenv("SQL_INCLUDE_TABLES", "").split(",")
            if os.getenv("SQL_INCLUDE_TABLES")
            else None
        ),
        description="Specific tables to include, if None then include all",
    )
    exclude_tables: list[str] = Field(
        default_factory=lambda: (
            os.getenv("SQL_EXCLUDE_TABLES", "").split(",")
            if os.getenv("SQL_EXCLUDE_TABLES")
            else []
        ),
        description="Tables to exclude from schema",
    )
    sample_rows_in_table_info: int = Field(
        default=3, description="Number of sample rows to include in table info"
    )
    custom_query: str | None = Field(
        default=None, description="Custom query to execute for schema info"
    )

    def get_connection_string(self) -> str:
        """Generate a connection string based on the database type.

        Returns:
            str: Properly formatted connection string for the database.

        Raises:
            ValueError: If the database type is not supported.

        Example:
            >>> config = SQLDatabaseConfig(
            ...     db_type="postgresql",
            ...     db_user="user",
            ...     db_password="pass",
            ...     db_host="localhost",
            ...     db_port="5432",
            ...     db_name="mydb"
            ... )
            >>> print(config.get_connection_string())
            'postgresql+psycopg2://user:pass@localhost:5432/mydb'
        """
        if self.db_uri:
            return self.db_uri

        if self.db_type == "postgresql":
            return f"postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        if self.db_type == "mysql":
            return f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        if self.db_type == "sqlite":
            # For SQLite, the db_name is the path to the file
            return f"sqlite:///{self.db_name}"
        if self.db_type == "mssql":
            return f"mssql+pyodbc://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        raise ValueError(f"Unsupported database type: {self.db_type}")

    def get_sql_db(self) -> SQLDatabase | None:
        """Create and return a SQLDatabase object for interacting with the database.

        Returns:
            Optional[SQLDatabase]: Connected database object or None if connection fails.

        Example:
            >>> config = SQLDatabaseConfig(db_uri="sqlite:///test.db")
            >>> db = config.get_sql_db()
            ✅ Connected to sqlite database at sqlite:///test.db
            >>> tables = db.get_usable_table_names()
            >>> print(f"Found {len(tables)} tables")
            Found 5 tables

        Note:
            The method handles backward compatibility for different versions
            of langchain_community.utilities.SQLDatabase.
        """
        try:
            connection_string = self.get_connection_string()

            # Create kwargs dictionary with only the parameters that are supported
            db_kwargs = {
                "include_tables": self.include_tables,
                "sample_rows_in_table_info": self.sample_rows_in_table_info,
            }

            # Older versions might not support exclude_tables
            # Check if the class accepts this parameter first
            sig = inspect.signature(SQLDatabase.from_uri)
            if "exclude_tables" in sig.parameters:
                db_kwargs["exclude_tables"] = self.exclude_tables

            db = SQLDatabase.from_uri(connection_string, **db_kwargs)
            print(f"✅ Connected to {self.db_type} database at {connection_string}")
            return db
        except Exception as e:
            print(f"🚨 Failed to connect to database: {e}")
            return None

    def get_db_schema(self) -> dict[str, Any]:
        """Retrieve the schema and basic table info from the database.

        Returns:
            Dict[str, Any]: Dictionary containing:
                - tables: List of table names
                - dialect: SQL dialect being used
                - table_info: Dictionary of table schemas

        Example:
            >>> config = SQLDatabaseConfig(db_uri="sqlite:///sales.db")
            >>> schema = config.get_db_schema()
            >>> print(f"Database dialect: {schema['dialect']}")
            Database dialect: sqlite
            >>> print(f"Tables: {', '.join(schema['tables'])}")
            Tables: customers, orders, products
        """
        db = self.get_sql_db()
        if not db:
            return {"tables": [], "dialect": "unknown"}

        schema = {
            "tables": db.get_usable_table_names(),
            "dialect": str(db.dialect),
            "table_info": {},
        }

        for table in schema["tables"]:
            schema["table_info"][table] = db.get_table_info([table])

        return schema


class SQLRAGConfig(AgentConfig):
    """Configuration for the SQL RAG Agent.

    This class configures the behavior of the SQL RAG agent including
    database connection, LLM engines, validation settings, and workflow
    parameters.

    Attributes:
        engines (Dict[str, AugLLMConfig]): LLM engines for each workflow step.
        llm_config (LLMConfig): Default LLM configuration.
        domain_name (str): Domain specialization (e.g., "sales", "inventory").
        domain_categories (List[str]): Valid categories for domain routing.
        state_schema (Any): State schema class for the agent.
        db_config (SQLDatabaseConfig): Database connection configuration.
        input_schema (Any): Input schema for agent invocation.
        output_schema (Any): Output schema for agent results.
        hallucination_check (bool): Enable hallucination detection.
        answer_grading (bool): Enable answer quality grading.
        examples_path (Optional[str]): Path to few-shot examples JSON.
        domain_examples (Dict[str, List[Dict[str, str]]]): Few-shot examples.
        max_iterations (int): Maximum SQL correction attempts.

    Example:
        Complete configuration example::

            >>> config = SQLRAGConfig(
            ...     domain_name="e-commerce",
            ...     domain_categories=["sales", "inventory", "customers"],
            ...     db_config=SQLDatabaseConfig(
            ...         db_type="postgresql",
            ...         db_name="ecommerce_db",
            ...         include_tables=["orders", "products", "customers"]
            ...     ),
            ...     hallucination_check=True,
            ...     answer_grading=True,
            ...     max_iterations=3,
            ...     domain_examples={
            ...         "e-commerce": [
            ...             {
            ...                 "question": "Top selling products",
            ...                 "query": "SELECT p.name, SUM(oi.quantity) as sold FROM products p JOIN order_items oi ON p.id = oi.product_id GROUP BY p.id ORDER BY sold DESC LIMIT 10"
            ...             }
            ...         ]
            ...     }
            ... )

        Using custom engines::

            >>> from haive.core.engine.aug_llm import AugLLMConfig
            >>>
            >>> custom_engines = {
            ...     "generate_sql": AugLLMConfig(
            ...         name="custom_sql_generator",
            ...         temperature=0.1,  # Lower temperature for SQL
            ...         model="gpt-4"
            ...     ),
            ...     **default_sql_engines  # Keep other defaults
            >>> }
            >>>
            >>> config = SQLRAGConfig(
            ...     engines=custom_engines,
            ...     domain_name="analytics"
            ... )

    Raises:
        ValueError: If required engines are missing from configuration.
    """

    engines: dict[str, AugLLMConfig] = Field(
        description="The LLM runnable configs for the SQL database agent",
        default=default_sql_engines,
    )

    llm_config: LLMConfig = Field(
        default_factory=AzureLLMConfig,
        description="The LLM config for the SQL database agent",
    )

    domain_name: str = Field(
        default="database",
        description="The domain name the agent is specialized for (e.g., 'SQL database', 'database records', etc.)",
    )

    domain_categories: list[str] = Field(
        default=["database"],
        description="Valid categories for the guardrails to recognize, in addition to 'end'",
    )

    state_schema: Any = Field(
        default=OverallState, description="The state schema for the SQL database agent"
    )

    db_config: SQLDatabaseConfig = Field(
        default_factory=SQLDatabaseConfig,
        description="The database config for the SQL database agent",
    )

    input_schema: Any = Field(
        default=InputState, description="The input schema for the SQL database agent"
    )

    output_schema: Any = Field(
        default=OutputState, description="The output schema for the SQL database agent"
    )

    hallucination_check: bool = Field(
        default=True, description="Whether to check for hallucinations in the response"
    )

    answer_grading: bool = Field(
        default=True,
        description="Whether to grade the answer for relevance to the question",
    )

    examples_path: str | None = Field(
        default=None, description="Path to examples JSON file"
    )

    domain_examples: dict[str, list[dict[str, str]]] = Field(
        default_factory=dict,
        description="Examples for different domains to guide the model",
    )

    max_iterations: int = Field(
        default=5, description="Maximum number of iterations for retrying SQL queries"
    )

    @field_validator("engines")
    def check_required_engines(
        cls, v: dict[str, AugLLMConfig]
    ) -> dict[str, AugLLMConfig]:
        """Validate that all required engines are present.

        Args:
            v: Dictionary of engine configurations.

        Returns:
            Dict[str, AugLLMConfig]: Validated engine configurations.

        Raises:
            ValueError: If any required engines are missing.
        """
        required_engines = [
            "analyze_query",
            "validate_sql",
            "generate_sql",
            "guardrails",
            "generate_final_answer",
        ]
        missing = [
            engine
            for engine in required_engines
            if engine not in v or v[engine] is None
        ]
        if missing:
            raise ValueError(f"Missing required engines: {', '.join(missing)}")
        return v


# For backward compatibility
SQLAgentConfig = SQLRAGConfig
