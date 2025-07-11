"""Configuration module for the Graph Database RAG Agent.

This module provides configuration classes for connecting to Neo4j databases
and configuring the Graph DB RAG Agent with appropriate engines, schemas,
and domain-specific settings.

Example:
    Basic configuration setup::

        >>> from haive.agents.rag.db_rag.graph_db.config import GraphDBRAGConfig
        >>>
        >>> # Create config with default settings
        >>> config = GraphDBRAGConfig(
        ...     domain_name="movies",
        ...     domain_categories=["movie", "actor", "director"]
        ... )
        >>>
        >>> # Create agent with config
        >>> agent = GraphDBRAGAgent(config)

Environment Variables:
    The following environment variables are used for Neo4j connection:

    - NEO4J_URI: The URI of the Neo4j database (e.g., "bolt://localhost:7687")
    - NEO4J_USER: Username for Neo4j authentication
    - NEO4J_PASSWORD: Password for Neo4j authentication
    - NEO4J_DATABASE: Database name (optional, defaults to "neo4j")
"""

import os
from typing import Any

from dotenv import load_dotenv
from haive.core.engine.agent.agent import AgentConfig
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_neo4j import Neo4jGraph
from pydantic import BaseModel, Field, field_validator

from haive.agents.rag.db_rag.graph_db.engines import (
    correct_cypher_aug_llm_config,
    generate_final_aug_llm_config,
    guardrails_aug_llm_config,
    text2cypher_aug_llm_config,
    validate_cypher_aug_llm_config,
)
from haive.agents.rag.db_rag.graph_db.state import InputState, OutputState, OverallState

# Try to load environment variables from .env file if it exists
load_dotenv(".env")


class GraphDBConfig(BaseModel):
    """Configuration for connecting to a Neo4j graph database.

    This class manages Neo4j connection parameters and provides methods
    for establishing connections and retrieving schema information.

    Attributes:
        graph_db_uri: Neo4j connection URI. Defaults to NEO4J_URI env var.
            Format: "bolt://host:port" or "neo4j://host:port"
        graph_db_user: Username for authentication. Defaults to NEO4J_USER env var.
        graph_db_password: Password for authentication. Defaults to NEO4J_PASSWORD env var.
        graph_db_database: Database name. Defaults to NEO4J_DATABASE env var or "neo4j".
        enhanced_schema: Whether to use enhanced schema scanning for better
            property and relationship detection.

    Example:
        >>> # Using environment variables
        >>> db_config = GraphDBConfig()
        >>>
        >>> # Explicit configuration
        >>> db_config = GraphDBConfig(
        ...     graph_db_uri="bolt://localhost:7687",
        ...     graph_db_user="neo4j",
        ...     graph_db_password="password",
        ...     graph_db_database="movies"
        ... )
        >>>
        >>> # Connect to database
        >>> graph = db_config.get_graph_db()
        >>> if graph:
        ...     schema = db_config.get_graph_db_schema()
    """

    graph_db_uri: str = Field(
        default=os.getenv("NEO4J_URI", ""),
        description="The URI of the Neo4j database (e.g., bolt://localhost:7687)",
    )
    graph_db_user: str = Field(
        default=os.getenv("NEO4J_USER", ""),
        description="The username for Neo4j authentication",
    )
    graph_db_password: str = Field(
        default=os.getenv("NEO4J_PASSWORD", ""),
        description="The password for Neo4j authentication",
    )
    graph_db_database: str = Field(
        default=os.getenv("NEO4J_DATABASE", "neo4j"),
        description="The database name in Neo4j (defaults to 'neo4j')",
    )
    enhanced_schema: bool = Field(
        default=True, description="Enable enhanced schema scanning for better detection"
    )

    def get_graph_db(self) -> Neo4jGraph | None:
        """Create and return a Neo4jGraph connection object.

        Establishes a secure connection to the Neo4j database with proper
        timeout, sanitization, and schema refresh settings.

        Returns:
            Neo4jGraph: Connected graph object if successful.
            None: If connection fails.

        Example:
            >>> config = GraphDBConfig()
            >>> graph = config.get_graph_db()
            >>> if graph:
            ...     print("✅ Connected to Neo4j")
            ... else:
            ...     print("❌ Connection failed")
        """
        try:
            graph_db = Neo4jGraph(
                url=self.graph_db_uri,
                username=self.graph_db_user,
                password=self.graph_db_password,
                database=self.graph_db_database,
                timeout=10,
                sanitize=True,
                refresh_schema=True,
                enhanced_schema=self.enhanced_schema,
            )
            return graph_db
        except Exception:
            return None

    def get_graph_db_schema(self) -> dict | None:
        """Retrieve the graph schema from the Neo4j database.

        Gets the complete schema including node labels, relationship types,
        and properties. Uses enhanced schema if enabled for more detailed
        information.

        Returns:
            dict: Schema dictionary with structure:
                {
                    "node_props": {label: [properties]},
                    "rel_props": {type: [properties]},
                    "relationships": [relationship_structures]
                }
            None: If connection fails or schema cannot be retrieved.

        Example:
            >>> config = GraphDBConfig(enhanced_schema=True)
            >>> schema = config.get_graph_db_schema()
            >>> if schema:
            ...     print(f"Node labels: {list(schema['node_props'].keys())}")
            ...     print(f"Relationship types: {list(schema['rel_props'].keys())}")
        """
        graph_db = self.get_graph_db()
        if graph_db:
            return graph_db.get_schema()  # type: ignore
        return None


class ExampleConfig(BaseModel):
    """Configuration for few-shot examples used in Cypher generation.

    This class manages example queries that help the LLM learn the mapping
    between natural language questions and Cypher queries for a specific domain.

    Attributes:
        examples_path: Path to JSON file containing examples. The file should
            contain a list of dicts with "question" and "query" keys.
        examples: Direct list of examples if not using a file. Each example
            should have "question" (natural language) and "query" (Cypher) keys.
        k: Number of examples to retrieve for few-shot prompting. More examples
            can improve accuracy but increase prompt length.

    Example:
        >>> # Using a file
        >>> example_config = ExampleConfig(
        ...     examples_path="examples/movie_queries.json",
        ...     k=3
        ... )
        >>>
        >>> # Using direct examples
        >>> example_config = ExampleConfig(
        ...     examples=[
        ...         {
        ...             "question": "Who directed Inception?",
        ...             "query": "MATCH (p:Person)-[:DIRECTED]->(m:Movie {title: 'Inception'}) RETURN p.name"
        ...         },
        ...         {
        ...             "question": "What movies did Tom Hanks act in?",
        ...             "query": "MATCH (p:Person {name: 'Tom Hanks'})-[:ACTED_IN]->(m:Movie) RETURN m.title"
        ...         }
        ...     ],
        ...     k=2
        ... )
    """

    examples_path: str | None = Field(
        default=None, description="Path to JSON file containing Cypher query examples"
    )
    examples: list[dict[str, str]] | None = Field(
        default=None,
        description="Direct list of examples with 'question' and 'query' keys",
    )
    k: int = Field(
        default=2, description="Number of examples to retrieve for few-shot prompting"
    )


class GraphDBRAGConfig(AgentConfig):
    """Main configuration for the Graph Database RAG Agent.

    This class provides comprehensive configuration for the Graph DB RAG Agent,
    including LLM engines, domain settings, database connection, and schemas.

    Attributes:
        engines: Dictionary of AugLLMConfig engines for different workflow steps:
            - "guardrails": Checks domain relevance
            - "text2cypher": Converts natural language to Cypher
            - "validate_cypher": Validates generated Cypher
            - "correct_cypher": Fixes Cypher errors
            - "generate_final_answer": Creates natural language response
        domain_name: The domain this agent specializes in (e.g., "movies", "healthcare").
            Used for guardrails and example selection.
        domain_categories: Valid categories within the domain for fine-grained routing.
        example_config: Configuration for few-shot examples.
        state_schema: Pydantic model for workflow state management.
        graph_db_config: Neo4j connection configuration.
        input_schema: Schema for agent input validation.
        output_schema: Schema for agent output structure.
        domain_examples: Domain-specific examples for different categories.

    Example:
        >>> # Configure a movie domain agent
        >>> config = GraphDBRAGConfig(
        ...     domain_name="movies",
        ...     domain_categories=["movie", "actor", "director", "genre"],
        ...     example_config=ExampleConfig(
        ...         examples_path="examples/movie_queries.json",
        ...         k=3
        ...     ),
        ...     graph_db_config=GraphDBConfig(
        ...         graph_db_uri="bolt://localhost:7687",
        ...         graph_db_user="neo4j",
        ...         graph_db_password="password"
        ...     )
        ... )
        >>>
        >>> # Create agent
        >>> agent = GraphDBRAGAgent(config)

    Note:
        All required engines must be present in the engines dictionary.
        The validator will check for their presence and raise an error
        if any are missing.
    """

    engines: dict[str, AugLLMConfig] = Field(
        description="LLM engine configurations for each workflow step",
        default={
            "correct_cypher": correct_cypher_aug_llm_config,
            "validate_cypher": validate_cypher_aug_llm_config,
            "text2cypher": text2cypher_aug_llm_config,
            "guardrails": guardrails_aug_llm_config,
            "generate_final_answer": generate_final_aug_llm_config,
        },
    )

    domain_name: str = Field(
        default="general",
        description="Domain specialization (e.g., 'movies', 'healthcare', 'finance')",
    )

    domain_categories: list[str] = Field(
        default_factory=list,
        description="Valid categories for routing within the domain",
    )

    example_config: ExampleConfig | None = Field(
        default=None, description="Configuration for Cypher query examples"
    )

    state_schema: Any = Field(
        default=OverallState, description="Pydantic model for workflow state management"
    )

    graph_db_config: GraphDBConfig = Field(
        default_factory=GraphDBConfig,
        description="Neo4j database connection configuration",
    )

    input_schema: Any = Field(
        default=InputState, description="Schema for validating agent inputs"
    )

    output_schema: Any = Field(
        default=OutputState, description="Schema for structuring agent outputs"
    )

    domain_examples: dict[str, list[dict[str, str]]] = Field(
        default_factory=dict,
        description="Domain-specific example queries for few-shot learning",
    )

    @field_validator("engines")
    def validate_engines(
        self, engines: dict[str, AugLLMConfig]
    ) -> dict[str, AugLLMConfig]:
        """Validate that all required engines are present.

        Checks for the presence of all required engine configurations and
        handles potential naming mismatches (e.g., "generate_cypher" vs "text2cypher").

        Args:
            engines: Dictionary of engine configurations.

        Returns:
            Dict[str, AugLLMConfig]: Validated engines dictionary.

        Raises:
            ValueError: If any required engine is missing.
        """
        required_engines = [
            "correct_cypher",
            "validate_cypher",
            "text2cypher",
            "guardrails",
            "generate_final_answer",
        ]

        for engine_name in required_engines:
            if engine_name not in engines:
                # Handle potential naming mismatch
                if engine_name == "text2cypher" and "generate_cypher" in engines:
                    engines["text2cypher"] = engines["generate_cypher"]
                else:
                    raise ValueError(
                        f"Missing required engine: {engine_name}. "
                        f"Available engines: {list(engines.keys())}"
                    )

        return engines


# For backward compatibility
GraphDBAgentConfig = GraphDBRAGConfig
"""Alias for backward compatibility with older code."""
