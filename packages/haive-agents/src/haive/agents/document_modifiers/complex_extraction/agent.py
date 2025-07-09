"""Complex Extraction Agent for structured data extraction from text.

This module provides the ComplexExtractionAgent class which implements sophisticated
structured data extraction using validation with retries and optional JSONPatch-based
error correction to reliably extract data according to specified schemas.

The agent supports multiple retry strategies and can handle complex validation
scenarios where initial extraction attempts may fail.

Classes:
    ComplexExtractionAgent: Main agent for complex structured data extraction

Examples:
    Basic usage::

        from haive.agents.document_modifiers.complex_extraction import ComplexExtractionAgent
        from haive.agents.document_modifiers.complex_extraction.config import ComplexExtractionAgentConfig
        from pydantic import BaseModel

        class PersonInfo(BaseModel):
            name: str
            age: int
            occupation: str

        config = ComplexExtractionAgentConfig(
            extraction_model=PersonInfo,
            max_retries=3
        )
        agent = ComplexExtractionAgent(config)

        text = "John Smith is a 35-year-old software engineer."
        result = agent.run(text)
        person_data = result["extracted_data"]

    With JSONPatch error correction::

        config = ComplexExtractionAgentConfig(
            extraction_model=PersonInfo,
            use_jsonpatch=True,
            max_retries=5
        )
        agent = ComplexExtractionAgent(config)
        result = agent.run(complex_text)

See Also:
    - :class:`~haive.agents.document_modifiers.complex_extraction.config.ComplexExtractionAgentConfig`: Configuration class
    - :class:`~haive.agents.document_modifiers.complex_extraction.models.RetryStrategy`: Retry strategy configuration
"""

import logging
from collections.abc import Callable, Sequence
from typing import Any, Dict, List, Optional, Union

from haive.core.engine.agent.agent import Agent, register_agent
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    AnyMessage,
    BaseMessage,
    HumanMessage,
)
from langchain_core.runnables import Runnable, RunnableLambda
from langchain_core.tools import Tool
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ValidationNode
from langgraph.types import Command
from pydantic import BaseModel

from haive.agents.document_modifiers.complex_extraction.config import (
    ComplexExtractionAgentConfig,
)
from haive.agents.document_modifiers.complex_extraction.models import (
    PatchFunctionParameters,
    RetryStrategy,
)
from haive.agents.document_modifiers.complex_extraction.utils import (
    decode,
    default_aggregator,
    encode,
)

logger = logging.getLogger(__name__)


@register_agent(ComplexExtractionAgentConfig)
class ComplexExtractionAgent(Agent[ComplexExtractionAgentConfig]):
    """Agent that extracts complex structured information from text.

    This agent implements sophisticated structured data extraction using validation
    with retries and optional JSONPatch-based error correction to reliably extract
    data according to specified Pydantic schemas.

    The agent creates a validation workflow that can handle complex extraction
    scenarios where initial attempts may fail due to parsing errors, validation
    issues, or incomplete data. It supports multiple retry strategies and can
    automatically correct errors using JSONPatch operations.

    Args:
        config: Configuration object containing extraction settings, model schema,
            retry parameters, and LLM configuration.

    Attributes:
        extraction_model: Pydantic model class defining the extraction schema
        max_retries: Maximum number of retry attempts for failed extractions
        force_tool_choice: Whether to force the LLM to use the extraction tool
        use_jsonpatch: Whether to enable JSONPatch-based error correction
        extraction_tool: Tool instance created from the extraction model
        llm: Language model instance for performing extractions

    Examples:
        Basic structured extraction::

            from pydantic import BaseModel

            class ProductInfo(BaseModel):
                name: str
                price: float
                category: str

            config = ComplexExtractionAgentConfig(
                extraction_model=ProductInfo,
                max_retries=3
            )
            agent = ComplexExtractionAgent(config)

            text = "The MacBook Pro costs $2499 and is a laptop computer."
            result = agent.run(text)
            product = result["extracted_data"]
            # product = {"name": "MacBook Pro", "price": 2499.0, "category": "laptop"}

        With advanced error correction::

            config = ComplexExtractionAgentConfig(
                extraction_model=ProductInfo,
                use_jsonpatch=True,
                max_retries=5,
                force_tool_choice=True
            )
            agent = ComplexExtractionAgent(config)

        Processing multiple documents::

            documents = ["Product A costs $100", "Product B is $200 software"]
            results = [agent.run(doc) for doc in documents]

    Note:
        The agent requires a Pydantic model class to define the extraction schema.
        JSONPatch functionality requires the 'jsonpatch' library to be installed.

    Raises:
        ImportError: If JSONPatch is enabled but the jsonpatch library is not installed
        ValueError: If extraction fails after maximum retry attempts

    See Also:
        - :class:`ComplexExtractionAgentConfig`: Configuration options
        - :class:`RetryStrategy`: Retry strategy configuration
        - :class:`PatchFunctionParameters`: JSONPatch parameter schema
    """

    def __init__(
        self, config: ComplexExtractionAgentConfig = ComplexExtractionAgentConfig()
    ) -> None:
        """Initialize the complex extraction agent.

        Sets up the extraction model, validation tools, and retry mechanisms
        based on the provided configuration.

        Args:
            config: Configuration object containing extraction model, retry settings,
                and LLM configuration. Defaults to a new instance with default values.

        Raises:
            ImportError: If JSONPatch is enabled in config but jsonpatch library
                is not installed.
        """
        self.extraction_model = config.extraction_model
        self.max_retries = config.max_retries
        self.force_tool_choice = config.force_tool_choice
        self.use_jsonpatch = config.use_jsonpatch
        self.extraction_tool = None
        self.extraction_runnable = None
        self.llm = config.llm_config.instantiate()

        # Try importing jsonpatch if needed
        if self.use_jsonpatch:
            try:
                import jsonpatch

                self.jsonpatch = jsonpatch
            except ImportError:
                logger.warning(
                    "jsonpatch library not installed - falling back to regular validation"
                )
                self.use_jsonpatch = False
                self.jsonpatch = None

        # Set up extraction tool if model is provided
        if self.extraction_model:
            self._setup_extraction_tool()

        # Call parent init
        super().__init__(config)
        # self.app = encode | self.app | decode

    def _setup_extraction_tool(self) -> None:
        """Set up the extraction tool based on the provided model.

        Creates a LangChain Tool instance from the Pydantic extraction model
        that can be used by the LLM for structured data extraction.

        The tool is configured with the model's schema as the args_schema,
        allowing the LLM to understand the expected output format.
        """
        if not self.extraction_model:
            logger.warning("No extraction model provided")
            return

        # Create a tool from the extraction model
        extract_name = f"extract_{self.extraction_model.__name__}"

        def extract_func(text: str) -> Dict[str, Any]:
            """Extract structured data according to the schema.

            This is a placeholder function that defines the interface for
            the extraction tool. The actual extraction is performed by the LLM.

            Args:
                text: Input text to extract data from.

            Returns:
                Empty dictionary (placeholder implementation).
            """
            # This is just a placeholder implementation
            # The actual extraction is performed by the LLM
            return {}

        # Create and configure the tool
        extract_data = Tool.from_function(
            func=extract_func,
            name=extract_name,
            description=f"Extract {self.extraction_model.__name__} data from text",
            args_schema=self.extraction_model,
        )

        # Store the tool
        self.extraction_tool = extract_data
        logger.info("Created extraction tool", extra={"tool_name": extract_name})

    def _bind_validator_with_retries(
        self,
        llm: Union[
            Runnable[Sequence[AnyMessage], AIMessage],
            Runnable[Sequence[BaseMessage], BaseMessage],
        ],
        *,
        validator: ValidationNode,
        retry_strategy: RetryStrategy,
        tool_choice: Optional[str] = None,
    ) -> StateGraph:
        """Bind a tool validator with retry logic and return the graph builder.

        Creates a StateGraph that implements validation with retry logic for
        tool calls. The graph includes nodes for message counting, LLM execution,
        validation, fallback handling, and result finalization.

        Args:
            llm: The language model runnable to generate responses. Can be either
                a message-to-AIMessage or message-to-BaseMessage runnable.
            validator: Validation node for checking tool call validity against
                the expected schema.
            retry_strategy: Strategy configuration for handling retries, including
                max attempts, fallback behavior, and message aggregation.
            tool_choice: Optional tool name to force the LLM to use. If specified,
                the LLM will be required to call this specific tool.

        Returns:
            StateGraph builder instance (not compiled). The graph must be compiled
            before use.

        Note:
            The returned graph includes the following nodes:
            - count_messages: Tracks initial message count
            - llm: Primary LLM execution
            - validator: Tool call validation
            - fallback: Fallback LLM for retry attempts
            - finalizer: Result aggregation and finalization
        """
        # Define message merging function

        # Create the state graph
        builder = StateGraph(self.state_schema)

        # Function to extract messages from state
        def dedict(x: Any) -> List[BaseMessage]:
            """Extract messages from state.

            Utility function to extract the messages list from various state formats.

            Args:
                x: State object that may contain messages.

            Returns:
                List of messages extracted from the state.

            Raises:
                ValueError: If messages cannot be extracted from the state.
            """
            if isinstance(x, dict) and "messages" in x:
                return x["messages"]
            if hasattr(x, "messages"):
                return x.messages
            raise ValueError(f"Cannot extract messages from {type(x)}")

        # Define model and fallback nodes
        model = dedict | llm | (lambda msg: {"messages": [msg], "attempt_number": 1})

        # Get fallback runnable
        fbrunnable = retry_strategy.get("fallback")
        if fbrunnable is None:
            fb_runnable = llm
        elif isinstance(fbrunnable, Runnable):
            fb_runnable = fbrunnable
        else:
            fb_runnable = RunnableLambda(fbrunnable)

        fallback = (
            dedict
            | fb_runnable
            | (lambda msg: {"messages": [msg], "attempt_number": 1})
        )

        # Function to count initial messages
        def count_messages(state: Any) -> Dict[str, Any]:
            """Count initial messages in state.

            Tracks the number of messages present at the start of processing
            to distinguish between initial and generated messages.

            Args:
                state: Current workflow state.

            Returns:
                Dictionary with initial_num_messages count.
            """
            if isinstance(state, dict):
                return {"initial_num_messages": len(state.get("messages", []))}
            return {"initial_num_messages": len(getattr(state, "messages", []))}

        # Add nodes to the graph
        builder.add_node("count_messages", count_messages)
        builder.add_node("llm", model)
        builder.add_node("fallback", fallback)

        # Set up message selection and validation
        select_messages = retry_strategy.get("aggregate_messages") or default_aggregator

        def select_generated_messages(state: Any) -> List[BaseMessage]:
            """Select only messages generated in this run.

            Filters out initial messages to return only those generated
            during the current execution.

            Args:
                state: Current workflow state containing messages.

            Returns:
                List of messages generated during this execution.
            """
            if isinstance(state, dict):
                selected = state["messages"][state["initial_num_messages"] :]
            else:
                selected = state.messages[state.initial_num_messages :]
            return [select_messages(selected)]

        def endict_validator_output(x: Sequence[AnyMessage]) -> Dict[str, Any]:
            """Format validator output for the graph.

            Converts validator output into the expected state format,
            handling cases where validation fails.

            Args:
                x: Sequence of messages from the validator.

            Returns:
                Dictionary containing formatted messages for the workflow.
            """
            if tool_choice and not x:
                return {
                    "messages": [
                        HumanMessage(
                            content=f"ValidationError: please respond with a valid tool call [tool_choice={tool_choice}].",
                            additional_kwargs={"is_error": True},
                        )
                    ]
                }
            return {"messages": x}

        # Create validator node
        validator_runnable = (
            select_generated_messages | validator | endict_validator_output
        )
        builder.add_node("validator", validator_runnable)

        # Define finalizer class
        class Finalizer:
            """Select final message to return."""

            def __init__(self, aggregator: Callable[[list], AIMessage] | None = None):
                self._aggregator = aggregator or default_aggregator

            def __call__(self, state: Any) -> dict:
                """Return the aggregated message."""
                if isinstance(state, dict):
                    initial_num_messages = state["initial_num_messages"]
                    generated_messages = state["messages"][initial_num_messages:]
                else:
                    initial_num_messages = state.initial_num_messages
                    generated_messages = state.messages[initial_num_messages:]

                return Command(
                    update={
                        "messages": {
                            "finalize": self._aggregator(generated_messages),
                        }
                    }
                )

        # Add finalizer node
        builder.add_node(
            "finalizer", Finalizer(retry_strategy.get("aggregate_messages"))
        )
        builder.add_node("encode", encode)
        builder.add_node("decode", decode)
        # Define graph connectivity
        builder.add_edge(START, "encode")
        builder.add_edge("encode", "count_messages")
        builder.add_edge("count_messages", "llm")
        # builder.add_edge("llm", "decode")
        # builder.add_edge("decode", "finalizer")
        builder.add_edge("finalizer", "decode")
        builder.add_edge("decode", END)

        # Define routing functions
        def route_validator(state: Any) -> str:
            """Decide whether to run validation.

            Determines if the current state requires validation based on
            the presence of tool calls in the last message.

            Args:
                state: Current workflow state.

            Returns:
                Next node name: 'validator' if validation needed, END otherwise.
            """
            messages = state["messages"] if isinstance(state, dict) else state.messages
            if not messages:
                return END

            last_msg = messages[-1]
            has_tool_calls = (
                hasattr(last_msg, "tool_calls") and last_msg.tool_calls
            ) or (isinstance(last_msg, dict) and last_msg.get("tool_calls"))

            if has_tool_calls or tool_choice is not None:
                return "validator"
            return END

        def route_validation(state: Any) -> str:
            """Route based on validation result.

            Determines the next step based on validation outcome and retry count.
            Can route to fallback for retry attempts or finalizer for completion.

            Args:
                state: Current workflow state with validation results.

            Returns:
                Next node name: 'finalizer' for success, 'fallback' for retry.

            Raises:
                ValueError: If maximum retry attempts are exceeded.
            """
            max_attempts = retry_strategy.get("max_attempts", 3)
            attempt_num = (
                state["attempt_number"]
                if isinstance(state, dict)
                else state.attempt_number
            )

            if attempt_num > max_attempts:
                raise ValueError(
                    f"Could not extract a valid value in {max_attempts} attempts."
                )

            messages = state["messages"] if isinstance(state, dict) else state.messages
            for m in messages[::-1]:
                if m.type == "ai":
                    break
                if hasattr(m, "additional_kwargs") and m.additional_kwargs.get(
                    "is_error"
                ):
                    return "fallback"
            return "finalizer"

        # Add conditional edges
        builder.add_conditional_edges("llm", route_validator, ["validator", END])
        builder.add_edge("fallback", "validator")
        builder.add_conditional_edges(
            "validator", route_validation, ["finalizer", "fallback"]
        )
        # builder.add_edge("finalizer", END)

        # Return the builder (not compiled)
        return builder

    def bind_validator_with_jsonpatch_retries(
        self,
        llm: BaseChatModel,
        *,
        tools: List[Tool],
        tool_choice: Optional[str] = None,
        max_attempts: int = 3,
    ) -> StateGraph:
        """Bind a validator with JSONPatch-based retries.

        Creates an advanced validation workflow that uses JSONPatch operations
        to automatically correct validation errors. When a tool call fails
        validation, the system generates patch instructions to fix the errors.

        Args:
            llm: The base language model to use for extraction and error correction.
            tools: List of tools available for extraction. The validation will
                ensure tool calls conform to these tool schemas.
            tool_choice: Optional specific tool name to force the LLM to use.
                If specified, the LLM must use this tool.
            max_attempts: Maximum number of retry attempts before giving up.
                Defaults to 3.

        Returns:
            StateGraph builder instance (not compiled). Must be compiled before use.

        Raises:
            ImportError: If the jsonpatch library is not installed but JSONPatch
                functionality is requested.

        Note:
            This method creates a sophisticated retry mechanism where:
            1. Initial extraction attempts use the primary LLM
            2. Validation errors trigger JSONPatch correction attempts
            3. Patch operations are applied to fix specific validation issues
            4. Multiple correction iterations are supported up to max_attempts
        """
        # Ensure jsonpatch is available
        if not self.jsonpatch:
            raise ImportError(
                "The 'jsonpatch' library is required for JSONPatch-based retries."
            )

        # Create bound LLMs
        bound_llm = llm.bind_tools(tools, tool_choice=tool_choice)
        fallback_llm = llm.bind_tools([PatchFunctionParameters])

        # Define message aggregation function
        def aggregate_messages(messages: Sequence[AnyMessage]) -> AIMessage:
            """Aggregate messages with JSONPatch corrections.

            Processes a sequence of AI messages and applies JSONPatch operations
            to correct tool call arguments, creating a final corrected message.

            Args:
                messages: Sequence of messages containing tool calls and patches.

            Returns:
                Single AIMessage with corrected and aggregated tool calls.

            Note:
                This function identifies JSONPatch tool calls and applies them
                to previously generated tool calls to fix validation errors.
            """
            # Get all the AI messages and apply json patches
            resolved_tool_calls = {}
            content = ""

            for m in messages:
                if m.type != "ai":
                    continue

                if not content:
                    content = m.content

                if not hasattr(m, "tool_calls"):
                    continue

                for tc in m.tool_calls:
                    if tc.get("name") == PatchFunctionParameters.__name__:
                        # Get target tool call ID
                        tcid = tc.get("args", {}).get("tool_call_id")
                        if tcid not in resolved_tool_calls:
                            logger.debug(
                                "JsonPatch tool call ID not found",
                                extra={
                                    "tool_call_id": tcid,
                                    "valid_ids": list(resolved_tool_calls.keys()),
                                },
                            )
                            # Fallback to first available tool call
                            tcid = next(iter(resolved_tool_calls.keys()), None)
                            if not tcid:
                                continue

                        # Get original tool call and apply patches
                        orig_tool_call = resolved_tool_calls[tcid]
                        current_args = orig_tool_call.get("args", {})
                        patches = tc.get("args", {}).get("patches", [])

                        try:
                            # Apply JSON patches
                            orig_tool_call["args"] = self.jsonpatch.apply_patch(
                                current_args,
                                patches,
                            )
                            # Update ID to latest
                            orig_tool_call["id"] = tc["id"]
                        except Exception as e:
                            logger.error(
                                "Error applying JSONPatch",
                                extra={"error": str(e)},
                                exc_info=True,
                            )
                    else:
                        # Regular tool call - add to resolved list
                        resolved_tool_calls[tc["id"]] = tc.copy()

            # Create final AI message with resolved tool calls
            return AIMessage(
                content=content,
                tool_calls=list(resolved_tool_calls.values()),
            )

        # Create format error function
        def format_exception(
            error: BaseException, call: Dict[str, Any], schema: type[BaseModel]
        ) -> str:
            """Format validation error for JSONPatch correction.

            Creates a detailed error message that includes the validation error,
            expected schema, and instructions for generating JSONPatch corrections.

            Args:
                error: The validation exception that occurred.
                call: The tool call that failed validation.
                schema: The expected schema (Pydantic model) for the tool.

            Returns:
                Formatted error message with correction instructions.
            """
            schema_json = (
                schema.schema_json() if hasattr(schema, "schema_json") else str(schema)
            )
            return (
                f"Error:\n\n```\n{error!r}\n```\n"
                "Expected Parameter Schema:\n\n" + f"```json\n{schema_json}\n```\n"
                f"Please respond with a JSONPatch to correct the error for tool_call_id=[{call.get('id', 'unknown')}]."
            )

        # Create validator and retry strategy
        validator = ValidationNode(
            tools + [PatchFunctionParameters],
            format_error=format_exception,
        )

        retry_strategy = RetryStrategy(
            max_attempts=max_attempts,
            fallback=fallback_llm,
            aggregate_messages=aggregate_messages,
        )

        # Return the graph builder
        return self._bind_validator_with_retries(
            bound_llm,
            validator=validator,
            retry_strategy=retry_strategy,
            tool_choice=tool_choice,
        )

    def bind_validator_with_retries(
        self,
        llm: BaseChatModel,
        *,
        tools: List[Tool],
        tool_choice: Optional[str] = None,
        max_attempts: int = 3,
    ) -> StateGraph:
        """Bind a validator with standard retries (no JSONPatch).

        Creates a basic validation workflow with simple retry logic. When
        validation fails, the system will retry the extraction up to the
        maximum number of attempts without advanced error correction.

        Args:
            llm: The base language model to use for extraction attempts.
            tools: List of tools available for extraction. Tool calls will be
                validated against these tool schemas.
            tool_choice: Optional specific tool name to force the LLM to use.
                If specified, the LLM must call this tool.
            max_attempts: Maximum number of retry attempts before failing.
                Defaults to 3.

        Returns:
            StateGraph builder instance (not compiled). Must be compiled before use.

        Note:
            This is the simpler alternative to JSONPatch-based retries. It will
            simply retry failed extractions without attempting to automatically
            correct validation errors.
        """
        bound_llm = llm.bind_tools(tools, tool_choice=tool_choice)
        retry_strategy = RetryStrategy(max_attempts=max_attempts)
        validator = ValidationNode(tools)

        # Return the graph builder without compiling
        return self._bind_validator_with_retries(
            bound_llm,
            validator=validator,
            tool_choice=tool_choice,
            retry_strategy=retry_strategy,
        )

    def setup_workflow(self) -> None:
        """Set up the agent workflow.

        Initializes the extraction workflow graph based on the agent configuration.
        This method creates the appropriate validation and retry mechanism (either
        JSONPatch-based or standard retries) and configures the processing pipeline.

        The workflow includes encoding/decoding steps, validation nodes, and
        state management for tracking extraction progress.

        Note:
            This method is called automatically when needed and does not need
            to be invoked manually. The workflow graph is not compiled here -
            compilation happens in the parent class.
        """
        logger.info(
            "Setting up workflow for ComplexExtractionAgent",
            extra={"agent_name": self.config.name},
        )

        # Create a state wrapper to pass configuration to the decoder
        def state_wrapper(state: Any) -> Any:
            """Attach configuration to state for downstream processing.

            Args:
                state: Current workflow state.

            Returns:
                State with attached configuration.
            """
            # Attach the config to the state for use in decode
            state.config = self.config
            return state

        # Add state_wrapper node to the graph before decode
        self.graph = self.bind_validator_with_jsonpatch_retries(
            self.llm, tools=[self.extraction_tool]
        )
        # Add the state wrapper before decode
        if hasattr(self.graph, "add_node") and hasattr(self.graph, "add_edge"):
            # Add state wrapper node
            self.graph.add_node("state_wrapper", state_wrapper)
            # Reroute finalizer to state_wrapper and state_wrapper to decode
            # Remove the edge from finalizer to decode
            if hasattr(self.graph, "_edges") and "finalizer" in self.graph._edges:
                if "decode" in self.graph._edges["finalizer"]:
                    self.graph._edges["finalizer"].remove("decode")
                self.graph._edges["finalizer"].append("state_wrapper")
                self.graph.add_edge("state_wrapper", "decode")
        # self.app = deddict
        # Note: We don't compile the graph here - that's done by the parent in compile()

    def extract_node(self, state: Any) -> Dict[str, Any]:
        """Main extraction node function.

        Processes the current state through the extraction pipeline, invoking
        the configured extraction tool and handling the results.

        Args:
            state: Current workflow state containing messages and other context.
                Can be either a dictionary with 'messages' key or an object
                with messages attribute.

        Returns:
            Updated state dictionary containing:
            - extracted_data: The structured data extracted by the tool
            - messages: Updated message list including extraction results
            - error: Error message if extraction failed

        Note:
            This method handles various state formats and gracefully manages
            errors during extraction. If no extraction runnable is available,
            the state is passed through unchanged.
        """
        # Check if we have the extraction runnable
        if hasattr(self, "extraction_runnable") and self.extraction_runnable:
            try:
                # Get messages from state
                if isinstance(state, dict) and "messages" in state:
                    messages = state["messages"]
                elif hasattr(state, "messages"):
                    messages = state.messages
                else:
                    # No messages found
                    return {"error": "No messages found in state"}

                if not messages:
                    # No messages to process
                    return state

                # Invoke the extraction runnable
                result = self.extraction_runnable.invoke(messages)

                # Extract data from the result
                extracted_data = None
                if hasattr(result, "tool_calls") and result.tool_calls:
                    for tool_call in result.tool_calls:
                        if tool_call.get("name") == self.extraction_tool.name:
                            extracted_data = tool_call.get("args", {})
                            break

                # Return updated state
                updates = {"extracted_data": extracted_data}

                # Add result message if it's not already in messages
                if hasattr(result, "content") or hasattr(result, "tool_calls"):
                    if isinstance(state, dict):
                        updated_messages = list(state.get("messages", []))
                        updated_messages.append(result)
                        updates["messages"] = updated_messages
                    else:
                        updates["messages"] = list(state.messages) + [result]

                return updates
            except Exception as e:
                # Log error and return error in state
                logger.error(
                    "Error in extraction node", extra={"error": str(e)}, exc_info=True
                )
                return {"error": str(e)}

        # If we don't have the extraction runnable, just pass through
        return state

    def run(
        self, input_data: Union[str, List[str], Dict[str, Any], BaseModel], **kwargs
    ) -> Dict[str, Any]:
        """Run the extraction agent on input data.

        Processes the input through the extraction pipeline, handling various
        input formats and returning structured extraction results.

        Args:
            input_data: Input text or data to extract information from. Supports:
                - str: Single text document
                - List[str]: Multiple text documents to process together
                - Dict[str, Any]: Dictionary with 'text', 'content', or 'messages' keys
                - BaseModel: Pydantic model with text content
            **kwargs: Additional runtime configuration options passed to the
                underlying workflow execution.

        Returns:
            Dictionary containing extraction results:
            - extracted_data: Structured data conforming to the extraction model
            - messages: Full conversation history during extraction
            - Additional metadata from the extraction process

        Example:
            Basic text extraction::

                agent = ComplexExtractionAgent(config)
                result = agent.run("John Smith is 30 years old.")
                person_data = result["extracted_data"]

            Multiple documents::

                docs = ["Person A info", "Person B info"]
                result = agent.run(docs)

        Note:
            If no extraction workflow has been set up, this method will
            automatically call setup_workflow() before processing.
        """
        # Ensure we have a validation workflow
        if (
            hasattr(self, "extraction_model")
            and self.extraction_model
            and not hasattr(self, "extraction_runnable")
        ):
            self.setup_workflow()

        # Convert input data to messages
        if isinstance(input_data, str) or (
            isinstance(input_data, list) and all(isinstance(i, str) for i in input_data)
        ):
            # messages = self._prepare_extraction_messages(input_data)

            # Create state with messages
            # input_state = {
            ##    "messages": messages
            # }

            # Run the graph with the input state
            result = super().run(input_data, **kwargs)
        else:
            # Use parent run method for complex inputs
            result = super().run(input_data, **kwargs)

        # Try to extract data from messages if not already in result
        if "extracted_data" not in result or not result.get("extracted_data"):
            extracted_data = None
            if "messages" in result:
                for message in reversed(result["messages"]):
                    if hasattr(message, "tool_calls") and message.tool_calls:
                        for tool_call in message.tool_calls:
                            if (
                                hasattr(self, "extraction_tool")
                                and tool_call.get("name") == self.extraction_tool.name
                            ):
                                extracted_data = tool_call.get("args", {})
                                break
                if extracted_data:
                    result["extracted_data"] = extracted_data

        return result

    # def compile(self):
    # self.app = dec
    def _prepare_extraction_messages(
        self, input_data: Union[str, List[str], Dict[str, Any], BaseModel]
    ) -> List[BaseMessage]:
        """Prepare messages for extraction.

        Converts various input formats into a standardized list of BaseMessage
        objects that can be processed by the extraction workflow.

        Args:
            input_data: Input data in various formats:
                - str: Single text to extract from
                - List[str]: Multiple texts to combine
                - Dict[str, Any]: Dictionary with text content
                - BaseModel: Pydantic model with extractable content
                - BaseMessage or List[BaseMessage]: Pre-formatted messages

        Returns:
            List of BaseMessage objects formatted for extraction. The messages
            include appropriate prompts that instruct the LLM to extract data
            according to the configured extraction model.

        Note:
            This method handles various edge cases and fallback scenarios to
            ensure robust message preparation regardless of input format.
        """
        # Handle string input
        if isinstance(input_data, str):
            return [
                HumanMessage(
                    content=f"Extract {self.extraction_model.__name__} from the following text:\n\n{input_data}"
                )
            ]

        # Handle list of strings
        if isinstance(input_data, list) and all(
            isinstance(item, str) for item in input_data
        ):
            combined = "\n".join(input_data)
            return [
                HumanMessage(
                    content=f"Extract {self.extraction_model.__name__} from the following text:\n\n{combined}"
                )
            ]

        # Handle BaseMessage
        if isinstance(input_data, BaseMessage):
            return [input_data]

        # Handle list of BaseMessages
        if isinstance(input_data, list) and all(
            isinstance(item, BaseMessage) for item in input_data
        ):
            return input_data

        # Handle dict
        if isinstance(input_data, dict):
            # Check if messages field is present
            if "messages" in input_data:
                messages = input_data["messages"]
                if isinstance(messages, list):
                    return messages

            # Check for text or content fields
            content = input_data.get("text") or input_data.get("content")
            if content:
                return [
                    HumanMessage(
                        content=f"Extract {self.extraction_model.__name__} from the following text:\n\n{content}"
                    )
                ]

        # Handle BaseModel
        elif isinstance(input_data, BaseModel):
            # Try to convert to dict
            if hasattr(input_data, "model_dump"):
                model_dict = input_data.model_dump()
            elif hasattr(input_data, "dict"):
                model_dict = input_data.dict()
            else:
                model_dict = {
                    attr: getattr(input_data, attr)
                    for attr in input_data.__annotations__
                }

            # Check for text content
            content = model_dict.get("text") or model_dict.get("content")
            if content:
                return [
                    HumanMessage(
                        content=f"Extract {self.extraction_model.__name__} from the following text:\n\n{content}"
                    )
                ]

        # Default case - convert to string
        return [
            HumanMessage(
                content=f"Extract {self.extraction_model.__name__} from the following:\n\n{input_data!s}"
            )
        ]
