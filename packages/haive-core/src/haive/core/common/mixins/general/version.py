"""Version mixin for tracking object versions.

This module provides a mixin for adding version tracking to Pydantic models.
It tracks the current version and maintains a history of previous versions,
which is useful for auditing, compatibility checking, and change tracking.

Usage:
    ```python
    from pydantic import BaseModel
    from haive.core.common.mixins.general import VersionMixin

    class Document(VersionMixin, BaseModel):
        title: str
        content: str

    # Create a document with default version 1.0.0
    doc = Document(title="Example", content="Content")

    # Make changes and bump version
    doc.content = "Updated content"
    doc.bump_version("1.1.0")

    # Check version history
    history = doc.get_version_history()  # ['1.0.0', '1.1.0']
    ```
"""

from pydantic import BaseModel, Field


class VersionMixin(BaseModel):
    """Mixin for adding version tracking to Pydantic models.

    This mixin adds version information to any model, with support for
    tracking version history. It's useful for managing model versions,
    checking compatibility, and auditing changes over time.

    Attributes:
        version: Current version string (defaults to "1.0.0").
        version_history: List of previous versions.
    """

    version: str = Field(default="1.0.0", description="Version string")
    version_history: list[str] = Field(
        default_factory=list, description="History of version changes"
    )

    def bump_version(self, new_version: str) -> None:
        """Update version and track the previous version in history.

        This method should be called whenever a significant change is made
        to the object that warrants a version increment.

        Args:
            new_version: The new version string to set.
        """
        self.version_history.append(self.version)
        self.version = new_version

    def get_version_history(self) -> list[str]:
        """Get complete version history including the current version.

        Returns:
            List containing all previous versions plus the current version.
        """
        return [*self.version_history, self.version]
