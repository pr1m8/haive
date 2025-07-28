"""Chess game UI using Rich for beautiful terminal display."""

import time

import chess
from rich.align import Align
from rich.box import ROUNDED, SIMPLE
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text

from haive.games.chess.agent import ChessAgent
from haive.games.chess.config import ChessAgentConfig
from haive.games.chess.state import ChessState


class ChessRichUI:
    """Beautiful Rich UI for displaying a live chess agent game."""

    def __init__(self):
        self.console = Console()
        self.layout = Layout()
        self.state: ChessState | None = None
        self.last_move: str | None = None
        self.move_count = 0
        self.start_time = time.time()
        self._setup_layout()

    def _setup_layout(self):
        """Initialize the layout structure."""
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="body", ratio=1),
            Layout(name="footer", size=4),
        )

        self.layout["body"].split_row(
            Layout(name="left_panel", ratio=1),
            Layout(name="main", ratio=2),
            Layout(name="right_panel", ratio=1),
        )

        self.layout["body"]["left_panel"].split(
            Layout(name="white_info", size=8),
            Layout(name="white_analysis", size=12),
            Layout(name="move_history"),
        )

        self.layout["body"]["main"].split(
            Layout(name="board", ratio=1),
            Layout(name="current_move", size=3),
        )

        self.layout["body"]["right_panel"].split(
            Layout(name="black_info", size=8),
            Layout(name="black_analysis", size=12),
            Layout(name="game_info"),
        )

    def render_header(self) -> Panel:
        """Render the header with title and game time."""
        elapsed = int(time.time() - self.start_time)
        minutes, seconds = divmod(elapsed, 60)

        header_text = Text()
        header_text.append("♔ ", style="bold white")
        header_text.append("AI Chess Arena", style="bold cyan")
        header_text.append(" ♚", style="bold black")
        header_text.append(f"\n⏱️  {minutes:02d}:{seconds:02d}", style="dim")

        return Panel(Align.center(header_text), border_style="cyan", box=ROUNDED)

    def render_footer(self) -> Panel:
        """Render the footer with controls and status."""
        if self.state and self.state.game_status != "ongoing":
            # Game over message
            result_text = Text()
            if self.state.game_result == "white_win":
                result_text.append("♔ WHITE WINS! ♔", style="bold green on black")
            elif self.state.game_result == "black_win":
                result_text.append("♚ BLACK WINS! ♚", style="bold red on black")
            else:
                result_text.append("🤝 DRAW! 🤝", style="bold yellow on black")

            return Panel(Align.center(result_text), border_style="yellow", box=ROUNDED)

        # Normal controls
        controls = Text()
        controls.append("Controls: ", style="dim")
        controls.append("Q", style="bold cyan")
        controls.append(" Quit  ", style="dim")
        controls.append("R", style="bold cyan")
        controls.append(" Restart  ", style="dim")
        controls.append("S", style="bold cyan")
        controls.append(" Save Game", style="dim")

        return Panel(Align.center(controls), border_style="dim", box=ROUNDED)

    def render_board(self) -> Panel:
        """Render the chess board with pieces."""
        if not self.state:
            # Loading state
            loading = Text()
            loading.append("♟️  ", style="blink")
            loading.append("Initializing board...", style="dim italic")
            return Panel(
                Align.center(loading, vertical="middle"),
                title="Chess Board",
                border_style="magenta",
                height=20,
            )

        try:
            board = chess.Board(self.state.board_fen)

            # Create board display
            board_text = Text()

            # Add rank numbers and pieces
            for rank in range(7, -1, -1):
                # Rank number
                board_text.append(f" {rank + 1} ", style="bold blue")

                # Squares
                for file in range(8):
                    square = chess.square(file, rank)
                    piece = board.piece_at(square)

                    # Determine square color
                    is_light = (rank + file) % 2 == 1
                    bg_color = "on grey85" if is_light else "on grey42"

                    # Check if this square is part of the last move
                    if self.last_move and len(self.last_move) >= 4:
                        try:
                            move = chess.Move.from_uci(self.last_move)
                            if square in [move.from_square, move.to_square]:
                                bg_color = "on yellow4" if is_light else "on yellow3"
                        except:
                            pass

                    if piece:
                        # Unicode chess pieces
                        piece_map = {
                            "K": "♔",
                            "Q": "♕",
                            "R": "♖",
                            "B": "♗",
                            "N": "♘",
                            "P": "♙",
                            "k": "♚",
                            "q": "♛",
                            "r": "♜",
                            "b": "♝",
                            "n": "♞",
                            "p": "♟",
                        }
                        piece_char = piece_map.get(piece.symbol(), piece.symbol())

                        # Piece color
                        if piece.color == chess.WHITE:
                            style = f"bold white {bg_color}"
                        else:
                            style = f"bold red {bg_color}"

                        board_text.append(f" {piece_char} ", style=style)
                    else:
                        # Empty square
                        board_text.append("   ", style=bg_color)

                board_text.append("\n")

            # File letters
            board_text.append("   ", style="")
            for file in "abcdefgh":
                board_text.append(f" {file} ", style="bold blue")

            return Panel(
                Align.center(board_text),
                title="♟️ Board Position ♟️",
                border_style="magenta",
                box=ROUNDED,
            )

        except Exception as e:
            return Panel(
                f"Error rendering board: {e}", title="Board", border_style="red"
            )

    def render_current_move(self) -> Panel:
        """Render the current move being made."""
        if not self.state:
            return Panel("", border_style="dim")

        current = self.state.current_player.upper()
        style = "bold green" if current == "WHITE" else "bold red"

        move_text = Text()
        move_text.append(f"{current} TO MOVE", style=style)

        if self.state.game_status == "check":
            move_text.append(" - CHECK!", style="bold yellow blink")

        return Panel(Align.center(move_text), border_style="cyan", box=SIMPLE)

    def render_player_info(self, color: str) -> Panel:
        """Render player information panel."""
        if not self.state:
            return Panel("", title=f"{color.title()}", border_style="dim")

        info = Table(show_header=False, box=None, padding=0)
        info.add_column(style="dim")
        info.add_column(style="bold")

        # Captured pieces
        captured = self.state.captured_pieces.get(color, [])
        if captured:
            piece_map = {
                "Q": "♕",
                "R": "♖",
                "B": "♗",
                "N": "♘",
                "P": "♙",
                "q": "♛",
                "r": "♜",
                "b": "♝",
                "n": "♞",
                "p": "♟",
            }
            captured_str = " ".join(piece_map.get(p, p) for p in captured)
        else:
            captured_str = "None"

        info.add_row("Captured:", captured_str)

        # Material count
        material = len([p for p in captured if p.upper() in "QRBN"])
        info.add_row("Material:", f"+{material}")

        style = "green" if color == "white" else "red"
        icon = "♔" if color == "white" else "♚"

        return Panel(
            info,
            title=f"{icon} {color.title()} Player",
            border_style=style,
            box=ROUNDED,
        )

    def render_analysis(self, color: str) -> Panel:
        """Render position analysis for a player."""
        if not self.state:
            return Panel(
                "No analysis yet", title=f"{color.title()} Analysis", border_style="dim"
            )

        analysis_list = getattr(self.state, f"{color}_analysis", [])
        if not analysis_list:
            return Panel(
                Text("Analyzing position...", style="dim italic"),
                title=f"{color.title()} Analysis",
                border_style="cyan",
            )

        # Get latest analysis
        analysis = analysis_list[-1]

        panel = Text()

        # Position score with visual bar
        score = analysis.get("position_score", 0)
        score_bar = self._create_score_bar(score)
        panel.append("Position: ", style="dim")
        panel.append(score_bar)
        panel.append(f" ({score:+.1f})\n", style="bold")

        # Attacking chances
        attack = analysis.get("attacking_chances", "Unknown")
        panel.append("Attack: ", style="dim")
        panel.append(f"{attack}\n", style="yellow")

        # Defensive needs
        defense = analysis.get("defensive_needs", "None")
        if defense and defense != "None":
            panel.append("Defense: ", style="dim")
            panel.append(f"{defense}\n", style="orange1")

        # Plans
        plans = analysis.get("suggested_plans", [])
        if plans:
            panel.append("\nPlans:\n", style="bold underline")
            for i, plan in enumerate(plans[:3], 1):
                panel.append(f" {i}. {plan}\n", style="cyan")

        style = "green" if color == "white" else "red"
        return Panel(
            panel, title=f"🧠 {color.title()} Analysis", border_style=style, box=ROUNDED
        )

    def render_move_history(self) -> Panel:
        """Render the move history."""
        if not self.state or not self.state.move_history:
            return Panel(
                Text("No moves yet", style="dim italic"),
                title="📜 Move History",
                border_style="yellow",
            )

        # Create a new table
        table = Table(box=SIMPLE, show_header=True, header_style="bold")
        table.add_column("#", style="dim", width=3)
        table.add_column("White", style="green", width=6)
        table.add_column("Black", style="red", width=6)

        # Group moves by pairs
        moves = self.state.move_history

        # Only use the last 10 move pairs (20 moves) for display
        start_idx = max(0, len(moves) - 20)
        start_idx = start_idx - (start_idx % 2)  # Ensure we start with a white move

        for i in range(start_idx, len(moves), 2):
            move_num = i // 2 + 1
            white_move = moves[i][1] if i < len(moves) else ""
            black_move = moves[i + 1][1] if i + 1 < len(moves) else ""

            # Highlight last move
            white_style = "bold green" if i == len(moves) - 1 else "green"
            black_style = "bold red" if i + 1 == len(moves) - 1 else "red"

            table.add_row(
                str(move_num),
                Text(white_move, style=white_style),
                Text(black_move, style=black_style),
            )

        return Panel(table, title="📜 Recent Moves", border_style="yellow", box=ROUNDED)

    def render_game_info(self) -> Panel:
        """Render game information and statistics."""
        if not self.state:
            return Panel("", title="Game Info", border_style="dim")

        info = Table(show_header=False, box=None)
        info.add_column(style="dim")
        info.add_column(style="bold")

        # Game status
        status = self.state.game_status.upper()
        status_style = "green" if status == "ONGOING" else "yellow"
        if status == "CHECKMATE":
            status_style = "red bold"
        info.add_row("Status:", Text(status, style=status_style))

        # Move count
        info.add_row("Moves:", str(len(self.state.move_history)))

        # Current turn
        turn = self.state.current_player.upper()
        turn_style = "green" if turn == "WHITE" else "red"
        info.add_row("Turn:", Text(turn, style=turn_style))

        # Time elapsed
        elapsed = int(time.time() - self.start_time)
        minutes, seconds = divmod(elapsed, 60)
        info.add_row("Time:", f"{minutes:02d}:{seconds:02d}")

        return Panel(info, title="📊 Game Info", border_style="cyan", box=ROUNDED)

    def _create_score_bar(self, score: float) -> Text:
        """Create a visual score bar."""
        # Clamp score between -10 and 10
        score = max(-10, min(10, score))

        # Create bar
        bar_length = 20
        center = bar_length // 2
        position = int(center + (score / 10) * center)

        bar = Text()
        for i in range(bar_length):
            if i == position:
                bar.append("●", style="bold yellow")
            elif i == center:
                bar.append("|", style="dim")
            else:
                bar.append("─", style="dim")

        return bar

    def _update_layout(self):
        """Update all layout components with current state."""
        self.layout["header"].update(self.render_header())
        self.layout["footer"].update(self.render_footer())

        # Left panel
        self.layout["body"]["left_panel"]["white_info"].update(
            self.render_player_info("white")
        )
        self.layout["body"]["left_panel"]["white_analysis"].update(
            self.render_analysis("white")
        )
        self.layout["body"]["left_panel"]["move_history"].update(
            self.render_move_history()
        )

        # Main panel
        self.layout["body"]["main"]["board"].update(self.render_board())
        self.layout["body"]["main"]["current_move"].update(self.render_current_move())

        # Right panel
        self.layout["body"]["right_panel"]["black_info"].update(
            self.render_player_info("black")
        )
        self.layout["body"]["right_panel"]["black_analysis"].update(
            self.render_analysis("black")
        )
        self.layout["body"]["right_panel"]["game_info"].update(self.render_game_info())

    def run(self, agent: ChessAgent, delay: float = 0.5):
        """Run the live UI with the chess agent.

        Args:
            agent: The chess agent to run
            delay: Minimum delay between UI updates (seconds)
        """
        # Create initial state
        initial_state = ChessState()

        # Reset timing
        self.start_time = time.time()

        # Compile the agent (this will build the graph using build_graph)
        app = agent._app

        # Show loading screen
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        ) as progress:
            task = progress.add_task("Initializing chess game...", total=None)
            time.sleep(1)
            progress.remove_task(task)

        try:
            with Live(self.layout, refresh_per_second=4, console=self.console) as live:
                last_update_time = time.time()

                # Stream the game
                # Prepare config with recursion_limit explicitly set
                stream_config = agent.config.runnable_config.copy()
                recursion_limit = stream_config.get("configurable", {}).get(
                    "recursion_limit", 200
                )
                stream_config["recursion_limit"] = recursion_limit

                for step in app.stream(
                    initial_state.model_dump(),
                    config=stream_config,
                    stream_mode="values",
                ):
                    # Convert dict to ChessState
                    if isinstance(step, dict):
                        self.state = ChessState(**step)
                    else:
                        self.state = step

                    # Track last move
                    if self.state.move_history:
                        self.last_move = self.state.move_history[-1][1]
                        self.move_count = len(self.state.move_history)

                    # Update UI with rate limiting
                    current_time = time.time()
                    if current_time - last_update_time >= delay:
                        try:
                            self._update_layout()
                            live.refresh()
                            last_update_time = current_time
                        except (AttributeError, TypeError) as e:
                            if "Row" in str(e):
                                # We already fixed the render_move_history, but in case there are other issues
                                self.console.print(
                                    f"\n[yellow]Row rendering issue: {e}[/yellow]"
                                )
                                # Continue anyway
                            else:
                                # Re-raise other errors
                                raise

                    # Check for game end
                    if self.state.game_status not in ["ongoing", "check"]:
                        # Final update
                        try:
                            self._update_layout()
                            live.refresh()
                            time.sleep(3)  # Show final position
                        except (AttributeError, TypeError) as e:
                            if "Row" in str(e):
                                self.console.print(
                                    f"\n[yellow]Row rendering issue in final update: {e}[/yellow]"
                                )
                            else:
                                # Re-raise other errors
                                raise
                        break

                    # Check for errors
                    if self.state.error_message:
                        self.console.print(
                            f"\n[bold red]Error: {self.state.error_message}[/bold red]"
                        )
                        time.sleep(2)
                        break

        except KeyboardInterrupt:
            self.console.print("\n[yellow]Game interrupted by user[/yellow]")
        except Exception as e:
            self.console.print(f"\n[bold red]Error during game: {e}[/bold red]")
            import traceback

            traceback.print_exc()

        # Show final summary
        if self.state:
            self.console.print("\n[bold cyan]Game Summary:[/bold cyan]")
            self.console.print(f"Total moves: {len(self.state.move_history)}")
            self.console.print(f"Final status: {self.state.game_status}")
            if self.state.game_result:
                self.console.print(f"Result: {self.state.game_result}")


def main():
    """Run a chess game with the Rich UI."""
    # Create configuration
    config = ChessAgentConfig(name="Chess UI Game", enable_analysis=True, max_moves=200)

    # Create agent
    agent = ChessAgent(config)

    # Create and run UI
    ui = ChessRichUI()
    ui.run(agent, delay=0.5)


if __name__ == "__main__":
    main()
