"""Query_Types core module.

This module provides query types functionality for the Haive framework.

Classes:
    QueryType: QueryType implementation.
"""

from enum import Enum


class QueryType(str, Enum):
    """Types of queries that can be handled by specialized strategies."""

    FACTUAL = "factual"
    ANALYTICAL = "analytical"
    TEMPORAL = "temporal"
    RELATIONAL = "relational"
