from __future__ import annotations

import uuid
from enum import Enum
from typing import Any

from game_framework_base import GamePiece, GridPosition, GridSpace
from pydantic import BaseModel, Field, field_validator, model_validator

# Import base framework classes

# ======================================================
# 2048 GAME COMPONENTS
# ======================================================


class Direction(str, Enum):
    """Move directions in 2048."""

    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class NumberTile(GamePiece[GridPosition]):
    """A tile in 2048 with a numeric value."""

    value: int
    merged_this_turn: bool = False

    @field_validator("value")
    @classmethod
    def validate_value(cls, v: int) -> int:
        """Ensure value is a valid power of 2."""
        # Check if it's a power of 2
        if v & (v - 1) != 0 or v <= 0:
            raise ValueError("Value must be a positive power of 2")
        return v

    def can_move_to(self, position: GridPosition, board: Board) -> bool:
        """Check if this tile can be placed at the specified position."""
        space = board.get_space_at_position(position)
        if not space:
            return False

        # Can move to empty space
        if not space.is_occupied():
            return True

        # Can move to space with same value (for merging)
        existing_tile = space.piece
        if isinstance(existing_tile, NumberTile) and existing_tile.value == self.value:
            # Can only merge once per turn
            return not existing_tile.merged_this_turn

        return False

    def merge_with(self, other: NumberTile) -> NumberTile:
        """Create a new tile from merging this tile with another."""
        if self.value != other.value:
            raise ValueError("Can only merge tiles with same value")

        new_tile = NumberTile(
            value=self.value * 2, position=self.position, merged_this_turn=True
        )
        return new_tile

    def reset_merge_status(self) -> None:
        """Reset the merged status for a new turn."""
        self.merged_this_turn = False

    def __str__(self) -> str:
        """String representation of the tile."""
        return str(self.value)


class TwentyFortyEightSquare(GridSpace[NumberTile]):
    """A square on the 2048 game board."""

    def place_tile(self, tile: NumberTile) -> bool:
        """Place a tile on this square, handling merges if needed."""
        if not self.is_occupied():
            # Empty space - just place the tile
            return super().place_piece(tile)

        # Check if we can merge with existing tile
        existing_tile = self.piece
        if (
            isinstance(existing_tile, NumberTile)
            and existing_tile.value == tile.value
            and not existing_tile.merged_this_turn
        ):
            # Create merged tile
            merged_tile = tile.merge_with(existing_tile)

            # Replace existing tile with merged tile
            self.piece = merged_tile
            return True

        return False


class TwentyFortyEightGame(BaseModel):
    """Model for managing a 2048 game."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    board: TwentyFortyEightBoard
    target: int = 2048
    game_over: bool = False
    win: bool = False
    moves: int = 0

    @model_validator(mode="after")
    @classmethod
    def validate_game(cls) -> TwentyFortyEightGame:
        """Ensure game has valid components."""
        # Initialize board if not done already
        if self.board and not self.board.spaces:
            self.board.initialize_board()
        return self

    @classmethod
    def new_game(cls) -> TwentyFortyEightGame:
        """Create a new 2048 game."""
        # Create board
        board = TwentyFortyEightBoard(name="2048 Board", rows=4, cols=4)
        board.initialize_board()

        # Create game
        game = cls(board=board)

        # Spawn initial tiles (2)
        game.board.spawn_random_tile()
        game.board.spawn_random_tile()

        return game

    def make_move(self, direction: Direction) -> tuple[bool, int]:
        """Make a move in the specified direction.

        Args:
            direction: Direction to move tiles

        Returns:
            Tuple of (success, points_earned)

        """
        if self.game_over:
            return False, 0

        # Store previous score
        previous_score = self.board.score

        # Move tiles
        moved = self.board.move_tiles(direction)

        if moved:
            # Spawn a new tile
            self.board.spawn_random_tile()

            # Increment move counter
            self.moves += 1

            # Calculate points earned
            points_earned = self.board.score - previous_score

            # Check for win
            if not self.win and self.board.has_winning_tile(self.target):
                self.win = True
                # Note: Game doesn't end on win, player can continue

            # Check for game over (no valid moves)
            if not self.board.has_valid_moves():
                self.game_over = True

            return True, points_earned

        return False, 0

    def restart(self) -> None:
        """Restart the game."""
        self.board.clear()
        self.game_over = False
        self.win = False
        self.moves = 0

        # Spawn initial tiles
        self.board.spawn_random_tile()
        self.board.spawn_random_tile()

    def get_status(self) -> dict[str, Any]:
        """Get the current game status."""
        return {
            "score": self.board.score,
            "moves": self.moves,
            "max_tile": self.board.get_max_tile(),
            "game_over": self.game_over,
            "win": self.win,
            "board": self.board.get_board_state(),
        }

    def __str__(self) -> str:
        """String representation of the game."""
        result = []
        result.append(f"Score: {self.board.score}")
        result.append(f"Moves: {self.moves}")

        # Board representation
        for row in range(self.board.rows):
            row_str = []
            for col in range(self.board.cols):
                square = self.board.get_space_at(row, col)
                if (
                    square
                    and square.is_occupied()
                    and isinstance(square.piece, NumberTile)
                ):
                    # Right-align values in 5-character field
                    row_str.append(f"{square.piece.value:5}")
                else:
                    row_str.append("    ·")
            result.append("|" + "|".join(row_str) + "|")

        if self.win:
            result.append("Congratulations! You've reached the target tile!")

        if self.game_over:
            result.append("Game Over!")

        return "\n".join(result)
