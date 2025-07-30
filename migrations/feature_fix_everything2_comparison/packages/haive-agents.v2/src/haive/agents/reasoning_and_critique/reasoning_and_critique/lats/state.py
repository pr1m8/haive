"""State core module.

This module provides state functionality for the Haive framework.

Classes:
    TreeState: TreeState implementation.
"""

from typing_extensions import TypedDict

from haive.agents.reasoning_and_critique.lats.node import Node


class TreeState(TypedDict):
    # The full tree
    root: Node
    # The original input
    input: str
