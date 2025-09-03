#!/usr/bin/env python3
"""Documentation Generator - Automated documentation creation for agents and examples.

This module provides comprehensive documentation generation capabilities,
creating consistent documentation across all Haive agent types and examples.
It integrates with the analyzer and visualization tools to create complete docs.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from scripts.doc_utils.agent_analyzer import AgentAnalyzer
from scripts.doc_utils.agent_analyzer import AgentArchitecture
from scripts.doc_utils.agent_analyzer import AgentInfo
from scripts.doc_utils.example_runner import UniversalExampleRunner
from scripts.doc_utils.visualization_utils import VisualizationConfig
from scripts.doc_utils.visualization_utils import VisualizationManager

logger = logging.getLogger(__name__)


@dataclass
class DocumentationConfig:
    """Configuration for documentation generation."""

    include_examples: bool = True
    include_visualizations: bool = True
    include_code_snippets: bool = True
    include_api_docs: bool = True
    include_performance_metrics: bool = False
    output_format: str = 'markdown'  # markdown, rst, html
    template_style: str = 'comprehensive'  # minimal, standard, comprehensive
    generate_index: bool = True
    cross_reference: bool = True


@dataclass
class DocumentationResult:
    """Result of documentation generation."""

    success: bool
    output_files: list[Path] = None
    index_file: Path | None = None
    error: str | None = None
    metadata: dict[str, Any] = None


class DocumentationGenerator:
    """Automated documentation generator for agents and examples."""

    def __init__(self, project_root: Path | None = None):
        """Initialize the documentation generator.

        Args:
            project_root: Root directory of the Haive project
        """
        self.analyzer = AgentAnalyzer(project_root)
        self.example_runner = UniversalExampleRunner(project_root)
        self.viz_manager = VisualizationManager()
        self.project_root = self.analyzer.project_root

    async def generate_agent_documentation(
        self,
        agent_info: AgentInfo,
        output_dir: Path,
        config: DocumentationConfig | None = None,
    ) -> DocumentationResult:
        """Generate comprehensive documentation for a single agent.

        Args:
            agent_info: Agent information
            output_dir: Output directory for documentation
            config: Documentation configuration

        Returns:
            Documentation generation result
        """
        if config is None:
            config = DocumentationConfig()

        output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Generating documentation for {agent_info.name}")

        try:
            output_files = []

            # Generate main agent documentation
            main_doc_path = (
                output_dir
                / f"{agent_info.name.lower()}.{self._get_file_extension(config.output_format)}"
            )
            doc_content = await self._generate_agent_doc_content(agent_info, config)

            with open(main_doc_path, 'w', encoding='utf-8') as f:
                f.write(doc_content)
            output_files.append(main_doc_path)

            # Generate visualization if requested
            viz_path = None
            if config.include_visualizations:
                viz_path = output_dir / f"{agent_info.name.lower()}_workflow.png"
                viz_result = await self.viz_manager.visualize_agent(
                    agent_info,
                    viz_path,
                    VisualizationConfig(),
                )
                if viz_result.success:
                    output_files.append(viz_path)

            # Generate example documentation if requested
            if config.include_examples and agent_info.example_files:
                examples_doc_path = (
                    output_dir
                    / f"{agent_info.name.lower()}_examples.{self._get_file_extension(config.output_format)}"
                )
                examples_content = await self._generate_examples_doc_content(
                    agent_info,
                    config,
                )

                with open(examples_doc_path, 'w', encoding='utf-8') as f:
                    f.write(examples_content)
                output_files.append(examples_doc_path)

            # Generate API documentation if requested
            if config.include_api_docs:
                api_doc_path = (
                    output_dir
                    / f"{agent_info.name.lower()}_api.{self._get_file_extension(config.output_format)}"
                )
                api_content = await self._generate_api_doc_content(agent_info, config)

                with open(api_doc_path, 'w', encoding='utf-8') as f:
                    f.write(api_content)
                output_files.append(api_doc_path)

            return DocumentationResult(
                success=True,
                output_files=output_files,
                metadata={
                    'agent_name': agent_info.name,
                    'architecture': agent_info.architecture.value,
                    'generated_at': datetime.now().isoformat(),
                    'visualization_included': viz_path is not None,
                },
            )

        except Exception as e:
            logger.exception(
                f"Failed to generate documentation for {agent_info.name}: {e}",
            )
            return DocumentationResult(success=False, error=str(e))

    async def generate_project_documentation(
        self,
        output_dir: Path,
        config: DocumentationConfig | None = None,
    ) -> DocumentationResult:
        """Generate documentation for the entire project.

        Args:
            output_dir: Output directory for documentation
            config: Documentation configuration

        Returns:
            Documentation generation result
        """
        if config is None:
            config = DocumentationConfig()

        output_dir.mkdir(parents=True, exist_ok=True)
        logger.info('Generating project-wide documentation')

        try:
            output_files = []

            # Discover all agents
            agents = self.analyzer.discover_all_agents()
            logger.info(f"Found {len(agents)} agents to document")

            # Generate documentation for each agent
            for agent in agents:
                agent_dir = output_dir / agent.name.lower()
                result = await self.generate_agent_documentation(
                    agent,
                    agent_dir,
                    config,
                )
                if result.success:
                    output_files.extend(result.output_files)

            # Generate project index
            index_file = None
            if config.generate_index:
                index_file = output_dir / \
                    f"index.{self._get_file_extension(config.output_format)}"
                index_content = await self._generate_project_index_content(
                    agents,
                    config,
                )

                with open(index_file, 'w', encoding='utf-8') as f:
                    f.write(index_content)
                output_files.append(index_file)

            # Generate comparison documentation
            comparison_file = (
                output_dir /
                f"agent_comparison.{self._get_file_extension(config.output_format)}"
            )
            comparison_content = await self._generate_comparison_content(agents, config)

            with open(comparison_file, 'w', encoding='utf-8') as f:
                f.write(comparison_content)
            output_files.append(comparison_file)

            # Generate architecture overview
            arch_file = (
                output_dir
                / f"architecture_overview.{self._get_file_extension(config.output_format)}"
            )
            arch_content = await self._generate_architecture_overview(agents, config)

            with open(arch_file, 'w', encoding='utf-8') as f:
                f.write(arch_content)
            output_files.append(arch_file)

            return DocumentationResult(
                success=True,
                output_files=output_files,
                index_file=index_file,
                metadata={
                    'total_agents': len(agents),
                    'generated_at': datetime.now().isoformat(),
                    'format': config.output_format,
                },
            )

        except Exception as e:
            logger.exception(f"Failed to generate project documentation: {e}")
            return DocumentationResult(success=False, error=str(e))

    def _get_file_extension(self, format_type: str) -> str:
        """Get file extension for format type."""
        extensions = {'markdown': 'md', 'rst': 'rst', 'html': 'html'}
        return extensions.get(format_type, 'md')

    async def _generate_agent_doc_content(
        self,
        agent_info: AgentInfo,
        config: DocumentationConfig,
    ) -> str:
        """Generate documentation content for a single agent."""
        if config.output_format == 'markdown':
            return await self._generate_markdown_agent_doc(agent_info, config)
        if config.output_format == 'rst':
            return await self._generate_rst_agent_doc(agent_info, config)
        if config.output_format == 'html':
            return await self._generate_html_agent_doc(agent_info, config)
        return await self._generate_markdown_agent_doc(agent_info, config)

    async def _generate_markdown_agent_doc(
        self,
        agent_info: AgentInfo,
        config: DocumentationConfig,
    ) -> str:
        """Generate Markdown documentation for an agent."""
        lines = [
            f"# {agent_info.name}",
            '',
            f"**Architecture**: {agent_info.architecture.value}",
            f"**File**: `{agent_info.file_path}`",
            f"**Module**: `{agent_info.module_path}`",
            '',
            '## Overview',
            '',
        ]

        # Add docstring if available
        if agent_info.metadata and 'docstring' in agent_info.metadata:
            lines.extend([agent_info.metadata['docstring'], ''])
        else:
            lines.extend(
                [
                    f"The {agent_info.name} is a {agent_info.architecture.value} agent that provides",
                    'specialized functionality within the Haive framework.',
                    '',
                ],
            )

        # Add inheritance information
        if agent_info.base_classes:
            lines.extend(
                [
                    '## Inheritance',
                    '',
                    'This agent inherits from the following base classes:',
                    '',
                ],
            )
            for base_class in agent_info.base_classes:
                lines.append(f"- `{base_class}`")
            lines.append('')

        # Add capabilities
        lines.extend(
            [
                '## Capabilities',
                '',
                f"- **Visualization**: {'✅ Supported' if agent_info.has_visualization else '❌ Not supported'}",
                f"- **Tools**: {'✅ Supported' if agent_info.tools_support else '❌ Not supported'}",
                f"- **Streaming**: {'✅ Supported' if agent_info.streaming_support else '❌ Not supported'}",
                f"- **Execution Pattern**: {agent_info.execution_pattern.title()}",
                f"- **Configuration**: {agent_info.config_pattern}",
                '',
            ],
        )

        # Add usage examples if code snippets are requested
        if config.include_code_snippets:
            lines.extend(
                [
                    '## Basic Usage',
                    '',
                    '```python',
                    self._generate_basic_usage_example(agent_info),
                    '```',
                    '',
                ],
            )

        # Add examples section
        if config.include_examples and agent_info.example_files:
            lines.extend(
                [
                    '## Examples',
                    '',
                    f"This agent has {len(agent_info.example_files)} example file(s):",
                    '',
                ],
            )
            for example_file in agent_info.example_files:
                lines.append(f"- [`{example_file.name}`]({example_file})")
            lines.append('')

        # Add visualization if included
        if config.include_visualizations and agent_info.has_visualization:
            lines.extend(
                [
                    '## Workflow Visualization',
                    '',
                    f"![{agent_info.name} Workflow](./{agent_info.name.lower()}_workflow.png)",
                    '',
                ],
            )

        # Add technical details
        if config.template_style == 'comprehensive':
            lines.extend(
                [
                    '## Technical Details',
                    '',
                    f"- **Method Count**: {agent_info.metadata.get('method_count', 'Unknown') if agent_info.metadata else 'Unknown'}",
                    f"- **File Size**: {self._get_file_size_info(agent_info.file_path)}",
                    f"- **Last Modified**: {self._get_file_modification_time(agent_info.file_path)}",
                    '',
                ],
            )

        # Add related agents if cross-referencing is enabled
        if config.cross_reference:
            related_agents = await self._find_related_agents(agent_info)
            if related_agents:
                lines.extend(
                    [
                        '## Related Agents',
                        '',
                        'Agents with similar architecture or functionality:',
                        '',
                    ],
                )
                for related in related_agents:
                    lines.append(f"- [{related.name}](./{related.name.lower()}.md)")
                lines.append('')

        return '\n'.join(lines)

    def _generate_basic_usage_example(self, agent_info: AgentInfo) -> str:
        """Generate basic usage example based on agent architecture."""
        if agent_info.architecture == AgentArchitecture.HAIVE_AGENTS_MIXIN:
            return f"""from {agent_info.module_path} import {agent_info.name}
from haive.core.engine.aug_llm import AugLLMConfig

# Create agent configuration
config = AugLLMConfig(
    temperature=0.7,
    max_tokens=500
)

# Create agent
agent = {agent_info.name}(
    name="my_agent",
    engine=config
)

# Use the agent
response = agent.run("Your input here")
print(response)"""

        if agent_info.architecture == AgentArchitecture.HAIVE_GAMES:
            return f"""from {agent_info.module_path} import {agent_info.name}

# Create game agent
agent = {agent_info.name}(name="player")

# Use in game context
action = agent.get_action(game_state)
print(f"Agent action: {{action}}")"""

        return f"""from {agent_info.module_path} import {agent_info.name}

# Create agent
agent = {agent_info.name}()

# Use the agent
result = agent.process("Your input")
print(result)"""

    async def _generate_examples_doc_content(
        self,
        agent_info: AgentInfo,
        config: DocumentationConfig,
    ) -> str:
        """Generate documentation content for agent examples."""
        lines = [
            f"# {agent_info.name} Examples",
            '',
            f"This document provides comprehensive examples for using the {agent_info.name}.",
            '',
        ]

        for example_file in agent_info.example_files:
            lines.extend(
                [
                    f"## {example_file.stem.replace('_', ' ').title()}",
                    '',
                    f"**File**: `{example_file}`",
                    '',
                ],
            )

            # Try to extract example content
            try:
                with open(example_file, encoding='utf-8') as f:
                    content = f.read()

                # Extract docstring if available
                if '"""' in content:
                    docstring_start = content.find('"""') + 3
                    docstring_end = content.find('"""', docstring_start)
                    if docstring_end > docstring_start:
                        docstring = content[docstring_start:docstring_end].strip()
                        lines.extend([docstring, ''])

                # Add code snippet if requested
                if config.include_code_snippets:
                    lines.extend(['```python', content, '```', ''])

            except Exception as e:
                lines.extend([f"*Error reading example file: {e}*", ''])

        return '\n'.join(lines)

    async def _generate_api_doc_content(
        self,
        agent_info: AgentInfo,
        config: DocumentationConfig,
    ) -> str:
        """Generate API documentation content."""
        lines = [
            f"# {agent_info.name} API Reference",
            '',
            f"Comprehensive API documentation for the {agent_info.name} class.",
            '',
        ]

        try:
            # Try to import and inspect the agent class
            import importlib.util

            spec = importlib.util.spec_from_file_location(
                agent_info.module_path,
                agent_info.file_path,
            )
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                agent_class = getattr(module, agent_info.name, None)
                if agent_class:
                    # Generate class documentation
                    lines.extend(self._generate_class_api_doc(agent_class))

        except Exception as e:
            lines.extend(
                [
                    f"*Error generating API documentation: {e}*",
                    '',
                    'Please refer to the source code for detailed API information.',
                    '',
                ],
            )

        return '\n'.join(lines)

    def _generate_class_api_doc(self, agent_class: type) -> list[str]:
        """Generate API documentation for a class."""
        lines = [f"## Class: {agent_class.__name__}", '']

        # Add class docstring
        if agent_class.__doc__:
            lines.extend([agent_class.__doc__.strip(), ''])

        # Add methods
        methods = inspect.getmembers(agent_class, predicate=inspect.isfunction)
        if methods:
            lines.extend(['### Methods', ''])

            for method_name, method in methods:
                if not method_name.startswith('_'):  # Skip private methods
                    lines.extend([f"#### `{method_name}`", ''])

                    # Add method signature
                    try:
                        sig = inspect.signature(method)
                        lines.extend(['```python', f"{method_name}{sig}", '```', ''])
                    except BaseException:
                        pass

                    # Add method docstring
                    if method.__doc__:
                        lines.extend([method.__doc__.strip(), ''])

        return lines

    async def _generate_project_index_content(
        self,
        agents: list[AgentInfo],
        config: DocumentationConfig,
    ) -> str:
        """Generate project index documentation."""
        lines = [
            '# Haive Agent Documentation Index',
            '',
            f"This is the comprehensive documentation index for all {
                len(agents)
            } agents in the Haive framework.",
            f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.",
            '',
            '## Quick Navigation',
            '',
            '- [Agent Comparison](./agent_comparison.md)',
            '- [Architecture Overview](./architecture_overview.md)',
            '',
        ]

        # Group by architecture
        arch_groups = {}
        for agent in agents:
            arch = agent.architecture
            if arch not in arch_groups:
                arch_groups[arch] = []
            arch_groups[arch].append(agent)

        # Generate sections for each architecture
        for arch, arch_agents in arch_groups.items():
            lines.extend([f"## {arch.value} Agents ({len(arch_agents)} agents)", ''])

            # Sort agents by name
            arch_agents.sort(key=lambda x: x.name)

            for agent in arch_agents:
                capabilities = []
                if agent.has_visualization:
                    capabilities.append('Visualization')
                if agent.tools_support:
                    capabilities.append('Tools')
                if agent.streaming_support:
                    capabilities.append('Streaming')

                cap_str = f" ({', '.join(capabilities)})" if capabilities else ''

                lines.extend(
                    [
                        f"- **[{agent.name}](./{agent.name.lower()}/{agent.name.lower()}.md)**{cap_str}",
                        f"  - Examples: {len(agent.example_files)}",
                        f"  - Execution: {agent.execution_pattern}",
                    ],
                )

            lines.append('')

        return '\n'.join(lines)

    async def _generate_comparison_content(
        self,
        agents: list[AgentInfo],
        config: DocumentationConfig,
    ) -> str:
        """Generate agent comparison documentation."""
        lines = [
            '# Agent Comparison',
            '',
            'Comprehensive comparison of all Haive agents across different dimensions.',
            '',
            '## Summary Statistics',
            '',
        ]

        # Calculate statistics
        total = len(agents)
        with_viz = sum(1 for a in agents if a.has_visualization)
        with_tools = sum(1 for a in agents if a.tools_support)
        with_streaming = sum(1 for a in agents if a.streaming_support)

        lines.extend(
            [
                f"- **Total Agents**: {total}",
                f"- **With Visualization**: {with_viz} ({with_viz / total * 100:.1f}%)",
                f"- **With Tools Support**: {with_tools} ({with_tools / total * 100:.1f}%)",
                f"- **With Streaming**: {with_streaming} ({with_streaming / total * 100:.1f}%)",
                '',
            ],
        )

        # Architecture breakdown
        arch_counts = {}
        for agent in agents:
            arch_counts[agent.architecture] = arch_counts.get(agent.architecture, 0) + 1

        lines.extend(['## Architecture Distribution', ''])

        for arch, count in arch_counts.items():
            lines.append(
                f"- **{arch.value}**: {count} agents ({count / total * 100:.1f}%)")

        lines.extend(
            [
                '',
                '## Detailed Comparison',
                '',
                '| Agent | Architecture | Viz | Tools | Streaming | Execution | Examples |',
                '|-------|-------------|-----|-------|-----------|-----------|----------|',
            ],
        )

        # Sort agents by name for consistent ordering
        sorted_agents = sorted(agents, key=lambda x: x.name)

        for agent in sorted_agents:
            viz_icon = '✅' if agent.has_visualization else '❌'
            tools_icon = '✅' if agent.tools_support else '❌'
            streaming_icon = '✅' if agent.streaming_support else '❌'

            arch_short = agent.architecture.value.split('.')[-1]

            lines.append(
                f"| [{agent.name}](./{agent.name.lower()}/{agent.name.lower()}.md) "
                f"| {arch_short} "
                f"| {viz_icon} "
                f"| {tools_icon} "
                f"| {streaming_icon} "
                f"| {agent.execution_pattern} "
                f"| {len(agent.example_files)} |",
            )

        return '\n'.join(lines)

    async def _generate_architecture_overview(
        self,
        agents: list[AgentInfo],
        config: DocumentationConfig,
    ) -> str:
        """Generate architecture overview documentation."""
        lines = [
            '# Architecture Overview',
            '',
            'This document provides an overview of the different agent architectures in Haive.',
            '',
        ]

        # Analyze inheritance patterns
        inheritance_map = self.analyzer.analyze_inheritance_patterns()

        lines.extend(
            [
                '## Inheritance Patterns',
                '',
                'The most common base classes across all agents:',
                '',
            ],
        )

        sorted_bases = sorted(
            inheritance_map.items(),
            key=lambda x: len(x[1]),
            reverse=True,
        )
        for base_class, derived in sorted_bases[:10]:
            lines.append(f"- **{base_class}**: {len(derived)} agents")

        lines.extend(['', '## Architecture Details', ''])

        # Group by architecture and provide detailed info
        arch_groups = {}
        for agent in agents:
            arch = agent.architecture
            if arch not in arch_groups:
                arch_groups[arch] = []
            arch_groups[arch].append(agent)

        for arch, arch_agents in arch_groups.items():
            lines.extend(
                [f"### {arch.value}", '', f"**Agent Count**: {len(arch_agents)}", ''],
            )

            # Architecture-specific characteristics
            if arch == AgentArchitecture.HAIVE_AGENTS_MIXIN:
                lines.extend(
                    [
                        '**Characteristics**:',
                        '- Mixin-based architecture with ExecutionMixin, StateMixin, PersistenceMixin',
                        '- Uses AugLLMConfig for engine configuration',
                        '- Built-in visualization support through visualize_graph() method',
                        '- Supports both sync and async execution patterns',
                        '',
                    ],
                )
            elif arch == AgentArchitecture.HAIVE_CORE_ENGINE:
                lines.extend(
                    [
                        '**Characteristics**:',
                        '- Protocol-based architecture with registry pattern',
                        '- Flexible configuration system',
                        '- Focus on composability and modularity',
                        '',
                    ],
                )
            elif arch == AgentArchitecture.HAIVE_GAMES:
                lines.extend(
                    [
                        '**Characteristics**:',
                        '- Game-specific agent implementations',
                        '- Inherits from game base classes',
                        '- Optimized for game state processing',
                        '',
                    ],
                )

            # Common patterns in this architecture
            config_patterns = {agent.config_pattern for agent in arch_agents}
            exec_patterns = {agent.execution_pattern for agent in arch_agents}

            lines.extend(
                [
                    f"**Configuration Patterns**: {', '.join(config_patterns)}",
                    f"**Execution Patterns**: {', '.join(exec_patterns)}",
                    '',
                ],
            )

        return '\n'.join(lines)

    async def _find_related_agents(self, agent_info: AgentInfo) -> list[AgentInfo]:
        """Find agents related to the given agent."""
        all_agents = self.analyzer.discover_all_agents()
        related = []

        for other_agent in all_agents:
            if other_agent.name == agent_info.name:
                continue

            # Check for relationship criteria
            relationship_score = 0

            # Same architecture
            if other_agent.architecture == agent_info.architecture:
                relationship_score += 3

            # Shared base classes
            shared_bases = set(agent_info.base_classes) & set(other_agent.base_classes)
            relationship_score += len(shared_bases) * 2

            # Similar capabilities
            if other_agent.has_visualization == agent_info.has_visualization:
                relationship_score += 1
            if other_agent.tools_support == agent_info.tools_support:
                relationship_score += 1
            if other_agent.execution_pattern == agent_info.execution_pattern:
                relationship_score += 1

            # Add to related if score is high enough
            if relationship_score >= 4:
                related.append(other_agent)

        # Sort by relationship strength and return top 5
        related.sort(
            key=lambda x: len(set(agent_info.base_classes) & set(x.base_classes)),
            reverse=True,
        )
        return related[:5]

    def _get_file_size_info(self, file_path: Path) -> str:
        """Get human-readable file size information."""
        try:
            size = file_path.stat().st_size
            for unit in ['B', 'KB', 'MB']:
                if size < 1024:
                    return f"{size:.1f} {unit}"
                size /= 1024
            return f"{size:.1f} GB"
        except BaseException:
            return 'Unknown'

    def _get_file_modification_time(self, file_path: Path) -> str:
        """Get file modification time."""
        try:
            mtime = file_path.stat().st_mtime
            return datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        except BaseException:
            return 'Unknown'
