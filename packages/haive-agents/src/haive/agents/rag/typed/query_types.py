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
