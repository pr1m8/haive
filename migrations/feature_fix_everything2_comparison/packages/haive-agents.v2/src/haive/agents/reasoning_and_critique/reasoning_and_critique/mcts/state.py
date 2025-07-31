from pydantic import BaseModel, Field

from haive.agents.reasoning_and_critique.mcts.models import TreeNode


class TreeState(BaseModel):
    """State schema for MCTS Agent."""

    root: TreeNode = Field(description="The root node of the tree")
    input: str = Field(description="The input to the agent")
