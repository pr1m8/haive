#!/usr/bin/env python3
"""Real Examples Integration Script.

This script finds and integrates real example outputs from the codebase
into the documentation system, replacing mock data with actual agent outputs.
"""

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class ExampleOutput:
    """Container for a real example output."""

    name: str
    type: str  # 'conversation', 'game', 'json_trace', 'markdown'
    path: Path
    content: str
    metadata: dict[str, Any]
    agent_type: str | None = None
    example_category: str | None = None


class RealExamplesIntegrator:
    """Integrates real examples from the codebase into documentation."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.examples: list[ExampleOutput] = []

    def discover_examples(self) -> list[ExampleOutput]:
        """Discover all real examples in the codebase."""

        # Find conversation outputs
        self._find_conversation_outputs()

        # Find game outputs and readmes
        self._find_game_outputs()

        # Find cached agent outputs
        self._find_cached_outputs()

        # Find capture files
        self._find_capture_files()

        return self.examples

    def _find_conversation_outputs(self):
        """Find conversation agent outputs."""
        conversation_dirs = [
            "packages/haive-agents/src/haive/agents/conversation/*/outputs",
            "packages/haive-agents/src/haive/agents/conversation/*/README.md",
        ]

        for pattern in conversation_dirs:
            for path in self.project_root.glob(pattern):
                if path.is_file() and path.suffix == ".md":
                    content = path.read_text(encoding="utf-8")

                    # Extract agent type from path
                    agent_type = (
                        path.parts[-3] if "conversation" in path.parts else None
                    )

                    example = ExampleOutput(
                        name=f"{agent_type}_{path.stem}",
                        type="conversation",
                        path=path,
                        content=content,
                        metadata={
                            "agent_type": agent_type,
                            "word_count": len(content.split()),
                            "sections": self._extract_sections(content),
                        },
                        agent_type=agent_type,
                        example_category="conversation",
                    )
                    self.examples.append(example)

    def _find_game_outputs(self):
        """Find game outputs and documentation."""
        game_patterns = [
            "packages/haive-games/src/haive/games/*/README.md",
            "packages/haive-games/src/haive/games/*/outputs/*.md",
            "packages/haive-games/examples/*.py",
        ]

        for pattern in game_patterns:
            for path in self.project_root.glob(pattern):
                if path.is_file():
                    content = path.read_text(encoding="utf-8")

                    # Extract game type from path
                    game_type = None
                    if "games" in path.parts:
                        games_idx = path.parts.index("games")
                        if games_idx + 1 < len(path.parts):
                            game_type = path.parts[games_idx + 1]

                    example = ExampleOutput(
                        name=f"{game_type}_{path.stem}" if game_type else path.stem,
                        type="game",
                        path=path,
                        content=content,
                        metadata={
                            "game_type": game_type,
                            "file_type": path.suffix,
                            "is_example": "examples" in str(path),
                        },
                        agent_type=game_type,
                        example_category="games",
                    )
                    self.examples.append(example)

    def _find_cached_outputs(self):
        """Find cached agent outputs."""
        cache_patterns = [
            "docs/source/agent_cache_*.json",
            "docs/scripts/cache_generation/agent_cache_*.json",
        ]

        for pattern in cache_patterns:
            for path in self.project_root.glob(pattern):
                if path.is_file():
                    try:
                        with open(path) as f:
                            cache_data = json.load(f)

                        agent_type = cache_data.get("agent_type", "unknown")

                        example = ExampleOutput(
                            name=f"cached_{agent_type}",
                            type="json_trace",
                            path=path,
                            content=json.dumps(cache_data, indent=2),
                            metadata={
                                "agent_type": agent_type,
                                "execution_count": len(
                                    cache_data.get("executions", [])
                                ),
                                "generated_at": cache_data.get("generated_at"),
                                "has_traces": bool(cache_data.get("executions")),
                            },
                            agent_type=agent_type,
                            example_category="execution_traces",
                        )
                        self.examples.append(example)
                    except (json.JSONDecodeError, Exception) as e:
                        pass

    def _find_capture_files(self):
        """Find capture files with agent execution data."""
        capture_dir = self.project_root / "docs" / "captures"
        if capture_dir.exists():
            for path in capture_dir.glob("*.json"):
                try:
                    with open(path) as f:
                        capture_data = json.load(f)

                    agent_name = capture_data.get("agent_name", "unknown")

                    example = ExampleOutput(
                        name=f"capture_{agent_name}_{path.stem[:8]}",
                        type="json_trace",
                        path=path,
                        content=json.dumps(capture_data, indent=2),
                        metadata={
                            "agent_name": agent_name,
                            "agent_type": capture_data.get("agent_type"),
                            "start_time": capture_data.get("start_time"),
                            "duration": self._calculate_duration(capture_data),
                            "steps": len(capture_data.get("steps", [])),
                        },
                        agent_type=capture_data.get("agent_type"),
                        example_category="execution_traces",
                    )
                    self.examples.append(example)
                except (json.JSONDecodeError, Exception) as e:
                    pass

    def _extract_sections(self, content: str) -> list[str]:
        """Extract section headers from markdown content."""
        sections = re.findall(r"^#+\s+(.+)$", content, re.MULTILINE)
        return sections

    def _calculate_duration(self, capture_data: dict) -> float | None:
        """Calculate duration from capture data."""
        try:
            from datetime import datetime

            start = capture_data.get("start_time")
            end = capture_data.get("end_time")
            if start and end:
                start_dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
                end_dt = datetime.fromisoformat(end.replace("Z", "+00:00"))
                return (end_dt - start_dt).total_seconds()
        except Exception:
            pass
        return None

    def generate_examples_index(self, output_path: Path):
        """Generate an index of all discovered examples."""

        # Group examples by category
        by_category = {}
        for example in self.examples:
            category = example.example_category or "other"
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(example)

        # Generate markdown index
        content = """# Real Examples Index

This index contains all the real, working examples discovered in the Haive codebase.
These are actual outputs from agents, games, and conversations - not mock data.

"""

        for category, examples in by_category.items():
            content += f"## {category.title()}\n\n"

            for example in examples:
                content += f"### {example.name}\n\n"
                content += f"- **Type**: {example.type}\n"
                content += (
                    f"- **Path**: `{example.path.relative_to(self.project_root)}`\n"
                )

                if example.agent_type:
                    content += f"- **Agent Type**: {example.agent_type}\n"

                # Add metadata info
                metadata = example.metadata
                if metadata.get("word_count"):
                    content += f"- **Word Count**: {metadata['word_count']}\n"
                if metadata.get("execution_count"):
                    content += f"- **Executions**: {metadata['execution_count']}\n"
                if metadata.get("steps"):
                    content += f"- **Steps**: {metadata['steps']}\n"
                if metadata.get("sections"):
                    content += f"- **Sections**: {', '.join(metadata['sections'][:3])}{'...' if len(metadata['sections']) > 3 else ''}\n"

                content += "\n"

        # Write index
        with open(output_path, "w") as f:
            f.write(content)


    def create_documentation_templates(self, output_dir: Path):
        """Create documentation templates using real examples."""

        output_dir.mkdir(parents=True, exist_ok=True)

        # Group examples by agent type
        by_agent_type = {}
        for example in self.examples:
            if example.agent_type:
                if example.agent_type not in by_agent_type:
                    by_agent_type[example.agent_type] = []
                by_agent_type[example.agent_type].append(example)

        # Create templates for each agent type
        for agent_type, examples in by_agent_type.items():
            self._create_agent_template(agent_type, examples, output_dir)

    def _create_agent_template(
        self, agent_type: str, examples: list[ExampleOutput], output_dir: Path
    ):
        """Create a documentation template for a specific agent type."""
        template_path = output_dir / f"{agent_type}_examples.md"

        content = f"""# {agent_type.title()} Agent Examples

Real examples and outputs from the {agent_type} agent.

"""

        for example in examples:
            content += f"## {example.name}\n\n"
            content += (
                f"**Source**: `{example.path.relative_to(self.project_root)}`\n\n"
            )

            # Add example content (truncated if too long)
            example_content = example.content
            if len(example_content) > 2000:
                example_content = example_content[:2000] + "\n\n... (truncated)\n"

            if example.type == "json_trace":
                content += "```json\n"
                content += example_content
                content += "\n```\n\n"
            else:
                content += example_content + "\n\n"

            content += "---\n\n"

        with open(template_path, "w") as f:
            f.write(content)


    def integrate_with_sphinx(self, docs_dir: Path):
        """Integrate examples with Sphinx documentation."""

        # Create examples directory in docs
        examples_dir = docs_dir / "source" / "real_examples"
        examples_dir.mkdir(parents=True, exist_ok=True)

        # Generate examples index
        self.generate_examples_index(examples_dir / "index.md")

        # Create templates
        self.create_documentation_templates(examples_dir)

        # Create rst index for Sphinx
        rst_content = """Real Examples
=============

.. toctree::
   :maxdepth: 2
   :caption: Real Agent Examples

"""

        # Add agent type sections
        agent_types = set(ex.agent_type for ex in self.examples if ex.agent_type)
        for agent_type in sorted(agent_types):
            rst_content += f"   real_examples/{agent_type}_examples\n"

        with open(docs_dir / "source" / "real_examples.rst", "w") as f:
            f.write(rst_content)



def main():
    """Main function to run the real examples integration."""
    project_root = Path(__file__).parent.parent.parent
    docs_dir = project_root / "docs"

    integrator = RealExamplesIntegrator(project_root)

    # Discover examples
    examples = integrator.discover_examples()

    if not examples:
        return

    # Generate summary

    by_type = {}
    for ex in examples:
        by_type[ex.type] = by_type.get(ex.type, 0) + 1

    for ex_type, count in by_type.items():
        pass

    # Integrate with documentation
    integrator.integrate_with_sphinx(docs_dir)



if __name__ == "__main__":
    main()
