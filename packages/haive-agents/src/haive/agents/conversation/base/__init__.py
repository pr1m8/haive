r"""Base Conversation Agent - Multi-Agent Orchestration Foundation.

Core foundation classes for conversation agents that orchestrate multi-agent interactions.
This module provides the base infrastructure for all conversation agent types, with a
focus on robust multi-agent conversation orchestration, automatic state tracking with
reducers, phase-based conversation management, and extensible graph-based conversation flow.

Architecture:
    The base conversation system is built around a hierarchical architecture:

    - BaseConversationAgent: Abstract orchestration foundation with speaker selection,
        agent execution, and extension hooks for customizable conversation patterns.
    - ConversationState: State schema with automatic tracking for conversation rounds,
        speaker history, and message accumulation using reducer-based state management.
    - Integration layer: Seamless connection with Haive core systems and graph workflows.

Core Components:
    BaseConversationAgent: Abstract base agent that implements the core conversation
        flow logic, speaker selection, agent execution, and extension hooks.
        Provides the foundation for all conversation types while maintaining
        consistent orchestration patterns.

    ConversationState: State schema with automatic tracking for conversation rounds,
        speaker history, and message accumulation using reducers. Includes computed
        properties for conversation progress and round management.

Key Features:
    - Multi-agent conversation orchestration with automatic turn management
    - Reducer-based automatic state tracking for rounds and speaker history
    - Phase-based conversation management with customizable flow control
    - Message routing and agent execution with error handling
    - Extensible graph-based conversation flow for complex patterns
    - Computed properties for conversation progress and state analysis
    - Integration with Haive core schema and graph systems

Conversation Types:
    All conversation types in the package extend these base classes to implement their
    specific conversation patterns while inheriting the core orchestration mechanisms:

    - Round Robin: Turn-taking conversations with ordered speaker rotation
    - Debate: Structured debate conversations with positions and judging
    - Directed: Moderator-controlled conversations with dynamic flow
    - Collaborative: Task-focused collaborative conversations with role coordination
    - Social Media: Social media-style interactions with post/reply patterns

Usage Patterns:
    Basic conversation state setup::\n

        from haive.agents.conversation.base import ConversationState

        # Create state with automatic tracking
        state = ConversationState(
            speakers=["Alice", "Bob", "Charlie"],
            topic="Future of AI",
            max_rounds=5
        )

        # State automatically tracks turns and rounds
        print(f"Round {state.round_number}, Turn {state.turn_count}")
        print(f"Progress: {state.conversation_progress:.1%}")

    Extending BaseConversationAgent::\n

        from haive.agents.conversation.base import BaseConversationAgent

        class CustomConversationAgent(BaseConversationAgent[ConversationState]):
            def select_next_speaker(self, state: ConversationState) -> str:
                # Custom speaker selection logic
                return state.remaining_speakers_this_round[0]

            def should_end_conversation(self, state: ConversationState) -> bool:
                # Custom termination conditions
                return state.should_end_by_rounds or len(state.messages) > 50

Integration:
    Base conversation components integrate seamlessly with:
    - Haive core schema system for state management
    - Graph-based workflow execution with automatic state updates
    - Message handling and routing systems
    - Agent lifecycle management and error handling
    - Performance monitoring and conversation analytics

Examples:
    For comprehensive examples, see the documentation and examples directory:
    - examples/base_conversation_usage.py
    - examples/custom_conversation_patterns.py
    - examples/state_tracking_demo.py

See Also:
    - :class:`~haive.agents.base.agent.Agent`: Parent class that BaseConversationAgent extends
    - :class:`~haive.agents.simple.agent.SimpleAgent`: Used for conversation participants
    - :class:`~haive.core.schema.state_schema.StateSchema`: Parent class of ConversationState
    - :class:`~haive.core.schema.prebuilt.messages_state.MessagesState`: Base state for ConversationState

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
    Protocol,
    Type,
    Union,
    runtime_checkable,
)

from typing_extensions import NotRequired, TypeAlias, TypedDict

if TYPE_CHECKING:
    from langchain_core.messages import BaseMessage

    from haive.agents.base.agent import Agent

# Core imports
from haive.agents.conversation.base.agent import BaseConversationAgent
from haive.agents.conversation.base.state import ConversationState

# Type aliases for better API clarity
ConversationParticipant: TypeAlias = Any  # Agent with conversation capabilities
SpeakerName: TypeAlias = str
ConversationTopic: TypeAlias = str
RoundNumber: TypeAlias = int
TurnCount: TypeAlias = int


# Protocol definitions for type safety
@runtime_checkable
class ConversationCapable(Protocol):
    """Protocol for agents that can participate in base conversations."""

    name: str

    async def arun(self, input_data: Any) -> Any:
        """Run the agent with input data."""
        ...

    def can_participate_in_conversation(self) -> bool:
        """Check if agent can participate in conversations."""
        ...


# Configuration types for base conversation
class BaseConversationConfig(TypedDict, total=False):
    """Configuration for base conversation agents."""

    max_rounds: NotRequired[int]
    timeout_seconds: NotRequired[float]
    enable_progress_tracking: NotRequired[bool]
    auto_end_on_round_limit: NotRequired[bool]
    speaker_selection_strategy: NotRequired[str]


# Define public API
__all__ = [
    # Core classes
    "BaseConversationAgent",
    # Configuration types
    "BaseConversationConfig",
    # Protocols
    "ConversationCapable",
    # Type aliases
    "ConversationParticipant",
    "ConversationState",
    "ConversationTopic",
    "RoundNumber",
    "SpeakerName",
    "TurnCount",
    "__author__",
    "__license__",
    # Version information
    "__version__",
    "create_conversation_state",
    "get_conversation_progress",
    # Utility functions
    "validate_conversation_participants",
]


# Module initialization
def _initialize_base_conversation_module() -> None:
    """Initialize the base conversation module with default configurations."""
    import logging

    # Set up logging for conversation operations
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Validate critical dependencies
    try:
        from haive.core.schema.prebuilt.messages_state import MessagesState
        from langchain_core.messages import BaseMessage

        from haive.agents.base.agent import Agent
    except ImportError as e:
        raise ImportError(
            f"Critical base conversation dependencies missing: {e.name}. "
            f"Please install with: pip install haive-agents[conversation]"
        )


# Utility functions
def validate_conversation_participants(
    participants: list[ConversationParticipant], min_participants: int = 2
) -> bool:
    """Validate that participants can engage in conversations.

    Args:
        participants: List of participant agents
        min_participants: Minimum number of participants required

    Returns:
        True if participants are valid for conversations

    Raises:
        ValueError: If validation fails with specific error details
    """
    if len(participants) < min_participants:
        raise ValueError(
            f"Base conversation requires at least {min_participants} participants, "
            f"got {len(participants)}"
        )

    # Check that all participants have required capabilities
    for i, participant in enumerate(participants):
        if not hasattr(participant, "name"):
            raise ValueError(f"Participant {i} missing required 'name' attribute")

        if not hasattr(participant, "arun"):
            raise ValueError(
                f"Participant {i} ({participant.name}) missing required 'arun' method"
            )

    # Check for unique names
    names = [getattr(p, "name", f"participant_{i}") for i, p in enumerate(participants)]
    if len(names) != len(set(names)):
        duplicates = [name for name in names if names.count(name) > 1]
        raise ValueError(f"Duplicate participant names found: {duplicates}")

    return True


def create_conversation_state(
    participants: list[ConversationParticipant],
    topic: str | None = None,
    max_rounds: int = 10,
    mode: str = "base",
    config: BaseConversationConfig | None = None,
) -> ConversationState:
    r"""Create a conversation state with participants and configuration.

    Args:
        participants: List of participant agents
        topic: Optional conversation topic
        max_rounds: Maximum number of conversation rounds
        mode: Conversation mode identifier
        config: Optional additional configuration

    Returns:
        Configured ConversationState instance

    Examples:
        Basic conversation state::\n

            state = create_conversation_state(
                participants=[alice, bob, charlie],
                topic="Future of AI",
                max_rounds=5
            )

        With custom configuration::\n

            state = create_conversation_state(
                participants=[expert1, expert2],
                topic="Technical discussion",
                config={"timeout_seconds": 300}
            )
    """
    # Validate participants
    validate_conversation_participants(participants)

    # Extract speaker names
    speaker_names = [
        getattr(p, "name", f"participant_{i}") for i, p in enumerate(participants)
    ]

    # Apply configuration
    config = config or {}
    final_max_rounds = config.get("max_rounds", max_rounds)

    return ConversationState(
        speakers=speaker_names, topic=topic, max_rounds=final_max_rounds, mode=mode
    )


def get_conversation_progress(state: ConversationState) -> dict[str, Any]:
    """Get detailed progress information for a conversation.

    Args:
        state: ConversationState to analyze

    Returns:
        Dictionary with progress metrics and status
    """
    return {
        "round_number": state.round_number,
        "turn_count": state.turn_count,
        "progress_percentage": state.conversation_progress * 100,
        "total_messages": len(state.messages),
        "speakers_count": len(state.speakers),
        "current_speaker": state.current_speaker,
        "remaining_speakers": state.remaining_speakers_this_round,
        "should_end": state.should_end_by_rounds,
        "conversation_ended": state.conversation_ended,
        "turns_per_round": state.turns_per_round,
    }


def __dir__() -> list[str]:
    """Override dir() to show only public API."""
    return __all__


# Initialize module
_initialize_base_conversation_module()

# Add convenience functions to global namespace
validate_conversation_participants.__module__ = __name__
create_conversation_state.__module__ = __name__
get_conversation_progress.__module__ = __name__
