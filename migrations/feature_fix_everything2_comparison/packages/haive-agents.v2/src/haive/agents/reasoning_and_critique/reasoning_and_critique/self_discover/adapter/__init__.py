"""Self-Discover Adapter Agent module."""

from haive.agents.reasoning_and_critique.self_discover.adapter.agent import AdapterAgent
from haive.agents.reasoning_and_critique.self_discover.adapter.models import (
    AdaptedModule,
    AdaptedModules,
)
from haive.agents.reasoning_and_critique.self_discover.adapter.prompts import (
    ADAPTER_PROMPT,
    ADAPTER_SYSTEM_MESSAGE,
)

__all__ = [
    "ADAPTER_PROMPT",
    "ADAPTER_SYSTEM_MESSAGE",
    "AdaptedModule",
    "AdaptedModules",
    "AdapterAgent",
]
