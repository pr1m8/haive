# src/haive/games/debate/models.py
from typing import List, Dict, Optional, Union, Literal
from pydantic import BaseModel, Field
from src.haive.games.framework.multi_player.models import GamePhase
from enum import Enum
class Statement(BaseModel):
    """Represents a single statement in a debate or discussion."""
    content: str = Field(..., description="The text of the statement")
    speaker_id: str = Field(..., description="ID of the speaker")
    target_id: Optional[str] = Field(None, description="ID of targeted participant (if any)")
    statement_type: str = Field("general", description="Type of statement (question, rebuttal, etc.)")
    references: List[str] = Field(default_factory=list, description="References or citations")
    sentiment: Optional[float] = Field(None, description="Sentiment score if applicable")
    timestamp: str = Field(..., description="When the statement was made")

class Topic(BaseModel):
    """Represents a debate topic or question."""
    title: str = Field(..., description="Title of the topic")
    description: str = Field(..., description="Detailed description of the topic")
    keywords: List[str] = Field(default_factory=list, description="Key terms related to topic")
    constraints: Optional[Dict[str, str]] = Field(None, description="Any constraints on discussion")
    
class Participant(BaseModel):
    """Represents a participant in the debate."""
    id: str = Field(..., description="Unique identifier for participant")
    name: str = Field(..., description="Display name of participant")
    role: str = Field(..., description="Role in the debate (moderator, debater, etc.)")
    position: Optional[str] = Field(None, description="Position on topic (pro/con/neutral)")
    persona: Optional[Dict[str, str]] = Field(None, description="Personality traits and characteristics")
    expertise: List[str] = Field(default_factory=list, description="Areas of expertise")
    bias: Optional[float] = Field(None, description="Bias level (-1.0 to 1.0)")
    
class Vote(BaseModel):
    """Represents a vote from a participant."""
    voter_id: str = Field(..., description="ID of the voter")
    vote_value: Union[str, int, float] = Field(..., description="Value of the vote")
    target_id: Optional[str] = Field(None, description="Target of the vote if applicable")
    reason: Optional[str] = Field(None, description="Reasoning behind the vote")

class DebatePhase(str, Enum):
    """Phases specific to debate-style interactions."""
    SETUP = "setup"
    OPENING_STATEMENTS = "opening_statements"
    DISCUSSION = "discussion"
    REBUTTAL = "rebuttal"
    QUESTIONS = "questions"
    CLOSING_STATEMENTS = "closing_statements"
    VOTING = "voting"
    JUDGMENT = "judgment"
    CONCLUSION = "conclusion"