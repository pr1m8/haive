# src/haive/agents/simple/routing_agent.py

import logging
from collections.abc import Callable

from agents.simple.agent import SimpleAgent, SimpleAgentConfig, SimpleAgentSchema
from haive.core.engine.agent.agent import register_agent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from langgraph.graph import END
from pydantic import BaseModel, Field

# Set up logging
logger = logging.getLogger(__name__)


# Extend SimpleAgentSchema to track routing state
class RoutingAgentSchema(SimpleAgentSchema):
    """Schema for routing agents."""

    current_node: str = Field(default="start", description="Current node in workflow")
    route_history: list[str] = Field(
        default_factory=list, description="History of routing"
    )


# Configuration for routing agent
class RoutingAgentConfig(SimpleAgentConfig):
    """Configuration for a routing agent."""

    # Override schema
    state_schema: type[BaseModel] = Field(default=RoutingAgentSchema)

    # Routing nodes (LLM engines or functions)
    handlers: dict[str, AugLLMConfig | Callable] = Field(
        default_factory=dict, description="Handler nodes (LLMs or functions)"
    )

    # Routing conditions
    conditions: dict[str, list[Callable]] = Field(
        default_factory=dict, description="Routing conditions by source node"
    )

    # Default routes
    default_routes: dict[str, str] = Field(
        default_factory=dict, description="Default routes when no conditions match"
    )


@register_agent(RoutingAgentConfig)
class RoutingAgent(SimpleAgent):
    """Simple agent with conditional routing capabilities."""

    def setup_workflow(self) -> None:
        """Set up the workflow with routing."""
        # Use DynamicGraph to build the workflow
        gb = DynamicGraph(
            components=[self.config.engine] + list(self.config.handlers.values()),
            state_schema=self.state_schema,
        )

        # Add the main node (from SimpleAgent)
        gb.add_node(name=self.config.node_name, config=self.config.engine)

        # Set main node's default route
        main_default = self.config.default_routes.get(self.config.node_name, END)

        # Add handlers
        for name, handler in self.config.handlers.items():
            gb.add_node(
                name=name,
                config=handler,
                command_goto=self.config.default_routes.get(name, END),
            )

        # Add routing conditions
        for source, conditions in self.config.conditions.items():
            # Get default destination
            default_dest = self.config.default_routes.get(source, END)

            # Create router function
            def route_function(state):
                # Track the node we're in
                if hasattr(state, "current_node"):
                    state.current_node = source
                    if hasattr(state, "route_history"):
                        state.route_history.append(source)

                # Check each condition
                for condition in conditions:
                    if condition(state):
                        # Get destination from condition name
                        # This is a simple approach - in practice, we'd want a more robust mapping
                        condition_name = condition.__name__
                        if condition_name.startswith("route_to_"):
                            dest = condition_name[
                                9:
                            ]  # Extract destination from "route_to_X"
                            return dest

                # No conditions matched, use default
                return "default"

            # Build routing map
            route_map = {}
            for condition in conditions:
                condition_name = condition.__name__
                if condition_name.startswith("route_to_"):
                    dest = condition_name[9:]
                    route_map[condition_name] = dest

            # Add default route
            route_map["default"] = default_dest

            # Add conditional edges
            gb.add_conditional_edges(source, route_function, route_map)

        # Build the graph
        self.graph = gb.build()
        logger.info(f"Set up routing workflow for {self.config.name}")


# Helper function to create a routing agent
def create_routing_agent(
    main_engine: AugLLMConfig,
    handlers: dict[str, AugLLMConfig | Callable],
    conditions: dict[str, list[Callable]],
    default_routes: dict[str, str],
    system_prompt: str = "You are a helpful assistant.",
    name: str | None = None,
) -> RoutingAgent:
    """Create a routing agent with the specified components.

    Args:
        main_engine: Main LLM engine
        handlers: Dictionary of handler nodes
        conditions: Routing conditions by source node
        default_routes: Default routes by source node
        system_prompt: System prompt for the agent
        name: Optional name for the agent

    Returns:
        RoutingAgent instance
    """
    # Create config
    config = RoutingAgentConfig(
        engine=main_engine,
        handlers=handlers,
        conditions=conditions,
        default_routes=default_routes,
        system_prompt=system_prompt,
        name=name or "routing_agent",
    )

    # Build and return agent
    return config.build_agent()


# Example usage
if __name__ == "__main__":
    from haive.core.models.llm.base import AzureLLMConfig
    from langchain_core.prompts import ChatPromptTemplate

    # Main engine
    main_engine = AugLLMConfig(
        name="main_processor", llm_config=AzureLLMConfig(model="gpt-4o")
    )

    # Handler nodes
    handlers = {
        "question_handler": AugLLMConfig(
            name="question_handler",
            llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.3}),
            prompt_template=ChatPromptTemplate.from_messages(
                [
                    ("system", "You answer questions concisely with facts only."),
                    ("human", "{input}"),
                ]
            ),
        ),
        "task_handler": AugLLMConfig(
            name="task_handler",
            llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.7}),
            prompt_template=ChatPromptTemplate.from_messages(
                [
                    ("system", "You help complete tasks step by step."),
                    ("human", "{input}"),
                ]
            ),
        ),
    }

    # Routing conditions
    def route_to_question_handler(state):
        # Check if input is a question
        message = state["messages"][-1].content
        return (
            "?" in message
            or message.lower().startswith("what")
            or message.lower().startswith("how")
        )

    def route_to_task_handler(state):
        # Check if input is a task
        message = state["messages"][-1].content
        task_phrases = ["can you", "please", "help me", "i need"]
        return any(phrase in message.lower() for phrase in task_phrases)

    # Add routing condition for main node
    conditions = {
        "simple_agent_node": [route_to_question_handler, route_to_task_handler]
    }

    # Default routes
    default_routes = {
        "simple_agent_node": END,
        "question_handler": END,
        "task_handler": END,
    }

    # Create the agent
    agent = create_routing_agent(
        main_engine=main_engine,
        handlers=handlers,
        conditions=conditions,
        default_routes=default_routes,
    )

    # Run with a question
    result = agent.run("What is the capital of France?")
    print(
        f"Question result: {result.get('route_history', [])} -> {result.get('output', '')}"
    )

    # Run with a task
    result = agent.run("Can you help me create a workout plan?")
    print(
        f"Task result: {result.get('route_history', [])} -> {result.get('output', '')}"
    )
