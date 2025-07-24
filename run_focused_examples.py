#!/usr/bin/env python3
"""Focused Example Runner - Run examples for agents and games only.
===========================================================

This script focuses on the core agent and game examples, skipping problematic packages
and using proper error handling.

Usage:
    python run_focused_examples.py --agent SimpleAgent
    python run_focused_examples.py --type react --visualize
    python run_focused_examples.py --list
"""

import argparse
import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional

from scripts.doc_utils.example_runner import ExecutionConfig, UniversalExampleRunner

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FocusedExampleRunner:
    """Focused runner for agents and games examples only."""

    def __init__(self):
        self.runner = UniversalExampleRunner()
        self.focus_packages = ["haive-agents", "haive-games", "haive-core"]
        self.skip_patterns = [
            # Skip .venv directories
            "*/.venv/*",
            "*/site-packages/*",
            # Skip prebuilt (as requested)
            "*/haive-prebuilt/*",
            # Skip broken test files
            "*/test_all_agents_comprehensive.py",
            "*/test_agent_supabase_standalone.py",
            "*react_agent_v3_comprehensive.py",
            "*simple_agent_v3_structured_output.py",
        ]

    async def discover_focused_examples(self) -> dict[str, list[Path]]:
        """Discover examples from agents and games packages only."""

        try:
            all_examples = await self.runner.discover_all_examples()

            # Filter to focus packages only
            focused_examples = []
            for example in all_examples:
                example_str = str(example)

                # Skip if not in focus packages
                if not any(pkg in example_str for pkg in self.focus_packages):
                    continue

                # Skip problematic patterns
                if any(example.match(pattern) for pattern in self.skip_patterns):
                    continue

                focused_examples.append(example)


            # Categorize by agent type
            agent_map = self._categorize_by_agent_type(focused_examples)

            return agent_map

        except Exception as e:
            logger.exception(f"Error discovering examples: {e}")
            return {}

    def _categorize_by_agent_type(self, examples: list[Path]) -> dict[str, list[Path]]:
        """Categorize examples by agent type."""
        categories = {
            "SimpleAgent": [],
            "ReactAgent": [],
            "RAGAgent": [],
            "MultiAgent": [],
            "GameAgent": [],
            "CoreExamples": [],
            "Other": [],
        }

        for example in examples:
            example_str = str(example).lower()
            content = self._safely_read_file(example)

            # Categorize based on path and content
            if "simple" in example_str or "simple" in content:
                categories["SimpleAgent"].append(example)
            elif "react" in example_str or "react" in content:
                categories["ReactAgent"].append(example)
            elif "rag" in example_str or "rag" in content:
                categories["RAGAgent"].append(example)
            elif "multi" in example_str or "multiagent" in content:
                categories["MultiAgent"].append(example)
            elif "haive-games" in example_str:
                categories["GameAgent"].append(example)
            elif "haive-core" in example_str:
                categories["CoreExamples"].append(example)
            else:
                categories["Other"].append(example)

        # Remove empty categories
        return {k: v for k, v in categories.items() if v}

    def _safely_read_file(self, file_path: Path) -> str:
        """Safely read file content for analysis."""
        try:
            with open(file_path, encoding="utf-8") as f:
                return f.read().lower()[:1000]  # First 1KB only
        except Exception:
            return ""

    def list_focused_examples(self, agent_map: dict[str, list[Path]]) -> None:
        """List all focused examples by category."""

        total = 0
        for category, examples in sorted(agent_map.items()):
            if examples:
                count = len(examples)
                total += count
                for i, example in enumerate(examples[:5], 1):  # Show first 5
                    rel_path = example.relative_to(self.runner.project_root)

                if len(examples) > 5:
                    pass


    async def run_category_examples(
        self,
        category: str,
        agent_map: dict[str, list[Path]],
        visualize: bool = True,
        max_examples: int = 5,
    ) -> None:
        """Run examples for a specific category."""
        if category not in agent_map:
            return

        examples = agent_map[category][:max_examples]  # Limit for safety

        # Configure execution with timeouts
        config = ExecutionConfig(
            timeout_seconds=180,  # 3 minutes max per example
            enable_visualization=visualize,
            stream_output=True,
            save_full_output=True,
            max_output_size=100000,  # 100KB limit
        )

        # Ask for confirmation
        response = input(f"\n🤔 Run {len(examples)} {category} examples? (y/N): ")
        if response.lower() not in ["y", "yes"]:
            return


        # Run examples one by one for better error handling
        results = []
        for i, example in enumerate(examples, 1):

            try:
                result = await self.runner.run_example(example, config)
                results.append(result)

                status = "✅" if result.success else "❌"
                time_str = f"{result.execution_time:.1f}s"

                if result.visualization_path:
                    pass}")

                if not result.success:
                    pass")

            except Exception as e:
                logger.exception(f"Exception running {example}: {e}")

        # Summary
        successful = sum(1 for r in results if r.success)
        failed = len(results) - successful

        if results:
            pass%")

        # Show visualizations
        viz_files = [r.visualization_path for r in results if r.visualization_path]
        if viz_files:
            for viz_file in viz_files:
                pass")


async def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="Run focused examples (agents + games)"
    )
    parser.add_argument(
        "--list", action="store_true", help="List all available examples"
    )
    parser.add_argument("--category", help="Run examples for specific category")
    parser.add_argument(
        "--type", help="Agent type (simple, react, rag, multi, game, core)"
    )
    parser.add_argument(
        "--visualize", action="store_true", default=True, help="Generate visualizations"
    )
    parser.add_argument("--no-viz", action="store_true", help="Skip visualizations")
    parser.add_argument(
        "--max", type=int, default=5, help="Max examples per category (default: 5)"
    )

    args = parser.parse_args()

    if args.no_viz:
        args.visualize = False

    runner = FocusedExampleRunner()


    # Discover focused examples
    try:
        agent_map = await runner.discover_focused_examples()

        if not agent_map:
            return

    except Exception as e:
        logger.exception(f"Discovery error: {e}")
        return

    if args.list:
        runner.list_focused_examples(agent_map)
        return

    if args.category:
        await runner.run_category_examples(
            args.category, agent_map, args.visualize, args.max
        )
        return

    if args.type:
        # Map type shortcuts to categories
        type_mapping = {
            "simple": "SimpleAgent",
            "react": "ReactAgent",
            "rag": "RAGAgent",
            "multi": "MultiAgent",
            "game": "GameAgent",
            "core": "CoreExamples",
        }

        category = type_mapping.get(args.type.lower(), args.type)
        await runner.run_category_examples(
            category, agent_map, args.visualize, args.max
        )
        return

    # Interactive mode
    runner.list_focused_examples(agent_map)

    while True:
        category = input("Enter category to run (or 'q' to quit): ").strip()

        if category.lower() == "q":
            break
        if category in agent_map:
            await runner.run_category_examples(
                category, agent_map, args.visualize, args.max
            )
        else:
            pass")


if __name__ == "__main__":
    asyncio.run(main())
