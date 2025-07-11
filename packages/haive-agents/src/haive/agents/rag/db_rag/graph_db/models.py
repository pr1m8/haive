"""Pydantic models for structured outputs in the Graph DB RAG Agent.

This module defines the structured output models used by various LLM engines
in the Graph DB RAG workflow. These models ensure type safety and validation
for LLM responses.

Example:
    Using the models for structured LLM outputs::

        >>> from haive.agents.rag.db_rag.graph_db.models import CypherQueryOutput
        >>>
        >>> # Create a Cypher query output
        >>> cypher_output = CypherQueryOutput(
        ...     query="MATCH (m:Movie) WHERE m.year = $year RETURN m.title",
        ...     parameters={"year": 2023}
        ... )
        >>> print(cypher_output.query)
        MATCH (m:Movie) WHERE m.year = $year RETURN m.title
"""

from typing import Any, Literal, TypeVar

from pydantic import BaseModel, Field, field_validator

T = TypeVar("T", bound=str)  # Used for dynamic literals


class PropertyFilter(BaseModel):
    """Represents a filter condition on a node property in a Cypher query.

    This model captures property-based filtering conditions that appear in
    WHERE clauses or inline property matches in Cypher queries.

    Attributes:
        node_label: The Neo4j label of the node being filtered (e.g., "Movie", "Person").
        property_key: The property name being filtered (e.g., "title", "year").
        property_value: The value to match against. Can be string, number, or boolean.
        filter_type: The comparison operator used. Defaults to equality.

    Example:
        >>> # Filter for movies released after 2020
        >>> filter = PropertyFilter(
        ...     node_label="Movie",
        ...     property_key="year",
        ...     property_value=2020,
        ...     filter_type=">"
        ... )

        >>> # Filter for person named "Keanu Reeves"
        >>> filter = PropertyFilter(
        ...     node_label="Person",
        ...     property_key="name",
        ...     property_value="Keanu Reeves"
        ... )

    Raises:
        ValueError: If filter_type is not one of the valid operators.
    """

    node_label: str = Field(
        description="The label of the node to which this property belongs"
    )
    property_key: str = Field(description="The key of the property being filtered")
    property_value: Any | None = Field(
        description="The value that the property is being matched against"
    )
    filter_type: Literal["=", "!=", ">", "<", ">=", "<="] | None = Field(
        default="=", description="Type of filter operation used in the Cypher query"
    )

    @field_validator("filter_type", mode="before")
    def validate_filter_type(self, v):
        """Validate that the filter type is a supported operator.

        Args:
            v: The filter type value to validate.

        Returns:
            str: The validated filter type.

        Raises:
            ValueError: If the filter type is not supported.
        """
        valid_types = {"=", "!=", ">", "<", ">=", "<="}
        if v not in valid_types:
            raise ValueError(
                f"Invalid filter type '{v}'. Must be one of: {', '.join(valid_types)}"
            )
        return v


class CypherQueryOutput(BaseModel):
    """Structured output for Cypher query generation.

    This model ensures that generated Cypher queries are properly formatted
    and optionally include parameters for parameterized queries.

    Attributes:
        query: The generated Cypher query string. Must start with a valid
            Cypher keyword (MATCH, CREATE, etc.).
        parameters: Optional dictionary of query parameters for parameterized
            queries. Keys are parameter names (without $), values are the
            parameter values.

    Example:
        >>> # Simple query without parameters
        >>> output = CypherQueryOutput(
        ...     query="MATCH (m:Movie) RETURN m.title LIMIT 10"
        ... )

        >>> # Parameterized query
        >>> output = CypherQueryOutput(
        ...     query="MATCH (m:Movie) WHERE m.year = $year RETURN m.title",
        ...     parameters={"year": 2023}
        ... )

    Raises:
        ValueError: If the query doesn't start with a valid Cypher keyword.
    """

    query: str = Field(..., description="The generated Cypher query")
    parameters: dict[str, Any] | None = Field(
        default=None,
        description="Query parameters if placeholders are used (e.g., $name)",
    )

    @field_validator("query", mode="before")
    def validate_cypher_syntax(self, query: str) -> str:
        """Validate that the query starts with a valid Cypher keyword.

        Args:
            query: The Cypher query string to validate.

        Returns:
            str: The validated query string.

        Raises:
            ValueError: If the query doesn't start with a valid keyword.
        """
        valid_keywords = [
            "MATCH",
            "MERGE",
            "CREATE",
            "RETURN",
            "DELETE",
            "SET",
            "WITH",
            "UNWIND",
        ]
        query_upper = query.strip().upper()

        if not any(query_upper.startswith(kw) for kw in valid_keywords):
            raise ValueError(
                f"Invalid Cypher query. Must start with one of: {', '.join(valid_keywords)}"
            )
        return query


class ValidateCypherOutput(BaseModel):
    """Validation result for a Cypher query.

    This model captures the results of validating a Cypher query against
    the database schema, including any errors found and filters detected.

    Attributes:
        is_valid: Whether the Cypher query is valid and can be executed.
        errors: List of syntax or semantic errors found. Each error should
            explain what's wrong and potentially how to fix it.
        filters: List of property filters detected in the query. Useful for
            understanding what the query is filtering on.

    Example:
        >>> # Valid query result
        >>> result = ValidateCypherOutput(
        ...     is_valid=True,
        ...     errors=[],
        ...     filters=[PropertyFilter(
        ...         node_label="Movie",
        ...         property_key="year",
        ...         property_value=2023
        ...     )]
        ... )

        >>> # Invalid query result
        >>> result = ValidateCypherOutput(
        ...     is_valid=False,
        ...     errors=[
        ...         "Label 'Film' does not exist in schema. Did you mean 'Movie'?",
        ...         "Property 'release_date' does not exist for Movie. Use 'year' instead."
        ...     ]
        ... )
    """

    is_valid: bool = Field(
        default=True, description="Whether the Cypher query is valid"
    )
    errors: list[str] | None = Field(
        default=[],
        description="List of syntax or semantic errors in the Cypher statement",
    )
    filters: list[PropertyFilter] | None = Field(
        default=[],
        description="Property-based filters detected in the Cypher statement",
    )


class GuardrailsOutput(BaseModel):
    """Output for domain relevance checking.

    This model represents the decision on whether a query is relevant to
    the configured domain. It supports multiple categories within a domain.

    Attributes:
        decision: The routing decision. Either "end" (not relevant) or one
            of the allowed categories (relevant to that category).
        allowed_categories: List of valid categories for the domain. The
            "end" option is always implicitly included.

    Example:
        >>> # Query about movies in a movie domain
        >>> output = GuardrailsOutput(
        ...     decision="movie",
        ...     allowed_categories=["movie", "actor", "director"]
        ... )

        >>> # Query not relevant to the domain
        >>> output = GuardrailsOutput(
        ...     decision="end",
        ...     allowed_categories=["movie", "actor", "director"]
        ... )

    Note:
        The validate_decision method should be called after instantiation
        to ensure the decision is valid.
    """

    decision: str = Field(
        description="Routing decision: 'end' or one of the allowed categories"
    )
    allowed_categories: list[str] = Field(
        default=["movie", "sports", "music"],
        description="List of allowed categories for this domain",
    )

    def validate_decision(self) -> None:
        """Validate that the decision is within allowed values.

        Raises:
            ValueError: If the decision is not 'end' or in allowed_categories.

        Example:
            >>> output = GuardrailsOutput(decision="movie")
            >>> output.validate_decision()  # No error

            >>> output = GuardrailsOutput(decision="invalid")
            >>> output.validate_decision()  # Raises ValueError
        """
        valid_values = ["end", *self.allowed_categories]
        if self.decision not in valid_values:
            raise ValueError(
                f"Invalid decision '{self.decision}'. "
                f"Must be one of: {', '.join(valid_values)}"
            )

    class Config:
        """Pydantic model configuration."""

        json_schema_extra = {
            "example": {
                "decision": "movie",
                "allowed_categories": ["movie", "sports", "music"],
            }
        }
