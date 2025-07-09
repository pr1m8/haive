# src/haive/core/graph/node/factory.py

import asyncio
import inspect
import logging
from typing import Any, Callable, Dict, Optional

from langgraph.graph import END
from langgraph.prebuilt import ToolNode, ValidationNode
from langgraph.types import Command, Send
from pydantic import BaseModel

from haive.core.engine.base import InvokableEngine, NonInvokableEngine
from haive.core.graph.node.config import NodeConfig
from haive.core.graph.node.types import NodeType

logger = logging.getLogger(__name__)


class NodeFactory:
    """
    Factory for creating node functions from configurations.

    This class provides methods for creating different types of node functions
    based on their configuration, engine type, or specialized functionality.
    """

    @classmethod
    def create_node_function(cls, config: NodeConfig) -> Callable:
        """
        Create a node function from a node configuration.

        Args:
            config: NodeConfig with all node configuration

        Returns:
            A callable node function for use in LangGraph
        """
        # Get engine
        engine, engine_id = config.get_engine()

        # Handle based on node type
        if config.node_type == NodeType.TOOL:
            return cls._create_tool_node(config)
        elif config.node_type == NodeType.VALIDATION:
            return cls._create_validation_node(config)
        # elif config.node_type == NodeType.BRANCH:
        # return cls._create_branch_node(config)
        # elif config.node_type == NodeType.SEND:
        # return cls._create_send_node(config)
        elif isinstance(engine, InvokableEngine):
            return cls._create_invokable_engine_node(config, engine, engine_id)
        elif isinstance(engine, NonInvokableEngine):
            return cls._create_non_invokable_engine_node(config, engine, engine_id)
        elif callable(engine):
            return cls._create_callable_node(config, engine)
        else:
            return cls._create_generic_node(config, engine)

    @classmethod
    def _create_invokable_engine_node(
        cls, config: NodeConfig, engine: InvokableEngine, engine_id: Optional[str]
    ) -> Callable:
        """
        Create a node function for an invokable engine.

        Args:
            config: Node configuration
            engine: Invokable engine
            engine_id: Optional engine ID

        Returns:
            Node function
        """
        # Core info
        command_goto = config.command_goto
        input_mapping = config.get_input_mapping()
        output_mapping = config.get_output_mapping()

        # Get engine-specific ID or name for lookup
        engine_id = (
            engine_id or getattr(engine, "name", None) or getattr(engine, "id", None)
        )

        def node_function(state, config=None):
            """Node function that uses engine's invoke method."""
            try:
                # Extract input from state using the fixed _extract_input method
                input_data = cls._extract_input(state, input_mapping, engine_id)
                # print(engine.prompt_template)
                # breakpoint()
                # Create a fresh runnable with appropriate config
                runnable = engine.create_runnable()
                print(runnable)

                # Invoke the runnable
                result = runnable.invoke(input_data)
                print(result)
                print(output_mapping)
                print(type(result))

                # print()
                logger.debug(f"Result: {result}")
                # Process output using the fixed _process_output method - ONLY PASS 2 REQUIRED ARGS
                processed_output = cls._process_output(result, output_mapping)

                # Handle structured output models (special case)
                if (
                    hasattr(engine, "structured_output_model")
                    and engine.structured_output_model
                ):
                    model_name = engine.structured_output_model.__name__.lower()
                    # If result is the model instance, ensure it's correctly mapped
                    if isinstance(result, engine.structured_output_model):
                        # Check if already properly placed
                        if model_name not in processed_output:
                            processed_output[model_name] = result

                # Return with Command for routing
                return Command(update=processed_output, goto=command_goto)
            except Exception as e:
                logger.error(f"Error in node {engine_id or 'unknown'}: {e}")
                return Command(update={"error": str(e)}, goto=command_goto)

        # Add metadata
        node_function.__node_config__ = config
        node_function.__engine_id__ = engine_id

        return node_function

    @classmethod
    def _create_non_invokable_engine_node(
        cls, config: NodeConfig, engine: NonInvokableEngine, engine_id: Optional[str]
    ) -> Callable:
        """
        Create a node function for a non-invokable engine.

        Args:
            config: Node configuration
            engine: Non-invokable engine
            engine_id: Optional engine ID

        Returns:
            Node function
        """
        # Core info
        command_goto = config.command_goto
        input_mapping = config.get_input_mapping()
        output_mapping = config.get_output_mapping()

        # Get input/output mappings from schema if empty
        if not input_mapping and config.input_schema:
            input_fields = config.input_schema.model_fields.keys()
            input_mapping = {field: field for field in input_fields}

        if not output_mapping and config.output_schema:
            output_fields = config.output_schema.model_fields.keys()
            output_mapping = {field: field for field in output_fields}

        def node_function(state, config=None):
            """Node function that instantiates the engine."""
            try:
                # Extract input from state
                cls._extract_input(state, input_mapping)

                # Just instantiate the engine
                instance = engine.instantiate(config)

                # Return the instance with Command for routing
                processed_output = {"instance": instance}
                if output_mapping:
                    mapped_output = {}
                    for output_key, state_key in output_mapping.items():
                        if output_key in processed_output:
                            mapped_output[state_key] = processed_output[output_key]
                    if mapped_output:
                        processed_output = mapped_output

                return Command(update=processed_output, goto=command_goto)
            except Exception as e:
                logger.error(
                    f"Error in non-invokable node {engine_id or 'unknown'}: {e}"
                )
                return Command(update={"error": str(e)}, goto=command_goto)

        # Add metadata
        node_function.__node_config__ = config
        node_function.__engine_id__ = engine_id

        return node_function

    @classmethod
    def _create_callable_node(cls, config: NodeConfig, func: Callable) -> Callable:
        """
        Create a node function from a callable.

        Args:
            config: Node configuration
            func: Callable function

        Returns:
            Node function
        """
        # Core info
        command_goto = config.command_goto
        input_mapping = config.get_input_mapping()
        output_mapping = config.get_output_mapping()

        # Get input/output mappings from schema if empty
        if not input_mapping and config.input_schema:
            input_fields = config.input_schema.model_fields.keys()
            input_mapping = {field: field for field in input_fields}

        if not output_mapping and config.output_schema:
            output_fields = config.output_schema.model_fields.keys()
            output_mapping = {field: field for field in output_fields}

        # Check if function is async
        is_async = inspect.iscoroutinefunction(func)

        # Check if function accepts config
        accepts_config = False
        try:
            sig = inspect.signature(func)
            accepts_config = "config" in sig.parameters
        except (ValueError, TypeError):
            # Can't inspect signature - assume no config
            pass

        def node_function(state, config=None):
            """Node function for callable."""
            try:
                # Extract input from state
                input_data = cls._extract_input(state, input_mapping)

                # Call function with or without config
                if accepts_config:
                    if is_async:
                        # Run async function in event loop
                        loop = asyncio.get_event_loop()
                        result = loop.run_until_complete(func(input_data, config))
                    else:
                        result = func(input_data, config)
                else:
                    if is_async:
                        # Run async function in event loop
                        loop = asyncio.get_event_loop()
                        result = loop.run_until_complete(func(input_data))
                    else:
                        result = func(input_data)

                # Handle result that's already a Command or Send
                if isinstance(result, (Command, Send)) or (
                    isinstance(result, list)
                    and all(isinstance(item, Send) for item in result)
                ):
                    return result

                # Process output
                processed_output = cls._process_output(result, output_mapping)

                # Return with Command for routing
                return Command(update=processed_output, goto=command_goto)
            except Exception as e:
                logger.error(f"Error in callable node: {e}")
                return Command(update={"error": str(e)}, goto=command_goto)

        # Add async support if function is async
        if is_async:

            async def async_node_function(state, config=None):
                """Async node function for callable."""
                try:
                    # Extract input from state
                    input_data = cls._extract_input(state, input_mapping)

                    # Call function with or without config
                    if accepts_config:
                        result = await func(input_data, config)
                    else:
                        result = await func(input_data)

                    # Handle result that's already a Command or Send
                    if isinstance(result, (Command, Send)) or (
                        isinstance(result, list)
                        and all(isinstance(item, Send) for item in result)
                    ):
                        return result

                    # Process output
                    processed_output = cls._process_output(result, output_mapping)

                    # Return with Command for routing
                    return Command(update=processed_output, goto=command_goto)
                except Exception as e:
                    logger.error(f"Error in async callable node: {e}")
                    return Command(update={"error": str(e)}, goto=command_goto)

            # Set async invoke method
            node_function.ainvoke = async_node_function

        # Add metadata
        node_function.__node_config__ = config

        return node_function

    @classmethod
    def _create_tool_node(cls, config: NodeConfig) -> Callable:
        """
        Create a tool node function.

        Args:
            config: Node configuration

        Returns:
            Tool node function
        """
        if not config.tools:
            raise ValueError("Tool node requires tools")

        # Create a ToolNode
        tool_node = ToolNode(
            tools=config.tools,
            name=config.name,
            handle_tool_errors=config.handle_tool_errors,
            messages_key=config.messages_field or "messages",
        )

        # Core info
        command_goto = config.command_goto
        input_mapping = config.get_input_mapping()
        output_mapping = config.get_output_mapping()

        # Get input/output mappings from schema if empty
        if not input_mapping and config.input_schema:
            input_fields = config.input_schema.model_fields.keys()
            input_mapping = {field: field for field in input_fields}

        if not output_mapping and config.output_schema:
            output_fields = config.output_schema.model_fields.keys()
            output_mapping = {field: field for field in output_fields}

        def node_function(state, config=None):
            """Node function for tool node."""
            try:
                # Extract input from state
                input_data = cls._extract_input(state, input_mapping)

                # Invoke the tool node
                result = tool_node.invoke(input_data, config)

                # If result is already a Command or Send, return it
                if isinstance(result, (Command, Send)) or (
                    isinstance(result, list)
                    and all(isinstance(item, Send) for item in result)
                ):
                    # If Command but no goto, add our goto
                    if (
                        isinstance(result, Command)
                        and result.goto is None
                        and command_goto is not None
                    ):
                        return Command(
                            update=result.update,
                            goto=command_goto,
                            resume=result.resume,
                            graph=result.graph,
                        )
                    return result

                # Process output
                processed_output = cls._process_output(result, output_mapping)

                # Return with Command for routing
                return Command(update=processed_output, goto=command_goto)
            except Exception as e:
                logger.error(f"Error in tool node: {e}")
                return Command(update={"error": str(e)}, goto=command_goto)

        # Add async support if tool node supports it
        if hasattr(tool_node, "ainvoke"):

            async def async_node_function(state, config=None):
                """Async node function for tool node."""
                try:
                    # Extract input from state
                    input_data = cls._extract_input(state, input_mapping)

                    # Invoke the tool node
                    result = await tool_node.ainvoke(input_data, config)

                    # If result is already a Command or Send, return it
                    if isinstance(result, (Command, Send)) or (
                        isinstance(result, list)
                        and all(isinstance(item, Send) for item in result)
                    ):
                        # If Command but no goto, add our goto
                        if (
                            isinstance(result, Command)
                            and result.goto is None
                            and command_goto is not None
                        ):
                            return Command(
                                update=result.update,
                                goto=command_goto,
                                resume=result.resume,
                                graph=result.graph,
                            )
                        return result

                    # Process output
                    processed_output = cls._process_output(result, output_mapping)

                    # Return with Command for routing
                    return Command(update=processed_output, goto=command_goto)
                except Exception as e:
                    logger.error(f"Error in async tool node: {e}")
                    return Command(update={"error": str(e)}, goto=command_goto)

            # Set async invoke method
            node_function.ainvoke = async_node_function

        # Add metadata
        node_function.__node_config__ = config

        return node_function

    @classmethod
    def _create_validation_node(cls, config: NodeConfig) -> Callable:
        """
        Create a validation node function.

        Args:
            config: Node configuration

        Returns:
            Validation node function
        """
        if not config.validation_schemas:
            raise ValueError("Validation node requires validation schemas")

        # Create a ValidationNode
        validation_node = ValidationNode(
            schemas=config.validation_schemas,
            name=config.name,
            messages_key=config.messages_field or "messages",
        )

        # Core info
        command_goto = config.command_goto
        input_mapping = config.get_input_mapping()
        output_mapping = config.get_output_mapping()

        # Get input/output mappings from schema if empty
        if not input_mapping and config.input_schema:
            input_fields = config.input_schema.model_fields.keys()
            input_mapping = {field: field for field in input_fields}

        if not output_mapping and config.output_schema:
            output_fields = config.output_schema.model_fields.keys()
            output_mapping = {field: field for field in output_fields}

        def node_function(state, config=None):
            """Node function for validation node."""
            try:
                # Extract input from state
                input_data = cls._extract_input(state, input_mapping)

                # Invoke the validation node
                result = validation_node.invoke(input_data, config)

                # If result is already a Command or Send, return it
                if isinstance(result, (Command, Send)) or (
                    isinstance(result, list)
                    and all(isinstance(item, Send) for item in result)
                ):
                    # If Command but no goto, add our goto
                    if (
                        isinstance(result, Command)
                        and result.goto is None
                        and command_goto is not None
                    ):
                        return Command(
                            update=result.update,
                            goto=command_goto,
                            resume=result.resume,
                            graph=result.graph,
                        )
                    return result

                # Process output
                processed_output = cls._process_output(result, output_mapping)

                # Return with Command for routing
                return Command(update=processed_output, goto=command_goto)
            except Exception as e:
                logger.error(f"Error in validation node: {e}")
                return Command(update={"error": str(e)}, goto=command_goto)

        # Add metadata
        node_function.__node_config__ = config

        return node_function

    @classmethod
    def _create_branch_node(cls, config: NodeConfig) -> Callable:
        """
        Create a branch node function.

        Args:
            config: Node configuration

        Returns:
            Branch node function
        """
        # Get condition function
        condition = config.condition
        if condition is None and config.condition_ref:
            try:
                module_name, func_name = config.condition_ref.rsplit(".", 1)
                module = __import__(module_name, fromlist=[func_name])
                condition = getattr(module, func_name)
            except (ValueError, ImportError, AttributeError) as e:
                logger.error(f"Error importing condition function: {e}")
                raise ValueError(f"Could not resolve condition function: {e}")

        if not condition or not config.routes:
            raise ValueError("Branch node requires condition function and routes")

        # Core info
        input_mapping = config.get_input_mapping()
        routes = config.routes

        # Get input mapping from schema if empty
        if not input_mapping and config.input_schema:
            input_fields = config.input_schema.model_fields.keys()
            input_mapping = {field: field for field in input_fields}

        def node_function(state, config=None):
            """Node function for branch node."""
            try:
                # Extract input from state
                input_data = cls._extract_input(state, input_mapping)

                # Call condition function
                result = condition(input_data)

                # Handle different result types
                if isinstance(result, list):
                    # Multiple results - create Send objects
                    sends = []
                    for item in result:
                        key = str(item)
                        target = routes.get(key, routes.get("default", END))
                        sends.append(Send(target, input_data))
                    return sends
                else:
                    # Single result - find matching route
                    key = str(result)
                    target = routes.get(key, routes.get("default", END))

                    # Return Command with no update (just routing)
                    return Command(goto=target)
            except Exception as e:
                logger.error(f"Error in branch node: {e}")
                # Fall through to default route
                default_target = routes.get("default", END)
                return Command(goto=default_target)

        # Add metadata
        node_function.__node_config__ = config

        return node_function

    @classmethod
    def _create_send_node(cls, config: NodeConfig) -> Callable:
        """
        Create a send node function.

        Args:
            config: Node configuration

        Returns:
            Send node function
        """
        if not config.send_targets:
            raise ValueError("Send node requires send_targets")

        # Core info
        input_mapping = config.get_input_mapping()
        send_targets = config.send_targets
        send_field = config.send_field

        # Get input mapping from schema if empty
        if not input_mapping and config.input_schema:
            input_fields = config.input_schema.model_fields.keys()
            input_mapping = {field: field for field in input_fields}

        def node_function(state, config=None):
            """Node function for send node."""
            try:
                # Extract input from state
                input_data = cls._extract_input(state, input_mapping)

                # Get items to distribute
                if not send_field:
                    # Just send the entire input to each target
                    return [Send(target, input_data) for target in send_targets]

                # Extract the field to distribute
                items = None
                if isinstance(input_data, dict):
                    items = input_data.get(send_field)
                elif hasattr(input_data, send_field):
                    items = getattr(input_data, send_field)

                if items is None:
                    logger.warning(f"Send field '{send_field}' not found in state")
                    # Return empty update to END
                    return Command(goto=END)

                # Ensure items is a list
                if not isinstance(items, (list, tuple)):
                    items = [items]

                # Create Send objects for each target
                sends = []

                # One item per target (round-robin if more items than targets)
                if len(items) > len(send_targets):
                    # Assign items round-robin
                    for i, item in enumerate(items):
                        target_idx = i % len(send_targets)
                        target = send_targets[target_idx]
                        sends.append(Send(target, {send_field: item}))
                else:
                    # One item per target (or fewer items than targets)
                    for i, item in enumerate(items):
                        if i < len(send_targets):
                            target = send_targets[i]
                            sends.append(Send(target, {send_field: item}))

                return sends
            except Exception as e:
                logger.error(f"Error in send node: {e}")
                return Command(goto=END)

        # Add metadata
        node_function.__node_config__ = config

        return node_function

    @classmethod
    def _create_generic_node(cls, config: NodeConfig, obj: Any) -> Callable:
        """
        Create a generic node function.

        Args:
            config: Node configuration
            obj: Generic object to wrap

        Returns:
            Node function
        """
        # Core info
        command_goto = config.command_goto
        output_mapping = config.get_output_mapping()

        # Get output mapping from schema if empty
        if not output_mapping and config.output_schema:
            output_fields = config.output_schema.model_fields.keys()
            output_mapping = {field: field for field in output_fields}

        def node_function(state, config=None):
            """Node function for generic object."""
            try:
                # Just return the object as result
                result = {"result": obj}

                # Process output
                processed_output = cls._process_output(result, output_mapping)

                # Return with Command for routing
                return Command(update=processed_output, goto=command_goto)
            except Exception as e:
                logger.error(f"Error in generic node: {e}")
                return Command(update={"error": str(e)}, goto=command_goto)

        # Add metadata
        node_function.__node_config__ = config

        return node_function

    @classmethod
    def _extract_input(
        cls, state: Any, input_mapping: Dict[str, str], engine_id: Optional[str] = None
    ) -> Any:
        """
        Extract input from state based on mapping with engine I/O awareness.

        Args:
            state: State object (dict, BaseModel, etc.)
            input_mapping: Mapping from state keys to input keys
            engine_id: Optional engine ID to look up in I/O mappings

        Returns:
            Extracted input
        """
        # Try to use engine I/O mappings if available
        if engine_id:
            # First check if state has I/O mappings
            state_io_mappings = None
            if hasattr(state, "__engine_io_mappings__"):
                state_io_mappings = getattr(state, "__engine_io_mappings__", {})
            elif isinstance(state, dict) and "__engine_io_mappings__" in state:
                state_io_mappings = state["__engine_io_mappings__"]

            # If we found mappings and this engine is in them
            if state_io_mappings and engine_id in state_io_mappings:
                engine_mapping = state_io_mappings[engine_id]
                input_fields = engine_mapping.get("inputs", [])

                if input_fields:
                    # Extract just the input fields for this engine
                    engine_input = {}

                    # Get the state as a dict for easier access
                    if isinstance(state, dict):
                        state_dict = state
                    elif hasattr(state, "model_dump"):
                        state_dict = state.model_dump()
                    elif hasattr(state, "dict"):
                        state_dict = state.dict()
                    else:
                        # Try attribute access
                        state_dict = {}
                        for field in input_fields:
                            if hasattr(state, field):
                                state_dict[field] = getattr(state, field)

                    # Extract each input field
                    for field in input_fields:
                        if field in state_dict:
                            engine_input[field] = state_dict[field]

                    # If only one field is expected and we have exactly one field, return it directly
                    if len(input_fields) == 1 and len(engine_input) == 1:
                        return list(engine_input.values())[0]

                    # Otherwise return the dictionary
                    return engine_input

        # Fallback: use input_mapping if provided
        if input_mapping:
            # Get the state as a dict for mapping
            if isinstance(state, dict):
                state_dict = state
            elif hasattr(state, "model_dump"):
                state_dict = state.model_dump()
            elif hasattr(state, "dict"):
                state_dict = state.dict()
            else:
                # Try attribute access
                state_dict = {}
                for state_key in input_mapping.keys():
                    if hasattr(state, state_key):
                        state_dict[state_key] = getattr(state, state_key)

            # Apply the mapping
            mapped_input = {}
            for state_key, input_key in input_mapping.items():
                if state_key in state_dict:
                    mapped_input[input_key] = state_dict[state_key]

            # If only one key was mapped, return the value directly
            if len(input_mapping) == 1 and len(mapped_input) == 1:
                return list(mapped_input.values())[0]

            return mapped_input

        # Final fallback: return state as-is
        if isinstance(state, dict):
            return state
        elif hasattr(state, "model_dump"):
            return state.model_dump()
        elif hasattr(state, "dict"):
            return state.dict()
        else:
            return state

    @classmethod
    def _process_output(
        cls, output: Any, output_mapping: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Process output according to mapping.

        Args:
            output: Output from function/engine
            output_mapping: Mapping from output keys to state keys

        Returns:
            Processed output
        """
        # Handle non-dict output - wrap in dictionary
        if not isinstance(output, dict) and not isinstance(output, BaseModel):
            return {"result": output}

        # Handle BaseModel directly
        if isinstance(output, BaseModel):
            # Extract model class name
            model_name = output.__class__.__name__.lower()

            # Check if model name is in output mapping
            if output_mapping:
                for output_key, state_key in output_mapping.items():
                    if state_key.lower() == model_name:
                        return {state_key: output}

            # Default to model name as key
            return {model_name: output}

        # Return as-is if no mapping
        if not output_mapping:
            return output

        # Apply mapping
        result = {}
        for output_key, state_key in output_mapping.items():
            if output_key in output:
                result[state_key] = output[output_key]

        # Return original output if no mapped keys were found
        return result if result else output
