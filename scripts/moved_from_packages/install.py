#!/usr/bin/env python3
"""Quick install script for haive-mcp.

This script provides a quick way to install and verify the haive-mcp package.
"""

import contextlib
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description, check=True):
    """Run a command with error handling."""
    try:
        if isinstance(cmd, str):
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, check=check
            )
        else:
            result = subprocess.run(cmd, capture_output=True, text=True, check=check)

        if result.returncode == 0:
            if result.stdout and len(result.stdout.strip()) < 200:
                pass
        elif result.stderr:
            pass
        return result.returncode == 0
    except Exception:
        return False


def main():
    """Main installation process."""
    # Check we're in the right directory
    if not Path("pyproject.toml").exists():
        return 1

    # Step 1: Install Python dependencies
    if not run_command("poetry install --all-extras", "Installing Python dependencies"):
        return 1

    # Step 2: Check MCP imports

    # Check core imports using poetry
    result = run_command(
        [
            "poetry",
            "run",
            "python",
            "-c",
            "from haive.mcp import MCPConfig, MCPServerConfig; print('Core imports OK')",
        ],
        "Core imports test",
        check=False,
    )

    # Check MCP SDK
    result = run_command(
        [
            "poetry",
            "run",
            "python",
            "-c",
            "from mcp.server import FastMCP; print('MCP SDK OK')",
        ],
        "MCP SDK test",
        check=False,
    )
    if not result:
        pass

    # Check LangChain MCP adapters
    result = run_command(
        [
            "poetry",
            "run",
            "python",
            "-c",
            "from langchain_mcp_adapters.client import MultiServerMCPClient; print('LangChain MCP OK')",
        ],
        "LangChain MCP test",
        check=False,
    )
    if not result:
        pass

    # Step 3: Create directories
    dirs = [
        Path.home() / ".haive" / "mcp" / "servers",
        Path.home() / ".haive" / "mcp" / "configs",
        Path("logs"),
        Path("data"),
    ]

    for dir_path in dirs:
        with contextlib.suppress(Exception):
            dir_path.mkdir(parents=True, exist_ok=True)

    # Step 4: Quick test
    if run_command(
        ["poetry", "run", "pytest", "tests/unit/test_config.py", "-q"],
        "Running quick test",
        check=False,
    ):
        pass
    else:
        pass

    # Step 5: Optional - Install a sample MCP server
    if sys.stdin.isatty():
        try:
            response = input().strip().lower()
            if response == "y":
                run_command(
                    "npm install -g @modelcontextprotocol/server-filesystem",
                    "Installing filesystem MCP server",
                    check=False,
                )
        except KeyboardInterrupt:
            pass
        except EOFError:
            pass
    else:
        pass

    # Summary

    return 0


if __name__ == "__main__":
    sys.exit(main())
