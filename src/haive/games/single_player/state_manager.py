
from src.haive.games.framework.base.state_manager import GameStateManager
from src.haive.games.base.state

class SinglePlayerStateManager(GameStateManager[WordConnectionsState]):
    """Base state manager for single-player games.
    
    This class extends the base GameStateManager with single-player specific
    functionality such as hint generation, difficulty scaling, and interactive
    input handling.
    
    Methods:
        initialize: Initialize a new game state
        apply_move: Apply a move to the game state
        generate_hint: Generate a hint for the current game state
        check_game_status: Check and update the game status
        interactive_input: Process interactive input from the player
    """
    
    @classmethod
    def initialize(cls, difficulty: GameDifficulty = GameDifficulty.MEDIUM, 
                  player_type: PlayerType = PlayerType.LLM, **kwargs) -> T:
        """Initialize a new game state.
        
        Args:
            difficulty: Difficulty level of the game
            player_type: Type of player
            **kwargs: Additional game-specific initialization parameters
            
        Returns:
            A new game state
        """
        raise NotImplementedError("Must be implemented by subclass")
    
    @classmethod
    def apply_move(cls, state: T, move: Any) -> T:
        """Apply a move to the game state.
        
        Args:
            state: Current game state
            move: Move to apply
            
        Returns:
            Updated game state
        """
        raise NotImplementedError("Must be implemented by subclass")
    
    @classmethod
    def generate_hint(cls, state: T) -> Tuple[T, str]:
        """Generate a hint for the current game state.
        
        Args:
            state: Current game state
            
        Returns:
            Tuple of (updated state, hint text)
        """
        # Create a copy of the state
        new_state = copy.deepcopy(state)
        
        # Increment hint count
        new_state.hint_count += 1
        
        # Default hint - should be overridden by subclasses
        hint = "This is a generic hint. Override this method in your game-specific state manager."
        
        return new_state, hint
    
    @classmethod
    def check_game_status(cls, state: T) -> T:
        """Check and update the game status.
        
        Args:
            state: Current game state
            
        Returns:
            Updated game state with status checked
        """
        raise NotImplementedError("Must be implemented by subclass")
    
    @classmethod
    def get_legal_moves(cls, state: T) -> List[Any]:
        """Get all legal moves for the current state.
        
        Args:
            state: Current game state
            
        Returns:
            List of legal moves
        """
        raise NotImplementedError("Must be implemented by subclass")
    
    @classmethod
    def interactive_input(cls, state: T, user_input: str) -> T:
        """Process interactive input from the player.
        
        This method handles general commands like 'hint', 'quit', etc.
        Game-specific commands should be handled by overriding this method.
        
        Args:
            state: Current game state
            user_input: User input string
            
        Returns:
            Updated game state
        """
        # Create a copy of the state
        new_state = copy.deepcopy(state)
        
        # Convert input to lowercase for easier matching
        input_lower = user_input.strip().lower()
        
        # Handle common commands
        if input_lower == "hint":
            new_state, hint_text = cls.generate_hint(new_state)
            new_state.error_message = f"HINT: {hint_text}"
        elif input_lower == "quit":
            new_state.game_status = "defeat"
            new_state.error_message = "Game quit by player"
        elif input_lower == "status":
            moves = new_state.move_count
            hints = new_state.hint_count
            new_state.error_message = f"Game Status: Moves: {moves}, Hints: {hints}"
        else:
            # Unknown command, let subclass handle it
            pass
            
        return new_state

