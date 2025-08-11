#!/usr/bin/env python3
"""Comprehensive setup script for haive-mcp package.

This script attempts to install and configure everything needed for haive-mcp,
including dependencies, MCP servers, and integration with haive-dataflow.
"""

import asyncio
import json
import logging
import os
import subprocess
import sys
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class MCPSetupManager:
    """Manages the complete setup process for haive-mcp."""

    def __init__(self):
        """Initialize setup manager."""
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.installed_servers: list[str] = []
        self.failed_servers: list[str] = []

    async def setup_all(self) -> bool:
        """Run the complete setup process.

        Returns:
            bool: True if setup completed successfully, False otherwise
        """
        logger.info("🚀 Starting haive-mcp setup process...")

        # Step 1: Check Python version
        if not self._check_python_version():
            return False

        # Step 2: Install package dependencies
        if not await self._install_dependencies():
            return False

        # Step 3: Setup MCP package
        if not await self._setup_mcp_package():
            return False

        # Step 4: Install common MCP servers
        await self._install_mcp_servers()

        # Step 5: Setup haive-dataflow integration
        await self._setup_dataflow_integration()

        # Step 6: Run validation tests
        await self._run_validation_tests()

        # Step 7: Generate configuration files
        await self._generate_configs()

        # Print summary
        self._print_summary()

        return len(self.errors) == 0

    def _check_python_version(self) -> bool:
        """Check if Python version is compatible."""
        try:
            logger.info("Checking Python version...")
            version = sys.version_info
            if version.major < 3 or (version.major == 3 and version.minor < 12):
                self.errors.append(
                    f"Python 3.12+ required, found {version.major}.{version.minor}"
                )
                return False
            logger.info(
                f"✓ Python {version.major}.{version.minor}.{version.micro} detected"
            )
            return True
        except Exception as e:
            self.errors.append(f"Failed to check Python version: {e}")
            return False

    async def _install_dependencies(self) -> bool:
        """Install package dependencies."""
        logger.info("\nInstalling dependencies...")

        dependencies = [
            ("poetry", "curl -sSL https://install.python-poetry.org | python3 -"),
            (
                "npm",
                (
                    "sudo apt-get install -y npm"
                    if sys.platform == "linux"
                    else "brew install npm"
                ),
            ),
            ("node", None),  # Usually comes with npm
        ]

        for dep, install_cmd in dependencies:
            try:
                # Check if already installed
                result = subprocess.run(
                    ["which", dep], capture_output=True, text=True, check=False
                )

                if result.returncode == 0:
                    logger.info(f"✓ {dep} already installed")
                    continue

                # Try to install
                if install_cmd:
                    logger.info(f"Installing {dep}...")
                    if sys.platform == "win32":
                        logger.warning(f"Please install {dep} manually on Windows")
                        self.warnings.append(
                            f"Manual installation required for {dep} on Windows"
                        )
                    else:
                        subprocess.run(install_cmd, shell=True, check=True)
                        logger.info(f"✓ {dep} installed successfully")
                else:
                    self.warnings.append(
                        f"{dep} not found, may need manual installation"
                    )

            except subprocess.CalledProcessError as e:
                self.warnings.append(f"Failed to install {dep}: {e}")
            except Exception as e:
                self.errors.append(f"Error checking/installing {dep}: {e}")

        # Install Python packages
        try:
            logger.info("\nInstalling Python packages...")
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True
            )

            # Install poetry dependencies
            subprocess.run(["poetry", "install", "--all-extras"], check=True)
            logger.info("✓ Python packages installed")

        except subprocess.CalledProcessError as e:
            self.errors.append(f"Failed to install Python packages: {e}")
            return False
        except Exception as e:
            self.errors.append(f"Error installing packages: {e}")
            return False

        return True

    async def _setup_mcp_package(self) -> bool:
        """Setup the MCP package itself."""
        logger.info("\nSetting up haive-mcp package...")

        try:
            # Run poetry install to ensure package is installed in editable mode
            subprocess.run(["poetry", "install", "--all-extras"], check=True)

            # Test imports using poetry run
            result = subprocess.run(
                [
                    "poetry",
                    "run",
                    "python",
                    "-c",
                    "from haive.mcp import MCPConfig, MCPServerConfig; from haive.mcp.manager import MCPManager; print('Imports successful')",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode == 0:
                logger.info("✓ MCP imports successful")
            else:
                self.errors.append(f"Failed to import MCP modules: {result.stderr}")
                return False

            # Create necessary directories
            dirs_to_create = [
                Path.home() / ".haive" / "mcp" / "servers",
                Path.home() / ".haive" / "mcp" / "configs",
                Path.home() / ".haive" / "mcp" / "logs",
            ]

            for dir_path in dirs_to_create:
                try:
                    dir_path.mkdir(parents=True, exist_ok=True)
                    logger.info(f"✓ Created directory: {dir_path}")
                except Exception as e:
                    self.warnings.append(f"Failed to create directory {dir_path}: {e}")

            return True

        except Exception as e:
            self.errors.append(f"Failed to setup MCP package: {e}")
            return False

    async def _install_mcp_servers(self):
        """Install common MCP servers."""
        logger.info("\nInstalling MCP servers...")

        servers = [
            {
                "name": "filesystem",
                "package": "@modelcontextprotocol/server-filesystem",
                "description": "File system operations",
            },
            {
                "name": "github",
                "package": "@modelcontextprotocol/server-github",
                "description": "GitHub integration",
                "env_required": ["GITHUB_TOKEN"],
            },
            {
                "name": "postgres",
                "package": "@modelcontextprotocol/server-postgres",
                "description": "PostgreSQL database access",
            },
            {
                "name": "sqlite",
                "package": "@modelcontextprotocol/server-sqlite",
                "description": "SQLite database access",
            },
            {
                "name": "slack",
                "package": "@modelcontextprotocol/server-slack",
                "description": "Slack integration",
                "env_required": ["SLACK_TOKEN"],
            },
        ]

        for server in servers:
            try:
                logger.info(f"\nInstalling {server['name']} server...")

                # Check environment requirements
                if "env_required" in server:
                    missing_env = [
                        var for var in server["env_required"] if not os.environ.get(var)
                    ]
                    if missing_env:
                        logger.warning(
                            f"⚠️  {server['name']} requires environment variables: {', '.join(missing_env)}"
                        )
                        self.warnings.append(
                            f"{server['name']} server installed but needs: {', '.join(missing_env)}"
                        )

                # Try npm install
                result = subprocess.run(
                    ["npm", "list", "-g", server["package"]],
                    capture_output=True,
                    text=True,
                    check=False,
                )

                if result.returncode == 0:
                    logger.info(f"✓ {server['name']} already installed")
                else:
                    subprocess.run(
                        ["npm", "install", "-g", server["package"]],
                        check=True,
                        capture_output=True,
                    )
                    logger.info(f"✓ {server['name']} installed successfully")

                self.installed_servers.append(server["name"])

            except subprocess.CalledProcessError as e:
                logger.warning(f"Failed to install {server['name']}: {e}")
                self.failed_servers.append(server["name"])
            except Exception as e:
                logger.exception(f"Error installing {server['name']}: {e}")
                self.failed_servers.append(server["name"])

    async def _setup_dataflow_integration(self):
        """Setup integration with haive-dataflow."""
        logger.info("\nSetting up haive-dataflow integration...")

        try:
            # Check if haive-dataflow is available using poetry
            result = subprocess.run(
                [
                    "poetry",
                    "run",
                    "python",
                    "-c",
                    "from haive.dataflow import registry_system, EntityType; print('OK')",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode != 0:
                self.warnings.append(
                    "haive-dataflow not available, skipping integration"
                )
                return

            logger.info("✓ haive-dataflow available")

            # Register each server using poetry run
            for server_name in self.installed_servers:
                try:
                    register_script = f"""
from haive.dataflow import registry_system, EntityType
from .registry.models import MCPServerConfig, MCPTransport

config = MCPServerConfig(
    name="{server_name}",
    transport=MCPTransport.STDIO,
    command="npx",
    args=["-y", "@modelcontextprotocol/server-{server_name}"]
)

server_id = registry_system.register_entity(
    name="{server_name}",
    entity_type=EntityType.MCP_SERVER,
    description="MCP {server_name} server",
    metadata={{"config": config.model_dump()}}
)
print(f"Registered {server_name}")
"""
                    result = subprocess.run(
                        ["poetry", "run", "python", "-c", register_script],
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    if result.returncode == 0:
                        logger.info(f"✓ Registered {server_name} in dataflow registry")
                    else:
                        self.warnings.append(
                            f"Failed to register {server_name}: {result.stderr}"
                        )

                except Exception as e:
                    self.warnings.append(f"Failed to register {server_name}: {e}")

        except ImportError:
            self.warnings.append("haive-dataflow not available, skipping integration")
        except Exception as e:
            self.errors.append(f"Failed to setup dataflow integration: {e}")

    async def _run_validation_tests(self):
        """Run validation tests to ensure setup is working."""
        logger.info("\nRunning validation tests...")

        # Test 1: Import test using poetry
        result = subprocess.run(
            [
                "poetry",
                "run",
                "python",
                "-c",
                "from haive.mcp import MCPManager, MCPConfig; print('Core imports OK')",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            logger.info("✓ Core import test passed")
        else:
            self.errors.append(f"Core import test failed: {result.stderr}")

        # Test 2: MCP SDK test
        result = subprocess.run(
            [
                "poetry",
                "run",
                "python",
                "-c",
                "from mcp.server import FastMCP; print('MCP SDK OK')",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            logger.info("✓ MCP SDK test passed")
        else:
            self.warnings.append(f"MCP SDK not available: {result.stderr}")

        # Test 3: Run pytest
        try:
            result = subprocess.run(
                ["poetry", "run", "pytest", "tests/unit/test_config.py", "-q"],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0:
                logger.info("✓ Unit tests passed")
            else:
                self.warnings.append("Some unit tests failed")
        except Exception as e:
            self.warnings.append(f"Could not run tests: {e}")

    async def _generate_configs(self):
        """Generate configuration files."""
        logger.info("\nGenerating configuration files...")

        # Create example config
        example_config = {
            "mcp": {
                "enabled": True,
                "servers": {
                    "filesystem": {
                        "transport": "stdio",
                        "command": "npx",
                        "args": ["-y", "@modelcontextprotocol/server-filesystem"],
                    }
                },
            }
        }

        config_path = Path.home() / ".haive" / "mcp" / "configs" / "example.json"
        try:
            with open(config_path, "w") as f:
                json.dump(example_config, f, indent=2)
            logger.info(f"✓ Created example config at {config_path}")
        except Exception as e:
            self.warnings.append(f"Failed to create example config: {e}")

    def _print_summary(self):
        """Print setup summary."""
        for _server in self.installed_servers:
            pass

        if self.failed_servers:
            for _server in self.failed_servers:
                pass

        if self.warnings:
            for _warning in self.warnings:
                pass

        if self.errors:
            for _error in self.errors:
                pass

        if not self.errors:
            pass
        else:
            pass


async def main():
    """Run the setup process."""
    manager = MCPSetupManager()
    success = await manager.setup_all()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
