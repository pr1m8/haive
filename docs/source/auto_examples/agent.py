"""Chess agent implementation using LangGraph.

This module provides a chess agent implementation using LangGraph, featuring:
    - LLM-powered chess players
    - Position analysis
    - Game state management
    - Workflow graph for turn-based gameplay
    - Error handling and retry logic

The agent orchestrates the game flow between two LLM players and handles
all game mechanics including move validation, position analysis, and
game status tracking.
"""

import copy

import chess
from haive.core.engine.agent.agent import Agent, register_agent
from langgraph.graph import END, StateGraph
from langgraph.types import Command

from haive.games.chess.config import ChessConfig
from haive.games.chess.state import ChessState
from haive.games.chess.utils import determine_game_status


@register_agent(ChessConfig)
class ChessAgent(Agent[ChessConfig]):
    """Chess agent implementation using LangGraph.

    This agent implements a complete chess game using language models for
    move generation and position analysis. It uses LangGraph to create a
    workflow graph that manages the game flow between players.

    Features:
        - LLM-powered chess players with structured outputs
        - Optional position analysis for enhanced play
        - Move validation and retry logic
        - Game status tracking and termination
        - Error handling and fallback moves

    Attributes:
        config (ChessConfig): Configuration for the chess agent
        engines (Dict[str, Any]): LLM engines for players and analyzers
        graph (StateGraph): LangGraph workflow for the chess game
    """

    def __init__(self, config: ChessConfig):
        """Initialize the chess agent.

        Args:
            config (ChessConfig): Configuration for the chess agent,
                including LLM engine settings, analysis options, and
                game parameters.
        """
        super().__init__(config)
        self.engines = {}

        # Ensure engines are properly set up
        for key, engine_config in config.engines.items():
            self.engines[key] = engine_config

    def setup_workflow(self) -> None:
        """Set up the workflow graph for the chess game.

        Creates a LangGraph StateGraph with nodes for:
            - White player's moves
            - Black player's moves
            - Game status checking
            - Optional position analysis

        The graph flow depends on the current player and game status,
        with conditional edges for routing between nodes.
        """
        # Build the graph using StateGraph
        builder = StateGraph(ChessState)

        # Add core nodes
        builder.add_node("white_move", self.make_white_move)
        builder.add_node("black_move", self.make_black_move)
        builder.add_node("check_game_status", self.check_game_status)

        # Add analysis nodes if enabled
        if self.config.enable_analysis:
            builder.add_node("analyze_for_white", self.analyze_white_position)
            builder.add_node("analyze_for_black", self.analyze_black_position)

            # Set entry point to white analysis
            builder.set_entry_point("analyze_for_white")

            # With analysis flow
            builder.add_edge("analyze_for_white", "white_move")
            builder.add_edge("white_move", "check_game_status")
            builder.add_edge("analyze_for_black", "black_move")
            builder.add_edge("black_move", "check_game_status")
        else:
            # Without analysis flow
            builder.set_entry_point("white_move")
            builder.add_edge("white_move", "check_game_status")
            builder.add_edge("black_move", "check_game_status")

        # Add conditional routing from check_game_status
        builder.add_conditional_edges(
            "check_game_status",
            self.route_next_step,
            {
                "continue_white": (
                    "analyze_for_white" if self.config.enable_analysis else "white_move"
                ),
                "continue_black": (
                    "analyze_for_black" if self.config.enable_analysis else "black_move"
                ),
                "game_over": END,
            },
        )

        # Compile the graph
        self.graph = builder
        # Compile the graph without recursion_limit,
        # which will be applied in the runtime config
        self._app = builder.compile()

    def make_move(self, state: ChessState, color: str) -> Command:
        """Make a move for the specified player with retry logic.

        This method handles the complete move generation process:
            1. Gets legal moves from the current position
            2. Sends context to the appropriate LLM engine
            3. Validates the returned move
            4. Updates the game state with the new move

        Includes retry logic for invalid moves, with fallback to a safe
        move if all attempts fail.

        Args:
            state (ChessState): Current game state
            color (str): Player color ("white" or "black")

        Returns:
            Command: LangGraph command with state updates

        Examples:
            >>> command = agent.make_move(state, "white")
            >>> command.update  # Contains the updated game state
            {'board_fens': [...], 'move_history': [...], ...}
        """
        print(f"\n🎲 {color.capitalize()}'s turn to move")

        # Get the engine for this player
        player_engine = self.engines.get(f"{color}_player")
        if not player_engine:
            error_msg = f"Missing engine for {color}_player"
            print(f"❌ {error_msg}")
            return Command(update={"error_message": error_msg})

        # Retry logic
        max_attempts = 3
        previous_errors = []

        for attempt in range(1, max_attempts + 1):
            try:
                # Create board for legal moves
                board = chess.Board(state.board_fen)

                # Get all legal moves in UCI format
                legal_moves = [move.uci() for move in board.legal_moves]

                # Format legal moves for display
                if len(legal_moves) > 30:
                    legal_moves_display = legal_moves[:30]
                    legal_moves_str = (
                        ", ".join(legal_moves_display)
                        + f"\n... and {len(legal_moves) - 30} more moves"
                    )
                else:
                    legal_moves_str = ", ".join(legal_moves)

                # Add examples of legal moves
                example_moves = []
                if legal_moves:
                    for move in legal_moves[:5]:
                        try:
                            chess_move = chess.Move.from_uci(move)
                            from_sq = chess.square_name(chess_move.from_square)
                            to_sq = chess.square_name(chess_move.to_square)
                            piece = board.piece_at(chess_move.from_square)
                            if piece:
                                piece_name = {
                                    chess.PAWN: "pawn",
                                    chess.KNIGHT: "knight",
                                    chess.BISHOP: "bishop",
                                    chess.ROOK: "rook",
                                    chess.QUEEN: "queen",
                                    chess.KING: "king",
                                }.get(piece.piece_type, "piece")
                                example_moves.append(
                                    f"{move} ({piece_name} from {from_sq} to {to_sq})"
                                )
                        except (ValueError, AttributeError):
                            example_moves.append(move)

                # Build error context for retry attempts
                error_context = ""
                if previous_errors and attempt > 1:
                    error_context = "\n⚠️ PREVIOUS ATTEMPT ERRORS:\n"
                    for i, err in enumerate(previous_errors, 1):
                        error_context += f"Attempt {i}: {err}\n"
                    error_context += (
                        f"\nThis is attempt {attempt} of {max_attempts}. "
                        "Please select a DIFFERENT legal move from the list below.\n"
                    )

                # Format recent moves
                recent_moves_formatted = []
                for i, (player, move) in enumerate(state.move_history[-5:]):
                    move_num = len(state.move_history) - 5 + i + 1
                    recent_moves_formatted.append(f"{move_num}. {player}: {move}")
                recent_moves_str = (
                    ", ".join(recent_moves_formatted)
                    if recent_moves_formatted
                    else "Game just started"
                )

                # Format captured pieces
                captured_str = {
                    "white": ", ".join(state.captured_pieces["white"]) or "none",
                    "black": ", ".join(state.captured_pieces["black"]) or "none",
                }

                # Prepare context with examples
                if example_moves:
                    legal_moves_with_examples = (
                        f"Example moves: {', '.join(example_moves[:3])}\n\n"
                        f"All legal moves:\n{legal_moves_str}"
                    )
                else:
                    legal_moves_with_examples = legal_moves_str

                context = {
                    "current_board_fen": state.board_fen,
                    "recent_moves": recent_moves_str,
                    "captured_pieces": captured_str,
                    "legal_moves": legal_moves_with_examples,
                    "error_context": error_context,
                }

                print(
                    f"📋 Attempt {attempt}/{max_attempts}: "
                    f"{color.capitalize()} has {len(legal_moves)} legal moves"
                )
                if previous_errors:
                    print(f"⚠️ Previous errors: {previous_errors[-1]}")

                # Get move from LLM
                player_decision = player_engine.invoke(context)

                # Extract move from structured output
                move_uci = None
                if hasattr(player_decision, "selected_move") and hasattr(
                    player_decision.selected_move, "move"
                ):
                    move_uci = player_decision.selected_move.move
                elif (
                    isinstance(player_decision, dict)
                    and "selected_move" in player_decision
                ):
                    selected = player_decision["selected_move"]
                    if isinstance(selected, dict):
                        move_uci = selected.get("move")
                    elif hasattr(selected, "move"):
                        move_uci = selected.move

                if not move_uci:
                    raise ValueError(
                        "Invalid move format returned by LLM - "
                        "no move found in response"
                    )

                print(f"🎯 {color.capitalize()} selected: {move_uci}")

                # Validate move is legal
                if move_uci not in legal_moves:
                    error_msg = (
                        f"Move '{move_uci}' is not in the legal moves list. "
                        f"Please select from: {', '.join(legal_moves[:10])}..."
                    )
                    previous_errors.append(error_msg)

                    if attempt < max_attempts:
                        print(f"❌ Invalid move: {move_uci}")
                        continue
                    # Last attempt failed, use first legal move
                    print(
                        f"❌ Invalid move after {max_attempts} attempts! "
                        "Using first legal move."
                    )
                    move_uci = legal_moves[0]
                    print(f"🔄 Auto-selected: {move_uci}")

                # Apply the move
                move = chess.Move.from_uci(move_uci)

                # Check for captures
                captured = None
                if board.is_capture(move):
                    captured_piece = board.piece_at(move.to_square)
                    if captured_piece:
                        captured = captured_piece.symbol()

                # Apply the move
                board.push(move)

                # Update captured pieces if needed
                updated_captured = copy.deepcopy(state.captured_pieces)
                if captured:
                    opponent = "black" if color == "white" else "white"
                    updated_captured[color].append(captured)
                    print(f"💥 Captured {opponent}'s {captured}")

                # Determine new game status
                new_status = determine_game_status(board)
                print(f"📊 Game status: {new_status}")

                next_player = "black" if color == "white" else "white"

                return Command(
                    update={
                        "board_fens": state.board_fens + [board.fen()],
                        "move_history": state.move_history + [(color, move_uci)],
                        "current_player": next_player,
                        "turn": next_player,
                        "game_status": new_status,
                        "captured_pieces": updated_captured,
                        "error_message": None,
                    }
                )

            except Exception as e:
                error_msg = f"Error making move for {color}: {e!s}"
                previous_errors.append(str(e))
                print(f"❌ Attempt {attempt} failed: {e}")

                if attempt >= max_attempts:
                    # Final attempt failed, try to use a safe move
                    try:
                        board = chess.Board(state.board_fen)
                        legal_moves = [move.uci() for move in board.legal_moves]
                        if legal_moves:
                            safe_move = legal_moves[0]
                            print(f"🔄 Using safe fallback move: {safe_move}")

                            move = chess.Move.from_uci(safe_move)
                            board.push(move)

                            return Command(
                                update={
                                    "board_fens": state.board_fens + [board.fen()],
                                    "move_history": state.move_history
                                    + [(color, safe_move)],
                                    "current_player": (
                                        "black" if color == "white" else "white"
                                    ),
                                    "turn": "black" if color == "white" else "white",
                                    "game_status": determine_game_status(board),
                                    "error_message": (
                                        f"Used fallback move after errors: "
                                        f"{', '.join(previous_errors)}"
                                    ),
                                }
                            )
                    except (ValueError, AttributeError):
                        pass

                    return Command(update={"error_message": error_msg})

    def make_white_move(self, state: ChessState) -> Command:
        """Make a move for the white player.

        Args:
            state (ChessState): Current game state

        Returns:
            Command: LangGraph command with state updates
        """
        return self.make_move(state, "white")

    def make_black_move(self, state: ChessState) -> Command:
        """Make a move for the black player.

        Args:
            state (ChessState): Current game state

        Returns:
            Command: LangGraph command with state updates
        """
        return self.make_move(state, "black")

    def analyze_position(self, state: ChessState, color: str) -> Command:
        """Analyze the board position for the specified player.

        This method uses the configured analyzer engine to generate
        a detailed position analysis from the perspective of the
        given player color.

        Args:
            state (ChessState): Current game state
            color (str): Player color ("white" or "black")

        Returns:
            Command: LangGraph command with analysis updates

        Note:
            Analysis results are stored in the state's white_analysis
            or black_analysis fields, depending on the color.
        """
        print(f"\n🧠 Analyzing position for {color}")

        # Get the engine for this analysis
        analyzer_engine = self.engines.get(f"{color}_analyzer")
        if not analyzer_engine:
            error_msg = f"Missing engine for {color}_analyzer"
            print(f"❌ {error_msg}")
            return Command(update={"error_message": error_msg})

        try:
            # Prepare context for the LLM
            context = {
                "current_board_fen": state.board_fen,
                "recent_moves": state.move_history[-5:] if state.move_history else [],
                "captured_pieces": state.captured_pieces,
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
                white_analysis = state.white_analysis + [analysis_dict]
                return Command(update={"white_analysis": white_analysis[-5:]})
            black_analysis = state.black_analysis + [analysis_dict]
            return Command(update={"black_analysis": black_analysis[-5:]})

        except Exception as e:
            error_msg = f"Error analyzing position for {color}: {e!s}"
            print(f"❌ {error_msg}")
            return Command(update={"error_message": error_msg})

    def analyze_white_position(self, state: ChessState) -> Command:
        """Analyze the board position for the white player.

        Args:
            state (ChessState): Current game state

        Returns:
            Command: LangGraph command with white analysis updates
        """
        return self.analyze_position(state, "white")

    def analyze_black_position(self, state: ChessState) -> Command:
        """Analyze the board position for the black player.

        Args:
            state (ChessState): Current game state

        Returns:
            Command: LangGraph command with black analysis updates
        """
        return self.analyze_position(state, "black")

    def check_game_status(self, state: ChessState) -> Command:
        """Check and update the game status.

        This method evaluates the current board position to determine
        if the game has ended (checkmate, stalemate, draw) or if it
        should continue.

        Game-ending conditions include:
        - Checkmate
        - Stalemate
        - Insufficient material
        - Maximum move limit reached

        Args:
            state (ChessState): Current game state

        Returns:
            Command: LangGraph command with game status updates
        """
        board = chess.Board(state.board_fen)

        # Check for game end conditions
        game_status = determine_game_status(board)

        # Check for max moves
        move_count = len(state.move_history)
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
                winner = "black" if state.current_player == "white" else "white"
                game_result = f"{winner}_win"
                print(f"🏆 Checkmate! {winner.capitalize()} wins")
            else:
                game_result = "draw"
                print("🤝 Game drawn")

        return Command(update={"game_status": game_status, "game_result": game_result})

    def route_next_step(self, state: ChessState) -> str:
        """Determine the next step in the workflow.

        This conditional router decides where to direct the flow next
        based on the current game state:
        - If the game is over, route to the end
        - Otherwise, route to the next player's turn

        Args:
            state (ChessState): Current game state

        Returns:
            str: The next step key for the workflow graph

        Note:
            Return values correspond to the keys in the conditional
            edges of the graph: "game_over", "continue_white", or
            "continue_black".
        """
        # Check if game is over
        if state.game_status in ["checkmate", "stalemate", "draw"] or state.game_result:
            return "game_over"

        # Route to appropriate player's turn
        if state.current_player == "white":
            return "continue_white"
        return "continue_black"
