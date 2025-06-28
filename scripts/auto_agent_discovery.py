#!/usr/bin/env python3
"""Automatic agent discovery and documentation generation.

This script automatically discovers all available agents in the Haive ecosystem,
runs example scenarios, and generates comprehensive documentation.
"""

import ast
import importlib.util
import inspect
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Type

# Add project paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "packages" / "haive-core" / "src"))
sys.path.insert(0, str(project_root / "packages" / "haive-agents" / "src"))

from haive.core.utils.agent_capture import capture_agent_run
from haive.core.utils.doc_agent_showcase import batch_document_agents

logger = logging.getLogger(__name__)


class AgentDiscovery:
    """Discovers and analyzes agents across the Haive ecosystem."""

    def __init__(self, packages_dir: Path):
        self.packages_dir = packages_dir
        self.discovered_agents: list[dict[str, Any]] = []
        self.failed_imports: list[str] = []

    def discover_all_agents(self) -> list[dict[str, Any]]:
        """Discover all agents across packages."""
        logger.info("🔍 Starting agent discovery across packages...")

        # Agent packages to scan
        agent_packages = ["haive-agents", "haive-core", "haive-prebuilt"]

        for package in agent_packages:
            package_path = self.packages_dir / package / "src"
            if package_path.exists():
                self._scan_package(package_path, package)

        logger.info(f"✅ Discovered {len(self.discovered_agents)} agents")
        logger.info(f"⚠️ Failed to import {len(self.failed_imports)} modules")

        return self.discovered_agents

    def _scan_package(self, package_path: Path, package_name: str):
        """Scan a package for agent classes."""
        logger.info(f"📦 Scanning {package_name}...")

        # Find all Python files that might contain agents
        python_files = list(package_path.rglob("*.py"))

        for py_file in python_files:
            if self._should_skip_file(py_file):
                continue

            try:
                self._analyze_file(py_file, package_name)
            except Exception as e:
                logger.debug(f"Failed to analyze {py_file}: {e}")

    def _should_skip_file(self, py_file: Path) -> bool:
        """Check if we should skip analyzing this file."""
        skip_patterns = [
            "__pycache__",
            ".pytest_cache",
            "test_",
            "_test.py",
            "__init__.py",
        ]

        file_str = str(py_file)
        return any(pattern in file_str for pattern in skip_patterns)

    def _analyze_file(self, py_file: Path, package_name: str):
        """Analyze a Python file for agent classes."""
        try:
            with open(py_file, encoding="utf-8") as f:
                content = f.read()

            # Parse AST to find agent classes
            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    if self._is_agent_class(node, content):
                        agent_info = self._extract_agent_info(
                            node, py_file, package_name, content
                        )
                        if agent_info:
                            self.discovered_agents.append(agent_info)

        except Exception as e:
            logger.debug(f"Error analyzing {py_file}: {e}")

    def _is_agent_class(self, node: ast.ClassDef, content: str) -> bool:
        """Check if a class is likely an agent."""
        # Check class name patterns
        agent_patterns = ["Agent", "agent"]
        if not any(pattern in node.name for pattern in agent_patterns):
            return False

        # Check for base classes that suggest it's an agent
        base_patterns = ["Agent", "BaseAgent", "ReactAgent"]
        for base in node.bases:
            if isinstance(base, ast.Name) and any(
                pattern in base.id for pattern in base_patterns
            ):
                return True

        # Check for agent-like methods
        method_names = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
        agent_methods = ["run", "stream", "invoke", "execute"]

        return any(method in method_names for method in agent_methods)

    def _extract_agent_info(
        self, node: ast.ClassDef, py_file: Path, package_name: str, content: str
    ) -> Dict[str, Any] | None:
        """Extract information about an agent class."""
        try:
            # Extract module path
            relative_path = py_file.relative_to(self.packages_dir)
            module_parts = list(relative_path.with_suffix("").parts)

            # Convert to import path
            if "src" in module_parts:
                src_index = module_parts.index("src")
                module_path = ".".join(module_parts[src_index + 1 :])
            else:
                module_path = ".".join(module_parts)

            # Extract docstring
            docstring = ""
            if (
                node.body
                and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Constant)
            ):
                docstring = node.body[0].value.value

            # Extract methods
            methods = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    methods.append(item.name)

            # Determine agent category
            category = self._categorize_agent(py_file, node.name, docstring)

            return {
                "name": node.name,
                "module_path": module_path,
                "file_path": str(py_file),
                "package": package_name,
                "category": category,
                "docstring": docstring.strip() if docstring else "",
                "methods": methods,
                "has_run": "run" in methods,
                "has_stream": "stream" in methods,
                "has_visualize": "visualize_graph" in methods or "visualize" in methods,
                "line_number": node.lineno,
            }

        except Exception as e:
            logger.debug(f"Error extracting info for {node.name}: {e}")
            return None

    def _categorize_agent(self, py_file: Path, class_name: str, docstring: str) -> str:
        """Categorize an agent based on its path and properties."""
        path_str = str(py_file).lower()
        name_lower = class_name.lower()
        doc_lower = docstring.lower()

        categories = {
            "react": ["react", "tool", "reasoning"],
            "rag": ["rag", "retrieval", "document", "search"],
            "research": ["research", "perplexity", "search"],
            "conversation": ["conversation", "chat", "dialogue"],
            "planning": ["planning", "plan", "execute", "workflow"],
            "simple": ["simple", "basic", "minimal"],
            "memory": ["memory", "recall", "long_term"],
            "game": ["game", "chess", "checkers", "battleship"],
            "analysis": ["analysis", "analyze", "review"],
            "generation": ["generation", "generate", "create", "write"],
        }

        for category, keywords in categories.items():
            if any(
                keyword in path_str or keyword in name_lower or keyword in doc_lower
                for keyword in keywords
            ):
                return category

        return "misc"


class RealAgentTester:
    """Tests real agents with appropriate inputs."""

    def __init__(self):
        self.test_cases = {
            "simple": [
                {"query": "What is artificial intelligence?"},
                {"question": "Explain machine learning briefly"},
                {"user_input": "What are the benefits of renewable energy?"},
            ],
            "react": [
                {"input": "Research the latest developments in quantum computing"},
                {
                    "task": "Find information about climate change solutions",
                    "tools_required": ["search"],
                },
                {"query": "What are the current trends in AI research?"},
            ],
            "rag": [
                {"question": "What is the impact of AI on healthcare?"},
                {"query": "Summarize recent papers on neural networks"},
                {
                    "context": "machine learning",
                    "question": "How does deep learning work?",
                },
            ],
            "research": [
                {
                    "research_topic": "renewable energy innovations",
                    "depth": "comprehensive",
                },
                {"query": "Latest breakthroughs in battery technology"},
                {"topic": "artificial intelligence ethics"},
            ],
            "conversation": [
                {"message": "Hello, how can you help me?"},
                {"input": "Let's discuss the future of AI"},
                {"user_input": "What's your opinion on automation?"},
            ],
            "planning": [
                {"goal": "Plan a research project on climate change"},
                {"task": "Create a workflow for data analysis"},
                {"objective": "Design a learning curriculum for AI"},
            ],
            "game": [
                {"move": "e4", "game_type": "chess"},
                {"action": "start_game"},
                {"command": "make_move", "position": "center"},
            ],
        }

    def get_test_input(self, agent_info: dict[str, Any]) -> dict[str, Any]:
        """Get appropriate test input for an agent."""
        category = agent_info.get("category", "simple")
        test_cases = self.test_cases.get(category, self.test_cases["simple"])

        # Return first test case for the category
        return test_cases[0] if test_cases else {"query": "Test input"}

    def can_test_agent(self, agent_info: dict[str, Any]) -> bool:
        """Check if we can safely test this agent."""
        # Skip agents that might require complex setup
        skip_patterns = [
            "abstract",
            "base",
            "test",
            "mock",
            "example",
            "template",
            "skeleton",
            "stub",
        ]

        name_lower = agent_info["name"].lower()
        return not any(pattern in name_lower for pattern in skip_patterns)


def main():
    """Main function to discover and document agents."""
    logging.basicConfig(level=logging.INFO)


    packages_dir = project_root / "packages"

    # Discover agents
    discovery = AgentDiscovery(packages_dir)
    agents = discovery.discover_all_agents()

    if not agents:
        return 1


    # Group by category
    by_category = {}
    for agent in agents:
        category = agent["category"]
        by_category.setdefault(category, []).append(agent)

    for category, category_agents in by_category.items():
        pass

    # Test and document promising agents
    tester = RealAgentTester()
    testable_agents = [agent for agent in agents if tester.can_test_agent(agent)]


    successful_tests = []

    for agent_info in testable_agents[:5]:  # Limit to first 5 for demo
        try:

            # Try to import and instantiate
            module_path = agent_info["module_path"]
            class_name = agent_info["name"]

            # Dynamic import
            spec = importlib.util.spec_from_file_location(
                module_path.replace("/", "."), agent_info["file_path"]
            )
            if not spec or not spec.loader:
                continue

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            agent_class = getattr(module, class_name, None)
            if not agent_class:
                continue

            # Try to instantiate (this might fail for many agents)
            try:
                agent = agent_class()
            except Exception:
                # Try with empty config if available
                try:
                    agent = agent_class(config={})
                except Exception:
                    continue

            # Get test input
            test_input = tester.get_test_input(agent_info)

            # Capture run
            run = capture_agent_run(
                agent, test_input, agent_name=class_name, capture_dir="docs/captures"
            )

            successful_tests.append(
                (
                    agent,
                    test_input,
                    {
                        "agent_name": class_name,
                        "description": f"Auto-discovered {agent_info['category']} agent",
                        "category": agent_info["category"],
                    },
                )
            )


        except Exception as e:
            continue

    if successful_tests:

        # Generate batch documentation
        generated_files = batch_document_agents(successful_tests)

        for file_path in generated_files:
            pass}")


    return 0


if __name__ == "__main__":
    sys.exit(main())
