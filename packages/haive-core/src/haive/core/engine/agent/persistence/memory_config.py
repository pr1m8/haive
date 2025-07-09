# src/haive/core/engine/agent/persistence/memory_config.py
from typing import Literal

from langgraph.checkpoint.memory import MemorySaver
from pydantic import Field

from haive.core.engine.agent.persistence.base import CheckpointerConfig
from haive.core.engine.agent.persistence.types import CheckpointerType


class MemoryCheckpointerConfig(CheckpointerConfig):
    """Configuration for in-memory checkpointing.

    This is the simplest checkpointer, but doesn't persist across sessions.
    """

    type: Literal[CheckpointerType.memory] = Field(default=CheckpointerType.memory)

    def create_checkpointer(self):
        """Create a memory checkpointer.

        Returns:
            MemorySaver instance
        """
        return MemorySaver()
