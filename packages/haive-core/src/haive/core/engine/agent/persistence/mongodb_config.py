# src/haive/core/engine/agent/persistence/mongodb_config.py
import logging
from typing import Literal

from pydantic import Field

from haive.core.engine.agent.persistence.base import CheckpointerConfig
from haive.core.engine.agent.persistence.types import CheckpointerType

logger = logging.getLogger(__name__)

# Check MongoDB support
try:
    from langgraph.checkpoint.mongodb import MongoDBSaver
    from langgraph.checkpoint.mongodb.aio import AsyncMongoDBSaver

    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False
    logger.warning(
        "MongoDB dependencies not available. Install with: pip install langgraph-checkpoint-mongodb"
    )


class MongoDBCheckpointerConfig(CheckpointerConfig):
    """Configuration for MongoDB-based checkpointing."""

    type: Literal[CheckpointerType.mongodb] = Field(default=CheckpointerType.mongodb)
    connection_string: str = Field(default="mongodb://localhost:27017/")
    database: str = Field(default="haive")
    collection: str = Field(default="checkpoints")
    use_async: bool = Field(default=False, description="Use async connections")

    def create_checkpointer(self):
        """Create a MongoDB checkpointer.

        Returns:
            MongoDBSaver instance or MemorySaver fallback
        """
        if not MONGODB_AVAILABLE:
            logger.warning(
                "MongoDB dependencies not available, falling back to memory checkpointer"
            )
            from langgraph.checkpoint.memory import MemorySaver

            return MemorySaver()

        try:
            # Create a MongoDB saver
            return MongoDBSaver.from_conn_string(
                self.connection_string,
                database=self.database,
                collection=self.collection,
            )
        except Exception as e:
            logger.error(f"Error creating MongoDB checkpointer: {e}")
            logger.warning("Falling back to memory checkpointer")
            from langgraph.checkpoint.memory import MemorySaver

            return MemorySaver()

    async def acreate_checkpointer(self):
        """Asynchronously create a MongoDB checkpointer.

        Returns:
            AsyncMongoDBSaver instance or MemorySaver fallback
        """
        if not MONGODB_AVAILABLE or not self.use_async:
            # Fall back to synchronous version if async not requested
            return self.create_checkpointer()

        try:
            # Create an async MongoDB saver
            return await AsyncMongoDBSaver.from_conn_string(
                self.connection_string,
                database=self.database,
                collection=self.collection,
            )
        except Exception as e:
            logger.error(f"Error creating async MongoDB checkpointer: {e}")
            logger.warning("Falling back to memory checkpointer")
            from langgraph.checkpoint.memory import MemorySaver

            return MemorySaver()
