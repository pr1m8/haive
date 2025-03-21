#!/usr/bin/env python
"""
Haive CLI - Command-line interface for downloading and running agents.
"""
import os
import sys
import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Add src to path if running from repo
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
if os.path.exists(os.path.join(repo_root, 'src')):
    sys.path.insert(0, repo_root)

from src.haive.cli.commands.download import download
from src.haive.cli.commands.run import run
from src.haive.cli.commands.list import list_agents
from src.haive.cli.ui.console import create_console
from src.haive.cli.utils.config import init_config, get_config_path

# Initialize console
console = create_console()

@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option(version='0.1.0', prog_name='haive')
def cli():
    """Haive CLI - Download and run AI agents with rich UI."""
    # Initialize configuration on first run
    if not os.path.exists(get_config_path()):
        init_config()
        console.print(Panel.fit(
            "[yellow]Welcome to Haive CLI![/yellow]\nConfiguration initialized at: " + 
            get_config_path(), 
            title="First Run"
        ))
    
    # Display header
    header = Text()
    header.append("HAIVE CLI", style="bold cyan")
    header.append(" - Agent Management Interface", style="dim")
    console.print(header)

# Import additional commands
from src.haive.cli.commands.create import create
from src.haive.cli.commands.game import game
from src.haive.cli.commands.reasoning import reasoning

# Register commands
cli.add_command(download)
cli.add_command(run)
cli.add_command(list_agents)
cli.add_command(create)
cli.add_command(game)
cli.add_command(reasoning)

if __name__ == '__main__':
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        if "--debug" in sys.argv:
            console.print_exception()
        sys.exit(1)