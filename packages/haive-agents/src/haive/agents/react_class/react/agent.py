import logging
from typing import Any

from haive.core.engine.agent.agent import Agent, register_agent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.tools import BaseTool
from langgraph.graph import END

from haive.agents.react_class.react.config import ReactAgentConfig
from haive.agents.react_class.react.tool_utils import (
    create_tool_executor,
    create_tool_executor_v2,
    filter_tools_for_query,
    prepare_tools,
    tools_router,
    tools_router_v2,
)

logger = logging.getLogger(__name__)


@register_agent(ReactAgentConfig)
class ReactAgent(Agent[ReactAgentConfig]):
    """React Agent implementation that extends SimpleAgent.

    Enables multi-step reasoning and tool usage by routing between
    an LLM and tool execution nodes.
    """

    def __init__(self, config: ReactAgentConfig):
        """Initialize the React Agent with its configuration."""
        super().__init__(config)
        self.config = config
        self.version = getattr(config, "version", "v1")

        # Prepare tools
        self.tools = prepare_tools(self.config.tools)
        logger.debug(f"Prepared {len(self.tools)} tools for React Agent")

    def setup_workflow(self) -> None:
        """Set up the React Agent workflow graph."""
        logger.debug(f"Setting up workflow for ReactAgent {self.config.name}")

        # Create dynamic graph builder
        gb = DynamicGraph(
            name=f"{self.config.name}_react_agent",
            components=[self.config.engine],
            state_schema=self.config.state_schema,
        )

        # Add system message if provided
        if self.config.system_prompt:
            self._add_system_message_node(gb)

        # Set up the LLM with tool binding
        self._setup_llm_node(gb)

        # Set up tool execution
        if self.config.version == "v1":
            self._setup_tools_v1(gb)
        else:
            self._setup_tools_v2(gb)

        # Add structured output node if schema provided
        if self.config.structured_output_schema:
            self._add_structured_output_node(gb)

        # Build the graph
        self.graph = gb.build()
        logger.info(f"Set up React workflow for {self.config.name}")

    def _add_system_message_node(self, gb: DynamicGraph) -> None:
        """Add a node for adding a system message to the state."""

        def add_system_message(state: dict[str, Any]) -> dict[str, Any]:
            """Add system message if none exists yet."""
            messages = state.get("messages", [])

            # Check if we already have a system message
            has_system = any(
                isinstance(m, SystemMessage)
                for m in messages
                if isinstance(m, BaseMessage)
            )

            if not has_system:
                # Add system message at the beginning
                system_msg = SystemMessage(content=self.config.system_prompt)

                # Return the updated messages list
                return {"messages": [system_msg]}

            # No change needed
            return {}

        # Add the node and connect it
        gb.add_node("add_system", add_system_message, self.config.llm_node_name)
        gb.set_entry_point("add_system")  # Make this the entry point

    def _setup_llm_node(self, gb: DynamicGraph) -> None:
        """Set up the LLM node with tool binding."""
        # Get the engine as a runnable
        llm_engine = self.config.engine

        # If it's an AugLLMConfig and has no tools bound yet, bind them
        if isinstance(llm_engine, AugLLMConfig) and not llm_engine.tools:
            llm_engine.tools = self.config.tools

            # Set tool_choice if specified
            if hasattr(self.config, "tool_choice") and self.config.tool_choice:
                if not llm_engine.bind_tools_kwargs:
                    llm_engine.bind_tools_kwargs = {}

                llm_engine.bind_tools_kwargs["tool_choice"] = self.config.tool_choice

        # Add the LLM node
        gb.add_node(
            name=self.config.llm_node_name,
            config=llm_engine,
            # Router function will handle routing decision
            command_goto=None,
        )

        # If no system message, set this as entry point
        if not self.config.system_prompt:
            gb.set_entry_point(self.config.llm_node_name)

    def _setup_tools_v1(self, gb: DynamicGraph) -> None:
        """Set up tools for v1 architecture (all tool calls in one node)."""
        # Create tool executor for all tools
        execute_tools_fn = create_tool_executor(self.tools)

        # Add tools node
        gb.add_node(
            name=self.config.tool_node_name,
            config=execute_tools_fn,
            command_goto=self.config.llm_node_name,  # Always return to LLM after executing tools
        )

        # Add router from agent to tools
        gb.add_conditional_edges(
            self.config.llm_node_name,
            tools_router,
            {self.config.tool_node_name: self.config.tool_node_name, END: END},
        )

    def _setup_tools_v2(self, gb: DynamicGraph) -> None:
        """Set up tools for v2 architecture (each tool call in separate node)."""
        # Create tool executor for individual tool calls
        execute_tool_fn = create_tool_executor_v2(self.config.tools)

        # Add tools node
        gb.add_node(
            name=self.config.tool_node_name,
            config=execute_tool_fn,
            command_goto=self.config.llm_node_name,  # Always return to LLM after executing tools
        )

        # Add router from agent to tools
        gb.add_conditional_edges(
            self.config.llm_node_name,
            tools_router_v2,
            routes=None,  # Using dynamic Send objects, not static routes
        )

    def _add_structured_output_node(self, gb: DynamicGraph) -> None:
        """Add a node for generating structured output."""
        # Use the built-in structured output node from DynamicGraph
        gb.add_structured_output_node(
            name=self.config.output_node_name,
            model=self.config.structured_output_schema,
            command_goto=END,
        )

        # Add edge from LLM to structured output if not already there
        try:
            gb.add_edge(self.config.llm_node_name, self.config.output_node_name)
        except Exception:
            # Edge might already exist via the router
            pass

    def filter_tools_for_query(self, query: str) -> list[BaseTool]:
        """Filter tools based on the user query."""
        return filter_tools_for_query(self.tools, query)

    def run_with_filtered_tools(
        self, input_data: str | dict[str, Any], filter_tools: bool = True, **kwargs
    ) -> dict[str, Any]:
        """Run agent with dynamically filtered tools based on the query.

        Args:
            input_data: Input query or state
            filter_tools: Whether to filter tools based on query
            **kwargs: Additional parameters for running

        Returns:
            Result from agent execution
        """
        # Extract query from input
        query = (
            input_data if isinstance(input_data, str) else input_data.get("query", "")
        )

        if filter_tools and query:
            # Filter tools based on query
            filtered_tools = self.filter_tools_for_query(query)

            # Store original tools
            original_tools = self.tools

            # Set filtered tools
            self.tools = filtered_tools

            # Rebuild the graph with filtered tools
            self.setup_workflow()
            self.compile()

            try:
                # Run with filtered tools
                result = self.run(input_data, **kwargs)
                return result
            finally:
                # Restore original tools
                self.tools = original_tools
                self.setup_workflow()
                self.compile()
        else:
            # Run with all tools
            return self.run(input_data, **kwargs)


a = ReactAgent(ReactAgentConfig())
a.run("What is the capital of France?")
