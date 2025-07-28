"""Example of Enhanced MultiAgent V4 - Sequential ReactAgent → SimpleAgent pattern.

This example demonstrates:
1. Enhanced base agent pattern (extending Agent, implementing build_graph)
2. Direct list initialization of agents
3. Sequential execution mode
4. AgentNodeV3 integration for state projection
5. Real LLM execution (no mocks)
"""

import asyncio
import logging

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import tool

from haive.agents.multi.enhanced_multi_agent_v4 import EnhancedMultiAgentV4
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Create tools for ReactAgent
@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions."""
    try:
        result = eval(expression)
        return f"The result of {expression} is {result}"
    except Exception as e:
        return f"Error calculating {expression}: {str(e)}"


@tool
def word_counter(text: str) -> str:
    """Count words in text."""
    words = text.split()
    return f"The text contains {len(words)} words"


async def main():
    """Run the enhanced multi-agent example."""

    # Configure LLMs (low temperature for consistency)
    react_config = AugLLMConfig(
        temperature=0.1,
        system_message="You are a reasoning agent. Use tools to analyze the request.",
    )

    simple_config = AugLLMConfig(
        temperature=0.1,
        system_message="You are a formatter. Summarize the analysis results clearly.",
    )

    # Create agents
    reasoner = ReactAgent(
        name="reasoner",
        engine=react_config,
        tools=[calculator, word_counter],
        max_iterations=3,
    )

    formatter = SimpleAgent(name="formatter", engine=simple_config)

    # Create multi-agent workflow using enhanced base agent pattern
    workflow = EnhancedMultiAgentV4(
        name="analysis_workflow",
        agents=[reasoner, formatter],  # Direct list initialization
        execution_mode="sequential",  # Sequential: reasoner → formatter
        build_mode="auto",  # Auto-build graph on init
    )

    # Display workflow info
    workflow.display_info()

    # Test the workflow
    test_input = {
        "messages": [
            {
                "role": "user",
                "content": "Calculate 15 * 23 and count the words in this sentence.",
            }
        ]
    }

    logger.info("Starting multi-agent workflow...")

    try:
        # Execute the workflow
        result = await workflow.arun(test_input)

        logger.info("Workflow completed successfully!")
        logger.info(f"Final result: {result}")

        # Show the flow of execution
        if hasattr(result, "messages"):
            logger.info("\n=== Execution Flow ===")
            for i, msg in enumerate(result.messages):
                logger.info(f"{i+1}. [{msg.type}]: {msg.content[:100]}...")

    except Exception as e:
        logger.error(f"Error running workflow: {e}")
        raise


def run_simple_example():
    """Simpler synchronous example."""
    # Create a simple sequential workflow
    agents = [
        SimpleAgent(name="analyzer", engine=AugLLMConfig()),
        SimpleAgent(name="summarizer", engine=AugLLMConfig()),
    ]

    workflow = EnhancedMultiAgentV4(
        name="simple_workflow", agents=agents, execution_mode="sequential"
    )

    # Run synchronously
    result = workflow.run("Analyze the benefits of renewable energy.")
    print(f"Result: {result}")


if __name__ == "__main__":
    # Run async example
    asyncio.run(main())

    # Uncomment to run simple sync example
    # run_simple_example()
