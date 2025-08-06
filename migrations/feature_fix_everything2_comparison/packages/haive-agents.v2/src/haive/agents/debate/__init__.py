"""Module exports."""

from haive.agents.conversation.debate.agent import (
    DebateConversation,
)
from haive.agents.conversation.debate.example import (
    example_oxford_debate,
    example_panel_debate,
    example_simple_debate,
    example_socratic_debate,
)
from haive.agents.conversation.debate.state import (
    DebateState,
)

__all__ = [
    "DebateConversation",
    "DebateState",
    "example_oxford_debate",
    "example_panel_debate",
    "example_simple_debate",
    "example_socratic_debate",
]
