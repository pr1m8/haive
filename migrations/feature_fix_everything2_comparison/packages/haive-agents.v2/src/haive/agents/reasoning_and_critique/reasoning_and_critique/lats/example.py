"""Example usage of the Language Agent Tree Search (LATS) agent."""

import logging
import os
import sys

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.lats.agent import create_lats_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Run an example of the LATS agent."""
    # Check for required API keys
    if not os.environ.get("AZURE_OPENAI_API_KEY"):
        raise ValueError("AZURE_OPENAI_API_KEY environment variable is required")

    # Set up tools - using Tavily search in this example
    tools = []
    if os.environ.get("TAVILY_API_KEY"):
        search = TavilySearchAPIWrapper()
        tavily_tool = TavilySearchResults(api_wrapper=search, max_results=5)
        tools.append(tavily_tool)
        logger.info("Tavily search tool added")
    else:
        logger.warning("TAVILY_API_KEY not found, continuing without search tool")

    # Create the LATS agent
    agent = create_lats_agent(
        system_prompt="You are a helpful AI assistant that answers questions accurately and concisely.",
        tools=tools,
        max_depth=3,  # Limit depth for faster execution in this example
        n_candidates=3,  # Generate 3 candidates at each step for faster execution
        name="lats_example_agent",
    )

    # Example questions to demonstrate the agent
    questions = [
        # "Generate a table with the average size and weight, as well as the oldest recorded instance for each of the top 5 most common birds.",
        # "What is the chemical composition of lithium-ion batteries and their environmental impact?",
        "Write out magnus carlson series of moves in his game against Alireza Firouzja and propose an alternate strategy"
    ]

    # Run the agent on each question
    for question in questions:
        logger.info(f"\n\n*** Running LATS agent on question: {question} ***\n")

        # Track the computation steps
        last_step = None
        step_count = 0

        # Stream the agent's processing steps
        for step in agent.app.stream(
            {"input": question}, debug=True, config=agent.config.runnable_config
        ):
            step_count += 1
            last_step = step

            # Print information about the current step
            step_name = next(iter(step.keys()))
            step_state = step[step_name]

            # Get tree height if available
            tree_height = 0
            if "nodes_data" in step_state and "root_id" in step_state:
                nodes_data = step_state.get("nodes_data", {})
                max_depth = 0
                for _node_id, node_data in nodes_data.items():
                    max_depth = max(max_depth, node_data.depth)
                tree_height = max_depth

            logger.info(f"Step {step_count}: {step_name} (tree height: {tree_height})")

            # Log the output if available
            if step_state.get("output"):
                logger.info(f"Output: {step_state['output'][:100]}...")

        # Extract and print the final answer
        if last_step:
            # Get the output from the final state
            final_state = last_step["output"]

            # Try to reconstruct messages for more details
            messages = []
            if "messages" in final_state:
                from agents.lats.models import SerializedMessage

                for msg_data in final_state["messages"]:
                    try:
                        if isinstance(msg_data, dict):
                            serialized_msg = SerializedMessage(**msg_data)
                            messages.append(serialized_msg.to_base_message())
                        else:
                            # Might already be a message object
                            messages.append(msg_data)
                    except Exception as e:
                        logger.warning(f"Error converting message: {e}")

            # Print some statistics
            if "nodes_data" in final_state:
                pass

            # Print reflection information if available
            if "nodes_data" in final_state and "root_id" in final_state:
                root_id = final_state["root_id"]
                if root_id in final_state["nodes_data"]:
                    root_data = final_state["nodes_data"][root_id]
                    if root_data.reflection:
                        pass


if __name__ == "__main__":
    main()
