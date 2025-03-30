# among_us_ui.py

from typing import Dict, Any, List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich.text import Text
from rich.box import ROUNDED, HEAVY
from rich.progress import Progress, BarColumn, TextColumn
from rich.style import Style
from rich.columns import Columns
from rich.rule import Rule
from rich import box
from rich.live import Live
from rich.align import Align

from src.haive.games.among_us.state import AmongUsState
from src.haive.games.among_us.models import PlayerRole, AmongUsGamePhase, TaskStatus

class AmongUsUI:
    """
    Rich UI implementation for the Among Us game.
    
    This class provides a visually appealing and informative interface
    for displaying game state and player information.
    """
    
    # Color scheme
    COLORS = {
        "primary": "deep_pink1",
        "secondary": "dark_violet",
        "accent": "medium_purple",
        "background": "black",
        "text": "white",
        "crewmate": "cyan",
        "impostor": "red",
        "alive": "green",
        "dead": "grey50",
        "highlight": "yellow",
        "warning": "orange_red1",
        "success": "green3",
        "error": "red1",
        "header": "purple4"
    }
    
    # Box styles
    BOX_STYLES = {
        "main": box.ROUNDED,
        "inner": box.SIMPLE,
        "header": box.HEAVY,
        "task": box.DOUBLE
    }
    
    def __init__(self, console: Optional[Console] = None):
        """Initialize the UI with an optional custom console."""
        self.console = console or Console()
    
    def display_game(self, state: AmongUsState, current_player: Optional[str] = None) -> Layout:
        """
        Display the full game state.
        
        Args:
            state: Current game state
            current_player: Optional player to highlight as currently active
            
        Returns:
            The complete layout object, which can be used in a Live display
        """
        # Create main layout
        layout = Layout()
        
        # Split into main sections
        layout.split(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=4)
        )
        
        # Split body into map and sidebar
        layout["body"].split_row(
            Layout(name="map", ratio=2),
            Layout(name="sidebar", ratio=1)
        )
        
        # Split sidebar into player list and stats
        layout["sidebar"].split(
            Layout(name="players", ratio=2),
            Layout(name="stats")
        )
        
        # Create the header
        self._create_header(layout["header"], state, current_player)
        
        # Create the map view
        self._create_map_view(layout["map"], state, current_player)
        
        # Create the player list
        self._create_player_list(layout["players"], state, current_player)
        
        # Create the stats section
        self._create_stats_view(layout["stats"], state)
        
        # Create the footer
        self._create_footer(layout["footer"], state, current_player)
        
        return layout
    
    def display_player_view(self, state: AmongUsState, player_id: str) -> Panel:
        """
        Display a detailed view for a specific player.
        
        Args:
            state: Current game state
            player_id: Player to display
            
        Returns:
            A panel containing the player view
        """
        # Check if player exists
        if player_id not in state.player_states:
            return Panel(f"Player {player_id} not found", title="Error")
        
        player_state = state.player_states[player_id]
        
        # Create player layout
        player_layout = Layout()
        player_layout.split(
            Layout(name="info"),
            Layout(name="tasks"),
            Layout(name="observations")
        )
        
        # Create player info
        role = "CREWMATE" if player_state["role"] == PlayerRole.CREWMATE else "IMPOSTOR"
        role_style = self.COLORS["crewmate"] if role == "CREWMATE" else self.COLORS["impostor"]
        status = "ALIVE" if player_state["is_alive"] else "DEAD"
        status_style = self.COLORS["alive"] if status == "ALIVE" else self.COLORS["dead"]
        
        info_table = Table(box=box.SIMPLE, show_header=False, expand=True)
        info_table.add_column("Property")
        info_table.add_column("Value")
        
        info_table.add_row("Role", Text(role, style=role_style))
        info_table.add_row("Status", Text(status, style=status_style))
        info_table.add_row("Location", Text(player_state["location"], style=self.COLORS["highlight"]))
        
        # Add impostor-specific info
        if player_state["role"] == PlayerRole.IMPOSTOR:
            fellow_impostors = [
                pid for pid, pstate in state.player_states.items()
                if pstate["role"] == PlayerRole.IMPOSTOR and pid != player_id
            ]
            if fellow_impostors:
                info_table.add_row(
                    "Fellow Impostors", 
                    Text(", ".join(fellow_impostors), style=self.COLORS["impostor"])
                )
            else:
                info_table.add_row("Fellow Impostors", Text("None (You are alone)", style="italic"))
        
        player_layout["info"].update(Panel(
            info_table,
            title="Player Information",
            border_style=role_style
        ))
        
        # Create tasks view
        tasks_table = Table(
            box=self.BOX_STYLES["task"],
            show_header=True,
            expand=True,
            header_style=self.COLORS["header"]
        )
        tasks_table.add_column("Task", style=self.COLORS["text"])
        tasks_table.add_column("Location", style=self.COLORS["accent"])
        tasks_table.add_column("Status", justify="center")
        
        for task in player_state["tasks"]:
            status_text = "✓" if task.status == TaskStatus.COMPLETED else "□"
            status_style = self.COLORS["success"] if task.status == TaskStatus.COMPLETED else self.COLORS["text"]
            
            # Highlight tasks in current location
            desc_style = self.COLORS["highlight"] if task.location == player_state["location"] else self.COLORS["text"]
            
            tasks_table.add_row(
                Text(task.description, style=desc_style),
                Text(task.location, style=desc_style if task.location == player_state["location"] else self.COLORS["accent"]),
                Text(status_text, style=status_style)
            )
        
        task_title = "Tasks" if player_state["role"] == PlayerRole.CREWMATE else "Fake Tasks"
        player_layout["tasks"].update(Panel(
            tasks_table,
            title=task_title,
            border_style=self.COLORS["secondary"]
        ))
        
        # Create observations view
        if player_state["observations"]:
            observations_text = "\n".join([f"• {obs}" for obs in player_state["observations"][-5:]])
            observations_panel = Align.center(
                Text(observations_text, style=self.COLORS["text"]),
                vertical="middle"
            )
        else:
            observations_panel = Align.center(
                Text("No observations yet", style="italic " + self.COLORS["text"]),
                vertical="middle"
            )
        
        player_layout["observations"].update(Panel(
            observations_panel,
            title="Recent Observations",
            border_style=self.COLORS["accent"]
        ))
        
        # Create the overall panel
        title_style = role_style
        title = f"[bold {title_style}]{player_id} - {role}[/]"
        
        return Panel(
            player_layout,
            title=title,
            border_style=title_style,
            box=self.BOX_STYLES["main"]
        )
    
    def display_meeting_view(self, state: AmongUsState) -> Layout:
        """
        Display the meeting screen.
        
        Args:
            state: Current game state
            
        Returns:
            A layout representing the meeting
        """
        # Create meeting layout
        layout = Layout()
        layout.split(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=4)
        )
        
        # Split body into discussion and voting
        layout["body"].split_row(
            Layout(name="discussion", ratio=2),
            Layout(name="voting", ratio=1)
        )
        
        # Create header
        title = "EMERGENCY MEETING" if not state.reported_body else "BODY REPORTED"
        subtitle = f"Called by {state.meeting_caller}"
        
        if state.reported_body:
            subtitle += f" • Body: {state.reported_body}"
        
        header_text = Align.center(
            Text(f"{title}\n{subtitle}", style=f"bold {self.COLORS['warning']}"),
            vertical="middle"
        )
        
        layout["header"].update(Panel(
            header_text,
            border_style=self.COLORS["warning"],
            box=self.BOX_STYLES["header"]
        ))
        
        # Create discussion history
        discussion_table = Table(box=self.BOX_STYLES["inner"], expand=True)
        discussion_table.add_column("Player", style=self.COLORS["text"])
        discussion_table.add_column("Message", style=self.COLORS["text"], ratio=3)
        
        for message in state.discussion_history[-10:]:  # Last 10 messages
            player_id = message["player_id"]
            player_style = self.COLORS["dead"]
            
            if player_id in state.player_states and state.player_states[player_id]["is_alive"]:
                role = state.player_states[player_id]["role"]
                player_style = self.COLORS["crewmate"] if role == PlayerRole.CREWMATE else self.COLORS["impostor"]
            
            discussion_table.add_row(
                Text(player_id, style=player_style),
                Text(message["message"])
            )
        
        layout["discussion"].update(Panel(
            discussion_table,
            title="Discussion",
            border_style=self.COLORS["primary"]
        ))
        
        # Create voting panel
        voting_table = Table(box=self.BOX_STYLES["inner"], expand=True)
        voting_table.add_column("Player", style=self.COLORS["text"])
        voting_table.add_column("Status", style=self.COLORS["text"])
        
        for player_id in state.players:
            if player_id in state.player_states and state.player_states[player_id]["is_alive"]:
                status = "VOTED" if player_id in state.votes else "NOT VOTED"
                status_style = self.COLORS["success"] if status == "VOTED" else self.COLORS["text"]
                
                voting_table.add_row(
                    Text(player_id),
                    Text(status, style=status_style)
                )
        
        # Add skip option
        skip_votes = sum(1 for vote in state.votes.values() if vote == "skip")
        voting_table.add_row(
            Text("SKIP", style="italic"),
            Text(f"{skip_votes} votes", style=self.COLORS["accent"])
        )
        
        layout["voting"].update(Panel(
            voting_table,
            title=f"Voting ({len(state.votes)}/{len([p for p, s in state.player_states.items() if s['is_alive']])})",
            border_style=self.COLORS["secondary"]
        ))
        
        # Create footer
        phase_text = "DISCUSSION PHASE" if state.game_phase == AmongUsGamePhase.MEETING else "VOTING PHASE"
        footer_text = Align.center(
            Text(phase_text, style=f"bold {self.COLORS['highlight']}"),
            vertical="middle"
        )
        
        layout["footer"].update(Panel(
            footer_text,
            border_style=self.COLORS["highlight"]
        ))
        
        return layout
    
    def display_game_over(self, state: AmongUsState) -> Panel:
        """
        Display the game over screen.
        
        Args:
            state: Final game state
            
        Returns:
            A panel showing the game results
        """
        # Create layout for results
        layout = Layout()
        layout.split(
            Layout(name="winner", size=5),
            Layout(name="players"),
            Layout(name="stats", size=5)
        )
        
        # Create winner announcement
        winner = getattr(state, "winner", None) or "unknown"
        winner_style = self.COLORS["crewmate"] if winner == "crewmates" else self.COLORS["impostor"]
        winner_text = "CREWMATES WIN!" if winner == "crewmates" else "IMPOSTORS WIN!"
        
        winner_panel = Align.center(
            Text(winner_text, style=f"bold {winner_style}", size=28),
            vertical="middle"
        )
        
        layout["winner"].update(Panel(
            winner_panel,
            border_style=winner_style,
            box=self.BOX_STYLES["header"]
        ))
        
        # Create player results
        players_table = Table(box=self.BOX_STYLES["main"], expand=True)
        players_table.add_column("Player", style=self.COLORS["text"])
        players_table.add_column("Role", style=self.COLORS["text"])
        players_table.add_column("Status", style=self.COLORS["text"])
        
        crewmates = []
        impostors = []
        
        for player_id, player_state in state.player_states.items():
            role = "CREWMATE" if player_state["role"] == PlayerRole.CREWMATE else "IMPOSTOR"
            role_style = self.COLORS["crewmate"] if role == "CREWMATE" else self.COLORS["impostor"]
            
            status = "ALIVE" if player_state["is_alive"] else "DEAD"
            status_style = self.COLORS["alive"] if status == "ALIVE" else self.COLORS["dead"]
            
            players_table.add_row(
                Text(player_id),
                Text(role, style=role_style),
                Text(status, style=status_style)
            )
            
            if role == "CREWMATE":
                crewmates.append(player_id)
            else:
                impostors.append(player_id)
        
        layout["players"].update(Panel(
            players_table,
            title="Player Results",
            border_style=self.COLORS["secondary"]
        ))
        
        # Create game stats
        stats_table = Table(box=self.BOX_STYLES["inner"], show_header=False, expand=True)
        stats_table.add_column("Stat")
        stats_table.add_column("Value")
        
        stats_table.add_row(
            "Rounds Played",
            Text(str(state.round_number), style=self.COLORS["highlight"])
        )
        
        stats_table.add_row(
            "Task Completion",
            Text(f"{self._get_task_completion_percentage(state):.1f}%", style=self.COLORS["crewmate"])
        )
        
        stats_table.add_row(
            "Crewmates",
            Text(", ".join(crewmates), style=self.COLORS["crewmate"])
        )
        
        stats_table.add_row(
            "Impostors",
            Text(", ".join(impostors), style=self.COLORS["impostor"])
        )
        
        layout["stats"].update(Panel(
            stats_table,
            title="Game Statistics",
            border_style=self.COLORS["accent"]
        ))
        
        return Panel(
            layout,
            title="GAME OVER",
            border_style=winner_style,
            box=self.BOX_STYLES["main"]
        )
    
    def _create_header(self, layout_section, state: AmongUsState, current_player: Optional[str] = None):
        """Create the game header."""
        phase_text = str(state.game_phase).replace("_", " ")
        
        header_elements = [
            Text("AMONG US", style=f"bold {self.COLORS['primary']}"),
            Text(f"ROUND {state.round_number}", style=self.COLORS['secondary']),
            Text(phase_text, style=self.COLORS['accent'])
        ]
        
        if current_player:
            header_elements.append(Text(f"CURRENT PLAYER: {current_player}", style=self.COLORS['highlight']))
        
        header_text = Text(" • ", style=self.COLORS['text']).join(header_elements)
        header_panel = Align.center(header_text, vertical="middle")
        
        layout_section.update(Panel(
            header_panel,
            border_style=self.COLORS['primary'],
            box=self.BOX_STYLES["header"]
        ))
    
    def _create_map_view(self, layout_section, state: AmongUsState, current_player: Optional[str] = None):
        """Create the map visualization."""
        map_grid = Table.grid(expand=True)
        
        # Group locations for better visualization
        location_groups = self._group_locations(state.map_locations)
        
        for group in location_groups:
            row_panels = []
            
            for location in group:
                # Get players at this location
                players_here = []
                for pid, pstate in state.player_states.items():
                    if pstate.location == location:
                        # Style based on player status
                        style = ""
                        if pid == current_player:
                            style += f"bold {self.COLORS['highlight']}"
                        elif not pstate.is_alive:
                            style += self.COLORS["dead"]
                        else:
                            # We'd show real roles in the UI but not to players
                            style += self.COLORS["crewmate"] if pstate.role == PlayerRole.CREWMATE else self.COLORS["impostor"]
                        
                        player_text = f"{pid}"
                        if not pstate.is_alive:
                            player_text += " (dead)"
                        
                        players_here.append(Text(player_text, style=style))
                
                # Create location panel
                location_text = "\n".join([str(p) for p in players_here]) if players_here else "Empty"
                
                # Highlight current player's location
                border_style = self.COLORS["highlight"] if (
                    current_player and 
                    current_player in state.player_states and
                    state.player_states[current_player].location == location
                ) else self.COLORS["secondary"]
                
                panel = Panel(
                    Align.center(Text(location_text) if players_here else Text("Empty", style="italic")),
                    title=location.capitalize(),
                    border_style=border_style,
                    box=self.BOX_STYLES["inner"],
                    width=24,
                    height=8
                )
                
                row_panels.append(panel)
            
            # Add row to grid
            map_grid.add_row(*row_panels)
        
        layout_section.update(Panel(
            map_grid,
            title="Ship Map",
            border_style=self.COLORS["primary"]
        ))
    
    def _group_locations(self, locations: List[str]) -> List[List[str]]:
        """Group locations into rows for better display."""
        # Default groups for "skeld" map
        if "cafeteria" in locations:
            return [
                ["cafeteria", "admin", "storage"],
                ["weapons", "navigation", "shields"],
                ["medbay", "electrical", "security"],
                ["o2", "reactor", "communications"]
            ]
        
        # For other maps or custom locations, create a balanced grid
        import math
        cols = math.ceil(math.sqrt(len(locations)))
        
        groups = []
        for i in range(0, len(locations), cols):
            groups.append(locations[i:i+cols])
        
        return groups
    
    def _create_player_list(self, layout_section, state: AmongUsState, current_player: Optional[str] = None):
        """Create the player list section."""
        players_table = Table(box=self.BOX_STYLES["inner"], expand=True)
        players_table.add_column("Player", style=self.COLORS["text"])
        players_table.add_column("Status", style=self.COLORS["text"])
        players_table.add_column("Location", style=self.COLORS["accent"])
        
        for player_id, player_state in state.player_states.items():
            # Status with appropriate styling
            status = "ALIVE" if player_state.is_alive else "DEAD"
            status_style = self.COLORS["alive"] if status == "ALIVE" else self.COLORS["dead"]
            
            # Style for current player
            player_style = ""
            if player_id == current_player:
                player_style = f"bold {self.COLORS['highlight']}"
            
            players_table.add_row(
                Text(player_id, style=player_style),
                Text(status, style=status_style),
                Text(player_state.location)
            )
        
        layout_section.update(Panel(
            players_table,
            title="Players",
            border_style=self.COLORS["secondary"]
        ))
    
    def _create_stats_view(self, layout_section, state: AmongUsState):
        """Create the game statistics section."""
        # Calculate task completion
        task_completion = self._get_task_completion_percentage(state)
        
        # Create a progress bar for task completion
        task_progress = Progress(
            TextColumn("[bold]Task Completion:"),
            BarColumn(complete_style=self.COLORS["crewmate"]),
            TextColumn("[bold]{task.percentage:.0f}%")
        )
        task_progress.add_task("", total=100, completed=task_completion)
        
        # Create a stats table
        stats_table = Table(box=None, show_header=False, show_edge=False, expand=True)
        stats_table.add_column("Stat")
        stats_table.add_column("Value")
        
        stats_table.add_row(
            "Crewmates Remaining:", 
            Text(str(state.crewmate_count), style=self.COLORS["crewmate"])
        )
        
        stats_table.add_row(
            "Impostors Remaining:", 
            Text(str(state.impostor_count), style=self.COLORS["impostor"])
        )
        
        if state.eliminated_players:
            stats_table.add_row(
                "Eliminated:", 
                Text(", ".join(state.eliminated_players), style=self.COLORS["dead"])
            )
        
        # Combine elements
        stats_layout = Layout()
        stats_layout.split(
            Layout(name="progress"),
            Layout(name="counts")
        )
        
        stats_layout["progress"].update(task_progress)
        stats_layout["counts"].update(stats_table)
        
        layout_section.update(Panel(
            stats_layout,
            title="Game Stats",
            border_style=self.COLORS["accent"]
        ))
    
    def _create_footer(self, layout_section, state: AmongUsState, current_player: Optional[str] = None):
        """Create the footer with game status and instructions."""
        footer_text = ""
        
        if state.game_phase == AmongUsGamePhase.TASKS:
            footer_text = "Perform tasks and watch for suspicious behavior!"
            
            # Add player-specific instructions
            if current_player and current_player in state.player_states:
                player_role = state.player_states[current_player].role 
                if player_role == PlayerRole.CREWMATE:
                    footer_text = "Complete your tasks and identify the impostors!"
                else:
                    footer_text = "Sabotage the ship and eliminate crewmates without getting caught!"
                    
        elif state.game_phase == AmongUsGamePhase.MEETING:
            if state.reported_body:
                footer_text = f"BODY REPORTED: {state.reported_body} was found by {state.meeting_caller}!"
            else:
                footer_text = f"EMERGENCY MEETING called by {state.meeting_caller}!"
                
        elif state.game_phase == AmongUsGamePhase.VOTING:
            votes_cast = len(state.votes)
            alive_players = len([p for p, s in state.player_states.items() if s.is_alive])
            footer_text = f"VOTING: {votes_cast}/{alive_players} votes cast"
            
        elif state.game_phase == AmongUsGamePhase.GAME_OVER:
            footer_text = "GAME OVER!"
            if hasattr(state, "winner"):
                if state.winner == "crewmates":
                    footer_text = "CREWMATES WIN! All tasks completed or all impostors eliminated!"
                else:
                    footer_text = "IMPOSTORS WIN! Crewmates eliminated or outnumbered!"
        
        footer_panel = Align.center(
            Text(footer_text, style=f"bold {self.COLORS['text']}"),
            vertical="middle"
        )
        
        style = self.COLORS["primary"]
        if state.game_phase == AmongUsGamePhase.MEETING:
            style = self.COLORS["warning"]
        elif state.game_phase == AmongUsGamePhase.GAME_OVER:
            style = self.COLORS["impostor"] if getattr(state, "winner", "") == "impostors" else self.COLORS["crewmate"]
        
        layout_section.update(Panel(
            footer_panel,
            border_style=style
        ))
    
    def _get_task_completion_percentage(self, state: AmongUsState) -> float:
        """Calculate task completion percentage."""
        # Only count real tasks (not impostor fake tasks)
        crewmate_tasks = []
        for pid, pstate in state.player_states.items():
            if pstate.role == PlayerRole.CREWMATE:
                crewmate_tasks.extend(pstate.tasks)
        
        total = len(crewmate_tasks)
        if total == 0:
            return 100.0
        
        completed = sum(1 for task in crewmate_tasks if task.status == TaskStatus.COMPLETED)
        return (completed / total) * 100
    
    def create_live_display(self, state: AmongUsState, current_player: Optional[str] = None) -> Live:
        """Create a live display for the game that can be updated."""
        layout = self.display_game(state, current_player)
        return Live(layout, console=self.console, screen=True, refresh_per_second=4)