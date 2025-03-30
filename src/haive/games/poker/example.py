import logging
import time
import argparse
import random
import sys
import os
import subprocess
from typing import Dict, List, Any, Optional
from datetime import datetime

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from src.haive.games.poker.state_manager import PokerStateManager
from src.haive.games.poker.config import PokerAgentConfig
from src.haive.games.poker.agent import PokerAgent
from src.haive.games.poker.models import Card, GamePhase, PlayerAction
from src.haive.games.poker.engines import poker_agent_configs

# Import the PokerUI class - if not available, the class is defined in the previous artifact
from src.haive.games.poker.ui import PokerUI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("poker_game.log")
    ]
)

logger = logging.getLogger(__name__)

# Global UI variables for persistence between frames
ui = None
live = None

def main():
    ai_player_names = [
        "Claude-3", 
        "GPT-4o", 
        "Gemini", 
        "DeepSeek",
        "Mistral"
    ]
    parser = argparse.ArgumentParser(description="Run a Texas Hold'em Poker game simulation")
    parser.add_argument("--players", type=int, default=len(ai_player_names), help="Number of players (2-10)")
    parser.add_argument("--chips", type=int, default=1000, help="Starting chips per player")
    parser.add_argument("--small-blind", type=int, default=50, help="Small blind amount")
    parser.add_argument("--big-blind", type=int, default=100, help="Big blind amount")
    parser.add_argument("--delay", type=float, default=1.5, help="Delay between game updates (seconds)")
    parser.add_argument("--text-only", action="store_true", help="Use text-only visualization")
    parser.add_argument("--separate-window", action="store_true", help="Open in a separate window")
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.players < 2 or args.players > 10:
        parser.error("Number of players must be between 2 and 10")
    
    # Ensure we have enough names for the requested players
    while len(ai_player_names) < args.players:
        ai_player_names.append(f"Player-{len(ai_player_names)+1}")
    
    # Shuffle the names and take the required number
    random.shuffle(ai_player_names)
    player_names = ai_player_names[:args.players]
    
    print(f"Players: {', '.join(player_names)}")
    
    # Create a complete game configuration with default engines
    config = PokerAgentConfig(
        player_names=player_names,
        starting_chips=args.chips,
        small_blind=args.small_blind,
        big_blind=args.big_blind,
        enable_detailed_analysis=True,
        engines=poker_agent_configs  # Use the pre-defined poker agent configs
    )
    
    # Print game information
    print("\n🃏 Starting Texas Hold'em Poker Game 🃏")
    print(f"Players: {', '.join(player_names)}")
    print(f"Starting chips: ${args.chips}")
    print(f"Blinds: ${args.small_blind}/${args.big_blind}")
    print("Game will run until only one player remains with chips")
    print("=" * 50)
    
    # Handle separate window option
    if args.separate_window:
        # Launch the game in a new terminal window
        launch_in_separate_window(args, player_names)
    else:
        # Run the game in the current terminal
        if args.text_only:
            run_text_game(config, args.delay)
        else:
            run_rich_ui_game(config, player_names, args.delay)
    
    print("\n✅ Game simulation complete!")

def launch_in_separate_window(args, player_names):
    """Launch the poker game in a separate terminal window"""
    try:
        # Construct the command to run in the new window
        script_path = os.path.abspath(__file__)
        cmd = [sys.executable, script_path]
        
        # Add all the original arguments except --separate-window
        if args.players != len(player_names):
            cmd.extend(["--players", str(args.players)])
        if args.chips != 1000:
            cmd.extend(["--chips", str(args.chips)])
        if args.small_blind != 5:
            cmd.extend(["--small-blind", str(args.small_blind)])
        if args.big_blind != 10:
            cmd.extend(["--big-blind", str(args.big_blind)])
        if args.delay != 1.5:
            cmd.extend(["--delay", str(args.delay)])
        if args.text_only:
            cmd.append("--text-only")
        
        # Detect OS and launch appropriate terminal
        if sys.platform.startswith('win'):
            # Windows: use start cmd
            full_cmd = ['start', 'cmd', '/c'] + cmd
            subprocess.Popen(full_cmd, shell=True)
        elif sys.platform.startswith('darwin'):
            # macOS: use Terminal.app
            os.system(f"osascript -e 'tell app \"Terminal\" to do script \"{' '.join(cmd)}\"'")
        else:
            # Linux/Unix: try common terminals
            terminals = ['gnome-terminal', 'xterm', 'konsole', 'terminator']
            for term in terminals:
                try:
                    if term == 'gnome-terminal':
                        subprocess.Popen([term, '--', *cmd])
                    else:
                        subprocess.Popen([term, '-e', ' '.join(cmd)])
                    break
                except FileNotFoundError:
                    continue
            else:
                print("Could not find a suitable terminal emulator. Running in current terminal.")
                run_rich_ui_game(create_config_from_args(args, player_names), player_names, args.delay)
        
        print("Game launched in a separate window.")
    
    except Exception as e:
        print(f"Error launching separate window: {str(e)}")
        print("Running in current terminal instead.")
        run_rich_ui_game(create_config_from_args(args, player_names), player_names, args.delay)

def create_config_from_args(args, player_names):
    """Create a poker agent config from command line args"""
    return PokerAgentConfig(
        player_names=player_names,
        starting_chips=args.chips,
        small_blind=args.small_blind,
        big_blind=args.big_blind,
        enable_detailed_analysis=True,
        engines=poker_agent_configs
    )

def run_rich_ui_game(config, player_names, delay, max_hands=None):
    """Run the game with rich UI visualization"""
    global ui, live
    
    # Initialize the UI
    console = Console()
    ui = PokerUI()
    ui.assign_ai_models(player_names)
    
    # Initialize the state manager directly
    state_manager = PokerStateManager()
    state_manager.initialize_game(config)
    state_manager.start_new_hand()
    
    # Start the Live display
    with Live(ui.layout, console=console, screen=True, refresh_per_second=2) as live:
        hands_played = 0
        game_over = False

        while not game_over:
            ui.current_game_state = {"game": state_manager.state.game}
            ui.animation_frame += 1
            update_ui()
            time.sleep(delay)

            game = state_manager.state.game

            if game.phase == GamePhase.GAME_OVER:
                hands_played += 1
                logger.info(f"Hand #{hands_played} completed")

                # ✅ Check if max hands played
                if max_hands is not None and hands_played >= max_hands:
                    logger.info(f"🔚 Reached max hands limit: {max_hands}")
                    game_over = True
                    update_ui()
                    time.sleep(delay * 2)
                    break

                players_with_chips = sum(1 for p in game.players if p.chips > 0)
                if players_with_chips <= 1:
                    game_over = True
                    update_ui()
                    time.sleep(delay * 2)
                    break

                state_manager.start_new_hand()
                update_ui()
                time.sleep(delay)
                continue

                
            # Otherwise, take the next game action
            if game.round_complete:
                # If the round is complete, advance to the next phase
                state_manager.advance_phase()
                
                # Show phase transition for a moment
                update_ui()
                time.sleep(delay)
            else:
                # Otherwise, handle the current player's action
                current_player = game.players[game.current_player_idx]
                
                # Skip inactive or all-in players
                if not current_player.is_active or current_player.is_all_in:
                    state_manager.state._advance_to_next_player()
                    continue
                
                # Show whose turn it is for a moment
                update_ui()
                time.sleep(delay / 2)
                
                # Determine a simple action for the player
                if game.current_bet == current_player.current_bet:
                    # Can check
                    state_manager.handle_player_action(current_player.id, PlayerAction.CHECK, 0)
                elif current_player.chips >= (game.current_bet - current_player.current_bet):
                    # Can call
                    state_manager.handle_player_action(
                        current_player.id,
                        PlayerAction.CALL,
                        game.current_bet - current_player.current_bet
                    )
                else:
                    # Must fold
                    state_manager.handle_player_action(current_player.id, PlayerAction.FOLD, 0)
                
                # Show the action that was taken
                update_ui()
                time.sleep(delay)
    
    # Print final results
    print("\n🏆 Game Complete 🏆")
    print("=" * 50)
    
    # Print final chip counts
    print("\nFinal Chip Counts:")
    sorted_players = sorted(state_manager.state.game.players, key=lambda p: p.chips, reverse=True)
    for i, player in enumerate(sorted_players):
        print(f"{i+1}. {player.name}: ${player.chips}")

def update_ui():
    """Helper function to update all UI components"""
    global ui, live
    
    if ui and live:
        # Header and footer
        ui.layout["header"].update(ui.render_header())
        ui.layout["footer"].update(ui.render_footer())
        
        # Left panel
        ui.layout["body"]["left_panel"]["game_info"].update(ui.render_game_info())
        ui.layout["body"]["left_panel"]["action_history"].update(ui.render_action_history())
        
        # Main area
        ui.layout["body"]["main"]["table"].update(ui.render_table())
        ui.layout["body"]["main"]["players"].update(ui.render_players())
        
        # Right panel
        ui.layout["body"]["right_panel"]["active_player"].update(ui.render_active_player())
        
        # Empty panels for other sections
        ui.layout["body"]["right_panel"]["decisions"].update(Panel("", title="Decisions", border_style="blue"))
        ui.layout["body"]["right_panel"]["info"].update(Panel("", title="Info", border_style="blue"))

def run_text_game(config, delay):
    """Run the game with text-only visualization"""
    # Initialize the state manager
    state_manager = PokerStateManager()
    state_manager.initialize_game(config)
    state_manager.start_new_hand()
    
    hands_played = 0
    game_over = False
    
    while not game_over:
        # Visualize the current game state
        visualize_game_state(state_manager.state.game)
        
        # Wait for the specified delay
        time.sleep(delay)
        
        # Get the current game state
        game = state_manager.state.game
        
        # If the hand is complete, start a new one or end the game
        if game.phase == GamePhase.GAME_OVER:
            hands_played += 1
            print(f"\nHand #{hands_played} completed")
            
            # Check if only one player has chips left
            players_with_chips = sum(1 for p in game.players if p.chips > 0)
            if players_with_chips <= 1:
                game_over = True
                break
                
            # Otherwise, start a new hand
            state_manager.start_new_hand()
            continue
            
        # Otherwise, take the next game action
        if game.round_complete:
            # If the round is complete, advance to the next phase
            state_manager.advance_phase()
        else:
            # Otherwise, handle the current player's action
            current_player = game.players[game.current_player_idx]
            
            # Skip inactive or all-in players
            if not current_player.is_active or current_player.is_all_in:
                state_manager.state._advance_to_next_player()
                continue
            
            # Determine a simple action for the player
            if game.current_bet == current_player.current_bet:
                # Can check
                state_manager.handle_player_action(current_player.id, PlayerAction.CHECK, 0)
            elif current_player.chips >= (game.current_bet - current_player.current_bet):
                # Can call
                state_manager.handle_player_action(
                    current_player.id,
                    PlayerAction.CALL,
                    game.current_bet - current_player.current_bet
                )
            else:
                # Must fold
                state_manager.handle_player_action(current_player.id, PlayerAction.FOLD, 0)
    
    # Print final results
    print("\n🏆 Game Complete 🏆")
    print("=" * 50)
    
    # Print final chip counts
    print("\nFinal Chip Counts:")
    sorted_players = sorted(state_manager.state.game.players, key=lambda p: p.chips, reverse=True)
    for i, player in enumerate(sorted_players):
        print(f"{i+1}. {player.name}: ${player.chips}")

def format_card(card: Card) -> str:
    """Format a card with unicode symbols"""
    suits = {
        "hearts": "♥️",
        "diamonds": "♦️",
        "clubs": "♣️",
        "spades": "♠️"
    }
    suit_symbol = suits.get(card.suit.value, card.suit.value)
    return f"{card.value.value}{suit_symbol}"

def get_position_name(position: int, num_players: int) -> str:
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

def visualize_game_state(game_state):
    """Visualize the current game state in a human-readable format"""
    print("\n" + "=" * 50)

    # Extract phase
    print(f"🃏 Phase: {game_state.phase.value}")

    print("=" * 50)

    # Community cards
    if game_state.community_cards:
        print("\n🎴 Community Cards:")
        print(" ".join([format_card(card) for card in game_state.community_cards]))
    else:
        print("\n🎴 No community cards yet")
    
    # Pot sizes
    total_pot = sum(pot.amount for pot in game_state.pots)
    print(f"\n💰 Total Pot: ${total_pot}")
    if len(game_state.pots) > 1:
        for i, pot in enumerate(game_state.pots):
            print(f"  {'Main' if i == 0 else f'Side {i}'} Pot: ${pot.amount}")
    
    # Current bet
    print(f"💵 Current bet: ${game_state.current_bet}")
    
    # Players
    print("\n👥 Players:")
    for player in game_state.players:
        is_dealer = "🎮 " if player.position == game_state.dealer_position else ""
        is_current = "➡️ " if game_state.players[game_state.current_player_idx].id == player.id else ""
        position_name = get_position_name(player.position, len(game_state.players))
        
        status = ""
        if not player.is_active:
            status = "folded"
        elif player.is_all_in:
            status = "all-in"
        elif player.current_bet > 0:
            status = f"bet ${player.current_bet}"
        
        highlight = ">" if is_current else " "
        
        print(f"{highlight} {is_dealer}{player.name} ({position_name}): ${player.chips} {status}")
        
        if player.is_active and player.hand and player.hand.cards:
            print(f"   Hand: {' '.join([format_card(card) for card in player.hand.cards])}")
    
    # Recent actions
    if game_state.action_history:
        print("\n🎬 Recent Actions:")
        recent_actions = game_state.action_history[-min(5, len(game_state.action_history)):]
        for action in recent_actions:
            player = next((p for p in game_state.players if p.id == action.player_id), None)
            if player:
                amount_str = f" ${action.amount}" if action.amount > 0 else ""
                print(f"  {player.name} {action.action.value}{amount_str}")

    print("\n" + "-" * 50)

if __name__ == "__main__":
    main()