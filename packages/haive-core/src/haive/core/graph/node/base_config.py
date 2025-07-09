# src/haive/core/graph/node/config.py
import logging
import uuid
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type

from langgraph.graph import END
from pydantic import BaseModel, Field

from haive.core.graph.node.types import CommandGoto, NodeType
from haive.core.schema.field_definition import FieldDefinition

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class NodeConfig(ABC, BaseModel):
    """
    Base configuration for a node in a graph with input/output schema support.

    This base class supports the LangGraph multiple schemas pattern where nodes
    can declare their input and output schemas as subsets of the overall state.
    This enables better state utilization and clearer node interfaces.

    Key features:
    - Input/output schema declarations
    - Field registry integration
    - Engine attribution support
    - Runtime configuration
    """

    # Core identification
    id: str = Field(
        default_factory=lambda: f"node_{uuid.uuid4().hex[:8]}",
        description="Unique identifier for this node",
    )
    name: str = Field(description="Name of the node in the graph")
    node_type: NodeType = Field(description="Type of node")

    # Schema definitions (LangGraph multiple schemas pattern)
    input_schema: Optional[Type[BaseModel]] = Field(
        default=None, description="Input schema for this node (subset of state)"
    )
    output_schema: Optional[Type[BaseModel]] = Field(
        default=None, description="Output schema for this node (subset of state)"
    )

    # Field registry integration
    input_field_defs: List[FieldDefinition] = Field(
        default_factory=list, description="Input field definitions for this node"
    )
    output_field_defs: List[FieldDefinition] = Field(
        default_factory=list, description="Output field definitions for this node"
    )

    # Engine attribution
    auto_add_engine_attribution: bool = Field(
        default=True, description="Automatically add engine_name/engine_id to outputs"
    )
    engine_name: Optional[str] = Field(
        default=None, description="Engine name for attribution"
    )

    # Control flow
    command_goto: Optional[CommandGoto] = Field(
        default=END, description="Next node to go to after this node (or END)"
    )

    # Runtime configuration
    config_overrides: Dict[str, Any] = Field(
        default_factory=dict, description="Configuration overrides for this node"
    )

    # Config schema for runtime parameters
    config_schema: Optional[Type[BaseModel]] = Field(
        default=None, description="Schema for runtime configuration parameters"
    )

    # Metadata
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata for this node"
    )

    model_config = {"arbitrary_types_allowed": True}

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
        self, field_defs: List[FieldDefinition], schema_name: str
    ) -> Type[BaseModel]:
        """Create a Pydantic schema from field definitions."""
        from pydantic import create_model

        fields = {}
        for field_def in field_defs:
            field_info = field_def.to_field_info()
            fields[field_def.name] = field_info

        return create_model(schema_name, **fields)

    def get_input_fields_for_state(self) -> Dict[str, Any]:
        """Get input fields that should be included in overall state schema."""
        if self.input_field_defs:
            return {fd.name: fd.to_field_info() for fd in self.input_field_defs}
        return {}

    def get_output_fields_for_state(self) -> Dict[str, Any]:
        """Get output fields that should be included in overall state schema."""
        if self.output_field_defs:
            return {fd.name: fd.to_field_info() for fd in self.output_field_defs}
        return {}

    def extract_input_from_state(self, state: Any) -> Dict[str, Any]:
        """Extract only the fields this node needs from the overall state."""
        if self.input_schema and hasattr(state, "__dict__"):
            input_dict = {}
            for field_name in self.input_schema.model_fields:
                if hasattr(state, field_name):
                    input_dict[field_name] = getattr(state, field_name)
            return input_dict
        elif self.input_field_defs:
            input_dict = {}
            for field_def in self.input_field_defs:
                if hasattr(state, field_def.name):
                    input_dict[field_def.name] = getattr(state, field_def.name)
            return input_dict
        return {}

    def create_output_for_state(self, result: Any) -> Dict[str, Any]:
        """Create output dict that conforms to this node's output schema."""
        output_dict = {}

        # Map result to output schema fields
        if self.output_schema:
            if isinstance(result, dict):
                for field_name in self.output_schema.model_fields:
                    if field_name in result:
                        output_dict[field_name] = result[field_name]
            else:
                # Try to map single result to first output field
                output_field_names = list(self.output_schema.model_fields.keys())
                if output_field_names:
                    output_dict[output_field_names[0]] = result
        elif isinstance(result, dict):
            output_dict = result

        # Add engine attribution if enabled
        if self.auto_add_engine_attribution and self.engine_name:
            output_dict["engine_name"] = self.engine_name

        return output_dict

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert this node config to a dictionary representation.
        """
        data = self.model_dump()

        # Convert CommandGoto.END to string representation
        if self.command_goto == END:
            data["command_goto"] = "END"

        return data

    @abstractmethod
    def __call__(
        self, state: Dict[str, Any], config: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Base implementation - subclasses should override this.
        """
        raise NotImplementedError(
            f"Node type {self.node_type} does not implement __call__"
        )
