"""Enhanced_Simple_Real core module.

This module provides enhanced simple real functionality for the Haive framework.

Classes:
    EnhancedAgentBase: EnhancedAgentBase implementation.
    setup: setup implementation.
    SimpleAgent: SimpleAgent implementation.

Functions:
    setup_agent: Setup Agent functionality.
    build_graph: Build Graph functionality.
    arun: Arun functionality.
"""

# src/haive/agents/simple/enhanced_simple_real.py

"""Enhanced SimpleAgent - Real implementation using Agent[AugLLMConfig].

This is the real SimpleAgent implementation showing it as Agent[AugLLMConfig].
It carefully imports only what's needed to avoid circular imports.
"""

import logging
from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field, model_validator

# Carefully import to avoid cycles
if TYPE_CHECKING:
    from haive.core.graph.state_graph.base_graph2 import BaseGraph

logger = logging.getLogger(__name__)


# First, let's define a minimal enhanced Agent base that we can use
# This avoids the circular import issues
class EnhancedAgentBase:
    """Minimal base for enhanced agents to avoid circular imports."""

    name: str = Field(default="Agent")
    engine: Any = Field(default=None)

    def setup_agent(self) -> None:
        """Hook for subclass setup."""

    def build_graph(self) -> Any:
        """Build the agent's graph."""
        raise NotImplementedError

    async def arun(self, input_data: Any) -> Any:
        """Async run method."""
        # In real implementation, this would execute the graph
        return f"{self.name} processed input"

    def run(self, input_data: Any) -> Any:
        """Sync run method."""
        import asyncio

        return asyncio.run(self.arun(input_data))


class SimpleAgent(EnhancedAgentBase):
    """Enhanced SimpleAgent that is essentially Agent[AugLLMConfig].

    This demonstrates the key insight: SimpleAgent IS Agent[AugLLMConfig].
    All the complexity is handled by the base Agent class and the engine type.

    In the full implementation with working imports, this would inherit from:
    Agent[AugLLMConfig] where Agent is from enhanced_agent.py

    Key points:
    - Engine is always AugLLMConfig
    - Minimal implementation needed
    - Type safety for engine-specific features
    - Clean separation of concerns
    """

    # Convenience fields that sync to AugLLMConfig
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int | None = Field(default=None, ge=1)
    system_message: str | None = Field(default=None)
    tools: list[Any] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def ensure_aug_llm_config(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Ensure we have an AugLLMConfig engine."""
        if not isinstance(values, dict):
            return values

        # Import here to avoid circular imports
        from haive.core.engine.aug_llm.config import AugLLMConfig

        # Create engine from fields if not provided
        if "engine" not in values or values["engine"] is None:
            values["engine"] = AugLLMConfig(
                temperature=values.get("temperature", 0.7),
                max_tokens=values.get("max_tokens"),
                system_message=values.get("system_message"),
                tools=values.get("tools", []),
            )
        elif not isinstance(values["engine"], AugLLMConfig):
            # Convert to AugLLMConfig if needed
            logger.warning("SimpleAgent requires AugLLMConfig engine, converting...")
            values["engine"] = AugLLMConfig()

        return values

    def setup_agent(self) -> None:
        """Sync convenience fields to the AugLLMConfig engine."""
        # Import here to avoid circular imports
        from haive.core.engine.aug_llm.config import AugLLMConfig

        if isinstance(self.engine, AugLLMConfig):
            # Sync fields to engine
            self.engine.temperature = self.temperature
            if self.max_tokens is not None:
                self.engine.max_tokens = self.max_tokens
            if self.system_message is not None:
                self.engine.system_message = self.system_message
            if self.tools:
                self.engine.tools = self.tools

    def build_graph(self) -> "BaseGraph":
        """Build minimal graph for SimpleAgent."""
        # Import here to avoid circular imports
        from haive.core.graph.node.engine_node import EngineNodeConfig
        from haive.core.graph.node.tool_node_config_v2 import ToolNodeConfig
        from haive.core.graph.state_graph.base_graph2 import BaseGraph
        from langchain_core.messages import AIMessage
        from langgraph.graph import END, START

        graph = BaseGraph(name=self.name)

        # Engine node
        engine_node = EngineNodeConfig(name="agent", engine=self.engine)
        graph.add_node("agent", engine_node)
        graph.add_edge(START, "agent")

        # Tool node if tools present
        if self.tools:
            tool_node = ToolNodeConfig(name="tools", tools=self.tools)
            graph.add_node("tools", tool_node)

            # Conditional routing based on tool calls
            def check_tools(state: dict[str, Any]) -> Literal["tools", "end"]:
                messages = state.get("messages", [])
                if messages and isinstance(messages[-1], AIMessage):
                    if messages[-1].tool_calls:
                        return "tools"
                return "end"

            graph.add_conditional_edges(
                "agent", check_tools, {"tools": "tools", "end": END}
            )
            graph.add_edge("tools", END)
        else:
            graph.add_edge("agent", END)

        return graph

    def __repr__(self) -> str:
        """String representation showing engine type."""
        engine_type = type(self.engine).__name__ if self.engine else "None"
        return f"SimpleAgent[{engine_type}](name='{self.name}')"


# Example usage
if __name__ == "__main__":
    # This would work with proper imports
    print("Enhanced SimpleAgent implementation")
    print("SimpleAgent = Agent[AugLLMConfig]")

    # Minimal demo without full imports
    agent = SimpleAgent(name="demo", temperature=0.5)
    print(f"\nCreated: {agent}")

    # In full implementation:
    # - SimpleAgent inherits from Agent[AugLLMConfig]
    # - All agent functionality comes from base Agent
    # - Engine type provides specialization
    # - Clean, minimal, type-safe
