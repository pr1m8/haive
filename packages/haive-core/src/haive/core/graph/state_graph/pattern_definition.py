class PatternDefinition(SerializableModel):
    """Definition of a reusable graph pattern."""

    pattern_type: str = Field(..., description="Type of pattern")
    apply_func: FunctionReference = Field(
        ..., description="Function to apply the pattern"
    )
    parameters: Dict[str, Any] = Field(
        default_factory=dict, description="Default parameter values"
    )
    example: Optional[str] = Field(default=None, description="Example usage")

    __model_type__: ClassVar[str] = "pattern"
    __abstract__ = False

    @classmethod
    def from_function(
        cls, func: Callable, name: str, pattern_type: str, **parameters
    ) -> "PatternDefinition":
        """Create a pattern definition from a function."""
        return cls(
            name=name,
            description=func.__doc__,
            pattern_type=pattern_type,
            apply_func=FunctionReference.from_callable(func, name=name),
            parameters=parameters,
        )
