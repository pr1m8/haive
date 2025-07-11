"""PostgreSQL-based persistence implementation for the Haive framework.

This module provides a PostgreSQL-backed checkpoint persistence implementation that
stores state data in a PostgreSQL database. This allows for durable, reliable state
persistence across application restarts and deployments.

The PostgreSQL implementation offers advanced features including connection pooling,
automatic retry with exponential backoff, comprehensive error handling, and support
for both synchronous and asynchronous operation modes. It integrates with LangGraph's
checkpoint system while adding enhanced robustness and configurability.

For production deployments, the PostgreSQL implementation is generally recommended
over in-memory or SQLite options due to its scalability, reliability, and
concurrent access capabilities.
"""

import logging
from typing import Any

from pydantic import Field, SecretStr

from haive.core.persistence.base import CheckpointerConfig
from haive.core.persistence.types import (
    CheckpointerMode,
    CheckpointerType,
    CheckpointStorageMode,
)

logger = logging.getLogger(__name__)


class PostgresCheckpointerConfig(CheckpointerConfig[dict[str, Any]]):
    """Configuration for PostgreSQL-based checkpoint persistence.

    This implementation provides a robust, production-ready persistence solution
    using PostgreSQL as the storage backend. It offers comprehensive configuration
    options for database connections, connection pooling, security, and performance
    tuning.

    PostgreSQL persistence is recommended for production deployments where durability,
    reliability, and concurrent access are important. It supports both full history
    tracking and space-efficient shallow mode that only retains the most recent state.

    Key features include:

    - Connection pooling for optimal performance under load
    - Automatic retry with exponential backoff for resilience
    - Comprehensive security options including SSL/TLS support
    - Support for both synchronous and asynchronous operation
    - Transaction management and prepared statement optimization
    - Thread registration for tracking active sessions
    - Support for both full history and shallow (latest-only) storage modes

    The implementation maintains connection pools separately for synchronous and
    asynchronous usage, ensuring optimal performance in both contexts. It also
    includes table setup and validation to ensure the database schema is properly
    configured.

    Example:
        ```python
        from haive.core.persistence import PostgresCheckpointerConfig
        from haive.core.persistence.types import CheckpointerMode, CheckpointStorageMode

        # Create a basic PostgreSQL checkpointer
        config = PostgresCheckpointerConfig(
            db_host="localhost",
            db_port=5432,
            db_name="haive",
            db_user="postgres",
            db_pass="secure_password",
            ssl_mode="require",
            mode=CheckpointerMode.ASYNC,
            storage_mode=CheckpointStorageMode.SHALLOW
        )

        # For async usage
        async def setup():
            async_checkpointer = await config.create_async_checkpointer()
            # Use the checkpointer...
        ```

    Notes:
        - Requires the psycopg and psycopg_pool packages to be installed
        - For best performance, use connection pooling with appropriate sizing
        - Consider shallow mode for applications that don't need full history
    """

    type: CheckpointerType = CheckpointerType.POSTGRES

    # Database connection parameters
    db_host: str = Field(default="localhost", description="PostgreSQL server hostname")
    db_port: int = Field(default=5432, description="PostgreSQL server port")
    db_name: str = Field(default="postgres", description="Database name")
    db_user: str = Field(default="postgres", description="Database username")
    db_pass: SecretStr = Field(
        default_factory=lambda: SecretStr("postgres"), description="Database password"
    )
    ssl_mode: str = Field(
        default="disable", description="SSL mode for database connection"
    )

    # Connection pool configuration
    min_pool_size: int = Field(
        default=1, description="Minimum number of connections in the pool"
    )
    max_pool_size: int = Field(
        default=5, description="Maximum number of connections in the pool"
    )

    # Additional connection options
    auto_commit: bool = Field(default=True, description="Auto-commit transactions")
    prepare_threshold: int | None = Field(
        default=None, description="Prepared statement threshold (None to disable)"
    )
    connection_kwargs: dict[str, Any] = Field(
        default_factory=lambda: {
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 5,
            "connect_timeout": 30,
        },
        description="Additional connection keyword arguments",
    )

    # Optional direct connection string
    connection_string: str | None = Field(
        default=None,
        description="Direct connection string (overrides individual parameters)",
    )

    # Pipeline mode
    use_pipeline: bool = Field(
        default=False, description="Whether to use pipeline mode for better performance"
    )

    class Config:
        arbitrary_types_allowed = True

    def is_async_mode(self) -> bool:
        """Check if this configuration is set to operate in asynchronous mode.

        This method determines whether the PostgreSQL checkpointer should use
        asynchronous operations based on the configured mode. It affects which
        connection pools and checkpointer implementations are used.

        For PostgreSQL, this is an important distinction as it determines whether
        synchronous or asynchronous database drivers are used, which have different
        connection management patterns and performance characteristics.

        Returns:
            bool: True if configured for async operations, False for synchronous
        """
        return self.mode == CheckpointerMode.ASYNC

    def get_connection_uri(self) -> str:
        """Generate a formatted connection URI for PostgreSQL.

        This method constructs a properly formatted PostgreSQL connection string
        based on the configured connection parameters. It handles proper escaping
        of special characters in passwords and formatting according to PostgreSQL
        standards.

        The method prioritizes using a direct connection string if one is provided,
        otherwise it builds the string from individual connection parameters.

        Returns:
            str: Formatted PostgreSQL connection string ready for use

        Example:
            ```python
            config = PostgresCheckpointerConfig(
                db_host="db.example.com",
                db_port=5432,
                db_name="haive",
                db_user="app_user",
                db_pass="secret_password",
                ssl_mode="require"
            )
            uri = config.get_connection_uri()
            # uri = "postgresql://app_user:secret_password@db.example.com:5432/haive?sslmode=require"
            ```
        """
        # Use direct connection string if provided
        if self.connection_string:
            return self.connection_string

        # Generate from individual parameters
        import urllib.parse

        encoded_pass = urllib.parse.quote_plus(self.db_pass.get_secret_value())
        db_uri = f"postgresql://{self.db_user}:{encoded_pass}@{self.db_host}:{self.db_port}/{self.db_name}"
        if self.ssl_mode:
            db_uri += f"?sslmode={self.ssl_mode}"
        return db_uri

    def get_connection_kwargs(self) -> dict[str, Any]:
        """Get connection keyword arguments for PostgreSQL connections.

        This method constructs a dictionary of connection options to be passed
        to the PostgreSQL connection pool and individual connections. It combines
        the standard configuration parameters with any additional custom parameters
        specified in connection_kwargs.

        The options include settings for transaction management, prepared statement
        handling, and timeout configuration, which can significantly impact
        performance and reliability.

        Returns:
            Dict[str, Any]: Dictionary of connection options ready to use with
                PostgreSQL connections or connection pools

        Example:
            ```python
            config = PostgresCheckpointerConfig(
                auto_commit=True,
                prepare_threshold=5,
                connection_kwargs={"application_name": "haive_app"}
            )
            kwargs = config.get_connection_kwargs()
            # kwargs = {
            #    "autocommit": True,
            #    "prepare_threshold": 5,
            #    "application_name": "haive_app"
            # }
            ```
        """
        kwargs = {
            "autocommit": self.auto_commit,
            "prepare_threshold": self.prepare_threshold,
        }
        # Add any additional kwargs
        kwargs.update(self.connection_kwargs)
        return kwargs

    def create_checkpointer(self) -> Any:
        """Create a synchronous PostgreSQL checkpointer.

        This method creates and configures a synchronous PostgreSQL checkpointer
        that matches the settings in this configuration. It handles connection
        pool creation, checkpointer initialization, and database table setup.

        The method automatically selects the appropriate implementation based on
        the storage_mode setting (full or shallow), and performs error checking
        to ensure the requested configuration is valid.

        Returns:
            Any: A configured PostgresSaver or ShallowPostgresSaver instance

        Raises:
            RuntimeError: If async mode is requested (use create_async_checkpointer instead)
            RuntimeError: If the PostgreSQL dependencies are missing or connection fails

        Example:
            ```python
            config = PostgresCheckpointerConfig(
                db_host="localhost",
                db_port=5432,
                storage_mode=CheckpointStorageMode.SHALLOW
            )
            try:
                # Creates a ShallowPostgresSaver instance
                checkpointer = config.create_checkpointer()

                # Use with a graph
                graph = Graph(checkpointer=checkpointer)
            except RuntimeError as e:
                print(f"Failed to create PostgreSQL checkpointer: {e}")
                # Handle error - perhaps fall back to memory checkpointer
            ```
        """
        try:
            # Handle async mode request
            if self.is_async_mode():
                raise RuntimeError(
                    "Cannot use create_checkpointer for async mode, use create_async_checkpointer instead"
                )

            from psycopg_pool import ConnectionPool

            # Try to use our custom PostgresSaver that disables prepared statements
            try:
                from haive.core.persistence.postgres_saver_override import (
                    PostgresSaverNoPreparedStatements as PostgresSaver,
                )

                logger.info(
                    "Using PostgresSaverNoPreparedStatements to avoid prepared statement conflicts"
                )
            except ImportError:
                logger.warning(
                    "Could not import PostgresSaverNoPreparedStatements, using standard PostgresSaver"
                )
                # Import appropriate checkpointer class
                if self.storage_mode == CheckpointStorageMode.SHALLOW:
                    try:
                        from langgraph.checkpoint.postgres import (
                            ShallowPostgresSaver as PostgresSaver,
                        )
                    except ImportError:
                        from langgraph.checkpoint.postgres import PostgresSaver
                else:
                    from langgraph.checkpoint.postgres import PostgresSaver

            # Create connection pool with forced parameters to avoid SSL issues
            connection_kwargs = self.get_connection_kwargs()

            # Force disable prepared statements and ensure proper SSL handling
            connection_kwargs.update(
                {
                    "prepare_threshold": None,  # Force disable prepared statements
                    "autocommit": True,  # Ensure autocommit
                }
            )

            pool = ConnectionPool(
                conninfo=self.get_connection_uri(),
                min_size=self.min_pool_size,
                max_size=self.max_pool_size,
                kwargs=connection_kwargs,
                check=ConnectionPool.check_connection,  # Add connection health checking
                max_lifetime=1800,  # 30 minutes max connection lifetime
                open=False,  # Don't open in constructor to avoid early failures
            )

            # Explicitly open the pool with error handling
            try:
                pool.open()
                logger.info("PostgreSQL connection pool opened successfully")
            except Exception as e:
                logger.exception(f"Failed to open PostgreSQL connection pool: {e}")
                raise

            # Create checkpointer
            checkpointer = PostgresSaver(pool)

            # Setup tables if needed
            if self.setup_needed:
                try:
                    checkpointer.setup()
                    logger.info("PostgreSQL tables set up successfully")
                except Exception as e:
                    logger.warning(f"Error during PostgreSQL setup: {e}")

            return checkpointer

        except Exception as e:
            logger.exception(f"Failed to create PostgreSQL checkpointer: {e}")
            raise RuntimeError(f"Failed to create PostgreSQL checkpointer: {e}")

    async def create_async_checkpointer(self) -> Any:
        """Create an asynchronous PostgreSQL checkpointer.

        This method creates and configures an asynchronous PostgreSQL checkpointer
        that matches the settings in this configuration. It handles async connection
        pool creation, checkpointer initialization, and database table setup.

        The method automatically selects the appropriate implementation based on
        the storage_mode setting (full or shallow). It uses the asynchronous
        PostgreSQL driver and connection pool for non-blocking database operations.

        Returns:
            Any: A configured AsyncPostgresSaver or AsyncShallowPostgresSaver instance

        Raises:
            RuntimeError: If the asynchronous PostgreSQL dependencies are missing
                or connection fails

        Example:
            ```python
            config = PostgresCheckpointerConfig(
                db_host="localhost",
                db_port=5432,
                mode=CheckpointerMode.ASYNC,
                storage_mode=CheckpointStorageMode.FULL
            )

            async def setup_graph():
                try:
                    # Creates an AsyncPostgresSaver instance
                    async_checkpointer = await config.create_async_checkpointer()

                    # Use with an async graph
                    graph = AsyncGraph(checkpointer=async_checkpointer)
                    return graph
                except RuntimeError as e:
                    print(f"Failed to create async PostgreSQL checkpointer: {e}")
                    # Handle error
            ```

        Note:
            This method automatically forces the mode to ASYNC for consistency,
            ensuring that the configuration accurately reflects the type of
            checkpointer being created.
        """
        try:
            # Force async mode
            self.mode = CheckpointerMode.ASYNC

            from psycopg_pool import AsyncConnectionPool

            # Try to use our custom AsyncPostgresSaver that disables prepared statements
            try:
                from haive.core.persistence.postgres_saver_override import (
                    AsyncPostgresSaverNoPreparedStatements as AsyncPostgresSaver,
                )

                logger.info(
                    "Using AsyncPostgresSaverNoPreparedStatements to avoid prepared statement conflicts"
                )
            except ImportError:
                logger.warning(
                    "Could not import AsyncPostgresSaverNoPreparedStatements, using standard AsyncPostgresSaver"
                )

                # Import appropriate checkpointer class
                try:
                    if self.storage_mode == CheckpointStorageMode.SHALLOW:
                        from langgraph.checkpoint.postgres.aio import (
                            AsyncShallowPostgresSaver as AsyncPostgresSaver,
                        )
                    else:
                        from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

                    logger.info(
                        "Successfully imported AsyncPostgresSaver from langgraph.checkpoint.postgres.aio"
                    )
                except ImportError as e:
                    logger.exception(
                        f"Failed to import AsyncPostgresSaver from aio module: {e}"
                    )

                    # Try alternative import paths
                    try:
                        # Some versions might have it in the main postgres module
                        from langgraph.checkpoint.postgres import AsyncPostgresSaver

                        logger.info(
                            "Successfully imported AsyncPostgresSaver from langgraph.checkpoint.postgres"
                        )
                    except ImportError:
                        try:
                            # Try langgraph_checkpoint_postgres package
                            from langgraph_checkpoint_postgres.aio import (
                                AsyncPostgresSaver,
                            )

                            logger.info(
                                "Successfully imported AsyncPostgresSaver from langgraph_checkpoint_postgres.aio"
                            )
                        except ImportError:
                            try:
                                from langgraph_checkpoint_postgres import (
                                    AsyncPostgresSaver,
                                )

                                logger.info(
                                    "Successfully imported AsyncPostgresSaver from langgraph_checkpoint_postgres"
                                )
                            except ImportError:
                                logger.exception(
                                    "AsyncPostgresSaver not available in any known location. "
                                    "Please ensure langgraph-checkpoint-postgres is installed with async support."
                                )
                                # Fall back to sync checkpointer with warning
                                logger.warning(
                                    "Falling back to sync PostgresSaver for async operations (not recommended)"
                                )
                                from langgraph.checkpoint.postgres import (
                                    PostgresSaver as AsyncPostgresSaver,
                                )

            # Create connection pool with forced parameters to avoid SSL issues
            connection_kwargs = self.get_connection_kwargs()

            # Force disable prepared statements and ensure proper SSL handling
            connection_kwargs.update(
                {
                    "prepare_threshold": None,  # Force disable prepared statements
                    "autocommit": True,  # Ensure autocommit
                }
            )

            pool = AsyncConnectionPool(
                conninfo=self.get_connection_uri(),
                min_size=self.min_pool_size,
                max_size=self.max_pool_size,
                kwargs=connection_kwargs,
                check=AsyncConnectionPool.check_connection,  # Add connection health checking
                max_lifetime=1800,  # 30 minutes max connection lifetime
                open=False,  # Don't open in constructor to avoid deprecation warning
            )

            # Explicitly open the pool with error handling
            try:
                await pool.open()
                logger.info("Async PostgreSQL connection pool opened successfully")
            except Exception as e:
                logger.exception(
                    f"Failed to open async PostgreSQL connection pool: {e}"
                )
                raise

            # Create checkpointer
            checkpointer = AsyncPostgresSaver(pool)

            # Setup tables if needed
            if self.setup_needed:
                try:
                    await checkpointer.setup()
                    logger.info("PostgreSQL tables set up successfully (async)")
                except Exception as e:
                    logger.warning(f"Error during PostgreSQL async setup: {e}")

            return checkpointer

        except Exception as e:
            logger.exception(f"Failed to create async PostgreSQL checkpointer: {e}")
            logger.exception(f"Connection URI: {self.get_connection_uri()}")
            logger.exception(f"Storage mode: {self.storage_mode}")
            logger.exception(f"Mode: {self.mode}")

            # Try to provide more specific error information
            if "AsyncPostgresSaver" in str(e):
                logger.exception("AsyncPostgresSaver import or creation failed")
            if "pool" in str(e).lower():
                logger.exception("Connection pool creation failed")
            if "connection" in str(e).lower():
                logger.exception("Database connection failed")

            raise RuntimeError(f"Failed to create async PostgreSQL checkpointer: {e}")

    async def initialize_async_checkpointer(self) -> Any:
        """Initialize an async checkpointer with proper resource management.

        This method creates and initializes an asynchronous PostgreSQL checkpointer
        with proper resource lifecycle management using an async context manager.
        This ensures that database connections are properly closed when they're
        no longer needed, preventing connection leaks and other resource issues.

        Unlike create_async_checkpointer, which returns a raw checkpointer instance,
        this method returns an async context manager that automatically handles
        resource cleanup when the context is exited, making it ideal for use
        in production environments.

        Returns:
            Any: An async context manager that yields a configured checkpointer
                and automatically cleans up resources on exit

        Raises:
            RuntimeError: If the asynchronous PostgreSQL dependencies are missing
                or connection fails

        Example:
            ```python
            config = PostgresCheckpointerConfig(
                db_host="localhost",
                db_port=5432,
                mode=CheckpointerMode.ASYNC
            )

            async def run_with_managed_resources():
                # Resources will be properly initialized and cleaned up
                async with await config.initialize_async_checkpointer() as checkpointer:
                    # Use checkpointer with async code
                    graph = AsyncGraph(checkpointer=checkpointer)
                    # Run operations with graph...
                # Connection pool is automatically closed here
            ```

        Note:
            This is the recommended method for asynchronous usage in production
            environments, as it ensures proper resource cleanup even if errors occur.
        """
        from contextlib import asynccontextmanager

        @asynccontextmanager
        async def async_checkpointer_context():
            """Context manager for async checkpointer with proper resource management."""
            checkpointer = None
            try:
                # Create the checkpointer
                checkpointer = await self.create_async_checkpointer()

                # Yield it for use
                yield checkpointer

            finally:
                # Clean up resources
                if checkpointer and hasattr(checkpointer, "conn") and checkpointer.conn:
                    # Close pool if available
                    try:
                        if hasattr(checkpointer.conn, "close"):
                            await checkpointer.conn.close()
                            logger.debug("Async PostgreSQL pool closed successfully")
                    except Exception as e:
                        logger.warning(f"Error closing async PostgreSQL pool: {e}")

        # Return the context manager
        return async_checkpointer_context()
