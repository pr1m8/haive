"""Conversation Agents - Multi-Agent Dialogue Orchestration System.

A comprehensive suite of multi-agent conversation orchestrators for facilitating
different types of agent-to-agent interactions and dialogues. This package provides
specialized conversation frameworks that enable multiple agents to interact with each
other according to different patterns, structures, and rules.

Architecture:
    The conversation system is built around a hierarchical architecture:

    - BaseConversationAgent: Core orchestration logic and state management
    - Specialized conversation types: Each with unique interaction patterns
    - Shared state system: Common message handling and flow control
    - Integration layer: Seamless connection with other Haive components

Core Conversation Types:
    BaseConversationAgent: Foundation for all conversation agents with core
        orchestration logic, state management, and message routing capabilities.

    RoundRobinConversation: Simple turn-taking conversation where each agent
        speaks in sequence. Useful for panel discussions and ordered dialogues.

    DirectedConversation: Conversations with a directed flow controlled by a
        moderator. Supports dynamic speaker selection and flow control.

    DebateConversation: Structured debates with positions, arguments, rebuttals,
        and judging. Includes scoring and evaluation mechanisms.

    CollaborativeConversation: Multiple agents collaborating on a shared task.
        Features task decomposition, role assignment, and result synthesis.

    SocialMediaConversation: Simulated social media interactions with posts,
        replies, reactions, and viral propagation patterns.

State Management:
    Each conversation type maintains rich state information including:
    - Participant registry and roles
    - Message history and threading
    - Turn management and flow control
    - Context and memory management
    - Performance metrics and analytics

Usage Patterns:
    Basic Round Robin Conversation::

        from haive.agents.conversation import RoundRobinConversation
        from haive.agents.simple import SimpleAgent

        # Create participants
        alice = SimpleAgent(name="Alice")
        bob = SimpleAgent(name="Bob")
        charlie = SimpleAgent(name="Charlie")

        # Create conversation
        conversation = RoundRobinConversation(
            participants=[alice, bob, charlie],
            topic="Future of AI",
            rounds=3
        )

        # Run conversation
        result = await conversation.arun()

    Structured Debate::

        from haive.agents.conversation import DebateConversation

        debate = DebateConversation(
            topic="Should AI be regulated?",
            pro_agents=[pro_agent1, pro_agent2],
            con_agents=[con_agent1, con_agent2],
            judge_agent=judge_agent,
            rounds=5
        )

        result = await debate.arun()
        winner = result.get("winner")

    Collaborative Task::

        from haive.agents.conversation import CollaborativeConversation

        collaboration = CollaborativeConversation(
            participants={
                "designer": designer_agent,
                "engineer": engineer_agent,
                "product_manager": pm_agent
            },
            task="Design a new mobile app",
            deliverables=["mockup", "specs", "timeline"]
        )

        result = await collaboration.arun()

Advanced Features:
    - Dynamic participant addition/removal
    - Conversation branching and merging
    - Real-time conversation monitoring
    - Conversation recording and playback
    - Integration with external chat systems
    - Conversation analytics and insights

Integration:
    Conversation agents integrate seamlessly with:
    - Haive core schema system for state management
    - Graph-based workflow execution
    - Tool integration for enhanced capabilities
    - Persistence systems for conversation history
    - Monitoring and analytics platforms

Examples:
    For comprehensive examples, see the documentation and examples directory:
    - examples/basic_round_robin.py
    - examples/structured_debate.py
    - examples/collaborative_design.py
    - examples/social_media_simulation.py

See Also:
    - :mod:`~haive.agents.base.agent`: Base agent classes that conversation agents extend
    - :mod:`~haive.agents.simple.agent`: Simple agent used for conversation participants
    - :mod:`~haive.core.graph.state_graph`: State graph system for conversation flow
    - :mod:`~haive.core.schema`: State schema system for conversation state

Version: 1.0.0
Author: Haive Team
License: MIT
"""

# Version information
__version__ = "1.0.0"
__author__ = "Haive Team"
__license__ = "MIT"

from collections.abc import Callable

# Type imports for better IDE support
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Literal,
    NotRequired,
    Optional,
    Protocol,
    Type,
    TypeAlias,
    Union,
    runtime_checkable,
)

from typing_extensions import (
    TypedDict,
)

if TYPE_CHECKING:
    from haive.core.schema import StateSchema

    from haive.agents.base.agent import Agent

# Core conversation agent imports
from haive.agents.conversation.base.agent import BaseConversationAgent
from haive.agents.conversation.collaberative.agent import CollaborativeConversation
from haive.agents.conversation.debate.agent import DebateConversation
from haive.agents.conversation.directed.agent import DirectedConversation
from haive.agents.conversation.round_robin.agent import RoundRobinConversation
from haive.agents.conversation.social_media.agent import SocialMediaConversation

# Type aliases for better API clarity
ConversationType: TypeAlias = Literal[
    "round_robin", "directed", "debate", "collaborative", "social_media"
]
ParticipantRole: TypeAlias = Literal["speaker", "moderator", "judge", "observer"]
ConversationStatus: TypeAlias = Literal[
    "pending", "active", "paused", "completed", "cancelled"
]
MessageType: TypeAlias = Literal[
    "statement", "question", "response", "argument", "rebuttal", "judgment"
]


# Protocol definitions for type safety
@runtime_checkable
class ConversationParticipant(Protocol):
    """Protocol for agents that can participate in conversations."""

    name: str

    async def arun(self, input_data: Any) -> Any:
        """Run the agent with input data."""
        ...

    def get_role(self) -> ParticipantRole:
        """Get the participant's role in the conversation."""
        ...


# Configuration types
class ConversationConfig(TypedDict, total=False):
    """Configuration for conversation agents."""

    max_turns: NotRequired[int]
    timeout_seconds: NotRequired[float]
    auto_moderation: NotRequired[bool]
    save_history: NotRequired[bool]
    allow_interruptions: NotRequired[bool]


class DebateConfig(ConversationConfig, total=False):
    """Configuration specific to debate conversations."""

    rounds: NotRequired[int]
    time_per_round: NotRequired[float]
    scoring_system: NotRequired[str]
    allow_rebuttals: NotRequired[bool]


class CollaborativeConfig(ConversationConfig, total=False):
    """Configuration specific to collaborative conversations."""

    task_decomposition: NotRequired[bool]
    role_assignment: NotRequired[dict[str, str]]
    deliverables: NotRequired[list[str]]
    progress_tracking: NotRequired[bool]


# Define public API
__all__ = [
    # Core conversation agents
    "BaseConversationAgent",
    "CollaborativeConfig",
    "CollaborativeConversation",
    # Configuration types
    "ConversationConfig",
    # Protocols
    "ConversationParticipant",
    "ConversationStatus",
    # Type aliases
    "ConversationType",
    "DebateConfig",
    "DebateConversation",
    "DirectedConversation",
    "MessageType",
    "ParticipantRole",
    "RoundRobinConversation",
    "SocialMediaConversation",
    "__author__",
    "__license__",
    # Version information
    "__version__",
    "create_collaboration",
    # Convenience functions
    "create_conversation",
    "create_debate",
    "get_conversation_types",
    "validate_participants",
]


# Module initialization
def _initialize_conversation_module() -> None:
    """Initialize the conversation module with default configurations."""
    import logging

    # Set up logging for conversation operations
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Validate critical dependencies
    try:
        from haive.core.schema import StateSchema

        from haive.agents.base.agent import Agent
    except ImportError as e:
        raise ImportError(
            f"Critical conversation dependencies missing: {e.name}. "
            f"Please install with: pip install haive-agents[conversation]"
        )


# Convenience factory functions
def create_conversation(
    conversation_type: ConversationType,
    participants: list[ConversationParticipant],
    topic: str,
    config: ConversationConfig | None = None,
    **kwargs: Any,
) -> BaseConversationAgent:
    """Create a conversation agent of the specified type.

    Args:
        conversation_type: Type of conversation to create
        participants: List of agents to participate in the conversation
        topic: Topic or subject of the conversation
        config: Optional configuration for the conversation
        **kwargs: Additional keyword arguments specific to the conversation type

    Returns:
        Configured conversation agent

    Examples:
        Round robin conversation::

            conversation = create_conversation(
                "round_robin",
                participants=[alice, bob, charlie],
                topic="Future of AI",
                config={"max_turns": 10}
            )

        Debate conversation::

            debate = create_conversation(
                "debate",
                participants=[pro_agent, con_agent],
                topic="Should AI be regulated?",
                judge_agent=judge_agent,
                rounds=3
            )
    """
    config = config or {}

    if conversation_type == "round_robin":
        return RoundRobinConversation(
            participants=participants, topic=topic, **config, **kwargs
        )
    if conversation_type == "directed":
        return DirectedConversation(
            participants=participants, topic=topic, **config, **kwargs
        )
    if conversation_type == "debate":
        return DebateConversation(topic=topic, **config, **kwargs)
    if conversation_type == "collaborative":
        return CollaborativeConversation(
            participants=participants, topic=topic, **config, **kwargs
        )
    if conversation_type == "social_media":
        return SocialMediaConversation(
            participants=participants, topic=topic, **config, **kwargs
        )
    raise ValueError(f"Unknown conversation type: {conversation_type}")


def create_debate(
    topic: str,
    pro_agents: list[ConversationParticipant],
    con_agents: list[ConversationParticipant],
    judge_agent: ConversationParticipant | None = None,
    rounds: int = 3,
    config: DebateConfig | None = None,
) -> DebateConversation:
    """Create a structured debate conversation.

    Args:
        topic: Topic to debate
        pro_agents: Agents arguing for the topic
        con_agents: Agents arguing against the topic
        judge_agent: Optional judge agent to score the debate
        rounds: Number of debate rounds
        config: Optional debate configuration

    Returns:
        Configured debate conversation

    Examples:
        Simple debate::

            debate = create_debate(
                topic="Should AI be regulated?",
                pro_agents=[regulatory_expert],
                con_agents=[tech_advocate],
                judge_agent=neutral_judge
            )

        Multi-participant debate::

            debate = create_debate(
                topic="Climate change solutions",
                pro_agents=[scientist1, activist],
                con_agents=[economist, skeptic],
                rounds=5,
                config={"time_per_round": 300}
            )
    """
    config = config or {}

    return DebateConversation(
        topic=topic,
        pro_agents=pro_agents,
        con_agents=con_agents,
        judge_agent=judge_agent,
        rounds=rounds,
        **config,
    )


def create_collaboration(
    task: str,
    participants: dict[str, ConversationParticipant],
    deliverables: list[str] | None = None,
    config: CollaborativeConfig | None = None,
) -> CollaborativeConversation:
    """Create a collaborative conversation for team tasks.

    Args:
        task: Task description for the collaboration
        participants: Dictionary mapping roles to participant agents
        deliverables: Optional list of expected deliverables
        config: Optional collaboration configuration

    Returns:
        Configured collaborative conversation

    Examples:
        Software development team::

            collaboration = create_collaboration(
                task="Design a new mobile app",
                participants={
                    "designer": ui_designer,
                    "engineer": developer,
                    "product_manager": pm
                },
                deliverables=["mockup", "specs", "timeline"]
            )

        Research team::

            collaboration = create_collaboration(
                task="Analyze market trends",
                participants={
                    "analyst": data_analyst,
                    "researcher": market_researcher,
                    "strategist": business_strategist
                },
                config={"progress_tracking": True}
            )
    """
    config = config or {}

    return CollaborativeConversation(
        task=task, participants=participants, deliverables=deliverables or [], **config
    )


def validate_participants(
    participants: list[ConversationParticipant],
    min_participants: int = 2,
    max_participants: int | None = None,
) -> bool:
    """Validate that participants meet conversation requirements.

    Args:
        participants: List of participant agents
        min_participants: Minimum number of participants required
        max_participants: Maximum number of participants allowed

    Returns:
        True if participants are valid, False otherwise

    Raises:
        ValueError: If validation fails with specific error details
    """
    if len(participants) < min_participants:
        raise ValueError(
            f"Conversation requires at least {min_participants} participants, "
            f"got {len(participants)}"
        )

    if max_participants and len(participants) > max_participants:
        raise ValueError(
            f"Conversation allows at most {max_participants} participants, "
            f"got {len(participants)}"
        )

    # Check that all participants implement the protocol
    for i, participant in enumerate(participants):
        if not isinstance(participant, ConversationParticipant):
            raise ValueError(
                f"Participant {i} does not implement ConversationParticipant protocol"
            )

    # Check for unique names
    names = [p.name for p in participants]
    if len(names) != len(set(names)):
        duplicates = [name for name in names if names.count(name) > 1]
        raise ValueError(f"Duplicate participant names found: {duplicates}")

    return True


def get_conversation_types() -> list[ConversationType]:
    """Get list of available conversation types.

    Returns:
        List of available conversation type strings
    """
    return ["round_robin", "directed", "debate", "collaborative", "social_media"]


def __dir__() -> list[str]:
    """Override dir() to show only public API."""
    return __all__


# Initialize module
_initialize_conversation_module()

# Add convenience functions to global namespace
create_conversation.__module__ = __name__
create_debate.__module__ = __name__
create_collaboration.__module__ = __name__
validate_participants.__module__ = __name__
get_conversation_types.__module__ = __name__
