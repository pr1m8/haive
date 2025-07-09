#!/usr/bin/env python
"""CLI tool for running the open_perplexity research agent.

This module provides command-line utilities for running research tasks
and visualizing research states. It supports loading research questions
from text files, configuring research parameters, and generating reports.
"""

import argparse
import json
import logging
import sys

from haive.core.models.embeddings.base import HuggingFaceEmbeddingConfig
from haive.core.models.vectorstore.base import VectorStoreConfig

from haive.agents.research.open_perplexity.agent import ResearchAgent
from haive.agents.research.open_perplexity.config import ResearchAgentConfig

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("research-cli")


def run_research(text_path: str, **kwargs) -> None:
    """Run a research process on text from the specified file.

    Loads a research question from a text file, configures a research agent with
    the specified parameters, runs the research process, and saves the results.

    Args:
        text_path: Path to a text file containing research question
        **kwargs: Additional arguments to pass to the agent, including:
            - output: Path to save the generated report
            - save_state_path: Path to save the state history
            - depth: Research depth (1-5)
            - concurrent_searches: Number of concurrent searches
            - max_sources: Maximum sources per query
            - vector_store_path: Path for the vector store
    """
    with open(text_path, encoding="utf-8") as f:
        text = f.read()

    # Create embedding configuration
    embedding_config = HuggingFaceEmbeddingConfig(
        model="sentence-transformers/all-mpnet-base-v2"
    )

    # Create vector store configuration
    vectorstore_config = VectorStoreConfig(
        embedding_model=embedding_config,
        vector_store_path=kwargs.get("vector_store_path", "research_vector_store"),
    )

    # Create the research agent configuration
    config = ResearchAgentConfig.from_scratch(
        vectorstore_config=vectorstore_config,
        research_depth=kwargs.get("depth", 3),
        concurrent_searches=kwargs.get("concurrent_searches", 3),
        max_sources_per_query=kwargs.get("max_sources", 5),
    )

    # Create and run the agent
    agent = ResearchAgent(config=config)
    final_state = agent.run({"input_text": text})

    # Save state history
    state_history_path = kwargs.get("save_state_path")
    if state_history_path:
        agent.save_state_history(state_history_path)
        logging.info(f"State history saved to {state_history_path}")

    # Generate report
    report = agent.generate_markdown_report(final_state)

    # Save report
    output_path = kwargs.get("output")
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)
        logging.info(f"Report saved to {output_path}")
    else:
        print(report)


def visualize_state(
    state_path: str, step: int | None = None, output_md: str | None = None
) -> None:
    """Visualize a specific state from a saved state history file.

    Loads a state from a saved state history file, displays a visualization
    of the research state, and optionally generates a markdown report.

    Args:
        state_path: Path to a saved state history JSON file
        step: Index of the state to visualize (default: last state)
        output_md: Path to save the markdown report (optional)
    """
    # Load the state history
    with open(state_path, encoding="utf-8") as f:
        try:
            state_data = json.load(f)

            # Check if this is a state history file (list of states)
            if isinstance(state_data, list):
                if not state_data:
                    logging.error(f"State history file is empty: {state_path}")
                    return

                # If step is specified, use that state
                if step is not None:
                    if step < 0 or step >= len(state_data):
                        logging.error(
                            f"Invalid step {step}, file contains {len(state_data)} states"
                        )
                        return
                    state = state_data[step]
                    print(f"Visualizing state at step {step} of {len(state_data)-1}")
                else:
                    # Default to the last state
                    state = state_data[-1]
                    print(f"Visualizing final state (step {len(state_data)-1})")
            else:
                # Single state
                state = state_data
                print("Visualizing single state")

        except json.JSONDecodeError:
            logging.exception(f"Failed to parse JSON from {state_path}")
            return

    # Set up the agent for visualization
    config = ResearchAgentConfig.from_scratch()
    agent = ResearchAgent(config=config)

    # Visualize the state
    agent.visualize_state(state)

    # Generate markdown report if requested
    if output_md:
        report = agent.generate_markdown_report(state)
        with open(output_md, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\nMarkdown report saved to {output_md}")


def main():
    """CLI entry point for the research tool.

    Parses command-line arguments and executes the appropriate command
    based on user input.
    """
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Open Perplexity Research Agent")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Research command
    research_parser = subparsers.add_parser(
        "research", help="Run research from a text file"
    )
    research_parser.add_argument(
        "file", help="Path to text file with research question"
    )
    research_parser.add_argument(
        "-o", "--output", help="Path to save the generated report"
    )
    research_parser.add_argument(
        "-s",
        "--save-state",
        dest="save_state_path",
        help="Path to save the state history for later visualization",
    )
    research_parser.add_argument(
        "-d",
        "--depth",
        type=int,
        default=3,
        help="Research depth (1-5, higher means more thorough)",
    )
    research_parser.add_argument(
        "-c",
        "--concurrent-searches",
        type=int,
        default=3,
        help="Number of concurrent searches",
    )
    research_parser.add_argument(
        "-m", "--max-sources", type=int, default=5, help="Maximum sources per query"
    )
    research_parser.add_argument(
        "-v",
        "--vector-store-path",
        default="research_vector_store",
        help="Path for the vector store",
    )

    # Visualize state command
    visualize_parser = subparsers.add_parser(
        "visualize", help="Visualize a state from a state history file"
    )
    visualize_parser.add_argument(
        "state_file", help="Path to saved state history JSON file"
    )
    visualize_parser.add_argument(
        "-s",
        "--step",
        type=int,
        help="Index of state to visualize (default: last state)",
    )
    visualize_parser.add_argument(
        "-m",
        "--markdown",
        dest="output_md",
        help="Generate and save markdown report to specified path",
    )

    # Parse arguments
    args = parser.parse_args()

    # Execute the appropriate command
    if args.command == "research":
        run_research(
            args.file,
            output=args.output,
            save_state_path=args.save_state_path,
            depth=args.depth,
            concurrent_searches=args.concurrent_searches,
            max_sources=args.max_sources,
            vector_store_path=args.vector_store_path,
        )
    elif args.command == "visualize":
        visualize_state(args.state_file, args.step, args.output_md)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
