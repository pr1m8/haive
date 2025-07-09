from collections.abc import Callable
from typing import Any

from pydantic import BaseModel, Field

from haive.core.graph.routers.conditions import RouteCondition


class RoutingConfig(BaseModel):
    """Configuration for node routing behavior."""

    default_destination: str = Field(
        ..., description="Default destination if no other routing applies"
    )
    condition_map: dict[Any, str] = Field(
        default_factory=dict, description="Map of condition values to destinations"
    )
    condition_function: Callable[[dict[str, Any]], Any] | None = Field(
        default=None, description="Function that determines routing"
    )
    allowed_destinations: list[str] = Field(
        default_factory=list,
        description="List of allowed destinations (for validation)",
    )
    is_dynamic: bool = Field(
        default=False, description="Whether routing is determined at runtime"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional routing metadata"
    )


class Route(BaseModel):
    """Defines a routing path with conditions."""

    name: str = Field(..., description="Name of the route")
    condition: RouteCondition = Field(
        ..., description="Condition that triggers this route"
    )
    destination: str = Field(..., description="Destination node or END")
    description: str | None = Field(
        default=None, description="Description of the route"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )
