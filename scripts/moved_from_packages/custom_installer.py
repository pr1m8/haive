#!/usr/bin/env python3
"""Example of creating a custom installer plugin.

This example shows how to extend the installer system with custom installation methods.
"""

import asyncio
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.haive.mcp.downloader import (
    GeneralMCPDownloader,
    InstallationMethod,
    MCPInstaller,
    ServerConfig,
    ServerTemplate,
)


class BinaryInstaller(MCPInstaller):
    """Custom installer for downloading binary executables."""

    async def can_handle(
        self, server_config: ServerConfig, template: ServerTemplate
    ) -> bool:
        """Check if this is a binary installation."""
        return template.installation_method.value == "binary"

    async def install(
        self, server_config: ServerConfig, template: ServerTemplate, install_dir: Path
    ) -> dict[str, Any]:
        """Download and install binary executable."""
        import stat

        import aiohttp

        binary_url = server_config.source
        binary_name = server_config.variables.get("binary_name", "mcp-server")
        binary_path = install_dir / binary_name

        try:
            # Download binary
            async with aiohttp.ClientSession() as session:
                async with session.get(binary_url) as response:
                    if response.status == 200:
                        content = await response.read()

                        # Save binary
                        binary_path.parent.mkdir(parents=True, exist_ok=True)
                        binary_path.write_bytes(content)

                        # Make executable
                        binary_path.chmod(binary_path.stat().st_mode | stat.S_IEXEC)

                        return {
                            "success": True,
                            "method": "binary",
                            "binary_path": str(binary_path),
                            "command": str(binary_path),
                        }
                    return {"success": False, "error": f"HTTP {response.status}"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def verify(
        self, server_config: ServerConfig, template: ServerTemplate, install_dir: Path
    ) -> bool:
        """Verify binary exists and is executable."""
        binary_name = server_config.variables.get("binary_name", "mcp-server")
        binary_path = install_dir / binary_name

        return binary_path.exists() and binary_path.is_file()


class ScriptInstaller(MCPInstaller):
    """Custom installer for script-based installations."""

    async def can_handle(
        self, server_config: ServerConfig, template: ServerTemplate
    ) -> bool:
        """Check if this is a script installation."""
        return template.installation_method.value == "script"

    async def install(
        self, server_config: ServerConfig, template: ServerTemplate, install_dir: Path
    ) -> dict[str, Any]:
        """Run custom installation script."""
        import subprocess

        script_commands = template.post_install

        try:
            # Create install directory
            server_dir = install_dir / server_config.name
            server_dir.mkdir(parents=True, exist_ok=True)

            # Run installation commands
            for command in script_commands:
                # Format command with variables
                formatted_cmd = command.format(**server_config.variables)

                # Run command
                result = subprocess.run(
                    formatted_cmd,
                    shell=True,
                    cwd=server_dir,
                    capture_output=True,
                    text=True,
                    check=False,
                )

                if result.returncode != 0:
                    return {
                        "success": False,
                        "error": f"Script failed: {result.stderr}",
                    }

            return {
                "success": True,
                "method": "script",
                "install_dir": str(server_dir),
                "command": template.command_pattern.format(**server_config.variables),
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def verify(
        self, server_config: ServerConfig, template: ServerTemplate, install_dir: Path
    ) -> bool:
        """Verify script installation."""
        server_dir = install_dir / server_config.name
        return server_dir.exists()


async def test_custom_installers():
    """Test custom installer plugins."""
    # Create downloader
    downloader = GeneralMCPDownloader()

    # Add custom installers
    downloader.installers.extend([BinaryInstaller(), ScriptInstaller()])

    # Add custom installation method to enum (for demo)
    # In production, extend the InstallationMethod enum

    # Example 1: Binary installer configuration
    binary_template = ServerTemplate(
        name="binary_server",
        installation_method=InstallationMethod.MANUAL,  # Using MANUAL as placeholder
        command_pattern="{install_dir}/{binary_name}",
        capabilities=["tools"],
    )

    binary_config = ServerConfig(
        name="test-binary",
        template="binary_server",
        source="https://example.com/mcp-server-binary",
        variables={"binary_name": "mcp-test-server", "install_dir": "/opt/mcp/bin"},
    )

    # Example 2: Script installer configuration
    script_template = ServerTemplate(
        name="script_server",
        installation_method=InstallationMethod.MANUAL,
        command_pattern="python {install_dir}/server.py",
        post_install=[
            "wget {script_url} -O install.sh",
            "chmod +x install.sh",
            "./install.sh",
        ],
        capabilities=["tools"],
    )

    script_config = ServerConfig(
        name="test-script",
        template="script_server",
        source="https://example.com/install-script.sh",
        variables={
            "script_url": "https://example.com/install-script.sh",
            "install_dir": "/opt/mcp/scripts",
        },
    )

    # Add configurations
    downloader.templates["binary_server"] = binary_template
    downloader.templates["script_server"] = script_template
    downloader.servers.extend([binary_config, script_config])

    # Test can_handle
    binary_installer = BinaryInstaller()
    await binary_installer.can_handle(binary_config, binary_template)

    return downloader


async def create_webhook_installer():
    """Example of webhook-based installer."""

    class WebhookInstaller(MCPInstaller):
        """Installer that notifies via webhook."""

        async def can_handle(self, server_config, template):
            return "webhook" in server_config.variables

        async def install(self, server_config, template, install_dir):
            # Regular installation
            # ... install logic ...

            # Send webhook notification
            webhook_url = server_config.variables.get("webhook")
            if webhook_url:
                import aiohttp

                async with aiohttp.ClientSession() as session:
                    await session.post(
                        webhook_url,
                        json={
                            "event": "mcp_server_installed",
                            "server": server_config.name,
                            "status": "success",
                        },
                    )

            return {"success": True}

        async def verify(self, server_config, template, install_dir):
            return True

    return WebhookInstaller()


async def main():
    """Run custom installer examples."""
    # Test custom installers
    await test_custom_installers()

    # Create webhook installer
    await create_webhook_installer()


if __name__ == "__main__":
    asyncio.run(main())
