r"""Directed Conversation - Moderator-Controlled Multi-Agent Dialogue.

Conversations with explicit flow control directed by a moderator agent. The directed
conversation implements a flexible conversation pattern where a moderator agent
directs the flow of the conversation by explicitly selecting which participant
should speak next, enabling dynamic and content-driven multi-agent interactions.

Architecture:
    The directed conversation extends BaseConversationAgent with a moderator-based
    speaker selection system that allows for organic conversation development
    guided by intelligent flow control. This provides maximum flexibility for
    complex conversational scenarios that require adaptive management.

Key Features:
    - Dynamic conversation flow based on content and context
    - Moderator agent with intelligent speaker selection control
    - Targeted follow-up questions and responses
    - Conversation branching and focusing capabilities
    - Structured interviews and panel discussions
    - Conditional speaker selection based on expertise and relevance
    - Adaptive flow control with reasoning-based decisions
    - Support for multiple conversation formats and styles

Core Components:
    DirectedConversation: Main agent class that orchestrates moderator-controlled
        conversations with dynamic speaker selection and flow management.
    DirectedState: Specialized state schema extending ConversationState with
        moderator-specific fields and flow control tracking.

Flow Control:
    Unlike round-robin conversations that follow a fixed pattern, directed
    conversations allow for organic development guided by a moderator's
    intelligent decisions about which participant should contribute at each
    point based on conversation context and goals.

Usage Patterns:
    Interview-style conversation::\n

        from haive.agents.conversation import DirectedConversation
        from haive.agents.simple import SimpleAgent

        # Create participants
        interviewer = SimpleAgent(name="Interviewer", role="moderator")
        expert1 = SimpleAgent(name="Expert1", role="interviewee")
        expert2 = SimpleAgent(name="Expert2", role="interviewee")
        expert3 = SimpleAgent(name="Expert3", role="interviewee")

        # Create directed conversation
        interview = DirectedConversation(
            moderator=interviewer,
            participants=[expert1, expert2, expert3],
            topic="Climate Change Solutions",
            conversation_format="interview",
            max_rounds=10
        )

        # Run the conversation
        result = await interview.arun()

        # Access conversation data
        messages = result["messages"]
        flow_decisions = result["moderator_decisions"]

    Panel discussion format::\n

        # Panel discussion with expert moderator
        panel = DirectedConversation(
            moderator=panel_moderator,
            participants=[scientist, policy_expert, industry_rep, activist],
            topic="Future of Renewable Energy",
            conversation_format="panel",
            selection_strategy="expertise_based",
            max_rounds=15
        )

        # Run with dynamic flow control
        result = await panel.arun()

    Factory method for quick setup::\n

        # Create interview format quickly
        interview = DirectedConversation.create_interview(
            interviewer=interviewer_agent,
            interviewees=[expert1, expert2, expert3],
            topic="AI Ethics and Governance",
            max_rounds=8
        )

Conversation Formats:
    - **Interview**: One-to-many questioning with follow-up control
    - **Panel**: Moderated multi-participant discussion
    - **Q&A**: Question and answer session with dynamic selection
    - **Seminar**: Educational format with guided discussion
    - **Investigation**: Deep-dive exploration with targeted questioning

Speaker Selection Strategies:
    - **Content-based**: Select speakers based on conversation content
    - **Expertise-based**: Choose speakers based on domain knowledge
    - **Round-robin-fallback**: Use round-robin when no specific preference
    - **Random**: Random selection for exploratory conversations
    - **Custom**: Moderator-defined selection logic

Moderator Capabilities:
    The moderator agent can:
    - Analyze conversation context and determine optimal next speaker
    - Ask targeted follow-up questions to specific participants
    - Guide conversation toward specific topics or goals
    - Balance participation across all participants
    - Adapt flow based on conversation quality and engagement

Use Cases:
    - Simulating interviews with multiple subjects
    - Creating panel discussions with intelligent moderation
    - Implementing Q&A sessions with dynamic follow-up
    - Content-driven conversations where flow matters more than turn equality
    - Educational scenarios with guided exploration
    - Investigation and fact-finding conversations
    - Expert consultation with targeted questioning

Integration:
    Directed conversations integrate seamlessly with:
    - Haive core schema system for state management
    - Base conversation infrastructure for orchestration
    - Moderator AI systems for intelligent flow control
    - Content analysis tools for context-aware selection
    - Educational and training platforms

Examples:
    For comprehensive examples, see the documentation and examples directory:
    - examples/directed_interview.py
    - examples/directed_panel.py
    - examples/directed_qa_session.py
    - examples/directed_investigation.py

See Also:
    - :class:`~haive.agents.conversation.base.agent.BaseConversationAgent`: Parent class
    - :class:`~haive.agents.conversation.base.state.ConversationState`: Base state management
    - :class:`~haive.agents.conversation.round_robin.agent.RoundRobinConversation`: Fixed order alternative
    - :class:`~haive.agents.conversation.debate.agent.DebateConversation`: Structured argument alternative

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
    Literal,
    Optional,
    Union,
)

from typing_extensions import NotRequired, TypeAlias, TypedDict

if TYPE_CHECKING:
    from haive.agents.conversation.base.agent import BaseConversationAgent
    from haive.agents.conversation.base.state import ConversationState

# Core imports
from haive.agents.conversation.directed.agent import DirectedConversation
from haive.agents.conversation.directed.state import DirectedState

# Type aliases for directed conversations
DirectedParticipant: TypeAlias = Any  # Agent with conversation capabilities
ModeratorAgent: TypeAlias = Any  # Agent with moderation capabilities
ConversationFormat: TypeAlias = Literal[
    "interview", "panel", "qa", "seminar", "investigation"
]
SelectionStrategy: TypeAlias = Literal[
    "content_based", "expertise_based", "round_robin_fallback", "random", "custom"
]
DirectedResult: TypeAlias = dict[str, Any]  # Conversation outcome and flow data


# Configuration types for directed conversations
class DirectedConfiguration(TypedDict, total=False):
    """Configuration for directed conversations."""

    conversation_format: NotRequired[ConversationFormat]
    selection_strategy: NotRequired[SelectionStrategy]
    moderator_instructions: NotRequired[str]
    follow_up_probability: NotRequired[float]
    max_consecutive_turns: NotRequired[int]
    enable_flow_reasoning: NotRequired[bool]
    balance_participation: NotRequired[bool]


class ModeratorConfig(TypedDict, total=False):
    """Configuration for moderator behavior."""

    selection_reasoning: NotRequired[bool]
    context_window_size: NotRequired[int]
    expertise_mapping: NotRequired[dict[str, list[str]]]
    flow_goals: NotRequired[list[str]]


# Define public API
__all__ = [
    "ConversationFormat",
    # Configuration types
    "DirectedConfiguration",
    # Core classes
    "DirectedConversation",
    # Type aliases
    "DirectedParticipant",
    "DirectedResult",
    "DirectedState",
    "ModeratorAgent",
    "ModeratorConfig",
    "SelectionStrategy",
    "__author__",
    "__license__",
    # Version information
    "__version__",
    # Utility functions
    "create_directed_conversation",
    "create_interview",
    "create_panel_discussion",
    "validate_moderator_setup",
]


# Utility functions
def create_directed_conversation(
    moderator: ModeratorAgent,
    participants: list[DirectedParticipant],
    topic: str,
    conversation_format: ConversationFormat = "panel",
    config: DirectedConfiguration | None = None,
) -> DirectedConversation:
    r"""Create a directed conversation with moderator control.

    Args:
        moderator: Moderator agent controlling conversation flow
        participants: List of participant agents
        topic: Conversation topic
        conversation_format: Format of the conversation
        config: Optional conversation configuration

    Returns:
        Configured DirectedConversation instance

    Examples:
        Basic directed conversation::\n

            conversation = create_directed_conversation(
                moderator=moderator_agent,
                participants=[expert1, expert2, expert3],
                topic="Future of Technology",
                conversation_format="panel"
            )

        Advanced configuration::\n

            conversation = create_directed_conversation(
                moderator=interviewer,
                participants=[subject1, subject2],
                topic="Research findings",
                conversation_format="interview",
                config={
                    "selection_strategy": "expertise_based",
                    "follow_up_probability": 0.7,
                    "balance_participation": True
                }
            )
    """
    config = config or {}

    return DirectedConversation(
        moderator=moderator,
        participants=participants,
        topic=topic,
        conversation_format=conversation_format,
        **config,
    )


def create_interview(
    interviewer: ModeratorAgent,
    interviewees: list[DirectedParticipant],
    topic: str,
    max_rounds: int = 10,
    config: DirectedConfiguration | None = None,
) -> DirectedConversation:
    r"""Create an interview-style directed conversation.

    Args:
        interviewer: Interviewer agent (acts as moderator)
        interviewees: List of interviewee agents
        topic: Interview topic
        max_rounds: Maximum number of conversation rounds
        config: Optional interview configuration

    Returns:
        Configured interview DirectedConversation

    Examples:
        Simple interview::\n

            interview = create_interview(
                interviewer=journalist,
                interviewees=[expert1, expert2],
                topic="Climate Change Impacts",
                max_rounds=8
            )

        Interview with follow-up control::\n

            interview = create_interview(
                interviewer=researcher,
                interviewees=[participant1, participant2, participant3],
                topic="User Experience Study",
                config={
                    "follow_up_probability": 0.8,
                    "max_consecutive_turns": 2
                }
            )
    """
    config = config or {}

    return DirectedConversation(
        moderator=interviewer,
        participants=interviewees,
        topic=topic,
        conversation_format="interview",
        max_rounds=max_rounds,
        **config,
    )


def create_panel_discussion(
    moderator: ModeratorAgent,
    panelists: list[DirectedParticipant],
    topic: str,
    expertise_areas: dict[str, list[str]] | None = None,
) -> DirectedConversation:
    r"""Create a panel discussion with expert moderation.

    Args:
        moderator: Panel moderator agent
        panelists: List of panelist agents
        topic: Discussion topic
        expertise_areas: Optional mapping of panelists to expertise areas

    Returns:
        Configured panel DirectedConversation

    Examples:
        Expert panel discussion::\n

            panel = create_panel_discussion(
                moderator=panel_moderator,
                panelists=[scientist, economist, policy_expert],
                topic="Sustainable Development Goals",
                expertise_areas={
                    "scientist": ["climate", "environment"],
                    "economist": ["finance", "markets"],
                    "policy_expert": ["governance", "regulation"]
                }
            )
    """
    config: DirectedConfiguration = {
        "selection_strategy": "expertise_based",
        "balance_participation": True,
        "enable_flow_reasoning": True,
    }

    if expertise_areas:
        config["moderator_instructions"] = f"Use expertise mapping: {expertise_areas}"

    return DirectedConversation(
        moderator=moderator,
        participants=panelists,
        topic=topic,
        conversation_format="panel",
        **config,
    )


def validate_moderator_setup(
    moderator: ModeratorAgent, participants: list[DirectedParticipant]
) -> bool:
    """Validate moderator and participant setup for directed conversation.

    Args:
        moderator: Moderator agent to validate
        participants: List of participant agents

    Returns:
        True if setup is valid for directed conversation

    Raises:
        ValueError: If validation fails with specific error details
    """
    # Validate moderator
    if not hasattr(moderator, "name"):
        raise ValueError("Moderator missing required 'name' attribute")

    if not hasattr(moderator, "arun"):
        raise ValueError("Moderator missing required 'arun' method")

    # Validate participants
    if len(participants) < 1:
        raise ValueError("Directed conversation requires at least one participant")

    for i, participant in enumerate(participants):
        if not hasattr(participant, "name"):
            raise ValueError(f"Participant {i} missing required 'name' attribute")

        if not hasattr(participant, "arun"):
            raise ValueError(f"Participant {i} missing required 'arun' method")

    # Check for unique names
    all_agents = [moderator, *participants]
    names = [getattr(agent, "name", f"agent_{i}") for i, agent in enumerate(all_agents)]
    if len(names) != len(set(names)):
        duplicates = [name for name in names if names.count(name) > 1]
        raise ValueError(f"Duplicate agent names found: {duplicates}")

    return True


def __dir__() -> list[str]:
    """Override dir() to show only public API."""
    return __all__


# Add convenience functions to global namespace
create_directed_conversation.__module__ = __name__
create_interview.__module__ = __name__
create_panel_discussion.__module__ = __name__
validate_moderator_setup.__module__ = __name__
