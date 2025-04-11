"""
Chess agent implementation using LangGraph.

This module provides the agent implementation for the chess game,
including the workflow graph, action handlers, and LLM integration.
"""

from typing import Dict, Any, List, Optional, Tuple, Literal, Union
from pydantic import BaseModel, Field
import copy
import time
import os
import json
import chess
from langgraph.graph import StateGraph, END
from langgraph.types import Command
from langchain_core.runnables import Runnable
from src.haive.core.engine.agent.agent import register_agent, Agent

from src.haive.games.chess.models import ChessMoveModel, SegmentedAnalysis
from src.haive.games.chess.state import ChessState
from src.haive.games.chess.config import ChessAgentConfig
from src.haive.games.chess.utils import determine_game_status

@register_agent(ChessAgentConfig)
class ChessAgent(Agent[ChessAgentConfig]):
    """
    Chess agent implementation using LangGraph.
    
    This agent manages a chess game between two AI players, including:
        - Game state tracking with FEN notation
        - Move validation and execution
        - Position analysis (optional)
        - Game status checking
        - Turn management
    
    Attributes:
        config (ChessAgentConfig): Configuration for the chess agent
        engines (Dict[str, Runnable]): Dictionary of LLM engines for players and analyzers
    """
    
    def __init__(self, config: ChessAgentConfig):
        """Initialize the chess agent."""
        super().__init__(config)
        self.engines = {}
        
        # Ensure engines are properly set up
        for key, engine_config in config.engines.items():
            self.engines[key] = engine_config.create_runnable()
            
            if self.engines[key] is None:
                raise ValueError(f"Failed to create engine for {key}")
    
    def setup_workflow(self):
        """
        Set up the workflow graph for the chess game.
        
        This method:
            1. Adds nodes for game actions (initialize, move, analyze)
            2. Connects nodes with edges based on game flow
            3. Handles conditional routing based on game status
            4. Configures optional analysis nodes
        """
        # Add core nodes
        self.graph.add_node("initialize_game", self.initialize_game)
        self.graph.add_node("white_move", self.make_white_move)
        self.graph.add_node("black_move", self.make_black_move)
        self.graph.add_node("check_game_status", self.check_game_status)
        
        # Set up entry point
        self.graph.set_entry_point("initialize_game")
        
        # Add analysis nodes if enabled
        if self.config.enable_analysis:
            # Use different node names to avoid collision with state keys
            self.graph.add_node("analyze_for_white", self.analyze_white_position)
            self.graph.add_node("analyze_for_black", self.analyze_black_position)
            
            # Connect nodes with analysis
            self.graph.add_edge("initialize_game", "analyze_for_white")
            self.graph.add_edge("analyze_for_white", "white_move")
            self.graph.add_edge("white_move", "check_game_status")
            
            # Add conditional edges from check_game_status
            self.graph.add_conditional_edges(
                "check_game_status",
                self.route_next_step,
                {
                    "continue_white": "analyze_for_white",
                    "continue_black": "analyze_for_black",
                    "game_over": END
                }
            )
            
            self.graph.add_edge("analyze_for_black", "black_move")
            self.graph.add_edge("black_move", "check_game_status")
        else:
            # Connect nodes without analysis
            self.graph.add_edge("initialize_game", "white_move")
            self.graph.add_edge("white_move", "check_game_status")
            
            # Add conditional edges from check_game_status
            self.graph.add_conditional_edges(
                "check_game_status",
                self.route_next_step,
                {
                    "continue_white": "white_move",
                    "continue_black": "black_move",
                    "game_over": END
                }
            )
            
            self.graph.add_edge("black_move", "check_game_status")
    
    def initialize_game(self, state: Optional[ChessState] = None) -> Dict[str, Any]:
        """
        Initialize a new chess game.
        
        Args:
            state: Current state (ignored for initialization)
            
        Returns:
            New game state with initial board position
        """
        print("♟️ Initializing chess game...")
        
        # Create a new chess board with starting position
        board = chess.Board()
        
        # Create initial state
        new_state = ChessState(
            board_fens=[board.fen()],
            current_player="white",
            turn="white",
            move_history=[],
            game_status="ongoing",
            white_analysis=[],
            black_analysis=[],
            captured_pieces={"white": [], "black": []},
            error_message=None
        )
        
        return new_state.model_dump()
    
    def make_move(self, state: Dict[str, Any], color: str) -> Command:
        """
        Make a move for the specified player.
        
        Args:
            state: Current game state
            color: Player color ("white" or "black")
            
        Returns:
            Command with updated state or error message
        """
        print(f"\n🎲 {color.capitalize()}'s turn to move")
        
        # Handle both dict and ChessState inputs
        if isinstance(state, ChessState):
            state_obj = state
        else:
            state_obj = ChessState(**state)
        
        # Get the engine for this player
        player_engine = self.engines.get(f"{color}_player")
        if not player_engine:
            error_msg = f"Missing engine for {color}_player"
            print(f"❌ {error_msg}")
            return Command(update={"error_message": error_msg})
        
        try:
            # Prepare context for the LLM
            context = {
                "color": color,
                "current_board_fen": state_obj.board_fen,
                "previous_board_fen": state_obj.board_fens[-2] if len(state_obj.board_fens) > 1 else None,
                "recent_moves": state_obj.move_history[-5:] if state_obj.move_history else [],
                "captured_pieces": state_obj.captured_pieces,
                "player_analysis": (
                    state_obj.white_analysis[-1] if color == "white" and state_obj.white_analysis else None,
                    state_obj.black_analysis[-1] if color == "black" and state_obj.black_analysis else None
                )[0]
            }
            
            # Get move from LLM
            player_decision = player_engine.invoke(context)
            
            # Extract and validate the move
            if hasattr(player_decision, "selected_move") and hasattr(player_decision.selected_move, "move"):
                move_uci = player_decision.selected_move.move
            else:
                # Try to extract from dictionary format
                move_uci = player_decision.get("selected_move", {}).get("move", None)
                if not move_uci:
                    raise ValueError("Invalid move format returned by LLM")
            
            print(f"🎯 {color.capitalize()} suggests move: {move_uci}")
            
            # Convert to chess.Move and validate
            board = chess.Board(state_obj.board_fen)
            try:
                move = chess.Move.from_uci(move_uci)
            except ValueError:
                raise ValueError(f"Invalid UCI format: {move_uci}")
            
            # Check if move is legal
            if move not in board.legal_moves:
                # Get legal moves for debugging
                legal_moves = [m.uci() for m in board.legal_moves]
                print(f"❌ Illegal move! Legal moves are: {legal_moves}")
                
                # Try to make a random legal move as fallback
                if board.legal_moves:
                    move = list(board.legal_moves)[0]  # Take first legal move
                    print(f"⚠️ Fallback to legal move: {move.uci()}")
                else:
                    raise ValueError("No legal moves available")
            
            # Track captured piece if any
            captured = None
            captured_piece_type = board.piece_at(move.to_square)
            if captured_piece_type and board.is_capture(move):
                captured = captured_piece_type.symbol()
            
            # Apply the move
            board.push(move)
            
            # Update captured pieces if a piece was captured
            updated_captured = copy.deepcopy(state_obj.captured_pieces)
            if captured:
                opponent = "black" if color == "white" else "white"
                updated_captured[color].append(captured)
                print(f"💥 Captured {opponent}'s {captured}")
            
            # Determine new game status
            new_status = determine_game_status(board)
            print(f"📊 New game status: {new_status}")
            
            # Update state
            next_player = "black" if color == "white" else "white"
            
            return Command(update={
                "board_fens": state_obj.board_fens + [board.fen()],
                "move_history": state_obj.move_history + [(color, move.uci())],
                "current_player": next_player,
                "turn": next_player,
                "game_status": new_status,
                "captured_pieces": updated_captured,
                "error_message": None
            })
            
        except Exception as e:
            error_msg = f"Error making move for {color}: {str(e)}"
            print(f"❌ {error_msg}")
            return Command(update={"error_message": error_msg})
    
    def make_white_move(self, state: Dict[str, Any]) -> Command:
        """Make a move for the white player."""
        return self.make_move(state, "white")
    
    def make_black_move(self, state: Dict[str, Any]) -> Command:
        """Make a move for the black player."""
        return self.make_move(state, "black")
    
    def analyze_position(self, state: Dict[str, Any], color: str) -> Command:
        """
        Analyze the board position for the specified player.
        
        Args:
            state: Current game state
            color: Player color ("white" or "black")
            
        Returns:
            Command with updated analysis
        """
        print(f"\n🧠 Analyzing position for {color}")
        
        # Handle both dict and ChessState inputs
        if isinstance(state, ChessState):
            state_obj = state
        else:
            state_obj = ChessState(**state)
        
        # Get the engine for this analysis
        analyzer_engine = self.engines.get(f"{color}_analyzer")
        if not analyzer_engine:
            error_msg = f"Missing engine for {color}_analyzer"
            print(f"❌ {error_msg}")
            return Command(update={"error_message": error_msg})
        
        try:
            # Prepare context for the LLM
            context = {
                "color": color,
                "current_board_fen": state_obj.board_fen,
                "previous_board_fen": state_obj.board_fens[-2] if len(state_obj.board_fens) > 1 else None,
                "recent_moves": state_obj.move_history[-5:] if state_obj.move_history else [],
                "captured_pieces": state_obj.captured_pieces
            }
            
            # Get analysis from LLM
            analysis_result = analyzer_engine.invoke(context)
            
            # Convert analysis to dictionary if needed
            if hasattr(analysis_result, "model_dump"):
                analysis_dict = analysis_result.model_dump()
            elif hasattr(analysis_result, "dict"):
                analysis_dict = analysis_result.dict()
            else:
                analysis_dict = dict(analysis_result)
            
            print(f"📝 Analysis completed for {color}")
            
            # Update the appropriate analysis field
            if color == "white":
                white_analysis = state_obj.white_analysis + [analysis_dict]
                return Command(update={"white_analysis": white_analysis[-5:]})  # Keep last 5
            else:
                black_analysis = state_obj.black_analysis + [analysis_dict]
                return Command(update={"black_analysis": black_analysis[-5:]})  # Keep last 5
                
        except Exception as e:
            error_msg = f"Error analyzing position for {color}: {str(e)}"
            print(f"❌ {error_msg}")
            return Command(update={"error_message": error_msg})
    
    def analyze_white_position(self, state: Dict[str, Any]) -> Command:
        """Analyze the board position for the white player."""
        return self.analyze_position(state, "white")
    
    def analyze_black_position(self, state: Dict[str, Any]) -> Command:
        """Analyze the board position for the black player."""
        return self.analyze_position(state, "black")
    
    def check_game_status(self, state: Dict[str, Any]) -> Command:
        """
        Check and update the game status.
        
        Args:
            state: Current game state
            
        Returns:
            Command with updated game status
        """
        # Handle both dict and ChessState inputs
        if isinstance(state, ChessState):
            state_obj = state
        else:
            state_obj = ChessState(**state)
            
        board = chess.Board(state_obj.board_fen)
        
        # Check for game end conditions
        game_status = determine_game_status(board)
        
        # Check for max moves
        move_count = len(state_obj.move_history)
        if move_count >= self.config.max_moves:
            game_status = "draw"
            print(f"🕑 Game drawn by move limit ({self.config.max_moves} moves)")
        
        # Check for special draw conditions
        if game_status == "ongoing" and board.is_insufficient_material():
            game_status = "draw"
            print("🤝 Game drawn by insufficient material")
        
        # Update the game result if needed
        game_result = None
        if game_status in ["checkmate", "stalemate", "draw"]:
            if game_status == "checkmate":
                winner = "black" if state_obj.current_player == "white" else "white"
                game_result = f"{winner}_win"
                print(f"🏆 Checkmate! {winner.capitalize()} wins")
            else:
                game_result = "draw"
                print("🤝 Game drawn")
        
        return Command(update={
            "game_status": game_status,
            "game_result": game_result
        })
    
    def route_next_step(self, state: Dict[str, Any]) -> str:
        """
        Determine the next step in the workflow.
        
        Args:
            state: Current game state
            
        Returns:
            Next node to route to
        """
        # Handle both dict and ChessState inputs
        if isinstance(state, ChessState):
            state_obj = state
        else:
            state_obj = ChessState(**state)
        
        # Check if game is over
        if state_obj.game_status in ["checkmate", "stalemate", "draw"] or state_obj.game_result:
            return "game_over"
        
        # Route to appropriate player's turn
        if state_obj.current_player == "white":
            return "continue_white"
        else:
            return "continue_black"