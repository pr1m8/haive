"""
UI layouts for Haive CLI.
"""
from typing import Dict, Any, List
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.console import Group
from rich.table import Table

def create_agent_layout(agent_name: str, debug_mode: bool = False) -> Layout:
    """Create a layout for the agent run view."""
    layout = Layout()
    
    # Split the layout into header and body
    layout.split(
        Layout(name="header", size=3),
        Layout(name="body")
    )
    
    # Create the header
    header_text = Text()
    header_text.append(f"Agent: ", style="dim")
    header_text.append(agent_name, style="bold green")
    
    header_panel = Panel(
        header_text,
        title="Haive CLI",
        title_align="left",
        subtitle="Press Ctrl+C to exit",
        subtitle_align="right"
    )
    
    layout["header"].update(header_panel)
    
    # Split the body based on debug mode
    if debug_mode:
        layout["body"].split_row(
            Layout(name="chat", ratio=2),
            Layout(name="debug", ratio=1)
        )
        
        # Initialize debug panel
        debug_panel = Panel(
            Text("Initializing...", style="dim"),
            title="Agent State",
            border_style="blue"
        )
        layout["debug"].update(debug_panel)
    else:
        layout["body"].update(Layout(name="chat"))
    
    # Initialize chat panel
    chat_panel = Panel(
        Text("Starting conversation...", style="dim"),
        title="Conversation",
        border_style="green",
        expand=True
    )
    layout["chat"].update(chat_panel)
    
    return layout

def update_chat_panel(layout: Layout, messages: List[Dict[str, str]]):
    """Update the chat panel with new messages."""
    message_groups = []
    
    for msg in messages:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        
        if role == "system":
            message_groups.append(Text(f"System: {content}", style="dim"))
        elif role == "user":
            text = Text()
            text.append("You: ", style="bold blue")
            text.append(content)
            message_groups.append(text)
        elif role == "assistant":
            text = Text()
            text.append("Agent: ", style="bold green")
            
            # Try rendering as markdown if it looks like markdown
            if "```" in content or "**" in content or "#" in content:
                try:
                    message_groups.append(text)
                    message_groups.append(Markdown(content))
                    continue
                except Exception:
                    # Fallback to plain text
                    pass
            
            text.append(content)
            message_groups.append(text)
        elif role == "error":
            text = Text()
            text.append("Error: ", style="bold red")
            text.append(content, style="red")
            message_groups.append(text)
        else:
            text = Text()
            text.append(f"{role.capitalize()}: ", style="bold")
            text.append(content)
            message_groups.append(text)
        
        # Add separator
        message_groups.append(Text(""))
    
    # Update the chat panel
    layout["chat"].update(
        Panel(
            Group(*message_groups),
            title="Conversation",
            border_style="green",
            expand=True
        )
    )

def update_state_panel(layout: Layout, state: Dict[str, Any]):
    """Update the debug panel with the current state."""
    if "debug" not in layout:
        return
    
    # Format the state for display
    state_table = Table(show_header=True, header_style="bold cyan", box=None)
    state_table.add_column("Key")
    state_table.add_column("Value")
    
    # Add rows for primitive values
    for key, value in state.items():
        if isinstance(value, (str, int, float, bool)) or value is None:
            # Truncate long strings
            if isinstance(value, str) and len(value) > 50:
                value = value[:47] + "..."
            state_table.add_row(key, str(value))
    
    # Format complex objects
    objects_text = []
    for key, value in state.items():
        if isinstance(value, (dict, list)) and value:
            import json
            objects_text.append(Text(f"{key}:", style="bold"))
            try:
                json_str = json.dumps(value, indent=2)
                objects_text.append(Syntax(json_str, "json", theme="monokai", line_numbers=False))
            except Exception:
                objects_text.append(Text(str(value)))
            objects_text.append(Text(""))
    
    # Combine table and objects
    if objects_text:
        layout["debug"].update(
            Panel(
                Group(state_table, *objects_text),
                title="Agent State",
                border_style="blue"
            )
        )
    else:
        layout["debug"].update(
            Panel(
                state_table,
                title="Agent State",
                border_style="blue"
            )
        )