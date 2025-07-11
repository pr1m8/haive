"""ChainAgent - The simplest way to build agent chains.

Just list your nodes and edges. That's it.
"""

from .chain_agent_simple import ChainAgent, FlowBuilder, flow, flow_with_edges

__all__ = ["ChainAgent", "FlowBuilder", "flow", "flow_with_edges"]
