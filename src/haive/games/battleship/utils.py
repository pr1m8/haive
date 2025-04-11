"""
Battleship game utility functions.

This module provides helper functions for the Battleship game, including:
    - Board visualization
    - Coordinate formatting
    - Game status checking
"""

from typing import Dict, Any, List, Tuple, Optional
from .models import Coordinates, PlayerBoard, ShipType
def visualize_board(board: Dict[str, Any], is_opponent: bool = False) -> str:
    """
    Create a string representation of the Battleship board.
    
    Args:
        board: Dictionary containing board information
        is_opponent: Whether this is the opponent's board
    
    Returns:
        String representation of the board
    """
    # Initialize empty 10x10 board
    grid = [['🟦' for _ in range(10)] for _ in range(10)]
    
    # Mark ship positions
    if board and 'ships' in board:
        for ship in board.get('ships', []):
            ship_type_to_emoji = {
                'Carrier': '⛵',      # Carrier
                'Battleship': '🚢',   # Battleship 
                'Cruiser': '⛴️',      # Cruiser
                'Submarine': '🛥️',    # Submarine
                'Destroyer': '🚤'     # Destroyer
            }
            
            # Always show both players' ships if board is being displayed
            for coord in ship.get('coordinates', []):
                row, col = coord['row'], coord['col']
                grid[row][col] = ship_type_to_emoji.get(ship.get('ship_type'), '🚢')
    
    # Convert grid to string representation
    board_str = "    0 1 2 3 4 5 6 7 8 9\n"
    board_str += "   +-----------------------------\n"
    
    for row_idx, row in enumerate(grid):
        board_str += f"{row_idx} | {' '.join(row)}\n"
    
    return board_str

def format_coordinates_list(coords_list: List[Dict[str, int]]) -> str:
    """
    Format a list of coordinates for display.
    
    Args:
        coords_list: List of coordinate dictionaries
        
    Returns:
        Formatted string of coordinates
    """
    if not coords_list:
        return "None"
    
    formatted = []
    for coord in coords_list:
        if isinstance(coord, dict) and "row" in coord and "col" in coord:
            formatted.append(f"({coord['row']}, {coord['col']})")
    
    return ", ".join(formatted)

def format_ship_types(ship_types: List[str]) -> str:
    """
    Format a list of ship types for display.
    
    Args:
        ship_types: List of ship type strings
        
    Returns:
        Formatted string of ship types
    """
    if not ship_types:
        return "None"
    
    return ", ".join(ship_types)

def calculate_game_stats(move_history: List[Tuple[str, Dict[str, Any]]]) -> Dict[str, Any]:
    """
    Calculate game statistics from move history.
    
    Args:
        move_history: List of (player, outcome) tuples
        
    Returns:
        Dictionary of game statistics
    """
    total_moves = len(move_history)
    player1_moves = sum(1 for player, _ in move_history if player == "player1")
    player2_moves = sum(1 for player, _ in move_history if player == "player2")
    
    player1_hits = sum(1 for player, outcome in move_history if player == "player1" and outcome["result"] in ["hit", "sunk"])
    player2_hits = sum(1 for player, outcome in move_history if player == "player2" and outcome["result"] in ["hit", "sunk"])
    
    player1_misses = sum(1 for player, outcome in move_history if player == "player1" and outcome["result"] == "miss")
    player2_misses = sum(1 for player, outcome in move_history if player == "player2" and outcome["result"] == "miss")
    
    player1_sunk = sum(1 for player, outcome in move_history if player == "player1" and outcome["result"] == "sunk")
    player2_sunk = sum(1 for player, outcome in move_history if player == "player2" and outcome["result"] == "sunk")
    
    return {
        "total_moves": total_moves,
        "player1_moves": player1_moves,
        "player2_moves": player2_moves,
        "player1_hits": player1_hits,
        "player2_hits": player2_hits,
        "player1_misses": player1_misses,
        "player2_misses": player2_misses,
        "player1_sunk": player1_sunk,
        "player2_sunk": player2_sunk,
        "player1_accuracy": round(player1_hits / player1_moves * 100, 1) if player1_moves > 0 else 0,
        "player2_accuracy": round(player2_hits / player2_moves * 100, 1) if player2_moves > 0 else 0
    }

def check_all_ships_placed(ship_placements: List[Dict[str, Any]]) -> Tuple[bool, Optional[str]]:
    """
    Check if all required ships have been placed.
    
    Args:
        ship_placements: List of ship placement dictionaries
        
    Returns:
        Tuple of (is_complete, error_message)
    """
    required_ships = set([t.value for t in ShipType])
    placed_ships = set([p.get("ship_type") for p in ship_placements])
    
    if placed_ships == required_ships:
        return True, None
    
    missing_ships = required_ships - placed_ships
    if missing_ships:
        return False, f"Missing ships: {', '.join(missing_ships)}"
    
    duplicate_ships = []
    seen_ships = set()
    for ship in [p.get("ship_type") for p in ship_placements]:
        if ship in seen_ships:
            duplicate_ships.append(ship)
        seen_ships.add(ship)
    
    if duplicate_ships:
        return False, f"Duplicate ships: {', '.join(set(duplicate_ships))}"
    
    return False, "Unknown error in ship placements"