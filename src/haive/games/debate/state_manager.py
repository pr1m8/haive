from typing import List, Dict, Any, Optional, Union, Tuple, Callable
import copy
from pydantic import BaseModel

from .state import DebateState, DebateParticipant, DebateMove, VoteResult
from src.haive.games.framework.base.state_manager import GameStateManager

class DebateStateManager(GameStateManager[DebateState]):
    """Manager for debate state transitions.
    
    This class handles state initialization and transitions for debates,
    applying the template method pattern from GameStateManager.
    """
    
    @classmethod
    def initialize(cls, 
                 topic: str,
                 participants: List[DebateParticipant] = None,
                 description: str = "",
                 max_rounds: int = 3,
                 phase_sequence: List[str] = None,
                 **kwargs) -> DebateState:
        """Initialize a new debate state.
        
        Args:
            topic: The topic of the debate
            participants: List of debate participants (optional)
            description: Description of the debate
            max_rounds: Maximum number of rounds
            phase_sequence: Sequence of phases for the debate
            **kwargs: Additional arguments for the state
            
        Returns:
            A new DebateState instance
        """
        # Set up default participants if none provided
        if participants is None:
            participants = [
                DebateParticipant(id="participant1", name="Participant 1", role="debater"),
                DebateParticipant(id="participant2", name="Participant 2", role="debater")
            ]
        
        # Set up default phase sequence if none provided
        if phase_sequence is None:
            phase_sequence = [
                "setup",
                "opening_statements",
                "arguments",
                "closing_statements",
                "voting",
                "results",
                "completed"
            ]
        
        # Identify judges
        judge_participants = [p.id for p in participants if p.role == "judge"]
        
        # Determine first participant
        non_judge_participants = [p for p in participants if p.role != "judge"]
        first_participant_id = non_judge_participants[0].id if non_judge_participants else None
        
        # Create and return initial state
        return DebateState(
            topic=topic,
            description=description,
            participants=participants,
            judge_participants=judge_participants,
            phase_sequence=phase_sequence,
            max_rounds=max_rounds,
            current_phase="setup",
            turn=first_participant_id,
            game_status="setup",
            move_history=[],
            **kwargs
        )
    
    @classmethod
    def apply_move(cls, state: DebateState, move: DebateMove) -> DebateState:
        """Apply a move to the debate state.
        
        Args:
            state: Current state
            move: Move to apply
            
        Returns:
            Updated state
        """
        # Create a deep copy to avoid modifying the original
        new_state = copy.deepcopy(state)
        
        # Add the move to history
        new_state.move_history.append(move)
        
        # Update phase if needed
        current_phase = new_state.current_phase
        if current_phase == "setup":
            # Move to the next phase after setup
            phase_idx = new_state.phase_sequence.index(current_phase)
            if phase_idx < len(new_state.phase_sequence) - 1:
                new_state.current_phase = new_state.phase_sequence[phase_idx + 1]
                new_state.game_status = "ongoing"
                
        elif current_phase == "opening_statements":
            # Check if all openings are done
            debater_ids = [p.id for p in new_state.participants if p.role == "debater"]
            opening_participants = set(m.participant_id for m in new_state.move_history 
                                    if m.move_type == "opening_statement")
            
            if all(debater_id in opening_participants for debater_id in debater_ids):
                # All openings done, move to arguments phase
                phase_idx = new_state.phase_sequence.index(current_phase)
                if phase_idx < len(new_state.phase_sequence) - 1:
                    new_state.current_phase = new_state.phase_sequence[phase_idx + 1]
                    new_state.current_round = 1  # Start first round
        
        elif current_phase == "arguments":
            # Handle argument rounds
            debater_ids = [p.id for p in new_state.participants if p.role == "debater"]
            
            # Set move round number if not provided
            if move.round_number is None:
                move.round_number = new_state.current_round
            
            # Check if we should move to next round
            current_round_moves = [m for m in new_state.move_history 
                                if m.round_number == new_state.current_round 
                                and m.move_type == "argument"]
            
            current_round_participants = set(m.participant_id for m in current_round_moves)
            
            if all(debater_id in current_round_participants for debater_id in debater_ids):
                # This round is complete
                if new_state.current_round >= new_state.max_rounds:
                    # All rounds done, move to closing statements
                    phase_idx = new_state.phase_sequence.index(current_phase)
                    if phase_idx < len(new_state.phase_sequence) - 1:
                        new_state.current_phase = new_state.phase_sequence[phase_idx + 1]
                else:
                    # Move to next round
                    new_state.current_round += 1
        
        elif current_phase == "closing_statements":
            # Check if all closings are done
            debater_ids = [p.id for p in new_state.participants if p.role == "debater"]
            closing_participants = set(m.participant_id for m in new_state.move_history 
                                     if m.move_type == "closing_statement")
            
            if all(debater_id in closing_participants for debater_id in debater_ids):
                # All closings done, move to voting phase
                phase_idx = new_state.phase_sequence.index(current_phase)
                if phase_idx < len(new_state.phase_sequence) - 1:
                    new_state.current_phase = new_state.phase_sequence[phase_idx + 1]
        
        # Determine next turn
        if new_state.current_phase in ["opening_statements", "arguments", "closing_statements"]:
            new_state.turn = cls._get_next_turn(new_state, move.participant_id)
        elif new_state.current_phase == "voting":
            # During voting, the turn belongs to the first judge who hasn't voted yet
            voted_judges = set(v.voter_id for v in new_state.votes)
            for judge_id in new_state.judge_participants:
                if judge_id not in voted_judges:
                    new_state.turn = judge_id
                    break
            else:
                # All judges have voted, move to results
                phase_idx = new_state.phase_sequence.index(new_state.current_phase)
                if phase_idx < len(new_state.phase_sequence) - 1:
                    new_state.current_phase = new_state.phase_sequence[phase_idx + 1]
        
        return new_state
    
    @classmethod
    def add_vote(cls, state: DebateState, vote: VoteResult) -> DebateState:
        """Add a vote to the debate state.
        
        Args:
            state: Current state
            vote: Vote to add
            
        Returns:
            Updated state
        """
        # Create a deep copy to avoid modifying the original
        new_state = copy.deepcopy(state)
        
        # Add the vote
        new_state.votes.append(vote)
        
        # Check if all judges have voted
        voted_judges = set(v.voter_id for v in new_state.votes)
        if all(judge_id in voted_judges for judge_id in new_state.judge_participants):
            # All judges have voted, move to results phase
            phase_idx = new_state.phase_sequence.index(new_state.current_phase)
            if phase_idx < len(new_state.phase_sequence) - 1:
                new_state.current_phase = new_state.phase_sequence[phase_idx + 1]
        else:
            # Update turn to next judge
            for judge_id in new_state.judge_participants:
                if judge_id not in voted_judges:
                    new_state.turn = judge_id
                    break
        
        return new_state
    
    @classmethod
    def set_results(cls, state: DebateState, result: str, winner: Optional[str] = None) -> DebateState:
        """Set the final results of the debate.
        
        Args:
            state: Current state
            result: Result text
            winner: ID of the winning participant (optional)
            
        Returns:
            Updated state
        """
        # Create a deep copy to avoid modifying the original
        new_state = copy.deepcopy(state)
        
        # Set results
        new_state.result = result
        new_state.winner = winner
        
        # Move to completed phase
        new_state.current_phase = "completed"
        new_state.game_status = "completed"
        new_state.turn = None  # No more turns
        
        return new_state
    
    @classmethod
    def generate_participants(cls, 
                           generator_func: Callable, 
                           topic: str, 
                           num_debaters: int = 2, 
                           num_judges: int = 3) -> List[DebateParticipant]:
        """Generate debate participants using a generator function.
        
        Args:
            generator_func: Function to generate participants
            topic: Debate topic
            num_debaters: Number of debaters
            num_judges: Number of judges
            
        Returns:
            List of generated participants
        """
        try:
            prompt = f"""
Create participants for a debate on: "{topic}"

Generate:
1. {num_debaters} debaters with opposing viewpoints
2. {num_judges} judges with different personalities/backgrounds

For each debater, include:
- Name
- Position/stance (brief description)
- System prompt for the AI (instructions on how to debate this position)

For each judge, include:
- Name
- Personality/background description
- Judging criteria/values

Format each debater as:
Debater: [Name]
Position: [Position]
System Prompt: [System prompt]

Format each judge as:
Judge: [Name]
Personality: [Personality]
Values: [Values]
"""
            
            # Generate participants
            result = generator_func(prompt)
            
            # Parse the result
            participants = []
            
            if isinstance(result, str):
                sections = result.split("\n\n")
                for section in sections:
                    lines = section.strip().split("\n")
                    if not lines or len(lines) < 2:
                        continue
                    
                    # Parse participant type and name
                    if lines[0].startswith("Debater:"):
                        # Parse debater
                        name = lines[0].replace("Debater:", "").strip()
                        position = ""
                        system_prompt = ""
                        
                        for line in lines[1:]:
                            if line.startswith("Position:"):
                                position = line.replace("Position:", "").strip()
                            elif line.startswith("System Prompt:"):
                                system_prompt = line.replace("System Prompt:", "").strip()
                        
                        participants.append(DebateParticipant(
                            id=f"debater_{len([p for p in participants if p.role == 'debater']) + 1}",
                            name=name,
                            role="debater",
                            position=position,
                            system_prompt=system_prompt
                        ))
                    
                    elif lines[0].startswith("Judge:"):
                        # Parse judge
                        name = lines[0].replace("Judge:", "").strip()
                        personality = ""
                        
                        for line in lines[1:]:
                            if line.startswith("Personality:") or line.startswith("Values:"):
                                personality += line.strip() + " "
                        
                        participants.append(DebateParticipant(
                            id=f"judge_{len([p for p in participants if p.role == 'judge']) + 1}",
                            name=name,
                            role="judge",
                            personality=personality
                        ))
            
            # Create default participants if parsing failed
            if not any(p.role == "debater" for p in participants):
                for i in range(num_debaters):
                    participants.append(DebateParticipant(
                        id=f"debater_{i+1}",
                        name=f"Debater {i+1}",
                        role="debater",
                        position=f"{'Support' if i == 0 else 'Oppose'} the topic"
                    ))
            
            if not any(p.role == "judge" for p in participants):
                for i in range(num_judges):
                    participants.append(DebateParticipant(
                        id=f"judge_{i+1}",
                        name=f"Judge {i+1}",
                        role="judge",
                        personality=f"{'Analytical' if i == 0 else 'Emotional' if i == 1 else 'Balanced'} approach to judging"
                    ))
            
            return participants
            
        except Exception as e:
            print(f"Error generating participants: {str(e)}")
            
            # Create default participants on error
            participants = []
            
            for i in range(num_debaters):
                participants.append(DebateParticipant(
                    id=f"debater_{i+1}",
                    name=f"Debater {i+1}",
                    role="debater",
                    position=f"{'Support' if i == 0 else 'Oppose'} the topic"
                ))
            
            for i in range(num_judges):
                participants.append(DebateParticipant(
                    id=f"judge_{i+1}",
                    name=f"Judge {i+1}",
                    role="judge",
                    personality=f"{'Analytical' if i == 0 else 'Emotional' if i == 1 else 'Balanced'} approach to judging"
                ))
            
            return participants
    
    @classmethod
    def calculate_results(cls, state: DebateState) -> Tuple[str, Optional[str]]:
        """Calculate results based on judge votes.
        
        Args:
            state: Current state
            
        Returns:
            Tuple of (result_text, winner_id)
        """
        if not state.votes:
            return "No votes were cast.", None
        
        # Count votes for each debater
        vote_counts = {}
        for vote in state.votes:
            if vote.vote not in vote_counts:
                vote_counts[vote.vote] = 0
            vote_counts[vote.vote] += 1
        
        # Find winner
        max_votes = max(vote_counts.values()) if vote_counts else 0
        winners = [debater for debater, count in vote_counts.items() if count == max_votes]
        
        if len(winners) > 1:
            # Tie
            result = f"The debate ended in a tie between {', '.join(winners)}."
            winner = None
        else:
            # Clear winner
            winner = winners[0]
            winner_name = state.get_participant_by_name(winner)
            if winner_name:
                winner_name = winner_name.name
            else:
                winner_name = winner
                
            result = f"{winner_name} won the debate with {vote_counts[winner]} out of {len(state.votes)} votes."
        
        # Create detailed results
        result += "\n\nJudge votes:\n"
        for vote in state.votes:
            judge = state.get_participant(vote.voter_id)
            judge_name = judge.name if judge else vote.voter_id
            result += f"- {judge_name}: voted for {vote.vote}\n"
        
        return result, winner
    
    @classmethod
    def get_legal_moves(cls, state: DebateState) -> List[Dict[str, Any]]:
        """Get all legal moves for the current state.
        
        Args:
            state: Current state
            
        Returns:
            List of legal move templates
        """
        legal_moves = []
        
        # Current participant and phase
        participant_id = state.turn
        phase = state.current_phase
        
        if not participant_id:
            return []
        
        participant = state.get_participant(participant_id)
        if not participant:
            return []
        
        # Add appropriate moves based on phase and participant role
        if participant.role == "debater":
            if phase == "opening_statements":
                legal_moves.append({
                    "participant_id": participant_id,
                    "move_type": "opening_statement",
                    "description": f"Present opening statement as {participant.name}"
                })
            elif phase == "arguments":
                legal_moves.append({
                    "participant_id": participant_id,
                    "move_type": "argument",
                    "round_number": state.current_round,
                    "description": f"Present argument for round {state.current_round} as {participant.name}"
                })
            elif phase == "closing_statements":
                legal_moves.append({
                    "participant_id": participant_id,
                    "move_type": "closing_statement",
                    "description": f"Present closing statement as {participant.name}"
                })
        elif participant.role == "judge" and phase == "voting":
            # Add votes for each debater
            for debater in state.participants:
                if debater.role == "debater":
                    legal_moves.append({
                        "participant_id": participant_id,
                        "move_type": "vote",
                        "vote_for": debater.id,
                        "description": f"Vote for {debater.name} as {participant.name}"
                    })
        
        return legal_moves
    
    @classmethod
    def check_game_status(cls, state: DebateState) -> DebateState:
        """Check and update the game status.
        
        Args:
            state: Current state
            
        Returns:
            Updated state
        """
        # Create a deep copy to avoid modifying the original
        new_state = copy.deepcopy(state)
        
        # Check if the debate is completed
        if new_state.current_phase == "completed":
            new_state.game_status = "completed"
        else:
            new_state.game_status = "ongoing"
        
        return new_state
    
    @classmethod
    def _get_next_turn(cls, state: DebateState, current_participant_id: str) -> str:
        """Get the next participant's turn.
        
        Args:
            state: Current state
            current_participant_id: ID of the current participant
            
        Returns:
            ID of the next participant
        """
        # Get debaters in order
        debaters = [p for p in state.participants if p.role == "debater"]
        if not debaters:
            return ""
        
        # Find current participant's index
        current_index = -1
        for i, participant in enumerate(debaters):
            if participant.id == current_participant_id:
                current_index = i
                break
        
        # Get next index (circular)
        next_index = (current_index + 1) % len(debaters)
        
        # Special case: in closing statements, check if this participant already made a closing
        if state.current_phase == "closing_statements":
            closings = [m for m in state.move_history if m.move_type == "closing_statement"]
            closing_participants = [m.participant_id for m in closings]
            
            # Find next participant who hasn't made a closing statement yet
            for _ in range(len(debaters)):
                next_participant = debaters[next_index]
                if next_participant.id not in closing_participants:
                    return next_participant.id
                next_index = (next_index + 1) % len(debaters)
            
            # If all have made closing statements, move to judges
            if state.judge_participants:
                return state.judge_participants[0]
            return ""
        
        # Default: return next debater's ID
        return debaters[next_index].id  