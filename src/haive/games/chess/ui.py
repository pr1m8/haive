# ✅ FIRST THIRD: RichChessUI class foundation (layout + static renderers, no stream yet)

from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.align import Align
from rich.box import ROUNDED, SIMPLE
from typing import Dict, Any, Optional
from rich.live import Live
import time
from typing import Any
import chess  # required for local usage
from src.haive.games.chess.agent import ChessAgent
from src.haive.games.chess.config import ChessAgentConfig

class ChessRichUI:
    """
    Beautiful Rich UI for displaying a live chess agent game.
    Inspired by PokerUI, structured with header, board, analysis, move history, and game info.
    """

    def __init__(self):
        self.console = Console()
        self.layout = Layout()
        self.state: Optional[Dict[str, Any]] = None
        self.last_move: Optional[str] = None
        self._setup_layout()

    def _setup_layout(self):
        """Initialize the layout structure"""
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="body", ratio=1),
            Layout(name="footer", size=3),
        )

        self.layout["body"].split_row(
            Layout(name="left_panel", ratio=1),
            Layout(name="main", ratio=2),
            Layout(name="right_panel", ratio=1),
        )

        self.layout["body"]["left_panel"].split(
            Layout(name="white_analysis", size=12),
            Layout(name="move_history"),
        )

        self.layout["body"]["main"].split(
            Layout(name="board", ratio=1),
        )

        self.layout["body"]["right_panel"].split(
            Layout(name="black_analysis", size=12),
            Layout(name="captured"),
            Layout(name="status"),
        )

    def render_header(self) -> Panel:
        header_text = Text("♟️ AI Chess Arena", justify="center", style="bold white on blue")
        return Panel(header_text, border_style="blue")

    def render_footer(self) -> Panel:
        controls = [
            ("Q", "Quit"),
            ("← →", "Move Nav"),
            ("A", "Toggle Analysis"),
            ("R", "Restart"),
        ]
        footer = Text()
        for key, desc in controls:
            footer.append(f" {key} ", style="black on white")
            footer.append(f" {desc}  ", style="white")
        return Panel(Align.center(footer), border_style="blue")

    def render_board(self) -> Panel:
        if not self.state:
            return Panel("Waiting for game state...", title="Board", border_style="magenta")

        import chess  # Only import if you have it installed locally
        board = chess.Board(self.state["board_fens"][-1])
        lines = str(board).splitlines()

        board_text = Text()
        for i, line in enumerate(reversed(lines)):
            board_text.append(f"{8 - i} ", style="bold dim")
            for c in line.split():
                style = "white"
                if c == ".":
                    piece = "·"
                    style = "dim"
                elif c.isupper():
                    piece = c
                    style = "bold green"
                else:
                    piece = c
                    style = "bold red"
                board_text.append(f"{piece} ", style=style)
            board_text.append("\n")
        board_text.append("  a b c d e f g h", style="dim")

        return Panel(board_text, title="Chessboard", border_style="magenta")

    def render_move_history(self) -> Panel:
        if not self.state or not self.state.get("move_history"):
            return Panel("No moves yet", title="Moves", border_style="yellow")

        table = Table(box=SIMPLE, style="dim")


        table.add_column("Color", style="dim", width=6)
        table.add_column("Move", style="bold")

        for color, move in self.state["move_history"][-10:]:
            move_style = "green" if color == "white" else "red"
            table.add_row(color.capitalize(), Text(move, style=move_style))

        return Panel(table, title="Move History", border_style="yellow")

    def render_analysis(self, color: str) -> Panel:
        if not self.state:
            return Panel("No data", title=f"{color.capitalize()} Analysis", border_style="cyan")

        analysis = self.state.get(f"{color}_analysis", [])
        if not analysis:
            return Panel("No analysis yet", title=f"{color.capitalize()} Analysis", border_style="cyan")

        last = analysis[-1]
        panel = Text()
        panel.append(f"Score: {last.get('position_score', 'N/A')}\n", style="bold")
        panel.append(f"Attack: {last.get('attacking_chances', 'N/A')}\n", style="yellow")
        panel.append(f"Defense: {last.get('defensive_needs', 'N/A')}\n", style="yellow")

        plans = last.get("suggested_plans", [])
        if plans:
            panel.append("\nPlans:\n", style="bold underline")
            for plan in plans:
                panel.append(f" - {plan}\n", style="dim")

        style = "green" if color == "white" else "red"
        return Panel(panel, title=f"{color.capitalize()} Analysis", border_style=style)

    def render_captured(self) -> Panel:
        if not self.state:
            return Panel("No captures", title="Captured", border_style="red")

        captured = self.state.get("captured_pieces", {"white": [], "black": []})
        text = Text()
        text.append("White captured:\n", style="bold green")
        text.append(", ".join(captured["white"]) or "None")
        text.append("\n\nBlack captured:\n", style="bold red")
        text.append(", ".join(captured["black"]) or "None")

        return Panel(text, title="Captured Pieces", border_style="red")

    def render_status(self) -> Panel:
        if not self.state:
            return Panel("Waiting...", title="Game Status", border_style="cyan")

        status = self.state.get("game_status", "Unknown").capitalize()
        player = self.state.get("current_player", "?").capitalize()

        text = Text()
        text.append(f"Status: {status}\n", style="bold")
        text.append(f"Current Player: {player}", style="green" if player == "White" else "red")

        return Panel(text, title="Game Info", border_style="cyan")
    def run(self, agent, delay: float = 1.0):
        """
        Run the live UI using LangGraph agent streaming.

        Args:
            agent (ChessAgent): Your instantiated chess agent.
            delay (float): Delay between frames for readability.
        """
        initial_state = {
            "board_fens": [chess.Board().fen()],
            "current_player": "white",
            "turn": "white",
            "move_history": [],
            "game_status": "ongoing",
            "white_analysis": [],
            "black_analysis": [],
            "captured_pieces": {"white": [], "black": []},
            "error_message": None,
        }

        with Live(self.layout, screen=True, refresh_per_second=4):
            for step in agent.app.stream(initial_state, config=agent.runnable_config, debug=False, stream_mode="values"):
                self.state = step
                self.last_move = step["move_history"][-1][1] if step.get("move_history") else None

                # Update all components
                self.layout["header"].update(self.render_header())
                self.layout["footer"].update(self.render_footer())

                self.layout["body"]["left_panel"]["white_analysis"].update(self.render_analysis("white"))
                self.layout["body"]["left_panel"]["move_history"].update(self.render_move_history())

                self.layout["body"]["main"]["board"].update(self.render_board())

                self.layout["body"]["right_panel"]["black_analysis"].update(self.render_analysis("black"))
                self.layout["body"]["right_panel"]["captured"].update(self.render_captured())
                self.layout["body"]["right_panel"]["status"].update(self.render_status())

                if step.get("game_status") != "ongoing":
                    time.sleep(2)
                    break

        self.console.print("\n[bold magenta]🏁 Game Over[/bold magenta]")
        agent.save_state_history()

def main():
    ui = ChessRichUI()
    agent = ChessAgent(config=ChessAgentConfig())
    ui.run(agent)

if __name__ == "__main__":
    main()  