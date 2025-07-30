"""Query_Types core module.

This module provides query types functionality for the Haive framework.

Classes:
    QueryCategory: QueryCategory implementation.
"""

from enum import Enum


class QueryCategory(str, Enum):
    """Categories of queries for specialized handling."""

    FACTOID = "factoid"
    CAUSAL = "causal"
    COMPARATIVE = "comparative"
    TEMPORAL = "temporal"
    PROCEDURAL = "procedural"
    COUNTERFACTUAL = "counterfactual"
    DEFINITIONAL = "definitional"
    QUANTITATIVE = "quantitative"
