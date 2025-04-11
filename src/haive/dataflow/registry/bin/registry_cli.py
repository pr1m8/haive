#!/usr/bin/env python
"""
Haive Registry CLI

This script provides a command-line interface for the Haive registry system.
It allows users to:
- Discover and register components (agents, tools, engines, games, etc.)
- View registry statistics
- Import LLM models
- Search for components
- View detailed information about components

Usage:
    python registry_cli.py discover all
    python registry_cli.py discover agents
    python registry_cli.py import llm-models
    python registry_cli.py stats
    python registry_cli.py search [type] [term]
    python registry_cli.py show [id]
"""

import os
import sys
import argparse
import json
import textwrap
import traceback
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from datetime import datetime

# Add project root to path if needed
project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Try to import rich for better formatting
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.syntax import Syntax
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# Import registry system
try:
    from src.haive.dataflow.registry.core import registry_system
    from src.haive.dataflow.registry.models import EntityType, ImportStatus
    from src.haive.dataflow.registry.discovery import discover_all, discover_agents, discover_tools, discover_toolkits, discover_engines, discover_games
    from src.haive.dataflow.registry.importers.litellm_importer import import_llm_models
except ImportError as e:
    print(f"Error importing registry system: {e}")
    print("Make sure you're running this script from the project root or that the module is in your PYTHONPATH.")
    sys.exit(1)

# Initialize console if rich is available
console = Console() if RICH_AVAILABLE else None


def print_rich(message, style="", highlight=False, markup=True):
    """Print with rich formatting if available, otherwise use regular print."""
    if RICH_AVAILABLE:
        console.print(message, style=style, highlight=highlight, markup=markup)
    else:
        print(message)


def print_header(title, style="bold blue"):
    """Print a header with rich formatting if available."""
    if RICH_AVAILABLE:
        console.print(f"\n[{style}]{title}[/{style}]")
        console.print("=" * len(title))
    else:
        print(f"\n{title}")
        print("=" * len(title))


def print_subheader(title, style="bold cyan"):
    """Print a subheader with rich formatting if available."""
    if RICH_AVAILABLE:
        console.print(f"\n[{style}]{title}[/{style}]")
        console.print("-" * len(title))
    else:
        print(f"\n{title}")
        print("-" * len(title))


def print_table(headers, rows, title=None):
    """Print a table with rich formatting if available."""
    if RICH_AVAILABLE:
        table = Table(title=title, box=box.ROUNDED)
        
        # Add headers
        for header in headers:
            table.add_column(header, style="bold")
        
        # Add rows
        for row in rows:
            # Convert all values to strings
            str_row = [str(val) if val is not None else "" for val in row]
            table.add_row(*str_row)
        
        console.print(table)
    else:
        # Simple ASCII table
        if title:
            print(f"\n{title}")
            print("-" * len(title))
        
        # Calculate column widths
        col_widths = []
        for i in range(len(headers)):
            col_width = max(len(headers[i]), max([len(str(row[i])) if i < len(row) and row[i] is not None else 0 for row in rows]) + 2)
            col_widths.append(col_width)
        
        # Print headers
        header_row = "| " + " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers)) + " |"
        print(header_row)
        print("|" + "-" * (len(header_row) - 2) + "|")
        
        # Print rows
        for row in rows:
            str_row = [str(val) if val is not None else "" for val in row]
            padded_row = [str_row[i].ljust(col_widths[i]) if i < len(str_row) else " " * col_widths[i] for i in range(len(col_widths))]
            print("| " + " | ".join(padded_row) + " |")


def setup_parser() -> argparse.ArgumentParser:
    """Set up command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Haive Registry CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        Examples:
          python registry_cli.py discover all
          python registry_cli.py discover agents
          python registry_cli.py import llm-models
          python registry_cli.py stats
          python registry_cli.py search agent "chat"
          python registry_cli.py show 123e4567-e89b-12d3-a456-426614174000
        """)
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Discover command
    discover_parser = subparsers.add_parser("discover", help="Discover and register components")
    discover_parser.add_argument(
        "type", 
        choices=["all", "agents", "tools", "toolkits", "engines", "games"],
        help="Type of components to discover"
    )
    discover_parser.add_argument(
        "--module", "-m",
        help="Specific module path to scan"
    )
    
    # Import command
    import_parser = subparsers.add_parser("import", help="Import data from external sources")
    import_parser.add_argument(
        "source",
        choices=["llm-models"],
        help="Source to import from"
    )
    
    # Stats command
    subparsers.add_parser("stats", help="Show registry statistics")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search for components")
    search_parser.add_argument(
        "type",
        choices=["all", "agent", "tool", "toolkit", "engine", "game", "llm-model", "llm-provider"],
        help="Type of components to search for"
    )
    search_parser.add_argument(
        "term",
        nargs="?",
        default="",
        help="Search term"
    )
    
    # Show command
    show_parser = subparsers.add_parser("show", help="Show component details")
    show_parser.add_argument(
        "id",
        help="Component ID to show"
    )
    
    # List command
    list_parser = subparsers.add_parser("list", help="List components of a specific type")
    list_parser.add_argument(
        "type",
        choices=["agents", "tools", "toolkits", "engines", "games", "llm-models", "llm-providers", "all"],
        help="Type of components to list"
    )
    
    # Clear command
    clear_parser = subparsers.add_parser("clear", help="Clear the registry")
    clear_parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force clearing without confirmation"
    )
    
    return parser


def format_json(data):
    """Format JSON data for display."""
    if RICH_AVAILABLE:
        return Syntax(json.dumps(data, indent=2), "json", theme="monokai")
    else:
        return json.dumps(data, indent=2)


def handle_discover(args):
    """Handle the discover command."""
    if args.type == "all":
        print_header("Discovering all component types...")
        
        try:
            results = discover_all()
            
            # Print statistics
            total = sum(len(ids) for ids in results.values())
            print_subheader(f"Discovery completed: {total} components registered")
            
            # Create table rows
            rows = []
            for entity_type, ids in results.items():
                rows.append([entity_type.value, len(ids)])
            
            # Print table
            print_table(["Entity Type", "Count"], rows, "Discovery Results")
        except Exception as e:
            print_rich(f"Error during discovery: {e}", style="bold red")
            print(traceback.format_exc())
    
    elif args.type == "agents":
        print_header("Discovering agents...")
        
        try:
            module_paths = [args.module] if args.module else None
            ids = discover_agents(module_paths)
            
            print_subheader(f"Discovered {len(ids)} agents")
            if ids:
                # Get agent details for table
                agents = []
                for agent_id in ids:
                    agent = registry_system.get_entity(agent_id)
                    if agent:
                        agents.append([
                            agent.name,
                            agent.id,
                            agent.module_path,
                            agent.description[:50] + "..." if agent.description and len(agent.description) > 50 else agent.description
                        ])
                
                # Print table
                print_table(["Name", "ID", "Module", "Description"], agents, "Discovered Agents")
        except Exception as e:
            print_rich(f"Error discovering agents: {e}", style="bold red")
            print(traceback.format_exc())
    
    elif args.type == "tools":
        print_header("Discovering tools...")
        
        try:
            module_paths = [args.module] if args.module else None
            ids = discover_tools(module_paths)
            
            print_subheader(f"Discovered {len(ids)} tools")
            if ids:
                # Get tool details for table
                tools = []
                for tool_id in ids:
                    tool = registry_system.get_entity(tool_id)
                    if tool:
                        tools.append([
                            tool.name,
                            tool.id,
                            tool.module_path,
                            tool.description[:50] + "..." if tool.description and len(tool.description) > 50 else tool.description
                        ])
                
                # Print table
                print_table(["Name", "ID", "Module", "Description"], tools, "Discovered Tools")
        except Exception as e:
            print_rich(f"Error discovering tools: {e}", style="bold red")
            print(traceback.format_exc())
    
    elif args.type == "toolkits":
        print_header("Discovering toolkits...")
        
        try:
            module_paths = [args.module] if args.module else None
            ids = discover_toolkits(module_paths)
            
            print_subheader(f"Discovered {len(ids)} toolkits")
            if ids:
                # Get toolkit details for table
                toolkits = []
                for toolkit_id in ids:
                    toolkit = registry_system.get_entity(toolkit_id)
                    if toolkit:
                        # Get tool count if available
                        tool_count = 0
                        if toolkit.metadata and "tools" in toolkit.metadata:
                            tools = toolkit.metadata["tools"]
                            tool_count = len(tools) if isinstance(tools, list) else 0
                        
                        toolkits.append([
                            toolkit.name,
                            toolkit.id,
                            tool_count,
                            toolkit.description[:50] + "..." if toolkit.description and len(toolkit.description) > 50 else toolkit.description
                        ])
                
                # Print table
                print_table(["Name", "ID", "Tools", "Description"], toolkits, "Discovered Toolkits")
        except Exception as e:
            print_rich(f"Error discovering toolkits: {e}", style="bold red")
            print(traceback.format_exc())
    
    elif args.type == "engines":
        print_header("Discovering engines...")
        
        try:
            module_paths = [args.module] if args.module else None
            ids = discover_engines(module_paths)
            
            print_subheader(f"Discovered {len(ids)} engines")
            if ids:
                # Get engine details for table
                engines = []
                for engine_id in ids:
                    engine = registry_system.get_entity(engine_id)
                    if engine:
                        # Get provider and model if available
                        provider = engine.metadata.get("provider", "") if engine.metadata else ""
                        model = engine.metadata.get("model", "") if engine.metadata else ""
                        
                        engines.append([
                            engine.name,
                            engine.id,
                            provider,
                            model,
                            engine.description[:50] + "..." if engine.description and len(engine.description) > 50 else engine.description
                        ])
                
                # Print table
                print_table(["Name", "ID", "Provider", "Model", "Description"], engines, "Discovered Engines")
        except Exception as e:
            print_rich(f"Error discovering engines: {e}", style="bold red")
            print(traceback.format_exc())
    
    elif args.type == "games":
        print_header("Discovering games...")
        
        try:
            module_paths = [args.module] if args.module else None
            ids = discover_games(module_paths)
            
            print_subheader(f"Discovered {len(ids)} games")
            if ids:
                # Get game details for table
                games = []
                for game_id in ids:
                    game = registry_system.get_entity(game_id)
                    if game:
                        games.append([
                            game.name,
                            game.id,
                            game.module_path,
                            game.description[:50] + "..." if game.description and len(game.description) > 50 else game.description
                        ])
                
                # Print table
                print_table(["Name", "ID", "Module", "Description"], games, "Discovered Games")
        except Exception as e:
            print_rich(f"Error discovering games: {e}", style="bold red")
            print(traceback.format_exc())


def handle_import(args):
    """Handle the import command."""
    if args.source == "llm-models":
        print_header("Importing LLM models from LiteLLM...")
        
        try:
            success = import_llm_models()
            
            if success:
                print_rich("Successfully imported LLM models", style="bold green")
            else:
                print_rich("Failed to import LLM models", style="bold red")
        except Exception as e:
            print_rich(f"Error importing LLM models: {e}", style="bold red")
            print(traceback.format_exc())


def handle_stats(args):
    """Handle the stats command."""
    print_header("Retrieving registry statistics...")
    
    try:
        stats = registry_system.get_registry_stats()
        
        if "error" in stats:
            print_rich(f"Error retrieving stats: {stats['error']}", style="bold red")
            return
        
        # Print total entities
        print_subheader("Registry Statistics")
        print_rich(f"Total entities: {stats.get('total_entities', 0)}", style="bold")
        
        # Print breakdown by type
        print_subheader("Breakdown by type")
        rows = []
        for entity_type, count in stats.get("by_type", {}).items():
            rows.append([entity_type, count])
        
        # Print table
        print_table(["Entity Type", "Count"], rows)
        
        # Print import status
        print_subheader("Import Status")
        print_rich(f"Successful imports: {stats.get('import_success', 0)}")
        print_rich(f"Failed imports: {stats.get('import_failure', 0)}")
        
        # Print relationships
        print_subheader("Relationships")
        print_rich(f"Environment Variables: {stats.get('environment_vars', 0)}")
        print_rich(f"Dependencies: {stats.get('dependencies', 0)}")
    except Exception as e:
        print_rich(f"Error retrieving stats: {e}", style="bold red")
        print(traceback.format_exc())


def handle_search(args):
    """Handle the search command."""
    entity_type_str = args.type
    search_term = args.term
    
    # Convert string type to EntityType enum
    entity_type = None
    if entity_type_str != "all":
        # Map CLI arg to EntityType
        type_mapping = {
            "agent": EntityType.AGENT,
            "tool": EntityType.TOOL,
            "toolkit": EntityType.TOOLKIT,
            "engine": EntityType.ENGINE,
            "game": EntityType.GAME,
            "llm-model": EntityType.LLM_MODEL,
            "llm-provider": EntityType.LLM_PROVIDER
        }
        entity_type = type_mapping.get(entity_type_str)
    
    print_header(f"Searching for {entity_type_str} components containing '{search_term}'...")
    
    try:
        # Get all entities
        if entity_type:
            entities = registry_system.list_entities(entity_type)
        else:
            entities = registry_system.list_entities()
        
        # Filter by search term if provided
        if search_term:
            filtered_entities = []
            for entity in entities:
                if (search_term.lower() in entity.name.lower() or
                    (entity.description and search_term.lower() in entity.description.lower()) or
                    (entity.module_path and search_term.lower() in entity.module_path.lower()) or
                    (entity.class_name and search_term.lower() in entity.class_name.lower())):
                    filtered_entities.append(entity)
            entities = filtered_entities
        
        # Print results
        if entities:
            print_subheader(f"Found {len(entities)} matching components")
            
            # Group by type
            entities_by_type = {}
            for entity in entities:
                if entity.type not in entities_by_type:
                    entities_by_type[entity.type] = []
                entities_by_type[entity.type].append(entity)
            
            # Print each type
            for entity_type, type_entities in entities_by_type.items():
                print_subheader(f"{entity_type.upper()} Components ({len(type_entities)})")
                
                rows = []
                for entity in type_entities:
                    # Truncate description if needed
                    description = entity.description
                    if description and len(description) > 60:
                        description = description[:57] + "..."
                    
                    rows.append([
                        entity.name,
                        entity.id,
                        description
                    ])
                
                print_table(["Name", "ID", "Description"], rows)
        else:
            print_rich("No matching components found", style="bold yellow")
    except Exception as e:
        print_rich(f"Error searching for components: {e}", style="bold red")
        print(traceback.format_exc())


def handle_show(args):
    """Handle the show command."""
    entity_id = args.id
    
    print_header(f"Retrieving details for component with ID '{entity_id}'...")
    
    try:
        details = registry_system.get_entity_details(entity_id)
        
        if "error" in details:
            print_rich(f"Error: {details['error']}", style="bold red")
            return
        
        # Print basic info
        if RICH_AVAILABLE:
            panel = Panel(
                f"[bold cyan]Name:[/bold cyan] {details.get('name')}\n"
                f"[bold cyan]Type:[/bold cyan] {details.get('type')}\n"
                f"[bold cyan]Description:[/bold cyan] {details.get('description')}"
            )
            console.print(panel)
        else:
            print_subheader("Component Details")
            print(f"Name: {details.get('name')}")
            print(f"Type: {details.get('type')}")
            print(f"Description: {details.get('description')}")
        
        # Print module info
        print_subheader("Implementation")
        print_rich(f"Module: {details.get('module_path')}")
        print_rich(f"Class: {details.get('class_name')}")
        
        # Print metadata if any
        metadata = details.get('metadata', {})
        if metadata:
            print_subheader("Metadata")
            if RICH_AVAILABLE:
                console.print(format_json(metadata))
            else:
                for key, value in metadata.items():
                    print(f"- {key}: {value}")
        
        # Print configurations
        configs = details.get('configurations', [])
        if configs:
            print_subheader("Configurations")
            for i, config in enumerate(configs):
                print_rich(f"Configuration {i+1}: {config.get('type')}", style="bold")
                
                if config.get('type') in ['state_schema', 'input_schema', 'output_schema']:
                    # For schemas, print fields
                    if isinstance(config.get('data'), dict) and 'fields' in config.get('data'):
                        fields = config.get('data').get('fields', [])
                        
                        rows = []
                        for field in fields:
                            rows.append([
                                field.get('name', ''),
                                field.get('type', ''),
                                "Required" if field.get('required') else "Optional",
                                str(field.get('default', ''))
                            ])
                        
                        print_table(["Field", "Type", "Required", "Default"], rows)
                    else:
                        # Just print the data
                        print_rich(format_json(config.get('data')))
                else:
                    # For other configs, print the data
                    print_rich(format_json(config.get('data')))
        
        # Print graph if available
        graph = details.get('graph')
        if graph:
            print_subheader("Graph Definition")
            print_rich(f"Nodes: {len(graph.get('nodes', []))}")
            print_rich(f"Edges: {len(graph.get('edges', []))}")
            
            # Print nodes
            if graph.get('nodes'):
                print_rich("Nodes:", style="bold")
                for node in graph.get('nodes', []):
                    print_rich(f"- {node.get('name', 'unnamed')}: {node.get('type', 'unknown type')}")
        
        # Print dependencies
        dependencies = details.get('dependencies', [])
        if dependencies:
            print_subheader("Dependencies")
            
            rows = []
            for dep in dependencies:
                rows.append([
                    dep.get('dependent_name', ''),
                    dep.get('dependent_id', ''),
                    dep.get('type', '')
                ])
            
            print_table(["Dependent", "ID", "Type"], rows)
        
        # Print environment variables
        env_vars = details.get('environment_vars', [])
        if env_vars:
            print_subheader("Environment Variables")
            
            rows = []
            for env in env_vars:
                rows.append([
                    env.get('name', ''),
                    "Required" if env.get('is_required') else "Optional",
                    env.get('default_value', '')
                ])
            
            print_table(["Variable", "Status", "Default Value"], rows)
    except Exception as e:
        print_rich(f"Error retrieving entity details: {e}", style="bold red")
        print(traceback.format_exc())


def handle_list(args):
    """Handle the list command."""
    entity_type_str = args.type
    
    # Convert string type to EntityType enum
    entity_type = None
    if entity_type_str != "all":
        # Map CLI arg to EntityType
        type_mapping = {
            "agents": EntityType.AGENT,
            "tools": EntityType.TOOL,
            "toolkits": EntityType.TOOLKIT,
            "engines": EntityType.ENGINE,
            "games": EntityType.GAME,
            "llm-models": EntityType.LLM_MODEL,
            "llm-providers": EntityType.LLM_PROVIDER
        }
        entity_type = type_mapping.get(entity_type_str)
    
    print_header(f"Listing {entity_type_str} in registry...")
    
    try:
        # Get entities
        if entity_type:
            entities = registry_system.list_entities(entity_type)
        else:
            entities = registry_system.list_entities()
        
        # Print results
        if entities:
            # Group by type if listing all
            if entity_type_str == "all":
                entities_by_type = {}
                for entity in entities:
                    if entity.type not in entities_by_type:
                        entities_by_type[entity.type] = []
                    entities_by_type[entity.type].append(entity)
                
                # Print each type
                for type_name, type_entities in entities_by_type.items():
                    print_subheader(f"{type_name.upper()} Components ({len(type_entities)})")
                    
                    rows = []
                    for entity in type_entities:
                        # Truncate description if needed
                        description = entity.description
                        if description and len(description) > 60:
                            description = description[:57] + "..."
                        
                        rows.append([
                            entity.name,
                            entity.id,
                            description
                        ])
                    
                    print_table(["Name", "ID", "Description"], rows)
            else:
                # Print single type
                print_subheader(f"Found {len(entities)} {entity_type_str}")
                
                rows = []
                for entity in entities:
                    # Truncate description if needed
                    description = entity.description
                    if description and len(description) > 60:
                        description = description[:57] + "..."
                    
                    rows.append([
                        entity.name,
                        entity.id,
                        description
                    ])
                
                print_table(["Name", "ID", "Description"], rows)
        else:
            print_rich(f"No {entity_type_str} found in registry", style="bold yellow")
    except Exception as e:
        print_rich(f"Error listing entities: {e}", style="bold red")
        print(traceback.format_exc())


def handle_clear(args):
    """Handle the clear command."""
    force = args.force
    
    if not force:
        confirm = input("WARNING: This will clear all registry data. This action cannot be undone.\nAre you sure? (y/N): ")
        if confirm.lower() != 'y':
            print_rich("Operation cancelled.", style="bold yellow")
            return
    
    print_header("Clearing registry...")
    
    try:
        success = registry_system.clear_registry()
        
        if success:
            print_rich("Registry cleared successfully", style="bold green")
        else:
            print_rich("Failed to clear registry", style="bold red")
    except Exception as e:
        print_rich(f"Error clearing registry: {e}", style="bold red")
        print(traceback.format_exc())


def main():
    """Main function."""
    parser = setup_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Handle commands
    if args.command == "discover":
        handle_discover(args)
    elif args.command == "import":
        handle_import(args)
    elif args.command == "stats":
        handle_stats(args)
    elif args.command == "search":
        handle_search(args)
    elif args.command == "show":
        handle_show(args)
    elif args.command == "list":
        handle_list(args)
    elif args.command == "clear":
        handle_clear(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()