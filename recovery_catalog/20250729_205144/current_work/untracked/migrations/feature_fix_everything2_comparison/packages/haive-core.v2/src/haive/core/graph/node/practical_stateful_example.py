"""From typing import Any, Dict
Practical Stateful Node Example - Real Implementation.

This shows how to practically implement stateful nodes that work with the current
SimpleAgent, LLMState, and MetaStateSchema architecture without breaking changes.

The key insight is that the existing architecture already provides most of what we need:
- SimpleAgent.engines dict for engine discovery
- LLMState.tool_routes for tool routing
- MetaStateSchema for agent composition
- Existing node *_config classes for patterns

We just need to enhance the discovery mechanisms in the existing nodes.
"""

from typing import Any

from haive.agents.simple.agent import SimpleAgent
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from pydantic import Field

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.parser_node_config import ParserNodeConfig
from haive.core.graph.node.validation_node_config_v2 import ValidationNodeConfigV2
from haive.core.schema.prebuilt.meta_state import MetaStateSchema

# =============================================================================
# EXAMPLE: Enhanced ValidationNodeConfigV2 with Stateful Discovery
# =============================================================================


class StatefulValidationNodeV2(ValidationNodeConfigV2):
    """Enhanced ValidationNodeConfigV2 with stateful discovery capabilities.

    This extends the existing ValidationNodeConfigV2 to add dynamic discovery while
    maintaining full backward compatibility.
    """

    # Enable stateful discovery
    discovery_enabled: bool = Field(
        default=True, description="Enable dynamic discovery"
    )

    def discover_routing_destinations(self, state: Any) -> dict[str, str]:
        """Discover routing destinations from state dynamically."""
        if not self.discovery_enabled:
            return {"tool_node": self.tool_node, "parser_node": self.parser_node}

        discovered = {}

        # Strategy 1: From state routing_config
        if hasattr(state, "routing_config") and state.routing_config:
            routing_config = state.routing_config
            discovered["tool_node"] = routing_config.get("tool_node", self.tool_node)
            discovered["parser_node"] = routing_config.get(
                "parser_node", self.parser_node
            )

        # Strategy 2: From state attributes
        if hasattr(state, "tool_node_name"):
            discovered["tool_node"] = state.tool_node_name
        if hasattr(state, "parser_node_name"):
            discovered["parser_node"] = state.parser_node_name

        # Strategy 3: From SimpleAgent graph metadata
        if hasattr(state, "graph_metadata") and state.graph_metadata:
            metadata = state.graph_metadata
            if "tool_node" in metadata:
                discovered["tool_node"] = metadata["tool_node"]
            if "parser_node" in metadata:
                discovered["parser_node"] = metadata["parser_node"]

        # Fallback to configured values
        return {
            "tool_node": discovered.get("tool_node", self.tool_node),
            "parser_node": discovered.get("parser_node", self.parser_node),
        }

    def __call__(self, state: dict[str, Any]) -> Command:
        """Execute with dynamic discovery."""
        # Discover routing destinations
        routing = self.discover_routing_destinations(state)

        # Temporarily update routing for this execution
        original_tool_node = self.tool_node
        original_parser_node = self.parser_node

        try:
            self.tool_node = routing["tool_node"]
            self.parser_node = routing["parser_node"]

            # Call parent implementation
            return super().__call__(state)
        finally:
            # Restore original values
            self.tool_node = original_tool_node
            self.parser_node = original_parser_node


# =============================================================================
# EXAMPLE: Enhanced ParserNodeConfig with Stateful Discovery
# =============================================================================


class StatefulParserNodeV2(ParserNodeConfig):
    """Enhanced ParserNodeConfig with stateful discovery capabilities."""

    # Enable stateful discovery
    discovery_enabled: bool = Field(
        default=True, description="Enable dynamic discovery"
    )

    def discover_agent_node(self, state: Any) -> str:
        """Discover agent node destination from state."""
        if not self.discovery_enabled:
            return self.agent_node

        # Strategy 1: From state routing_config
        if hasattr(state, "routing_config") and state.routing_config:
            agent_node = state.routing_config.get("agent_node")
            if agent_node:
                return agent_node

        # Strategy 2: From state attributes
        if hasattr(state, "agent_node_name"):
            return state.agent_node_name

        # Strategy 3: From SimpleAgent metadata
        if hasattr(state, "graph_metadata") and state.graph_metadata:
            metadata = state.graph_metadata
            if "agent_node" in metadata:
                return metadata["agent_node"]

        # Fallback to configured value
        return self.agent_node

    def __call__(self, state: Any, config: Any | None = None) -> Command:
        """Execute with dynamic discovery."""
        # Discover agent node
        agent_node = self.discover_agent_node(state)

        # Temporarily update agent_node for this execution
        original_agent_node = self.agent_node

        try:
            self.agent_node = agent_node

            # Call parent implementation
            return super().__call__(state, config)
        finally:
            # Restore original value
            self.agent_node = original_agent_node


# =============================================================================
# EXAMPLE: Enhanced SimpleAgent with Stateful Node Support
# =============================================================================


class StatefulSimpleAgent(SimpleAgent):
    """Enhanced SimpleAgent that uses stateful nodes for dynamic discovery."""

    use_stateful_nodes: bool = Field(default=True, description="Use stateful nodes")

    def build_graph(self) -> Any:
        """Override build_graph to use stateful nodes."""
        if not self.use_stateful_nodes:
            return super().build_graph()

        # Use the existing build_graph logic but with stateful nodes
        from langgraph.graph import END, START

        from haive.core.graph.node.engine_node import EngineNodeConfig
        from haive.core.graph.node.tool_node_config_v2 import ToolNodeConfig
        from haive.core.graph.state_graph.base_graph2 import BaseGraph

        graph = BaseGraph(name=self.name)

        # Add engine node (same as before)
        engine_node = EngineNodeConfig(name="agent_node", engine=self.engine)
        graph.add_node("agent_node", engine_node)
        graph.add_edge(START, "agent_node")

        available_nodes = ["agent_node"]

        # Check what nodes we need
        needs_tool_node = self._needs_tool_node()
        needs_parser_node = self._needs_parser_node()
        has_force_tool_use = self._has_force_tool_use()

        if not needs_tool_node and not needs_parser_node:
            graph.add_edge("agent_node", END)
            return graph

        # Add tool node if needed
        if needs_tool_node:
            tool_config = ToolNodeConfig(
                name="tool_node",
                engine_name=self.engine.name,
            )
            graph.add_node("tool_node", tool_config)
            graph.add_edge("tool_node", END)
            available_nodes.append("tool_node")

        # Add parser node if needed (using stateful version)
        if needs_parser_node:
            parser_config = StatefulParserNodeV2(
                name="parse_output",
                engine_name=self.engine.name,
                discovery_enabled=True,
            )
            graph.add_node("parse_output", parser_config)
            graph.add_edge("parse_output", END)
            available_nodes.append("parse_output")

        # Add validation node (using stateful version)
        validation_config = StatefulValidationNodeV2(
            name="validation",
            engine_name=self.engine.name,
            tool_node="tool_node",
            parser_node="parse_output",
            available_nodes=available_nodes,
            discovery_enabled=True,
        )
        graph.add_node("validation", validation_config)
        available_nodes.append("validation")

        # Add routing
        if has_force_tool_use:
            graph.add_edge("agent_node", "validation")
        else:
            from haive.agents.simple.agent import has_tool_calls

            graph.add_conditional_edges(
                "agent_node", has_tool_calls, {True: "validation", False: END}
            )

        # Store metadata for stateful discovery
        graph.metadata["available_nodes"] = available_nodes
        graph.metadata["tool_routes"] = self.get_tool_routes()
        graph.metadata["stateful_routing"] = {
            "tool_node": "tool_node",
            "parser_node": "parse_output",
            "agent_node": "agent_node",
        }

        return graph

    def create_runnable(self, runnable_config: dict[str, Any] | None = None):
        """Override to inject routing config into state."""
        compiled = super().create_runnable(runnable_config)

        # Add routing configuration to initial state
        if (
            hasattr(self, "graph")
            and self.graph
            and hasattr(self.graph, "metadata")
            and "stateful_routing" in self.graph.metadata
        ):
            # This would be injected into the state during execution
            routing_config = self.graph.metadata["stateful_routing"]

            # Store routing config for stateful discovery
            if hasattr(compiled, "_initial_state"):
                compiled._initial_state["routing_config"] = routing_config
            elif hasattr(compiled, "_channels"):
                # Add routing_config channel
                from langgraph.channels import Value

                compiled._channels["routing_config"] = Value(routing_config)

        return compiled


# =============================================================================
# EXAMPLE: Practical Usage with Current Architecture
# =============================================================================


def practical_stateful_example() -> Any:
    """Practical example showing how stateful nodes work with current architecture."""
    # 1. Create a normal SimpleAgent (or use StatefulSimpleAgent)
    agent = StatefulSimpleAgent(
        name="practical_agent",
        engine=AugLLMConfig(name="practical_engine", model="gpt-4", temperature=0.7),
        use_stateful_nodes=True,
    )

    # 2. Create input that will trigger tool calls
    input_data = {
        "messages": [HumanMessage(content="Calculate 15 * 23 and explain the result")]
    }

    # 3. The agent will automatically:
    #    - Use StatefulValidationNodeV2 for validation
    #    - Use StatefulParserNodeV2 for parsing
    #    - Discover routing from graph metadata
    #    - Fall back to configured values

    # 4. Execute the agent
    try:
        result = agent.invoke(input_data)
        return result
    except Exception:
        return None


# =============================================================================
# EXAMPLE: Integration with MetaStateSchema
# =============================================================================


def meta_state_integration_example() -> Any:
    """Show how stateful nodes work with MetaStateSchema."""
    # 1. Create stateful agent
    agent = StatefulSimpleAgent(
        name="meta_agent", engine=AugLLMConfig(name="meta_engine", model="gpt-4")
    )

    # 2. Create meta state with routing configuration
    meta_state = MetaStateSchema(
        agent=agent,
        agent_state={
            "routing_config": {
                "tool_node": "custom_tool_executor",
                "parser_node": "custom_parser",
                "agent_node": "main_agent",
            }
        },
        graph_context={"discovery_mode": "full"},
    )

    # 3. Execute - the stateful nodes will discover the custom routing
    meta_state.execute_agent(
        input_data={"messages": [HumanMessage(content="Test message")]}
    )

    return meta_state


# =============================================================================
# EXAMPLE: Backward Compatibility
# =============================================================================


def backward_compatibility_example() -> dict[str, Any]:
    """Show that existing code continues to work unchanged."""
    # 1. Create regular SimpleAgent (existing code)
    regular_agent = SimpleAgent(
        name="regular_agent", engine=AugLLMConfig(name="regular_engine", model="gpt-4")
    )

    # 2. Create stateful agent
    stateful_agent = StatefulSimpleAgent(
        name="stateful_agent",
        engine=AugLLMConfig(name="stateful_engine", model="gpt-4"),
        use_stateful_nodes=True,
    )

    # 3. Both work the same way
    input_data = {"messages": [HumanMessage(content="Hello")]}

    regular_result = regular_agent.invoke(input_data)
    stateful_result = stateful_agent.invoke(input_data)

    # 4. But stateful agent can discover routing dynamically
    return {"regular": regular_result, "stateful": stateful_result}


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":

    practical_stateful_example()

    meta_state_integration_example()

    backward_compatibility_example()
