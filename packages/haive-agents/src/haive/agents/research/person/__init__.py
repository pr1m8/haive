"""Person - TODO: Add brief description.

TODO: Add detailed description of module functionality



Example:
    Basic usage::

        from haive.person import module_function

        # TODO: Add example


"""

# src/haive/agents/person_research/__init__.py

from haive.agents.research.person.agent import PersonResearchAgent
from haive.agents.research.person.config import PersonResearchAgentConfig
from haive.agents.research.person.state import (
    Person,
    PersonResearchInputState,
    PersonResearchOutputState,
    PersonResearchState,
)

__all__ = [
    "Person",
    "PersonResearchAgent",
    "PersonResearchAgentConfig",
    "PersonResearchInputState",
    "PersonResearchOutputState",
    "PersonResearchState",
]
