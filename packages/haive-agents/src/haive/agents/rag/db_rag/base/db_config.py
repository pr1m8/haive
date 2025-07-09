from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

# Type variable for the database connection object
T = TypeVar("T")


class BaseDBConfig(ABC, BaseModel, Generic[T]):
    """Abstract base configuration model for database connections.

    This class defines the common interface that all database
    configurations should implement, regardless of database type.
    """

    db_type: str = Field(
        description="Type of database (e.g., 'sql', 'graph', 'document')"
    )

    @abstractmethod
    def get_connection_string(self) -> str:
        """Generate a connection string for the database."""

    @abstractmethod
    def get_db(self) -> T | None:
        """Creates and returns a database connection object."""

    @abstractmethod
    def get_db_schema(self) -> dict[str, Any] | None:
        """Retrieves the schema information from the database."""
