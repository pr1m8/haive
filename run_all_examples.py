#!/usr/bin/env python3
"""Run All Examples - Execute all agent examples and generate visualizations.
===============================================

This script uses the Universal Example Runner system to:
1. Discover all example files across all Haive packages
2. Run each example with streaming output and error handling
3. Generate visualizations for compatible agents
4. Create a comprehensive report

Usage:
    python run_all_examples.py [--concurrent 3] [--timeout 300] [--viz-only]
"""

import argparse
import asyncio
import logging
from pathlib import Path

from scripts.doc_utils.example_runner import ExecutionConfig, UniversalExampleRunner

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Run all Haive agent examples")
    parser.add_argument(
        "--concurrent",
        type=int,
        default=3,
        help="Maximum concurrent executions (default: 3)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Timeout per example in seconds (default: 300)",
    )
    parser.add_argument(
        "--viz-only",
        action="store_true",
        help="Only generate visualizations, skip execution",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="example_outputs",
        help="Directory to save outputs (default: example_outputs)",
    )

    args = parser.parse_args()

    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)

    # Initialize the runner
    runner = UniversalExampleRunner()

    # Configure execution
    config = ExecutionConfig(
        timeout_seconds=args.timeout,
        enable_visualization=True,
        stream_output=True,
        save_full_output=True,
        output_file=output_dir / "full_output.txt",
    )


    # Discover all examples
    example_files = await runner.discover_all_examples()

    if not example_files:
        return


    # Print discovered examples
    for i, example_file in enumerate(example_files[:10], 1):  # Show first 10
        relative_path = example_file.relative_to(runner.project_root)

    if len(example_files) > 10:
        pass


    if args.viz_only:
        pass")
    else:
        pass")

    # Ask for confirmation
    response = input(f"\n🤔 Run {len(example_files)} examples? (y/N): ")
    if response.lower() not in ["y", "yes"]:
        return


    # Run all examples
    if args.viz_only:
        # Only generate visualizations (faster)
        results = []
        for example_file in example_files:
            try:
                # Try to generate visualization only
                result = await runner.run_example(example_file, config)
                results.append(result)

                status = "✅" if result.success else "❌"

            except Exception as e:
                pass")

    else:
        # Full execution
        results = await runner.run_multiple_examples(
            example_files, config, max_concurrent=args.concurrent
        )


    # Generate and save report
    report = runner.generate_example_report(results)
    report_file = output_dir / "execution_report.md"

    with open(report_file, "w") as f:
        f.write(report)


    # Show visualization files
    viz_files = [r.visualization_path for r in results if r.visualization_path]
    if viz_files:
        for viz_file in viz_files:
            pass")

    # Show output files
    output_files = [r.output_file for r in results if r.output_file]
    if output_files:
        for output_file in output_files:
            pass")



if __name__ == "__main__":
    asyncio.run(main())
