"""Generic Engine Node Configuration with Type Safety and Field Registry Integration.

This module provides generic engine node configurations that can distinguish between
different engine types (LLM, RAG, etc.) while maintaining backwards compatibility.
It integrates with the field registry for standardized field definitions.
"""

from abc import ABC
from datetime import datetime
from typing import (
    Any,
    Dict,
    Generic,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)

from langgraph.types import Command, RetryPolicy, Send
from pydantic import BaseModel, Field

from haive.core.engine.base import Engine, EngineType
from haive.core.graph.common.types import ConfigLike, StateLike
from haive.core.graph.node.base_config import NodeConfig
from haive.core.graph.node.types import NodeType
from haive.core.logging.rich_logger import LogLevel, get_logger
from haive.core.schema.field_definition import FieldDefinition
from haive.core.schema.field_registry import CommonFieldSets, StandardFields

# Type variables for input/output schemas
TInput = TypeVar("TInput", bound=BaseModel)
TOutput = TypeVar("TOutput", bound=BaseModel)

# Get module logger
logger = get_logger(__name__)
logger.set_level(LogLevel.DEBUG)


class GenericEngineNodeConfig(NodeConfig, Generic[TInput, TOutput]):
    """Generic engine node with type-safe input/output schemas.

    This base class provides the foundation for type-safe engine nodes
    that can declare their input and output schemas explicitly.
    """

    # Core identity
    node_type: NodeType = Field(default=NodeType.ENGINE)
    engine: Engine | None = Field(default=None)
    engine_name: str | None = Field(default=None)

    # Schema definitions (new approach)
    input_schema: Type[TInput] | None = Field(default=None)
    output_schema: Type[TOutput] | None = Field(default=None)

    # Field registry integration
    input_field_defs: list[FieldDefinition] = Field(default_factory=list)
    output_field_defs: list[FieldDefinition] = Field(default_factory=list)

    # Legacy field mappings (backwards compatibility)
    input_fields: Union[List[str], Dict[str, str]] | None = Field(default=None)
    output_fields: Union[List[str], Dict[str, str]] | None = Field(default=None)

    # Engine attribution
    auto_add_engine_attribution: bool = Field(
        default=True, description="Automatically add engine_name to outputs"
    )

    # Options
    retry_policy: RetryPolicy | None = Field(default=None)
    use_send: bool = Field(default=False)
    debug: bool = Field(default=True)

    def model_post_init(self, __context):
        """Post-initialization to setup schemas from field definitions."""
        super().model_post_init(__context)
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

        with logger.track_time(f"Executing node {self.name}"):
            try:
                # Get engine
                engine = self._get_engine(state)
                if not engine:
                    raise ValueError(f"No engine available for node '{self.name}'")

                # Extract input using schema-aware method
                input_data = self._extract_typed_input(state, engine)

                # Execute engine
                result = self._execute_with_config(engine, input_data, config)

                # Wrap result with type-safe output
                wrapped = self._wrap_typed_result(result, state, engine)

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
        if self.output_schema:
            # Create typed output
            output_dict = {}

            # Map result to output schema fields
            if isinstance(result, dict):
                for field_name in self.output_schema.model_fields:
                    if field_name in result:
                        output_dict[field_name] = result[field_name]
            elif (
                hasattr(result, "content")
                and "ai_message" in self.output_schema.model_fields
            ):
                # Handle AIMessage result
                output_dict["ai_message"] = result

            # Add engine attribution if enabled
            if self.auto_add_engine_attribution and "engine_name" in output_dict:
                output_dict["engine_name"] = engine.name

            return output_dict
        # Fallback to original logic
        return self._wrap_smart_result(result, state, engine)

    # Placeholder methods for backwards compatibility
    def _get_engine(self, state: StateLike | None = None) -> Engine | None:
        """Get engine (to be implemented by subclasses or copied from original)."""
        raise NotImplementedError("Subclasses should implement _get_engine")

    def _extract_smart_input(self, state: StateLike, engine: Engine) -> Any:
        """Extract smart input (to be implemented by subclasses or copied from original)."""
        raise NotImplementedError("Subclasses should implement _extract_smart_input")

    def _execute_with_config(
        self, engine: Engine, input_data: Any, config: ConfigLike | None
    ) -> Any:
        """Execute engine with config (to be implemented by subclasses or copied from original)."""
        raise NotImplementedError("Subclasses should implement _execute_with_config")

    def _wrap_smart_result(
        self, result: Any, state: StateLike, engine: Engine
    ) -> Command | Send:
        """Wrap smart result (to be implemented by subclasses or copied from original)."""
        raise NotImplementedError("Subclasses should implement _wrap_smart_result")


# Specialized node configurations for different engine types


class LLMNodeConfig(GenericEngineNodeConfig[BaseModel, BaseModel]):
    """Specialized node configuration for LLM engines."""

    def __init__(self, **kwargs):
        # Set default field definitions for LLM nodes
        if "input_field_defs" not in kwargs:
            kwargs["input_field_defs"] = [StandardFields.messages(with_tokens=True)]
        if "output_field_defs" not in kwargs:
            kwargs["output_field_defs"] = [
                StandardFields.ai_message(),
                StandardFields.engine_name(),
            ]

        super().__init__(**kwargs)


class RAGNodeConfig(GenericEngineNodeConfig[BaseModel, BaseModel]):
    """Specialized node configuration for RAG engines."""

    def __init__(self, **kwargs):
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
        custom_input_fields: List[FieldDefinition] | None = None,
        custom_output_fields: List[FieldDefinition] | None = None,
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
        custom_input_fields: List[FieldDefinition] | None = None,
        custom_output_fields: List[FieldDefinition] | None = None,
        **kwargs,
    ) -> RAGNodeConfig:
        """Create a RAG node with optional custom fields."""
        if custom_input_fields:
            kwargs["input_field_defs"] = custom_input_fields
        if custom_output_fields:
            kwargs["output_field_defs"] = custom_output_fields

        return RAGNodeConfig(engine=engine, name=name, **kwargs)
