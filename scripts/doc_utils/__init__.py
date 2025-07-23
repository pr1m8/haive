"""
Haive Documentation Utilities

A comprehensive toolkit for agent analysis, example discovery, and documentation generation.
This module provides utilities to systematically analyze and document the Haive agent ecosystem.

Key Components:
- AgentAnalyzer: Comprehensive agent type detection and analysis
- UniversalExampleRunner: Execute any agent example with streaming and visualization
- VisualizationManager: Universal agent visualization and workflow diagram generation
- DocumentationGenerator: Automated documentation creation for agents and examples

Usage:
    Command Line Interface:
        python -m scripts.doc_utils.cli analyze --report
        python -m scripts.doc_utils.cli run --discover
        python -m scripts.doc_utils.cli visualize --compare
        python -m scripts.doc_utils.cli docs --output ./documentation

    Programmatic API:
        from scripts.doc_utils import AgentAnalyzer, UniversalExampleRunner

        analyzer = AgentAnalyzer()
        agents = analyzer.discover_all_agents()

        runner = UniversalExampleRunner()
        result = await runner.run_example("path/to/example.py")
"""

from .agent_analyzer import AgentAnalyzer, AgentArchitecture, AgentInfo
from .doc_generator import DocumentationConfig, DocumentationGenerator
from .example_runner import ExecutionConfig, ExecutionResult, UniversalExampleRunner
from .visualization_utils import VisualizationConfig, VisualizationManager

__version__ = "1.0.0"

__all__ = [
    # Main classes
    "AgentAnalyzer",
    "UniversalExampleRunner",
    "DocumentationGenerator",
    "VisualizationManager",
    # Data classes and configs
    "AgentInfo",
    "AgentArchitecture",
    "ExecutionResult",
    "ExecutionConfig",
    "DocumentationConfig",
    "VisualizationConfig",
]
