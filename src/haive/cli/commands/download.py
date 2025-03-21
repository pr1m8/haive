"""
Agent download command for Haive CLI.
"""
import os
import sys
import time
import click
import requests
from typing import Optional, Dict, Any, List
from rich.progress import Progress, TextColumn, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn
from rich.panel import Panel

from src.haive.cli.ui.console import create_console
from src.haive.cli.utils.config import get_config, update_config
from src.haive.cli.utils.registry import register_agent, get_agent_path

console = create_console()

AGENT_REGISTRY_URL = "https://api.haive.ai/registry/agents"  # Example URL

@click.command()
@click.argument('agent_id', required=False)
@click.option('--list', '-l', is_flag=True, help='List available agents from registry')
@click.option('--force', '-f', is_flag=True, help='Force download even if agent exists')
@click.option('--token', '-t', help='API token for private agents')
def download(agent_id: Optional[str], list: bool, force: bool, token: Optional[str]):
    """Download an agent from the registry.
    
    If no AGENT_ID is provided and --list is not specified, interactive selection will be shown.
    """
    if list:
        list_available_agents(token)
        return
    
    if not agent_id:
        agent_id = select_agent_interactive(token)
        if not agent_id:
            console.print("[yellow]Download cancelled[/yellow]")
            return
    
    download_agent(agent_id, force, token)

def list_available_agents(token: Optional[str]):
    """List all available agents from the registry."""
    console.print("Fetching available agents...")
    
    try:
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        response = requests.get(AGENT_REGISTRY_URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        agents = response.json()
        
        if not agents:
            console.print("[yellow]No agents available in the registry[/yellow]")
            return
        
        from rich.table import Table
        table = Table(title="Available Agents")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Description")
        table.add_column("Version", style="magenta")
        table.add_column("Size", style="blue")
        
        for agent in agents:
            table.add_row(
                agent['id'],
                agent['name'],
                agent.get('description', ''),
                agent.get('version', '1.0.0'),
                format_size(agent.get('size_bytes', 0))
            )
        
        console.print(table)
        
    except requests.RequestException as e:
        console.print(f"[bold red]Error fetching agents:[/bold red] {str(e)}")
        sys.exit(1)

def select_agent_interactive(token: Optional[str]) -> Optional[str]:
    """Show interactive selection for agents."""
    try:
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        response = requests.get(AGENT_REGISTRY_URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        agents = response.json()
        
        if not agents:
            console.print("[yellow]No agents available in the registry[/yellow]")
            return None
        
        # Create agent choices
        choices = []
        for i, agent in enumerate(agents, 1):
            choices.append((
                f"{i}. {agent['name']} - {agent.get('description', '')[:50]}...",
                agent['id']
            ))
        
        # Add option to cancel
        choices.append(("0. Cancel", None))
        
        # Print choices
        console.print(Panel.fit("\n".join([choice[0] for choice in choices]), 
                                title="Available Agents"))
        
        # Get user selection
        selection = click.prompt("Select an agent to download", type=int, default=0)
        
        if selection == 0 or selection > len(agents):
            return None
        
        return agents[selection-1]['id']
        
    except requests.RequestException as e:
        console.print(f"[bold red]Error fetching agents:[/bold red] {str(e)}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        return None

def download_agent(agent_id: str, force: bool, token: Optional[str]):
    """Download an agent by ID."""
    # Check if agent already exists
    agent_path = get_agent_path(agent_id)
    
    if os.path.exists(agent_path) and not force:
        console.print(f"[yellow]Agent '{agent_id}' already exists.[/yellow] Use --force to download again.")
        return
    
    console.print(f"Fetching agent metadata for '{agent_id}'...")
    
    try:
        # Get agent metadata
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        response = requests.get(f"{AGENT_REGISTRY_URL}/{agent_id}", headers=headers, timeout=10)
        response.raise_for_status()
        
        agent_data = response.json()
        download_url = agent_data.get('download_url')
        
        if not download_url:
            console.print("[bold red]Error:[/bold red] Agent has no download URL")
            return
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(agent_path), exist_ok=True)
        
        # Download the agent
        console.print(f"Downloading agent: {agent_data['name']} (v{agent_data.get('version', '1.0.0')})")
        
        with Progress(
            TextColumn("[bold blue]Downloading...", justify="right"),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            DownloadColumn(),
            "•",
            TransferSpeedColumn(),
            "•",
            TimeRemainingColumn(),
        ) as progress:
            task = progress.add_task("Downloading", total=int(agent_data.get('size_bytes', 1000000)))
            
            with requests.get(download_url, headers=headers, stream=True) as r:
                r.raise_for_status()
                with open(agent_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            progress.update(task, advance=len(chunk))
        
        # Register the agent
        register_agent(agent_id, agent_data)
        
        console.print(f"[bold green]Successfully downloaded agent:[/bold green] {agent_data['name']}")
        console.print(f"Run with: [cyan]haive run {agent_id}[/cyan]")
        
    except requests.RequestException as e:
        console.print(f"[bold red]Error downloading agent:[/bold red] {str(e)}")
        # Clean up partial download
        if os.path.exists(agent_path):
            os.remove(agent_path)
        sys.exit(1)

def format_size(size_bytes: int) -> str:
    """Format size in bytes to human readable format."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024**2:
        return f"{size_bytes/1024:.1f} KB"
    elif size_bytes < 1024**3:
        return f"{size_bytes/(1024**2):.1f} MB"
    else:
        return f"{size_bytes/(1024**3):.1f} GB"