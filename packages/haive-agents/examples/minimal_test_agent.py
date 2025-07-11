"""Minimal test for the MultiAgent serialization fix."""

import logging

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage

from haive.agents.multi.agent import MultiAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent

# Enable debug logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def minimal_test():
    """Create the simplest possible MultiAgent to test serialization."""
    # Create the engines
    simple_engine = AugLLMConfig()
    react_engine = AugLLMConfig()

    # Create the agents
    simple_agent = SimpleAgent(engine=simple_engine, name="Simple Test Agent")
    react_agent = ReactAgent(engine=react_engine, name="React Test Agent")

    # Create the multi-agent
    multi_agent = MultiAgent(
        agents=[simple_agent, react_agent], name="Serialization Test"
    )

    # Print the initial state
    for _agent_id, _agent in multi_agent._state_instance.agents.items():
        pass

    # Create minimal input with just a message
    input_data = {"messages": [HumanMessage(content="Test message")]}

    # Run the invoke with just the input data
    try:
        # Simple invocation
        result = multi_agent.invoke(input_data)

        # Check if agents were preserved
        if hasattr(result, "agents"):
            for _agent_id, _agent in result.agents.items():
                pass

        # Check messages
        for _msg in result.messages:
            pass

    except Exception:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    minimal_test()
