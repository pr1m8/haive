from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.align import Align
from rich.box import ROUNDED, SIMPLE

class PokerUI:
    """Clean, readable UI for the poker game simulation"""
    
    def __init__(self):
        self.layout = Layout()
        self.current_game_state = None
        self.animation_frame = 0
        self.player_models = {}  # Will store AI model info
        
        self._setup_layout()
    
    def _setup_layout(self):
        """Set up the UI layout with clean, simple sections"""
        # Main layout with header, body, footer
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3),
        )
        
        # Split the body into three columns
        self.layout["body"].split_row(
            Layout(name="left_panel", ratio=1),
            Layout(name="main", ratio=2),
            Layout(name="right_panel", ratio=1),
        )
        
        # Add game info and history to left panel
        self.layout["body"]["left_panel"].split(
            Layout(name="game_info", size=10),
            Layout(name="action_history"),
        )
        
        # Add table and players to main area
        self.layout["body"]["main"].split(
            Layout(name="table", ratio=1),
            Layout(name="players", ratio=1),
        )
        
        # Add active player to right panel
        self.layout["body"]["right_panel"].split(
            Layout(name="active_player", size=10),
            Layout(name="decisions", size=10),
            Layout(name="info")
        )
    
    def assign_ai_models(self, player_names):
        """Assign consistent AI models to players"""
        ai_models = {
            "Claude-3": {"model": "Claude-3", "arch": "Anthropic"},
            "GPT-4o": {"model": "GPT-4o", "arch": "OpenAI"},
            "Gemini": {"model": "Gemini", "arch": "Google"},
            "DeepSeek": {"model": "DeepSeek", "arch": "DeepSeek"},
            "Mistral": {"model": "Mistral", "arch": "Mistral AI"}
        }
        
        # Default model for any player not in the predefined list
        default_model = {"model": "Custom", "arch": "Generic"}
        
        # Assign models to players
        self.player_models = {name: ai_models.get(name, default_model) for name in player_names}
    
    def render_header(self):
        """Render a clean header with title"""
        header_text = Text("♠️ TEXAS HOLD'EM POKER ♥️", justify="center", style="bold white on blue")
        return Panel(header_text, border_style="blue")
    
    def render_footer(self):
        """Render a simple footer with controls"""
        controls = [
            ("ENTER", "Continue"),
            ("ESC", "Exit"),
            ("S", "Statistics"),
            ("H", "History")
        ]
        
        footer_content = Text()
        for key, action in controls:
            footer_content.append(f" {key} ", style="black on white")
            footer_content.append(f" {action} ", style="white")
            footer_content.append("  ")
        
        return Panel(Align.center(footer_content), border_style="blue")
    
    def render_game_info(self):
        """Render clean game info panel"""
        if not self.current_game_state:
            return Panel("Game not started", title="Game Info", border_style="green")
        
        game = self.current_game_state["game"]
        
        # Create game info text
        content = Text()
        
        # Add phase info
        content.append("Phase: ", style="bold")
        phase = game.phase.value if hasattr(game, "phase") else "Unknown"
        content.append(f"{phase}\n\n", style="cyan")
        
        # Add pot info
        content.append("Pot: ", style="bold")
        total_pot = sum(pot.amount for pot in game.pots) if hasattr(game, "pots") else 0
        content.append(f"${total_pot}\n\n", style="green")
        
        # Add current bet
        content.append("Current Bet: ", style="bold")
        current_bet = game.current_bet if hasattr(game, "current_bet") else 0
        content.append(f"${current_bet}\n", style="yellow")
        
        return Panel(content, title="Game Info", border_style="green")
    
    def render_action_history(self):
        """Render clean action history"""
        if not self.current_game_state:
            return Panel("No actions yet", title="Recent Actions", border_style="yellow")
        
        game = self.current_game_state["game"]
        
        if not hasattr(game, "action_history") or not game.action_history:
            return Panel("No actions yet", title="Recent Actions", border_style="yellow")
        
        # Get last 5 actions
        recent_actions = game.action_history[-min(5, len(game.action_history)):]
        
        # Create action history text
        content = Text()
        
        for i, action in enumerate(recent_actions, 1):
            # Find player name
            player = next((p for p in game.players if p.id == action.player_id), None)
            player_name = player.name if player else "Unknown"
            
            # Add action with proper styling
            content.append(f"{i}. ", style="dim")
            
            # Style based on action type
            action_style = "green"
            if action.action.value in ["fold", "check"]:
                action_style = "yellow"
            elif action.action.value in ["bet", "raise", "all-in"]:
                action_style = "red"
            
            content.append(f"{player_name}: ", style="bold")
            content.append(action.action.value.upper(), style=action_style)
            
            # Add amount if applicable
            if action.amount > 0:
                content.append(f" ${action.amount}", style="cyan")
            
            content.append("\n")
        
        return Panel(content, title="Recent Actions", border_style="yellow")
    
    def render_table(self):
        """Render poker table with community cards"""
        if not self.current_game_state:
            return Panel("Table not set up", title="Poker Table", border_style="red")
        
        game = self.current_game_state["game"]
        
        # Create table content
        content = Text("\n")  # Start with space
        
        # Add community cards if available
        if hasattr(game, "community_cards") and game.community_cards:
            cards_text = " ".join(self._format_card(card) for card in game.community_cards)
            content.append("Community Cards:\n", style="bold")
            content.append(f"{cards_text}\n\n", style="cyan")
        else:
            content.append("No community cards yet\n\n", style="dim")
        
        # Add pot information
        total_pot = sum(pot.amount for pot in game.pots) if hasattr(game, "pots") else 0
        content.append(f"Total Pot: ${total_pot}\n", style="green bold")
        
        # Show individual pots if there are side pots
        if hasattr(game, "pots") and len(game.pots) > 1:
            for i, pot in enumerate(game.pots):
                pot_name = "Main Pot" if i == 0 else f"Side Pot {i}"
                content.append(f"{pot_name}: ${pot.amount}\n", style="green")
        
        return Panel(
            Align.center(content),
            title="♦️ Poker Table ♣️",
            border_style="red"
        )
    
    def render_players(self):
        """Render players table with clear information"""
        if not self.current_game_state:
            return Panel("No players", title="Players", border_style="blue")
        
        game = self.current_game_state["game"]
        
        # Create player table
        table = Table(
            box=SIMPLE,
            title="Players",
            title_style="bold blue",
            border_style="blue",
            header_style="bold cyan",
            show_header=True,
            expand=True
        )
        
        # Add columns
        table.add_column("Position", style="dim")
        table.add_column("Player", style="bold")
        table.add_column("AI Model", style="cyan")
        table.add_column("Chips", style="green")
        table.add_column("Status", style="yellow")
        
        # Add rows for each player
        current_player_idx = game.current_player_idx if hasattr(game, "current_player_idx") else -1
        dealer_position = game.dealer_position if hasattr(game, "dealer_position") else -1
        
        for player in game.players:
            # Determine position name
            position = player.position if hasattr(player, "position") else -1
            position_name = self._get_position_name(position, len(game.players))
            
            # Add dealer indicator
            if position == dealer_position:
                position_name = "⭐ " + position_name
            
            # Get player status
            status = "Active"
            status_style = "green"
            
            if not player.is_active:
                status = "Folded"
                status_style = "red"
            elif player.is_all_in:
                status = "All-In"
                status_style = "magenta"
            elif player.current_bet > 0:
                status = f"Bet: ${player.current_bet}"
                status_style = "yellow"
            
            # Highlight current player
            row_style = "on dark_blue" if player.id == game.players[current_player_idx].id else ""
            
            # Get AI model info
            model_info = self.player_models.get(player.name, {"model": "Unknown", "arch": "Unknown"})
            model_text = f"{model_info['model']}"
            
            # Add player to table
            table.add_row(
                position_name,
                player.name,
                model_text,
                f"${player.chips}",
                Text(status, style=status_style),
                style=row_style
            )
            
            # Show cards for active players (in a real game, this would only show for the human player)
            if player.is_active and hasattr(player, "hand") and player.hand and player.hand.cards:
                cards_text = " ".join([self._format_card(card) for card in player.hand.cards])
                table.add_row(
                    "",
                    f"Hand: {cards_text}",
                    "",
                    "",
                    "",
                    style=row_style
                )
        
        return table
    
    def render_active_player(self):
        """Render active player information"""
        if not self.current_game_state:
            return Panel("No active player", title="🎮 Active Player 🎮", border_style="cyan")
        
        game = self.current_game_state["game"]
        
        if not hasattr(game, "current_player_idx") or game.current_player_idx >= len(game.players):
            return Panel("No active player", title="🎮 Active Player 🎮", border_style="cyan")
        
        # Get current player
        current_player = game.players[game.current_player_idx]
        
        # Create player info text
        content = Text()
        
        # Add player name
        content.append(f"{current_player.name}\n\n", style="bold white")
        
        # Add player chips
        content.append("Chips: ", style="bold")
        content.append(f"${current_player.chips}\n", style="green")
        
        # Add current bet
        content.append("Current Bet: ", style="bold")
        content.append(f"${current_player.current_bet}\n", style="yellow")
        
        # Add AI model info if available
        model_info = self.player_models.get(current_player.name, {"model": "Unknown", "arch": "Unknown"})
        content.append("\nAI: ", style="bold")
        content.append(f"{model_info['model']} ({model_info['arch']})", style="cyan")
        
        return Panel(content, title="🎮 Active Player 🎮", border_style="cyan")
    
    def _format_card(self, card):
        """Format a card with unicode symbols"""
        suits = {
            "hearts": "♥",
            "diamonds": "♦",
            "clubs": "♣",
            "spades": "♠"
        }
        
        suit_value = card.suit.value if hasattr(card.suit, "value") else str(card.suit)
        suit_symbol = suits.get(suit_value, suit_value)
        
        card_value = card.value.value if hasattr(card.value, "value") else str(card.value)
        
        # Color based on suit
        color = "red" if suit_value in ["hearts", "diamonds"] else "white"
        
        return f"[bold {color}]{card_value}{suit_symbol}[/bold {color}]"
    
    def _get_position_name(self, position, num_players):
        """Get the poker position name"""
        if position == 0:
            return "Dealer"
        elif position == 1:
            return "Small Blind"
        elif position == 2:
            return "Big Blind"
        elif position == 3:
            return "UTG"  # Under the Gun
        elif position == num_players - 1:
            return "Cutoff"
        else:
            return f"MP{position-2}"  # Middle Position