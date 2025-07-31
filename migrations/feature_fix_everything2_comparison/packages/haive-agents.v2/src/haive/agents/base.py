"""Compatibility module for legacy imports.

This module provides compatibility for legacy imports from haive.agents.multi.base.
New code should import from haive.agents.multi.clean instead.

The modern implementation uses string-based execution modes instead of enums:
- "sequential" for sequential execution
- "parallel" for parallel execution
- "conditional" for conditional routing
- "branch" for branching logic
- "infer" for automatic sequence inference (default)
"""

# Import ExecutionMode from the archived implementation for backward compatibility
from haive.agents.multi.archive.base import ExecutionMode

# Import everything from the current implementation (clean.py is the modern approach)
from haive.agents.multi.clean import MultiAgent

# Create aliases for backward compatibility
# Note: These all resolve to MultiAgent since the modern implementation
# uses execution_mode strings instead of separate classes
SequentialAgent = MultiAgent
ConditionalAgent = MultiAgent
ParallelAgent = MultiAgent
BranchAgent = MultiAgent

# Export the main classes
__all__ = [
    "BranchAgent",
    "ConditionalAgent",
    "ExecutionMode",  # For legacy code that still uses the enum
    "MultiAgent",
    "ParallelAgent",
    "SequentialAgent",
]
