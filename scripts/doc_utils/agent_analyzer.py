#!/usr/bin/env python3
"""Agent Analyzer - Comprehensive agent type detection and analysis.

This module provides utilities to automatically detect agent types, analyze inheritance
patterns, and extract metadata from agent implementations across the Haive ecosystem.
"""

import ast
import logging
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class AgentArchitecture(Enum):
    """Agent architecture types."""

    HAIVE_AGENTS_MIXIN = "haive.agents"  # Mixin-based architecture
    HAIVE_CORE_ENGINE = "haive.core.engine"  # Protocol-based architecture
    HAIVE_GAMES = "haive.games"  # Game-specific agents
    UNKNOWN = "unknown"


@dataclass
class AgentInfo:
    """Complete agent information container."""

    name: str
    file_path: Path
    module_path: str
    architecture: AgentArchitecture
    base_classes: list[str]
    has_visualization: bool
    execution_pattern: str  # 'sync', 'async', 'both'
    example_files: list[Path]
    config_pattern: str
    tools_support: bool
    streaming_support: bool
    metadata: dict[str, Any]


class AgentAnalyzer:
    """Comprehensive agent analysis and type detection."""

    def __init__(self, project_root: Path | None = None):
        """Initialize the analyzer.

        Args:
            project_root: Root directory of the Haive project
        """
        if project_root is None:
            # Auto-detect project root
            current = Path(__file__).resolve()
            while current.parent != current:
                if (current / "pyproject.toml").exists():
                    project_root = current
                    break
                current = current.parent
            else:
                project_root = Path.cwd()

        self.project_root = project_root
        self.packages_dir = project_root / "packages"
        self._agent_cache: dict[str, AgentInfo] = {}

    def discover_all_agents(self) -> list[AgentInfo]:
        """Discover all agent implementations across the project.

        Returns:
            List of AgentInfo objects for all discovered agents
        """
        logger.info("Starting comprehensive agent discovery...")

        agents = []

        # Scan all packages for agent files
        if self.packages_dir.exists():
            for package_dir in self.packages_dir.iterdir():
                if package_dir.is_dir() and package_dir.name.startswith("haive-"):
                    agents.extend(self._scan_package_for_agents(package_dir))

        # Scan examples directory
        examples_dir = self.project_root / "examples"
        if examples_dir.exists():
            agents.extend(self._scan_examples_for_agents(examples_dir))

        logger.info(f"Discovered {len(agents)} agents")
        return agents

    def _scan_package_for_agents(self, package_dir: Path) -> list[AgentInfo]:
        """Scan a package directory for agent files.

        Args:
            package_dir: Package directory to scan

        Returns:
            List of discovered agents
        """
        agents = []

        # Find all agent.py files
        agent_files = list(package_dir.rglob("agent.py"))

        # Also check for files named *agent*.py
        for py_file in package_dir.rglob("*.py"):
            if "agent" in py_file.stem.lower() and py_file not in agent_files:
                agent_files.append(py_file)

        for agent_file in agent_files:
            try:
                agent_info = self._analyze_agent_file(agent_file)
                if agent_info:
                    agents.append(agent_info)
            except Exception as e:
                logger.warning(f"Failed to analyze {agent_file}: {e}")

        return agents

    def _scan_examples_for_agents(self, examples_dir: Path) -> list[AgentInfo]:
        """Scan examples directory for agent implementations.

        Args:
            examples_dir: Examples directory to scan

        Returns:
            List of discovered agents in examples
        """
        agents = []

        for example_file in examples_dir.rglob("*.py"):
            if "agent" in example_file.stem.lower():
                try:
                    agent_info = self._analyze_agent_file(example_file)
                    if agent_info:
                        agents.append(agent_info)
                except Exception as e:
                    logger.warning(f"Failed to analyze example {example_file}: {e}")

        return agents

    def _analyze_agent_file(self, file_path: Path) -> AgentInfo | None:
        """Analyze a single agent file for metadata.

        Args:
            file_path: Path to the agent file

        Returns:
            AgentInfo object or None if not a valid agent
        """
        if not file_path.exists():
            return None

        try:
            # Parse the file to extract information
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Parse AST for analysis
            tree = ast.parse(content)

            # Extract agent classes
            agent_classes = self._extract_agent_classes(tree)
            if not agent_classes:
                return None

            # For now, take the first agent class found
            main_class = agent_classes[0]

            # Determine architecture
            architecture = self._detect_architecture(file_path, content)

            # Analyze class details
            base_classes = self._extract_base_classes(main_class)
            has_visualization = self._has_visualization_method(tree)
            execution_pattern = self._detect_execution_pattern(tree, content)

            # Find related example files
            example_files = self._find_related_examples(file_path)

            # Create module path
            module_path = self._create_module_path(file_path)

            return AgentInfo(
                name=main_class.name,
                file_path=file_path,
                module_path=module_path,
                architecture=architecture,
                base_classes=base_classes,
                has_visualization=has_visualization,
                execution_pattern=execution_pattern,
                example_files=example_files,
                config_pattern=self._detect_config_pattern(tree, content),
                tools_support=self._has_tools_support(tree, content),
                streaming_support=self._has_streaming_support(tree, content),
                metadata=self._extract_metadata(tree, content),
            )

        except Exception as e:
            logger.exception(f"Error analyzing {file_path}: {e}")
            return None

    def _extract_agent_classes(self, tree: ast.AST) -> list[ast.ClassDef]:
        """Extract agent class definitions from AST.

        Args:
            tree: Parsed AST

        Returns:
            List of class definitions that appear to be agents
        """
        agent_classes = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check if class name suggests it's an agent
                if (
                    node.name.endswith("Agent")
                    or "agent" in node.name.lower()
                    or any(
                        base.id.endswith("Agent") if hasattr(base, "id") else False
                        for base in node.bases
                        if hasattr(base, "id")
                    )
                ):
                    agent_classes.append(node)

        return agent_classes

    def _detect_architecture(self, file_path: Path, content: str) -> AgentArchitecture:
        """Detect which agent architecture is being used.

        Args:
            file_path: Path to the file
            content: File content

        Returns:
            Detected architecture type
        """
        path_str = str(file_path)

        if "haive-games" in path_str or "/games/" in path_str:
            return AgentArchitecture.HAIVE_GAMES
        if "haive-agents" in path_str or "/agents/" in path_str:
            return AgentArchitecture.HAIVE_AGENTS_MIXIN
        if "haive-core" in path_str and "/engine/" in path_str:
            return AgentArchitecture.HAIVE_CORE_ENGINE
        if "from haive.agents" in content:
            return AgentArchitecture.HAIVE_AGENTS_MIXIN
        if "from haive.core.engine" in content:
            return AgentArchitecture.HAIVE_CORE_ENGINE
        if "from haive.games" in content:
            return AgentArchitecture.HAIVE_GAMES
        return AgentArchitecture.UNKNOWN

    def _extract_base_classes(self, class_node: ast.ClassDef) -> list[str]:
        """Extract base class names.

        Args:
            class_node: Class AST node

        Returns:
            List of base class names
        """
        bases = []
        for base in class_node.bases:
            if hasattr(base, "id"):
                bases.append(base.id)
            elif hasattr(base, "attr") and hasattr(base, "value"):
                # Handle module.ClassName format
                if hasattr(base.value, "id"):
                    bases.append(f"{base.value.id}.{base.attr}")
                else:
                    bases.append(base.attr)
        return bases

    def _has_visualization_method(self, tree: ast.AST) -> bool:
        """Check if the agent has visualization capabilities.

        Args:
            tree: Parsed AST

        Returns:
            True if visualization methods are found
        """
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if "visualize" in node.name.lower() or node.name in [
                    "visualize_graph",
                    "generate_graph",
                ]:
                    return True
        return False

    def _detect_execution_pattern(self, tree: ast.AST, content: str) -> str:
        """Detect if agent supports sync, async, or both execution patterns.

        Args:
            tree: Parsed AST
            content: File content

        Returns:
            Execution pattern: 'sync', 'async', or 'both'
        """
        has_async = False
        has_sync = False

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name in ["run", "execute", "process"]:
                    has_sync = True
                elif node.name in ["arun", "aexecute", "aprocess"]:
                    has_async = True

        # Also check for async keywords in content
        if "async def" in content or "await " in content:
            has_async = True

        if has_async and has_sync:
            return "both"
        if has_async:
            return "async"
        return "sync"

    def _find_related_examples(self, agent_file: Path) -> list[Path]:
        """Find example files related to this agent.

        Args:
            agent_file: Path to the agent file

        Returns:
            List of related example files
        """
        examples = []

        # Check in same directory
        agent_dir = agent_file.parent
        for example_file in agent_dir.glob("example*.py"):
            examples.append(example_file)

        # Check for examples directory nearby
        examples_dir = agent_dir / "examples"
        if examples_dir.exists():
            for example_file in examples_dir.glob("*.py"):
                examples.append(example_file)

        return examples

    def _create_module_path(self, file_path: Path) -> str:
        """Create importable module path from file path.

        Args:
            file_path: Path to the file

        Returns:
            Module import path
        """
        # Convert file path to module path
        relative_path = file_path.relative_to(self.project_root)

        # Handle packages structure
        parts = list(relative_path.parts)

        # Find src directory if it exists
        if "src" in parts:
            src_idx = parts.index("src")
            parts = parts[src_idx + 1 :]

        # Remove .py extension
        if parts[-1].endswith(".py"):
            parts[-1] = parts[-1][:-3]

        return ".".join(parts)

    def _detect_config_pattern(self, tree: ast.AST, content: str) -> str:
        """Detect configuration pattern used by the agent.

        Args:
            tree: Parsed AST
            content: File content

        Returns:
            Configuration pattern description
        """
        if "AugLLMConfig" in content:
            return "AugLLMConfig"
        if "AgentConfig" in content:
            return "AgentConfig"
        if "BaseModel" in content:
            return "Pydantic"
        return "Unknown"

    def _has_tools_support(self, tree: ast.AST, content: str) -> bool:
        """Check if agent supports tools.

        Args:
            tree: Parsed AST
            content: File content

        Returns:
            True if tools are supported
        """
        return "tools" in content.lower() or "Tool" in content or "@tool" in content

    def _has_streaming_support(self, tree: ast.AST, content: str) -> bool:
        """Check if agent supports streaming.

        Args:
            tree: Parsed AST
            content: File content

        Returns:
            True if streaming is supported
        """
        return (
            "stream" in content.lower()
            or "chunk" in content.lower()
            or "yield" in content
        )

    def _extract_metadata(self, tree: ast.AST, content: str) -> dict[str, Any]:
        """Extract additional metadata from agent file.

        Args:
            tree: Parsed AST
            content: File content

        Returns:
            Metadata dictionary
        """
        metadata = {}

        # Extract docstring
        if (
            isinstance(tree, ast.Module)
            and tree.body
            and isinstance(tree.body[0], ast.Expr)
            and isinstance(tree.body[0].value, ast.Constant)
        ):
            metadata["docstring"] = tree.body[0].value.value

        # Count methods
        method_count = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                method_count += 1
        metadata["method_count"] = method_count

        # Check for common imports
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import | ast.ImportFrom):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        imports.append(name.name)
                elif node.module:
                    imports.append(node.module)
        metadata["imports"] = imports

        return metadata

    def get_agent_by_name(self, name: str) -> AgentInfo | None:
        """Get agent information by name.

        Args:
            name: Agent name to search for

        Returns:
            AgentInfo if found, None otherwise
        """
        if name in self._agent_cache:
            return self._agent_cache[name]

        # Search through discovered agents
        for agent in self.discover_all_agents():
            if agent.name.lower() == name.lower():
                self._agent_cache[name] = agent
                return agent

        return None

    def get_agents_by_architecture(
        self, architecture: AgentArchitecture
    ) -> list[AgentInfo]:
        """Get all agents using a specific architecture.

        Args:
            architecture: Architecture type to filter by

        Returns:
            List of agents using the specified architecture
        """
        return [
            agent
            for agent in self.discover_all_agents()
            if agent.architecture == architecture
        ]

    def analyze_inheritance_patterns(self) -> dict[str, list[str]]:
        """Analyze inheritance patterns across all agents.

        Returns:
            Dictionary mapping base classes to derived classes
        """
        inheritance_map = {}

        for agent in self.discover_all_agents():
            for base_class in agent.base_classes:
                if base_class not in inheritance_map:
                    inheritance_map[base_class] = []
                inheritance_map[base_class].append(agent.name)

        return inheritance_map

    def generate_analysis_report(self) -> str:
        """Generate a comprehensive analysis report.

        Returns:
            Formatted analysis report
        """
        agents = self.discover_all_agents()

        report = ["# Agent Analysis Report", ""]
        report.append(f"**Total Agents Found**: {len(agents)}")
        report.append("")

        # Architecture breakdown
        arch_counts = {}
        for agent in agents:
            arch_counts[agent.architecture] = arch_counts.get(agent.architecture, 0) + 1

        report.append("## Architecture Distribution")
        for arch, count in arch_counts.items():
            report.append(f"- {arch.value}: {count} agents")
        report.append("")

        # Visualization support
        viz_count = sum(1 for agent in agents if agent.has_visualization)
        report.append("## Visualization Support")
        report.append(f"- With visualization: {viz_count}")
        report.append(f"- Without visualization: {len(agents) - viz_count}")
        report.append("")

        # Execution patterns
        exec_patterns = {}
        for agent in agents:
            exec_patterns[agent.execution_pattern] = (
                exec_patterns.get(agent.execution_pattern, 0) + 1
            )

        report.append("## Execution Patterns")
        for pattern, count in exec_patterns.items():
            report.append(f"- {pattern}: {count} agents")
        report.append("")

        # Top base classes
        inheritance = self.analyze_inheritance_patterns()
        report.append("## Top Base Classes")
        sorted_bases = sorted(
            inheritance.items(), key=lambda x: len(x[1]), reverse=True
        )
        for base_class, derived in sorted_bases[:10]:
            report.append(f"- {base_class}: {len(derived)} agents")

        return "\n".join(report)
