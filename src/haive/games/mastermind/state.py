from typing import List, Dict, Literal, Optional
from pydantic import BaseModel, Field
from src.haive.games.framework.base.state import GameState
from src.haive.games.mastermind.models import MastermindGuess, MastermindFeedback
from .models import ColorCode, MastermindGuess, MastermindFeedback, MastermindAnalysis
import random
from typing import Union
class MastermindState(GameState):
    """State for a Mastermind game."""
    secret_code: List[str] = Field(..., min_items=4, max_items=4, description="Secret color code (4 colors)")
    guesses: List[MastermindGuess] = Field(default_factory=list, description="History of guesses")
    feedback: List[MastermindFeedback] = Field(default_factory=list, description="Feedback for each guess")
    turn: Literal["player1", "player2"] = Field(..., description="Current player's turn (codebreaker)")
    codemaker: Literal["player1", "player2"] = Field(..., description="Player who created the code")
    max_turns: int = Field(default=10, description="Maximum number of turns")
    game_status: Literal["ongoing", "player1_win", "player2_win"] = Field(
        default="ongoing", description="Status of the game"
    )
    winner: Optional[str] = Field(default=None, description="Winner of the game, if any")
    player1_analysis: List[Dict[str, any]] = Field(default_factory=list, description="Analyses by player1")
    player2_analysis: List[Dict[str, any]] = Field(default_factory=list, description="Analyses by player2")
    @classmethod
    def initialize(
        cls,
        codemaker: str = "player1",
        colors: Optional[List[str]] = None,
        code_length: int = 4,
        max_turns: int = 10,
        secret_code: Optional[Union[List[str], ColorCode, dict]] = None
    ) -> "MastermindState":
        colors = colors or ["red", "blue", "green", "yellow", "purple", "orange"]
        codebreaker = "player2" if codemaker == "player1" else "player1"

        # Unwrap or generate secret code
        if isinstance(secret_code, ColorCode):
            secret_code = secret_code.code
        elif isinstance(secret_code, dict) and "code" in secret_code:
            secret_code = secret_code["code"]
        elif not secret_code:
            secret_code = random.choices(colors, k=code_length)

        return cls(
            secret_code=secret_code,
            guesses=[],
            feedback=[],
            turn=codebreaker,
            codemaker=codemaker,
            max_turns=max_turns,
            game_status="ongoing"
        )
    @property
    def current_turn_number(self) -> int:
        """Get the current turn number."""
        return len(self.guesses) + 1
    
    @property
    def turns_remaining(self) -> int:
        """Get the number of turns remaining."""
        return max(0, self.max_turns - len(self.guesses))
    
    @property
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.game_status != "ongoing"
    
    @property
    def last_guess(self) -> Optional[MastermindGuess]:
        """Get the last guess made."""
        return self.guesses[-1] if self.guesses else None
    
    @property
    def last_feedback(self) -> Optional[MastermindFeedback]:
        """Get the feedback for the last guess."""
        return self.feedback[-1] if self.feedback else None
    
    @property
    def board_string(self) -> str:
        """Get a string representation of the board."""
        if not self.guesses:
            return "No guesses yet."
        
        result = []
        result.append("Turn | Guess                     | Feedback")
        result.append("-" * 50)
        
        for i, (guess, feedback) in enumerate(zip(self.guesses, self.feedback)):
            guess_str = f"{', '.join(guess.colors)}"
            feedback_str = f"🎯 {feedback.correct_position} | 🔄 {feedback.correct_color}"
            result.append(f"{i+1:4d} | {guess_str:25s} | {feedback_str}")
        
        return "\n".join(result)
    