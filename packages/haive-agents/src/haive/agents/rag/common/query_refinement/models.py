# ============================================================================
# QUERY REFINEMENT MODELS
# ============================================================================


from pydantic import BaseModel, Field


class QueryRefinementSuggestion(BaseModel):
    """Individual query refinement suggestion."""

    refined_query: str = Field(description="The refined/improved query")
    improvement_type: str = Field(
        description="Type of improvement made (clarity, specificity, scope, etc.)"
    )
    rationale: str = Field(description="Why this refinement improves the query")
    expected_benefit: str = Field(
        description="Expected improvement in retrieval or answering"
    )


class QueryRefinementResponse(BaseModel):
    """Query refinement analysis and suggestions."""

    original_query: str = Field(description="The original user query")
    query_analysis: str = Field(
        description="Analysis of the original query's strengths and weaknesses"
    )
    query_type: str = Field(description="Classification of query type")
    complexity_level: str = Field(description="simple, moderate, or complex")
    refinement_suggestions: list[QueryRefinementSuggestion] = Field(
        description="List of suggested query improvements"
    )
    best_refined_query: str = Field(description="The recommended best refined query")
    search_strategy_recommendations: list[str] = Field(
        description="Recommendations for search strategy"
    )
