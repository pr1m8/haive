# src/haive/core/graph/node/engine_node.py

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Type, Union

from langgraph.types import Command, RetryPolicy, Send
from pydantic import BaseModel, Field

from haive.core.engine.base import Engine, EngineType
from haive.core.graph.common.types import ConfigLike, StateLike
from haive.core.graph.node.base_config import NodeConfig
from haive.core.graph.node.types import NodeType
from haive.core.logging.rich_logger import LogLevel, get_logger

# Get module logger
logger = get_logger(__name__)
logger.set_level(LogLevel.DEBUG)


class EngineNodeConfig(NodeConfig):
    """Engine-based node with intelligent I/O handling and schema support.

    This node config extends the base NodeConfig with engine-specific functionality
    while maintaining the new input/output schema pattern for better state utilization.
    """

    # Core identity
    node_type: NodeType = Field(default=NodeType.ENGINE)
    engine: Engine | None = Field(default=None)

    # Legacy field mappings (backwards compatibility)
    input_fields: list[str] | dict[str, str] | None = Field(default=None)
    output_fields: list[str] | dict[str, str] | None = Field(default=None)

    # Options
    retry_policy: RetryPolicy | None = Field(default=None)
    use_send: bool = Field(default=False)
    debug: bool = Field(default=True)

    def model_post_init(self, __context):
        """Post-initialization to setup engine-specific configurations."""
        # Set engine_name from engine if not provided
        if self.engine and not self.engine_name:
            self.engine_name = self.engine.name

        # Setup default field definitions based on engine type if not provided
        if self.engine and not self.input_field_defs and not self.output_field_defs:
            self._setup_default_field_defs_from_engine()

        # Call parent post_init to handle schema setup
        super().model_post_init(__context)

    def _setup_default_field_defs_from_engine(self):
        """Setup default field definitions based on engine type."""
        if not self.engine:
            return

        from haive.core.schema.field_registry import StandardFields

        # Set defaults based on engine type
        if self.engine.engine_type == EngineType.LLM:
            if not self.input_field_defs:
                self.input_field_defs = [StandardFields.messages(use_enhanced=True)]
            if not self.output_field_defs:
                self.output_field_defs = [
                    StandardFields.ai_message(),
                    StandardFields.engine_name(),
                ]

        elif self.engine.engine_type == EngineType.RETRIEVER:
            if not self.input_field_defs:
                self.input_field_defs = [
                    StandardFields.query(),
                    StandardFields.messages(use_enhanced=True),
                ]
            if not self.output_field_defs:
                # Use the actual output schema from the retriever engine
                # The retriever output schema has 'retrieved_documents' field
                self.output_field_defs = (
                    []
                )  # Let it use the engine's actual output schema

        # Add structured output field if engine has structured_output_model
        if (
            hasattr(self.engine, "structured_output_model")
            and self.engine.structured_output_model
        ):
            structured_field = StandardFields.structured_output(
                self.engine.structured_output_model
            )
            if structured_field not in self.output_field_defs:
                self.output_field_defs.append(structured_field)

    def __call__(
        self, state: StateLike, config: ConfigLike | None = None
    ) -> Command | Send:
        """Execute engine node with schema-aware I/O handling."""
        logger.info("=" * 80)
        logger.info(f"ENGINE NODE EXECUTION: {self.name}")
        logger.info("=" * 80)

        with logger.track_time(f"Executing node {self.name}"):
            try:
                # Get engine and validate
                logger.info("Step 1: Getting Engine")
                engine = self._get_engine(state)
                if not engine:
                    logger.error(f"No engine available for node '{self.name}'")
                    logger.error(f"  engine_name: {self.engine_name}")
                    logger.error(f"  direct engine: {self.engine}")
                    raise ValueError(f"No engine available for node '{self.name}'")

                logger.info(
                    f"✅ Got engine: {engine.name} (type: {engine.engine_type.value})"
                )

                # Extract input using schema-aware method
                logger.info("Step 2: Extracting Input")
                if self.input_schema or self.input_field_defs:
                    input_data = self.extract_input_from_state(state)
                    logger.info(
                        f"Using schema-based input extraction: {list(input_data.keys()) if isinstance(input_data, dict) else type(input_data)}"
                    )
                else:
                    input_data = self._extract_smart_input(state, engine)
                    logger.info("Using legacy smart input extraction")

                logger.debug(f"Input data type: {type(input_data).__name__}")
                if isinstance(input_data, dict):
                    logger.debug(f"Input keys: {list(input_data.keys())}")
                    for key, value in input_data.items():
                        logger.debug(
                            f"  {key}: {type(value).__name__} = {str(value)[:100]}..."
                        )
                else:
                    logger.debug(f"Input value: {str(input_data)[:200]}...")

                # Execute with merged config
                logger.info("Step 3: Executing Engine")
                result = self._execute_with_config(engine, input_data, config)

                # Log result details
                logger.debug(f"Result type: {type(result).__name__}")
                self._log_result_details(result)

                # Wrap result using schema-aware method
                logger.info("Step 4: Creating Update")
                if self.output_schema or self.output_field_defs:
                    wrapped = self.create_output_for_state(result)
                    logger.info(
                        f"Using schema-based output creation: {list(wrapped.keys()) if isinstance(wrapped, dict) else type(wrapped)}"
                    )
                else:
                    wrapped = self._wrap_smart_result(result, state, engine)
                    logger.info("Using legacy smart result wrapping")

                # Log final update
                self._log_final_update(wrapped)

                logger.info(f"✅ ENGINE NODE COMPLETED: {self.name}")

                return wrapped

            except Exception as e:
                self._log_error(e)
                raise

    def _get_engine(self, state: StateLike | None = None) -> Engine | None:
        """Get engine from direct reference or state's engines dict."""
        logger.debug("Getting engine...")

        # Priority 1: Direct engine reference
        if self.engine:
            logger.debug(f"Using direct engine reference: {self.engine.name}")
            return self.engine

        # Priority 2: Get from state's engines dict using engine_name
        if self.engine_name and state:
            logger.debug(f"Looking for engine_name: {self.engine_name}")

            # Try to get from engines dict in state
            if hasattr(state, "engines"):
                engines_dict = getattr(state, "engines", {})
                logger.debug(
                    f"Found state.engines dict with {len(engines_dict)} engines"
                )

                if isinstance(engines_dict, dict):
                    # Log available engines
                    if engines_dict:
                        logger.debug("Available engines in state:")
                        for name, eng in engines_dict.items():
                            logger.debug(f"  - {name}: {type(eng).__name__}")

                    if self.engine_name in engines_dict:
                        engine = engines_dict[self.engine_name]
                        if engine:
                            logger.info(
                                f"✅ Found engine '{self.engine_name}' in state.engines!"
                            )
                            self.engine = engine  # Cache it
                            return engine
                        logger.error(f"Engine '{self.engine_name}' exists but is None")
                    else:
                        logger.error(
                            f"Engine '{self.engine_name}' not found in state.engines"
                        )
                        logger.error(f"Available engines: {list(engines_dict.keys())}")
                else:
                    logger.error(f"state.engines is not a dict: {type(engines_dict)}")
            else:
                logger.debug("State has no 'engines' attribute")

                # Also check if state is a dict with engines key
                if isinstance(state, dict) and "engines" in state:
                    logger.debug("State is a dict, checking state['engines']...")
                    engines_dict = state["engines"]
                    if (
                        isinstance(engines_dict, dict)
                        and self.engine_name in engines_dict
                    ):
                        engine = engines_dict[self.engine_name]
                        if engine:
                            logger.info(
                                f"✅ Found engine '{self.engine_name}' in state['engines']!"
                            )
                            self.engine = engine  # Cache it
                            return engine

        logger.error("No engine found!")
        return None

    def _log_result_details(self, result: Any):
        """Log details about the result."""
        try:
            from langchain_core.messages import AIMessage, BaseMessage

            if isinstance(result, BaseMessage):
                logger.info(f"✅ Result is a {type(result).__name__}")
                logger.debug(f"  Content: {result.content[:200]}...")

                if isinstance(result, AIMessage) and hasattr(result, "tool_calls"):
                    if result.tool_calls:
                        logger.debug(f"  Tool Calls: {len(result.tool_calls)}")
        except ImportError:
            pass

        if isinstance(result, dict):
            logger.debug("Result is a dictionary:")
            for key, value in result.items():
                logger.debug(f"  {key}: {type(value).__name__}")
        elif isinstance(result, str):
            logger.debug(f"Result is string: {result[:200]}...")
        else:
            logger.debug(f"Result: {str(result)[:200]}...")

    def _log_final_update(self, wrapped: Command | Send):
        """Log the final wrapped update."""
        logger.info("Final Update:")

        if isinstance(wrapped, Command):
            logger.info("  Type: Command")
            logger.info(f"  Goto: {wrapped.goto}")

            if wrapped.update:
                logger.debug("  Update dict:")
                for key, value in wrapped.update.items():
                    if key == "messages":
                        if isinstance(value, list):
                            logger.debug(f"    {key}: List with {len(value)} messages")
                            if value:
                                last_msg = value[-1]
                                logger.debug(
                                    f"      Last message type: {type(last_msg).__name__}"
                                )
                        else:
                            logger.debug(f"    {key}: {type(value).__name__}")
                    else:
                        logger.debug(f"    {key}: {str(value)[:100]}...")
        elif isinstance(wrapped, Send):
            logger.info("  Type: Send")
            logger.info(f"  Node: {wrapped.node}")
            logger.debug(f"  Arg type: {type(wrapped.arg).__name__}")

    def _extract_smart_input(self, state: StateLike, engine: Engine) -> Any:
        """Extract input using the most appropriate strategy."""
        logger.debug(f"Extracting input for {engine.engine_type.value} engine...")

        # Strategy 1: Explicit mapping
        if self.input_fields:
            logger.debug("Using explicit input field mapping")
            return self._extract_mapped_input(
                state, self._normalize_mapping(self.input_fields)
            )

        # Strategy 2: Schema-defined inputs
        schema_inputs = self._get_schema_inputs(state, engine.name)
        if schema_inputs:
            logger.debug(f"Using schema-defined inputs: {schema_inputs}")
            return self._extract_typed_input(state, schema_inputs, engine.engine_type)

        # Strategy 3: Engine-defined inputs
        engine_inputs = self._get_engine_inputs(engine)
        if engine_inputs:
            logger.debug(f"Using engine-defined inputs: {engine_inputs}")
            return self._extract_typed_input(state, engine_inputs, engine.engine_type)

        # Strategy 4: Type-based defaults
        logger.debug("Using type-based default extraction")
        return self._extract_default_input(state, engine.engine_type)

    def _extract_typed_input(
        self, state: StateLike, fields: list[str], engine_type: EngineType
    ) -> dict[str, Any]:
        """Extract fields with type-specific intelligence."""
        logger.debug(f"Extracting typed input for {engine_type.value}")

        extractors = {
            EngineType.RETRIEVER: self._extract_retriever_fields,
            EngineType.LLM: self._extract_llm_fields,
            EngineType.VECTOR_STORE: self._extract_vectorstore_fields,
            EngineType.EMBEDDINGS: self._extract_embeddings_fields,
            EngineType.AGENT: self._extract_agent_fields,
        }

        extractor = extractors.get(engine_type, self._extract_generic_fields)
        return extractor(state, fields)

    def _extract_retriever_fields(
        self, state: StateLike, fields: list[str]
    ) -> dict[str, Any]:
        """Retriever-specific extraction: always include query, filter None values."""
        logger.debug("Extracting retriever fields")
        input_data = {}

        for field in fields:
            value = self._get_state_value(state, field)

            if field == "query":
                # Always include query, even if empty
                input_data[field] = value or ""
                logger.debug(f"Retriever query: '{value or ''}'")
            elif value is not None:
                # Only include other fields if they have values
                input_data[field] = value
                logger.debug(f"Retriever {field}: {value}")
            else:
                logger.debug(f"Skipping None value for {field}")

        return input_data

    def _extract_llm_fields(
        self, state: StateLike, fields: list[str]
    ) -> dict[str, Any]:
        """LLM-specific extraction: include all fields."""
        logger.debug("Extracting LLM fields")
        result = {field: self._get_state_value(state, field) for field in fields}
        logger.debug(f"LLM input fields: {list(result.keys())}")
        return result

    def _extract_vectorstore_fields(
        self, state: StateLike, fields: list[str]
    ) -> dict[str, Any]:
        """Vector store extraction: filter None values except query."""
        logger.debug("Extracting vector store fields")
        input_data = {}
        for field in fields:
            value = self._get_state_value(state, field)
            if field == "query" or value is not None:
                input_data[field] = value
        return input_data

    def _extract_embeddings_fields(self, state: StateLike, fields: list[str]) -> Any:
        """Embeddings extraction: often just needs text."""
        logger.debug("Extracting embeddings fields")
        # Try to get text/query field first
        for field in ["query", "text", "content"]:
            if field in fields:
                value = self._get_state_value(state, field)
                if value:
                    logger.debug(
                        f"Using {field} field for embeddings: {str(value)[:100]}..."
                    )
                    return value

        # Fall back to all fields as dict
        return {field: self._get_state_value(state, field) for field in fields}

    def _extract_agent_fields(
        self, state: StateLike, fields: list[str]
    ) -> dict[str, Any]:
        """Agent-specific extraction: include all fields, prioritize messages."""
        logger.debug("Extracting agent fields")
        result = {}

        # Always include messages if it's in the fields
        if "messages" in fields:
            messages = self._get_state_value(state, "messages", [])
            result["messages"] = messages
            logger.debug(f"Agent messages: {len(messages) if messages else 0} messages")

        # Include all other fields
        for field in fields:
            if field != "messages":  # Already handled
                value = self._get_state_value(state, field)
                if value is not None:
                    result[field] = value
                    logger.debug(f"Agent {field}: {type(value).__name__}")

        return result

    def _extract_generic_fields(
        self, state: StateLike, fields: list[str]
    ) -> dict[str, Any]:
        """Generic extraction: include non-None values."""
        logger.debug("Extracting generic fields")
        return {
            field: value
            for field in fields
            if (value := self._get_state_value(state, field)) is not None
        }

    def _extract_default_input(self, state: StateLike, engine_type: EngineType) -> Any:
        """Default extraction when no fields are specified."""
        logger.debug(f"Using default extraction for {engine_type.value}")

        defaults = {
            EngineType.RETRIEVER: lambda: self._extract_retriever_fields(
                state, ["query", "k", "filter", "search_type", "score_threshold"]
            ),
            EngineType.LLM: lambda: {
                "messages": self._get_state_value(state, "messages", [])
            },
            EngineType.VECTOR_STORE: lambda: self._extract_vectorstore_fields(
                state, ["query", "k", "filter"]
            ),
            EngineType.EMBEDDINGS: lambda: self._get_state_value(state, "query", ""),
            EngineType.AGENT: lambda: self._state_as_dict(
                state
            ),  # Agents typically need full state
        }

        extractor = defaults.get(engine_type, lambda: self._state_as_dict(state))
        return extractor()

    def _wrap_smart_result(
        self, result: Any, state: StateLike, engine: Engine
    ) -> Command | Send:
        """Intelligently wrap result based on type and configuration."""
        logger.debug("Wrapping result...")

        # Already wrapped? Return as-is
        if isinstance(result, Command | Send):
            logger.debug("Result already wrapped, returning as-is")
            return result

        # Generate update dictionary
        update = self._create_update_dict(result, state, engine)

        # Return appropriate wrapper
        if self.use_send and self.command_goto:
            logger.debug(f"Creating Send to {self.command_goto}")
            return Send(node=self.command_goto, arg=update)
        logger.debug(f"Creating Command with goto={self.command_goto}")
        return Command(update=update, goto=self.command_goto)

    def _create_update_dict(
        self, result: Any, state: StateLike, engine: Engine
    ) -> dict[str, Any]:
        """Create state update dictionary from result."""
        logger.debug("Creating update dictionary...")

        # Strategy 1: Explicit output mapping
        if self.output_fields:
            logger.debug("Using explicit output field mapping")
            return self._apply_output_mapping(result)

        # Strategy 2: Schema-defined outputs
        schema_outputs = self._get_schema_outputs(state, engine.name)
        if schema_outputs:
            logger.debug(f"Using schema-defined outputs: {schema_outputs}")
            return self._map_to_outputs(result, schema_outputs)

        # Strategy 3: Smart type-based mapping
        logger.debug("Using smart type-based result mapping")
        return self._smart_result_mapping(result, state, engine.engine_type)

    def _smart_result_mapping(
        self, result: Any, state: StateLike, engine_type: EngineType
    ) -> dict[str, Any]:
        """Smart result mapping based on result type and engine type."""
        logger.debug(f"Smart result mapping for {engine_type.value} engine...")

        # Check if it's a message first
        if self._is_message_like(result):
            logger.info("✅ Result is message-like, updating messages")
            return self._update_messages(result, state)

        # Check if it's a string that might be a response from LLM
        if isinstance(result, str) and engine_type == EngineType.LLM:
            logger.info(
                "LLM returned string, converting to AIMessage and updating messages"
            )
            try:
                from langchain_core.messages import AIMessage

                ai_msg = AIMessage(content=result)
                return self._update_messages(ai_msg, state)
            except ImportError:
                logger.exception("Could not import AIMessage")

        # Agent results are typically full state updates
        if engine_type == EngineType.AGENT and isinstance(result, dict):
            logger.info("Agent returned dict state update")
            return result

        # Dictionary results
        if isinstance(result, dict):
            logger.debug("Result is dict, returning as-is")
            if "messages" in result:
                logger.debug("Dict contains 'messages' key")
            return result

        # Engine-specific single value mapping
        field_map = {
            EngineType.RETRIEVER: "documents",
            EngineType.LLM: "response",
            EngineType.EMBEDDINGS: "embeddings",
            EngineType.VECTOR_STORE: "documents",
            EngineType.AGENT: "agent_output",  # Generic field for agent outputs
        }

        field = field_map.get(engine_type, "result")
        logger.debug(f"Mapping result to field: {field}")
        return {field: result}

    def _update_messages(self, result: Any, state: StateLike) -> dict[str, Any]:
        """Update messages list with new message(s)."""
        logger.info("Updating messages list...")

        # Get existing messages
        existing = self._get_state_value(state, "messages", [])
        logger.debug(f"Existing messages: {len(existing) if existing else 0}")

        # Create new list
        messages = list(existing) if existing else []

        # Add new messages
        if isinstance(result, list):
            messages.extend(result)
            logger.debug(f"Added {len(result)} messages")
        else:
            messages.append(result)
            logger.debug(f"Added 1 message: {type(result).__name__}")

        logger.info(f"✅ Total messages after update: {len(messages)}")

        return {"messages": messages}

    def _is_message_like(self, obj: Any) -> bool:
        """Check if object is message-like."""
        try:
            from langchain_core.messages import BaseMessage

            is_msg = isinstance(obj, BaseMessage)
            if is_msg:
                logger.debug(f"✅ Object is a BaseMessage: {type(obj).__name__}")
            return is_msg
        except ImportError:
            logger.debug("Could not import BaseMessage, checking attributes")
            has_attrs = hasattr(obj, "content") and hasattr(obj, "type")
            if has_attrs:
                logger.debug("Object has message-like attributes")
            return has_attrs

    # ... rest of utility methods remain the same ...

    def _get_state_value(self, state: StateLike, key: str, default: Any = None) -> Any:
        """Get value from state with fallback."""
        if hasattr(state, key):
            return getattr(state, key)
        if isinstance(state, dict):
            return state.get(key, default)
        return default

    def _get_schema_inputs(
        self, state: StateLike, engine_name: str
    ) -> list[str] | None:
        """Get engine inputs from schema."""
        if not hasattr(state, "__engine_io_mappings__") or not engine_name:
            return None
        return (
            getattr(state, "__engine_io_mappings__", {})
            .get(engine_name, {})
            .get("inputs")
        )

    def _get_schema_outputs(
        self, state: StateLike, engine_name: str
    ) -> list[str] | None:
        """Get engine outputs from schema."""
        if not hasattr(state, "__engine_io_mappings__") or not engine_name:
            return None
        return (
            getattr(state, "__engine_io_mappings__", {})
            .get(engine_name, {})
            .get("outputs")
        )

    def _get_engine_inputs(self, engine: Engine) -> list[str] | None:
        """Get input fields from engine definition."""
        if hasattr(engine, "get_input_fields"):
            return list(engine.get_input_fields().keys())
        return None

    def _extract_mapped_input(
        self, state: StateLike, mapping: dict[str, str]
    ) -> dict[str, Any]:
        """Extract using explicit state->input mapping."""
        logger.debug(f"Extracting with mapping: {mapping}")
        return {
            input_key: self._get_state_value(state, state_key)
            for state_key, input_key in mapping.items()
            if self._get_state_value(state, state_key) is not None
        }

    def _apply_output_mapping(self, result: Any) -> dict[str, Any]:
        """Apply explicit output mapping."""
        mapping = self._normalize_mapping(self.output_fields)
        logger.debug(f"Applying output mapping: {mapping}")

        if isinstance(result, dict):
            return {
                state_key: result.get(result_key)
                for result_key, state_key in mapping.items()
                if result_key in result
            }
        # Single value to first mapped field
        if mapping:
            first_state_key = next(iter(mapping.values()))
            return {first_state_key: result}
        return {"result": result}

    def _map_to_outputs(self, result: Any, output_fields: list[str]) -> dict[str, Any]:
        """Map result to schema output fields."""
        if isinstance(result, dict):
            return {
                field: result.get(field) for field in output_fields if field in result
            }
        return {output_fields[0]: result} if output_fields else {"result": result}

    def _execute_with_config(
        self, engine: Engine, input_data: Any, config: ConfigLike | None
    ) -> Any:
        """Execute engine with merged configuration."""
        merged_config = self._build_merged_config(config, engine)

        # Log execution details
        logger.debug(f"Executing engine: {engine.name}")
        logger.debug(f"Engine type: {getattr(engine, 'engine_type', 'unknown')}")
        logger.debug(f"Input type: {type(input_data).__name__}")

        # Special handling for retrievers - they need string queries
        if hasattr(engine, "engine_type") and engine.engine_type.value == "retriever":
            logger.info("RETRIEVER DETECTED - Special handling")

            if isinstance(input_data, dict):
                if "query" in input_data:
                    query_str = str(input_data["query"])
                    logger.debug(f"Extracting query string: '{query_str}'")
                    logger.debug(
                        f"Other params: {[k for k in input_data if k != 'query']}"
                    )
                    return engine.invoke(query_str, merged_config)
                logger.debug("No 'query' key in dict, using whole dict as string")
                return engine.invoke(str(input_data), merged_config)
            logger.debug(f"Input is not dict, converting to string: '{input_data!s}'")
            return engine.invoke(str(input_data), merged_config)

        logger.debug("Standard engine invoke")
        return engine.invoke(input_data, merged_config)

    def _build_merged_config(
        self, runtime_config: ConfigLike | None, engine: Engine
    ) -> dict[str, Any] | None:
        """Build merged configuration."""
        if not runtime_config and not self.config_overrides:
            return None

        config = dict(runtime_config or {})

        # Ensure configurable section
        config.setdefault("configurable", {})

        # Apply node-level overrides
        config["configurable"].update(self.config_overrides)

        # Apply engine-specific overrides
        engine_id = getattr(engine, "id", None)
        if engine_id and self.config_overrides:
            config["configurable"].setdefault("engine_configs", {})
            config["configurable"]["engine_configs"].setdefault(engine_id, {})
            config["configurable"]["engine_configs"][engine_id].update(
                self.config_overrides
            )

        return config

    def _normalize_mapping(
        self, fields: list[str] | dict[str, str] | None
    ) -> dict[str, str]:
        """Normalize field mapping to dict."""
        if isinstance(fields, list):
            return {field: field for field in fields}
        return fields or {}

    def _state_as_dict(self, state: StateLike) -> dict[str, Any]:
        """Convert state to dictionary."""
        if isinstance(state, dict):
            return state
        if hasattr(state, "model_dump"):
            return state.model_dump()
        if hasattr(state, "__dict__"):
            return state.__dict__
        return {"value": state}

    def _log_error(self, error: Exception) -> None:
        """Log error with full context."""
        logger.log_exception(error, f"Engine node '{self.name}' failed")

    def __repr__(self) -> str:
        """Clean string representation."""
        engine_ref = self.engine.name if self.engine else self.engine_name or "None"
        return f"EngineNode(name='{self.name}', engine='{engine_ref}')"


# Factory function for creating appropriate node configs
def create_engine_node_config(engine: Engine, name: str, **kwargs) -> NodeConfig:
    """Factory function to create appropriate node config based on engine type.

    Routes agents to AgentNodeConfig if available, otherwise uses EngineNodeConfig.

    Args:
        engine: The engine to create a node for
        name: Name for the node
        **kwargs: Additional configuration parameters

    Returns:
        Appropriate NodeConfig subclass instance
    """
    # Check if it's an agent
    if hasattr(engine, "engine_type") and engine.engine_type == EngineType.AGENT:
        try:
            # Try to import AgentNodeConfig
            from haive.core.graph.node.agent_node import AgentNodeConfig

            logger.debug(f"Creating AgentNodeConfig for agent: {name}")
            return AgentNodeConfig(name=name, engine=engine, **kwargs)
        except ImportError:
            # Fall back to regular EngineNodeConfig
            logger.debug(
                "AgentNodeConfig not available, using EngineNodeConfig for agent"
            )

    # Default to EngineNodeConfig
    return EngineNodeConfig(
        name=name, engine=engine, node_type=NodeType.ENGINE, **kwargs
    )
