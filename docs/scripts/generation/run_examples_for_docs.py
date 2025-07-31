#!/usr/bin/env python3
"""Documentation Example Runner - Generate examples for docs with visualizations.
==========================================================================

This script is specifically designed to run examples for documentation generation:
1. Discovers all examples across packages
2. Runs examples with docs-friendly output
3. Generates visualizations in docs/source/auto_examples/
4. Creates gallery entries and RST files
5. Integrates with Sphinx Gallery

Usage:
    cd docs/
    python run_examples_for_docs.py
"""

import asyncio
import json
import logging
import os
import sys
from pathlib import Path

# Add parent directory to path so we can import the runner
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.doc_utils.example_runner import (ExecutionConfig,
                                              UniversalExampleRunner)

# Configure logging for docs
logging.basicConfig(
    level=logging.INFO,
    filename="docs/logs/example_generation.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class DocsExampleRunner:
    """Documentation-specific example runner."""

    def __init__(self):
        self.runner = UniversalExampleRunner()
        self.docs_root = Path(__file__).parent
        self.source_dir = self.docs_root / "source"
        self.auto_examples_dir = self.source_dir / "auto_examples"
        self.gallery_data = []

        # Ensure directories exist
        self.auto_examples_dir.mkdir(exist_ok=True)
        (self.docs_root / "logs").mkdir(exist_ok=True)

    async def generate_docs_examples(self):
        """Generate all examples for documentation."""

        # Create docs-specific config
        config = ExecutionConfig(
            timeout_seconds=120,  # Shorter timeout for docs
            enable_visualization=True,
            visualization_path=self.auto_examples_dir,
            stream_output=False,  # Don't stream during docs generation
            save_full_output=True,
            max_output_size=50000,  # 50KB limit for docs
        )

        # Discover examples
        example_files = await self.runner.discover_all_examples()

        # Filter to important examples only (not all)
        important_examples = self._filter_important_examples(example_files)


        # Run examples and generate docs

        gallery_entries = []

        for i, example_file in enumerate(important_examples, 1):

            try:
                # Run the example
                result = await self.runner.run_example(example_file, config)

                if result.success:
                    # Create gallery entry
                    entry = await self._create_gallery_entry(example_file, result)
                    if entry:
                        gallery_entries.append(entry)

                    # Generate RST file for Sphinx Gallery
                    await self._generate_rst_file(example_file, result)

                else:
                    pass")

            except Exception as e:
                logger.exception(f"Failed to process {example_file}: {e}")

        # Generate gallery index
        await self._generate_gallery_index(gallery_entries)

        # Update main examples index
        await self._update_examples_index()


        return gallery_entries

    def _filter_important_examples(self, all_examples):
        """Filter to most important examples for documentation."""
        important_patterns = [
            # Agent examples
            "**/simple/**/example*.py",
            "**/react/**/example*.py",
            "**/rag/**/example*.py",
            # Specific showcase examples
            "**/showcase/*.py",
            "**/demo*.py",
            # Prebuilt examples
            "**/prebuilt/**/example.py",
        ]

        # Exclude internal/test examples
        exclude_patterns = [
            "**/test_*.py",
            "**/*test*.py",
            "**/tests/*",
            "**/.venv/*",
            "**/site-packages/*",
        ]

        important = []
        for example in all_examples:
            example_str = str(example)

            # Check exclude patterns first
            if any(example.match(pattern) for pattern in exclude_patterns):
                continue

            # Check important patterns
            if any(example.match(pattern) for pattern in important_patterns):
                important.append(example)
            # Also include any example.py file in src directories
            elif example.name == "example.py" and "/src/" in example_str:
                important.append(example)

        # Limit to reasonable number for docs
        return important[:20]  # Top 20 examples

    async def _create_gallery_entry(self, example_file, result):
        """Create a gallery entry for an example."""
        try:
            # Extract metadata
            relative_path = example_file.relative_to(self.runner.project_root)

            # Try to determine category from path
            category = "General"

            if "simple" in str(relative_path):
                category = "Simple Agents"
            elif "react" in str(relative_path):
                category = "ReAct Agents"
            elif "rag" in str(relative_path):
                category = "RAG Agents"
            elif "games" in str(relative_path):
                category = "Game Agents"
            elif "prebuilt" in str(relative_path):
                category = "Prebuilt Agents"

            entry = {
                "title": self._generate_title_from_path(example_file),
                "file": str(relative_path),
                "category": category,
                "description": self._extract_description(example_file),
                "execution_time": f"{result.execution_time:.1f}s",
                "has_visualization": result.visualization_path is not None,
                "visualization": (
                    str(result.visualization_path.name)
                    if result.visualization_path
                    else None
                ),
            }

            return entry

        except Exception as e:
            logger.exception(f"Failed to create gallery entry for {example_file}: {e}")
            return None

    def _generate_title_from_path(self, example_file):
        """Generate a readable title from file path."""
        # Extract meaningful parts
        parts = example_file.parts

        # Look for agent type in path
        title_parts = []

        for part in parts:
            if part in ["simple", "react", "rag", "planning", "games"]:
                title_parts.append(part.title())
            elif "agent" in part.lower():
                title_parts.append(part.replace("_", " ").title())

        if not title_parts:
            # Fallback to filename
            name = example_file.stem.replace("_", " ").title()
            title_parts = [name]

        title = " ".join(title_parts)
        if not title.endswith("Example"):
            title += " Example"

        return title

    def _extract_description(self, example_file):
        """Extract description from example file."""
        try:
            with open(example_file) as f:
                content = f.read()

            # Look for docstring or comments
            lines = content.split("\n")
            description = ""

            # Try to find module docstring
            in_docstring = False
            for line in lines[:20]:  # Check first 20 lines
                line = line.strip()
                if line.startswith(('"""', "'''")):
                    if in_docstring:
                        break
                    in_docstring = True
                    desc_line = line[3:].strip()
                    if desc_line:
                        description = desc_line
                elif in_docstring and line:
                    if not line.startswith(('"""', "'''")):
                        description = line
                        break
                elif line.startswith("#") and "example" in line.lower():
                    description = line[1:].strip()
                    break

            return description if description else "Agent example demonstration"

        except Exception:
            return "Agent example demonstration"

    async def _generate_rst_file(self, example_file, result):
        """Generate RST file for Sphinx Gallery."""
        try:
            # Create RST filename
            rst_name = example_file.stem + ".rst"
            rst_path = self.auto_examples_dir / rst_name

            # Read original Python file
            with open(example_file) as f:
                python_content = f.read()

            # Create RST content
            title = self._generate_title_from_path(example_file)
            description = self._extract_description(example_file)

            rst_content = f"""
{title}
{"=" * len(title)}

{description}

This example demonstrates the usage and capabilities of the agent.

.. code-block:: python

{self._indent_code(python_content)}

"""

            # Add visualization if available
            if result.visualization_path:
                viz_name = result.visualization_path.name
                rst_content += f"""

Generated Visualization
-----------------------

.. image:: {viz_name}
   :alt: Agent workflow visualization
   :align: center

"""

            # Add execution info
            rst_content += f"""

Execution Information
--------------------

- **Execution Time**: {result.execution_time:.2f} seconds
- **Success**: {"✅ Yes" if result.success else "❌ No"}

"""

            if result.agent_info:
                rst_content += f"""
- **Agent Type**: {result.agent_info.name}
- **Architecture**: {result.agent_info.architecture.value}
- **Has Visualization**: {"✅ Yes" if result.agent_info.has_visualization else "❌ No"}

"""

            # Write RST file
            with open(rst_path, "w") as f:
                f.write(rst_content)


        except Exception as e:
            logger.exception(f"Failed to generate RST for {example_file}: {e}")

    def _indent_code(self, code, indent="   "):
        """Indent code for RST code block."""
        lines = code.split("\n")
        return "\n".join(indent + line for line in lines)

    async def _generate_gallery_index(self, gallery_entries):
        """Generate the main gallery index page."""
        try:
            # Group by category
            by_category = {}
            for entry in gallery_entries:
                category = entry["category"]
                if category not in by_category:
                    by_category[category] = []
                by_category[category].append(entry)

            # Generate RST content
            rst_content = """
Examples Gallery
================

This gallery showcases practical examples of using various Haive agents.

.. toctree::
   :maxdepth: 2
   :caption: Example Categories:

"""

            for category, entries in by_category.items():
                rst_content += f'\n{category}\n{"-" * len(category)}\n\n'

                for entry in entries:
                    rst_file = Path(entry["file"]).stem
                    rst_content += f"   {rst_file}\n"

                rst_content += "\n"

            # Save gallery index
            gallery_path = self.source_dir / "examples" / "gallery.rst"
            gallery_path.parent.mkdir(exist_ok=True)

            with open(gallery_path, "w") as f:
                f.write(rst_content)


        except Exception as e:
            logger.exception(f"Failed to generate gallery index: {e}")

    async def _update_examples_index(self):
        """Update the main examples index to include the gallery."""
        try:
            index_path = self.source_dir / "examples" / "index.rst"

            if not index_path.exists():
                # Create new index
                content = """
Examples
========

Practical examples and demonstrations of Haive agents.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   gallery

"""
            else:
                # Update existing index to include gallery
                with open(index_path) as f:
                    content = f.read()

                if "gallery" not in content:
                    # Add gallery to toctree
                    content = content.replace(
                        "Contents:\n", "Contents:\n\n   gallery\n"
                    )

            with open(index_path, "w") as f:
                f.write(content)


        except Exception as e:
            logger.exception(f"Failed to update examples index: {e}")


async def main():
    """Main function for docs example generation."""
    runner = DocsExampleRunner()

    # Check if we're in the docs directory
    if not Path("source").exists():
        return None

    try:
        gallery_entries = await runner.generate_docs_examples()

        # Save gallery data for other scripts
        with open("gallery_data.json", "w") as f:
            json.dump(gallery_entries, f, indent=2)


    except Exception as e:
        logger.exception(f"Main execution failed: {e}")
        return 1


if __name__ == "__main__":
    asyncio.run(main())
