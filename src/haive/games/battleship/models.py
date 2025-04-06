"""
Battleship game models module.

This module provides data models for the Battleship game, including:
    - Ship representation
    - Board state
    - Move commands
    - Placement validation
    - Game state tracking
"""

from typing import List, Dict, Tuple, Optional, Any, Set, Literal
from pydantic import BaseModel, Field, field_validator, root_validator
from enum import Enum

class ShipType(str, Enum):
    """Ship types in Battleship."""
    CARRIER = "Carrier"
    BATTLESHIP = "Battleship"
    CRUISER = "Cruiser"
    SUBMARINE = "Submarine"
    DESTROYER = "Destroyer"

# Ship sizes by type
SHIP_SIZES = {
    ShipType.CARRIER: 5,
    ShipType.BATTLESHIP: 4,
    ShipType.CRUISER: 3,
    ShipType.SUBMARINE: 3,
    ShipType.DESTROYER: 2
}

class Coordinates(BaseModel):
    """Represents a coordinate on the board."""
    row: int = Field(..., ge=0, le=9, description="Row index (0-9)")
    col: int = Field(..., ge=0, le=9, description="Column index (0-9)")
    
    def to_tuple(self) -> Tuple[int, int]:
        """Convert to tuple representation."""
        return (self.row, self.col)
    
    def __str__(self) -> str:
        """String representation of coordinates."""
        return f"({self.row}, {self.col})"

class Ship(BaseModel):
    """Represents a ship on the board."""
    ship_type: ShipType
    size: int = Field(..., description="Size of the ship")
    coordinates: List[Coordinates] = Field(default_factory=list)
    hits: int = Field(default=0, description="Number of hits on this ship")
    
    @property
    def is_sunk(self) -> bool:
        """Check if the ship is sunk."""
        return self.hits >= self.size
    
    def get_occupied_positions(self) -> List[Tuple[int, int]]:
        """Get all positions occupied by this ship."""
        return [(c.row, c.col) for c in self.coordinates]
    
    def __str__(self) -> str:
        """String representation of the ship."""
        return f"{self.ship_type} ({self.size}): {[str(c) for c in self.coordinates]}"

class ShipPlacement(BaseModel):
    """Represents a ship placement command."""
    ship_type: ShipType
    coordinates: List[Coordinates]
    
    @field_validator("coordinates")
    @classmethod
    def validate_coordinates(cls, coords):
        """Ensure coordinates list contains valid Coordinates instances."""
        if not isinstance(coords, list):
            raise ValueError("Coordinates must be a list")
        
        processed_coords = []
        for c in coords:
            if isinstance(c, Coordinates):
                processed_coords.append(c)
            elif isinstance(c, dict):
                processed_coords.append(Coordinates(**c))
            else:
                raise ValueError(f"Invalid coordinate format: {c}")
                
        return processed_coords
    
    def __str__(self) -> str:
        """String representation of the placement."""
        return f"{self.ship_type} at {[str(c) for c in self.coordinates]}"

class ShipPlacementWrapper(BaseModel):
    """Wrapper for a list of ship placements returned by LLM."""
    placements: List[ShipPlacement] = Field(..., description="List of ship placements")
    
    @root_validator(skip_on_failure=True)
    def validate_placements(cls, values):
        """Validate ship placements."""
        placements = values.get("placements", [])
        if not isinstance(placements, list):
            raise ValueError("Placements must be a list")
        
        # Ensure all required ship types are included
        ship_types = [p.ship_type for p in placements]
        all_ship_types = list(ShipType)
        
        if sorted(ship_types) != sorted(all_ship_types):
            # Find missing ship types
            missing_types = set(all_ship_types) - set(ship_types)
            if missing_types:
                raise ValueError(f"Missing ship types: {', '.join(t.value for t in missing_types)}")
            
            # Find duplicate ship types
            duplicates = [t for t in ship_types if ship_types.count(t) > 1]
            if duplicates:
                raise ValueError(f"Duplicate ship types: {', '.join(t.value for t in set(duplicates))}")
        
        return values

class MoveResult(str, Enum):
    """Possible results of a move."""
    HIT = "hit"
    MISS = "miss"
    SUNK = "sunk"
    INVALID = "invalid"

class MoveCommand(BaseModel):
    """Represents an attack command."""
    row: int = Field(..., ge=0, le=9)
    col: int = Field(..., ge=0, le=9)
    
    def to_coordinates(self) -> Coordinates:
        """Convert to Coordinates object."""
        return Coordinates(row=self.row, col=self.col)
    
    def __str__(self) -> str:
        """String representation of the move."""
        return f"Attack ({self.row}, {self.col})"

class MoveOutcome(BaseModel):
    """Outcome of a move."""
    row: int
    col: int
    result: MoveResult
    sunk_ship: Optional[ShipType] = None
    
    def __str__(self) -> str:
        """String representation of the outcome."""
        result = f"({self.row}, {self.col}): {self.result}"
        if self.sunk_ship:
            result += f" - {self.sunk_ship} sunk!"
        return result

class Analysis(BaseModel):
    """Strategic analysis of the game state."""
    analysis: str = Field(..., description="Strategic analysis text")
    priority_targets: Optional[List[Coordinates]] = Field(default_factory=list, description="Priority targets for next attacks")
    
    @field_validator("priority_targets")
    @classmethod
    def validate_targets(cls, targets):
        """Validate priority targets."""
        if not isinstance(targets, list):
            return []
        
        processed_targets = []
        for t in targets:
            if isinstance(t, Coordinates):
                processed_targets.append(t)
            elif isinstance(t, dict):
                processed_targets.append(Coordinates(**t))
            else:
                # Skip invalid targets
                continue
                
        return processed_targets

class PlayerBoard(BaseModel):
    """Represents a player's board state."""
    ships: List[Ship] = Field(default_factory=list)
    hits: List[Coordinates] = Field(default_factory=list)  # Hits by opponent
    misses: List[Coordinates] = Field(default_factory=list)  # Misses by opponent
    attacks: List[Coordinates] = Field(default_factory=list)  # All attacks made by this player
    successful_hits: List[Coordinates] = Field(default_factory=list)  # Successful hits made by player
    failed_attacks: List[Coordinates] = Field(default_factory=list)  # Missed attacks made by player
    sunk_ships: List[ShipType] = Field(default_factory=list)  # Ships sunk by opponent
    
    def is_valid_placement(self, placement: ShipPlacement) -> bool:
        """Check if a ship placement is valid."""
        # Check if ship size matches expected size
        expected_size = SHIP_SIZES[placement.ship_type]
        if len(placement.coordinates) != expected_size:
            return False
        
        # Check if ship is in a straight line (horizontal or vertical)
        rows = [c.row for c in placement.coordinates]
        cols = [c.col for c in placement.coordinates]
        
        if len(set(rows)) == 1:  # Horizontal ship
            # Check if columns are consecutive
            sorted_cols = sorted(cols)
            if sorted_cols != list(range(min(cols), max(cols) + 1)):
                return False
        elif len(set(cols)) == 1:  # Vertical ship
            # Check if rows are consecutive
            sorted_rows = sorted(rows)
            if sorted_rows != list(range(min(rows), max(rows) + 1)):
                return False
        else:
            # Neither horizontal nor vertical
            return False
        
        # Check if ship overlaps with existing ships
        proposed_coords = {(c.row, c.col) for c in placement.coordinates}
        existing_coords = {(c.row, c.col) for ship in self.ships for c in ship.coordinates}
        
        if proposed_coords.intersection(existing_coords):
            return False
        
        return True
    
    def place_ship(self, placement: ShipPlacement) -> bool:
        """Place a ship on the board."""
        if not self.is_valid_placement(placement):
            return False
        
        ship = Ship(
            ship_type=placement.ship_type,
            size=SHIP_SIZES[placement.ship_type],
            coordinates=placement.coordinates
        )
        
        self.ships.append(ship)
        return True
    
    def receive_attack(self, row: int, col: int) -> MoveOutcome:
        """Process an attack from the opponent."""
        coord = Coordinates(row=row, col=col)
        coord_tuple = coord.to_tuple()
        
        # Check if this position has already been attacked
        for hit in self.hits:
            if hit.to_tuple() == coord_tuple:
                return MoveOutcome(row=row, col=col, result=MoveResult.INVALID)
        
        for miss in self.misses:
            if miss.to_tuple() == coord_tuple:
                return MoveOutcome(row=row, col=col, result=MoveResult.INVALID)
        
        # Check if the attack hits any ship
        for ship in self.ships:
            for ship_coord in ship.coordinates:
                if ship_coord.to_tuple() == coord_tuple:
                    # Record hit
                    self.hits.append(coord)
                    ship.hits += 1
                    
                    if ship.is_sunk:
                        # Record ship as sunk
                        self.sunk_ships.append(ship.ship_type)
                        return MoveOutcome(row=row, col=col, result=MoveResult.SUNK, sunk_ship=ship.ship_type)
                    
                    return MoveOutcome(row=row, col=col, result=MoveResult.HIT)
        
        # No hit, record as miss
        self.misses.append(coord)
        return MoveOutcome(row=row, col=col, result=MoveResult.MISS)
    
    def all_ships_sunk(self) -> bool:
        """Check if all ships on the board are sunk."""
        return all(ship.is_sunk for ship in self.ships)
    
    def get_occupied_positions(self) -> List[Tuple[int, int]]:
        """Get all positions occupied by ships."""
        return [(c.row, c.col) for ship in self.ships for c in ship.coordinates]

class GamePhase(str, Enum):
    """Game phases."""
    SETUP = "setup"
    PLAYING = "playing"
    ENDED = "ended"