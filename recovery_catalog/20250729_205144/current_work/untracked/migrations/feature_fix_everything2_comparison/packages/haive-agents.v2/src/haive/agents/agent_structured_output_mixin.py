"""Mixin for adding structured output capabilities to agents.

This mixin provides class methods for creating agents with structured output,
enabling any agent to be composed with a StructuredOutputAgent for type-safe
output conversion.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar

from pydantic import BaseModel

if TYPE_CHECKING:
    from langchain_core.prompts import ChatPromptTemplate

    from haive.agents.base.agent import Agent

T = TypeVar("T", bound=BaseModel)
TAgent = TypeVar("TAgent", bound="Agent")


class StructuredOutputMixin:
    """Mixin that adds structured output capabilities to any agent."""

    @classmethod
    def with_structured_output(
        cls: type[TAgent],
        output_model: type[T],
        name: str | None = None,
        custom_context: str | None = None,
        custom_prompt: ChatPromptTemplate | None = None,
        **agent_kwargs,
    ) -> tuple[TAgent, Agent]:
        """Create an agent paired with a StructuredOutputAgent for structured output.

        This method creates a two-agent workflow where:
        1. The original agent produces unstructured output
        2. A StructuredOutputAgent converts it to the specified model

        The agents are designed to work in sequence in a multi-agent workflow,
        with the structured output agent reading from messages state.

        Args:
            output_model: The Pydantic model to structure output into
            name: Optional name for the agent (defaults to class name)
            custom_context: Optional context for extraction
            custom_prompt: Optional custom prompt template
            **agent_kwargs: Arguments passed to the original agent constructor

        Returns:
            Tuple of (original_agent, structured_output_agent)

        Examples:
            Basic usage::

                # Create ReactAgent with structured output
                planner, structurer = ReactAgent.with_structured_output(
                    output_model=PlanOutput,
                    name="planner"
                )

                # Use in multi-agent workflow
                agents = [planner, structurer]

            Custom extraction::

                analyzer, structurer = SimpleAgent.with_structured_output(
                    output_model=AnalysisResult,
                    custom_context="Focus on quantitative metrics",
                    temperature=0.7
                )

            In state definition::

                class WorkflowState(MultiAgentState):
                    # AnalysisResult fields will be populated
                    summary: str = ""
                    metrics: Dict[str, float] = Field(default_factory=dict)
                    confidence: float = 0.0
        """
        # Avoid circular import
        from haive.agents.structured import StructuredOutputAgent

        # Create the original agent
        agent_name = name or cls.__name__.lower()
        original_agent = cls(name=agent_name, **agent_kwargs)

        # Create the structured output agent
        structurer_name = f"{agent_name}_structured"
        structured_agent = StructuredOutputAgent(
            name=structurer_name,
            output_model=output_model,
            custom_context=custom_context,
            custom_prompt=custom_prompt,
            # Use low temperature for consistent extraction
            engine=agent_kwargs.get("engine"),
        )

        return original_agent, structured_agent

    @classmethod
    def as_structured_tool(
        cls: type[TAgent],
        output_model: type[T],
        name: str | None = None,
        description: str | None = None,
        **agent_kwargs,
    ) -> Any:
        """Convert agent to a tool that returns structured output.

        This creates a tool that:
        1. Runs the agent
        2. Converts output to structured format
        3. Returns the Pydantic model instance

        Args:
            output_model: The Pydantic model for output
            name: Optional tool name
            description: Optional tool description
            **agent_kwargs: Arguments for agent construction

        Returns:
            LangChain tool that returns structured output

        Examples:
            Create structured tool::

                research_tool = ResearchAgent.as_structured_tool(
                    output_model=ResearchResult,
                    name="research_tool",
                    description="Research topics and return structured results"
                )

                # Use in another agent
                coordinator = ReactAgent(
                    name="coordinator",
                    tools=[research_tool]
                )
        """
        from langchain_core.tools import Tool

        from haive.agents.structured import StructuredOutputAgent

        tool_name = name or f"{cls.__name__.lower()}_structured_tool"
        tool_description = (
            description or f"Run {cls.__name__} and return structured output"
        )

        def run_with_structured_output(input_text: str) -> T:
            """Run agent and convert to structured output."""
            # Create agent instance
            agent = cls(**agent_kwargs)

            # Run agent
            result = agent.run(input_text)

            # Convert to structured output
            structurer = StructuredOutputAgent(
                name=f"{agent.name}_structurer",
                output_model=output_model,
                engine=agent_kwargs.get("engine"),
            )

            # Handle different result types
            if isinstance(result, str):
                structured_result = structurer.run(result)
            elif hasattr(result, "content"):
                structured_result = structurer.run(result.content)
            elif isinstance(result, dict) and "output" in result:
                structured_result = structurer.run(result["output"])
            else:
                structured_result = structurer.run(str(result))

            return structured_result

        return Tool(
            name=tool_name,
            description=tool_description,
            func=run_with_structured_output,
            args_schema=agent_kwargs.get("input_schema"),
        )

    def ensure_structured_output(
        self, output: Any, output_model: type[T], handle_errors: bool = True
    ) -> T | None:
        """Ensure agent output conforms to a structured model.

        This instance method can be used to validate/convert output
        after execution, handling various output formats gracefully.

        Args:
            output: The output to structure (str, BaseMessage, dict, etc.)
            output_model: The Pydantic model to convert to
            handle_errors: Whether to return None on errors (vs raising)

        Returns:
            Structured output instance or None if error and handle_errors=True

        Examples:
            In agent implementation::

                def run(self, input_text: str) -> Any:
                    # Get raw output
                    raw_output = self.engine.invoke(input_text)

                    # Ensure it's structured
                    return self.ensure_structured_output(
                        raw_output,
                        self.output_schema
                    )
        """
        from langchain_core.messages import BaseMessage
        from langchain_core.output_parsers import PydanticToolsParser

        from haive.agents.structured import StructuredOutputAgent

        try:
            # If already the right type, return it
            if isinstance(output, output_model):
                return output

            # Extract content from various formats
            content = None

            if isinstance(output, str):
                content = output
            elif isinstance(output, BaseMessage):
                # Check for tool calls first
                if hasattr(output, "tool_calls") and output.tool_calls:
                    # Parse tool calls
                    parser = PydanticToolsParser(tools=[output_model])
                    parsed = parser.parse(output)
                    if parsed and isinstance(parsed[0], output_model):
                        return parsed[0]
                content = output.content
            elif isinstance(output, dict):
                # Try direct model construction first
                try:
                    return output_model(**output)
                except BaseException:
                    # Fall back to string conversion
                    content = output.get("output", output.get("content", str(output)))
            elif isinstance(output, list):
                # Handle list of messages
                if output and isinstance(output[0], BaseMessage):
                    return self.ensure_structured_output(
                        output[-1], output_model, handle_errors
                    )
                content = str(output)
            else:
                content = str(output)

            # Use StructuredOutputAgent for conversion
            if content:
                structurer = StructuredOutputAgent(
                    name="temp_structurer",
                    output_model=output_model,
                    engine=getattr(self, "engine", None),
                )
                return structurer.run(content)

            if handle_errors:
                return None
            raise ValueError(
                f"Could not convert output to {
                    output_model.__name__}"
            )

        except Exception:
            if handle_errors:
                return None
            raise
