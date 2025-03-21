"""
List installed agents for Haive CLI.
"""
import os
import click
from rich.table import Table

from src.haive.cli.ui.console import create_console
from src.haive.cli.utils.config import get_config
from src.haive.cli.utils.registry import get_agent_path

console = create_console()

@click.command(name="list")
@click.option('--verbose', '-v', is_flag=True, help='Show detailed information')
def list_agents(verbose: bool):
    """List all installed agents."""
    config = get_config()
    agents = config.get('agents', {})
    
    if not agents:
        console.print("[yellow]No agents installed. Use 'haive download' to install agents.[/yellow]")
        return
    
    table = Table(title="Installed Agents")
    
    # Basic columns
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Version", style="magenta")
    
    # Add verbose columns
    if verbose:
        table.add_column("Description")
        table.add_column("Path", style="dim")
        table.add_column("Tags")
    
    # Add rows for each agent
    for agent_id, agent_data in agents.items():
        row = [
            agent_id,
            agent_data.get('name', agent_id),
            agent_data.get('version', '1.0.0')
        ]
        
        if verbose:
            path = get_agent_path(agent_id)
            exists = "✓" if os.path.exists(path) else "✗"
            
            row.extend([
                agent_data.get('description', ''),
                f"{path} [{exists}]",
                ", ".join(agent_data.get('tags', []))
            ])
        
        table.add_row(*row)
    
    console.print(table)
    
    # Show usage hint
    console.print("\nTo run an agent: [cyan]haive run AGENT_ID[/cyan]")