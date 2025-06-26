#!/usr/bin/env python3
"""Comprehensive Agent Discovery Script for Haive Codebase

This script discovers all agent classes across the haive-agents, haive-prebuilt, 
and haive-games packages, analyzing their:
- Module path and class name
- Description/docstring
- Category/type
- Base class inheritance
- Special features
- File location

The results are organized by package and category for building an automated agent showcase.
"""

import ast
from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path
import sys


@dataclass
class AgentInfo:
    """Information about a discovered agent class."""
    class_name: str
    module_path: str
    file_path: str
    description: str
    base_classes: list[str]
    category: str
    package: str
    docstring: str
    fields: list[str]
    imports: list[str]
    is_abstract: bool
    has_build_graph: bool
    special_features: list[str]


class AgentDiscoverer:
    """Discovers and analyzes agent classes in the Haive codebase."""

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.agents: list[AgentInfo] = []
        self.problematic_modules: set[str] = set()

        # Skip patterns - modules that should be avoided during discovery
        self.skip_patterns = {
            "__pycache__", ".ipynb_checkpoints", "test_", "tests/",
            ".history/", "debug_", "example.py", "mock_", "fix_",
            "simple_demo.py", "standalone_demo.py", "verification.py",
            "verify_imports.py", "minimal_test.py", "test.py",
            ".pyc", "example2.py", "example3.py", "dynamic_graph.log"
        }

    def should_skip_file(self, file_path: str) -> bool:
        """Check if a file should be skipped based on patterns."""
        file_str = str(file_path)
        return any(pattern in file_str for pattern in self.skip_patterns)

    def get_category_from_path(self, file_path: Path, package: str) -> str:
        """Determine agent category from file path."""
        path_parts = file_path.parts

        if package == "haive-agents":
            # Map directory structure to categories
            category_map = {
                "simple": "simple",
                "react": "react",
                "conversation": "conversation",
                "rag": "rag",
                "reasoning_and_critique": "reasoning",
                "planning": "planning",
                "multi": "multi_agent",
                "document_loader": "document_processing",
                "document_modifiers": "document_processing",
                "memory": "memory",
                "long_term_memory": "memory",
                "research": "research",
                "task_analysis": "analysis",
                "sequential": "sequential",
                "self_healing_code": "development"
            }

            for part in path_parts:
                if part in category_map:
                    return category_map[part]

        elif package == "haive-prebuilt":
            return "prebuilt"

        elif package == "haive-games":
            if "single_player" in path_parts:
                return "single_player_games"
            if any(game in path_parts for game in ["chess", "poker", "monopoly", "mafia", "hold_em"]):
                return "multi_player_games"
            if "framework" in path_parts or "base" in path_parts or "core" in path_parts:
                return "game_framework"
            return "games"

        return "other"

    def extract_docstring(self, node: ast.ClassDef) -> str:
        """Extract docstring from class definition."""
        if (node.body and isinstance(node.body[0], ast.Expr) and
            isinstance(node.body[0].value, ast.Constant) and
            isinstance(node.body[0].value.value, str)):
            return node.body[0].value.value.strip()
        return ""

    def extract_base_classes(self, node: ast.ClassDef) -> list[str]:
        """Extract base class names from class definition."""
        bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                # Handle cases like module.ClassName
                bases.append(ast.unparse(base))
            elif isinstance(base, ast.Subscript):
                # Handle generic types like Agent[Config]
                bases.append(ast.unparse(base))
        return bases

    def extract_class_fields(self, node: ast.ClassDef) -> list[str]:
        """Extract field definitions from class."""
        fields = []
        for item in node.body:
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                fields.append(item.target.id)
            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        fields.append(target.id)
        return fields

    def has_method(self, node: ast.ClassDef, method_name: str) -> bool:
        """Check if class has a specific method."""
        for item in node.body:
            if (isinstance(item, ast.FunctionDef) and
                item.name == method_name):
                return True
        return False

    def is_abstract_class(self, node: ast.ClassDef) -> bool:
        """Check if class is abstract (has @abstractmethod decorators)."""
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                for decorator in item.decorator_list:
                    if (isinstance(decorator, ast.Name) and
                        decorator.id == "abstractmethod"):
                        return True
        return False

    def extract_imports(self, tree: ast.AST) -> list[str]:
        """Extract import statements from module."""
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}")
        return imports

    def analyze_special_features(self, node: ast.ClassDef, fields: list[str],
                                base_classes: list[str]) -> list[str]:
        """Analyze special features of the agent class."""
        features = []

        # Check for tool support
        if any("tool" in field.lower() for field in fields):
            features.append("tool_support")

        # Check for memory capabilities
        if any("memory" in field.lower() for field in fields):
            features.append("memory")

        # Check for multi-agent capabilities
        if any("multi" in base.lower() or "conversation" in base.lower()
               for base in base_classes):
            features.append("multi_agent")

        # Check for structured output
        if any("structured" in field.lower() or "output_model" in field.lower()
               for field in fields):
            features.append("structured_output")

        # Check for RAG capabilities
        if any("rag" in base.lower() or "retriever" in base.lower()
               for base in base_classes):
            features.append("rag")

        # Check for react pattern
        if any("react" in base.lower() for base in base_classes):
            features.append("react_pattern")

        return features

    def analyze_file(self, file_path: Path) -> list[AgentInfo]:
        """Analyze a Python file for agent classes."""
        agents = []

        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)
            imports = self.extract_imports(tree)

            # Determine package from path
            if "haive-agents" in str(file_path):
                package = "haive-agents"
            elif "haive-prebuilt" in str(file_path):
                package = "haive-prebuilt"
            elif "haive-games" in str(file_path):
                package = "haive-games"
            else:
                package = "unknown"

            # Find all class definitions
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_name = node.name

                    # Check if this is likely an agent class
                    base_classes = self.extract_base_classes(node)

                    # Skip non-agent classes (configs, states, etc.)
                    if (not class_name.endswith("Agent") and
                        not any("Agent" in base for base in base_classes) and
                        "Agent" not in class_name):
                        continue

                    # Skip test and config classes
                    if any(skip in class_name.lower() for skip in
                          ["test", "config", "state", "factory", "debug"]):
                        continue

                    docstring = self.extract_docstring(node)
                    fields = self.extract_class_fields(node)

                    # Create module path
                    rel_path = file_path.relative_to(self.base_path)
                    module_parts = list(rel_path.parts[:-1])  # Remove filename
                    module_parts.append(rel_path.stem)  # Add filename without extension
                    module_path = ".".join(module_parts)

                    category = self.get_category_from_path(file_path, package)

                    special_features = self.analyze_special_features(
                        node, fields, base_classes)

                    # Extract description from docstring (first line/paragraph)
                    description = ""
                    if docstring:
                        lines = docstring.split("\n")
                        # Get first non-empty line as description
                        for line in lines:
                            line = line.strip()
                            if line and not line.startswith('"""'):
                                description = line
                                break

                    agent_info = AgentInfo(
                        class_name=class_name,
                        module_path=module_path,
                        file_path=str(file_path),
                        description=description,
                        base_classes=base_classes,
                        category=category,
                        package=package,
                        docstring=docstring,
                        fields=fields,
                        imports=imports,
                        is_abstract=self.is_abstract_class(node),
                        has_build_graph=self.has_method(node, "build_graph"),
                        special_features=special_features
                    )

                    agents.append(agent_info)

        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            self.problematic_modules.add(str(file_path))

        return agents

    def discover_agents(self) -> None:
        """Discover all agents in the specified packages."""
        target_packages = [
            "packages/haive-agents/src",
            "packages/haive-prebuilt/src",
            "packages/haive-games/src"
        ]

        for package_path in target_packages:
            full_path = self.base_path / package_path
            if not full_path.exists():
                print(f"Warning: Package path {full_path} does not exist")
                continue

            # Walk through all Python files
            for py_file in full_path.rglob("*.py"):
                if self.should_skip_file(str(py_file)):
                    continue

                discovered_agents = self.analyze_file(py_file)
                self.agents.extend(discovered_agents)

        print(f"Discovered {len(self.agents)} agent classes")
        if self.problematic_modules:
            print(f"Encountered issues with {len(self.problematic_modules)} files")

    def organize_by_category(self) -> dict[str, dict[str, list[AgentInfo]]]:
        """Organize agents by package and category."""
        organized = {}

        for agent in self.agents:
            package = agent.package
            category = agent.category

            if package not in organized:
                organized[package] = {}

            if category not in organized[package]:
                organized[package][category] = []

            organized[package][category].append(agent)

        return organized

    def generate_report(self) -> dict:
        """Generate a comprehensive report of discovered agents."""
        organized = self.organize_by_category()

        report = {
            "discovery_summary": {
                "total_agents": len(self.agents),
                "packages": list(organized.keys()),
                "categories": set(),
                "problematic_modules": list(self.problematic_modules)
            },
            "agents_by_package": {},
            "agent_details": []
        }

        # Add all categories to summary
        for package_data in organized.values():
            report["discovery_summary"]["categories"].update(package_data.keys())

        report["discovery_summary"]["categories"] = list(
            report["discovery_summary"]["categories"])

        # Organize by package
        for package, categories in organized.items():
            report["agents_by_package"][package] = {}

            for category, agents in categories.items():
                report["agents_by_package"][package][category] = []

                for agent in agents:
                    summary = {
                        "class_name": agent.class_name,
                        "module_path": agent.module_path,
                        "description": agent.description,
                        "base_classes": agent.base_classes,
                        "special_features": agent.special_features
                    }
                    report["agents_by_package"][package][category].append(summary)

                    # Add full details
                    report["agent_details"].append(asdict(agent))

        return report

    def save_report(self, output_file: str) -> None:
        """Save the discovery report to a JSON file."""
        report = self.generate_report()

        with open(output_file, "w") as f:
            json.dump(report, f, indent=2, default=str)

        print(f"Report saved to {output_file}")


def main():
    """Main function to run agent discovery."""
    # Get the base path (project root)
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        # Default to current working directory if run from project root
        base_path = "/home/will/Projects/haive/backend/haive"

    print(f"Starting agent discovery from: {base_path}")

    discoverer = AgentDiscoverer(base_path)
    discoverer.discover_agents()

    # Generate and save report
    output_file = os.path.join(base_path, "agent_discovery_report.json")
    discoverer.save_report(output_file)

    # Print summary
    organized = discoverer.organize_by_category()
    print("\n=== DISCOVERY SUMMARY ===")

    for package, categories in organized.items():
        print(f"\n{package.upper()}:")
        for category, agents in categories.items():
            print(f"  {category}: {len(agents)} agents")
            for agent in agents[:3]:  # Show first 3
                print(f"    - {agent.class_name}")
            if len(agents) > 3:
                print(f"    ... and {len(agents) - 3} more")

    if discoverer.problematic_modules:
        print(f"\nProblematic modules ({len(discoverer.problematic_modules)}):")
        for module in list(discoverer.problematic_modules)[:5]:
            print(f"  - {module}")
        if len(discoverer.problematic_modules) > 5:
            print(f"  ... and {len(discoverer.problematic_modules) - 5} more")


if __name__ == "__main__":
    main()
