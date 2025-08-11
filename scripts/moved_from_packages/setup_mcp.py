#!/usr/bin/env python3
"""Setup script for the General MCP Downloader.

This script sets up the general MCP downloader system and handles dependencies.
"""

import asyncio
import logging
import subprocess
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def install_dependencies():
    """Install required dependencies."""
    required_packages = ["aiohttp", "click", "pyyaml"]

    for package in required_packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except subprocess.CalledProcessError:
            return False

    return True


def setup_directories():
    """Create necessary directories."""
    dirs = [
        Path.home() / ".mcp",
        Path.home() / ".mcp" / "servers",
        Path.home() / ".mcp" / "configs",
        Path.home() / ".mcp" / "logs",
        Path.home() / ".mcp" / "backups",
    ]

    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)


def make_executable():
    """Make scripts executable."""
    scripts = [
        "general_mcp_downloader.py",
        "mcp_manager.py",
        "test_general_downloader.py",
    ]

    for script in scripts:
        script_path = Path(script)
        if script_path.exists():
            script_path.chmod(0o755)
        else:
            pass


async def test_installation():
    """Test the installation."""
    try:
        from general_mcp_downloader import GeneralMCPDownloader

        # Create a test downloader
        GeneralMCPDownloader()

        return True

    except Exception:
        return False


def create_aliases():
    """Create convenient command aliases."""
    current_dir = Path.cwd()

    # Create shell aliases
    aliases = f"""
# MCP Manager Aliases
alias mcp-discover='python "{current_dir}/mcp_manager.py" discover'
alias mcp-install='python "{current_dir}/mcp_manager.py" install'
alias mcp-list='python "{current_dir}/mcp_manager.py" list-servers'
alias mcp-health='python "{current_dir}/mcp_manager.py" health-check'
alias mcp-update='python "{current_dir}/mcp_manager.py" update'
alias mcp-config='python "{current_dir}/mcp_manager.py" config'

# Quick commands
alias mcp-install-core='python "{current_dir}/mcp_manager.py" install --categories official core'
alias mcp-install-all='python "{current_dir}/mcp_manager.py" install --all'
alias mcp-discover-install='python "{current_dir}/mcp_manager.py" discover --auto-install --limit 10'
"""

    # Save to aliases file
    aliases_file = Path.home() / ".mcp" / "aliases.sh"
    with open(aliases_file, "w") as f:
        f.write(aliases)


def show_usage_examples():
    """Show usage examples."""
    examples = [
        (
            "Discover servers",
            "python mcp_manager.py discover --auto-install --limit 10",
        ),
        (
            "Install specific servers",
            "python mcp_manager.py install --servers filesystem github postgres",
        ),
        ("Install by category", "python mcp_manager.py install --categories official"),
        ("List all servers", "python mcp_manager.py list-servers"),
        ("Health check", "python mcp_manager.py health-check"),
        ("Update servers", "python mcp_manager.py update --all"),
        ("Test the system", "python test_general_downloader.py"),
    ]

    for _description, _command in examples:
        pass


async def main():
    """Main setup function."""
    # Install dependencies
    if not install_dependencies():
        return False

    # Setup directories
    setup_directories()

    # Make scripts executable
    make_executable()

    # Test installation
    test_success = await test_installation()

    if test_success:
        # Create aliases
        create_aliases()

        # Show usage examples
        show_usage_examples()

        return True
    return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
