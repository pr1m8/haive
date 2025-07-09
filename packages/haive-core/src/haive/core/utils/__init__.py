"""Core utility functions and helpers.

This module provides common utility functions and helpers used throughout
the Haive framework. It includes utilities for Pydantic models, tools,
discovery mechanisms, and other shared functionality.

The utilities are organized into submodules:
    - pydantic_utils: Helpers for working with Pydantic models
    - tools: Tool-related utilities and helpers
    - haive_discovery: Discovery and introspection utilities

Example:
    Basic usage::

        from haive.core.utils import pydantic_utils
        from haive.core.utils.tools import create_tool

        # Use utilities for model operations
        serialized = pydantic_utils.model_to_dict(my_model)

See Also:
    :mod:`haive.core.utils.pydantic_utils`: Pydantic model utilities
    :mod:`haive.core.utils.tools`: Tool creation and management utilities
    :mod:`haive.core.utils.haive_discovery`: Component discovery utilities
"""
