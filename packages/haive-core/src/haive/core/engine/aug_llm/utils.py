"""
Utility functions for working with AugLLMConfig instances.

This module provides helper functions for composing, managing, and utilizing
augmented LLM runnables within the Haive framework. The utilities here enable
flexible configuration management, runtime composition, and chain construction
for augmented language models.

Key functionalities include:
- Creating runnables from configuration objects
- Managing collections of runnables
- Chaining runnables together
- Merging configuration dictionaries with special handling for LLM settings
"""

import copy
import logging
from typing import Any, Dict, List, Optional, TypeVar, Union

from langchain_core.runnables import Runnable, RunnableConfig

from haive.core.engine.aug_llm.config import AugLLMConfig

# Type for runnable configs
T = TypeVar("T")

logger = logging.getLogger(__name__)


def compose_runnable(
    aug_llm_config: AugLLMConfig, runnable_config: Optional[RunnableConfig] = None
) -> Runnable:
    """
    Compose a runnable LLM chain from an AugLLMConfig.

    Creates a ready-to-use runnable object from the provided configuration,
    applying any runtime configuration overrides as needed.

    Args:
        aug_llm_config (AugLLMConfig): Configuration object for the LLM chain,
            containing all the necessary settings and components.
        runnable_config (Optional[RunnableConfig]): Optional runtime configuration
            overrides to apply when creating the runnable.

    Returns:
        Runnable: A fully composed, executable LLM chain.

    Raises:
        Exception: Any exceptions from the underlying creation process are logged
            and re-raised.

    Examples:
        >>> from haive.core.engine.aug_llm.config import AugLLMConfig
        >>> config = AugLLMConfig(name="my_llm", model="gpt-4")
        >>> runnable = compose_runnable(config)
        >>> result = runnable.invoke("Hello, world!")
    """
    try:
        return aug_llm_config.create_runnable(runnable_config)
    except Exception as e:
        logger.error(f"Error composing runnable: {e}")
        raise


def create_runnables_dict(
    runnables: Union[List[AugLLMConfig], Dict[str, AugLLMConfig], AugLLMConfig],
) -> Dict[str, AugLLMConfig]:
    """
    Create a dictionary mapping names to runnable configs from various input formats.

    Normalizes different input formats (list, dictionary, or single config) into
    a consistent dictionary format mapping names to configurations. This is useful
    for managing collections of runnables in a standardized way.

    Args:
        runnables (Union[List[AugLLMConfig], Dict[str, AugLLMConfig], AugLLMConfig]):
            LLM configs in various formats:
            - List of AugLLMConfig objects (uses their names as keys)
            - Dictionary mapping names to AugLLMConfig objects
            - Single AugLLMConfig object (uses its name as key)

    Returns:
        Dict[str, AugLLMConfig]: Dictionary mapping names to AugLLMConfig objects.
        Returns an empty dictionary if the input cannot be processed.

    Examples:
        >>> from haive.core.engine.aug_llm.config import AugLLMConfig
        >>> config1 = AugLLMConfig(name="llm1", model="gpt-4")
        >>> config2 = AugLLMConfig(name="llm2", model="claude-3")
        >>>
        >>> # From list
        >>> configs_dict = create_runnables_dict([config1, config2])
        >>> list(configs_dict.keys())
        ['llm1', 'llm2']
        >>>
        >>> # From dictionary
        >>> configs_dict = create_runnables_dict({"custom_name": config1})
        >>> list(configs_dict.keys())
        ['custom_name']
        >>>
        >>> # From single config
        >>> configs_dict = create_runnables_dict(config1)
        >>> list(configs_dict.keys())
        ['llm1']
    """
    # Handle list input
    if isinstance(runnables, list):
        return {runnable.name: runnable for runnable in runnables}

    # Handle dictionary input
    if isinstance(runnables, dict):
        return runnables

    # Handle single runnable
    if hasattr(runnables, "name"):
        return {runnables.name: runnables}

    # Fallback
    logger.warning(
        f"Unsupported input type for create_runnables_dict: {type(runnables)}"
    )
    return {}


def compose_runnables_from_dict(
    runnables: Dict[str, Union[AugLLMConfig, Any]],
    runnable_config: Optional[RunnableConfig] = None,
) -> Dict[str, Runnable]:
    """
    Compose and return a dictionary of runnables from a dictionary of configs.

    Takes a dictionary mapping names to configurations and returns a dictionary
    mapping the same names to fully composed, executable runnables. This is useful
    for bulk-creating multiple runnables with consistent configuration.

    Args:
        runnables (Dict[str, Union[AugLLMConfig, Any]]): Dictionary mapping names
            to configuration objects. Objects must have a create_runnable method.
        runnable_config (Optional[RunnableConfig]): Optional runtime configuration
            overrides to apply to all runnables.

    Returns:
        Dict[str, Runnable]: Dictionary mapping names to composed runnables.
        Entries that fail to compose are omitted from the result.

    Examples:
        >>> from haive.core.engine.aug_llm.config import AugLLMConfig
        >>> configs = {
        ...     "qa": AugLLMConfig(name="qa_llm", model="gpt-4"),
        ...     "summarizer": AugLLMConfig(name="summary_llm", model="claude-3")
        ... }
        >>> runnables = compose_runnables_from_dict(configs)
        >>> # Use the composed runnables
        >>> qa_response = runnables["qa"].invoke("What is the capital of France?")
        >>> summary = runnables["summarizer"].invoke("Summarize this long text...")
    """
    result = {}
    for key, config in runnables.items():
        try:
            if hasattr(config, "create_runnable"):
                result[key] = compose_runnable(config, runnable_config)
            else:
                logger.warning(f"Config for {key} does not have create_runnable method")
        except Exception as e:
            logger.error(f"Error composing runnable for {key}: {e}")

    return result


def chain_runnables(
    runnables: List[Runnable], override_config: Optional[Dict[str, Any]] = None
) -> Runnable:
    """
    Chain multiple runnables together with optional configuration overrides.

    Creates a composite runnable that passes the output of each runnable to the
    input of the next one in sequence. This is useful for creating processing
    pipelines that transform data through multiple stages.

    Args:
        runnables (List[Runnable]): List of runnables to chain together in sequence.
            The output of each runnable is passed as input to the next one.
        override_config (Optional[Dict[str, Any]]): Optional configuration overrides
            to apply to the final chained runnable.

    Returns:
        Runnable: A composite runnable representing the chain of all input runnables.

    Raises:
        ValueError: If the input list is empty.

    Examples:
        >>> from langchain_core.runnables import Runnable
        >>> # Define some runnables
        >>> prompt_formatter = RunnablePromptFormatter()
        >>> llm = RunnableLLM()
        >>> output_parser = RunnableOutputParser()
        >>>
        >>> # Chain them together
        >>> pipeline = chain_runnables([prompt_formatter, llm, output_parser])
        >>>
        >>> # Use the chained runnable
        >>> result = pipeline.invoke({"question": "What is the capital of France?"})
    """
    if not runnables:
        raise ValueError("No runnables provided to chain")

    if len(runnables) == 1:
        return runnables[0]

    from langchain_core.runnables import chain

    chained = chain(*runnables)

    if override_config:
        chained = chained.with_config(**override_config)

    return chained


def merge_configs(
    base_config: Optional[RunnableConfig], override_config: Optional[RunnableConfig]
) -> RunnableConfig:
    """
    Merge two runnable configs, with override taking precedence.

    Performs a deep merge of two configuration dictionaries, with special handling
    for nested structures like engine_configs. The override values take precedence
    over base values when keys conflict, except for nested dictionaries which are
    merged recursively.

    Args:
        base_config (Optional[RunnableConfig]): Base configuration dictionary to start with.
        override_config (Optional[RunnableConfig]): Configuration dictionary whose values
            will override corresponding values in the base config.

    Returns:
        RunnableConfig: A new configuration dictionary containing the merged values.

    Examples:
        >>> base = {
        ...     "configurable": {
        ...         "temperature": 0.7,
        ...         "engine_configs": {
        ...             "gpt-4": {"max_tokens": 1000}
        ...         }
        ...     }
        ... }
        >>> override = {
        ...     "configurable": {
        ...         "temperature": 0.5,
        ...         "engine_configs": {
        ...             "gpt-4": {"temperature": 0.9}
        ...         }
        ...     }
        ... }
        >>> merged = merge_configs(base, override)
        >>> merged["configurable"]["temperature"]
        0.5
        >>> merged["configurable"]["engine_configs"]["gpt-4"]
        {'max_tokens': 1000, 'temperature': 0.9}
    """
    # Handle None cases
    if not base_config:
        return override_config or {}
    if not override_config:
        return base_config

    # Copy base config to avoid modifying the original
    result = copy.deepcopy(base_config)

    # Ensure configurable section exists
    if "configurable" not in result:
        result["configurable"] = {}

    # Merge configurable section
    if "configurable" in override_config:
        for key, value in override_config["configurable"].items():
            # Special handling for engine_configs section
            if key == "engine_configs" and "engine_configs" in result["configurable"]:
                if not result["configurable"]["engine_configs"]:
                    result["configurable"]["engine_configs"] = {}

                # Merge engine configs
                for engine_name, engine_config in override_config["configurable"][
                    "engine_configs"
                ].items():
                    if engine_name in result["configurable"]["engine_configs"]:
                        # Update existing engine config
                        result["configurable"]["engine_configs"][engine_name].update(
                            engine_config
                        )
                    else:
                        # Add new engine config
                        result["configurable"]["engine_configs"][
                            engine_name
                        ] = engine_config
            else:
                # Regular key override
                result["configurable"][key] = value

    # Handle other top-level sections
    for key, value in override_config.items():
        if key != "configurable":
            result[key] = value

    return result
