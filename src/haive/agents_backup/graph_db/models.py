from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Literal, TypeVar, Tuple, Dict, Any

T = TypeVar("T", bound=str)  # Used for dynamic literals


class PropertyFilter(BaseModel):
    """
    Represents a filter condition based on a specific node property in a Cypher query.
    """

    node_label: str = Field(description="The label of the node to which this property belongs.")
    property_key: str = Field(description="The key of the property being filtered.")
    property_value: Optional[Any] = Field(
        description="The value that the property is being matched against. Can be a string, number, or boolean."
    )
    filter_type: Optional[Literal["=", "!=", ">", "<", ">=", "<="]] = Field(
        default="=", description="Type of filter operation used in the Cypher query."
    )

    @field_validator("filter_type", mode="before")  # Fix for Pydantic v2
    def validate_filter_type(cls, v):
        if v not in {"=", "!=", ">", "<", ">=", "<="}:
            raise ValueError(f"Invalid filter type '{v}'. Must be one of '=', '!=', '>', '<', '>=', '<='. ")
        return v


class CypherQueryOutput(BaseModel):
    """Validated structured output model for Cypher query generation."""

    query: str = Field(..., description="The generated Cypher query.")
    parameters: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Query parameters if placeholders are used (e.g., $name)."
    )

    @field_validator("query", mode="before")  # Fix for Pydantic v2
    def validate_cypher_syntax(cls, query: str) -> str:
        """Ensure the query starts with a valid Cypher keyword."""
        valid_keywords = ["MATCH", "MERGE", "CREATE", "RETURN", "DELETE", "SET", "WITH", "UNWIND"]
        if not any(query.strip().upper().startswith(kw) for kw in valid_keywords):
            raise ValueError("Invalid Cypher query. Must start with a valid Cypher keyword.")
        return query


class ValidateCypherOutput(BaseModel):
    """
    Represents the validation result of a Cypher query's output,
    including any errors and applied filters.
    """

    errors: Optional[List[str]] = Field(
        default=[],
        description="List of syntax or semantic errors in the Cypher statement. "
                    "Always explain the discrepancy between the schema and the Cypher statement."
    )
    filters: Optional[List[PropertyFilter]] = Field(
        default=[],
        description="A list of property-based filters applied in the Cypher statement."
    )


class GuardrailsOutput(BaseModel):
    """
    Represents the decision on whether a given query falls into predefined categories.
    This model ensures the output is JSON serializable.
    """

    decision: str = Field(
        description="Decision on the category of the input. "
                    "Must be 'end' or one of the allowed categories."
    )
    allowed_categories: List[str] = Field(
        default=["movie", "sports", "music"],
        description="List of dynamically allowed categories. 'end' is always included."
    )

    def validate_decision(self):
        """Ensures the decision is within the allowed values."""
        if self.decision not in ["end"] + self.allowed_categories:
            raise ValueError(
                f"Invalid decision '{self.decision}'. Must be one of: {['end'] + self.allowed_categories}"
            )

    class Config:
        json_schema_extra= {
            "example": {
                "decision": "movie",
                "allowed_categories": ["movie", "sports", "music"]
            }
        }
