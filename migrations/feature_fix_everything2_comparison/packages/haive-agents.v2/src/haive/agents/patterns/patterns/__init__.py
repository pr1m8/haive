"""Agent patterns module.

This module provides reusable patterns for combining agents in various ways.
"""

from haive.agents.patterns.sequential_with_structured_output import (
    SequentialAgentWithStructuredOutput,
    SequentialHooks,
    create_analysis_to_report,
    create_react_to_structured,
)

__all__ = [
    "SequentialAgentWithStructuredOutput",
    "SequentialHooks",
    "create_analysis_to_report",
    "create_react_to_structured",
]
