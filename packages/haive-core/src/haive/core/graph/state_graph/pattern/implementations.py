# src/haive/core/graph/state_graph/patterns/implementations.py

import logging
from typing import Any, ClassVar, Dict, List, Optional

from langgraph.graph import END, START

from haive.core.graph.common.types import NodeLike
from haive.core.graph.state_graph.pattern.base import GraphPattern

logger = logging.getLogger(__name__)


@GraphPattern.register("simple")
class SimplePattern(GraphPattern):
    """Simple agent pattern with a single LLM node.

    Structure:
    - Single agent node that processes input
    - Linear flow: START -> agent -> END
    """

    # Define structure through class attributes - use 'pattern_' prefix
    # to match the attribute names in the base class
    pattern_nodes: ClassVar[dict[str, NodeLike | None]] = {
        "agent": None  # Placeholder to be filled at build time
    }

    pattern_edges: ClassVar[list[tuple]] = [(START, "agent"), ("agent", END)]

    def _build(self):
        """Implementation-specific logic."""
        # Check if agent implementation is provided
        if "agent" in self.implementations:
            # Node might already exist from parent class
            if "agent" in self.nodes:
                self.replace_node("agent", self.implementations["agent"])
            else:
                self.add_node("agent", self.implementations["agent"])
        elif "agent" not in self.nodes:
            logger.warning("No agent implementation provided for SimplePattern")
            self.add_node("agent", lambda state: state)


@GraphPattern.register("react")
class ReactPattern(SimplePattern):  # Change to inherit from SimplePattern!
    """ReAct pattern extending SimplePattern with tools.

    Structure:
    - Agent node from SimplePattern
    - Additional tools node for task execution
    - Conditional routing from agent to either tools or END
    - Feedback loop from tools back to agent
    """

    # Define only NEW structure not in SimplePattern
    pattern_nodes: ClassVar[dict[str, NodeLike | None]] = {
        "tools": None  # Only add tools, agent comes from SimplePattern
    }

    pattern_edges: ClassVar[list[tuple]] = [
        # Remove (START, "agent") since it comes from SimplePattern
        # Remove ("agent", END) to replace with conditional
        ("tools", "agent")  # Add edge from tools back to agent
    ]

    pattern_conditionals: ClassVar[list[dict[str, Any]]] = [
        {
            "source": "agent",
            "condition": lambda state: (
                "use_tools" if state.get("needs_tools", False) else "finish"
            ),
            "destinations": {"use_tools": "tools", "finish": END},
        }
    ]

    def _build(self):
        """Implementation-specific logic.

        1. First call parent's _build to set up agent node
        2. Then add our tools node
        """
        # Call parent _build to set up agent node
        super()._build()

        # Add tools node if implementation provided
        if "tools" in self.implementations:
            if "tools" in self.nodes:
                self.replace_node("tools", self.implementations["tools"])
            else:
                self.add_node("tools", self.implementations["tools"])
        elif "tools" not in self.nodes:
            logger.warning("Tools node missing in ReactPattern - adding placeholder")
            self.add_node("tools", lambda state: state)
