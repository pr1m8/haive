"""State management for the Mafia game.

This module provides the core state management functionality for the Mafia game,
handling game state transitions, move validation, and game progression logic.

The state manager is responsible for:
    - Game initialization and setup
    - Phase transitions (day/night cycles)
    - Move validation and application
    - Game state filtering for information hiding
    - Win condition checking

Example:
    >>> from mafia.state_manager import MafiaStateManager
    >>> 
    >>> # Initialize a new game
    >>> players = ["Player_1", "Player_2", "Player_3", "Narrator"]
    >>> state = MafiaStateManager.initialize(players)
    >>> 
    >>> # Apply a move
    >>> move = MafiaAction(
    ...     player_id="Player_1",
    ...     action_type=ActionType.VOTE,
    ...     target_id="Player_2",
    ...     phase=GamePhase.DAY_VOTING,
    ...     round_number=1
    ... )
    >>> new_state = MafiaStateManager.apply_move(state, "Player_1", move)
"""

import copy
import random
from typing import List, Dict, Any, Optional, Union, Tuple

from .models import (
    PlayerRole, GamePhase, ActionType,
    MafiaAction, NarratorAction, PlayerState
)
from src.haive.games.framework.multi_player.state_manager import MultiPlayerGameStateManager
from .state import MafiaGameState
from loguru import logger   

class MafiaStateManager(MultiPlayerGameStateManager[MafiaGameState]):
    """Manager for the Mafia game state.
    
    This class extends MultiPlayerGameStateManager to provide Mafia-specific
    state management functionality. It handles game progression, move validation,
    and state transitions.

    The manager maintains game state including:
        - Player roles and alive/dead status
        - Day/night cycle progression
        - Vote tracking and resolution
        - Night action resolution (kills, saves, investigations)
        - Win condition checking

    Note:
        This class is designed to be used statically, with all methods being
        class methods that take and return game states.
    """
    
    @classmethod
    def advance_phase(cls, state: MafiaGameState) -> MafiaGameState:
        """Advance the game to the next phase.
        
        This method handles the transition between game phases, including:
            - Setup → Night (first night)
            - Night → Day Discussion (with night action resolution)
            - Day Discussion → Day Voting
            - Day Voting → Night (with vote resolution)
            - Game Over checks at appropriate points

        Args:
            state (MafiaGameState): Current game state

        Returns:
            MafiaGameState: Updated game state with new phase and relevant changes

        Example:
            >>> new_state = MafiaStateManager.advance_phase(current_state)
            >>> print(new_state.game_phase)  # Shows the new phase
        """
        # Create a deep copy of the state to avoid modifying the original
        if hasattr(state, 'model_copy'):
            new_state = state.model_copy(deep=True)
        else:
            new_state = copy.deepcopy(state)
        
        # Get the current phase and determine the next phase
        current_phase = new_state.game_phase
        
        # Add debug logs
        logger.debug(f"Advancing phase from {current_phase}")
        logger.debug(f"Current state fields: {dir(new_state)}")
        
        # Make sure all required fields are present
        if not hasattr(new_state, 'day_number'):
            logger.debug("Adding missing day_number field")
            new_state.day_number = 0
        
        if not hasattr(new_state, 'round_number'):
            logger.debug("Adding missing round_number field")
            new_state.round_number = 0
        
        if not hasattr(new_state, 'killed_at_night'):
            logger.debug("Adding missing killed_at_night field")
            new_state.killed_at_night = None
        
        if not hasattr(new_state, 'saved_at_night'):
            logger.debug("Adding missing saved_at_night field")
            new_state.saved_at_night = None
        
        # Phase transition logic
        if current_phase == GamePhase.SETUP:
            # From SETUP, transition to NIGHT for the first night
            new_state.game_phase = GamePhase.NIGHT
            new_state.day_number = 1
            new_state.round_number += 1
            
            # Make sure add_public_announcement is available
            if hasattr(new_state, 'add_public_announcement'):
                new_state.add_public_announcement(
                    f"Night {new_state.day_number} falls upon the village. The residents go to sleep."
                )
            else:
                # Fallback to direct append
                if not hasattr(new_state, 'public_announcements'):
                    new_state.public_announcements = []
                new_state.public_announcements.append(
                    f"Night {new_state.day_number} falls upon the village. The residents go to sleep."
                )
        
            
        elif current_phase == GamePhase.NIGHT:
            # From NIGHT, transition to DAY_DISCUSSION
            new_state.game_phase = GamePhase.DAY_DISCUSSION
            new_state.add_public_announcement(f"Day {new_state.day_number} begins. The village awakens.")
            
            # Process night actions (usually done by narrator in their turn)
            # This is a fallback if narrator didn't process them
            if new_state.killed_at_night and new_state.killed_at_night != new_state.saved_at_night:
                victim_id = new_state.killed_at_night
                if victim_id in new_state.player_states:
                    new_state.player_states[victim_id].is_alive = False
                    new_state.add_public_announcement(f"{victim_id} was found dead this morning!")
        
        elif current_phase == GamePhase.DAY_DISCUSSION:
            # From DAY_DISCUSSION, transition to DAY_VOTING
            new_state.game_phase = GamePhase.DAY_VOTING
            new_state.votes = {}  # Reset votes
            new_state.add_public_announcement("The discussion period has ended. Time to vote!")
        
        elif current_phase == GamePhase.DAY_VOTING:
            # From DAY_VOTING, transition to NIGHT (or GAME_OVER if end conditions met)
            # Process votes first
            if new_state.votes:
                # Count votes
                vote_count = {}
                for _, voted_for in new_state.votes.items():
                    if voted_for in vote_count:
                        vote_count[voted_for] += 1
                    else:
                        vote_count[voted_for] = 1
                
                # Find player with most votes (handle ties by random selection)
                max_votes = 0
                tied_players = []
                for player, count in vote_count.items():
                    if count > max_votes:
                        max_votes = count
                        tied_players = [player]
                    elif count == max_votes:
                        tied_players.append(player)
                
                # Eliminate the chosen player
                if tied_players:
                    eliminated_player = random.choice(tied_players) if len(tied_players) > 1 else tied_players[0]
                    new_state.player_states[eliminated_player].is_alive = False
                    new_state.add_public_announcement(f"{eliminated_player} has been eliminated by the village vote!")
            
            # Check game end conditions
            if new_state.alive_mafia_count == 0:
                new_state.game_phase = GamePhase.GAME_OVER
                new_state.winner = "village"
                new_state.game_status = "ended"
                new_state.add_public_announcement("All mafia members have been eliminated! The village wins!")
                return new_state
            
            if new_state.alive_mafia_count >= new_state.alive_village_count:
                new_state.game_phase = GamePhase.GAME_OVER
                new_state.winner = "mafia"
                new_state.game_status = "ended"
                new_state.add_public_announcement("The mafia now equals or outnumbers the villagers! The mafia wins!")
                return new_state
                
            # Continue to next night
            new_state.game_phase = GamePhase.NIGHT
            new_state.day_number += 1
            new_state.round_number += 1
            new_state.killed_at_night = None
            new_state.saved_at_night = None
            new_state.add_public_announcement(f"Night {new_state.day_number} falls. The village sleeps.")
        
        elif current_phase == GamePhase.GAME_OVER:
            # Game is already over, do nothing
            pass
        
        # Reset current player to the first player for the new phase
        if current_phase != GamePhase.GAME_OVER:
            # For night phase, set to first alive player
            # For day phases, also set to first alive player
            alive_players = [idx for idx, pid in enumerate(new_state.players) if new_state.player_states[pid].is_alive]
            if alive_players:
                new_state.current_player_idx = alive_players[0]
        
        return new_state
    @classmethod
    def resolve_night_actions(cls,state: MafiaGameState) -> MafiaGameState:
        """Resolve night actions and determine outcomes.
        
        This method processes all night actions in the correct order:
            1. Mafia kill attempt
            2. Doctor save attempt
            3. Detective investigation results

        Args:
            state (MafiaGameState): Current game state with night actions recorded

        Returns:
            MafiaGameState: Updated state with night actions resolved

        Example:
            >>> # After all night actions are recorded
            >>> new_state = MafiaStateManager.resolve_night_actions(state)
            >>> if new_state.night_deaths:
            ...     print("Someone died tonight!")
        """
        new_state = copy.deepcopy(state)
        
        # Initialize night deaths if not present
        if not hasattr(new_state, 'night_deaths'):
            new_state.night_deaths = []
        
        # Check for mafia kill
        killed_player = new_state.killed_at_night
        saved_player = new_state.saved_at_night
        
        # Log night actions for debugging
        logger.info(f"Night actions - Kill: {killed_player}, Save: {saved_player}")
        
        # If doctor saved the target, they survive
        if killed_player and saved_player and killed_player == saved_player:
            logger.info(f"Doctor saved {saved_player} from being killed!")
            # Reset night action tracking
            new_state.killed_at_night = None
            new_state.saved_at_night = None
            return new_state
        
        # If kill wasn't prevented
        if killed_player:
            # Mark player as dead
            if killed_player in new_state.player_states:
                new_state.player_states[killed_player].is_alive = False
                
                # Track night deaths
                new_state.night_deaths.append(killed_player)
                
                # Update alive counts
                role = new_state.roles.get(killed_player)
                if role == PlayerRole.MAFIA:
                    new_state.alive_mafia_count -= 1
                    logger.info(f"Mafia member {killed_player} was killed at night")
                else:  # All other roles count as village
                    new_state.alive_village_count -= 1
                    logger.info(f"Villager {killed_player} was killed at night")
        
        # Reset night action tracking
        new_state.killed_at_night = None
        new_state.saved_at_night = None
        
        return new_state
    
    @classmethod
    def handle_phase_transition(cls, state: Dict[str, Any]) -> Dict[str, Any]:
        """Handle phase transition with error handling.
        
        This method safely transitions the game phase, handling any errors
        that might occur during the transition.

        Args:
            state (Dict[str, Any]): Current game state as a dictionary

        Returns:
            Dict[str, Any]: Updated state after phase transition

        Raises:
            Exception: If critical game state fields are missing

        Example:
            >>> try:
            ...     new_state = MafiaStateManager.handle_phase_transition(state)
            ... except Exception as e:
            ...     print(f"Phase transition failed: {e}")
        """
        logger.debug(f"Handling phase transition for state: {state.game_phase}")
        
        try:
            # Convert to MafiaGameState if it's a dict
            if isinstance(state, dict):
                # Check if we have the necessary fields
                if 'game_phase' not in state:
                    logger.error("game_phase not found in state")
                    state['error_message'] = "game_phase not found in state"
                    return state
                    
                # Create a proper game state
                from .state import MafiaGameState
                mafia_state = MafiaGameState.model_validate(state)
            else:
                mafia_state = state
            
            # Use the state manager to advance the phase
            new_state = cls.advance_phase(mafia_state)
            
            # Set current player to the first player for the new phase
            new_state.current_player_idx = 0
            
            # Convert back to dict for the graph
            if hasattr(new_state, 'model_dump'):
                return new_state.model_dump()
            elif hasattr(new_state, 'dict'):
                return new_state.dict()
            else:
                return dict(new_state)
                
        except Exception as e:
            error_msg = f"Error in phase transition: {str(e)}"
            logger.error(error_msg, exc_info=True)
            
            # Return state with error
            if isinstance(state, dict):
                state['error_message'] = error_msg
                return state
            
            # If it's a model, try to add the error
            try:
                state.error_message = error_msg
                if hasattr(state, 'model_dump'):
                    return state.model_dump()
                elif hasattr(state, 'dict'):
                    return state.dict()
                else:
                    return dict(state)
            except:
                # Last resort, create a new dict
                return {
                    "error_message": error_msg,
                    "game_status": "ended"
                }

    @classmethod
    def apply_move(cls,state: MafiaGameState, player_id: str, move: Union[MafiaAction, NarratorAction]) -> MafiaGameState:
        """Apply a move to the game state.
        
        This method validates and applies a player's move or narrator's action
        to the game state, updating all relevant state fields.

        Args:
            state (MafiaGameState): Current game state
            player_id (str): ID of the player making the move
            move (Union[MafiaAction, NarratorAction]): Move to apply

        Returns:
            MafiaGameState: Updated game state after applying the move

        Example:
            >>> move = MafiaAction(
            ...     player_id="Player_1",
            ...     action_type=ActionType.VOTE,
            ...     target_id="Player_2",
            ...     phase=GamePhase.DAY_VOTING,
            ...     round_number=1
            ... )
            >>> new_state = MafiaStateManager.apply_move(state, "Player_1", move)
        """
        # Create a copy of state
        new_state = copy.deepcopy(state)
        
        # Handle MafiaAction
        if isinstance(move, MafiaAction):
            # Add action to history
            new_state.action_history.append(move)
            
            # Handle different action types
            if move.action_type == ActionType.SPEAK:
                # Add message to public announcements
                new_state.public_announcements.append(str(move))
                
            elif move.action_type == ActionType.VOTE:
                # Record vote
                new_state.votes[player_id] = move.target_id
                # Add to public announcements
                new_state.public_announcements.append(f"{player_id} has voted for {move.target_id}.")
                
            elif move.action_type == ActionType.KILL and new_state.game_phase == GamePhase.NIGHT:
                # Record kill target
                new_state.killed_at_night = move.target_id
                
            elif move.action_type == ActionType.INVESTIGATE and new_state.game_phase == GamePhase.NIGHT:
                # Perform investigation
                target_id = move.target_id
                is_mafia = new_state.roles.get(target_id) == PlayerRole.MAFIA
                
                # Store investigation result
                if player_id not in new_state.player_states:
                    new_state.player_states[player_id] = PlayerState(role=PlayerRole.DETECTIVE)
                
                if not hasattr(new_state.player_states[player_id], 'investigation_results'):
                    new_state.player_states[player_id].investigation_results = {}
                    
                new_state.player_states[player_id].investigation_results[target_id] = is_mafia
                
            elif move.action_type == ActionType.SAVE and new_state.game_phase == GamePhase.NIGHT:
                # Record save target
                new_state.saved_at_night = move.target_id
                
        # Handle NarratorAction
        elif isinstance(move, NarratorAction):
            # Add action to history with special marking
            new_state.action_history.append(move)
            
            # Add announcement to public announcements
            if move.announcement:
                new_state.public_announcements.append(move.announcement)
            
            # Handle phase transition if requested
            if move.phase_transition:
                new_state = cls.handle_phase_transition(new_state)
        
        return new_state
    @classmethod
    def initialize(cls, player_names: List[str], **kwargs) -> MafiaGameState:
        """Initialize a new Mafia game with the given players.
        
        This method sets up a new game state with:
            - Random role assignment
            - Initial player states
            - Game phase setup
            - Role knowledge distribution

        Args:
            player_names (List[str]): List of player names/IDs
            **kwargs: Additional configuration options
                include_all_roles (bool): Force inclusion of all special roles

        Returns:
            MafiaGameState: Initial game state

        Raises:
            ValueError: If there aren't enough players (minimum 4)

        Example:
            >>> players = ["Player_1", "Player_2", "Player_3", "Narrator"]
            >>> state = MafiaStateManager.initialize(players)
            >>> print(state.game_phase)  # Should be SETUP
        """
        # Default role distribution
        num_players = len(player_names)
        
        # Ensure we have enough players (at least 3 plus narrator)
        if num_players < 4:
            raise ValueError("Mafia requires at least 4 players (including narrator)")
        
        # Remove the narrator from the regular player count
        num_regular_players = num_players - 1
        
        # Calculate role counts based on player count
        num_mafia = max(1, num_regular_players // 4)
        
        # Always include one detective and one doctor if we have enough players
        num_detectives = 1 if num_regular_players >= 6 else 0
        num_doctors = 1 if num_regular_players >= 7 else 0
        
        # Override for testing/debugging - include at least one of each special role
        if kwargs.get("include_all_roles", False):
            num_detectives = min(1, num_regular_players // 3)
            num_doctors = min(1, num_regular_players // 3)
            num_mafia = min(1, num_regular_players // 3)
        
        num_villagers = num_regular_players - num_mafia - num_detectives - num_doctors
        
        # Assign roles - fix narrator key to match the player ID exactly
        narrator_id = player_names[-1]  # Last player is narrator
        roles = {narrator_id: PlayerRole.NARRATOR}  # Use exact player ID
        regular_players = player_names[:-1]
        
        # Shuffle players for random role assignment
        shuffled_players = list(regular_players)
        import random
        random.shuffle(shuffled_players)
        
        # Keep track of assigned players
        assigned_players = []
        
        # Assign mafia roles
        for i in range(num_mafia):
            if i < len(shuffled_players):
                roles[shuffled_players[i]] = PlayerRole.MAFIA
                assigned_players.append(shuffled_players[i])
        
        # Assign detective roles
        for i in range(num_mafia, num_mafia + num_detectives):
            if i < len(shuffled_players):
                roles[shuffled_players[i]] = PlayerRole.DETECTIVE
                assigned_players.append(shuffled_players[i])
        
        # Assign doctor roles
        for i in range(num_mafia + num_detectives, num_mafia + num_detectives + num_doctors):
            if i < len(shuffled_players):
                roles[shuffled_players[i]] = PlayerRole.DOCTOR
                assigned_players.append(shuffled_players[i])
        
        # Assign villager roles to everyone else
        for player in shuffled_players:
            if player not in assigned_players:
                roles[player] = PlayerRole.VILLAGER
        
        # Initialize player states
        player_states = {}
        for player_id in player_names:
            role = roles.get(player_id, PlayerRole.VILLAGER)
            
            # Initialize known roles (players know their own role)
            known_roles = {player_id: role}
            
            # Mafia know who other mafia are
            if role == PlayerRole.MAFIA:
                for pid, r in roles.items():
                    if r == PlayerRole.MAFIA:
                        known_roles[pid] = r
            
            # Narrator knows all roles
            if role == PlayerRole.NARRATOR:
                known_roles = roles.copy()
            
            player_states[player_id] = PlayerState(
                player_id=player_id,
                role=role,
                known_roles=known_roles
            )
        
        # Count alive players by role
        alive_mafia_count = sum(1 for pid, role in roles.items() if role == PlayerRole.MAFIA)
        alive_village_count = sum(1 for pid, role in roles.items() 
                                if role != PlayerRole.MAFIA and role != PlayerRole.NARRATOR)
        
        # Create the initial state
        state = MafiaGameState(
            players=player_names,
            current_player_idx=0,  # Start with first player, not narrator
            roles=roles,
            player_states=player_states,
            game_phase=GamePhase.SETUP,
            game_status="ongoing",
            move_history=[],
            action_history=[],
            public_announcements=["The game of Mafia begins!"],
            alive_mafia_count=alive_mafia_count,
            alive_village_count=alive_village_count
        )
        
        return state

    @classmethod
    def _apply_player_action(cls, state: MafiaGameState, player_id: str, action: MafiaAction) -> MafiaGameState:
        """Apply a player's action to the game state.
        
        This internal method handles the details of applying a player's action,
        including validation and state updates.

        Args:
            state (MafiaGameState): Current game state
            player_id (str): ID of the player making the action
            action (MafiaAction): Action to apply

        Returns:
            MafiaGameState: Updated game state

        Raises:
            ValueError: If the player is dead or action is invalid

        Note:
            This is an internal method used by apply_move.
        """
        # Verify player is alive
        if player_id not in state.player_states or not state.player_states[player_id].is_alive:
            raise ValueError(f"Player {player_id} is not alive and cannot perform actions.")
        
        # Make sure round_number is set
        if action.round_number is None:
            action.round_number = state.round_number
            
        # Log the action
        state.log_action(action)
        
        # Process based on action type and game phase
        if action.action_type == ActionType.SPEAK:
            # For speak actions, just log them (already done above)
            if state.game_phase in [GamePhase.DAY_DISCUSSION, GamePhase.DAY_VOTING]:
                # Public speech during the day is visible to all
                message = f"{player_id} says: {action.message}"
                state.add_public_announcement(message)
            
        elif action.action_type == ActionType.VOTE:
            # For voting actions
            if state.game_phase == GamePhase.DAY_VOTING:
                # Ensure the target is alive
                if action.target_id in state.player_states and state.player_states[action.target_id].is_alive:
                    state.votes[player_id] = action.target_id
                    state.add_public_announcement(f"{player_id} has voted for {action.target_id}.")
                else:
                    state.add_public_announcement(f"{player_id} tried to vote for {action.target_id}, but they are not an eligible target.")
            
        elif action.action_type == ActionType.KILL:
            # For kill actions (mafia only)
            if state.game_phase == GamePhase.NIGHT and state.roles[player_id] == PlayerRole.MAFIA:
                # Ensure the target is alive
                if action.target_id in state.player_states and state.player_states[action.target_id].is_alive:
                    state.killed_at_night = action.target_id
                    # This is private information until processed by the narrator
            
        elif action.action_type == ActionType.SAVE:
            # For save actions (doctor only)
            if state.game_phase == GamePhase.NIGHT and state.roles[player_id] == PlayerRole.DOCTOR:
                # Ensure the target is alive
                if action.target_id in state.player_states and state.player_states[action.target_id].is_alive:
                    state.saved_at_night = action.target_id
                    # This is private information until processed by the narrator
            
        elif action.action_type == ActionType.INVESTIGATE:
            # For investigate actions (detective only)
            if state.game_phase == GamePhase.NIGHT and state.roles[player_id] == PlayerRole.DETECTIVE:
                # Ensure the target is alive
                if action.target_id in state.player_states and state.player_states[action.target_id].is_alive:
                    # Determine if target is mafia
                    is_mafia = state.roles[action.target_id] == PlayerRole.MAFIA
                    
                    # Store the result in the detective's investigations
                    if 'investigation_results' not in state.player_states[player_id]:
                        state.player_states[player_id].investigation_results = {}
                    
                    state.player_states[player_id].investigation_results[action.target_id] = is_mafia
                    # This is private information for the detective
        
        # Move to the next player
        state.current_player_idx = (state.current_player_idx + 1) % len(state.players)
        
        return state
    
    @classmethod
    def get_legal_moves(cls, state: MafiaGameState, player_id: str) -> List[Any]:
        """Get legal moves for a specific player.
        
        This method determines what moves are legal for a player based on:
            - Current game phase
            - Player's role
            - Player's alive/dead status
            - Previous actions in the current phase

        Args:
            state (MafiaGameState): Current game state
            player_id (str): ID of the player to get moves for

        Returns:
            List[Any]: List of legal moves (MafiaAction or NarratorAction)

        Example:
            >>> moves = MafiaStateManager.get_legal_moves(state, "Player_1")
            >>> for move in moves:
            ...     print(f"Can do: {move}")
        """
        legal_moves = []
        
        # Check if player is alive (except for narrator)
        if player_id not in state.player_states:
            return legal_moves
            
        if not state.player_states[player_id].is_alive and state.roles.get(player_id) != PlayerRole.NARRATOR:
            return legal_moves
        
        # Get player role
        player_role = state.roles.get(player_id)
        
        # Narrator moves
        if player_role == PlayerRole.NARRATOR:
            # Narrator can always make announcements
            legal_moves.append(
                NarratorAction(
                    announcement="[Example announcement]",
                    player_state_updates={},
                    phase_transition=False,
                    round_number=state.round_number
                )
            )
            
            # Narrator can transition phases if appropriate
            if state.game_phase == GamePhase.SETUP:
                legal_moves.append(
                    NarratorAction(
                        announcement="The game begins! Night falls upon the village.",
                        player_state_updates={},
                        phase_transition=True,
                        next_phase=GamePhase.NIGHT,
                        round_number=state.round_number
                    )
                )
            
            elif state.game_phase == GamePhase.NIGHT:
                # Check if all night actions are complete
                legal_moves.append(
                    NarratorAction(
                        announcement="The night ends, and a new day begins.",
                        player_state_updates={},
                        phase_transition=True,
                        next_phase=GamePhase.DAY_DISCUSSION,
                        round_number=state.round_number
                    )
                )
            
            elif state.game_phase == GamePhase.DAY_DISCUSSION:
                legal_moves.append(
                    NarratorAction(
                        announcement="The discussion period has ended. Time to vote!",
                        player_state_updates={},
                        phase_transition=True,
                        next_phase=GamePhase.DAY_VOTING,
                        round_number=state.round_number
                    )
                )
            
            elif state.game_phase == GamePhase.DAY_VOTING:
                legal_moves.append(
                    NarratorAction(
                        announcement="The votes have been tallied. Night falls again.",
                        player_state_updates={},
                        phase_transition=True,
                        next_phase=GamePhase.NIGHT,
                        round_number=state.round_number
                    )
                )
            
            return legal_moves
        
        # Player moves based on game phase
        if state.game_phase == GamePhase.DAY_DISCUSSION or state.game_phase == GamePhase.DAY_VOTING:
            # All players can speak during the day
            legal_moves.append(
                MafiaAction(
                    player_id=player_id,
                    action_type=ActionType.SPEAK,
                    message="[Example message]",
                    phase=state.game_phase,
                    round_number=state.round_number
                )
            )
        
        if state.game_phase == GamePhase.DAY_VOTING:
            # All players can vote during voting phase
            for target_id, target_state in state.player_states.items():
                # Can only vote for alive players other than yourself
                if target_state.is_alive and target_id != player_id:
                    legal_moves.append(
                        MafiaAction(
                            player_id=player_id,
                            action_type=ActionType.VOTE,
                            target_id=target_id,
                            phase=state.game_phase,
                            round_number=state.round_number
                        )
                    )
        
        if state.game_phase == GamePhase.NIGHT:
            # Night actions based on roles
            if player_role == PlayerRole.MAFIA:
                # Mafia can kill during the night
                for target_id, target_state in state.player_states.items():
                    # Can only kill alive players who are not mafia
                    if target_state.is_alive and state.roles.get(target_id) != PlayerRole.MAFIA:
                        legal_moves.append(
                            MafiaAction(
                                player_id=player_id,
                                action_type=ActionType.KILL,
                                target_id=target_id,
                                phase=state.game_phase,
                                round_number=state.round_number
                            )
                        )
            
            elif player_role == PlayerRole.DOCTOR:
                # Doctor can save during the night
                for target_id, target_state in state.player_states.items():
                    # Can save any alive player, including themselves
                    if target_state.is_alive:
                        legal_moves.append(
                            MafiaAction(
                                player_id=player_id,
                                action_type=ActionType.SAVE,
                                target_id=target_id,
                                phase=state.game_phase,
                                round_number=state.round_number
                            )
                        )
            
            elif player_role == PlayerRole.DETECTIVE:
                # Detective can investigate during the night
                for target_id, target_state in state.player_states.items():
                    # Can investigate any alive player other than themselves
                    if target_state.is_alive and target_id != player_id:
                        legal_moves.append(
                            MafiaAction(
                                player_id=player_id,
                                action_type=ActionType.INVESTIGATE,
                                target_id=target_id,
                                phase=state.game_phase,
                                round_number=state.round_number
                            )
                        )
        
        return legal_moves
    
    @classmethod
    def check_game_status(cls, state: MafiaGameState) -> MafiaGameState:
        """Check if the game has ended and determine the winner.
        
        This method checks win conditions:
            - Village wins if all mafia are dead
            - Mafia wins if they equal/outnumber villagers

        Args:
            state (MafiaGameState): Current game state

        Returns:
            MafiaGameState: Updated state with game status and winner if game is over

        Example:
            >>> new_state = MafiaStateManager.check_game_status(state)
            >>> if new_state.winner:
            ...     print(f"Game over! {new_state.winner} wins!")
        """
        new_state = copy.deepcopy(state)
        
        # Game ends if all mafia are dead (village wins)
        if new_state.alive_mafia_count == 0:
            new_state.game_status = "ended"
            new_state.winner = "village"
            new_state.public_announcements.append("All mafia members have been eliminated! The village wins!")
            logger.info("Game over: Village wins (all mafia eliminated)")
        
        # Game ends if mafia equals or outnumbers villagers (mafia wins)
        elif new_state.alive_mafia_count >= new_state.alive_village_count:
            new_state.game_status = "ended"
            new_state.winner = "mafia"
            new_state.public_announcements.append("The mafia has won! They now equal or outnumber the villagers.")
            logger.info("Game over: Mafia wins (villagers outnumbered)")
        
        return new_state
    
    @classmethod
    def filter_state_for_player(cls, state: MafiaGameState, player_id: str) -> Dict[str, Any]:
        """Filter the state to include only information visible to a specific player.
        
        This method implements information hiding, ensuring players only see
        information they should have access to based on their role and the
        game phase.

        Args:
            state (MafiaGameState): Full game state
            player_id (str): ID of the player to filter for

        Returns:
            Dict[str, Any]: Filtered state containing only visible information

        Example:
            >>> # Get state visible to Player_1
            >>> visible_state = MafiaStateManager.filter_state_for_player(
            ...     state, "Player_1"
            ... )
        """
        # Create a filtered copy of the state
        filtered_state = {}
        
        # Basic game information visible to all
        filtered_state["players"] = state.players
        filtered_state["game_phase"] = state.game_phase
        filtered_state["day_number"] = state.day_number
        filtered_state["round_number"] = state.round_number
        filtered_state["public_announcements"] = state.public_announcements
        
        # Information about who is alive
        filtered_state["alive_players"] = [pid for pid, p_state in state.player_states.items() if p_state.is_alive]
        filtered_state["dead_players"] = [pid for pid, p_state in state.player_states.items() if not p_state.is_alive]
        
        # Player's own information
        if player_id in state.player_states:
            filtered_state["my_role"] = state.roles.get(player_id)
            filtered_state["known_roles"] = state.player_states[player_id].known_roles
            
            # Add investigation results for detectives
            if state.roles.get(player_id) == PlayerRole.DETECTIVE:
                filtered_state["investigation_results"] = state.player_states[player_id].investigation_results
        
        # During voting, everyone can see the votes
        if state.game_phase == GamePhase.DAY_VOTING:
            filtered_state["votes"] = state.votes
        
        # Narrator can see everything
        if state.roles.get(player_id) == PlayerRole.NARRATOR:
            filtered_state["full_state"] = {
                "roles": {pid: role.value for pid, role in state.roles.items()},
                "player_states": {pid: {
                    "is_alive": p_state.is_alive,
                    "role": state.roles.get(pid).value,
                    "known_roles": {k: v.value for k, v in p_state.known_roles.items()},
                    "investigation_results": p_state.investigation_results
                } for pid, p_state in state.player_states.items()},
                "killed_at_night": state.killed_at_night,
                "saved_at_night": state.saved_at_night
            }
        
        return filtered_state