# src/haive/core/engine/agent/persistence/base.py
import logging
from typing import Any, Dict

from pydantic import BaseModel, Field

from haive.core.engine.agent.persistence.types import CheckpointerType

logger = logging.getLogger(__name__)


class CheckpointerConfig(BaseModel):
    """Base configuration for agent persistence.

    CheckpointerConfig provides a consistent interface for configuring
    how agent state is persisted.
    """

    type: CheckpointerType = Field(default=CheckpointerType.memory)
    setup_needed: bool = Field(
        default=True, description="Whether to run setup on initialization"
    )

    class Config:
        arbitrary_types_allowed = True

    def create_checkpointer(self):
        """Create a checkpointer instance based on this configuration.

        Returns:
            The appropriate checkpointer instance
        """
        from langgraph.checkpoint.memory import MemorySaver

        return MemorySaver()

    async def acreate_checkpointer(self):
        """Asynchronously create a checkpointer instance (default implementation).

        Returns:
            The appropriate checkpointer instance
        """
        # Default implementation returns same as synchronous version
        return self.create_checkpointer()

    def to_dict(self) -> dict[str, Any]:
        """Convert configuration to a dictionary for serialization.

        Returns:
            Dictionary representation
        """
        if hasattr(self, "model_dump"):
            # Pydantic v2
            return self.model_dump(exclude={"_pool", "_pool_opened"})
        # Pydantic v1
        return self.dict(exclude={"_pool", "_pool_opened"})
