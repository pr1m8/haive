"""Utilities for converting Pydantic models to prompt templates.

This module provides utilities to create prompt templates from Pydantic models,
supporting the structured output pattern where prompts focus on generation
and parsers handle the structured parsing separately.

Key features:
- Generate prompts that guide LLMs to create content parseable by Pydantic models
- Support for different prompt styles (descriptive, example-based, schema-based)
- Field-specific guidance and constraints
- Optional examples and formatting hints
"""

import json
from enum import Enum
from typing import Any, Dict, List, Optional, Type, Union, get_args, get_origin

from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from pydantic import BaseModel, Field


class PromptStyle(str, Enum):
    """Different styles for generating prompts from Pydantic models."""

    DESCRIPTIVE = "descriptive"  # Focus on field descriptions
    SCHEMA_BASED = "schema_based"  # Include JSON schema information
    EXAMPLE_BASED = "example_based"  # Use examples to guide format
    NATURAL = "natural"  # Natural language description
    STRUCTURED = "structured"  # Explicit structure guidance


class PydanticPromptConfig(BaseModel):
    """Configuration for Pydantic model to prompt conversion."""

    style: PromptStyle = Field(
        default=PromptStyle.DESCRIPTIVE, description="Style of prompt to generate"
    )
    include_field_types: bool = Field(
        default=True, description="Whether to include field type information"
    )
    include_constraints: bool = Field(
        default=True,
        description="Whether to include field constraints (min/max length, etc.)",
    )
    include_examples: bool = Field(
        default=False, description="Whether to include example values"
    )
    use_json_format: bool = Field(
        default=False, description="Whether to request JSON format output"
    )
    custom_instructions: str | None = Field(
        default=None, description="Additional custom instructions"
    )
    field_priorities: dict[str, int] | None = Field(
        default=None, description="Priority ordering for fields (1=highest)"
    )


def analyze_pydantic_field(field_info: Any, field_name: str) -> dict[str, Any]:
    """Analyze a Pydantic field to extract information for prompt generation.

    Args:
        field_info: Pydantic FieldInfo object
        field_name: Name of the field

    Returns:
        Dictionary containing field analysis
    """
    analysis = {
        "name": field_name,
        "description": getattr(field_info, "description", ""),
        "default": getattr(field_info, "default", None),
        "required": getattr(field_info, "default", Field.Ellipsis) is Field.Ellipsis,
        "type_info": {},
        "constraints": {},
        "examples": [],
    }

    # Extract type information
    field_annotation = getattr(field_info, "annotation", None)
    if field_annotation:
        analysis["type_info"] = analyze_type_annotation(field_annotation)

    # Extract constraints
    if hasattr(field_info, "constraints"):
        for constraint_name in ["min_length", "max_length", "ge", "le", "gt", "lt"]:
            if hasattr(field_info.constraints, constraint_name):
                value = getattr(field_info.constraints, constraint_name)
                if value is not None:
                    analysis["constraints"][constraint_name] = value

    # Extract examples from field metadata
    if hasattr(field_info, "json_schema_extra") and field_info.json_schema_extra:
        if isinstance(field_info.json_schema_extra, dict):
            analysis["examples"] = field_info.json_schema_extra.get("examples", [])

    return analysis


def analyze_type_annotation(annotation: type) -> dict[str, Any]:
    """Analyze a type annotation to extract useful information.

    Args:
        annotation: Type annotation to analyze

    Returns:
        Dictionary containing type analysis
    """
    type_info = {
        "base_type": None,
        "is_optional": False,
        "is_list": False,
        "is_enum": False,
        "enum_values": [],
        "nested_model": None,
    }

    # Handle Union types (including Optional)
    origin = get_origin(annotation)
    args = get_args(annotation)

    if origin is Union:
        # Check if it's Optional (Union with None)
        non_none_args = [arg for arg in args if arg is not type(None)]
        if len(non_none_args) == 1 and type(None) in args:
            type_info["is_optional"] = True
            annotation = non_none_args[0]
            origin = get_origin(annotation)
            args = get_args(annotation)

    # Handle List types
    if origin is list or origin is list:
        type_info["is_list"] = True
        if args:
            annotation = args[0]

    # Determine base type
    if isinstance(annotation, type):
        type_info["base_type"] = annotation.__name__

        # Check if it's an Enum
        if issubclass(annotation, Enum):
            type_info["is_enum"] = True
            type_info["enum_values"] = [e.value for e in annotation]

        # Check if it's a nested Pydantic model
        elif issubclass(annotation, BaseModel):
            type_info["nested_model"] = annotation
    else:
        type_info["base_type"] = str(annotation)

    return type_info


def generate_field_description(
    field_analysis: dict[str, Any], style: PromptStyle
) -> str:
    """Generate a description for a field based on analysis and style.

    Args:
        field_analysis: Field analysis from analyze_pydantic_field
        style: Prompt style to use

    Returns:
        Description string for the field
    """
    name = field_analysis["name"]
    desc = field_analysis["description"]
    type_info = field_analysis["type_info"]
    constraints = field_analysis["constraints"]
    required = field_analysis["required"]

    if style == PromptStyle.DESCRIPTIVE:
        parts = [f"**{name}**"]
        if required:
            parts.append("(required)")
        else:
            parts.append("(optional)")

        if desc:
            parts.append(f"- {desc}")

        # Add type information
        if type_info.get("base_type"):
            type_desc = f"Type: {type_info['base_type']}"
            if type_info["is_list"]:
                type_desc = f"List of {type_desc.lower()}"
            if type_info["is_optional"]:
                type_desc += " (optional)"
            parts.append(f"- {type_desc}")

        # Add enum values
        if type_info["is_enum"] and type_info["enum_values"]:
            values = ", ".join(f"'{v}'" for v in type_info["enum_values"])
            parts.append(f"- Allowed values: {values}")

        # Add constraints
        if constraints:
            constraint_parts = []
            if "min_length" in constraints:
                constraint_parts.append(f"min length {constraints['min_length']}")
            if "max_length" in constraints:
                constraint_parts.append(f"max length {constraints['max_length']}")
            if "ge" in constraints:
                constraint_parts.append(f"≥ {constraints['ge']}")
            if "le" in constraints:
                constraint_parts.append(f"≤ {constraints['le']}")
            if constraint_parts:
                parts.append(f"- Constraints: {', '.join(constraint_parts)}")

        return "\n".join(parts)

    if style == PromptStyle.NATURAL:
        base = (
            f"Provide {desc.lower()}"
            if desc
            else f"Provide the {name.replace('_', ' ')}"
        )

        if type_info["is_enum"] and type_info["enum_values"]:
            values = ", ".join(f"'{v}'" for v in type_info["enum_values"])
            base += f" (choose from: {values})"

        if not required:
            base += " (optional)"

        return base

    if style == PromptStyle.STRUCTURED:
        parts = [f"{name}:"]
        if desc:
            parts.append(f"  Description: {desc}")
        if type_info.get("base_type"):
            parts.append(f"  Type: {type_info['base_type']}")
        if type_info["is_enum"]:
            parts.append(f"  Options: {', '.join(type_info['enum_values'])}")
        if not required:
            parts.append("  (Optional)")
        return "\n".join(parts)

    # Default fallback
    return f"{name}: {desc or 'No description'}"


def create_pydantic_prompt(
    model_class: type[BaseModel],
    config: PydanticPromptConfig,
    base_instruction: str = "Generate content with the following structure:",
) -> ChatPromptTemplate:
    """Create a prompt template from a Pydantic model.

    Args:
        model_class: Pydantic model class to create prompt for
        config: Configuration for prompt generation
        base_instruction: Base instruction for the prompt

    Returns:
        ChatPromptTemplate that guides LLM to generate parseable content
    """
    # Analyze model fields
    field_analyses = []
    for field_name, field_info in model_class.model_fields.items():
        analysis = analyze_pydantic_field(field_info, field_name)
        field_analyses.append(analysis)

    # Sort fields by priority if specified
    if config.field_priorities:
        field_analyses.sort(key=lambda x: config.field_priorities.get(x["name"], 999))

    # Generate field descriptions
    field_descriptions = []
    for analysis in field_analyses:
        desc = generate_field_description(analysis, config.style)
        field_descriptions.append(desc)

    # Build the complete prompt
    prompt_parts = [base_instruction]

    if config.style == PromptStyle.SCHEMA_BASED:
        # Include JSON schema
        schema = model_class.model_json_schema()
        prompt_parts.append(
            f"\nJSON Schema:\n```json\n{json.dumps(schema, indent=2)}\n```"
        )

    # Add field descriptions
    if config.style == PromptStyle.NATURAL:
        prompt_parts.append("\nPlease provide:")
        for desc in field_descriptions:
            prompt_parts.append(f"- {desc}")
    else:
        prompt_parts.append("\nRequired fields:")
        prompt_parts.extend(field_descriptions)

    # Add format instructions
    if config.use_json_format:
        prompt_parts.append("\nProvide your response in valid JSON format.")
    else:
        prompt_parts.append("\nStructure your response clearly with labeled sections.")

    # Add custom instructions
    if config.custom_instructions:
        prompt_parts.append(f"\nAdditional instructions: {config.custom_instructions}")

    # Add examples if requested
    if config.include_examples:
        example = create_example_from_model(model_class)
        if example:
            prompt_parts.append(f"\nExample format:\n{example}")

    system_prompt = "\n".join(prompt_parts)

    return ChatPromptTemplate.from_messages(
        [("system", system_prompt), ("human", "{query}")]
    )


def create_example_from_model(model_class: type[BaseModel]) -> str:
    """Create an example output from a Pydantic model.

    Args:
        model_class: Pydantic model class

    Returns:
        Example string showing the expected format
    """
    try:
        # Try to create an example with default values
        example_data = {}
        for field_name, field_info in model_class.model_fields.items():
            analysis = analyze_pydantic_field(field_info, field_name)
            type_info = analysis["type_info"]

            if type_info["is_enum"] and type_info["enum_values"]:
                example_data[field_name] = type_info["enum_values"][0]
            elif type_info["base_type"] == "str":
                example_data[field_name] = f"Example {field_name.replace('_', ' ')}"
            elif type_info["base_type"] == "int":
                example_data[field_name] = 42
            elif type_info["base_type"] == "float":
                example_data[field_name] = 3.14
            elif type_info["base_type"] == "bool":
                example_data[field_name] = True
            elif type_info["is_list"]:
                example_data[field_name] = ["example_item_1", "example_item_2"]
            else:
                example_data[field_name] = f"<{field_name}>"

        # Create example instance and return JSON
        example_instance = model_class(**example_data)
        return json.dumps(example_instance.model_dump(), indent=2)

    except Exception:
        # Fallback to schema-based example
        return f"<Example for {model_class.__name__}>"


def create_parsing_prompt(
    model_class: type[BaseModel], content_field: str = "content"
) -> ChatPromptTemplate:
    """Create a prompt for parsing content into a Pydantic model.

    This creates a separate parsing prompt that can be used after generation
    to extract structured information from unstructured content.

    Args:
        model_class: Pydantic model class to parse into
        content_field: Name of the field containing the content to parse

    Returns:
        ChatPromptTemplate for parsing content
    """
    schema = model_class.model_json_schema()

    prompt = f"""Parse the following content and extract structured information according to the schema.

Target Schema: {model_class.__name__}
```json
{json.dumps(schema, indent=2)}
```

Content to parse:
{{{content_field}}}

Extract the information and provide it in valid JSON format matching the schema above.
If information is missing or unclear, use null for optional fields or provide reasonable defaults.
Focus on accuracy and completeness of the extracted information."""

    return ChatPromptTemplate.from_messages(
        [("system", prompt), ("human", "Parse this content: {content}")]
    )


# ==============================================================================
# CONVENIENCE FUNCTIONS
# ==============================================================================


def create_generation_and_parsing_prompts(
    model_class: type[BaseModel],
    generation_instruction: str = "Generate comprehensive content about the topic:",
    config: PydanticPromptConfig | None = None,
) -> tuple[ChatPromptTemplate, ChatPromptTemplate]:
    """Create both generation and parsing prompts for structured output pattern.

    This follows the best practice of separating content generation from
    structured parsing, allowing the LLM to focus on creating good content
    first, then extracting structure from that content.

    Args:
        model_class: Pydantic model class
        generation_instruction: Instruction for content generation
        config: Configuration for prompt generation

    Returns:
        Tuple of (generation_prompt, parsing_prompt)
    """
    if config is None:
        config = PydanticPromptConfig(style=PromptStyle.NATURAL)

    # Generation prompt focuses on content creation
    generation_prompt = ChatPromptTemplate.from_messages(
        [("system", generation_instruction), ("human", "{query}")]
    )

    # Parsing prompt extracts structure from generated content
    parsing_prompt = create_parsing_prompt(model_class)

    return generation_prompt, parsing_prompt


def quick_pydantic_prompt(
    model_class: type[BaseModel],
    style: PromptStyle = PromptStyle.DESCRIPTIVE,
    use_json: bool = False,
) -> ChatPromptTemplate:
    """Quick way to create a basic prompt from a Pydantic model.

    Args:
        model_class: Pydantic model class
        style: Prompt style to use
        use_json: Whether to request JSON format

    Returns:
        ChatPromptTemplate for the model
    """
    config = PydanticPromptConfig(
        style=style, use_json_format=use_json, include_examples=True
    )

    return create_pydantic_prompt(
        model_class=model_class,
        config=config,
        base_instruction=f"Generate content that can be structured as {model_class.__name__}:",
    )
