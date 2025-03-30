# state_manager_mixin.py

from typing import Dict, Any, List, Optional, Type
from datetime import datetime
from pydantic import BaseModel

from src.haive.games.framework.multi_player.state_manager import MultiPlayerGameStateManager
from src.haive.games.among_us.state import AmongUsState
from src.haive.games.among_us.models import PlayerRole, TaskStatus, AmongUsGamePhase, SabotageEvent, Task, TaskType

class AmongUsStateManagerMixin(MultiPlayerGameStateManager[AmongUsState]):
    """
    Mixin class that implements state management for Among Us game.
    
    This class separates state management from agent behavior while allowing
    any class that inherits from it to have state management capabilities.
    """
    
    @classmethod
    def initialize(cls, player_names: List[str], **kwargs) -> AmongUsState:
        """Initialize a new Among Us game state."""
        # Default map locations if not provided
        map_locations = kwargs.get("map_locations", [
            "cafeteria", "admin", "electrical", "storage", "medbay", 
            "navigation", "shields", "weapons", "o2", "security"
        ])
        
        # Determine number of impostors based on player count
        num_players = len(player_names)
        num_impostors = kwargs.get("num_impostors", max(1, num_players // 5))
        
        # Randomly assign roles
        import random
        random.seed(kwargs.get("seed", None))
        impostor_indices = random.sample(range(num_players), min(num_impostors, num_players))
        
        # Create player states
        player_states = {}
        tasks_per_player = kwargs.get("tasks_per_player", 5)
        all_tasks = {}
        
        for i, player_name in enumerate(player_names):
            role = PlayerRole.IMPOSTOR if i in impostor_indices else PlayerRole.CREWMATE
            
            # Generate tasks for crewmates (impostors get fake tasks)
            player_tasks = []
            if role == PlayerRole.CREWMATE:
                for j in range(tasks_per_player):
                    task_id = f"{player_name}_task_{j}"
                    location = random.choice(map_locations)
                    task_type = random.choice(list(TaskType))
                    
                    task = Task(
                        id=task_id,
                        type=task_type,
                        location=location,
                        description=cls._generate_task_description(task_type, location),
                        status=TaskStatus.NOT_STARTED
                    )
                    player_tasks.append(task)
                    all_tasks[task_id] = task
            else:
                # Fake tasks for impostors (not counted in completion)
                for j in range(tasks_per_player):
                    task_id = f"{player_name}_fake_task_{j}"
                    location = random.choice(map_locations)
                    task_type = random.choice(list(TaskType))
                    
                    task = Task(
                        id=task_id,
                        type=task_type,
                        location=location,
                        description=cls._generate_task_description(task_type, location),
                        status=TaskStatus.NOT_STARTED
                    )
                    player_tasks.append(task)
            
            # Create player state
            player_states[player_name] = {
                "id": player_name,
                "role": role,
                "location": "cafeteria",  # Everyone starts in cafeteria
                "tasks": player_tasks,
                "is_alive": True,
                "observations": []
            }
        
        # Initialize roles dictionary
        roles = {player_id: player_data["role"] for player_id, player_data in player_states.items()}
        
        # Initialize state
        state = AmongUsState(
            players=player_names,
            current_player_idx=0,
            game_phase=AmongUsGamePhase.TASKS,
            game_status="ongoing",
            move_history=[],
            round_number=0,
            player_data={},  # Will use player_states instead
            public_state={},
            map_locations=map_locations,
            player_states=player_states,
            tasks=all_tasks,
            sabotages=[],
            eliminated_players=[],
            meeting_active=False,
            meeting_caller=None,
            reported_body=None,
            votes={},
            impostor_count=num_impostors,
            crewmate_count=num_players - num_impostors,
            roles=roles,
            discussion_history=[]
        )
        
        return state
    
    @classmethod
    def _generate_task_description(cls, task_type, location) -> str:
        """Generate a description for a task based on its type and location."""
        task_descriptions = {
            TaskType.VISUAL: {
                "medbay": "Submit scan",
                "weapons": "Clear asteroids",
                "shields": "Prime shields"
            },
            TaskType.COMMON: {
                "admin": "Swipe card",
                "electrical": "Divert power",
                "o2": "Empty garbage"
            },
            TaskType.SHORT: {
                "electrical": "Fix wiring",
                "navigation": "Chart course",
                "admin": "Download data"
            },
            TaskType.LONG: {
                "electrical": "Calibrate distributor",
                "navigation": "Stabilize steering",
                "medbay": "Inspect sample"
            }
        }
        
        # Get possible descriptions for this type and location
        possible_descriptions = task_descriptions.get(task_type, {}).get(location)
        if possible_descriptions:
            return possible_descriptions
        
        # Fallback descriptions by type
        fallback_by_type = {
            TaskType.VISUAL: "Perform visual task",
            TaskType.COMMON: "Complete common task",
            TaskType.SHORT: "Complete short task",
            TaskType.LONG: "Complete long task"
        }
        
        return f"{fallback_by_type[task_type]} in {location}"
    
    @classmethod
    def apply_move(cls, state: AmongUsState, player_id: str, move: Dict[str, Any]) -> AmongUsState:
        """Apply a player's move to the game state."""
        # Create a copy of the state to avoid modifying the original
        state = state.model_copy(deep=True)
        
        # Validate player exists
        if player_id not in state.player_states:
            state.error_message = f"Player {player_id} not found"
            return state
        
        # Record the action in history
        action = {
            "player_id": player_id,
            "action_type": move.get("action"),
            "timestamp": datetime.now().isoformat(),
            "phase": state.game_phase,
            "round_number": state.round_number,
            "details": move
        }
        state.move_history.append(action)
        
        # Update player's last action
        if "last_action" in state.player_states[player_id]:
            state.player_states[player_id]["last_action"] = move.get("action")
        
        # Handle different action types based on game phase
        action_type = move.get("action")
        
        # Delegate to appropriate handler
        if state.game_phase == AmongUsGamePhase.TASKS:
            if action_type == "move":
                return cls._handle_move_action(state, player_id, move)
            elif action_type == "complete_task":
                return cls._handle_complete_task_action(state, player_id, move)
            elif action_type == "kill":
                return cls._handle_kill_action(state, player_id, move)
            elif action_type == "report_body":
                return cls._handle_report_action(state, player_id, move)
            elif action_type == "call_emergency_meeting":
                return cls._handle_emergency_meeting_action(state, player_id, move)
            elif action_type == "sabotage":
                return cls._handle_sabotage_action(state, player_id, move)
        
        elif state.game_phase == AmongUsGamePhase.MEETING:
            if action_type == "discuss":
                return cls._handle_discussion_action(state, player_id, move)
        
        elif state.game_phase == AmongUsGamePhase.VOTING:
            if action_type == "vote":
                return cls._handle_vote_action(state, player_id, move)
        
        # If we get here, the action wasn't handled
        state.error_message = f"Invalid action '{action_type}' for phase '{state.game_phase}'"
        return state
    
    # Action handlers for different game actions
    @classmethod
    def _handle_move_action(cls, state: AmongUsState, player_id: str, move: Dict[str, Any]) -> AmongUsState:
        """Handle a player moving to a new location."""
        target_location = move.get("location")
        
        # Validate location
        if target_location not in state.map_locations:
            state.error_message = f"Invalid location '{target_location}'"
            return state
        
        # Get current location for observation
        current_location = state.player_states[player_id]["location"]
        
        # Update player location
        state.player_states[player_id]["location"] = target_location
        
        # Add observation about their movement for other players in source/target
        observation = f"{player_id} moved from {current_location} to {target_location}"
        
        # Players in the target location observe the arrival
        for pid, pstate in state.player_states.items():
            if (pid != player_id and 
                pstate["is_alive"] and 
                pstate["location"] == target_location):
                
                pstate["observations"].append(observation)
        
        return state
    
    @classmethod
    def _handle_complete_task_action(cls, state: AmongUsState, player_id: str, move: Dict[str, Any]) -> AmongUsState:
        """Handle a player completing a task."""
        player_state = state.player_states[player_id]
        task_id = move.get("task_id")
        
        # Validate player is a crewmate (impostors can't complete real tasks)
        if player_state["role"] != PlayerRole.CREWMATE:
            # Impostors pretend to do tasks but don't actually complete them
            return state
        
        # Find the task
        player_tasks = [t for t in player_state["tasks"] if t.id == task_id]
        if not player_tasks:
            state.error_message = f"Task {task_id} not found for player {player_id}"
            return state
        
        task = player_tasks[0]
        
        # Validate task is in the player's current location
        if task.location != player_state["location"]:
            state.error_message = f"Task {task_id} is not in this location"
            return state
        
        # Update task status
        for i, t in enumerate(player_state["tasks"]):
            if t.id == task_id:
                player_state["tasks"][i].status = TaskStatus.COMPLETED
                break
                
        if task_id in state.tasks:
            state.tasks[task_id].status = TaskStatus.COMPLETED
        
        # Add observation for other players in the same location
        if task.type == TaskType.VISUAL:
            observation = f"{player_id} completed a visual task ({task.description}) in {task.location}"
            for pid, pstate in state.player_states.items():
                if (pid != player_id and 
                    pstate["is_alive"] and 
                    pstate["location"] == player_state["location"]):
                    
                    pstate["observations"].append(observation)
        
        return state
    
    @classmethod
    def _handle_kill_action(cls, state: AmongUsState, player_id: str, move: Dict[str, Any]) -> AmongUsState:
        """Handle an impostor killing a crewmate."""
        player_state = state.player_states[player_id]
        target_id = move.get("target_id")
        
        # Validate player is an impostor
        if player_state["role"] != PlayerRole.IMPOSTOR:
            state.error_message = "Only impostors can perform kills"
            return state
        
        # Validate target exists and is alive
        if target_id not in state.player_states:
            state.error_message = f"Target {target_id} not found"
            return state
        
        target_state = state.player_states[target_id]
        if not target_state["is_alive"]:
            state.error_message = f"Target {target_id} is already dead"
            return state
        
        # Validate target is in the same location
        if target_state["location"] != player_state["location"]:
            state.error_message = f"Target {target_id} is not in the same location"
            return state
        
        # Check for witnesses (other players in the same location)
        witnesses = [
            pid for pid, pstate in state.player_states.items()
            if (pid != player_id and 
                pid != target_id and
                pstate["is_alive"] and
                pstate["location"] == player_state["location"] and
                pstate["role"] != PlayerRole.IMPOSTOR)  # Other impostors don't count as witnesses
        ]
        
        if witnesses:
            state.error_message = "Cannot kill when there are witnesses"
            return state
        
        # Perform the kill
        target_state["is_alive"] = False
        state.eliminated_players.append(target_id)
        
        # Update counts
        if target_state["role"] == PlayerRole.CREWMATE:
            state.crewmate_count -= 1
        
        return state
    
    @classmethod
    def _handle_report_action(cls, state: AmongUsState, player_id: str, move: Dict[str, Any]) -> AmongUsState:
        """Handle a player reporting a dead body."""
        player_state = state.player_states[player_id]
        
        # Check if there's a dead body in the current location
        location = player_state["location"]
        dead_bodies = [
            pid for pid, pstate in state.player_states.items()
            if not pstate["is_alive"] and pstate["location"] == location
        ]
        
        if not dead_bodies:
            state.error_message = "No dead bodies to report"
            return state
        
        # Transition to meeting phase
        state.game_phase = AmongUsGamePhase.MEETING
        state.meeting_active = True
        state.meeting_caller = player_id
        state.reported_body = dead_bodies[0]
        
        return state
    
    @classmethod
    def _handle_emergency_meeting_action(cls, state: AmongUsState, player_id: str, move: Dict[str, Any]) -> AmongUsState:
        """Handle a player calling an emergency meeting."""
        player_state = state.player_states[player_id]
        
        # Validate player is in cafeteria
        if player_state.location != "cafeteria":
            state.error_message = "Emergency meetings can only be called in cafeteria"
            return state
        
        # Transition to meeting phase
        state.game_phase = AmongUsGamePhase.MEETING
        state.meeting_active = True
        state.meeting_caller = player_id
        
        return state
    
    @classmethod
    def _handle_discussion_action(cls, state: AmongUsState, player_id: str, move: Dict[str, Any]) -> AmongUsState:
        """Handle a player's discussion contribution."""
        message = move.get("message", "")
        
        # Record the message in the discussion history
        if not hasattr(state, "discussion_history"):
            state.discussion_history = []
        
        state.discussion_history.append({
            "player_id": player_id,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Check if all alive players have contributed to the discussion
        alive_players = [pid for pid, pstate in state.player_states.items() if pstate.is_alive]
        current_round_messages = [msg for msg in state.discussion_history 
                                if msg["player_id"] in alive_players]
        
        players_who_discussed = set(msg["player_id"] for msg in current_round_messages)
        
        if len(players_who_discussed) >= len(alive_players):
            # Transition to voting phase
            state.game_phase = AmongUsGamePhase.VOTING
        
        return state
    
    @classmethod
    def _handle_vote_action(cls, state: AmongUsState, player_id: str, move: Dict[str, Any]) -> AmongUsState:
        """Handle a player's vote."""
        target_id = move.get("vote_for")
        
        # Validate target exists or is "skip"
        if target_id != "skip" and target_id not in state.player_states:
            state.error_message = f"Invalid vote target: {target_id}"
            return state
        
        # Record the vote
        state.votes[player_id] = target_id
        
        # Check if all alive players have voted
        alive_players = [pid for pid, pstate in state.player_states.items() if pstate.is_alive]
        
        if len(state.votes) >= len(alive_players):
            # Count votes and eliminate player if needed
            vote_counts = {}
            for voted_for in state.votes.values():
                vote_counts[voted_for] = vote_counts.get(voted_for, 0) + 1
            
            # Find the player with the most votes (excluding skip)
            max_votes = 0
            player_to_eject = None
            
            for pid, count in vote_counts.items():
                if pid != "skip" and count > max_votes:
                    max_votes = count
                    player_to_eject = pid
            
            # In case of a tie, no one is ejected
            skip_votes = vote_counts.get("skip", 0)
            
            if player_to_eject and skip_votes < max_votes:
                # Check if anyone else has the same number of votes (tie)
                tied_players = [pid for pid, count in vote_counts.items() 
                              if pid != "skip" and pid != player_to_eject and count == max_votes]
                
                if not tied_players:  # No tie
                    # Eject the player
                    state.player_states[player_to_eject]["is_alive"] = False
                    state.eliminated_players.append(player_to_eject)
                    
                    # Update counts
                    if state.player_states[player_to_eject]["role"] == PlayerRole.IMPOSTOR:
                        state.impostor_count -= 1
                    else:
                        state.crewmate_count -= 1
            
            # Reset for next round
            state.votes = {}
            state.meeting_active = False
            state.meeting_caller = None
            state.reported_body = None
            
            # Transition back to tasks phase
            state.game_phase = AmongUsGamePhase.TASKS
            state.round_number += 1
        
        return state
    
    @classmethod
    def _handle_sabotage_action(cls, state: AmongUsState, player_id: str, move: Dict[str, Any]) -> AmongUsState:
        """Handle an impostor sabotaging a system."""
        player_state = state.player_states[player_id]
        
        # Validate player is an impostor
        if player_state["role"] != PlayerRole.IMPOSTOR:
            state.error_message = "Only impostors can sabotage"
            return state
        
        sabotage_type = move.get("sabotage_type")
        location = move.get("location")
        
        # Create the sabotage event
        sabotage = SabotageEvent(
            type=sabotage_type,
            location=location,
            timer=60,  # Default 60 second timer
            resolved=False
        )
        
        state.sabotages.append(sabotage)
        
        return state
    
    @classmethod
    def get_legal_moves(cls, state: AmongUsState, player_id: str) -> List[Dict[str, Any]]:
        """Get legal moves for a specific player."""
        if player_id not in state.player_states:
            return []
        
        player_state = state.player_states[player_id]
        
        # Dead players can only observe
        if not player_state.is_alive:
            return [{"action": "observe"}]
        
        legal_moves = []
        
        # Handle different game phases
        if state.game_phase == AmongUsGamePhase.TASKS:
            # Movement
            for location in state.map_locations:
                if location != player_state.location:
                    legal_moves.append({
                        "action": "move",
                        "location": location
                    })
            
            # Task completion (for crewmates)
            if player_state.role == PlayerRole.CREWMATE:
                for task in player_state.tasks:
                    if task.location == player_state.location and task.status != TaskStatus.COMPLETED:
                        legal_moves.append({
                            "action": "complete_task",
                            "task_id": task.id
                        })
            
            # Kill action (for impostors)
            if player_state.role == PlayerRole.IMPOSTOR:
                targets = cls._get_potential_targets(state, player_id)
                for target_id in targets:
                    legal_moves.append({
                        "action": "kill",
                        "target_id": target_id
                    })
            
            # Report action
            dead_bodies = [
                pid for pid, pstate in state.player_states.items()
                if not pstate.is_alive and pstate.location == player_state.location
            ]
            if dead_bodies:
                legal_moves.append({
                    "action": "report_body"
                })
            
            # Emergency meeting
            if player_state.location == "cafeteria":
                legal_moves.append({
                    "action": "call_emergency_meeting"
                })
            
            # Sabotage (for impostors)
            if player_state.role == PlayerRole.IMPOSTOR:
                sabotage_types = ["lights", "o2", "reactor", "comms"]
                for sabotage_type in sabotage_types:
                    legal_moves.append({
                        "action": "sabotage",
                        "sabotage_type": sabotage_type,
                        "location": sabotage_type
                    })
        
        elif state.game_phase == AmongUsGamePhase.MEETING:
            # Discussion 
            legal_moves.append({
                "action": "discuss",
                "message": "[Your message here]"
            })
        
        elif state.game_phase == AmongUsGamePhase.VOTING:
            # Voting
            for pid, pstate in state.player_states.items():
                if pstate.is_alive and pid != player_id:
                    legal_moves.append({
                        "action": "vote",
                        "vote_for": pid
                    })
            
            # Skip vote
            legal_moves.append({
                "action": "vote",
                "vote_for": "skip"
            })
        
        return legal_moves
    
    @classmethod
    def _get_potential_targets(cls, state: AmongUsState, player_id: str) -> List[str]:
        """Get potential kill targets for an impostor."""
        if player_id not in state.player_states:
            return []
            
        player_state = state.player_states[player_id]
        if player_state.role != PlayerRole.IMPOSTOR:
            return []
        
        # Find alive crewmates in the same location
        targets = []
        
        for pid, pstate in state.player_states.items():
            if (pid != player_id and
                pstate.is_alive and
                pstate.role == PlayerRole.CREWMATE and
                pstate.location == player_state.location):
                
                # Check for witnesses
                witnesses = [
                    wpid for wpid, wpstate in state.player_states.items()
                    if (wpid != player_id and
                        wpid != pid and
                        wpstate.is_alive and
                        wpstate.role != PlayerRole.IMPOSTOR and
                        wpstate.location == player_state.location)
                ]
                
                if not witnesses:
                    targets.append(pid)
        
        return targets
    
    @classmethod
    def check_game_status(cls, state: AmongUsState) -> AmongUsState:
        """Check and update game status."""
        winner = cls._check_win_condition(state)
        
        if winner:
            state.game_phase = AmongUsGamePhase.GAME_OVER
            state.game_status = "ended"
            state.winner = winner
        
        return state
    
    @classmethod
    def _check_win_condition(cls, state: AmongUsState) -> Optional[str]:
        """Check if either side has won."""
        # Calculate task completion
        task_completion = cls._get_task_completion_percentage(state)
        
        if task_completion >= 100:
            return "crewmates"
        
        alive_impostors = sum(1 for pid, pstate in state.player_states.items()
                             if pstate.is_alive and pstate.role == PlayerRole.IMPOSTOR)
        
        alive_crewmates = sum(1 for pid, pstate in state.player_states.items()
                             if pstate.is_alive and pstate.role == PlayerRole.CREWMATE)
        
        if alive_impostors == 0:
            return "crewmates"
        
        if alive_impostors >= alive_crewmates:
            return "impostors"
        
        return None
    
    @classmethod
    def _get_task_completion_percentage(cls, state: AmongUsState) -> float:
        """Calculate task completion percentage."""
        # Only count real tasks (not impostor fake tasks)
        crewmate_tasks = []
        for pid, pstate in state.player_states.items():
            if pstate.role == PlayerRole.CREWMATE:
                crewmate_tasks.extend(pstate.tasks)
        
        total = len(crewmate_tasks)
        if total == 0:
            return 100.0
        
        completed = sum(1 for task in crewmate_tasks if task.status == TaskStatus.COMPLETED)
        return (completed / total) * 100
    
    @classmethod
    def advance_phase(cls, state: AmongUsState) -> AmongUsState:
        """Advance the game to the next phase."""
        if state.game_phase == AmongUsGamePhase.TASKS:
            # TASKS -> MEETING
            state.game_phase = AmongUsGamePhase.MEETING
            state.meeting_active = True
        
        elif state.game_phase == AmongUsGamePhase.MEETING:
            # MEETING -> VOTING
            state.game_phase = AmongUsGamePhase.VOTING
        
        elif state.game_phase == AmongUsGamePhase.VOTING:
            # VOTING -> TASKS
            state.game_phase = AmongUsGamePhase.TASKS
            state.meeting_active = False
            state.votes = {}
            state.round_number += 1
        
        return state
    
    # Patched version of the filter_state_for_player method to handle discussion_history

    @classmethod
    def filter_state_for_player(cls, state: 'AmongUsState', player_id: str) -> Dict[str, Any]:
        """Filter the state to include only information visible to a specific player."""
        if player_id not in state.player_states:
            return {}
            
        player_state = state.player_states[player_id]
        
        # Create a filtered copy of the state
        filtered_state = {
            "game_phase": state.game_phase,
            "map_locations": state.map_locations,
            "meeting_active": state.meeting_active,
            "meeting_caller": state.meeting_caller,
            "round_number": state.round_number,
            
            # Player-specific info
            "player_id": player_id,
            "location": player_state.location,
            "is_alive": player_state.is_alive,
            "role": player_state.role,
            "tasks": [task.dict() if hasattr(task, 'dict') else task for task in player_state.tasks],
            "observations": player_state.observations
        }
        
        # If player is impostor, add info about other impostors
        if player_state.role == PlayerRole.IMPOSTOR:
            filtered_state["fellow_impostors"] = [
                pid for pid, pstate in state.player_states.items()
                if pstate.role == PlayerRole.IMPOSTOR and pid != player_id
            ]
        
        # Info about other players
        visible_players = []
        for pid, pstate in state.player_states.items():
            if pid == player_id:
                continue
            
            # Basic info about all players
            player_info = {
                "id": pid,
                "is_alive": pstate.is_alive
            }
            
            # Add location if they're visible (same location or meeting)
            if (pstate.location == player_state.location or 
                state.game_phase in [AmongUsGamePhase.MEETING, AmongUsGamePhase.VOTING]):
                player_info["location"] = pstate.location
            
            # Add role only if they're a fellow impostor
            if player_state.role == PlayerRole.IMPOSTOR and pstate.role == PlayerRole.IMPOSTOR:
                player_info["role"] = "impostor"
            else:
                player_info["role"] = "unknown"
            
            visible_players.append(player_info)
        
        filtered_state["visible_players"] = visible_players
        
        # Meeting and voting info
        if state.game_phase in [AmongUsGamePhase.MEETING, AmongUsGamePhase.VOTING]:
            # Only add discussion_history if it exists in the state
            if hasattr(state, "discussion_history"):
                filtered_state["discussion_history"] = getattr(state, "discussion_history", [])
            else:
                filtered_state["discussion_history"] = []
                
            if state.game_phase == AmongUsGamePhase.VOTING:
                # Show who has voted but not who they voted for
                filtered_state["voted_players"] = list(state.votes.keys())
                
                # Show my vote if I've voted
                if player_id in state.votes:
                    filtered_state["my_vote"] = state.votes[player_id]
        
        return filtered_state