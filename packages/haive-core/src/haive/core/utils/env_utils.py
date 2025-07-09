# src/haive.core/utils/env_utils.py

import logging
import os
from pathlib import Path
from typing import Any, TypeVar

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

T = TypeVar("T")


def load_env_file(
    filepath: str | Path | None = None, override: bool = False
) -> dict[str, str]:
    """Load environment variables from a .env file.

    Args:
        filepath: Path to the .env file. If None, will try to find .env in parent directories.
        override: Whether to override existing environment variables.

    Returns:
        Dictionary of loaded environment variables.
    """
    # Handle None filepath - search for .env in parent directories
    if filepath is None:
        # Start from current working directory
        current_dir = Path.cwd()

        # Look for .env in current and parent directories (up to 5 levels)
        for _ in range(5):
            env_path = current_dir / ".env"
            if env_path.exists():
                filepath = env_path
                break
            # Move to parent directory
            parent_dir = current_dir.parent
            if parent_dir == current_dir:  # Reached root
                break
            current_dir = parent_dir

    # Convert filepath to Path if it's a string
    if isinstance(filepath, str):
        filepath = Path(filepath)

    # If no file found or specified
    if filepath is None or not filepath.exists():
        logger.warning(f"No .env file found at {filepath or 'any parent directory'}")
        return {}

    # Load the file
    logger.info(f"Loading environment variables from {filepath}")
    loaded_vars = {}

    # Use dotenv to load the file
    load_dotenv(filepath, override=override)

    # Get loaded variables for return value
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith("#"):
                continue
            # Parse key-value pairs
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                # Only include if the variable exists in os.environ
                if key in os.environ:
                    loaded_vars[key] = os.environ[key]

    return loaded_vars


def get_env_var(
    name: str,
    default: Any = None,
    cast_to: type[T] | None = None,
    required: bool = False,
) -> str | T | None:
    """Get an environment variable with optional casting and default value.

    Args:
        name: Name of the environment variable
        default: Default value if variable is not set
        cast_to: Type to cast the value to (int, float, bool, etc.)
        required: Whether the variable is required (raises error if missing)

    Returns:
        The environment variable value, cast to the specified type if provided

    Raises:
        ValueError: If required is True and the variable is not set
    """
    value = os.environ.get(name)

    # Handle missing variable
    if value is None:
        if required:
            raise ValueError(f"Required environment variable '{name}' is not set")
        return default

    # Cast value if requested
    if cast_to is not None:
        try:
            if cast_to is bool:
                # Special handling for boolean values
                return cast_to(value.lower() in ("true", "yes", "1", "y"))
            return cast_to(value)
        except (ValueError, TypeError) as e:
            logger.warning(
                f"Failed to cast environment variable '{name}' to {cast_to.__name__}: {e}"
            )
            return default

    return value


def load_project_env_files() -> dict[str, str]:
    """Load environment variables from multiple locations in the project.

    Searches for and loads .env files in this priority order:
    1. Project root .env (base settings)
    2. Package-specific .env (can override root settings)
    3. Local development .env (highest priority, not in version control)

    Returns:
        Dictionary of loaded environment variables
    """
    loaded_vars = {}

    # Get module path to find project root
    module_path = Path(__file__)

    # Navigate to project root (src/haive.core/utils → src/haive.core → src → packages/haive-core → packages → project_root)
    project_root = module_path.parent.parent.parent.parent.parent.parent

    # Load from project root
    root_env = project_root / ".env"
    if root_env.exists():
        loaded_vars.update(load_env_file(root_env))

    # Find which package we're in
    package_dir = (
        module_path.parent.parent.parent.parent
    )  # src/haive.core/utils → src/haive.core → src → packages/haive-core

    # Load package-specific .env
    package_env = package_dir / ".env"
    if package_env.exists():
        loaded_vars.update(load_env_file(package_env))

    # Load local development .env (highest priority, typically gitignored)
    local_env = project_root / ".env.local"
    if local_env.exists():
        loaded_vars.update(load_env_file(local_env, override=True))

    return loaded_vars


def is_production() -> bool:
    """Check if the application is running in production mode."""
    return get_env_var("ENV", "development").lower() == "production"


def is_development() -> bool:
    """Check if the application is running in development mode."""
    return get_env_var("ENV", "development").lower() == "development"


def is_test() -> bool:
    """Check if the application is running in test mode."""
    return get_env_var("ENV", "development").lower() == "test"


def is_testing() -> bool:
    """Alias for is_test(). Check if the application is running in test mode."""
    return is_test()
