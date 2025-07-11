"""Custom Sphinx extension to provide better sidebar titles for Haive documentation."""

from pathlib import Path
import re
from typing import Any, Dict, Optional

from docutils import nodes
from sphinx.addnodes import toctree as toctree_node
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment


# Module name to human-readable title mapping
MODULE_TITLES = {
    # Core modules
    "haive.core": "Core Framework",
    "haive.core.engine": "Engine & LLM",
    "haive.core.graph": "Graph System",
    "haive.core.schema": "State Schemas",
    "haive.core.persistence": "Persistence",
    "haive.core.registry": "Registry System",
    "haive.core.utils": "Utilities",
    "haive.core.config": "Configuration",
    "haive.core.common": "Common Types",
    # Agent modules
    "haive.agents": "Agent System",
    "haive.agents.base": "Base Agent",
    "haive.agents.simple": "Simple Agent",
    "haive.agents.react": "ReAct Agent",
    "haive.agents.rag": "RAG Agents",
    "haive.agents.multi": "Multi-Agent",
    "haive.agents.planning": "Planning Agents",
    "haive.agents.conversation": "Conversation Agent",
    "haive.agents.document_modifiers": "Document Modifiers",
    "haive.agents.reasoning_and_critique": "Reasoning & Critique",
    "haive.agents.task_analysis": "Task Analysis",
    # Tool modules
    "haive.tools": "Tool System",
    "haive.tools.base": "Base Tools",
    "haive.tools.core": "Core Tools",
    "haive.tools.search": "Search Tools",
    "haive.tools.code": "Code Tools",
    "haive.tools.data": "Data Tools",
    "haive.tools.math": "Math Tools",
    "haive.tools.api": "API Tools",
    "haive.tools.utility": "Utility Tools",
    "haive.tools.individual": "Individual Tools",
    "haive.tools.toolkits": "Tool Toolkits",
    # Game modules
    "haive.games": "Game Environments",
    "haive.games.base": "Game Base",
    "haive.games.classic": "Classic Games",
    "haive.games.board_games": "Board Games",
    "haive.games.card_games": "Card Games",
    "haive.games.framework": "Game Framework",
    "haive.games.components": "Game Components",
    "haive.games.other": "Other Games",
    # Other packages
    "haive.dataflow": "Data Flow",
    "haive.prebuilt": "Prebuilt Solutions",
    "haive.mcp": "MCP Integration",
}


def get_readable_title(module_name: str) -> str:
    """Convert a module name to a human-readable title."""
    # Check if we have a custom title
    if module_name in MODULE_TITLES:
        return MODULE_TITLES[module_name]

    # Otherwise, generate a title from the module name
    parts = module_name.split(".")
    if len(parts) > 0:
        # Take the last part and make it human-readable
        last_part = parts[-1]
        # Convert snake_case to Title Case
        title = last_part.replace("_", " ").title()
        # Handle special cases
        title = title.replace("Api", "API")
        title = title.replace("Rag", "RAG")
        title = title.replace("Llm", "LLM")
        title = title.replace("Mcp", "MCP")
        return title

    return module_name


def process_toctree_entries(app: Sphinx, doctree: nodes.document, docname: str) -> None:
    """Process toctree entries to add better titles."""
    for toctree in doctree.traverse(toctree_node):
        entries = toctree.get("entries", [])
        new_entries = []

        for entry in entries:
            if isinstance(entry, tuple) and len(entry) == 2:
                title, ref = entry
                # If the title looks like a module path, replace it
                if title and "." in title and title.startswith("haive"):
                    new_title = get_readable_title(title)
                    new_entries.append((new_title, ref))
                else:
                    new_entries.append(entry)
            else:
                new_entries.append(entry)

        if new_entries:
            toctree["entries"] = new_entries


def add_module_title_to_page(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: dict[str, Any],
    doctree: nodes.document,
) -> None:
    """Add a human-readable title to module pages."""
    # Check if this is a module page
    if pagename.startswith(("api/generated/", "generated/")):
        # Extract module name from page name
        module_name = pagename.replace("api/generated/", "").replace("generated/", "")
        module_name = module_name.replace("/", ".")

        # Get readable title
        readable_title = get_readable_title(module_name)

        # Add to context for use in templates
        context["module_readable_title"] = readable_title
        context["module_full_name"] = module_name

        # Update the page title if it looks like a module path
        if "title" in context and context["title"] == module_name:
            context["title"] = readable_title


def source_read_handler(app: Sphinx, docname: str, source: list) -> None:
    """Modify source content to add better titles."""
    if docname.startswith(("api/generated/", "generated/")):
        content = source[0]

        # Look for module heading pattern
        lines = content.split("\n")
        for i, line in enumerate(lines):
            # Check if this line is a module name followed by underline
            if line.startswith("haive.") and i + 1 < len(lines):
                next_line = lines[i + 1]
                # Check if next line is an underline
                if next_line and all(c in '=-~^"' for c in next_line.strip()):
                    # Get readable title
                    readable_title = get_readable_title(line.strip())
                    # Replace the title
                    lines[i] = readable_title
                    # Adjust underline length
                    lines[i + 1] = next_line[0] * len(readable_title)

        source[0] = "\n".join(lines)


def setup(app: Sphinx) -> dict[str, Any]:
    """Setup the Haive sidebar titles extension."""
    app.connect("doctree-resolved", process_toctree_entries)
    app.connect("html-page-context", add_module_title_to_page)
    app.connect("source-read", source_read_handler)

    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
