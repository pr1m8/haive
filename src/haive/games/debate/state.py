from src.haive.games.framework.base.state import GameState
from src.haive.games.debate.models import DebateParticipant, DebateMove, VoteResult
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage

class DebateState(GameState):
    """State for a multi-agent debate or conversation.
    
    This extends the base GameState with debate-specific attributes.
    """
    # Debate topic and structure
    topic: str = Field(..., description="Topic of the debate/conversation")
    description: str = Field(default="", description="Description of the debate scenario")
    current_phase: str = Field(default="setup", description="Current phase of the debate")
    phase_sequence: List[str] = Field(default_factory=list, description="Sequence of phases in the debate")
    current_round: int = Field(default=0, description="Current round number")
    max_rounds: int = Field(default=3, description="Maximum number of rounds")
    
    # Participants
    participants: List[DebateParticipant] = Field(default_factory=list, description="List of participants")
    judge_participants: List[str] = Field(default_factory=list, description="IDs of participants who are judges")
    
    # Override GameState fields
    turn: str = Field(default="", description="ID of the participant whose turn it is")
    game_status: str = Field(default="setup", description="Status of the debate")
    move_history: List[DebateMove] = Field(default_factory=list, description="History of moves")
    
    # Voting
    votes: List[VoteResult] = Field(default_factory=list, description="Votes from judges")
    result: Optional[str] = Field(default=None, description="Final result of the debate")
    winner: Optional[str] = Field(default=None, description="Winner of the debate (if applicable)")
    
    # Additional fields
    messages: List[BaseMessage] = Field(default_factory=list, description="Conversation messages")
    references: Dict[str, Any] = Field(default_factory=dict, description="Reference materials for the debate")
    
    def get_transcript(self) -> str:
        """Get a formatted transcript of the debate."""
        transcript = f"# Debate: {self.topic}\n\n"
        transcript += f"{self.description}\n\n"
        
        # Show participants
        transcript += "## Participants\n\n"
        for participant in self.participants:
            if participant.position:
                transcript += f"**{participant.name}**: {participant.position}\n"
            else:
                transcript += f"**{participant.name}** ({participant.role})\n"
        transcript += "\n"
        
        # Show moves by round
        if self.move_history:
            current_round = None
            current_phase = None
            
            for move in self.move_history:
                # Show phase header if it changed
                if move.move_type != current_phase:
                    current_phase = move.move_type
                    transcript += f"## {current_phase.capitalize()}\n\n"
                
                # Show round header if it changed
                if move.round_number != current_round:
                    current_round = move.round_number
                    if current_round is not None:
                        transcript += f"### Round {current_round}\n\n"
                
                # Get participant name
                participant_name = next((p.name for p in self.participants if p.id == move.participant_id), move.participant_id)
                
                # Show the move
                transcript += f"**{participant_name}**: {move.content}\n\n"
                
                # Show references if any
                if move.references:
                    transcript += "References:\n"
                    for ref in move.references:
                        transcript += f"- {ref}\n"
                    transcript += "\n"
        
        # Show votes if any
        if self.votes:
            transcript += "## Votes\n\n"
            for vote in self.votes:
                transcript += f"**{vote.voter_id}** voted for: {vote.vote}\n"
                transcript += f"Reasoning: {vote.reasoning}\n\n"
        
        # Show result if any
        if self.result:
            transcript += f"## Result\n\n{self.result}\n\n"
            if self.winner:
                transcript += f"Winner: {self.winner}\n"
        
        return transcript
    
    def get_participant(self, participant_id: str) -> Optional[DebateParticipant]:
        """Get a participant by ID."""
        for participant in self.participants:
            if participant.id == participant_id:
                return participant
        return None
    
    def get_participant_by_name(self, name: str) -> Optional[DebateParticipant]:
        """Get a participant by name."""
        for participant in self.participants:
            if participant.name == name:
                return participant
        return None
    
    def get_current_participant(self) -> Optional[DebateParticipant]:
        """Get the current participant (whose turn it is)."""
        return self.get_participant(self.turn)
    
    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True