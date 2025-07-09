# src/haive/agents/task_analysis/complexity/models.py

from enum import Enum

from pydantic import BaseModel, Field, field_validator


class ComplexityLevel(str, Enum):
    """Overall complexity classification."""

    TRIVIAL = "trivial"
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    HIGHLY_COMPLEX = "highly_complex"
    EXTREME = "extreme"


class ComplexityVector(BaseModel):
    """Multi-dimensional complexity assessment."""

    # Dimensions (0-10 scale)
    structural: float = Field(
        ..., ge=0, le=10, description="Depth, breadth, and interconnectedness"
    )
    execution: float = Field(
        ..., ge=0, le=10, description="Parallelization and coordination complexity"
    )
    knowledge: float = Field(
        ..., ge=0, le=10, description="Domain expertise requirements"
    )
    integration: float = Field(
        ..., ge=0, le=10, description="System and API integration needs"
    )
    uncertainty: float = Field(
        ..., ge=0, le=10, description="Unknown factors and research needs"
    )

    # Computed fields
    overall_level: ComplexityLevel | None = None
    confidence: float = Field(default=0.8, ge=0, le=1)

    def total_score(self, weights: dict[str, float] | None = None) -> float:
        """Calculate weighted total complexity score."""
        if weights is None:
            weights = {
                "structural": 0.2,
                "execution": 0.2,
                "knowledge": 0.2,
                "integration": 0.2,
                "uncertainty": 0.2,
            }

        score = (
            self.structural * weights.get("structural", 0.2)
            + self.execution * weights.get("execution", 0.2)
            + self.knowledge * weights.get("knowledge", 0.2)
            + self.integration * weights.get("integration", 0.2)
            + self.uncertainty * weights.get("uncertainty", 0.2)
        )

        return round(score, 2)

    def determine_level(self) -> ComplexityLevel:
        """Determine overall complexity level from scores."""
        total = self.total_score()

        if total <= 2:
            return ComplexityLevel.TRIVIAL
        if total <= 3.5:
            return ComplexityLevel.SIMPLE
        if total <= 5:
            return ComplexityLevel.MODERATE
        if total <= 7:
            return ComplexityLevel.COMPLEX
        if total <= 8.5:
            return ComplexityLevel.HIGHLY_COMPLEX
        return ComplexityLevel.EXTREME

    @field_validator(
        "structural", "execution", "knowledge", "integration", "uncertainty"
    )
    def validate_scores(cls, v):
        """Ensure scores are within valid range."""
        return round(v, 1)


class ComplexityFactors(BaseModel):
    """Detailed factors contributing to complexity."""

    # Structural factors
    task_depth: int = Field(..., ge=1, description="Maximum depth of task tree")
    task_breadth: int = Field(..., ge=1, description="Maximum parallel branches")
    total_subtasks: int = Field(..., ge=0, description="Total number of subtasks")
    dependency_density: float = Field(
        ..., ge=0, le=1, description="Ratio of dependencies to tasks"
    )

    # Execution factors
    parallelization_ratio: float = Field(
        ..., ge=0, le=1, description="Ratio of parallelizable tasks"
    )
    join_complexity: int = Field(..., ge=0, description="Number of complex join points")
    coordination_points: int = Field(
        ..., ge=0, description="Number of coordination needs"
    )

    # Knowledge factors
    domain_count: int = Field(..., ge=1, description="Number of knowledge domains")
    expertise_level: str = Field(..., description="Required expertise level")
    learning_curve: str = Field(
        default="moderate", description="Steepness of learning curve"
    )

    # Integration factors
    external_systems: int = Field(..., ge=0, description="Number of external systems")
    api_complexity: str = Field(
        default="simple", description="API integration complexity"
    )
    data_transformations: int = Field(
        ..., ge=0, description="Number of data transformations"
    )

    # Uncertainty factors
    unknown_requirements: int = Field(
        ..., ge=0, description="Number of unclear requirements"
    )
    research_components: int = Field(..., ge=0, description="Number of research tasks")
    solution_confidence: float = Field(
        ..., ge=0, le=1, description="Confidence in solution approach"
    )


class ComplexityAnalysis(BaseModel):
    """Complete complexity analysis result."""

    # Core assessment
    complexity_vector: ComplexityVector
    complexity_factors: ComplexityFactors

    # Risk assessment
    risk_factors: list[str] = Field(default_factory=list)
    mitigation_strategies: list[str] = Field(default_factory=list)

    # Recommendations
    recommendations: list[str] = Field(default_factory=list)
    simplification_opportunities: list[str] = Field(default_factory=list)

    # Confidence
    analysis_confidence: float = Field(default=0.8, ge=0, le=1)
    confidence_factors: dict[str, float] = Field(default_factory=dict)
