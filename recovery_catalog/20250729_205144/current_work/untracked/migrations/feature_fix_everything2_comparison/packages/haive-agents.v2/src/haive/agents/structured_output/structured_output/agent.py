"""Generalized Structured Output Agent for enhancing any agent with structured output parsing."""

from typing import Any, Optional

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.prebuilt.messages.messages_with_token_usage import (
    MessagesStateWithTokenUsage,
)
from langchain_core.output_parsers import PydanticToolsParser
from pydantic import BaseModel, Field

from haive.agents.base.agent import Agent
from haive.agents.multi.proper_base import ProperMultiAgent
from haive.agents.simple.agent import SimpleAgent


class StructuredOutputAgent(SimpleAgent):
    """Agent that adds structured output parsing to any other agent.

    This agent acts as a post-processor that takes the output from any agent
    and ensures it conforms to a structured format. It can work standalone or
    as part of a sequential multi-agent chain.

    Key features:
    - Works with any agent type (SimpleAgent, ReactAgent, etc.)
    - Preserves original context and input
    - Uses PydanticToolsParser for robust parsing
    - Can be chained sequentially with any agent
    - Supports multiple output models

    Example:
        .. code-block:: python

            # Enhance any agent with structured output
            enhanced_agent = StructuredOutputAgent.enhance_agent(
            base_agent=my_agent,
            output_models=[SearchResult, AnalysisResult]
            )

            # Or use as standalone post-processor
            processor = StructuredOutputAgent.create_processor(
            output_models=[ResultModel],
            include_original_input=True
            )

    """

    # Configuration
    output_models: list[type[BaseModel]] = Field(
        default_factory=list, description="Pydantic models to parse outputs into"
    )

    include_original_input: bool = Field(
        default=True,
        description="Include original task/input in processing for context",
    )

    fallback_on_error: bool = Field(
        default=True, description="Return original content if parsing fails"
    )

    @classmethod
    def enhance_agent(
        cls,
        base_agent: Agent,
        output_models: list[type[BaseModel]],
        name: str | None = None,
        include_original_input: bool = True,
        **kwargs,
    ) -> ProperMultiAgent:
        """Enhance any agent with structured output capabilities.

        Creates a sequential multi-agent that runs:
        1. Base agent (processes input normally)
        2. StructuredOutputAgent (ensures output is structured)

        Args:
            base_agent: The agent to enhance
            output_models: List of Pydantic models for output formats
            name: Name for the enhanced agent
            include_original_input: Include original input for context
            **kwargs: Additional arguments for the structured output agent

        Returns:
            ProperMultiAgent configured for sequential execution
        """
        # Create structured output agent
        structured_agent = cls.create_processor(
            output_models=output_models,
            include_original_input=include_original_input,
            name=f"{base_agent.name}_structured_output",
            **kwargs,
        )

        # Create sequential multi-agent
        enhanced_name = name or f"{base_agent.name}_with_structured_output"

        # Create enhanced state class with proper annotations

        enhanced_state_attrs = {
            "__annotations__": {
                "structured_output_models": Optional[list[type[BaseModel]]],
                "parse_structured_outputs": bool,
            },
            "structured_output_models": Field(default=output_models),
            "parse_structured_outputs": Field(default=True),
        }

        enhanced_state_class = type(
            "EnhancedState", (MessagesStateWithTokenUsage,), enhanced_state_attrs
        )

        return ProperMultiAgent(
            name=enhanced_name,
            agents=[base_agent, structured_agent],
            execution_mode="sequential",
            state_schema=enhanced_state_class,
        )

    @classmethod
    def create_processor(
        cls,
        output_models: list[type[BaseModel]],
        name: str = "structured_output_processor",
        include_original_input: bool = True,
        system_message: str | None = None,
        **kwargs,
    ) -> "StructuredOutputAgent":
        """Create a standalone structured output processor.

        Args:
            output_models: List of Pydantic models for output formats
            name: Name for the processor
            include_original_input: Include original input for context
            system_message: Custom system message (auto-generated if not provided)
            **kwargs: Additional configuration

        Returns:
            Configured StructuredOutputAgent instance
        """
        # Generate format instructions
        PydanticToolsParser(tools=output_models)

        # Get example schemas
        model_examples = []
        for model in output_models:
            schema = model.schema()
            model_examples.append(f"{model.__name__}: {schema}")

        # Default system message if not provided
        if not system_message:
            system_message = f"""You are a structured output processor. Your task is to take the provided content and format it according to one of these schemas:

{chr(10).join(model_examples)}

Instructions:
1. Analyze the input content carefully
2. Determine which output model best fits the content
3. Extract and structure the information according to the chosen model
4. Output ONLY valid JSON that matches one of the schemas
5. If the content doesn't fit any model perfectly, choose the closest match

{'Include context from the original task when structuring the output.' if include_original_input else ''}

Remember: Output must be valid JSON matching one of the provided schemas."""

        # Create engine configuration
        engine = AugLLMConfig(
            name=f"{name}_engine",
            system_message=system_message,
            temperature=0.1,  # Low temperature for consistent parsing
            structured_output_version="v2",
        )

        # Create the agent
        return cls(
            name=name,
            engine=engine,
            output_models=output_models,
            include_original_input=include_original_input,
            **kwargs,
        )

    def process_with_context(
        self, content: str, original_input: str | None = None
    ) -> dict[str, Any]:
        """Process content with optional original context.

        Args:
            content: The content to structure
            original_input: Original task/query for context

        Returns:
            Structured output result
        """
        # Build prompt
        prompt_parts = []

        if self.include_original_input and original_input:
            prompt_parts.append(f"Original Task: {original_input}")
            prompt_parts.append("---")

        prompt_parts.append(f"Content to Structure:\n{content}")

        prompt = "\n".join(prompt_parts)

        # Process with structured output state
        result = self.run(prompt)
        return result

    @classmethod
    def create_reflection_processor(
        cls,
        reflection_models: list[type[BaseModel]],
        name: str = "reflection_processor",
        **kwargs,
    ) -> "StructuredOutputAgent":
        """Create a processor specifically for reflection patterns.

        This is optimized for reflection/reflexion agents that need to
        analyze their own outputs and provide structured feedback.

        Args:
            reflection_models: Models for reflection (e.g., Critique, Improvement)
            name: Name for the processor
            **kwargs: Additional configuration

        Returns:
            StructuredOutputAgent configured for reflection
        """
        system_message = """You are a reflection processor that analyzes agent outputs and provides structured feedback.

Analyze the provided content and output one of the following reflection formats:
{model_schemas}

Focus on:
1. Quality assessment
2. Identifying issues or improvements
3. Suggesting specific enhancements
4. Providing actionable feedback

Output must be valid JSON matching one of the reflection schemas."""

        return cls.create_processor(
            output_models=reflection_models,
            name=name,
            system_message=system_message,
            temperature=0.3,  # Slightly higher for creative reflection
            **kwargs,
        )

    @classmethod
    def create_validation_processor(
        cls,
        validation_models: list[type[BaseModel]],
        name: str = "validation_processor",
        **kwargs,
    ) -> "StructuredOutputAgent":
        """Create a processor for validation patterns.

        Args:
            validation_models: Models for validation results
            name: Name for the processor
            **kwargs: Additional configuration

        Returns:
            StructuredOutputAgent configured for validation
        """
        system_message = """You are a validation processor that checks outputs against requirements.

Validate the provided content and output one of the following validation formats:
{model_schemas}

Check for:
1. Completeness
2. Accuracy
3. Format compliance
4. Quality standards

Output must be valid JSON matching one of the validation schemas."""

        return cls.create_processor(
            output_models=validation_models,
            name=name,
            system_message=system_message,
            temperature=0.0,  # Deterministic for validation
            **kwargs,
        )

    def setup_agent(self) -> None:
        """Setup hook to configure structured output state."""
        super().setup_agent()

        # Ensure state has structured output capabilities
        if self.state_schema and self.output_models:
            # Configure structured output parsing
            if hasattr(self.state_schema, "structured_output_models"):
                self.state_schema.structured_output_models = self.output_models
                self.state_schema.parse_structured_outputs = True
