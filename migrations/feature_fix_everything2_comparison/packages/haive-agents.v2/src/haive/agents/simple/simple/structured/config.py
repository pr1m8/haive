"""Config configuration module.

This module provides config functionality for the Haive framework.

Classes:
    StructuredOutputAgentConfig: StructuredOutputAgentConfig implementation.

Functions:
    validate_and_setup: Validate And Setup functionality.
    set_output_parser: Set Output Parser functionality.
"""

from __future__ import annotations

from typing import Any

from haive.agents import tools
from haive.agents.simple.config import SimpleAgentConfig
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from pydantic import Field
from pydantic import model_validator


class StructuredOutputAgentConfig(SimpleAgentConfig):
    """Configuration for a structured output agent.

    Automatically sets up a single StructuredOutputTool for the provided
    model and configures the engine to always use this tool.
    """

    structured_output_model: type[BaseModel]
    engine: AugLLMConfig = Field(
        default_factory=lambda: AugLLMConfig(
            force_tool_use=True,  # Force using a tool
            # Auto-select the appropriate tool (will be the only one)
            force_tool_choice=True,
        ),
    )
    output_parser: PydanticOutputParser = Field(
        default_factory=lambda: PydanticOutputParser(),
    )
    output_schema = structured_output_model

    @model_validator(mode="after")
    @classmethod
    def validate_and_setup(cls) -> Any:
        """Set up the structured output tool and configure the engine."""
        # Create the StructuredOutputTool with the model
        output_tool = tools.StructuredOutputTool(self.structured_output_model)

        # Set up the engine configuration
        self.engine.tools = [output_tool]
        self.engine.structured_output_model = self.structured_output_model

        # The tool configuration should happen automatically through the engine's
        # _configure_tool_choice method, but we'll ensure it explicitly
        # as a safeguard and for backward compatibility
        if hasattr(output_tool, "name"):
            self.engine.force_tool_choice = output_tool.name
        elif hasattr(output_tool, "id"):
            self.engine.force_tool_choice = output_tool.id
        else:
            raise ValueError("StructuredOutputTool must have a name or id attribute")
        self.output_parser = PydanticOutputParser(
            pydantic_object=self.structured_output_model,
        )
        # Validate tool setup
        if len(self.engine.tools) != 1:
            raise ValueError(
                f"Expected exactly one tool, but got {len(self.engine.tools)}",
            )

        return self

    # @field_validator("output_parser", mode="after")
    # def set_output_parser(cls, v, values):
