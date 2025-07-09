# src/haive/core/config/runnable.py

"""Configuration management for Haive runnables.

This module provides utilities for creating, managing, and manipulating runtime configurations
for Haive engines and runnables. It handles parameter management, metadata tracking, and
configuration merging.

The main class RunnableConfigManager provides a comprehensive set of static methods for
working with RunnableConfig objects, which are used to configure the behavior of engines
at runtime.

Classes:
    RunnableConfigManager: Static utility class for managing runnable configurations

Example:
    ```python
    # Create a basic config with thread tracking
    config = RunnableConfigManager.create(
        thread_id="123",
        user_id="user_456"
    )

    # Add engine-specific configuration
    config = RunnableConfigManager.add_engine_config(
        config,
        "my_llm",
        temperature=0.7,
        max_tokens=100
    )
    ```
"""

import copy
import uuid
from typing import Any

from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel


class RunnableConfigManager:
    """Enhanced manager for creating and manipulating RunnableConfig objects.

    Provides methods for creating standardized configs, extracting values,
    and managing engine-specific configurations.
    """

    @staticmethod
    def create(
        thread_id: str | None = None, user_id: str | None = None, **kwargs
    ) -> RunnableConfig:
        """Create a standardized RunnableConfig with common parameters.

        Args:
            thread_id: Optional thread ID for persistence (generated if not provided)
            user_id: Optional user ID for attribution and permissions
            **kwargs: Additional parameters to include in configurable section

        Returns:
            A properly structured RunnableConfig
        """
        # Initialize configurable section
        configurable = {
            "thread_id": thread_id or str(uuid.uuid4()),
        }

        # Add user_id if provided (required for proper tracking)
        if user_id is not None:
            configurable["user_id"] = user_id

        # Add any additional parameters
        for key, value in kwargs.items():
            configurable[key] = value

        # Ensure engine_configs exists
        if "engine_configs" not in configurable:
            configurable["engine_configs"] = {}

        # Create the config with proper structure
        config: RunnableConfig = {"configurable": configurable}

        return config

    @staticmethod
    def create_with_engine(
        engine: Any, thread_id: str | None = None, user_id: str | None = None, **kwargs
    ) -> RunnableConfig:
        """Create a RunnableConfig with engine parameters auto-populated.

        Args:
            engine: Engine object to extract params from
            thread_id: Optional thread ID
            user_id: Optional user ID
            **kwargs: Additional configurable parameters

        Returns:
            RunnableConfig with engine parameters
        """
        # Create base config
        config = RunnableConfigManager.create(
            thread_id=thread_id, user_id=user_id, **kwargs
        )

        # Extract engine parameters
        engine_params = {}

        # Try extract_params method first (preferred)
        if hasattr(engine, "extract_params"):
            engine_params = engine.extract_params()
        # Fall back to model_dump/dict
        elif hasattr(engine, "model_dump"):
            # Pydantic v2
            all_params = engine.model_dump(
                exclude={"id", "name", "engine_type", "description"}
            )
            # Filter out None values and complex objects
            engine_params = {
                k: v
                for k, v in all_params.items()
                if v is not None and not isinstance(v, (BaseModel, dict, list))
            }
        elif hasattr(engine, "dict"):
            # Pydantic v1
            all_params = engine.dict(
                exclude={"id", "name", "engine_type", "description"}
            )
            # Filter out None values and complex objects
            engine_params = {
                k: v
                for k, v in all_params.items()
                if v is not None and not isinstance(v, (BaseModel, dict, list))
            }

        # Add engine parameters to both global config and engine-specific sections
        if engine_params:
            # Add by engine ID (most specific)
            engine_id = getattr(engine, "id", str(uuid.uuid4()))
            config["configurable"]["engine_configs"][engine_id] = engine_params

            # Add by engine name (for convenience)
            engine_name = getattr(engine, "name", "default_engine")
            config["configurable"]["engine_configs"][engine_name] = engine_params

            # Also add by engine type if available (least specific)
            engine_type = getattr(engine, "engine_type", None)
            if engine_type:
                type_key = f"{engine_type.value}_config"
                config["configurable"]["engine_configs"][type_key] = engine_params

            # Add common LLM parameters to the global scope for convenience
            common_params = ["model", "temperature", "max_tokens"]
            for param in common_params:
                if param in engine_params:
                    config["configurable"][param] = engine_params[param]

        return config

    @staticmethod
    def create_with_metadata(
        metadata: dict[str, Any],
        thread_id: str | None = None,
        user_id: str | None = None,
        **kwargs,
    ) -> RunnableConfig:
        """Create a RunnableConfig with metadata.

        Useful for tracing, logging, and debugging.

        Args:
            metadata: Dictionary of metadata values
            thread_id: Optional thread ID
            user_id: Optional user ID
            **kwargs: Additional configurable parameters

        Returns:
            RunnableConfig with metadata section
        """
        # Create base config
        config = RunnableConfigManager.create(
            thread_id=thread_id, user_id=user_id, **kwargs
        )

        # Add metadata section
        config["metadata"] = metadata

        return config

    @staticmethod
    def merge(base: RunnableConfig, override: RunnableConfig) -> RunnableConfig:
        """Merge two RunnableConfigs, with override taking precedence.

        Args:
            base: Base configuration
            override: Configuration that takes precedence

        Returns:
            Merged configuration
        """
        # Start with a deep copy of base
        result = copy.deepcopy(base)

        # Merge configurable section
        if "configurable" in override:
            if "configurable" not in result:
                result["configurable"] = {}

            for key, value in override["configurable"].items():
                # Special handling for engine_configs to do a deep merge
                if (
                    key == "engine_configs"
                    and "engine_configs" in result["configurable"]
                ):
                    for engine_name, engine_config in override["configurable"][
                        "engine_configs"
                    ].items():
                        if engine_name in result["configurable"]["engine_configs"]:
                            # Merge existing engine config
                            result["configurable"]["engine_configs"][
                                engine_name
                            ].update(engine_config)
                        else:
                            # Add new engine config
                            result["configurable"]["engine_configs"][
                                engine_name
                            ] = engine_config
                else:
                    # Regular key overwrite
                    result["configurable"][key] = value

        # Merge metadata if present
        if "metadata" in override:
            if "metadata" not in result:
                result["metadata"] = {}

            result["metadata"].update(override["metadata"])

        # Merge other top-level keys
        for key, value in override.items():
            if key not in ["configurable", "metadata"]:
                result[key] = value

        return result

    @staticmethod
    def get_thread_id(config: RunnableConfig) -> str | None:
        """Extract thread_id from a RunnableConfig.

        Args:
            config: RunnableConfig to extract from

        Returns:
            thread_id if present, otherwise None
        """
        return RunnableConfigManager.extract_value(config, "thread_id")

    @staticmethod
    def get_user_id(config: RunnableConfig) -> str | None:
        """Extract user_id from a RunnableConfig.

        Args:
            config: RunnableConfig to extract from

        Returns:
            user_id if present, otherwise None
        """
        return RunnableConfigManager.extract_value(config, "user_id")

    @staticmethod
    def extract_value(config: RunnableConfig, key: str, default: Any = None) -> Any:
        """Extract a value from RunnableConfig's configurable section.

        Args:
            config: RunnableConfig to extract from
            key: Key to extract
            default: Default value if key not found

        Returns:
            Extracted value or default
        """
        if config and "configurable" in config and key in config["configurable"]:
            return config["configurable"][key]
        return default

    @staticmethod
    def extract_engine_config(
        config: RunnableConfig, engine_name: str
    ) -> dict[str, Any]:
        """Extract engine-specific configuration.

        Args:
            config: RunnableConfig to extract from
            engine_name: Name of the engine to extract config for

        Returns:
            Engine-specific configuration dictionary
        """
        if (
            config
            and "configurable" in config
            and "engine_configs" in config["configurable"]
            and engine_name in config["configurable"]["engine_configs"]
        ):
            return config["configurable"]["engine_configs"][engine_name]
        return {}

    @staticmethod
    def extract_engine_type_config(
        config: RunnableConfig, engine_type: str
    ) -> dict[str, Any]:
        """Extract configuration for a specific engine type.

        Args:
            config: RunnableConfig to extract from
            engine_type: The engine type (e.g., "llm", "retriever")

        Returns:
            Configuration for the engine type
        """
        type_key = f"{engine_type}_config"
        return RunnableConfigManager.extract_engine_config(config, type_key)

    @staticmethod
    def add_engine_config(
        config: RunnableConfig, engine_name: str, **params
    ) -> RunnableConfig:
        """Add engine-specific configuration.

        Args:
            config: RunnableConfig to add to
            engine_name: Name of the engine to add config for
            **params: Configuration parameters for the engine

        Returns:
            Updated RunnableConfig
        """
        result = copy.deepcopy(config)

        if "configurable" not in result:
            result["configurable"] = {}

        # Create or update engine_configs section
        if "engine_configs" not in result["configurable"]:
            result["configurable"]["engine_configs"] = {}

        # Create engine config if it doesn't exist
        if engine_name not in result["configurable"]["engine_configs"]:
            result["configurable"]["engine_configs"][engine_name] = {}

        # Add or update parameters
        for key, value in params.items():
            result["configurable"]["engine_configs"][engine_name][key] = value

        return result

    @staticmethod
    def add_engine(config: RunnableConfig, engine: Any) -> RunnableConfig:
        """Add an engine's parameters to the RunnableConfig.

        Args:
            config: RunnableConfig to add to
            engine: Engine to add

        Returns:
            Updated RunnableConfig
        """
        result = copy.deepcopy(config)

        # Extract engine parameters
        engine_params = {}

        # Try extract_params method first (preferred)
        if hasattr(engine, "extract_params"):
            engine_params = engine.extract_params()
        # Fall back to model_dump/dict
        elif hasattr(engine, "model_dump"):
            # Pydantic v2
            engine_params = engine.model_dump(
                exclude={"name", "engine_type", "description"}
            )
        elif hasattr(engine, "dict"):
            # Pydantic v1
            engine_params = engine.dict(exclude={"name", "engine_type", "description"})

        # Get engine identifiers
        engine_id = getattr(engine, "id", None)
        engine_name = getattr(engine, "name", "default_engine")

        # Add to config by ID if available
        if engine_id:
            result = RunnableConfigManager.add_engine_config(
                result, engine_id, **engine_params
            )

        # Add by engine name
        result = RunnableConfigManager.add_engine_config(
            result, engine_name, **engine_params
        )

        # Also add by engine type if available
        engine_type = getattr(engine, "engine_type", None)
        if engine_type:
            type_key = f"{engine_type.value}_config"
            result = RunnableConfigManager.add_engine_config(
                result, type_key, **engine_params
            )

        return result

    @staticmethod
    def from_dict(input_dict: dict[str, Any]) -> RunnableConfig:
        """Create a RunnableConfig from a dictionary.

        Args:
            input_dict: Dictionary to convert

        Returns:
            Properly structured RunnableConfig
        """
        if "configurable" in input_dict:
            # Already in correct format
            return input_dict

        # Convert to proper format
        return {"configurable": input_dict}

    @staticmethod
    def from_model(model: BaseModel) -> RunnableConfig:
        """Create a RunnableConfig from a Pydantic model.

        Args:
            model: Pydantic model to convert

        Returns:
            Properly structured RunnableConfig
        """
        # Convert model to dict
        if hasattr(model, "model_dump"):
            # Pydantic v2
            model_dict = model.model_dump()
        else:
            # Pydantic v1
            model_dict = model.dict()

        return RunnableConfigManager.from_dict(model_dict)

    @staticmethod
    def to_model(config: RunnableConfig, model_cls: type[BaseModel]) -> BaseModel:
        """Convert a RunnableConfig to a Pydantic model.

        Args:
            config: RunnableConfig to convert
            model_cls: Pydantic model class to convert to

        Returns:
            Instantiated model
        """
        if "configurable" in config:
            return model_cls(**config["configurable"])
        return model_cls(**config)
