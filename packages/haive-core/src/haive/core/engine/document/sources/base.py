import hashlib
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, Optional, Protocol

from pydantic import BaseModel, ConfigDict, Field, computed_field

from haive.core.engine.loaders.sources.types import SourceType


class SourceInterface(Protocol):
    """Protocol defining what a source must provide."""

    source_type: SourceType

    def get_source_value(self) -> Any: ...
    def validate(self) -> bool: ...
    def get_metadata(self) -> dict[str, Any]: ...


class BaseSource(BaseModel, ABC):
    """Abstract base class for all document sources.

    Provides common functionality and required methods for all sources.
    """

    source_type: SourceType = Field(description="Type of source")
    name: str | None = Field(default=None, description="Optional name for the source")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @abstractmethod
    def get_source_value(self) -> Any:
        """Get the underlying source value."""

    @abstractmethod
    def validate(self) -> bool:
        """Validate that the source exists and is accessible."""

    @computed_field
    def source_id(self) -> str:
        """Unique identifier for the source, calculated from source value."""
        value = str(self.get_source_value())
        return hashlib.md5(value.encode()).hexdigest()

    @computed_field
    def source_category(self) -> str:
        """Category of the source (web, file, etc.)."""
        from haive.core.engine.loaders.sources.groups import SOURCE_TO_GROUP

        return SOURCE_TO_GROUP.get(self.source_type, "OTHER")

    def get_metadata(self) -> dict[str, Any]:
        """Get basic metadata about the source."""
        return {
            "source_id": self.source_id,
            "source_type": str(self.source_type),
            "source_category": self.source_category,
            "created_at": self.created_at.isoformat(),
            "name": self.name if self.name else "Unnamed Source",
        }
