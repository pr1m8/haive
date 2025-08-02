"""mixins.timestamps.
=================

Reusable timestamp mixins for Pydantic models.

This module provides composable mixins for automatic creation and access
timestamps in Pydantic models, with built-in UTC, field freezing, custom
serialization, and age calculation (as both seconds and human-readable string).

Mixins:
    - CreatedTimestampMixin: Adds a frozen `created_at` datetime field.
    - AccessTimestampsMixin: Adds a frozen `last_accessed_at` datetime field,
      internal touch logic, and computed age fields.

Typical usage example:

    class MyLog(CreatedTimestampMixin):
        event: str

    class MySession(AccessTimestampsMixin):
        user_id: int

    log = MyLog(event="example")
    session = MySession(user_id=42)
    print(log.created_at)          # UTC datetime of creation
    print(session.age_human)       # e.g. '0 minutes, 2 seconds'

All datetime fields are timezone-aware (UTC).
All serialization returns integer POSIX timestamps for compatibility.

Intended for use with Sphinx AutoAPI and Google-style docstrings.
"""

from datetime import UTC, datetime, timedelta
from typing import Any, Self

from pydantic import BaseModel, Field, computed_field, field_serializer, model_validator


def utcnow() -> datetime:
    """Get the current UTC datetime with timezone information.

    Returns:
        datetime: The current UTC datetime.
    """
    return datetime.now(UTC)


def to_int_timestamp(dt: datetime, _info: Any = None) -> int:
    """Convert a datetime object to an integer POSIX timestamp.

    Args:
        dt (datetime): The datetime to convert.
        _info (Any, optional): Not used, for Pydantic serializer compatibility.

    Returns:
        int: POSIX timestamp.
    """
    return int(dt.timestamp())


class CreatedTimestampMixin(BaseModel):
    """Mixin to provide a frozen, auto-populated UTC `created_at` timestamp field.

    Attributes:
        created_at (datetime): The UTC datetime when the object was created.
    """

    created_at: datetime = Field(
        default_factory=utcnow,
        frozen=True,
        description="UTC datetime when the object was created.",
    )

    @field_serializer("created_at")
    def _serialize_created(self, dt: datetime, _info: Any) -> int:
        """Serialize `created_at` as an integer timestamp.

        Args:
            dt (datetime): The datetime value.
            _info (Any): Pydantic serialization context.

        Returns:
            int: POSIX timestamp.
        """
        return to_int_timestamp(dt, _info)

    @property
    def created_at_iso(self) -> str:
        """Get the ISO 8601 string of the creation time.

        Returns:
            str: The `created_at` timestamp as an ISO string.
        """
        return self.created_at.isoformat()


class AccessTimestampsMixin(CreatedTimestampMixin):
    """Mixin to add a frozen `last_accessed_at` timestamp, `touch` logic, and age calculation.

    Inherits:
        CreatedTimestampMixin: Provides `created_at`.

    Attributes:
        last_accessed_at (datetime): The UTC datetime when the object was last accessed.
    """

    last_accessed_at: datetime = Field(
        default_factory=utcnow,
        frozen=True,
        description="UTC datetime when the object was last accessed.",
    )

    @model_validator(mode="after")
    def _sync_last_accessed(cls) -> Self:
        """Sync `last_accessed_at` to `created_at` immediately after model creation.

        Returns:
            AccessTimestampsMixin: The validated model instance.
        """
        object.__setattr__(self, "last_accessed_at", self.created_at)
        return self

    @field_serializer("last_accessed_at")
    def _serialize_accessed(self, dt: datetime, _info: Any) -> int:
        """Serialize `last_accessed_at` as an integer timestamp.

        Args:
            dt (datetime): The datetime value.
            _info (Any): Pydantic serialization context.

        Returns:
            int: POSIX timestamp.
        """
        return to_int_timestamp(dt, _info)

    def _touch(self) -> None:
        """Update the `last_accessed_at` timestamp to the current time.

        Only to be used by internal logic; bypasses frozen field restriction.
        """
        object.__setattr__(self, "last_accessed_at", utcnow())

    @property
    def age(self) -> timedelta:
        """Get the time since object creation as a `timedelta`.

        Returns:
            timedelta: The duration since `created_at`.
        """
        return utcnow() - self.created_at

    @computed_field
    @property
    def age_seconds(self) -> int:
        """Get the object's age in seconds since creation.

        Returns:
            int: Age in seconds.
        """
        return int(self.age.total_seconds())

    @property
    def age_human(self) -> str:
        """Get a human-readable string for the object's age.

        Returns:
            str: Age as 'X days, Y hours, Z minutes, N seconds'.
        """
        td = self.age
        mins, secs = divmod(td.total_seconds(), 60)
        hours, mins = divmod(mins, 60)
        days, hours = divmod(hours, 24)
        parts = []
        if days:
            parts.append(f"{int(days)} days")
        if hours:
            parts.append(f"{int(hours)}")
