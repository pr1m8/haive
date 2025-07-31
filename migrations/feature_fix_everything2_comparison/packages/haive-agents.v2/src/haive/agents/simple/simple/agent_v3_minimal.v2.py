"""Agent_V3_Minimal core module.

This module provides agent v3 minimal functionality for the Haive framework.

Classes:
    SimpleAgentV3Minimal: SimpleAgentV3Minimal implementation.
    is: is implementation.
    return: return implementation.

Functions:
    as_tool: As Tool functionality.
    as_structured_tool: As Structured Tool functionality.
"""

# SimpleAgent v3 - Minimal Import Path
"""
SimpleAgent v3 implementation with minimal import overhead.

This implementation provides the same SimpleAgentV3 functionality but with
lazy loading of all heavy dependencies to achieve sub-5 second import times.

Usage:
    # Fast import - no heavy dependencies loaded
    from haive.agents.simple.agent_v3_minimal import SimpleAgentV3Minimal as SimpleAgentV3

    # Full functionality available when actually used
    agent = SimpleAgentV3(name="test")
    result = await agent.arun("Hello")
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Import types only for static analysis
    from haive.agents.simple.agent_v3 import SimpleAgentV3 as _SimpleAgentV3
else:
    _SimpleAgentV3 = None


class SimpleAgentV3Minimal:
    """Minimal wrapper for SimpleAgentV3 with lazy loading."""

    _real_class = None

    def __new__(cls, *args, **kwargs):
        """Dynamically import and create the real SimpleAgentV3 instance."""
        if cls._real_class is None:
            from haive.agents.simple.agent_v3 import SimpleAgentV3

            cls._real_class = SimpleAgentV3

        # Create instance of the real class
        return cls._real_class(*args, **kwargs)

    @classmethod
    def as_tool(cls, *args, **kwargs):
        """Lazy loading for as_tool class method."""
        if cls._real_class is None:
            from haive.agents.simple.agent_v3 import SimpleAgentV3

            cls._real_class = SimpleAgentV3
        return cls._real_class.as_tool(*args, **kwargs)

    @classmethod
    def as_structured_tool(cls, *args, **kwargs):
        """Lazy loading for as_structured_tool class method."""
        if cls._real_class is None:
            from haive.agents.simple.agent_v3 import SimpleAgentV3

            cls._real_class = SimpleAgentV3
        return cls._real_class.as_structured_tool(*args, **kwargs)


# Alias for easy switching
SimpleAgentV3 = SimpleAgentV3Minimal
