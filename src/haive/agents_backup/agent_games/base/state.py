from pydantic import BaseModel, Field
from typing import List, Tuple, Dict, Optional, Literal, Generic
from src.haive.agents.agent_games.base.models import PlayerState, MoveModel,TMove

class GameState(BaseModel):
    """Generic state for any multi-agent game."""
    players: List[str] = Field(..., description="List of player identifiers.")
    current_turn: str = Field(..., description="ID of the player whose turn it is.")
    move_history: List[Tuple[str, str]] = Field(default_factory=list, description="History of (player_id, move).")
    status: Literal["ongoing", "finished"] = Field(default="ongoing", description="Current game status.")
    private_states: Dict[str, PlayerState] = Field(default_factory=dict, description="Private state per player.")

    def get_private_state(self, player_id: str) -> Optional[PlayerState]:
        """Returns the private state for a specific player."""
        return self.private_states.get(player_id)

class PlayerState(BaseModel):
    """Private state per player, stored separately from GameState."""
    agent_id: str = Field(..., description="Unique identifier for the player.")
    planned_moves: List[str] = Field(default_factory=list)
    strategic_thoughts: List[str] = Field(default_factory=list)
    evaluation: Optional[str] = None

    
class GameStateManager(Generic[TMove]):
    """Manages game state and move application."""

    @staticmethod
    def initialize(players: List[str]) -> GameState:
        """Creates an initial state with the given players."""
        return GameState(players=players, current_turn=players[0])

    @staticmethod
    def apply_move(state: GameState, move_model: MoveModel[TMove], player_id: str) -> GameState:
        """Applies a move to the game state."""
        if state.current_turn != player_id:
            raise ValueError(f"Not {player_id}'s turn!")

        new_state = GameState(
            players=state.players,
            current_turn=state.players[(state.players.index(player_id) + 1) % len(state.players)],  # Rotate turn
            move_history=state.move_history + [(player_id, str(move_model.move))],
            status="ongoing",
            private_states=state.private_states.copy()
        )
        return new_state
