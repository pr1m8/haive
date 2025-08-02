from __future__ import annotations

import uuid
from enum import Enum
from re import T
from typing import Any, Generic, Literal, TypeVar, cast

from haive.games.framework.core.board import Board
from haive.games.framework.core.container import GamePieceContainer
from haive.games.framework.core.game import Game
from haive.games.framework.core.piece import GamePiece
from haive.games.framework.core.position import Position
from haive.games.framework.core.space import Space
from pydantic import BaseModel, Field, computed_field, field_validator, model_validator

# Import from our base framework

# ======================================================
# BASE GAME CLASS (Added to framework)
# ======================================================


class Game(BaseModel, Generic[P, T]):
    """Base class for all games."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    board: Board
    status: str = "not_started"
    current_player_id: str | None = None
    players: list[str] = Field(default_factory=list)
    moves: list[dict[str, any]] = Field(default_factory=list)

    def start_game(self) -> None:
        """Start the game."""
        self.status = "in_progress"

    def is_valid_move(self, move: dict[str, any]) -> bool:
        """Check if a move is valid."""
        return True

    def make_move(self, move: dict[str, any]) -> bool:
        """Make a move in the game."""
        if self.is_valid_move(move):
            self.moves.append(move)
            return True
        return False

    def end_game(self) -> None:
        """End the game."""
        self.status = "completed"

    @computed_field
    @property
    def move_count(self) -> int:
        """Get the number of moves made so far."""
        return len(self.moves)

    def reset(self) -> None:
        """Reset the game to initial state."""
        self.status = "not_started"
        self.moves = []


# ======================================================
# TOWER OF HANOI TYPES AND CONSTANTS
# ======================================================

# Use Literal types for peg numbers for type safety
PegNumber = Literal[1, 2, 3]  # Standard Tower of Hanoi has 3 pegs


class GameStatus(str, Enum):
    """Status of a Tower of Hanoi game."""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


# Type variables for generic relationships
D = TypeVar("D", bound="Disk")  # Disk type
P = TypeVar("P", bound="PegPosition")  # Position type
S = TypeVar("S", bound="PegSpace")  # Space type

# ======================================================
# TOWER OF HANOI POSITION
# ======================================================


class PegPosition(Position):
    """Position on a Tower of Hanoi peg."""

    peg: PegNumber  # Which peg (1, 2, or 3)
    level: int  # Position in stack (0 = bottom)

    @field_validator("level")
    @classmethod
    def validate_level(cls, v: int) -> int:
        """Ensure level is valid."""
        if v < 0:
            raise ValueError("Level must be non-negative")
        return v

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PegPosition):
            return False
        return self.peg == other.peg and self.level == other.level

    def __hash__(self) -> int:
        return hash((self.peg, self.level))

    @computed_field
    @property
    def display_coords(self) -> str:
        """Return human-readable coordinates."""
        return f"Peg {self.peg}, Level {self.level}"


# ======================================================
# TOWER OF HANOI DISK (GAME PIECE)
# ======================================================


class Disk(GamePiece[PegPosition]):
    """A disk in the Tower of Hanoi game."""

    size: int  # Disk size (1 = smallest)
    color: str | None = None

    @field_validator("size")
    @classmethod
    def validate_size(cls, v: int) -> int:
        """Ensure size is positive."""
        if v <= 0:
            raise ValueError("Disk size must be positive")
        return v

    def can_move_to(self, position: PegPosition, board: HanoiBoard) -> bool:
        """Check if this disk can be moved to the specified position."""
        # Get the current position
        if self.position is None:
            return False

        # Must be moving to a different peg
        if position.peg == self.position.peg:
            return False

        # Must be the top disk on current peg
        if not self._is_top_disk(board):
            return False

        # Target position must be the top level of the target peg
        top_level = board.get_top_level(position.peg)
        if position.level != top_level + 1:  # +1 because it will be on top
            return False

        # Can only place on top of a larger disk
        top_disk = board.get_top_disk(position.peg)
        return not (top_disk is not None and top_disk.size < self.size)

    def _is_top_disk(self, board: HanoiBoard) -> bool:
        """Check if this disk is the top disk on its peg."""
        if self.position is None:
            return False

        top_disk = board.get_top_disk(self.position.peg)
        return top_disk is not None and top_disk.id == self.id


# ======================================================
# TOWER OF HANOI SPACE
# ======================================================


class PegSpace(Space[PegPosition, Disk]):
    """A space on a Tower of Hanoi peg."""

    position: PegPosition

    @computed_field
    @property
    def peg_number(self) -> PegNumber:
        """Get the peg number this space is on."""
        return self.position.peg

    @computed_field
    @property
    def level(self) -> int:
        """Get the level of this space."""
        return self.position.level

    def is_valid_for_disk(self, disk: Disk) -> bool:
        """Check if a disk can be placed on this space."""
        # Empty space is valid if it's the bottom or if space below has a disk
        if not self.is_occupied():
            return True

        # Otherwise, can only place smaller disk on top of larger disk
        return not (self.piece and disk.size >= self.piece.size)


# ======================================================
# TOWER OF HANOI BOARD
# ======================================================


class HanoiBoard(Board[PegSpace[Disk], PegPosition, Disk]):
    """A Tower of Hanoi board with pegs and disks."""

    num_disks: int
    num_pegs: Literal[3] = 3  # Standard Tower of Hanoi has 3 pegs

    @field_validator("num_disks")
    @classmethod
    def validate_num_disks(cls, v: int) -> int:
        """Ensure there's at least one disk."""
        if v <= 0:
            raise ValueError("Number of disks must be positive")
        return v

    def get_space_at_position(self, position: PegPosition) -> PegSpace[Disk] | None:
        """Get the space at the specified peg position."""
        for space in self.spaces.values():
            if (
                isinstance(space.position, PegPosition)
                and space.position.peg == position.peg
                and space.position.level == position.level
            ):
                return space
        return None

    def get_peg_spaces(self, peg: PegNumber) -> list[PegSpace[Disk]]:
        """Get all spaces on a specific peg."""
        return [
            space
            for space in self.spaces.values()
            if isinstance(space.position, PegPosition) and space.position.peg == peg
        ]

    def get_peg_disks(self, peg: PegNumber) -> list[Disk]:
        """Get all disks on a specific peg, from bottom to top."""
        spaces = self.get_peg_spaces(peg)
        # Sort by level, bottom (0) to top
        spaces.sort(key=lambda s: s.position.level)
        return [s.piece for s in spaces if s.piece is not None]

    def get_top_disk(self, peg: PegNumber) -> Disk | None:
        """Get the top disk on a specific peg."""
        disks = self.get_peg_disks(peg)
        return disks[-1] if disks else None

    def get_top_level(self, peg: PegNumber) -> int:
        """Get the level of the top occupied space on a peg."""
        spaces = self.get_peg_spaces(peg)
        occupied_spaces = [s for s in spaces if s.is_occupied()]

        if not occupied_spaces:
            return -1  # Peg is empty, so next level would be 0

        return max(s.position.level for s in occupied_spaces)

    def initialize_board(self) -> None:
        """Initialize the Tower of Hanoi board with all disks on the first peg."""
        # Create spaces for each peg and level
        self.num_disks - 1
        for peg in range(1, self.num_pegs + 1):
            peg_num = cast(PegNumber, peg)  # Cast to satisfy the type checker
            for level in range(self.num_disks):
                position = PegPosition(peg=peg_num, level=level)
                space = PegSpace[Disk](position=position)
                self.add_space(space)

        # Create and place disks on the first peg
        for i in range(self.num_disks):
            size = self.num_disks - i  # Largest disk at bottom
            disk = Disk(size=size, position=PegPosition(peg=1, level=i))
            self.place_piece(disk, disk.position)

    def move_disk(self, from_peg: PegNumber, to_peg: PegNumber) -> bool:
        """Move the top disk from one peg to another."""
        # Get the top disk on the source peg
        source_disk = self.get_top_disk(from_peg)
        if source_disk is None:
            return False  # No disk to move

        # Calculate the level for the disk on the destination peg
        dest_level = self.get_top_level(to_peg) + 1
        dest_position = PegPosition(peg=to_peg, level=dest_level)

        # Check if the move is valid
        if not source_disk.can_move_to(dest_position, self):
            return False

        # Remove disk from source peg and update its position
        current_position = source_disk.position
        if current_position:
            self.remove_piece(current_position)

        # Place disk on destination peg
        return self.place_piece(source_disk, dest_position)

    @computed_field
    @property
    def is_solved(self) -> bool:
        """Check if all disks have been moved to the final peg."""
        # All disks should be on peg 3 (standard goal)
        target_peg: PegNumber = 3
        disks_on_target = self.get_peg_disks(target_peg)

        # Check if we have all disks on the target peg
        if len(disks_on_target) != self.num_disks:
            return False

        # Check if disks are in correct order (largest at bottom)
        for i, disk in enumerate(disks_on_target):
            expected_size = self.num_disks - i
            if disk.size != expected_size:
                return False

        return True


# ======================================================
# TOWER OF HANOI GAME - EXTENDS BASE GAME CLASS
# ======================================================


class HanoiGame(Game[PegPosition, Disk]):
    """Tower of Hanoi game, extending the base Game class."""

    board: HanoiBoard
    status: GameStatus = GameStatus.NOT_STARTED
    min_moves: int = 0

    @model_validator(mode="after")
    @classmethod
    def calculate_min_moves(cls) -> HanoiGame:
        """Calculate the minimum number of moves to solve the puzzle."""
        # Formula: 2^n - 1 where n is the number of disks
        self.min_moves = (2**self.board.num_disks) - 1
        return self

    def start_game(self) -> None:
        """Start a new game."""
        # Initialize the board
        self.board.initialize_board()
        self.status = GameStatus.IN_PROGRESS
        self.moves = []

    def is_valid_move(self, move: dict[str, any]) -> bool:
        """Check if a move is valid according to Tower of Hanoi rules."""
        if "from_peg" not in move or "to_peg" not in move:
            return False

        from_peg = move["from_peg"]
        to_peg = move["to_peg"]

        # Check if source peg has disks
        source_disk = self.board.get_top_disk(from_peg)
        if source_disk is None:
            return False

        # Calculate destination position
        dest_level = self.board.get_top_level(to_peg) + 1
        dest_position = PegPosition(peg=to_peg, level=dest_level)

        # Use the disk's can_move_to method to validate
        return source_disk.can_move_to(dest_position, self.board)

    def make_move(self, move: dict[str, any]) -> bool:
        """Make a move in the Tower of Hanoi game."""
        if self.status != GameStatus.IN_PROGRESS:
            return False

        if not self.is_valid_move(move):
            return False

        # Extract move details
        from_peg = move["from_peg"]
        to_peg = move["to_peg"]

        # Try to move the disk
        if self.board.move_disk(from_peg, to_peg):
            # Record the move
            self.moves.append(move)

            # Check for win condition
            if self.board.is_solved:
                self.status = GameStatus.COMPLETED

            return True
        return False

    # Convenience method to make a move with just peg numbers
    def move_disk(self, from_peg: PegNumber, to_peg: PegNumber) -> bool:
        """Move disk from one peg to another (convenience method)."""
        move = {"from_peg": from_peg, "to_peg": to_peg}
        return self.make_move(move)

    @computed_field
    @property
    def is_optimal(self) -> bool:
        """Check if the solution is optimal (using minimum moves)."""
        return self.status == GameStatus.COMPLETED and self.move_count == self.min_moves

    def reset(self) -> None:
        """Reset the game to the initial state."""
        super().reset()
        self.board.initialize_board()
        self.status = GameStatus.NOT_STARTED


# ======================================================
# PEG CONTAINER
# ======================================================


class Peg(GamePieceContainer[Disk]):
    """A peg in Tower of Hanoi that contains disks."""

    peg_number: PegNumber
    max_disks: int

    def add_disk(self, disk: Disk, validate: bool = True) -> bool:
        """Add a disk to this peg if valid."""
        # Check if peg is full
        if len(self.pieces) >= self.max_disks:
            return False

        # If validating, check if disk can be added (smaller than top disk)
        if validate and self.pieces:
            top_disk = self.pieces[-1]
            if disk.size >= top_disk.size:
                return False

        # Add disk to top of peg
        self.pieces.append(disk)

        # Update disk position
        if hasattr(disk, "position"):
            disk.position = PegPosition(peg=self.peg_number, level=len(self.pieces) - 1)

        return True

    def remove_top_disk(self) -> Disk | None:
        """Remove and return the top disk."""
        if not self.pieces:
            return None
        return self.pieces.pop()

    @computed_field
    @property
    def top_disk(self) -> Disk | None:
        """Get the top disk without removing it."""
        if not self.pieces:
            return None
        return self.pieces[-1]


# ======================================================
# TOWER OF HANOI MOVE
# ======================================================


class HanoiMove(BaseModel):
    """Represents a move in Tower of Hanoi."""

    from_peg: PegNumber
    to_peg: PegNumber

    @field_validator("to_peg")
    @classmethod
    def validate_different_pegs(cls, v: PegNumber, info: Any) -> PegNumber:
        """Validate that source and destination pegs are different."""
        if "from_peg" in info.data and v == info.data["from_peg"]:
            raise ValueError("Source and destination pegs must be different")
        return v


# ======================================================
# MOVE SOLVER
# ======================================================


class HanoiSolver(BaseModel):
    """Solver for Tower of Hanoi puzzles."""

    @staticmethod
    def solve(num_disks: int) -> list[HanoiMove]:
        """Generate the optimal solution sequence."""
        moves: list[HanoiMove] = []

        def move_tower(
            n: int, source: PegNumber, target: PegNumber, auxiliary: PegNumber
        ) -> None:
            if n > 0:
                # Move n-1 disks from source to auxiliary using target as
                # auxiliary
                move_tower(n - 1, source, auxiliary, target)
                # Move the largest disk from source to target
                moves.append(HanoiMove(from_peg=source, to_peg=target))
                # Move n-1 disks from auxiliary to target using source as
                # auxiliary
                move_tower(n - 1, auxiliary, target, source)

        # Call the recursive function to generate moves
        source_peg: PegNumber = 1
        target_peg: PegNumber = 3
        auxiliary_peg: PegNumber = 2
        move_tower(num_disks, source_peg, target_peg, auxiliary_peg)

        return moves
