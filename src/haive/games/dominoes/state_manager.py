# src/haive/agents/agent_games/dominoes/state.py

import random
from typing import List, Optional, Dict, Tuple, Union, Literal
import copy
from src.haive.games.dominoes.models import DominoesState, DominoTile, DominoMove

from src.haive.games.framework.base import GameStateManager

class DominoesStateManager(GameStateManager[DominoesState]):
    """Manager for dominoes game state."""
    
    @classmethod
    def initialize(cls, player_names: List[str] = ["player1", "player2"], tiles_per_hand: int = 7) -> DominoesState:
        """Initialize a new dominoes game."""
        # Create all tiles from 0-0 to 6-6
        all_tiles = []
        for i in range(7):
            for j in range(i + 1):
                all_tiles.append(DominoTile(left=i, right=j))
        
        # Shuffle the tiles
        random.shuffle(all_tiles)
        
        # Deal tiles to players
        hands = {}
        for player in player_names:
            hands[player] = all_tiles[:tiles_per_hand]
            all_tiles = all_tiles[tiles_per_hand:]
        
        # Rest of tiles go to the boneyard
        boneyard = all_tiles
        
        # Determine who goes first
        # Traditional rule: player with highest double goes first
        first_player = player_names[0]  # Default
        highest_double = -1
        
        for player in player_names:
            for tile in hands[player]:
                if tile.is_double() and tile.left > highest_double:
                    highest_double = tile.left
                    first_player = player
        
        # If no doubles, player with highest tile goes first
        if highest_double == -1:
            highest_sum = -1
            for player in player_names:
                for tile in hands[player]:
                    tile_sum = tile.sum()
                    if tile_sum > highest_sum:
                        highest_sum = tile_sum
                        first_player = player
        
        # Create the initial state
        return DominoesState(
            players=player_names,
            hands=hands,
            board=[],
            boneyard=boneyard,
            turn=first_player,
            game_status="ongoing",
            move_history=[],
            last_passes=0,
            scores={player: 0 for player in player_names}
        )
    
    @classmethod
    def apply_move(cls, state: DominoesState, move: Union[DominoMove, Literal["pass"]]) -> DominoesState:
        """Apply a move to the dominoes state."""
        # Create a deep copy of the state to avoid modifying the original
        new_state = copy.deepcopy(state)
        
        # Handle passing
        if move == "pass":
            # Check if there are tiles in the boneyard
            if new_state.boneyard:
                # Draw a tile
                drawn_tile = new_state.boneyard.pop(0)
                new_state.hands[new_state.turn].append(drawn_tile)
                new_state.last_passes = 0  # Reset consecutive passes
            else:
                # No tiles to draw, count as a pass
                new_state.last_passes += 1
            
            # Switch turns
            current_idx = new_state.players.index(new_state.turn)
            next_idx = (current_idx + 1) % len(new_state.players)
            new_state.turn = new_state.players[next_idx]
            
            # Update move history
            new_state.move_history.append("pass")
            
            # Check game status
            new_state = cls.check_game_status(new_state)
            
            return new_state
        
        # Handle playing a tile
        tile = move.tile
        location = move.location
        player = new_state.turn
        
        # Check if the player has the tile
        player_hand = new_state.hands[player]
        matching_tiles = [t for t in player_hand if (t.left == tile.left and t.right == tile.right) or 
                                                  (t.left == tile.right and t.right == tile.left)]
        if not matching_tiles:
            raise ValueError(f"Player {player} doesn't have tile {tile}")
        
        # Remove the tile from the player's hand
        for i, hand_tile in enumerate(player_hand):
            if (hand_tile.left == tile.left and hand_tile.right == tile.right) or \
               (hand_tile.left == tile.right and hand_tile.right == tile.left):
                new_state.hands[player].pop(i)
                break
        
        # Place the tile on the board
        if not new_state.board:
            # First tile
            new_state.board.append(tile)
        else:
            if location == "left":
                # Check if the tile matches the left end
                left_val = new_state.left_value
                if tile.right == left_val:
                    new_state.board.insert(0, tile)
                elif tile.left == left_val:
                    new_state.board.insert(0, tile.reversed())
                else:
                    raise ValueError(f"Tile {tile} doesn't match left end {left_val}")
            else:  # right
                # Check if the tile matches the right end
                right_val = new_state.right_value
                if tile.left == right_val:
                    new_state.board.append(tile)
                elif tile.right == right_val:
                    new_state.board.append(tile.reversed())
                else:
                    raise ValueError(f"Tile {tile} doesn't match right end {right_val}")
        
        # Reset consecutive passes
        new_state.last_passes = 0
        
        # Check if player won
        if not new_state.hands[player]:
            new_state.game_status = f"{player}_win"
            new_state.winner = player
            
            # Calculate score (sum of opponent's tiles)
            opponent_tiles = []
            for p in new_state.players:
                if p != player:
                    opponent_tiles.extend(new_state.hands[p])
            
            score = sum(tile.left + tile.right for tile in opponent_tiles)
            new_state.scores[player] += score
        else:
            # Switch turns
            current_idx = new_state.players.index(new_state.turn)
            next_idx = (current_idx + 1) % len(new_state.players)
            new_state.turn = new_state.players[next_idx]
        
        # Update move history
        new_state.move_history.append(move)
        
        # Check game status
        new_state = cls.check_game_status(new_state)
        
        return new_state
    
    @classmethod
    def check_game_status(cls, state: DominoesState) -> DominoesState:
        """Check and update the game status."""
        # Game already ended
        if state.game_status != "ongoing":
            return state
        
        # Check if any player has won
        for player in state.players:
            if not state.hands[player]:
                state.game_status = f"{player}_win"
                state.winner = player
                return state
        
        # Check for locked game (everyone passes)
        if state.last_passes >= len(state.players):
            # Game is locked, count points
            player_pips = {}
            for player in state.players:
                player_pips[player] = sum(tile.left + tile.right for tile in state.hands[player])
            
            # Player with least pips wins
            winner = min(player_pips.items(), key=lambda x: x[1])[0]
            
            # In case of a tie, it's a draw
            min_pips = player_pips[winner]
            if list(player_pips.values()).count(min_pips) > 1:
                state.game_status = "draw"
            else:
                state.game_status = f"{winner}_win"
                state.winner = winner
                
                # Calculate score (difference between winner's pips and sum of others)
                total_pips = sum(player_pips.values())
                winner_score = total_pips - player_pips[winner]
                state.scores[winner] += winner_score
        
        return state
    
    @classmethod
    def get_legal_moves(cls, state: DominoesState) -> List[Union[DominoMove, Literal["pass"]]]:
        """Get all legal moves for the current player."""
        moves = []
        player = state.turn
        
        # If the board is empty, any tile can be played
        if not state.board:
            for tile in state.hands[player]:
                moves.append(DominoMove(tile=tile, location="right"))  # Direction doesn't matter for first move
            return moves if moves else ["pass"]
        
        # Check for moves that match the left end
        left_val = state.left_value
        for tile in state.hands[player]:
            if tile.left == left_val:
                moves.append(DominoMove(tile=tile, location="left"))
            elif tile.right == left_val:
                moves.append(DominoMove(tile=tile, location="left"))
        
        # Check for moves that match the right end
        right_val = state.right_value
        for tile in state.hands[player]:
            if tile.left == right_val:
                moves.append(DominoMove(tile=tile, location="right"))
            elif tile.right == right_val:
                moves.append(DominoMove(tile=tile, location="right"))
        
        # If no legal moves, player must pass
        if not moves:
            return ["pass"]
        
        return moves