"""Chess game state manager module.

This module provides state management functionality for chess games, including:
    - Game state initialization
    - Move application and validation
    - Game status tracking
    - Captured pieces management

Example:
    >>> from src.haive.games.chess import ChessGameStateManager
    >>> 
    >>> # Initialize a new game state
    >>> state = ChessGameStateManager.initialize()
    >>> 
    >>> # Apply a move
    >>> new_state = ChessGameStateManager.apply_move(state, "e2e4")
"""

from typing import Dict, Any, Optional
from .state import ChessState


class ChessGameStateManager:
    """Chess game state manager.
    
    This class provides static methods for managing chess game states:
        - Game initialization with default settings
        - Move application with validation
        - Game status updates
        - Captured pieces tracking
    
    Example:
        >>> state = ChessGameStateManager.initialize()
        >>> print(state.board_fen)
        rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
    """

    @staticmethod
    def initialize() -> ChessState:
        """Initialize a new chess game state.
        
        This method:
            1. Creates a new chess board
            2. Sets up initial piece positions
            3. Configures starting player
            4. Initializes game status
        
        Returns:
            ChessGameState: A fresh game state with default settings.
        
        Example:
            >>> state = ChessGameStateManager.initialize()
            >>> assert state.turn == "white"
            >>> assert state.game_status == "ongoing"
        """
        import chess
        return ChessState(
            board_fen=chess.Board().fen(),
            turn="white",
            move_history=[],
            captured_pieces={},
            game_status="ongoing",
            analysis={},
            #current_player="white"
            #turn="white"
        )

    @staticmethod
    def apply_move(state: ChessState, move_uci: str) -> ChessState:
        """Apply a move to the current game state.
        
        This method:
            1. Validates the move format
            2. Updates the board position
            3. Tracks captured pieces
            4. Updates game status
            5. Switches the current player
        
        Args:
            state (ChessGameState): Current game state.
            move_uci (str): Move in UCI notation (e.g., "e2e4").
        
        Returns:
            ChessGameState: New game state after applying the move.
        
        Example:
            >>> state = ChessGameStateManager.initialize()
            >>> new_state = ChessGameStateManager.apply_move(state, "e2e4")
            >>> assert new_state.turn == "black"
        """
        import chess
        board = chess.Board(state.board_fen)
        move = chess.Move.from_uci(move_uci)
        
        # Track captured piece
        captured_piece = board.piece_at(move.to_square)
        
        # Apply move
        board.push(move)
        
        # Create new state
        new_state = ChessState(
            board_fen=board.fen(),
            move_history=state.move_history + [move_uci],
            captured_pieces=dict(state.captured_pieces),
            turn="black" if state.turn == "white" else "white",
            game_status=state.game_status,
            analysis=state.analysis
        )

        # Update game status
        if board.is_checkmate():
            new_state.game_status = "checkmate"
        elif board.is_stalemate():
            new_state.game_status = "stalemate"
        elif board.is_check():
            new_state.game_status = "check"
        
        # Track captured pieces
        if captured_piece:
            piece_symbol = captured_piece.symbol()
            new_state.captured_pieces[state.turn].append(piece_symbol)

        return new_state
