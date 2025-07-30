"""Generic Sequential Agent Pattern with Structured Output Hooks.

This module provides a flexible pattern for creating sequential agent flows
where the first agent performs some task and the second agent structures
the output into a specific format.

Examples:
    ReactAgent → StructuredOutputAgent
    ResearchAgent → SummaryAgent
    AnalysisAgent → ReportAgent
"""

from collections.abc import Callable
from typing import Any, Generic, TypeVar

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from haive.agents.base.agent import Agent
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent

# Type variable for structured output models
OutputT = TypeVar("OutputT", bound=BaseModel)


class SequentialHooks(BaseModel):
    """Hooks for customizing sequential agent behavior."""

    pre_process: Callable[[dict[str, Any]], dict[str, Any]] | None = Field(
        default=None, description="Function to preprocess input before first agent"
    )

    intermediate_transform: Callable[[Any], dict[str, Any]] | None = Field(
        default=None,
        description="Function to transform output from first agent for second agent",
    )

    post_process: Callable[[Any], Any] | None = Field(
        default=None, description="Function to post-process final output"
    )

    error_handler: Callable[[Exception], Any] | None = Field(
        default=None, description="Function to handle errors in the pipeline"
    )

    class Config:
        arbitrary_types_allowed = True


class SequentialAgentWithStructuredOutput(Generic[OutputT]):
    """Generic sequential agent pattern with structured output.

    This class orchestrates two agents in sequence:
    1. First agent performs the main task (e.g., reasoning, research)
    2. Second agent structures the output into a specific format

    The pattern is flexible and works with any agent types.
    """

    def __init__(
        self,
        first_agent: Agent,
        structured_output_model: type[OutputT],
        structured_output_prompt: ChatPromptTemplate | None = None,
        second_agent: Agent | None = None,
        hooks: SequentialHooks | None = None,
        name: str = "sequential_structured",
        debug: bool = False,
    ):
        """Initialize sequential agent with structured output.

        Args:
            first_agent: The agent that performs the main task
            structured_output_model: Pydantic model for structured output
            structured_output_prompt: Optional custom prompt for structuring
            second_agent: Optional custom second agent (otherwise creates SimpleAgent)
            hooks: Optional hooks for customizing behavior
            name: Name for this sequential pattern
            debug: Enable debug mode
        """
        self.first_agent = first_agent
        self.structured_output_model = structured_output_model
        self.name = name
        self.debug = debug
        self.hooks = hooks or SequentialHooks()

        # Create or use provided second agent
        if second_agent:
            self.second_agent = second_agent
        else:
            # Create default structured output agent
            self.second_agent = self._create_structured_output_agent(
                structured_output_prompt
            )

    def _create_structured_output_agent(
        self, custom_prompt: ChatPromptTemplate | None = None
    ) -> SimpleAgent:
        """Create default agent for structured output."""
        # Default structured output prompt if none provided
        if custom_prompt is None:
            custom_prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """You are a structured output specialist. Your role is to take the provided
information and organize it into the requested structured format.

Ensure all required fields are populated accurately based on the input data.
If certain information is not available, use reasonable defaults or indicate
that the information is missing.""",
                    ),
                    (
                        "human",
                        """Please structure the following information into the required format.

Input Information:
{input_data}

Additional Context:
{context}

Requirements:
- Extract all relevant information from the input
- Organize it according to the output schema
- Ensure accuracy and completeness
- Flag any missing or uncertain information

Provide the structured output now:""",
                    ),
                ]
            ).partial(context="")

        return SimpleAgent(
            name=f"{self.name}_structurer",
            engine=AugLLMConfig(
                prompt_template=custom_prompt,
                structured_output_model=self.structured_output_model,
                structured_output_version="v2",
                temperature=0.3,  # Lower temperature for consistent structuring
            ),
        )

    async def arun(
        self, input_data: Any, context: dict[str, Any] | None = None, **kwargs
    ) -> OutputT:
        """Run the sequential agent pipeline asynchronously.

        Args:
            input_data: Input for the first agent
            context: Optional context to pass through pipeline
            **kwargs: Additional arguments for agents

        Returns:
            Structured output according to the model
        """
        try:
            # Pre-process input if hook provided
            if self.hooks.pre_process:
                input_data = self.hooks.pre_process(input_data)

            if self.debug:
                print(f"\n🔄 Sequential Pattern: {self.name}")
                print(f"   First Agent: {self.first_agent.name}")
                print(f"   Second Agent: {self.second_agent.name}")

            # Step 1: Run first agent
            if self.debug:
                print(f"\n📍 Step 1: Running {self.first_agent.name}...")

            first_result = await self.first_agent.arun(input_data, **kwargs)

            if self.debug:
                print("   ✅ First agent completed")
                print(f"   Result type: {type(first_result)}")

            # Transform intermediate result if hook provided
            if self.hooks.intermediate_transform:
                structured_input = self.hooks.intermediate_transform(first_result)
            else:
                # Default transformation
                structured_input = self._default_transform(
                    first_result, input_data, context
                )

            # Step 2: Run structured output agent
            if self.debug:
                print(
                    f"\n📍 Step 2: Structuring output with {self.second_agent.name}..."
                )

            structured_result = await self.second_agent.arun(structured_input, **kwargs)

            if self.debug:
                print("   ✅ Structured output completed")
                print(f"   Output type: {type(structured_result)}")

            # Extract the actual structured output from the result
            if hasattr(structured_result, "messages") and structured_result.messages:
                # Get the last message
                last_message = structured_result.messages[-1]

                # Check if it has tool calls (structured output)
                if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                    for tool_call in last_message.tool_calls:
                        if (
                            "name" in tool_call
                            and tool_call["name"]
                            == self.structured_output_model.__name__
                        ):
                            # Parse the structured output
                            import json

                            args = tool_call.get("args", {})
                            if isinstance(args, str):
                                args = json.loads(args)
                            structured_result = self.structured_output_model(**args)
                            break
                        if "function" in tool_call:
                            # Handle OpenAI format
                            func = tool_call["function"]
                            if (
                                func.get("name")
                                == self.structured_output_model.__name__
                            ):
                                args = func.get("arguments", {})
                                if isinstance(args, str):
                                    args = json.loads(args)
                                structured_result = self.structured_output_model(**args)
                                break
            elif isinstance(structured_result, dict):
                # Try to extract from dict format
                if self.structured_output_model.__name__.lower() in structured_result:
                    structured_result = structured_result[
                        self.structured_output_model.__name__.lower()
                    ]
                elif "output" in structured_result:
                    structured_result = structured_result["output"]

                # Try to parse as the model if it's a dict
                if isinstance(structured_result, dict):
                    try:
                        structured_result = self.structured_output_model(
                            **structured_result
                        )
                    except:
                        pass

            # Post-process if hook provided
            if self.hooks.post_process:
                structured_result = self.hooks.post_process(structured_result)

            return structured_result

        except Exception as e:
            if self.hooks.error_handler:
                return self.hooks.error_handler(e)
            raise

    def _default_transform(
        self,
        first_result: Any,
        original_input: Any,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Default transformation of first agent output for second agent."""
        # Handle different output types
        if isinstance(first_result, dict):
            input_data = first_result
        elif isinstance(first_result, str):
            input_data = {"content": first_result}
        elif isinstance(first_result, BaseMessage):
            input_data = {"content": first_result.content}
        elif hasattr(first_result, "messages"):
            # Handle agent state with messages
            messages = first_result.messages
            if messages:
                input_data = {"content": messages[-1].content if messages else ""}
            else:
                input_data = {"content": str(first_result)}
        else:
            input_data = {"content": str(first_result)}

        # Add original query if available
        if isinstance(original_input, dict) and "query" in original_input:
            input_data["original_query"] = original_input["query"]
        elif isinstance(original_input, str):
            input_data["original_query"] = original_input

        # Add context if provided
        if context:
            input_data["context"] = context

        return {"input_data": input_data, "context": context or {}}


# Convenience factory functions


def create_react_to_structured(
    tools: list[Any],
    structured_output_model: type[OutputT],
    name: str = "react_structured",
    react_config: dict[str, Any] | None = None,
    structured_prompt: ChatPromptTemplate | None = None,
    hooks: SequentialHooks | None = None,
    debug: bool = False,
) -> SequentialAgentWithStructuredOutput[OutputT]:
    """Create a ReactAgent → StructuredOutput pipeline.

    Args:
        tools: Tools for the ReactAgent
        structured_output_model: Output model for structuring
        name: Name for the pipeline
        react_config: Optional config for ReactAgent
        structured_prompt: Optional custom structuring prompt
        hooks: Optional behavior hooks
        debug: Enable debug mode

    Returns:
        Configured sequential agent pipeline
    """
    react_config = react_config or {}

    react_agent = ReactAgent(
        name=f"{name}_react", tools=tools, engine=AugLLMConfig(**react_config)
    )

    return SequentialAgentWithStructuredOutput(
        first_agent=react_agent,
        structured_output_model=structured_output_model,
        structured_output_prompt=structured_prompt,
        hooks=hooks,
        name=name,
        debug=debug,
    )


def create_analysis_to_report(
    analysis_prompt: ChatPromptTemplate,
    report_model: type[OutputT],
    name: str = "analysis_report",
    analysis_config: dict[str, Any] | None = None,
    report_prompt: ChatPromptTemplate | None = None,
    hooks: SequentialHooks | None = None,
    debug: bool = False,
) -> SequentialAgentWithStructuredOutput[OutputT]:
    """Create an Analysis → Report pipeline.

    Args:
        analysis_prompt: Prompt for analysis agent
        report_model: Model for structured report
        name: Name for the pipeline
        analysis_config: Optional config for analysis agent
        report_prompt: Optional custom report prompt
        hooks: Optional behavior hooks
        debug: Enable debug mode

    Returns:
        Configured sequential agent pipeline
    """
    analysis_config = analysis_config or {}

    analysis_agent = SimpleAgent(
        name=f"{name}_analyzer",
        engine=AugLLMConfig(prompt_template=analysis_prompt, **analysis_config),
    )

    return SequentialAgentWithStructuredOutput(
        first_agent=analysis_agent,
        structured_output_model=report_model,
        structured_output_prompt=report_prompt,
        hooks=hooks,
        name=name,
        debug=debug,
    )


__all__ = [
    "SequentialAgentWithStructuredOutput",
    "SequentialHooks",
    "create_analysis_to_report",
    "create_react_to_structured",
]
