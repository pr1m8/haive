# src/haive/core/graph/NodeFactory.py

import importlib
import inspect
import logging
from collections.abc import Callable
from functools import wraps
from typing import Any, Protocol, runtime_checkable

from langchain_core.runnables import RunnableConfig
from langgraph.types import Command
from pydantic import BaseModel

from haive.core.config.runnable import RunnableConfigManager
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.base import (
    Engine,
    EngineType,
    InvokableEngine,
    NonInvokableEngine,
)
from haive.core.engine.embeddings import EmbeddingsEngineConfig
from haive.core.engine.retriever import BaseRetrieverConfig
from haive.core.engine.vectorstore.vectorstore import VectorStoreConfig
from haive.core.graph.graph_pattern_registry import GraphRegistry

logger = logging.getLogger(__name__)


@runtime_checkable
class NodeFunction(Protocol):
    """Protocol for node functions."""

    def __call__(self, state: Any, config: dict[str, Any] | None = None) -> Any: ...


class NodeFactory:
    """Factory for creating node functions with comprehensive engine support.

    Handles creation of node functions from different engine types,
    ensuring proper input/output mapping and runtime configuration.
    """

    # Improvements to NodeFactory.py to better handle Engine integration

    @classmethod
    def create_node_function(
        cls,
        config: Engine | Callable | str,
        command_goto: str | None = None,
        input_mapping: dict[str, str] | None = None,
        output_mapping: dict[str, str] | None = None,
        runnable_config: RunnableConfig | None = None,
    ) -> NodeFunction:
        """Create a node function with enhanced engine handling."""
        # Always import EngineType at the start of the method
        from haive.core.engine.base import (
            Engine,
            EngineRegistry,
            EngineType,
            InvokableEngine,
            NonInvokableEngine,
        )

        # Handle string references to engines
        if isinstance(config, str):
            registry = EngineRegistry.get_instance()

            resolved = False
            for engine_type in EngineType:
                engine = registry.get(engine_type, config)
                if engine:
                    config = engine
                    resolved = True
                    break

            # If not found, try graph registry
            if not resolved:
                graph_registry = GraphRegistry.get_instance()
                components = graph_registry.list_components(tags=["engine"])
                for component in components:
                    if component.name == config:
                        if component.metadata.get("source_module"):
                            try:
                                module = importlib.import_module(
                                    component.metadata["source_module"]
                                )
                                class_obj = getattr(module, component.name)
                                if issubclass(class_obj, Engine):
                                    config = class_obj()
                                    resolved = True
                                    break
                            except (ImportError, AttributeError):
                                pass

            if not resolved:
                raise ValueError(f"Engine '{config}' not found in registries")

        # Derive input and output mappings if not provided
        if input_mapping is None and hasattr(config, "_derive_input_mapping"):
            input_mapping = cls._derive_input_mapping(config)

        if output_mapping is None and hasattr(config, "_derive_output_mapping"):
            output_mapping = cls._derive_output_mapping(config)

        # Handle different types of configs
        if isinstance(config, Engine):
            # Invokable engines
            if isinstance(config, InvokableEngine):
                # Specialized handling for different engine types
                if config.engine_type == EngineType.LLM:
                    return cls._create_llm_node(
                        config,
                        command_goto,
                        input_mapping,
                        output_mapping,
                        runnable_config,
                    )
                if config.engine_type == EngineType.VECTOR_STORE:
                    return cls._create_vectorstore_node(
                        config,
                        command_goto,
                        input_mapping,
                        output_mapping,
                        runnable_config,
                    )
                if config.engine_type == EngineType.RETRIEVER:
                    return cls._create_retriever_node(
                        config,
                        command_goto,
                        input_mapping,
                        output_mapping,
                        runnable_config,
                    )
                if config.engine_type == EngineType.AGENT:
                    return cls._create_agent_node(
                        config,
                        command_goto,
                        input_mapping,
                        output_mapping,
                        runnable_config,
                    )
                return cls._create_invokable_engine_node(
                    config, command_goto, input_mapping, output_mapping, runnable_config
                )

            # Non-invokable engines
            if isinstance(config, NonInvokableEngine):
                # Handle Non-Invokable engine types
                if config.engine_type == EngineType.EMBEDDINGS:
                    return cls._create_embeddings_node(
                        config,
                        command_goto,
                        input_mapping,
                        output_mapping,
                        runnable_config,
                    )
                return cls._create_non_invokable_engine_node(
                    config, command_goto, input_mapping, output_mapping, runnable_config
                )

            # Generic engine fallback
            return cls._create_generic_engine_node(
                config, command_goto, input_mapping, output_mapping, runnable_config
            )

        # Callable config
        if callable(config):
            # Ensure the callable is config-aware
            return cls._ensure_config_aware(config, command_goto, runnable_config)

        # Unsupported config type
        raise ValueError(f"Unsupported node configuration type: {type(config)}")

    @classmethod
    def create_node_function(
        cls,
        config: Engine | Callable | str,
        command_goto: str | None = None,
        input_mapping: dict[str, str] | None = None,
        output_mapping: dict[str, str] | None = None,
        runnable_config: RunnableConfig | None = None,
    ) -> NodeFunction:
        """Create a node function with enhanced engine handling."""
        # Import EngineType at method level to ensure it's always available
        from haive.core.engine.base import (
            Engine,
            EngineRegistry,
            EngineType,
            InvokableEngine,
            NonInvokableEngine,
        )

        # Handle string references to engines
        if isinstance(config, str):
            registry = EngineRegistry.get_instance()

            resolved = False
            for engine_type in EngineType:
                engine = registry.get(engine_type, config)
                if engine:
                    config = engine
                    resolved = True
                    break

            # If not found, try graph registry
            if not resolved:
                graph_registry = GraphRegistry.get_instance()
                components = graph_registry.list_components(tags=["engine"])
                for component in components:
                    if component.name == config:
                        if component.metadata.get("source_module"):
                            try:
                                module = importlib.import_module(
                                    component.metadata["source_module"]
                                )
                                class_obj = getattr(module, component.name)
                                if issubclass(class_obj, Engine):
                                    config = class_obj()
                                    resolved = True
                                    break
                            except (ImportError, AttributeError):
                                pass

            if not resolved:
                raise ValueError(f"Engine '{config}' not found in registries")

        # Derive input and output mappings if not provided
        if input_mapping is None and hasattr(config, "_derive_input_mapping"):
            input_mapping = cls._derive_input_mapping(config)

        if output_mapping is None and hasattr(config, "_derive_output_mapping"):
            output_mapping = cls._derive_output_mapping(config)

        # Handle different types of configs
        if isinstance(config, Engine):
            # Invokable engines
            if isinstance(config, InvokableEngine):
                # Specialized handling for different engine types
                if config.engine_type == EngineType.LLM:
                    return cls._create_llm_node(
                        config,
                        command_goto,
                        input_mapping,
                        output_mapping,
                        runnable_config,
                    )
                if config.engine_type == EngineType.VECTOR_STORE:
                    return cls._create_vectorstore_node(
                        config,
                        command_goto,
                        input_mapping,
                        output_mapping,
                        runnable_config,
                    )
                if config.engine_type == EngineType.RETRIEVER:
                    return cls._create_retriever_node(
                        config,
                        command_goto,
                        input_mapping,
                        output_mapping,
                        runnable_config,
                    )
                if config.engine_type == EngineType.AGENT:
                    return cls._create_agent_node(
                        config,
                        command_goto,
                        input_mapping,
                        output_mapping,
                        runnable_config,
                    )
                return cls._create_invokable_engine_node(
                    config, command_goto, input_mapping, output_mapping, runnable_config
                )

            # Non-invokable engines
            if isinstance(config, NonInvokableEngine):
                # Handle Non-Invokable engine types
                if config.engine_type == EngineType.EMBEDDINGS:
                    return cls._create_embeddings_node(
                        config,
                        command_goto,
                        input_mapping,
                        output_mapping,
                        runnable_config,
                    )
                return cls._create_non_invokable_engine_node(
                    config, command_goto, input_mapping, output_mapping, runnable_config
                )

            # Generic engine fallback
            return cls._create_generic_engine_node(
                config, command_goto, input_mapping, output_mapping, runnable_config
            )

        # Callable config
        if callable(config):
            # Ensure the callable is config-aware
            return cls._ensure_config_aware(config, command_goto, runnable_config)

        # Unsupported config type
        raise ValueError(f"Unsupported node configuration type: {type(config)}")

    @classmethod
    def create_node_function(
        cls,
        config: Engine | Callable | str,
        command_goto: str | None = None,
        input_mapping: dict[str, str] | None = None,
        output_mapping: dict[str, str] | None = None,
        runnable_config: RunnableConfig | None = None,
    ) -> NodeFunction:
        """Create a node function with enhanced engine handling."""
        # Handle string references to engines
        if isinstance(config, str):
            # Try to resolve from engine registry
            from haive.core.engine.base import EngineRegistry, EngineType

            registry = EngineRegistry.get_instance()

            resolved = False
            for engine_type in EngineType:
                engine = registry.get(engine_type, config)
                if engine:
                    config = engine
                    resolved = True
                    break

            # If not found, try graph registry
            if not resolved:
                graph_registry = GraphRegistry.get_instance()
                components = graph_registry.list_components(tags=["engine"])
                for component in components:
                    if component.name == config:
                        if component.metadata.get("source_module"):
                            try:
                                module = importlib.import_module(
                                    component.metadata["source_module"]
                                )
                                class_obj = getattr(module, component.name)
                                if issubclass(class_obj, Engine):
                                    config = class_obj()
                                    resolved = True
                                    break
                            except (ImportError, AttributeError):
                                pass

            if not resolved:
                raise ValueError(f"Engine '{config}' not found in registries")

        # Derive input and output mappings if not provided
        if input_mapping is None and hasattr(config, "_derive_input_mapping"):
            input_mapping = cls._derive_input_mapping(config)

        if output_mapping is None and hasattr(config, "_derive_output_mapping"):
            output_mapping = cls._derive_output_mapping(config)

        # Handle different types of configs
        if isinstance(config, Engine):
            # Invokable engines
            if isinstance(config, InvokableEngine):
                # Specialized handling for different engine types
                if config.engine_type == EngineType.LLM:
                    return cls._create_llm_node(
                        config,
                        command_goto,
                        input_mapping,
                        output_mapping,
                        runnable_config,
                    )
                if config.engine_type == EngineType.VECTOR_STORE:
                    return cls._create_vectorstore_node(
                        config,
                        command_goto,
                        input_mapping,
                        output_mapping,
                        runnable_config,
                    )
                if config.engine_type == EngineType.RETRIEVER:
                    return cls._create_retriever_node(
                        config,
                        command_goto,
                        input_mapping,
                        output_mapping,
                        runnable_config,
                    )
                if config.engine_type == EngineType.AGENT:
                    return cls._create_agent_node(
                        config,
                        command_goto,
                        input_mapping,
                        output_mapping,
                        runnable_config,
                    )
                return cls._create_invokable_engine_node(
                    config, command_goto, input_mapping, output_mapping, runnable_config
                )

            # Non-invokable engines
            if isinstance(config, NonInvokableEngine):
                # Handle Non-Invokable engine types
                if config.engine_type == EngineType.EMBEDDINGS:
                    return cls._create_embeddings_node(
                        config,
                        command_goto,
                        input_mapping,
                        output_mapping,
                        runnable_config,
                    )
                return cls._create_non_invokable_engine_node(
                    config, command_goto, input_mapping, output_mapping, runnable_config
                )

            # Generic engine fallback
            return cls._create_generic_engine_node(
                config, command_goto, input_mapping, output_mapping, runnable_config
            )

        # Callable config
        if callable(config):
            # Ensure the callable is config-aware
            return cls._ensure_config_aware(config, command_goto, runnable_config)

        # Unsupported config type
        raise ValueError(f"Unsupported node configuration type: {type(config)}")

    @classmethod
    def create_tool_node(
        cls,
        tools: list[Any],
        post_processor: Callable | None = None,
        command_goto: str | None = None,
        runnable_config: RunnableConfig | None = None,
    ) -> NodeFunction:
        """Create a tool node with config awareness.

        Args:
            tools: List of tools to use
            post_processor: Optional function to process tool results
            command_goto: Optional next node to go to
            runnable_config: Optional default runtime configuration

        Returns:
            A node function for tool execution
        """
        # Import here to avoid circular imports
        from langgraph.prebuilt import ToolNode

        # Create base tool node
        base_tool_node = ToolNode(tools)

        def node_function(state, config: RunnableConfig | None = None):
            """Config-aware tool node."""
            # Merge configs
            merged_config = cls._merge_configs(runnable_config, config)

            # Extract allowed tools if specified
            allowed_tools = cls._extract_from_config(merged_config, "allowed_tools")

            # Use all tools or filter based on config
            active_tools = tools
            if allowed_tools:
                # Filter tools
                active_tools = [t for t in tools if t.name in allowed_tools]
                if not active_tools:
                    logger.warning(f"No tools match allowed_tools: {allowed_tools}")
                    active_tools = tools

                # Create temporary node with filtered tools
                node = ToolNode(active_tools)
                result = node.invoke(state)
            else:
                # Use all tools
                result = base_tool_node.invoke(state)

            # Process with post_processor if provided
            if post_processor:
                result = post_processor(result)

            # Return result with command
            return Command(update=result, goto=command_goto)

        return node_function

    @classmethod
    def create_runnable_config_node(
        cls, runnable_config: RunnableConfig, command_goto: str | None = None
    ) -> NodeFunction:
        """Create a node that sets runnable_config in the state.

        Args:
            runnable_config: Configuration to set
            command_goto: Optional next node to go to

        Returns:
            A node function that sets config in state
        """

        def node_function(state, config=None):
            """Set runnable_config in state."""
            # Create a merged config
            merged_config = cls._merge_configs(runnable_config, config)

            # Update state with the merged config
            state_update = {"__runnable_config__": merged_config}

            # Return with command
            return Command(update=state_update, goto=command_goto)

        return node_function

    @classmethod
    def create_structured_output_node(
        cls,
        model: type[BaseModel],
        command_goto: str | None = None,
        runnable_config: RunnableConfig | None = None,
    ) -> NodeFunction:
        """Create a node that formats the output according to a schema.

        Args:
            model: Pydantic model to use for structuring output
            command_goto: Optional next node to go to
            runnable_config: Optional default runtime configuration

        Returns:
            A node function that structures output
        """

        def node_function(state, config=None):
            """Process state into structured output."""
            try:
                # Get the last message content
                messages = state.messages if hasattr(state, "messages") else []
                if not messages:
                    return Command(
                        update={"error": "No messages found in state"},
                        goto=command_goto,
                    )

                # Get the last message content
                last_message = messages[-1]
                content = (
                    last_message.content
                    if hasattr(last_message, "content")
                    else str(last_message)
                )

                # Store raw output
                result = {"raw_output": content}

                # Try to parse JSON from the content
                try:
                    import json
                    import re

                    # Try to extract a JSON block if it exists
                    json_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", content)
                    if json_match:
                        json_str = json_match.group(1)
                    else:
                        # Try to find any JSON-like structure
                        json_match = re.search(r"({[\s\S]*?})", content)
                        if json_match:
                            json_str = json_match.group(1)
                        else:
                            json_str = content

                    # Parse the JSON
                    parsed_data = json.loads(json_str)

                    # Validate against the model
                    if hasattr(model, "model_validate"):
                        # Pydantic v2
                        structured_output = model.model_validate(parsed_data)
                        result["output"] = structured_output.model_dump()
                    else:
                        # Pydantic v1
                        structured_output = model(**parsed_data)
                        result["output"] = structured_output.dict()

                except Exception as e:
                    # If JSON parsing or validation fails, log error
                    logger.warning(f"Failed to parse structured output: {e}")
                    result["parsing_errors"] = f"Error parsing output: {e!s}"

                return Command(update=result, goto=command_goto)

            except Exception as e:
                logger.error(f"Error in structured output processor: {e!s}")
                return Command(
                    update={"error": f"Processing error: {e!s}"}, goto=command_goto
                )

        return node_function

    @classmethod
    def _create_invokable_engine_node(
        cls,
        engine: InvokableEngine,
        command_goto: str | None = None,
        input_mapping: dict[str, str] | None = None,
        output_mapping: dict[str, str] | None = None,
        runnable_config: RunnableConfig | None = None,
    ) -> NodeFunction:
        """Create a node function for an invokable engine.

        Args:
            engine: Invokable engine to use
            command_goto: Optional next node to go to
            input_mapping: Optional mapping from state keys to engine input keys
            output_mapping: Optional mapping from engine output keys to state keys
            runnable_config: Optional default runtime configuration

        Returns:
            A node function for the engine
        """
        # Create specialized node based on engine type
        if engine.engine_type == EngineType.LLM:
            return cls._create_llm_node(
                engine, command_goto, input_mapping, output_mapping, runnable_config
            )
        if engine.engine_type == EngineType.VECTOR_STORE:
            return cls._create_vectorstore_node(
                engine, command_goto, input_mapping, output_mapping, runnable_config
            )
        if engine.engine_type == EngineType.RETRIEVER:
            return cls._create_retriever_node(
                engine, command_goto, input_mapping, output_mapping, runnable_config
            )
        if engine.engine_type == EngineType.AGENT:
            return cls._create_agent_node(
                engine, command_goto, input_mapping, output_mapping, runnable_config
            )

        # Generic invokable engine node
        def node_function(state, config: RunnableConfig | None = None):
            """Invokable engine node."""
            logger.debug(f"Invokable engine node called with state: {state}")

            # Merge runtime configs
            merged_config = cls._merge_configs(runnable_config, config)

            # Extract input from state
            input_data = cls._extract_input(state, input_mapping)

            # Invoke the engine
            try:
                result = engine.invoke(input_data, merged_config)
                logger.debug(f"Engine result type: {type(result)}")
            except Exception as e:
                logger.error(f"Error invoking engine: {e}")
                return cls._create_error_command(state, str(e), command_goto)

            # Process result into state update
            state_update = cls._process_result(result, state, output_mapping)

            # Return result with command
            return Command(update=state_update, goto=command_goto)

        return node_function

    @classmethod
    def _create_llm_node(
        cls,
        engine: AugLLMConfig | InvokableEngine,
        command_goto: str | None = None,
        input_mapping: dict[str, str] | None = None,
        output_mapping: dict[str, str] | None = None,
        runnable_config: RunnableConfig | None = None,
    ) -> NodeFunction:
        """Create a node function for an LLM engine.

        Args:
            engine: LLM engine to use
            command_goto: Optional next node to go to
            input_mapping: Optional mapping from state keys to engine input keys
            output_mapping: Optional mapping from engine output keys to state keys
            runnable_config: Optional default runtime configuration

        Returns:
            A node function for the LLM
        """

        def node_function(state, config: RunnableConfig | None = None):
            """LLM node function."""
            logger.debug("LLM node called with state")

            # Merge runtime configs
            merged_config = cls._merge_configs(runnable_config, config)

            # Extract input according to mapping
            input_data = cls._extract_input(state, input_mapping)

            # Add messages if not present
            if "messages" not in input_data and hasattr(state, "messages"):
                input_data["messages"] = state.messages

            # Invoke the LLM
            try:
                result = engine.invoke(input_data, merged_config)
                logger.debug(f"LLM result: {type(result)}")
            except Exception as e:
                logger.error(f"Error invoking LLM: {e}")
                return cls._create_error_command(state, str(e), command_goto)

            # Process result into state update
            state_update = cls._process_result(result, state, output_mapping)

            # Return with command
            return Command(update=state_update, goto=command_goto)

        return node_function

    @classmethod
    def _create_vectorstore_node(
        cls,
        engine: VectorStoreConfig,
        command_goto: str | None = None,
        input_mapping: dict[str, str] | None = None,
        output_mapping: dict[str, str] | None = None,
        runnable_config: RunnableConfig | None = None,
    ) -> NodeFunction:
        """Create a node function for a vector store engine.

        Args:
            engine: Vector store engine to use
            command_goto: Optional next node to go to
            input_mapping: Optional mapping from state keys to engine input keys
            output_mapping: Optional mapping from engine output keys to state keys
            runnable_config: Optional default runtime configuration

        Returns:
            A node function for the vector store
        """

        def node_function(state, config: RunnableConfig | None = None):
            """Vector store node function."""
            logger.debug("Vector store node called with state")

            # Merge runtime configs
            merged_config = cls._merge_configs(runnable_config, config)

            # Extract input according to mapping
            input_data = cls._extract_input(state, input_mapping)

            # Ensure there's a query
            if not isinstance(input_data, str) and "query" not in input_data:
                # Try to find a query in the state
                if hasattr(state, "query"):
                    input_data = {"query": state.query}
                elif hasattr(state, "question"):
                    input_data = {"query": state.question}
                elif hasattr(state, "input"):
                    input_data = {"query": state.input}
                elif hasattr(state, "messages") and state.messages:
                    # Use the last message as query
                    last_message = state.messages[-1]
                    content = (
                        last_message.content
                        if hasattr(last_message, "content")
                        else str(last_message)
                    )
                    input_data = {"query": content}

            # Invoke the vector store
            try:
                documents = engine.invoke(input_data, merged_config)
                logger.debug(f"Vector store result: {len(documents)} documents")
            except Exception as e:
                logger.error(f"Error invoking vector store: {e}")
                return cls._create_error_command(state, str(e), command_goto)

            # Process result into state update
            state_update = cls._process_vectorstore_result(
                documents, state, output_mapping
            )

            # Return with command
            return Command(update=state_update, goto=command_goto)

        return node_function

    @classmethod
    def _create_retriever_node(
        cls,
        engine: BaseRetrieverConfig,
        command_goto: str | None = None,
        input_mapping: dict[str, str] | None = None,
        output_mapping: dict[str, str] | None = None,
        runnable_config: RunnableConfig | None = None,
    ) -> NodeFunction:
        """Create a node function for a retriever engine.

        Args:
            engine: Retriever engine to use
            command_goto: Optional next node to go to
            input_mapping: Optional mapping from state keys to engine input keys
            output_mapping: Optional mapping from engine output keys to state keys
            runnable_config: Optional default runtime configuration

        Returns:
            A node function for the retriever
        """

        def node_function(state, config: RunnableConfig | None = None):
            """Retriever node function."""
            logger.debug("Retriever node called with state")

            # Merge runtime configs
            merged_config = cls._merge_configs(runnable_config, config)

            # Extract input according to mapping
            input_data = cls._extract_input(state, input_mapping)

            # Ensure there's a query
            if not isinstance(input_data, str) and "query" not in input_data:
                # Try to find a query in the state
                if hasattr(state, "query"):
                    input_data = {"query": state.query}
                elif hasattr(state, "question"):
                    input_data = {"query": state.question}
                elif hasattr(state, "input"):
                    input_data = {"query": state.input}
                elif hasattr(state, "messages") and state.messages:
                    # Use the last message as query
                    last_message = state.messages[-1]
                    content = (
                        last_message.content
                        if hasattr(last_message, "content")
                        else str(last_message)
                    )
                    input_data = {"query": content}

            # Invoke the retriever
            try:
                documents = engine.invoke(input_data, merged_config)
                logger.debug(f"Retriever result: {len(documents)} documents")
            except Exception as e:
                logger.error(f"Error invoking retriever: {e}")
                return cls._create_error_command(state, str(e), command_goto)

            # Process result into state update
            state_update = cls._process_vectorstore_result(
                documents, state, output_mapping
            )

            # Return with command
            return Command(update=state_update, goto=command_goto)

        return node_function

    @classmethod
    def _create_agent_node(
        cls,
        engine: InvokableEngine,
        command_goto: str | None = None,
        input_mapping: dict[str, str] | None = None,
        output_mapping: dict[str, str] | None = None,
        runnable_config: RunnableConfig | None = None,
    ) -> NodeFunction:
        """Create a node function for an agent engine.

        Args:
            engine: Agent engine to use
            command_goto: Optional next node to go to
            input_mapping: Optional mapping from state keys to engine input keys
            output_mapping: Optional mapping from engine output keys to state keys
            runnable_config: Optional default runtime configuration

        Returns:
            A node function for the agent
        """

        def node_function(state, config: RunnableConfig | None = None):
            """Agent node function."""
            logger.debug("Agent node called with state")

            # Merge runtime configs
            merged_config = cls._merge_configs(runnable_config, config)

            # Extract input according to mapping
            input_data = cls._extract_input(state, input_mapping)

            # Invoke the agent
            try:
                result = engine.invoke(input_data, merged_config)
                logger.debug(f"Agent result type: {type(result)}")
            except Exception as e:
                logger.error(f"Error invoking agent: {e}")
                return cls._create_error_command(state, str(e), command_goto)

            # Process result into state update
            state_update = cls._process_result(result, state, output_mapping)

            # Return with command
            return Command(update=state_update, goto=command_goto)

        return node_function

    @classmethod
    def _create_non_invokable_engine_node(
        cls,
        engine: NonInvokableEngine,
        command_goto: str | None = None,
        input_mapping: dict[str, str] | None = None,
        output_mapping: dict[str, str] | None = None,
        runnable_config: RunnableConfig | None = None,
    ) -> NodeFunction:
        """Create a node function for a non-invokable engine.

        Args:
            engine: Non-invokable engine to use
            command_goto: Optional next node to go to
            input_mapping: Optional mapping from state keys to engine input keys
            output_mapping: Optional mapping from engine output keys to state keys
            runnable_config: Optional default runtime configuration

        Returns:
            A node function for the engine
        """
        # Create specialized node based on engine type
        if engine.engine_type == EngineType.EMBEDDINGS:
            return cls._create_embeddings_node(
                engine, command_goto, input_mapping, output_mapping, runnable_config
            )

        # Generic non-invokable engine node
        def node_function(state, config: RunnableConfig | None = None):
            """Non-invokable engine node."""
            logger.debug("Non-invokable engine node called with state")

            # Merge runtime configs
            merged_config = cls._merge_configs(runnable_config, config)

            # Extract input according to mapping
            input_data = cls._extract_input(state, input_mapping)

            # Instantiate the engine
            try:
                instance = engine.instantiate(merged_config)
                logger.debug(f"Engine instantiated: {type(instance)}")

                # Process with the instantiated engine
                result = cls._process_with_non_invokable(instance, input_data)
            except Exception as e:
                logger.error(f"Error with non-invokable engine: {e}")
                return cls._create_error_command(state, str(e), command_goto)

            # Process result into state update
            state_update = cls._process_result(result, state, output_mapping)

            # Return with command
            return Command(update=state_update, goto=command_goto)

        return node_function

    @classmethod
    def _create_embeddings_node(
        cls,
        engine: EmbeddingsEngineConfig,
        command_goto: str | None = None,
        input_mapping: dict[str, str] | None = None,
        output_mapping: dict[str, str] | None = None,
        runnable_config: RunnableConfig | None = None,
    ) -> NodeFunction:
        """Create a node function for an embeddings engine.

        Args:
            engine: Embeddings engine to use
            command_goto: Optional next node to go to
            input_mapping: Optional mapping from state keys to engine input keys
            output_mapping: Optional mapping from engine output keys to state keys
            runnable_config: Optional default runtime configuration

        Returns:
            A node function for the embeddings engine
        """

        def node_function(state, config: RunnableConfig | None = None):
            """Embeddings node function."""
            logger.debug("Embeddings node called with state")

            # Merge runtime configs
            merged_config = cls._merge_configs(runnable_config, config)

            # Extract input according to mapping
            input_data = cls._extract_input(state, input_mapping)

            try:
                # Process based on input type
                if isinstance(input_data, str):
                    # Single text
                    result = engine.embed_query(
                        input_data, runnable_config=merged_config
                    )
                elif isinstance(input_data, list) and all(
                    isinstance(x, str) for x in input_data
                ):
                    # List of texts
                    result = engine.embed_documents(
                        input_data, runnable_config=merged_config
                    )
                elif isinstance(input_data, dict):
                    # Dictionary with text or documents
                    if "text" in input_data:
                        result = engine.embed_query(
                            input_data["text"], runnable_config=merged_config
                        )
                    elif "documents" in input_data or "texts" in input_data:
                        docs = input_data.get("documents") or input_data.get("texts")
                        result = engine.embed_documents(
                            docs, runnable_config=merged_config
                        )
                    else:
                        raise ValueError(
                            f"Unsupported input format for embeddings: {input_data.keys()}"
                        )
                else:
                    raise ValueError(
                        f"Unsupported input type for embeddings: {type(input_data)}"
                    )

                logger.debug(
                    f"Embeddings generated with shape: {len(result) if isinstance(result, list) else 'unknown'}"
                )
            except Exception as e:
                logger.error(f"Error generating embeddings: {e}")
                return cls._create_error_command(state, str(e), command_goto)

            # Process result into state update
            state_update = cls._process_embeddings_result(result, state, output_mapping)

            # Return with command
            return Command(update=state_update, goto=command_goto)

        return node_function

    @classmethod
    def _process_with_non_invokable(cls, instance, input_data):
        """Process input with a non-invokable engine instance."""
        # Handle different input types
        if isinstance(input_data, dict):
            # Common patterns for embeddings
            if "text" in input_data:
                return instance.embed_query(input_data["text"])
            if "documents" in input_data or "texts" in input_data:
                docs = input_data.get("documents") or input_data.get("texts")
                return instance.embed_documents(docs)
            if "queries" in input_data:
                return [instance.embed_query(q) for q in input_data["queries"]]
            # Try first value
            first_key = next(iter(input_data))
            first_value = input_data[first_key]
            if isinstance(first_value, str):
                return instance.embed_query(first_value)
            if isinstance(first_value, list) and all(
                isinstance(x, str) for x in first_value
            ):
                return instance.embed_documents(first_value)
        elif isinstance(input_data, str):
            return instance.embed_query(input_data)
        elif isinstance(input_data, list) and all(
            isinstance(x, str) for x in input_data
        ):
            return instance.embed_documents(input_data)

        # If we can't figure it out, try returning the instance
        return instance

    @classmethod
    def _create_generic_engine_node(
        cls,
        engine: Engine,
        command_goto: str | None = None,
        input_mapping: dict[str, str] | None = None,
        output_mapping: dict[str, str] | None = None,
        runnable_config: RunnableConfig | None = None,
    ) -> NodeFunction:
        """Create a generic node function for an engine.

        Args:
            engine: Engine to use
            command_goto: Optional next node to go to
            input_mapping: Optional mapping from state keys to engine input keys
            output_mapping: Optional mapping from engine output keys to state keys
            runnable_config: Optional default runtime configuration

        Returns:
            A node function for the engine
        """

        def node_function(state, config: RunnableConfig | None = None):
            """Generic engine node."""
            logger.debug("Generic engine node called with state")

            # Merge runtime configs
            merged_config = cls._merge_configs(runnable_config, config)

            # Extract input according to mapping
            input_data = cls._extract_input(state, input_mapping)

            # Create runnable
            try:
                runnable = engine.create_runnable(merged_config)

                # Try to invoke the runnable
                if hasattr(runnable, "invoke"):
                    result = runnable.invoke(input_data)
                elif callable(runnable):
                    result = runnable(input_data)
                else:
                    # Can't invoke, return the runnable itself
                    result = runnable
            except Exception as e:
                logger.error(f"Error with generic engine: {e}")
                return cls._create_error_command(state, str(e), command_goto)

            # Process result into state update
            state_update = cls._process_result(result, state, output_mapping)

            # Return with command
            return Command(update=state_update, goto=command_goto)

        return node_function

    @classmethod
    def _extract_input(cls, state, input_mapping: dict[str, str]) -> Any:
        """Extract input from state based on mapping.

        Args:
            state: State to extract from
            input_mapping: Mapping from state keys to input keys

        Returns:
            Extracted input
        """
        # Handle different state types
        if hasattr(state, "model_dump"):
            # Pydantic v2
            state_dict = state.model_dump()
        elif hasattr(state, "dict"):
            # Pydantic v1
            state_dict = state.dict()
        else:
            # Dict-like or other
            state_dict = state if hasattr(state, "__getitem__") else vars(state)

        # If no mapping, check if state is simple enough to use directly
        if not input_mapping:
            # If state is just a string, return it
            if isinstance(state, str):
                return state

            # If state has only one field, use that
            if isinstance(state_dict, dict) and len(state_dict) == 1:
                return next(iter(state_dict.values()))

            # Otherwise return the full state dict
            return state_dict

        # Apply mapping
        engine_input = {}
        for state_key, engine_key in input_mapping.items():
            if state_key in state_dict:
                engine_input[engine_key] = state_dict[state_key]

        # If nothing matched but there's a messages field, use that
        if not engine_input and "messages" in state_dict:
            engine_input["messages"] = state_dict["messages"]

        # If the mapping expects a single value, check if we can extract it
        if len(input_mapping) == 1 and len(input_mapping.values()) == 1:
            engine_key = next(iter(input_mapping.values()))
            if engine_key in engine_input:
                return engine_input[engine_key]

        return engine_input

    @classmethod
    def _process_result(
        cls, result, state, output_mapping: dict[str, str]
    ) -> dict[str, Any]:
        """Process result into state update.

        Args:
            result: Result to process
            state: Current state
            output_mapping: Mapping from result keys to state keys

        Returns:
            State update dictionary
        """
        from langchain_core.messages import AIMessage

        # Initialize state update
        state_update = {}

        # Handle different result types
        if isinstance(result, dict):
            # Map dictionary fields
            if output_mapping:
                for output_key, state_key in output_mapping.items():
                    if output_key in result:
                        state_update[state_key] = result[output_key]
            else:
                # No mapping, use result directly
                state_update = result
        elif hasattr(result, "content"):
            # Message-like object
            if output_mapping:
                for output_key, state_key in output_mapping.items():
                    if output_key == "content":
                        state_update[state_key] = result.content
            else:
                # Default to output field
                state_update["output"] = result.content

            # Handle messages list
            if hasattr(state, "messages") or (
                isinstance(state, dict) and "messages" in state
            ):
                messages = (
                    state.messages if hasattr(state, "messages") else state["messages"]
                )
                state_update["messages"] = messages + [result]
        elif isinstance(result, list) and all(
            hasattr(item, "content") for item in result
        ):
            # List of messages
            if hasattr(state, "messages") or (
                isinstance(state, dict) and "messages" in state
            ):
                messages = (
                    state.messages if hasattr(state, "messages") else state["messages"]
                )
                state_update["messages"] = messages + result
        elif isinstance(result, str):
            # String result
            if output_mapping:
                # Use first mapping as default
                output_key, state_key = next(iter(output_mapping.items()))
                state_update[state_key] = result
            else:
                # Default to output field
                state_update["output"] = result

            # Add as message if messages exist
            if hasattr(state, "messages") or (
                isinstance(state, dict) and "messages" in state
            ):
                messages = (
                    state.messages if hasattr(state, "messages") else state["messages"]
                )
                state_update["messages"] = messages + [AIMessage(content=result)]
        # Simple value
        elif output_mapping:
            # Use first mapping as default
            output_key, state_key = next(iter(output_mapping.items()))
            state_update[state_key] = result
        else:
            # Default to output field
            state_update["output"] = result

        return state_update

    @classmethod
    def _process_vectorstore_result(
        cls, documents, state, output_mapping: dict[str, str]
    ) -> dict[str, Any]:
        """Process document results into state update.

        Args:
            documents: List of documents
            state: Current state
            output_mapping: Mapping from result keys to state keys

        Returns:
            State update dictionary
        """
        # Initialize state update
        state_update = {}

        # Map documents to the appropriate field
        if output_mapping:
            doc_field = next(
                (
                    state_key
                    for output_key, state_key in output_mapping.items()
                    if output_key == "documents"
                ),
                "documents",
            )
        else:
            doc_field = "documents"

        state_update[doc_field] = documents

        # Handle context field if in mapping or requested
        if output_mapping and any(
            output_key == "context" for output_key in output_mapping.values()
        ):
            # Get the state key for context
            context_field = next(
                (
                    state_key
                    for output_key, state_key in output_mapping.items()
                    if output_key == "context"
                ),
                "context",
            )

            # Extract text from documents
            context = "\n\n".join([doc.page_content for doc in documents])
            state_update[context_field] = context

        return state_update

    @classmethod
    def _process_embeddings_result(
        cls, result, state, output_mapping: dict[str, str]
    ) -> dict[str, Any]:
        """Process embeddings results into state update.

        Args:
            result: Embeddings result
            state: Current state
            output_mapping: Mapping from result keys to state keys

        Returns:
            State update dictionary
        """
        # Initialize state update
        state_update = {}

        # Map embeddings to the appropriate field
        if output_mapping:
            embedding_field = next(
                (
                    state_key
                    for output_key, state_key in output_mapping.items()
                    if output_key == "embeddings"
                ),
                "embeddings",
            )
        else:
            embedding_field = "embeddings"

        state_update[embedding_field] = result

        return state_update

    @classmethod
    def _create_error_command(
        cls, state, error_message: str, command_goto: str | None = None
    ) -> Command:
        """Create an error command.

        Args:
            state: Current state
            error_message: Error message
            command_goto: Optional next node to go to

        Returns:
            Command with error information
        """
        from langchain_core.messages import AIMessage

        # Initialize state update with error
        state_update = {"error": error_message}

        # Add error message to messages if present
        if hasattr(state, "messages") or (
            isinstance(state, dict) and "messages" in state
        ):
            messages = (
                state.messages if hasattr(state, "messages") else state["messages"]
            )
            error_msg = AIMessage(content=f"Error: {error_message}")
            state_update["messages"] = messages + [error_msg]

        return Command(update=state_update, goto=command_goto)

    @classmethod
    def _ensure_config_aware(
        cls,
        func: Callable,
        command_goto: str | None = None,
        runnable_config: RunnableConfig | None = None,
    ) -> NodeFunction:
        """Ensure a function is config-aware.

        Args:
            func: Function to wrap
            command_goto: Optional next node to go to
            runnable_config: Optional default runtime configuration

        Returns:
            Config-aware node function
        """
        # Check if already config-aware
        sig = inspect.signature(func)
        accepts_config = "config" in sig.parameters

        # If it already accepts config, create wrapper that merges configs
        if accepts_config:

            @wraps(func)
            def config_wrapper(state, config=None):
                # Merge configs
                merged_config = cls._merge_configs(runnable_config, config)

                # Call with merged config
                result = func(state, merged_config)

                # Handle Command result
                if isinstance(result, Command):
                    if command_goto and result.goto is None:
                        return Command(update=result.update, goto=command_goto)
                    return result

                # Handle other results
                return Command(update=result, goto=command_goto)

            return config_wrapper

        # Make it config-aware
        @wraps(func)
        def basic_wrapper(state, config=None):
            # Call without config
            result = func(state)

            # Handle Command result
            if isinstance(result, Command):
                if command_goto and result.goto is None:
                    return Command(update=result.update, goto=command_goto)
                return result

            # Handle other results
            return Command(update=result, goto=command_goto)

        return basic_wrapper

    @classmethod
    def _merge_configs(
        cls,
        base_config: RunnableConfig | None = None,
        override_config: RunnableConfig | None = None,
    ) -> RunnableConfig | None:
        """Merge two RunnableConfigs.

        Args:
            base_config: Base configuration
            override_config: Configuration to override with

        Returns:
            Merged configuration or None if both inputs are None
        """
        if base_config is None and override_config is None:
            return None

        if base_config is None:
            return override_config

        if override_config is None:
            return base_config

        # Use RunnableConfigManager to merge
        return RunnableConfigManager.merge(base_config, override_config)

    @classmethod
    def _extract_from_config(
        cls, config: RunnableConfig | None, key: str, default: Any = None
    ) -> Any:
        """Extract a value from RunnableConfig's configurable section.

        Args:
            config: RunnableConfig to extract from
            key: Key to extract
            default: Default value if not found

        Returns:
            Extracted value or default
        """
        if config and "configurable" in config and key in config["configurable"]:
            return config["configurable"][key]
        return default

    @classmethod
    def _derive_input_mapping(cls, component: Any) -> dict[str, str]:
        """Derive input mapping based on component type.

        Args:
            component: Component to derive mapping for

        Returns:
            Input mapping dictionary
        """
        mapping = {}

        # For Engine components
        if isinstance(component, Engine):
            # Get schema fields
            try:
                if hasattr(component, "get_schema_fields"):
                    fields = component.get_schema_fields()
                    for field_name in fields:
                        mapping[field_name] = field_name
            except Exception:
                pass

            # Try to derive from engine type
            if isinstance(component, InvokableEngine):
                if component.engine_type == EngineType.LLM:
                    # For LLMs, include messages and common prompt variables
                    mapping["messages"] = "messages"
                    if hasattr(component, "prompt_template") and hasattr(
                        component.prompt_template, "input_variables"
                    ):
                        for var in component.prompt_template.input_variables:
                            mapping[var] = var
                elif component.engine_type in [
                    EngineType.VECTOR_STORE,
                    EngineType.RETRIEVER,
                ]:
                    # For search engines, map query
                    mapping["query"] = "query"
                    mapping["question"] = "query"
                    mapping["filter"] = "filter"
                    mapping["k"] = "k"

        # For callables, check parameter names
        elif callable(component):
            sig = inspect.signature(component)
            for param_name in sig.parameters:
                if param_name != "config" and param_name != "self":
                    mapping[param_name] = param_name

        # Common fallbacks
        if not mapping:
            for field in ["input", "query", "messages", "text"]:
                mapping[field] = field

        return mapping

    @classmethod
    def _derive_output_mapping(cls, component: Any) -> dict[str, str]:
        """Derive output mapping based on component type.

        Args:
            component: Component to derive mapping for

        Returns:
            Output mapping dictionary
        """
        mapping = {}

        # For Engine components
        if isinstance(component, Engine):
            # Try to use output schema
            try:
                output_schema = component.derive_output_schema()

                # Add fields from output schema
                if hasattr(output_schema, "model_fields"):
                    # Pydantic v2
                    for field_name in output_schema.model_fields:
                        mapping[field_name] = field_name
                elif hasattr(output_schema, "__fields__"):
                    # Pydantic v1
                    for field_name in output_schema.__fields__:
                        mapping[field_name] = field_name
            except (AttributeError, NotImplementedError):
                pass

            # Handle special cases by engine type
            if isinstance(component, InvokableEngine):
                if component.engine_type in [
                    EngineType.VECTOR_STORE,
                    EngineType.RETRIEVER,
                ]:
                    mapping["documents"] = "documents"
                    mapping["context"] = "context"
                elif component.engine_type == EngineType.LLM:
                    mapping["content"] = "output"

                    # If it has structured output, use that name
                    if (
                        hasattr(component, "structured_output_model")
                        and component.structured_output_model
                    ):
                        model_name = component.structured_output_model.__name__.lower()
                        mapping[model_name] = model_name

        # If still no mapping, use defaults
        if not mapping:
            mapping["output"] = "output"
            mapping["content"] = "output"
            mapping["result"] = "result"
            mapping["documents"] = "documents"

        return mapping
