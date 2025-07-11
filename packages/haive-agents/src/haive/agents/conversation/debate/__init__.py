r"""Debate Conversation - Structured Argumentative Multi-Agent Dialogue.

Structured debate agent with formal positions, arguments, rebuttals, and judging
systems. The debate conversation implements a formal debate structure where participants
argue from assigned positions following a multi-phase conversational format with
automatic phase management and scoring capabilities.

Architecture:
    The debate conversation extends BaseConversationAgent with specialized state
    management for structured debates, including position tracking, argument
    counting, phase progression, and optional judging systems. This provides
    a comprehensive framework for formal argumentative discourse.

Key Features:
    - Multiple debate formats (traditional, oxford, parliamentary, lincoln-douglas)
    - Configurable debate phases with automatic progression
    - Position assignment and tracking with role-based speaking
    - Automatic argument and rebuttal counting per participant
    - Optional judge participant for scoring and feedback
    - Comprehensive debate statistics and results analysis
    - Phase-based flow control with customizable rules
    - Argument strength assessment and evaluation metrics

Core Components:
    DebateConversation: Main agent class that orchestrates structured debates
        with position-based speaking, phase management, and scoring systems.
    DebateState: Specialized state schema extending ConversationState with
        debate-specific fields for positions, phases, and argument tracking.

Debate Phases:
    1. **Opening Statements**: Initial position presentations
    2. **Main Arguments**: Core argumentative content with time limits
    3. **Cross-Examination**: Direct questioning between opposing sides
    4. **Rebuttals**: Responses to opposing arguments with counter-points
    5. **Closing Statements**: Final position summaries and appeals
    6. **Judging**: Optional evaluation and winner determination

Usage Patterns:
    Basic two-sided debate::\n

        from haive.agents.conversation import DebateConversation
        from haive.agents.simple import SimpleAgent

        # Create debate participants
        pro_agent = SimpleAgent(name="ProAI", role="proponent")
        con_agent = SimpleAgent(name="ConAI", role="opponent")
        judge_agent = SimpleAgent(name="Judge", role="judge")

        # Create structured debate
        debate = DebateConversation(
            topic="Artificial Intelligence Benefits Outweigh Risks",
            pro_agents=[pro_agent],
            con_agents=[con_agent],
            judge_agent=judge_agent,
            debate_format="traditional",
            rounds=3
        )

        # Run the debate
        result = await debate.arun()

        # Access debate results
        messages = result["messages"]
        winner = result["debate_winner"]
        scores = result["argument_scores"]

    Multi-participant debate::\n

        # Oxford-style debate with multiple participants per side
        debate = DebateConversation(
            topic="Climate Change Requires Immediate Action",
            pro_agents=[scientist, activist, policy_expert],
            con_agents=[economist, skeptic, industry_rep],
            debate_format="oxford",
            arguments_per_participant=2,
            enable_cross_examination=True
        )

    Factory method for quick setup::\n

        # Create a simple debate with automatic participant creation
        debate = DebateConversation.create_simple_debate(
            topic="Universal Basic Income Should Be Implemented",
            position_a=("Supporter", "UBI provides economic security"),
            position_b=("Critic", "UBI creates dependency and inflation"),
            enable_judge=True,
            arguments_per_side=3
        )

Debate Formats:
    - **Traditional**: Opening, arguments, rebuttals, closing
    - **Oxford**: Formal university-style with cross-examination
    - **Parliamentary**: Government vs. opposition with points of order
    - **Lincoln-Douglas**: Value-based philosophical debates
    - **Policy**: Evidence-based policy analysis debates

Position Management:
    The debate system automatically manages position assignments and ensures
    balanced participation through role-based speaking order and argument
    tracking. Each participant is assigned a position and speaks according
    to debate format rules and phase requirements.

Scoring and Evaluation:
    Optional judge agents can evaluate arguments based on:
    - Logical consistency and evidence quality
    - Persuasiveness and rhetorical effectiveness
    - Response to opposing arguments
    - Overall debate performance and conduct

Use Cases:
    - Exploring different perspectives on complex topics
    - Creating balanced discussions with formal structure
    - Educational simulations of debate formats
    - Testing argument strength and persuasive capabilities
    - Training agents in argumentative reasoning
    - Policy analysis and decision-making support

Integration:
    Debate conversations integrate seamlessly with:
    - Haive core schema system for specialized state management
    - Base conversation infrastructure for orchestration
    - Scoring and evaluation systems for argument assessment
    - Research tools for evidence gathering and fact-checking
    - Educational platforms for learning and training

Examples:
    For comprehensive examples, see the documentation and examples directory:
    - examples/debate_traditional.py
    - examples/debate_oxford_style.py
    - examples/debate_with_judging.py
    - examples/debate_multi_participant.py

See Also:
    - :class:`~haive.agents.conversation.base.agent.BaseConversationAgent`: Parent class
    - :class:`~haive.agents.conversation.base.state.ConversationState`: Base state management
    - :class:`~haive.agents.conversation.directed.agent.DirectedConversation`: Moderated alternative
    - :class:`~haive.agents.conversation.round_robin.agent.RoundRobinConversation`: Sequential alternative

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
from haive.agents.conversation.debate.agent import DebateConversation
from haive.agents.conversation.debate.state import DebateState

# Type aliases for debate conversations
DebateParticipant: TypeAlias = Any  # Agent with debate capabilities
DebatePosition: TypeAlias = Literal["pro", "con", "judge", "moderator"]
DebateFormat: TypeAlias = Literal[
    "traditional", "oxford", "parliamentary", "lincoln-douglas", "policy"
]
DebatePhase: TypeAlias = Literal[
    "opening", "arguments", "cross_exam", "rebuttals", "closing", "judging"
]
DebateResult: TypeAlias = dict[str, Any]  # Debate outcome and statistics


# Configuration types for debates
class DebateConfiguration(TypedDict, total=False):
    """Configuration for debate conversations."""

    debate_format: NotRequired[DebateFormat]
    arguments_per_participant: NotRequired[int]
    rebuttal_rounds: NotRequired[int]
    time_limit_per_argument: NotRequired[float]
    enable_cross_examination: NotRequired[bool]
    enable_judge_scoring: NotRequired[bool]
    scoring_criteria: NotRequired[list[str]]


class DebatePositionConfig(TypedDict, total=False):
    """Configuration for debate positions."""

    position_name: NotRequired[str]
    position_description: NotRequired[str]
    required_arguments: NotRequired[int]
    speaking_order: NotRequired[int]


# Define public API
__all__ = [
    # Configuration types
    "DebateConfiguration",
    # Core classes
    "DebateConversation",
    "DebateFormat",
    # Type aliases
    "DebateParticipant",
    "DebatePhase",
    "DebatePosition",
    "DebatePositionConfig",
    "DebateResult",
    "DebateState",
    "__author__",
    "__license__",
    # Version information
    "__version__",
    # Utility functions
    "create_debate",
    "create_oxford_debate",
    "create_traditional_debate",
    "validate_debate_participants",
]


# Utility functions
def create_debate(
    topic: str,
    pro_agents: list[DebateParticipant],
    con_agents: list[DebateParticipant],
    judge_agent: DebateParticipant | None = None,
    debate_format: DebateFormat = "traditional",
    config: DebateConfiguration | None = None,
) -> DebateConversation:
    r"""Create a structured debate conversation.

    Args:
        topic: Debate topic or resolution
        pro_agents: Agents arguing for the proposition
        con_agents: Agents arguing against the proposition
        judge_agent: Optional judge agent for scoring
        debate_format: Format of the debate
        config: Optional debate configuration

    Returns:
        Configured DebateConversation instance

    Examples:
        Basic debate::\n

            debate = create_debate(
                topic="AI should be regulated",
                pro_agents=[regulatory_expert],
                con_agents=[tech_advocate],
                judge_agent=neutral_judge
            )

        Advanced debate with configuration::\n

            debate = create_debate(
                topic="Climate change requires immediate action",
                pro_agents=[scientist, activist],
                con_agents=[economist, skeptic],
                debate_format="oxford",
                config={
                    "arguments_per_participant": 3,
                    "enable_cross_examination": True,
                    "time_limit_per_argument": 300
                }
            )
    """
    config = config or {}

    return DebateConversation(
        topic=topic,
        pro_agents=pro_agents,
        con_agents=con_agents,
        judge_agent=judge_agent,
        debate_format=debate_format,
        **config,
    )


def create_traditional_debate(
    topic: str,
    pro_agent: DebateParticipant,
    con_agent: DebateParticipant,
    judge_agent: DebateParticipant | None = None,
    rounds: int = 3,
) -> DebateConversation:
    r"""Create a traditional two-participant debate.

    Args:
        topic: Debate topic or resolution
        pro_agent: Agent arguing for the proposition
        con_agent: Agent arguing against the proposition
        judge_agent: Optional judge agent for scoring
        rounds: Number of argument rounds

    Returns:
        Configured traditional DebateConversation

    Examples:
        Simple traditional debate::\n

            debate = create_traditional_debate(
                topic="Social media does more harm than good",
                pro_agent=social_critic,
                con_agent=tech_optimist,
                judge_agent=media_expert,
                rounds=3
            )
    """
    return DebateConversation(
        topic=topic,
        pro_agents=[pro_agent],
        con_agents=[con_agent],
        judge_agent=judge_agent,
        debate_format="traditional",
        rounds=rounds,
    )


def create_oxford_debate(
    topic: str,
    pro_team: list[DebateParticipant],
    con_team: list[DebateParticipant],
    moderator: DebateParticipant | None = None,
) -> DebateConversation:
    r"""Create an Oxford-style debate with teams.

    Args:
        topic: Debate resolution
        pro_team: Team arguing for the proposition
        con_team: Team arguing against the proposition
        moderator: Optional moderator for flow control

    Returns:
        Configured Oxford-style DebateConversation

    Examples:
        Oxford debate with teams::\n

            debate = create_oxford_debate(
                topic="This house believes AI will replace human creativity",
                pro_team=[ai_researcher, tech_futurist, innovation_expert],
                con_team=[artist, philosopher, human_advocate],
                moderator=debate_moderator
            )
    """
    return DebateConversation(
        topic=topic,
        pro_agents=pro_team,
        con_agents=con_team,
        moderator_agent=moderator,
        debate_format="oxford",
        enable_cross_examination=True,
    )


def validate_debate_participants(
    pro_agents: list[DebateParticipant],
    con_agents: list[DebateParticipant],
    judge_agent: DebateParticipant | None = None,
) -> bool:
    """Validate debate participants for proper configuration.

    Args:
        pro_agents: Agents arguing for the proposition
        con_agents: Agents arguing against the proposition
        judge_agent: Optional judge agent

    Returns:
        True if participants are valid for debate

    Raises:
        ValueError: If validation fails with specific error details
    """
    if not pro_agents:
        raise ValueError("Debate requires at least one pro agent")

    if not con_agents:
        raise ValueError("Debate requires at least one con agent")

    # Check for participant capabilities
    all_participants = pro_agents + con_agents
    if judge_agent:
        all_participants.append(judge_agent)

    for i, participant in enumerate(all_participants):
        if not hasattr(participant, "name"):
            raise ValueError(f"Participant {i} missing required 'name' attribute")

        if not hasattr(participant, "arun"):
            raise ValueError(f"Participant {i} missing required 'arun' method")

    # Check for unique names
    names = [
        getattr(p, "name", f"participant_{i}") for i, p in enumerate(all_participants)
    ]
    if len(names) != len(set(names)):
        duplicates = [name for name in names if names.count(name) > 1]
        raise ValueError(f"Duplicate participant names found: {duplicates}")

    return True


def __dir__() -> list[str]:
    """Override dir() to show only public API."""
    return __all__


# Add convenience functions to global namespace
create_debate.__module__ = __name__
create_traditional_debate.__module__ = __name__
create_oxford_debate.__module__ = __name__
validate_debate_participants.__module__ = __name__
