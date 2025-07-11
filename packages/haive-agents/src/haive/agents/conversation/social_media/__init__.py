r"""Social Media Conversation - Platform-Style Multi-Agent Interactions.

Agent conversations that simulate social media platform interactions with realistic
social dynamics, content engagement, and viral propagation patterns. The social media
conversation implements a specialized conversation pattern that mimics typical social
media platform interactions in a controlled multi-agent environment.

Architecture:
    The social media conversation extends BaseConversationAgent with specialized
    state management for social platform dynamics, including post/reply threading,
    engagement tracking, persona simulation, and content propagation mechanisms.
    This provides a comprehensive framework for studying social media behavior.

Key Features:
    - Posts and threaded replies with realistic conversation branching
    - Reactions, likes, and comprehensive engagement metrics tracking
    - User profiles, personas, and authentic social behavior simulation
    - Content moderation mechanisms and community guidelines enforcement
    - Network effects, viral propagation, and influence patterns
    - Trending topics and hashtag dynamics
    - Real-time engagement and interaction simulations
    - Platform-specific behavior patterns and constraints

Core Components:
    SocialMediaConversation: Main agent class that orchestrates platform-style
        conversations with post threading, engagement tracking, and viral dynamics.
    SocialMediaState: Specialized state schema extending ConversationState with
        social media-specific fields for posts, engagement, and network metrics.

Social Media Dynamics:
    The system simulates authentic social media behavior including:
    - Post creation with content optimization for engagement
    - Reply threading and conversation branching
    - Like, share, and reaction mechanics
    - Follower dynamics and influence propagation
    - Trending content identification and amplification
    - Community formation and interaction patterns

Usage Patterns:
    Twitter-style conversation thread::\n

        from haive.agents.conversation import SocialMediaConversation
        from haive.agents.simple import SimpleAgent

        # Create social media personas
        tech_enthusiast = SimpleAgent(name="TechEnthusiast", persona="tech_early_adopter")
        ai_researcher = SimpleAgent(name="AI_Researcher", persona="academic_expert")
        skeptic = SimpleAgent(name="Skeptic", persona="critical_thinker")
        student = SimpleAgent(name="Student", persona="curious_learner")

        # Create social media conversation
        social_thread = SocialMediaConversation(
            original_poster=tech_enthusiast,
            topic="The Impact of Large Language Models on Education",
            participants=[ai_researcher, skeptic, student],
            platform_type="twitter",
            max_thread_depth=4,
            max_replies_per_post=6
        )

        # Run the conversation
        result = await social_thread.arun()

        # Access conversation data
        thread_structure = result["thread"]
        engagement_metrics = result["engagement_metrics"]
        viral_patterns = result["viral_analysis"]

    Multi-platform simulation::\n

        # Simulate cross-platform discussion
        platforms = ["twitter", "reddit", "linkedin"]

        for platform in platforms:
            social_conv = SocialMediaConversation(
                topic="Remote work trends 2024",
                participants=participant_pool,
                platform_type=platform,
                engagement_algorithms=platform_configs[platform]
            )

        # Platform-specific behavior adaptation
        results = await social_conv.arun()

    Viral content simulation::\n

        # Create viral content experiment
        viral_sim = SocialMediaConversation.create_viral_simulation(
            seed_content="Breaking: Major AI breakthrough announced",
            influencers=[tech_influencer, science_communicator],
            general_users=[user1, user2, user3, user4, user5],
            virality_threshold=0.8,
            simulation_duration=24  # hours
        )

Platform Types:
    - **Twitter**: Short-form posts with hashtags and trending topics
    - **Reddit**: Threaded discussions with upvote/downvote mechanics
    - **LinkedIn**: Professional networking and industry discussions
    - **Facebook**: Social networking with varied content types
    - **Instagram**: Visual content with caption discussions
    - **TikTok**: Short-form video with comment interactions

Engagement Mechanics:
    - Like/reaction tracking with sentiment analysis
    - Share and repost mechanics with attribution
    - Comment threading with conversation branching
    - Follower influence and network amplification
    - Trending algorithm simulation
    - Content recommendation and discovery

Persona System:
    The social media system supports rich persona definitions:
    - Demographic characteristics and interests
    - Communication style and language patterns
    - Engagement preferences and behaviors
    - Influence level and follower count simulation
    - Content creation and consumption patterns

Moderation and Safety:
    - Automated content moderation with configurable rules
    - Community guidelines enforcement
    - Harassment and toxicity detection
    - Content flagging and review processes
    - Misinformation identification and handling

Use Cases:
    - Simulating information spread and viral content dynamics
    - Testing content moderation strategies and policies
    - Exploring social dynamics in online discussions
    - Training agents to recognize and respond to social media patterns
    - Studying influence networks and opinion formation
    - Marketing campaign simulation and optimization
    - Social media crisis management training

Integration:
    Social media conversations integrate seamlessly with:
    - Haive core schema system for state management
    - Base conversation infrastructure for orchestration
    - Content analysis and sentiment tracking tools
    - Network analysis and influence measurement systems
    - Real-time analytics and monitoring platforms

Examples:
    For comprehensive examples, see the documentation and examples directory:
    - examples/social_media_thread.py
    - examples/viral_content_simulation.py
    - examples/platform_comparison.py
    - examples/influence_network_analysis.py

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
from haive.agents.conversation.social_media.agent import SocialMediaConversation
from haive.agents.conversation.social_media.state import SocialMediaState

# Type aliases for social media conversations
SocialMediaParticipant: TypeAlias = Any  # Agent with social media persona capabilities
PlatformType: TypeAlias = Literal[
    "twitter", "reddit", "linkedin", "facebook", "instagram", "tiktok"
]
EngagementAction: TypeAlias = Literal[
    "like", "share", "reply", "repost", "reaction", "follow"
]
ContentType: TypeAlias = Literal["post", "reply", "share", "story", "video", "image"]
ViralityLevel: TypeAlias = Literal["low", "medium", "high", "viral"]
SocialMediaResult: TypeAlias = dict[
    str, Any
]  # Conversation outcome and engagement data


# Configuration types for social media conversations
class SocialMediaConfiguration(TypedDict, total=False):
    """Configuration for social media conversations."""

    platform_type: NotRequired[PlatformType]
    max_thread_depth: NotRequired[int]
    max_replies_per_post: NotRequired[int]
    engagement_algorithms: NotRequired[dict[str, Any]]
    virality_threshold: NotRequired[float]
    moderation_rules: NotRequired[list[str]]
    trending_topics: NotRequired[list[str]]
    character_limit: NotRequired[int]


class PersonaConfig(TypedDict, total=False):
    """Configuration for social media personas."""

    persona_type: NotRequired[str]
    follower_count: NotRequired[int]
    engagement_rate: NotRequired[float]
    posting_frequency: NotRequired[str]
    interests: NotRequired[list[str]]
    communication_style: NotRequired[str]
    influence_level: NotRequired[str]


class EngagementConfig(TypedDict, total=False):
    """Configuration for engagement tracking."""

    track_likes: NotRequired[bool]
    track_shares: NotRequired[bool]
    track_comments: NotRequired[bool]
    track_impressions: NotRequired[bool]
    sentiment_analysis: NotRequired[bool]
    influence_scoring: NotRequired[bool]


# Define public API
__all__ = [
    "ContentType",
    "EngagementAction",
    "EngagementConfig",
    "PersonaConfig",
    "PlatformType",
    # Configuration types
    "SocialMediaConfiguration",
    # Core classes
    "SocialMediaConversation",
    # Type aliases
    "SocialMediaParticipant",
    "SocialMediaResult",
    "SocialMediaState",
    "ViralityLevel",
    "__author__",
    "__license__",
    # Version information
    "__version__",
    "create_reddit_discussion",
    # Utility functions
    "create_social_media_conversation",
    "create_twitter_thread",
    "create_viral_simulation",
    "validate_social_setup",
]


# Utility functions
def create_social_media_conversation(
    topic: str,
    participants: list[SocialMediaParticipant],
    platform_type: PlatformType = "twitter",
    original_poster: SocialMediaParticipant | None = None,
    config: SocialMediaConfiguration | None = None,
) -> SocialMediaConversation:
    r"""Create a social media conversation simulation.

    Args:
        topic: Discussion topic or original post content
        participants: List of participant agents with social personas
        platform_type: Social media platform to simulate
        original_poster: Agent who creates the initial post
        config: Optional social media configuration

    Returns:
        Configured SocialMediaConversation instance

    Examples:
        Basic social media thread::\n

            social_conv = create_social_media_conversation(
                topic="AI ethics in the workplace",
                participants=[tech_expert, ethicist, worker, manager],
                platform_type="linkedin",
                original_poster=tech_expert
            )

        Twitter thread with configuration::\n

            twitter_thread = create_social_media_conversation(
                topic="Breaking news about climate research",
                participants=[scientist, journalist, activist, skeptic],
                platform_type="twitter",
                config={
                    "max_thread_depth": 3,
                    "character_limit": 280,
                    "virality_threshold": 0.7
                }
            )
    """
    config = config or {}

    return SocialMediaConversation(
        topic=topic,
        participants=participants,
        platform_type=platform_type,
        original_poster=original_poster or participants[0],
        **config,
    )


def create_twitter_thread(
    initial_tweet: str,
    participants: list[SocialMediaParticipant],
    max_replies: int = 10,
    enable_hashtags: bool = True,
) -> SocialMediaConversation:
    r"""Create a Twitter-style threaded conversation.

    Args:
        initial_tweet: Content of the initial tweet
        participants: List of Twitter user agents
        max_replies: Maximum number of replies per tweet
        enable_hashtags: Whether to enable hashtag tracking

    Returns:
        Configured Twitter SocialMediaConversation

    Examples:
        Twitter discussion thread::\n

            twitter_thread = create_twitter_thread(
                initial_tweet="Just read about the new AI safety research. Thoughts?",
                participants=[ai_researcher, safety_expert, tech_journalist, curious_user],
                max_replies=15,
                enable_hashtags=True
            )
    """
    config: SocialMediaConfiguration = {
        "platform_type": "twitter",
        "max_replies_per_post": max_replies,
        "character_limit": 280,
        "trending_topics": ["AI", "research", "safety"] if enable_hashtags else [],
    }

    return SocialMediaConversation(
        topic=initial_tweet,
        participants=participants,
        platform_type="twitter",
        original_poster=participants[0],
        **config,
    )


def create_reddit_discussion(
    subreddit_topic: str,
    participants: list[SocialMediaParticipant],
    post_title: str,
    enable_voting: bool = True,
) -> SocialMediaConversation:
    r"""Create a Reddit-style discussion thread.

    Args:
        subreddit_topic: Subreddit theme or topic
        participants: List of Reddit user agents
        post_title: Title of the original post
        enable_voting: Whether to enable upvote/downvote mechanics

    Returns:
        Configured Reddit SocialMediaConversation

    Examples:
        Reddit discussion::\n

            reddit_discussion = create_reddit_discussion(
                subreddit_topic="r/MachineLearning",
                participants=[ml_expert, student, practitioner, researcher],
                post_title="[Discussion] Best practices for model deployment in production",
                enable_voting=True
            )
    """
    config: SocialMediaConfiguration = {
        "platform_type": "reddit",
        "max_thread_depth": 6,
        "engagement_algorithms": {"voting": enable_voting},
        "moderation_rules": ["no_spam", "relevant_content"],
    }

    return SocialMediaConversation(
        topic=f"{subreddit_topic}: {post_title}",
        participants=participants,
        platform_type="reddit",
        original_poster=participants[0],
        **config,
    )


def create_viral_simulation(
    seed_content: str,
    influencers: list[SocialMediaParticipant],
    general_users: list[SocialMediaParticipant],
    virality_threshold: float = 0.8,
    platform_type: PlatformType = "twitter",
) -> SocialMediaConversation:
    r"""Create a viral content propagation simulation.

    Args:
        seed_content: Initial content that may go viral
        influencers: List of high-influence participant agents
        general_users: List of regular user participant agents
        virality_threshold: Threshold for viral propagation
        platform_type: Platform to simulate viral behavior on

    Returns:
        Configured viral SocialMediaConversation

    Examples:
        Viral content simulation::\n

            viral_sim = create_viral_simulation(
                seed_content="BREAKING: Revolutionary AI discovery changes everything",
                influencers=[tech_influencer, science_communicator],
                general_users=[user1, user2, user3, user4, user5],
                virality_threshold=0.9,
                platform_type="twitter"
            )
    """
    all_participants = influencers + general_users

    config: SocialMediaConfiguration = {
        "platform_type": platform_type,
        "virality_threshold": virality_threshold,
        "engagement_algorithms": {
            "amplification": True,
            "influencer_boost": True,
            "network_effects": True,
        },
    }

    return SocialMediaConversation(
        topic=seed_content,
        participants=all_participants,
        platform_type=platform_type,
        original_poster=influencers[0],
        **config,
    )


def validate_social_setup(
    participants: list[SocialMediaParticipant], platform_type: PlatformType
) -> bool:
    """Validate social media conversation setup.

    Args:
        participants: List of participant agents
        platform_type: Target social media platform

    Returns:
        True if setup is valid for social media simulation

    Raises:
        ValueError: If validation fails with specific error details
    """
    if len(participants) < 2:
        raise ValueError("Social media conversation requires at least 2 participants")

    # Validate participants
    for i, participant in enumerate(participants):
        if not hasattr(participant, "name"):
            raise ValueError(f"Participant {i} missing required 'name' attribute")

        if not hasattr(participant, "arun"):
            raise ValueError(f"Participant {i} missing required 'arun' method")

        # Check for social media persona attributes (optional but recommended)
        if not hasattr(participant, "persona") and not hasattr(
            participant, "social_profile"
        ):
            import warnings

            warnings.warn(
                f"Participant {participant.name} lacks persona/social_profile attributes. "
                f"Social media simulation will be less realistic.",
                stacklevel=2,
            )

    # Platform-specific validations
    if platform_type == "twitter" and len(participants) > 20:
        import warnings

        warnings.warn(
            "Twitter simulations work best with fewer participants for realistic threading",
            stacklevel=2,
        )

    # Check for unique names
    names = [getattr(p, "name", f"participant_{i}") for i, p in enumerate(participants)]
    if len(names) != len(set(names)):
        duplicates = [name for name in names if names.count(name) > 1]
        raise ValueError(f"Duplicate participant names found: {duplicates}")

    return True


def __dir__() -> list[str]:
    """Override dir() to show only public API."""
    return __all__


# Add convenience functions to global namespace
create_social_media_conversation.__module__ = __name__
create_twitter_thread.__module__ = __name__
create_reddit_discussion.__module__ = __name__
create_viral_simulation.__module__ = __name__
validate_social_setup.__module__ = __name__
