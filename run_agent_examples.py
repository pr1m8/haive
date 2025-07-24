#!/usr/bin/env python3
"""Agent-Specific Example Runner - Run examples for specific agent types.
================================================================

This script makes it easy to find and run examples for specific agent classes:

Usage:
    python run_agent_examples.py --agent SimpleAgent
    python run_agent_examples.py --agent ReactAgent --visualize
    python run_agent_examples.py --list-agents
    python run_agent_examples.py --agent-type simple
"""

import argparse
import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional

from scripts.doc_utils.example_runner import ExecutionConfig, UniversalExampleRunner

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentExampleRunner:
    """Agent-specific example discovery and execution."""

    def __init__(self):
        self.runner = UniversalExampleRunner()
        self.agent_examples_map = {}

    async def discover_agent_examples(self) -> dict[str, list[Path]]:
        """Discover examples organized by agent type."""

        all_examples = await self.runner.discover_all_examples()
        agent_map = {}

        # Categorize examples by agent type
        for example_file in all_examples:
            agent_types = self._detect_agent_types_in_file(example_file)

            for agent_type in agent_types:
                if agent_type not in agent_map:
                    agent_map[agent_type] = []
                agent_map[agent_type].append(example_file)

        # Also organize by path-based categories
        path_categories = {
            "simple": "SimpleAgent",
            "react": "ReactAgent",
            "rag": "RAGAgent",
            "planning": "PlanningAgent",
            "conversation": "ConversationAgent",
            "research": "ResearchAgent",
            "games": "GameAgent",
            "multi": "MultiAgent",
        }

        for example_file in all_examples:
            path_str = str(example_file).lower()
            for path_key, agent_class in path_categories.items():
                if path_key in path_str:
                    if agent_class not in agent_map:
                        agent_map[agent_class] = []
                    if example_file not in agent_map[agent_class]:
                        agent_map[agent_class].append(example_file)

        self.agent_examples_map = agent_map
        return agent_map

    def _detect_agent_types_in_file(self, example_file: Path) -> list[str]:
        """Detect agent types used in an example file."""
        try:
            with open(example_file) as f:
                content = f.read()

            agent_types = []

            # Look for import statements and class usage
            lines = content.split("\n")
            for line in lines:
                line = line.strip()

                # Check imports
                if "from haive.agents" in line:
                    if "SimpleAgent" in line:
                        agent_types.append("SimpleAgent")
                    if "ReactAgent" in line:
                        agent_types.append("ReactAgent")
                    if "RAGAgent" in line or "BaseRAGAgent" in line:
                        agent_types.append("RAGAgent")
                    if "PlanningAgent" in line:
                        agent_types.append("PlanningAgent")
                    if "MultiAgent" in line:
                        agent_types.append("MultiAgent")

                # Check class instantiation
                if "=" in line and "Agent(" in line:
                    for agent_type in [
                        "SimpleAgent",
                        "ReactAgent",
                        "RAGAgent",
                        "PlanningAgent",
                        "MultiAgent",
                    ]:
                        if agent_type in line:
                            agent_types.append(agent_type)

            return list(set(agent_types))  # Remove duplicates

        except Exception as e:
            logger.debug(f"Could not analyze {example_file}: {e}")
            return []

    def list_available_agents(self) -> None:
        """List all available agent types with example counts."""
        if not self.agent_examples_map:
            return


        for agent_type, examples in sorted(self.agent_examples_map.items()):
            count = len(examples)

        total = sum(len(examples) for examples in self.agent_examples_map.values())

    def list_examples_for_agent(self, agent_type: str) -> list[Path]:
        """List examples for a specific agent type."""
        if agent_type not in self.agent_examples_map:
            return []

        examples = self.agent_examples_map[agent_type]

        for i, example in enumerate(examples, 1):
            rel_path = example.relative_to(self.runner.project_root)

        return examples

    async def run_agent_examples(
        self, agent_type: str, visualize: bool = True, concurrent: int = 2
    ) -> None:
        """Run all examples for a specific agent type."""
        examples = self.list_examples_for_agent(agent_type)

        if not examples:
            return


        # Configure execution
        config = ExecutionConfig(
            timeout_seconds=300,
            enable_visualization=visualize,
            stream_output=True,
            save_full_output=True,
        )

        # Ask for confirmation
        response = input(f"\n🤔 Run {len(examples)} examples? (y/N): ")
        if response.lower() not in ["y", "yes"]:
            return


        # Run examples
        results = await self.runner.run_multiple_examples(
            examples, config, max_concurrent=concurrent
        )

        # Show results
        successful = sum(1 for r in results if r.success)
        failed = len(results) - successful


        # Show visualizations
        viz_files = [r.visualization_path for r in results if r.visualization_path]
        if viz_files:
            for viz_file in viz_files:
                pass")

        # Show failures
        if failed > 0:
            for result in results:
                if not result.success:
                    example_name = Path(
                        result.metadata.get("example_path", "Unknown")
                    ).name

    async def run_single_example(
        self, example_path: str, visualize: bool = True
    ) -> None:
        """Run a single example by path."""
        example_file = Path(example_path)

        if not example_file.exists():
            # Try to find it relative to project root
            example_file = self.runner.project_root / example_path

        if not example_file.exists():
            return


        config = ExecutionConfig(
            timeout_seconds=300, enable_visualization=visualize, stream_output=True
        )

        result = await self.runner.run_example(example_file, config)

        if result.success:

            if result.visualization_path:
                pass}")
        else:
            pass")

    def search_examples(self, search_term: str) -> list[Path]:
        """Search examples by name or content."""
        matching_examples = []

        for examples in self.agent_examples_map.values():
            for example in examples:
                # Search in filename
                if search_term.lower() in example.name.lower():
                    matching_examples.append(example)
                    continue

                # Search in file content
                try:
                    with open(example) as f:
                        content = f.read().lower()
                    if search_term.lower() in content:
                        matching_examples.append(example)
                except Exception:
                    pass

        return list(set(matching_examples))  # Remove duplicates


async def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="Run examples for specific agent types"
    )
    parser.add_argument(
        "--agent", help="Specific agent class to run (e.g., SimpleAgent)"
    )
    parser.add_argument(
        "--agent-type", help="Agent type category (e.g., simple, react, rag)"
    )
    parser.add_argument(
        "--list-agents", action="store_true", help="List all available agent types"
    )
    parser.add_argument("--list-examples", help="List examples for specific agent type")
    parser.add_argument("--run-single", help="Run a single example by path")
    parser.add_argument("--search", help="Search examples by term")
    parser.add_argument(
        "--visualize", action="store_true", default=True, help="Generate visualizations"
    )
    parser.add_argument(
        "--no-visualize", action="store_true", help="Skip visualization generation"
    )
    parser.add_argument(
        "--concurrent", type=int, default=2, help="Max concurrent executions"
    )

    args = parser.parse_args()

    if args.no_visualize:
        args.visualize = False

    runner = AgentExampleRunner()


    # Discover examples
    await runner.discover_agent_examples()

    if args.list_agents:
        runner.list_available_agents()
        return

    if args.list_examples:
        runner.list_examples_for_agent(args.list_examples)
        return

    if args.search:
        examples = runner.search_examples(args.search)
        for i, example in enumerate(examples, 1):
            rel_path = example.relative_to(runner.runner.project_root)
        return

    if args.run_single:
        await runner.run_single_example(args.run_single, args.visualize)
        return

    if args.agent:
        await runner.run_agent_examples(args.agent, args.visualize, args.concurrent)
        return

    if args.agent_type:
        # Map agent type to class name
        type_mapping = {
            "simple": "SimpleAgent",
            "react": "ReactAgent",
            "rag": "RAGAgent",
            "planning": "PlanningAgent",
            "multi": "MultiAgent",
            "conversation": "ConversationAgent",
            "research": "ResearchAgent",
            "games": "GameAgent",
        }

        agent_class = type_mapping.get(args.agent_type.lower())
        if agent_class:
            await runner.run_agent_examples(
                agent_class, args.visualize, args.concurrent
            )
        else:
        return

    # Interactive mode

    while True:
        choice = input("\nSelect option (1-4, or 'q' to quit): ").strip()

        if choice.lower() == "q":
            break
        if choice == "1":
            runner.list_available_agents()
        elif choice == "2":
            runner.list_available_agents()
            agent_type = input("\nEnter agent type: ").strip()
            if agent_type:
                await runner.run_agent_examples(
                    agent_type, args.visualize, args.concurrent
                )
        elif choice == "3":
            search_term = input("Enter search term: ").strip()
            if search_term:
                examples = runner.search_examples(search_term)
                for i, example in enumerate(examples, 1):
                    rel_path = example.relative_to(runner.runner.project_root)
        elif choice == "4":
            example_path = input("Enter example path: ").strip()
            if example_path:
                await runner.run_single_example(example_path, args.visualize)
        else:
            pass")


if __name__ == "__main__":
    asyncio.run(main())
