"""From typing import Any, Dict
Stateful Node Integration Example - How it works with SimpleAgent and LLMState.

This example shows how the stateful node architecture integrates with the existing
SimpleAgent, LLMState, and MetaStateSchema to provide truly dynamic discovery.
"""

from haive.agents.simple.agent import SimpleAgent
from langchain_core.messages import AIMessage, HumanMessage

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.stateful_node_config import (
    StatefulParserNodeConfig,
    StatefulValidationNodeConfig,
)
from haive.core.schema.prebuilt.llm_state import LLMState
from haive.core.schema.prebuilt.meta_state import MetaStateSchema

# =============================================================================
# EXAMPLE 1: SimpleAgent with Stateful Nodes
# =============================================================================


def create_simple_agent_with_stateful_nodes() -> Any:
    """Create a SimpleAgent that uses stateful nodes for dynamic discovery."""
    # Create engine
    engine = AugLLMConfig(
        name="main_engine",
        model="gpt-4",
        temperature=0.7,
        tools=["calculator", "search"],
    )

    # Create SimpleAgent (which registers engine in engines dict)
    agent = SimpleAgent(name="stateful_agent", engine=engine, temperature=0.7)

    # The agent's setup_agent() method:
    # 1. Adds engine to self.engines["main"]
    # 2. Registers engine in EngineRegistry
    # 3. Sets up tool routes

    return agent


# =============================================================================
# EXAMPLE 2: LLMState with Dynamic Engine Discovery
# =============================================================================


def create_llm_state_with_dynamic_nodes() -> Any:
    """Create LLMState that works with stateful nodes."""
    # Create engine
    engine = AugLLMConfig(name="llm_engine", model="gpt-4-turbo", temperature=0.3)

    # Create LLMState (which manages engine automatically)
    state = LLMState(
        engine=engine,
        messages=[
            HumanMessage(content="Calculate 15 * 23"),
            AIMessage(
                content="I'll calculate that for you.",
                tool_calls=[
                    {
                        "name": "calculator",
                        "id": "calc_1",
                        "args": {"expression": "15 * 23"},
                    }
                ],
            ),
        ],
    )

    # LLMState automatically:
    # 1. Puts engine in engines["main"], engines["llm"], engines["primary"]
    # 2. Tracks token usage
    # 3. Provides engine metadata

    return state


# =============================================================================
# EXAMPLE 3: How Stateful Nodes Discover from State
# =============================================================================


def demonstrate_stateful_discovery() -> Any:
    """Show how stateful nodes discover resources from state."""
    # Create state with engine and routing configuration
    state = LLMState(
        engine=AugLLMConfig(name="discovery_engine", model="gpt-4"),
        messages=[
            HumanMessage(content="Test message"),
            AIMessage(
                content="Response",
                tool_calls=[
                    {
                        "name": "Plan",
                        "id": "plan_1",
                        "args": {"task": "analyze", "steps": ["step1", "step2"]},
                    }
                ],
            ),
        ],
    )

    # Add routing configuration to state
    state.routing_config = {
        "tool_node": "execute_tools",
        "parser_node": "parse_results",
        "agent_node": "main_agent",
    }

    # Add node registry
    state.node_registry = {
        "execute_tools": "tool_execution_node",
        "parse_results": "result_parser_node",
        "main_agent": "agent_node",
    }

    # Create stateful validation node
    validation_node = StatefulValidationNodeConfig(
        name="stateful_validation",
        engine_name="discovery_engine",  # Will try this first
        routing_prefix="validation_",  # Will look for validation_tool_node
        fallback_routing={
            "tool_node": "execute_tools",
            "parser_node": "parse_results",
            "default": "END",
        },
    )

    # Execute validation - it will discover:
    # 1. Engine from state.engines["discovery_engine"]
    # 2. tool_node from state.routing_config["tool_node"]
    # 3. parser_node from state.routing_config["parser_node"]
    result = validation_node(state)

    return result


# =============================================================================
# EXAMPLE 4: MetaStateSchema with Stateful Agent Composition
# =============================================================================


def demonstrate_meta_state_composition() -> Any:
    """Show how MetaStateSchema works with stateful nodes."""
    # Create inner agent with stateful nodes
    inner_agent = SimpleAgent(
        name="inner_agent",
        engine=AugLLMConfig(name="inner_engine", model="gpt-4"),
        structured_output_model=None,  # Could be any Pydantic model
    )

    # Create meta state containing the agent
    meta_state = MetaStateSchema(
        agent=inner_agent,
        agent_state={"initialized": True},
        graph_context={"composition_type": "stateful"},
    )

    # The meta state can execute the inner agent
    # The inner agent's nodes will discover engines from the meta state
    meta_state.execute_agent(
        input_data={"messages": [HumanMessage(content="Hello from meta state")]}
    )

    return meta_state


# =============================================================================
# EXAMPLE 5: Dynamic Field Configuration
# =============================================================================


def demonstrate_dynamic_field_configuration() -> Any:
    """Show how nodes discover field configurations dynamically."""
    # Create state with custom field mapping
    state = LLMState(engine=AugLLMConfig(name="field_engine", model="gpt-4"))

    # Add field mapping configuration
    state.field_mapping = {
        "messages": "chat_history",  # Map messages to chat_history
        "tools": "available_tools",  # Map tools to available_tools
        "result": "parsed_output",  # Map result to parsed_output
    }

    # Add tool routes
    state.tool_routes = {
        "Plan": "pydantic_model",
        "calculator": "langchain_tool",
        "search": "function",
    }

    # Create stateful parser node
    parser_node = StatefulParserNodeConfig(
        name="dynamic_parser",
        engine_name="field_engine",
        field_discovery_enabled=True,
        auto_field_mapping=True,
    )

    # Parser will discover:
    # 1. Engine from state.engines["field_engine"]
    # 2. Field mappings from state.field_mapping
    # 3. Tool routes from state.tool_routes
    # 4. Agent node from state.routing_config or fallback

    return parser_node


# =============================================================================
# EXAMPLE 6: Integration with Existing SimpleAgent Graph
# =============================================================================


def show_integration_with_simple_agent() -> Any:
    """Show how stateful nodes integrate with existing SimpleAgent graph building."""
    # Create SimpleAgent as usual
    agent = SimpleAgent(
        name="integrated_agent",
        engine=AugLLMConfig(name="integrated_engine", model="gpt-4"),
        tools=["calculator", "search"],
    )

    # Override build_graph to use stateful nodes
    def build_stateful_graph(agent_instance: Any):
        from langgraph.graph import END, START

        from haive.core.graph.node.engine_node import EngineNodeConfig
        from haive.core.graph.state_graph.base_graph2 import BaseGraph

        graph = BaseGraph(name=agent_instance.name)

        # Add engine node as usual
        engine_node = EngineNodeConfig(name="agent_node", engine=agent_instance.engine)
        graph.add_node("agent_node", engine_node)
        graph.add_edge(START, "agent_node")

        # Add stateful validation node instead of regular
        # ValidationNodeConfigV2
        validation_node = StatefulValidationNodeConfig(
            name="stateful_validation",
            engine_name=agent_instance.engine.name,
            discovery_enabled=True,
            routing_discovery_enabled=True,
            field_discovery_enabled=True,
            fallback_routing={
                "tool_node": "tool_node",
                "parser_node": "parse_output",
                "default": "END",
            },
        )
        graph.add_node("validation", validation_node)

        # Add stateful parser node
        parser_node = StatefulParserNodeConfig(
            name="stateful_parsef",
            engine_name=agent_instance.engine.name,
            discovery_enabled=True,
            fallback_routing={"agent_node": "agent_node", "default": "END"},
        )
        graph.add_node("parse_output", parser_node)

        # Add routing
        graph.add_conditional_edges(
            "agent_node",
            lambda state: (
                bool(getattr(state.messages[-1], "tool_calls", None))
                if state.messages
                else False
            ),
            {True: "validation", False: END},
        )

        return graph

    # Replace the agent's build_graph method
    agent.build_graph = lambda: build_stateful_graph(agent)

    return agent


# =============================================================================
# EXAMPLE 7: Complete Integration Example
# =============================================================================


def complete_integration_example() -> dict[str, Any]:
    """Complete example showing all components working together."""
    # 1. Create base components
    engine = AugLLMConfig(
        name="complete_engine",
        model="gpt-4",
        temperature=0.7,
        tools=["calculator", "search"],
    )

    # 2. Create agent with stateful capabilities
    agent = SimpleAgent(name="complete_agent", engine=engine)

    # 3. Create state that supports dynamic discovery
    state = LLMState.from_engine(engine)

    # 4. Add configuration for dynamic discovery
    state.routing_config = {
        "tool_node": "execute_tools",
        "parser_node": "parse_results",
        "agent_node": "main_agent",
    }

    state.field_mapping = {
        "messages": "messages",
        "tools": "available_tools",
        "engine": "llm_engine",
    }

    # 5. Create meta state for composition
    meta_state = MetaStateSchema.from_agent(
        agent=agent,
        initial_state=state.model_dump(),
        graph_context={"discovery_mode": "full"},
    )

    # 6. Execute with full dynamic discovery
    result = meta_state.execute_agent(
        input_data={
            "messages": [
                HumanMessage(content="Calculate 15 * 23 and explain the result")
            ]
        }
    )

    return {"agent": agent, "state": state, "meta_state": meta_state, "result": result}


# =============================================================================
# KEY INSIGHTS FROM INTEGRATION
# =============================================================================

"""
KEY INSIGHTS:

1. **SimpleAgent Already Does Discovery**:
   - Registers engine in engines dict
   - Creates tool routes
   - Passes engine_name to nodes

2. **LLMState Provides Foundation**:
   - Manages multiple engines
   - Tracks token usage
   - Provides engine metadata

3. **MetaStateSchema Enables Composition**:
   - Contains agents in state
   - Executes agents with recompilation
   - Manages graph-level coordination

4. **Stateful Nodes Enhance Discovery**:
   - Find engines from state.engines
   - Discover routing from state.routing_config
   - Auto-map fields from state.field_mapping
   - Fallback to existing patterns

5. **No Breaking Changes Needed**:
   - Existing ValidationNodeConfigV2 → StatefulValidationNodeConfig
   - Existing ParserNodeConfigV2 → StatefulParserNodeConfig
   - Same interfaces, enhanced discovery

6. **Progressive Enhancement**:
   - Works with existing SimpleAgent architecture
   - Can be adopted gradually
   - Maintains backward compatibility
"""

if __name__ == "__main__":

    # Run examples
    agent = create_simple_agent_with_stateful_nodes()

    state = create_llm_state_with_dynamic_nodes()

    demonstrate_stateful_discovery()

    demonstrate_meta_state_composition()

    complete_integration_example()
