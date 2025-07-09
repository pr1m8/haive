#!/usr/bin/env python3
"""Simple example demonstrating how to use the Open Perplexity research agent
for a specific research topic.
"""

import logging
import sys
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


def main():
    """Run a simple research example on AI ethics."""
    # Define research question
    research_question = """
    What are the key ethical concerns in artificial intelligence development?
    Focus on issues like bias, privacy, and transparency.
    """

    logger.info(f"Research question: {research_question}")

    # Create configuration for the research agent
    config = ResearchAgentConfig.from_scratch(
        research_depth=2,  # Lower depth for faster execution
        concurrent_searches=2,
        max_sources_per_query=3,
    )

    # Create and run the agent
    logger.info("Creating research agent...")
    agent = ResearchAgent(config=config)

    logger.info("Running research process...")
    final_state = agent.run({"input_text": research_question})

    # Generate and display report
    logger.info("Generating research report...")
    report = agent.generate_markdown_report(final_state)

    # Save report to file
    report_path = "ai_ethics_research.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    logger.info(f"Report saved to {report_path}")

    # Show summary
    print("\n" + "=" * 50)
    print("RESEARCH SUMMARY")
    print("=" * 50)

    # Print a brief summary
    topic = final_state.get("research_topic", "Unknown topic")
    sections = final_state.get("report_sections", [])
    sources = final_state.get("sources", [])
    confidence = final_state.get("confidence_level", "Unknown")

    print(f"Topic: {topic}")
    print(f"Sections: {len(sections)}")
    print(f"Sources: {len(sources)}")
    print(f"Confidence: {confidence}")
    print("=" * 50)

    print(f"\nFull report saved to: {report_path}")


if __name__ == "__main__":
    main()
