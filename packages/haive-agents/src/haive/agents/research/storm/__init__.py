# src/haive/agents/research/storm/__init__.py

"""STORM Agent - a research assistant that generates comprehensive
Wikipedia-style articles on a user-provided topic.

The STORM agent consists of three main components:
1. Research Agent: Generates initial outline and identifies perspectives
2. Interview Agent: Conducts expert interviews for diverse insights
3. Writing Agent: Refines outline, writes sections, and assembles final article

Each component is implemented as a separate agent, and the main STORM agent
orchestrates the flow between them.

NOTE: This module is currently under development. The agent implementation
is not yet complete.
"""

# NOTE: The following imports are placeholders for future implementation
# The STORM agent components are still being developed

# For now, we'll only export the config class since it exists
from haive.agents.research.storm.config import STORMAgentConfig

__all__ = [
    "STORMAgentConfig",
]

# Placeholder classes that will be implemented later
__all__.extend(
    [
        "Editor",
        "Interview",
        # Interview components (to be implemented)
        "InterviewAgent",
        "InterviewAgentConfig",
        "InterviewState",
        # State models (to be implemented)
        "Outline",
        "Perspectives",
        "RelatedSubjects",
        # Research components (to be implemented)
        "ResearchAgent",
        "ResearchAgentConfig",
        "ResearchState",
        # Main STORM components (to be implemented)
        "STORMAgent",
        "STORMAgentState",
        "Section",
        "Subsection",
        "WikiSection",
        # Writing components (to be implemented)
        "WritingAgent",
        "WritingAgentConfig",
        "WritingState",
    ]
)
