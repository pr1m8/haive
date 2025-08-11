#!/usr/bin/env python3
"""MCP Server Management CLI.

Manage installed MCP servers, view logs, test connections, and configure settings.
"""

import asyncio
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import click
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.haive.mcp.manager import MCPServerManager

console = Console()


@click.group()
def cli():
    """MCP Server Manager - Manage and monitor MCP servers."""


@cli.command()
@click.argument("server_name")
@click.option("--timeout", "-t", default=30, help="Connection timeout in seconds")
def test(server_name: str, timeout: int):
    """Test connection to an MCP server."""
    console.print(f"[cyan]Testing connection to {server_name}...[/cyan]")

    manager = MCPServerManager()

    async def run_test():
        try:
            result = await manager.test_connection(server_name, timeout=timeout)

            if result["success"]:
                console.print(
                    f"[green]✓ Successfully connected to {server_name}[/green]"
                )

                # Show server info
                info = result.get("info", {})
                if info:
                    table = Table(title="Server Information")
                    table.add_column("Property", style="cyan")
                    table.add_column("Value")

                    for key, value in info.items():
                        table.add_row(key, str(value))

                    console.print(table)
            else:
                console.print(f"[red]✗ Failed to connect to {server_name}[/red]")
                console.print(
                    f"[red]Error: {result.get('error', 'Unknown error')}[/red]"
                )

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    asyncio.run(run_test())


@cli.command()
@click.argument("server_name")
@click.option("--lines", "-n", default=50, help="Number of log lines to show")
@click.option("--follow", "-f", is_flag=True, help="Follow log output")
def logs(server_name: str, lines: int, follow: bool):
    """View logs for an MCP server."""
    manager = MCPServerManager()

    log_file = manager.get_log_file(server_name)
    if not log_file or not log_file.exists():
        console.print(f"[yellow]No logs found for {server_name}[/yellow]")
        return

    console.print(
        Panel.fit(
            f"[bold]Logs for {server_name}[/bold]\n[dim]{log_file}[/dim]",
            title="Server Logs",
        )
    )

    if follow:
        # Follow logs in real-time
        try:
            subprocess.run(["tail", "-f", str(log_file)], check=False)
        except KeyboardInterrupt:
            console.print("\n[yellow]Stopped following logs[/yellow]")
    else:
        # Show last N lines
        with open(log_file) as f:
            all_lines = f.readlines()
            last_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines

            for line in last_lines:
                console.print(line.rstrip())


@cli.command()
@click.argument("server_name")
def info(server_name: str):
    """Show detailed information about an MCP server."""
    manager = MCPServerManager()

    info = manager.get_server_info(server_name)
    if not info:
        console.print(f"[red]Server {server_name} not found[/red]")
        return

    console.print(
        Panel.fit(f"[bold cyan]{server_name}[/bold cyan]", title="Server Information")
    )

    # Basic info
    table = Table(show_header=False, box=None)
    table.add_column("Property", style="cyan")
    table.add_column("Value")

    table.add_row("Command", info.get("command", "Unknown"))
    table.add_row("Installation Path", str(info.get("path", "Unknown")))
    table.add_row("Installation Method", info.get("method", "Unknown"))
    table.add_row("Installed Date", info.get("installed_date", "Unknown"))

    console.print(table)

    # Environment variables
    if info.get("env"):
        console.print("\n[bold]Environment Variables:[/bold]")
        for key, value in info["env"].items():
            console.print(f"  {key}: {value}")

    # Arguments
    if info.get("args"):
        console.print("\n[bold]Arguments:[/bold]")
        for arg in info["args"]:
            console.print(f"  {arg}")


@cli.command()
@click.argument("server_name")
@click.option("--key", "-k", help="Configuration key to set")
@click.option("--value", "-v", help="Configuration value")
@click.option("--env", "-e", multiple=True, help="Environment variable (KEY=VALUE)")
@click.option("--arg", "-a", multiple=True, help="Command argument")
def config(
    server_name: str, key: str | None, value: str | None, env: tuple, arg: tuple
):
    """Configure an MCP server."""
    manager = MCPServerManager()

    if key and value:
        # Set a specific configuration value
        success = manager.set_config(server_name, key, value)
        if success:
            console.print(f"[green]Set {key} = {value} for {server_name}[/green]")
        else:
            console.print("[red]Failed to set configuration[/red]")

    if env:
        # Set environment variables
        env_vars = {}
        for env_var in env:
            if "=" in env_var:
                k, v = env_var.split("=", 1)
                env_vars[k] = v

        if env_vars:
            success = manager.set_env_vars(server_name, env_vars)
            if success:
                console.print(
                    f"[green]Updated environment variables for {server_name}[/green]"
                )

    if arg:
        # Set command arguments
        success = manager.set_args(server_name, list(arg))
        if success:
            console.print(f"[green]Updated arguments for {server_name}[/green]")

    # Show current configuration
    config = manager.get_server_config(server_name)
    if config:
        console.print("\n[bold]Current Configuration:[/bold]")
        console.print(json.dumps(config, indent=2))


@cli.command()
@click.option("--all", "test_all", is_flag=True, help="Test all servers")
def health(test_all: bool):
    """Check health status of MCP servers."""
    manager = MCPServerManager()

    console.print(
        Panel.fit(
            "[bold cyan]MCP Server Health Check[/bold cyan]", title="Health Status"
        )
    )

    servers = manager.list_servers()
    if not servers:
        console.print("[yellow]No servers installed[/yellow]")
        return

    async def check_health():
        table = Table(title="Server Health Status")
        table.add_column("Server", style="cyan")
        table.add_column("Status")
        table.add_column("Response Time")
        table.add_column("Last Check")

        with Live(table, console=console, refresh_per_second=1):
            for server_name in servers:
                if test_all or manager.should_check_health(server_name):
                    result = await manager.test_connection(server_name, timeout=5)

                    if result["success"]:
                        status = "[green]✓ Healthy[/green]"
                        response_time = f"{result.get('response_time', 0):.2f}s"
                    else:
                        status = "[red]✗ Unhealthy[/red]"
                        response_time = "-"

                    table.add_row(
                        server_name,
                        status,
                        response_time,
                        datetime.now().strftime("%H:%M:%S"),
                    )

    asyncio.run(check_health())


@cli.command()
def validate():
    """Validate MCP server configurations."""
    manager = MCPServerManager()

    console.print(
        Panel.fit("[bold cyan]Configuration Validation[/bold cyan]", title="Validate")
    )

    results = manager.validate_all_configs()

    table = Table(title="Validation Results")
    table.add_column("Server", style="cyan")
    table.add_column("Status")
    table.add_column("Issues")

    all_valid = True
    for server_name, result in results.items():
        if result["valid"]:
            status = "[green]✓ Valid[/green]"
            issues = "-"
        else:
            status = "[red]✗ Invalid[/red]"
            issues = ", ".join(result["issues"])
            all_valid = False

        table.add_row(server_name, status, issues)

    console.print(table)

    if all_valid:
        console.print("\n[green]All configurations are valid![/green]")
    else:
        console.print("\n[red]Some configurations have issues[/red]")


@cli.command()
@click.option("--output", "-o", help="Output file for export")
@click.option("--format", "-f", type=click.Choice(["json", "yaml"]), default="json")
def export(output: str | None, format: str):
    """Export MCP server configurations."""
    manager = MCPServerManager()

    config = manager.export_config(format=format)

    if output:
        output_path = Path(output)
        with open(output_path, "w") as f:
            f.write(config)
        console.print(f"[green]Exported to {output_path}[/green]")
    else:
        console.print(config)


@cli.command()
@click.argument("config_file")
@click.option("--merge", "-m", is_flag=True, help="Merge with existing configuration")
def import_(config_file: str, merge: bool):
    """Import MCP server configurations."""
    manager = MCPServerManager()

    try:
        result = manager.import_config(config_file, merge=merge)

        if result["success"]:
            console.print(
                f"[green]Successfully imported {result['imported']} servers[/green]"
            )
            if result.get("skipped"):
                console.print(
                    f"[yellow]Skipped {result['skipped']} existing servers[/yellow]"
                )
        else:
            console.print(f"[red]Import failed: {result['error']}[/red]")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    cli()
