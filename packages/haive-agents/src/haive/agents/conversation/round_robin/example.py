# examples/conversation/round_robin_example.py
"""Examples for round-robin conversation patterns."""

import logging

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.messages import AIMessage, SystemMessage

from haive.agents.conversation.round_robin.agent import RoundRobinConversation
from haive.agents.simple.agent import SimpleAgent

# Set logging
logging.getLogger("haive").setLevel(logging.WARNING)


def example_simple_round_robin():
    """Simple round-robin conversation with auto-generated agents."""
    # Create using the factory method
    conversation = RoundRobinConversation.create_simple(
        participants=["Alice", "Bob", "Charlie"],
        topic="What's your favorite programming language and why?",
        max_rounds=2,
        announce_speaker=True,
    )

    # Run conversation
    result = conversation.invoke({})

    # Display results
    for msg in result.get("messages", []):
        if isinstance(msg, SystemMessage):
            pass


def example_custom_round_robin():
    """Round-robin with custom agent configurations."""
    # Create custom agents with specific personalities
    agents = {
        "Optimist": AugLLMConfig(
            name="optimist_engine",
            llm_config=AzureLLMConfig(),
            system_message="You are an eternal optimist. Always find the positive side. Keep responses to 2-3 sentences.",
            temperature=0.8,
        ),
        "Realist": AugLLMConfig(
            name="realist_engine",
            llm_config=AzureLLMConfig(),
            system_message="You are a practical realist. Focus on facts and practicality. Keep responses to 2-3 sentences.",
            temperature=0.6,
        ),
        "Pessimist": AugLLMConfig(
            name="pessimist_engine",
            llm_config=AzureLLMConfig(),
            system_message="You are a pessimist. Point out potential problems and risks. Keep responses to 2-3 sentences.",
            temperature=0.7,
        ),
    }

    # Create conversation
    conversation = RoundRobinConversation.create(
        participants=agents,  # type: ignore
        topic="The future of remote work",
        max_rounds=2,
        skip_unavailable=True,
    )

    # Run with custom config
    config = {"recursion_limit": 50}
    result = conversation.invoke({}, config)

    # Display
    for msg in result.get("messages", []):
        if isinstance(msg, AIMessage) and hasattr(msg, "name"):
            pass


def example_panel_discussion():
    """Simulate a panel discussion with round-robin format."""
    # Create panel discussion
    panelists = {
        "Moderator": SimpleAgent(
            name="Moderator",
            engine=AugLLMConfig(
                name="moderator_engine",
                system_message="You are a panel moderator. Ask thought-provoking questions and guide the discussion. Keep it brief.",
                temperature=0.7,
            ),
        ),
        "Expert1": SimpleAgent(
            name="Dr. Smith",
            engine=AugLLMConfig(
                name="expert1_engine",
                system_message="You are Dr. Smith, an AI researcher. Share technical insights concisely.",
                temperature=0.6,
            ),
        ),
        "Expert2": SimpleAgent(
            name="Prof. Johnson",
            engine=AugLLMConfig(
                name="expert2_engine",
                system_message="You are Prof. Johnson, an ethics professor. Focus on ethical implications.",
                temperature=0.6,
            ),
        ),
        "Expert3": SimpleAgent(
            name="Ms. Chen",
            engine=AugLLMConfig(
                name="expert3_engine",
                system_message="You are Ms. Chen, a tech entrepreneur. Share business perspectives.",
                temperature=0.7,
            ),
        ),
    }

    conversation = RoundRobinConversation(
        participant_agents=panelists,  # type: ignore
        topic="The Impact of AI on Society",
        max_rounds=2,
        announce_speaker=True,
    )

    result = conversation.invoke(
        {
            "messages": [
                SystemMessage(
                    content="Welcome to our panel discussion on AI's impact on society."
                )
            ]
        }
    )

    # Display key points
    for msg in result.get("messages", []):
        if isinstance(msg, AIMessage) and hasattr(msg, "name"):
            pass


if __name__ == "__main__":
    example_simple_round_robin()
