"""
Agent creation command for Haive CLI.
"""
import os
import sys
import time
import click
import json
import uuid
import datetime
from typing import Optional, Dict, Any, List
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.markdown import Markdown

from src.haive.cli.ui.console import create_console
from src.haive.cli.utils.config import get_config, get_agents_dir
from src.haive.cli.utils.registry import register_agent, get_agent_path, get_agent_config_path

console = create_console()

# Agent templates by type
AGENT_TEMPLATES = {
    'simple': {
        'name': 'Simple Agent',
        'description': 'A basic agent that processes input and generates output',
        'template_file': 'simple_agent.py.template',
        'config': {
            'agent_type': 'simple',
            'agent_class': 'SimpleAgent',
            'ui_config': {
                'theme': 'default',
                'show_thinking': False
            }
        }
    },
    'chat': {
        'name': 'Chat Agent',
        'description': 'An interactive chat agent with conversation memory',
        'template_file': 'chat_agent.py.template',
        'config': {
            'agent_type': 'chat',
            'agent_class': 'ChatAgent',
            'ui_config': {
                'theme': 'chat',
                'show_thinking': True,
                'memory_enabled': True
            }
        }
    },
    'game': {
        'name': 'Game Agent',
        'description': 'An interactive narrative game agent with state tracking',
        'template_file': 'game_agent.py.template',
        'config': {
            'agent_type': 'game',
            'agent_class': 'GameAgent',
            'ui_config': {
                'theme': 'game',
                'show_inventory': True,
                'show_stats': True
            },
            'game_config': {
                'title': 'Adventure Game',
                'initial_description': 'You find yourself at the beginning of an adventure.',
                'initial_location': 'Start',
                'initial_actions': ['look', 'help', 'inventory'],
                'initial_stats': {'health': 100, 'score': 0}
            }
        }
    },
    'reasoning': {
        'name': 'Reasoning Agent',
        'description': 'An agent that shows step-by-step reasoning for complex tasks',
        'template_file': 'reasoning_agent.py.template',
        'config': {
            'agent_type': 'reasoning',
            'agent_class': 'ReasoningAgent',
            'ui_config': {
                'theme': 'reasoning',
                'show_thinking': True,
                'show_confidence': True,
                'show_alternatives': True
            }
        }
    },
    'tool': {
        'name': 'Tool-using Agent',
        'description': 'An agent with access to external tools and APIs',
        'template_file': 'tool_agent.py.template',
        'config': {
            'agent_type': 'tool',
            'agent_class': 'ToolAgent',
            'ui_config': {
                'theme': 'tool',
                'show_tool_calls': True,
                'show_thinking': True
            },
            'tools_config': {
                'available_tools': ['calculator', 'weather', 'search', 'calendar'],
                'default_tools': ['calculator']
            }
        }
    }
}

@click.command()
@click.argument('agent_id', required=False)
@click.option('--type', '-t', 'agent_type', 
              type=click.Choice(['simple', 'chat', 'game', 'reasoning', 'tool']),
              help='Type of agent to create')
@click.option('--name', '-n', help='Display name for the agent')
@click.option('--description', '-d', help='Description of the agent')
@click.option('--template', help='Path to custom template file')
@click.option('--edit/--no-edit', default=True, help='Open agent file in editor after creation')
def create(agent_id: Optional[str], agent_type: Optional[str], name: Optional[str], 
         description: Optional[str], template: Optional[str], edit: bool):
    """Create a new agent from a template.
    
    If you don't specify an AGENT_ID, you will be prompted to enter one.
    """
    # Show agent types if none selected
    if not agent_type:
        agent_type = select_agent_type_interactive()
        if not agent_type:
            console.print("[yellow]Creation cancelled[/yellow]")
            return
    
    # Prompt for agent ID if not provided
    if not agent_id:
        agent_id = click.prompt("Enter a unique ID for your agent", type=str)
        # Sanitize the ID
        agent_id = agent_id.lower().replace(" ", "_").replace("-", "_")
    
    # Get existing agents
    config = get_config()
    existing_agents = config.get('agents', {})
    
    # Check if agent ID already exists
    if agent_id in existing_agents:
        overwrite = click.confirm(f"Agent with ID '{agent_id}' already exists. Overwrite?", default=False)
        if not overwrite:
            console.print("[yellow]Creation cancelled[/yellow]")
            return
    
    # Prompt for name if not provided
    if not name:
        template_name = AGENT_TEMPLATES[agent_type]['name']
        name = click.prompt("Enter a display name for your agent", type=str, default=f"My {template_name}")
    
    # Prompt for description if not provided
    if not description:
        template_desc = AGENT_TEMPLATES[agent_type]['description']
        description = click.prompt("Enter a description for your agent", 
                                 type=str, 
                                 default=f"Custom {template_desc.lower()}")
    
    # Create the agent
    create_agent_from_template(agent_id, agent_type, name, description, template, edit)

def select_agent_type_interactive() -> Optional[str]:
    """Show interactive selection for agent types."""
    # Create choices
    choices = []
    for i, (type_id, template) in enumerate(AGENT_TEMPLATES.items(), 1):
        choices.append((
            f"{i}. {template['name']} - {template['description']}",
            type_id
        ))
    
    # Add option to cancel
    choices.append(("0. Cancel", None))
    
    # Print choices
    console.print(Panel.fit("\n".join([choice[0] for choice in choices]), 
                            title="Agent Types"))
    
    # Get user selection
    selection = click.prompt("Select an agent type", type=int, default=0)
    
    if selection == 0 or selection > len(AGENT_TEMPLATES):
        return None
    
    return list(AGENT_TEMPLATES.keys())[selection-1]

def create_agent_from_template(agent_id: str, agent_type: str, name: str, description: str, 
                             template_path: Optional[str], edit: bool):
    """Create a new agent from a template."""
    # Get the template
    if template_path:
        if not os.path.exists(template_path):
            console.print(f"[bold red]Error:[/bold red] Template file '{template_path}' not found.")
            return
        
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
    else:
        # Get the built-in template
        template_file = AGENT_TEMPLATES[agent_type]['template_file']
        template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
        template_path = os.path.join(template_dir, template_file)
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
        except FileNotFoundError:
            # Fallback to embedded templates
            template_content = get_embedded_template(agent_type)
    
    # Replace template placeholders
    agent_content = template_content.replace("{{AGENT_ID}}", agent_id)
    agent_content = agent_content.replace("{{AGENT_NAME}}", name)
    agent_content = agent_content.replace("{{AGENT_DESCRIPTION}}", description)
    agent_content = agent_content.replace("{{AGENT_TYPE}}", agent_type)
    agent_content = agent_content.replace("{{CREATION_DATE}}", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    agent_content = agent_content.replace("{{UUID}}", str(uuid.uuid4()))
    
    # Create agent file
    agent_path = get_agent_path(agent_id)
    os.makedirs(os.path.dirname(agent_path), exist_ok=True)
    
    with open(agent_path, 'w', encoding='utf-8') as f:
        f.write(agent_content)
    
    # Create agent config
    template_config = AGENT_TEMPLATES[agent_type]['config'].copy()
    agent_config = {
        'name': name,
        'description': description,
        'agent_type': agent_type,
        'version': '1.0.0',
        'created_at': datetime.datetime.now().isoformat(),
        'tags': [agent_type, 'custom'],
        **template_config
    }
    
    # Save agent config
    config_path = get_agent_config_path(agent_id)
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(agent_config, f, indent=2)
    
    # Register the agent
    register_agent(agent_id, agent_config)
    
    console.print(f"[bold green]Agent created successfully:[/bold green] {name}")
    console.print(f"Agent ID: [cyan]{agent_id}[/cyan]")
    console.print(f"Agent Type: [cyan]{agent_type}[/cyan]")
    console.print(f"Agent File: [cyan]{agent_path}[/cyan]")
    
    # Show a preview of the agent code
    console.print("\n[yellow]Agent Code Preview:[/yellow]")
    syntax = Syntax(agent_content[:500] + "...", "python", theme="monokai", line_numbers=True)
    console.print(syntax)
    
    # Open in editor if requested
    if edit:
        click.edit(filename=agent_path)
    
    console.print(f"\nTo run your agent: [green]haive run {agent_id}[/green]")

def get_embedded_template(agent_type: str) -> str:
    """Get an embedded template if file templates are not available."""
    templates = {
        'simple': '''"""
{{AGENT_NAME}}
{{AGENT_DESCRIPTION}}

Created: {{CREATION_DATE}}
Agent ID: {{AGENT_ID}}
Agent Type: {{AGENT_TYPE}}
"""
from typing import Dict, Any, List, Optional
from src.haive.agents.base import Agent, AgentConfig
from src.haive.agents.simple.agent import SimpleAgentConfig, SimpleAgent

class CustomSimpleAgentConfig(SimpleAgentConfig):
    """Configuration for the {{AGENT_NAME}}."""
    
    def __init__(self, **kwargs):
        super().__init__(
            name="{{AGENT_NAME}}",
            system_prompt="You are {{AGENT_NAME}}, {{AGENT_DESCRIPTION}}",
            **kwargs
        )

class CustomSimpleAgent(SimpleAgent):
    """Implementation of the {{AGENT_NAME}}."""
    
    def run(self, input_text: str, **kwargs) -> Dict[str, Any]:
        """Process the input and generate a response."""
        # You can customize the processing here
        return super().run(input_text, **kwargs)

# Create the agent - this is what will be loaded
agent = CustomSimpleAgent(CustomSimpleAgentConfig())
''',
        'chat': '''"""
{{AGENT_NAME}}
{{AGENT_DESCRIPTION}}

Created: {{CREATION_DATE}}
Agent ID: {{AGENT_ID}}
Agent Type: {{AGENT_TYPE}}
"""
from typing import Dict, Any, List, Optional
from src.haive.agents.base import Agent, AgentConfig
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

class ChatAgent(Agent):
    """Implementation of a chat agent with memory."""
    
    def __init__(self):
        """Initialize the chat agent."""
        self.messages = []
        self.system_prompt = "You are {{AGENT_NAME}}, {{AGENT_DESCRIPTION}}"
        self.add_system_message(self.system_prompt)
    
    def add_system_message(self, content: str):
        """Add a system message to the conversation."""
        self.messages.append(SystemMessage(content=content))
    
    def add_user_message(self, content: str):
        """Add a user message to the conversation."""
        self.messages.append(HumanMessage(content=content))
    
    def add_assistant_message(self, content: str):
        """Add an assistant message to the conversation."""
        self.messages.append(AIMessage(content=content))
    
    def process_message(self, message: str) -> str:
        """Process a user message and generate a response."""
        # Add the user message
        self.add_user_message(message)
        
        # Generate a response using the LLM
        from src.haive.core.models.llm.base import AzureLLMConfig
        llm = AzureLLMConfig(model="gpt-4o").instantiate_llm()
        response = llm.invoke(self.messages)
        
        # Add the assistant's response
        self.add_assistant_message(response.content)
        
        return response.content
    
    def run(self, input_text: str, **kwargs) -> Dict[str, Any]:
        """Process the input and return the response with full message history."""
        response = self.process_message(input_text)
        return {
            "messages": self.messages,
            "output": response
        }

# Create the agent - this is what will be loaded
agent = ChatAgent()
''',
        'game': '''"""
{{AGENT_NAME}}
{{AGENT_DESCRIPTION}}

Created: {{CREATION_DATE}}
Agent ID: {{AGENT_ID}}
Agent Type: {{AGENT_TYPE}}
"""
from typing import Dict, Any, List, Optional
import json
import os
import uuid

class GameAgent:
    """Implementation of a game agent with state tracking."""
    
    def __init__(self):
        """Initialize the game agent."""
        self.game_title = "{{AGENT_NAME}}"
        self.game_description = "{{AGENT_DESCRIPTION}}"
        self.current_state = {}
    
    def initialize_game(self, new_game: bool = True, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Initialize a new game state."""
        session_id = session_id or str(uuid.uuid4())
        
        # Define the initial game state
        self.current_state = {
            'game_title': self.game_title,
            'description': self.game_description,
            'location': 'Start',
            'inventory': [],
            'status': 'active',
            'turn': 0,
            'session_id': session_id,
            'stats': {'health': 100, 'score': 0},
            'actions': ['look', 'help', 'inventory'],
            'message': 'Welcome to the game!'
        }
        
        return self.current_state
    
    def process_command(self, command: str, game_state: Dict[str, Any]) -> Dict[str, Any]:
        """Process a game command and update the state."""
        # Create a new state based on the current one
        new_state = game_state.copy()
        
        # Increment turn counter
        new_state['turn'] = game_state.get('turn', 0) + 1
        
        # Process the command
        command = command.lower().strip()
        
        if command == 'help':
            new_state['message'] = "Available commands: look, inventory, go [direction], examine [item], take [item], use [item]"
        
        elif command == 'look' or command == 'l':
            location = game_state.get('location', 'Unknown')
            if location == 'Start':
                new_state['message'] = "You are standing at the beginning of a great adventure. There is a path ahead and a small cottage to the east."
                new_state['actions'] = ['go north', 'go east', 'examine cottage']
            else:
                new_state['message'] = f"You are at {location}. There's not much to see here."
        
        elif command == 'inventory' or command == 'i':
            items = game_state.get('inventory', [])
            if items:
                new_state['message'] = f"You are carrying: {', '.join(items)}"
            else:
                new_state['message'] = "You are not carrying anything."
        
        elif command.startswith('go '):
            direction = command[3:].strip()
            if direction == 'north' and game_state.get('location') == 'Start':
                new_state['location'] = 'Forest Path'
                new_state['description'] = "You are on a winding forest path. Trees surround you on all sides."
                new_state['message'] = "You head north along the path and enter a forest."
                new_state['actions'] = ['go south', 'look', 'examine trees']
            elif direction == 'east' and game_state.get('location') == 'Start':
                new_state['location'] = 'Cottage'
                new_state['description'] = "You are inside a small, cozy cottage. There's a table with a key on it."
                new_state['message'] = "You enter the small cottage."
                new_state['actions'] = ['go west', 'look', 'take key', 'examine table']
            elif direction == 'south' and game_state.get('location') == 'Forest Path':
                new_state['location'] = 'Start'
                new_state['description'] = "You are at the beginning of your adventure."
                new_state['message'] = "You return to where you started."
                new_state['actions'] = ['go north', 'go east', 'look']
            elif direction == 'west' and game_state.get('location') == 'Cottage':
                new_state['location'] = 'Start'
                new_state['description'] = "You are at the beginning of your adventure."
                new_state['message'] = "You exit the cottage and return to the starting area."
                new_state['actions'] = ['go north', 'go east', 'look']
            else:
                new_state['message'] = f"You can't go {direction} from here."
        
        elif command.startswith('take '):
            item = command[5:].strip()
            if item == 'key' and game_state.get('location') == 'Cottage':
                if 'key' not in game_state.get('inventory', []):
                    new_state['inventory'] = game_state.get('inventory', []) + ['key']
                    new_state['message'] = "You pick up the key."
                    # Update the stats
                    new_state['stats'] = game_state.get('stats', {}).copy()
                    new_state['stats']['score'] = new_state['stats'].get('score', 0) + 10
                else:
                    new_state['message'] = "You already have the key."
            else:
                new_state['message'] = f"You don't see a {item} here that you can take."
        
        elif command.startswith('examine '):
            item = command[8:].strip()
            if item == 'cottage' and game_state.get('location') == 'Start':
                new_state['message'] = "It's a small, thatched-roof cottage. The door is slightly ajar."
            elif item == 'trees' and game_state.get('location') == 'Forest Path':
                new_state['message'] = "Tall, ancient trees surround you. They seem to whisper secrets in the wind."
            elif item == 'table' and game_state.get('location') == 'Cottage':
                new_state['message'] = "A simple wooden table. There's a small silver key on it."
            elif item == 'key' and (game_state.get('location') == 'Cottage' or 'key' in game_state.get('inventory', [])):
                new_state['message'] = "A small silver key. It might unlock something important."
            else:
                new_state['message'] = f"You don't see a {item} here to examine."
        
        elif command.startswith('use '):
            item = command[4:].strip()
            if item == 'key' and 'key' in game_state.get('inventory', []):
                new_state['message'] = "You don't see anything to use the key on right now."
            else:
                if item in game_state.get('inventory', []):
                    new_state['message'] = f"You're not sure how to use the {item} here."
                else:
                    new_state['message'] = f"You don't have a {item} to use."
        
        else:
            new_state['message'] = f"I don't understand '{command}'. Try 'help' for a list of commands."
        
        # Store the updated state
        self.current_state = new_state
        return new_state
    
    def run(self, input_text: str, **kwargs) -> Dict[str, Any]:
        """Process input and return the updated game state."""
        # Initialize game if needed
        if not self.current_state:
            session_id = kwargs.get('thread_id', str(uuid.uuid4()))
            self.initialize_game(True, session_id)
        
        # Process the command
        updated_state = self.process_command(input_text, self.current_state)
        return updated_state

# Create the agent - this is what will be loaded
agent = GameAgent()
''',
        'reasoning': '''"""
{{AGENT_NAME}}
{{AGENT_DESCRIPTION}}

Created: {{CREATION_DATE}}
Agent ID: {{AGENT_ID}}
Agent Type: {{AGENT_TYPE}}
"""
from typing import Dict, Any, List, Optional
import json
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

class ReasoningAgent:
    """Implementation of a reasoning agent that explains its thinking."""
    
    def __init__(self):
        """Initialize the reasoning agent."""
        self.system_prompt = """You are {{AGENT_NAME}}, {{AGENT_DESCRIPTION}}
        
When answering questions:
1. Break down the problem into steps
2. Think through each step carefully
3. Consider alternative approaches
4. Show your reasoning process
5. Provide a confidence level for your answer
"""
        self.messages = [SystemMessage(content=self.system_prompt)]
    
    def process_with_reasoning(self, query: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Process a query with detailed reasoning steps."""
        # Add the query to messages
        self.messages.append(HumanMessage(content=query))
        
        # First, generate reasoning steps
        from src.haive.core.models.llm.base import AzureLLMConfig
        llm = AzureLLMConfig(model="gpt-4o").instantiate_llm()
        
        thinking_prompt = f"""I need to answer this question: {query}
        
First, I'll think step by step about how to solve this problem. Break it down into clear reasoning steps.
        
My thinking:
"""
        thinking_response = llm.invoke(thinking_prompt)
        thinking_steps = thinking_response.content.split("\n")
        
        # Then, generate the final answer
        answer_prompt = f"""Based on my analysis:
{thinking_response.content}

My final answer to the original question is:
"""
        answer_response = llm.invoke(answer_prompt)
        
        # Estimate confidence level (simplified method)
        confidence_terms = ["certain", "confident", "likely", "possible", "uncertain", "doubtful"]
        confidence_score = 0.8  # Default: reasonably confident
        
        for term in confidence_terms:
            if term in thinking_response.content.lower() or term in answer_response.content.lower():
                if term in ["certain", "confident"]:
                    confidence_score = 0.9
                elif term in ["likely"]:
                    confidence_score = 0.7
                elif term in ["possible"]:
                    confidence_score = 0.5
                else:
                    confidence_score = 0.3
                break
        
        # Add the answer to messages
        self.messages.append(AIMessage(content=answer_response.content))
        
        # Return structured result
        return {
            "query": query,
            "answer": answer_response.content,
            "reasoning": {
                "steps": thinking_steps,
                "conclusion": answer_response.content,
                "confidence": confidence_score
            },
            "messages": self.messages,
            "session_id": session_id
        }
    
    def run(self, input_text: str, **kwargs) -> Dict[str, Any]:
        """Process input with reasoning and return structured output."""
        session_id = kwargs.get('thread_id', None)
        return self.process_with_reasoning(input_text, session_id)

# Create the agent - this is what will be loaded
agent = ReasoningAgent()
''',
        'tool': '''"""
{{AGENT_NAME}}
{{AGENT_DESCRIPTION}}

Created: {{CREATION_DATE}}
Agent ID: {{AGENT_ID}}
Agent Type: {{AGENT_TYPE}}
"""
from typing import Dict, Any, List, Optional
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import Tool
from datetime import datetime
import math
import json
import requests

class ToolAgent:
    """Implementation of an agent that uses external tools."""
    
    def __init__(self):
        """Initialize the tool-using agent."""
        self.system_prompt = """You are {{AGENT_NAME}}, {{AGENT_DESCRIPTION}}
        
You have access to the following tools:
- calculator: Perform mathematical calculations
- date_time: Get current date and time information
- weather: Get weather information for a location (requires API key)
- web_search: Search the web for information (requires API key)
"""
        self.messages = [SystemMessage(content=self.system_prompt)]
        self.tools = self._create_tools()
    
    def _create_tools(self) -> List[Tool]:
        """Create the tools available to the agent."""
        tools = []
        
        # Calculator tool
        def calculator(expression: str) -> str:
            """Evaluate a mathematical expression."""
            try:
                # Define safe mathematical functions
                safe_dict = {
                    'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                    'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
                    'sqrt': math.sqrt, 'log': math.log, 'log10': math.log10,
                    'exp': math.exp, 'pi': math.pi, 'e': math.e,
                    'abs': abs, 'int': int, 'float': float, 'round': round,
                    'ceil': math.ceil, 'floor': math.floor,
                    'max': max, 'min': min, 'sum': sum
                }
                
                # Evaluate the expression in the safe environment
                result = eval(expression, {"__builtins__": {}}, safe_dict)
                return f"Result: {result}"
            except Exception as e:
                return f"Error: {str(e)}"
        
        tools.append(Tool.from_function(
            func=calculator,
            name="calculator",
            description="Calculate mathematical expressions. Example: calculator('2 + 2 * 3')"
        ))
        
        # Date and time tool
        def date_time(format_string: Optional[str] = None) -> str:
            """Get the current date and time."""
            now = datetime.now()
            if format_string:
                try:
                    return now.strftime(format_string)
                except Exception as e:
                    return f"Error: {str(e)}"
            return now.strftime("%Y-%m-%d %H:%M:%S")
        
        tools.append(Tool.from_function(
            func=date_time,
            name="date_time",
            description="Get current date and time. Optional format string."
        ))
        
        # Weather tool (stub - would need API key in real implementation)
        def weather(location: str) -> str:
            """Get weather information for a location."""
            return f"Weather information for {location} is not available in this demo version. Would require API key."
        
        tools.append(Tool.from_function(
            func=weather,
            name="weather",
            description="Get weather information for a location."
        ))
        
        # Web search tool (stub - would need API key in real implementation)
        def web_search(query: str) -> str:
            """Search the web for information."""
            return f"Web search results for '{query}' are not available in this demo version. Would require API key."
        
        tools.append(Tool.from_function(
            func=web_search,
            name="web_search",
            description="Search the web for information."
        ))
        
        return tools
    
    def process_with_tools(self, query: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Process a query using tools when appropriate."""
        # Add the query to messages
        self.messages.append(HumanMessage(content=query))
        
        # Generate a response using the LLM with tools
        from src.haive.core.models.llm.base import AzureLLMConfig
        from langchain.agents import initialize_agent, AgentType
        
        llm = AzureLLMConfig(model="gpt-4o").instantiate_llm()
        
        # Initialize an agent with the LLM and tools
        agent = initialize_agent(
            tools=self.tools,
            llm=llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True
        )
        
        # Run the agent
        agent_response = agent.run(
            input=query,
            chat_history=self.messages[1:]  # Skip the system message
        )
        
        # Add the response to messages
        self.messages.append(AIMessage(content=agent_response))
        
        # Extract tool usage from agent execution (in a real implementation,
        # this would be extracted from the agent's execution trace)
        tool_usage = []
        
        for tool in self.tools:
            if tool.name.lower() in query.lower():
                # This is a simplification - in practice, we'd capture actual tool invocations
                tool_usage.append({
                    "tool": tool.name,
                    "description": tool.description,
                    "used": True
                })
        
        # Return structured result
        return {
            "query": query,
            "response": agent_response,
            "messages": self.messages,
            "tool_usage": tool_usage,
            "session_id": session_id
        }
    
    def run(self, input_text: str, **kwargs) -> Dict[str, Any]:
        """Process input with tools and return structured output."""
        session_id = kwargs.get('thread_id', None)
        return self.process_with_tools(input_text, session_id)

# Create the agent - this is what will be loaded
agent = ToolAgent()
'''
    }
    
    # Return the template for the requested agent type
    if agent_type in templates:
        return templates[agent_type]
    else:
        # Fall back to simple template if type not found
        return templates['simple']