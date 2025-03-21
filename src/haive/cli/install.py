#!/usr/bin/env python
"""
Installation script for Haive CLI.
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

def install_cli():
    """Install the Haive CLI."""
    print("Installing Haive CLI...")
    
    # Get the current directory
    current_dir = Path(__file__).parent.absolute()
    
    # Create template directory if it doesn't exist
    templates_dir = current_dir / "templates"
    os.makedirs(templates_dir, exist_ok=True)
    
    # Create example template files
    create_example_templates(templates_dir)
    
    # Ensure the script is executable
    make_executable(current_dir / "main.py")
    
    # Create symlink to main.py in a directory in PATH
    create_command_symlink(current_dir / "main.py")
    
    # Create config directory
    from src.haive.cli.utils.config import get_config_dir, init_config
    config_dir = get_config_dir()
    os.makedirs(config_dir, exist_ok=True)
    
    # Initialize config
    init_config()
    
    print(f"Haive CLI installed successfully. Configuration at: {config_dir}")
    print("Run 'haive --help' to get started.")

def create_example_templates(templates_dir):
    """Create example template files."""
    # Check if templates already exist
    if list(templates_dir.glob("*.template")):
        print("Template files already exist, skipping creation.")
        return
    
    # Create template files from the embedded templates in create.py
    from src.haive.cli.commands.create import get_embedded_template
    
    for agent_type in ['simple', 'chat', 'game', 'reasoning', 'tool']:
        template_content = get_embedded_template(agent_type)
        template_file = templates_dir / f"{agent_type}_agent.py.template"
        
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        print(f"Created template: {template_file}")

def make_executable(file_path):
    """Make a file executable."""
    if sys.platform != 'win32':
        # Add execute permission
        os.chmod(file_path, os.stat(file_path).st_mode | 0o111)
        print(f"Made {file_path} executable")

def create_command_symlink(main_script):
    """Create a symlink to the main script in a directory in PATH."""
    # Different approach based on platform
    if sys.platform == 'win32':
        # On Windows, create a batch file in Scripts directory
        python_scripts = Path(sys.executable).parent / "Scripts"
        if not python_scripts.exists():
            print("Could not find Python Scripts directory.")
            return
        
        batch_file = python_scripts / "haive.bat"
        with open(batch_file, 'w') as f:
            f.write(f'@echo off\n"{sys.executable}" "{main_script}" %*')
        
        print(f"Created command batch file: {batch_file}")
    else:
        # On Unix-like systems, create a symlink in /usr/local/bin if possible
        bin_dir = Path("/usr/local/bin")
        if not bin_dir.exists() or not os.access(bin_dir, os.W_OK):
            # Fall back to user's home bin directory
            bin_dir = Path.home() / ".local" / "bin"
            os.makedirs(bin_dir, exist_ok=True)
        
        symlink_path = bin_dir / "haive"
        
        # Remove existing symlink if it exists
        if symlink_path.exists() or symlink_path.is_symlink():
            os.remove(symlink_path)
        
        # Create the symlink
        os.symlink(main_script, symlink_path)
        print(f"Created command symlink: {symlink_path}")
        
        # Add to PATH if needed
        if bin_dir == Path.home() / ".local" / "bin":
            add_to_path(bin_dir)

def add_to_path(bin_dir):
    """Add a directory to PATH in the user's shell config."""
    shell = os.environ.get('SHELL', '').split('/')[-1]
    home = Path.home()
    
    if shell == 'bash':
        config_file = home / ".bashrc"
    elif shell == 'zsh':
        config_file = home / ".zshrc"
    else:
        print(f"Unknown shell: {shell}. Please add {bin_dir} to your PATH manually.")
        return
    
    # Check if bin_dir is already in PATH
    if str(bin_dir) in os.environ.get('PATH', ''):
        return
    
    # Add to shell config
    path_line = f'\n# Added by Haive CLI installer\nexport PATH="$PATH:{bin_dir}"\n'
    
    try:
        with open(config_file, 'a') as f:
            f.write(path_line)
        print(f"Added {bin_dir} to PATH in {config_file}")
        print(f"Please run 'source {config_file}' or start a new terminal session.")
    except Exception as e:
        print(f"Could not update {config_file}: {e}")
        print(f"Please add {bin_dir} to your PATH manually.")

if __name__ == "__main__":
    install_cli()