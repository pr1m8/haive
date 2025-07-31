"""Enhanced_Simple_Agent_V2 core module.

This module provides enhanced simple agent v2 functionality for the Haive framework.

Classes:
    directly: directly implementation.
    SimpleAgentV2: SimpleAgentV2 implementation.

Functions:
    ensure_engine: Ensure Engine functionality.
    setup_agent: Setup Agent functionality.
    build_graph: Build Graph functionality.
"""

# src/haive/agents/simple/enhanced_simple_agent_v2.py

"""Enhanced SimpleAgent V2 - Using the enhanced Agent pattern directly.

This version imports the enhanced Agent class directly to avoid conflicts
with the regular Agent class.
"""

import logging
import os

# Import enhanced Agent directly - bypassing base/__init__.py
import sys
from typing import Any, Literal

from langchain_core.messages import AIMessage
from langgraph.graph import END, START
from pydantic import Field, model_validator

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

# Now import the enhanced Agent directly
from base.enhanced_agent import Agent as EnhancedAgent

# Import other dependencies normally
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.node.tool_node_config_v2 import ToolNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph

logger = logging.getLogger(__name__)


class SimpleAgentV2(EnhancedAgent[AugLLMConfig]):
    """SimpleAgent V2 using the enhanced Agent pattern.

    This demonstrates SimpleAgent as Agent[AugLLMConfig] - the cleanest
    possible implementation using engine-focused generics.

    Key points:
    - Inherits from enhanced Agent with AugLLMConfig as engine type
    - Engine is guaranteed to be AugLLMConfig
    - All complex logic handled by base enhanced Agent
    - SimpleAgent is just configuration and graph building
    """

    # Convenience fields that sync to AugLLMConfig
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int | None = Field(default=None, ge=1)
    system_message: str | None = Field(default=None)
    tools: list[Any] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def ensure_engine(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Ensure we have an AugLLMConfig engine."""
        if not isinstance(values, dict):
            return values

        # Create engine from fields if not provided
        if "engine" not in values or values["engine"] is None:
            config = AugLLMConfig(
                temperature=values.get("temperature", 0.7),
                max_tokens=values.get("max_tokens"),
                system_message=values.get("system_message"),
                tools=values.get("tools", []),
            )
            values["engine"] = config

        return values

    def setup_agent(self) -> None:
        """Sync fields to engine."""
        # Enhanced pattern guarantees engine is AugLLMConfig
        if self.engine:
            self.engine.temperature = self.temperature
            if self.max_tokens:
                self.engine.max_tokens = self.max_tokens
            if self.system_message:
                self.engine.system_message = self.system_message
            if self.tools:
                self.engine.tools = self.tools

    def build_graph(self) -> BaseGraph:
        """Build minimal graph for SimpleAgent."""
        graph = BaseGraph(name=self.name)

        # Engine node
        engine_node = EngineNodeConfig(name="agent", engine=self.engine)
        graph.add_node("agent", engine_node)
        graph.add_edge(START, "agent")

        # Tool node if needed
        if self.tools:
            tool_node = ToolNodeConfig(name="tools", tools=self.tools)
            graph.add_node("tools", tool_node)

            # Conditional routing
            def check_tools(state: dict[str, Any]) -> Literal["tools", "end"]:
                msgs = state.get("messages", [])
                if msgs and isinstance(msgs[-1], AIMessage) and msgs[-1].tool_calls:
                    return "tools"
                return "end"

            graph.add_conditional_edges(
                "agent", check_tools, {"tools": "tools", "end": END}
            )
            graph.add_edge("tools", END)
        else:
            graph.add_edge("agent", END)

        return graph
