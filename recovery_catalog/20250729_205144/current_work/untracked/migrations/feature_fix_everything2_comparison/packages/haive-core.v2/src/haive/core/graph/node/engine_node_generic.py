"""Generic Engine Node Configuration with Type Safety and Field Registry Integration.

This module provides generic engine node configurations that can distinguish between
different engine types (LLM, RAG, etc.) while maintaining backwards compatibility. It
integrates with the field registry for standardized field definitions.
"""

import logging
from typing import Any, Generic, TypeVar, overload

from langgraph.graph import END
from langgraph.types import Command, RetryPolicy, Send
from pydantic import BaseModel, Field

from haive.core.engine.base import Engine, EngineType
from haive.core.graph.common.types import ConfigLike, StateLike
from haive.core.graph.node.base_config import NodeConfig
from haive.core.graph.node.types import NodeType
from haive.core.schema.field_definition import FieldDefinition
from haive.core.schema.field_registry import StandardFields

# Type variables for input/output schemas
TInput = TypeVar("TInput", bound=BaseModel)
TOutput = TypeVar("TOutput", bound=BaseModel)

# Get module logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class GenericEngineNodeConfig(NodeConfig, Generic[TInput, TOutput]):
    """Generic engine node with type-safe input/output schemas.

    This base class provides the foundation for type-safe engine nodes that can declare
    their input and output schemas explicitly.
    """

    # Core identity
    node_type: NodeType = Field(default=NodeType.ENGINE)
    engine: Engine | None = Field(default=None)
    engine_name: str | None = Field(default=None)

    # Schema definitions (new approach)
    input_schema: type[TInput] | None = Field(default=None)
    output_schema: type[TOutput] | None = Field(default=None)

    # Field registry integration
    input_field_defs: list[FieldDefinition] = Field(default_factory=list)
    output_field_defs: list[FieldDefinition] = Field(default_factory=list)

    # Legacy field mappings (backwards compatibility)
    input_fields: list[str] | dict[str, str] | None = Field(default=None)
    output_fields: list[str] | dict[str, str] | None = Field(default=None)

    # Engine attribution
    auto_add_engine_attribution: bool = Field(
        default=True, description="Automatically add engine_name to outputs"
    )

    # Options
    retry_policy: RetryPolicy | None = Field(default=None)
    use_send: bool = Field(default=False)
    debug: bool = Field(default=True)
    config_overrides: dict[str, Any] = Field(default_factory=dict)
    command_goto: str | None = Field(default=None)

    def model_post_init(self, __context) -> None:
        """Post-initialization to setup schemas from field definitions."""
        super().model_post_init(__context)

        # Setup default field definitions from engine if not provided (like EngineNodeConfig)
        if self.engine and not self.input_field_defs and not self.output_field_defs:
            self._setup_default_field_defs_from_engine()

        self._setup_schemas_from_field_defs()

    def _setup_schemas_from_field_defs(self):
        """Setup input/output schemas from field definitions if not provided."""
        if not self.input_schema and self.input_field_defs:
            self.input_schema = self._create_schema_from_fields(
                self.input_field_defs, f"{self.name}Input"
            )

        if not self.output_schema and self.output_field_defs:
            self.output_schema = self._create_schema_from_fields(
                self.output_field_defs, f"{self.name}Output"
            )

    def _create_schema_from_fields(
        self, field_defs: list[FieldDefinition], schema_name: str
    ) -> type[BaseModel]:
        """Create a Pydantic schema from field definitions."""
        from pydantic import create_model

        fields = {}
        for field_def in field_defs:
            field_info = field_def.to_field_info()
            fields[field_def.name] = field_info

        return create_model(schema_name, **fields)

    def _setup_default_field_defs_from_engine(self):
        """Setup default field definitions based on engine type (like EngineNodeConfig)."""
        if not self.engine:
            return

        from haive.core.schema.field_registry import StandardFields

        # Set defaults based on engine type
        if self.engine.engine_type == EngineType.LLM:
            if not self.input_field_defs:
                # Use the engine's derived input fields instead of hardcoding
                if hasattr(self.engine, "get_input_fields"):
                    engine_input_fields = self.engine.get_input_fields()
                    logger.debug(
                        f"Engine derived input fields: {
                            list(
                                engine_input_fields.keys())}"
                    )

                    # Convert engine fields to field definitions using
                    # StandardFields when possible
                    self.input_field_defs = []
                    for field_name, (
                        type_hint,
                        _field_info,
                    ) in engine_input_fields.items():
                        # Try to use StandardFields for known field types
                        try:
                            if field_name == "messages":
                                field_def = StandardFields.messages(use_enhanced=True)
                            elif field_name == "query":
                                field_def = StandardFields.query()
                            elif field_name == "context":
                                field_def = StandardFields.context()
                            else:
                                # For other fields, try StandardFields first,
                                # then fallback
                                field_method = getattr(StandardFields, field_name, None)
                                if field_method and callable(field_method):
                                    field_def = field_method()
                                else:
                                    # Create generic field definition
                                    from haive.core.schema.field_definition import (
                                        FieldDefinition,
                                    )

                                    field_def = FieldDefinition(
                                        name=field_name, type_hint=type_hint
                                    )

                            self.input_field_defs.append(field_def)
                        except Exception as e:
                            logger.debug(
                                f"Failed to create field definition for {field_name}: {e}"
                            )
                            # Fallback to generic field definition
                            from haive.core.schema.field_definition import (
                                FieldDefinition,
                            )

                            field_def = FieldDefinition(
                                name=field_name, type_hint=type_hint
                            )
                            self.input_field_defs.append(field_def)
                else:
                    # Fallback to messages only
                    self.input_field_defs = [StandardFields.messages(use_enhanced=True)]
            if not self.output_field_defs:
                # LLM engines should ONLY output to messages field
                # V2 structured output: Tool calls in AIMessage are extracted by downstream validation nodes
                # V1 regular output: AI response appended to messages
                self.output_field_defs = [
                    # ONLY messages field
                    StandardFields.messages(use_enhanced=True),
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

    def get_input_fields_for_state(self) -> dict[str, Any]:
        """Get input fields that should be included in state schema."""
        if self.input_field_defs:
            return {fd.name: fd.to_field_info() for fd in self.input_field_defs}
        return {}

    def get_output_fields_for_state(self) -> dict[str, Any]:
        """Get output fields that should be included in state schema."""
        if self.output_field_defs:
            return {fd.name: fd.to_field_info() for fd in self.output_field_defs}
        return {}

    def __call__(
        self, state: StateLike, config: ConfigLike | None = None
    ) -> Command | Send:
        """Execute the engine node with type-safe I/O."""
        logger.info("=" * 80)
        logger.info(f"GENERIC ENGINE NODE EXECUTION: {self.name}")
        logger.info("=" * 80)

        logger.debug(f"Starting execution of node {self.name}")
        try:
            # Get engine
            engine = self._get_engine(state)
            if not engine:
                raise ValueError(f"No engine available for node '{self.name}'")

            # Extract input using schema-aware method like EngineNodeConfig
            logger.info("Step 2: Extracting Input")
            logger.debug(f"Node input_schema: {self.input_schema}")
            logger.debug(f"Node input_field_defs: {self.input_field_defs}")
            logger.debug(
                f"State fields available: {
                    [
                        field for field in dir(state) if not field.startswith('_')]}"
            )

            if self.input_schema or self.input_field_defs:
                input_data = self.extract_input_from_state(state)
                logger.info(
                    f"Using schema-based input extraction: {
                        list(
                            input_data.keys()) if isinstance(
                            input_data,
                            dict) else type(input_data)}"
                )
                logger.debug(f"Extracted input_data: {input_data}")
            else:
                input_data = self._extract_smart_input(state, engine)
                logger.info("Using legacy smart input extraction")
                logger.debug(f"Smart extracted input_data: {input_data}")

            # Execute engine
            result = self._execute_with_config(engine, input_data, config)
            logger.debug(f"Engine execution returned: {type(result)} - {result}")

            # Wrap result with type-safe output
            logger.info("Step 4: Wrapping Result")
            wrapped = self._wrap_typed_result(result, state, engine)
            logger.info(f"Final wrapped result: {type(wrapped)} - {wrapped}")

            return wrapped

        except Exception as e:
            logger.exception(f"Error in {self.name}: {e}")
            raise

    def _extract_typed_input(self, state: StateLike, engine: Engine) -> Any:
        """Extract input using input schema if available."""
        if self.input_schema:
            # Extract only the fields defined in input schema
            input_dict = {}
            for field_name in self.input_schema.model_fields:
                if hasattr(state, field_name):
                    input_dict[field_name] = getattr(state, field_name)
            return input_dict
        # Fallback to original logic
        return self._extract_smart_input(state, engine)

    def _wrap_typed_result(
        self, result: Any, state: StateLike, engine: Engine
    ) -> Command | Send:
        """Wrap result using output schema if available."""
        logger.debug(
            f"_wrap_typed_result called with output_schema: {self.output_schema}"
        )

        if self.output_schema:
            logger.debug("Using typed output schema wrapping")
            # Create typed output
            output_dict = {}

            # Map result to output schema fields
            if isinstance(result, dict):
                for field_name in self.output_schema.model_fields:
                    if field_name in result:
                        output_dict[field_name] = result[field_name]
            elif hasattr(result, "content"):
                # Handle AIMessage result - check for both "ai_message" and "messages" fields
                if "ai_message" in self.output_schema.model_fields:
                    output_dict["ai_message"] = result
                elif "messages" in self.output_schema.model_fields:
                    # For LLM engines that output to messages field
                    output_dict["messages"] = [result]
                    logger.debug("Added AI message to messages field")
                else:
                    logger.warning(
                        f"AI message result but no ai_message or messages field in output schema: {list(self.output_schema.model_fields.keys())}"
                    )

            # Add engine attribution if enabled
            if self.auto_add_engine_attribution and "engine_name" in output_dict:
                output_dict["engine_name"] = engine.name

            logger.debug(f"Typed output_dict: {output_dict}")
            # Don't force goto=END, let the graph routing handle the flow
            if output_dict:
                return Command(update=output_dict)
            logger.warning("Empty output_dict - falling back to smart result wrapping")
            return self._wrap_smart_result(result, state, engine)

        # Fallback to original logic
        logger.debug("Falling back to _wrap_smart_result")
        return self._wrap_smart_result(result, state, engine)

    # Simple implementation - just copy the core method that was missing
    def _get_engine(self, state: StateLike | None = None) -> Engine | None:
        """Get engine from direct reference or state's engines dict."""
        # Priority 1: Direct engine reference
        if self.engine:
            return self.engine

        # Priority 2: Get from state's engines dict using engine_name
        if self.engine_name and state and hasattr(state, "engines"):
            engines_dict = getattr(state, "engines", {})
            if isinstance(engines_dict, dict) and self.engine_name in engines_dict:
                return engines_dict[self.engine_name]

        return None

    def _extract_smart_input(self, state: StateLike, engine: Engine) -> Any:
        """Extract input using the most appropriate strategy (like EngineNodeConfig)."""
        logger.debug(f"Extracting input for {engine.engine_type.value} engine...")

        # Strategy 1: Explicit mapping
        if hasattr(self, "input_fields") and self.input_fields:
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

    def _get_schema_inputs(
        self, state: StateLike, engine_name: str
    ) -> list[str] | None:
        """Get input fields from state schema mappings."""
        return (
            getattr(state, "__engine_io_mappings__", {})
            .get(engine_name, {})
            .get("inputs")
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

    def _normalize_mapping(self, mapping: dict[str, str] | list[str]) -> dict[str, str]:
        """Convert mapping to state_key -> input_key format."""
        if isinstance(mapping, list):
            return {field: field for field in mapping}
        return mapping

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

    def _extract_default_input(self, state: StateLike, engine_type: EngineType) -> Any:
        """Extract default input based on engine type."""
        logger.debug(f"Using default extraction for {engine_type.value}")

        if engine_type == EngineType.LLM:
            messages = self._get_state_value(state, "messages", [])
            return {"messages": messages}
        if engine_type == EngineType.RETRIEVER:
            query = (
                self._get_state_value(state, "query")
                or self._get_state_value(state, "messages", [""])[-1]
                if self._get_state_value(state, "messages")
                else ""
            )
            return {"query": query}
        if engine_type == EngineType.VECTOR_STORE:
            query = self._get_state_value(state, "query") or ""
            return {"query": query}
        if engine_type == EngineType.EMBEDDINGS:
            text = (
                self._get_state_value(state, "text")
                or self._get_state_value(state, "query")
                or ""
            )
            return text
        # Return state as-is for unknown types
        return state

    def _extract_retriever_fields(
        self, state: StateLike, fields: list[str]
    ) -> dict[str, Any]:
        """Retriever-specific extraction: ensure query is always present."""
        logger.debug("Extracting retriever fields")
        input_data = {}

        for field in fields:
            value = self._get_state_value(state, field)
            if field == "query":
                # Query is required for retrievers, use empty string if None
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
            field: self._get_state_value(state, field)
            for field in fields
            if self._get_state_value(state, field) is not None
        }

    def _execute_with_config(
        self, engine: Engine, input_data: Any, config: ConfigLike | None
    ) -> Any:
        """Execute engine with detailed debugging."""
        logger.info("Step 3: Engine Execution")
        logger.debug(f"Engine: {type(engine)} - {engine.name}")
        logger.debug(f"Input data type: {type(input_data)}")
        logger.debug(
            f"Input data keys: {list(input_data.keys()) if isinstance(input_data, dict) else 'Not a dict'}"
        )
        logger.debug(f"Config: {config}")

        # Log engine configuration details
        if hasattr(engine, "structured_output_model"):
            logger.debug(
                f"Engine structured_output_model: {engine.structured_output_model}"
            )
        if hasattr(engine, "structured_output_version"):
            logger.debug(
                f"Engine structured_output_version: {engine.structured_output_version}"
            )
        if hasattr(engine, "temperature"):
            logger.debug(f"Engine temperature: {engine.temperature}")

        try:
            logger.debug("🚀 Calling engine.invoke...")
            result = engine.invoke(input_data, config)
            logger.info("✅ Engine execution completed")
            logger.debug(f"Result type: {type(result)}")
            logger.debug(f"Result: {result}")

            # Check for tool calls if it's an AI message
            if hasattr(result, "tool_calls"):
                logger.debug(f"Tool calls: {result.tool_calls}")
                if result.tool_calls:
                    for i, tool_call in enumerate(result.tool_calls):
                        logger.debug(
                            f"  Tool call {i}: name={tool_call.get('name')}, args={tool_call.get('args')}"
                        )
                else:
                    logger.warning("❌ NO TOOL CALLS FOUND in AI message")

            return result
        except Exception as e:
            logger.exception(f"❌ Engine execution failed: {e}")
            import traceback

            logger.exception(f"Traceback: {traceback.format_exc()}")
            raise

    def _wrap_smart_result(
        self, result: Any, state: StateLike, engine: Engine
    ) -> Command | Send:
        """Simple result wrapping - handle messages for LLM engines."""
        logger.info("Step 4: Result Wrapping")
        logger.debug("🔍 WRAPPING RESULT:")
        logger.debug(f"   Result type: {type(result)}")
        logger.debug(f"   Result value: {result}")
        logger.debug(f"   Has content: {hasattr(result, 'content')}")
        logger.debug(f"   Has type: {hasattr(result, 'type')}")

        # Check if it's an AI message with structured output
        if hasattr(result, "content") and hasattr(result, "tool_calls"):
            logger.debug(
                f"   AI message with tool calls: {len(result.tool_calls) if result.tool_calls else 0}"
            )
            if result.tool_calls:
                for i, tool_call in enumerate(result.tool_calls):
                    logger.debug(
                        f"     Tool call {i}: {tool_call.get('name')} with args {tool_call.get('args')}"
                    )

        # Check if result is a message-like object
        if hasattr(result, "content") and hasattr(result, "type"):
            update = {"messages": [result]}
            logger.debug(
                f"   ✅ Treating as message, update keys: {list(update.keys())}"
            )
            logger.debug(
                f"   Message content length: {len(str(result.content)) if hasattr(result, 'content') else 'N/A'}"
            )
        else:
            update = {"result": result}
            logger.debug(
                f"   ⚠️  Treating as generic result, update keys: {list(update.keys())}"
            )

        logger.debug(f"   Creating Command with goto: {self.command_goto}")

        if update is None:
            logger.error("   ❌ UPDATE IS NONE! This will crash LangGraph!")
            update = {}

        # Fix: If command_goto is None, default to END
        goto = self.command_goto if self.command_goto is not None else END
        logger.debug(f"   Fixed goto: {goto}")

        # Log the final command being created
        command = Command(update=update, goto=goto)
        logger.info(
            f"✅ Created Command: update_keys={list(update.keys())}, goto={goto}"
        )
        logger.debug(f"   Command details: {command}")

        return command

    def extract_input_from_state(self, state: Any) -> dict[str, Any]:
        """Extract input fields from state using engine-aware logic (like
        EngineNodeConfig).
        """
        logger.debug("Generic engine node extracting input from state...")

        # Use input schema if available
        if self.input_schema:
            input_dict = {}
            for field_name in self.input_schema.model_fields:
                value = self._get_state_value(state, field_name)
                if value is not None:
                    input_dict[field_name] = value
            logger.debug(f"Schema-based extraction: {list(input_dict.keys())}")
            return input_dict

        # Use field definitions if available
        if self.input_field_defs:
            input_dict = {}
            for field_def in self.input_field_defs:
                value = self._get_state_value(state, field_def.name)
                if value is not None:
                    input_dict[field_def.name] = value
            logger.debug(
                f"Field definition extraction: {
                    list(
                        input_dict.keys())}"
            )
            return input_dict

        logger.debug("No input schema or field defs, returning empty dict")
        return {}

    def _get_state_value(self, state: Any, key: str, default: Any = None) -> Any:
        """Get value from state with fallback (like EngineNodeConfig)."""
        if hasattr(state, key):
            return getattr(state, key)
        if isinstance(state, dict):
            return state.get(key, default)
        return default


# Specialized node configurations for different engine types


class LLMNodeConfig(GenericEngineNodeConfig[BaseModel, BaseModel]):
    """Specialized node configuration for LLM engines."""

    def __init__(self, **kwargs) -> None:
        # For LLM engines, prefer using the engine's own input/output schemas if available
        # Only set defaults if no field defs are provided and engine doesn't
        # have schemas
        engine = kwargs.get("engine")

        if "input_field_defs" not in kwargs and engine:
            # Check if engine has its own input schema
            if not (hasattr(engine, "input_schema") and engine.input_schema):
                kwargs["input_field_defs"] = [
                    StandardFields.messages(use_enhanced=True)
                ]

        if "output_field_defs" not in kwargs and engine:
            # Check if engine has its own output schema
            if not (hasattr(engine, "output_schema") and engine.output_schema):
                # LLM engines should ONLY output to messages field
                # V2 structured output: Tool calls in AIMessage are extracted
                # by downstream validation nodes
                kwargs["output_field_defs"] = [
                    # ONLY messages field
                    StandardFields.messages(use_enhanced=True),
                ]

        super().__init__(**kwargs)


class RAGNodeConfig(GenericEngineNodeConfig[BaseModel, BaseModel]):
    """Specialized node configuration for RAG engines."""

    def __init__(self, **kwargs) -> None:
        # Set default field definitions for RAG nodes
        if "input_field_defs" not in kwargs:
            kwargs["input_field_defs"] = [
                StandardFields.query(),
                StandardFields.messages(),
            ]
        if "output_field_defs" not in kwargs:
            kwargs["output_field_defs"] = [
                StandardFields.context(),
                StandardFields.documents(),
                StandardFields.engine_name(),
            ]

        super().__init__(**kwargs)


# Factory functions with overloads for type safety


@overload
def create_engine_node(
    engine: Engine, name: str, *, engine_type: EngineType.LLM
) -> LLMNodeConfig: ...


@overload
def create_engine_node(
    engine: Engine, name: str, *, engine_type: EngineType.RETRIEVER
) -> RAGNodeConfig: ...


@overload
def create_engine_node(engine: Engine, name: str) -> GenericEngineNodeConfig: ...


# Convenience class methods for creating specific node types


class NodeFactory:
    """Factory for creating specialized node configurations."""

    @classmethod
    def llm_node(
        cls,
        engine: Engine,
        name: str,
        custom_input_fields: list[FieldDefinition] | None = None,
        custom_output_fields: list[FieldDefinition] | None = None,
        **kwargs,
    ) -> LLMNodeConfig:
        """Create an LLM node with optional custom fields."""
        if custom_input_fields:
            kwargs["input_field_defs"] = custom_input_fields
        if custom_output_fields:
            kwargs["output_field_defs"] = custom_output_fields

        return LLMNodeConfig(engine=engine, name=name, **kwargs)

    @classmethod
    def rag_node(
        cls,
        engine: Engine,
        name: str,
        custom_input_fields: list[FieldDefinition] | None = None,
        custom_output_fields: list[FieldDefinition] | None = None,
        **kwargs,
    ) -> RAGNodeConfig:
        """Create a RAG node with optional custom fields."""
        if custom_input_fields:
            kwargs["input_field_defs"] = custom_input_fields
        if custom_output_fields:
            kwargs["output_field_defs"] = custom_output_fields

        return RAGNodeConfig(engine=engine, name=name, **kwargs)
