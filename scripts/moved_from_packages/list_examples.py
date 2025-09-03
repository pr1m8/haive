#!/usr/bin/env python3
"""Quick Example Lister - See all examples at a glance.

Usage:
  python list_examples.py                 # Show all examples
  python list_examples.py beginner        # Show beginner examples
  python list_examples.py --tree          # Show as directory tree
  python list_examples.py --run simple    # Quick run an example by name
  python list_examples.py --stats         # Show quick statistics
"""

import argparse
import subprocess
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree

console = Console()

# Example locations and metadata
EXAMPLE_LOCATIONS = {
    "🌱 Beginner Gallery": {
        "path": "galleries/beginner/",
        "examples": [
            ("simple_agent_tutorial.py", "1 min", "⭐", "Your first agent"),
            ("react_agent_tutorial.py", "10 min", "⭐⭐", "Tools & reasoning"),
            ("simple_agent_example.py", "1 min", "⭐", "Basic demo"),
            ("react_agent_example.py", "10 min", "⭐⭐", "Tool demo"),
        ],
    },
    "🌿 Intermediate Gallery": {
        "path": "galleries/intermediate/",
        "examples": [
            ("plan_and_execute_guide.py", "10 min", "⭐⭐⭐", "Strategic planning"),
            ("multi_agent_example.py", "20 min", "⭐⭐⭐", "Agent coordination"),
            ("structured_output_demo.py", "10 min", "⭐⭐", "Data extraction"),
        ],
    },
    "🌲 Advanced Gallery": {
        "path": "galleries/advanced/",
        "examples": [
            (
                "dynamic_activation_advanced_example.py",
                "30 min",
                "⭐⭐⭐⭐",
                "Dynamic network",
            ),
        ],
    },
    "🎮 Games Gallery": {
        "path": "galleries/games/",
        "examples": [
            ("tic_tac_toe_ai.py", "10 min", "⭐⭐", "Game strategy"),
            ("chess_strategy.py", "20 min", "⭐⭐⭐", "Chess AI"),
        ],
    },
    "🏛️ Legacy Example": {
        "path": "example/",
        "examples": [
            ("plan_and_execute_example.py", "10 min", "⭐⭐⭐", "Original planning"),
            ("dynamic_activation_basic_example.py", "20 min", "⭐⭐", "Basic dynamic"),
            ("dynamic_react_agent_example.py", "10 min", "⭐⭐", "Dynamic react"),
            ("dynamic_supervisor_demo.py", "20 min", "⭐⭐⭐", "Supervisor demo"),
            ("dynamic_supervisor_example.py", "20 min", "⭐⭐⭐", "Supervisor example"),
            ("enhanced_memory_retriever_demo.py", "20 min", "⭐⭐⭐", "Memory system"),
            ("full_supervisor_demo.py", "30 min", "⭐⭐⭐⭐", "Full supervisor"),
            ("output_adapter_demo.py", "10 min", "⭐⭐", "Output formatting"),
            ("token_tracking_example.py", "10 min", "⭐⭐", "Token management"),
            (
                "validation_integration_example.py",
                "10 min",
                "⭐⭐⭐",
                "Validation pattern",
            ),
        ],
    },
    "🎯 Reference Pattern": {
        "path": "reference/",
        "examples": [
            ("agent_type/", "Various", "📚", "Agent implementation pattern"),
            ("tool/", "Various", "📚", "Tool development pattern"),
            ("state/", "Various", "📚", "State management pattern"),
            ("integration/", "Various", "📚", "Integration pattern"),
        ],
    },
    "🚀 Production Showcase": {
        "path": "showcase/",
        "examples": [
            ("chat_assistant.py", "As needed", "🏭", "Production chat bot"),
            ("research_assistant.py", "As needed", "🏭", "Research automation"),
            ("code_analyst.py", "As needed", "🏭", "Code analysis"),
            ("game_coordinator.py", "As needed", "🏭", "Game management"),
            ("workflow_automation.py", "As needed", "🏭", "Business automation"),
        ],
    },
}


def show_all_examples():
    """Show all examples in a comprehensive table."""
    console.print("[bold blue]📋 All Haive Examples[/bold blue]")
    console.print()

    for category, info in EXAMPLE_LOCATIONS.items():
        console.print(f"[bold cyan]{category}[/bold cyan]")
        console.print(f"[dim]📁 {info['path']}[/dim]")

        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("Name", min_width=3)
        table.add_column("Time", width=10)
        table.add_column("Difficulty", width=1)
        table.add_column("Description", min_width=2)

        for name, time, difficulty, desc in info["examples"]:
            # Check if file exists
            full_path = Path(info["path"]) / name
            if full_path.exists():
                status = "✅"
            elif full_path.is_dir():
                status = "📁"
            else:
                status = "❌"

            table.add_row(f"{status} {name}", time, difficulty, desc)

        console.print(table)
        console.print()


def show_tree_view():
    """Show examples as a directory tree."""
    console.print("[bold blue]🌳 Haive Examples Tree[/bold blue]")
    console.print()

    tree = Tree("[bold blue]📁 haive-agents[/bold blue]")

    for category, info in EXAMPLE_LOCATIONS.items():
        category_node = tree.add(f"[cyan]{category}[/cyan]")
        path_node = category_node.add(f"[dim]📁 {info['path']}[/dim]")

        for name, time, difficulty, desc in info["examples"]:
            full_path = Path(info["path"]) / name
            if full_path.exists():
                status = "✅"
            elif full_path.is_dir():
                status = "📁"
            else:
                status = "❌"

            path_node.add(
                f"{status} [green]{name}[/green] [dim]({time}, {difficulty})[/dim] - {desc}"
            )

    console.print(tree)
    console.print()


def show_category(category_name: str):
    """Show examples for a specific category."""
    # Find matching category
    matching_category = None
    for cat_name, info in EXAMPLE_LOCATIONS.items():
        if category_name.lower() in cat_name.lower():
            matching_category = (cat_name, info)
            break

    if not matching_category:
        console.print(f"[red]❌ Category '{category_name}' not found[/red]")
        console.print("[yellow]Available categories:[/yellow]")
        for cat_name in EXAMPLE_LOCATIONS:
            console.print(f"  • {cat_name}")
        return

    cat_name, info = matching_category

    console.print(f"[bold cyan]{cat_name}[/bold cyan]")
    console.print(f"[dim]📁 {info['path']}[/dim]")
    console.print()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Status", width=1)
    table.add_column("Example", min_width=3)
    table.add_column("Time", width=1)
    table.add_column("Difficulty", width=1)
    table.add_column("Description", min_width=2)

    for name, time, difficulty, desc in info["examples"]:
        full_path = Path(info["path"]) / name
        if full_path.exists():
            status = "✅"
        elif full_path.is_dir():
            status = "📁"
        else:
            status = "❌"

        table.add_row(status, name, time, difficulty, desc)

    console.print(table)
    console.print()


def quick_run(example_name: str):
    """Quickly run an example by name."""
    # Find the example
    found_example = None
    for _category, info in EXAMPLE_LOCATIONS.items():
        for name, _time, _difficulty, desc in info["examples"]:
            if example_name.lower() in name.lower():
                found_example = (name, info["path"], desc)
                break
        if found_example:
            break

    if not found_example:
        console.print(f"[red]❌ Example '{example_name}' not found[/red]")
        return

    name, path, desc = found_example
    full_path = Path(path) / name

    if not full_path.exists():
        console.print(f"[red]❌ Example file not found: {full_path}[/red]")
        return

    console.print(f"[yellow]🚀 Running {name}...[/yellow]")
    console.print(f"[dim]{desc}[/dim]")
    console.print(f"[dim]📁 {full_path}[/dim]")
    console.print()

    try:
        cmd = ["poetry", "run", "python", str(full_path)]
        console.print(f"[dim]Command: {' '.join(cmd)}[/dim]")
        console.print("[dim]" + "=" * 10 + "[/dim]")

        result = subprocess.run(cmd, capture_output=False, check=False)

        console.print("[dim]" + "=" * 10 + "[/dim]")
        if result.returncode == 0:
            console.print(f"[green]✅ {name} completed successfully![/green]")
        else:
            console.print(
                f"[red]❌ {name} failed with exit code {result.returncode}[/red]"
            )

    except Exception as e:
        console.print(f"[red]❌ Error running {name}: {e}[/red]")


def show_quick_stats():
    """Show quick statistics."""
    total_examples = sum(len(info["examples"]) for info in EXAMPLE_LOCATIONS.values())

    stats_panel = Panel.fit(
        "[bold blue]📊 Quick Stats[/bold blue]\n\n"
        f"[cyan]Total Examples:[/cyan] {total_examples}\n"
        f"[cyan]Categories:[/cyan] {len(EXAMPLE_LOCATIONS)}\n\n"
        f"[green]✅ Beginner:[/green] {len(EXAMPLE_LOCATIONS['🌱 Beginner Gallery']['examples'])}\n"
        f"[yellow]🌿 Intermediate:[/yellow] {len(EXAMPLE_LOCATIONS['🌿 Intermediate Gallery']['examples'])}\n"
        f"[red]🌲 Advanced:[/red] {len(EXAMPLE_LOCATIONS['🌲 Advanced Gallery']['examples'])}\n"
        f"[blue]🎮 Games:[/blue] {len(EXAMPLE_LOCATIONS['🎮 Games Gallery']['examples'])}\n"
        f"[dim]🏛️ Legacy:[/dim] {len(EXAMPLE_LOCATIONS['🏛️ Legacy Example']['examples'])}",
        title="Haive Examples",
        border_style="blue",
    )
    console.print(stats_panel)
    console.print()


def main():
    parser = argparse.ArgumentParser(description="Haive Examples Quick Lister")
    parser.add_argument(
        "category",
        nargs="?",
        help="Show specific category (beginner, intermediate, advanced, games, legacy)",
    )
    parser.add_argument("--tree", action="store_true", help="Show as directory tree")
    parser.add_argument("--run", help="Quick run an example by name")
    parser.add_argument("--stats", action="store_true", help="Show quick statistics")

    args = parser.parse_args()

    if args.stats:
        show_quick_stats()
    elif args.run:
        quick_run(args.run)
    elif args.tree:
        show_tree_view()
    elif args.category:
        show_category(args.category)
    else:
        show_all_examples()


if __name__ == "__main__":
    main()
