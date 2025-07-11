class PerformanceMetrics(BaseModel):
    """Detailed performance tracking for episodic memories."""

    success_rate: float = Field(
        default=0.0, ge=0.0, le=1.0, description="Task success rate"
    )
    completion_time: float = Field(
        default=0.0, ge=0.0, description="Average completion time in seconds"
    )
    user_satisfaction: Optional[float] = Field(
        None, ge=1.0, le=5.0, description="User satisfaction score (1-5)"
    )
    complexity_score: int = Field(
        default=1, ge=1, le=10, description="Task complexity (1-10)"
    )
    error_frequency: float = Field(
        default=0.0, ge=0.0, le=1.0, description="Error rate"
    )

    @model_validator(mode="after")
    def validate_performance_logic(self) -> "PerformanceMetrics":
        """Validate performance metric consistency."""
        if self.success_rate > 0.9 and self.error_frequency > 0.1:
            raise ValueError("High success rate inconsistent with high error frequency")

        return self


class TaskExecution(BaseModel):
    """Detailed task execution context."""

    task_type: str = Field(..., description="Type of task executed")
    input_parameters: Dict[str, Any] = Field(
        default_factory=dict, description="Task input parameters"
    )
    execution_steps: List[str] = Field(
        default_factory=list, description="Step-by-step execution log"
    )
    tools_used: List[str] = Field(
        default_factory=list, description="Tools utilized during execution"
    )
    decision_points: List[Dict[str, Any]] = Field(
        default_factory=list, description="Key decision points"
    )

    @field_validator("execution_steps")
    @classmethod
    def validate_execution_steps(cls, v: List[str]) -> List[str]:
        """Validate execution step format."""
        if len(v) > 100:
            raise ValueError("Too many execution steps (max 100)")

        return [step.strip() for step in v if step.strip()]
