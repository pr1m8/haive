#!/usr/bin/env python3
"""Batch research example demonstrating how to use the Open Perplexity research agent
to process multiple research topics in sequence.
"""

import logging
import os
import sys
import time
from pathlib import Path

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent.parent))

from agents.open_perplexity.agent import ResearchAgent
from agents.open_perplexity.config import ResearchAgentConfig

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Research topics to process
RESEARCH_TOPICS = [
    {
        "title": "quantum_computing",
        "query": "What are the recent advancements in quantum computing and their potential applications?",
    },
    {
        "title": "climate_tech",
        "query": "What are promising climate technologies for carbon capture and storage?",
    },
    {
        "title": "space_exploration",
        "query": "What are the current challenges and future prospects for human Mars exploration?",
    },
]


def conduct_research(
    agent: ResearchAgent, topic: dict[str, str], output_dir: str
) -> dict:
    """Conduct research on a specific topic and save the report.

    Args:
        agent: The research agent
        topic: Dict containing the research topic with title and query
        output_dir: Directory to save the report

    Returns:
        Dict containing research results and metadata
    """
    start_time = time.time()
    title = topic["title"]
    query = topic["query"]

    logger.info(f"Starting research on: {title}")
    logger.info(f"Query: {query}")

    # Run the research
    final_state = agent.run({"input_text": query})

    # Generate report
    report = agent.generate_markdown_report(final_state)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Save report
    report_path = os.path.join(output_dir, f"{title}_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    elapsed_time = time.time() - start_time

    # Collect metadata
    metadata = {
        "title": title,
        "query": query,
        "report_path": report_path,
        "elapsed_time": elapsed_time,
        "confidence": final_state.get("confidence_level", "Unknown"),
        "num_sources": len(final_state.get("sources", [])),
        "num_sections": len(final_state.get("report_sections", [])),
    }

    logger.info(f"Completed research on {title} in {elapsed_time:.2f} seconds")
    logger.info(f"Report saved to {report_path}")

    return metadata


def main():
    """Run batch research on multiple topics."""
    logger.info("Initializing batch research process...")

    # Create output directory for reports
    output_dir = "research_reports"

    # Create configuration for the research agent
    config = ResearchAgentConfig.from_scratch(
        research_depth=2,  # Lower depth for faster execution
        concurrent_searches=3,
        max_sources_per_query=4,
    )

    # Create research agent
    logger.info("Creating research agent...")
    agent = ResearchAgent(config=config)

    # Process each research topic
    results = []
    for topic in RESEARCH_TOPICS:
        try:
            metadata = conduct_research(agent, topic, output_dir)
            results.append(metadata)
        except Exception as e:
            logger.error(f"Error processing research topic '{topic['title']}': {e}")

    # Generate summary report
    logger.info("Generating batch research summary...")
    summary_path = os.path.join(output_dir, "batch_summary.md")

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("# Batch Research Summary\n\n")
        f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Total Topics Processed: {len(results)}\n\n")

        f.write("## Research Topics\n\n")
        for result in results:
            f.write(f"### {result['title']}\n\n")
            f.write(f"**Query**: {result['query']}\n\n")
            f.write(f"**Confidence**: {result['confidence']}\n\n")
            f.write(f"**Sources**: {result['num_sources']}\n\n")
            f.write(f"**Sections**: {result['num_sections']}\n\n")
            f.write(f"**Processing Time**: {result['elapsed_time']:.2f} seconds\n\n")
            f.write(
                f"**Report**: [View Report]({os.path.basename(result['report_path'])})\n\n"
            )
            f.write("---\n\n")

    logger.info(f"Batch summary saved to {summary_path}")

    # Print overall summary
    print("\n" + "=" * 50)
    print("BATCH RESEARCH SUMMARY")
    print("=" * 50)
    print(f"Total topics processed: {len(results)}")
    print(
        f"Average processing time: {sum(r['elapsed_time'] for r in results) / len(results):.2f} seconds"
    )
    print(f"All reports saved to: {output_dir}")
    print("=" * 50)


if __name__ == "__main__":
    main()
