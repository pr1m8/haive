import logging
import uuid
from collections.abc import Sequence
from typing import Annotated, Literal

from haive.core.config.runnable import RunnableConfigManager
from haive.core.engine.agent.agent import Agent, AgentConfig, register_agent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.branches import Branch
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from haive.core.graph.node.config import NodeConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import BaseTool
from langgraph.graph import END, add_messages
from langgraph.prebuilt import ToolNode
from langgraph.types import Send
from pydantic import BaseModel, Field

from haive.agents.react_class.react_agent2.state2 import ReactAgentState

# Set up logging
logger = logging.getLogger(__name__)


# Define our state schema with messages and step tracking
class ReactAgentState(BaseModel):
    """State schema for ReAct agent."""

    messages: Annotated[Sequence[BaseMessage], add_messages] = Field(
        default_factory=list, description="Messages in the conversation"
    )
    remaining_iterations: int = Field(
        default=5, description="Number of remaining iterations"
    )
    iteration_count: int = Field(default=0, description="Current iteration count")
    tools_used: list[str] = Field(
        default_factory=list, description="List of tools used in this session"
    )
    status: str = Field(default="initialized", description="Current agent status")


# Define our agent configuration
class ReactAgentConfig(AgentConfig):
    """Configuration for the ReAct agent."""

    system_prompt: str = Field(
        default="You are a helpful assistant that can use tools to answer user questions.",
        description="System prompt for the agent",
    )
    max_iterations: int = Field(
        default=5, description="Maximum number of interaction iterations"
    )
    tool_names: list[str] = Field(
        default_factory=list, description="Names of available tools"
    )
    temperature: float = Field(
        default=0.7, description="Temperature for LLM generation"
    )
    model: str = Field(default="gpt-4o", description="LLM model to use")
    parallel_tool_execution: bool = Field(
        default=True, description="Whether to execute tools in parallel (v2 style)"
    )
    tool_routing: dict[str, str] = Field(
        default_factory=dict, description="Mapping of tool names to specific nodes"
    )
    structured_output_model: type[BaseModel] | None = Field(
        default=None, description="Optional structured output model for final response"
    )

    @classmethod
    def from_tools(
        cls,
        tools: list[BaseTool],
        system_prompt: str = "You are a helpful assistant with access to tools.",
        max_iterations: int = 5,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        parallel_tool_execution: bool = True,
        tool_routing: dict[str, str] | None = None,
        structured_output_model: type[BaseModel] | None = None,
        **kwargs,
    ) -> "ReactAgentConfig":
        """Create a ReactAgentConfig from a list of tools."""
        tool_names = [tool.name for tool in tools]

        llm_config = AugLLMConfig(
            name="react_agent_llm",
            llm_config=AzureLLMConfig(
                model=model, parameters={"temperature": temperature}
            ),
            prompt_template=ChatPromptTemplate.from_messages(
                [
                    ("system", system_prompt),
                    MessagesPlaceholder(variable_name="messages"),
                ]
            ),
            tools=tools,
        )

        # Set structured output if provided
        if structured_output_model is not None:
            llm_config.structured_output_model = structured_output_model

        return cls(
            engine=llm_config,
            system_prompt=system_prompt,
            max_iterations=max_iterations,
            tool_names=tool_names,
            model=model,
            temperature=temperature,
            parallel_tool_execution=parallel_tool_execution,
            tool_routing=tool_routing or {},
            structured_output_model=structured_output_model,
            state_schema=ReactAgentState,
            **kwargs,
        )


# Implement our ReAct agent
@register_agent(ReactAgentConfig)
class ReactAgent(Agent[ReactAgentConfig]):
    """ReAct agent implementation with tool usage and routing capabilities."""

    def setup_workflow(self) -> None:
        """Set up the agent workflow with nodes and edges."""
        logger.debug(f"Setting up workflow for ReactAgent {self.config.name}")

        # Get tools from config
        tools = self.config.engine.tools or []
        if not tools:
            logger.warning(f"No tools provided for ReactAgent {self.config.name}")

        # Create DynamicGraph with proper component registration
        gb = DynamicGraph(
            name=f"{self.config.name}_graph",
            components=[self.config.engine],
            state_schema=self.config.state_schema,
        )

        # Track tool groupings if using custom routing
        tool_groups = {}

        # Create the agent node configuration
        agent_node_config = NodeConfig(
            name="agent",
            engine=self.config.engine,
            config_overrides={"temperature": self.config.temperature},
        )

        # Add the agent node
        gb.add_node(
            name="agent",
            config=agent_node_config,
            input_mapping={"messages": "messages"},
        )

        # Set up tools based on configuration
        if self.config.tool_routing:
            # Group tools by their routing nodes
            for tool in tools:
                # Determine which node should handle this tool
                tool_route = self.config.tool_routing.get(tool.name)
                if tool_route:
                    # Add to existing group or create new one
                    if tool_route not in tool_groups:
                        tool_groups[tool_route] = []
                    tool_groups[tool_route].append(tool)
                else:
                    # Default to general tools node
                    if "tools" not in tool_groups:
                        tool_groups["tools"] = []
                    tool_groups["tools"].append(tool)

            # Create a node for each tool group
            for node_name, group_tools in tool_groups.items():
                gb.add_node(node_name, ToolNode(group_tools))
                # Add edge from each tool node back to agent
                gb.add_edge(node_name, "agent")
        else:
            # Use a single tools node for all tools
            gb.add_node("tools", ToolNode(tools))
            # Add edge from tools back to agent
            gb.add_edge("tools", "agent")

        # Add structured output node if configured
        if self.config.structured_output_model is not None:
            structured_output_node = self._create_structured_output_node_config()
            gb.add_node(
                name="generate_structured_output",
                config=structured_output_node,
                command_goto=END,
            )

        # Set entry point
        gb.set_entry_point("agent")

        # Create the router function based on our configuration
        if self.config.tool_routing:
            # Use a router that can route to specific tool nodes
            router_destinations = {node_name: node_name for node_name in tool_groups}

            # Add structured output or END as destinations
            if self.config.structured_output_model is not None:
                router_destinations[END] = "generate_structured_output"
            else:
                router_destinations[END] = END

            router_branch = Branch.from_function(
                self._route_to_specific_tools, destinations=router_destinations
            )

            gb.add_conditional_edges("agent", router_branch.evaluator)
        else:
            # Use the standard router
            destinations = {"tools": "tools"}

            # Add structured output or END as destination
            if self.config.structured_output_model is not None:
                destinations[END] = "generate_structured_output"
            else:
                destinations[END] = END

            router_branch = Branch.from_function(
                self._should_continue, destinations=destinations
            )

            gb.add_conditional_edges("agent", router_branch.evaluator)

        # Set default runnable config
        default_config = RunnableConfigManager.create(
            temperature=self.config.temperature, model=self.config.model
        )
        gb.set_default_runnable_config(default_config)

        # Build the graph
        self.graph = gb.build()

        logger.info(f"Workflow setup complete for ReactAgent {self.config.name}")

    def _create_structured_output_node_config(self) -> NodeConfig:
        """Create the configuration for the structured output node."""

        def structured_output_node(state: ReactAgentState):
            """Generate structured output from the conversation."""
            # Get the model for structured output
            model_class = self.config.structured_output_model

            # Get the base LLM config
            llm_config = self.config.engine.llm_config

            # Create a model with structured output

            # Convert to a chat model if needed
            llm = llm_config.instantiate()

            # Create structured output version
            llm_with_structured_output = llm.with_structured_output(model_class)

            # Process the messages (excluding the last message which may have tool calls)
            messages = list(state.messages)

            # Add a final instruction to format the response
            model_name = model_class.__name__
            messages.append(
                HumanMessage(
                    content=f"Based on our conversation, please provide a final response in the required {model_name} format."
                )
            )

            # Generate structured output
            structured_response = llm_with_structured_output.invoke(messages)

            # Return the structured output
            return {"structured_response": structured_response, "status": "completed"}

        # Create a NodeConfig for the structured output node
        return NodeConfig(
            name="generate_structured_output",
            engine=structured_output_node,
            command_goto=END,
        )

    def _should_continue(
        self, state: ReactAgentState
    ) -> str | list[Send] | Literal["END"]:
        """Determine if we should continue to tools or end."""
        # Check if we're out of iterations
        if state.remaining_iterations <= 0:
            return END

        # Get last message
        if not state.messages:
            return END

        last_message = state.messages[-1]

        # Check for tool calls
        if (
            isinstance(last_message, AIMessage)
            and hasattr(last_message, "tool_calls")
            and last_message.tool_calls
        ):
            # Track tools used
            tool_names = [call.get("name") for call in last_message.tool_calls]
            for tool in tool_names:
                if tool not in state.tools_used:
                    state.tools_used.append(tool)

            # For parallel tool execution (v2 style)
            if self.config.parallel_tool_execution:
                # Get the tool calls from the message
                tool_calls = last_message.tool_calls

                # Create a Send object for each tool call
                # This allows parallel processing of multiple tools
                return [Send("tools", [tool_call]) for tool_call in tool_calls]

            # Standard routing to tools node
            return "tools"

        # No tool calls, so we're done
        return END

    def _route_to_specific_tools(
        self, state: ReactAgentState
    ) -> str | list[Send] | Literal["END"]:
        """Route to specific tool nodes based on tool calls."""
        # Check if we're out of iterations
        if state.remaining_iterations <= 0:
            return END

        # Get last message
        if not state.messages:
            return END

        last_message = state.messages[-1]

        # Check for tool calls
        if (
            isinstance(last_message, AIMessage)
            and hasattr(last_message, "tool_calls")
            and last_message.tool_calls
        ):
            # Track tools used
            tool_names = [call.get("name") for call in last_message.tool_calls]
            for tool in tool_names:
                if tool not in state.tools_used:
                    state.tools_used.append(tool)

            # Group tools by their destination nodes
            sends_by_node = {}

            for tool_call in last_message.tool_calls:
                tool_name = tool_call.get("name", "")
                # Determine which node should handle this tool
                node_name = self.config.tool_routing.get(tool_name)

                if not node_name:
                    # Fall back to default tools node
                    node_name = "tools"

                # Add to the sends for this node
                if node_name not in sends_by_node:
                    sends_by_node[node_name] = []
                sends_by_node[node_name].append(tool_call)

            # Create Send objects for each node
            if self.config.parallel_tool_execution:
                sends = []
                for node_name, tool_calls in sends_by_node.items():
                    for tool_call in tool_calls:
                        sends.append(Send(node_name, [tool_call]))
                return sends
            # Find the first node with tools and route all its tools
            for node_name, tool_calls in sends_by_node.items():
                return node_name

        # No tool calls, so we're done
        return END

    def run(self, input_text: str | dict | ReactAgentState):
        """Run the agent with the given input."""
        logger.debug(f"Running ReactAgent with input: {input_text}")

        # Process the input
        if isinstance(input_text, str):
            # Create a state from a simple text input
            initial_state = ReactAgentState(
                messages=[HumanMessage(content=input_text)],
                remaining_iterations=self.config.max_iterations,
                iteration_count=0,
                tools_used=[],
                status="initialized",
            )
        elif isinstance(input_text, dict):
            # Convert dict to state
            if "messages" in input_text and isinstance(input_text["messages"], list):
                # If messages are provided as tuples, convert them
                if all(isinstance(m, tuple) for m in input_text["messages"]):
                    messages = [
                        (
                            HumanMessage(content=content)
                            if role in ("human", "user")
                            else AIMessage(content=content)
                        )
                        for role, content in input_text["messages"]
                    ]
                    input_text["messages"] = messages

            # Create state from dict with defaults for missing fields
            state_data = {
                "messages": input_text.get("messages", []),
                "remaining_iterations": input_text.get(
                    "remaining_iterations", self.config.max_iterations
                ),
                "iteration_count": input_text.get("iteration_count", 0),
                "tools_used": input_text.get("tools_used", []),
                "status": input_text.get("status", "initialized"),
            }
            initial_state = ReactAgentState(**state_data)
        else:
            # Use provided state
            initial_state = input_text

        # Set default values if needed
        if initial_state.remaining_iterations == 0:
            initial_state.remaining_iterations = self.config.max_iterations

        # Create a unique thread ID for this run
        thread_id = str(uuid.uuid4())
        config = RunnableConfigManager.create(thread_id=thread_id)

        # Run the agent
        result = self.app.invoke(initial_state, config)

        # Log results
        logger.debug(f"Agent completed with status: {result.get('status')}")
        logger.debug(
            f"Iterations used: {result.get('iteration_count')}/{self.config.max_iterations}"
        )

        return result


# Convenience function to create a ReAct agent
def create_react_agent(
    tools: list[BaseTool],
    system_prompt: str = "You are a helpful assistant with access to tools.",
    max_iterations: int = 5,
    model: str = "gpt-4o",
    temperature: float = 0.7,
    parallel_tool_execution: bool = True,
    tool_routing: dict[str, str] | None = None,
    structured_output_model: type[BaseModel] | None = None,
    name: str | None = None,
) -> ReactAgent:
    """Create a ReAct agent with the specified configuration."""
    config = ReactAgentConfig.from_tools(
        tools=tools,
        system_prompt=system_prompt,
        max_iterations=max_iterations,
        model=model,
        temperature=temperature,
        parallel_tool_execution=parallel_tool_execution,
        tool_routing=tool_routing,
        structured_output_model=structured_output_model,
        name=name or f"react_agent_{uuid.uuid4().hex[:8]}",
    )

    return config.build_agent()


# Example usage
if __name__ == "__main__":
    # Create a simple test tool
    from langchain_core.tools import tool

    @tool
    def search(query: str) -> str:
        """Search for information about a topic."""
        # This is a mock implementation
        if "france" in query.lower() or "paris" in query.lower():
            return "Paris is the capital of France."
        return "No information found."

    # Create a React agent with the tool
    agent = create_react_agent(
        tools=[search],
        system_prompt="You are a helpful assistant that can search for information.",
        max_iterations=3,
    )

    # Run the agent
    result = agent.run("What is the capital of France?")
    print(result)
