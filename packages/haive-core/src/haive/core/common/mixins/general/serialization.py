"""Serialization mixin for enhanced data conversion capabilities.

This module provides a mixin for adding enhanced serialization and
deserialization capabilities to Pydantic models. It offers methods for
converting models to dictionaries and JSON strings, and for creating models
from dictionaries and JSON strings.

Usage:
    ```python
    from pydantic import BaseModel
    from haive.core.common.mixins.general import SerializationMixin

    class User(SerializationMixin, BaseModel):
        id: str
        name: str
        age: int
        _private_data: str = "hidden"

    # Create a user
    user = User(id="123", name="Alice", age=30)

    # Serialize to dict (excludes _private_data by default)
    user_dict = user.to_dict()

    # Serialize to JSON with indentation
    user_json = user.to_json(indent=2)

    # Deserialize from dict
    new_user = User.from_dict(user_dict)

    # Deserialize from JSON
    new_user = User.from_json(user_json)
    ```
"""

from typing import Any, Dict

from pydantic import BaseModel, Field

from haive.core.common.mixins.general.id import IdMixin
from haive.core.common.mixins.general.metadata import MetadataMixin
from haive.core.common.mixins.general.timestamp import TimestampMixin
from haive.core.common.mixins.general.version import VersionMixin


class SerializationMixin(BaseModel):
    """Mixin for enhanced serialization and deserialization capabilities.

    This mixin provides methods for converting Pydantic models to dictionaries
    and JSON strings, and for creating models from dictionaries and JSON strings.
    It handles private fields (starting with underscore) appropriately.

    When combined with other mixins like IdMixin, TimestampMixin, etc.,
    it provides a complete solution for model persistence.
    """

    def to_dict(self, exclude_private: bool = True) -> dict[str, Any]:
        """Convert to dictionary with options.

        This method converts the model to a dictionary, with the option
        to exclude private fields (those starting with an underscore).

        Args:
            exclude_private: Whether to exclude private fields.

        Returns:
            Dictionary representation of the model.
        """
        exclude_set = set()
        if exclude_private:
            # Exclude private attributes (those starting with _)
            exclude_set.update(
                field_name
                for field_name in self.model_fields
                if field_name.startswith("_")
            )

        return self.model_dump(exclude=exclude_set)

    def to_json(self, exclude_private: bool = True, **kwargs) -> str:
        """Convert to JSON string.

        This method converts the model to a JSON string, with options
        for controlling the JSON serialization.

        Args:
            exclude_private: Whether to exclude private fields.
            **kwargs: Additional arguments to pass to json.dumps().

        Returns:
            JSON string representation of the model.
        """
        data = self.to_dict(exclude_private=exclude_private)
        import json

        return json.dumps(data, default=str, **kwargs)

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        """Create instance from dictionary.

        This class method creates a model instance from a dictionary,
        using Pydantic's validation.

        Args:
            data: Dictionary containing model data.

        Returns:
            New model instance.
        """
        return cls.model_validate(data)

    @classmethod
    def from_json(cls, json_str: str):
        """Create instance from JSON string.

        This class method creates a model instance from a JSON string,
        parsing the JSON and then using from_dict().

        Args:
            json_str: JSON string containing model data.

        Returns:
            New model instance.
        """
        import json

        data = json.loads(json_str)
        return cls.from_dict(data)
