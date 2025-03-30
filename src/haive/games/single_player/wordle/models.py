from typing import List, Dict, Literal, Optional
from enum import Enum
from pydantic import BaseModel, Field, model_validator
from src.haive.games.framework.base import GameState

class WordCell(BaseModel):
    """Represents a cell in the Word Connections grid."""
    word: str = Field(..., description="The word in this cell")
    index: int = Field(..., description="Position index in the grid (0-15)")
    selected: bool = Field(default=False, description="Whether this cell is currently selected")
    solved: bool = Field(default=False, description="Whether this cell has been solved (part of a found group)")
    category: Optional[str] = Field(default=None, description="Category this word belongs to (once discovered)")
    
    def __str__(self):
        status = ""
        if self.solved:
            status = " (Solved)"
        elif self.selected:
            status = " (Selected)"
        return f"{self.word}{status}"

class WordConnectionsMove(BaseModel):
    """Represents a move in Word Connections game."""
    words: List[str] = Field(..., description="Set of 4 words that the player believes are connected")
    category_guess: Optional[str] = Field(default=None, description="Player's guess about what connects these words")
    indices: Optional[List[int]] = Field(default=None, description="Indices of the selected cells")
    result: Optional[str] = Field(default=None, description="Result of this move (correct, incorrect)")
    
    @model_validator(mode='after')
    def validate_length(self):
        """Validate that exactly 4 words are provided."""
        if len(self.words) != 4:
            raise ValueError(f"Must select exactly 4 words, selected {len(self.words)}")
        return self
    
    def __str__(self):
        """String representation of the move."""
        result_str = ""
        if self.result:
            result_str = f" - {self.result.upper()}"
            
        if self.category_guess:
            return f"Group: {', '.join(self.words)} (Category guess: {self.category_guess}){result_str}"
        return f"Group: {', '.join(self.words)}{result_str}"

class WordConnectionsAnalysis(BaseModel):
    """Analysis of a Word Connections position."""
    potential_groups: List[Dict[str, List[str]]] = Field(
        default_factory=list, 
        description="Potential groupings with category names and word lists"
    )
    difficult_words: List[str] = Field(
        default_factory=list,
        description="Words that are difficult to categorize"
    )
    patterns_observed: List[str] = Field(
        default_factory=list,
        description="Patterns or themes observed in the remaining words"
    )
    strategy: str = Field(
        default="",
        description="Strategic recommendations for the next move"
    )
    previous_attempt_analysis: str = Field(
        default="",
        description="Analysis of why previous attempts may have failed"
    )

class GameSource(str, Enum):
    """Source of the game data."""
    INTERNAL = "internal"
    NYT = "nyt"

class WordConnectionsState(GameState):
    """State for a Word Connections game."""
    # Grid and word tracking
    cells: List[WordCell] = Field(..., description="Grid cells with words and their states")
    remaining_words: List[str] = Field(..., description="Words still available on the grid")
    
    # Game progress tracking
    discovered_groups: Dict[str, List[str]] = Field(
        default_factory=dict, 
        description="Groups that have been correctly identified with their category"
    )
    incorrect_attempts: List[List[str]] = Field(
        default_factory=list,
        description="List of incorrect word groups that have been attempted"
    )
    attempts_remaining: int = Field(
        default=4,
        description="Number of incorrect attempts allowed before game ends"
    )
    incorrect_submissions: int = Field(
        default=0,
        description="Number of incorrect submissions made"
    )
    
    # Game definition (private to the game)
    categories: Dict[str, List[str]] = Field(
        ..., 
        description="The correct categories and word groupings (hidden from players during game)"
    )
    category_difficulty: Dict[str, str] = Field(
        default_factory=dict,
        description="Difficulty level for each category (yellow, green, blue, purple from easiest to hardest)"
    )
    
    # Game metadata
    game_source: GameSource = Field(
        default=GameSource.INTERNAL,
        description="Source of the game data (internal or NYT)"
    )
    game_date: Optional[str] = Field(
        default=None,
        description="Date of the game if from NYT"
    )
    
    # Game state
    turn: str = Field(default="player", description="Current player's turn (always 'player' in single-player mode)")
    game_status: Literal["ongoing", "victory", "defeat"] = Field(
        default="ongoing", description="Status of the game"
    )
    move_history: List[WordConnectionsMove] = Field(
        default_factory=list, description="History of moves"
    )
    analysis_history: List[Dict] = Field(
        default_factory=list, description="History of analyses"
    )
    score: int = Field(
        default=0, description="Number of categories found"
    )
    
    # Current selection tracking
    selected_indices: List[int] = Field(
        default_factory=list,
        description="Currently selected cell indices"
    )
    
    @property
    def board_string(self) -> str:
        """Get a string representation of the board."""
        if not self.remaining_words:
            return "All words have been grouped successfully!"
            
        # Create a visual representation of the 4x4 grid
        display = "Current Word Grid:\n\n"
        
        # Find the maximum length for formatting
        max_len = max(len(cell.word) for cell in self.cells)
        
        # Format in a 4x4 grid with cell states
        for i in range(0, 16, 4):
            row_cells = self.cells[i:i+4]
            row = []
            for cell in row_cells:
                word = cell.word
                
                # Format based on cell state
                if cell.solved:
                    # Show solved words with their category color
                    category = cell.category or ""
                    difficulty = self.category_difficulty.get(category, "")
                    color_code = {
                        "yellow": "🟨", "green": "🟩", 
                        "blue": "🟦", "purple": "🟪"
                    }.get(difficulty, "")
                    formatted = f"{color_code} {word.ljust(max_len)}"
                elif cell.selected or cell.index in self.selected_indices:
                    # Show selected words with indicator
                    formatted = f"✓ {word.ljust(max_len)}"
                else:
                    # Show normal words
                    formatted = f"  {word.ljust(max_len)}"
                
                row.append(formatted)
                
            display += " | ".join(row) + "\n"
            if i < 12:  # Don't add a separator after the last row
                display += "-" * (max_len * 4 + 20) + "\n"
                
        # Add cell indices for reference
        display += "\nCell indices for reference:\n"
        for i in range(0, 16, 4):
            indices = [str(j).ljust(max_len) for j in range(i, i+4)]
            display += "  " + " | ".join(indices) + "\n"
        
        # Add information about discovered groups
        if self.discovered_groups:
            display += "\nDiscovered Groups:\n"
            for category, words in self.discovered_groups.items():
                difficulty = self.category_difficulty.get(category, "")
                color_code = {
                    "yellow": "🟨", "green": "🟩", 
                    "blue": "🟦", "purple": "🟪"
                }.get(difficulty, "")
                display += f"{color_code} {category}: {', '.join(words)}\n"
                
        # Add information about incorrect attempts
        if self.incorrect_attempts:
            display += "\nIncorrect Attempts:\n"
            for i, attempt in enumerate(self.incorrect_attempts):
                display += f"{i+1}. {', '.join(attempt)}\n"
                
        # Add attempts information
        display += f"\nIncorrect submissions: {self.incorrect_submissions}/4"
        display += f"\nAttempts remaining: {self.attempts_remaining}"
        
        # Add currently selected words
        if self.selected_indices:
            selected_words = [self.cells[i].word for i in self.selected_indices]
            display += f"\n\nCurrently selected: {', '.join(selected_words)}"
        
        return display


class WordConnectionsPlayerDecision(BaseModel):
    """Decision made by a player in Word Connections."""
    move: WordConnectionsMove = Field(..., description="The move to make")
    reasoning: str = Field(..., description="Reasoning behind the move")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Confidence level in this grouping (0-1)")
    alternative_groups: List[Dict[str, List[str]]] = Field(
        default_factory=list, 
        description="Alternative groupings considered"
    )
    
    @model_validator(mode='after')
    def validate_move(self):
        """Ensure the move contains exactly 4 words."""
        if len(self.move.words) != 4:
            raise ValueError(f"A move must contain exactly 4 words, got {len(self.move.words)}")
        return self