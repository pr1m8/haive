from typing import List, Dict, Any, Optional, Union, Literal
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from src.haive.games.framework.base.state import GameState

class DebateMove(BaseModel):
    """A move made by a participant in a debate/conversation."""
    participant_id: str = Field(..., description="ID of the participant making the move")
    content: str = Field(..., description="Content of the move (argument, statement, etc.)")
    move_type: str = Field(default="statement", description="Type of move (opening, argument, closing, etc.)")
    round_number: Optional[int] = Field(default=None, description="Round number for this move")
    references: List[str] = Field(default_factory=list, description="References/citations used in this move")
    
    def __str__(self) -> str:
        """String representation of the move."""
        return f"{self.participant_id}: {self.content[:50]}..."

class VoteResult(BaseModel):
    """A vote from a judge/evaluator."""
    voter_id: str = Field(..., description="ID of the voter")
    personality: str = Field(..., description="Description of the voter's personality")
    vote: str = Field(..., description="Who or what the voter voted for")
    reasoning: str = Field(..., description="Reasoning for the vote")
    score: Optional[Dict[str, float]] = Field(default=None, description="Optional numerical scores")
    
    def __str__(self) -> str:
        """String representation of the vote."""
        return f"{self.voter_id} voted for {self.vote}"

class DebateParticipant(BaseModel):
    """Information about a debate participant."""
    id: str = Field(..., description="Unique identifier for the participant")
    name: str = Field(..., description="Display name for the participant")
    role: str = Field(default="debater", description="Role in the debate (debater, judge, moderator)")
    position: Optional[str] = Field(default=None, description="Position or stance of the participant")
    personality: Optional[str] = Field(default=None, description="Personality description for the participant")
    system_prompt: Optional[str] = Field(default=None, description="System prompt for this participant's LLM")
    
    def __str__(self) -> str:
        """String representation of the participant."""
        return f"{self.name} ({self.role})"
