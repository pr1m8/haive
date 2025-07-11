# src/haive/agents/react_agent2/agent2.py
import logging
import uuid
from collections.abc import Callable
from typing import Any

from haive.core.engine.agent.agent import Agent, register_agent
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from haive.core.utils.message_utils import normalize_message, normalize_messages
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import BaseTool, StructuredTool, Tool
from langgraph.graph import END
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel

from haive.agents.react_class.react_agent2.config2 import ReactAgentConfig

# Set up logging
logger = logging.getLogger(__name__)


# Helper function to check if the last message has tool calls
def has_tool_calls(state):
    """Check if the last message has tool calls."""
    # Get messages from the state based on its type
    if isinstance(state, dict):
        messages = state.get("messages", [])
    elif hasattr(state, "messages"):
        messages = state.messages
    else:
        return False

    # No messages, no tool calls
    if not messages:
        return False

    # Get the last message
    last_message = messages[-1]

    # Handle different message types
    if isinstance(last_message, AIMessage):
        # Check direct tool_calls attribute
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return True

        # Check in additional_kwargs
        if (
            hasattr(last_message, "additional_kwargs")
            and "tool_calls" in last_message.additional_kwargs
            and last_message.additional_kwargs["tool_calls"]
        ):
            return True

    # Dict format - from LangChain's response
    elif isinstance(last_message, dict):
        if last_message.get("type") == "ai":
            additional_kwargs = last_message.get("additional_kwargs", {})
            tool_calls = additional_kwargs.get("tool_calls", [])
            return bool(tool_calls)

        # Direct tool_calls in dict
        if last_message.get("tool_calls"):
            return True

    return False


# Custom wrapper for ToolNode to ensure proper message normalization
class MessageNormalizingToolNode:
    """A wrapper around ToolNode that ensures proper serialization and message type compatibility.
    This fixes the Pydantic serialization warnings by properly normalizing message objects.
    """

    def __init__(self, tools):
        """Initialize with the tools to use."""
        self.tools = tools
        self.tool_node = ToolNode(tools)

    def __call__(self, state):
        """Process the state with tools, ensuring message compatibility."""
        # Convert state to dict if needed
        state_dict = state.model_dump() if hasattr(state, "model_dump") else dict(state)

        # Normalize messages to proper BaseMessage objects
        if "messages" in state_dict:
            from langchain_core.messages import (
                AIMessage,
                HumanMessage,
                SystemMessage,
                ToolMessage,
            )

            normalized_messages = []
            for msg in state_dict["messages"]:
                # Already a proper message object
                if isinstance(
                    msg, AIMessage | HumanMessage | SystemMessage | ToolMessage
                ):
                    normalized_messages.append(msg)
                # Dict representation of a message
                elif isinstance(msg, dict):
                    msg_type = msg.get("type")
                    content = msg.get("content", "")

                    if msg_type == "ai":
                        additional_kwargs = msg.get("additional_kwargs", {})
                        normalized_messages.append(
                            AIMessage(
                                content=content, additional_kwargs=additional_kwargs
                            )
                        )
                    elif msg_type == "human":
                        normalized_messages.append(HumanMessage(content=content))
                    elif msg_type == "system":
                        normalized_messages.append(SystemMessage(content=content))
                    elif msg_type == "tool":
                        tool_call_id = msg.get("tool_call_id")
                        name = msg.get("name", "")
                        normalized_messages.append(
                            ToolMessage(
                                content=content, tool_call_id=tool_call_id, name=name
                            )
                        )
                # Unknown type, default to HumanMessage
                else:
                    normalized_messages.append(HumanMessage(content=str(msg)))

            # Replace with normalized messages
            state_dict["messages"] = normalized_messages

        # Process with the actual tool node
        result = self.tool_node.invoke(state_dict)

        return result


# =============================================
# React Agent Implementation
# =============================================

# =============================================
# React Agent Implementation
# =============================================


@register_agent(ReactAgentConfig)
class ReactAgent(Agent[ReactAgentConfig]):
    """A React agent implementation using LangGraph.

    This agent implements the ReAct pattern (Reasoning, Action, Observation)
    to solve complex tasks using language models and tools.
    """

    def __init__(self, config: ReactAgentConfig):
        """Initialize the ReactAgent with a configuration.

        Args:
            config: ReactAgentConfig instance
        """
        # Store tools for easy access
        self.tools = config.tools

        # Update engine with system prompt if provided
        if config.system_prompt:
            self._update_system_prompt(config)

        # Initialize tool node
        self.tool_node = MessageNormalizingToolNode(config.tools)

        # Call parent constructor
        super().__init__(config)

    def _update_system_prompt(self, config: ReactAgentConfig) -> None:
        """Update the engine's system prompt if a custom one is provided.

        Args:
            config: ReactAgentConfig instance
        """
        if hasattr(config.engine, "prompt_template") and config.system_prompt:
            # Get existing messages from prompt template
            if hasattr(config.engine.prompt_template, "messages"):
                messages = list(config.engine.prompt_template.messages)

                # Replace system message or add one at the beginning
                found_system = False
                for i, message in enumerate(messages):
                    if (hasattr(message, "role") and message.role == "system") or (
                        isinstance(message, tuple) and message[0] == "system"
                    ):
                        messages[i] = ("system", config.system_prompt)
                        found_system = True
                        break

                if not found_system:
                    messages.insert(0, ("system", config.system_prompt))

                # Create new prompt template
                updated_prompt = ChatPromptTemplate.from_messages(messages)
                config.engine.prompt_template = updated_prompt

    def setup_workflow(self) -> None:
        """Set up the ReAct agent workflow."""
        logger.info(f"Setting up workflow for ReactAgent {self.config.name}")

        # Create DynamicGraph with our state schema
        graph_builder = DynamicGraph(
            name=self.config.name,
            components=[self.config.engine],
            state_schema=self.state_schema,
        )

        # 1. Add agent node (LLM reasoning)
        graph_builder.add_node(
            name=self.config.agent_node_name, config=self.config.engine
        )

        # 2. Add the tool node
        graph_builder.add_node(name=self.config.tool_node_name, config=self.tool_node)

        # 3. Create structured output node if needed
        has_structured_output = self.config.structured_output_model is not None
        if has_structured_output:
            structured_node = self._create_structured_output_node()
            graph_builder.add_node(
                name="structured_output_node", config=structured_node, command_goto=END
            )

        # 4. Define branch for conditional routing
        def should_use_tools(state):
            """Determine if we should route to tools based on the last message."""
            # Normalize state if needed
            state_dict = (
                state.model_dump() if hasattr(state, "model_dump") else dict(state)
            )

            # Check if the last message has tool calls
            return has_tool_calls(state_dict)

        # 5. Add conditional edges from agent node
        if has_structured_output:
            # With structured output: Agent → (Tools or StructuredOutput)
            graph_builder.add_conditional_edges(
                self.config.agent_node_name,
                should_use_tools,
                {True: self.config.tool_node_name, False: "structured_output_node"},
            )
        else:
            # Without structured output: Agent → (Tools or END)
            graph_builder.add_conditional_edges(
                self.config.agent_node_name,
                should_use_tools,
                {True: self.config.tool_node_name, False: END},
            )

        # 6. Always route tools back to agent for the next reasoning step
        graph_builder.add_edge(self.config.tool_node_name, self.config.agent_node_name)

        # 7. Set entry point
        graph_builder.set_entry_point(self.config.agent_node_name)

        # 8. Build the graph
        self.graph = graph_builder.build()

        logger.info(f"Workflow set up successfully for {self.config.name}")

    def _create_structured_output_node(self) -> Callable:
        """Create a node that generates structured output.

        Returns:
            Function to use as a node in the graph
        """

        def structured_output_node(state):
            """Generate structured output from conversation history."""
            try:
                # Convert state to dict if needed
                state_dict = (
                    state.model_dump() if hasattr(state, "model_dump") else dict(state)
                )

                # Get the LLM from engine
                llm = self.config.engine.llm_config.instantiate()

                # Add structured output capability
                llm_with_structured_output = llm.with_structured_output(
                    self.config.structured_output_model
                )

                # Get messages and normalize them
                messages = state_dict.get("messages", [])
                normalized_messages = normalize_messages(messages)

                # Generate structured output
                output = llm_with_structured_output.invoke(normalized_messages)

                # Update state
                return {"structured_output": output}

            except Exception as e:
                # Handle error
                error_msg = f"Failed to generate structured output: {e!s}"
                logger.exception(error_msg)

                return {"error": error_msg}

        return structured_output_node

    def _prepare_input(
        self, input_data: str | list[str] | dict[str, Any] | BaseModel
    ) -> dict[str, Any]:
        """Prepare input for the agent, ensuring proper initialization and message normalization.

        Args:
            input_data: Input in various formats

        Returns:
            Properly formatted input state for the agent
        """
        # Process input with parent's method
        state = super()._prepare_input(input_data)

        # Normalize message objects if needed
        if isinstance(state, dict) and "messages" in state:
            normalized_messages = normalize_messages(state["messages"])
            state["messages"] = normalized_messages

        # Ensure ReactAgent-specific fields are initialized
        if isinstance(state, dict):
            # Initialize step counters
            if "current_step" not in state:
                state["current_step"] = 0

            # Initialize max_iterations if not present
            if "max_iterations" not in state:
                state["max_iterations"] = self.config.max_iterations

            # Initialize remaining_steps if not present
            if "remaining_steps" not in state:
                state["remaining_steps"] = self.config.max_iterations

            # Initialize is_last_step if not present
            if "is_last_step" not in state:
                state["is_last_step"] = False

            # Initialize tool_results if not present
            if "tool_results" not in state:
                state["tool_results"] = []

            # Initialize tool_usage_stats if not present
            if "tool_usage_stats" not in state:
                state["tool_usage_stats"] = {}

        return state

    def run(
        self, input_data: str | list[str] | dict[str, Any] | BaseModel, **kwargs
    ) -> dict[str, Any]:
        """Run the agent with the given input.

        Args:
            input_data: Input data in various formats
            **kwargs: Additional runtime configuration

        Returns:
            Final state or output
        """
        # Prepare input state
        processed_input = self._prepare_input(input_data)

        # Set up config with thread ID if not provided
        if "configurable" not in kwargs:
            kwargs["configurable"] = {"thread_id": str(uuid.uuid4())}
        elif "thread_id" not in kwargs["configurable"]:
            kwargs["configurable"]["thread_id"] = str(uuid.uuid4())

        # Merge with runtime config from src.config
        config = {**self.config.runnable_config, **kwargs}

        if self.config.debug:
            logger.debug(
                f"Running agent {self.config.name} with input: {processed_input}"
            )
        else:
            logger.info(f"Running agent {self.config.name}")

        try:
            # Run the agent
            result = self.app.invoke(
                processed_input, config=config, debug=self.config.debug
            )

            # Save state history if requested
            if self.config.save_history:
                self.save_state_history()

            return result

        except Exception as e:
            logger.exception(f"Error running agent: {e!s}")

            # Add error to state
            if isinstance(processed_input, dict):
                processed_input["error"] = str(e)

                # Add error message
                if "messages" in processed_input:
                    error_msg = AIMessage(content=f"Error: {e!s}")
                    processed_input["messages"] = [
                        *list(processed_input["messages"]),
                        error_msg,
                    ]

            return processed_input

    def chat(self):
        """Start an interactive chat session with the agent."""
        # Create a thread ID for this conversation
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}

        # Chat history for this session - use proper LangChain Message objects
        history = []

        while True:
            # Get user input
            user_input = input("\nYou: ")

            # Check for exit command
            if user_input.lower() in ["exit", "quit", "bye"]:
                break

            # Always use proper LangChain message objects
            history.append(HumanMessage(content=user_input))

            # Create input state with history
            input_state = {"messages": history}

            # Run the agent
            result = self.run(input_state, **config)

            # Process the result
            if isinstance(result, dict) and "messages" in result:
                result_messages = result["messages"]
                current_history_len = len(history)

                # Process new messages after the current history length
                new_messages = []
                if len(result_messages) > current_history_len:
                    new_messages = result_messages[current_history_len:]

                # Process and display new messages
                for msg in new_messages:
                    # Normalize message to ensure it's a proper LangChain message object
                    normalized_msg = normalize_message(msg)

                    # Add normalized message to history
                    history.append(normalized_msg)

                    # Display AI messages
                    if isinstance(normalized_msg, AIMessage):
                        pass

    def stream(
        self, input_data: str | list[str] | dict[str, Any] | BaseModel, **kwargs
    ):
        """Stream the agent execution with given input.

        Args:
            input_data: Input data in various formats
            **kwargs: Additional runtime configuration

        Returns:
            Generator yielding states
        """
        # Prepare input state
        processed_input = self._prepare_input(input_data)

        # Set up config with thread ID if not provided
        if "configurable" not in kwargs:
            kwargs["configurable"] = {"thread_id": str(uuid.uuid4())}
        elif "thread_id" not in kwargs["configurable"]:
            kwargs["configurable"]["thread_id"] = str(uuid.uuid4())

        # Merge with runtime config from src.config
        config = {**self.config.runnable_config, **kwargs}

        # Stream the execution
        logger.info(f"Streaming agent {self.config.name}")

        try:
            yield from self.app.stream(
                processed_input,
                config=config,
                stream_mode="values",
                debug=self.config.debug,
            )

            # Save state history if requested
            if self.config.save_history:
                self.save_state_history()

        except Exception as e:
            logger.exception(f"Error streaming agent: {e!s}")

            # Add error to state
            if isinstance(processed_input, dict):
                processed_input["error"] = str(e)

                # Add error message
                if "messages" in processed_input:
                    error_msg = AIMessage(content=f"Error: {e!s}")
                    processed_input["messages"] = [
                        *list(processed_input["messages"]),
                        error_msg,
                    ]

                yield processed_input


# =============================================
# Helper function to create React agent
# =============================================
def create_react_agent(
    tools: list[BaseTool | StructuredTool | Tool],
    model: str = "gpt-4o",
    temperature: float = 0.7,
    system_prompt: str | None = None,
    name: str | None = None,
    max_iterations: int = 10,
    response_format: type[BaseModel] | dict[str, Any] | None = None,
    use_memory: bool = True,
    visualize: bool = True,
    debug: bool = False,
    structured_output_model: type[BaseModel] | dict[str, Any] | None = None,
    additional_input_vars: list[str] | None = None,
    **kwargs,
) -> ReactAgent:
    """Create a React agent with the specified configuration.

    Args:
        tools: List of tools for the agent
        model: Model name to use (default: "gpt-4o")
        temperature: Temperature for generation (default: 0.7)
        system_prompt: Optional system prompt
        name: Optional name for the agent
        max_iterations: Maximum number of iterations (default: 10)
        response_format: Optional schema for structured output
        use_memory: Whether to use memory (default: True)
        visualize: Whether to generate graph visualization (default: True)
        debug: Whether to enable debug mode (default: False)
        structured_output_model: Optional schema for structured output
        additional_input_vars: Additional input variables for prompt
        **kwargs: Additional configuration parameters

    Returns:
        ReactAgent instance
    """
    # Create ReactAgentConfig
    config = ReactAgentConfig.from_tools(
        tools=tools,
        model=model,
        temperature=temperature,
        system_prompt=system_prompt,
        name=name,
        max_iterations=max_iterations,
        response_format=response_format,
        use_memory=use_memory,
        visualize=visualize,
        debug=debug,
        structured_output_model=structured_output_model,
        additional_input_vars=additional_input_vars,
        **kwargs,
    )

    # Build and return agent
    return config.build_agent()
