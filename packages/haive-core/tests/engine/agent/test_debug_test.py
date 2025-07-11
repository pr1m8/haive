# tests/engine/agent/debug_test.py

import logging
import uuid
from typing import Any

from haive.agents.simple.config import SimpleAgentConfig
from langchain_core.messages import HumanMessage

from haive.core.engine.aug_llm import AugLLMConfig

logger = logging.getLogger(__name__)


def debug_state_inspection():
    """Debug test that inspects state directly."""
    # Create a unique thread ID for persistence
    thread_id = f"debug-thread-{uuid.uuid4().hex[:8]}"
    logger.info(f"Using thread ID: {thread_id}")

    # Create a simple agent
    aug_llm = AugLLMConfig(
        name="debug_llm", system_prompt="You are a helpful assistant for debugging."
    )

    agent_config = SimpleAgentConfig(name="DebugAgent", engine=aug_llm)

    agent = agent_config.build_agent()

    # Define a config with thread ID
    config = {"configurable": {"thread_id": thread_id}}

    # First run to set up initial state
    logger.info("First run - setting up state")
    input_message = HumanMessage(content="Remember the number 12345")

    # Run the agent
    result = agent.run({"messages": [input_message]}, config=config)
    # Debug output
    logger.info("FIRST RUN RESULT:")
    print_state_deeply(result)

    # Get saved state and inspect it
    logger.info("RETRIEVING SAVED STATE")
    saved_state = agent.app.get_state(config)
    print_state_deeply(saved_state)

    # Second run
    logger.info("Second run - getting state")
    input_message2 = HumanMessage(content="What number did I tell you to remember?")

    # Run the agent again with the same thread ID
    result2 = agent.run({"messages": [input_message2]}, config=config)

    # Debug output
    logger.info("SECOND RUN RESULT:")
    print_state_deeply(result2)

    # Compare and output differences
    messages1 = extract_messages(result)
    messages2 = extract_messages(result2)

    logger.info(f"First run had {len(messages1)} messages")
    logger.info(f"Second run has {len(messages2)} messages")

    logger.info("DEBUG TEST COMPLETED")


def extract_messages(state: Any) -> list:
    """Extract messages from state, regardless of format."""
    if state is None:
        return []

    # Handle dict with messages
    if isinstance(state, dict) and "messages" in state:
        return state["messages"]

    # Handle StateSnapshot with values
    if hasattr(state, "values") and state.values:
        values = state.values
        if isinstance(values, dict) and "messages" in values:
            return values["messages"]

    # Handle StateSnapshot with channel_values
    if hasattr(state, "channel_values") and state.channel_values:
        values = state.channel_values
        if isinstance(values, dict) and "messages" in values:
            return values["messages"]

    # Handle direct messages attribute
    if hasattr(state, "messages"):
        return state.messages

    return []


def print_state_deeply(state: Any, level: int = 0):
    """Print state recursively with type information."""
    indent = "  " * level

    if state is None:
        logger.info(f"{indent}None")
        return

    if isinstance(state, dict):
        logger.info(f"{indent}Dict with {len(state)} keys:")
        for key, value in state.items():
            logger.info(f"{indent}  {key} ({type(value).__name__}):")
            print_state_deeply(value, level + 2)
    elif isinstance(state, list):
        logger.info(f"{indent}List with {len(state)} items:")
        for i, item in enumerate(state):
            logger.info(f"{indent}  {i}: ({type(item).__name__})")
            print_state_deeply(item, level + 2)
    elif hasattr(state, "__dict__"):
        logger.info(f"{indent}Object of type {type(state).__name__}:")

        # Handle special types
        if hasattr(state, "values") and state.values:
            logger.info(f"{indent}  .values ({type(state.values).__name__}):")
            print_state_deeply(state.values, level + 2)
        elif hasattr(state, "channel_values") and state.channel_values:
            logger.info(
                f"{indent}  .channel_values ({type(state.channel_values).__name__}):"
            )
            print_state_deeply(state.channel_values, level + 2)
        elif hasattr(state, "state") and state.state:
            logger.info(f"{indent}  .state ({type(state.state).__name__}):")
            print_state_deeply(state.state, level + 2)
        else:
            # Regular object with attributes
            for attr, value in state.__dict__.items():
                if not attr.startswith("_"):
                    logger.info(f"{indent}  .{attr} ({type(value).__name__}):")
                    print_state_deeply(value, level + 2)
    else:
        # Show the value directly
        value_str = str(state)
        if len(value_str) > 100:
            value_str = value_str[:100] + "..."
        logger.info(f"{indent}Value: {value_str}")

        # For message objects, show content
        if hasattr(state, "content"):
            logger.info(f"{indent}  .content: {state.content}")

        # For tuples that might be messages, show components
        if isinstance(state, tuple) and len(state) >= 2:
            logger.info(f"{indent}  Tuple components: {state[0]}, {state[1]}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    debug_state_inspection()
