from typing import Any

from agents.react_agent2.models import ReactState, Thought
from haive.core.engine.agent.agent import AgentConfig
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import Field


class ReactAgentConfig(AgentConfig):
    """Configuration for a React agent that follows the ReAct pattern:
    1. Think: Reason about the current state
    2. Act: Decide on an action and execute it
    3. Observe: See the result of the action
    4. Repeat until a final answer is reached.
    """

    # Schema
    state_schema: type[ReactState] = ReactState

    # System prompts
    system_prompt: str = Field(
        default="""You are an AI assistant that follows the ReAct framework:

1. Think: Reason step-by-step about the problem
2. Act: Choose an action from the available tools
3. Observe: See the result of your action
4. Repeat until you have a final answer

Remember to:
1. Break down complex problems into steps
2. Use tools when you need specific information
3. Properly interpret tool outputs
4. Provide a clear final answer when done

Available tools:
{tool_descriptions}

For each step, output your thought process and chosen action in a structured format:

Thought: <your step-by-step reasoning about what to do next>
Action: <tool_name>
Action Input: <input for the tool>

When you're ready to provide the final answer, use:

Thought: <your final reasoning>
Action: final_answer
Action Input: <your final answer>
""",
        description="System prompt for the React agent.",
    )

    # Tools configuration
    tools: dict[str, Any] | list[Any] = Field(
        default_factory=dict,
        description="Tools available to the agent, either as a dictionary or list.",
    )

    # Max iterations
    max_iterations: int = Field(
        default=10,
        description="Maximum number of iterations before forcing termination.",
    )

    # Max retries per tool
    max_retry_attempts: int = Field(
        default=3, description="Maximum number of retry attempts per tool on failure."
    )

    # Model settings
    model: str = Field(default="gpt-4o", description="Model to use for thinking.")

    temperature: float = Field(
        default=0.7, description="Temperature for the thinking LLM."
    )

    # AugLLM for thinking (will be created in from_scratch)
    think_llm: AugLLMConfig | None = None

    @classmethod
    def from_scratch(
        cls,
        tools: dict[str, Any] | list[Any],
        system_prompt: str | None = None,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        max_iterations: int = 10,
        max_retry_attempts: int = 3,
        name: str | None = None,
        **kwargs,
    ) -> "ReactAgentConfig":
        """Create a ReactAgentConfig from scratch.

        Args:
            tools: Dictionary of tool name to tool function, or list of tools
            system_prompt: Optional system prompt override
            model: Model name
            temperature: Temperature for the thinking LLM
            max_iterations: Maximum number of thinking iterations
            max_retry_attempts: Maximum retry attempts per tool
            name: Optional agent name
            **kwargs: Additional configuration

        Returns:
            ReactAgentConfig instance
        """
        # Extract tool names and descriptions
        tool_names = []
        tool_descriptions = []

        if isinstance(tools, dict):
            for name, tool in tools.items():
                tool_names.append(name)
                description = (
                    tool.__doc__
                    if hasattr(tool, "__doc__") and tool.__doc__
                    else f"Tool: {name}"
                )
                tool_descriptions.append(f"- {name}: {description}")
        elif isinstance(tools, list):
            for tool in tools:
                # Get tool name
                if hasattr(tool, "name"):
                    name = tool.name
                elif hasattr(tool, "__name__"):
                    name = tool.__name__
                else:
                    name = "unknown_tool"

                tool_names.append(name)

                # Get tool description
                if hasattr(tool, "description"):
                    description = tool.description
                elif hasattr(tool, "__doc__") and tool.__doc__:
                    description = tool.__doc__
                else:
                    description = f"Tool: {name}"

                tool_descriptions.append(f"- {name}: {description}")

        # Create config instance
        config = cls(
            name=name or "react_agent",
            tools=tools,
            tool_names=tool_names,
            max_iterations=max_iterations,
            max_retry_attempts=max_retry_attempts,
            model=model,
            temperature=temperature,
            **kwargs,
        )

        # Override system prompt if provided
        if system_prompt:
            config.system_prompt = system_prompt

        think_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    config.system_prompt.format(
                        tool_descriptions="\n".join(tool_descriptions),
                        tool_names=", ".join(tool_names),
                    ),
                ),
                ("human", "{input}"),
                ("placeholder", "{messages}"),
                (
                    "placeholder",
                    "{steps}",
                ),  # ✅ Corrected: Use "user" instead of "steps"
            ]
        )

        # Create LLM config
        llm_config = AzureLLMConfig(
            model=model, parameters={"temperature": temperature}
        )

        # Create AugLLM for thinking
        think_llm = AugLLMConfig(
            name="think_llm",
            llm_config=llm_config,
            prompt_template=think_prompt,
            output_parser=PydanticOutputParser(pydantic_object=Thought),
        )
        # Add to config
        config.think_llm = think_llm
        config.engine = think_llm  # For compatibility with AgentConfig
        return config
