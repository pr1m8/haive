# src/haive/core/engine/agent/registry.py

"""Agent registry module for managing and resolving agent classes.

This module provides a registry for associating agent configurations with
their implementing classes, allowing dynamic discovery and resolution.
"""

import importlib
import logging

logger = logging.getLogger(__name__)

# Global registry mapping config classes to agent classes
AGENT_REGISTRY: dict[type, type] = {}


def register_agent(config_class: type):
    """Register an agent class with its configuration class.

    Args:
        config_class: The agent config class to register

    Returns:
        A decorator function that registers the agent class
    """

    def decorator(agent_class: type):
        AGENT_REGISTRY[config_class] = agent_class
        logger.debug(
            f"Registered agent {agent_class.__name__} for config {config_class.__name__}"
        )
        return agent_class

    return decorator


def resolve_agent_class(config_class: type) -> type | None:
    """Resolve an agent class for a given config class.

    First checks the registry, then tries to resolve by naming convention,
    looking in the same module or sibling modules.

    Args:
        config_class: The agent config class to find an implementation for

    Returns:
        The agent class if found, None otherwise
    """
    # Try to find agent class in registry
    agent_class = AGENT_REGISTRY.get(config_class)

    # Try class attribute if not in registry
    if agent_class is None and hasattr(config_class, "agent_class"):
        agent_class = config_class.agent_class

    # Try to resolve by naming convention
    if agent_class is None:
        agent_class = _resolve_agent_class_by_name(config_class)

    if agent_class is None:
        logger.warning(f"No agent class found for {config_class.__name__}")

    return agent_class


def _resolve_agent_class_by_name(config_class: type) -> type | None:
    """Try to resolve agent class by naming convention.

    Args:
        config_class: The agent config class to find an implementation for

    Returns:
        The agent class if found, None otherwise
    """
    agent_class_name = config_class.__name__.replace("Config", "")

    # Try same module
    try:
        module = importlib.import_module(config_class.__module__)
        agent_class = getattr(module, agent_class_name, None)
        if agent_class:
            return agent_class
    except (ImportError, AttributeError):
        pass

    # Try sibling module
    try:
        base_module = config_class.__module__.rsplit(".", 1)[0]
        for suffix in ["agent", "impl", ""]:
            try:
                agent_module = importlib.import_module(f"{base_module}.{suffix}")
                agent_class = getattr(agent_module, agent_class_name, None)
                if agent_class:
                    return agent_class
            except (ImportError, AttributeError):
                continue
    except Exception:
        pass

    return None


def register_agents_from_module(module_path: str) -> int:
    """Register all agents from a module.

    Args:
        module_path: The module path to scan for agents

    Returns:
        Number of agents registered
    """
    try:
        module = importlib.import_module(module_path)
        count = 0

        for name in dir(module):
            obj = getattr(module, name)

            # Look for classes with a ClassVar[Type] annotation named "config_class"
            if isinstance(obj, type) and hasattr(obj, "__annotations__"):
                annotations = getattr(obj, "__annotations__", {})
                if "config_class" in annotations:
                    config_class = getattr(obj, "config_class", None)
                    if config_class and isinstance(config_class, type):
                        AGENT_REGISTRY[config_class] = obj
                        count += 1
                        logger.debug(
                            f"Registered agent {obj.__name__} for config {config_class.__name__}"
                        )

        return count
    except ImportError as e:
        logger.error(f"Error importing module {module_path}: {e}")
        return 0
