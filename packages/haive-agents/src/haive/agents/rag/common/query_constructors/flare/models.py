# ============================================================================
# FLARE MODELS
# ============================================================================


from pydantic import BaseModel, Field


class FLAREStep(BaseModel):
    """Individual step in FLARE generation."""

    step_number: int = Field(description="Step number in the FLARE process")
    generated_content: str = Field(description="Content generated in this step")
    confidence_level: str = Field(description="HIGH, MEDIUM, or LOW confidence")
    information_needs: list[str] = Field(
        default_factory=list, description="Additional information needed to continue"
    )
    search_queries: list[str] = Field(
        default_factory=list,
        description="Specific search queries for missing information",
    )
    uncertainties: list[str] = Field(
        default_factory=list, description="Areas of uncertainty that need clarification"
    )


class FLAREResponse(BaseModel):
    """FLARE (Forward-Looking Active Retrieval) response."""

    original_query: str = Field(description="The original user query")
    generation_steps: list[FLAREStep] = Field(
        description="Steps in the FLARE generation process"
    )
    final_answer: str = Field(description="Complete answer after all iterations")
    retrieval_requests: list[str] = Field(
        description="All retrieval requests made during generation"
    )
    confidence_assessment: str = Field(
        description="Overall confidence in the final answer"
    )
    remaining_uncertainties: list[str] = Field(
        default_factory=list, description="Uncertainties that could not be resolved"
    )
