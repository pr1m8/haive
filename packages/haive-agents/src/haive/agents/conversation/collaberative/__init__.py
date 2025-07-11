r"""Collaborative Conversation - Cooperative Multi-Agent Problem-Solving.

Multi-agent conversations focused on collaborative problem-solving and teamwork.
The collaborative conversation implements a specialized conversation pattern designed
for task-oriented teamwork and cooperative problem-solving between multiple agents
with complementary roles and expertise areas.

Architecture:
    The collaborative conversation extends BaseConversationAgent with specialized
    state management for team-based work, including role assignment, task tracking,
    work product management, and consensus-building mechanisms. This provides a
    comprehensive framework for productive multi-agent collaboration.

Key Features:
    - Joint task completion between specialized agents with defined roles
    - Role-based contributions to shared goals and objectives
    - Brainstorming, idea refinement, and iterative improvement
    - Consensus-building mechanisms and conflict resolution
    - Progress tracking toward deliverables and milestones
    - Final output synthesis from multiple contributors
    - Work product versioning and contribution tracking
    - Configurable collaboration modes and workflow patterns

Core Components:
    CollaborativeConversation: Main agent class that orchestrates team-based
        conversations with role management, task coordination, and output synthesis.
    CollaborativeState: Specialized state schema extending ConversationState with
        collaboration-specific fields for roles, tasks, and work products.

Collaboration Philosophy:
    Unlike debate or round-robin conversations, collaborative conversations emphasize
    constructive cooperation toward a common objective rather than turn-taking or
    dialectical exchange. The focus is on building shared understanding and
    producing valuable outputs through collective intelligence.

Usage Patterns:
    Software development team::\n

        from haive.agents.conversation import CollaborativeConversation
        from haive.agents.simple import SimpleAgent

        # Create specialized team members
        architect = SimpleAgent(name="Architect", role="system_design")
        backend_dev = SimpleAgent(name="Backend", role="api_development")
        devops = SimpleAgent(name="DevOps", role="infrastructure")

        # Create collaborative conversation
        collab = CollaborativeConversation(
            objective="Design a REST API for a todo application",
            participants=[architect, backend_dev, devops],
            roles={
                "Architect": "Focus on overall system design and patterns",
                "Backend": "Define API endpoints and data models",
                "DevOps": "Consider deployment and scaling concerns"
            },
            deliverables=["system_design", "api_spec", "deployment_plan"],
            max_rounds=5
        )

        # Run the collaboration
        result = await collab.arun()

        # Access collaboration results
        messages = result["messages"]
        final_output = result["work_product"]
        contributions = result["role_contributions"]

    Research team collaboration::\n

        # Multi-disciplinary research collaboration
        research_collab = CollaborativeConversation(
            objective="Analyze climate change impacts on urban planning",
            participants=[climate_scientist, urban_planner, data_analyst],
            collaboration_mode="research",
            phases=["literature_review", "data_analysis", "synthesis"],
            consensus_threshold=0.8
        )

    Creative collaboration::\n

        # Creative team working on content strategy
        creative_collab = CollaborativeConversation.create_creative_team(
            objective="Develop marketing campaign for sustainable products",
            roles={
                "Strategist": "Overall campaign strategy and messaging",
                "Creative": "Visual concepts and creative execution",
                "Copywriter": "Compelling copy and messaging",
                "Analyst": "Target audience and performance metrics"
            },
            brainstorming_rounds=3,
            refinement_rounds=2
        )

Collaboration Modes:
    - **Development**: Software development team workflows
    - **Research**: Academic or scientific research collaboration
    - **Creative**: Creative and design team collaboration
    - **Strategy**: Strategic planning and decision-making
    - **Analysis**: Data analysis and insight generation
    - **Problem-solving**: General problem-solving workflows

Role Management:
    The collaborative system manages participant roles and ensures appropriate
    contributions through:
    - Role-based speaking order and contribution timing
    - Expertise-driven task assignment and responsibility
    - Balanced participation across all team members
    - Role-specific contribution assessment and feedback

Work Product Management:
    - Version control for evolving deliverables
    - Contribution tracking and attribution
    - Quality assessment and iterative improvement
    - Final synthesis and output generation
    - Deliverable validation against objectives

Consensus Building:
    - Conflict identification and resolution mechanisms
    - Agreement tracking and validation
    - Compromise and alternative solution exploration
    - Decision point management and consensus thresholds

Use Cases:
    - Multi-agent problem solving with specialized roles
    - Simulating team dynamics and collaborative workflows
    - Producing composite outputs requiring diverse expertise
    - Brainstorming and idea refinement sessions
    - Strategic planning and decision-making processes
    - Research collaboration with multiple perspectives
    - Creative projects requiring diverse skill sets

Integration:
    Collaborative conversations integrate seamlessly with:
    - Haive core schema system for state management
    - Base conversation infrastructure for orchestration
    - Project management tools for task tracking
    - Version control systems for work product management
    - Quality assessment and feedback systems

Examples:
    For comprehensive examples, see the documentation and examples directory:
    - examples/collaborative_development.py
    - examples/collaborative_research.py
    - examples/collaborative_creative.py
    - examples/collaborative_strategy.py

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
from haive.agents.conversation.collaberative.agent import CollaborativeConversation
from haive.agents.conversation.collaberative.state import CollaborativeState

# Type aliases for collaborative conversations
CollaborativeParticipant: TypeAlias = Any  # Agent with collaboration capabilities
TeamRole: TypeAlias = str  # Role identifier and description
CollaborationMode: TypeAlias = Literal[
    "development", "research", "creative", "strategy", "analysis", "problem_solving"
]
CollaborationPhase: TypeAlias = Literal[
    "planning", "brainstorming", "development", "review", "synthesis", "consensus"
]
WorkProduct: TypeAlias = dict[str, Any]  # Collaborative output and deliverables
CollaborativeResult: TypeAlias = dict[str, Any]  # Collaboration outcome and artifacts


# Configuration types for collaborative conversations
class CollaborativeConfiguration(TypedDict, total=False):
    """Configuration for collaborative conversations."""

    collaboration_mode: NotRequired[CollaborationMode]
    phases: NotRequired[list[CollaborationPhase]]
    deliverables: NotRequired[list[str]]
    consensus_threshold: NotRequired[float]
    max_brainstorming_rounds: NotRequired[int]
    enable_role_rotation: NotRequired[bool]
    track_contributions: NotRequired[bool]
    output_format: NotRequired[str]


class RoleConfiguration(TypedDict, total=False):
    """Configuration for team roles."""

    role_name: NotRequired[str]
    role_description: NotRequired[str]
    expertise_areas: NotRequired[list[str]]
    responsibilities: NotRequired[list[str]]
    contribution_weight: NotRequired[float]


class WorkProductConfig(TypedDict, total=False):
    """Configuration for work product management."""

    versioning_enabled: NotRequired[bool]
    quality_gates: NotRequired[list[str]]
    review_criteria: NotRequired[list[str]]
    output_templates: NotRequired[dict[str, str]]


# Define public API
__all__ = [
    "CollaborationMode",
    "CollaborationPhase",
    # Configuration types
    "CollaborativeConfiguration",
    # Core classes
    "CollaborativeConversation",
    # Type aliases
    "CollaborativeParticipant",
    "CollaborativeResult",
    "CollaborativeState",
    "RoleConfiguration",
    "TeamRole",
    "WorkProduct",
    "WorkProductConfig",
    "__author__",
    "__license__",
    # Version information
    "__version__",
    # Utility functions
    "create_collaborative_conversation",
    "create_creative_team",
    "create_development_team",
    "create_research_team",
    "validate_team_setup",
]


# Utility functions
def create_collaborative_conversation(
    objective: str,
    participants: list[CollaborativeParticipant],
    roles: dict[str, str],
    collaboration_mode: CollaborationMode = "problem_solving",
    config: CollaborativeConfiguration | None = None,
) -> CollaborativeConversation:
    r"""Create a collaborative conversation for team-based work.

    Args:
        objective: Collaboration objective or goal
        participants: List of participant agents
        roles: Dictionary mapping participant names to role descriptions
        collaboration_mode: Mode of collaboration
        config: Optional collaboration configuration

    Returns:
        Configured CollaborativeConversation instance

    Examples:
        Basic team collaboration::\n

            collab = create_collaborative_conversation(
                objective="Design a mobile app",
                participants=[designer, developer, product_manager],
                roles={
                    "designer": "UI/UX design and user experience",
                    "developer": "Technical implementation and architecture",
                    "product_manager": "Requirements and project coordination"
                },
                collaboration_mode="development"
            )

        Research collaboration::\n

            research = create_collaborative_conversation(
                objective="Analyze market trends in renewable energy",
                participants=[data_analyst, industry_expert, policy_researcher],
                roles={
                    "data_analyst": "Data collection and statistical analysis",
                    "industry_expert": "Industry insights and trends",
                    "policy_researcher": "Policy implications and regulatory factors"
                },
                collaboration_mode="research",
                config={
                    "phases": ["planning", "analysis", "synthesis"],
                    "consensus_threshold": 0.8
                }
            )
    """
    config = config or {}

    return CollaborativeConversation(
        objective=objective,
        participants=participants,
        roles=roles,
        collaboration_mode=collaboration_mode,
        **config,
    )


def create_development_team(
    project_goal: str,
    team_members: dict[str, CollaborativeParticipant],
    sprint_length: int = 5,
) -> CollaborativeConversation:
    r"""Create a software development team collaboration.

    Args:
        project_goal: Development project goal
        team_members: Dictionary mapping roles to team member agents
        sprint_length: Number of rounds for development sprint

    Returns:
        Configured development CollaborativeConversation

    Examples:
        Development team::\n

            dev_team = create_development_team(
                project_goal="Build user authentication system",
                team_members={
                    "architect": system_architect,
                    "backend_dev": backend_developer,
                    "frontend_dev": frontend_developer,
                    "qa_engineer": qa_specialist
                },
                sprint_length=7
            )
    """
    return CollaborativeConversation(
        objective=project_goal,
        participants=list(team_members.values()),
        roles={agent.name: role for role, agent in team_members.items()},
        collaboration_mode="development",
        phases=["planning", "development", "review"],
        max_rounds=sprint_length,
        deliverables=["technical_design", "implementation_plan", "test_strategy"],
    )


def create_research_team(
    research_question: str,
    researchers: list[CollaborativeParticipant],
    methodology: str = "mixed_methods",
) -> CollaborativeConversation:
    r"""Create a research team collaboration.

    Args:
        research_question: Research question or hypothesis
        researchers: List of researcher agents
        methodology: Research methodology approach

    Returns:
        Configured research CollaborativeConversation

    Examples:
        Research collaboration::\n

            research_team = create_research_team(
                research_question="What factors influence remote work productivity?",
                researchers=[survey_researcher, data_scientist, behavioral_psychologist],
                methodology="mixed_methods"
            )
    """
    return CollaborativeConversation(
        objective=research_question,
        participants=researchers,
        collaboration_mode="research",
        phases=["planning", "data_collection", "analysis", "synthesis"],
        deliverables=[
            "research_design",
            "data_analysis",
            "findings",
            "recommendations",
        ],
        consensus_threshold=0.75,
        track_contributions=True,
    )


def create_creative_team(
    creative_brief: str,
    creative_roles: dict[str, CollaborativeParticipant],
    brainstorming_rounds: int = 3,
) -> CollaborativeConversation:
    r"""Create a creative team collaboration.

    Args:
        creative_brief: Creative project brief or objective
        creative_roles: Dictionary mapping creative roles to team member agents
        brainstorming_rounds: Number of brainstorming rounds

    Returns:
        Configured creative CollaborativeConversation

    Examples:
        Creative team::\n

            creative_team = create_creative_team(
                creative_brief="Develop brand identity for eco-friendly startup",
                creative_roles={
                    "brand_strategist": brand_expert,
                    "visual_designer": designer,
                    "copywriter": writer,
                    "creative_director": director
                },
                brainstorming_rounds=4
            )
    """
    return CollaborativeConversation(
        objective=creative_brief,
        participants=list(creative_roles.values()),
        roles={agent.name: role for role, agent in creative_roles.items()},
        collaboration_mode="creative",
        phases=["brainstorming", "development", "refinement", "consensus"],
        max_brainstorming_rounds=brainstorming_rounds,
        deliverables=["concept", "visual_identity", "messaging", "guidelines"],
    )


def validate_team_setup(
    participants: list[CollaborativeParticipant], roles: dict[str, str]
) -> bool:
    """Validate team setup for collaborative conversation.

    Args:
        participants: List of participant agents
        roles: Dictionary mapping names to role descriptions

    Returns:
        True if team setup is valid for collaboration

    Raises:
        ValueError: If validation fails with specific error details
    """
    if len(participants) < 2:
        raise ValueError("Collaborative conversation requires at least 2 participants")

    # Validate participants
    for i, participant in enumerate(participants):
        if not hasattr(participant, "name"):
            raise ValueError(f"Participant {i} missing required 'name' attribute")

        if not hasattr(participant, "arun"):
            raise ValueError(f"Participant {i} missing required 'arun' method")

    # Check role assignments
    participant_names = [
        getattr(p, "name", f"participant_{i}") for i, p in enumerate(participants)
    ]

    for name in roles:
        if name not in participant_names:
            raise ValueError(f"Role assigned to unknown participant: {name}")

    # Check for unique names
    if len(participant_names) != len(set(participant_names)):
        duplicates = [
            name for name in participant_names if participant_names.count(name) > 1
        ]
        raise ValueError(f"Duplicate participant names found: {duplicates}")

    return True


def __dir__() -> list[str]:
    """Override dir() to show only public API."""
    return __all__


# Add convenience functions to global namespace
create_collaborative_conversation.__module__ = __name__
create_development_team.__module__ = __name__
create_research_team.__module__ = __name__
create_creative_team.__module__ = __name__
validate_team_setup.__module__ = __name__
