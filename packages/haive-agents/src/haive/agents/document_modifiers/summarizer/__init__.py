"""Summarizer document modifiers.

This module provides tools for summarizing documents using various strategies.
"""

# Import classes from submodules
try:
    from .base import SummarizerAgent
except ImportError:
    SummarizerAgent = None

try:
    from .iterative_refinement.iterative_summarizer import IterativeSummarizer
except ImportError:
    IterativeSummarizer = None

__all__ = [
    "IterativeSummarizer",
    "SummarizerAgent",
]
