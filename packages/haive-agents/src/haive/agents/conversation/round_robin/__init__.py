r"""Round Robin Conversation - Sequential Turn-Based Multi-Agent Dialogue.

A simple turn-based conversation agent where participants speak in sequence with
automatic round tracking and progress management. The round robin conversation
follows a strict order of speakers, ensuring that each participant gets exactly
one turn per round in a predictable and balanced manner.

Architecture:
    The round robin conversation extends BaseConversationAgent with a sequential
    speaker selection strategy that rotates through participants in a fixed order.
    This provides the most straightforward form of multi-agent conversation with
    guaranteed turn equality and predictable flow.

Key Features:
    - Participants speak in a fixed, predictable order
    - Each speaker gets exactly one turn per round
    - The conversation progresses through complete rounds
    - Round counts and progress are automatically tracked via ConversationState
    - Configurable round limit with automatic termination
    - Optional speaker announcements and context sharing
    - Ability to skip unavailable speakers
    - Rich progress tracking and analytics

Core Components:
    RoundRobinConversation: Main agent class that orchestrates sequential conversations
        with automatic speaker rotation and turn management.
    ConversationState: Inherited state management with round tracking and progress
        calculation (from base conversation module).

Usage Patterns:
    Basic round robin conversation::\n

        from haive.agents.conversation import RoundRobinConversation
        from haive.agents.simple import SimpleAgent

        # Create participants
        alice = SimpleAgent(name="Alice")
        bob = SimpleAgent(name="Bob")
        charlie = SimpleAgent(name="Charlie")

        # Create conversation
        conversation = RoundRobinConversation(
            participants=[alice, bob, charlie],
            topic="The future of AI",
            max_rounds=3
        )

        # Run the conversation
        result = await conversation.arun()

        # Access conversation data
        messages = result["messages"]
        final_state = result["conversation_state"]

    Factory method for quick setup::\n

        # Create a simple round-robin conversation
        conversation = RoundRobinConversation.create_simple(
            participants=["Alice", "Bob", "Charlie"],
            topic="The future of AI",
            max_rounds=3
        )

        # Run the conversation
        result = await conversation.arun()

Speaker Selection:
    The round robin agent uses a simple modulo-based speaker selection strategy:
    1. Determine current round based on turn count and speaker count
    2. Select next speaker in sequence based on remaining speakers
    3. Continue until all speakers in round have spoken or max rounds reached
    4. Automatic progress tracking through ConversationState computed properties

Use Cases:
    - Structured discussions where turn equality is important
    - Balanced group conversations with fair participation
    - Panel discussions with ordered speaking opportunities
    - Educational scenarios requiring equal participation
    - Simulated meetings with democratic turn distribution

Integration:
    Round robin conversations integrate seamlessly with:
    - Haive core schema system for state management
    - Base conversation infrastructure for orchestration
    - Message handling and routing systems
    - Progress tracking and analytics
    - Custom agent implementations as participants

Examples:
    For comprehensive examples, see the documentation and examples directory:
    - examples/round_robin_basic.py
    - examples/round_robin_advanced.py
    - examples/round_robin_with_context.py

See Also:
    - :class:`~haive.agents.conversation.base.agent.BaseConversationAgent`: Parent class
    - :class:`~haive.agents.conversation.base.state.ConversationState`: State management
    - :class:`~haive.agents.conversation.directed.agent.DirectedConversation`: Moderated alternative
    - :class:`~haive.agents.conversation.debate.agent.DebateConversation`: Structured debate alternative

Version: 1.0.0
Author: Haive Team
License: MIT
"""

# Version information
__version__ = "1.0.0"
__author__ = "Haive Team"
__license__ = "MIT"

# Type imports for better IDE support
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Optional,
)

from typing_extensions import TypeAlias

if TYPE_CHECKING:
    from haive.agents.conversation.base.agent import BaseConversationAgent
    from haive.agents.conversation.base.state import ConversationState

# Core imports
from haive.agents.conversation.round_robin.agent import RoundRobinConversation

# Type aliases for round robin conversations
RoundRobinParticipant: TypeAlias = Any  # Agent with conversation capabilities
RoundRobinResult: TypeAlias = dict[str, Any]  # Conversation result data

# Define public API
__all__ = [
    # Core classes
    "RoundRobinConversation",
    # Type aliases
    "RoundRobinParticipant",
    "RoundRobinResult",
    "__author__",
    "__license__",
    # Version information
    "__version__",
    # Utility functions
    "create_round_robin_conversation",
]


# Utility functions
def create_round_robin_conversation(
    participants: list[RoundRobinParticipant],
    topic: str,
    max_rounds: int = 3,
    **kwargs: Any
) -> RoundRobinConversation:
    r"""Create a round robin conversation with participants.

    Args:
        participants: List of participant agents
        topic: Conversation topic
        max_rounds: Maximum number of rounds
        **kwargs: Additional configuration options

    Returns:
        Configured RoundRobinConversation instance

    Examples:
        Basic round robin conversation::\n

            conversation = create_round_robin_conversation(
                participants=[alice, bob, charlie],
                topic="Future of AI",
                max_rounds=5
            )

        With custom configuration::\n

            conversation = create_round_robin_conversation(
                participants=[expert1, expert2, expert3],
                topic="Technical discussion",
                max_rounds=3,
                enable_speaker_announcements=True
            )
    """
    return RoundRobinConversation(
        participants=participants, topic=topic, max_rounds=max_rounds, **kwargs
    )


# Add convenience functions to global namespace
create_round_robin_conversation.__module__ = __name__
