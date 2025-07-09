# src/haive/agents/react/agent.py

import logging
import uuid
from collections.abc import Sequence
from datetime import datetime
from typing import Annotated, Any, Literal

from haive.core.engine.agent.agent import Agent, AgentConfig, register_agent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from haive.core.models.llm.base import AzureLLMConfig
from haive.core.utils.visualize_graph_utils import render_and_display_graph
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import BaseTool, StructuredTool, Tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import add_messages
from pydantic import BaseModel, Field, field_validator

# Set up logging
logger = logging.getLogger(__name__)

# =============================================
# React Agent State Schema
# =============================================


class ReactAgentState(BaseModel):
    """Schema for React agents with tool usage."""

    messages: Annotated[Sequence[BaseMessage], add_messages] = Field(
        default_factory=list, description="Messages in the conversation"
    )

    error: str | None = Field(default=None, description="Error message if any")

    current_step: int = Field(default=0, description="Current execution step")

    max_iterations: int = Field(default=10, description="Maximum number of iterations")

    tool_results: list[dict[str, Any]] = Field(
        default_factory=list, description="Results from tool executions"
    )

    structured_output: dict[str, Any] | None = Field(
        default=None, description="Structured output from the agent"
    )

    remaining_steps: int = Field(
        default=10, description="Number of steps remaining before forced termination"
    )

    is_last_step: bool = Field(
        default=False, description="Whether this is the last step before termination"
    )


# =============================================
# React Agent Config
# =============================================


class ReactAgentConfig(AgentConfig):
    """Configuration for a ReAct agent that can use tools.

    This is an implementation of the ReAct pattern (Reasoning and Acting)
    where the agent alternates between reasoning (using the LLM) and
    acting (using tools) to solve problems.
    """

    # Tool configuration
    tools: list[BaseTool | StructuredTool | Tool | dict[str, Any]] = Field(
        default_factory=list, description="Tools available to the agent"
    )

    # Default state schema to ReactAgentState
    state_schema: type[BaseModel] = Field(
        default=ReactAgentState, description="Schema for the agent state"
    )

    # Execution configuration
    max_iterations: int = Field(
        default=10, description="Maximum number of reasoning steps"
    )

    # Node names configuration
    agent_node_name: str = Field(
        default="agent", description="Name for the agent reasoning node"
    )

    tools_node_name: str = Field(
        default="tools", description="Name for the tools execution node"
    )

    # System prompt for the agent
    system_prompt_template: str = Field(
        default="""# Expert Problem-Solving Assistant

You are an AI assistant with expertise in solving complex problems by breaking them down methodically and using specialized tools.

## Your Capabilities

You have access to the following tools that can help you gather information and perform actions:

{tool_descriptions}

## How to Respond

When you need to use a tool, respond in this format:
```json
{{
  "thought": "Your step-by-step reasoning about what needs to be done",
  "action": "tool_name",
  "action_input": {{
    "parameter1": "value1",
    "parameter2": "value2"
  }}
}}
```

When you've solved the problem and want to provide a final answer, respond like this:
```json
{{
  "thought": "Your final reasoning process",
  "action": "final_answer",
  "action_input": "Your comprehensive answer to the user's question"
}}
```

## Your Problem-Solving Approach

1. **Understand the request** - Make sure you fully comprehend what the user is asking
2. **Plan your approach** - Consider what information you need and which tools can help
3. **Execute methodically** - Use tools strategically to gather necessary information
4. **Synthesize findings** - Bring together all relevant information
5. **Provide clear conclusions** - Deliver a comprehensive answer

## Guidelines

- Always think step-by-step
- Be thorough in your reasoning
- Use tools to verify information and avoid hallucinations
- Provide detailed, evidence-based responses
- When uncertain, gather more information rather than guessing
- Respond in a helpful, accurate, and educational manner

Remember: Your goal is to provide maximum value by giving accurate, well-reasoned, and insightful responses.
""",
        description="System prompt template for the agent with tools",
    )

    # Branch configuration for routing
    use_tool_branch: bool = Field(
        default=True, description="Whether to use Branch class for tool routing"
    )

    # Graph version (v1: synchronous tools, v2: distributed tool execution)
    version: Literal["v1", "v2"] = Field(
        default="v1",
        description="Graph version: v1=synchronous tools, v2=distributed tool execution",
    )

    # Structured output configuration
    structured_output_model: type[BaseModel] | None = Field(
        default=None, description="Model for structured output"
    )

    # Runtime configuration
    runnable_config: dict[str, Any] = Field(
        default_factory=lambda: {"configurable": {"thread_id": str(uuid.uuid4())}},
        description="Runtime configuration for the agent",
    )

    # Checkpointing and persistence
    use_memory: bool = Field(
        default=True, description="Whether to use memory for checkpointing"
    )

    # Visualization settings
    visualize: bool = Field(default=True, description="Whether to visualize the graph")

    @field_validator("tools", mode="before")
    def preprocess_tools(cls, v):
        """Preprocess tools to ensure consistency."""
        if v is None:
            return []

        # Convert dictionaries to Tool objects
        processed_tools = []
        for tool in v:
            if isinstance(tool, dict):
                # Create a Tool from dictionary
                if "func" in tool and "name" in tool:
                    processed_tools.append(
                        Tool(
                            name=tool["name"],
                            description=tool.get("description", ""),
                            func=tool["func"],
                            return_direct=tool.get("return_direct", False),
                        )
                    )
            else:
                processed_tools.append(tool)

        return processed_tools

    @classmethod
    def from_tools(
        cls,
        tools: list[BaseTool | StructuredTool | Tool | dict[str, Any]],
        name: str | None = None,
        system_prompt: str | None = None,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        max_iterations: int = 10,
        version: Literal["v1", "v2"] = "v1",
        **kwargs,
    ) -> "ReactAgentConfig":
        """Create a ReactAgentConfig from a list of tools.

        Args:
            tools: List of tools to use
            name: Optional name for the agent
            system_prompt: Optional system prompt override
            model: Model name to use
            temperature: Temperature for model generation
            max_iterations: Maximum number of reasoning steps
            version: Graph version (v1 or v2)
            **kwargs: Additional configuration parameters

        Returns:
            ReactAgentConfig instance
        """
        # Create LLM config
        llm_config = AzureLLMConfig(
            model=model, parameters={"temperature": temperature}
        )

        # Generate default name if not provided
        if not name:
            name = f"react_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Create and return the config
        return cls(
            name=name,
            tools=tools,
            llm_config=llm_config,
            system_prompt=system_prompt,
            max_iterations=max_iterations,
            version=version,
            **kwargs,
        )


# =============================================
# React Agent Implementation
# =============================================


@register_agent(ReactAgentConfig)
class ReactAgent(Agent[ReactAgentConfig]):
    """An agent that implements the ReAct pattern for reasoning and acting.

    This agent alternates between:
    1. Reasoning (using the LLM to decide what to do)
    2. Acting (executing tools based on the reasoning)
    """

    def __init__(self, config: ReactAgentConfig):
        """Initialize the ReactAgent with its configuration."""
        # Store tools list
        self.tools = config.tools
        self.checkpointer = MemorySaver() if config.use_memory else None

        # Call the parent constructor
        super().__init__(config)

    def setup_workflow(self) -> None:
        """Set up the ReAct workflow graph."""
        logger.debug(f"Setting up workflow for ReactAgent {self.config.name}")

        # Create dynamic graph builder with tools integration
        if isinstance(self.state_schema, type):
            gb = DynamicGraph(
                components=[self.config.engine] + self.config.tools,
                state_schema=self.state_schema,
                name=self.config.name,
            )
        else:
            # If state_schema is already instantiated, use it directly
            gb = DynamicGraph(
                components=[self.config.engine] + self.config.tools,
                state_schema=self.state_schema,
                name=self.config.name,
            )

        # Use the graph builder's add_react_agent_pattern method to set up the workflow
        gb.add_react_agent_pattern(
            agent_node_name=self.config.agent_node_name,
            tools_node_name=self.config.tools_node_name,
            agent_config=self._create_agent_llm(),
            tools=self.config.tools,
            version=self.config.version,
        )

        # Get the built graph
        self.graph = gb.build()

        # Compile the graph
        self.compile()

        # Generate visualization if requested
        if self.config.visualize:
            self.visualize_graph()

        logger.info(f"Set up ReAct workflow for {self.config.name}")

    def _create_agent_llm(self) -> AugLLMConfig:
        """Create the agent LLM configuration with tool descriptions."""
        # Get tool descriptions
        tool_descriptions = self._get_tool_descriptions()

        # Create the system prompt
        system_prompt = self.config.system_prompt_template.format(
            tool_descriptions=tool_descriptions
        )

        # Create the prompt template
        prompt_template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=system_prompt),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        # Create the LLM config that will be used by the agent
        agent_llm = AugLLMConfig(
            name=f"{self.config.name}_agent_llm",
            llm_config=self.config.llm_config,
            prompt_template=prompt_template,
            tools=self.config.tools,
        )

        return agent_llm

    def _get_tool_descriptions(self) -> str:
        """Format tool descriptions for the system prompt."""
        descriptions = []

        for i, tool in enumerate(self.config.tools):
            # Get tool name
            name = getattr(tool, "name", f"tool_{i}")

            # Get tool description
            description = getattr(tool, "description", "No description provided")

            # Get function signature if available
            signature = ""
            if hasattr(tool, "args_schema"):
                # If tool has an args_schema, extract parameter info
                schema = tool.args_schema
                parameters = []
                for field_name, field in schema.__annotations__.items():
                    # Get field type and whether it's required
                    field_type = (
                        field.__name__ if hasattr(field, "__name__") else str(field)
                    )
                    field_type = field_type.replace("typing.", "")

                    # Check if field is required
                    field_required = "Optional" not in field_type

                    parameters.append(
                        f"  - {field_name} ({field_type}){' (required)' if field_required else ''}"
                    )

                if parameters:
                    signature = "\nParameters:\n" + "\n".join(parameters)

            descriptions.append(f"### {name}\n{description}{signature}")

        return "\n\n".join(descriptions)

    def compile(self) -> None:
        """Compile the workflow graph."""
        if not self.graph:
            raise RuntimeError("Workflow graph is not set up.")

        if self.app is None:
            self.app = self.graph.compile(checkpointer=self.checkpointer)
        else:
            logger.info(f"Workflow already compiled for {self.config.name}")

        logger.info(f"Workflow compiled for {self.config.name}")

    def run(
        self, input_data: str | list[str] | dict[str, Any] | BaseModel, **kwargs
    ) -> dict[str, Any]:
        """Run the agent with the given input.

        Args:
            input_data: Input data for the agent (string, messages, or state dict)
            **kwargs: Additional runtime configuration

        Returns:
            Final state with agent's response
        """
        # Prepare runtime config
        runtime_config = {**self.config.runnable_config, **kwargs}

        # Run the agent
        return super().run(input_data, **runtime_config)

    def stream(
        self, input_data: str | list[str] | dict[str, Any] | BaseModel, **kwargs
    ):
        """Stream the agent execution with the given input.

        Args:
            input_data: Input data for the agent (string, messages, or state dict)
            **kwargs: Additional runtime configuration

        Returns:
            Generator yielding states
        """
        # Prepare runtime config
        runtime_config = {**self.config.runnable_config, **kwargs}

        # Stream the execution
        return super().stream(input_data, **runtime_config)

    def visualize_graph(self) -> None:
        """Generate and save visualization of the agent's graph."""
        if self.app:
            try:
                render_and_display_graph(
                    self.app, output_name=f"{self.config.name}_graph.png"
                )
                logger.info(f"Graph visualization saved for {self.config.name}")
            except Exception as e:
                logger.error(f"Failed to visualize graph: {e!s}")

    def chat(self, interactive=True):
        """Start an interactive chat session with the agent.

        Args:
            interactive: Whether to run in interactive mode (default: True)
        """
        if interactive:
            print(f"\n===== Starting chat with {self.config.name} =====")
            print("Type 'exit', 'quit', or 'q' to end the conversation.\n")

            # Create a thread ID for this conversation
            thread_id = str(uuid.uuid4())
            runtime_config = {"configurable": {"thread_id": thread_id}}

            while True:
                # Get user input
                user_input = input("You: ")

                # Check for exit command
                if user_input.lower() in ["exit", "quit", "q"]:
                    print("\n===== Ending chat =====")
                    break

                # Create input message
                user_message = HumanMessage(content=user_input)

                # Run agent with input
                try:
                    # Prepare input state
                    if not self.app.get_state(runtime_config):
                        # First message in conversation
                        input_data = {"messages": [user_message]}
                    else:
                        # Continue existing conversation
                        input_data = {"messages": [user_message]}

                    # Stream the agent's response
                    print("\nAgent: ", end="", flush=True)

                    last_message = None
                    tool_calls_seen = set()

                    for state in self.app.stream(
                        input_data, config=runtime_config, stream_mode="values"
                    ):
                        if "messages" in state:
                            messages = state["messages"]
                            if messages and len(messages) > 0:
                                # Find the latest message that should be displayed
                                for msg in reversed(messages):
                                    # Skip tool messages - we'll display them differently
                                    if isinstance(msg, ToolMessage):
                                        continue

                                    # Skip AIMessages with tool calls - they're intermediates
                                    if (
                                        isinstance(msg, AIMessage)
                                        and hasattr(msg, "tool_calls")
                                        and msg.tool_calls
                                    ):
                                        # Check if we've already seen these tool calls
                                        current_calls = {
                                            call["id"] for call in msg.tool_calls
                                        }
                                        if not current_calls.issubset(tool_calls_seen):
                                            # New tool calls, print them differently
                                            for call in msg.tool_calls:
                                                if call["id"] not in tool_calls_seen:
                                                    tool_calls_seen.add(call["id"])
                                                    print(
                                                        f"\n[Using {call['name']}...]",
                                                        end="",
                                                        flush=True,
                                                    )
                                        continue

                                    # Found a message to display
                                    if msg != last_message and isinstance(
                                        msg, AIMessage
                                    ):
                                        # New AI message to display
                                        if last_message is None:
                                            # First message
                                            print(f"{msg.content}", end="", flush=True)
                                        else:
                                            # Updated content
                                            print(
                                                f"\n{msg.content}", end="", flush=True
                                            )
                                        last_message = msg
                                        break

                    print("\n")
                except Exception as e:
                    print(f"\nError: {e!s}")
        else:
            # Non-interactive mode for testing or scripting
            pass


# =============================================
# Helper Functions
# =============================================


def create_react_agent(
    tools: list[BaseTool | StructuredTool | Tool | dict[str, Any]],
    system_prompt: str | None = None,
    model: str = "gpt-4o",
    temperature: float = 0.7,
    name: str | None = None,
    max_iterations: int = 10,
    version: Literal["v1", "v2"] = "v1",
    structured_output_model: type[BaseModel] | None = None,
    visualize: bool = True,
    use_memory: bool = True,
    **kwargs,
) -> ReactAgent:
    """Create a React agent that can use tools to solve problems.

    Args:
        tools: List of tools for the agent to use
        system_prompt: Optional system prompt override
        model: Model name to use
        temperature: Temperature for generation
        name: Optional name for the agent
        max_iterations: Maximum number of reasoning steps
        version: Graph version (v1: synchronous tools, v2: distributed tool execution)
        structured_output_model: Optional model for structured output
        visualize: Whether to generate graph visualization
        use_memory: Whether to use memory for checkpointing
        **kwargs: Additional configuration parameters

    Returns:
        ReactAgent instance
    """
    # Create config
    config = ReactAgentConfig.from_tools(
        tools=tools,
        name=name,
        system_prompt=system_prompt,
        model=model,
        temperature=temperature,
        max_iterations=max_iterations,
        version=version,
        structured_output_model=structured_output_model,
        visualize=visualize,
        use_memory=use_memory,
        **kwargs,
    )

    # Build and return the agent
    return config.build_agent()


# Example usage
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Define a simple tool
    from langchain_core.tools import tool

    @tool
    def search(query: str) -> str:
        """Search for information on the given query."""
        return f"Search results for '{query}': This is a simulation of search results."

    @tool
    def calculator(expression: str) -> str:
        """Evaluate a mathematical expression."""
        try:
            # Warning: In production, use safer evaluation methods
            return f"Result of '{expression}' = {eval(expression)}"
        except Exception as e:
            return f"Error evaluating expression: {e!s}"

    # Import Tavily search tool (if available)
    try:
        from haive.tools.tools.search_tools import tavily_search_tool

        tools = [tavily_search_tool, calculator]
    except ImportError:
        tools = [search, calculator]

    # Create the agent
    agent = create_react_agent(
        tools=tools, name="react_agent_example", version="v1", use_memory=True
    )

    # Start interactive chat
    agent.chat()
