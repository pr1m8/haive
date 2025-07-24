#!/usr/bin/env python3
"""Module Example Runner - Run example.py files from specific agent/game modules.
==========================================================================

This script finds and runs the example.py files that are embedded within each
agent and game module, supporting different visualization types and configurations.

Usage:
    python run_module_examples.py --list-modules
    python run_module_examples.py --module simple --visualize
    python run_module_examples.py --module chess --run
    python run_module_examples.py --type agent --visualize
"""

import argparse
import asyncio
import importlib.util
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from scripts.doc_utils.example_runner import ExecutionConfig, UniversalExampleRunner


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModuleExampleRunner:
    """Runner for module-specific example.py files."""

    def __init__(self):
        self.runner = UniversalExampleRunner()
        self.project_root = self.runner.project_root

    def discover_module_examples(self) -> dict[str, dict[str, any]]:
        """Discover example.py files in agent and game modules."""

        modules = {}

        # Discover agent modules
        agent_modules = self._discover_agent_modules()
        for module_info in agent_modules:
            modules[module_info["name"]] = module_info

        # Discover game modules
        game_modules = self._discover_game_modules()
        for module_info in game_modules:
            modules[module_info["name"]] = module_info

        return modules

    def _discover_agent_modules(self) -> list[dict[str, any]]:
        """Discover agent modules with example.py files."""
        agent_base = self.project_root / "packages/haive-agents/src/haive/agents"
        modules = []

        for example_file in agent_base.rglob("example.py"):
            # Extract module path and info
            relative_path = example_file.relative_to(agent_base)
            module_path_parts = relative_path.parts[:-1]  # Remove 'example.py'

            if not module_path_parts:
                continue

            module_name = "/".join(module_path_parts)
            module_dir = example_file.parent

            # Try to find agent.py in same directory
            agent_file = module_dir / "agent.py"

            # Determine agent type from path
            agent_type = self._classify_agent_type(module_path_parts)

            module_info = {
                "name": module_name,
                "type": "agent",
                "agent_type": agent_type,
                "example_file": example_file,
                "module_dir": module_dir,
                "agent_file": agent_file if agent_file.exists() else None,
                "description": self._get_module_description(example_file, agent_type),
                "supports_viz": self._check_visualization_support(module_dir),
                "config_pattern": self._detect_config_pattern(example_file),
            }

            modules.append(module_info)

        return modules

    def _discover_game_modules(self) -> list[dict[str, any]]:
        """Discover game modules with example.py files."""
        games_base = self.project_root / "packages/haive-games/src/haive/games"
        modules = []

        for example_file in games_base.rglob("example.py"):
            relative_path = example_file.relative_to(games_base)
            module_path_parts = relative_path.parts[:-1]

            if not module_path_parts:
                continue

            game_name = "/".join(module_path_parts)
            module_dir = example_file.parent

            # Look for game-specific files
            game_file = module_dir / "game.py"
            agent_file = module_dir / "agent.py"

            module_info = {
                "name": game_name,
                "type": "game",
                "agent_type": "GameAgent",
                "example_file": example_file,
                "module_dir": module_dir,
                "game_file": game_file if game_file.exists() else None,
                "agent_file": agent_file if agent_file.exists() else None,
                "description": self._get_game_description(game_name),
                "supports_viz": self._check_game_visualization_support(module_dir),
                "config_pattern": self._detect_config_pattern(example_file),
            }

            modules.append(module_info)

        return modules

    def _classify_agent_type(self, path_parts: tuple[str, ...]) -> str:
        """Classify agent type from module path."""
        path_str = "/".join(path_parts).lower()

        if "simple" in path_str:
            return "SimpleAgent"
        if "react" in path_str:
            return "ReactAgent"
        elif "rag" in path_str:
            return "RAGAgent"
        elif "planning" in path_str or "plan" in path_str:
            return "PlanningAgent"
        elif "reasoning" in path_str or "critique" in path_str:
            return "ReasoningAgent"
        elif "research" in path_str:
            return "ResearchAgent"
        elif "conversation" in path_str:
            return "ConversationAgent"
        elif "sequential" in path_str:
            return "SequentialAgent"
        else:
            return "Agent"

    def _get_module_description(self, example_file: Path, agent_type: str) -> str:
        """Get description from example file docstring."""
        try:
            with open(example_file) as f:
                content = f.read()

            # Look for module docstring
            lines = content.split("\n")
            for i, line in enumerate(lines[:10]):
                if '"""' in line or "'''" in line:
                    # Extract first line of docstring
                    desc_start = (
                        line.find('"""') + 3 if '"""' in line else line.find("'''") + 3
                    )
                    first_desc = line[desc_start:].strip()
                    if first_desc:
                        return first_desc[:100]

                    # Check next line
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if next_line and not next_line.startswith(('"""', "'''")):
                            return next_line[:100]

            return f"{agent_type} example demonstration"

        except Exception:
            return f"{agent_type} example"

    def _get_game_description(self, game_name: str) -> str:
        """Get description for game module."""
        descriptions = {
            "chess": "Classic chess game with AI opponents",
            "tic_tac_toe": "Simple 3x3 grid strategy game",
            "checkers": "Classic checkers with jumping rules",
            "monopoly": "Property trading and economic strategy",
            "clue": "Mystery solving deduction game",
            "mafia": "Social deduction party game",
            "poker": "Texas Hold'em poker with AI players",
            "nim": "Mathematical strategy game",
            "mastermind": "Code-breaking logic puzzle",
            "mancala": "Ancient count-and-capture game",
        }

        base_name = game_name.split("/")[-1]
        return descriptions.get(base_name, f"{base_name.title()} game")

    def _check_visualization_support(self, module_dir: Path) -> bool:
        """Check if module supports visualization."""
        # Look for visualization-related files or code
        viz_files = ["visualize.py", "viz.py", "graph.py", "diagram.py"]

        for viz_file in viz_files:
            if (module_dir / viz_file).exists():
                return True

        # Check if agent.py has visualization methods
        agent_file = module_dir / "agent.py"
        if agent_file.exists():
            try:
                with open(agent_file) as f:
                    content = f.read()
                if "visualize" in content.lower() or "graph" in content.lower():
                    return True
            except Exception:
                pass

        return True  # Assume most agents support basic visualization

    def _check_game_visualization_support(self, module_dir: Path) -> bool:
        """Check if game supports visualization."""
        # Games often have board representations or game state visualization
        viz_indicators = ["board.py", "display.py", "render.py", "visualize.py"]

        for indicator in viz_indicators:
            if (module_dir / indicator).exists():
                return True

        return True  # Most games can show state

    def _detect_config_pattern(self, example_file: Path) -> str:
        """Detect configuration pattern used in example."""
        try:
            with open(example_file) as f:
                content = f.read()

            if "AugLLMConfig" in content:
                return "AugLLMConfig"
            if "Config" in content:
                return "Config"
            elif "config" in content.lower():
                return "config"
            else:
                return "default"

        except Exception:
            return "unknown"

    def list_modules(self, modules: dict[str, dict[str, any]]) -> None:
        """List all discovered modules."""

        # Group by type and agent_type
        agents_by_type = {}
        games = []

        for name, info in modules.items():
            if info["type"] == "agent":
                agent_type = info["agent_type"]
                if agent_type not in agents_by_type:
                    agents_by_type[agent_type] = []
                agents_by_type[agent_type].append((name, info))
            else:
                games.append((name, info))

        # Show agents by type
        for agent_type, agent_list in sorted(agents_by_type.items()):
            for name, info in sorted(agent_list):
                viz_icon = "🎨" if info["supports_viz"] else "  "
                config_info = f"[{info['config_pattern']}]"

        # Show games
        if games:
            for name, info in sorted(games):
                viz_icon = "🎨" if info["supports_viz"] else "  "


    async def run_module_example(
        self,
        module_name: str,
        modules: dict[str, dict[str, any]],
        visualize: bool = True,
        auto_confirm: bool = False,
    ) -> None:
        """Run example for a specific module."""
        if module_name not in modules:
            return

        module_info = modules[module_name]
        example_file = module_info["example_file"]


        # Configure execution
        config = ExecutionConfig(
            timeout_seconds=300,  # 5 minutes max
            enable_visualization=visualize and module_info["supports_viz"],
            stream_output=True,
            save_full_output=True,
            max_output_size=200000,  # 200KB limit
        )

        # Confirm execution
        if not auto_confirm:
            try:
                response = input(f"\n🤔 Run {module_name} example? (y/N): ")
                if response.lower() not in ["y", "yes"]:
                    return
            except (EOFError, KeyboardInterrupt):
                return
        else:
            pass")


        try:
            # Run the example with proper error handling
            result = await self.runner.run_example(example_file, config)

            # Show results
            if result.success:

                if result.visualization_path:
                    pass}")

                if result.output_file:
                    pass}")

                # Show preview of output
                if result.output:
                    preview = result.output[:500]
                    if len(result.output) > 500:
                        pass

            else:

        except Exception as e:
            logger.exception(f"Exception: {e}")

    async def run_type_examples(
        self,
        example_type: str,
        modules: dict[str, dict[str, any]],
        visualize: bool = True,
        max_examples: int = 3,
    ) -> None:
        """Run examples for all modules of a specific type."""
        # Filter modules by type
        if example_type == "agent":
            filtered = {
                name: info for name, info in modules.items() if info["type"] == "agent"
            }
        elif example_type == "game":
            filtered = {
                name: info for name, info in modules.items() if info["type"] == "game"
            }
        else:
            # Try to match as agent_type
            filtered = {
                name: info
                for name, info in modules.items()
                if info.get("agent_type", "").lower() == example_type.lower()
            }

        if not filtered:
            return

        # Limit number of examples
        limited = dict(list(filtered.items())[:max_examples])


        # Confirm
        response = input(f"\n🤔 Run {len(limited)} {example_type} examples? (y/N): ")
        if response.lower() not in ["y", "yes"]:
            return

        # Run each example
        for i, (module_name, module_info) in enumerate(limited.items(), 1):

            try:
                config = ExecutionConfig(
                    timeout_seconds=180,  # 3 minutes per example
                    enable_visualization=visualize and module_info["supports_viz"],
                    stream_output=False,  # Less verbose for batch
                    save_full_output=True,
                    max_output_size=100000,
                )

                result = await self.runner.run_example(
                    module_info["example_file"], config
                )

                status = "✅" if result.success else "❌"
                time_str = f"{result.execution_time:.1f}s"
                viz_str = "🎨"��" if result.visualization_path else ""


                if not result.success:
                    pass

            except Exception as e:
                pass")


async def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(description="Run module-specific example.py files")
    parser.add_argument(
        "--list-modules", action="store_true", help="List all available modules"
    )
    parser.add_argument(
        "--module", help="Run example for specific module (e.g., simple, chess)"
    )
    parser.add_argument(
        "--type", help="Run examples for type (agent, game, SimpleAgent, etc.)"
    )
    parser.add_argument(
        "--visualize", action="store_true", default=True, help="Generate visualizations"
    )
    parser.add_argument("--no-viz", action="store_true", help="Skip visualizations")
    parser.add_argument(
        "--max", type=int, default=3, help="Max examples for type (default: 3)"
    )
    parser.add_argument(
        "--auto", action="store_true", help="Auto-confirm execution (no prompts)"
    )

    args = parser.parse_args()

    if args.no_viz:
        args.visualize = False

    runner = ModuleExampleRunner()


    # Discover modules
    try:
        modules = runner.discover_module_examples()

        if not modules:
            return

    except Exception as e:
        logger.exception(f"Discovery error: {e}")
        return

    if args.list_modules:
        runner.list_modules(modules)
        return

    if args.module:
        await runner.run_module_example(args.module, modules, args.visualize, args.auto)
        return

    if args.type:
        await runner.run_type_examples(args.type, modules, args.visualize, args.max)
        return

    # Interactive mode
    runner.list_modules(modules)

    while True:

        choice = input("\nSelect option (1-3, or 'q' to quit): ").strip()

        if choice.lower() == "q":
            break
        if choice == "1":
            module_name = input("Enter module name: ").strip()
            if module_name:
                await runner.run_module_example(module_name, modules, args.visualize)
        elif choice == "2":
            example_type = input(
                "Enter type (agent, game, SimpleAgent, etc.): "
            ).strip()
            if example_type:
                await runner.run_type_examples(
                    example_type, modules, args.visualize, args.max
                )
        elif choice == "3":
            runner.list_modules(modules)
        else:
            pass")


if __name__ == "__main__":
    asyncio.run(main())
