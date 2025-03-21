"""
Console setup for Haive CLI.
"""
from rich.console import Console
from rich.theme import Theme

def create_console() -> Console:
    """Create and configure a Rich console with custom theme."""
    custom_theme = Theme({
        "info": "dim cyan",
        "warning": "yellow",
        "danger": "bold red",
        "success": "bold green",
        "command": "bold cyan",
        "param": "bold yellow",
        "agent": "bold green",
        "user": "bold blue",
        "system": "dim white",
        "error": "red",
    })
    
    return Console(theme=custom_theme, highlight=True)