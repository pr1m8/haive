"""
Agent registry management for Haive CLI.
"""
import os
import json
import shutil
from typing import Dict, Any, List, Optional
from pathlib import Path
import datetime
from src.haive.cli.utils.config import get_config, update_config, get_agents_dir

def get_agent_path(agent_id: str) -> Path:
    """Get the path to the agent implementation file."""
    agents_dir = get_agents_dir()
    return agents_dir / f"{agent_id}.py"

def get_agent_config_path(agent_id: str) -> Path:
    """Get the path to the agent configuration file."""
    agents_dir = get_agents_dir()
    return agents_dir / f"{agent_id}.json"

def get_agent_config(agent_id: str) -> Dict[str, Any]:
    """Get the configuration for an agent."""
    config = get_config()
    agent_data = config.get('agents', {}).get(agent_id, {})
    
    # Try to load additional config from file if exists
    config_path = get_agent_config_path(agent_id)
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                file_config = json.load(f)
                # Merge configs, with file config taking precedence
                agent_data = {**agent_data, **file_config}
        except Exception as e:
            print(f"Warning: Failed to load agent config file: {e}")
    
    return agent_data

def register_agent(agent_id: str, agent_data: Dict[str, Any]) -> None:
    """Register an agent in the configuration."""
    config = get_config()
    
    if 'agents' not in config:
        config['agents'] = {}
    
    # Update the agent data
    config['agents'][agent_id] = agent_data
    
    # Update the configuration
    update_config(config)
    
    # Save agent-specific config to file if it contains UI_config or game_config
    if 'ui_config' in agent_data or 'game_config' in agent_data:
        config_path = get_agent_config_path(agent_id)
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(agent_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to save agent config file: {e}")

def unregister_agent(agent_id: str, delete_files: bool = True) -> bool:
    """Unregister an agent and optionally delete its files."""
    config = get_config()
    
    if 'agents' not in config or agent_id not in config['agents']:
        return False
    
    # Remove from configuration
    del config['agents'][agent_id]
    
    # Remove from favorites if present
    if 'favorites' in config and agent_id in config['favorites']:
        config['favorites'].remove(agent_id)
    
    # Update the configuration
    update_config(config)
    
    # Delete files if requested
    if delete_files:
        agent_path = get_agent_path(agent_id)
        config_path = get_agent_config_path(agent_id)
        
        if os.path.exists(agent_path):
            os.remove(agent_path)
        
        if os.path.exists(config_path):
            os.remove(config_path)
    
    return True

def list_installed_agents() -> List[Dict[str, Any]]:
    """Get a list of all installed agents with their configurations."""
    config = get_config()
    agents = config.get('agents', {})
    
    result = []
    for agent_id, agent_data in agents.items():
        # Check if the agent file exists
        agent_path = get_agent_path(agent_id)
        installed = os.path.exists(agent_path)
        
        # Get the full config
        full_config = get_agent_config(agent_id)
        
        # Add installed status
        result.append({
            'id': agent_id,
            'installed': installed,
            **full_config
        })
    
    return result

def get_agent_ui_config(agent_id: str) -> Optional[Dict[str, Any]]:
    """Get UI configuration for a specific agent."""
    agent_config = get_agent_config(agent_id)
    return agent_config.get('ui_config')

def get_agent_game_config(agent_id: str) -> Optional[Dict[str, Any]]:
    """Get game configuration for a specific agent."""
    agent_config = get_agent_config(agent_id)
    return agent_config.get('game_config')

def add_agent_to_favorites(agent_id: str) -> bool:
    """Add an agent to favorites."""
    config = get_config()
    
    if 'agents' not in config or agent_id not in config['agents']:
        return False
    
    if 'favorites' not in config:
        config['favorites'] = []
    
    if agent_id not in config['favorites']:
        config['favorites'].append(agent_id)
        update_config(config)
    
    return True

def remove_agent_from_favorites(agent_id: str) -> bool:
    """Remove an agent from favorites."""
    config = get_config()
    
    if 'favorites' not in config or agent_id not in config['favorites']:
        return False
    
    config['favorites'].remove(agent_id)
    update_config(config)
    
    return True

def get_favorite_agents() -> List[Dict[str, Any]]:
    """Get a list of favorite agents with their configurations."""
    config = get_config()
    favorites = config.get('favorites', [])
    
    result = []
    for agent_id in favorites:
        if agent_id in config.get('agents', {}):
            agent_config = get_agent_config(agent_id)
            agent_path = get_agent_path(agent_id)
            installed = os.path.exists(agent_path)
            
            result.append({
                'id': agent_id,
                'installed': installed,
                **agent_config
            })
    
    return result

def create_agent_scaffold(agent_id: str, agent_type: str, name: str, 
                        description: str = "", version: str = "1.0.0") -> bool:
    """Create a scaffold for a new agent."""
    from src.haive.cli.utils.config import get_agent_config_by_type
    
    # Get the base configuration for the agent type
    base_config = get_agent_config_by_type(agent_type)
    if not base_config:
        return False
    
    # Create the agent configuration
    agent_config = {
        'name': name,
        'description': description,
        'version': version,
        'agent_type': agent_type,
        'created_at': str(datetime.datetime.now()),
        **base_config
    }
    
    # Get the template code
    template_code = base_config.get('template_code', "")
    
    # Create the agent file
    agent_path = get_agent_path(agent_id)
    with open(agent_path, 'w', encoding='utf-8') as f:
        f.write(template_code)
    
    # Register the agent
    register_agent(agent_id, agent_config)
    
    return True