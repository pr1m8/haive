"""
Reusable UI components for Haive CLI.
"""
from typing import List, Dict, Any, Optional
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.tree import Tree

def create_progress_bar(description: str = "Processing") -> Progress:
    """Create a rich progress bar."""
    return Progress(
        SpinnerColumn(),
        TextColumn(f"[bold blue]{description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        expand=True
    )

def create_agent_card(agent: Dict[str, Any], installed: bool = False) -> Panel:
    """Create a panel displaying agent information."""
    content = Text()
    
    # Add name and version
    content.append(agent.get('name', 'Unknown Agent'), style="bold green")
    content.append(f" (v{agent.get('version', '1.0.0')})", style="cyan")
    content.append("\n\n")
    
    # Add description
    if 'description' in agent:
        content.append(agent['description'])
        content.append("\n\n")
    
    # Add tags
    if 'tags' in agent and agent['tags']:
        content.append("Tags: ", style="dim")
        for i, tag in enumerate(agent['tags']):
            if i > 0:
                content.append(", ")
            content.append(tag, style="bold magenta")
        content.append("\n")
    
    # Add status
    status_style = "bold green" if installed else "bold yellow"
    status_text = "Installed" if installed else "Not Installed"
    content.append(f"\nStatus: ", style="dim")
    content.append(status_text, style=status_style)
    
    # Add agent type if available
    if 'agent_type' in agent:
        content.append(f"\nType: ", style="dim")
        content.append(agent['agent_type'], style="bold blue")
    
    return Panel(
        content,
        title=agent.get('id', 'Agent'),
        border_style="green" if installed else "yellow"
    )

def create_game_ui(game_state: Dict[str, Any], agent_name: str) -> Panel:
    """Create a game UI panel for game-based agents."""
    content = Text()
    
    # Add game title
    if 'game_title' in game_state:
        content.append(f"{game_state['game_title']}\n", style="bold cyan")
        content.append("=" * len(game_state['game_title']) + "\n\n", style="cyan")
    
    # Add current scene/location
    if 'location' in game_state:
        content.append("Location: ", style="dim")
        content.append(f"{game_state['location']}\n\n", style="bold yellow")
    
    # Add description
    if 'description' in game_state:
        content.append(f"{game_state['description']}\n\n")
    
    # Add inventory if available
    if 'inventory' in game_state and game_state['inventory']:
        content.append("Inventory:\n", style="bold blue")
        for item in game_state['inventory']:
            content.append(f"- {item}\n", style="blue")
        content.append("\n")
    
    # Add stats if available
    if 'stats' in game_state and game_state['stats']:
        content.append("Stats:\n", style="bold magenta")
        for stat, value in game_state['stats'].items():
            content.append(f"- {stat}: {value}\n", style="magenta")
        content.append("\n")
    
    # Add available actions
    if 'actions' in game_state and game_state['actions']:
        content.append("Available Actions:\n", style="bold green")
        for action in game_state['actions']:
            content.append(f"- {action}\n", style="green")
    
    return Panel(
        content,
        title=f"Game Agent: {agent_name}",
        border_style="cyan"
    )

def create_decision_tree(decisions: Dict[str, Any], title: str = "Decision Tree") -> Panel:
    """Create a decision tree visualization for reasoning agents."""
    tree = Tree(f"[bold]{title}")
    
    def add_decision_node(node, tree_node):
        if isinstance(node, dict):
            for key, value in node.items():
                if key == 'decision':
                    tree_node.add(f"[bold green]Decision: {value}")
                elif key == 'reason':
                    tree_node.add(f"[yellow]Reason: {value}")
                elif key == 'confidence':
                    tree_node.add(f"[blue]Confidence: {value*100:.1f}%")
                elif key == 'alternatives':
                    alt_node = tree_node.add("[bold red]Alternatives:")
                    for alt in value:
                        alt_item = alt_node.add(f"[red]{alt.get('option', 'Unknown')}")
                        if 'reason' in alt:
                            alt_item.add(f"[yellow]Reason: {alt['reason']}")
                        if 'confidence' in alt:
                            alt_item.add(f"[blue]Confidence: {alt['confidence']*100:.1f}%")
                elif key == 'steps':
                    steps_node = tree_node.add("[bold cyan]Steps:")
                    for i, step in enumerate(value, 1):
                        steps_node.add(f"[cyan]{i}. {step}")
                elif key == 'children':
                    for child_key, child_value in value.items():
                        child_node = tree_node.add(f"[bold]{child_key}")
                        add_decision_node(child_value, child_node)
                else:
                    child_node = tree_node.add(f"[bold]{key}")
                    add_decision_node(value, child_node)
        elif isinstance(node, list):
            for item in node:
                if isinstance(item, (dict, list)):
                    add_decision_node(item, tree_node)
                else:
                    tree_node.add(str(item))
        else:
            tree_node.add(str(node))
    
    add_decision_node(decisions, tree)
    
    return Panel(
        tree,
        title=title,
        border_style="blue"
    )

def create_agent_grid(agents: List[Dict[str, Any]], columns: int = 2) -> Table:
    """Create a grid display of multiple agents."""
    table = Table.grid(padding=1, expand=True)
    
    # Add columns
    for _ in range(columns):
        table.add_column()
    
    # Add rows
    row = []
    for i, agent in enumerate(agents):
        row.append(create_agent_card(agent, agent.get('installed', False)))
        
        # Complete the row or at the end
        if (i + 1) % columns == 0 or i == len(agents) - 1:
            # Fill empty cells
            while len(row) < columns:
                row.append("")
            
            table.add_row(*row)
            row = []
    
    return table

def create_chat_bubble(message: Dict[str, str], timestamp: Optional[str] = None) -> Panel:
    """Create a chat bubble for message display."""
    role = message.get('role', 'unknown')
    content = message.get('content', '')
    
    style_map = {
        'user': {'border': 'blue', 'title_style': 'bold blue', 'title': 'You'},
        'assistant': {'border': 'green', 'title_style': 'bold green', 'title': 'Assistant'},
        'system': {'border': 'dim', 'title_style': 'dim', 'title': 'System'},
        'error': {'border': 'red', 'title_style': 'bold red', 'title': 'Error'}
    }
    
    style = style_map.get(role, {'border': 'white', 'title_style': 'bold', 'title': role.capitalize()})
    
    # Add timestamp to subtitle if provided
    subtitle = timestamp if timestamp else None
    
    return Panel(
        content,
        title=style['title'],
        title_align="left",
        subtitle=subtitle,
        subtitle_align="right",
        border_style=style['border'],
        title_style=style['title_style']
    )