"""Timestamp mixin for tracking creation and modification times.

This module provides a mixin for adding timestamp tracking to Pydantic models.
It automatically records creation time and provides methods for updating and
querying timestamps, which is useful for auditing, caching, and expiration logic.

Usage:
    ```python
    from pydantic import BaseModel
    from haive.core.common.mixins.general import TimestampMixin

    class Document(TimestampMixin, BaseModel):
        title: str
        content: str

    # Create a document (timestamps automatically set)
    doc = Document(title="Example", content="Content")

    # Check how old the document is
    age = doc.age_in_seconds()

    # Update document and its timestamp
    doc.content = "Updated content"
    doc.update_timestamp()

    # Check time since last update
    time_since_update = doc.time_since_update()
    ```
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, PrivateAttr


class TimestampMixin(BaseModel):
    """Mixin for adding timestamp tracking to Pydantic models.

    This mixin adds creation and update timestamps to any model,
    with methods for updating timestamps and calculating time intervals.
    It's useful for tracking when objects were created and modified,
    which helps with auditing, caching strategies, and expiration logic.

    Attributes:
        created_at: When this object was created (auto-set on instantiation).
        updated_at: When this object was last updated (initially same as created_at).
    """

    created_at: datetime = Field(
        default_factory=datetime.now, description="When this object was created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, description="When this object was last updated"
    )

    def update_timestamp(self) -> None:
        """Update the updated_at timestamp to the current time.

        This method should be called whenever the object is modified
        to track the time of the latest change.
        """
        self.updated_at = datetime.now()

    def age_in_seconds(self) -> float:
        """Get age of this object in seconds.

        This method calculates how much time has passed since the
        object was created.

        Returns:
            Number of seconds since creation.
        """
        return (datetime.now() - self.created_at).total_seconds()

    def time_since_update(self) -> float:
        """Get time since last update in seconds.

        This method calculates how much time has passed since the
        object was last updated.

        Returns:
            Number of seconds since last update.
        """
        return (datetime.now() - self.updated_at).total_seconds()
