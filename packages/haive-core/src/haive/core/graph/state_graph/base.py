from datetime import datetime
from typing import ClassVar, Dict, List, Optional, Type, TypeVar
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr

from haive.core.registry.base import AbstractRegistry

T = TypeVar("T")


class SerializableModelMetaclass(type(BaseModel)):
    """Metaclass for serializable models to register them with a registry."""

    def __new__(mcs, name, bases, namespace, **kwargs):
        cls = super().__new__(mcs, name, bases, namespace, **kwargs)

        # Register the model if it has a registry defined and is not an abstract base
        if (
            hasattr(cls, "_registry")
            and cls._registry is not None
            and not getattr(cls, "__abstract__", False)
        ):
            # Initialize the registry mapping if it doesn't exist
            if not hasattr(cls, "_registry_mapping"):
                cls._registry_mapping = {}

            # Register the model class
            model_type = namespace.get("__model_type__", name.lower())
            cls._registry_mapping[model_type] = cls

        return cls


class SerializableModel(BaseModel, metaclass=SerializableModelMetaclass):
    """Base class for all serializable models with registry support."""

    id: str = Field(
        default_factory=lambda: str(uuid4()), description="Unique identifier"
    )
    name: str = Field(..., description="Name of the model")
    description: str | None = Field(default=None, description="Optional description")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, description="Last update timestamp"
    )

    # Class variables
    _registry: ClassVar[AbstractRegistry | None] = None
    _registry_mapping: ClassVar[dict[str, type["SerializableModel"]]] = {}
    __abstract__: ClassVar[bool] = True

    # Private attributes
    _modified: bool = PrivateAttr(default=False)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
        json_encoders={datetime: lambda dt: dt.isoformat()},
    )

    def mark_modified(self) -> None:
        """Mark the model as modified and update timestamp."""
        self._modified = True
        self.updated_at = datetime.now()

    def is_modified(self) -> bool:
        """Check if the model has been modified."""
        return self._modified

    def reset_modified(self) -> None:
        """Reset the modified flag."""
        self._modified = False

    @classmethod
    def register(cls, instance: "SerializableModel") -> "SerializableModel":
        """Register an instance with the class registry."""
        if cls._registry is not None:
            return cls._registry.register(instance)
        return instance

    @classmethod
    def get(cls, name: str) -> Optional["SerializableModel"]:
        """Get an instance by name from the registry."""
        if cls._registry is not None:
            return cls._registry.get(cls.__name__, name)
        return None

    @classmethod
    def find_by_id(cls, id: str) -> Optional["SerializableModel"]:
        """Find an instance by ID from the registry."""
        if cls._registry is not None:
            return cls._registry.find_by_id(id)
        return None

    @classmethod
    def list_all(cls) -> list[str]:
        """List all instances of this type from the registry."""
        if cls._registry is not None:
            return cls._registry.list(cls.__name__)
        return []

    @classmethod
    def get_all(cls) -> dict[str, "SerializableModel"]:
        """Get all instances of this type from the registry."""
        if cls._registry is not None:
            return cls._registry.get_all(cls.__name__)
        return {}
