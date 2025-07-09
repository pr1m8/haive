from typing import Any, Optional, TypeVar, Union

# from langchain_core.output_parsers
from pydantic import BaseModel, Field

from haive.core.engine.output_parser.types import OutputParserType

# class OutputParsingInputSchema(BaseModel):
"""
Output parser engine for the Haive framework.

This module provides an engine implementation for LangChain output parsers,
allowing them to be used consistently within the Haive framework's engine system.
"""

import inspect
import logging
import uuid
from datetime import datetime
from enum import Enum
from typing import (
    Dict,
    List,
    Type,
)

from langchain_core.messages import BaseMessage
from langchain_core.runnables import RunnableConfig

from haive.core.engine.base import EngineType, InvokableEngine
from haive.core.registry.decorators import register_component

logger = logging.getLogger(__name__)

# Define a bounded type variable for output types
TOut = TypeVar(
    "TOut",
    bound=Union[
        # Primitive types
        bool,
        str,
        int,
        float,
        datetime,
        # Collection types
        List[Any],
        Dict[str, Any],
        List[Dict[str, Any]],
        # Pydantic models (handled specially)
        BaseModel,
        # Any for truly custom parsers
        Any,
    ],
)

# Input can be string, message, or collection
TIn = TypeVar("TIn", bound=Union[str, BaseMessage, List[BaseMessage], Dict[str, Any]])


@register_component(registry_getter="engine_registry", component_type=EngineType.TOOL)
class OutputParserEngine(InvokableEngine[TIn, TOut]):
    """
    Engine that wraps LangChain OutputParsers to convert text to structured data.

    The generic parameter TOut represents the specific return type of the parser.
    This allows for type-safe usage of parsers in your workflows.

    Supported output types include:
    - Primitive types (bool, str, int, float, datetime)
    - Collection types (List[str], Dict[str, Any], etc.)
    - Pydantic models (any BaseModel subclass)
    - Specialized types (pandas.DataFrame, Enum values)
    - Custom structured types

    Example:
        ```python
        # Create a JSON parser
        json_parser = create_output_parser_engine(
            OutputParserType.JSON,
            name="my_json_parser"
        )

        # Use in a graph
        graph.add_node("parse_json", json_parser)
        ```
    """

    engine_type: EngineType = Field(default=EngineType.OUTPUT_PARSER)

    # Parser configuration
    parser_type: OutputParserType = Field(
        description="Type of parser to use (from OutputParserType enum)"
    )

    parser_config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional configuration parameters for the parser",
    )

    # Special configuration fields for specific parsers
    pydantic_model: Optional[Type[BaseModel]] = Field(
        default=None,
        description="Pydantic model for PydanticOutputParser",
        exclude=True,  # Exclude from serialization
    )

    regex_pattern: Optional[str] = Field(
        default=None, description="Regex pattern for RegexParser"
    )

    enum_class: Optional[Type[Enum]] = Field(
        default=None, description="Enum class for EnumOutputParser", exclude=True
    )

    response_schemas: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Response schemas for StructuredOutputParser"
    )

    def get_input_fields(self) -> Dict[str, tuple]:
        """Define input field requirements."""
        return {
            "input": (
                Union[str, BaseMessage, List[BaseMessage], Dict[str, Any]],
                Field(
                    description="Text, message, or dictionary to parse into structured data"
                ),
            )
        }

    def get_output_fields(self) -> Dict[str, tuple]:
        """Define output field requirements based on parser type."""
        if self.parser_type == OutputParserType.BOOLEAN:
            return {"result": (bool, Field(description="Parsed boolean result"))}

        elif self.parser_type in [
            OutputParserType.LIST,
            OutputParserType.COMMA_SEPARATED_LIST,
            OutputParserType.NUMBERED_LIST,
            OutputParserType.MARKDOWN_LIST,
        ]:
            return {
                "result": (
                    List[str],
                    Field(default_factory=list, description="Parsed list result"),
                )
            }

        elif self.parser_type == OutputParserType.DATETIME:
            return {"result": (datetime, Field(description="Parsed datetime result"))}

        elif self.parser_type in [
            OutputParserType.JSON,
            OutputParserType.SIMPLE_JSON,
            OutputParserType.COMBINING,
            OutputParserType.REGEX_DICT,
            OutputParserType.XML,
            OutputParserType.YAML,
        ]:
            return {
                "result": (
                    Dict[str, Any],
                    Field(default_factory=dict, description="Parsed dictionary result"),
                )
            }

        elif self.parser_type == OutputParserType.PYDANTIC and self.pydantic_model:
            return {
                "result": (
                    self.pydantic_model,
                    Field(description="Parsed Pydantic model"),
                )
            }

        elif self.parser_type == OutputParserType.STRING:
            return {"result": (str, Field(description="Parsed string result"))}

        elif self.parser_type == OutputParserType.PANDAS_DATAFRAME:
            # Using Any here since we can't import pandas directly in the type hint
            return {"result": (Any, Field(description="Parsed pandas DataFrame"))}

        elif self.parser_type == OutputParserType.ENUM and self.enum_class:
            return {"result": (self.enum_class, Field(description="Parsed enum value"))}

        elif self.parser_type in [
            OutputParserType.OPENAI_TOOLS,
            OutputParserType.OPENAI_TOOLS_KEY,
            OutputParserType.PYDANTIC_TOOLS,
        ]:
            return {"result": (Any, Field(description="Parsed tool output"))}

        # Default for unknown types
        return {"result": (Any, Field(description="Parsed result"))}

    def create_runnable(self, runnable_config: Optional[RunnableConfig] = None) -> Any:
        """
        Create the appropriate parser based on configuration.

        Args:
            runnable_config: Optional runtime configuration

        Returns:
            An instantiated output parser

        Raises:
            ValueError: If parser type is unknown or required config is missing
            ImportError: If required packages are not installed
        """
        params = self.apply_runnable_config(runnable_config) or {}
        config = {**self.parser_config, **params}

        # Common module prefixes
        MODULES = {
            "core": "langchain_core.output_parsers",
            "langchain": "langchain.output_parsers",
            "openai_tools": "langchain_core.output_parsers.openai_tools",
        }

        # General parser configuration with more concise format
        # Format: parser_type: (module_key, class_name_override, config_handler)
        # If class_name_override is None, derive from enum value
        # If config_handler is None, just pass filtered kwargs
        PARSER_MAP = {
            # Core simple parsers
            OutputParserType.LIST: ("core", None, None),
            OutputParserType.COMMA_SEPARATED_LIST: ("core", None, None),
            OutputParserType.NUMBERED_LIST: ("core", None, None),
            OutputParserType.MARKDOWN_LIST: ("core", None, None),
            OutputParserType.STRING: ("core", "StrOutputParser", None),
            OutputParserType.JSON: (
                "core",
                None,
                lambda s, c: {"schema": c.get("schema")},
            ),
            OutputParserType.SIMPLE_JSON: ("core", None, None),
            OutputParserType.XML: ("core", None, None),
            OutputParserType.PYDANTIC: (
                "core",
                None,
                lambda s, c: {"pydantic_object": s.pydantic_model},
            ),
            # LangChain extension parsers
            OutputParserType.BOOLEAN: ("langchain", None, None),
            OutputParserType.DATETIME: ("langchain", None, None),
            OutputParserType.COMBINING: (
                "langchain",
                None,
                lambda s, c: {"parsers": c.get("parsers", [])},
            ),
            OutputParserType.REGEX: (
                "langchain",
                None,
                lambda s, c: {
                    "regex_pattern": s.regex_pattern,
                    "output_keys": c.get("output_keys", []),
                },
            ),
            OutputParserType.REGEX_DICT: (
                "langchain",
                None,
                lambda s, c: {"regex_patterns": c.get("regex_patterns", {})},
            ),
            OutputParserType.PANDAS_DATAFRAME: ("langchain", None, None),
            OutputParserType.YAML: ("langchain", None, None),
            OutputParserType.ENUM: (
                "langchain",
                None,
                lambda s, c: {"enum": s.enum_class},
            ),
            # OpenAI tools parsers
            OutputParserType.OPENAI_TOOLS: (
                "openai_tools",
                "JsonOutputToolsParser",
                lambda s, c: {"schema": c.get("schema")},
            ),
            OutputParserType.OPENAI_TOOLS_KEY: (
                "openai_tools",
                "JsonOutputKeyToolsParser",
                lambda s, c: {"schema": c.get("schema"), "key": c.get("key")},
            ),
            OutputParserType.PYDANTIC_TOOLS: (
                "openai_tools",
                "PydanticToolsParser",
                lambda s, c: {"pydantic_schemas": c.get("pydantic_schemas", [])},
            ),
        }

        # Special case handlers - for parsers that need custom instantiation
        SPECIAL_HANDLERS = {
            OutputParserType.STRUCTURED: lambda s, c: self._create_structured_parser(
                s.response_schemas
            )
        }

        # Required attributes and parameters validation
        REQUIRED_ATTRS = {
            OutputParserType.PYDANTIC: ["pydantic_model"],
            OutputParserType.REGEX: ["regex_pattern"],
            OutputParserType.ENUM: ["enum_class"],
            OutputParserType.STRUCTURED: ["response_schemas"],
        }

        REQUIRED_PARAMS = {
            OutputParserType.COMBINING: ["parsers"],
            OutputParserType.REGEX: ["output_keys"],
            OutputParserType.REGEX_DICT: ["regex_patterns"],
            OutputParserType.OPENAI_TOOLS: ["schema"],
            OutputParserType.OPENAI_TOOLS_KEY: ["schema", "key"],
            OutputParserType.PYDANTIC_TOOLS: ["pydantic_schemas"],
        }

        try:
            # Check for special case handlers first
            if self.parser_type in SPECIAL_HANDLERS:
                return SPECIAL_HANDLERS[self.parser_type](self, config)

            # Check if we have a configuration for this parser type
            if self.parser_type not in PARSER_MAP:
                raise ValueError(f"Unknown parser type: {self.parser_type}")

            module_key, class_override, config_handler = PARSER_MAP[self.parser_type]

            # Get the module path
            if module_key not in MODULES:
                raise ValueError(f"Unknown module key: {module_key}")
            module_path = MODULES[module_key]

            # Determine class name
            if class_override:
                class_name = class_override
            else:
                # Convert enum value to CamelCase and append OutputParser
                parts = self.parser_type.value.split("_")
                class_name = "".join(p.capitalize() for p in parts) + "OutputParser"

            # Validate required attributes
            if self.parser_type in REQUIRED_ATTRS:
                for attr in REQUIRED_ATTRS[self.parser_type]:
                    if getattr(self, attr, None) is None:
                        raise ValueError(
                            f"{self.parser_type} requires {attr} to be set"
                        )

            # Validate required parameters
            if self.parser_type in REQUIRED_PARAMS:
                for param in REQUIRED_PARAMS[self.parser_type]:
                    if param not in config:
                        raise ValueError(
                            f"{self.parser_type} requires '{param}' in configuration"
                        )

            # Import the parser class
            parser_class = self._import_class(module_path, class_name)

            # Determine parameters
            if config_handler:
                params = config_handler(self, config)
            else:
                params = self._filter_kwargs_for_class(parser_class, config)

            # Create and return instance
            return parser_class(**params)

        except ImportError as e:
            logger.error(f"Failed to import parser for {self.parser_type}: {str(e)}")
            raise ImportError(
                f"Required package for {self.parser_type} parser not installed: {str(e)}"
            )

    def invoke(
        self, input_data: TIn, runnable_config: Optional[RunnableConfig] = None
    ) -> TOut:
        """
        Invoke the parser with the input data.

        Args:
            input_data: Input text, message, or dictionary
            runnable_config: Optional runtime configuration

        Returns:
            Parsed output based on parser type

        Raises:
            ValueError: If the input cannot be processed
            Exception: If parsing fails and no error handler is provided
        """
        # Create the parser
        parser = self.create_runnable(runnable_config)

        # Extract text from various input types
        text = self._extract_text(input_data)

        # Parse the text
        try:
            if (
                hasattr(parser, "parse_with_prompt")
                and runnable_config
                and "prompt" in runnable_config.get("configurable", {})
            ):
                # If we have a prompt in the config and the parser supports it
                prompt = runnable_config["configurable"]["prompt"]
                return parser.parse_with_prompt(text, prompt)
            # Otherwise, use regular parse
            return parser.parse(text)
        except Exception as e:
            # Handle parsing errors
            logger.error(f"Error parsing with {self.parser_type}: {str(e)}")
            if "error_handler" in self.parser_config:
                error_handler = self.parser_config["error_handler"]
                return error_handler(text, e)
            # Re-raise if no error handler
            raise

    async def ainvoke(
        self, input_data: TIn, runnable_config: Optional[RunnableConfig] = None
    ) -> TOut:
        """
        Asynchronously invoke the parser with the input data.

        Args:
            input_data: Input text, message, or dictionary
            runnable_config: Optional runtime configuration

        Returns:
            Parsed output based on parser type
        """
        # Create the parser
        parser = self.create_runnable(runnable_config)

        # Extract text
        text = self._extract_text(input_data)

        # Parse asynchronously if supported
        try:
            if (
                hasattr(parser, "aparse_with_prompt")
                and runnable_config
                and "prompt" in runnable_config.get("configurable", {})
            ):
                prompt = runnable_config["configurable"]["prompt"]
                return await parser.aparse_with_prompt(text, prompt)
            elif hasattr(parser, "aparse"):
                return await parser.aparse(text)
            else:
                # Fall back to synchronous parsing in an async context
                import asyncio

                return await asyncio.to_thread(parser.parse, text)
        except Exception as e:
            logger.error(
                f"Error parsing asynchronously with {self.parser_type}: {str(e)}"
            )
            if "error_handler" in self.parser_config:
                error_handler = self.parser_config["error_handler"]
                return await asyncio.to_thread(error_handler, text, e)
            raise

    def _extract_text(self, input_data: TIn) -> str:
        """
        Extract text content from various input types.

        Args:
            input_data: Input data in various formats

        Returns:
            Extracted text string

        Raises:
            ValueError: If text cannot be extracted
        """
        if isinstance(input_data, str):
            # If input is already a string, use it directly
            return input_data

        elif hasattr(input_data, "content") and isinstance(input_data.content, str):
            # If input is a message with text content, extract it
            return input_data.content

        elif isinstance(input_data, list) and all(
            hasattr(m, "content") for m in input_data
        ):
            # If input is a list of messages, concatenate their contents
            return "\n".join(
                m.content for m in input_data if isinstance(m.content, str)
            )

        elif isinstance(input_data, dict):
            # Try to extract text from dictionary
            if "text" in input_data:
                return str(input_data["text"])
            elif "content" in input_data:
                return str(input_data["content"])
            elif "input" in input_data:
                return str(input_data["input"])

        # Try to convert to string as a fallback
        try:
            return str(input_data)
        except Exception as e:
            raise ValueError(f"Cannot extract text from input: {str(e)}")

    def _import_class(self, module_path: str, class_name: str) -> Type:
        """Dynamically import a class."""
        import importlib

        module = importlib.import_module(module_path)
        return getattr(module, class_name)

    def _filter_kwargs_for_class(
        self, cls: Type, kwargs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Filter kwargs to only include those accepted by the class's __init__."""
        if not hasattr(cls, "__init__"):
            return {}

        # Get the signature of the class's __init__ method
        sig = inspect.signature(cls.__init__)
        # Get parameter names, excluding 'self'
        valid_params = [param for param in sig.parameters if param != "self"]

        # Return only the kwargs that are valid parameters
        return {k: v for k, v in kwargs.items() if k in valid_params}

    def _create_structured_parser(self, schemas: List[Dict[str, Any]]) -> Any:
        """Create a StructuredOutputParser instance."""
        from langchain.output_parsers import ResponseSchema, StructuredOutputParser

        response_schemas = [ResponseSchema(**schema) for schema in schemas]
        return StructuredOutputParser.from_response_schemas(response_schemas)


def create_output_parser_engine(
    parser_type: Union[str, OutputParserType], name: Optional[str] = None, **kwargs
) -> OutputParserEngine:
    """
    Factory function to create an OutputParserEngine.

    Args:
        parser_type: Type of parser (from OutputParserType enum or string)
        name: Optional name for the engine
        **kwargs: Additional configuration parameters

    Returns:
        Configured OutputParserEngine
    """
    # Convert string to enum if needed
    if isinstance(parser_type, str):
        try:
            parser_type = OutputParserType(parser_type)
        except ValueError:
            raise ValueError(f"Unknown parser type: {parser_type}")

    if name is None:
        name = f"{parser_type.value}_parser_{uuid.uuid4().hex[:6]}"

    # Extract special parameters
    parser_config = {
        k: v
        for k, v in kwargs.items()
        if k
        not in ["pydantic_model", "regex_pattern", "enum_class", "response_schemas"]
    }

    return OutputParserEngine(
        name=name,
        parser_type=parser_type,
        parser_config=parser_config,
        pydantic_model=kwargs.get("pydantic_model"),
        regex_pattern=kwargs.get("regex_pattern"),
        enum_class=kwargs.get("enum_class"),
        response_schemas=kwargs.get("response_schemas"),
    )


# Convenience functions for common parser types
def create_str_parser(name: Optional[str] = None, **kwargs) -> OutputParserEngine:
    """Create a StrOutputParser engine."""
    return create_output_parser_engine(OutputParserType.STRING, name, **kwargs)


def create_list_parser(
    list_type: str = "list", name: Optional[str] = None, **kwargs
) -> OutputParserEngine:
    """
    Create a list parser engine.

    Args:
        list_type: Type of list parser ('list', 'comma_separated', 'numbered', 'markdown')
        name: Optional name for the engine
        **kwargs: Additional configuration

    Returns:
        List parser engine
    """
    type_map = {
        "list": OutputParserType.LIST,
        "comma_separated": OutputParserType.COMMA_SEPARATED_LIST,
        "numbered": OutputParserType.NUMBERED_LIST,
        "markdown": OutputParserType.MARKDOWN_LIST,
    }

    if list_type not in type_map:
        raise ValueError(
            f"Unknown list type: {list_type}. Must be one of {list(type_map.keys())}"
        )

    return create_output_parser_engine(type_map[list_type], name, **kwargs)


def create_json_parser(
    name: Optional[str] = None, schema: Optional[Dict] = None, **kwargs
) -> OutputParserEngine:
    """Create a JsonOutputParser engine."""
    if schema:
        kwargs["schema"] = schema
    return create_output_parser_engine(OutputParserType.JSON, name, **kwargs)


def create_pydantic_parser(
    pydantic_model: Type[BaseModel], name: Optional[str] = None, **kwargs
) -> OutputParserEngine:
    """Create a PydanticOutputParser engine."""
    return create_output_parser_engine(
        OutputParserType.PYDANTIC, name, pydantic_model=pydantic_model, **kwargs
    )


def create_structured_parser(
    response_schemas: List[Dict[str, Any]], name: Optional[str] = None, **kwargs
) -> OutputParserEngine:
    """Create a StructuredOutputParser engine."""
    return create_output_parser_engine(
        OutputParserType.STRUCTURED, name, response_schemas=response_schemas, **kwargs
    )


def create_regex_parser(
    regex_pattern: str, output_keys: List[str], name: Optional[str] = None, **kwargs
) -> OutputParserEngine:
    """Create a RegexParser engine."""
    return create_output_parser_engine(
        OutputParserType.REGEX,
        name,
        regex_pattern=regex_pattern,
        output_keys=output_keys,
        **kwargs,
    )


def create_enum_parser(
    enum_class: Type[Enum], name: Optional[str] = None, **kwargs
) -> OutputParserEngine:
    """Create an EnumOutputParser engine."""
    return create_output_parser_engine(
        OutputParserType.ENUM, name, enum_class=enum_class, **kwargs
    )
