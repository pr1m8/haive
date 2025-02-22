from typing import List, Literal, Type
from pydantic import BaseModel, Field, model_validator

class BaseOutputSchema(BaseModel):
    """Base output schema with dynamic routing options and validation."""

    message: str = Field(..., description="Primary message content.")
    next_step: str = Field(..., description="Next step suggested by the agent.")
    available_routes: List[str] = Field(default=[], description="List of valid routing options.")

    @model_validator(mode="after")
    def validate_routing(cls, values):
        """
        Ensures both 'next_step' exists and is in 'available_routes'.
        """
        available_routes = values.available_routes
        next_step = values.next_step

        if not available_routes:
            raise ValueError("available_routes cannot be empty.")
        
        if next_step not in available_routes:
            raise ValueError(f"Invalid next_step '{next_step}'. Must be one of: {available_routes}")

        return values

    def add_route(self, new_route: str):
        """Dynamically add a new route and regenerate the schema."""
        if not isinstance(new_route, str) or not new_route.strip():
            raise ValueError("New route must be a non-empty string.")
        if new_route in self.available_routes:
            raise ValueError(f"Route '{new_route}' already exists.")
        
        self.available_routes.append(new_route)

    def get_dynamic_schema(self) -> Type[BaseModel]:
        """Generate a schema with Literal choices dynamically."""
        dynamic_routes = Literal[*self.available_routes]  # Dynamically enforce available routes

        class DynamicRoutingSchema(self.__class__):
            """Dynamically generated schema based on available_routes."""
            next_step: dynamic_routes = Field(..., description="Select one of the available routes.")

        return DynamicRoutingSchema

