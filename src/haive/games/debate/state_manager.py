# src/haive/games/debate/state_manager.py
import copy
from typing import List, Dict, Any, Optional, Type
from src.haive.games.framework.multi_player.state_manager import MultiPlayerGameStateManager
from src.haive.games.debate.state import DebateState
from src.haive.games.debate.models import Statement, Topic, Participant, Vote, DebatePhase
from datetime import datetime

class DebateStateManager(MultiPlayerGameStateManager[DebateState]):
    """Manager for debate game states."""
    
    @classmethod
    def initialize(cls, player_names: List[str], topic: Topic, format_type: str = "standard", **kwargs) -> DebateState:
        """Initialize a new debate state.
        
        Args:
            player_names: List of participant IDs
            topic: The debate topic
            format_type: Type of debate (presidential, trial, etc.)
            **kwargs: Additional format-specific parameters
            
        Returns:
            DebateState: A new debate state
        """
        # Create base state
        state = DebateState(
            players=player_names,
            topic=topic,
            game_phase=DebatePhase.SETUP,
            debate_phase=DebatePhase.SETUP
        )
        
        # Set up participants
        participants = {}
        for idx, player_id in enumerate(player_names):
            role = "debater"
            position = None
            
            # Handle special roles
            if format_type == "moderated" and idx == 0:
                role = "moderator"
                state.moderator_id = player_id
            elif format_type == "trial":
                if idx == 0:
                    role = "judge"
                elif idx == 1:
                    role = "prosecutor"
                    position = "prosecution"
                elif idx == 2:
                    role = "defense"
                    position = "defense"
                else:
                    role = "witness"
            elif format_type == "presidential":
                position = "pro" if idx % 2 == 0 else "con"
            
            participants[player_id] = Participant(
                id=player_id,
                name=f"Participant {idx+1}",
                role=role,
                position=position
            )
        
        state.participants = participants
        
        # Setup turn order (default to player list order)
        state.turn_order = player_names.copy()
        
        # Format-specific setup
        if format_type == "presidential":
            state.phase_time_limit = kwargs.get("time_limit", 120)
            state.interruptions_allowed = False
        elif format_type == "moderated":
            state.interruptions_allowed = False
        elif format_type == "trial":
            state.phase_time_limit = kwargs.get("time_limit", 300)
            state.interruptions_allowed = kwargs.get("interruptions", True)
        
        return state
    
    @classmethod
    def apply_move(cls, state: DebateState, player_id: str, move: Dict[str, Any]) -> DebateState:
        """Apply a player's move to the state.
        
        Args:
            state: Current debate state
            player_id: ID of the player making the move
            move: Move to apply (typically a statement)
            
        Returns:
            DebateState: Updated debate state
        """
        new_state = copy.deepcopy(state)
        
        # Process based on move type
        move_type = move.get("type", "statement")
        
        if move_type == "statement":
            # Create and add a new statement
            statement = Statement(
                content=move.get("content", ""),
                speaker_id=player_id,
                target_id=move.get("target_id"),
                statement_type=move.get("statement_type", "general"),
                references=move.get("references", []),
                timestamp=datetime.now().isoformat()
            )
            
            new_state.statements.append(statement)
            
            # Advance to next speaker if not an interruption
            if not (move.get("is_interruption", False) and new_state.interruptions_allowed):
                new_state.current_speaker_idx = (new_state.current_speaker_idx + 1) % len(new_state.turn_order)
                
        elif move_type == "vote":
            # Add a vote
            vote = Vote(
                voter_id=player_id,
                vote_value=move.get("vote_value"),
                target_id=move.get("target_id"),
                reason=move.get("reason")
            )
            
            if player_id not in new_state.votes:
                new_state.votes[player_id] = []
                
            new_state.votes[player_id].append(vote)
            
        elif move_type == "moderation":
            # Handle moderation actions
            if player_id == new_state.moderator_id:
                action = move.get("action")
                
                if action == "advance_phase":
                    new_state = cls.advance_phase(new_state)
                elif action == "interrupt":
                    new_state.moderation_notes.append(move.get("note", "Moderator interruption"))
                elif action == "change_turn_order":
                    new_state.turn_order = move.get("new_order", new_state.turn_order)
                    
        # Record move in history
        new_state.move_history.append({
            "player_id": player_id,
            "move_type": move_type,
            "move_data": move,
            "timestamp": datetime.now().isoformat()
        })
                    
        return new_state
    
    @classmethod
    def get_legal_moves(cls, state: DebateState, player_id: str) -> List[Dict[str, Any]]:
        """Get legal moves for a player.
        
        Args:
            state: Current debate state
            player_id: ID of the player
            
        Returns:
            List[Dict[str, Any]]: List of legal moves
        """
        moves = []
        
        # Get participant info
        participant = state.participants.get(player_id)
        if not participant:
            return moves
            
        # Add moves based on role and phase
        if participant.role == "moderator":
            moves.append({"type": "moderation", "action": "advance_phase"})
            moves.append({"type": "moderation", "action": "interrupt"})
            moves.append({"type": "statement", "statement_type": "question"})
            
        elif state.current_speaker == player_id:
            # Regular statement when it's the player's turn
            moves.append({"type": "statement", "statement_type": "general"})
            
            # Phase-specific moves
            if state.debate_phase == DebatePhase.REBUTTAL:
                moves.append({"type": "statement", "statement_type": "rebuttal"})
            elif state.debate_phase == DebatePhase.QUESTIONS:
                moves.append({"type": "statement", "statement_type": "question"})
            elif state.debate_phase == DebatePhase.VOTING:
                moves.append({"type": "vote"})
                
        elif state.interruptions_allowed:
            # Interruption when allowed
            moves.append({"type": "statement", "is_interruption": True})
            
        return moves
    
    @classmethod
    def check_game_status(cls, state: DebateState) -> DebateState:
        """Check and update game status.
        
        Args:
            state: Current debate state
            
        Returns:
            DebateState: Updated debate state with status
        """
        new_state = copy.deepcopy(state)
        
        # End conditions
        if state.debate_phase == DebatePhase.CONCLUSION:
            new_state.game_status = "ended"
            
        # Check for phase completion
        if state.phase_statement_limit:
            # Count statements in current phase
            phase_statements = [s for s in state.statements 
                               if s.statement_type == state.debate_phase]
            
            if len(phase_statements) >= state.phase_statement_limit:
                new_state = cls.advance_phase(new_state)
        
        return new_state
    
    @classmethod
    def advance_phase(cls, state: DebateState) -> DebateState:
        """Advance to the next debate phase.
        
        Args:
            state: Current debate state
            
        Returns:
            DebateState: State in the next phase
        """
        new_state = copy.deepcopy(state)
        
        # Phase advancement based on format
        phase_map = {
            DebatePhase.SETUP: DebatePhase.OPENING_STATEMENTS,
            DebatePhase.OPENING_STATEMENTS: DebatePhase.DISCUSSION,
            DebatePhase.DISCUSSION: DebatePhase.REBUTTAL,
            DebatePhase.REBUTTAL: DebatePhase.QUESTIONS,
            DebatePhase.QUESTIONS: DebatePhase.CLOSING_STATEMENTS,
            DebatePhase.CLOSING_STATEMENTS: DebatePhase.VOTING,
            DebatePhase.VOTING: DebatePhase.JUDGMENT,
            DebatePhase.JUDGMENT: DebatePhase.CONCLUSION
        }
        
        new_state.debate_phase = phase_map.get(state.debate_phase, DebatePhase.CONCLUSION)
        
        # Move game phase if debate is over
        if new_state.debate_phase == DebatePhase.CONCLUSION:
            new_state.game_phase = "game_over"
            
        # Reset turns for new phase
        new_state.current_speaker_idx = 0
        
        # Phase-specific settings
        if new_state.debate_phase == DebatePhase.OPENING_STATEMENTS:
            new_state.phase_statement_limit = len(new_state.turn_order)
            
        elif new_state.debate_phase == DebatePhase.VOTING:
            # Calculate scores based on statements
            scores = {}
            for participant_id in new_state.participants:
                # Simple scoring: count statements
                statement_count = len([s for s in new_state.statements 
                                      if s.speaker_id == participant_id])
                scores[participant_id] = statement_count
                
            new_state.scores = scores
        
        return new_state
    
    @classmethod
    def filter_state_for_player(cls, state: DebateState, player_id: str) -> Dict[str, Any]:
        """Filter state information for a specific player.
        
        Args:
            state: Current debate state
            player_id: ID of the player
            
        Returns:
            Dict[str, Any]: Filtered state visible to the player
        """
        # In a debate, most information is public
        visible_state = state.dict()
        
        # Hide other players' private data
        for pid, data in state.player_data.items():
            if pid != player_id:
                visible_state["player_data"][pid] = {"public_info": data.get("public_info", {})}
                
        # Hide future topics or questions if planned ahead
        # (implementation would depend on specific debate format)
        
        return visible_state