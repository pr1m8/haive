"""Mafia game agent implementation.

This module provides the core agent implementation for the Mafia game,
handling:
    - Game initialization and setup
    - Player turn management
    - Move generation and validation
    - Game state visualization
    - Role-specific behavior

The agent uses LLMs to generate player decisions and narrator actions,
creating an engaging and strategic game experience.

Example:
    >>> from mafia.agent import MafiaAgent
    >>> from mafia.config import MafiaAgentConfig
    >>> 
    >>> # Create and initialize agent
    >>> config = MafiaAgentConfig.default_config(player_count=7)
    >>> agent = MafiaAgent(config)
    >>> 
    >>> # Run the game
    >>> for state in agent.app.stream(initial_state):
    ...     agent.visualize_state(state)
"""

from typing import Dict, Any, List, Optional, Union
from langgraph.types import Command
from src.haive.games.framework.multi_player.agent import MultiPlayerGameAgent
from .models import (
    PlayerRole, GamePhase, ActionType,
    MafiaAction, NarratorAction, PlayerState, MafiaPlayerDecision, NarratorDecision
)
import logging
from .state_manager import MafiaStateManager
from .config import MafiaAgentConfig
from src.haive.core.engine.agent.agent import register_agent
from .state import MafiaGameState
import time
import copy

# Set up logging
logger = logging.getLogger(__name__)

@register_agent(MafiaAgentConfig)
class MafiaAgent(MultiPlayerGameAgent[MafiaAgentConfig]):
    """Agent for playing Mafia.
    
    This class implements the core game logic for Mafia, managing player
    turns, move generation, and game progression.

    The agent handles:
        - Role assignment and management
        - Turn sequencing and validation
        - LLM-based decision making
        - Game state visualization
        - Win condition checking

    Attributes:
        state_manager (MafiaStateManager): Manager for game state
        role_enum_mapping (Dict[PlayerRole, str]): Role to engine mapping
        role_mapping (Dict[str, PlayerRole]): Engine to role mapping

    Example:
        >>> config = MafiaAgentConfig.default_config(player_count=7)
        >>> agent = MafiaAgent(config)
        >>> initial_state = MafiaStateManager.initialize(
        ...     ["Player_1", "Player_2", "Narrator"]
        ... )
        >>> for state in agent.app.stream(initial_state):
        ...     agent.visualize_state(state)
    """

    def __init__(self, config: MafiaAgentConfig):
        """Initialize the Mafia agent.
        
        Args:
            config (MafiaAgentConfig): Configuration for the agent

        Example:
            >>> config = MafiaAgentConfig.default_config(player_count=7)
            >>> agent = MafiaAgent(config)
        """
        super().__init__(config)
        self.state_manager = MafiaStateManager
        
        # Create a direct mapping between PlayerRole enum values and engine keys
        self.role_enum_mapping = {
            PlayerRole.VILLAGER: "villager",
            PlayerRole.MAFIA: "mafia",
            PlayerRole.DETECTIVE: "detective",
            PlayerRole.DOCTOR: "doctor",
            PlayerRole.NARRATOR: "narrator"
        }
        
        # Create the reverse mapping for lookups
        self.role_mapping = {value: key for key, value in self.role_enum_mapping.items()}
        print(self.role_mapping)

    def get_player_role(self, state: MafiaGameState, player_id: str) -> PlayerRole:
        """Get the role of a player.
        
        Args:
            state (MafiaGameState): Current game state
            player_id (str): ID of the player to check

        Returns:
            PlayerRole: The player's role

        Raises:
            Exception: If player not found in state

        Example:
            >>> role = agent.get_player_role(state, "Player_1")
            >>> print(role)  # Shows PlayerRole.VILLAGER
        """
        # Handle narrator case specially
        print(player_id)
        if player_id.lower() == 'narrator':
            return PlayerRole.NARRATOR
        if player_id.lower() =='doctor':
            return PlayerRole.DOCTOR
        if player_id.lower() =='detective':
            return PlayerRole.DETECTIVE
        if player_id.lower() =='mafia':
            return PlayerRole.MAFIA
        # Check if the player_id exists in roles
        if player_id in state.roles:
            return state.roles[player_id]
        
        return Exception(f"Player {player_id} not found in state")
        # Default to VILLAGER if role not found
        #return PlayerRole.VILLAGER
    
    def get_engine_for_player(self, role: Union[PlayerRole, str], function: str) -> Optional[Any]:
        """Get the appropriate engine for a player based on role and function.
        
        Args:
            role (Union[PlayerRole, str]): Player's role or role string
            function (str): Function type (e.g., "player")

        Returns:
            Optional[Any]: Engine configuration if found, None otherwise

        Example:
            >>> engine = agent.get_engine_for_player(
            ...     PlayerRole.MAFIA, "player"
            ... )
            >>> print(engine.name)  # Shows "mafia_player"
        """
        # 1. If role is an enum, convert to normalized string key
        if isinstance(role, PlayerRole):
            role_key = self.role_enum_mapping.get(role, role.value.lower())
        else:
            role_key = str(role).lower()  # Normalize to lowercase
        
        logger.debug(f"Looking for engine with role: {role_key}, function: {function}")
        
        # 2. Check engines directly
        if role_key in self.engines and function in self.engines[role_key]:
            return self.engines[role_key][function]
        
        # 3. Try some variations of the role key
        role_variations = [
            role_key,
            role_key.lower(),
            role_key.upper(),
            role_key.capitalize()
        ]
        
        for variation in role_variations:
            if variation in self.engines and function in self.engines[variation]:
                return self.engines[variation][function]
        
        # 4. Log failure and return None
        logger.error(f"No engine found for {role} ({type(role)}), function {function}")
        logger.error(f"Available engines: {list(self.engines.keys())}")
        
        return None
        
    def prepare_move_context(self, state: MafiaGameState, player_id: str) -> Dict[str, Any]:
        """Prepare context for move generation.
        
        This method gathers all relevant information for a player's move,
        including:
            - Game state information
            - Player-specific knowledge
            - Legal moves
            - Recent history

        Args:
            state (MafiaGameState): Current game state
            player_id (str): ID of the player making the move

        Returns:
            Dict[str, Any]: Context for move generation

        Example:
            >>> context = agent.prepare_move_context(state, "Player_1")
            >>> print(context["phase"])  # Shows current game phase
        """
        # Get player's role
        player_role = self.get_player_role(state, player_id)
        role_name = player_role.value if player_role else "unknown"
        
        # Get player's state
        player_state = state.player_states.get(player_id)
        
        # Get legal moves
        legal_moves = self.state_manager.get_legal_moves(state, player_id)
        formatted_legal_moves = [str(move) for move in legal_moves]
        
        # Create a summary of the game state
        alive_players = [pid for pid, p_state in state.player_states.items() if p_state.is_alive]
        dead_players = [pid for pid, p_state in state.player_states.items() if not p_state.is_alive]
        
        # Recent actions visible to the player
        visible_actions = []
        for action in state.action_history[-10:]:  # Last 10 actions
            # Night actions are private except to narrator and the player who did the action
            if isinstance(action, dict) and action.get('phase') == GamePhase.NIGHT.value:
                action_player_id = action.get('player_id')
                if action_player_id == player_id or player_role == PlayerRole.NARRATOR:
                    visible_actions.append(str(action))
            else:
                visible_actions.append(str(action))
        
        # Get public announcements
        public_info = state.public_announcements[-10:]  # Last 10 announcements
        
        # Get player-specific information
        private_info = []
        
        # Special information based on role
        if player_role == PlayerRole.MAFIA:
            # Mafia know who other mafia are
            other_mafia = [pid for pid, role in state.roles.items() 
                        if role == PlayerRole.MAFIA and pid != player_id and state.player_states[pid].is_alive]
            if other_mafia:
                private_info.append(f"Your fellow mafia members are: {', '.join(other_mafia)}")
            else:
                private_info.append("You are the only remaining mafia member.")
        
        elif player_role == PlayerRole.DETECTIVE:
            # Detectives know the results of their investigations
            if player_state and hasattr(player_state, 'investigation_results') and player_state.investigation_results:
                for target, is_mafia in player_state.investigation_results.items():
                    result = "is mafia" if is_mafia else "is not mafia"
                    private_info.append(f"Your investigation revealed: {target} {result}")
        
        # Prepare task based on phase
        current_task = "Wait for your turn"
        
        if state.game_phase == GamePhase.NIGHT:
            if player_role == PlayerRole.MAFIA:
                current_task = "Choose a player to kill tonight"
            elif player_role == PlayerRole.DOCTOR:
                current_task = "Choose a player to save tonight"
            elif player_role == PlayerRole.DETECTIVE:
                current_task = "Choose a player to investigate tonight"
            else:
                current_task = "Wait for night actions to complete"
        
        elif state.game_phase == GamePhase.DAY_DISCUSSION:
            current_task = "Discuss what happened and who might be mafia"
        
        elif state.game_phase == GamePhase.DAY_VOTING:
            current_task = "Vote for who you suspect is mafia"
        
        # Prepare phase context
        phase_context = {"task": current_task}
        
        if state.game_phase == GamePhase.DAY_DISCUSSION and state.votes:
            vote_summary = []
            for voter, votee in state.votes.items():
                vote_summary.append(f"{voter} voted for {votee}")
            phase_context["current_votes"] = vote_summary
        
        elif state.game_phase == GamePhase.DAY_VOTING and player_id in state.votes:
            phase_context["your_vote"] = state.votes[player_id]
        
        # Complete context with both variations of phase_context access
        return {
            "player_id": player_id,
            "role": role_name,
            "phase": state.game_phase.value,
            "day_number": state.day_number,
            "round_number": state.round_number,
            "alive_players": alive_players,
            "dead_players": dead_players,
            "legal_moves": formatted_legal_moves,
            "public_info": public_info,
            "private_info": private_info,
            "recent_actions": visible_actions,
            "phase_context": phase_context,
            "phase_context_task": current_task  # Direct field for compatibility
        }
    
    def prepare_narrator_context(self, state: MafiaGameState) -> Dict[str, Any]:
        """Prepare context for narrator actions.
        
        This method gathers all information needed for narrator decisions,
        including:
            - Complete game state
            - Player summaries
            - Phase-specific information
            - Action histories

        Args:
            state (MafiaGameState): Current game state

        Returns:
            Dict[str, Any]: Context for narrator decisions

        Example:
            >>> context = agent.prepare_narrator_context(state)
            >>> print(context["phase"])  # Shows current game phase
        """
        # Create a detailed game state summary for the narrator
        player_summary = []
        for player_id, player_state in state.player_states.items():
            status = "alive" if player_state.is_alive else "dead"
            role = state.roles.get(player_id, "unknown")
            player_summary.append(f"{player_id}: {role.value}, {status}")
        
        # Get phase-specific information
        phase_info = {}
        
        if state.game_phase == GamePhase.NIGHT:
            # Track night actions
            phase_info["killed_player"] = state.killed_at_night
            phase_info["saved_player"] = state.saved_at_night
            
            # Count completed actions
            expected_actions = 0
            completed_actions = 0
            
            for player_id, role in state.roles.items():
                if state.player_states[player_id].is_alive:
                    if role in [PlayerRole.MAFIA, PlayerRole.DOCTOR, PlayerRole.DETECTIVE]:
                        expected_actions += 1
                        # Check if action was performed
                        for action in reversed(state.action_history):
                            action_player = None
                            if isinstance(action, dict):
                                action_player = action.get('player_id')
                                action_phase = action.get('phase')
                                action_round = action.get('round_number')
                            else:
                                action_player = getattr(action, 'player_id', None)
                                action_phase = getattr(action, 'phase', None)
                                action_round = getattr(action, 'round_number', None)
                                
                            if (action_player == player_id and 
                                action_phase == GamePhase.NIGHT.value and 
                                action_round == state.round_number):
                                completed_actions += 1
                                break
            
            phase_info["expected_actions"] = expected_actions
            phase_info["completed_actions"] = completed_actions
        
        elif state.game_phase == GamePhase.DAY_VOTING:
            # Track voting
            votes = {}
            for voter, votee in state.votes.items():
                if votee in votes:
                    votes[votee].append(voter)
                else:
                    votes[votee] = [voter]
            
            vote_counts = {votee: len(voters) for votee, voters in votes.items()}
            phase_info["votes"] = votes
            phase_info["vote_counts"] = vote_counts
            
            # Count expected votes
            expected_votes = len([pid for pid, p_state in state.player_states.items() if p_state.is_alive])
            phase_info["expected_votes"] = expected_votes
            phase_info["completed_votes"] = len(state.votes)
        
        # Create a task field for the narrator
        current_task = "Observe and narrate the game"
        if state.game_phase == GamePhase.NIGHT and phase_info.get("completed_actions") == phase_info.get("expected_actions"):
            current_task = "Resolve night actions and transition to day"
        elif state.game_phase == GamePhase.DAY_VOTING and phase_info.get("completed_votes") == phase_info.get("expected_votes"):
            current_task = "Count votes and transition to night"
        
        # Add phase_context_task for compatibility
        phase_context = {"task": current_task}
        
        # Complete context
        return {
            "player_summary": player_summary,
            "phase": state.game_phase.value,
            "day_number": state.day_number,
            "round_number": state.round_number,
            "alive_mafia_count": state.alive_mafia_count,
            "alive_village_count": state.alive_village_count,
            "phase_info": phase_info,
            "public_announcements": state.public_announcements[-5:],
            "action_history": [str(action) for action in state.action_history[-10:]],
            "phase_context": phase_context,
            "phase_context_task": current_task  # Direct field for compatibility
        }
    
    def extract_move(self, response, player_id: str) -> Union[MafiaAction, NarratorAction]:
        """Extract move from engine response.
        
        This method processes the LLM response into a valid game action,
        handling:
            - Response validation
            - Action type conversion
            - Default action generation
            - Error handling

        Args:
            response: Raw response from the LLM
            player_id (str): ID of the player making the move

        Returns:
            Union[MafiaAction, NarratorAction]: Validated game action

        Example:
            >>> response = engine.invoke(context)
            >>> move = agent.extract_move(response, "Player_1")
            >>> print(move.action_type)  # Shows the action type
        """
        logger.debug(f"Extracting move from response: {response}")
        
        # Determine role from player_id
        role = "narrator" if player_id.lower() == "narrator" else "player"
        if hasattr(self, 'state') and self.state and player_id in self.state.roles:
            role = self.state.roles[player_id].value
        
        # Add specific debug for doctor's move
        if role.lower() == "doctor":
            logger.info(f"Doctor's decision: {response}")
        
        # Handle response from Schema models
        if hasattr(response, 'action_type'):
            # This is a MafiaPlayerDecisionSchema
            action_type_str = response.action_type
            # Convert string to ActionType enum
            try:
                action_type = ActionType(action_type_str)
            except ValueError:
                logger.warning(f"Unknown action type: {action_type_str}, defaulting to SPEAK")
                action_type = ActionType.SPEAK
            
            # Get current state info
            state = self.state if hasattr(self, 'state') else None
            current_phase = state.game_phase if state else GamePhase.NIGHT
            round_number = state.round_number if state else 1
            
            # Create MafiaAction
            action = MafiaAction(
                player_id=player_id,
                action_type=action_type,
                phase=current_phase,
                round_number=round_number,
                target_id=response.target_id,
                message=response.message
            )
            
            if role.lower() == "doctor" and action_type == ActionType.SAVE:
                logger.info(f"Doctor chose to save: {response.target_id}")
            
            return action
        
        elif hasattr(response, 'announcement') and hasattr(response, 'phase_transition'):
            # This is a NarratorDecisionSchema
            action = NarratorAction(
                announcement=response.announcement,
                phase_transition=response.phase_transition,
                round_number=1
            )
            return action
        
        # The old approach for handling directly returned actions
        if isinstance(response, MafiaAction) or isinstance(response, NarratorAction):
            # Make sure round_number is set for MafiaAction
            if isinstance(response, MafiaAction) and not hasattr(response, 'round_number'):
                response.round_number = 1  # Default to round 1 if none set
            return response
        
        # Handle player decision
        if isinstance(response, MafiaPlayerDecision):
            action = response.action
            # Add debug logging for doctor actions
            if role.lower() == "doctor" and hasattr(action, 'action_type'):
                if action.action_type == ActionType.SAVE:
                    logger.info(f"Doctor chose to save: {action.target_id}")
                    
            # Ensure round_number is set
            if action and hasattr(action, 'round_number') and action.round_number is None:
                action.round_number = 1
            return action
        
        # Handle narrator decision
        if isinstance(response, NarratorDecision):
            action = getattr(response, 'action', None)
            if action is None:
                # Create a default narrator action if none provided
                action = NarratorAction(
                    announcement="The narrator observes silently.",
                    phase_transition=False,
                    round_number=1
                )
            # Ensure round_number is set
            if action.round_number is None:
                action.round_number = 1
            return action
        
        # Handle dict response (for backwards compatibility)
        if isinstance(response, dict):
            if 'action_type' in response:
                # This is from MafiaPlayerDecisionSchema
                action_type_str = response['action_type']
                try:
                    action_type = ActionType(action_type_str)
                except ValueError:
                    logger.warning(f"Unknown action type: {action_type_str}, defaulting to SPEAK")
                    action_type = ActionType.SPEAK
                    
                # Get current state info
                state = self.state if hasattr(self, 'state') else None
                current_phase = state.game_phase if state else GamePhase.NIGHT
                round_number = state.round_number if state else 1
                
                return MafiaAction(
                    player_id=player_id,
                    action_type=action_type,
                    phase=current_phase,
                    round_number=round_number,
                    target_id=response.get('target_id'),
                    message=response.get('message')
                )
                
            elif 'announcement' in response:
                # This is from NarratorDecisionSchema
                return NarratorAction(
                    announcement=response.get('announcement'),
                    phase_transition=response.get('phase_transition', False),
                    round_number=1
                )
            
            elif 'action' in response:
                # Old format with action field
                action = response['action']
                # Convert to proper action object if needed
                if isinstance(action, dict):
                    if 'announcement' in action:
                        # It's a narrator action
                        return NarratorAction(**action)
                    else:
                        # It's a player action
                        action_dict = action.copy()
                        if 'round_number' not in action_dict:
                            action_dict['round_number'] = 1
                        return MafiaAction(**action_dict)
                return action
        
        # If we got here, we need to create a default action based on role
        logger.warning(f"Creating default action for {player_id} - unexpected response type: {type(response)}")
        
        if role.lower() == "narrator":
            return NarratorAction(
                announcement="The narrator observes silently.",
                phase_transition=False,
                round_number=1
            )
        elif role.lower() == "doctor":
            # For doctor, create a SAVE action with a random target if possible
            alive_players = []
            if hasattr(self, 'state'):
                alive_players = [pid for pid, p_state in self.state.player_states.items() 
                                if p_state.is_alive]
            
            target = alive_players[0] if alive_players else "Player_1"
            logger.info(f"Created default SAVE action for doctor targeting {target}")
            
            return MafiaAction(
                player_id=player_id,
                action_type=ActionType.SAVE,
                target_id=target,
                phase=GamePhase.NIGHT,
                round_number=1
            )
        else:
            # Default for other roles
            return MafiaAction(
                player_id=player_id,
                action_type=ActionType.SPEAK,
                message="I have nothing to say.",
                phase=GamePhase.NIGHT,
                round_number=1
            )
    
    def handle_player_turn(self, state: MafiaGameState) -> Dict[str, Any]:
        """Handle a player's turn with special Mafia logic.
        
        This method manages a player's turn, including:
            - Role-specific behavior
            - Move generation and validation
            - State updates
            - Error handling

        Args:
            state (MafiaGameState): Current game state

        Returns:
            Dict[str, Any]: Updated game state after the turn

        Example:
            >>> new_state = agent.handle_player_turn(state)
            >>> print(new_state["game_phase"])  # Shows current phase
        """
        # Make a copy of state available for other methods
        self.state = state
        
        # Get current player
        current_idx = state.current_player_idx
        
        try:
            player_id = state.players[current_idx]
        except IndexError:
            logger.error(f"Invalid player index: {current_idx}, max: {len(state.players)-1}")
            # Default to first player
            player_id = state.players[0] if state.players else "Player_1"
        
        logger.info(f"Handling turn for player: {player_id}")
        
        # Create a deep copy of the state for modification
        new_state = copy.deepcopy(state)
        
        # Get player's role
        player_role = self.get_player_role(state, player_id)
        logger.info(f"Player {player_id} has role {player_role}")
        
        # Skip if player is dead
        if player_id in state.player_states and not state.player_states[player_id].is_alive:
            logger.info(f"Player {player_id} is dead, skipping turn")
            # Advance to next player
            next_idx = (current_idx + 1) % len(state.players)
            new_state.current_player_idx = next_idx
            return self.state_to_dict(new_state)
        
        # Special handling for narrator
        if player_role == PlayerRole.NARRATOR:
            logger.info(f"Handling narrator turn for {player_id}")
            return self.handle_narrator_turn(state)
        
        # Skip villagers during the night (but NOT doctors or other special roles)
        if state.game_phase == GamePhase.NIGHT and player_role == PlayerRole.VILLAGER:
            logger.info(f"Skipping villager {player_id} during night phase")
            # Advance to next player
            next_idx = (current_idx + 1) % len(state.players)
            new_state.current_player_idx = next_idx
            return self.state_to_dict(new_state)
        
        # Get the move engine for this role
        move_engine = self.get_engine_for_player(player_role, "player")
        
        # If no engine found, log error and move to next player
        if not move_engine:
            logger.error(f"No move engine found for player {player_id} with role {player_role}")
            # Move to next player
            next_idx = (current_idx + 1) % len(state.players)
            new_state.current_player_idx = next_idx
            new_state.public_announcements.append(f"{player_id} is unable to act.")
            return self.state_to_dict(new_state)
        
        try:
            # Prepare context for the move
            context = self.prepare_move_context(state, player_id)
            logger.debug(f"Prepared context for {player_id}: {list(context.keys())}")
            
            # CRITICAL CHANGE: Set a default timeout to prevent hanging
            from concurrent.futures import ThreadPoolExecutor, TimeoutError, wait, FIRST_COMPLETED
            
            # Set a timeout for engine invocation
            with ThreadPoolExecutor() as executor:
                # Add a timeout to the move engine invocation
                future = executor.submit(move_engine.invoke, context)
                
                # Wait for 10 seconds or until completion
                done, not_done = wait([future], timeout=10, return_when=FIRST_COMPLETED)
                
                if future in done:
                    # Engine completed normally, get response
                    response = future.result()
                    logger.info(f"Got response from engine for player {player_id}")
                else:
                    # Engine took too long, create a default response and move on
                    logger.warning(f"Engine for player {player_id} timed out, using default action")
                    response = None
            
            # Add fallback if response is None
            if response is None:
                # Create default action based on role
                if player_role == PlayerRole.MAFIA:
                    # Pick random target for mafia
                    import random
                    targets = [pid for pid, p_state in state.player_states.items()
                            if p_state.is_alive and pid != player_id 
                            and state.roles.get(pid) != PlayerRole.MAFIA]
                    
                    if targets:
                        target = random.choice(targets)
                        response = MafiaAction(
                            player_id=player_id,
                            action_type=ActionType.KILL,
                            target_id=target,
                            phase=state.game_phase,
                            round_number=state.round_number
                        )
                        logger.info(f"Created default kill action for {player_id} targeting {target}")
                
                # Other default responses could be added for doctor/detective roles
                elif player_role == PlayerRole.DOCTOR:
                    # Pick random target for doctor
                    import random
                    targets = [pid for pid, p_state in state.player_states.items()
                            if p_state.is_alive]
                    
                    if targets:
                        target = random.choice(targets)
                        response = MafiaAction(
                            player_id=player_id,
                            action_type=ActionType.SAVE,
                            target_id=target,
                            phase=state.game_phase,
                            round_number=state.round_number
                        )
                        logger.info(f"Created default save action for {player_id} targeting {target}")
                
                # If still no response, create a "skip turn" message
                if response is None:
                    response = MafiaAction(
                        player_id=player_id,
                        action_type=ActionType.SPEAK,
                        message="I pass my turn.",
                        phase=state.game_phase,
                        round_number=state.round_number
                    )
                    logger.info(f"Created default speak action for {player_id}")
            
            # Extract move from response
            move = self.extract_move(response, player_id)
            logger.info(f"Player {player_id} move: {move}")
            
            # Apply move to state
            updated_state = self.state_manager.apply_move(new_state, player_id, move)
            
            # Move to next player
            next_idx = (current_idx + 1) % len(state.players)
            updated_state.current_player_idx = next_idx
            
            # Return the updated state
            return self.state_to_dict(updated_state)
        
        except Exception as e:
            # If any error occurs, log it and move to next player
            logger.error(f"Error processing turn for {player_id}: {str(e)}", exc_info=True)
            next_idx = (current_idx + 1) % len(state.players)
            new_state.current_player_idx = next_idx
            new_state.public_announcements.append(f"{player_id} encountered an error during their turn.")
            return self.state_to_dict(new_state)
            
    def handle_narrator_turn(self, state: MafiaGameState) -> Dict[str, Any]:
        """Handle the narrator's turn.
        
        This method manages narrator actions, including:
            - Phase transitions
            - Night action resolution
            - Public announcements
            - Game state updates

        Args:
            state (MafiaGameState): Current game state

        Returns:
            Dict[str, Any]: Updated game state after narrator action

        Example:
            >>> new_state = agent.handle_narrator_turn(state)
            >>> print(new_state["public_announcements"][-1])
        """
        # Make state accessible to other methods
        self.state = state
        
        # Get the narrator engine
        narrator_engine = None
        
        # Try direct lookup with all possible variations
        narrator_variations = ["Narrator", "narrator", "NARRATOR"]
        for variation in narrator_variations:
            if variation in self.engines and "player" in self.engines[variation]:
                narrator_engine = self.engines[variation]["player"]
                break
        
        # Try through role_enum_mapping
        if not narrator_engine:
            role_key = self.role_enum_mapping.get(PlayerRole.NARRATOR)
            if role_key in self.engines and "player" in self.engines[role_key]:
                narrator_engine = self.engines[role_key]["player"]
        
        if not narrator_engine:
            error_msg = "No narrator engine found"
            logger.error(error_msg)
            logger.error(f"Available engines: {list(self.engines.keys())}")
            state_dict = self.state_to_dict(state)
            state_dict["error_message"] = error_msg
            return state_dict
        
        try:
            # Prepare narrator context
            narrator_context = self.prepare_narrator_context(state)
            logger.debug("Prepared narrator context")
            
            # Get decision from the engine
            logger.debug("Invoking narrator engine")
            response = narrator_engine.invoke(narrator_context)
            logger.debug(f"Got narrator response: {response}")
            
            # Find the narrator's player_id
            narrator_id = None
            for pid, role in state.roles.items():
                if role == PlayerRole.NARRATOR:
                    narrator_id = pid
                    break
            
            if not narrator_id:
                # Fallback to the last player in the list
                narrator_id = state.players[-1]
            
            # Extract the action
            action = self.extract_move(response, narrator_id)
            logger.debug(f"Extracted narrator action: {action}")
            
            # Apply action to state
            logger.debug(f"Applying narrator action using ID: {narrator_id}")
            new_state = self.state_manager.apply_move(state, narrator_id, action)
            
            # If we need to resolve night actions
            if (state.game_phase == GamePhase.NIGHT and 
                action.phase_transition and 
                state.killed_at_night is not None):
                new_state = self.state_manager.resolve_night_actions(new_state)
                logger.debug("Resolved night actions")
            
            # Convert to dict for the graph
            return self.state_to_dict(new_state)
            
        except Exception as e:
            error_msg = f"Error in narrator's turn: {str(e)}"
            logger.error(f"{error_msg}\n", exc_info=True)
            state_dict = self.state_to_dict(state)
            state_dict["error_message"] = error_msg
            return state_dict
    
    def determine_next_step_after_player_turn(self, state: MafiaGameState) -> str:
        """Determine what to do after a player's turn.
        
        This method decides the next game action based on:
            - Current game phase
            - Completed actions
            - Game end conditions
            - Maximum day limit

        Args:
            state (MafiaGameState): Current game state

        Returns:
            str: Next action ("end_game", "phase_transition", or "next_player")

        Example:
            >>> next_step = agent.determine_next_step_after_player_turn(state)
            >>> print(next_step)  # Shows what happens next
        """
        # If game is over, end the game
        if state.game_status != "ongoing" or state.game_phase == GamePhase.GAME_OVER:
            logger.debug("Game is over, ending game")
            return "end_game"
        
        # Check for maximum days limit
        if hasattr(self.config, 'max_days') and state.day_number > self.config.max_days:
            logger.info(f"Reached maximum days limit ({self.config.max_days}), ending game")
            return "end_game"
        
        # If night phase and all night actions are complete, transition to day
        if state.game_phase == GamePhase.NIGHT:
            all_night_actions_complete = True
            
            # Check if all expected night actors have acted
            for player_id, role in state.roles.items():
                # Skip narrator and dead players
                if role == PlayerRole.NARRATOR or not state.player_states[player_id].is_alive:
                    continue
                    
                if role in [PlayerRole.MAFIA, PlayerRole.DOCTOR, PlayerRole.DETECTIVE]:
                    has_acted = False
                    for action in reversed(state.action_history):
                        action_player = None
                        action_phase = None
                        action_round = None
                        
                        if isinstance(action, dict):
                            action_player = action.get('player_id')
                            action_phase = action.get('phase')
                            action_round = action.get('round_number')
                        else:
                            action_player = getattr(action, 'player_id', None)
                            action_phase = getattr(action, 'phase', None)
                            action_round = getattr(action, 'round_number', None)
                        
                        # Convert phase to string value if it's an enum
                        if isinstance(action_phase, GamePhase):
                            action_phase = action_phase.value
                            
                        if (action_player == player_id and 
                            action_phase == GamePhase.NIGHT.value and 
                            action_round == state.round_number):
                            
                            has_acted = True
                            break
                    
                    if not has_acted:
                        all_night_actions_complete = False
                        break
            
            if all_night_actions_complete:
                logger.debug("All night actions complete, transitioning to day phase")
                return "phase_transition"
        
        # If day voting phase and all votes are in, transition to night
        if state.game_phase == GamePhase.DAY_VOTING:
            alive_players = [pid for pid, p_state in state.player_states.items() 
                            if p_state.is_alive and state.roles.get(pid) != PlayerRole.NARRATOR]
            
            if len(state.votes) >= len(alive_players):
                logger.debug("All votes are in, transitioning to next phase")
                return "phase_transition"
        
        # Get current player
        current_idx = state.current_player_idx
        try:
            player_id = state.players[current_idx]
        except IndexError:
            logger.error(f"Invalid player index: {current_idx}, max: {len(state.players)-1}")
            player_id = state.players[0] if state.players else "Player_1"
        
        # Check if current player is narrator
        is_narrator = False
        for pid, role in state.roles.items():
            if pid == player_id and role == PlayerRole.NARRATOR:
                is_narrator = True
                break
        
        # If current player is narrator, always let narrator act
        if is_narrator:
            logger.debug("Current player is narrator, continuing with narrator turn")
            # After a full round of players, let narrator transition the phase
            if state.game_phase == GamePhase.DAY_DISCUSSION:
                # Check if a full discussion round has occurred
                discussion_count = 0
                for action in reversed(state.action_history):
                    action_phase = None
                    action_round = None
                    
                    if isinstance(action, dict):
                        action_phase = action.get('phase')
                        action_round = action.get('round_number')
                    else:
                        action_phase = getattr(action, 'phase', None)
                        action_round = getattr(action, 'round_number', None)
                    
                    # Convert phase to string value if it's an enum
                    if isinstance(action_phase, GamePhase):
                        action_phase = action_phase.value
                        
                    if (action_phase == GamePhase.DAY_DISCUSSION.value and 
                        action_round == state.round_number):
                        discussion_count += 1
                
                alive_player_count = len([p for p, p_state in state.player_states.items() 
                                         if p_state.is_alive and state.roles.get(p) != PlayerRole.NARRATOR])
                
                if discussion_count >= alive_player_count:
                    logger.debug("Full discussion round completed, transitioning to voting phase")
                    return "phase_transition"
        
        # Otherwise, continue with next player
        logger.debug("Continuing with next player")
        return "next_player"

    def visualize_state(self, state_obj, debug=False):
        """Visualize the current game state.
        
        This method creates a human-readable display of:
            - Game phase and status
            - Player information
            - Recent announcements
            - Game statistics
            - Voting results (if applicable)

        Args:
            state_obj: Game state (dict, MafiaGameState, or agent)
            debug (bool, optional): Show debug information. Defaults to False.

        Example:
            >>> agent.visualize_state(state, debug=True)
        """
        try:
            # Handle the case where an agent was passed instead of a state
            if hasattr(state_obj, 'state') and state_obj.state is not None:
                state = state_obj.state
            elif isinstance(state_obj, dict):
                state = state_obj
            else:
                state = state_obj

            # Handle MafiaGameState objects
            if hasattr(state, 'model_dump'):
                state_dict = state.model_dump()
            elif hasattr(state, 'dict'):
                state_dict = state.dict()
            elif isinstance(state, dict):
                state_dict = state
            else:
                # Fallback to extracting attributes manually
                state_dict = {}
                for attr in dir(state):
                    if not attr.startswith('_') and not callable(getattr(state, attr)):
                        try:
                            state_dict[attr] = getattr(state, attr)
                        except Exception:
                            pass

            # Display basic game info
            print("\n" + "=" * 60)
            day_number = state_dict.get('day_number', 0)
            game_phase = state_dict.get('game_phase', 'unknown')
            if hasattr(game_phase, 'value'):
                game_phase = game_phase.value

            print(f"🎮 MAFIA GAME - Day {day_number}, {str(game_phase).replace('_', ' ').title()}")
            print(f"📌 Game Status: {state_dict.get('game_status', 'unknown')}")
            print("=" * 60)

            # Show players
            players = state_dict.get('players', [])
            player_states = state_dict.get('player_states', {})
            current_player_idx = state_dict.get('current_player_idx', 0)

            print("\n👥 Players:")
            current_player = None
            if 0 <= current_player_idx < len(players):
                current_player = players[current_player_idx]

            # Display player info
            for player_id, player_state in player_states.items():
                is_alive = player_state.get('is_alive', True) if isinstance(player_state, dict) else getattr(player_state, 'is_alive', True)
                status = "🟢 ALIVE" if is_alive else "🔴 DEAD"

                # Get role info for debug mode
                role_info = ""
                if debug:
                    roles = state_dict.get('roles', {})
                    player_role = roles.get(player_id, "unknown")
                    if hasattr(player_role, 'value'):
                        role_info = f" ({player_role.value})"
                    else:
                        role_info = f" ({player_role})"

                if player_id == current_player:
                    print(f"  ➡️ {player_id}{role_info}: {status}")
                else:
                    print(f"    {player_id}{role_info}: {status}")

            # Show announcements
            announcements = state_dict.get('public_announcements', [])
            if announcements:
                print("\n📢 Recent Announcements:")
                for announcement in announcements[-3:]:
                    print(f"  {announcement}")

            # Show game statistics
            alive_mafia = state_dict.get('alive_mafia_count', 0)
            alive_village = state_dict.get('alive_village_count', 0)
            alive_doctor = state_dict.get('alive_doctor_count', 0)
            alive_detective = state_dict.get('alive_detective_count', 0)

            print("\n📊 Game Statistics:")
            print(f"  Alive Villagers: {alive_village}")
            print(f"  Alive Mafia: {alive_mafia}")
            print(f"  Alive Doctors: {alive_doctor}")
            print(f"  Alive Detectives: {alive_detective}")

            # Show voting in voting phase
            votes = state_dict.get('votes', {})
            if game_phase == "day_voting" and votes:
                print("\n🗳️ Current Votes:")
                vote_count = {}
                for voter, votee in votes.items():
                    print(f"  {voter} voted for {votee}")
                    vote_count[votee] = vote_count.get(votee, 0) + 1

                print("\n📊 Vote Tally:")
                for votee, count in vote_count.items():
                    print(f"  {votee}: {count} vote(s)")

            # Show any errors
            error_message = state_dict.get('error_message')
            if error_message:
                print(f"\n❌ Error: {error_message}")

            # Show winner if game is over
            winner = state_dict.get('winner')
            if state_dict.get('game_status') != "ongoing" and winner:
                print("\n🏆 Winner: " + winner.upper())
                if winner == "mafia":
                    print("  The mafia has taken over the village!")
                else:
                    print("  The village has eliminated all mafia members!")

        except Exception as e:
            print(f"\n❌ Error visualizing state: {e}")
            print("\n📑 Raw State Information:")
            if isinstance(state_obj, dict):
                for key, value in state_obj.items():
                    print(f"  {key}: {str(value)[:100]}")
            else:
                print(f"  Type: {type(state_obj)}")
                print(f"  Content: {str(state_obj)[:200]}")

    def state_to_dict(self, state: MafiaGameState) -> Dict[str, Any]:
        """Convert state to dictionary consistently.
        
        This method handles various state formats and ensures consistent
        dictionary conversion for the game graph.

        Args:
            state (MafiaGameState): State to convert

        Returns:
            Dict[str, Any]: Dictionary representation of the state

        Example:
            >>> state_dict = agent.state_to_dict(state)
            >>> print(state_dict["game_phase"])
        """
        try:
            if hasattr(state, "model_dump"):
                return state.model_dump()
            elif hasattr(state, "dict"):
                return state.dict()
            elif isinstance(state, dict):
                # Already a dictionary
                return state
            else:
                # Manual conversion as fallback
                state_dict = {}
                for key in dir(state):
                    # Skip private attributes and methods
                    if key.startswith('_') or callable(getattr(state, key)):
                        continue
                    try:
                        state_dict[key] = getattr(state, key)
                    except Exception:
                        pass
                return state_dict
        except Exception as e:
            logger.error(f"Error converting state to dict: {e}")
            # Return minimal state to avoid failures
            return {
                "error_message": f"Error converting state: {str(e)}",
                "game_status": getattr(state, "game_status", "ongoing"),
                "players": getattr(state, "players", []),
                "current_player_idx": getattr(state, "current_player_idx", 0)
            }
