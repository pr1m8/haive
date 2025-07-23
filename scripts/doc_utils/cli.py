#!/usr/bin/env python3
"""Documentation Utilities CLI - Command-line interface for all documentation utilities.

This module provides a unified command-line interface to access all documentation
utilities: agent analysis, example running, visualization, and documentation generation.
"""

import argparse
import asyncio
import logging
import sys
from pathlib import Path
from typing import List, Optional

from .agent_analyzer import AgentAnalyzer
from .doc_generator import DocumentationConfig, DocumentationGenerator
from .example_runner import ExecutionConfig, UniversalExampleRunner
from .visualization_utils import VisualizationConfig, VisualizationManager

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def analyze_agents(args):
    """Analyze agents command."""
    analyzer = AgentAnalyzer(args.project_root)

    if args.agent_name:
        # Analyze specific agent
        agent = analyzer.get_agent_by_name(args.agent_name)
        if agent:
            print(f"Agent: {agent.name}")
            print(f"Architecture: {agent.architecture}")
            print(f"File: {agent.file_path}")
        else:
            print(f"Agent '{args.agent_name}' not found")
    else:
        # Analyze all agents
        agents = analyzer.discover_all_agents()

        if args.report:
            report = analyzer.generate_analysis_report()
            if args.output:
                with open(args.output, "w") as f:
                    f.write(report)
                print(f"Report saved to {args.output}")
            else:
                print(report)
        else:

            # Group by architecture
            arch_groups = {}
            for agent in agents:
                arch = agent.architecture.value
                if arch not in arch_groups:
                    arch_groups[arch] = []
                arch_groups[arch].append(agent)

            for arch, arch_agents in arch_groups.items():
                for agent in sorted(arch_agents, key=lambda x: x.name):
                    capabilities = []
                    if agent.has_visualization:
                        capabilities.append("viz")
                    if agent.tools_support:
                        capabilities.append("tools")
                    if agent.streaming_support:
                        capabilities.append("stream")

                    cap_str = f" [{', '.join(capabilities)}]" if capabilities else ""


async def run_examples(args):
    """Run examples command."""
    runner = UniversalExampleRunner(args.project_root)

    config = ExecutionConfig(
        max_output_size=args.max_output_size,
        enable_visualization=args.visualize,
        stream_output=not args.no_stream,
        timeout_seconds=args.timeout,
    )

    if args.example_path:
        # Run specific example
        result = await runner.run_example(args.example_path, config)

        if result.agent_info:
            print(f"Agent: {result.agent_info.name}")

        if result.error:
            print(f"Error: {result.error}")

        if result.visualization_path:
            print(f"Visualization: {result.visualization_path}")

        if result.output_file:
            print(f"Output: {result.output_file}")

    elif args.discover:
        # Discover all examples
        examples = await runner.discover_all_examples()

        for example in sorted(examples):
            print(f"Found example: {example}")

    elif args.run_all:
        # Run all examples
        examples = await runner.discover_all_examples()

        results = await runner.run_multiple_examples(
            examples, config, max_concurrent=args.max_concurrent
        )

        # Generate report
        report = runner.generate_example_report(results)

        if args.output:
            with open(args.output, "w") as f:
                f.write(report)
        else:
            print(report)


async def visualize_agents(args):
    """Visualize agents command."""
    viz_manager = VisualizationManager()
    analyzer = AgentAnalyzer(args.project_root)

    config = VisualizationConfig(
        output_format=args.format,
        theme=args.theme,
        width=args.width,
        height=args.height,
        include_metadata=not args.no_metadata,
    )

    if args.agent_name:
        # Visualize specific agent
        agent = analyzer.get_agent_by_name(args.agent_name)
        if agent:
            output_path = Path(args.output) if args.output else None
            result = await viz_manager.visualize_agent(agent, output_path, config)

            if result.success:
                print(f"✅ Generated visualization for {agent.name}")
            else:
                print(f"❌ Failed to generate visualization for {agent.name}")
        else:
            print(f"Agent '{args.agent_name}' not found")

    elif args.compare:
        # Create comparison visualization
        agents = analyzer.discover_all_agents()
        output_path = (
            Path(args.output) if args.output else Path("agent_comparison.html")
        )

        result = await viz_manager.create_comparison_visualization(
            agents, output_path, config
        )

        if result.success:
            print(f"✅ Generated comparison visualization: {output_path}")
        else:
            print(f"❌ Failed to generate comparison visualization")

    else:
        # Visualize all agents
        agents = analyzer.discover_all_agents()
        output_dir = Path(args.output) if args.output else Path("visualizations")
        output_dir.mkdir(exist_ok=True)

        for agent in agents:
            viz_path = output_dir / f"{agent.name.lower()}_viz.{config.output_format}"
            result = await viz_manager.visualize_agent(agent, viz_path, config)

            if result.success:
                print(f"✅ Generated {viz_path}")
            else:
                print(f"❌ Failed to generate {viz_path}")


async def generate_docs(args):
    """Generate documentation command."""
    doc_generator = DocumentationGenerator(args.project_root)

    config = DocumentationConfig(
        include_examples=not args.no_examples,
        include_visualizations=not args.no_visualizations,
        include_code_snippets=not args.no_code,
        include_api_docs=args.api_docs,
        output_format=args.format,
        template_style=args.style,
        generate_index=not args.no_index,
    )

    output_dir = Path(args.output) if args.output else Path("docs")

    if args.agent_name:
        # Generate docs for specific agent
        analyzer = AgentAnalyzer(args.project_root)
        agent = analyzer.get_agent_by_name(args.agent_name)

        if agent:
            result = await doc_generator.generate_agent_documentation(
                agent, output_dir, config
            )

            if result.success:
                for file_path in result.output_files:
                    print(f"✅ Generated documentation: {file_path}")
            else:
                print(f"❌ Failed to generate documentation for {agent.name}")
        else:
            print(f"Agent '{args.agent_name}' not found")

    else:
        # Generate project-wide documentation
        result = await doc_generator.generate_project_documentation(output_dir, config)

        if result.success:
            print("Documentation generation successful")
        else:
            print("Documentation generation failed")


def create_parser():
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        description="Haive Documentation Utilities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--project-root",
        type=Path,
        help="Root directory of the Haive project (auto-detected if not provided)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze agents")
    analyze_parser.add_argument("--agent-name", help="Analyze specific agent")
    analyze_parser.add_argument(
        "--report", action="store_true", help="Generate analysis report"
    )
    analyze_parser.add_argument("--output", help="Output file for report")

    # Run examples command
    run_parser = subparsers.add_parser("run", help="Run examples")
    run_parser.add_argument("--example-path", help="Path to specific example to run")
    run_parser.add_argument(
        "--discover", action="store_true", help="Discover all examples"
    )
    run_parser.add_argument("--run-all", action="store_true", help="Run all examples")
    run_parser.add_argument(
        "--max-output-size",
        type=int,
        default=10_000_000,
        help="Maximum output size in bytes",
    )
    run_parser.add_argument(
        "--no-stream", action="store_true", help="Disable output streaming"
    )
    run_parser.add_argument(
        "--visualize", action="store_true", help="Generate visualizations"
    )
    run_parser.add_argument(
        "--timeout", type=int, default=300, help="Timeout in seconds"
    )
    run_parser.add_argument(
        "--max-concurrent", type=int, default=3, help="Maximum concurrent executions"
    )
    run_parser.add_argument("--output", help="Output file for report")

    # Visualize command
    viz_parser = subparsers.add_parser("visualize", help="Create visualizations")
    viz_parser.add_argument("--agent-name", help="Visualize specific agent")
    viz_parser.add_argument(
        "--compare", action="store_true", help="Create comparison visualization"
    )
    viz_parser.add_argument(
        "--format",
        choices=["png", "svg", "html", "mermaid"],
        default="png",
        help="Output format",
    )
    viz_parser.add_argument(
        "--theme",
        choices=["default", "dark", "minimal"],
        default="default",
        help="Visualization theme",
    )
    viz_parser.add_argument("--width", type=int, default=800, help="Width in pixels")
    viz_parser.add_argument("--height", type=int, default=600, help="Height in pixels")
    viz_parser.add_argument(
        "--no-metadata", action="store_true", help="Exclude metadata"
    )
    viz_parser.add_argument("--output", help="Output file or directory")

    # Documentation command
    docs_parser = subparsers.add_parser("docs", help="Generate documentation")
    docs_parser.add_argument("--agent-name", help="Generate docs for specific agent")
    docs_parser.add_argument(
        "--format",
        choices=["markdown", "rst", "html"],
        default="markdown",
        help="Output format",
    )
    docs_parser.add_argument(
        "--style",
        choices=["minimal", "standard", "comprehensive"],
        default="comprehensive",
        help="Documentation style",
    )
    docs_parser.add_argument(
        "--no-examples", action="store_true", help="Exclude examples"
    )
    docs_parser.add_argument(
        "--no-visualizations", action="store_true", help="Exclude visualizations"
    )
    docs_parser.add_argument(
        "--no-code", action="store_true", help="Exclude code snippets"
    )
    docs_parser.add_argument(
        "--no-index", action="store_true", help="Skip index generation"
    )
    docs_parser.add_argument(
        "--api-docs", action="store_true", help="Include API documentation"
    )
    docs_parser.add_argument("--output", help="Output directory", default="docs")

    return parser


async def main():
    """Main CLI function."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        if args.command == "analyze":
            await analyze_agents(args)
        elif args.command == "run":
            await run_examples(args)
        elif args.command == "visualize":
            await visualize_agents(args)
        elif args.command == "docs":
            await generate_docs(args)
        else:
            parser.print_help()

    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Command failed: {e}")
        if logging.getLogger().level <= logging.DEBUG:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
