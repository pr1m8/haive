"""Docstring Fixers Module.

This module contains specialized fixers for different types of docstring issues
identified by pydocstyle. Each fixer targets specific error codes and applies
automated corrections.

Available Fixers:
    D415Fixer: Fix missing punctuation at end of first line
    D205Fixer: Add missing blank lines after summary
    D202Fixer: Remove extra blank lines after docstring
    D100Fixer: Add missing module docstrings
    D102Fixer: Add missing method docstrings
    D107Fixer: Add missing __init__ docstrings
"""

from .base_fixer import BaseFixer
from .d100_d107_simple_fixer import (
    CombinedD100D107Fixer,
    D100SimpleFixer,
    D107SimpleFixer,
)
from .d202_fixer import D202Fixer
from .d212_fixer import D212Fixer
from .d403_fixer import D403Fixer
from .d415_fixer import D415Fixer

__all__ = [
    "D415Fixer",
    "D202Fixer",
    "D403Fixer",
    "D212Fixer",
    "BaseFixer",
    "D100SimpleFixer",
    "D107SimpleFixer",
    "CombinedD100D107Fixer",
]
