"""Haive Sphinx Extension.

Custom Sphinx extension for Haive documentation that provides:
- Agent run display directive
- README discovery and integration
- Automatic agent showcase generation
- Enhanced autosummary features
"""

import ast
from collections import defaultdict
from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective


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


class AgentRunCaptureDirective(SphinxDirective):
    """Directive to display captured agent runs with interactive replay.

    Usage:
        .. agent-run-capture:: path/to/capture.json
           :paginated:
           :page-size: 10
           :show-graph:
           :show-logs:
           :show-metrics:
    """

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    option_spec = {
        "paginated": directives.flag,
        "page-size": directives.positive_int,
        "show-graph": directives.flag,
        "show-logs": directives.flag,
        "show-metrics": directives.flag,
    }

    def run(self):
        """Process the directive."""
        # Get capture file path
        capture_path = Path(self.arguments[0])
        if not capture_path.is_absolute():
            # Make relative to source directory
            capture_path = Path(self.env.srcdir) / capture_path

        if not capture_path.exists():
            logger.warning(f"Agent run capture not found: {capture_path}")
            return []

        # Load capture data
        try:
            with open(capture_path) as f:
                capture_data = json.load(f)
        except Exception:
            logger.exception("Failed to load capture")
            return []

        # Extract options
        paginated = "paginated" in self.options
        page_size = self.options.get("page-size", 10)
        show_graph = "show-graph" in self.options
        show_metrics = "show-metrics" in self.options

        # Create main container
        container = nodes.container(classes=["agent-run-capture"])

        # Add capture metadata section
        self._add_capture_metadata(container, capture_data)

        # Add graph visualization if requested and available
        if show_graph and capture_data.get("graph_visualization_path"):
            self._add_graph_section(container, capture_data)

        # Add execution steps
        self._add_execution_steps(container, capture_data, paginated, page_size)

        # Add metrics if requested
        if show_metrics:
            self._add_metrics_section(container, capture_data)

        return [container]

    def _add_capture_metadata(self, container, capture_data):
        """Add capture metadata section."""
        metadata_section = nodes.section()
        metadata_title = nodes.title(text="Execution Overview")
        metadata_section += metadata_title

        # Create summary table
        table = nodes.table()
        tgroup = nodes.tgroup(cols=2)
        table += tgroup

        # Add column specifications
        tgroup += nodes.colspec(colwidth=30)
        tgroup += nodes.colspec(colwidth=70)

        # Add table body
        tbody = nodes.tbody()
        tgroup += tbody

        # Add metadata rows
        metadata_items = [
            ("Agent Name", capture_data.get("agent_name", "Unknown")),
            ("Agent Type", capture_data.get("agent_type", "Unknown")),
            ("Run ID", capture_data.get("run_id", "Unknown")[:8] + "..."),
            (
                "Status",
                "✅ Success" if capture_data.get("error") is None else "❌ Failed",
            ),
            (
                "Duration",
                (
                    f"{capture_data.get('duration', 0):.2f}s"
                    if capture_data.get("end_time")
                    else "Running..."
                ),
            ),
            ("Steps", str(len(capture_data.get("steps", [])))),
        ]

        for key, value in metadata_items:
            row = nodes.row()
            row += nodes.entry("", nodes.paragraph(text=key))
            row += nodes.entry("", nodes.paragraph(text=str(value)))
            tbody += row

        metadata_section += table
        container += metadata_section

    def _add_graph_section(self, container, capture_data):
        """Add graph visualization section."""
        graph_section = nodes.section()
        graph_title = nodes.title(text="Agent Architecture")
        graph_section += graph_title

        graph_path = capture_data.get("graph_visualization_path")
        if graph_path:
            # Create figure node
            figure = nodes.figure()
            image = nodes.image()
            image["uri"] = str(Path(graph_path).relative_to(Path.cwd()))
            image["alt"] = f"{capture_data.get('agent_name', 'Agent')} Graph"
            image["align"] = "center"
            figure += image

            # Add caption
            caption = nodes.caption(text="Agent workflow graph showing the execution flow")
            figure += caption

            graph_section += figure

        container += graph_section

    def _add_execution_steps(self, container, capture_data, paginated, page_size):
        """Add execution steps section."""
        steps_section = nodes.section()
        steps_title = nodes.title(text="Execution Steps")
        steps_section += steps_title

        steps = capture_data.get("steps", [])

        if not steps:
            steps_section += nodes.paragraph(text="No execution steps recorded.")
            container += steps_section
            return

        # Determine which steps to show
        display_steps = steps
        if paginated and len(steps) > page_size:
            display_steps = steps[:page_size]
            remaining = len(steps) - page_size

            # Add pagination info
            pagination_info = nodes.paragraph(
                text=f"Showing first {page_size} of {len(steps)} steps. "
                f"{remaining} more steps available in full capture."
            )
            pagination_info["classes"] = ["pagination-info"]
            steps_section += pagination_info

        # Create steps as numbered list
        step_list = nodes.enumerated_list()

        for _i, step in enumerate(display_steps):
            list_item = nodes.list_item()

            # Step header with type and timestamp
            step_type = step.get("step_type", "unknown")
            timestamp = step.get("timestamp", "")
            node_name = step.get("node_name", "")

            header_text = f"**{step_type.title()}**"
            if node_name:
                header_text += f" - {node_name}"
            if timestamp:
                header_text += f" ({timestamp})"

            header = nodes.paragraph()
            header += nodes.raw("", header_text, format="rst")
            list_item += header

            # Step content
            content = step.get("content", {})
            if content:
                # Create collapsible content section
                content_container = nodes.container(classes=["step-content"])

                # Add content as code block
                content_text = json.dumps(content, indent=2)
                code_block = nodes.literal_block(content_text, content_text)
                code_block["language"] = "json"
                content_container += code_block

                list_item += content_container

            step_list += list_item

        steps_section += step_list
        container += steps_section

    def _add_metrics_section(self, container, capture_data):
        """Add metrics section."""
        metrics_section = nodes.section()
        metrics_title = nodes.title(text="Performance Metrics")
        metrics_section += metrics_title

        steps = capture_data.get("steps", [])

        # Calculate step type distribution
        step_types = {}
        for step in steps:
            step_type = step.get("step_type", "unknown")
            step_types[step_type] = step_types.get(step_type, 0) + 1

        # Create metrics table
        table = nodes.table()
        tgroup = nodes.tgroup(cols=2)
        table += tgroup

        tgroup += nodes.colspec(colwidth=50)
        tgroup += nodes.colspec(colwidth=50)

        # Add header
        thead = nodes.thead()
        header_row = nodes.row()
        header_row += nodes.entry("", nodes.paragraph(text="Metric"))
        header_row += nodes.entry("", nodes.paragraph(text="Value"))
        thead += header_row
        tgroup += thead

        # Add body
        tbody = nodes.tbody()
        tgroup += tbody

        # Add step type breakdown
        for step_type, count in step_types.items():
            row = nodes.row()
            row += nodes.entry("", nodes.paragraph(text=f"{step_type.title()} Steps"))
            row += nodes.entry("", nodes.paragraph(text=str(count)))
            tbody += row

        metrics_section += table
        container += metrics_section
        container["classes"].append("agent-run-output")
        if paginated:
            container["data-paginated"] = "true"
            container["data-page-size"] = str(page_size)

        # Add header
        header = nodes.container()
        header["classes"].append("run-header")

        metadata = capture_data.get("metadata", {})

        # Agent info
        agent_info = nodes.paragraph()
        agent_info += nodes.strong(text="Agent: ")
        agent_info += nodes.Text(metadata.get("agent_name", "Unknown"))
        header += agent_info

        # Type info
        type_info = nodes.paragraph()
        type_info += nodes.strong(text="Type: ")
        type_info += nodes.Text(metadata.get("agent_type", "Unknown"))
        header += type_info

        # Timestamp
        timestamp_info = nodes.paragraph()
        timestamp_info += nodes.strong(text="Timestamp: ")
        timestamp_info += nodes.Text(metadata.get("timestamp", "Unknown"))
        header += timestamp_info

        # Duration
        duration_info = nodes.paragraph()
        duration_info += nodes.strong(text="Duration: ")
        duration = metadata.get("duration", 0)
        duration_info += nodes.Text(f"{duration:.2f}s")
        header += duration_info

        # Status
        status_info = nodes.paragraph()
        status_info += nodes.strong(text="Status: ")
        success = metadata.get("success", False)
        status_text = "✅ Success" if success else "❌ Failed"
        status_info += nodes.Text(status_text)
        header += status_info

        container += header

        # Add content
        if show_logs and "logs" in capture_data:
            content = nodes.container()
            content["classes"].append("run-content")

            # Create code block with logs
            logs = capture_data["logs"]
            log_text = ""

            for log in logs[:100]:  # Show first 100 logs
                timestamp = log.get("timestamp", "")
                level = log.get("level", "INFO")
                message = log.get("message", "")
                log_text += f"[{timestamp}] {level}: {message}\n"

            if len(logs) > 100:
                log_text += f"\n... and {len(logs) - 100} more logs"

            literal = nodes.literal_block(log_text, log_text)
            literal["language"] = "text"
            content += literal
            container += content

        # Add metrics
        if show_metrics and "performance_metrics" in capture_data:
            metrics_section = nodes.container()
            metrics_section["classes"].append("run-metrics")

            metrics_title = nodes.paragraph()
            metrics_title += nodes.strong(text="Performance Metrics:")
            metrics_section += metrics_title

            metrics = capture_data["performance_metrics"]
            metrics_list = nodes.bullet_list()

            for key, value in metrics.items():
                item = nodes.list_item()
                para = nodes.paragraph()
                para += nodes.Text(f"{key}: {value}")
                item += para
                metrics_list += item

            metrics_section += metrics_list
            container += metrics_section

        # Add graph visualization
        if show_graph and "graph_visualizations" in capture_data:
            graphs = capture_data["graph_visualizations"]
            if graphs:
                graph_container = nodes.container()
                graph_container["classes"].append("agent-graph")

                # Add image
                image_path = graphs[0]
                image = nodes.image(uri=image_path)
                image["alt"] = "Agent Graph Visualization"
                image["align"] = "center"
                graph_container += image

                container += graph_container

        return [container]


class ReadmeDiscoveryDirective(SphinxDirective):
    """Directive to automatically discover and include README files.

    Usage:
        .. readme-discovery:: packages/haive-agents
           :pattern: **/README.md
           :max-depth: 3
    """

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    option_spec = {
        "pattern": directives.unchanged,
        "max-depth": directives.positive_int,
        "exclude": directives.unchanged,
    }

    def run(self):
        """Process the directive."""
        search_path = Path(self.arguments[0])
        if not search_path.is_absolute():
            search_path = Path(self.env.srcdir).parent.parent / search_path

        pattern = self.options.get("pattern", "**/README.md")
        max_depth = self.options.get("max-depth", 3)
        exclude_patterns = self.options.get("exclude", "").split(",")

        # Find README files
        readme_files = []
        for readme_path in search_path.rglob(pattern):
            # Check depth
            relative_path = readme_path.relative_to(search_path)
            if len(relative_path.parts) > max_depth:
                continue

            # Check exclusions
            if any(exc.strip() in str(relative_path) for exc in exclude_patterns if exc.strip()):
                continue

            readme_files.append((readme_path, relative_path))

        # Sort by path
        readme_files.sort(key=lambda x: x[1])

        # Create container
        container = nodes.container()

        # Add title
        title = nodes.title(text="Discovered Documentation")
        container += title

        # Create toctree-like structure
        toc_list = nodes.bullet_list()

        for readme_path, relative_path in readme_files:
            item = nodes.list_item()

            # Create reference
            ref = nodes.reference()
            ref["refuri"] = str(relative_path)
            ref += nodes.Text(str(relative_path.parent))

            para = nodes.paragraph()
            para += ref

            # Try to extract first paragraph as description
            try:
                with open(readme_path) as f:
                    content = f.read()
                    lines = content.split("\n")
                    for line in lines:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            para += nodes.Text(f" - {line[:100]}...")
                            break
            except:
                pass

            item += para
            toc_list += item

        container += toc_list

        return [container]


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

        # Skip non-Python files or __init__.py files
        return bool(file_path.suffix != ".py" or file_path.name == "__init__.py")

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
                    agent_info = self.analyze_class_node(node, file_path, module_docstring)
                    if agent_info:
                        agents.append(agent_info)

        except SyntaxError as e:
            self.errors.append(f"Syntax error in {file_path}: {e}")
        except Exception as e:
            self.errors.append(f"Error parsing {file_path}: {e}")

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
            module_parts = list(module_parts) + [file_path.stem]  # Add filename without extension
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
                module_parts = [*list(module_parts[:-1]), file_path.stem]
                return ".".join(module_parts)
            except ValueError:
                return str(file_path.stem)

    def categorize_agent(self, file_path: Path, class_name: str, docstring: str) -> str:
        """Categorize an agent based on its location and characteristics."""
        path_str = str(file_path).lower()

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

    def determine_complexity(self, node: ast.ClassDef, docstring: str, features: list[str]) -> str:
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
            if first_line and not first_line.startswith(("Args:", "Parameters:", "Returns:")):
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
        packages = ["haive-agents", "haive-prebuilt", "haive-games"]

        for package_name in packages:
            package_path = self.packages_dir / package_name
            if not package_path.exists():
                continue

            self.scan_package(package_path)

        # Organize by categories
        for agent in self.agents:
            self.categories[agent.category].append(agent)

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
                continue

            agents = self.extract_agent_info_from_ast(file_path)
            self.agents.extend(agents)


def generate_agent_showcase(workspace_root: Path, output_dir: Path) -> dict[str, Any]:
    """Generate agent showcase data and documentation."""
    logger.info("🤖 Discovering agents across haive packages...")

    discovery = AgentDiscovery(workspace_root)
    discovery.discover_agents()

    # Generate showcase data
    showcase_data = {
        "metadata": {
            "total_agents": len(discovery.agents),
            "total_categories": len(discovery.categories),
            "packages": list({agent.package for agent in discovery.agents}),
            "errors_count": len(discovery.errors),
        },
        "categories": {},
        "agents": [],
        "stats": {
            "by_package": defaultdict(int),
            "by_category": defaultdict(int),
            "by_complexity": defaultdict(int),
            "features": defaultdict(int),
        },
    }

    # Organize by categories
    for category, agents in discovery.categories.items():
        showcase_data["categories"][category] = {
            "count": len(agents),
            "agents": [agent.name for agent in agents],
            "packages": list({agent.package for agent in agents}),
            "complexity_breakdown": {
                "simple": len([a for a in agents if a.complexity == "simple"]),
                "medium": len([a for a in agents if a.complexity == "medium"]),
                "complex": len([a for a in agents if a.complexity == "complex"]),
            },
        }

    # Add detailed agent information
    for agent in discovery.agents:
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

        # Update stats
        showcase_data["stats"]["by_package"][agent.package] += 1
        showcase_data["stats"]["by_category"][agent.category] += 1
        showcase_data["stats"]["by_complexity"][agent.complexity] += 1

        for feature in agent.features:
            showcase_data["stats"]["features"][feature] += 1

    # Convert defaultdicts to regular dicts
    for key, value in showcase_data["stats"].items():
        if isinstance(value, defaultdict):
            showcase_data["stats"][key] = dict(value)

    # Generate showcase documentation
    agents_dir = output_dir / "agents"
    agents_dir.mkdir(exist_ok=True)

    # Generate main showcase page
    showcase_content = generate_showcase_content(showcase_data)
    (agents_dir / "showcase.md").write_text(showcase_content)

    # Generate complete index
    index_content = generate_complete_index(showcase_data["agents"])
    (agents_dir / "complete_index.md").write_text(index_content)

    logger.info(
        f"✅ Generated showcase for {showcase_data['metadata']['total_agents']} agents across {showcase_data['metadata']['total_categories']} categories"
    )

    return showcase_data


def generate_showcase_content(data: dict[str, Any]) -> str:
    """Generate the main showcase content."""
    metadata = data["metadata"]
    stats = data["stats"]
    categories = data["categories"]

    content = f"""# 🤖 Haive Agent Showcase

Welcome to the comprehensive showcase of Haive's intelligent agent ecosystem! This showcase presents **{metadata["total_agents"]} agents** across **{metadata["total_categories"]} categories**, demonstrating the full breadth and power of the Haive framework.

## 📊 Agent Ecosystem Overview

### 📈 Quick Stats

| Metric | Value |
|--------|-------|
| **Total Agents** | {metadata["total_agents"]} |
| **Categories** | {metadata["total_categories"]} |
| **Packages** | {len(metadata["packages"])} |
| **Complex Agents** | {stats["by_complexity"].get("complex", 0)} |

### 🏷️ Top Agent Categories

"""

    # Add category overview
    sorted_categories = sorted(categories.items(), key=lambda x: x[1]["count"], reverse=True)

    content += "| Category | Agents | Primary Package |\n"
    content += "|----------|--------|----------------|\n"

    for category, cat_data in sorted_categories[:10]:  # Top 10 categories
        primary_package = (
            max(cat_data["packages"], key=lambda x: x.count(x))
            if cat_data["packages"]
            else "unknown"
        )
        content += f"| **{category}** | {cat_data['count']} | `{primary_package}` |\n"

    if len(sorted_categories) > 10:
        content += f"| *...and {len(sorted_categories) - 10} more categories* | | |\n"

    # Add getting started section
    content += """

## 🚀 Getting Started

### Quick Start Guide

1. **Choose Your Agent Type**
   - 🌟 **New to Haive?** Start with Foundation Agents (SimpleAgent, ReactAgent)
   - 🎯 **Building Apps?** Check out Prebuilt Solutis
   - 🎮 **Want Fun?** Explore Game Agents
   - 🧠 **Advanced Use?** Try Reasoning & Critique agents

2. **Install & Import**
   ```bash
   pip install haive[agents]    # Core agents
   pip install haive[games]     # Game agents
   pip install haive[prebuilt]  # Business solutions
   ```

3. **Basic Usage Pattern**
   ```python
   from haive.agents.simple import SimpleAgent

   # Create agent
   agent = SimpleAgent(
       name="my_agent",
       model="gpt-4"
   )

   # Use agent
   result = agent.invoke({"query": "Your task here"})
   ```

## 📚 Complete Agent Catalog

"""

    # Generate complete catalog
    for category, cat_data in sorted_categories:
        content += f"### {category}\n\n"
        content += f"**{cat_data['count']} agents** | "
        content += f"**Packages:** {', '.join(cat_data['packages'])}\n\n"

        # Get agents in this category
        category_agents = [a for a in data["agents"] if a["category"] == category]
        category_agents.sort(key=lambda x: (x["complexity"], x["name"]))

        # Show agents in a table
        content += "| Agent | Complexity | Features | Description |\n"
        content += "|-------|------------|----------|-------------|\n"

        for agent in category_agents:
            complexity_badge = {
                "simple": "🟢 Simple",
                "medium": "🟡 Medium",
                "complex": "🔴 Complex",
            }.get(agent["complexity"], "❓ Unknown")
            features_str = ", ".join(agent["features"][:2]) if agent["features"] else "Basic"
            if len(agent["features"]) > 2:
                features_str += f" +{len(agent['features']) - 2}"

            description = (
                agent["description"][:80] + "..."
                if len(agent["description"]) > 80
                else agent["description"]
            )

            content += (
                f"| **{agent['name']}** | {complexity_badge} | {features_str} | {description} |\n"
            )

        content += "\n"

    return content


def generate_complete_index(agents: list[dict[str, Any]]) -> str:
    """Generate a complete alphabetical index of all agents."""
    agents = sorted(agents, key=lambda x: x["name"])

    content = """# 📚 Complete Agent Index

Alphabetical listing of all agents in the Haive ecosystem.

"""

    # Group by first letter
    by_letter = {}
    for agent in agents:
        letter = agent["name"][0].upper()
        if letter not in by_letter:
            by_letter[letter] = []
        by_letter[letter].append(agent)

    # Generate index by letter
    for letter in sorted(by_letter.keys()):
        content += f"## {letter}\n\n"

        for agent in by_letter[letter]:
            complexity_badge = {
                "simple": "🟢 Simple",
                "medium": "🟡 Medium",
                "complex": "🔴 Complex",
            }.get(agent["complexity"], "❓ Unknown")
            features_str = ", ".join(agent["features"][:3]) if agent["features"] else "Basic"
            if len(agent["features"]) > 3:
                features_str += f", +{len(agent['features']) - 3} more"

            content += f"""
**{agent["name"]}** ({complexity_badge})
*{agent["category"]} | {agent["package"]}*
{agent["description"][:150]}{"..." if len(agent["description"]) > 150 else ""}
**Features:** {features_str}
**Module:** `{agent["module_path"]}`

"""

    return content


def discover_readmes(app: Sphinx, config: Any) -> None:
    """Discover README files and create index."""
    if not getattr(config, "haive_readme_discovery", True):
        return

    logger.info("Discovering README files...")

    # Get workspace root
    workspace_root = Path(app.srcdir).parent.parent
    packages_dir = workspace_root / "packages"

    # Output directory for discovered READMEs
    readme_dir = Path(app.srcdir) / "discovered_readmes"
    readme_dir.mkdir(exist_ok=True)

    # Find all README files
    readme_files = []
    for package_dir in packages_dir.glob("haive-*"):
        for readme in package_dir.rglob("README.md"):
            # Skip node_modules, build directories, etc.
            if any(
                part in readme.parts
                for part in ["node_modules", "build", "dist", "__pycache__", ".git"]
            ):
                continue

            readme_files.append(readme)

    # Create index file
    index_content = """
Discovered README Files
=======================

This page lists all README files discovered in the Haive packages.

.. toctree::
   :maxdepth: 2
   :caption: Package READMEs

"""

    # Process each README
    for readme_path in sorted(readme_files):
        relative_path = readme_path.relative_to(workspace_root)

        # Create a copy in the docs with proper path
        output_path = readme_dir / relative_path.parent / readme_path.name
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Copy the file
        output_path.write_text(readme_path.read_text())

        # Add to index
        doc_path = output_path.relative_to(Path(app.srcdir))
        index_content += f"   {doc_path.with_suffix('')}\n"

    # Write index
    index_path = readme_dir / "index.rst"
    index_path.write_text(index_content)

    logger.info(f"Discovered {len(readme_files)} README files")


def generate_agent_showcase_hook(app: Sphinx, config: Any) -> None:
    """Generate agent showcase during documentation build."""
    if not getattr(config, "haive_agent_showcase", True):
        return

    workspace_root = Path(app.srcdir).parent.parent
    output_dir = Path(app.srcdir)

    try:
        showcase_data = generate_agent_showcase(workspace_root, output_dir)

        # Save data for potential use by other tools
        data_file = workspace_root / "docs" / "agent_showcase_data.json"
        data_file.parent.mkdir(exist_ok=True)
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(showcase_data, f, indent=2, ensure_ascii=False)

    except Exception as e:
        logger.exception(f"Failed to generate agent showcase: {e}")


def setup(app: Sphinx) -> dict[str, Any]:
    """Setup the extension."""
    # Add directives
    app.add_directive("agent-run-capture", AgentRunCaptureDirective)
    app.add_directive("readme-discovery", ReadmeDiscoveryDirective)

    # Add event handlers
    app.connect("config-inited", discover_readmes)
    app.connect("config-inited", generate_agent_showcase_hook)

    # Add configuration values
    app.add_config_value("haive_agent_runs_dir", "resources/agent_runs", "env")
    app.add_config_value("haive_agent_showcase", True, "env")

    return {
        "version": "0.2",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
