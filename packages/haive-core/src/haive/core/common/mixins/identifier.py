"""Identifier mixin for unique identification of objects.

This module provides a mixin class that adds UUID-based identification and
human-readable naming to Pydantic models. The mixin handles validation,
generation, and utility methods for working with identifiers.

Uses Pydantic v2 patterns with field_validator and computed fields.

Usage:
    ```python
    from haive.core.common.mixins.identifier import IdentifierMixin

    class MyComponent(IdentifierMixin, BaseModel):
        # Other fields
        content: str

        def __init__(self, **data):
            super().__init__(**data)
            # Now the component has an ID and optional name

    # Create with auto-generated ID
    component = MyComponent(content="Hello")
    print(component.id)  # UUID string
    print(component.short_id)  # First 8 chars of UUID

    # Create with custom name
    named_component = MyComponent(content="Hello", name="GreetingComponent")
    print(named_component.display_name)  # "GreetingComponent"
    ```
"""

import uuid
from typing import Optional
from uuid import UUID

from pydantic import (
    BaseModel,
    Field,
    PrivateAttr,
    computed_field,
    field_validator,
    model_validator,
)


class IdentifierMixin(BaseModel):
    """Mixin that adds unique identification to any Pydantic model.

    This mixin provides both UUID-based identification and human-readable
    naming capabilities. It automatically generates UUIDs, validates
    provided IDs, and offers convenience methods for working with the
    identifiers.

    Attributes:
        id: A UUID string that uniquely identifies the object.
        name: An optional human-readable name for the object.
        short_id: First 8 characters of the UUID (computed).
        display_name: User-friendly name for display (computed).
        uuid_obj: UUID object representation of the ID (computed).
        has_custom_name: Whether a custom name is set (computed).
    """

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for this object",
    )
    name: Optional[str] = Field(
        default=None, description="Human-readable name for this object"
    )

    # Private attribute for UUID object
    _uuid_obj: Optional[UUID] = PrivateAttr(default=None)

    @field_validator("id")
    @classmethod
    def validate_id(cls, v: str) -> str:
        """Ensure ID is a valid UUID string.

        Args:
            v: The ID string to validate.

        Returns:
            The validated ID string, or a new UUID if invalid.
        """
        try:
            # Validate that it's a proper UUID
            UUID(v)
            return v
        except ValueError:
            # If not valid, generate a new UUID
            return str(uuid.uuid4())

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        """Validate and clean the name field.

        Args:
            v: The name string to validate.

        Returns:
            The cleaned name string, or None if empty after cleaning.
        """
        if v is not None:
            # Strip whitespace and ensure non-empty
            cleaned = v.strip()
            return cleaned if cleaned else None
        return v

    @model_validator(mode="after")
    def initialize_uuid_obj(self) -> "IdentifierMixin":
        """Initialize UUID object after model validation.

        Returns:
            Self, with the _uuid_obj private attribute initialized.
        """
        try:
            self._uuid_obj = UUID(self.id)
        except ValueError:
            # If id is somehow not a valid UUID, regenerate
            self._uuid_obj = uuid.uuid4()
            self.id = str(self._uuid_obj)
        return self

    @computed_field
    @property
    def short_id(self) -> str:
        """Short version of the ID (first 8 characters).

        Returns:
            The first 8 characters of the UUID string.
        """
        return self.id[:8]

    @computed_field
    @property
    def display_name(self) -> str:
        """Display name (uses name if available, otherwise short_id).

        Returns:
            The human-readable name if set, otherwise "Object-{short_id}".
        """
        return self.name or f"Object-{self.short_id}"

    @computed_field
    @property
    def uuid_obj(self) -> UUID:
        """UUID object representation of the ID.

        Returns:
            The UUID object corresponding to the ID string.
        """
        if self._uuid_obj is None:
            self._uuid_obj = UUID(self.id)
        return self._uuid_obj

    @computed_field
    @property
    def has_custom_name(self) -> bool:
        """Whether this object has a custom name (not auto-generated).

        Returns:
            True if a non-empty name is set, False otherwise.
        """
        return self.name is not None and self.name.strip() != ""

    def regenerate_id(self) -> str:
        """Generate a new ID and return it.

        This method creates a new UUID, updates the ID field,
        and returns the new ID string.

        Returns:
            The newly generated UUID string.
        """
        self._uuid_obj = uuid.uuid4()
        self.id = str(self._uuid_obj)
        return self.id

    def set_name(self, name: str) -> None:
        """Set the name with validation.

        Args:
            name: The new name to set.
        """
        if name and name.strip():
            self.name = name.strip()
        else:
            self.name = None

    def clear_name(self) -> None:
        """Clear the name."""
        self.name = None

    def matches_id(self, id_or_name: str) -> bool:
        """Check if this object matches the given ID or name.

        This method checks if the provided string matches this object's
        full ID, short ID, or name (case-insensitive).

        Args:
            id_or_name: The ID or name string to check against.

        Returns:
            True if there's a match, False otherwise.
        """
        if not id_or_name:
            return False

        # Check full ID
        if self.id == id_or_name:
            return True

        # Check short ID
        if self.short_id == id_or_name:
            return True

        # Check name (case-insensitive)
        if self.name and self.name.lower() == id_or_name.lower():
            return True

        return False

    def identifier_info(self) -> dict[str, str]:
        """Get comprehensive identifier information.

        Returns:
            A dictionary containing all identifier-related information.
        """
        return {
            "id": self.id,
            "short_id": self.short_id,
            "name": self.name or "unnamed",
            "display_name": self.display_name,
            "has_custom_name": self.has_custom_name,
        }
