"""AugLLM configuration system for enhanced LLM chains.

This module provides a comprehensive configuration system for creating and
managing enhanced LLM chains within the Haive framework. The AugLLMConfig class
serves as a central configuration point that integrates prompts, tools, output
parsers, and structured output models with extensive validation and debugging
capabilities.

Key features:
- Flexible prompt template creation and management with support for few-shot learning
- Comprehensive tool integration with automatic discovery and configuration
- Structured output handling via two approaches (v1: parser-based, v2: tool-based)
- Rich debugging and validation to ensure proper configuration
- Pre/post processing hooks for customizing input and output
- Support for both synchronous and asynchronous execution

The configuration system is designed to be highly customizable while providing
sensible defaults and automatic detection of configuration requirements.
"""

from __future__ import annotations

import json
import logging
import os
import uuid
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    Union,
    cast,
)

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import (
    BaseOutputParser,
    PydanticOutputParser,
    StrOutputParser,
)
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.prompts import (
    BasePromptTemplate,
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
)
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.tools import BaseTool, StructuredTool
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PrivateAttr,
    field_validator,
    model_validator,
)
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree

from haive.core.common.mixins.structured_output_mixin import StructuredOutputMixin
from haive.core.common.mixins.tool_route_mixin import ToolRouteMixin
from haive.core.engine.base import EngineType, InvokableEngine
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig

logger = logging.getLogger(__name__)
console = Console()
logger.setLevel(logging.WARNING)

# Create a module-level flag to control debug output
DEBUG_OUTPUT = os.getenv("HAIVE_DEBUG_CONFIG", "FALSE").lower() in ("true", "1", "yes")


def debug_print(*args, **kwargs):
    """Print debug output only if DEBUG_OUTPUT is enabled."""
    if DEBUG_OUTPUT:
        # Use rich print if available, otherwise regular print
        try:
            from rich import print as rprint

            rprint(*args, **kwargs)  # Changed from debug_print to rprint
        except ImportError:
            pass
    elif args:
        logger.debug(" ".join(str(arg) for arg in args))


# Literal types for better type safety
ParserType = Literal["pydantic", "pydantic_tools", "str", "json", "custom"]
StructuredOutputVersion = Literal["v1", "v2"]
ToolChoiceMode = Literal["auto", "required", "optional", "none"]


class AugLLMConfig(
    ToolRouteMixin,
    StructuredOutputMixin,
    InvokableEngine[
        Union[str, dict[str, Any], list[BaseMessage]],
        Union[BaseMessage, dict[str, Any]],
    ],
):
    """Configuration for creating enhanced LLM chains with flexible message handling.

    AugLLMConfig provides a structured way to configure and create LLM chains
    with prompts, tools, output parsers, and structured output models with
    comprehensive validation and automatic updates. It serves as the central
    configuration class for language model interactions in the Haive framework.

    This class integrates several key functionalities:
    1. Prompt template management with support for few-shot learning
    2. Tool integration and discovery with automatic routing
    3. Structured output handling (both parser-based and tool-based approaches)
    4. Message handling for chat-based LLMs
    5. Pre/post processing hooks for customization

    The configuration system is designed to be highly flexible while enforcing
    consistent patterns and proper validation, making it easier to create reliable
    language model interactions.

    Attributes:
        engine_type (EngineType): The type of engine (always LLM).
        llm_config (LLMConfig): Configuration for the LLM provider.
        prompt_template (Optional[BasePromptTemplate]): Template for structuring prompts.
        system_message (Optional[str]): System message for chat models.
        tools (Sequence[Union[Type[BaseTool], Type[BaseModel], Callable, StructuredTool, BaseModel]]):
            Tools that can be bound to the LLM.
        structured_output_model (Optional[Type[BaseModel]]): Pydantic model for structured outputs.
        structured_output_version (Optional[StructuredOutputVersion]):
            Version of structured output handling (v1: parser-based, v2: tool-based).
        temperature (Optional[float]): Temperature parameter for the LLM.
        max_tokens (Optional[int]): Maximum number of tokens to generate.
        preprocess (Optional[Callable]): Function to preprocess input before sending to LLM.
        postprocess (Optional[Callable]): Function to postprocess output from LLM.

    Examples:
        >>> from haive.core.engine.aug_llm.config import AugLLMConfig
        >>> from haive.core.models.llm.base import AzureLLMConfig
        >>> from pydantic import BaseModel, Field
        >>>
        >>> # Define a structured output model
        >>> class MovieReview(BaseModel):
        ...     title: str = Field(description="Title of the movie")
        ...     rating: int = Field(description="Rating from 1-10")
        ...     review: str = Field(description="Detailed review of the movie")
        >>>
        >>> # Create a basic configuration
        >>> config = AugLLMConfig(
        ...     name="movie_reviewer",
        ...     llm_config=AzureLLMConfig(model="gpt-4"),
        ...     system_message="You are a professional movie critic.",
        ...     structured_output_model=MovieReview,
        ...     temperature=0.7
        ... )
        >>>
        >>> # Create a runnable from the configuration
        >>> reviewer = config.create_runnable()
        >>>
        >>> # Use the runnable
        >>> result = reviewer.invoke("Review the movie 'Inception'")
    """

    engine_type: EngineType = Field(
        default=EngineType.LLM, description="The type of engine"
    )

    # Core LLM configuration
    llm_config: LLMConfig = Field(
        default_factory=lambda: AzureLLMConfig(model="gpt-4o"),
        description="LLM provider configuration",
    )

    # Prompt components
    prompt_template: BasePromptTemplate | None = Field(
        default=None, description="Prompt template for the LLM"
    )
    system_message: str | None = Field(
        default=None, description="System message for chat models"
    )

    # Message placeholder configuration
    messages_placeholder_name: str = Field(
        default="messages",
        description="Name of the messages placeholder in chat templates",
    )
    add_messages_placeholder: bool = Field(
        default=True, description="Whether to automatically add MessagesPlaceholder"
    )
    force_messages_optional: bool = Field(
        default=True, description="Force messages placeholder to be optional"
    )

    # Few-shot components
    examples: List[Dict[str, Any]] | None = Field(
        default=None, description="Examples for few-shot prompting"
    )
    example_prompt: PromptTemplate | None = Field(
        default=None, description="Template for formatting few-shot examples"
    )
    prefix: str | None = Field(
        default=None, description="Text before examples in few-shot prompting"
    )
    suffix: str | None = Field(
        default=None, description="Text after examples in few-shot prompting"
    )
    example_separator: str = Field(
        default="\n\n", description="Separator between examples in few-shot prompting"
    )
    input_variables: List[str] | None = Field(
        default=None, description="Input variables for the prompt template"
    )

    # Tools are inherited from ToolRouteMixin - no need to redefine
    # When tools are passed to AugLLMConfig, they'll be stored in the mixin

    # Tool routes (provided by ToolRouteMixin)
    schemas: Sequence[
        Type[BaseTool] | Type[BaseModel] | Callable | StructuredTool | BaseModel
    ] = Field(default_factory=list, description="Schemas for tools")
    pydantic_tools: list[type[BaseModel]] = Field(
        default_factory=list, description="Pydantic models for tool schemas"
    )

    # Flags for format instructions from tools
    use_tool_for_format_instructions: bool = Field(
        default=False,
        description="Use a single tool Pydantic model for format instructions",
    )
    tool_is_base_model: bool = Field(
        default=False,
        description="Whether a tool is a BaseModel type (detected automatically)",
    )

    # Tool selection options
    force_tool_use: bool = Field(
        default=False, description="Whether to force the LLM to use a tool (any tool)"
    )
    force_tool_choice: Union[bool, str, List[str]] | None = Field(
        default=None, description="Force specific tool(s) to be used"
    )
    tool_choice_mode: ToolChoiceMode = Field(
        default="auto", description="Tool choice mode to use for binding tools"
    )

    # Output handling
    # TODO: TYPED DICT and DICT, use tool choice mixin.
    # TODO: STructured output model mixin.
    structured_output_model: Type[BaseModel] | None = Field(
        default=None, description="Pydantic model for structured output"
    )
    structured_output_version: StructuredOutputVersion | None = Field(
        default=None,
        description="Version of structured output handling: v1 (traditional), v2 (tool-based), None (disabled)",
    )
    # Use TYPE_CHECKING to avoid runtime type evaluation issues with LangGraph
    if TYPE_CHECKING:
        output_parser: BaseOutputParser | None = Field(
            default=None, description="Parser for LLM output", exclude=True
        )
    else:
        output_parser: Any | None = Field(
            default=None, description="Parser for LLM output", exclude=True
        )
    parse_raw_output: bool = Field(
        default=False,
        description="Force parsing raw output even with structured output model",
    )
    include_format_instructions: bool = Field(
        default=True, description="Whether to include format instructions in the prompt"
    )
    # TODO: WILL FIX
    parser_type: ParserType | None = Field(
        default=None,
        description="Parser type: 'pydantic', 'pydantic_tools', 'str', 'json', or 'custom'",
    )

    # Output field naming
    output_field_name: str | None = Field(
        default=None, description="Custom name for the primary output field in schema"
    )
    output_key: str | None = Field(
        default=None, description="Custom key for output when needed"
    )

    # Tool configuration
    tool_kwargs: dict[str, dict[str, Any]] = Field(
        default_factory=dict, description="Parameters for tool instantiation"
    )
    bind_tools_kwargs: dict[str, Any] = Field(
        default_factory=dict, description="Parameters for binding tools to the LLM"
    )
    bind_tools_config: dict[str, Any] = Field(
        default_factory=dict, description="Configuration for bind_tools"
    )

    # Pre/post processing
    preprocess: Callable[[Any], Any] | None = Field(
        default=None,
        description="Function to preprocess input before sending to LLM",
        exclude=True,  # Exclude from serialization
    )
    postprocess: Callable[[Any], Any] | None = Field(
        default=None,
        description="Function to postprocess output from LLM",
        exclude=True,  # Exclude from serialization
    )

    # Runtime options
    temperature: float | None = Field(
        default=None, description="Temperature parameter for the LLM"
    )
    max_tokens: int | None = Field(
        default=None, description="Maximum number of tokens to generate"
    )
    runtime_options: dict[str, Any] = Field(
        default_factory=dict, description="Additional runtime options for the LLM"
    )

    # Custom runnables to chain
    custom_runnables: List[Runnable] | None = Field(
        default=None,
        description="Custom runnables to add to the chain",
        exclude=True,  # Exclude from serialization
    )

    # Partial variables for templates
    partial_variables: dict[str, Any] = Field(
        default_factory=dict, description="Partial variables for the prompt template"
    )

    # Optional variables for templates
    optional_variables: list[str] = Field(
        default_factory=list, description="Optional variables for the prompt template"
    )

    # Message field detection
    uses_messages_field: bool | None = Field(
        default=None,
        description="Explicitly specify if this engine uses a messages field. If None, auto-detected.",
    )

    # Private attributes for internal state tracking
    _computed_input_fields: dict[str, tuple[type, Any]] = PrivateAttr(
        default_factory=dict
    )
    _computed_output_fields: dict[str, tuple[type, Any]] = PrivateAttr(
        default_factory=dict
    )
    _format_instructions_text: str | None = PrivateAttr(default=None)
    _is_processing_validation: bool = PrivateAttr(default=False)
    _tool_name_mapping: dict[str, str] = PrivateAttr(default_factory=dict)

    model_config = ConfigDict(
        arbitrary_types_allowed=True, validate_assignment=True, extra="forbid"
    )

    def __init__(self, **kwargs):
        """Initialize with comprehensive debug logging."""
        # Set default name if not provided
        if "name" not in kwargs:
            kwargs["name"] = f"aug_llm_{uuid.uuid4().hex[:8]}"

        # Initialize the engine
        super().__init__(**kwargs)

        # Initialize ToolListMixin functionality manually to avoid recursion
        self._initialize_tool_mixin()

        # Show initialization summary
        self._debug_initialization_summary()

    def _initialize_tool_mixin(self):
        """Initialize ToolListMixin functionality manually."""
        # Initialize tool mixin attributes
        if not hasattr(self, "tool_routes"):
            self.tool_routes = {}

        # Process existing tools
        self._sync_tool_routes()

    def _sync_tool_routes(self):
        """Synchronize tool_routes with current tools using mixin functionality."""
        if not self.tools:
            self.clear_tool_routes()
            return

        # Use the mixin's method to sync routes from tools
        self.sync_tool_routes_from_tools(self.tools)

        # Add specific metadata for structured output
        if self.structured_output_model:
            for tool_name, route in self.tool_routes.items():
                if route == "pydantic_model":
                    metadata = self.get_tool_metadata(tool_name) or {}
                    metadata["is_structured_output"] = (
                        tool_name == self.structured_output_model.__name__
                    )
                    self.set_tool_route(tool_name, route, metadata)

    def _debug_initialization_summary(self):
        """Show rich initialization summary."""
        if not DEBUG_OUTPUT:
            return

        tree = Tree("🚀 [bold blue]AugLLMConfig Initialization[/bold blue]")

        # Basic info
        basic = tree.add("📋 [cyan]Basic Configuration[/cyan]")
        basic.add(f"Name: [yellow]{self.name}[/yellow]")
        basic.add(f"ID: [yellow]{self.id}[/yellow]")
        basic.add(f"Engine Type: [yellow]{self.engine_type.value}[/yellow]")

        # LLM config
        llm_info = tree.add("🤖 [cyan]LLM Configuration[/cyan]")
        llm_info.add(f"Provider: [yellow]{type(self.llm_config).__name__}[/yellow]")
        llm_info.add(
            f"Model: [yellow]{getattr(self.llm_config, 'model', 'Unknown')}[/yellow]"
        )

        # Tools info
        tools_info = tree.add("🔧 [cyan]Tools Configuration[/cyan]")
        tools_info.add(f"Total Tools: [yellow]{len(self.tools)}[/yellow]")
        tools_info.add(f"Pydantic Tools: [yellow]{len(self.pydantic_tools)}[/yellow]")
        tools_info.add(f"Tool Routes: [yellow]{len(self.tool_routes)}[/yellow]")

        # Output config
        output_info = tree.add("📤 [cyan]Output Configuration[/cyan]")
        output_info.add(
            f"Structured Output Model: [yellow]{self.structured_output_model.__name__ if self.structured_output_model else 'None'}[/yellow]"
        )
        output_info.add(
            f"Structured Output Version: [yellow]{self.structured_output_version or 'None'}[/yellow]"
        )
        output_info.add(f"Parser Type: [yellow]{self.parser_type or 'None'}[/yellow]")

        console.print(
            Panel(tree, title="Initialization Complete", border_style="green")
        )

    @field_validator("tools")
    @classmethod
    def validate_tools(cls, v):
        """Validate and auto-name tools."""
        if not v:
            return v

        validated_tools = []
        for _i, tool in enumerate(v):
            # Auto-assign name if tool doesn't have one and needs one
            if hasattr(tool, "name") or isinstance(tool, type) or callable(tool):
                validated_tools.append(tool)
            else:
                validated_tools.append(tool)

        return validated_tools

    @field_validator("schemas")
    @classmethod
    def validate_schemas(cls, v):
        """Validate and auto-name schemas."""
        if not v:
            return v
        return v

    @field_validator("structured_output_model")
    @classmethod
    def validate_structured_output_model(cls, v):
        """Validate structured output model and default to tools-based validation."""
        if not v:
            return v

        # Just validate the model itself - version defaulting will be handled in model_validator
        if not issubclass(v, BaseModel):
            raise ValueError("structured_output_model must be a BaseModel subclass")

        return v

    @model_validator(mode="before")
    @classmethod
    def set_default_structured_output_version(cls, data):
        """Set default structured output version to v2 (tools) when model is provided but version is not."""
        if isinstance(data, dict):
            structured_output_model = data.get("structured_output_model")
            structured_output_version = data.get("structured_output_version")

            # If model is provided but no version specified, default to v2 (tool-based)
            if structured_output_model and not structured_output_version:
                data["structured_output_version"] = "v2"

        return data

    @model_validator(mode="before")
    @classmethod
    def ensure_structured_output_as_tool(cls, data):
        """Ensure structured output model is properly configured for both v1 and v2."""
        if isinstance(data, dict):
            structured_output_model = data.get("structured_output_model")
            structured_output_version = data.get("structured_output_version")

            if not structured_output_model:
                return data

            # For BOTH v1 and v2, add the model to tools
            tools = data.get("tools", [])
            if not isinstance(tools, list):
                tools = list(tools) if tools else []

            # Add structured output model to tools if not already there
            if structured_output_model not in tools:
                tools.append(structured_output_model)
                data["tools"] = tools

            # Handle v2-specific settings: tool forcing
            if structured_output_version == "v2":
                # Force tool use settings for v2
                data["force_tool_use"] = True
                data["tool_choice_mode"] = "required"

                # Set force_tool_choice to the model's class name
                # This ensures we use the exact class name for tool forcing
                if hasattr(structured_output_model, "__name__"):
                    data["force_tool_choice"] = structured_output_model.__name__

            # v1 doesn't need force_tool_use - it uses traditional parsing

        return data

    @model_validator(mode="before")
    @classmethod
    def default_schemas_to_tools(cls, data):
        """Default schemas to tools if schemas isn't provided but tools has values."""
        if isinstance(data, dict):
            tools = data.get("tools", [])
            schemas = data.get("schemas", [])

            # If tools exist but schemas is empty, default schemas to tools
            if tools and not schemas:
                data["schemas"] = tools

        return data

    @model_validator(mode="after")
    def comprehensive_validation_and_setup(self):
        """Comprehensive validation and setup after initialization."""
        # Prevent infinite recursion
        if self._is_processing_validation:
            return self

        self._is_processing_validation = True

        try:
            debug_print(
                "🔍 [bold blue]Starting comprehensive validation and setup[/bold blue]"
            )

            # Step 1: Process tools and update tool-related fields
            self._process_and_validate_tools()

            # Step 2: Create prompt template components if needed
            self._create_prompt_template_if_needed()

            # Step 3: Ensure messages placeholder is properly handled
            self._ensure_messages_placeholder_handling()

            # Step 4: Apply partial variables to the prompt template if needed
            self._apply_partial_variables()

            # Step 5: Apply optional variables to the prompt template
            self._apply_optional_variables()

            # Step 6: Set up format instructions (with proper validation)
            self._setup_format_instructions()

            # Step 7: Set up output handling (with proper validation)
            self._setup_output_handling()

            # Step 8: Configure tool choice options
            self._configure_tool_choice()

            # Step 9: Auto-detect uses_messages_field if not explicitly set
            if self.uses_messages_field is None:
                self.uses_messages_field = self._detect_uses_messages_field()

            # Step 10: Compute input and output fields
            self._compute_schema_fields()

            # Step 11: Final validation check
            self._final_validation_check()

            # Step 12: Debug final state
            self._debug_final_configuration()

            debug_print(
                "✅ [bold green]Comprehensive validation and setup complete[/bold green]"
            )

        except Exception as e:
            debug_print(f"❌ [bold red]Error during validation: {e}[/bold red]")
            raise
        finally:
            self._is_processing_validation = False

        return self

    def _analyze_tool(self, tool: Any) -> tuple[str, Dict[str, Any] | None]:
        """Analyze tool with AugLLM-specific context awareness.

        Extends ToolRouteMixin's analysis with structured output detection.
        """
        # Check if this is the structured output model
        if self.structured_output_model and tool == self.structured_output_model:
            route = (
                "structured_output_tool"
                if self.structured_output_version == "v2"
                else "parser"
            )
            metadata = {
                "purpose": "structured_output",
                "version": self.structured_output_version,
                "force_choice": self.structured_output_version == "v2",
                "class_name": tool.__name__ if hasattr(tool, "__name__") else str(tool),
            }
            return route, metadata

        # Use parent implementation for regular tools
        return super()._analyze_tool(tool)

    def _process_and_validate_tools(self):
        """Process tools using unified ToolRouteMixin functionality."""
        debug_print("🔧 [blue]Processing and validating tools...[/blue]")

        if not self.tools:
            # Clear all tool data using mixin method
            self.clear_tools()
            self.pydantic_tools = []
            self.tool_is_base_model = False
            self._tool_name_mapping = {}
            debug_print(
                "📝 [yellow]No tools provided - cleared tool-related fields[/yellow]"
            )
            return

        # Process each tool through the routing system
        basemodel_tools = []
        tool_names = []
        tool_name_mapping = {}

        for i, tool in enumerate(self.tools):
            # Add tool through unified routing system
            # This will analyze the tool and set appropriate route
            self.add_tool(tool)

            # Get the tool name and route that was assigned
            tool_name = self._get_tool_name(tool, i)
            self.tool_routes.get(tool_name, "unknown")
            actual_tool_name = tool_name  # The name that will be used in LLM binding

            # Track BaseModel tools
            if isinstance(tool, type) and issubclass(tool, BaseModel):
                basemodel_tools.append(tool)

                # Add to pydantic_tools if not already there
                if tool not in self.pydantic_tools:
                    self.pydantic_tools.append(tool)
                    debug_print(
                        f"➕ [green]Added BaseModel {tool.__name__} to pydantic_tools[/green]"
                    )

            # Track tool names and mapping
            if tool_name:
                tool_names.append(tool_name)
                # Map display name to actual binding name
                tool_name_mapping[tool_name] = actual_tool_name

        # Store the name mapping
        self._tool_name_mapping = tool_name_mapping

        # Remove tools from pydantic_tools that are no longer in tools
        current_basemodel_tools = set(basemodel_tools)
        self.pydantic_tools = [
            tool for tool in self.pydantic_tools if tool in current_basemodel_tools
        ]

        # Set flag if BaseModel tools are found
        self.tool_is_base_model = len(basemodel_tools) > 0

        # Store discovered tool names for later validation
        if not hasattr(self, "metadata"):
            self.metadata = {}
        self.metadata["tool_names"] = tool_names
        self.metadata["has_basemodel_tools"] = bool(basemodel_tools)
        self.metadata["basemodel_tool_count"] = len(basemodel_tools)
        self.metadata["tool_name_mapping"] = tool_name_mapping

        debug_print(
            f"📊 [cyan]Tool processing complete: {len(tool_names)} tools, {len(basemodel_tools)} BaseModel tools[/cyan]"
        )

    def _setup_format_instructions(self):
        """Set up format instructions with proper validation - for both v1 and v2."""
        debug_print("📝 [blue]Setting up format instructions...[/blue]")

        # Clear existing format instructions
        if "format_instructions" in self.partial_variables:
            del self.partial_variables["format_instructions"]
            self._format_instructions_text = None

        # Only set up format instructions if conditions are met
        should_setup = self._should_setup_format_instructions()

        if not should_setup:
            debug_print(
                "🚫 [yellow]Format instructions not needed - conditions not met[/yellow]"
            )
            return

        try:
            debug_print(
                f"📋 [green]Setting up format instructions for: {self.structured_output_model.__name__}[/green]"
            )

            # ✅ Use PydanticOutputParser ONLY for format instructions
            # This is correct for both v1 and v2:
            # - v1: Uses format instructions + parser
            # - v2: Uses format instructions + tool forcing (NO parser)
            parser = PydanticOutputParser(pydantic_object=self.structured_output_model)
            instructions = parser.get_format_instructions()

            self.partial_variables["format_instructions"] = instructions
            self._format_instructions_text = instructions
            debug_print(
                "✅ [green]Format instructions added using PydanticOutputParser[/green]"
            )

        except Exception as e:
            debug_print(f"❌ [red]Error setting up format instructions: {e}[/red]")

    def _should_setup_format_instructions(self) -> bool:
        """Determine if format instructions should be set up."""
        if not self.include_format_instructions:
            debug_print("❌ [yellow]include_format_instructions is False[/yellow]")
            return False

        if "format_instructions" in self.partial_variables:
            debug_print(
                "❌ [yellow]format_instructions already exists in partial_variables[/yellow]"
            )
            return False

        # Must have structured_output_model set
        if not self.structured_output_model:
            debug_print("❌ [yellow]No structured_output_model set[/yellow]")
            return False

        # ✅ Format instructions are useful for both v1 and v2:
        # v1: traditional parsing with format instructions
        # v2: tool forcing with format instructions to guide output format
        debug_print("✅ [green]Conditions met for format instructions[/green]")
        return True

    def _setup_output_handling(self):
        """Set up output handling based on configuration with proper validation."""
        debug_print("📤 [blue]Setting up output handling...[/blue]")

        # Case 1: Raw output parsing requested
        if self.parse_raw_output:
            debug_print("📄 [yellow]Using StrOutputParser for raw output[/yellow]")
            self.output_parser = StrOutputParser()
            self.parser_type = "str"
            return

        # Case 2: Explicit output_parser provided - don't override
        if self.output_parser:
            debug_print("🎯 [cyan]Using explicitly provided output_parser[/cyan]")
            # Determine parser_type from output_parser if not set
            if not self.parser_type:
                if isinstance(self.output_parser, StrOutputParser):
                    self.parser_type = "str"
                elif isinstance(self.output_parser, PydanticOutputParser):
                    self.parser_type = "pydantic"
                elif isinstance(self.output_parser, PydanticToolsParser):
                    self.parser_type = "pydantic_tools"
                else:
                    self.parser_type = "custom"
            return

        # ✅ FIX: Case 3: v2 structured output - NO PARSER
        if self.structured_output_model and self.structured_output_version == "v2":
            debug_print(
                "[cyan]V2 structured output: NO PARSER (tool-based approach)[/cyan]"
            )
            # Explicitly set to None
            self.output_parser = None
            self.parser_type = None
            debug_print(
                "[green]V2 mode: output_parser and parser_type set to None[/green]"
            )
            return

        # ✅ Case 4: v1 structured output - use parser
        if self.structured_output_model and self.structured_output_version == "v1":
            debug_print("[cyan]V1 structured output: setting up parser[/cyan]")
            self.parser_type = "pydantic"
            self.output_parser = PydanticOutputParser(
                pydantic_object=self.structured_output_model
            )
            return

        # Case 5: Pydantic tools exist but no structured output
        elif self.pydantic_tools and not self.structured_output_model:
            debug_print(
                "🔧 [cyan]Pydantic tools detected but no structured output model[/cyan]"
            )
            # For regular pydantic tools (not structured output), don't set any parser
            # Let the user specify what they want via parser_type
            if self.parser_type == "pydantic_tools":
                self.output_parser = PydanticToolsParser(tools=self.pydantic_tools)
                debug_print(
                    "[green]Created PydanticToolsParser for explicit pydantic tools[/green]"
                )
            else:
                debug_print(
                    "🎯 [cyan]No automatic parser set for pydantic tools - user must specify parser_type[/cyan]"
                )

        # Case 6: No specific output handling - leave as None
        else:
            debug_print("📝 [yellow]No specific output parser configuration[/yellow]")

    def _setup_v2_structured_output(self):
        """Setup v2 (tool-based) approach - force tool usage with format instructions, NO parsing."""
        debug_print(
            f"🔧 [cyan]Setting up v2 approach (tool + format instructions, NO PARSER) with {self.structured_output_model.__name__}[/cyan]"
        )

        # Ensure the model is in tools list
        if self.structured_output_model not in self.tools:
            self.tools = list(self.tools) if self.tools else []
            self.tools.append(self.structured_output_model)
            debug_print(
                f"➕ [green]Added {self.structured_output_model.__name__} to tools[/green]"
            )

        # Add to pydantic_tools for tracking
        if self.structured_output_model not in self.pydantic_tools:
            self.pydantic_tools.append(self.structured_output_model)

        # ✅ FIX: Don't aggressively filter tools - let user manage multiple BaseModel tools
        # Only ensure our structured output model is present

        # ✅ FIX: Explicitly set parser_type to None for v2
        self.parser_type = None

        # ✅ FIX: Explicitly set output_parser to None for v2
        self.output_parser = None

        debug_print(
            "🎯 [green]V2 mode: NO PARSER - tool forcing with format instructions only[/green]"
        )

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
        debug_print(
            f"🎯 [green]Set force_tool_choice to '{actual_tool_name}' (exact class name)[/green]"
        )

        # Add format instructions for the model using PydanticOutputParser
        if self.include_format_instructions:
            try:
                parser = PydanticOutputParser(
                    pydantic_object=self.structured_output_model
                )
                instructions = parser.get_format_instructions()
                self.partial_variables["format_instructions"] = instructions
                self._format_instructions_text = instructions
                debug_print(
                    "✅ [green]Added format instructions from PydanticOutputParser for structured output model[/green]"
                )
            except Exception as e:
                debug_print(f"❌ [red]Error setting up format instructions: {e}[/red]")

        # Update bind_tools_kwargs to use the correct tool choice format
        self._update_bind_tools_kwargs_for_v2()

    def _setup_v1_structured_output(self):
        """Setup v1 (traditional) structured output."""
        debug_print(
            f"📋 [cyan]Setting up v1 structured output with {self.structured_output_model.__name__}[/cyan]"
        )

        self.parser_type = "pydantic"
        self.output_parser = PydanticOutputParser(
            pydantic_object=self.structured_output_model
        )

    def _configure_tool_choice(self):
        """Configure tool choice based on available tools and settings."""
        if not self.tools:
            self.force_tool_use = False
            self.force_tool_choice = None
            self.tool_choice_mode = "auto"
            debug_print("🚫 [yellow]No tools - disabling tool choice[/yellow]")
            return

        debug_print("⚙️ [blue]Configuring tool choice...[/blue]")

        # Get discovered tool names
        tool_names = self.metadata.get("tool_names", [])

        # Handle different force_tool_choice types
        if isinstance(self.force_tool_choice, bool):
            if self.force_tool_choice:
                self.tool_choice_mode = "required"
                self.force_tool_use = True
                self.force_tool_choice = None  # Convert to 'any tool'
            else:
                self.tool_choice_mode = "optional"
                self.force_tool_use = False
                self.force_tool_choice = None
            debug_print(
                f"🔄 [yellow]Converted boolean force_tool_choice to mode: {self.tool_choice_mode}[/yellow]"
            )

        elif isinstance(self.force_tool_choice, str):
            self.force_tool_use = True
            self.tool_choice_mode = "required"

            # Validate the tool name exists
            actual_tool_names = list(self._tool_name_mapping.values())
            if (
                self.force_tool_choice not in actual_tool_names
                and self.force_tool_choice not in tool_names
            ):
                debug_print(
                    f"⚠️ [yellow]Warning: force_tool_choice '{self.force_tool_choice}' not in available tools: {actual_tool_names}[/yellow]"
                )

        elif (
            isinstance(self.force_tool_choice, list | tuple) and self.force_tool_choice
        ):
            self.force_tool_use = True
            self.tool_choice_mode = "required"
            self.force_tool_choice = self.force_tool_choice[0]
            debug_print(
                f"📝 [yellow]Multiple forced tools not supported - using first: {self.force_tool_choice}[/yellow]"
            )

        elif self.force_tool_use and not self.force_tool_choice:
            self.tool_choice_mode = "required"
            if len(tool_names) == 1:
                display_name = tool_names[0]
                actual_name = self._tool_name_mapping.get(display_name, display_name)
                self.force_tool_choice = actual_name
                debug_print(
                    f"🎯 [green]Auto-selected single tool: {self.force_tool_choice}[/green]"
                )

        # Set bind_tools_kwargs based on configuration (only if not v2 which handles it separately)
        if self.structured_output_version != "v2":
            self._update_bind_tools_kwargs()

    def _update_bind_tools_kwargs(self):
        """Update bind_tools_kwargs based on current tool choice configuration."""
        if self.tool_choice_mode == "required":
            if self.force_tool_choice:
                self.bind_tools_kwargs["tool_choice"] = {
                    "type": "function",
                    "function": {"name": self.force_tool_choice},
                }
            else:
                self.bind_tools_kwargs["tool_choice"] = "required"
        elif self.tool_choice_mode == "auto":
            self.bind_tools_kwargs["tool_choice"] = "auto"
        elif self.tool_choice_mode == "none":
            self.bind_tools_kwargs["tool_choice"] = "none"
        else:
            self.bind_tools_kwargs["tool_choice"] = "auto"

    def _update_bind_tools_kwargs_for_v2(self):
        """Update bind_tools_kwargs specifically for v2 structured output."""
        # For v2, we always force the specific tool
        if self.force_tool_choice:
            self.bind_tools_kwargs["tool_choice"] = {
                "type": "function",
                "function": {"name": self.force_tool_choice},
            }
            debug_print(
                f"🔧 [green]Set bind_tools_kwargs for v2: forcing tool '{self.force_tool_choice}'[/green]"
            )
        else:
            # Fallback to required if no specific tool
            self.bind_tools_kwargs["tool_choice"] = "required"
            debug_print(
                "🔧 [yellow]Set bind_tools_kwargs for v2: 'required' (no specific tool)[/yellow]"
            )

    def _create_prompt_template_if_needed(self):
        """Create appropriate prompt template based on available components."""
        if self.prompt_template is not None:
            return

        debug_print("📝 [blue]Creating prompt template...[/blue]")

        # Create FewShotPromptTemplate if components are available
        if self.examples and self.example_prompt and self.prefix and self.suffix:
            debug_print("📚 [green]Creating FewShotPromptTemplate[/green]")
            self._create_few_shot_template()

        # Handle FewShotChatMessagePromptTemplate scenario
        elif self.examples and isinstance(self.example_prompt, ChatPromptTemplate):
            debug_print("💬 [green]Creating FewShotChatMessagePromptTemplate[/green]")
            self._create_few_shot_chat_template()

        # Create ChatPromptTemplate from system message
        elif self.system_message:
            debug_print(
                "🤖 [green]Creating ChatPromptTemplate from system message[/green]"
            )
            self._create_chat_template_from_system()

        # Create default ChatPromptTemplate
        elif self.add_messages_placeholder:
            debug_print("📋 [green]Creating default ChatPromptTemplate[/green]")
            self._create_default_chat_template()

    def _ensure_messages_placeholder_handling(self):
        """Ensure messages placeholder is properly handled based on configuration."""
        if not self.prompt_template:
            return

        if isinstance(self.prompt_template, ChatPromptTemplate):
            debug_print(
                "💬 [blue]Handling messages placeholder for ChatPromptTemplate[/blue]"
            )
            self._handle_chat_template_messages_placeholder()
        elif isinstance(self.prompt_template, FewShotChatMessagePromptTemplate):
            debug_print(
                "📚 [blue]FewShotChatMessagePromptTemplate detected - messages enabled[/blue]"
            )
            self.uses_messages_field = True
        elif isinstance(self.prompt_template, FewShotPromptTemplate):
            debug_print(
                "📝 [blue]FewShotPromptTemplate detected - messages not applicable[/blue]"
            )
            self.uses_messages_field = False
        else:
            debug_print("🔍 [blue]Checking template for message variables[/blue]")
            self._check_template_for_messages_variables()

    def _handle_chat_template_messages_placeholder(self):
        """Handle messages placeholder in ChatPromptTemplate."""
        messages = list(self.prompt_template.messages)
        has_messages_placeholder = False
        messages_placeholder_index = -1

        # Check existing placeholders
        for i, msg in enumerate(messages):
            if (
                isinstance(msg, MessagesPlaceholder)
                and getattr(msg, "variable_name", "") == self.messages_placeholder_name
            ):
                has_messages_placeholder = True
                messages_placeholder_index = i
                break

        # Add placeholder if needed
        if not has_messages_placeholder and self.add_messages_placeholder:
            should_be_optional = (
                self.force_messages_optional
                or self.messages_placeholder_name in self.optional_variables
            )

            new_placeholder = MessagesPlaceholder(
                variable_name=self.messages_placeholder_name,
                optional=should_be_optional,
            )
            messages.append(new_placeholder)
            self._update_chat_template_messages(messages)
            debug_print(
                f"➕ [green]Added messages placeholder (optional={should_be_optional})[/green]"
            )

        # Update existing placeholder if needed
        elif has_messages_placeholder:
            placeholder = messages[messages_placeholder_index]
            should_be_optional = (
                self.force_messages_optional
                or self.messages_placeholder_name in self.optional_variables
            )

            if (
                hasattr(placeholder, "optional")
                and placeholder.optional != should_be_optional
            ):
                messages[messages_placeholder_index] = MessagesPlaceholder(
                    variable_name=self.messages_placeholder_name,
                    optional=should_be_optional,
                )
                self._update_chat_template_messages(messages)
                debug_print(
                    f"🔄 [cyan]Updated messages placeholder optional={should_be_optional}[/cyan]"
                )

    def _update_chat_template_messages(self, messages: list[Any]):
        """Update ChatPromptTemplate with new messages list."""
        partial_vars = getattr(self.prompt_template, "partial_variables", {}) or {}
        self.prompt_template = ChatPromptTemplate.from_messages(messages)

        if partial_vars:
            self.prompt_template = self.prompt_template.partial(**partial_vars)

        self.uses_messages_field = True

    def _create_default_chat_template(self):
        """Create a default ChatPromptTemplate with optional messages placeholder."""
        should_be_optional = (
            self.force_messages_optional
            or self.messages_placeholder_name in self.optional_variables
        )

        messages = [
            MessagesPlaceholder(
                variable_name=self.messages_placeholder_name,
                optional=should_be_optional,
            )
        ]

        self.prompt_template = ChatPromptTemplate.from_messages(messages)
        self.uses_messages_field = True

    def _create_chat_template_from_system(self):
        """Create a ChatPromptTemplate from system_message."""
        messages = [SystemMessage(content=self.system_message)]

        if self.add_messages_placeholder:
            should_be_optional = (
                self.force_messages_optional
                or self.messages_placeholder_name in self.optional_variables
            )

            messages.append(
                MessagesPlaceholder(
                    variable_name=self.messages_placeholder_name,
                    optional=should_be_optional,
                )
            )

        self.prompt_template = ChatPromptTemplate.from_messages(messages)
        self.uses_messages_field = True

    def _create_few_shot_template(self):
        """Create a FewShotPromptTemplate from examples and example_prompt."""
        self.prompt_template = FewShotPromptTemplate(
            examples=self.examples,
            example_prompt=self.example_prompt,
            prefix=self.prefix,
            suffix=self.suffix,
            input_variables=self.input_variables or [],
            example_separator=self.example_separator,
            partial_variables=self.partial_variables,
            optional_variables=self.optional_variables,
        )
        self.uses_messages_field = False

    def _create_few_shot_chat_template(self):
        """Create a FewShotChatMessagePromptTemplate using example_prompt."""
        prefix_messages = []
        if self.system_message:
            prefix_messages = [SystemMessage(content=self.system_message)]

        few_shot_prompt = FewShotChatMessagePromptTemplate(
            examples=self.examples,
            example_prompt=self.example_prompt,
        )

        messages = [*prefix_messages, few_shot_prompt]

        if self.add_messages_placeholder:
            should_be_optional = (
                self.force_messages_optional
                or self.messages_placeholder_name in self.optional_variables
            )
            messages.append(
                MessagesPlaceholder(
                    variable_name=self.messages_placeholder_name,
                    optional=should_be_optional,
                )
            )

        self.prompt_template = ChatPromptTemplate.from_messages(messages)
        self.uses_messages_field = True

    def _check_template_for_messages_variables(self):
        """Check if the template uses messages variables."""
        if hasattr(self.prompt_template, "input_variables"):
            input_vars = getattr(self.prompt_template, "input_variables", [])
            if self.messages_placeholder_name in input_vars:
                self.uses_messages_field = True
                return

        self.uses_messages_field = False

    def _apply_partial_variables(self):
        """Apply partial variables to the prompt template."""
        if not self.prompt_template or not self.partial_variables:
            return

        try:
            if hasattr(self.prompt_template, "partial"):
                self.prompt_template = self.prompt_template.partial(
                    **self.partial_variables
                )
                debug_print(
                    f"✅ [green]Applied {len(self.partial_variables)} partial variables[/green]"
                )
        except Exception as e:
            debug_print(f"❌ [red]Error applying partial variables: {e}[/red]")

    def _apply_optional_variables(self):
        """Apply optional variables to the prompt template."""
        if not self.optional_variables or not self.prompt_template:
            return

        if isinstance(self.prompt_template, ChatPromptTemplate):
            if self.messages_placeholder_name in self.optional_variables:
                self._handle_chat_template_messages_placeholder()
        elif hasattr(self.prompt_template, "optional_variables"):
            if not hasattr(self.prompt_template.optional_variables, "extend"):
                self.prompt_template.optional_variables = list(
                    self.prompt_template.optional_variables
                )

            for var in self.optional_variables:
                if var not in self.prompt_template.optional_variables:
                    self.prompt_template.optional_variables.append(var)

    def _detect_uses_messages_field(self) -> bool:
        """Detect if this LLM configuration uses a messages field."""
        if not self.add_messages_placeholder:
            if isinstance(self.prompt_template, ChatPromptTemplate):
                for msg in self.prompt_template.messages:
                    if (
                        isinstance(msg, MessagesPlaceholder)
                        and getattr(msg, "variable_name", "")
                        == self.messages_placeholder_name
                    ):
                        return True
            return False

        if self.tools or self.system_message:
            return True

        if self.prompt_template:
            if isinstance(
                self.prompt_template,
                ChatPromptTemplate | FewShotChatMessagePromptTemplate,
            ):
                return True
            if isinstance(self.prompt_template, FewShotPromptTemplate):
                return False
            elif hasattr(self.prompt_template, "input_variables"):
                return (
                    self.messages_placeholder_name
                    in self.prompt_template.input_variables
                )

        return True

    def _compute_schema_fields(self):
        """Compute input and output schema fields."""
        debug_print("📊 [blue]Computing schema fields...[/blue]")

        # Compute input fields
        self._computed_input_fields = self._compute_input_fields()

        # Compute output fields
        self._computed_output_fields = self._compute_output_fields()

        debug_print(
            f"📥 [cyan]Input fields: {list(self._computed_input_fields.keys())}[/cyan]"
        )
        debug_print(
            f"📤 [cyan]Output fields: {list(self._computed_output_fields.keys())}[/cyan]"
        )

    def _compute_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Compute input fields based on prompt template and configuration."""
        from typing import Any as AnyType
        from typing import List as ListType
        from typing import Optional as OptionalType

        fields = {}

        # Get required input variables from prompt template
        required_vars = self._get_input_variables()

        # Get partial variables from prompt template (these should be optional with defaults)
        partial_vars = {}
        if self.prompt_template and hasattr(self.prompt_template, "partial_variables"):
            partial_vars = getattr(self.prompt_template, "partial_variables", {})

        # Handle messages field specially if using messages
        if self.uses_messages_field:
            is_optional = (
                self.force_messages_optional
                or self.messages_placeholder_name in self.optional_variables
            )

            if is_optional:
                fields[self.messages_placeholder_name] = (
                    OptionalType[list[BaseMessage]],
                    Field(default_factory=list),
                )
            else:
                fields[self.messages_placeholder_name] = (
                    list[BaseMessage],
                    Field(default_factory=list),
                )

        # Process all other required variables from prompt template
        # BUT exclude partial variables since they should be optional
        for var in required_vars:
            if (
                var != self.messages_placeholder_name
                and var not in fields
                and var not in partial_vars
            ):  # Skip partial variables!
                # Use None as default instead of Field(...) to avoid PydanticUndefined
                fields[var] = (AnyType, None)

        # Process optional variables from template
        for var in self.optional_variables:
            if var != self.messages_placeholder_name and var not in fields:
                fields[var] = (OptionalType[AnyType], None)

        # Process partial variables as optional fields with default values
        # EXCLUDE format_instructions as it's internal prompt machinery
        for var, default_value in partial_vars.items():
            if (
                var != self.messages_placeholder_name
                and var not in fields
                and var != "format_instructions"
            ):  # EXCLUDE format_instructions
                fields[var] = (OptionalType[AnyType], Field(default=default_value))

        return fields

    def _compute_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Compute output fields based on configuration."""
        from typing import Any as AnyType
        from typing import (
            Dict,
        )
        from typing import List as ListType
        from typing import Optional as OptionalType

        fields = {}

        # Case 1: V2 structured output (tool-based) - ONLY MESSAGES
        if self.structured_output_version == "v2":
            fields[self.messages_placeholder_name] = (
                list[BaseMessage],
                Field(default_factory=list),
            )
            return fields

        # Case 2: We have an output parser (v1 or explicit parser)
        if self.output_parser:
            # Handle different parser types
            if self.parser_type == "str" or isinstance(
                self.output_parser, StrOutputParser
            ):
                field_name = self.output_field_name or self.output_key or "content"
                fields[field_name] = (str, None)

            elif self.parser_type == "json":
                field_name = self.output_field_name or self.output_key or "content"
                fields[field_name] = (dict[str, AnyType], None)

            elif self.parser_type == "pydantic" and hasattr(
                self.output_parser, "pydantic_object"
            ):
                # Extract fields from PydanticOutputParser
                pydantic_model = self.output_parser.pydantic_object
                if hasattr(pydantic_model, "model_fields"):
                    for field_name, field_info in pydantic_model.model_fields.items():
                        fields[field_name] = (field_info.annotation, field_info.default)
                else:
                    model_name = self.output_field_name or self.output_key or "result"
                    fields[model_name] = (pydantic_model, None)

            elif self.parser_type == "pydantic_tools":
                field_name = self.output_field_name or self.output_key or "tool_result"
                fields[field_name] = (dict[str, AnyType], None)

            else:
                # Custom parser
                field_name = self.output_field_name or self.output_key or "content"
                fields[field_name] = (AnyType, None)

            # Also include messages for parsers that work with messages
            if self.uses_messages_field:
                fields[self.messages_placeholder_name] = (
                    list[BaseMessage],
                    Field(default_factory=list),
                )

            return fields

        # Case 3: No parser, no v2 - just messages
        fields[self.messages_placeholder_name] = (
            list[BaseMessage],
            Field(default_factory=list),
        )

        return fields

    def _get_input_variables(self) -> set[str]:
        """Get all input variables required by the prompt template."""
        all_vars = set()

        if not self.prompt_template:
            return (
                {self.messages_placeholder_name} if self.uses_messages_field else set()
            )

        # Direct input_variables attribute
        if hasattr(self.prompt_template, "input_variables"):
            vars_list = getattr(self.prompt_template, "input_variables", [])
            all_vars.update(vars_list)

        # Chat templates message variables
        if isinstance(self.prompt_template, ChatPromptTemplate):
            # Get partial variables to exclude them from required inputs
            partial_vars = getattr(self.prompt_template, "partial_variables", {})

            for msg in self.prompt_template.messages:
                if hasattr(msg, "prompt") and hasattr(msg.prompt, "input_variables"):
                    # Only add variables that are NOT in partial_variables
                    msg_vars = set(msg.prompt.input_variables) - set(
                        partial_vars.keys()
                    )
                    all_vars.update(msg_vars)

                if hasattr(msg, "variable_name"):
                    var_name = msg.variable_name
                    if (
                        not getattr(msg, "optional", False)
                        or not self.force_messages_optional
                    ):
                        all_vars.add(var_name)

        # Remove partial and optional variables
        partial_vars = set(self.partial_variables.keys())
        if hasattr(self.prompt_template, "partial_variables"):
            template_partials = getattr(self.prompt_template, "partial_variables", {})
            partial_vars.update(template_partials.keys())

        optional_vars = set(self.optional_variables)
        if hasattr(self.prompt_template, "optional_variables"):
            template_optionals = getattr(self.prompt_template, "optional_variables", [])
            optional_vars.update(template_optionals)

        result = all_vars - partial_vars - optional_vars

        # Default to messages if empty and uses_messages_field
        if (
            not result
            and self.uses_messages_field
            and self.messages_placeholder_name not in optional_vars
        ):
            return {self.messages_placeholder_name}

        return result

    def _format_model_schema(
        self, model_name: str, schema: dict[str, Any], as_section: bool = False
    ) -> str:
        """Format a model schema as instructions."""
        schema_json = json.dumps(schema, indent=2)
        header = f"## {model_name}\n" if as_section else ""
        return f"""{header}You must format your response as JSON that matches this schema:

```json
{schema_json}
```

The output should be valid JSON that conforms to the {model_name} schema."""

    def _final_validation_check(self):
        """Perform final validation checks."""
        debug_print("🔍 [blue]Performing final validation checks...[/blue]")

        # Check tool consistency
        if self.structured_output_model and self.structured_output_version:
            if self.structured_output_model not in self.pydantic_tools:
                debug_print(
                    "⚠️ [yellow]Structured output model not in pydantic_tools - adding[/yellow]"
                )
                self.pydantic_tools.append(self.structured_output_model)

        # Validate tool choice configuration
        if self.force_tool_choice and not self.tools:
            debug_print(
                "⚠️ [yellow]force_tool_choice set but no tools available[/yellow]"
            )
            self.force_tool_choice = None
            self.force_tool_use = False

        # ✅ FIX: Enhanced v2 validation - ensure parser is None
        if self.structured_output_version == "v2":
            # Ensure parser settings are correct for v2
            if self.output_parser is not None:
                debug_print(
                    "🔧 [yellow]V2 detected: clearing output_parser (should be None)[/yellow]"
                )
                self.output_parser = None

            if self.parser_type is not None:
                debug_print(
                    "🔧 [yellow]V2 detected: clearing parser_type (should be None)[/yellow]"
                )
                self.parser_type = None

            # Ensure structured output model is properly configured as tool
            if self.structured_output_model:
                if self.structured_output_model not in self.tools:
                    self.tools = list(self.tools) if self.tools else []
                    self.tools.append(self.structured_output_model)
                    debug_print(
                        "🔧 [green]Added structured_output_model to tools for v2[/green]"
                    )

                # Ensure force_tool_choice is set correctly
                expected_tool_name = self.structured_output_model.__name__
                if self.force_tool_choice != expected_tool_name:
                    self.force_tool_choice = expected_tool_name
                    debug_print(
                        f"🔧 [green]Set force_tool_choice to '{expected_tool_name}' for v2[/green]"
                    )

                # Ensure tool choice mode is required
                if self.tool_choice_mode != "required":
                    self.tool_choice_mode = "required"
                    debug_print(
                        "🔧 [green]Set tool_choice_mode to 'required' for v2[/green]"
                    )

                if not self.force_tool_use:
                    self.force_tool_use = True
                    debug_print("🔧 [green]Set force_tool_use to True for v2[/green]")

        # ✅ FIX: v1 validation - ensure parser is set
        elif self.structured_output_version == "v1" and self.structured_output_model:
            if self.output_parser is None and self.parser_type != "pydantic":
                debug_print(
                    "🔧 [yellow]V1 detected: setting up PydanticOutputParser[/yellow]"
                )
                self.output_parser = PydanticOutputParser(
                    pydantic_object=self.structured_output_model
                )
                self.parser_type = "pydantic"

        debug_print("✅ [green]Final validation checks complete[/green]")

    def _debug_final_configuration(self):
        """Debug final configuration state."""
        if not DEBUG_OUTPUT:
            return

        tree = Tree("🎯 [bold blue]Final Configuration State[/bold blue]")

        # Tools section
        tools_section = tree.add("🔧 [cyan]Tools Configuration[/cyan]")
        tools_section.add(f"Total Tools: [yellow]{len(self.tools)}[/yellow]")
        tools_section.add(
            f"Pydantic Tools: [yellow]{len(self.pydantic_tools)}[/yellow]"
        )
        tools_section.add(f"Tool Routes: [yellow]{len(self.tool_routes)}[/yellow]")
        tools_section.add(
            f"Tool Is BaseModel: [yellow]{self.tool_is_base_model}[/yellow]"
        )
        tools_section.add(f"Force Tool Use: [yellow]{self.force_tool_use}[/yellow]")
        tools_section.add(f"Tool Choice Mode: [yellow]{self.tool_choice_mode}[/yellow]")
        tools_section.add(
            f"Force Tool Choice: [yellow]{self.force_tool_choice}[/yellow]"
        )

        # Output section
        output_section = tree.add("📤 [cyan]Output Configuration[/cyan]")
        output_section.add(
            f"Structured Output Model: [yellow]{self.structured_output_model.__name__ if self.structured_output_model else 'None'}[/yellow]"
        )
        output_section.add(
            f"Structured Output Version: [yellow]{self.structured_output_version or 'None'}[/yellow]"
        )
        output_section.add(
            f"Parser Type: [yellow]{self.parser_type or 'None'}[/yellow]"
        )
        output_section.add(
            f"Format Instructions: [yellow]{'Set' if self._format_instructions_text else 'None'}[/yellow]"
        )

        # Schema section
        schema_section = tree.add("📊 [cyan]Schema Configuration[/cyan]")
        schema_section.add(
            f"Uses Messages Field: [yellow]{self.uses_messages_field}[/yellow]"
        )
        schema_section.add(
            f"Input Fields: [yellow]{len(self._computed_input_fields)}[/yellow]"
        )
        schema_section.add(
            f"Output Fields: [yellow]{len(self._computed_output_fields)}[/yellow]"
        )

        # Tool name mapping section
        if self._tool_name_mapping:
            mapping_section = tree.add("🏷️ [cyan]Tool Name Mapping[/cyan]")
            for display_name, actual_name in self._tool_name_mapping.items():
                mapping_section.add(f"{display_name} → [yellow]{actual_name}[/yellow]")

        console.print(Panel(tree, title="Configuration Complete", border_style="green"))

    def _debug_log(self, title: str, content: dict[str, Any]):
        """Pretty print debug information."""
        if not DEBUG_OUTPUT:
            return

        table = Table(title=title, title_justify="left", show_header=False)
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="yellow")

        for key, value in content.items():
            if value is not None:
                formatted_value = str(value)
                if len(formatted_value) > 100:
                    formatted_value = formatted_value[:97] + "..."
                table.add_row(key, formatted_value)

        console.print(Panel(table, expand=False))

    def _get_prompt_template_info(self) -> str:
        """Get detailed information about the prompt template."""
        if not self.prompt_template:
            return "None"

        info = f"{type(self.prompt_template).__name__}"

        if isinstance(self.prompt_template, ChatPromptTemplate):
            msg_count = len(self.prompt_template.messages)
            has_placeholder = any(
                isinstance(msg, MessagesPlaceholder)
                and getattr(msg, "variable_name", "") == self.messages_placeholder_name
                for msg in self.prompt_template.messages
            )
            info += f" ({msg_count} messages, placeholder={has_placeholder})"
        elif isinstance(self.prompt_template, FewShotChatMessagePromptTemplate):
            example_count = len(getattr(self.prompt_template, "examples", []))
            info += f" ({example_count} examples)"

        return info

    # Engine base class implementation
    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Get schema fields for input."""
        return self._computed_input_fields

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Get schema fields for output."""
        return self._computed_output_fields

    def create_runnable(
        self, runnable_config: RunnableConfig | None = None
    ) -> Runnable:
        """Create a runnable LLM chain based on this configuration."""
        from haive.core.engine.aug_llm.factory import AugLLMFactory

        # Extract config parameters
        config_params = self.apply_runnable_config(runnable_config)

        # Create factory and build runnable
        factory = AugLLMFactory(self, config_params)
        return factory.create_runnable()

    def apply_runnable_config(
        self, runnable_config: RunnableConfig | None = None
    ) -> dict[str, Any]:
        """Extract parameters from runnable_config relevant to this engine."""
        # Start with common parameters from base class
        params = super().apply_runnable_config(runnable_config)

        if runnable_config and "configurable" in runnable_config:
            configurable = runnable_config["configurable"]

            # AugLLM specific parameters to extract
            aug_llm_params = [
                "tools",
                "force_tool_choice",
                "force_tool_use",
                "tool_choice_mode",
                "temperature",
                "max_tokens",
                "system_message",
                "partial_variables",
                "parse_raw_output",
                "messages_placeholder_name",
                "optional_variables",
                "include_format_instructions",
                "parser_type",
                "pydantic_tools",
                "add_messages_placeholder",
                "force_messages_optional",
                "use_tool_for_format_instructions",
                "structured_output_version",
                "output_field_name",
                "output_key",
            ]

            for param in aug_llm_params:
                if param in configurable:
                    params[param] = configurable[param]

        return params

    def _process_input(
        self, input_data: str | Dict[str, Any] | List[BaseMessage]
    ) -> dict[str, Any]:
        """Process input into a format usable by the runnable."""
        debug_print("[blue]Processing input data[/blue]")

        # Find input variables required by the prompt template
        required_vars = self._get_input_variables()

        # Handle dictionary input
        if isinstance(input_data, dict):
            debug_print("[green]Input is already a dictionary[/green]")
            return input_data

        # Handle string input
        if isinstance(input_data, str):
            result = {}

            # If we need messages
            if (
                self.uses_messages_field
                and self.messages_placeholder_name not in result
            ):
                result[self.messages_placeholder_name] = [
                    HumanMessage(content=input_data)
                ]
                debug_print("[green]Added string to messages field[/green]")

            # For other variables, use the string directly
            for var in required_vars:
                if var != self.messages_placeholder_name:
                    result[var] = input_data
                    debug_print(f"[cyan]Added string to field: {var}[/cyan]")

            return result

        # Handle list of messages
        if isinstance(input_data, list) and all(
            isinstance(item, BaseMessage) for item in input_data
        ):
            result = {self.messages_placeholder_name: input_data}
            debug_print("[green]Added message list to messages field[/green]")
            return result

        # Default case - convert to human message
        debug_print("[yellow]Converting unknown input to human message[/yellow]")
        return {self.messages_placeholder_name: [HumanMessage(content=str(input_data))]}

    def get_format_instructions(
        self, model: Type[BaseModel] | None = None, as_tools: bool = False
    ) -> str:
        """Get format instructions for a model without changing the config."""
        # Figure out which model to use
        target_model = model
        if target_model is None:
            if self.structured_output_model:
                target_model = self.structured_output_model
            elif self.pydantic_tools:
                if as_tools:
                    # Use all tools
                    tool_instructions = []
                    for tool_model in self.pydantic_tools:
                        schema = tool_model.model_json_schema()
                        model_name = tool_model.__name__
                        tool_instructions.append(
                            self._format_model_schema(
                                model_name, schema, as_section=True
                            )
                        )

                    # Combine instructions
                    if len(tool_instructions) == 1:
                        return tool_instructions[0]
                    return (
                        "You must respond using one of the following formats:\n\n"
                        + "\n\n".join(tool_instructions)
                    )
                else:
                    # Use first tool
                    target_model = self.pydantic_tools[0]
            elif (
                len(self.tools) == 1
                and isinstance(self.tools[0], type)
                and issubclass(self.tools[0], BaseModel)
            ):
                target_model = self.tools[0]

        if not target_model:
            debug_print("[yellow]No model available for format instructions[/yellow]")
            return ""

        # Generate schema-based instructions for the model
        try:
            schema = target_model.model_json_schema()
            model_name = target_model.__name__
            return self._format_model_schema(model_name, schema)
        except Exception as e:
            debug_print(f"[yellow]Error generating format instructions: {e}[/yellow]")
            return ""

    def add_format_instructions(
        self,
        model: Type[BaseModel] | None = None,
        as_tools: bool = False,
        var_name: str = "format_instructions",
    ) -> AugLLMConfig:
        """Add format instructions to partial_variables without changing structured output configuration."""
        instructions = self.get_format_instructions(model, as_tools)
        if instructions:
            self.partial_variables[var_name] = instructions
            self._apply_partial_variables()
            debug_print(f"[green]Added format instructions to {var_name}[/green]")
        return self

    def add_system_message(self, content: str) -> AugLLMConfig:
        """Add or update system message in the prompt template."""
        debug_print("[blue]Adding/updating system message[/blue]")

        # Update system_message property
        self.system_message = content

        # Update prompt template if it's a chat template
        if isinstance(self.prompt_template, ChatPromptTemplate):
            new_messages = []
            has_system = False

            # Check existing messages
            for msg in self.prompt_template.messages:
                if hasattr(msg, "role") and msg.role == "system":
                    # Replace existing system message
                    new_messages.append(SystemMessage(content=content))
                    has_system = True
                    debug_print("[yellow]Updated existing system message[/yellow]")
                else:
                    new_messages.append(msg)

            # Add system message if none exists
            if not has_system:
                new_messages.insert(0, SystemMessage(content=content))
                debug_print("[green]Added new system message[/green]")

            # Create new template with updated messages
            self._update_chat_template_messages(new_messages)
        else:
            # Create chat template if none exists
            debug_print("[green]Creating new chat template with system message[/green]")
            self._create_chat_template_from_system()

        self.uses_messages_field = True
        return self

    def add_human_message(self, content: str) -> AugLLMConfig:
        """Add a human message to the prompt template."""
        debug_print("[blue]Adding human message[/blue]")

        if isinstance(self.prompt_template, ChatPromptTemplate):
            # Add to existing chat template
            new_messages = list(self.prompt_template.messages)
            new_messages.append(HumanMessage(content=content))
            debug_print("[green]Added human message to existing template[/green]")

            # Create new template
            self._update_chat_template_messages(new_messages)
        else:
            # Create new chat template
            messages = []
            if self.system_message:
                messages.append(SystemMessage(content=self.system_message))
            messages.append(HumanMessage(content=content))

            # Only add MessagesPlaceholder if auto-add is enabled
            if self.add_messages_placeholder:
                should_be_optional = (
                    self.force_messages_optional
                    or self.messages_placeholder_name in self.optional_variables
                )
                messages.append(
                    MessagesPlaceholder(
                        variable_name=self.messages_placeholder_name,
                        optional=should_be_optional,
                    )
                )

            self.prompt_template = ChatPromptTemplate.from_messages(messages)
            debug_print("[green]Created new chat template with human message[/green]")

        self.uses_messages_field = True
        return self

    def replace_message(self, index: int, message: str | BaseMessage) -> AugLLMConfig:
        """Replace a message in the prompt template."""
        if not isinstance(self.prompt_template, ChatPromptTemplate):
            raise ValueError("Can only replace messages in a ChatPromptTemplate")

        debug_print(f"[blue]Replacing message at index {index}[/blue]")

        # Convert string to message if needed
        if isinstance(message, str):
            # Determine message role based on the message being replaced
            if index < len(self.prompt_template.messages):
                old_msg = self.prompt_template.messages[index]
                if hasattr(old_msg, "role"):
                    role = old_msg.role
                    if role == "system":
                        message = SystemMessage(content=message)
                    elif role == "human":
                        message = HumanMessage(content=message)
                    elif role == "ai":
                        message = AIMessage(content=message)
                    else:
                        message = HumanMessage(content=message)
                else:
                    message = HumanMessage(content=message)
            else:
                message = HumanMessage(content=message)

        # Replace the message
        if index < len(self.prompt_template.messages):
            new_messages = list(self.prompt_template.messages)
            new_messages[index] = message

            self._update_chat_template_messages(new_messages)
            debug_print(f"[green]Replaced message at index {index}[/green]")

        return self

    def remove_message(self, index: int) -> AugLLMConfig:
        """Remove a message from the prompt template."""
        if not isinstance(self.prompt_template, ChatPromptTemplate):
            raise ValueError("Can only remove messages from a ChatPromptTemplate")

        debug_print(f"[blue]Removing message at index {index}[/blue]")

        if index < len(self.prompt_template.messages):
            new_messages = list(self.prompt_template.messages)
            removed = new_messages.pop(index)

            # Create new template
            self._update_chat_template_messages(new_messages)

            # Update uses_messages_field if we removed the MessagesPlaceholder
            if (
                isinstance(removed, MessagesPlaceholder)
                and removed.variable_name == self.messages_placeholder_name
            ):
                # Re-add the placeholder if add_messages_placeholder is True
                if self.add_messages_placeholder:
                    self._ensure_messages_placeholder_handling()
                else:
                    # Check if there's still a messages placeholder
                    self.uses_messages_field = self._detect_uses_messages_field()

            debug_print(f"[green]Removed message at index {index}[/green]")

        return self

    def add_optional_variable(self, var_name: str) -> AugLLMConfig:
        """Add an optional variable to the prompt template."""
        if var_name not in self.optional_variables:
            self.optional_variables.append(var_name)
            debug_print(f"[blue]Added optional variable: {var_name}[/blue]")

            # Apply optional variables to prompt template
            self._apply_optional_variables()

        return self

    def with_structured_output(
        self,
        model: type[BaseModel],
        include_instructions: bool = True,
        version: str = "v2",
    ) -> AugLLMConfig:
        """Configure with Pydantic structured output."""
        debug_print(
            f"[blue]Configuring with structured output (version {version})[/blue]"
        )

        # Set the structured output model
        self.structured_output_model = model
        self.include_format_instructions = include_instructions

        # Validate version
        if version not in ["v1", "v2"]:
            debug_print(
                f"[yellow]Invalid version '{version}' - defaulting to 'v2'[/yellow]"
            )
            version = "v2"

        self.structured_output_version = cast(StructuredOutputVersion, version)

        # Re-run validation to update everything
        if not self._is_processing_validation:
            self.comprehensive_validation_and_setup()

        return self

    def with_pydantic_tools(
        self,
        tool_models: list[type[BaseModel]],
        include_instructions: bool = True,
        force_use: bool = False,
    ) -> AugLLMConfig:
        """Configure with Pydantic tools output parsing."""
        debug_print("[blue]Configuring with pydantic tools[/blue]")

        # Set the pydantic tools
        self.pydantic_tools = tool_models

        # Add to tools list if not already there
        self.tools = list(self.tools) if self.tools else []
        for model in tool_models:
            if model not in self.tools:
                self.tools.append(model)

        self.include_format_instructions = include_instructions

        # Configure tool use if requested
        if force_use:
            self.force_tool_use = True
            self.tool_choice_mode = "required"

            # If single tool, set it as the forced choice
            if len(tool_models) == 1:
                model_name = tool_models[0].__name__  # Use exact class name
                self.force_tool_choice = model_name
                debug_print(f"[green]Forcing use of tool: {model_name}[/green]")

        # Re-run validation
        if not self._is_processing_validation:
            self.comprehensive_validation_and_setup()

        return self

    def with_format_instructions(
        self,
        model: type[BaseModel],
        as_tool: bool = False,
        var_name: str = "format_instructions",
    ) -> AugLLMConfig:
        """Add format instructions without setting up structured output or parser."""
        # Get instructions
        instructions = self.get_format_instructions(model, as_tool)

        # Add to partial variables if instructions were generated
        if instructions:
            self.partial_variables[var_name] = instructions
            self._apply_partial_variables()
            debug_print(f"[green]Added format instructions to {var_name}[/green]")

        return self

    def with_tools(
        self,
        tools: list[
            Type[BaseTool]
            | Type[BaseModel]
            | Callable
            | StructuredTool
            | BaseTool
            | str
        ],
        force_use: bool = False,
        specific_tool: str | None = None,
    ) -> AugLLMConfig:
        """Configure with specified tools."""
        debug_print("[blue]Configuring with tools[/blue]")

        # Set tools
        self.tools = tools

        # Configure tool choice
        self.force_tool_use = force_use

        if specific_tool:
            self.force_tool_choice = specific_tool
            self.tool_choice_mode = "required"
            debug_print(f"[green]Forcing use of specific tool: {specific_tool}[/green]")
        elif force_use:
            self.tool_choice_mode = "required"
            debug_print("[green]Forcing use of any tool[/green]")

        # Re-run validation
        if not self._is_processing_validation:
            self.comprehensive_validation_and_setup()

        return self

    def add_prompt_template(self, prompt_template: BasePromptTemplate) -> AugLLMConfig:
        """Add a prompt template to the configuration."""
        debug_print(
            f"[blue]Adding prompt template: {type(prompt_template).__name__}[/blue]"
        )

        # Set prompt template
        self.prompt_template = prompt_template

        # Re-run validation
        if not self._is_processing_validation:
            self.comprehensive_validation_and_setup()

        debug_print(
            f"[green]Added prompt template: {type(prompt_template).__name__}[/green]"
        )
        return self

    # Tool management methods from ToolListMixin
    def add_tool(
        self, tool: Any, name: str | None = None, route: str | None = None
    ) -> AugLLMConfig:
        """Add a single tool with optional name and route."""
        if tool not in self.tools:
            self.tools = [*list(self.tools), tool]

            # Auto-assign name and route
            if name or route:
                auto_name = name or (
                    getattr(tool, "name", None)
                    or getattr(tool, "__name__", f"tool_{len(self.tools)}")
                )
                auto_route = route or "manual"
                self.tool_routes[auto_name] = auto_route

            debug_print(f"➕ [green]Added tool: {name or type(tool).__name__}[/green]")

            # Re-sync tool routes
            self._sync_tool_routes()

        return self

    def remove_tool(self, tool: Any) -> AugLLMConfig:
        """Remove a tool and update all related configurations."""
        if tool in self.tools:
            self.tools = [t for t in self.tools if t != tool]

            # Remove from pydantic_tools if it's there
            if tool in self.pydantic_tools:
                self.pydantic_tools = [t for t in self.pydantic_tools if t != tool]

            # Remove from tool_routes
            tool_name = getattr(tool, "name", None) or getattr(tool, "__name__", None)
            if tool_name and tool_name in self.tool_routes:
                del self.tool_routes[tool_name]

            debug_print(
                f"➖ [yellow]Removed tool: {tool_name or type(tool).__name__}[/yellow]"
            )

            # Re-sync and recompute fields
            self._sync_tool_routes()
            if not self._is_processing_validation:
                self._compute_schema_fields()

        return self

    def instantiate_llm(self) -> Any:
        """Instantiate the LLM based on the configuration."""
        return self.llm_config.instantiate()

    # Specialized tool creation for AugLLMConfig
    def _create_tool_implementation(self, name: str, description: str, **kwargs) -> Any:
        """Create tool implementation specialized for AugLLMConfig.

        Can create:
        - LLM function tools that invoke the configured LLM
        - Retriever tools if configured as retriever
        - Pydantic tools from structured output models
        """
        # Check if this should be a retriever tool
        route = self.get_tool_route(name)
        if route == "retriever" and hasattr(self, "instantiate"):
            return self._create_retriever_tool(name, description, **kwargs)

        # Check if this should be a pydantic tool based on structured output
        if self.structured_output_model and route == "pydantic_model":
            return self._create_structured_output_tool(name, description, **kwargs)

        # Default: create an LLM function tool
        return self._create_llm_function_tool(name, description, **kwargs)

    def _create_llm_function_tool(self, name: str, description: str, **kwargs) -> Any:
        """Create a function tool that invokes this LLM configuration."""
        try:
            from langchain_core.tools import StructuredTool
            from pydantic import BaseModel, Field

            # Create input schema based on LLM's input fields
            input_fields = self.get_input_fields()

            # Create a dynamic input model
            class LLMInput(BaseModel):
                pass

            # Add fields from input_fields
            for field_name, (_field_type, field_default) in input_fields.items():
                if field_default is not None:
                    setattr(
                        LLMInput,
                        field_name,
                        Field(
                            default=field_default, description=f"Input for {field_name}"
                        ),
                    )
                else:
                    setattr(
                        LLMInput,
                        field_name,
                        Field(description=f"Input for {field_name}"),
                    )

            # Create the function that invokes the LLM
            def llm_function(**inputs):
                """Invoke the configured LLM with inputs."""
                runnable = self.create_runnable()
                return runnable.invoke(inputs)

            # Set function metadata
            llm_function.__name__ = name
            llm_function.__doc__ = description

            return StructuredTool.from_function(
                func=llm_function,
                name=name,
                description=description,
                args_schema=LLMInput,
                **kwargs,
            )
        except ImportError:
            raise ImportError("langchain_core.tools is required for LLM function tools")

    def _create_structured_output_tool(
        self, name: str, description: str, **kwargs
    ) -> Any:
        """Create a tool from the structured output model."""
        if not self.structured_output_model:
            raise ValueError("No structured output model configured")

        # For structured output models, return the model class itself
        # but add tool metadata
        tool_class = self.structured_output_model

        # Add metadata
        metadata = {
            "llm_config": self.name or "anonymous",
            "version": self.structured_output_version,
            "tool_type": "structured_output",
        }

        self.set_tool_route(name, "structured_output", metadata)

        return tool_class

    # Enhanced tool management methods
    def add_tool_with_route(
        self,
        tool: Any,
        route: str,
        name: str | None = None,
        metadata: Dict[str, Any] | None = None,
    ) -> AugLLMConfig:
        """Add a tool with explicit route and metadata."""
        # Add to tools list
        if tool not in self.tools:
            self.tools = [*list(self.tools), tool]

        # Determine tool name
        tool_name = name or (
            getattr(tool, "name", None)
            or getattr(tool, "__name__", f"tool_{len(self.tools)}")
        )

        # Set route and metadata
        self.set_tool_route(tool_name, route, metadata)

        debug_print(f"➕ [green]Added tool with route: {tool_name} -> {route}[/green]")

        # Re-sync tool routes to update mappings
        self._sync_tool_routes()
        return self

    def create_tool_from_config(
        self,
        config: Any,
        name: str | None = None,
        route: str | None = None,
        **kwargs,
    ) -> Any:
        """Create a tool from another config object.

        Args:
            config: Configuration object that has a to_tool method
            name: Tool name
            route: Tool route to set
            **kwargs: Additional kwargs for tool creation

        Returns:
            Created tool
        """
        if not hasattr(config, "to_tool"):
            raise ValueError(
                f"Config {type(config).__name__} does not support to_tool conversion"
            )

        # Create the tool
        tool = config.to_tool(name=name, **kwargs)

        # Add to our tools with route
        if route:
            self.add_tool_with_route(tool, route, name)
        else:
            self.add_tool(tool, name)

        return tool

    # Class method constructors
    @classmethod
    def from_llm_config(cls, llm_config: LLMConfig, **kwargs):
        """Create from an existing LLMConfig."""
        return cls(llm_config=llm_config, **kwargs)

    @classmethod
    def from_prompt(
        cls,
        prompt: BasePromptTemplate,
        llm_config: LLMConfig | None = None,
        **kwargs,
    ):
        """Create from a prompt template."""
        if llm_config is None:
            llm_config = AzureLLMConfig(model="gpt-4o")

        debug_print(f"[blue]Creating AugLLMConfig from {type(prompt).__name__}[/blue]")

        # Handle partial variables if provided in kwargs
        partial_variables = kwargs.pop("partial_variables", {})
        optional_variables = []
        if hasattr(prompt, "optional_variables") and getattr(
            prompt, "optional_variables", None
        ):
            optional_variables = list(getattr(prompt, "optional_variables", []))

        # Override with explicit kwargs if provided
        if "optional_variables" in kwargs:
            optional_variables = kwargs.pop("optional_variables")

        uses_messages = kwargs.pop("uses_messages_field", None)
        messages_placeholder_name = kwargs.pop("messages_placeholder_name", "messages")

        if uses_messages is None:
            # Auto-detect based on prompt type
            if isinstance(prompt, ChatPromptTemplate):
                uses_messages = any(
                    (
                        isinstance(msg, MessagesPlaceholder)
                        and getattr(msg, "variable_name", "")
                        == messages_placeholder_name
                    )
                    or (hasattr(msg, "role") and msg.role == "system")
                    for msg in prompt.messages
                )
            elif isinstance(prompt, FewShotChatMessagePromptTemplate):
                uses_messages = True
            else:
                uses_messages = False

        config = cls(
            prompt_template=prompt,
            llm_config=llm_config,
            partial_variables=partial_variables,
            uses_messages_field=uses_messages,
            messages_placeholder_name=messages_placeholder_name,
            optional_variables=optional_variables,
            **kwargs,
        )

        debug_print("[green]Successfully created AugLLMConfig from prompt[/green]")
        return config

    @classmethod
    def from_system_prompt(
        cls, system_prompt: str, llm_config: LLMConfig | None = None, **kwargs
    ):
        """Create from a system prompt string."""
        if llm_config is None:
            llm_config = AzureLLMConfig(model="gpt-4o")

        debug_print("[blue]Creating AugLLMConfig from system prompt string[/blue]")

        messages_placeholder_name = kwargs.pop("messages_placeholder_name", "messages")
        optional_variables = kwargs.pop("optional_variables", [])
        add_messages_placeholder = kwargs.pop("add_messages_placeholder", True)

        is_optional = messages_placeholder_name in optional_variables

        # Create messages list with system message
        messages = [SystemMessage(content=system_prompt)]

        # Only add MessagesPlaceholder if auto-add is enabled
        if add_messages_placeholder:
            messages.append(
                MessagesPlaceholder(
                    variable_name=messages_placeholder_name, optional=is_optional
                )
            )

        # Create template
        prompt = ChatPromptTemplate.from_messages(messages)

        return cls(
            prompt_template=prompt,
            system_message=system_prompt,
            llm_config=llm_config,
            uses_messages_field=True,
            messages_placeholder_name=messages_placeholder_name,
            optional_variables=optional_variables,
            add_messages_placeholder=add_messages_placeholder,
            **kwargs,
        )

    @classmethod
    def from_few_shot(
        cls,
        examples: list[dict[str, Any]],
        example_prompt: PromptTemplate,
        prefix: str,
        suffix: str,
        input_variables: list[str],
        llm_config: LLMConfig | None = None,
        **kwargs,
    ):
        """Create with few-shot examples."""
        if llm_config is None:
            llm_config = AzureLLMConfig(model="gpt-4o")

        debug_print("[blue]Creating AugLLMConfig with few-shot examples[/blue]")

        partial_variables = kwargs.pop("partial_variables", {})
        example_separator = kwargs.pop("example_separator", "\n\n")
        optional_variables = kwargs.pop("optional_variables", [])

        # Create few-shot prompt template
        few_shot_prompt = FewShotPromptTemplate(
            examples=examples,
            example_prompt=example_prompt,
            prefix=prefix,
            suffix=suffix,
            input_variables=input_variables,
            example_separator=example_separator,
            partial_variables=partial_variables,
            optional_variables=optional_variables,
        )

        return cls(
            prompt_template=few_shot_prompt,
            examples=examples,
            example_prompt=example_prompt,
            prefix=prefix,
            suffix=suffix,
            input_variables=input_variables,
            example_separator=example_separator,
            llm_config=llm_config,
            uses_messages_field=False,
            partial_variables=partial_variables,
            optional_variables=optional_variables,
            **kwargs,
        )

    @classmethod
    def from_few_shot_chat(
        cls,
        examples: list[dict[str, Any]],
        example_prompt: ChatPromptTemplate,
        system_message: str | None = None,
        llm_config: LLMConfig | None = None,
        **kwargs,
    ):
        """Create with few-shot examples for chat templates."""
        if llm_config is None:
            llm_config = AzureLLMConfig(model="gpt-4o")

        debug_print("[blue]Creating AugLLMConfig with few-shot chat examples[/blue]")

        partial_variables = kwargs.pop("partial_variables", {})
        messages_placeholder_name = kwargs.pop("messages_placeholder_name", "messages")
        optional_variables = kwargs.pop("optional_variables", [])
        add_messages_placeholder = kwargs.pop("add_messages_placeholder", True)

        # Build few shot template
        few_shot_prompt = FewShotChatMessagePromptTemplate(
            examples=examples,
            example_prompt=example_prompt,
        )

        # Create messages list
        messages = []
        if system_message:
            messages.append(SystemMessage(content=system_message))

        # Add few-shot examples
        messages.append(few_shot_prompt)

        # Add messages placeholder if needed
        if add_messages_placeholder:
            is_optional = messages_placeholder_name in optional_variables
            messages.append(
                MessagesPlaceholder(
                    variable_name=messages_placeholder_name, optional=is_optional
                )
            )

        # Create prompt template
        prompt = ChatPromptTemplate.from_messages(messages)

        return cls(
            prompt_template=prompt,
            examples=examples,
            example_prompt=example_prompt,
            system_message=system_message,
            llm_config=llm_config,
            uses_messages_field=True,
            messages_placeholder_name=messages_placeholder_name,
            partial_variables=partial_variables,
            optional_variables=optional_variables,
            add_messages_placeholder=add_messages_placeholder,
            **kwargs,
        )

    @classmethod
    def from_system_and_few_shot(
        cls,
        system_message: str,
        examples: list[dict[str, Any]],
        example_prompt: PromptTemplate,
        prefix: str,
        suffix: str,
        input_variables: list[str],
        llm_config: LLMConfig | None = None,
        **kwargs,
    ):
        """Create with system message and few-shot examples."""
        if llm_config is None:
            llm_config = AzureLLMConfig(model="gpt-4o")

        debug_print(
            "[blue]Creating AugLLMConfig with system message and few-shot examples[/blue]"
        )

        partial_variables = kwargs.pop("partial_variables", {})
        example_separator = kwargs.pop("example_separator", "\n\n")
        optional_variables = kwargs.pop("optional_variables", [])

        # Create a prefix with system message
        enhanced_prefix = f"{system_message}\n\n{prefix}"

        # Create few-shot prompt template
        few_shot_prompt = FewShotPromptTemplate(
            examples=examples,
            example_prompt=example_prompt,
            prefix=enhanced_prefix,
            suffix=suffix,
            input_variables=input_variables,
            example_separator=example_separator,
            partial_variables=partial_variables,
            optional_variables=optional_variables,
        )

        return cls(
            prompt_template=few_shot_prompt,
            examples=examples,
            example_prompt=example_prompt,
            prefix=prefix,
            suffix=suffix,
            system_message=system_message,
            input_variables=input_variables,
            example_separator=example_separator,
            llm_config=llm_config,
            uses_messages_field=False,
            partial_variables=partial_variables,
            optional_variables=optional_variables,
            **kwargs,
        )

    @classmethod
    def from_tools(
        cls,
        tools: list[BaseTool | Type[BaseTool] | str | Type[BaseModel]],
        system_message: str | None = None,
        llm_config: LLMConfig | None = None,
        use_tool_for_format_instructions: bool | None = None,
        force_tool_use: bool = False,
        **kwargs,
    ):
        """Create with specified tools."""
        if llm_config is None:
            llm_config = AzureLLMConfig(model="gpt-4o")

        debug_print("[blue]Creating AugLLMConfig with tools[/blue]")

        messages_placeholder_name = kwargs.pop("messages_placeholder_name", "messages")
        optional_variables = kwargs.pop("optional_variables", [])
        add_messages_placeholder = kwargs.pop("add_messages_placeholder", True)

        force_tool_choice = kwargs.pop("force_tool_choice", None)
        tool_choice_mode = kwargs.pop("tool_choice_mode", "auto")

        # Create messages list
        messages = []
        if system_message:
            messages.append(SystemMessage(content=system_message))

        # Add MessagesPlaceholder if auto-add is enabled
        if add_messages_placeholder:
            is_optional = messages_placeholder_name in optional_variables
            messages.append(
                MessagesPlaceholder(
                    variable_name=messages_placeholder_name, optional=is_optional
                )
            )

        # Create template
        prompt_template = (
            ChatPromptTemplate.from_messages(messages) if messages else None
        )

        # Create instance
        instance = cls(
            tools=tools,
            prompt_template=prompt_template,
            system_message=system_message,
            llm_config=llm_config,
            uses_messages_field=True,
            messages_placeholder_name=messages_placeholder_name,
            optional_variables=optional_variables,
            add_messages_placeholder=add_messages_placeholder,
            use_tool_for_format_instructions=use_tool_for_format_instructions,
            force_tool_use=force_tool_use,
            force_tool_choice=force_tool_choice,
            tool_choice_mode=tool_choice_mode,
            **kwargs,
        )

        return instance

    @classmethod
    def from_pydantic_tools(
        cls,
        tool_models: list[type[BaseModel]],
        system_message: str | None = None,
        llm_config: LLMConfig | None = None,
        include_instructions: bool = True,
        force_tool_use: bool = False,
        **kwargs,
    ):
        """Create with Pydantic tool models."""
        if llm_config is None:
            llm_config = AzureLLMConfig(model="gpt-4o")

        debug_print("[blue]Creating AugLLMConfig with pydantic tools[/blue]")

        messages_placeholder_name = kwargs.pop("messages_placeholder_name", "messages")
        optional_variables = kwargs.pop("optional_variables", [])
        add_messages_placeholder = kwargs.pop("add_messages_placeholder", True)

        force_tool_choice = kwargs.pop("force_tool_choice", None)
        tool_choice_mode = kwargs.pop("tool_choice_mode", "auto")

        if force_tool_use:
            tool_choice_mode = "required"
            if len(tool_models) == 1:
                force_tool_choice = tool_models[0].__name__  # Use exact class name

        # Create messages list
        messages = []
        if system_message:
            messages.append(SystemMessage(content=system_message))

        if add_messages_placeholder:
            is_optional = messages_placeholder_name in optional_variables
            messages.append(
                MessagesPlaceholder(
                    variable_name=messages_placeholder_name, optional=is_optional
                )
            )

        prompt_template = (
            ChatPromptTemplate.from_messages(messages) if messages else None
        )

        partial_variables = kwargs.pop("partial_variables", {})

        # Create instance first
        instance = cls(
            pydantic_tools=tool_models,
            tools=tool_models,
            # Don't set parser_type - let user specify
            prompt_template=prompt_template,
            system_message=system_message,
            llm_config=llm_config,
            uses_messages_field=True,
            messages_placeholder_name=messages_placeholder_name,
            partial_variables=partial_variables,
            include_format_instructions=include_instructions,
            optional_variables=optional_variables,
            add_messages_placeholder=add_messages_placeholder,
            force_tool_use=force_tool_use,
            force_tool_choice=force_tool_choice,
            tool_choice_mode=tool_choice_mode,
            **kwargs,
        )

        # Add format instructions if needed
        if include_instructions:
            instance.add_format_instructions(None, True)

        return instance

    @classmethod
    def from_format_instructions(
        cls,
        model: type[BaseModel],
        system_message: str | None = None,
        llm_config: LLMConfig | None = None,
        as_tool: bool = False,
        var_name: str = "format_instructions",
        **kwargs,
    ):
        """Create config with format instructions but without structured output."""
        if llm_config is None:
            llm_config = AzureLLMConfig(model="gpt-4o")

        debug_print(
            f"[blue]Creating AugLLMConfig with format instructions from {model.__name__}[/blue]"
        )

        config = cls.from_system_prompt(
            system_message=system_message or "", llm_config=llm_config, **kwargs
        )

        config.add_format_instructions(model, as_tool, var_name)
        return config

    @classmethod
    def from_structured_output_v1(
        cls,
        model: type[BaseModel],
        system_message: str | None = None,
        llm_config: LLMConfig | None = None,
        include_instructions: bool = True,
        **kwargs,
    ):
        """Create with v1 structured output using traditional parsing."""
        if llm_config is None:
            llm_config = AzureLLMConfig(model="gpt-4o")

        debug_print(
            f"[blue]Creating AugLLMConfig with v1 structured output using {model.__name__}[/blue]"
        )

        # Set v1 specific parameters
        kwargs["structured_output_version"] = "v1"
        kwargs["structured_output_model"] = model
        kwargs["include_format_instructions"] = include_instructions

        # Create messages list
        messages = []
        if system_message:
            messages.append(SystemMessage(content=system_message))

        # Get message parameters
        messages_placeholder_name = kwargs.pop("messages_placeholder_name", "messages")
        add_messages_placeholder = kwargs.pop("add_messages_placeholder", True)
        force_messages_optional = kwargs.pop("force_messages_optional", True)

        # Add MessagesPlaceholder if auto-add is enabled
        if add_messages_placeholder:
            optional_variables = kwargs.get("optional_variables", [])
            is_optional = (
                force_messages_optional
                or messages_placeholder_name in optional_variables
            )

            # Ensure optional_variables list includes messages_placeholder_name if needed
            if is_optional and messages_placeholder_name not in optional_variables:
                optional_variables.append(messages_placeholder_name)
                kwargs["optional_variables"] = optional_variables

            # Add the placeholder
            messages.append(
                MessagesPlaceholder(
                    variable_name=messages_placeholder_name, optional=is_optional
                )
            )

        # Create prompt template
        if messages:
            prompt_template = ChatPromptTemplate.from_messages(messages)
            kwargs["prompt_template"] = prompt_template

        # Create the config
        instance = cls(
            llm_config=llm_config,
            system_message=system_message,
            messages_placeholder_name=messages_placeholder_name,
            add_messages_placeholder=add_messages_placeholder,
            force_messages_optional=force_messages_optional,
            **kwargs,
        )

        return instance

    @classmethod
    def from_structured_output_v2(
        cls,
        model: type[BaseModel],
        system_message: str | None = None,
        llm_config: LLMConfig | None = None,
        include_instructions: bool = False,
        output_field_name: str | None = None,
        **kwargs,
    ):
        """Create with v2 structured output using the tool-based approach."""
        if llm_config is None:
            llm_config = AzureLLMConfig(model="gpt-4o")

        debug_print(
            f"[blue]Creating AugLLMConfig with v2 structured output using {model.__name__}[/blue]"
        )

        # Ensure proper settings for v2
        kwargs["structured_output_version"] = "v2"
        kwargs["structured_output_model"] = model
        kwargs["force_tool_use"] = True
        kwargs["tool_choice_mode"] = "required"

        # V2 doesn't use structured output parsing - just forces tools with format instructions
        kwargs["include_format_instructions"] = include_instructions

        # Auto-set tool name if not specified - use the actual name that will be used in binding
        if "force_tool_choice" not in kwargs:
            kwargs["force_tool_choice"] = (
                model.__name__
            )  # Use exact class name, not lowercase

        # Set output field name if specified
        if output_field_name:
            kwargs["output_field_name"] = output_field_name

        # Create messages list
        messages = []
        if system_message:
            messages.append(SystemMessage(content=system_message))

        # Get message parameters
        messages_placeholder_name = kwargs.pop("messages_placeholder_name", "messages")
        add_messages_placeholder = kwargs.pop("add_messages_placeholder", True)
        force_messages_optional = kwargs.pop("force_messages_optional", True)

        # Add MessagesPlaceholder if auto-add is enabled
        if add_messages_placeholder:
            optional_variables = kwargs.get("optional_variables", [])
            is_optional = (
                force_messages_optional
                or messages_placeholder_name in optional_variables
            )

            # Ensure optional_variables list includes messages_placeholder_name if needed
            if is_optional and messages_placeholder_name not in optional_variables:
                optional_variables.append(messages_placeholder_name)
                kwargs["optional_variables"] = optional_variables

            # Add the placeholder
            messages.append(
                MessagesPlaceholder(
                    variable_name=messages_placeholder_name, optional=is_optional
                )
            )

        # Create prompt template
        if messages:
            prompt_template = ChatPromptTemplate.from_messages(messages)
            kwargs["prompt_template"] = prompt_template

        # Now create the config
        instance = cls(
            llm_config=llm_config,
            system_message=system_message,
            messages_placeholder_name=messages_placeholder_name,
            add_messages_placeholder=add_messages_placeholder,
            force_messages_optional=force_messages_optional,
            **kwargs,
        )

        # The tool will be added during validation, no need to manually add here
        return instance

    def debug_tool_configuration(self) -> AugLLMConfig:
        """Print detailed debug information about tool configuration."""
        console.print("\n" + "=" * 80)
        console.print("[bold blue]🔧 TOOL CONFIGURATION DEBUG[/bold blue]")
        console.print("=" * 80)

        # Basic tool info
        basic_tree = Tree("📋 [cyan]Basic Tool Information[/cyan]")
        basic_tree.add(f"Total Tools: [yellow]{len(self.tools)}[/yellow]")
        basic_tree.add(f"Pydantic Tools: [yellow]{len(self.pydantic_tools)}[/yellow]")
        basic_tree.add(f"Tool Is BaseModel: [yellow]{self.tool_is_base_model}[/yellow]")
        basic_tree.add(f"Force Tool Use: [yellow]{self.force_tool_use}[/yellow]")
        basic_tree.add(f"Tool Choice Mode: [yellow]{self.tool_choice_mode}[/yellow]")
        basic_tree.add(f"Force Tool Choice: [yellow]{self.force_tool_choice}[/yellow]")
        console.print(basic_tree)

        # Tool details
        if self.tools:
            tools_tree = Tree("🔧 [cyan]Tool Details[/cyan]")
            for i, tool in enumerate(self.tools):
                tool_info = f"[{i}] {type(tool).__name__}"
                if hasattr(tool, "name"):
                    tool_info += f" (name: {tool.name})"
                if hasattr(tool, "__name__"):
                    tool_info += f" (__name__: {tool.__name__})"
                tools_tree.add(tool_info)
            console.print(tools_tree)

        # Tool routes
        if self.tool_routes:
            routes_tree = Tree("🛤️ [cyan]Tool Routes[/cyan]")
            for name, route in self.tool_routes.items():
                routes_tree.add(f"{name} → [yellow]{route}[/yellow]")
            console.print(routes_tree)

        # Tool name mapping
        if self._tool_name_mapping:
            mapping_tree = Tree("🏷️ [cyan]Tool Name Mapping[/cyan]")
            for display_name, actual_name in self._tool_name_mapping.items():
                mapping_tree.add(f"{display_name} → [yellow]{actual_name}[/yellow]")
            console.print(mapping_tree)

        # Bind tools kwargs
        if self.bind_tools_kwargs:
            bind_tree = Tree("⚙️ [cyan]Bind Tools Kwargs[/cyan]")
            for key, value in self.bind_tools_kwargs.items():
                bind_tree.add(f"{key}: [yellow]{value}[/yellow]")
            console.print(bind_tree)

        # Structured output info
        if self.structured_output_model:
            struct_tree = Tree("📤 [cyan]Structured Output[/cyan]")
            struct_tree.add(
                f"Model: [yellow]{self.structured_output_model.__name__}[/yellow]"
            )
            struct_tree.add(
                f"Version: [yellow]{self.structured_output_version}[/yellow]"
            )
            struct_tree.add(f"Parser Type: [yellow]{self.parser_type}[/yellow]")
            console.print(struct_tree)

        console.print("=" * 80 + "\n")
        return self

    def instantiate_llm(self) -> Any:
        """Instantiate the LLM based on the configuration."""
        return self.llm_config.instantiate()
