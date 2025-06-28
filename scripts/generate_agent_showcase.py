#!/usr/bin/env python3
"""Agent Showcase Generator for Haive Framework

This script automatically discovers and categorizes all agents across the haive packages
(haive-agents, haive-prebuilt, haive-games) and generates comprehensive documentation
showcasing their capabilities, usage patterns, and categorization.

Features:
- Safe module discovery that avoids problematic imports
- Intelligent categorization based on directory structure and class analysis
- Rich documentation generation with examples and usage patterns
- Comprehensive error handling to prevent build failures
"""

import ast
import json
import logging
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class AgentInfo:
    """Information about a discovered agent."""

    name: str
    module_path: str
    file_path: str
    category: str
    package: str
    description: str = ""
    base_classes: list[str] = field(default_factory=list)
    features: list[str] = field(default_factory=list)
    docstring: str = ""
    is_abstract: bool = False
    has_tools: bool = False
    has_memory: bool = False
    complexity: str = "medium"  # simple, medium, complex


class AgentDiscovery:
    """Discovers and analyzes agents across haive packages."""

    # Known problematic modules to skip
    SKIP_MODULES = {
        "haive.games.chess",  # Syntax errors
        "haive.agents.conversation.social_media",  # Import issues
        "haive.tools.toolkits.gradio_toolkit",  # External dependencies
        "haive.dataflow.db.supabase",  # External dependencies
        "haive.core.persistence.supabase_config",  # External dependencies
    }

    # File patterns to skip
    SKIP_PATTERNS = {
        "__pycache__",
        ".pytest_cache",
        "test_",
        "_test",
        "tests",
        "testing",
        "example",
        "examples",
        "demo",
        "demos",
        "ui.py",
        "temp_",
        "placeholder",
    }

    def __init__(self, workspace_root: Path):
        """Initialize the agent discovery system."""
        self.workspace_root = workspace_root
        self.packages_dir = workspace_root / "packages"
        self.agents: list[AgentInfo] = []
        self.categories: dict[str, list[AgentInfo]] = defaultdict(list)
        self.errors: list[str] = []

    def should_skip_file(self, file_path: Path) -> bool:
        """Check if a file should be skipped during discovery."""
        file_str = str(file_path)

        # Skip based on patterns
        for pattern in self.SKIP_PATTERNS:
            if pattern in file_str.lower():
                return True

        # Skip non-Python files
        if not file_path.suffix == ".py":
            return True

        # Skip __init__.py files (we'll handle them separately)
        if file_path.name == "__init__.py":
            return True

        return False

    def extract_agent_info_from_ast(self, file_path: Path) -> list[AgentInfo]:
        """Extract agent information from Python AST without importing."""
        agents = []

        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Parse AST
            tree = ast.parse(content)

            # Extract module docstring
            module_docstring = ast.get_docstring(tree) or ""

            # Find agent classes
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    agent_info = self.analyze_class_node(
                        node, file_path, module_docstring
                    )
                    if agent_info:
                        agents.append(agent_info)

        except SyntaxError as e:
            self.errors.append(f"Syntax error in {file_path}: {e}")
            logger.warning(f"Skipping {file_path} due to syntax error: {e}")
        except Exception as e:
            self.errors.append(f"Error parsing {file_path}: {e}")
            logger.warning(f"Error parsing {file_path}: {e}")

        return agents

    def analyze_class_node(
        self, node: ast.ClassDef, file_path: Path, module_docstring: str
    ) -> AgentInfo | None:
        """Analyze a class AST node to determine if it's an agent."""
        class_name = node.name

        # Skip classes that don't look like agents
        if not self.looks_like_agent(class_name, node):
            return None

        # Extract class information
        base_classes = [self.get_base_class_name(base) for base in node.bases]
        docstring = ast.get_docstring(node) or ""
        is_abstract = any(
            isinstance(item, ast.FunctionDef)
            and any(
                isinstance(dec, ast.Name) and dec.id == "abstractmethod"
                for dec in item.decorator_list
            )
            for item in node.body
        )

        # Determine module path
        module_path = self.file_path_to_module_path(file_path)

        # Categorize the agent
        category = self.categorize_agent(file_path, class_name, docstring)
        package = self.get_package_name(file_path)

        # Extract features
        features = self.extract_features(node, docstring)

        # Determine complexity
        complexity = self.determine_complexity(node, docstring, features)

        return AgentInfo(
            name=class_name,
            module_path=module_path,
            file_path=str(file_path),
            category=category,
            package=package,
            description=self.extract_description(docstring, module_docstring),
            base_classes=base_classes,
            features=features,
            docstring=docstring,
            is_abstract=is_abstract,
            has_tools="tools" in features,
            has_memory="memory" in features,
            complexity=complexity,
        )

    def looks_like_agent(self, class_name: str, node: ast.ClassDef) -> bool:
        """Determine if a class looks like an agent."""
        # Check name patterns
        if "agent" in class_name.lower():
            return True

        # Check base classes
        for base in node.bases:
            base_name = self.get_base_class_name(base)
            if base_name and ("agent" in base_name.lower() or "Agent" in base_name):
                return True

        return False

    def get_base_class_name(self, base_node: ast.expr) -> str:
        """Extract base class name from AST node."""
        if isinstance(base_node, ast.Name):
            return base_node.id
        if isinstance(base_node, ast.Attribute):
            return base_node.attr
        if isinstance(base_node, ast.Subscript):
            return self.get_base_class_name(base_node.value)
        return ""

    def file_path_to_module_path(self, file_path: Path) -> str:
        """Convert file path to Python module path."""
        # Find the src directory
        parts = file_path.parts
        try:
            src_index = parts.index("src")
            module_parts = parts[src_index + 1 : -1]  # Exclude 'src' and file extension
            module_parts = list(module_parts) + [
                file_path.stem
            ]  # Add filename without extension
            return ".".join(module_parts)
        except ValueError:
            # Fallback: use relative path from packages
            try:
                packages_index = parts.index("packages")
                module_parts = parts[packages_index + 1 :]
                if "src" in module_parts:
                    src_index = module_parts.index("src")
                    module_parts = module_parts[src_index + 1 :]
                # Remove file extension
                module_parts = list(module_parts[:-1]) + [file_path.stem]
                return ".".join(module_parts)
            except ValueError:
                return str(file_path.stem)

    def categorize_agent(self, file_path: Path, class_name: str, docstring: str) -> str:
        """Categorize an agent based on its location and characteristics."""
        path_str = str(file_path).lower()
        class_lower = class_name.lower()
        doc_lower = docstring.lower()

        # Package-based categorization
        if "haive-games" in path_str:
            if any(game in path_str for game in ["chess", "poker", "checkers", "go"]):
                return "Classic Games"
            if any(game in path_str for game in ["among_us", "mafia", "risk"]):
                return "Strategy Games"
            if any(game in path_str for game in ["cards", "blackjack"]):
                return "Card Games"
            return "Games"

        if "haive-prebuilt" in path_str:
            if any(term in path_str for term in ["contract", "legal"]):
                return "Legal & Business"
            if any(term in path_str for term in ["scientific", "research", "paper"]):
                return "Academic & Research"
            return "Prebuilt Solutions"

        if "haive-agents" in path_str:
            # Directory-based categorization
            if "conversation" in path_str:
                return "Conversation & Multi-Agent"
            if "rag" in path_str:
                return "RAG & Retrieval"
            if "reasoning" in path_str or "critique" in path_str:
                return "Reasoning & Critique"
            if "react" in path_str:
                return "ReAct & Tool Use"
            if "simple" in path_str:
                return "Foundation Agents"
            if "document" in path_str:
                return "Document Processing"
            if "planning" in path_str:
                return "Planning & Strategy"
            if "memory" in path_str:
                return "Memory & Persistence"
            if "research" in path_str:
                return "Research & Information"
            if "multi" in path_str:
                return "Multi-Agent Systems"
            return "Specialized Agents"

        return "Other"

    def get_package_name(self, file_path: Path) -> str:
        """Extract package name from file path."""
        path_str = str(file_path)
        if "haive-agents" in path_str:
            return "haive-agents"
        if "haive-prebuilt" in path_str:
            return "haive-prebuilt"
        if "haive-games" in path_str:
            return "haive-games"
        return "unknown"

    def extract_features(self, node: ast.ClassDef, docstring: str) -> list[str]:
        """Extract features from class definition and docstring."""
        features = []
        doc_lower = docstring.lower()

        # Check for common features in docstring
        feature_keywords = {
            "tools": ["tool", "function", "external"],
            "memory": ["memory", "persist", "checkpoint", "history"],
            "structured_output": ["structured", "schema", "output", "pydantic"],
            "conversation": ["conversation", "chat", "dialogue", "multi-agent"],
            "reasoning": ["reasoning", "thought", "critique", "reflection"],
            "retrieval": ["rag", "retrieval", "vector", "search", "knowledge"],
            "planning": ["plan", "strategy", "goal", "decompose"],
        }

        for feature, keywords in feature_keywords.items():
            if any(keyword in doc_lower for keyword in keywords):
                features.append(feature)

        # Check class fields for features
        for item in node.body:
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                field_name = item.target.id.lower()
                if "tool" in field_name:
                    features.append("tools")
                elif "memory" in field_name:
                    features.append("memory")

        return list(set(features))  # Remove duplicates

    def determine_complexity(
        self, node: ast.ClassDef, docstring: str, features: list[str]
    ) -> str:
        """Determine the complexity level of an agent."""
        # Count methods
        method_count = sum(1 for item in node.body if isinstance(item, ast.FunctionDef))

        # Complexity indicators
        complex_features = ["reasoning", "planning", "conversation", "multi-agent"]
        has_complex_features = any(feature in features for feature in complex_features)

        doc_lower = docstring.lower()
        complex_keywords = [
            "multi",
            "complex",
            "advanced",
            "sophisticated",
            "framework",
        ]
        has_complex_keywords = any(keyword in doc_lower for keyword in complex_keywords)

        if method_count > 10 or has_complex_features or has_complex_keywords:
            return "complex"
        if method_count > 5 or len(features) > 3:
            return "medium"
        return "simple"

    def extract_description(self, docstring: str, module_docstring: str) -> str:
        """Extract a concise description from docstrings."""
        # Try class docstring first
        if docstring:
            lines = docstring.strip().split("\n")
            first_line = lines[0].strip()
            if first_line and not first_line.startswith(
                ("Args:", "Parameters:", "Returns:")
            ):
                return first_line

        # Fallback to module docstring
        if module_docstring:
            lines = module_docstring.strip().split("\n")
            for line in lines:
                line = line.strip()
                if line and not line.startswith(('"""', "'''", '#"')):
                    return line

        return "No description available"

    def discover_agents(self) -> None:
        """Main discovery method that scans all packages."""
        logger.info("Starting agent discovery...")

        packages = ["haive-agents", "haive-prebuilt", "haive-games"]

        for package_name in packages:
            package_path = self.packages_dir / package_name
            if not package_path.exists():
                logger.warning(f"Package {package_name} not found at {package_path}")
                continue

            logger.info(f"Scanning package: {package_name}")
            self.scan_package(package_path)

        # Organize by categories
        for agent in self.agents:
            self.categories[agent.category].append(agent)

        logger.info(
            f"Discovery complete! Found {len(self.agents)} agents across {len(self.categories)} categories"
        )

        if self.errors:
            logger.warning(f"Encountered {len(self.errors)} errors during discovery")

    def scan_package(self, package_path: Path) -> None:
        """Scan a package directory for agents."""
        src_path = package_path / "src"
        if src_path.exists():
            self.scan_directory(src_path)
        else:
            # Fallback to scanning the package directory directly
            self.scan_directory(package_path)

    def scan_directory(self, directory: Path) -> None:
        """Recursively scan a directory for Python agent files."""
        for file_path in directory.rglob("*.py"):
            if self.should_skip_file(file_path):
                continue

            # Check if module should be skipped
            module_path = self.file_path_to_module_path(file_path)
            if any(skip_module in module_path for skip_module in self.SKIP_MODULES):
                logger.debug(f"Skipping module {module_path} (in skip list)")
                continue

            agents = self.extract_agent_info_from_ast(file_path)
            self.agents.extend(agents)

    def generate_showcase_data(self) -> dict[str, Any]:
        """Generate structured data for the agent showcase."""
        showcase_data = {
            "metadata": {
                "total_agents": len(self.agents),
                "total_categories": len(self.categories),
                "packages": list(set(agent.package for agent in self.agents)),
                "generation_timestamp": (
                    str(pd.Timestamp.now()) if "pd" in globals() else "unknown"
                ),
                "errors_count": len(self.errors),
            },
            "categories": {},
            "agents": [],
            "stats": self.generate_stats(),
        }

        # Organize by categories
        for category, agents in self.categories.items():
            showcase_data["categories"][category] = {
                "count": len(agents),
                "agents": [agent.name for agent in agents],
                "packages": list(set(agent.package for agent in agents)),
                "complexity_breakdown": {
                    "simple": len([a for a in agents if a.complexity == "simple"]),
                    "medium": len([a for a in agents if a.complexity == "medium"]),
                    "complex": len([a for a in agents if a.complexity == "complex"]),
                },
            }

        # Add detailed agent information
        for agent in self.agents:
            showcase_data["agents"].append(
                {
                    "name": agent.name,
                    "module_path": agent.module_path,
                    "category": agent.category,
                    "package": agent.package,
                    "description": agent.description,
                    "features": agent.features,
                    "complexity": agent.complexity,
                    "has_tools": agent.has_tools,
                    "has_memory": agent.has_memory,
                    "is_abstract": agent.is_abstract,
                    "base_classes": agent.base_classes,
                }
            )

        return showcase_data

    def generate_stats(self) -> dict[str, Any]:
        """Generate statistics about the discovered agents."""
        stats = {
            "by_package": defaultdict(int),
            "by_category": defaultdict(int),
            "by_complexity": defaultdict(int),
            "features": defaultdict(int),
        }

        for agent in self.agents:
            stats["by_package"][agent.package] += 1
            stats["by_category"][agent.category] += 1
            stats["by_complexity"][agent.complexity] += 1

            for feature in agent.features:
                stats["features"][feature] += 1

        # Convert defaultdicts to regular dicts
        return {
            k: dict(v) if isinstance(v, defaultdict) else v for k, v in stats.items()
        }


def main():
    """Main function to run agent discovery and generate showcase."""
    # Find workspace root
    current_dir = Path(__file__).resolve().parent
    workspace_root = current_dir.parent  # Assuming script is in scripts/ directory

    logger.info(f"Workspace root: {workspace_root}")

    # Initialize discovery
    discovery = AgentDiscovery(workspace_root)

    # Run discovery
    discovery.discover_agents()

    # Generate showcase data
    showcase_data = discovery.generate_showcase_data()

    # Save to JSON file
    output_file = workspace_root / "docs" / "agent_showcase_data.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(showcase_data, f, indent=2, ensure_ascii=False)

    logger.info(f"Agent showcase data saved to: {output_file}")

    # Print summary
    print("\n🤖 Agent Discovery Summary:")
    print(f"📊 Total Agents: {showcase_data['metadata']['total_agents']}")
    print(f"📁 Categories: {showcase_data['metadata']['total_categories']}")
    print(f"📦 Packages: {', '.join(showcase_data['metadata']['packages'])}")

    print("\n📈 By Package:")
    for package, count in showcase_data["stats"]["by_package"].items():
        print(f"  {package}: {count} agents")

    print("\n🏷️ By Category:")
    for category, count in showcase_data["stats"]["by_category"].items():
        print(f"  {category}: {count} agents")

    if discovery.errors:
        print(f"\n⚠️ Errors encountered: {len(discovery.errors)}")
        for error in discovery.errors[:5]:  # Show first 5 errors
            print(f"  {error}")
        if len(discovery.errors) > 5:
            print(f"  ... and {len(discovery.errors) - 5} more errors")


if __name__ == "__main__":
    main()
