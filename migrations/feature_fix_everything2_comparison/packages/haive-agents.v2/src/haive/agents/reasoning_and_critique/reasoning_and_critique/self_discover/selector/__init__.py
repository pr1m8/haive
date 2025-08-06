"""Self-Discover Selector Agent module."""

from haive.agents.reasoning_and_critique.self_discover.selector.agent import (
    SelectorAgent,
)
from haive.agents.reasoning_and_critique.self_discover.selector.models import (
    ModuleSelection,
    SelectedModule,
)
from haive.agents.reasoning_and_critique.self_discover.selector.prompts import (
    SELECTOR_PROMPT,
    SELECTOR_SYSTEM_MESSAGE,
)

__all__ = [
    "SELECTOR_PROMPT",
    "SELECTOR_SYSTEM_MESSAGE",
    "ModuleSelection",
    "SelectedModule",
    "SelectorAgent",
]
