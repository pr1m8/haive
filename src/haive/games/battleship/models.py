from typing import List, Dict, Literal, Optional, Tuple, Set
from pydantic import BaseModel, Field, field_validator

# ------------------------------
# 🚢 1. Predefined Ships for Battleship
# ------------------------------
PREBUILT_SHIP_DICT: Dict[str, int] = {
    "Carrier": 5,
    "Battleship": 4,
    "Cruiser": 3,
    "Submarine": 3,
    "Destroyer": 2,
}

# ------------------------------
# 📍 2. Coordinates Model
# ------------------------------
class Coordinates(BaseModel):
    """Represents a coordinate on the board."""
    row: int = Field(..., ge=0, le=9, description="Row of the coordinate (0-9).")
    col: int = Field(..., ge=0, le=9, description="Column of the coordinate (0-9).")

    def to_tuple(self) -> Tuple[int, int]:
        """Returns coordinates as a tuple."""
        return (self.row, self.col)

# ------------------------------
# 🚢 3. Ship Model
# ------------------------------
class Ship(BaseModel):
    """Represents a ship in Battleship."""
    name: Literal["Carrier", "Battleship", "Cruiser", "Submarine", "Destroyer"]
    size: int
    coordinates: List[Coordinates] = Field(default_factory=list)
    hits: int = 0

    @property
    def is_sunk(self) -> bool:
        """Checks if the ship is completely destroyed."""
        return self.hits >= self.size

# ✅ Prebuilt Ship Objects
PREBUILT_SHIPS = [Ship(name=name, size=size) for name, size in PREBUILT_SHIP_DICT.items()]

# ------------------------------
# 🛠️ 4. Battleship Placement Model
# ------------------------------
class BattleshipPlacement(BaseModel):
    """Represents ship placement on the board."""
    ship_name: Literal["Carrier", "Battleship", "Cruiser", "Submarine", "Destroyer"]
    coordinates: List[Coordinates]

    @field_validator("coordinates", mode="before")
    @classmethod
    def validate_coordinates(cls, coords):
        """Ensure coordinates are valid instances of `Coordinates`."""
        if not isinstance(coords, list):
            raise ValueError("Coordinates must be a list.")
        return [Coordinates(**coord) if isinstance(coord, dict) else coord for coord in coords]

class BattleshipPlayerDecision(BaseModel):
    """Represents a player's decision in Battleship."""
    move: Coordinates = Field(..., description="The coordinates of the move.")
class BattleshipAnalysis(BaseModel):
    """Represents a player's analysis in Battleship."""
    analysis: str = Field(..., description="The analysis of the player's position.")

# ------------------------------
# 📋 5. Board Placement Model (Ensuring All Ships Are Placed)
# ------------------------------
class BattleshipBoardPlacement(BaseModel):
    """Ensures all ships are placed before starting the game."""
    ship_placements: List[BattleshipPlacement]

    @field_validator("ship_placements", mode="before")
    @classmethod
    def validate_ship_placements(cls, placements):
        """Ensure all ships are placed and validate coordinate data."""
        validated_placements = [
            BattleshipPlacement(**placement) if isinstance(placement, dict) else placement
            for placement in placements
        ]

        placed_ships = {placement.ship_name for placement in validated_placements}
        missing_ships = [ship.name for ship in PREBUILT_SHIPS if ship.name not in placed_ships]

        if missing_ships:
            raise ValueError(f"❌ Missing ships: {', '.join(missing_ships)}")

        return validated_placements

# ------------------------------
# 🎯 6. Move & Move Result Models
# ------------------------------
class BattleshipMoveModel(BaseModel):
    """Represents a structured attack move in Battleship."""
    row: int = Field(..., ge=0, le=9)
    col: int = Field(..., ge=0, le=9)

    
    def to_tuple(self) -> Tuple[int, int]:
        """Returns the move as a tuple."""
        return (self.row, self.col)

class BattleshipMoveResult(BattleshipMoveModel):
    """Represents the result of an attack move, including whether a ship was sunk."""
    result: Literal["hit", "miss", "sunk", "invalid"]
    sunk_ship: Optional[str] = None

# ------------------------------
# 📊 7. Board Model
# ------------------------------
class Board(BaseModel):
    """Represents a player's board state, including private and opponent views."""
    size: int = 10
    ships: List[Ship] = Field(default_factory=list)
    hits: List[Coordinates] = Field(default_factory=list)
    misses: List[Coordinates] = Field(default_factory=list)
    guesses: List[Coordinates] = Field(default_factory=list)
    sunk_ships: List[str] = Field(default_factory=list)

    def is_valid_placement(self, proposed_positions: Set[Tuple[int, int]]) -> bool:
        """Ensure the proposed ship placement is within bounds and does not overlap."""
        occupied_positions = {pos.to_tuple() for s in self.ships for pos in s.coordinates}
        return not any(pos in occupied_positions for pos in proposed_positions)


    def place_ship(self, ship_placement: BattleshipPlacement) -> bool:
        """Adds a ship to the board if it's a valid placement."""
        if ship_placement.ship_name not in [ship.name for ship in PREBUILT_SHIPS]:
            raise ValueError(f"Unknown ship type: {ship_placement.ship_name}")

        ship_size = PREBUILT_SHIP_DICT[ship_placement.ship_name]
        if len(ship_placement.coordinates) != ship_size:
            raise ValueError(f"Invalid placement for {ship_placement.ship_name}: Expected {ship_size} coordinates.")

        ship = Ship(name=ship_placement.ship_name, size=ship_size, coordinates=ship_placement.coordinates)
        if self.is_valid_placement(ship):
            self.ships.append(ship)
            return True
        return False

    def receive_attack(self, row: int, col: int) -> BattleshipMoveResult:
        """
        Processes an attack and returns the result.
        """
        coord = Coordinates(row=row, col=col)

        # Prevent duplicate attacks
        if coord.to_tuple() in [g.to_tuple() for g in self.guesses]:
            return BattleshipMoveResult(row=row, col=col, result="invalid")

        # Add to guessed locations
        self.guesses.append(coord)

        for ship in self.ships:
            if coord.to_tuple() in [c.to_tuple() for c in ship.coordinates]:
                ship.hits += 1
                self.hits.append(coord)

                if ship.is_sunk:
                    self.sunk_ships.append(ship.name)
                    return BattleshipMoveResult(row=row, col=col, result="sunk", sunk_ship=ship.name)

                return BattleshipMoveResult(row=row, col=col, result="hit")

        # If no hits, mark as miss
        self.misses.append(coord)
        return BattleshipMoveResult(row=row, col=col, result="miss")
    def all_ships_sunk(self) -> bool:
        """Check if all ships on the board are sunk."""
        return all(ship.is_sunk for ship in self.ships)