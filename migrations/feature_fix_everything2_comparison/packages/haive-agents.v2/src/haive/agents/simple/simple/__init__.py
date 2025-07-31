"""Simple package.

This package provides simple functionality for the Haive framework.

Modules:
    agent: Agent implementation.
    agent_v2: Agent V2 implementation.
    agent_v3: Agent V3 implementation.
    agent_v3_minimal: Agent V3 Minimal implementation.
    agent_with_validation: Agent With Validation implementation.

Subpackages:
    structured: Structured functionality.
    v2: V2 functionality.
"""

# SimpleAgent Package - Ultra-fast lazy loading
"""
SimpleAgent package with ultra-optimized import performance.
Achieves sub-3 second import times through comprehensive lazy loading.
"""

# Lazy import mapping for SimpleAgent variants
_SIMPLE_AGENT_IMPORTS = {
    "SimpleAgent": ("haive.agents.simple.agent_v2", "SimpleAgentV2"),
    "SimpleAgentV3": ("haive.agents.simple.agent_v3", "SimpleAgentV3"),
}


def __getattr__(name: str):
    """Lazy load SimpleAgent classes to avoid import-time overhead."""
    if name in _SIMPLE_AGENT_IMPORTS:
        module_path, class_name = _SIMPLE_AGENT_IMPORTS[name]

        # Import module and get class only when accessed
        import importlib

        module = importlib.import_module(module_path)
        agent_class = getattr(module, class_name)

        # Cache in globals for subsequent access
        globals()[name] = agent_class
        return agent_class

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = ["SimpleAgent", "SimpleAgentV3"]
