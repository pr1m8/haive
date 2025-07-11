# examples/storm_agent_example.py

"""Example demonstrating how to use the STORM agent to generate
a comprehensive Wikipedia-style article on a given topic.
"""

import argparse
import asyncio
import logging
import os

from agents.sequence.storm import STORMAgentConfig
from haive.core.engine.retriever import VectorStoreRetrieverConfig
from haive.core.engine.vectorstore import VectorStoreConfig
from haive.core.models.embeddings.base import OpenAIEmbeddingConfig
from haive.core.models.llm.base import AzureLLMConfig

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def setup_environment():
    """Set up required environment variables."""
    # Check for Azure OpenAI credentials
    missing_vars = []
    required_vars = [
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_API_VERSION",
        "AZURE_OPENAI_API_BASE",
        "OPENAI_API_KEY",  # For embeddings
    ]

    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)

    if missing_vars:
        logger.error(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )
        logger.error("Please set these variables before running the example.")
        exit(1)


async def run_storm_agent(
    topic: str,
    output_file: str | None = None,
    num_perspectives: int = 3,
    max_turns: int = 5,
    verbose: bool = False,
):
    """Run the STORM agent on a given topic.

    Args:
        topic: The topic to research and write about
        output_file: Optional file path to save the generated article
        num_perspectives: Number of perspectives to interview
        max_turns: Maximum number of conversation turns per interview
        verbose: Whether to enable verbose logging
    """
    # Set logging level based on verbosity
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    logger.info(f"Setting up STORM agent for topic: {topic}")

    # Configure LLMs
    fast_llm = AzureLLMConfig(
        model="gpt-4o-mini",
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
        api_base=os.environ.get("AZURE_OPENAI_API_BASE"),
    )

    long_context_llm = AzureLLMConfig(
        model="gpt-4o",
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
        api_base=os.environ.get("AZURE_OPENAI_API_BASE"),
    )

    # Configure embeddings
    embedding_model = OpenAIEmbeddingConfig(
        model="text-embedding-3-small", api_key=os.environ.get("OPENAI_API_KEY")
    )

    # Configure vector store
    vector_store_config = VectorStoreConfig(
        name="storm_references",
        vector_store_provider="InMemory",
        embedding_model=embedding_model,
    )

    # Configure retriever
    retriever_config = VectorStoreRetrieverConfig(
        name="storm_retriever",
        vector_store_config=vector_store_config,
        k=4,
        search_type="similarity",
    )

    # Create the STORM agent config
    storm_config = STORMAgentConfig(
        name="storm_research_assistant",
        topic=topic,
        num_perspectives=num_perspectives,
        max_interview_turns=max_turns,
        fast_llm_config=fast_llm,
        long_context_llm_config=long_context_llm,
        vector_store_config=vector_store_config,
        retriever_config=retriever_config,
    )

    # Build the agent
    storm_agent = storm_config.build_agent()

    # Track progress through the stages
    logger.info("Starting STORM agent execution")
    progress_stages = {
        "research_stage": "Generating outline and identifying perspectives",
        "interview_stage": "Conducting expert interviews",
        "writing_stage": "Refining outline, writing sections, and assembling article",
    }

    # Execute with progress tracking
    try:
        async for step in storm_agent.astream(topic):
            # Get the current stage
            stage_name = next(iter(step))
            if stage_name in progress_stages:
                logger.info(f"Progress: {progress_stages[stage_name]}")

        # Get the final state
        final_state = storm_agent.app.get_state(storm_agent.config.runnable_config)

        # Extract the article
        if (
            final_state
            and "values" in final_state
            and "article" in final_state["values"]
        ):
            article = final_state["values"]["article"]

            # Print a preview of the article
            logger.info("Article generation complete!")

            # Print just the beginning of the article for a preview
            "\n".join(article.split("\n")[:20])

            # Save to file if requested
            if output_file:
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(f"# {topic}\n\n{article}")
                logger.info(f"Article saved to {output_file}")
        else:
            logger.error("Failed to generate article.")

    except Exception as e:
        logger.exception(f"Error running STORM agent: {e!s}")
        raise


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Generate a Wikipedia-style article using the STORM agent"
    )
    parser.add_argument("topic", help="Topic to research and write about")
    parser.add_argument("--output", "-o", help="Output file path (optional)")
    parser.add_argument(
        "--perspectives",
        "-p",
        type=int,
        default=3,
        help="Number of perspectives (default: 3)",
    )
    parser.add_argument(
        "--turns", "-t", type=int, default=5, help="Max conversation turns (default: 5)"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Set up environment
    setup_environment()

    # Run the agent
    asyncio.run(
        run_storm_agent(
            topic=args.topic,
            output_file=args.output,
            num_perspectives=args.perspectives,
            max_turns=args.turns,
            verbose=args.verbose,
        )
    )


if __name__ == "__main__":
    main()
