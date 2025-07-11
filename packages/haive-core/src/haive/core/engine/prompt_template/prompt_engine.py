"""PromptTemplateEngine: InvokableEngine wrapper for LangChain prompt templates.

This module provides the PromptTemplateEngine class, which wraps LangChain prompt
templates as first-class InvokableEngines with automatic input schema derivation
and robust formatting capabilities.

The PromptTemplateEngine bridges the gap between LangChain's prompt template system
and Haive's engine architecture, enabling prompt templates to be treated as
composable, schema-aware components within complex agent workflows.

Key Features:
    - Automatic input schema derivation from prompt template variables
    - Smart type inference for common variable patterns (messages, lists, context)
    - Enhanced variable detection that extracts variables from message content
    - Robust formatting using LangChain's PromptValue system
    - Support for both text and chat templates
    - Seamless integration with Haive's engine composition system

Example:
    Basic usage with a simple text template:

    ```python
    from langchain_core.prompts import PromptTemplate
    from haive.core.engine.prompt_template import PromptTemplateEngine

    # Create a prompt template
    template = PromptTemplate.from_template(
        "Question: {question}\\nContext: {context}\\nAnswer:"
    )

    # Wrap as an engine
    engine = PromptTemplateEngine(
        name="qa_prompt",
        prompt_template=template
    )

    # Get auto-derived input schema
    schema = engine.derive_input_schema()
    print(schema.model_fields.keys())  # ['question', 'context']

    # Use the engine
    result = engine.invoke({
        "question": "What is Python?",
        "context": "Python is a programming language"
    })
    ```

    Advanced usage with chat templates:

    ```python
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

    # Create a chat template with messages placeholder
    chat_template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant"),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "Question: {question}")
    ])

    # Wrap as an engine
    engine = PromptTemplateEngine(
        name="chat_prompt",
        prompt_template=chat_template
    )

    # Schema includes both 'question' and 'chat_history' fields
    schema = engine.derive_input_schema()

    # Format with messages
    result = engine.invoke({
        "question": "How are you?",
        "chat_history": [...]  # Optional
    })
    ```

Classes:
    PromptTemplateEngine: Main engine class for wrapping prompt templates

Dependencies:
    - langchain_core: For prompt template functionality
    - pydantic: For schema generation and validation
    - haive.core.engine.base: For InvokableEngine base class

Author:
    Haive Core Team

Version:
    1.0.0
"""

from typing import Any, Dict, List, Optional, Type, Union
from uuid import uuid4

from langchain_core.messages import AnyMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    BasePromptTemplate,
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
)
from langchain_core.prompts.base import FormatOutputType
from pydantic import BaseModel, Field, computed_field

from haive.core.engine.base import EngineType, InvokableEngine
from haive.core.schema.schema_composer import SchemaComposer


class PromptTemplateEngine(InvokableEngine[Dict[str, Any], FormatOutputType]):
    """An invokable engine that wraps LangChain prompt templates with automatic schema derivation.

    This engine makes prompt templates first-class citizens in the Haive framework,
    providing automatic input schema generation, robust formatting, and seamless
    integration with the engine composition system.

    The PromptTemplateEngine automatically analyzes prompt templates to extract
    variable information and generates appropriate Pydantic schemas for validation
    and documentation. It supports both simple text templates and complex chat
    templates with message placeholders.

    Attributes:
        engine_type (EngineType): Always set to EngineType.PROMPT
        prompt_template (BasePromptTemplate): The wrapped LangChain prompt template
        custom_input_schema (Optional[Type[BaseModel]]): Optional override for input schema

    Note:
        The output type depends on the prompt template type:
        - ChatPromptTemplate/FewShotChatMessagePromptTemplate -> List[AnyMessage]
        - PromptTemplate/FewShotPromptTemplate -> str

    Examples:
        Basic text template usage:

        ```python
        from langchain_core.prompts import PromptTemplate

        template = PromptTemplate.from_template("Hello {name}, you are {age} years old")
        engine = PromptTemplateEngine(name="greeting", prompt_template=template)

        # Input schema automatically includes 'name' and 'age' fields
        result = engine.invoke({"name": "Alice", "age": 30})
        # Returns: "Hello Alice, you are 30 years old"
        ```

        Chat template with message placeholders:

        ```python
        from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

        template = ChatPromptTemplate.from_messages([
            ("system", "You are {role}"),
            MessagesPlaceholder("history", optional=True),
            ("human", "{question}")
        ])

        engine = PromptTemplateEngine(name="chat", prompt_template=template)

        # Schema includes 'role', 'question', and optional 'history'
        result = engine.invoke({
            "role": "a helpful assistant",
            "question": "What is AI?",
            "history": []  # Optional
        })
        # Returns: List[AnyMessage] with formatted messages
        ```

    Raises:
        ValidationError: When input data doesn't match the derived schema
        AttributeError: When prompt template lacks required properties
    """

    engine_type: EngineType = Field(
        default=EngineType.PROMPT, description="Engine type identifier"
    )

    prompt_template: BasePromptTemplate = Field(
        description="The LangChain prompt template to wrap"
    )

    # Optional overrides
    custom_input_schema: Optional[Type[BaseModel]] = Field(
        default=None, description="Custom input schema to use instead of deriving"
    )

    def __init__(self, **data):
        """Initialize the prompt template engine with automatic ID generation.

        Args:
            **data: Keyword arguments for engine initialization. Must include
                'prompt_template'. Other common arguments include 'name', 'description'.

        Note:
            If 'id' is not provided, a UUID4 string will be automatically generated.
        """
        if "id" not in data:
            data["id"] = str(uuid4())
        # Don't override name field - let parent class handle it
        super().__init__(**data)

    def derive_input_schema(self) -> Type[BaseModel]:
        """Derive input schema from prompt template variables with intelligent type inference.

        This method analyzes the prompt template to extract all input variables and
        generates a Pydantic BaseModel schema with appropriate field types. It uses
        both LangChain's built-in variable detection and enhanced regex parsing to
        identify variables in message content.

        Returns:
            Type[BaseModel]: A Pydantic model class with fields corresponding to
                the prompt template's input variables. Field types are inferred
                based on variable name patterns (e.g., 'messages' -> List[AnyMessage]).

        Note:
            If custom_input_schema is provided, it takes precedence over automatic
            derivation. Optional variables (from MessagesPlaceholder with optional=True)
            are marked as optional fields with appropriate defaults.

        Examples:
            For a simple template "Hello {name}, you are {age}":
            - Creates schema with 'name': str and 'age': str fields

            For a chat template with MessagesPlaceholder:
            - Creates schema with required prompt variables and optional message fields
        """
        if self.custom_input_schema:
            return self.custom_input_schema

        # Use langchain's built-in variable detection
        input_vars = set(self.prompt_template.input_variables or [])
        partial_vars = set(
            self.prompt_template.partial_variables.keys()
            if self.prompt_template.partial_variables
            else []
        )

        # Get optional variables (available in ChatPromptTemplate)
        optional_vars = set()
        if (
            hasattr(self.prompt_template, "optional_variables")
            and self.prompt_template.optional_variables
        ):
            optional_vars.update(self.prompt_template.optional_variables)

        # For chat prompts, inspect messages for placeholders and extract variables
        if isinstance(self.prompt_template, ChatPromptTemplate):
            import re

            for msg in self.prompt_template.messages:
                if isinstance(msg, MessagesPlaceholder):
                    var_name = msg.variable_name
                    if msg.optional:
                        optional_vars.add(var_name)
                    else:
                        input_vars.add(var_name)
                # Extract variables from message content using regex
                elif hasattr(msg, "content") and isinstance(msg.content, str):
                    # Find all {variable} patterns in message content
                    variables = re.findall(r"\{([^}]+)\}", msg.content)
                    for var in variables:
                        # Clean variable name (remove format specifiers)
                        clean_var = var.split(":")[0].split("!")[0].strip()
                        if clean_var and clean_var not in partial_vars:
                            input_vars.add(clean_var)

        # Remove partial variables from required inputs (they're already filled)
        input_vars = input_vars - partial_vars

        # Build schema fields with type inference
        fields = {}

        # Add required fields with smart type detection
        for var in input_vars:
            if var not in optional_vars:
                field_type, description = self._infer_field_type(var)
                fields[var] = (field_type, Field(description=description))

        # Add optional fields
        for var in optional_vars:
            field_type, description = self._infer_field_type(var, optional=True)
            fields[var] = (
                field_type,
                Field(default=None, description=f"Optional: {description}"),
            )

        # Create schema class using pydantic create_model
        from pydantic import create_model

        schema_name = f"{self.name.title().replace('_', '')}Input"
        return create_model(schema_name, **fields)

    def _infer_field_type(self, var_name: str, optional: bool = False):
        """Infer the field type and description based on variable name patterns."""
        var_lower = var_name.lower()

        # Message-type variables
        if "message" in var_lower or var_name in [
            "messages",
            "chat_history",
            "conversation",
        ]:
            base_type = List[AnyMessage]
            description = f"Chat messages for {var_name}"

        # List-type variables
        elif any(
            pattern in var_lower
            for pattern in ["list", "items", "examples", "docs", "documents"]
        ):
            base_type = List[str]
            description = f"List of items for {var_name}"

        # Common specific types
        elif var_name in ["context", "background", "instructions", "system_prompt"]:
            base_type = str
            description = f"Context or instructions for {var_name}"

        elif var_name in ["question", "query", "input", "prompt", "request"]:
            base_type = str
            description = f"User input for {var_name}"

        # Default to string
        else:
            base_type = str
            description = f"Input value for {var_name}"

        # Wrap in Optional if needed
        if optional:
            return Optional[base_type], description
        else:
            return base_type, description

    def derive_output_schema(self) -> Type[BaseModel]:
        """Derive output schema based on prompt template type."""
        # Determine output type based on prompt template
        if isinstance(
            self.prompt_template, (ChatPromptTemplate, FewShotChatMessagePromptTemplate)
        ):
            output_type = List[AnyMessage]
            field_name = "messages"
            description = "Formatted chat messages"
        else:
            output_type = str
            field_name = "text"
            description = "Formatted prompt text"

        # Create output schema
        schema_name = f"{self.name.title().replace('_', '')}Output"
        return SchemaComposer.create_schema(
            schema_name,
            {field_name: (output_type, Field(description=description))},
            description=f"Output schema for {self.name} prompt template",
        )

    def invoke(
        self, input_data: Dict[str, Any], config: Optional[Dict[str, Any]] = None
    ) -> Union[str, List[AnyMessage]]:
        """Format the prompt template with input data using langchain's robust formatting."""
        # Validate input against schema
        input_schema = self.derive_input_schema()
        validated_input = input_schema(**input_data)

        # Convert to dict, handling special message fields properly
        input_dict = self._prepare_input_dict(validated_input.model_dump())

        try:
            # Use langchain's format_prompt for most robust handling
            prompt_value = self.prompt_template.format_prompt(**input_dict)

            # Convert PromptValue to appropriate output format
            if isinstance(
                self.prompt_template,
                (ChatPromptTemplate, FewShotChatMessagePromptTemplate),
            ):
                # Return as messages for chat templates
                result = prompt_value.to_messages()
            else:
                # Return as string for text templates
                result = prompt_value.to_string()

        except Exception as e:
            # Fallback to direct formatting if PromptValue fails
            if isinstance(
                self.prompt_template,
                (ChatPromptTemplate, FewShotChatMessagePromptTemplate),
            ):
                result = self.prompt_template.format_messages(**input_dict)
            else:
                result = self.prompt_template.format(**input_dict)

        # Track the invocation if tracking is enabled
        if hasattr(self, "_track_invocation"):
            self._track_invocation(input_dict, result)

        return result

    def _prepare_input_dict(self, input_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare input dictionary, handling special cases like message serialization."""
        prepared = {}

        for key, value in input_dict.items():
            if value is None:
                # Skip None values for optional variables
                continue

            # Handle message lists - ensure they're properly formatted
            if isinstance(value, list) and value and hasattr(value[0], "__class__"):
                if "Message" in value[0].__class__.__name__:
                    # Already proper message objects
                    prepared[key] = value
                else:
                    # Convert if needed (shouldn't normally happen with our schema)
                    prepared[key] = value
            else:
                prepared[key] = value

        return prepared

    async def ainvoke(
        self, input_data: Dict[str, Any], config: Optional[Dict[str, Any]] = None
    ) -> Union[str, List[AnyMessage]]:
        """Async format the prompt template with input data."""
        # For now, prompt formatting is synchronous
        return self.invoke(input_data, config)

    def get_input_fields(self) -> Dict[str, Any]:
        """Get input fields for this engine."""
        schema = self.derive_input_schema()
        if schema:
            fields = {}
            for name, field_info in schema.model_fields.items():
                fields[name] = (field_info.annotation, field_info.default)
            return fields
        return {}

    def get_output_fields(self) -> Dict[str, Any]:
        """Get output fields for this engine."""
        schema = self.derive_output_schema()
        if schema:
            fields = {}
            for name, field_info in schema.model_fields.items():
                fields[name] = (field_info.annotation, field_info.default)
            return fields
        return {"formatted_output": (Union[str, List[AnyMessage]], None)}

    def create_runnable(self, config: Optional[Dict[str, Any]] = None):
        """Create a runnable from this engine."""
        # The prompt template itself is already a runnable
        return self.prompt_template

    def to_runnable(self):
        """Convert to a LangChain runnable."""
        # The prompt template itself is already a runnable
        return self.prompt_template

    @classmethod
    def from_template(
        cls, template: Union[str, BasePromptTemplate], **kwargs
    ) -> "PromptTemplateEngine":
        """Create from a template string or prompt template."""
        if isinstance(template, str):
            prompt = PromptTemplate.from_template(template)
        else:
            prompt = template

        return cls(prompt_template=prompt, **kwargs)

    @classmethod
    def from_messages(cls, messages: List[Any], **kwargs) -> "PromptTemplateEngine":
        """Create from chat messages."""
        prompt = ChatPromptTemplate.from_messages(messages)
        return cls(prompt_template=prompt, **kwargs)
