"""ReactAgent implementation with tool usage and ReAct pattern.

This module implements a tool-using agent that follows the ReAct pattern
(Reasoning, Acting, and Observing) for solving tasks.
"""

import logging
from typing import Any

from haive.core.engine.agent.agent import Agent, register_agent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from haive.core.schema.schema_composer import SchemaComposer
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langgraph.graph import END, StateGraph
from pydantic import BaseModel

from haive.agents.react_class.react_v3.config import ReactAgentConfig

# Set up logging
logger = logging.getLogger(__name__)


@register_agent(ReactAgentConfig)
class ReactAgent(Agent[ReactAgentConfig]):
    """A tool-using agent implementing the ReAct pattern.

    Features:
    - Integration with LangChain tools
    - Automatic schema composition from tools and engine
    - Reasoning → Tool Use → Observation cycle
    - Retry policies for resilience
    - Configurable termination conditions
    """

    def setup_workflow(self) -> None:
        """Set up the ReAct workflow with reasoning and tool execution nodes.

        This creates a graph with:
        1. A reasoning node that decides what to do
        2. A tool execution node that carries out actions
        3. Conditional branching based on message types
        """
        logger.info(f"Setting up workflow for {self.config.name}")

        # Auto-derive schema if not provided
        if self.config.state_schema is None:
            components = [self.config.engine, *self.config.tools]
            schema_composer = SchemaComposer.from_components(components)
            self.config.state_schema = schema_composer.build()
            logger.info(
                f"Auto-derived state schema: {self.config.state_schema.__name__}"
            )

        # Create dynamic graph with state schema
        gb = DynamicGraph(
            name=self.config.name,
            components=[self.config.engine, *self.config.tools],
            state_schema=self.config.state_schema,
            visualize=self.config.visualize,
        )

        # Configure reasoning node
        gb.add_node(
            name=self.config.reasoning_node_name,
            config=self.config.engine,
            retry=self.config.reasoning_retry,
        )

        # Configure tool node
        gb.add_node(
            name=self.config.tool_node_name,
            function=self._create_tool_node(),
            retry=self.config.tool_retry,
        )

        # Add conditional branching
        gb.add_conditional_edges(
            self.config.reasoning_node_name,
            self._should_use_tool,
            {True: self.config.tool_node_name, False: END},
        )

        # Add edge from tool node back to reasoning
        gb.add_edge(self.config.tool_node_name, self.config.reasoning_node_name)

        # Set entry point to reasoning
        gb.set_entry_point(self.config.reasoning_node_name)

        # Build the graph
        self.graph = gb.build()

        logger.info(f"Workflow setup complete for {self.config.name}")

    def _create_tool_node(self):
        """Create a function that handles tool execution.

        Returns:
            Function that executes the appropriate tool based on state
        """
        # Get tools indexed by name
        tools_by_name = self.config.get_tools_by_name()

        def execute_tool(state):
            """Execute the appropriate tool based on the last AI message."""
            # Get messages
            messages = state.get("messages", [])

            # Find the last AI message with tool calls
            tool_call_message = None
            for message in reversed(messages):
                if (
                    isinstance(message, AIMessage)
                    and hasattr(message, "tool_calls")
                    and message.tool_calls
                ):
                    tool_call_message = message
                    break

            if not tool_call_message:
                logger.warning("No tool call found in messages")
                return {"messages": messages}

            # Process each tool call
            for tool_call in tool_call_message.tool_calls:
                tool_name = tool_call.get("name")
                tool_args = tool_call.get("args", {})
                tool_id = tool_call.get("id", "tool_call")

                if tool_name not in tools_by_name:
                    error_msg = f"Tool '{tool_name}' not found"
                    messages.append(
                        ToolMessage(content=error_msg, tool_call_id=tool_id)
                    )
                    continue

                # Execute the tool
                tool = tools_by_name[tool_name]
                try:
                    logger.debug(f"Executing tool: {tool_name} with args: {tool_args}")
                    result = tool.invoke(tool_args)

                    # Add result as ToolMessage
                    messages.append(
                        ToolMessage(content=str(result), tool_call_id=tool_id)
                    )
                except Exception as e:
                    error_msg = f"Error executing tool '{tool_name}': {e!s}"
                    logger.exception(error_msg)
                    messages.append(
                        ToolMessage(content=error_msg, tool_call_id=tool_id)
                    )

            return {"messages": messages}

        return execute_tool

    def _should_use_tool(self, state) -> bool:
        """Determine if we should use a tool based on the last message.

        Args:
            state: Current state with messages

        Returns:
            True if we should use a tool, False otherwise
        """
        # Get messages
        messages = state.get("messages", [])

        if not messages:
            return False

        # Check the last message
        last_message = messages[-1]

        # If last message is from AI and has tool calls, use tools
        if (
            isinstance(last_message, AIMessage)
            and hasattr(last_message, "tool_calls")
            and last_message.tool_calls
        ):
            return True

        # If we've reached max iterations, stop
        ai_messages = [m for m in messages if isinstance(m, AIMessage)]
        if len(ai_messages) >= self.config.max_iterations:
            logger.info(
                f"Reached maximum iterations ({self.config.max_iterations}), stopping"
            )
            return False

        # If last message is from a tool, we should go back to reasoning
        if isinstance(last_message, ToolMessage):
            return False

        return False

    def run(self, input_data: Any) -> Any:
        """Run the agent on the provided input.

        Args:
            input_data: Input in various formats

        Returns:
            Agent result
        """
        # Ensure graph is compiled
        self.compile()

        # Process input data
        processed_input = self._prepare_input(input_data)

        # Invoke the graph
        result = self.graph.invoke(processed_input)

        return result

    def _prepare_input(self, input_data: Any) -> dict[str, Any]:
        """Prepare input for the agent.

        Args:
            input_data: Raw input in various formats

        Returns:
            Properly formatted input dictionary
        """
        # Handle string input
        if isinstance(input_data, str):
            return {"messages": [HumanMessage(content=input_data)]}

        # Handle list of messages
        if isinstance(input_data, list) and all(
            isinstance(m, BaseMessage) for m in input_data
        ):
            return {"messages": input_data}

        # Handle dictionary input
        if isinstance(input_data, dict):
            # If no messages field, try to create one from other fields
            if "messages" not in input_data:
                for field in ["input", "query", "content"]:
                    if field in input_data and isinstance(input_data[field], str):
                        input_data["messages"] = [
                            HumanMessage(content=input_data[field])
                        ]
                        break
            return input_data

        # Handle Pydantic model input
        if isinstance(input_data, BaseModel):
            model_dict = input_data.model_dump()
            return self._prepare_input(model_dict)

        # Default case: wrap in dictionary
        return {"input": input_data}

    @classmethod
    def from_tools(
        cls,
        tools: list[Any],
        llm: AugLLMConfig | None = None,
        system_prompt: str | None = None,
        **kwargs,
    ) -> "ReactAgent":
        """Create a ReactAgent from a list of tools.

        Args:
            tools: List of tools to use
            llm: Optional LLM configuration (auto-created if not provided)
            system_prompt: Optional system prompt
            **kwargs: Additional configuration parameters

        Returns:
            Configured ReactAgent instance
        """
        from haive.core.engine.aug_llm import AugLLMConfig

        # Create LLM if not provided
        if llm is None:
            llm = AugLLMConfig(
                name="react_llm",
                model="gpt-4o",
                system_prompt=system_prompt
                or (
                    "You are a helpful assistant with access to tools. "
                    "Use these tools to help the user with their request."
                ),
            )
        elif system_prompt:
            # Update system prompt if provided
            llm.system_prompt = system_prompt

        # Create config
        config = ReactAgentConfig(
            name=kwargs.pop("name", "react_agent"), engine=llm, tools=tools, **kwargs
        )

        # Build and return agent
        return config.build_agent()

    @classmethod
    def from_langgraph(cls, react_state_graph: StateGraph, **kwargs) -> "ReactAgent":
        """Create a ReactAgent from an existing LangGraph StateGraph.

        This allows using LangGraph's `create_react_agent` directly and then
        wrapping it with our ReactAgent class.

        Args:
            react_state_graph: Existing React agent StateGraph
            **kwargs: Additional configuration parameters

        Returns:
            ReactAgent instance wrapping the provided StateGraph
        """
        from haive.core.engine.aug_llm import AugLLMConfig

        # Create minimal config
        config = ReactAgentConfig(
            name=kwargs.pop("name", "langgraph_react_agent"),
            engine=AugLLMConfig(),  # Placeholder
            **kwargs,
        )

        # Create agent
        agent = cls(config)

        # Replace graph with provided StateGraph
        agent.graph = react_state_graph

        return agent
