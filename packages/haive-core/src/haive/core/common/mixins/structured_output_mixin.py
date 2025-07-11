"""Mixin for handling structured output in LLM configurations.

This mixin provides functionality to configure and manage structured output models
with support for both v1 (parser-based) and v2 (tool-based) approaches.
"""

from typing import TYPE_CHECKING, Any, Dict, List, Literal, Optional, Type, Union, cast

from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel

if TYPE_CHECKING:
    from langchain_core.output_parsers import BaseOutputParser

StructuredOutputVersion = Literal["v1", "v2"]


class StructuredOutputMixin:
    """Mixin to provide structured output functionality for LLM configurations.

    This mixin adds support for:
    - Configuring structured output models with v1 (parser) or v2 (tool) approaches
    - Automatic format instruction generation
    - Tool-based structured output forcing
    """

    # These fields must be defined by subclasses
    # We use type annotations to indicate expected types
    structured_output_model: type[BaseModel] | None
    structured_output_version: StructuredOutputVersion | None
    include_format_instructions: bool
    output_parser: Optional["BaseOutputParser"]
    parser_type: str | None
    partial_variables: dict[str, Any]
    tools: list[Any]
    pydantic_tools: list[type[BaseModel]]
    force_tool_use: bool
    force_tool_choice: bool | str | list[str] | None
    tool_choice_mode: str
    bind_tools_kwargs: dict[str, Any]
    _tool_name_mapping: dict[str, str]
    _format_instructions_text: str | None
    _is_processing_validation: bool

    def with_structured_output(
        self,
        model: type[BaseModel],
        include_instructions: bool = True,
        version: str = "v2",
    ) -> "StructuredOutputMixin":
        """Configure with Pydantic structured output.

        Args:
            model: The Pydantic model to use for structured output
            include_instructions: Whether to include format instructions
            version: Version of structured output ("v1" for parser-based, "v2" for tool-based)

        Returns:
            Self for method chaining
        """
        # Set the structured output model
        self.structured_output_model = model
        self.include_format_instructions = include_instructions

        # Validate version
        if version not in ["v1", "v2"]:
            version = "v2"

        self.structured_output_version = cast(StructuredOutputVersion, version)

        # Trigger validation if the subclass has it
        if (
            hasattr(self, "comprehensive_validation_and_setup")
            and not self._is_processing_validation
        ):
            self.comprehensive_validation_and_setup()

        return self

    def _setup_v2_structured_output(self):
        """Setup v2 (tool-based) approach - force tool usage with format instructions, NO parsing."""
        if not self.structured_output_model:
            return

        # Ensure the model is in tools list
        if self.structured_output_model not in self.tools:
            self.tools = list(self.tools) if self.tools else []
            self.tools.append(self.structured_output_model)

        # Add to pydantic_tools for tracking
        if self.structured_output_model not in self.pydantic_tools:
            self.pydantic_tools.append(self.structured_output_model)

        # Explicitly set parser_type to None for v2
        self.parser_type = None

        # Explicitly set output_parser to None for v2
        self.output_parser = None

        # Configure tool usage - FORCE this specific tool
        self.force_tool_use = True
        self.tool_choice_mode = "required"

        # The actual tool name used in binding is the class name (exact case)
        model_class_name = self.structured_output_model.__name__
        actual_tool_name = model_class_name

        # Update tool name mapping
        self._tool_name_mapping[model_class_name] = actual_tool_name

        # Set force_tool_choice to the actual tool name
        self.force_tool_choice = actual_tool_name

        # Add format instructions for the model using PydanticOutputParser
        if self.include_format_instructions:
            try:
                parser = PydanticOutputParser(
                    pydantic_object=self.structured_output_model
                )
                instructions = parser.get_format_instructions()
                self.partial_variables["format_instructions"] = instructions
                self._format_instructions_text = instructions
            except Exception:
                pass  # Silently handle errors

        # Update bind_tools_kwargs to use the correct tool choice format
        self._update_bind_tools_kwargs_for_v2()

    def _setup_v1_structured_output(self):
        """Setup v1 (traditional) structured output."""
        if not self.structured_output_model:
            return

        self.parser_type = "pydantic"
        self.output_parser = PydanticOutputParser(
            pydantic_object=self.structured_output_model
        )

    def _update_bind_tools_kwargs_for_v2(self):
        """Update bind_tools_kwargs specifically for v2 structured output."""
        if self.structured_output_version == "v2" and self.force_tool_choice:
            self.bind_tools_kwargs["tool_choice"] = {
                "type": "function",
                "function": {"name": self.force_tool_choice},
            }
        elif self.tool_choice_mode == "required":
            self.bind_tools_kwargs["tool_choice"] = "required"

    def _create_structured_output_tool(
        self, name: str, description: str, **kwargs
    ) -> Any:
        """Create a tool from the structured output model."""
        if not self.structured_output_model:
            raise ValueError("No structured output model configured")

        # For structured output models, return the model class itself
        # but add tool metadata
        tool_class = self.structured_output_model

        # Add metadata if subclass has set_tool_route method
        if hasattr(self, "set_tool_route"):
            metadata = {
                "llm_config": getattr(self, "name", "anonymous"),
                "version": self.structured_output_version,
                "tool_type": "structured_output",
            }
            self.set_tool_route(name, "structured_output", metadata)

        return tool_class

    def _mark_structured_output_tools(self):
        """Mark tools that are structured output models with metadata."""
        if not self.structured_output_model:
            return

        structured_model_name = self.structured_output_model.__name__

        for tool in self.tools:
            if hasattr(tool, "__name__") and tool.__name__ == structured_model_name:
                # Add metadata if this is the subclass's set_tool_route method
                if hasattr(self, "set_tool_route"):
                    metadata = {
                        "is_structured_output": True,
                        "version": self.structured_output_version,
                    }
                    self.set_tool_route(tool.__name__, "structured_output", metadata)
