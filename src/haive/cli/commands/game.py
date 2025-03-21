"""
Game agent commands for Haive CLI.
"""
import os
import sys
import time
import json
import click
import importlib.util
import uuid
from typing import Optional, Dict, Any, List
from rich.panel import Panel
from rich.live import Live
from rich.layout import Layout
from rich.console import Console
from rich.prompt import Prompt

from src.haive.cli.ui.console import create_console
from src.haive.cli.ui.layouts import create_agent_layout
from src.haive.cli.ui.components import create_game_ui
from src.haive.cli.utils.config import get_config
from src.haive.cli.utils.registry import get_agent_path, get_agent_config, get_agent_game_config

console = create_console()

@click.command()
@click.argument('agent_id', required=False)
@click.option('--new-game', '-n', is_flag=True, help='Start a new game')
@click.option('--load', '-l', type=str, help='Load a saved game')
@click.option('--save', '-s', type=str, help='Save game with specified name')
def game(agent_id: Optional[str], new_game: bool, load: Optional[str], save: Optional[str]):
    """Run a game-based agent.
    
    Game agents provide an interactive narrative experience with state tracking.
    """
    if not agent_id:
        agent_id = select_game_agent_interactive()
        if not agent_id:
            console.print("[yellow]Game cancelled[/yellow]")
            return
    
    # Check agent type
    agent_config = get_agent_config(agent_id)
    if agent_config.get('agent_type') != 'game':
        console.print(f"[bold red]Error:[/bold red] Agent '{agent_id}' is not a game agent.")
        return
    
    run_game_agent(agent_id, new_game, load, save)

def select_game_agent_interactive() -> Optional[str]:
    """Show interactive selection for installed game agents."""
    config = get_config()
    installed_agents = config.get('agents', {})
    
    # Filter to only show game agents
    game_agents = {}
    for agent_id, agent_data in installed_agents.items():
        if agent_data.get('agent_type') == 'game':
            game_agents[agent_id] = agent_data
    
    if not game_agents:
        console.print("[yellow]No game agents installed. Use 'haive download' to install agents.[/yellow]")
        return None
    
    # Create agent choices
    choices = []
    agents_list = list(game_agents.items())
    for i, (agent_id, agent_data) in enumerate(agents_list, 1):
        choices.append((
            f"{i}. {agent_data.get('name', agent_id)} - {agent_data.get('description', '')[:50]}...",
            agent_id
        ))
    
    # Add option to cancel
    choices.append(("0. Cancel", None))
    
    # Print choices
    console.print(Panel.fit("\n".join([choice[0] for choice in choices]), 
                            title="Installed Game Agents"))
    
    # Get user selection
    selection = click.prompt("Select a game agent", type=int, default=0)
    
    if selection == 0 or selection > len(agents_list):
        return None
    
    return agents_list[selection-1][0]

def run_game_agent(agent_id: str, new_game: bool, load_game: Optional[str], save_game: Optional[str]):
    """Run a game agent."""
    agent_path = get_agent_path(agent_id)
    agent_config = get_agent_config(agent_id)
    game_config = get_agent_game_config(agent_id)
    
    if not os.path.exists(agent_path):
        console.print(f"[bold red]Error:[/bold red] Agent '{agent_id}' not found.")
        return
    
    if not game_config:
        console.print(f"[bold red]Error:[/bold red] Agent '{agent_id}' does not have game configuration.")
        return
    
    console.print(f"Loading game agent: {agent_config.get('name', agent_id)}")
    
    try:
        # Import the agent module
        spec = importlib.util.spec_from_file_location("game_agent_module", agent_path)
        agent_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(agent_module)
        
        # Get the game agent class
        agent_class = getattr(agent_module, agent_config.get('agent_class', 'GameAgent'))
        agent_instance = agent_class()
        
        # Create a unique session ID
        session_id = str(uuid.uuid4())
        
        # Initialize game state
        if load_game:
            game_state = load_game_state(agent_id, load_game)
            if not game_state:
                console.print(f"[bold red]Error:[/bold red] Could not load saved game '{load_game}'.")
                return
            console.print(f"[green]Loaded saved game: {load_game}[/green]")
        else:
            game_state = initialize_game_state(agent_instance, game_config, new_game, session_id)
        
        # Set up the UI layout
        layout = Layout()
        
        # Run the game
        run_interactive_game(agent_instance, layout, game_state, agent_id, agent_config.get('name', agent_id), save_game)
        
    except Exception as e:
        console.print(f"[bold red]Error running game agent:[/bold red] {str(e)}")
        import traceback
        traceback.print_exc()
        return

def initialize_game_state(agent_instance, game_config: Dict[str, Any], new_game: bool, session_id: str) -> Dict[str, Any]:
    """Initialize game state."""
    # Check if agent instance has initialize_game method
    if hasattr(agent_instance, 'initialize_game'):
        return agent_instance.initialize_game(new_game, session_id)
    
    # Default initialization
    return {
        'game_title': game_config.get('title', 'Adventure Game'),
        'description': game_config.get('initial_description', 'Welcome to the game.'),
        'location': game_config.get('initial_location', 'Start'),
        'inventory': [],
        'status': 'active',
        'turn': 0,
        'session_id': session_id,
        'stats': game_config.get('initial_stats', {}),
        'actions': game_config.get('initial_actions', ['look', 'help'])
    }

def load_game_state(agent_id: str, save_name: str) -> Optional[Dict[str, Any]]:
    """Load a saved game state."""
    from src.haive.cli.utils.config import get_config_dir
    
    save_dir = get_config_dir() / 'saves' / agent_id
    save_path = save_dir / f"{save_name}.json"
    
    if not os.path.exists(save_path):
        return None
    
    try:
        with open(save_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

def save_game_state(agent_id: str, save_name: str, game_state: Dict[str, Any]) -> bool:
    """Save the current game state."""
    import json
    from src.haive.cli.utils.config import get_config_dir
    
    save_dir = get_config_dir() / 'saves' / agent_id
    os.makedirs(save_dir, exist_ok=True)
    
    save_path = save_dir / f"{save_name}.json"
    
    try:
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(game_state, f, indent=2)
        return True
    except Exception:
        return False

def run_interactive_game(agent_instance, layout: Layout, game_state: Dict[str, Any], 
                       agent_id: str, agent_name: str, auto_save: Optional[str]):
    """Run the game in interactive mode."""
    # Set up the UI layout for the game
    layout = create_agent_layout(agent_name, False)
    
    # Initialize the game panel
    game_panel = create_game_ui(game_state, agent_name)
    layout["chat"].update(game_panel)
    
    # Get command processor from agent or use default
    process_command = getattr(agent_instance, 'process_command', default_process_command)
    
    # Main game loop
    with Live(layout, refresh_per_second=4, screen=True):
        while game_state.get('status') != 'game_over':
            # Update the game panel
            game_panel = create_game_ui(game_state, agent_name)
            layout["chat"].update(game_panel)
            
            # Get user input
            command = Prompt.ask("[bold cyan]Enter command[/bold cyan]")
            
            if command.lower() in ['quit', 'exit', 'bye']:
                if auto_save:
                    if save_game_state(agent_id, auto_save, game_state):
                        console.print(f"[green]Game saved as: {auto_save}[/green]")
                    else:
                        console.print("[red]Failed to save game[/red]")
                break
            
            if command.lower().startswith('save ') and len(command) > 5:
                save_name = command[5:].strip()
                if save_game_state(agent_id, save_name, game_state):
                    game_state['message'] = f"Game saved as: {save_name}"
                else:
                    game_state['message'] = "Failed to save game"
                continue
            
            # Process the command
            game_state = process_command(agent_instance, command, game_state)
            
            # Auto-save if specified
            if auto_save:
                save_game_state(agent_id, auto_save, game_state)
    
    # Game over
    if game_state.get('status') == 'game_over':
        game_state['message'] = "Game Over: " + game_state.get('end_message', 'Thanks for playing!')
        game_panel = create_game_ui(game_state, agent_name)
        layout["chat"].update(game_panel)
        time.sleep(2)  # Give the user time to read the game over message

def default_process_command(agent_instance, command: str, game_state: Dict[str, Any]) -> Dict[str, Any]:
    """Default command processor if agent doesn't provide one."""
    # Copy the game state to avoid modifying the original
    new_state = game_state.copy()
    
    # Increment turn counter
    new_state['turn'] = game_state.get('turn', 0) + 1
    
    # Process common commands
    command = command.lower().strip()
    
    if command == 'help':
        new_state['message'] = "Available commands depend on the game. Try: look, inventory, examine, go, take, use, talk"
    elif command == 'look' or command == 'l':
        new_state['message'] = game_state.get('description', 'You see nothing special.')
    elif command == 'inventory' or command == 'i':
        items = game_state.get('inventory', [])
        if items:
            new_state['message'] = f"You are carrying: {', '.join(items)}"
        else:
            new_state['message'] = "You are not carrying anything."
    else:
        new_state['message'] = f"I don't understand '{command}'. Try 'help' for a list of commands."
    
    return new_state