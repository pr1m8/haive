import math
import uuid
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

from pydantic import BaseModel, Field, field_validator


class TreeNode(BaseModel):
    """Non-recursive tree node for LATS."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    parent_id: Optional[str] = None
    children_ids: List[str] = Field(default_factory=list)

    # Node content
    messages: List[Dict[str, Any]] = Field(default_factory=list)
    action: Optional[Dict[str, Any]] = None  # Tool call if any
    tool_response: Optional[Dict[str, Any]] = None

    # Search metrics
    value: float = 0.0
    visits: int = 0
    depth: int = 1

    # Reflection results
    reflection_score: float = 0.0
    reflection_text: str = ""
    is_solved: bool = False
    is_terminal: bool = False

    def uct_score(self, parent_visits: int, exploration_weight: float = 1.0) -> float:
        """Calculate Upper Confidence Bound for tree search."""
        if self.visits == 0:
            return float("inf")  # Unexplored nodes have highest priority

        average_reward = self.value / self.visits
        exploration_term = math.sqrt(math.log(parent_visits) / self.visits)
        return average_reward + exploration_weight * exploration_term

    class Config:
        arbitrary_types_allowed = True


# Agent output models
class Reflection(BaseModel):
    """Output from reflection agent."""

    reflections: str = Field(
        description="Critique and reflections on the response quality"
    )
    score: float = Field(
        ge=0,
        le=10,
        description="Score from 0-10 on the quality of the candidate response",
    )
    found_solution: bool = Field(
        description="Whether the response has fully solved the question or task"
    )

    @property
    def normalized_score(self) -> float:
        return self.score / 10.0


class CandidateActions(BaseModel):
    """Output from expansion agent."""

    candidates: List[Dict[str, Any]] = Field(
        description="List of candidate next actions (tool calls or responses)"
    )
    reasoning: str = Field(description="Reasoning for the selected candidates")


class SelectionDecision(BaseModel):
    """Output from selection agent."""

    selected_node_id: str = Field(description="ID of the node to expand from")
    should_terminate: bool = Field(description="Whether to end the search")
    termination_reason: Optional[str] = None
