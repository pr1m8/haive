"""
Factory for creating LLM chain runnables from AugLLMConfig.

This module provides a specialized factory implementation that transforms
AugLLMConfig configurations into executable LLM chain runnables. It enforces
a clean separation between configuration (AugLLMConfig) and runtime creation
(AugLLMFactory), allowing for runtime overrides and specialized handling.

Key features:
- Runtime configuration overrides for flexible deployment
- Structured output handling with multiple approaches (v1/v2)
- Comprehensive tool binding with graceful fallbacks
- Chain composition with preprocessing and postprocessing
- Detailed logging for debugging and monitoring

The factory handles the complex process of assembling different components
(LLMs, prompts, tools, parsers) into a cohesive, executable chain while
respecting the configuration specifications from AugLLMConfig.
"""

import json
import logging
from typing import Any, Dict, Optional, Type

from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import (
    PydanticOutputParser,
    StrOutputParser,
)
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.runnables import Runnable, RunnableLambda
from langchain_core.tools import BaseTool
from pydantic import BaseModel

from haive.core.logging.rich_logger import LogLevel, get_logger

# Get logger for this module
logger = get_logger(__name__)
logger.set_level(LogLevel.WARNING)


class AugLLMFactory:
    """
    Factory for creating structured LLM runnables from AugLLMConfig with flexible message handling.

    This factory class takes an AugLLMConfig instance and transforms it into an
    executable LLM chain runnable, applying any runtime configuration overrides
    in the process. It handles the complex assembly of various components including
    LLM initialization, tool binding, structured output configuration, and chain
    composition.

    The factory follows a builder pattern, handling each aspect of chain creation
    in discrete steps while maintaining proper validation and logging throughout
    the process. It provides graceful fallbacks for various scenarios and specialized
    handling for different tool and output configurations.

    Attributes:
        aug_config (AugLLMConfig): The configuration object that defines how the
            runnable should be constructed.
        config_params (Dict[str, Any]): Runtime configuration overrides that take
            precedence over the settings in aug_config.

    Examples:
        >>> from haive.core.engine.aug_llm.config import AugLLMConfig
        >>> from haive.core.engine.aug_llm.factory import AugLLMFactory
        >>>
        >>> # Create a base configuration
        >>> config = AugLLMConfig(name="text_summarizer", system_message="Summarize text concisely.")
        >>>
        >>> # Create a factory with runtime overrides
        >>> factory = AugLLMFactory(
        ...     config,
        ...     config_params={"temperature": 0.3, "max_tokens": 200}
        ... )
        >>>
        >>> # Build the runnable
        >>> summarizer = factory.create_runnable()
        >>>
        >>> # Use the runnable
        >>> summary = summarizer.invoke("Long text to summarize...")
    """

    def __init__(self, aug_config: Any, config_params: Optional[Dict[str, Any]] = None):
        """
        Initialize the factory with an AugLLMConfig.

        Args:
            aug_config: Configuration for the LLM chain
            config_params: Optional runtime parameters to override defaults
        """
        self.aug_config = aug_config
        self.config_params = config_params or {}

        # Apply runtime config overrides if any
        self._apply_config_params()

        # Log initialization state
        logger.debug_table(
            "AugLLMFactory Initialization",
            {
                "config_name": self.aug_config.name,
                "runtime_overrides": bool(config_params),
                "has_prompt_template": self.aug_config.prompt_template is not None,
                "has_tools": len(self.aug_config.tools) > 0,
                "has_structured_output": self.aug_config.structured_output_model
                is not None,
                "force_messages_optional": self.aug_config.force_messages_optional,
                "messages_in_optional_vars": self.aug_config.messages_placeholder_name
                in self.aug_config.optional_variables,
                "use_tool_for_format_instructions": self.aug_config.use_tool_for_format_instructions,
                "tool_is_base_model": self.aug_config.tool_is_base_model,
                "force_tool_use": self.aug_config.force_tool_use,
                "force_tool_choice": self.aug_config.force_tool_choice,
                "tool_choice_mode": self.aug_config.tool_choice_mode,
                "structured_output_version": self.aug_config.structured_output_version,
            },
        )

    def _apply_config_params(self):
        """Apply runtime config parameters to the factory instance."""
        # Skip if no config params provided
        if not self.config_params:
            return

        logger.info("Applying runtime config parameters")

        # Track what we're overriding
        override_summary = {}

        # Apply overrides to augLLMConfig for the factory instance
        for param in [
            "temperature",
            "max_tokens",
            "system_message",
            "tools",
            "parse_raw_output",
            "messages_placeholder_name",
            "force_tool_choice",
            "force_tool_use",
            "tool_choice_mode",
            "optional_variables",
            "include_format_instructions",
            "parser_type",
            "pydantic_tools",
            "add_messages_placeholder",
            "force_messages_optional",
            "use_tool_for_format_instructions",
            "structured_output_version",
            "output_field_name",
        ]:
            if param in self.config_params:
                setattr(self.aug_config, param, self.config_params[param])
                override_summary[param] = self.config_params[param]
                logger.debug(f"Overriding {param}: {self.config_params[param]}")

        # Handle partial variables separately (update, don't replace)
        if "partial_variables" in self.config_params:
            self.aug_config.partial_variables.update(
                self.config_params["partial_variables"]
            )
            override_summary["partial_variables"] = "updated"
            logger.debug("Updated partial variables")

        # Ensure messages is in optional variables when required
        if (
            self.aug_config.messages_placeholder_name
            not in self.aug_config.optional_variables
            and self.aug_config.force_messages_optional
        ):
            self.aug_config.optional_variables.append(
                self.aug_config.messages_placeholder_name
            )
            logger.warning(
                f"Added {self.aug_config.messages_placeholder_name} to optional_variables during config param application"
            )

        # Handle prompt modification if system_message was updated
        if "system_message" in self.config_params and self.aug_config.prompt_template:
            self._update_system_message_in_prompt()

        # Update format instructions if needed
        if (
            "include_format_instructions" in self.config_params
            or "structured_output_model" in self.config_params
        ):
            self.aug_config._setup_format_instructions()

        # Process tools if they were updated
        if "tools" in self.config_params or "pydantic_tools" in self.config_params:
            self.aug_config._process_tools()

        # Configure tool choice if settings changed
        if (
            "force_tool_use" in self.config_params
            or "force_tool_choice" in self.config_params
            or "tool_choice_mode" in self.config_params
        ):
            self.aug_config._configure_tool_choice()

        # Apply optional variables if changed
        if "optional_variables" in self.config_params:
            self.aug_config._apply_optional_variables()

        # Apply optional messages placeholder handling if changed
        if any(
            param in self.config_params
            for param in [
                "force_messages_optional",
                "messages_placeholder_name",
                "add_messages_placeholder",
            ]
        ):
            self.aug_config._handle_chat_template_messages_placeholder()

        # Handle BaseModel tools for format instructions if flag was set
        if (
            "use_tool_for_format_instructions" in self.config_params
            and self.config_params["use_tool_for_format_instructions"]
        ):
            self.aug_config._process_tools()

        # Debug summary
        if override_summary:
            logger.debug_table("Applied Runtime Overrides", override_summary)

    def _update_system_message_in_prompt(self):
        """Update system message in prompt template if changed in config params."""
        if not isinstance(self.aug_config.prompt_template, ChatPromptTemplate):
            logger.warning("Not a ChatPromptTemplate - skipping system message update")
            return

        new_system_message = self.aug_config.system_message
        if not new_system_message:
            logger.warning("No system message to update")
            return

        logger.info("Updating system message in prompt template")

        # Build new messages list with updated system message
        new_messages = []
        system_updated = False

        for msg in self.aug_config.prompt_template.messages:
            if hasattr(msg, "role") and msg.role == "system":
                new_messages.append(SystemMessage(content=new_system_message))
                system_updated = True
                logger.success("Replaced existing system message")
            else:
                new_messages.append(msg)

        # Add system message at the beginning if none was updated
        if not system_updated:
            new_messages.insert(0, SystemMessage(content=new_system_message))
            logger.success("Added new system message at beginning")

        # Create new template with updated messages
        partial_vars = getattr(
            self.aug_config.prompt_template, "partial_variables", None
        )
        self.aug_config.prompt_template = ChatPromptTemplate.from_messages(
            new_messages, partial_variables=partial_vars
        )

    def create_runnable(self) -> Runnable:
        """
        Create the complete runnable chain with proper message handling.

        Assembles a fully configured runnable chain based on the AugLLMConfig
        settings and any runtime overrides. This method performs several key steps:
        1. Ensures messages placeholders are properly configured
        2. Initializes the LLM with appropriate parameters
        3. Binds tools to the LLM if specified
        4. Configures structured output handling
        5. Builds the complete chain with prompt templates
        6. Adds pre/post processing functions if specified

        Returns:
            Runnable: A complete, executable LLM chain that can be invoked with
                input data to generate responses.

        Raises:
            ValueError: If the LLM cannot be instantiated from the configuration.

        Examples:
            >>> factory = AugLLMFactory(config)
            >>> runnable = factory.create_runnable()
            >>> response = runnable.invoke("What is the capital of France?")
            >>> print(response)
        """
        logger.info("Creating runnable chain")

        # Final check to ensure messages are optional if required
        if (
            self.aug_config.messages_placeholder_name
            not in self.aug_config.optional_variables
            and self.aug_config.force_messages_optional
        ):
            self.aug_config.optional_variables.append(
                self.aug_config.messages_placeholder_name
            )
            logger.warning(
                f"Added {self.aug_config.messages_placeholder_name} to optional_variables during runnable creation"
            )

        # Force chat templates to have optional messages placeholder if required
        if (
            isinstance(self.aug_config.prompt_template, ChatPromptTemplate)
            and self.aug_config.force_messages_optional
        ):
            self.aug_config._handle_chat_template_messages_placeholder()
            logger.success("Enforced optional messages in chat template")

        # Handle FewShotChatMessagePromptTemplate if present
        elif isinstance(
            self.aug_config.prompt_template, FewShotChatMessagePromptTemplate
        ):
            logger.info("Processing FewShotChatMessagePromptTemplate")
            # Special handling is done in config

        # Initialize LLM with any runtime parameters
        llm_params = {}
        if self.aug_config.temperature is not None:
            llm_params["temperature"] = self.aug_config.temperature
        if self.aug_config.max_tokens is not None:
            llm_params["max_tokens"] = self.aug_config.max_tokens

        # Debug LLM initialization
        logger.debug_table(
            "LLM Initialization",
            {
                "model": self.aug_config.llm_config.model,
                "temperature": self.aug_config.temperature,
                "max_tokens": self.aug_config.max_tokens,
                "override_params": llm_params,
            },
        )

        # Create base LLM
        runnable_llm = self.aug_config.llm_config.instantiate(**llm_params)

        # Make sure we have a valid LLM
        if runnable_llm is None:
            error_msg = "Failed to instantiate LLM from llm_config"
            logger.failure(error_msg)
            raise ValueError(error_msg)

        logger.success("Successfully instantiated base LLM")

        # Add tools if specified
        if self.aug_config.tools:
            runnable_llm = self._initialize_llm_with_tools(runnable_llm)

        # Add structured output handling
        runnable_llm = self._configure_structured_output(runnable_llm)

        # Build the complete chain with prompt template and pre/post processing
        runnable_chain = self._build_chain(runnable_llm)

        # Make sure we have a valid chain
        if runnable_chain is None:
            # If we have no prompt template, just use the LLM as the chain
            runnable_chain = runnable_llm
            logger.warning("No prompt template - using raw LLM as chain")

        # Apply runtime config if any
        if self.aug_config.runtime_options:
            runnable_chain = runnable_chain.with_config(
                **self.aug_config.runtime_options
            )
            logger.info("Applied runtime options to chain")

        logger.success("Successfully created runnable chain")
        return runnable_chain

    def _initialize_llm_with_tools(self, llm: Runnable) -> Runnable:
        """
        Configure LLM with tools based on configuration.

        This method handles the complex process of binding tools to an LLM, including:
        1. Processing different tool types (BaseModel, BaseTool, callables)
        2. Instantiating tool classes as needed
        3. Configuring tool choice mode (auto, required, optional, none)
        4. Handling tool forcing for specific scenarios
        5. Providing fallbacks for different LLM implementations

        Args:
            llm (Runnable): Base LLM runnable to which tools will be bound

        Returns:
            Runnable: LLM with tools configured according to the specifications

        Notes:
            This method implements multiple fallback strategies to maximize
            compatibility with different LLM implementations. It attempts to use
            bind_tools() first, then falls back to with_tools() if needed.
        """
        tools = self.aug_config.tools

        # Check if list is empty
        if not tools:
            logger.warning("No tools to bind - returning LLM unchanged")
            return llm

        logger.progress(f"Binding {len(tools)} tools to LLM")

        # Resolve tool instances if needed
        tool_instances = []
        basemodel_tools = []
        failed_tools = []

        for i, tool in enumerate(tools):
            with logger.track_time(f"Processing tool {i+1}"):
                try:
                    # Case 1: Tool is a BaseModel type for function/schema definition
                    if isinstance(tool, type) and issubclass(tool, BaseModel):
                        basemodel_tools.append(tool)
                        tool_instances.append(
                            tool
                        )  # v2 structured output needs it as a tool
                        logger.success(f"Adding BaseModel {tool.__name__} as tool")

                        # If using v2 structured output, ensure proper field names
                        if (
                            self.aug_config.structured_output_version == "v2"
                            and tool == self.aug_config.structured_output_model
                        ):
                            if self.aug_config.output_field_name and hasattr(
                                tool, "__name__"
                            ):
                                logger.info(
                                    f"Using custom output field: {self.aug_config.output_field_name}"
                                )

                    # Case 2: Tool is a BaseTool instance or needs instantiation
                    elif isinstance(tool, BaseTool) or (
                        isinstance(tool, type) and issubclass(tool, BaseTool)
                    ):
                        # If it's a class, instantiate it
                        if isinstance(tool, type):
                            # Get tool kwargs from config or use empty dict
                            kwargs = self.aug_config.tool_kwargs.get(
                                getattr(tool, "__name__", "Tool"), {}
                            )
                            try:
                                tool_instances.append(tool(**kwargs))
                                logger.success(
                                    f"Instantiated tool {i+1}: {getattr(tool, '__name__', 'Unknown')}"
                                )
                            except Exception as e:
                                logger.failure(
                                    f"Failed to instantiate tool {getattr(tool, '__name__', 'Unknown')}: {e}"
                                )
                                failed_tools.append((tool, str(e)))
                        else:
                            # Already an instance
                            tool_instances.append(tool)
                            tool_class_name = tool.__class__.__name__
                            logger.success(
                                f"Using tool instance {i+1}: {tool_class_name}"
                            )

                    # Case 3: Tool is a string (reference to a tool)
                    elif isinstance(tool, str):
                        # Look up tool by name
                        try:
                            # The import would be from haive.core.engine.tool import ToolRegistry in real code
                            # This is a placeholder - in actual implementation this would be proper registry lookup
                            tool_instance = {
                                "name": tool,
                                "description": f"Mock tool for {tool}",
                            }
                            tool_instances.append(tool_instance)
                            logger.success(f"Resolved tool {i+1}: {tool}")
                        except (ImportError, AttributeError) as e:
                            # Fallback - just skip this tool
                            logger.failure(
                                f"Failed to resolve tool {i+1}: {tool} - {e}"
                            )
                            failed_tools.append(
                                (tool, f"Tool resolution failed: {str(e)}")
                            )
                            continue

                    # Case 4: Callable function
                    elif callable(tool) and not isinstance(tool, type):
                        # Add function name as tool name
                        func_name = getattr(tool, "__name__", "unnamed_function")
                        tool_instances.append(tool)
                        logger.success(f"Added callable tool {i+1}: {func_name}")

                    # Case 5: Other tool types (log warning)
                    else:
                        tool_type = type(tool).__name__
                        logger.warning(f"Unrecognized tool type: {tool_type}")
                        failed_tools.append(
                            (tool, f"Unrecognized tool type: {tool_type}")
                        )
                except Exception as e:
                    logger.error(f"Unexpected error processing tool {i+1}: {e}")
                    failed_tools.append((tool, f"Unexpected error: {str(e)}"))

        # Log any failed tools
        if failed_tools:
            logger.warning(f"Failed to process {len(failed_tools)} tools")
            for failed_tool, error in failed_tools:
                tool_name = getattr(failed_tool, "__name__", str(failed_tool))
                logger.debug(f"  - {tool_name}: {error}")

        # Check if we found any valid tools
        if not tool_instances:
            logger.warning("No valid tools found - returning LLM unchanged")
            return llm

        # Bind tools to the LLM
        bind_kwargs = self.aug_config.bind_tools_kwargs.copy()

        # Set tool_choice based on configuration
        if self.aug_config.force_tool_choice and isinstance(
            self.aug_config.force_tool_choice, str
        ):
            # Force specific tool
            bind_kwargs["tool_choice"] = {
                "type": "function",
                "function": {"name": self.aug_config.force_tool_choice},
            }
            logger.info(f"Forcing specific tool: {self.aug_config.force_tool_choice}")
        elif self.aug_config.tool_choice_mode == "required":
            # Force using any tool
            bind_kwargs["tool_choice"] = "required"
            logger.info("Forcing tool use (any tool)")
        elif self.aug_config.tool_choice_mode == "auto":
            # Auto tool choice
            bind_kwargs["tool_choice"] = "auto"
            logger.info("Setting tool_choice to 'auto'")
        elif self.aug_config.tool_choice_mode == "none":
            # Disable tool usage
            bind_kwargs["tool_choice"] = "none"
            logger.info("Setting tool_choice to 'none' (disabled)")

        # Use bind_tools method if available
        if hasattr(llm, "bind_tools"):
            logger.info(f"Using bind_tools method with {len(tool_instances)} tools")
            try:
                return llm.bind_tools(tool_instances, **bind_kwargs)
            except Exception as e:
                logger.error(f"Error binding tools: {e}")
                # Try with fewer kwargs in case of compatibility issues
                try:
                    # Simplified binding with just tool_choice
                    if "tool_choice" in bind_kwargs:
                        return llm.bind_tools(
                            tool_instances, tool_choice=bind_kwargs["tool_choice"]
                        )
                    else:
                        return llm.bind_tools(tool_instances)
                except Exception as e2:
                    logger.failure(f"Failed simplified tool binding: {e2}")
                    return llm

        # Fallback - try with_tools for OpenAI compatibility
        logger.warning("Falling back to with_tools method")
        if hasattr(llm, "with_tools"):
            try:
                return llm.with_tools(tool_instances, **bind_kwargs)
            except Exception as e:
                logger.error(f"Error with fallback tool binding: {e}")
                # Very simplified binding attempt
                try:
                    return llm.with_tools(tool_instances)
                except Exception as e3:
                    logger.failure(f"Cannot bind tools with minimal args: {e3}")

        # If no tool binding method available, return original LLM with warning
        logger.error("No tool binding method available on LLM")
        return llm

    def _configure_structured_output(self, llm: Runnable) -> Runnable:
        """
        Configure structured output parsing based on configuration.

        This method sets up the structured output handling based on the configuration
        in AugLLMConfig. It supports multiple approaches to structured output:

        1. V1 (Traditional): Uses output parsers (typically PydanticOutputParser) to
           parse the LLM's text output into structured objects
        2. V2 (Tool-based): Uses function/tool calling to get structured output directly
           from the LLM's tool calls without a separate parser
        3. Raw output: Returns the raw text output from the LLM
        4. Custom parsers: Uses custom output parsers specified in the configuration

        The method implements a decision tree to determine the appropriate
        structured output approach based on the configuration settings.

        Args:
            llm (Runnable): The LLM runnable to configure with structured output handling

        Returns:
            Runnable: LLM with structured output handling configured
        """
        logger.info("Configuring structured output")

        # If parse_raw_output is True, use StrOutputParser regardless of other settings
        if self.aug_config.parse_raw_output:
            logger.info("Using StrOutputParser for raw output")
            return llm | StrOutputParser()

        # ✅ FIX: v2 structured output = NO PARSER, just return LLM with bound tools
        if self.aug_config.structured_output_version == "v2":
            logger.info(
                "V2 structured output: tool binding + format instructions (NO PARSER)"
            )
            logger.success("Returning raw LLM to get AIMessage with tool_calls")
            # Tools already bound in _initialize_llm_with_tools()
            # Format instructions already added in config
            # Return raw LLM to get AIMessage with tool_calls
            return llm

        # ✅ Handle v1 structured output with traditional parsing
        elif (
            self.aug_config.structured_output_model
            and self.aug_config.structured_output_version == "v1"
        ):
            logger.info("Using v1 structured output with parsing")

            # Use with_structured_output for best support
            try:
                if hasattr(llm, "with_structured_output"):
                    configured_llm = llm.with_structured_output(
                        self.aug_config.structured_output_model,
                        method="function_calling",  # Explicitly use function_calling
                    )
                    logger.success("Successfully configured v1 structured output")
                    return configured_llm
                else:
                    logger.warning(
                        "with_structured_output not available - falling back to parser"
                    )
            except Exception as e:
                logger.error(f"Failed to configure structured output: {e}")

            # Fallback to PydanticOutputParser for v1
            if self.aug_config.output_parser:
                logger.warning("Using existing output parser for v1")
                return llm | self.aug_config.output_parser
            else:
                logger.warning("Creating PydanticOutputParser for v1")
                parser = PydanticOutputParser(
                    pydantic_object=self.aug_config.structured_output_model
                )
                return llm | parser

        # ✅ Handle explicit pydantic tools (NOT structured output, separate use case)
        elif (
            self.aug_config.pydantic_tools
            and self.aug_config.parser_type == "pydantic_tools"
            and not self.aug_config.structured_output_model
        ):
            logger.info(
                "Using PydanticToolsParser for explicit pydantic tools (not structured output)"
            )
            if isinstance(self.aug_config.output_parser, PydanticToolsParser):
                return llm | self.aug_config.output_parser
            else:
                parser = PydanticToolsParser(tools=self.aug_config.pydantic_tools)
                return llm | parser

        # ✅ Handle custom output parser
        elif self.aug_config.output_parser:
            logger.info(
                f"Using custom output parser: {type(self.aug_config.output_parser).__name__}"
            )
            return llm | self.aug_config.output_parser

        # ✅ Default - no parsing, return raw LLM
        logger.warning("No output parsing configuration - returning raw LLM")
        return llm

    def _build_chain(self, llm: Runnable) -> Runnable:
        """
        Build the complete chain with prompt template and pre/post processing.

        This method assembles the final runnable chain by combining the configured LLM
        with prompt templates and optional pre/post processing functions. It handles
        various prompt template types and ensures proper configuration of messages
        placeholders for chat models.

        The chain assembly follows these steps:
        1. Verify and create prompt template if needed
        2. Connect prompt template to LLM
        3. Add preprocessing if specified
        4. Add postprocessing if specified
        5. Add any custom runnables

        Args:
            llm (Runnable): LLM runnable with tools/output handling already configured

        Returns:
            Runnable: Complete runnable chain ready for execution

        Notes:
            If no prompt template is available, the method returns the raw LLM as the chain.
            For chat models, this method ensures proper handling of system messages and
            messages placeholders according to the configuration.
        """
        logger.info("Building complete chain")

        # If no prompt template, just return the LLM
        if not self.aug_config.prompt_template:
            logger.warning("No prompt template - returning LLM as chain")
            return llm

        # Ensure we have a proper prompt template
        if not self.aug_config.prompt_template and self.aug_config.system_message:
            logger.info("Creating prompt template from system message")
            messages = [SystemMessage(content=self.aug_config.system_message)]

            # Add messages placeholder if needed
            if self.aug_config.add_messages_placeholder:
                # Make messages optional based on config
                is_optional = self.aug_config.force_messages_optional
                messages.append(
                    MessagesPlaceholder(
                        variable_name=self.aug_config.messages_placeholder_name,
                        optional=is_optional,
                    )
                )
                logger.success(f"Added messages placeholder (optional={is_optional})")

            self.aug_config.prompt_template = ChatPromptTemplate.from_messages(messages)

        # If still no prompt template, just return the LLM
        if not self.aug_config.prompt_template:
            logger.warning("Still no prompt template - returning LLM unchanged")
            return llm

        # Create full chain with prompt
        chain = self.aug_config.prompt_template | llm
        logger.success("Created base chain with prompt template")

        # Add preprocessing if specified
        if self.aug_config.preprocess:
            chain = RunnableLambda(self.aug_config.preprocess) | chain
            logger.info("Added preprocessing to chain")

        # Add postprocessing if specified
        if self.aug_config.postprocess:
            chain = chain | RunnableLambda(self.aug_config.postprocess)
            logger.info("Added postprocessing to chain")

        # Add custom runnables if specified
        if self.aug_config.custom_runnables:
            for i, runnable in enumerate(self.aug_config.custom_runnables):
                chain = chain | runnable
                logger.info(f"Added custom runnable {i+1}")

        # Debug final chain composition
        logger.debug_table(
            "Chain Composition",
            {
                "prompt_template_type": type(self.aug_config.prompt_template).__name__,
                "has_preprocess": bool(self.aug_config.preprocess),
                "has_postprocess": bool(self.aug_config.postprocess),
                "custom_runnables": len(self.aug_config.custom_runnables or []),
                "messages_optional": self.aug_config.force_messages_optional,
                "has_format_instructions": "format_instructions"
                in self.aug_config.partial_variables,
                "tool_is_base_model": self.aug_config.tool_is_base_model,
                "structured_output_version": self.aug_config.structured_output_version,
            },
        )

        return chain

    def _generate_schema_instructions(self, model: Type[BaseModel]) -> str:
        """Generate schema-based instructions for a model.

        Args:
            model: The Pydantic model

        Returns:
            Formatted instructions string
        """
        # Get the schema
        schema = model.schema()

        # Format JSON with indentation
        schema_json = json.dumps(schema, indent=2)

        # Format instructions
        return f"""You must format your response as JSON that matches this schema:

```json
{schema_json}
```

The output should be valid JSON that conforms to the {model.__name__} schema.
"""

    def _create_pydantic_model_tool(self, model: Type[BaseModel]) -> BaseTool:
        """Create a tool from a Pydantic model for structured output.

        Args:
            model: The Pydantic model to convert to a tool

        Returns:
            Created tool
        """
        from langchain_core.tools import BaseTool, StructuredTool

        model_name = model.__name__.lower()
        model_description = getattr(
            model, "__doc__", f"Create a {model.__name__} object"
        )

        # Define a function that will validate against the model
        def model_func(**kwargs):
            try:
                # Validate with the model
                result = model(**kwargs)
                # Return as dict for JSON serialization
                return result.dict() if hasattr(result, "dict") else result.model_dump()
            except Exception as e:
                return {"error": f"Failed to create {model_name}: {str(e)}"}

        # Get parameter schema from model
        if hasattr(model, "schema"):
            model.schema().get("properties", {})
        else:
            pass

        # Try to create a structured tool if possible
        try:
            tool = StructuredTool.from_function(
                func=model_func, name=model_name, description=model_description
            )
            return tool
        except Exception as e:
            logger.warning(f"Failed to create structured tool from model: {e}")

            # Fallback to simple BaseTool
            class PydanticModelTool(BaseTool):
                name = model_name
                description = model_description

                def _run(self, **kwargs):
                    return model_func(**kwargs)

                async def _arun(self, **kwargs):
                    return model_func(**kwargs)

            return PydanticModelTool()
