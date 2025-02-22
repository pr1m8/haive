from typing_extensions import TypedDict
from src.haive.agents.lats.node import Node
from pydantic import Field
class TreeState(TypedDict):
    """The state of the tree"""
    # The full tree
    root: Node = Field(...,description="The root node of the tree")
    # The original input
    input: str = Field(...,description="The original input")