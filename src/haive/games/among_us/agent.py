# among_us_agent.py

import re
from typing import Dict, Any, List, Optional, Union

from src.haive.games.framework.multi_player.agent import MultiPlayerGameAgent
from src.haive.games.among_us.state import AmongUsState
from src.haive.games.among_us.models import PlayerRole, AmongUsGamePhase, TaskStatus
from src.haive.games.among_us.state_manager import AmongUsStateManagerMixin
from src.haive.games.among_us.ui import AmongUsUI
from src.haive.games.among_us.config import AmongUsAgentConfig
from src.haive.core.engine.agent.agent import register_agent
@register_agent(AmongUsAgentConfig)
class AmongUsAgent(AmongUsStateManagerMixin, MultiPlayerGameAgent[AmongUsAgentConfig]):
    """
    Agent implementation for the Among Us game.
    
    This class inherits state management from AmongUsStateManagerMixin
    and agent behavior from MultiPlayerGameAgent.
    """
    
    def __init__(self, config):
        """Initialize the Among Us agent with configuration."""
        super().__init__(config)
        self.state_manager = self  # Still point to self, but using mixin methods
        self.ui = AmongUsUI()  # Initialize the UI component
    
    def visualize_state(self, state: Union[Dict[str, Any], AmongUsState]) -> None:
        """
        Visualize the current game state using the AmongUsUI.
        
        This method is required by the MultiPlayerGameAgent parent class.
        
        Args:
            state: Current game state (dict or AmongUsState object)
        """
        # Ensure state is in the right format
        if isinstance(state, dict):
            from src.haive.games.among_us.state import AmongUsState
            try:
                state_obj = AmongUsState(**state)
            except Exception as e:
                print(f"Error converting state dict to AmongUsState: {e}")
                return
        else:
            state_obj = state
        
        # Use the UI to display the game
        display = self.ui.display_game(state_obj)
        
        # Print the display
        from rich.console import Console
        console = Console()
        console.print(display)
    # Add this method to the AmongUsAgent class

    def get_engine_for_player(self, role: str, engine_key: str):
        """
        Get the appropriate engine for a player based on their role and the current phase.
        
        Args:
            role: Player role (CREWMATE or IMPOSTOR)
            engine_key: Engine type key (player, meeting, voting)
            
        Returns:
            The appropriate engine runnable
        """
        # Convert PlayerRole enum to string if needed
        if isinstance(role, PlayerRole):
            role_str = role.name
        else:
            role_str = role.upper()
        
        # Check if role is valid
        if role_str not in ["CREWMATE", "IMPOSTOR"]:
            print(f"Invalid role: {role}")
            return None
        
        # Get engines from src.config
        if not hasattr(self.config, "engines") or not self.config.engines:
            print("No engines found in config")
            return None
        
        # Get engine for role
        role_engines = self.config.engines.get(role_str)
        if not role_engines:
            print(f"No engines for role: {role_str}")
            return None
        
        # Get specific engine
        engine = role_engines.get(engine_key)
        if not engine:
            print(f"No {engine_key} engine found for {role_str}")
            return None
        
        # Create runnable if needed
        if hasattr(engine, "create_runnable"):
            return engine.create_runnable()
        
        return engine
    def prepare_move_context(self, state: AmongUsState, player_id: str) -> Dict[str, Any]:
        """Prepare context for a player's move decision."""
        if player_id not in state.player_states:
            return {"error": f"Player {player_id} not found"}
                
        player_state = state.player_states[player_id]
        
        # Get filtered state for this player
        filtered_state = self.filter_state_for_player(state, player_id)
        
        # Add game-phase specific context
        if state.game_phase == AmongUsGamePhase.TASKS:
            # Add available actions
            filtered_state["available_actions"] = self.get_legal_moves(state, player_id)
            
            # Add role-specific information
            if player_state.role == PlayerRole.CREWMATE:
                filtered_state["task_completion"] = self._get_task_completion_percentage(state)
            else:  # Impostor
                filtered_state["potential_targets"] = self._get_potential_targets(state, player_id)
                filtered_state["kill_cooldown"] = getattr(self.config, "kill_cooldown", 45)  # Default 45s
                filtered_state["fellow_impostors"] = [
                    pid for pid, pstate in state.player_states.items() 
                    if pstate.role == PlayerRole.IMPOSTOR and pid != player_id
                ]
        
        elif state.game_phase == AmongUsGamePhase.MEETING:
            # Add meeting-specific context
            filtered_state["discussion_time"] = getattr(self.config, "discussion_time", 45)
            filtered_state["alive_players"] = [pid for pid, pdata in state.player_states.items() 
                                            if pdata.is_alive]
            
            # Add reason for meeting
            if state.reported_body:
                filtered_state["reason"] = "Body Reported"
                filtered_state["reported_body"] = state.reported_body
                if state.reported_body in state.player_states:
                    filtered_state["body_location"] = state.player_states[state.reported_body].location
            else:
                filtered_state["reason"] = "Emergency Meeting"
                filtered_state["reported_body"] = None
        
        elif state.game_phase == AmongUsGamePhase.VOTING:
            # Add voting-specific context
            filtered_state["voting_time"] = getattr(self.config, "voting_time", 30)
            filtered_state["alive_players"] = [pid for pid, pdata in state.player_states.items() 
                                            if pdata.is_alive]
            filtered_state["voted_players"] = list(state.votes.keys())
            
            # Add discussion summary
            if hasattr(state, "discussion_history") and state.discussion_history:
                filtered_state["discussion_summary"] = "\n".join([
                    f"{msg['player_id']}: {msg['message']}" 
                    for msg in state.discussion_history[-10:]  # Last 10 messages
                ])
        
        # Add game configuration information
        filtered_state["player_count"] = len(state.players)
        filtered_state["impostor_count"] = state.impostor_count
        filtered_state["map_locations"] = state.map_locations
        
        # Always ensure player's own location is included
        filtered_state["location"] = player_state.location
        
        # Format tasks for prompt
        tasks_str = []
        for task in player_state.tasks:
            status = "✓" if task.status == TaskStatus.COMPLETED else "□"
            tasks_str.append(f"{status} {task.description} (in {task.location})")
        
        filtered_state["tasks"] = "\n".join(tasks_str)
        
        # Format observations
        if player_state.observations:
            filtered_state["observations"] = "\n".join([f"• {obs}" for obs in player_state.observations])
        else:
            filtered_state["observations"] = "None"
        
        # CRITICAL FIX: Add 'messages' field for the prompt template
        # Create a list with a single HumanMessage containing a formatted situation description
        from langchain_core.messages import HumanMessage
        
        # Create a concise situation message based on the game phase
        if state.game_phase == AmongUsGamePhase.TASKS:
            situation = f"I am in {filtered_state['location']}. My tasks: {filtered_state['tasks']}."
            if player_state.role == PlayerRole.IMPOSTOR:
                fellow = ", ".join(filtered_state.get("fellow_impostors", []))
                situation += f" I am an impostor. Fellow impostors: {fellow or 'none'}."
            else:
                situation += f" Overall task completion: {filtered_state.get('task_completion', 0)}%."
        
        elif state.game_phase == AmongUsGamePhase.MEETING:
            situation = f"Emergency meeting called by {filtered_state['meeting_caller']}!"
            if filtered_state.get("reported_body"):
                situation += f" Body of {filtered_state['reported_body']} was found."
        
        elif state.game_phase == AmongUsGamePhase.VOTING:
            situation = "It's time to vote! Discussion summary:\n"
            situation += filtered_state.get("discussion_summary", "No discussion recorded.")
        
        # Add observations
        situation += f"\nRecent observations: {filtered_state['observations']}"
        
        # Add message to context
        filtered_state["messages"] = [HumanMessage(content=situation)]
        
        return filtered_state

    def extract_move(self, response: Any, role: str) -> Dict[str, Any]:
        """Extract structured move from engine response."""
        # If response is already a structured dictionary, return it
        if isinstance(response, dict) and "action" in response:
            return response
        
        # If response is a string, try to extract structured move
        if isinstance(response, str):
            # Try to parse as JSON
            try:
                import json
                parsed = json.loads(response)
                if isinstance(parsed, dict) and "action" in parsed:
                    return parsed
            except:
                pass
            
            # Try to extract based on simple patterns
            if "move to" in response.lower():
                # Extract location from text like "I move to electrical"
                for location in self.config.map_locations:
                    if location.lower() in response.lower():
                        return {
                            "action": "move",
                            "location": location
                        }
            
            elif "complete task" in response.lower() or "do task" in response.lower():
                # Try to extract task ID from message
                task_match = re.search(r"task[_\s]*(\w+)", response, re.IGNORECASE)
                if task_match:
                    return {
                        "action": "complete_task",
                        "task_id": task_match.group(1)
                    }
            
            elif "kill" in response.lower():
                # Try to extract target from message like "I kill blue"
                for player in self.config.player_names:
                    if player.lower() in response.lower():
                        return {
                            "action": "kill",
                            "target_id": player
                        }
            
            elif "report" in response.lower() or "body" in response.lower():
                return {
                    "action": "report_body"
                }
            
            elif "emergency" in response.lower() or "meeting" in response.lower():
                return {
                    "action": "call_emergency_meeting"
                }
            
            elif "vote" in response.lower():
                # Try to extract vote target
                for player in self.config.player_names:
                    if player.lower() in response.lower():
                        return {
                            "action": "vote",
                            "vote_for": player
                        }
                
                if "skip" in response.lower():
                    return {
                        "action": "vote",
                        "vote_for": "skip"
                    }
            
            elif "sabotage" in response.lower():
                # Try to identify sabotage type
                sabotage_types = {
                    "light": "lights",
                    "oxygen": "o2",
                    "o2": "o2",
                    "reactor": "reactor",
                    "communication": "comms",
                    "comms": "comms"
                }
                
                for key, value in sabotage_types.items():
                    if key in response.lower():
                        return {
                            "action": "sabotage",
                            "sabotage_type": value,
                            "location": value
                        }
            
            # If we couldn't parse a specific action, but we're in discussion phase
            if "discuss" in response.lower() or len(response) > 20:
                return {
                    "action": "discuss",
                    "message": response
                }
        
        # If we couldn't extract a structured move, return an "observe" action as fallback
        return {
            "action": "observe"
        }