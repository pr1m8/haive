"""Type definitions for the Haive persistence system.

This module provides enumeration types and utility classes for the persistence
system, defining the available checkpointer types, operational modes, and
storage strategies. These types are used throughout the persistence system
for configuration and operation.

The module includes special handling for Python keyword conflicts (like 'async')
and backward compatibility mappings for evolving terminology.
"""

from enum import Enum
from typing import Dict


class CheckpointerType(str, Enum):
    """Types of checkpointer implementations available in the system.

    This enumeration defines the supported storage backend types for state
    persistence. Each type corresponds to a specific implementation class
    that handles the details of storing and retrieving state data.

    Attributes:
        MEMORY: In-memory storage (non-persistent, for development/testing)
        POSTGRES: PostgreSQL database storage
        MYSQL: MySQL database storage
        SQLITE: SQLite database storage
        REDIS: Redis database storage
        SUPABASE: Supabase database storage
    """

    MEMORY = "memory"
    POSTGRES = "postgres"
    MYSQL = "mysql"
    SQLITE = "sqlite"
    REDIS = "redis"
    SUPABASE = "supabase"


class CheckpointerMode(str, Enum):
    """Operational modes for checkpointers.

    This enumeration defines how checkpointers should operate in terms of
    synchronicity. It determines whether operations are performed synchronously
    (blocking) or asynchronously (non-blocking).

    The enum includes special handling for the 'async' value, which is a Python
    keyword, allowing both 'async' and 'async_' to be used interchangeably.

    Attributes:
        SYNC: Synchronous operations (blocking)
        ASYNC: Asynchronous operations (non-blocking)
        async_: Alias for ASYNC (to avoid Python keyword conflict)
    """

    SYNC = "sync"
    ASYNC = "async"

    # Special handling for async mode
    # This is needed because 'async' is a Python keyword
    async_ = "async"

    def __eq__(self, other):
        """Custom equality to handle async_ special case.

        This method implements special handling for comparing 'async' and 'async_'
        values, treating them as equivalent. This allows for more flexible API usage
        where either form can be accepted.

        Args:
            other: The value to compare against

        Returns:
            bool: True if values are equal, considering special cases
        """
        if isinstance(other, str):
            if self.value == "async" and other == "async_":
                return True
            if self.value == "async_" and other == "async":
                return True
        return super().__eq__(other)


class CheckpointStorageMode(str, Enum):
    """Storage strategies for checkpointers.

    This enumeration defines how state history is managed within the persistence
    system. Different modes offer trade-offs between storage efficiency and
    history retention.

    The enum includes backward compatibility mappings between older terminology
    ('standard') and current terminology ('full').

    Attributes:
        FULL: Store the complete history of all checkpoints
        SHALLOW: Store only the most recent state (space efficient)
        CHAIN: Store checkpoints in a chain/linked list structure
        STANDARD: Alias for FULL (for backward compatibility)
    """

    FULL = "full"  # Store full history
    SHALLOW = "shallow"  # Store only the most recent state
    CHAIN = "chain"  # Store checkpoints in a chain/linked list

    # For compatibility with earlier versions
    STANDARD = "full"

    def __eq__(self, other):
        """Custom equality to handle compatibility modes.

        This method implements special handling for comparing 'full' and 'standard'
        values, treating them as equivalent for backward compatibility with older
        code that might use the 'standard' terminology.

        Args:
            other: The value to compare against

        Returns:
            bool: True if values are equal, considering compatibility mappings
        """
        if isinstance(other, str):
            if self.value == "full" and other == "standard":
                return True
            if self.value == "standard" and other == "full":
                return True
        return super().__eq__(other)


class ConnectionOptions:
    """Common connection options and utilities for database-backed checkpointers.

    This utility class provides standardized methods for working with database
    connection parameters across different checkpointer implementations. It
    includes helpers for constructing connection strings, validating connection
    parameters, and accessing standard options for different database systems.

    The class is designed to be used statically without instantiation, offering
    a centralized place for connection-related utilities that can be shared
    across different database-backed checkpointer implementations.
    """

    @staticmethod
    def get_postgres_ssl_modes() -> Dict[str, str]:
        """Get valid PostgreSQL SSL connection modes with descriptions.

        This method returns a dictionary of valid SSL mode options for PostgreSQL
        connections along with human-readable descriptions of each mode. These
        modes control how SSL is used for securing database connections.

        Returns:
            Dict[str, str]: Dictionary mapping SSL mode names to descriptions

        Example:
            ```python
            ssl_modes = ConnectionOptions.get_postgres_ssl_modes()
            print(ssl_modes['require'])  # "Require SSL connection"
            ```
        """
        return {
            "disable": "No SSL",
            "allow": "Allow SSL connection but don't require",
            "prefer": "Prefer SSL connection but accept non-SSL",
            "require": "Require SSL connection",
            "verify-ca": "Verify server certificate",
            "verify-full": "Verify server certificate and hostname",
        }

    @staticmethod
    def get_postgres_dsn(
        host: str = "localhost",
        port: int = 5432,
        dbname: str = "postgres",
        user: str = "postgres",
        password: str = "postgres",
        ssl_mode: str = "disable",
    ) -> str:
        """Create a PostgreSQL DSN (Data Source Name) connection string.

        This method constructs a properly formatted connection string for
        PostgreSQL databases based on the provided parameters. It handles
        proper escaping of special characters in passwords and formatting
        the string according to PostgreSQL standards.

        Args:
            host: Database server hostname or IP address
            port: Database server port number
            dbname: Name of the database to connect to
            user: Username for authentication
            password: Password for authentication
            ssl_mode: SSL mode for the connection (see get_postgres_ssl_modes)

        Returns:
            str: Formatted PostgreSQL connection string ready for use

        Example:
            ```python
            dsn = ConnectionOptions.get_postgres_dsn(
                host="db.example.com",
                port=5432,
                dbname="myapp",
                user="appuser",
                password="secret",
                ssl_mode="require"
            )
            # dsn = "postgresql://appuser:secret@db.example.com:5432/myapp?sslmode=require"
            ```
        """
        import urllib.parse

        encoded_pass = urllib.parse.quote_plus(password)
        return f"postgresql://{user}:{encoded_pass}@{host}:{port}/{dbname}?sslmode={ssl_mode}"
