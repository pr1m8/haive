from agents.mcts.models import TreeNode
from pydantic import BaseModel, Field


class TreeState(BaseModel):
    """State schema for MCTS Agent."""

    root: TreeNode = Field(description="The root node of the tree")
    input: str = Field(description="The input to the agent")
