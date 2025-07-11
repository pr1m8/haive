# src/haive/core/graph/graph_mixin.py

from typing import Any, Dict, Generic, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from haive.core.graph.common.types import C, T


class GraphSchemaMixin(BaseModel, Generic[T, C]):
    """Mixin for schema management in graphs.

    This mixin provides functionality for managing state, input, and output schemas
    in graph objects.
    """

    state_schema: T = Field(description="Schema for graph state")
    input_schema: T = Field(description="Schema for graph inputs")
    output_schema: T = Field(description="Schema for graph outputs")
    config_schema: C = Field(
        default=None, description="Optional schema for graph configuration"
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @model_validator(mode="before")
    @classmethod
    def validate_schema_setup(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Validate schema relationships and set defaults.

        Args:
            data: Dictionary of values being validated

        Returns:
            Validated values dictionary
        """
        # Create a copy to avoid modifying the input
        values = data.copy() if isinstance(data, dict) else {"__root__": data}

        # Case 1: state_schema is provided, derive input/output if needed
        if "state_schema" in values and values["state_schema"] is not None:
            state_schema = values["state_schema"]
            # Use state_schema for input if not provided
            if "input_schema" not in values or values["input_schema"] is None:
                values["input_schema"] = state_schema
            # Use state_schema for output if not provided
            if "output_schema" not in values or values["output_schema"] is None:
                values["output_schema"] = state_schema
        # Case 2: input_schema and output_schema are provided, derive state_schema
        elif (
            "input_schema" in values
            and values["input_schema"] is not None
            and "output_schema" in values
            and values["output_schema"] is not None
        ):
            # If input and output schemas are provided but state isn't, create a pass-through state schema
            if "state_schema" not in values or values["state_schema"] is None:

                class PassThroughState(BaseModel):
                    model_config = ConfigDict(arbitrary_types_allowed=True)

                values["state_schema"] = PassThroughState

        # Ensure we have schemas
        if "state_schema" not in values or values["state_schema"] is None:
            raise ValueError("state_schema must be provided")
        if "input_schema" not in values or values["input_schema"] is None:
            raise ValueError("input_schema must be provided")
        if "output_schema" not in values or values["output_schema"] is None:
            raise ValueError("output_schema must be provided")

        return values

    def validate_input(self, data: Any) -> Any:
        """Validate input data against input schema.

        Args:
            data: Input data

        Returns:
            Validated input data
        """
        return self.input_schema.model_validate(data)

    def validate_output(self, data: Any) -> Any:
        """Validate output data against output schema.

        Args:
            data: Output data

        Returns:
            Validated output data
        """
        return self.output_schema.model_validate(data)

    def create_state(self, data: Any | None = None) -> Any:
        """Create a state instance based on state schema.

        Args:
            data: Optional initial data

        Returns:
            State instance
        """
        if data is None:
            return self.state_schema()
        return self.state_schema.model_validate(data)
