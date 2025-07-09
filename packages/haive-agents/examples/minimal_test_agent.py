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
    print(f"Created multi-agent with {len(multi_agent._state_instance.agents)} agents")
    for agent_id, agent in multi_agent._state_instance.agents.items():
        print(f"  - Agent {agent_id}: {agent.name} ({agent.__class__.__name__})")

    # Create minimal input with just a message
    input_data = {"messages": [HumanMessage(content="Test message")]}

    # Run the invoke with just the input data
    try:
        # Simple invocation
        result = multi_agent.invoke(input_data)
        print("\nInvocation successful!")

        # Check if agents were preserved
        print(f"Result has agents: {hasattr(result, 'agents')}")
        if hasattr(result, "agents"):
            print(f"Agents in result: {len(result.agents)}")
            for agent_id, agent in result.agents.items():
                print(
                    f"  - Agent {agent_id}: {agent.name} ({agent.__class__.__name__})"
                )

        # Check messages
        print(f"\nMessages in result: {len(result.messages)}")
        for msg in result.messages:
            print(f"  - {msg.type}: {msg.content[:50]}...")

    except Exception as e:
        print(f"\nError during invocation: {type(e).__name__}: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    print("Running minimal MultiAgent serialization test...\n")
    minimal_test()
    print("\nTest completed.")
