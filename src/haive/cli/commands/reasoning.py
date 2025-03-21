"""
Reasoning agent commands for Haive CLI.
"""
import os
import sys
import time
import click
import importlib.util
import uuid
from typing import Optional, Dict, Any, List
from rich.panel import Panel
from rich.live import Live
from rich.layout import Layout
from rich.console import Console
from rich.markdown import Markdown

from src.haive.cli.ui.console import create_console
from src.haive.cli.ui.layouts import create_agent_layout
from src.haive.cli.ui.components import create_decision_tree
from src.haive.cli.utils.config import get_config
from src.haive.cli.utils.registry import get_agent_path, get_agent_config
from rich.syntax import Syntax
console = create_console()

@click.command()
@click.argument('agent_id', required=False)
@click.option('--query', '-q', help='Question or problem to solve')
@click.option('--verbose/--no-verbose', default=True, help='Show reasoning steps')
@click.option('--format', '-f', type=click.Choice(['text', 'tree', 'json']), default='tree', 
              help='Format for displaying reasoning')
def reasoning(agent_id: Optional[str], query: Optional[str], verbose: bool, format: str):
    """Run a reasoning agent showing decision process.
    
    Reasoning agents provide step-by-step explanations of their thinking.
    """
    if not agent_id:
        agent_id = select_reasoning_agent_interactive()
        if not agent_id:
            console.print("[yellow]Reasoning process cancelled[/yellow]")
            return
    
    # Check agent type
    agent_config = get_agent_config(agent_id)
    if agent_config.get('agent_type') != 'reasoning':
        console.print(f"[bold red]Error:[/bold red] Agent '{agent_id}' is not a reasoning agent.")
        return
    
    run_reasoning_agent(agent_id, query, verbose, format)

def select_reasoning_agent_interactive() -> Optional[str]:
    """Show interactive selection for installed reasoning agents."""
    config = get_config()
    installed_agents = config.get('agents', {})
    
    # Filter to only show reasoning agents
    reasoning_agents = {}
    for agent_id, agent_data in installed_agents.items():
        if agent_data.get('agent_type') == 'reasoning':
            reasoning_agents[agent_id] = agent_data
    
    if not reasoning_agents:
        console.print("[yellow]No reasoning agents installed. Use 'haive download' to install agents.[/yellow]")
        return None
    
    # Create agent choices
    choices = []
    agents_list = list(reasoning_agents.items())
    for i, (agent_id, agent_data) in enumerate(agents_list, 1):
        choices.append((
            f"{i}. {agent_data.get('name', agent_id)} - {agent_data.get('description', '')[:50]}...",
            agent_id
        ))
    
    # Add option to cancel
    choices.append(("0. Cancel", None))
    
    # Print choices
    console.print(Panel.fit("\n".join([choice[0] for choice in choices]), 
                            title="Installed Reasoning Agents"))
    
    # Get user selection
    selection = click.prompt("Select a reasoning agent", type=int, default=0)
    
    if selection == 0 or selection > len(agents_list):
        return None
    
    return agents_list[selection-1][0]

def run_reasoning_agent(agent_id: str, initial_query: Optional[str], verbose: bool, format_type: str):
    """Run a reasoning agent."""
    agent_path = get_agent_path(agent_id)
    agent_config = get_agent_config(agent_id)
    
    if not os.path.exists(agent_path):
        console.print(f"[bold red]Error:[/bold red] Agent '{agent_id}' not found.")
        return
    
    console.print(f"Loading reasoning agent: {agent_config.get('name', agent_id)}")
    
    try:
        # Import the agent module
        spec = importlib.util.spec_from_file_location("reasoning_agent_module", agent_path)
        agent_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(agent_module)
        
        # Get the reasoning agent class
        agent_class = getattr(agent_module, agent_config.get('agent_class', 'ReasoningAgent'))
        agent_instance = agent_class()
        
        # Create a unique session ID
        session_id = str(uuid.uuid4())
        
        # Get query from user if not provided
        query = initial_query
        if not query:
            query = click.prompt("Enter your question or problem", type=str)
        
        # Set up the UI layout
        layout = create_agent_layout(
            agent_name=agent_config.get('name', agent_id),
            debug_mode=verbose
        )
        
        # Run the reasoning agent
        run_reasoning_process(agent_instance, layout, query, verbose, format_type, session_id)
        
    except Exception as e:
        console.print(f"[bold red]Error running reasoning agent:[/bold red] {str(e)}")
        import traceback
        traceback.print_exc()
        return

def run_reasoning_process(agent_instance, layout: Layout, query: str, verbose: bool, 
                         format_type: str, session_id: str):
    """Run the reasoning process."""
    # Update initial state in the layout
    if verbose:
        update_state_panel(layout, {"status": "Reasoning", "query": query, "session_id": session_id})
    
    # Update the query in the chat panel
    messages = [
        {"role": "user", "content": query}
    ]
    update_chat_panel(layout, messages)
    
    # Check if agent has specific reasoning method
    if hasattr(agent_instance, 'process_with_reasoning'):
        reasoning_method = agent_instance.process_with_reasoning
    else:
        reasoning_method = lambda q, s: agent_instance.run(q, thread_id=s)
    
    # Start the reasoning process with live updates
    with Live(layout, refresh_per_second=2):
        # Process the query with reasoning
        result = reasoning_method(query, session_id)
        
        # Update the debug panel if verbose mode
        if verbose:
            update_state_panel(layout, result)
        
        # Extract reasoning steps and answer
        reasoning_data = extract_reasoning_data(result)
        answer = extract_answer(result)
        
        # Display the reasoning based on format
        if format_type == 'tree' and reasoning_data:
            reasoning_display = create_decision_tree(reasoning_data, "Reasoning Process")
        elif format_type == 'json' and reasoning_data:
            import json
            reasoning_display = Panel(
                Syntax(json.dumps(reasoning_data, indent=2), "json", theme="monokai"),
                title="Reasoning Process",
                border_style="blue"
            )
        else:
            # Default to text format
            reasoning_text = format_reasoning_as_text(reasoning_data)
            reasoning_display = Panel(
                Markdown(reasoning_text),
                title="Reasoning Process",
                border_style="blue"
            )
        
        # Update the panels
        layout["chat"].update(
            Panel(
                Markdown(f"**Question:** {query}\n\n**Answer:** {answer}"),
                title="Results",
                border_style="green"
            )
        )
        
        if verbose:
            layout["debug"].update(reasoning_display)
        else:
            # If not verbose, show reasoning in chat panel
            messages.append({"role": "assistant", "content": answer})
            if reasoning_data:
                messages.append({"role": "system", "content": "Reasoning process:"})
                messages.append({"role": "system", "content": format_reasoning_as_text(reasoning_data)})
            update_chat_panel(layout, messages)

def update_state_panel(layout: Layout, state: Dict[str, Any]):
    """Update the debug panel with the current state."""
    if "debug" not in layout:
        return
    
    # Format the state for display - simplified version, the full implementation 
    # would be in the layouts.py module
    from rich.table import Table
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
    
    layout["debug"].update(
        Panel(
            state_table,
            title="State",
            border_style="blue"
        )
    )

def update_chat_panel(layout: Layout, messages: List[Dict[str, str]]):
    """Update the chat panel with new messages - placeholder."""
    from rich.markdown import Markdown
    from rich.console import Group
    from rich.text import Text
    
    message_parts = []
    
    for msg in messages:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        
        if role == "user":
            message_parts.append(Text("You:", style="bold blue"))
            message_parts.append(Markdown(content))
        elif role == "assistant":
            message_parts.append(Text("Assistant:", style="bold green"))
            message_parts.append(Markdown(content))
        elif role == "system":
            message_parts.append(Text("System:", style="dim"))
            message_parts.append(Markdown(content))
        else:
            message_parts.append(Text(f"{role.capitalize()}:", style="bold"))
            message_parts.append(Markdown(content))
        
        message_parts.append(Text(""))  # Empty line as separator
    
    layout["chat"].update(
        Panel(
            Group(*message_parts),
            title="Conversation",
            border_style="green"
        )
    )

def extract_reasoning_data(result: Any) -> Dict[str, Any]:
    """Extract reasoning data from the result."""
    if isinstance(result, dict):
        # Look for reasoning-related fields
        for field in ['reasoning', 'reasoning_steps', 'thinking', 'steps', 'chain_of_thought']:
            if field in result:
                return result[field]
        
        # Look for nested fields
        for key, value in result.items():
            if key in ['state', 'reasoning_state', 'thinking_process'] and isinstance(value, dict):
                return value
    
    # Default empty reasoning
    return {}

def extract_answer(result: Any) -> str:
    """Extract the final answer from the result."""
    if isinstance(result, str):
        return result
    
    if isinstance(result, dict):
        # Common answer fields
        for field in ['answer', 'response', 'output', 'conclusion']:
            if field in result:
                return str(result[field])
        
        # Check for messages
        if 'messages' in result:
            messages = result['messages']
            if messages and len(messages) > 0:
                last_message = messages[-1]
                if hasattr(last_message, 'content'):
                    return last_message.content
                elif isinstance(last_message, tuple) and len(last_message) > 1:
                    return last_message[1]
                elif isinstance(last_message, dict) and 'content' in last_message:
                    return last_message['content']
    
    # Fallback
    return str(result)

def format_reasoning_as_text(reasoning_data: Dict[str, Any]) -> str:
    """Format reasoning data as markdown text."""
    if not reasoning_data:
        return "No detailed reasoning provided."
    
    # Convert reasoning data to markdown
    markdown = []
    
    # Handle different reasoning formats
    if 'steps' in reasoning_data and isinstance(reasoning_data['steps'], list):
        markdown.append("## Reasoning Steps\n")
        for i, step in enumerate(reasoning_data['steps'], 1):
            if isinstance(step, str):
                markdown.append(f"{i}. {step}\n")
            elif isinstance(step, dict) and 'description' in step:
                markdown.append(f"{i}. **{step.get('name', 'Step')}**: {step['description']}\n")
    
    elif 'thoughts' in reasoning_data and isinstance(reasoning_data['thoughts'], list):
        markdown.append("## Thinking Process\n")
        for i, thought in enumerate(reasoning_data['thoughts'], 1):
            markdown.append(f"{i}. {thought}\n")
    
    # Add conclusion if available
    if 'conclusion' in reasoning_data:
        markdown.append("\n## Conclusion\n")
        markdown.append(reasoning_data['conclusion'])
    
    # Add confidence if available
    if 'confidence' in reasoning_data:
        confidence = reasoning_data['confidence']
        if isinstance(confidence, (int, float)):
            confidence_percent = f"{confidence*100:.1f}%" if confidence <= 1 else f"{confidence:.1f}%"
            markdown.append(f"\n**Confidence**: {confidence_percent}")
    
    return "\n".join(markdown)