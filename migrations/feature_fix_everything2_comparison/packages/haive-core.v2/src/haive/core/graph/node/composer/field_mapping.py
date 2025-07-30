"""Field mapping for flexible node I/O configuration.

This module provides the core data structures for mapping fields between source and
target paths with optional transformations.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class FieldMapping:
    """Configuration for mapping a field from source to target.

    This is a simple dataclass that holds the mapping configuration.
    No __init__ method per Pydantic patterns - just data.

    Attributes:
        source_path: Path to extract value from (e.g., "messages", "result")
        target_path: Path to place value in update (e.g., "potato", "output")
        transform: Optional list of transform function names to apply
        default: Default value if source is missing or None
        required: Whether to raise error if source is missing

    Examples:
        # Simple field rename
        FieldMapping("result", "potato")

        # With transform
        FieldMapping("content", "text", transform=["strip", "uppercase"])

        # With default
        FieldMapping("temperature", "temp", default=0.7)
    """

    source_path: str
    target_path: str
    transform: list[str] | None = None
    default: Any = None
    required: bool = False
