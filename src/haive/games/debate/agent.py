# src/haive/games/debate/agent.py
from typing import Dict, List, Any, Optional
from langgraph.types import Command
from langgraph.graph import END
from src.haive.games.framework.multi_player import MultiPlayerGameAgent
from src.haive.games.debate.config import DebateAgentConfig
from src.haive.games.debate.state import DebateState
from src.haive.games.debate.state_manager import DebateStateManager
from src.haive.games.debate.models import Statement, Topic, Participant, DebatePhase
from src.haive.core.engine.agent.agent import register_agent
from src.haive.core.graph.GraphBuilder import DynamicGraph
import time

@register_agent(DebateAgentConfig)
class DebateAgent(MultiPlayerGameAgent[DebateAgentConfig]):
    """Agent for facilitating debates and structured discussions."""
    
    def __init__(self, config: DebateAgentConfig):
        self.state_manager = DebateStateManager
        super().__init__(config)
    
    def initialize_game(self, state: Dict[str, Any]) -> Command:
        """Initialize the debate with topic and participants."""
        # Extract debate topic if provided, otherwise use default
        topic_data = state.get("topic", {
            "title": "AI Ethics in Society",
            "description": "Discuss the ethical implications of AI in modern society"
        })
        
        if isinstance(topic_data, str):
            topic_data = {"title": topic_data, "description": topic_data}
            
        topic = Topic(**topic_data)
        
        # Extract participants or use default
        player_list = state.get("participants", [f"participant_{i}" for i in range(4)])
        if isinstance(player_list, dict):
            player_list = list(player_list.keys())
        
        # Initialize with format from config
        debate_state = self.state_manager.initialize(
            player_list,
            topic,
            format_type=self.config.debate_format,
            time_limit=self.config.time_limit,
            max_statements=self.config.max_statements,
            allow_interruptions=self.config.allow_interruptions
        )
        
        # Convert to dict for graph
        if hasattr(debate_state, "model_dump"):
            state_dict = debate_state.model_dump()
        else:
            state_dict = debate_state.dict()
            
        return Command(update=state_dict, goto="debate_setup")
    
    def get_player_role(self, state: DebateState, player_id: str) -> str:
        """Get the role of a player in the debate."""
        if player_id in state.participants:
            return state.participants[player_id].role
        return "debater"  # Default role
    
   # src/haive/games/debate/agent.py (continued)
    def prepare_move_context(self, state: DebateState, player_id: str) -> Dict[str, Any]:
        """Prepare context for a participant's move."""
        participant = state.participants.get(player_id)
        if not participant:
            return {}
            
        # Get recent statements (last 5)
        recent_statements = state.statements[-5:] if state.statements else []
        formatted_recent = []
        
        for stmt in recent_statements:
            speaker_name = state.participants.get(stmt.speaker_id, Participant(id=stmt.speaker_id, name=stmt.speaker_id, role="unknown")).name
            formatted_recent.append(f"{speaker_name}: {stmt.content}")
        
        # Get this player's previous statements
        player_statements = [s for s in state.statements if s.speaker_id == player_id]
        formatted_player = [f"{s.statement_type.capitalize()}: {s.content}" for s in player_statements]
        
        # Determine statement type based on phase
        statement_type = "statement"
        if state.debate_phase == DebatePhase.OPENING_STATEMENTS:
            statement_type = "opening statement"
        elif state.debate_phase == DebatePhase.REBUTTAL:
            statement_type = "rebuttal"
        elif state.debate_phase == DebatePhase.QUESTIONS:
            statement_type = "response to question"
        elif state.debate_phase == DebatePhase.CLOSING_STATEMENTS:
            statement_type = "closing statement"
        
        # Format based on role
        if participant.role == "moderator":
            action_prompt = "provide guidance or ask a question to move the debate forward"
            if state.debate_phase in [DebatePhase.SETUP, DebatePhase.JUDGMENT]:
                action_prompt = "summarize the current state and suggest next steps"
            
            return {
                "topic": state.topic.title,
                "topic_description": state.topic.description,
                "debate_phase": state.debate_phase,
                "participants": "\n".join([f"{p.name} ({p.role})" for p in state.participants.values()]),
                "recent_statements": "\n".join(formatted_recent),
                "current_speaker": state.participants.get(state.current_speaker, Participant(id="unknown", name="Unknown", role="unknown")).name,
                "action_prompt": action_prompt
            }
            
        elif participant.role == "judge":
            # For trial format
            all_statements = [f"{state.participants.get(s.speaker_id, Participant(id=s.speaker_id, name=s.speaker_id, role='unknown')).name}: {s.content}" 
                            for s in state.statements]
            
            action_prompt = "provide your analysis of the arguments presented so far"
            if state.debate_phase == DebatePhase.JUDGMENT:
                action_prompt = "render your final decision with explanation"
            
            return {
                "topic": state.topic.title,
                "topic_description": state.topic.description,
                "debate_phase": state.debate_phase,
                "all_statements": "\n".join(all_statements),
                "key_arguments": self._extract_key_arguments(state),
                "action_prompt": action_prompt
            }
            
        elif participant.role in ["prosecutor", "defense"]:
            # For trial format
            opponent_role = "defense" if participant.role == "prosecutor" else "prosecutor"
            opponent_claims = [s.content for s in state.statements 
                              if state.participants.get(s.speaker_id, Participant(id="", name="", role="")).role == opponent_role]
            
            evidence = "Evidence is still being collected" # Would be populated from state
            
            return {
                "topic": state.topic.title,
                "debate_phase": state.debate_phase,
                "evidence": evidence,
                "witness_statements": self._format_witness_statements(state),
                "recent_statements": "\n".join(formatted_recent),
                "statement_type": statement_type,
                "prosecution_claims": "\n".join(opponent_claims) if participant.role == "defense" else "",
                "client_info": "Defendant information" if participant.role == "defense" else ""
            }
            
        else:
            # Standard debater
            return {
                "topic": state.topic.title,
                "topic_description": state.topic.description,
                "debate_phase": state.debate_phase,
                "position": participant.position or "neutral",
                "recent_statements": "\n".join(formatted_recent),
                "your_statements": "\n".join(formatted_player),
                "statement_type": statement_type
            }
    
    def _extract_key_arguments(self, state: DebateState) -> str:
        """Extract key arguments from debate statements."""
        pro_args = []
        con_args = []
        
        for stmt in state.statements:
            participant = state.participants.get(stmt.speaker_id)
            if not participant:
                continue
                
            if participant.position == "pro":
                pro_args.append(f"- {stmt.content[:100]}..." if len(stmt.content) > 100 else f"- {stmt.content}")
            elif participant.position == "con":
                con_args.append(f"- {stmt.content[:100]}..." if len(stmt.content) > 100 else f"- {stmt.content}")
        
        result = "PRO Arguments:\n" + "\n".join(pro_args[-3:])  # Last 3 arguments
        result += "\n\nCON Arguments:\n" + "\n".join(con_args[-3:])
        
        return result
    
    def _format_witness_statements(self, state: DebateState) -> str:
        """Format witness statements for trial format."""
        witness_stmts = []
        
        for stmt in state.statements:
            participant = state.participants.get(stmt.speaker_id)
            if participant and participant.role == "witness":
                witness_stmts.append(f"{participant.name}: {stmt.content}")
        
        if not witness_stmts:
            return "No witness testimony yet."
            
        return "\n".join(witness_stmts)
    
    def extract_move(self, response: Any, role: str) -> Dict[str, Any]:
        """Extract move from engine response."""
        if isinstance(response, Statement):
            # If response is already a structured Statement
            return {
                "type": "statement",
                "content": response.content,
                "statement_type": response.statement_type,
                "target_id": response.target_id,
                "references": response.references
            }
        
        # Handle other response types based on role
        if isinstance(response, dict):
            if "vote_value" in response:
                return {
                    "type": "vote",
                    "vote_value": response.get("vote_value"),
                    "target_id": response.get("target_id"),
                    "reason": response.get("reason", "")
                }
            elif "action" in response and role == "moderator":
                return {
                    "type": "moderation",
                    "action": response.get("action"),
                    "note": response.get("note", "")
                }
        
        # Fallback: treat as general statement
        content = str(response)
        if hasattr(response, "content"):
            content = response.content
            
        return {
            "type": "statement",
            "content": content,
            "statement_type": "general"
        }
    
    def debate_setup(self, state: Dict[str, Any]) -> Command:
        """Handle debate setup phase."""
        state_obj = DebateState(**state) if isinstance(state, dict) else state
        
        # Initialize participant personas if needed
        if self.config.participant_roles:
            for player_id, role in self.config.participant_roles.items():
                if player_id in state_obj.participants:
                    state_obj.participants[player_id].role = role
        
        # Set moderator if configured
        if self.config.moderator_role and state_obj.players:
            moderator_id = state_obj.players[0]  # Default first player as moderator
            if moderator_id in state_obj.participants:
                state_obj.participants[moderator_id].role = "moderator"
                state_obj.moderator_id = moderator_id
        
        # Advance to opening phase
        updated_state = self.state_manager.advance_phase(state_obj)
        
        if hasattr(updated_state, "model_dump"):
            return Command(update=updated_state.model_dump(), goto="handle_participant_turn")
        return Command(update=updated_state.dict(), goto="handle_participant_turn")
    
    def handle_participant_turn(self, state: Dict[str, Any]) -> Command:
        """Handle a participant's turn in the debate."""
        state_obj = DebateState(**state) if isinstance(state, dict) else state
        
        # Check for game end
        if state_obj.game_status != "ongoing" or state_obj.debate_phase == DebatePhase.CONCLUSION:
            if hasattr(state_obj, "model_dump"):
                return Command(update=state_obj.model_dump(), goto=END)
            return Command(update=state_obj.dict(), goto=END)
        
        # Get current speaker
        current_speaker = state_obj.current_speaker
        if not current_speaker:
            # No current speaker, advance phase
            updated_state = self.state_manager.advance_phase(state_obj)
            if hasattr(updated_state, "model_dump"):
                return Command(update=updated_state.model_dump(), goto="handle_phase_transition")
            return Command(update=updated_state.dict(), goto="handle_phase_transition")
        
        # Check if special handling needed for moderator
        if state_obj.participants.get(current_speaker, Participant(id="", name="", role="")).role == "moderator":
            updated_state = self.handle_moderator_turn(state_obj)
            next_step = self.determine_next_step(updated_state)
            if hasattr(updated_state, "model_dump"):
                return Command(update=updated_state.model_dump(), goto=next_step)
            return Command(update=updated_state.dict(), goto=next_step)
        
        # Process regular participant turn
        participant = state_obj.participants.get(current_speaker)
        if not participant:
            # Invalid participant, skip turn
            state_obj.current_speaker_idx = (state_obj.current_speaker_idx + 1) % len(state_obj.turn_order)
            if hasattr(state_obj, "model_dump"):
                return Command(update=state_obj.model_dump(), goto="handle_participant_turn")
            return Command(update=state_obj.dict(), goto="handle_participant_turn")
        
        # Get the appropriate engine for this role
        role = participant.role
        position = participant.position
        
        # Select engine based on role and position
        if role == "debater" and position in ["pro", "con"]:
            engine_key = position
        else:
            engine_key = "statement"
            
        engine = self.get_engine_for_player(role, engine_key)
        if not engine:
            # Fallback to default debater engine
            engine = self.get_engine_for_player("debater", "statement")
            
        if not engine:
            # Still no engine, skip turn
            state_obj.current_speaker_idx = (state_obj.current_speaker_idx + 1) % len(state_obj.turn_order)
            if hasattr(state_obj, "model_dump"):
                return Command(update=state_obj.model_dump(), goto="handle_participant_turn")
            return Command(update=state_obj.dict(), goto="handle_participant_turn")
        
        # Generate move
        try:
            context = self.prepare_move_context(state_obj, current_speaker)
            response = engine.invoke(context)
            move = self.extract_move(response, role)
            
            # Apply move
            updated_state = self.state_manager.apply_move(state_obj, current_speaker, move)
            
            # Check game status
            updated_state = self.state_manager.check_game_status(updated_state)
            
            # Determine next step
            next_step = self.determine_next_step(updated_state)
            
            if hasattr(updated_state, "model_dump"):
                return Command(update=updated_state.model_dump(), goto=next_step)
            return Command(update=updated_state.dict(), goto=next_step)
            
        except Exception as e:
            print(f"Error in participant turn: {e}")
            # Skip turn on error
            state_obj.current_speaker_idx = (state_obj.current_speaker_idx + 1) % len(state_obj.turn_order)
            if hasattr(state_obj, "model_dump"):
                return Command(update=state_obj.model_dump(), goto="handle_participant_turn")
            return Command(update=state_obj.dict(), goto="handle_participant_turn")
    
    def handle_moderator_turn(self, state: DebateState) -> DebateState:
        """Handle the moderator's turn."""
        moderator_id = state.moderator_id
        if not moderator_id:
            # No designated moderator, skip
            state.current_speaker_idx = (state.current_speaker_idx + 1) % len(state.turn_order)
            return state
            
        engine = self.get_engine_for_player("moderator", "moderate")
        if not engine:
            # No moderator engine, skip
            state.current_speaker_idx = (state.current_speaker_idx + 1) % len(state.turn_order)
            return state
            
        try:
            context = self.prepare_move_context(state, moderator_id)
            response = engine.invoke(context)
            move = self.extract_move(response, "moderator")
            
            # Apply move
            updated_state = self.state_manager.apply_move(state, moderator_id, move)
            
            # Special handling for moderator actions
            if move.get("type") == "moderation" and move.get("action") == "advance_phase":
                updated_state = self.state_manager.advance_phase(updated_state)
            
            return updated_state
            
        except Exception as e:
            print(f"Error in moderator turn: {e}")
            # Skip turn on error
            state.current_speaker_idx = (state.current_speaker_idx + 1) % len(state.turn_order)
            return state
    
    def determine_next_step(self, state: DebateState) -> str:
        """Determine the next step in the debate flow."""
        # End if game over
        if state.game_status != "ongoing" or state.debate_phase == DebatePhase.CONCLUSION:
            return END
            
        # Check phase completion
        if state.debate_phase in [DebatePhase.OPENING_STATEMENTS, DebatePhase.CLOSING_STATEMENTS]:
            # Count statements in current phase
            phase_statements = [s for s in state.statements 
                               if getattr(s, "timestamp", "").startswith(state.debate_phase)]
            
            participant_count = len(state.participants)
            if len(phase_statements) >= participant_count:
                return "handle_phase_transition"
                
        # Check if everyone has voted in voting phase
        if state.debate_phase == DebatePhase.VOTING:
            if len(state.votes) >= len(state.participants):
                return "handle_phase_transition"
                
        # Continue with participant turns
        return "handle_participant_turn"
    
    def handle_phase_transition(self, state: Dict[str, Any]) -> Command:
        """Handle transition between debate phases."""
        state_obj = DebateState(**state) if isinstance(state, dict) else state
        
        try:
            # Advance to the next phase
            updated_state = self.state_manager.advance_phase(state_obj)
            
            # Reset speaker index for new phase
            updated_state.current_speaker_idx = 0
            
            # Check if game has ended
            if updated_state.game_status != "ongoing" or updated_state.debate_phase == DebatePhase.CONCLUSION:
                if hasattr(updated_state, "model_dump"):
                    return Command(update=updated_state.model_dump(), goto=END)
                return Command(update=updated_state.dict(), goto=END)
                
            # Continue with participant turns in new phase
            if hasattr(updated_state, "model_dump"):
                return Command(update=updated_state.model_dump(), goto="handle_participant_turn")
            return Command(update=updated_state.dict(), goto="handle_participant_turn")
            
        except Exception as e:
            print(f"Error in phase transition: {e}")
            # On error, end the debate
            state_obj.game_status = "ended"
            if hasattr(state_obj, "model_dump"):
                return Command(update=state_obj.model_dump(), goto=END)
            return Command(update=state_obj.dict(), goto=END)
    
    def visualize_state(self, state: Dict[str, Any]) -> None:
        """Visualize the current debate state."""
        if not self.config.visualize:
            return
            
        state_obj = state if isinstance(state, DebateState) else DebateState(**state)
        
        print("\n" + "=" * 60)
        print(f"🎭 DEBATE: {state_obj.topic.title}")
        print(f"📊 Phase: {state_obj.debate_phase}")
        print(f"👤 Current Speaker: {state_obj.current_speaker}")
        print("=" * 60)
        
        # Show recent statements
        if state_obj.statements:
            print("\n📝 Recent Statements:")
            for i, stmt in enumerate(state_obj.statements[-5:]):
                participant = state_obj.participants.get(stmt.speaker_id, Participant(id=stmt.speaker_id, name=f"Unknown-{stmt.speaker_id}", role="unknown"))
                print(f"{i+1}. [{participant.role.upper()}] {participant.name}: {stmt.content[:100]}..." 
                     if len(stmt.content) > 100 else f"{i+1}. [{participant.role.upper()}] {participant.name}: {stmt.content}")
        
        # Show votes in voting phase
        if state_obj.debate_phase == DebatePhase.VOTING and state_obj.votes:
            print("\n🗳️ Current Votes:")
            for voter_id, vote_list in state_obj.votes.items():
                if not vote_list:
                    continue
                voter = state_obj.participants.get(voter_id, Participant(id=voter_id, name=f"Unknown-{voter_id}", role="unknown"))
                latest_vote = vote_list[-1]
                target = state_obj.participants.get(latest_vote.target_id, Participant(id=latest_vote.target_id, name=f"Unknown-{latest_vote.target_id}", role="unknown")) if latest_vote.target_id else None
                if target:
                    print(f"- {voter.name} voted for {target.name}: {latest_vote.vote_value}")
                else:
                    print(f"- {voter.name} voted: {latest_vote.vote_value}")
        
        time.sleep(0.5)  # Brief pause for readability
    
    def setup_workflow(self) -> None:
        """Setup the debate workflow."""
        gb = DynamicGraph(components=[self.config], state_schema=self.config.state_schema)
        
        # Add the nodes
        gb.add_node("initialize", self.initialize_game)
        gb.add_node("debate_setup", self.debate_setup)
        gb.add_node("handle_participant_turn", self.handle_participant_turn)
        gb.add_node("handle_phase_transition", self.handle_phase_transition)
        
        # Add the edges
        gb.add_edge("initialize", "debate_setup")
        gb.add_edge("debate_setup", "handle_participant_turn")
        gb.add_edge("handle_participant_turn", "handle_participant_turn")
        gb.add_edge("handle_participant_turn", "handle_phase_transition")
        gb.add_edge("handle_phase_transition", "handle_participant_turn")
        gb.add_edge("handle_phase_transition", END)
        
        self.graph = gb.build()