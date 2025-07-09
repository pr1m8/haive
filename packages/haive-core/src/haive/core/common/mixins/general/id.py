"""ID mixin for basic identification capabilities.

This module provides a simple mixin for adding UUID-based identification
to Pydantic models. It's a lightweight alternative to the more comprehensive
IdentifierMixin when only basic ID capabilities are needed.

Usage:
    ```python
    from pydantic import BaseModel
    from haive.core.common.mixins.general import IdMixin

    class MyComponent(IdMixin, BaseModel):
        name: str

        def __init__(self, **data):
            super().__init__(**data)
            # Now the component has a UUID string ID

    # Create with auto-generated ID
    component = MyComponent(name="Test")
    print(component.id)  # UUID string

    # Create with specific ID
    custom_component = MyComponent.with_id("custom-id-123", name="Custom")
    print(custom_component.id)  # "custom-id-123"
    ```
"""

import uuid

from pydantic import BaseModel, Field


class IdMixin(BaseModel):
    """Mixin for adding basic ID generation and management capabilities.

    This mixin adds a UUID-based ID field to any Pydantic model, with
    methods for regenerating the ID and creating instances with specific IDs.

    Attributes:
        id: A UUID string that uniquely identifies the object.
    """

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), description="Unique identifier"
    )

    def regenerate_id(self) -> str:
        """Generate a new UUID and return it.

        This method replaces the current ID with a new UUID.

        Returns:
            The newly generated UUID string.
        """
        self.id = str(uuid.uuid4())
        return self.id

    @classmethod
    def with_id(cls, id_value: str, **kwargs):
        """Create an instance with a specific ID.

        This class method provides a convenient way to create an instance
        with a predetermined ID value.

        Args:
            id_value: The ID value to use.
            **kwargs: Additional attributes for the instance.

        Returns:
            A new instance with the specified ID.
        """
        return cls(id=id_value, **kwargs)
