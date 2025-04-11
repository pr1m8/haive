"""
State manager for the Mastermind game.

This module defines the state manager for the Mastermind game,
which manages the state of the game and provides methods for initializing,
updating, and analyzing the game state.
"""
from typing import List, Dict, Any, Optional, Set, Tuple
import random
from src.haive.games.mastermind.models import MastermindGuess, MastermindFeedback, MastermindAnalysis, ColorCode
from src.haive.games.framework.base.state_manager import GameStateManager
from src.haive.games.mastermind.state import MastermindState
class MastermindStateManager(GameStateManager[MastermindState]):
    """Manager for Mastermind game state.

    This class provides methods for initializing, updating, and analyzing the game state.
    """
    
    VALID_COLORS = ["red", "blue", "green", "yellow", "purple", "orange"]
    
    @classmethod
    def initialize(cls, **kwargs) -> MastermindState:
        """
        Initialize a new Mastermind game.

        Args:
            **kwargs: Keyword arguments for game initialization.
                codemaker: Player who creates the code (player1 or player2). Default is player1.
                colors: List of valid colors. Default is standard 6 colors.
                code_length: Length of the secret code. Default is 4.
                max_turns: Maximum number of turns. Default is 10.
                secret_code: Optional predetermined secret code (List[str] or ColorCode).

        Returns:
            MastermindState: A new Mastermind game state.
        """
        codemaker = kwargs.get('codemaker', "player1")
        codebreaker = "player2" if codemaker == "player1" else "player1"
        colors = kwargs.get('colors', cls.VALID_COLORS)
        code_length = kwargs.get('code_length', 4)
        max_turns = kwargs.get('max_turns', 10)

        # Unwrap or generate secret code
        secret_code = kwargs.get('secret_code')
        if isinstance(secret_code, ColorCode):
            secret_code = secret_code.code
        elif isinstance(secret_code, dict) and "code" in secret_code:
            secret_code = secret_code["code"]
        elif not secret_code:
            secret_code = random.choices(colors, k=code_length)

        return MastermindState(
            secret_code=secret_code,
            guesses=[],
            feedback=[],
            turn=codebreaker,  # Codebreaker starts
            codemaker=codemaker,
            max_turns=max_turns,
            game_status="ongoing"
        )

    @classmethod
    def get_legal_moves(cls, state: MastermindState) -> List[MastermindGuess]:
        """
        Get all legal moves for the current state.
        
        For Mastermind, this is impractical to enumerate all possible color combinations,
        so this method returns an empty list. The agent will generate guesses based on analysis.
        
        Args:
            state: The current game state.
            
        Returns:
            List[MastermindGuess]: An empty list (agent should generate its own guesses).
        """
        return []
    
    @classmethod
    def apply_move(cls, state: MastermindState, move: MastermindGuess) -> MastermindState:
        """
        Apply a guess to the current state and return the new state.
        
        Args:
            state: The current game state.
            move: The guess to apply.
            
        Returns:
            MastermindState: A new game state after applying the guess.
            
        Raises:
            ValueError: If the move is invalid.
        """
        # Validate player's turn
        if move.player != state.turn:
            raise ValueError(f"Not {move.player}'s turn")
        
        # Validate turn limit
        if len(state.guesses) >= state.max_turns:
            raise ValueError("Maximum number of turns reached")
        
        # Create a new state
        new_state = state.model_copy()
        
        # Add the guess
        new_state.guesses.append(move)
        
        # Calculate feedback
        feedback = cls._calculate_feedback(new_state.secret_code, move.colors)
        new_state.feedback.append(feedback)
        
        # Check if the game is over
        if feedback.is_winning():
            # Codebreaker wins
            new_state.game_status = f"{move.player}_win"
            new_state.winner = move.player
        elif len(new_state.guesses) >= new_state.max_turns:
            # Codemaker wins if max turns reached without correct guess
            new_state.game_status = f"{new_state.codemaker}_win"
            new_state.winner = new_state.codemaker
        
        return new_state
    
    @classmethod
    def _calculate_feedback(cls, secret_code: List[str], guess: List[str]) -> MastermindFeedback:
        """
        Calculate feedback for a guess compared to the secret code.
        
        Args:
            secret_code: The secret code to guess.
            guess: The player's guess.
            
        Returns:
            MastermindFeedback: Feedback with correct position and color counts.
        """
        # Count exact matches (correct position and color)
        correct_position = sum(1 for s, g in zip(secret_code, guess) if s == g)
        
        # Count color matches (regardless of position)
        # We need to handle duplicates carefully
        secret_counts = {}
        guess_counts = {}
        
        for color in secret_code:
            secret_counts[color] = secret_counts.get(color, 0) + 1
        
        for color in guess:
            guess_counts[color] = guess_counts.get(color, 0) + 1
        
        # Count colors that appear in both lists (take minimum count for each color)
        correct_color_total = sum(min(secret_counts.get(color, 0), guess_counts.get(color, 0)) for color in set(secret_code + guess))
        
        # Subtract exact matches to get only color matches
        correct_color = correct_color_total - correct_position
        
        return MastermindFeedback(
            correct_position=correct_position,
            correct_color=correct_color
        )
    
    @classmethod
    def check_game_status(cls, state: MastermindState) -> MastermindState:
        """
        Check and update the game status.
        
        For Mastermind, this is handled in apply_move, so this method just returns the state.
        
        Args:
            state: The current game state.
            
        Returns:
            MastermindState: The game state (unchanged).
        """
        return state
    
    @classmethod
    def get_winner(cls, state: MastermindState) -> Optional[str]:
        """
        Get the winner of the game, if any.
        
        Args:
            state: The current game state.
            
        Returns:
            Optional[str]: The winner, or None if the game is ongoing.
        """
        return state.winner
    
    @classmethod
    def add_analysis(cls, state: MastermindState, player: str, analysis: MastermindAnalysis) -> MastermindState:
        """
        Add an analysis to the state.
        
        Args:
            state: The current game state.
            player: The player who performed the analysis.
            analysis: The analysis to add.
            
        Returns:
            MastermindState: Updated state with the analysis added.
        """
        new_state = state.model_copy()
        
        if player == "player1":
            new_state.player1_analysis.append(analysis)
        else:
            new_state.player2_analysis.append(analysis)
        
        return new_state
    
    @classmethod
    def get_possible_codes(cls, state: MastermindState) -> Set[Tuple[str, ...]]:
        """
        Get all possible secret codes that are consistent with all guesses and feedback so far.
        
        This is computationally expensive for a full game, so it's limited to use for analysis.
        
        Args:
            state: The current game state.
            
        Returns:
            Set[Tuple[str, ...]]: Set of possible codes as tuples.
        """
        # Start with all possible codes
        colors = cls.VALID_COLORS
        code_length = 4  # Standard Mastermind code length
        
        # Generate all possible codes (expensive, but acceptable for analysis)
        import itertools
        all_codes = set(itertools.product(colors, repeat=code_length))
        
        # Filter based on previous guesses and feedback
        for guess, feedback in zip(state.guesses, state.feedback):
            guess_tuple = tuple(guess.colors)
            all_codes = {code for code in all_codes if 
                         cls._is_consistent_with_feedback(code, guess_tuple, feedback)}
        
        return all_codes
    
    @classmethod
    def _is_consistent_with_feedback(cls, code: Tuple[str, ...], guess: Tuple[str, ...], 
                                    feedback: MastermindFeedback) -> bool:
        """
        Check if a potential code is consistent with a guess and its feedback.
        
        Args:
            code: Potential secret code.
            guess: A previous guess.
            feedback: Feedback for the guess.
            
        Returns:
            bool: True if the code is consistent with the guess and feedback.
        """
        # Calculate what the feedback would be if this code were the secret
        calculated_feedback = cls._calculate_feedback(list(code), list(guess))
        
        # Check if it matches the actual feedback
        return (calculated_feedback.correct_position == feedback.correct_position and
                calculated_feedback.correct_color == feedback.correct_color)