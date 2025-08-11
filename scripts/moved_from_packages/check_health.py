#!/usr/bin/env python3
"""Health check script for haive-mcp installation.

This script verifies that all components are properly installed and working.
"""

import asyncio
import subprocess
import sys
from pathlib import Path


class HealthChecker:
    """Check health of haive-mcp installation."""

    def __init__(self):
        self.checks_passed = 0
        self.checks_failed = 0
        self.issues = []

    async def run_all_checks(self) -> bool:
        """Run all health checks."""
        # Basic checks
        self.check_python_version()
        self.check_dependencies()
        self.check_imports()
        self.check_directories()

        # Advanced checks
        await self.check_mcp_servers()
        await self.check_dataflow_integration()
        await self.check_example_server()

        # Print summary
        self.print_summary()

        return self.checks_failed == 0

    def check_python_version(self):
        """Check Python version."""
        try:
            version = sys.version_info
            if version.major >= 3 and version.minor >= 12:
                self._pass(f"Python {version.major}.{version.minor}.{version.micro}")
            else:
                self._fail(
                    f"Python 3.12+ required, found {version.major}.{version.minor}"
                )
        except Exception as e:
            self._fail(f"Could not check Python version: {e}")

    def check_dependencies(self):
        """Check required dependencies."""
        deps = [
            ("poetry", "Poetry (package manager)"),
            ("npm", "NPM (for MCP servers)"),
            ("node", "Node.js"),
        ]

        for cmd, name in deps:
            try:
                result = subprocess.run(
                    ["which", cmd], capture_output=True, text=True, check=False
                )
                if result.returncode == 0:
                    self._pass(f"{name} installed")
                else:
                    self._fail(f"{name} not found")
                    self.issues.append(f"Install {name}: see installation guide")
            except Exception as e:
                self._fail(f"Could not check {name}: {e}")

    def check_imports(self):
        """Check Python imports."""
        imports = [
            ("haive.mcp", "Core MCP package"),
            ("haive.mcp.config", "MCP configuration"),
            ("haive.mcp.manager", "MCP manager"),
            ("mcp.server", "MCP SDK"),
            ("langchain_mcp_adapters.client", "LangChain MCP adapters"),
            ("haive.dataflow", "Haive dataflow (optional)"),
        ]

        for module, name in imports:
            # Use poetry run to check imports
            result = subprocess.run(
                ["poetry", "run", "python", "-c", f"import {module}; print('OK')"],
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode == 0:
                if module == "haive.dataflow":
                    self._pass(f"{name} available")
                else:
                    self._pass(f"{name} imported")
            elif module == "haive.dataflow":
                self._warn(f"{name} not available (optional)")
            else:
                self._fail(f"{name} import failed: {result.stderr.strip()}")
                if "mcp" in module:
                    self.issues.append("Run: poetry install --all-extras")

    def check_directories(self):
        """Check required directories."""
        dirs = [
            (Path.home() / ".haive" / "mcp", "User MCP directory"),
            (Path.cwd() / "src" / "haive" / "mcp", "Source directory"),
            (Path.cwd() / "tests", "Test directory"),
            (Path.cwd() / "examples", "Examples directory"),
        ]

        for dir_path, name in dirs:
            if dir_path.exists():
                self._pass(f"{name} exists")
            else:
                self._warn(f"{name} not found")
                self.issues.append(f"Create directory: {dir_path}")

    async def check_mcp_servers(self):
        """Check installed MCP servers."""
        servers = [
            "@modelcontextprotocol/server-filesystem",
            "@modelcontextprotocol/server-github",
            "@modelcontextprotocol/server-sqlite",
        ]

        for server in servers:
            try:
                result = subprocess.run(
                    ["npm", "list", "-g", server],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if result.returncode == 0:
                    self._pass(f"{server} installed")
                else:
                    self._warn(f"{server} not installed")
                    self.issues.append(f"Install: npm install -g {server}")
            except Exception as e:
                self._warn(f"Could not check {server}: {e}")

    async def check_dataflow_integration(self):
        """Check haive-dataflow integration."""
        # Check dataflow using poetry run
        check_script = """from haive.dataflow import registry_system, EntityType
servers = registry_system.get_entities_by_type(EntityType.MCP_SERVER)
print(f"OK:{len(servers)}")
"""

        result = subprocess.run(
            ["poetry", "run", "python", "-c", check_script],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode == 0 and result.stdout.startswith("OK:"):
            count = result.stdout.strip().split(":")[1]
            self._pass(f"Dataflow integration working ({count} servers registered)")
        elif "ImportError" in result.stderr:
            self._warn("Dataflow not available (optional)")
        else:
            self._fail(f"Dataflow integration error: {result.stderr.strip()}")

    async def check_example_server(self):
        """Check if example server can be created."""
        # Check server creation using poetry run
        server_script = """from mcp.server import FastMCP
server = FastMCP("health-check-server")
@server.tool()
async def test_tool(message: str) -> str:
    return f"Echo: {message}"
print("Server created OK")
"""

        result = subprocess.run(
            ["poetry", "run", "python", "-c", server_script],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode == 0:
            self._pass("FastMCP server creation working")
        else:
            self._fail(f"Server creation failed: {result.stderr.strip()}")
            self.issues.append("Check MCP SDK installation")

    def _pass(self, message: str):
        """Mark a check as passed."""
        self.checks_passed += 1

    def _fail(self, message: str):
        """Mark a check as failed."""
        self.checks_failed += 1

    def _warn(self, message: str):
        """Show a warning (not counted as failure)."""

    def print_summary(self):
        """Print health check summary."""
        self.checks_passed + self.checks_failed

        if self.issues:
            for _i, _issue in enumerate(self.issues, 1):
                pass

        if self.checks_failed == 0:
            pass
        else:
            pass


async def main():
    """Run health checks."""
    checker = HealthChecker()
    success = await checker.run_all_checks()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
