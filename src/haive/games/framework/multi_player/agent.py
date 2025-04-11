"""Multi-player game agent implementation.

This module provides the base agent class for multi-player games, supporting:
    - Variable number of players
    - Role-based player configurations
    - Phase-based game flow
    - Information hiding between players
    - Concurrent or sequential player actions

Example:
    >>> from src.haive.agents.agent_games.framework.multi_player.agent import MultiPlayerGameAgent
    >>> 
    >>> class ChessAgent(MultiPlayerGameAgent[ChessState]):
    ...     def __init__(self, config: ChessConfig):
    ...         super().__init__(config)
    ...         self.state_manager = ChessStateManager
"""

from typing import Generic, Type, TypeVar, Any, Dict, Optional
from src.haive.games.framework.multi_player.config import MultiPlayerGameConfig
from src.haive.games.framework.multi_player.state import MultiPlayerGameState
from src.haive.core.engine.agent.agent import Agent
from langgraph.graph import START, END
from langgraph.graph import StateGraph  
from src.haive.core.graph.GraphBuilder import DynamicGraph
from pydantic import BaseModel


T = TypeVar('T', bound=BaseModel)

class MultiPlayerGameAgent(Agent[MultiPlayerGameConfig], Generic[T]):
    """Base game agent for multi-player games.
    
    This class provides the foundation for implementing multi-player game agents
    with support for role-based configurations, phase-based gameplay, and
    information hiding between players.
    
    Type Parameters:
        T: The game state type, must be a Pydantic BaseModel.
    
    Attributes:
        config (MultiPlayerGameConfig): Agent configuration.
        engines (Dict[str, Dict[str, Any]]): LLM engines by role and function.
        state_manager (Type[MultiPlayerGameStateManager]): State manager class.
        graph (StateGraph): Game workflow graph.
    
    Example:
        >>> class MafiaAgent(MultiPlayerGameAgent[MafiaState]):
        ...     def __init__(self, config: MafiaConfig):
        ...         super().__init__(config)
        ...         self.state_manager = MafiaStateManager
        ...
        ...     def prepare_move_context(self, state, player_id):
        ...         return {
        ...             "game_state": state.board_string,
        ...             "player_role": self.get_player_role(state, player_id)
        ...         }
    """
    
    def __init__(self, config: MultiPlayerGameConfig):
        """Initialize the multi-player game agent.
        
        Args:
            config (MultiPlayerGameConfig): Agent configuration including
                state schema, LLM configurations, and game settings.
        """
        super().__init__(config)
        # Compose all LLMs from src.configs based on roles
        
    def _init_engines(self):
        """Initialize the engines from the configuration.
        
        This method sets up LLM engines for each role and function,
        handling both AugLLM configurations and direct runnables.
        """
        self.engines = {}
        
        # Store engines directly by role and function
        # This matches how they're accessed in get_engine_for_player
        if hasattr(self.config, 'engines'):
            for role, role_engines in self.config.engines.items():
                # Store the engine configs by role directly (not prefixed)
                if role not in self.engines:
                    self.engines[role] = {}
                    
                for engine_name, engine_config in role_engines.items():
                    # Convert AugLLMConfig to runnable if possible
                    try:
                        if hasattr(engine_config, 'create_runnable'):
                            self.engines[role][engine_name] = engine_config.create_runnable()
                        else:
                            # If it already looks like a runnable, store as is
                            self.engines[role][engine_name] = engine_config
                    except Exception as e:
                        import logging
                        logging.error(f"Error creating runnable for {role}.{engine_name}: {e}")
                        self.engines[role][engine_name] = engine_config  # Store config for debugging
                    
        # Log the available engines for debugging
        import logging
        logging.info(f"Initialized engines for {list(self.engines.keys())} roles")
        for role, engines in self.engines.items():
            logging.debug(f"Role {role} has engines: {list(engines.keys())}")
    def setup_workflow(self):
        """Setup the standard game workflow with phases.
        
        This method creates a workflow graph with the following structure:
            1. Game initialization
            2. Setup phase
            3. Player turns
            4. Phase transitions
            5. Game end
        
        The workflow supports conditional transitions based on game state
        and can be overridden for custom game flows.
        """
        # Use DynamicGraph to build the workflow
        graph_builder = DynamicGraph(
            components=[],  # Not using components directly here
            state_schema=self.config.state_schema
        )
        
        # Add the phase nodes
        graph_builder.add_node("initialize_game", self.initialize_game)
        graph_builder.add_node("setup_phase", self.handle_setup_phase)
        graph_builder.add_node("player_turn", self.handle_player_turn)
        graph_builder.add_node("phase_transition", self.handle_phase_transition)
        graph_builder.add_node("end_game", self.handle_end_game)
        
        # Standard flow:
        # Start -> Initialize -> Setup -> Player Turns -> Phase Transitions -> End
        graph_builder.add_edge(START, "initialize_game")
        graph_builder.add_edge("initialize_game", "setup_phase")
        
        # Setup phase can go to player turns or end directly
        graph_builder.add_conditional_edges(
            "setup_phase",
            self.should_continue_to_main_phase,
            {True: "player_turn", False: "end_game"}
        )
        
        # Player turn can continue with next player, go to phase transition, or end
        graph_builder.add_conditional_edges(
            "player_turn",
            self.determine_next_step_after_player_turn,
            {
                "next_player": "player_turn", 
                "phase_transition": "phase_transition",
                "end_game": "end_game"
            }
        )
        
        # Phase transition can go back to player turns or end
        graph_builder.add_conditional_edges(
            "phase_transition",
            self.should_continue_after_phase_transition,
            {True: "player_turn", False: "end_game"}
        )
        
        # End game goes to END
        graph_builder.add_edge("end_game", END)
        
        # Build the graph
        self.graph = graph_builder.build()

    def get_player_role(self, state: MultiPlayerGameState, player_id: str) -> str:
        """Get the role of a player, handling case sensitivity.
        
        This method attempts to find the player's role while handling different
        case variations of player IDs and special roles like 'narrator'.
        
        Args:
            state (MultiPlayerGameState): Current game state.
            player_id (str): ID of the player to look up.
        
        Returns:
            str: Role of the player, defaulting to "VILLAGER" if not found.
        
        Example:
            >>> state = MafiaGameState(roles={"player1": "MAFIA", "narrator": "NARRATOR"})
            >>> agent.get_player_role(state, "Player1")  # Case-insensitive
            'MAFIA'
            >>> agent.get_player_role(state, "narrator")
            'NARRATOR'
        """
        # Fix the capitalization issue with 'narrator' vs 'Narrator'
        if player_id.lower() == 'narrator':
            return "NARRATOR"
        
        # Check both capitalization variants
        if player_id in state.roles:
            return state.roles[player_id]
        
        # Try lowercase version (in case roles are stored with lowercase keys)
        lowercase_player_id = player_id.lower()
        if lowercase_player_id in state.roles:
            return state.roles[lowercase_player_id]
        
        # Default to VILLAGER if role not found
        return "VILLAGER"

    def determine_next_step_after_player_turn(self, state: MultiPlayerGameState) -> str:
        """Determine what to do after a player's turn.
        
        This method handles complex game flow logic, including:
        - Checking game end conditions
        - Managing phase transitions
        - Handling night/day cycle transitions
        - Processing voting and action completions
        
        Args:
            state (MultiPlayerGameState): Current game state.
        
        Returns:
            str: Next step to take, one of:
                - "end_game": Game is over
                - "phase_transition": Move to next phase
                - "next_player": Continue with next player
        
        Example:
            >>> state = MafiaGameState(game_phase="NIGHT", votes={"p1": "p2"})
            >>> # If all night actions complete
            >>> agent.determine_next_step_after_player_turn(state)
            'phase_transition'  # Move to day phase
            >>> # If more players need to act
            >>> agent.determine_next_step_after_player_turn(state)
            'next_player'  # Continue with next player
        """
        # If game is over, end the game
        if state.game_status != "ongoing" or state.game_phase == "GAME_OVER":
            return "end_game"
        
        # Get the current player
        current_player = state.current_player
        
        # If night phase and all night actions are complete, transition to day
        if state.game_phase == "NIGHT":
            all_night_actions_complete = True
            
            # Check if all expected night actors have acted
            for player_id, role in state.roles.items():
                if player_id.lower() == 'narrator':
                    continue  # Skip narrator when checking night actions
                    
                if (state.player_states[player_id].is_alive and 
                    role in ["MAFIA", "DOCTOR", "DETECTIVE"]):
                    
                    has_acted = False
                    for action in reversed(state.action_history):
                        if (hasattr(action, 'player_id') and 
                            action.player_id == player_id and 
                            hasattr(action, 'phase') and 
                            action.phase == "NIGHT" and 
                            state.round_number == getattr(action, 'round_number', -1)):
                            
                            has_acted = True
                            break
                    
                    if not has_acted:
                        all_night_actions_complete = False
                        break
            
            if all_night_actions_complete:
                return "phase_transition"
        
        # If day voting phase and all votes are in, transition to night
        if state.game_phase == "DAY_VOTING":
            alive_players = [pid for pid, p_state in state.player_states.items() if p_state.is_alive]
            if len(state.votes) >= len(alive_players):
                return "phase_transition"
        
        # Check if current player is narrator (handle case sensitivity)
        is_narrator = False
        current_player_role = None
        
        # Try to get role from state.roles using current_player
        if current_player in state.roles:
            current_player_role = state.roles[current_player]
        # Try with lowercase key
        elif current_player.lower() in state.roles:
            current_player_role = state.roles[current_player.lower()]
        
        is_narrator = (current_player_role == "NARRATOR" or 
                    current_player.lower() == 'narrator')
        
        # If current player is narrator, check for phase transition
        if is_narrator:
            # After a full round of players, let narrator transition the phase
            if state.game_phase == "DAY_DISCUSSION":
                # Check if a full discussion round has occurred
                discussion_count = 0
                for action in reversed(state.action_history):
                    if (hasattr(action, 'phase') and 
                        action.phase == "DAY_DISCUSSION" and 
                        state.round_number == getattr(action, 'round_number', -1)):
                        discussion_count += 1
                
                alive_player_count = len([p for p in state.player_states.values() if p.is_alive])
                if discussion_count >= alive_player_count:
                    return "phase_transition"
        
        # Otherwise, continue with next player
        return "next_player"

    def handle_narrator_turn(self, state: MultiPlayerGameState) -> Dict[str, Any]:
        """Handle the narrator's turn in the game.
        
        This method manages the narrator's actions, including:
        - Getting the appropriate narrator engine
        - Preparing narrator context
        - Processing narrator decisions
        - Applying narrator actions to the game state
        
        Args:
            state (MultiPlayerGameState): Current game state.
        
        Returns:
            Dict[str, Any]: Updated game state after narrator's action.
        
        Example:
            >>> state = MafiaGameState(phase="NIGHT")
            >>> # Narrator processes night actions
            >>> new_state = agent.handle_narrator_turn(state)
            >>> new_state["phase"]  # Narrator may have changed phase
            'DAY'
        
        Notes:
            - Handles case sensitivity issues with narrator role
            - Provides error handling for missing narrator engine
            - Converts state between dict and model forms as needed
        """
        # Get the narrator engine - fix case sensitivity issues
        narrator_key = "narrator"
        narrator_engine = None
        
        # Try different capitalization options for narrator engines
        for key in self.engines:
            if key.lower() == "narrator":
                narrator_engine = self.engines[key]
                break
        
        if not narrator_engine:
            error_msg = "No narrator engine found"
            state_dict = state.dict() if hasattr(state, "dict") else dict(state)
            state_dict["error_message"] = error_msg
            return state_dict
        
        try:
            # Prepare narrator context
            narrator_context = self.prepare_narrator_context(state)
            
            # Get decision from the engine
            response = narrator_engine.invoke(narrator_context)
            
            # Extract the action
            action = self.extract_move(response, "narrator")
            
            # Apply action to state
            new_state = self.state_manager.apply_move(state, "Narrator", action)
            
            # Convert to dict for the graph
            if hasattr(new_state, "model_dump"):
                return new_state.model_dump()
            return new_state.dict()
            
        except Exception as e:
            error_msg = f"Error in narrator's turn: {str(e)}"
            state_dict = state.dict() if hasattr(state, "dict") else dict(state)
            state_dict["error_message"] = error_msg
            return state_dict

    def prepare_narrator_context(self, state: MultiPlayerGameState) -> Dict[str, Any]:
        """Prepare context for narrator's decision making.
        
        This method should be implemented by game-specific agents to provide
        the narrator with appropriate context for the current game state.
        
        Args:
            state (MultiPlayerGameState): Current game state.
        
        Returns:
            Dict[str, Any]: Context for narrator's decision making.
        
        Raises:
            NotImplementedError: Must be implemented by subclass.
        
        Example:
            >>> def prepare_narrator_context(self, state):
            ...     return {
            ...         "phase": state.game_phase,
            ...         "alive_players": [p for p in state.players if p.is_alive],
            ...         "recent_actions": state.action_history[-5:]
            ...     }
        """
        raise NotImplementedError("Must be implemented by subclass")

    def initialize_game(self, state:BaseModel) -> Dict[str, Any]:
        """Initialize the game state.
        
        Args:
            state (BaseModel): Initial state data or empty state.
        
        Returns:
            Dict[str, Any]: Initialized game state.
        
        Raises:
            ValueError: If state manager is not set.
        """
        if not self.state_manager:
            raise ValueError("State manager must be set by subclass")
        if isinstance(state, dict):
            player_list = state.get("players", [f"player_{i}" for i in range(self.config.initial_player_count)])
        else:
            if state.players is None:
                player_list = [f"player_{i}" for i in range(self.config.initial_player_count)]
            else:
                player_list = state.players
        # Create initial game state with player list
        game_state = self.state_manager.initialize(player_list)
        
        # Convert to dict for the graph
        if hasattr(game_state, "model_dump"):
            return game_state.model_dump()
        return game_state.dict()
    
    def handle_setup_phase(self, state: T) -> Dict[str, Any]:
        """Handle the setup phase of the game.
        
        Args:
            state (T): Current game state.
        
        Returns:
            Dict[str, Any]: Updated game state after setup.
        """
        # Implement game-specific setup logic
        # Default implementation just advances to main phase
        state = self.state_manager.advance_phase(state)
        
        # Convert to dict for the graph
        if hasattr(state, "model_dump"):
            return state.model_dump()
        return state.dict()
    
    def handle_player_turn(self, state: T) -> Dict[str, Any]:
        """Handle a player's turn.
        
        This method:
        1. Gets the current player and their role
        2. Retrieves the appropriate move engine
        3. Filters state information for the player
        4. Gets and applies the player's move
        5. Checks game status after the move
        
        Args:
            state (T): Current game state.
        
        Returns:
            Dict[str, Any]: Updated game state after the player's move.
        """
        # Get current player
        player_id = state.current_player
        
        # Get player's role (default to player_id if no specific role)
        player_role = self.get_player_role(state, player_id)
        
        # Get the move engine for this role
        move_engine = self.get_engine_for_player(player_role, "player")
        if not move_engine:
            return {"error_message": f"No move engine found for player {player_id} with role {player_role}"}
        
        try:
            # Filter state for this player (information hiding)
            player_view = self.state_manager.filter_state_for_player(state, player_id)
            
            # Get decision from the engine
            move_context = self.prepare_move_context(state, player_id)
            response = move_engine.invoke(move_context)
            
            # Extract the move
            move = self.extract_move(response, player_role)
            
            # Apply move to state
            new_state = self.state_manager.apply_move(state, player_id, move)
            
            # Check game status after move
            new_state = self.state_manager.check_game_status(new_state)
            
            # Convert to dict for the graph
            if hasattr(new_state, "model_dump"):
                return new_state.model_dump()
            return new_state.dict()
            
        except Exception as e:
            error_msg = f"Error in {player_id}'s turn: {str(e)}"
            state_dict = state.dict() if hasattr(state, "dict") else dict(state)
            state_dict["error_message"] = error_msg
            return state_dict
    
    def handle_phase_transition(self, state: T) -> Dict[str, Any]:
        """Handle transition between game phases.
        
        Args:
            state (T): Current game state.
        
        Returns:
            Dict[str, Any]: Updated game state in the new phase.
        """
        try:
            # Advance to the next phase
            new_state = self.state_manager.advance_phase(state)
            
            # Check game status after phase transition
            new_state = self.state_manager.check_game_status(new_state)
            
            # Convert to dict for the graph
            if hasattr(new_state, "model_dump"):
                return new_state.model_dump()
            return new_state.dict()
            
        except Exception as e:
            error_msg = f"Error in phase transition: {str(e)}"
            state_dict = state.dict() if hasattr(state, "dict") else dict(state)
            state_dict["error_message"] = error_msg
            return state_dict
    
    def handle_end_game(self, state: T) -> Dict[str, Any]:
        """Handle the end of the game.
        
        Args:
            state (T): Current game state.
        
        Returns:
            Dict[str, Any]: Final game state.
        """
        # Set game status to ended if not already
        state_dict = state.dict() if hasattr(state, "dict") else dict(state)
        if state_dict.get("game_status") == "ongoing":
            state_dict["game_status"] = "ended"
        
        # Store the final state
        return state_dict
    
    # Router methods
    def should_continue_to_main_phase(self, state: T) -> bool:
        """Determine if we should continue to the main phase.
        
        Args:
            state (T): Current game state.
        
        Returns:
            bool: True if game should continue to main phase.
        """
        # Default: continue if game is ongoing
        return state.game_status == "ongoing"
    
    
    
    def should_continue_after_phase_transition(self, state: T) -> bool:
        """Determine if we should continue after a phase transition.
        
        Args:
            state (T): Current game state.
        
        Returns:
            bool: True if game should continue.
        """
        # Continue if game is ongoing
        return state.game_status == "ongoing"
    
    def should_transition_phase(self, state: T) -> bool:
        """Determine if we should transition to a new phase.
        
        Args:
            state (T): Current game state.
        
        Returns:
            bool: True if phase transition should occur.
        """
        # Default implementation: transition after all players have had a turn
        # Override this for game-specific logic
        return state.current_player_idx == 0 and state.round_number > 0
    
    # Helper methods
    def get_player_role(self, state: T, player_id: str) -> str:
        """Get the role of a player.
        
        Args:
            state (T): Current game state.
            player_id (str): ID of the player.
        
        Returns:
            str: Role of the player.
        """
        # Default implementation: all players have the same role
        # Override this for role-based games
        return "default"
    
    def get_engine_for_player(self, role: str, function: str) -> Optional[Any]:
        """Get the appropriate engine for a player based on role and function.
        
        Args:
            role (str): Player's role.
            function (str): Function to get engine for.
        
        Returns:
            Optional[Any]: Engine for the role and function, or None if not found.
        """
        role_engines = self.engines.get(role)
        if not role_engines:
            # Try default role
            role_engines = self.engines.get("default")
            if not role_engines:
                return None
        
        return role_engines.get(function)
    
    def prepare_move_context(self, state: T, player_id: str) -> Dict[str, Any]:
        """Prepare context for move generation.
        
        Args:
            state (T): Current game state.
            player_id (str): ID of the player.
        
        Returns:
            Dict[str, Any]: Context for move generation.
        
        Raises:
            NotImplementedError: Must be implemented by subclass.
        """
        # This should be implemented by the subclass
        raise NotImplementedError("Must be implemented by subclass")
    
    def extract_move(self, response: Any, role: str) -> Any:
        """Extract move from engine response.
        
        Args:
            response (Any): Response from the engine.
            role (str): Role of the player.
        
        Returns:
            Any: Extracted move.
        
        Raises:
            NotImplementedError: Must be implemented by subclass.
        """
        # This should be implemented by the subclass
        raise NotImplementedError("Must be implemented by subclass")
    
    def visualize_state(self, state: Dict[str, Any]) -> None:
        """Visualize the current game state.
        
        Args:
            state (Dict[str, Any]): Current game state.
        
        Raises:
            NotImplementedError: Must be implemented by subclass.
        """
        # This should be implemented by the subclass
        raise NotImplementedError("Must be implemented by subclass")
