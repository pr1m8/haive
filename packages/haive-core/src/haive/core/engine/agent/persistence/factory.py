# src/haive/core/engine/agent/persistence/factory.py
import logging
from typing import Any, Dict, Optional, Type, Union

from haive.core.engine.agent.persistence.base import CheckpointerConfig
from haive.core.engine.agent.persistence.memory_config import MemoryCheckpointerConfig
from haive.core.engine.agent.persistence.mongodb_config import MongoDBCheckpointerConfig
from haive.core.engine.agent.persistence.postgres_config import (
    PostgresCheckpointerConfig,
)
from haive.core.engine.agent.persistence.types import CheckpointerType

logger = logging.getLogger(__name__)

# Registry of checkpointer types to their config classes
CHECKPOINTER_CONFIG_MAP: Dict[str, Type[CheckpointerConfig]] = {
    CheckpointerType.memory: MemoryCheckpointerConfig,
    CheckpointerType.postgres: PostgresCheckpointerConfig,
    CheckpointerType.mongodb: MongoDBCheckpointerConfig,
}


def load_checkpointer_config(data: Dict[str, Any]) -> CheckpointerConfig:
    """Create a checkpointer configuration from a dictionary.

    Args:
        data: Dictionary representation of a checkpointer configuration

    Returns:
        The appropriate CheckpointerConfig instance
    """
    # Extract type from data
    type_str = data.get("type", CheckpointerType.memory)

    # Get the config class
    config_cls = CHECKPOINTER_CONFIG_MAP.get(type_str)

    if not config_cls:
        logger.warning(
            f"Unsupported checkpointer type: {type_str}, falling back to memory"
        )
        return MemoryCheckpointerConfig()

    # Create and return the config instance
    return config_cls(**data)


def create_persistence_manager(
    persistence_config: Optional[Union[Dict[str, Any], CheckpointerConfig]] = None,
) -> "PersistenceManager":
    """Create a PersistenceManager from a CheckpointerConfig.

    Args:
        persistence_config: Configuration for persistence

    Returns:
        Configured PersistenceManager
    """
from haive.core.engine.agent.persistence.manager import PersistenceManager

    if persistence_config is None:
        # Default to memory persistence
        return PersistenceManager()

    # Process config based on type
    if isinstance(persistence_config, dict):
        checkpointer_config = load_checkpointer_config(persistence_config)
        return PersistenceManager(checkpointer_config)
    elif isinstance(persistence_config, CheckpointerConfig):
        return PersistenceManager(persistence_config)
    else:
        # Extract config from object if possible
        extracted_config = _extract_config_from_object(persistence_config)
        if extracted_config:
            checkpointer_config = load_checkpointer_config(extracted_config)
            return PersistenceManager(checkpointer_config)

    # Fallback to default
    return PersistenceManager()


def _extract_config_from_object(obj: Any) -> Optional[Dict[str, Any]]:
    """Extract persistence configuration from an arbitrary object.

    Args:
        obj: Object that might contain persistence configuration

    Returns:
        Extracted configuration dictionary or None
    """
    # If it has a persistence attribute
    if hasattr(obj, "persistence"):
        persistence = obj.persistence

        # Handle dict-like persistence attribute
        if isinstance(persistence, dict):
            return persistence

        # Handle Pydantic model-like persistence attribute
        if hasattr(persistence, "model_dump"):
            # Pydantic v2
            return persistence.model_dump()
        if hasattr(persistence, "dict"):
            # Pydantic v1
            return persistence.dict()

    return None
