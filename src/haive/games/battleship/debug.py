#!/usr/bin/env python
"""
Debug script for testing Battleship game.
"""
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.traceback import install
from rich.table import Table

from src.haive.games.battleship.agent import BattleshipAgent
from src.haive.games.battleship.config import BattleshipAgentConfig
from src.haive.games.battleship.utils import visualize_board
from src.haive.games.battleship.models import GamePhase

# Enable rich traceback for better debugging
install()
console = Console()

def test_battleship():
    """Run a test game of Battleship with detailed logging."""
    console.rule("[bold blue]Battleship Game Debug Test")
    console.print("Initializing game agent...")
    
    # Create configuration with debugging enabled
    config = BattleshipAgentConfig(
        name="battleship_debug",
        enable_analysis=True,
        visualize_board=True,
        debug=True
    )
    
    try:
        # Create agent
        agent = BattleshipAgent(config)
        console.print("[green]Agent initialized successfully![/green]")
        
        # Run the game step by step
        step_count = 0
        for state in agent.app.stream({}, stream_mode="values", debug=True, config=agent.runnable_config):
            step_count += 1
            
            # Display step information
            console.rule(f"[bold cyan]Step {step_count}")
            
            # Basic game state
            phase = state.get('game_phase', 'unknown')
            current_player = state.get('current_player', 'unknown')
            winner = state.get('winner', None)
            
            # Create status table
            status = Table(title="Game Status")
            status.add_column("Phase")
            status.add_column("Current Player")
            status.add_column("Winner")
            status.add_row(
                f"[bold]{phase}[/bold]", 
                f"[bold]{current_player}[/bold]", 
                f"[bold green]{winner}[/bold green]" if winner else "None"
            )
            console.print(status)
            
            # Display error if any
            if 'error_message' in state and state['error_message']:
                console.print(Panel(
                    f"[bold red]{state['error_message']}[/bold red]",
                    title="ERROR",
                    border_style="red"
                ))
            
            # Phase-specific displays
            if phase == 'setup':
                player1_placed = state.get('player1_state', {}).get('has_placed_ships', False)
                player2_placed = state.get('player2_state', {}).get('has_placed_ships', False)
                
                setup_status = Table(title="Setup Status")
                setup_status.add_column("Player")
                setup_status.add_column("Ships Placed")
                setup_status.add_row(
                    "Player 1", 
                    "[green]Yes[/green]" if player1_placed else "[red]No[/red]"
                )
                setup_status.add_row(
                    "Player 2", 
                    "[green]Yes[/green]" if player2_placed else "[red]No[/red]"
                )
                console.print(setup_status)
                
                # Display ship placements if available
                if player1_placed or player2_placed:
                    ships_table = Table(title="Ship Placements")
                    ships_table.add_column("Player")
                    ships_table.add_column("Ship Type")
                    ships_table.add_column("Coordinates")
                    
                    if player1_placed:
                        placements = state.get('player1_state', {}).get('ship_placements', [])
                        for placement in placements:
                            ships_table.add_row(
                                "Player 1",
                                str(placement.get('ship_type', 'Unknown')),
                                str([f"({c.get('row', '?')},{c.get('col', '?')})" 
                                     for c in placement.get('coordinates', [])])
                            )
                    
                    if player2_placed:
                        placements = state.get('player2_state', {}).get('ship_placements', [])
                        for placement in placements:
                            ships_table.add_row(
                                "Player 2",
                                str(placement.get('ship_type', 'Unknown')),
                                str([f"({c.get('row', '?')},{c.get('col', '?')})" 
                                     for c in placement.get('coordinates', [])])
                            )
                    
                    console.print(ships_table)
            
            elif phase == 'playing':
                # Display move history
                move_history = state.get('move_history', [])
                if move_history:
                    moves_table = Table(title="Recent Moves")
                    moves_table.add_column("Player")
                    moves_table.add_column("Target")
                    moves_table.add_column("Result")
                    
                    # Display the last 5 moves
                    for player, result in move_history[-5:]:
                        result_text = result.get('result', 'unknown')
                        result_style = {
                            'hit': '[bold green]HIT[/bold green]',
                            'miss': '[bold red]MISS[/bold red]',
                            'sunk': '[bold yellow]SUNK[/bold yellow]',
                            'invalid': '[bold orange]INVALID[/bold orange]'
                        }.get(result_text, result_text)
                        
                        moves_table.add_row(
                            player,
                            f"({result.get('row', '?')}, {result.get('col', '?')})",
                            result_style
                        )
                    
                    console.print(moves_table)
                
                # Display strategic analysis if available
                player1_analysis = state.get('player1_state', {}).get('strategic_analysis', [])
                player2_analysis = state.get('player2_state', {}).get('strategic_analysis', [])
                
                if player1_analysis or player2_analysis:
                    analysis_table = Table(title="Strategic Analysis")
                    analysis_table.add_column("Player")
                    analysis_table.add_column("Analysis")
                    
                    if player1_analysis:
                        latest = player1_analysis[-1] if player1_analysis else ""
                        analysis_table.add_row(
                            "Player 1",
                            latest[:100] + "..." if len(latest) > 100 else latest
                        )
                    
                    if player2_analysis:
                        latest = player2_analysis[-1] if player2_analysis else ""
                        analysis_table.add_row(
                            "Player 2",
                            latest[:100] + "..." if len(latest) > 100 else latest
                        )
                    
                    console.print(analysis_table)
            
            # Game over display
            elif phase == 'ended':
                console.print(Panel(
                    f"[bold green]Game Over! Winner: {winner}[/bold green]",
                    title="🏆 VICTORY 🏆",
                    border_style="green"
                ))
            
            # Brief pause between steps
            time.sleep(0.5)
        
        # Final game summary
        console.rule("[bold green]Game Complete")
        console.print(f"Total steps: {step_count}")
    
    except Exception as e:
        console.print_exception()
        console.print(f"[bold red]Error:[/bold red] {str(e)}")

if __name__ == "__main__":
    test_battleship()