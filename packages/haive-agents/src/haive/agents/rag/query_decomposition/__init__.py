"""Query Decomposition Module.

Modular query decomposition agents that break complex queries into manageable sub-queries.
Can be plugged into any RAG workflow with compatible I/O schemas.
"""

from .agent import (
    AdaptiveQueryDecomposerAgent,
    ContextualQueryDecomposerAgent,
    HierarchicalQueryDecomposerAgent,
    QueryDecomposerAgent,
)

__all__ = [
    "AdaptiveQueryDecomposerAgent",
    "ContextualQueryDecomposerAgent",
    "HierarchicalQueryDecomposerAgent",
    "QueryDecomposerAgent",
]
