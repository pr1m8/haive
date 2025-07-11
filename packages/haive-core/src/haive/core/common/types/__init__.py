"""Common type definitions used throughout the Haive framework.

This module provides type definitions that are used across different components
of the Haive system for consistent type hinting and improved code clarity.
"""

import os
from pathlib import Path
from typing import Any, Dict, Union

# JSON-compatible type (dict, list, str, int, float, bool, None)
JsonType = Union[dict[str, Any], list, str, int, float, bool, None]

# Dictionary with string keys and any values
DictStrAny = dict[str, Any]

# String or Path-like object
StrOrPath = Union[str, Path, os.PathLike]
