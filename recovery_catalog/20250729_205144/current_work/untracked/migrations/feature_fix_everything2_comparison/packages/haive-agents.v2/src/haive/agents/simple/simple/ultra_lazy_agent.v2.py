"""Ultra_Lazy_Agent core module.

This module provides ultra lazy agent functionality for the Haive framework.

Classes:
    UltraLazyAgent: UltraLazyAgent implementation.

Functions:
    name: Name functionality.
"""

# UltraLazyAgent - Sub-3 Second Import Target
"""
Ultra-aggressive lazy loading implementation that defers ALL dependencies
until the moment of first actual use. Target: <3 second import time.

This uses the most minimal possible imports and defers everything else.
"""

# MINIMAL IMPORTS ONLY - no logging, no complex types, no frameworks
from typing import Any


class UltraLazyAgent:
    """Ultra-minimal agent proxy with maximum lazy loading."""

    def __init__(self, name: str = "UltraLazyAgent", **kwargs):
        # Store ONLY basic data - no complex objects
        self._name = name
        self._kwargs = kwargs
        self._real_agent = None
        self._initialized = False

    @property
    def name(self) -> str:
        return self._name

    def _load_real_agent(self):
        """Load the real SimpleAgentV3 only when absolutely necessary."""
        if self._real_agent is None:
            # Import and create real agent only now
            import importlib

            module = importlib.import_module("haive.agents.simple.agent_v3")
            SimpleAgentV3 = module.SimpleAgentV3

            # Create real instance
            self._real_agent = SimpleAgentV3(name=self._name, **self._kwargs)
            self._initialized = True

        return self._real_agent

    def __getattr__(self, name: str):
        """Proxy everything to real agent."""
        if name.startswith("_"):
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )
        return getattr(self._load_real_agent(), name)

    def __setattr__(self, name: str, value: Any):
        """Handle attribute setting."""
        if name.startswith("_") or name == "name":
            super().__setattr__(name, value)
        else:
            setattr(self._load_real_agent(), name, value)

    def __call__(self, *args, **kwargs):
        """Make callable."""
        return self._load_real_agent()(*args, **kwargs)

    async def arun(self, *args, **kwargs):
        """Async run - triggers loading."""
        real_agent = self._load_real_agent()
        return await real_agent.arun(*args, **kwargs)

    def run(self, *args, **kwargs):
        """Sync run - triggers loading."""
        return self._load_real_agent().run(*args, **kwargs)

    @classmethod
    def as_tool(cls, **kwargs):
        """Class method - triggers loading."""
        import importlib

        module = importlib.import_module("haive.agents.simple.agent_v3")
        SimpleAgentV3 = module.SimpleAgentV3
        return SimpleAgentV3.as_tool(**kwargs)

    @classmethod
    def as_structured_tool(cls, **kwargs):
        """Class method - triggers loading."""
        import importlib

        module = importlib.import_module("haive.agents.simple.agent_v3")
        SimpleAgentV3 = module.SimpleAgentV3
        return SimpleAgentV3.as_structured_tool(**kwargs)

    def __repr__(self) -> str:
        status = "initialized" if self._initialized else "ultra-lazy"
        return f"UltraLazyAgent(name='{self._name}', status='{status}')"


# Export as SimpleAgentV3 for compatibility
SimpleAgentV3 = UltraLazyAgent
