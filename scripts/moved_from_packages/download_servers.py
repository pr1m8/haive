#!/usr/bin/env python3
"""Main CLI for downloading MCP servers.

A unified command-line interface for downloading and managing MCP servers
from various sources including npm, PyPI, GitHub, and Docker Hub.
"""

import asyncio
import json
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.haive.mcp.downloader.legacy_core import GeneralMCPDownloader

# from src.haive.mcp.downloader.discovery import ServerDiscovery

console = Console()


@click.group()
def cli():
    """MCP Server Download Manager - Download and manage MCP servers."""


@cli.command()
@click.option(
    "--config",
    "-c",
    help="Configuration file path",
    default="configs/default_config.yaml",
)
@click.option("--servers", "-s", multiple=True, help="Specific servers to download")
@click.option("--category", "-cat", multiple=True, help="Server categories to download")
@click.option(
    "--all", "download_all", is_flag=True, help="Download all configured servers"
)
@click.option("--max-concurrent", "-m", default=5, help="Maximum concurrent downloads")
@click.option("--output-dir", "-o", help="Output directory for installations")
def download(
    config: str,
    servers: tuple,
    category: tuple,
    download_all: bool,
    max_concurrent: int,
    output_dir: str | None,
):
    """Download MCP servers based on configuration."""
    console.print(
        Panel.fit(
            "[bold cyan]MCP Server Downloader[/bold cyan]\nDownloading and configuring MCP servers",
            title="Download",
        )
    )

    # Create downloader
    downloader = GeneralMCPDownloader(config_file=config, install_dir=output_dir)

    # Determine what to download
    server_list = list(servers) if servers else None
    category_list = list(category) if category else None

    if download_all:
        server_list = None
        category_list = None
        console.print("[yellow]Downloading all configured servers...[/yellow]")
    elif not server_list and not category_list:
        console.print("[red]Error: Specify servers, categories, or use --all[/red]")
        return

    # Run download
    async def run_download():
        result = await downloader.download_servers(
            server_names=server_list,
            categories=category_list,
            max_concurrent=max_concurrent,
        )

        # Display results
        table = Table(title="Download Results")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", justify="right")

        table.add_row("Total Servers", str(result["total"]))
        table.add_row("Successful", f"[green]{result['successful']}[/green]")
        table.add_row("Failed", f"[red]{result['failed']}[/red]")
        table.add_row("Success Rate", f"{result['success_rate']:.1f}%")

        console.print("\n")
        console.print(table)

        if result.get("failed_servers"):
            console.print("\n[red]Failed servers:[/red]")
            for failure in result["failed_servers"]:
                console.print(f"  - {failure['server']}: {failure['error']}")

        console.print(
            f"\n[green]Configuration saved to:[/green] {result['config_file']}"
        )

    asyncio.run(run_download())


@cli.command()
@click.option("--source", "-s", help="Discovery source URL or registry")
@click.option("--limit", "-l", type=int, help="Limit number of servers to discover")
@click.option("--output", "-o", help="Output file for discovered servers")
def discover(source: str | None, limit: int | None, output: str | None):
    """Discover MCP servers from registries and sources."""
    console.print(
        Panel.fit(
            "[bold cyan]MCP Server Discovery[/bold cyan]\nFinding MCP servers from various sources",
            title="Discover",
        )
    )

    discovery = ServerDiscovery()

    async def run_discovery():
        if source:
            servers = await discovery.discover_from_url(source)
        else:
            # Discover from all known sources
            servers = await discovery.discover_all()

        if limit:
            servers = servers[:limit]

        console.print(f"\n[green]Discovered {len(servers)} servers[/green]")

        # Display discovered servers
        table = Table(title="Discovered Servers")
        table.add_column("Name", style="cyan")
        table.add_column("Source")
        table.add_column("Type")
        table.add_column("Tags")

        for server in servers[:10]:  # Show first 10
            table.add_row(
                server.get("name", "Unknown"),
                server.get("source", "Unknown"),
                server.get("template", "Unknown"),
                ", ".join(server.get("tags", [])),
            )

        if len(servers) > 10:
            table.add_row("...", f"and {len(servers) - 10} more", "", "")

        console.print(table)

        # Save if output specified
        if output:
            output_path = Path(output)
            with open(output_path, "w") as f:
                json.dump(servers, f, indent=2)
            console.print(f"\n[green]Saved to:[/green] {output_path}")

    asyncio.run(run_discovery())


@cli.command()
@click.option("--npm", is_flag=True, help="List npm packages")
@click.option("--pypi", is_flag=True, help="List PyPI packages")
@click.option("--github", is_flag=True, help="List GitHub repositories")
@click.option("--installed", is_flag=True, help="List installed servers")
def list(npm: bool, pypi: bool, github: bool, installed: bool):
    """List available MCP servers from various sources."""
    console.print(
        Panel.fit(
            "[bold cyan]MCP Server List[/bold cyan]\nAvailable servers from different sources",
            title="List",
        )
    )

    # Implementation would query different sources
    console.print("[yellow]Feature coming soon...[/yellow]")


@cli.command()
@click.argument("server_name")
@click.option(
    "--force", "-f", is_flag=True, help="Force update even if already installed"
)
def update(server_name: str, force: bool):
    """Update a specific MCP server to the latest version."""
    console.print(f"[cyan]Updating {server_name}...[/cyan]")

    # Implementation would update the specified server
    console.print("[yellow]Feature coming soon...[/yellow]")


@cli.command()
@click.argument("server_name")
@click.option("--purge", "-p", is_flag=True, help="Remove all data and configuration")
def remove(server_name: str, purge: bool):
    """Remove an installed MCP server."""
    console.print(f"[cyan]Removing {server_name}...[/cyan]")

    # Implementation would remove the specified server
    console.print("[yellow]Feature coming soon...[/yellow]")


@cli.command()
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def status(output_json: bool):
    """Show status of installed MCP servers."""
    console.print(
        Panel.fit(
            "[bold cyan]MCP Server Status[/bold cyan]\nCurrent installation status",
            title="Status",
        )
    )

    # Check for config file
    config_path = Path.home() / ".mcp" / "servers" / "mcp_servers_config.json"
    if not config_path.exists():
        console.print("[yellow]No servers installed yet[/yellow]")
        return

    with open(config_path) as f:
        config = json.load(f)

    servers = config.get("mcpServers", {})

    if output_json:
        pass
    else:
        table = Table(title="Installed MCP Servers")
        table.add_column("Server", style="cyan")
        table.add_column("Command")
        table.add_column("Status")

        for name, server_config in servers.items():
            table.add_row(
                name,
                server_config.get("command", "Unknown"),
                "[green]Installed[/green]",
            )

        console.print(table)
        console.print(f"\n[dim]Configuration: {config_path}[/dim]")


if __name__ == "__main__":
    cli()
