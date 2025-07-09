import uuid
from collections.abc import Callable
from datetime import datetime
from typing import Any

from haive.core.engine.agent.agent import AgentConfig
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool, StructuredTool, Tool
from pydantic import BaseModel, Field, field_validator

from haive.agents.react_class.react_agent2.state2 import ReactAgentState

# =============================================
# React Agent Config
# =============================================

# Default system prompt for React agent
DEFAULT_REACT_SYSTEM_PROMPT = """You are an intelligent assistant with access to tools.
You solve problems step-by-step by thinking carefully and using tools when needed.

When you need information, use the appropriate tool to gather it.
After seeing a tool's results, reflect on what you've learned and decide if you
need more information or can now answer the question.

FORMAT:
1. If you need to use a tool, format your response like this:
  Thought: I need to find out X, so I should use the Y tool.
  Action: Use the correct tool name and provide the required parameters.

2. If you have enough information to provide a final answer, respond
   conversationally to the user.

Remember to be helpful, accurate, and respond directly to what the user is asking.
"""


class ReactAgentConfig(AgentConfig):
    """Configuration for a React agent that can use tools.

    Enables step-by-step reasoning with tool usage for information gathering.
    """

    # Allow arbitrary types for tools and other objects
    model_config = {"arbitrary_types_allowed": True}

    # Core components
    engine: AugLLMConfig = Field(
        default_factory=lambda: AugLLMConfig(
            llm_config=AzureLLMConfig(model="gpt-4o"),
            prompt_template=ChatPromptTemplate.from_messages(
                [
                    ("system", DEFAULT_REACT_SYSTEM_PROMPT),
                    MessagesPlaceholder(variable_name="messages"),
                ]
            ),
        ),
        description="LLM configuration for the ReactAgent.",
    )

    # Tools configuration
    tools: list[BaseTool | StructuredTool | Tool] = Field(
        default_factory=list, description="Tools available to the agent."
    )

    # Graph configuration
    agent_node_name: str = Field(
        default="agent_node", description="Name for the agent node in the graph."
    )

    tool_node_name: str = Field(
        default="tool_node", description="Name for the tool node in the graph."
    )

    # Execution configuration
    max_iterations: int = Field(
        default=10,
        description="Maximum number of iterations before forced termination.",
    )

    # Runtime configuration
    runnable_config: RunnableConfig = Field(
        default_factory=lambda: {"configurable": {"thread_id": str(uuid.uuid4())}},
        description="Configuration for the agent's runnable execution.",
    )

    # Input/output mapping
    input_mapping: dict[str, str] | None = Field(
        default=None, description="Maps state fields to engine input fields."
    )

    output_mapping: dict[str, str] | None = Field(
        default=None, description="Maps engine output fields to state fields."
    )

    # Optional structured output
    structured_output_model: type[BaseModel] | None = Field(
        default=None, description="Schema for structured output."
    )

    response_format: type[BaseModel] | dict[str, Any] | None = Field(
        default=None,
        description="Format for structured responses (alias for structured_output_model)",
    )

    # Optional routing function
    routing_function: Callable | None = Field(
        default=None, description="Custom function to determine routing between nodes."
    )

    # State schema
    state_schema: type[BaseModel] = Field(
        default=ReactAgentState, description="Schema for the agent state."
    )

    # Debug configuration
    debug: bool = Field(default=False, description="Enable debug logging.")

    # Memory options
    use_memory: bool = Field(
        default=True, description="Whether to use memory for state persistence."
    )

    # Visualization
    visualize: bool = Field(default=True, description="Whether to visualize the graph.")

    # System prompt customization
    system_prompt: str | None = Field(
        default=None, description="Custom system prompt to override the default."
    )

    # Validators for tools list
    @field_validator("tools", mode="before")
    @classmethod
    def ensure_tools_list(cls, v):
        """Ensure tools are always a list."""
        if v is None:
            return []
        return v

    # Validator to align output formats
    @field_validator("structured_output_model", "response_format", mode="before")
    @classmethod
    def align_output_format(cls, v, info):
        """Align the structured output model and response format."""
        # If response_format is set but structured_output_model is not
        if info.field_name == "structured_output_model" and v is None:
            return info.data.get("response_format")
        # If structured_output_model is set but response_format is not
        if info.field_name == "response_format" and v is None:
            return info.data.get("structured_output_model")
        return v

    # Validator for system prompt
    @field_validator("system_prompt", mode="before")
    @classmethod
    def update_system_prompt(cls, v):
        """Update the system prompt in the engine if provided."""
        return v or DEFAULT_REACT_SYSTEM_PROMPT

    # Factory methods
    @classmethod
    def from_scratch(
        cls,
        system_prompt: str | None = None,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        tools: list[BaseTool] | None = None,
        name: str | None = None,
        max_iterations: int = 10,
        **kwargs,
    ) -> "ReactAgentConfig":
        """Create a ReactAgentConfig from scratch.

        Args:
            system_prompt: Optional system prompt
            model: Model name to use
            temperature: Temperature for generation
            tools: Optional list of tools
            name: Optional agent name
            max_iterations: Maximum number of iterations
            **kwargs: Additional kwargs for the config

        Returns:
            ReactAgentConfig instance
        """
        # Import required classes
        from haive.core.models.llm.base import AzureLLMConfig
        from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

        # Create LLM config
        llm_config = AzureLLMConfig(
            model=model, parameters={"temperature": temperature}
        )

        # Create prompt template with system prompt
        system_prompt = system_prompt or DEFAULT_REACT_SYSTEM_PROMPT
        messages = [
            SystemMessage(content=system_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ]
        prompt_template = ChatPromptTemplate.from_messages(messages)

        # Create AugLLM config with prompt template
        aug_llm = AugLLMConfig(
            name=f"{name or 'react'}_llm",
            llm_config=llm_config,
            prompt_template=prompt_template,
        )

        # Create and return the config
        return cls(
            name=name or f"react_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            engine=aug_llm,
            tools=tools or [],
            max_iterations=max_iterations,
            system_prompt=system_prompt,
            **kwargs,
        )

    @classmethod
    def from_aug_llm(
        cls,
        aug_llm: AugLLMConfig,
        tools: list[BaseTool] | None = None,
        name: str | None = None,
        max_iterations: int = 10,
        **kwargs,
    ) -> "ReactAgentConfig":
        """Create a ReactAgentConfig from an existing AugLLMConfig.

        Args:
            aug_llm: Existing AugLLMConfig to use
            tools: Optional list of tools
            name: Optional agent name
            max_iterations: Maximum number of iterations
            **kwargs: Additional kwargs for the config

        Returns:
            ReactAgentConfig instance
        """
        from datetime import datetime

        return cls(
            name=name or f"react_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            engine=aug_llm,
            tools=tools or [],
            max_iterations=max_iterations,
            **kwargs,
        )

    @classmethod
    def create_prompt_template(
        cls,
        system_prompt: str | None = None,
        additional_input_vars: list[str] | None = None,
    ) -> ChatPromptTemplate:
        """Create a flexible prompt template that supports system prompt
        and additional input variables.

        Args:
            system_prompt: Custom system prompt
            additional_input_vars: List of additional input variables to include

        Returns:
            ChatPromptTemplate with flexible input handling
        """
        # Prepare messages list
        messages = []

        # Add system message if provided
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))

        # Add additional variables as placeholders
        if additional_input_vars:
            for var in additional_input_vars:
                messages.append(f"{{{{ {var} }}}}")

        # Always add messages placeholder
        messages.append(MessagesPlaceholder(variable_name="messages"))

        # Create prompt template
        return ChatPromptTemplate.from_messages(messages)

    @classmethod
    def from_tools(
        cls,
        tools: list[BaseTool | StructuredTool | Tool],
        system_prompt: str | None = None,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        name: str | None = None,
        max_iterations: int = 10,
        **kwargs,
    ) -> "ReactAgentConfig":
        """Create a ReactAgentConfig from a list of tools.

        Args:
            tools: List of tools
            system_prompt: Optional system prompt
            model: Model name to use
            temperature: Temperature for generation
            name: Optional agent name
            max_iterations: Maximum number of iterations
            **kwargs: Additional kwargs for the config

        Returns:
            ReactAgentConfig instance
        """
        return cls.from_scratch(
            system_prompt=system_prompt,
            model=model,
            temperature=temperature,
            tools=tools,
            name=name,
            max_iterations=max_iterations,
            **kwargs,
        )
