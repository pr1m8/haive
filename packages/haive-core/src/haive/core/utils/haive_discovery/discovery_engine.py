"""
Main discovery engine for finding and analyzing components.
"""

import importlib
import inspect
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from haive.core.utils.haive_discovery.base_analyzer import ComponentAnalyzer
from haive.core.utils.haive_discovery.component_info import ComponentInfo
from haive.core.utils.haive_discovery.engine_analyzer import EngineAnalyzer
from haive.core.utils.haive_discovery.retriever_analyzers import (
    RetrieverAnalyzer,
    VectorStoreAnalyzer,
)
from haive.core.utils.haive_discovery.tool_analyzers import (
    DocumentLoaderAnalyzer,
    ToolAnalyzer,
)

logger = logging.getLogger(__name__)


class EnhancedComponentDiscovery:
    """Enhanced discovery engine with tool creation capabilities."""

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.analyzers = [
            ToolAnalyzer(),
            DocumentLoaderAnalyzer(),
            RetrieverAnalyzer(),
            VectorStoreAnalyzer(),
            EngineAnalyzer(),
        ]
        self.failed_modules = []
        self.discovered_components = []

    def add_analyzer(self, analyzer: ComponentAnalyzer):
        """Add a custom analyzer."""
        self.analyzers.append(analyzer)

    def discover_from_directory(
        self,
        directory: Union[str, Path],
        module_prefix: str,
        recursive: bool = True,
        create_tools: bool = True,
        ignore_errors: bool = True,
    ) -> List[ComponentInfo]:
        """Discover components from a directory."""
        directory = Path(directory)
        components = []

        if not directory.exists():
            logger.warning(f"Directory not found: {directory}")
            return []

        logger.info(f"Discovering components in: {directory}")

        # Add to Python path if needed
        if str(self.base_path) not in sys.path:
            sys.path.insert(0, str(self.base_path))

        pattern = "**/*.py" if recursive else "*.py"
        for py_file in directory.glob(pattern):
            if py_file.name == "__init__.py":
                continue

            try:
                module_path = self._file_to_module_path(py_file, module_prefix)
                new_components = self._discover_from_module(module_path, create_tools)

                if new_components:
                    logger.debug(
                        f"Found {len(new_components)} components in {module_path}"
                    )
                    components.extend(new_components)

            except Exception as e:
                if ignore_errors:
                    logger.debug(f"Error processing file {py_file}: {e}")
                    self.failed_modules.append((str(py_file), str(e)))
                else:
                    raise

        return components

    def _file_to_module_path(self, file_path: Path, module_prefix: str) -> str:
        """Convert file path to module path."""
        relative_path = file_path.relative_to(self.base_path)
        parts = list(relative_path.parts[:-1]) + [relative_path.stem]

        if parts[0] == "src":
            parts = parts[1:]

        return ".".join(parts)

    def _discover_from_module(
        self, module_path: str, create_tools: bool = True
    ) -> List[ComponentInfo]:
        """Discover components from a single module."""
        components = []

        try:
            logger.debug(f"Loading module: {module_path}")

            module = self._safe_import_module(module_path)
            if module is None:
                return components

            for name, obj in inspect.getmembers(module):
                if name.startswith("_"):
                    continue

                try:
                    # Check for lists of components
                    if isinstance(obj, list):
                        for item in obj:
                            try:
                                component_info = self._analyze_object(
                                    item, module_path, create_tools
                                )
                                if component_info:
                                    components.append(component_info)
                            except Exception as e:
                                logger.debug(f"Error analyzing list item: {e}")
                                continue
                    else:
                        # Check individual objects
                        component_info = self._analyze_object(
                            obj, module_path, create_tools
                        )
                        if component_info:
                            components.append(component_info)

                except Exception as e:
                    logger.debug(f"Error analyzing object {name}: {e}")
                    continue

        except Exception as e:
            logger.warning(f"Error loading module {module_path}: {e}")
            self.failed_modules.append((module_path, str(e)))

        return components

    def _safe_import_module(self, module_path: str):
        """Safely import a module, handling sys.exit() and other issues."""
        try:
            module = importlib.import_module(module_path)
            return module

        except SystemExit as e:
            logger.warning(f"Module {module_path} called sys.exit({e.code})")
            self.failed_modules.append(
                (module_path, f"Module called sys.exit({e.code})")
            )
            return None

        except ImportError as e:
            error_msg = str(e)
            if "No module named" in error_msg:
                logger.debug(f"Missing dependency for {module_path}: {error_msg}")
            else:
                logger.warning(f"Import error for {module_path}: {error_msg}")
            self.failed_modules.append((module_path, f"ImportError: {error_msg}"))
            return None

        except Exception as e:
            logger.warning(f"Unexpected error importing {module_path}: {e}")
            self.failed_modules.append((module_path, f"Unexpected error: {str(e)}"))
            return None

    def _analyze_object(
        self, obj: Any, module_path: str, create_tools: bool = True
    ) -> Optional[ComponentInfo]:
        """Analyze an object using available analyzers."""
        for analyzer in self.analyzers:
            try:
                if analyzer.can_analyze(obj):
                    try:
                        component_info = analyzer.analyze(obj, module_path)

                        if create_tools:
                            # Try to create tool instance
                            if not component_info.tool_instance:
                                try:
                                    component_info.tool_instance = analyzer.create_tool(
                                        component_info
                                    )
                                except Exception as e:
                                    logger.debug(f"Could not create tool: {e}")

                            # Try to create engine config
                            if not component_info.engine_config:
                                try:
                                    component_info.engine_config = (
                                        analyzer.create_engine_config(component_info)
                                    )
                                except Exception as e:
                                    logger.debug(f"Could not create engine config: {e}")

                        return component_info

                    except Exception as e:
                        logger.debug(f"Error analyzing {obj}: {e}")
                        continue

            except Exception as e:
                logger.debug(f"Error checking analyzer: {e}")
                continue

        return None

    def get_tools(self, components: List[ComponentInfo]) -> List[Any]:
        """Extract all created tools from components."""
        tools = []
        for comp in components:
            if comp.tool_instance:
                tools.append(comp.tool_instance)
        return tools

    def get_engine_configs(
        self, components: List[ComponentInfo]
    ) -> List[Dict[str, Any]]:
        """Extract all engine configs from components."""
        configs = []
        for comp in components:
            if comp.engine_config:
                configs.append(comp.engine_config)
        return configs

    def _find_project_root(self) -> str:
        """Find project root by looking for common markers."""
        current = Path.cwd()
        markers = ["pyproject.toml", ".git", "setup.py", "requirements.txt"]

        while current != current.parent:
            for marker in markers:
                if (current / marker).exists():
                    return str(current)
            current = current.parent

        return str(Path.cwd())
