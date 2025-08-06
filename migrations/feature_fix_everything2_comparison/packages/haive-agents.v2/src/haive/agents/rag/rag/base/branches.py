"""Branches core module.

This module provides branches functionality for the Haive framework.
"""

from __future__ import annotations

from haive.core.graph.branches import Branch

branch_logic = Branch(
    key="documents",
    comparison="exists",
    destinations={True: "generate", False: "transform_query"},
)
