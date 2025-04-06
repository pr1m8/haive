from typing import Literal, List, Tuple, Optional, Dict, Any, Annotated, Sequence
from pydantic import BaseModel, Field
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage

from src.haive.games.battleship.models import GamePhase, MoveOutcome, PlayerBoard, ShipPlacement


class PlayerState(BaseModel):
    """Complete state for a player including board and analysis."""
    board: PlayerBoard = Field(default_factory=PlayerBoard)
    strategic_analysis: List[str] = Field(default_factory=list)
    
    has_placed_ships: bool = Field(default=False)
    ship_placements: List[ShipPlacement] = Field(default_factory=list)


class BattleshipState(BaseModel):
    """Complete game state for Battleship."""
    # Player states - using Annotated for accumulation
    player1_state: Annotated[PlayerState, "accumulate"] = Field(default_factory=PlayerState)
    player2_state: Annotated[PlayerState, "accumulate"] = Field(default_factory=PlayerState)
    
    # Game state
    current_player: Literal["player1", "player2"] = Field(default="player1")
    game_phase: GamePhase = Field(default=GamePhase.SETUP)
    winner: Optional[Literal["player1", "player2"]] = Field(default=None)
    
    # Move history
    move_history: List[Tuple[str, MoveOutcome]] = Field(default_factory=list)
    
    # Error state
    error_message: Optional[str] = Field(default=None)
    
    def get_player_state(self, player: str) -> PlayerState:
        """Get a player's state by name."""
        if player == "player1":
            return self.player1_state
        elif player == "player2":
            return self.player2_state
        else:
            raise ValueError(f"Invalid player: {player}")
    
    def get_opponent(self, player: str) -> str:
        """Get the name of a player's opponent."""
        return "player2" if player == "player1" else "player1"
    
    def is_setup_complete(self) -> bool:
        """Check if setup phase is complete."""
        return (self.player1_state.has_placed_ships and 
                self.player2_state.has_placed_ships)
    
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return (self.game_phase == GamePhase.ENDED or 
                self.player1_state.board.all_ships_sunk() or 
                self.player2_state.board.all_ships_sunk())
        
    def get_public_state_for_player(self, player: str) -> Dict[str, Any]:
        """
        Get a public view of the game state for a player.
        This hides the opponent's ship positions.
        """
        opponent = self.get_opponent(player)
        player_state = self.get_player_state(player)
        opponent_state = self.get_player_state(opponent)

        # Ensure strategic thoughts are available
        strategic_thoughts = (player_state.strategic_analysis[-1] 
                            if player_state.strategic_analysis 
                            else "No previous strategic analysis.")

        return {
            # Game status information
            "game_phase": self.game_phase,
            "current_player": self.current_player,
            "is_your_turn": self.current_player == player,

            # Hits, misses, and sunk ships
            "your_hits": [c.model_dump() for c in player_state.board.successful_hits],
            "your_misses": [c.model_dump() for c in player_state.board.failed_attacks],
            "your_sunk_ships": [ship.value for ship in player_state.board.sunk_ships],

            "opponent_hits": [c.model_dump() for c in opponent_state.board.successful_hits],
            "opponent_misses": [c.model_dump() for c in opponent_state.board.failed_attacks],
            "opponent_sunk_ships": [ship.value for ship in opponent_state.board.sunk_ships],

            # Strategic information
            "strategic_thoughts": strategic_thoughts,

            # Optional extras for debugging/logging
            "move_history": [(p, m.model_dump()) for p, m in self.move_history],
            "your_analysis": player_state.strategic_analysis,

            # Ensure structured output compatibility
            "row": None,  # Add this to match prompt template expectations
            "col": None
        }