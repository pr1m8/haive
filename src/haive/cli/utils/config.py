"""
Configuration management for Haive CLI.
"""
import os
import json
from typing import Dict, Any, Optional
from pathlib import Path

# Default configuration directory based on platform
def get_config_dir() -> Path:
    """Get the platform-specific config directory."""
    if os.name == 'nt':  # Windows
        config_dir = Path(os.environ.get('APPDATA', '')) / 'Haive'
    else:  # Linux, macOS, etc.
        config_dir = Path.home() / '.config' / 'haive'
    
    return config_dir

def get_config_path() -> Path:
    """Get the path to the configuration file."""
    return get_config_dir() / 'config.json'

def get_default_config() -> Dict[str, Any]:
    """Get the default configuration."""
    return {
        'version': '1.0.0',
        'agents_dir': str(get_config_dir() / 'agents'),
        'registry_url': 'https://api.haive.ai/registry',
        'theme': 'dark',
        'cache_dir': str(get_config_dir() / 'cache'),
        'api_timeout': 30,
        'agents': {},
        'favorites': [],
        'show_welcome': True
    }

def init_config() -> None:
    """Initialize the configuration file with defaults."""
    config_dir = get_config_dir()
    config_path = get_config_path()
    
    # Create config directory if it doesn't exist
    os.makedirs(config_dir, exist_ok=True)
    
    # Create agents directory
    agents_dir = config_dir / 'agents'
    os.makedirs(agents_dir, exist_ok=True)
    
    # Create cache directory
    cache_dir = config_dir / 'cache'
    os.makedirs(cache_dir, exist_ok=True)
    
    # Write default config
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(get_default_config(), f, indent=2)

def get_config() -> Dict[str, Any]:
    """Get the current configuration."""
    config_path = get_config_path()
    
    if not os.path.exists(config_path):
        init_config()
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def update_config(update: Dict[str, Any]) -> Dict[str, Any]:
    """Update the configuration with new values."""
    config = get_config()
    
    # Deep update
    def deep_update(d, u):
        for k, v in u.items():
            if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                deep_update(d[k], v)
            else:
                d[k] = v
    
    deep_update(config, update)
    
    # Write updated config
    with open(get_config_path(), 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    
    return config

def get_agents_dir() -> Path:
    """Get the directory for storing agent files."""
    config = get_config()
    agents_dir = Path(config.get('agents_dir', str(get_config_dir() / 'agents')))
    os.makedirs(agents_dir, exist_ok=True)
    return agents_dir

def get_cache_dir() -> Path:
    """Get the directory for cache files."""
    config = get_config()
    cache_dir = Path(config.get('cache_dir', str(get_config_dir() / 'cache')))
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir

def get_agent_config_by_type(agent_type: str) -> Optional[Dict[str, Any]]:
    """Get configuration for a specific agent type."""
    config = get_config()
    agent_types = config.get('agent_types', {})
    return agent_types.get(agent_type)

def register_agent_type(agent_type: str, config_data: Dict[str, Any]) -> None:
    """Register a new agent type with custom configuration."""
    config = get_config()
    
    if 'agent_types' not in config:
        config['agent_types'] = {}
    
    config['agent_types'][agent_type] = config_data
    
    # Write updated config
    with open(get_config_path(), 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)