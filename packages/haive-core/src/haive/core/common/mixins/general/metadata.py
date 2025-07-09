"""Metadata mixin for arbitrary key-value storage.

This module provides a mixin for adding flexible metadata storage to
Pydantic models. It enables storing arbitrary key-value pairs as additional
information that may not warrant dedicated model fields.

Usage:
    ```python
    from pydantic import BaseModel
    from haive.core.common.mixins.general import MetadataMixin

    class Document(MetadataMixin, BaseModel):
        title: str
        content: str

    # Create a document with metadata
    doc = Document(
        title="Example",
        content="Sample content",
        metadata={"author": "John Doe", "tags": ["example", "sample"]}
    )

    # Add additional metadata
    doc.add_metadata("created_at", "2025-06-19")

    # Access metadata
    author = doc.get_metadata("author")  # "John Doe"

    # Check if metadata exists
    if doc.has_metadata("tags"):
        tags = doc.get_metadata("tags")
    ```
"""

from typing import Any, Dict

from pydantic import BaseModel, Field


class MetadataMixin(BaseModel):
    """Mixin for adding flexible metadata storage capabilities.

    This mixin provides a dictionary for storing arbitrary key-value pairs
    as metadata, along with methods for adding, retrieving, updating, and
    removing metadata entries.

    Attributes:
        metadata: Dictionary containing arbitrary metadata.
    """

    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Arbitrary metadata"
    )

    def add_metadata(self, key: str, value: Any) -> None:
        """Add a metadata key-value pair.

        Args:
            key: The metadata key.
            value: The value to store.
        """
        self.metadata[key] = value

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata value by key.

        Args:
            key: The metadata key to retrieve.
            default: Value to return if key doesn't exist.

        Returns:
            The metadata value or the default value if key doesn't exist.
        """
        return self.metadata.get(key, default)

    def has_metadata(self, key: str) -> bool:
        """Check if metadata key exists.

        Args:
            key: The metadata key to check.

        Returns:
            True if the key exists in metadata, False otherwise.
        """
        return key in self.metadata

    def remove_metadata(self, key: str) -> Any:
        """Remove and return metadata value.

        Args:
            key: The metadata key to remove.

        Returns:
            The removed value, or None if key doesn't exist.
        """
        return self.metadata.pop(key, None)

    def update_metadata(self, updates: Dict[str, Any]) -> None:
        """Update multiple metadata fields.

        Args:
            updates: Dictionary containing key-value pairs to update.
        """
        self.metadata.update(updates)

    def clear_metadata(self) -> None:
        """Clear all metadata.

        This method removes all metadata entries, resulting in an empty
        metadata dictionary.
        """
        self.metadata.clear()
