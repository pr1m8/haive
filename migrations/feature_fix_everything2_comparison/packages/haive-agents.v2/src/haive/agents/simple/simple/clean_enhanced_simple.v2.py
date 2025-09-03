"""Clean_Enhanced_Simple core module.

This module provides clean enhanced simple functionality for the Haive framework.

Classes:
    SimpleAgent: SimpleAgent implementation.

Functions:
    setup_agent: Setup Agent functionality.
    build_graph: Build Graph functionality.
"""

# src/haive/agents/simple/clean_enhanced_simple.py
"""Clean Enhanced SimpleAgent - SimpleAgent as Agent[AugLLMConfig].

This is the cleanest implementation showing SimpleAgent is just Agent[AugLLMConfig].
"""
from __future__ import annotations

import logging

# Import from enhanced base module

logger = logging.getLogger(__name__)


class SimpleAgent(Agent[AugLLMConfig]):
    """SimpleAgent is just Agent[AugLLMConfig].

    This is the entire implementation - SimpleAgent is nothing more than
    an Agent with its engine type locked to AugLLMConfig. Everything else
    comes from the enhanced base Agent class.

    This demonstrates the power of engine-focused generics:
    - SimpleAgent = Agent[AugLLMConfig]
    - ReactAgent = Agent[AugLLMConfig] + looping
    - RAGAgent = Agent[RetrieverEngine]
    - etc.
    """

    # Optional convenience fields that sync to engine
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int | None = Field(default=None)
    system_message: str | None = Field(default=None)
    tools: list[Any] = Field(default_factory=list)

    def setup_agent(self) -> None:
        """Setup by ensuring we have AugLLMConfig and syncing fields."""
        # Create engine if needed
        if not self.engine:
            self.engine = AugLLMConfig(
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                system_message=self.system_message,
                tools=self.tools,
            )
        else:
            # Sync fields to existing engine
            self.engine.temperature = self.temperature
            if self.max_tokens:
                self.engine.max_tokens = self.max_tokens
            if self.system_message:
                self.engine.system_message = self.system_message
            if self.tools:
                self.engine.tools = self.tools

    def build_graph(self) -> BaseGraph:
        """Build simple graph: START -> agent -> (tools?) -> END."""
        graph = BaseGraph(name=self.name)

        # Agent node
        engine_node = EngineNodeConfig(name="agent", engine=self.engine)
        graph.add_node("agent", engine_node)
        graph.add_edge(START, "agent")

        # Tools if present
        if self.tools:
            tool_node = ToolNodeConfig(name="tools", tools=self.tools)
            graph.add_node("tools", tool_node)

            # Route based on tool calls
            graph.add_conditional_edges(
                "agent",
                lambda s: "tools" if self._has_tool_calls(s) else "end",
                {"tools": "tools", "end": END},
            )
            graph.add_edge("tools", END)
        else:
            graph.add_edge("agent", END)

        return graph

    def _has_tool_calls(self, state: dict[str, Any]) -> bool:
        """Check if last message has tool calls."""
        messages = state.get("messages", [])
        if messages:
            last = messages[-1]
            return isinstance(last, AIMessage) and bool(last.tool_calls)
        return False


# That's it! SimpleAgent is now Agent[AugLLMConfig] - clean and type-safe.
