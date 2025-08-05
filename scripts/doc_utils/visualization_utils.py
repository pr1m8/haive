#!/usr/bin/env python3
"""Visualization Utilities - Universal agent visualization and workflow diagram generation.

This module provides comprehensive visualization capabilities for all Haive agents,
regardless of architecture or type. It creates consistent visual outputs including
workflow diagrams, execution traces, and performance metrics.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from scripts.doc_utils.agent_analyzer import AgentArchitecture, AgentInfo

logger = logging.getLogger(__name__)


@dataclass
class VisualizationConfig:
    """Configuration for visualization generation."""

    output_format: str = "png"  # png, svg, html, mermaid
    include_metadata: bool = True
    show_execution_time: bool = True
    show_tool_calls: bool = True
    theme: str = "default"  # default, dark, minimal
    width: int = 800
    height: int = 600
    dpi: int = 300


@dataclass
class VisualizationResult:
    """Result of visualization generation."""

    success: bool
    output_path: Path | None = None
    error: str | None = None
    metadata: dict[str, Any] = None


class VisualizationManager:
    """Universal visualization manager for all agent types."""

    def __init__(self):
        """Initialize the visualization manager."""
        self.supported_formats = ["png", "svg", "html", "mermaid"]

    async def visualize_agent(
        self,
        agent_info: AgentInfo,
        output_path: Path | None = None,
        config: VisualizationConfig | None = None,
    ) -> VisualizationResult:
        """Generate visualization for any agent type.

        Args:
            agent_info: Agent information
            output_path: Output file path
            config: Visualization configuration

        Returns:
            Visualization result
        """
        if config is None:
            config = VisualizationConfig()

        if output_path is None:
            timestamp = int(time.time())
            output_path = Path(
                f"{agent_info.name.lower()}_viz_{timestamp}.{config.output_format}",
            )

        logger.info(f"Generating visualization for {agent_info.name}")

        try:
            # Choose visualization strategy based on agent architecture
            if agent_info.has_visualization:
                # Agent has native visualization support
                result = await self._use_native_visualization(
                    agent_info,
                    output_path,
                    config,
                )
            else:
                # Create visualization from analysis
                result = await self._create_synthetic_visualization(
                    agent_info,
                    output_path,
                    config,
                )

            return result

        except Exception as e:
            logger.exception(f"Failed to visualize agent {agent_info.name}: {e}")
            return VisualizationResult(success=False, error=str(e))

    async def _use_native_visualization(
        self,
        agent_info: AgentInfo,
        output_path: Path,
        config: VisualizationConfig,
    ) -> VisualizationResult:
        """Use the agent's native visualization method.

        Args:
            agent_info: Agent information
            output_path: Output file path
            config: Visualization configuration

        Returns:
            Visualization result
        """
        try:
            import importlib.util

            # Import the agent module
            spec = importlib.util.spec_from_file_location(
                agent_info.module_path,
                agent_info.file_path,
            )
            if not spec or not spec.loader:
                raise ImportError(f"Cannot load module {agent_info.module_path}")

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Get the agent class
            agent_class = getattr(module, agent_info.name)

            # Create agent instance with minimal config
            agent = await self._create_agent_instance(agent_info, agent_class)

            # Compile if necessary
            if hasattr(agent, "compile"):
                agent.compile()

            # Generate visualization
            if hasattr(agent, "visualize_graph"):
                agent.visualize_graph(str(output_path))
            elif hasattr(agent, "visualize"):
                agent.visualize(str(output_path))
            else:
                raise AttributeError("Agent has no visualization method")

            # Add metadata if requested
            metadata = {}
            if config.include_metadata:
                metadata = await self._extract_visualization_metadata(agent, agent_info)

            return VisualizationResult(
                success=True,
                output_path=output_path,
                metadata=metadata,
            )

        except Exception as e:
            logger.exception(f"Native visualization failed for {agent_info.name}: {e}")
            # Fallback to synthetic visualization
            return await self._create_synthetic_visualization(
                agent_info,
                output_path,
                config,
            )

    async def _create_synthetic_visualization(
        self,
        agent_info: AgentInfo,
        output_path: Path,
        config: VisualizationConfig,
    ) -> VisualizationResult:
        """Create visualization from agent analysis without instantiating.

        Args:
            agent_info: Agent information
            output_path: Output file path
            config: Visualization configuration

        Returns:
            Visualization result
        """
        try:
            # Generate different visualizations based on format
            if config.output_format == "mermaid":
                return await self._create_mermaid_diagram(
                    agent_info,
                    output_path,
                    config,
                )
            if config.output_format == "html":
                return await self._create_html_visualization(
                    agent_info,
                    output_path,
                    config,
                )
            if config.output_format in ["png", "svg"]:
                return await self._create_graph_visualization(
                    agent_info,
                    output_path,
                    config,
                )
            raise ValueError(f"Unsupported format: {config.output_format}")

        except Exception as e:
            logger.exception(
                f"Synthetic visualization failed for {agent_info.name}: {e}",
            )
            return VisualizationResult(success=False, error=str(e))

    async def _create_mermaid_diagram(
        self,
        agent_info: AgentInfo,
        output_path: Path,
        config: VisualizationConfig,
    ) -> VisualizationResult:
        """Create Mermaid diagram from agent info.

        Args:
            agent_info: Agent information
            output_path: Output file path
            config: Visualization configuration

        Returns:
            Visualization result
        """
        # Generate Mermaid syntax based on agent architecture
        mermaid_content = self._generate_mermaid_content(agent_info, config)

        # Write to file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(mermaid_content)

        return VisualizationResult(
            success=True,
            output_path=output_path,
            metadata={
                "format": "mermaid",
                "architecture": agent_info.architecture.value,
                "base_classes": agent_info.base_classes,
            },
        )

    def _generate_mermaid_content(
        self,
        agent_info: AgentInfo,
        config: VisualizationConfig,
    ) -> str:
        """Generate Mermaid diagram content.

        Args:
            agent_info: Agent information
            config: Visualization configuration

        Returns:
            Mermaid diagram as string
        """
        lines = ["graph TD", f"    Start([Start]) --> Agent[{agent_info.name}]"]

        # Add architecture-specific nodes
        if agent_info.architecture == AgentArchitecture.HAIVE_AGENTS_MIXIN:
            lines.extend(
                [
                    "    Agent --> Engine[AugLLM Engine]",
                    "    Engine --> Process[Process Input]",
                    "    Process --> Response[Generate Response]",
                ],
            )
        elif agent_info.architecture == AgentArchitecture.HAIVE_CORE_ENGINE:
            lines.extend(
                [
                    "    Agent --> Config[Agent Config]",
                    "    Config --> Execute[Execute]",
                    "    Execute --> Response[Response]",
                ],
            )
        elif agent_info.architecture == AgentArchitecture.HAIVE_GAMES:
            lines.extend(
                [
                    "    Agent --> GameState[Game State]",
                    "    GameState --> Action[Generate Action]",
                    "    Action --> Response[Game Response]",
                ],
            )
        else:
            lines.extend(
                [
                    "    Agent --> Processing[Processing]",
                    "    Processing --> Response[Response]",
                ],
            )

        # Add tools if supported
        if agent_info.tools_support:
            lines.append("    Processing --> Tools[Tool Execution]")
            lines.append("    Tools --> Processing")

        # Add end node
        lines.append("    Response --> End([End])")

        # Add styling based on theme
        if config.theme == "dark":
            lines.extend(
                [
                    "    classDef default fill:#2d3748,stroke:#4a5568,stroke-width:2px,color:#e2e8f0",
                    "    classDef agent fill:#4299e1,stroke:#3182ce,stroke-width:3px,color:#ffffff",
                ],
            )
            lines.append("    class Agent agent")

        return "\n".join(lines)

    async def _create_html_visualization(
        self,
        agent_info: AgentInfo,
        output_path: Path,
        config: VisualizationConfig,
    ) -> VisualizationResult:
        """Create interactive HTML visualization.

        Args:
            agent_info: Agent information
            output_path: Output file path
            config: Visualization configuration

        Returns:
            Visualization result
        """
        html_content = self._generate_html_content(agent_info, config)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return VisualizationResult(
            success=True,
            output_path=output_path,
            metadata={"format": "html", "interactive": True},
        )

    def _generate_html_content(
        self,
        agent_info: AgentInfo,
        config: VisualizationConfig,
    ) -> str:
        """Generate HTML visualization content.

        Args:
            agent_info: Agent information
            config: Visualization configuration

        Returns:
            HTML content as string
        """
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{agent_info.name} - Agent Visualization</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: {"#1a1a1a" if config.theme == "dark" else "#ffffff"};
            color: {"#e2e8f0" if config.theme == "dark" else "#333333"};
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            border-radius: 10px;
            background: {"#2d3748" if config.theme == "dark" else "#f7fafc"};
        }}
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .info-card {{
            padding: 20px;
            border-radius: 8px;
            background: {"#2d3748" if config.theme == "dark" else "#f7fafc"};
            border: {"1px solid #4a5568" if config.theme == "dark" else "1px solid #e2e8f0"};
        }}
        .info-card h3 {{
            margin-top: 0;
            color: {"#4299e1" if config.theme == "dark" else "#3182ce"};
        }}
        .tag {{
            display: inline-block;
            padding: 4px 8px;
            margin: 2px;
            border-radius: 4px;
            font-size: 0.8em;
            background: {"#4299e1" if config.theme == "dark" else "#e6f3ff"};
            color: {"#ffffff" if config.theme == "dark" else "#1a365d"};
        }}
        .workflow {{
            text-align: center;
            margin: 30px 0;
            padding: 20px;
            background: {"#2d3748" if config.theme == "dark" else "#f7fafc"};
            border-radius: 8px;
        }}
        .workflow-step {{
            display: inline-block;
            padding: 10px 20px;
            margin: 5px;
            border-radius: 20px;
            background: {"#4299e1" if config.theme == "dark" else "#3182ce"};
            color: #ffffff;
        }}
        .arrow {{
            display: inline-block;
            margin: 0 10px;
            font-size: 1.5em;
            color: {"#4a5568" if config.theme == "dark" else "#718096"};
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{agent_info.name}</h1>
        <p><strong>Architecture:</strong> {agent_info.architecture.value}</p>
        <p><strong>File:</strong> {agent_info.file_path.name}</p>
    </div>

    <div class="info-grid">
        <div class="info-card">
            <h3>Base Classes</h3>
            {"".join(f'<span class="tag">{base}</span>' for base in agent_info.base_classes)}
        </div>

        <div class="info-card">
            <h3>Capabilities</h3>
            <div>
                <span class="tag">{"✓" if agent_info.has_visualization else "✗"} Visualization</span>
                <span class="tag">{"✓" if agent_info.tools_support else "✗"} Tools</span>
                <span class="tag">{"✓" if agent_info.streaming_support else "✗"} Streaming</span>
            </div>
        </div>

        <div class="info-card">
            <h3>Execution</h3>
            <span class="tag">{agent_info.execution_pattern.title()}</span>
            <span class="tag">{agent_info.config_pattern}</span>
        </div>

        <div class="info-card">
            <h3>Examples</h3>
            <div>
                {f"<p>{len(agent_info.example_files)} example files found</p>" if agent_info.example_files else "<p>No example files found</p>"}
            </div>
        </div>
    </div>

    <div class="workflow">
        <h3>Typical Workflow</h3>
        <div>
            <span class="workflow-step">Input</span>
            <span class="arrow">→</span>
            <span class="workflow-step">Process</span>
            <span class="arrow">→</span>
            <span class="workflow-step">Generate</span>
            <span class="arrow">→</span>
            <span class="workflow-step">Output</span>
        </div>
    </div>

    <div class="info-card">
        <h3>Module Information</h3>
        <p><strong>Module Path:</strong> {agent_info.module_path}</p>
        <p><strong>File Path:</strong> {agent_info.file_path}</p>
        {f"<p><strong>Method Count:</strong> {agent_info.metadata.get('method_count', 'Unknown')}</p>" if agent_info.metadata else ""}
    </div>
</body>
</html>
        """

    async def _create_graph_visualization(
        self,
        agent_info: AgentInfo,
        output_path: Path,
        config: VisualizationConfig,
    ) -> VisualizationResult:
        """Create graph visualization using graphviz or similar.

        Args:
            agent_info: Agent information
            output_path: Output file path
            config: Visualization configuration

        Returns:
            Visualization result
        """
        try:
            # Try to use graphviz if available
            try:
                pass

                return await self._create_graphviz_visualization(
                    agent_info,
                    output_path,
                    config,
                )
            except ImportError:
                pass

            # Try matplotlib as fallback
            try:
                pass

                return await self._create_matplotlib_visualization(
                    agent_info,
                    output_path,
                    config,
                )
            except ImportError:
                pass

            # If no graphical libraries available, create text-based diagram
            return await self._create_text_visualization(
                agent_info,
                output_path,
                config,
            )

        except Exception as e:
            logger.exception(f"Graph visualization failed: {e}")
            return VisualizationResult(success=False, error=str(e))

    async def _create_matplotlib_visualization(
        self,
        agent_info: AgentInfo,
        output_path: Path,
        config: VisualizationConfig,
    ) -> VisualizationResult:
        """Create visualization using matplotlib.

        Args:
            agent_info: Agent information
            output_path: Output file path
            config: Visualization configuration

        Returns:
            Visualization result
        """
        import matplotlib.pyplot as plt
        from matplotlib import patches

        fig, ax = plt.subplots(1, 1, figsize=(config.width / 100, config.height / 100))

        # Set theme
        if config.theme == "dark":
            fig.patch.set_facecolor("#1a1a1a")
            ax.set_facecolor("#2d3748")
            text_color = "#e2e8f0"
        else:
            fig.patch.set_facecolor("white")
            ax.set_facecolor("white")
            text_color = "#333333"

        # Draw workflow boxes
        boxes = [
            ("Start", 0.1, 0.8, 0.15, 0.1),
            (agent_info.name, 0.35, 0.6, 0.3, 0.2),
            ("Process", 0.35, 0.3, 0.3, 0.1),
            ("Output", 0.35, 0.1, 0.3, 0.1),
        ]

        for label, x, y, width, height in boxes:
            rect = patches.Rectangle(
                (x, y),
                width,
                height,
                linewidth=2,
                edgecolor="#4299e1",
                facecolor="#e6f3ff",
            )
            ax.add_patch(rect)
            ax.text(
                x + width / 2,
                y + height / 2,
                label,
                ha="center",
                va="center",
                fontsize=10,
                color=text_color,
            )

        # Draw arrows
        arrows = [
            (0.175, 0.8, 0.35, 0.7),  # Start -> Agent
            (0.5, 0.6, 0.5, 0.4),  # Agent -> Process
            (0.5, 0.3, 0.5, 0.2),  # Process -> Output
        ]

        for x1, y1, x2, y2 in arrows:
            ax.annotate(
                "",
                xy=(x2, y2),
                xytext=(x1, y1),
                arrowprops={"arrowstyle": "->", "color": "#4299e1", "lw": 2},
            )

        # Add title and metadata
        ax.set_title(
            f"{agent_info.name} Workflow",
            fontsize=16,
            color=text_color,
            pad=20,
        )

        if config.include_metadata:
            metadata_text = f"""Architecture: {agent_info.architecture.value}
Execution: {agent_info.execution_pattern}
Tools: {"Yes" if agent_info.tools_support else "No"}
Visualization: {"Yes" if agent_info.has_visualization else "No"}"""

            ax.text(
                0.02,
                0.02,
                metadata_text,
                transform=ax.transAxes,
                fontsize=8,
                color=text_color,
                verticalalignment="bottom",
                bbox={
                    "boxstyle": "round,pad=0.3",
                    "facecolor": "#f7fafc",
                    "alpha": 0.8,
                },
            )

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

        # Save the figure
        plt.tight_layout()
        plt.savefig(
            output_path,
            dpi=config.dpi,
            bbox_inches="tight",
            facecolor=fig.get_facecolor(),
            edgecolor="none",
        )
        plt.close()

        return VisualizationResult(
            success=True,
            output_path=output_path,
            metadata={"format": config.output_format, "created_with": "matplotlib"},
        )

    async def _create_text_visualization(
        self,
        agent_info: AgentInfo,
        output_path: Path,
        config: VisualizationConfig,
    ) -> VisualizationResult:
        """Create text-based visualization when no graphical libraries are
        available.

        Args:
            agent_info: Agent information
            output_path: Output file path
            config: Visualization configuration

        Returns:
            Visualization result
        """
        text_content = f"""
{agent_info.name} - Agent Visualization
{"=" * (len(agent_info.name) + 25)}

Architecture: {agent_info.architecture.value}
File: {agent_info.file_path}
Module: {agent_info.module_path}

Base Classes:
{chr(10).join(f"  - {base}" for base in agent_info.base_classes)}

Capabilities:
  - Visualization: {"Yes" if agent_info.has_visualization else "No"}
  - Tools Support: {"Yes" if agent_info.tools_support else "No"}
  - Streaming: {"Yes" if agent_info.streaming_support else "No"}
  - Execution: {agent_info.execution_pattern}

Workflow:
┌─────────┐    ┌──────────────────────┐    ┌─────────┐    ┌────────┐
│  Start  │ -> │  {agent_info.name:^20} │ -> │ Process │ -> │ Output │
└─────────┘    └──────────────────────┘    └─────────┘    └────────┘

Examples: {len(agent_info.example_files)} files found
"""

        # Write as .txt file regardless of requested format
        txt_path = output_path.with_suffix(".txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text_content.strip())

        return VisualizationResult(
            success=True,
            output_path=txt_path,
            metadata={"format": "text", "fallback": True},
        )

    async def _create_agent_instance(
        self,
        agent_info: AgentInfo,
        agent_class: type,
    ) -> Any:
        """Create an agent instance with minimal configuration.

        Args:
            agent_info: Agent information
            agent_class: Agent class

        Returns:
            Agent instance
        """
        try:
            if agent_info.architecture == AgentArchitecture.HAIVE_AGENTS_MIXIN:
                # Try with AugLLMConfig
                from haive.core.engine.aug_llm import AugLLMConfig

                config = AugLLMConfig(temperature=0.1)  # Low temp for consistency
                return agent_class(name=f"viz_{agent_info.name.lower()}", engine=config)

            if agent_info.architecture == AgentArchitecture.HAIVE_GAMES:
                # Game agents often need less configuration
                return agent_class(name=f"viz_{agent_info.name.lower()}")

            # Try with default constructor
            return agent_class()

        except Exception as e:
            logger.warning(f"Failed to create instance with default config: {e}")
            # Try with just name
            return agent_class(name=f"viz_{agent_info.name.lower()}")

    async def _extract_visualization_metadata(
        self,
        agent: Any,
        agent_info: AgentInfo,
    ) -> dict[str, Any]:
        """Extract metadata from agent instance.

        Args:
            agent: Agent instance
            agent_info: Agent information

        Returns:
            Metadata dictionary
        """
        metadata = {
            "agent_name": agent_info.name,
            "has_graph": hasattr(agent, "graph"),
            "compiled": hasattr(agent, "graph")
            and getattr(agent, "graph", None) is not None,
        }

        # Try to extract additional info
        try:
            if hasattr(agent, "engine"):
                metadata["engine_type"] = type(agent.engine).__name__
                if hasattr(agent.engine, "model"):
                    metadata["model"] = agent.engine.model
                if hasattr(agent.engine, "temperature"):
                    metadata["temperature"] = agent.engine.temperature
        except BaseException:
            pass

        return metadata

    async def create_comparison_visualization(
        self,
        agents_info: list[AgentInfo],
        output_path: Path,
        config: VisualizationConfig | None = None,
    ) -> VisualizationResult:
        """Create comparison visualization for multiple agents.

        Args:
            agents_info: List of agent information
            output_path: Output file path
            config: Visualization configuration

        Returns:
            Visualization result
        """
        if config is None:
            config = VisualizationConfig()

        try:
            if config.output_format == "html":
                return await self._create_comparison_html(
                    agents_info,
                    output_path,
                    config,
                )
            return await self._create_comparison_table(agents_info, output_path, config)

        except Exception as e:
            logger.exception(f"Comparison visualization failed: {e}")
            return VisualizationResult(success=False, error=str(e))

    async def _create_comparison_html(
        self,
        agents_info: list[AgentInfo],
        output_path: Path,
        config: VisualizationConfig,
    ) -> VisualizationResult:
        """Create HTML comparison table."""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agent Comparison</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            background: {"#1a1a1a" if config.theme == "dark" else "#ffffff"};
            color: {"#e2e8f0" if config.theme == "dark" else "#333333"};
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: {"#2d3748" if config.theme == "dark" else "#ffffff"};
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border: {"1px solid #4a5568" if config.theme == "dark" else "1px solid #ddd"};
        }}
        th {{
            background: {"#4a5568" if config.theme == "dark" else "#f2f2f2"};
            font-weight: bold;
        }}
        .yes {{ color: #48bb78; }}
        .no {{ color: #f56565; }}
        .architecture {{
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            color: white;
        }}
        .haive-agents {{ background: #4299e1; }}
        .haive-core {{ background: #9f7aea; }}
        .haive-games {{ background: #38b2ac; }}
        .unknown {{ background: #a0aec0; }}
    </style>
</head>
<body>
    <h1>Agent Comparison</h1>
    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Architecture</th>
                <th>Visualization</th>
                <th>Tools</th>
                <th>Streaming</th>
                <th>Execution</th>
                <th>Examples</th>
            </tr>
        </thead>
        <tbody>
"""

        for agent in agents_info:
            arch_class = agent.architecture.value.replace(".", "-").replace("_", "-")
            html_content += f"""
            <tr>
                <td><strong>{agent.name}</strong></td>
                <td><span class="architecture {arch_class}">{agent.architecture.value}</span></td>
                <td class="{"yes" if agent.has_visualization else "no"}">
                    {"✓ Yes" if agent.has_visualization else "✗ No"}
                </td>
                <td class="{"yes" if agent.tools_support else "no"}">
                    {"✓ Yes" if agent.tools_support else "✗ No"}
                </td>
                <td class="{"yes" if agent.streaming_support else "no"}">
                    {"✓ Yes" if agent.streaming_support else "✗ No"}
                </td>
                <td>{agent.execution_pattern.title()}</td>
                <td>{len(agent.example_files)}</td>
            </tr>
"""

        html_content += """
        </tbody>
    </table>
</body>
</html>
        """

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return VisualizationResult(
            success=True,
            output_path=output_path,
            metadata={
                "format": "html",
                "agents_count": len(agents_info),
                "comparison": True,
            },
        )
