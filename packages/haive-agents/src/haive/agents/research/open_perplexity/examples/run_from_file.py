#!/usr/bin/env python3
"""Example script that demonstrates running the open_perplexity research agent
with a research question loaded from a text file.
"""

import argparse
import logging
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent.parent))

from agents.open_perplexity.agent import ResearchAgent
from agents.open_perplexity.config import ResearchAgentConfig
from haive.core.engine.vectorstore import VectorStoreConfig


def setup_logging(log_file="research_run.log"):
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file, mode="w"),  # Overwrite the log file
        ],
    )
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    return logger


def load_research_question(file_path):
    """Load research question from a text file."""
    try:
        with open(file_path, encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        raise ValueError(f"Error reading research question file: {e}")


def run_research(question_file, output_dir=None, research_depth=2, max_sources=5):
    """Run research based on a question from a file.

    Args:
        question_file: Path to file containing the research question
        output_dir: Directory for outputs (default: ./outputs)
        research_depth: Depth of research (1-3)
        max_sources: Maximum number of sources per query

    Returns:
        Boolean indicating success or failure
    """
    # Set up logging
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"research_run_{timestamp}.log"
    logger = setup_logging(log_file)

    try:
        logger.info(f"Starting research run with question file: {question_file}")

        # Create output directory if needed
        output_dir = Path.cwd() / "outputs" if output_dir is None else Path(output_dir)

        output_dir.mkdir(exist_ok=True)
        logger.info(f"Using output directory: {output_dir}")

        # Load research question
        question_path = Path(question_file)
        research_question = load_research_question(question_path)
        question_name = question_path.stem

        logger.info(f"Loaded research question: {question_name}")
        logger.info("Question text:")
        logger.info(f"\n{research_question}")

        # Create output file paths
        state_history_path = str(
            output_dir / f"{question_name}_state_history_{timestamp}.json"
        )
        report_path = str(output_dir / f"{question_name}_report_{timestamp}.md")
        vectorstore_path = str(output_dir / f"{question_name}_vectorstore")

        # Create agent configuration
        config = ResearchAgentConfig(
            name=f"research_{question_name}",
            description=f"Research agent for {question_name}",
            research_depth=research_depth,
            max_sources_per_query=max_sources,
            concurrent_searches=True,
            vectorstore_config=VectorStoreConfig(
                name=f"{question_name}_vectorstore",
                vector_store_type="FAISS",
                persist_directory=vectorstore_path,
            ),
        )

        # Create and run agent
        logger.info("Creating research agent...")
        agent = ResearchAgent(config=config)

        logger.info("Running research process...")
        start_time = time.time()

        final_state = agent.run({"input_context": research_question})

        logger.info("Research completed successfully")

        # Save state history
        history_path = agent.save_state_history(state_history_path)
        logger.info(f"State history saved to {history_path}")

        # Save report
        report = final_state.get("final_report", "No report generated.")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        logger.info(f"Research report saved to {report_path}")

        # Display execution information
        execution_time = time.time() - start_time
        logger.info(f"Research completed in {execution_time:.2f} seconds")

        return True

    except Exception as e:
        logger.exception(f"Error running research: {e}")
        logger.exception(traceback.format_exc())
        return False


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Run research based on a question file"
    )

    parser.add_argument(
        "question_file", help="Path to file containing the research question"
    )

    parser.add_argument(
        "-o",
        "--output-dir",
        help="Directory for outputs (default: ./outputs)",
        default=None,
    )

    parser.add_argument(
        "-d",
        "--depth",
        type=int,
        choices=[1, 2, 3],
        default=2,
        help="Research depth: 1=superficial, 2=medium, 3=deep (default: 2)",
    )

    parser.add_argument(
        "-s",
        "--max-sources",
        type=int,
        default=5,
        help="Maximum number of sources per query (default: 5)",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    success = run_research(
        question_file=args.question_file,
        output_dir=args.output_dir,
        research_depth=args.depth,
        max_sources=args.max_sources,
    )

    sys.exit(0 if success else 1)
