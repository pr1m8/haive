"""Knowledge Graph document modifiers.

This module provides tools for transforming documents into knowledge graphs.
"""

# Import classes from submodules
try:
    from .kg_base.kg_transformer import ParallelKGTransformer
except ImportError:
    ParallelKGTransformer = None

try:
    from .kg_iterative_refinement.iterative_graph_transformer import (
        IterativeGraphTransformer,
    )
except ImportError:
    IterativeGraphTransformer = None

try:
    from .kg_map_merge.structured_kg_agent import StructuredKGAgent
except ImportError:
    StructuredKGAgent = None

__all__ = [
    "IterativeGraphTransformer",
    "ParallelKGTransformer",
    "StructuredKGAgent",
]
