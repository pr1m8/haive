from src.haive.games.framework.base.state import GameState
from src.haive.games.single_player.wordle.models import WordCell, WordConnectionsMove, GameSource
from pydantic import Field
from typing import List, Dict, Optional, Literal

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