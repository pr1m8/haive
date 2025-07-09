# src/haive/core/utils/config_utils.py

import logging
from typing import Any

from langchain_core.runnables import RunnableConfig

logger = logging.getLogger(__name__)


def apply_config_to_app(app: Any, config: RunnableConfig | None = None) -> Any:
    """Apply a config to an app after compilation.

    Args:
        app: The compiled application
        config: The config to apply

    Returns:
        The app with config applied
    """
    if not config:
        return app

    # Check if app supports with_config
    if hasattr(app, "with_config"):
        try:
            return app.with_config(**config)
        except Exception as e:
            logger.warning(f"Error applying config to app: {e}")
            logger.debug("Falling back to original app")

    return app


def prepare_compile_kwargs(
    checkpointer=None, default_config=None, **kwargs
) -> dict[str, Any]:
    """Prepare kwargs for StateGraph.compile() method, filtering out unsupported parameters.

    Args:
        checkpointer: Optional checkpoint saver
        default_config: Config that won't be passed to compile but will be applied after
        **kwargs: Additional compilation parameters

    Returns:
        Dictionary of supported compile kwargs
    """
    # Start with safe parameters
    compile_kwargs = {}

    # Add checkpointer if provided
    if checkpointer:
        compile_kwargs["checkpointer"] = checkpointer

    # Add other kwargs, excluding default_config
    for k, v in kwargs.items():
        if k != "default_config":
            compile_kwargs[k] = v

    return compile_kwargs
