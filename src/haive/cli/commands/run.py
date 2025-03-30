"""
Agent run command for Haive CLI.
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
from rich.table import Table
from rich.syntax import Syntax
from rich.markdown import Markdown

from src.haive.cli.ui.console import create_console
from src.haive.cli.ui.layouts import create_agent_layout, update_chat_panel, update_state_panel
from src.haive.cli.utils.config import get_config
from src.haive.cli.utils.registry import get_agent_path, get_agent_config
from src.haive.core.engine.agent.agent import Agent

console = create_console()

@click.command()
@click.argument('agent_id', required=False)
@click.option('--input', '-i', help='Input text to send to the agent')
@click.option('--interactive/--non-interactive', default=True, help='Run in interactive mode')
@click.option('--debug/--no-debug', default=False, help='Run in debug mode to see state')
@click.option('--params', '-p', multiple=True, help='Parameters to pass to the agent (format: key=value)')
def run(agent_id: Optional[str], input: Optional[str], interactive: bool, debug: bool, params: List[str]):
    """Run an agent from the local registry.
    
    If no AGENT_ID is provided, interactive selection will be shown.
    """
    if not agent_id:
        agent_id = select_agent_interactive()
        if not agent_id:
            console.print("[yellow]Run cancelled[/yellow]")
            return
    
    # Convert params list to dictionary
    parameters = {}
    for param in params:
        if '=' in param:
            key, value = param.split('=', 1)
            parameters[key] = value
    
    run_agent(agent_id, input, interactive, debug, parameters)

def select_agent_interactive() -> Optional[str]:
    """Show interactive selection for installed agents."""
    config = get_config()
    installed_agents = config.get('agents', {})
    
    if not installed_agents:
        console.print("[yellow]No agents installed. Use 'haive download' to install agents.[/yellow]")
        return None
    
    # Create agent choices
    choices = []
    agents_list = list(installed_agents.items())
    for i, (agent_id, agent_data) in enumerate(agents_list, 1):
        choices.append((
            f"{i}. {agent_data.get('name', agent_id)} - {agent_data.get('description', '')[:50]}...",
            agent_id
        ))
    
    # Add option to cancel
    choices.append(("0. Cancel", None))
    
    # Print choices
    console.print(Panel.fit("\n".join([choice[0] for choice in choices]), 
                            title="Installed Agents"))
    
    # Get user selection
    selection = click.prompt("Select an agent to run", type=int, default=0)
    
    if selection == 0 or selection > len(agents_list):
        return None
    
    return agents_list[selection-1][0]

def run_agent(agent_id: str, initial_input: Optional[str], interactive: bool, debug: bool, parameters: Dict[str, str]):
    """Run an agent by ID."""
    agent_path = get_agent_path(agent_id)
    agent_config = get_agent_config(agent_id)
    
    if not os.path.exists(agent_path):
        console.print(f"[bold red]Error:[/bold red] Agent '{agent_id}' not found. Use 'haive download {agent_id}' to install it.")
        return
    
    console.print(f"Loading agent: {agent_config.get('name', agent_id)}")
    
    try:
        # Import the agent module
        spec = importlib.util.spec_from_file_location("agent_module", agent_path)
        agent_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(agent_module)
        
        # Get the agent class and instantiate it
        agent_class = getattr(agent_module, agent_config.get('agent_class', 'Agent'))
        agent_instance = agent_class()
        
        # Create a unique thread ID for this run
        thread_id = str(uuid.uuid4())
        
        # Set up the UI layout
        layout = create_agent_layout(
            agent_name=agent_config.get('name', agent_id),
            debug_mode=debug
        )
        
        # Update initial state
        if debug:
            update_state_panel(layout, {"status": "Initializing", "thread_id": thread_id})
        
        # Run the agent in interactive mode
        if interactive:
            run_interactive(agent_instance, layout, debug, thread_id, initial_input, parameters)
        else:
            # Non-interactive mode
            if not initial_input:
                console.print("[bold red]Error:[/bold red] Input is required in non-interactive mode.")
                return
            
            console.print("Running agent in non-interactive mode...")
            response = agent_instance.run(
                initial_input,
                thread_id=thread_id,
                **parameters
            )
            
            # Print the response
            output = response.get('output', str(response))
            console.print(Panel.fit(output, title="Agent Response"))
            
    except Exception as e:
        console.print(f"[bold red]Error running agent:[/bold red] {str(e)}")
        if debug:
            console.print_exception()
        return

def run_interactive(agent_instance: Agent, layout: Layout, debug: bool, thread_id: str, 
                   initial_input: Optional[str], parameters: Dict[str, str]):
    """Run the agent in interactive mode."""
    messages = []
    
    # Add initial system message
    if hasattr(agent_instance, 'config') and hasattr(agent_instance.config, 'system_prompt'):
        messages.append({"role": "system", "content": agent_instance.config.system_prompt})
    
    # Add initial user message if provided
    if initial_input:
        messages.append({"role": "user", "content": initial_input})
        update_chat_panel(layout, messages)
    
    with Live(layout, refresh_per_second=10, screen=True):
        # Process initial input if provided
        if initial_input:
            try:
                response = agent_instance.run(
                    initial_input,
                    thread_id=thread_id,
                    **parameters
                )
                
                # Update state panel if in debug mode
                if debug:
                    update_state_panel(layout, response)
                
                # Extract AI response
                ai_response = extract_response(response)
                messages.append({"role": "assistant", "content": ai_response})
                update_chat_panel(layout, messages)
                
            except Exception as e:
                messages.append({"role": "error", "content": f"Error: {str(e)}"})
                update_chat_panel(layout, messages)
        
        # Continue conversation
        while True:
            try:
                # Get user input
                user_input = click.prompt("\nYou", prompt_suffix="> ", type=str)
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    console.print("[yellow]Exiting agent session[/yellow]")
                    break
                
                # Add user message to chat
                messages.append({"role": "user", "content": user_input})
                update_chat_panel(layout, messages)
                
                # Run agent with user input
                response = agent_instance.run(
                    user_input,
                    thread_id=thread_id,
                    **parameters
                )
                
                # Update state panel if in debug mode
                if debug:
                    update_state_panel(layout, response)
                
                # Extract AI response
                ai_response = extract_response(response)
                messages.append({"role": "assistant", "content": ai_response})
                update_chat_panel(layout, messages)
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Exiting agent session[/yellow]")
                break
            except Exception as e:
                messages.append({"role": "error", "content": f"Error: {str(e)}"})
                update_chat_panel(layout, messages)

def extract_response(response: Dict[str, Any]) -> str:
    """Extract the text response from the agent output."""
    # Try to find output in different possible locations
    if isinstance(response, str):
        return response
    
    if isinstance(response, dict):
        # Check for common output fields
        if 'output' in response:
            return response['output']
        
        # Check for messages
        if 'messages' in response:
            messages = response['messages']
            if messages and len(messages) > 0:
                last_message = messages[-1]
                if hasattr(last_message, 'content'):
                    return last_message.content
                elif isinstance(last_message, tuple) and len(last_message) > 1:
                    return last_message[1]
                elif isinstance(last_message, dict) and 'content' in last_message:
                    return last_message['content']
    
    # Fallback to string representation
    return str(response)