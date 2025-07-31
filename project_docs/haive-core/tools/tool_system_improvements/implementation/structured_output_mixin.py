"""Structured output mixin for handling LLM structured output patterns.

This module provides a mixin for handling structured output with LLMs,
supporting both parser-based and tool-calling approaches. It integrates
with BaseChatModel's bind_tools and with_structured_output methods.

The mixin provides:
- Automatic detection of structured output context
- Smart Pydantic model routing (parser vs tool)
- Integration with existing tool routing system
- Support for both v1 (parser) and v2 (tool-calling) approaches
"""

import logging
from typing import Any, Literal

from langchain_core.output_parsers import BaseOutputParser, PydanticOutputParser
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.runnables import Runnable
from pydantic import BaseModel, Field, model_validator

logger = logging.getLogger(__name__)

# Type for structured output methods
StructuredOutputMethod = Literal["parser", "tool_calling"]
StructuredOutputVersion = Literal["v1", "v2"]


class StructuredOutputMixin(BaseModel):
    """Mixin for handling structured output with LLMs.

    This mixin provides functionality for configuring LLMs to output
    structured data using either parser-based or tool-calling approaches.
    It detects usage context and routes Pydantic models appropriately.

    Attributes:
        structured_output_model: Optional Pydantic model for structured output
        structured_output_method: Method to use (parser or tool_calling)
        structured_output_version: Version to use (v1 or v2)
        include_raw: Whether to include raw output alongside structured
        structured_output_contexts: Track contexts where models are used
    """

    # Core configuration
    structured_output_model: type[BaseModel] | None = Field(
        default=None, description="Pydantic model for structured output"
    )

    structured_output_method: StructuredOutputMethod = Field(
        default="tool_calling",
        description="Method for structured output: 'parser' or 'tool_calling'",
    )

    structured_output_version: StructuredOutputVersion = Field(
        default="v2",
        description="Version of structured output: 'v1' (parser) or 'v2' (tool)",
    )

    include_raw: bool = Field(
        default=False, description="Include raw output alongside structured"
    )

    # Context tracking
    structured_output_contexts: dict[str, str] = Field(
        default_factory=dict,
        description="Track contexts where models are used (model_name -> context)",
    )

    # Parser management
    _structured_output_parser: BaseOutputParser | None = None

    def with_structured_output(
        self,
        schema: dict[str, Any] | type[BaseModel],
        *,
        method: StructuredOutputMethod | None = None,
        include_raw: bool | None = None,
        version: StructuredOutputVersion | None = None,
        **kwargs,
    ) -> "StructuredOutputMixin":
        """Configure for structured output.

        This method configures the mixin to handle structured output,
        automatically detecting the best approach based on the schema
        and configuration.

        Args:
            schema: Dictionary schema or Pydantic model class
            method: Override default method (parser or tool_calling)
            include_raw: Override default include_raw setting
            version: Override default version (v1 or v2)
            **kwargs: Additional configuration options

        Returns:
            Self for method chaining
        """
        # Handle schema
        if isinstance(schema, dict):
            # Convert dict schema to Pydantic model
            # This is a simplified version - real implementation would be more robust
            logger.warning("Dictionary schemas not fully implemented yet")
            return self
        if isinstance(schema, type) and issubclass(schema, BaseModel):
            self.structured_output_model = schema
        else:
            raise ValueError(f"Invalid schema type: {type(schema)}")

        # Update configuration
        if method is not None:
            self.structured_output_method = method
        if include_raw is not None:
            self.include_raw = include_raw
        if version is not None:
            self.structured_output_version = version

        # Track context
        model_name = schema.__name__ if hasattr(schema, "__name__") else str(schema)
        self.structured_output_contexts[model_name] = "structured_output"

        # Create parser if using parser method
        if (
            self.structured_output_method == "parser"
            or self.structured_output_version == "v1"
        ):
            self._create_structured_output_parser()

        logger.debug(
            f"Configured structured output: model={model_name}, "
            f"method={self.structured_output_method}, version={self.structured_output_version}"
        )

        return self

    def _create_structured_output_parser(self) -> None:
        """Create appropriate parser for structured output."""
        if not self.structured_output_model:
            return

        if self.structured_output_method == "parser":
            # Use PydanticOutputParser for v1 approach
            self._structured_output_parser = PydanticOutputParser(
                pydantic_object=self.structured_output_model
            )
        else:
            # Use PydanticToolsParser for v2 approach
            self._structured_output_parser = PydanticToolsParser(
                tools=[self.structured_output_model]
            )

    def get_structured_output_parser(self) -> BaseOutputParser | None:
        """Get the configured structured output parser.

        Returns:
            Configured parser or None if not using parser method
        """
        if (
            self.structured_output_method == "parser"
            and not self._structured_output_parser
        ):
            self._create_structured_output_parser()
        return self._structured_output_parser

    def _detect_structured_output_usage(self, model: type[BaseModel]) -> bool:
        """Detect if a model is being used for structured output.

        Args:
            model: Pydantic model to check

        Returns:
            True if model is configured for structured output
        """
        if self.structured_output_model and model == self.structured_output_model:
            return True

        model_name = model.__name__ if hasattr(model, "__name__") else str(model)
        return self.structured_output_contexts.get(model_name) == "structured_output"

    def route_pydantic_model(
        self, model: type[BaseModel], force_tool: bool = False
    ) -> str:
        """Smart routing for Pydantic models based on usage context.

        Args:
            model: Pydantic model to route
            force_tool: Force routing as tool regardless of context

        Returns:
            Route string: "parser" if for structured output, "pydantic_model" otherwise
        """
        if force_tool:
            return "pydantic_model"

        # Check if this is our structured output model
        if self._detect_structured_output_usage(model):
            # For structured output, route based on method/version
            if (
                self.structured_output_method == "parser"
                or self.structured_output_version == "v1"
            ):
                return "parser"
            # v2 uses tool calling, but we still mark it differently
            return "structured_output_tool"

        # Check if model has __call__ method (executable tool)
        if callable(model) and callable(model.__call__):
            return "pydantic_model"  # It's an executable tool

        # Default to parser if no clear indication
        return "parser"

    def bind_structured_output_tools(
        self, llm: Any, tools: list[Any] | None = None
    ) -> Any:
        """Bind tools for structured output using tool calling approach.

        This method handles the v2 approach where structured output
        uses bind_tools with tool_choice.

        Args:
            llm: Language model to bind tools to
            tools: Optional additional tools to bind

        Returns:
            LLM with tools bound for structured output
        """
        if not self.structured_output_model:
            raise ValueError("No structured output model configured")

        if (
            self.structured_output_method != "tool_calling"
            and self.structured_output_version != "v2"
        ):
            raise ValueError("This method is only for tool_calling/v2 approach")

        # Prepare tools list
        all_tools = []

        # Add structured output model as a tool
        all_tools.append(self.structured_output_model)

        # Add any additional tools
        if tools:
            all_tools.extend(tools)

        # Bind tools with tool_choice for structured output
        return llm.bind_tools(
            tools=all_tools, tool_choice=self.structured_output_model.__name__
        )

    def create_structured_output_chain(
        self, llm: Any, prompt: Any | None = None
    ) -> Runnable:
        """Create a complete chain for structured output.

        This method creates a chain that handles structured output
        based on the configured method and version.

        Args:
            llm: Language model to use
            prompt: Optional prompt template

        Returns:
            Runnable chain for structured output
        """
        if not self.structured_output_model:
            raise ValueError("No structured output model configured")

        # Version 1: Parser-based approach
        if (
            self.structured_output_method == "parser"
            or self.structured_output_version == "v1"
        ):
            parser = self.get_structured_output_parser()
            if not parser:
                raise ValueError("Failed to create parser")

            if prompt:
                return prompt | llm | parser
            return llm | parser

        # Version 2: Tool-calling approach
        # Use with_structured_output if available
        if hasattr(llm, "with_structured_output"):
            structured_llm = llm.with_structured_output(
                self.structured_output_model, include_raw=self.include_raw
            )
        else:
            # Fallback to bind_tools
            structured_llm = self.bind_structured_output_tools(llm)

        if prompt:
            return prompt | structured_llm
        return structured_llm

    @model_validator(mode="after")
    def _validate_structured_output_config(self) -> "StructuredOutputMixin":
        """Validate structured output configuration."""
        # Ensure version matches method
        if (
            self.structured_output_method == "parser"
            and self.structured_output_version == "v2"
        ):
            logger.warning("Parser method typically uses v1, adjusting version")
            self.structured_output_version = "v1"
        elif (
            self.structured_output_method == "tool_calling"
            and self.structured_output_version == "v1"
        ):
            logger.warning("Tool calling method typically uses v2, adjusting version")
            self.structured_output_version = "v2"

        return self

    def clear_structured_output(self) -> "StructuredOutputMixin":
        """Clear structured output configuration.

        Returns:
            Self for method chaining
        """
        self.structured_output_model = None
        self._structured_output_parser = None
        self.structured_output_contexts.clear()
        logger.debug("Cleared structured output configuration")
        return self

    def is_structured_output_configured(self) -> bool:
        """Check if structured output is configured.

        Returns:
            True if structured output model is set
        """
        return self.structured_output_model is not None

    def get_structured_output_info(self) -> dict[str, Any]:
        """Get information about structured output configuration.

        Returns:
            Dictionary with configuration details
        """
        if not self.structured_output_model:
            return {"configured": False}

        return {
            "configured": True,
            "model": self.structured_output_model.__name__,
            "method": self.structured_output_method,
            "version": self.structured_output_version,
            "include_raw": self.include_raw,
            "contexts": self.structured_output_contexts,
            "parser_type": (
                type(self._structured_output_parser).__name__
                if self._structured_output_parser
                else None
            ),
        }
