import logging
import uuid
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Type, Union

from langchain_core.tools import BaseTool
from langgraph.graph import END
from langgraph.types import RetryPolicy
from pydantic import BaseModel, Field, model_validator

from haive.core.engine.base import Engine
from haive.core.graph.node.types import CommandGoto, NodeType

logger = logging.getLogger(__name__)


class NodeConfig(BaseModel):
    """
    Configuration for a node in a graph.

    A NodeConfig defines all aspects of a node's behavior, including:
    - Core identification (id, name)
    - Engine/callable to execute
    - State schema integration
    - Input/output field mappings
    - Control flow behavior
    - Node type-specific options
    """

    # Core identification
    id: str = Field(
        default_factory=lambda: f"node_{uuid.uuid4().hex[:8]}",
        description="Unique identifier for this node",
    )
    name: str = Field(description="Name of the node in the graph")
    node_type: Optional[NodeType] = Field(
        default=None,  # Will be determined based on engine/options
        description="Type of node (determined automatically if not specified)",
    )
    schemas: Sequence[Union[BaseTool, Type[BaseModel], Callable]] = Field(
        default_factory=list, description="The schemas to use for the node"
    )
    # Engine/Callable (one of these must be set)
    engine: Optional[Engine] = Field(
        default=None, description="Engine instance to use for this node"
    )
    engine_name: Optional[str] = Field(
        default=None, description="Name of engine to look up in registry"
    )
    callable_func: Optional[Callable] = Field(
        default=None,
        description="Callable function to use for this node",
        exclude=True,  # Exclude only non-serializable callables
    )
    callable_ref: Optional[str] = Field(
        default=None, description="Reference to callable function (module.function)"
    )

    # State schema - CRUCIAL ELEMENT
    state_schema: Optional[Type[BaseModel]] = Field(
        default=None, description="State schema class for this node"
    )

    # Schema integration
    input_schema: Optional[Type[BaseModel]] = Field(
        default=None, description="Input schema for this node"
    )
    output_schema: Optional[Type[BaseModel]] = Field(
        default=None, description="Output schema for this node"
    )

    # Input/Output mapping
    input_fields: Optional[Union[List[str], Dict[str, str]]] = Field(
        default=None,
        description="List of input fields or mapping from state keys to node input keys",
    )
    output_fields: Optional[Union[List[str], Dict[str, str]]] = Field(
        default=None,
        description="List of output fields or mapping from node output keys to state keys",
    )

    # Control flow
    command_goto: Optional[CommandGoto] = Field(
        default=None, description="Next node to go to after this node (or END)"
    )

    # Execution options
    retry_policy: Optional[RetryPolicy] = Field(
        default=None, description="Retry policy for node execution"
    )

    # Node type specific options
    # Tool node options
    tools: Optional[List[Any]] = Field(default=None, description="Tools for tool nodes")
    messages_field: Optional[str] = Field(
        default="messages",
        description="Field containing messages for tool/validation nodes",
    )
    handle_tool_errors: Union[bool, str, Callable] = Field(
        default=True, description="How to handle tool errors"
    )

    # Validation node options
    validation_schemas: Optional[List[Union[Type[BaseModel], Callable]]] = Field(
        default=None, description="Validation schemas for validation nodes"
    )

    # Branch node options
    condition: Optional[Callable] = Field(
        default=None, description="Condition function for branch nodes", exclude=True
    )
    condition_ref: Optional[str] = Field(
        default=None, description="Reference to condition function (module.function)"
    )
    routes: Optional[Dict[Any, str]] = Field(
        default=None, description="Routes mapping condition results to node names"
    )

    # Send node options
    send_targets: Optional[List[str]] = Field(
        default=None, description="Target nodes for send operations"
    )
    send_field: Optional[str] = Field(
        default=None, description="Field containing items to distribute to targets"
    )

    # Runtime configuration
    config_overrides: Dict[str, Any] = Field(
        default_factory=dict, description="Engine configuration overrides for this node"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata for this node"
    )

    model_config = {"arbitrary_types_allowed": True, "validate_assignment": True}

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert this node config to a dictionary representation.

        Returns:
            Dictionary representation of this node config
        """
        # Use model_dump for serialization
        data = self.model_dump(exclude={"engine", "callable_func", "condition"})

        # Handle engine reference
        if self.engine:
            if hasattr(self.engine, "to_dict"):
                data["engine"] = self.engine.to_dict()
            elif hasattr(self.engine, "model_dump"):
                data["engine"] = self.engine.model_dump()
            else:
                data["engine"] = {
                    "name": getattr(self.engine, "name", "unknown"),
                    "type": getattr(self.engine, "engine_type", "unknown"),
                }

        # Handle specific fields that need serialization
        # Add state_schema class name if present
        if self.state_schema:
            data["state_schema"] = (
                f"{self.state_schema.__module__}.{self.state_schema.__name__}"
            )

        # Add input_schema class name if present
        if self.input_schema:
            data["input_schema"] = (
                f"{self.input_schema.__module__}.{self.input_schema.__name__}"
            )

        # Add output_schema class name if present
        if self.output_schema:
            data["output_schema"] = (
                f"{self.output_schema.__module__}.{self.output_schema.__name__}"
            )

        # Convert CommandGoto.END to string representation
        if self.command_goto == END:
            data["command_goto"] = "END"

        return data

    @model_validator(mode="after")
    def validate_and_determine_node_type(self) -> "NodeConfig":
        """
        Validate the configuration and determine the node type automatically if not specified.
        """
        # Convert END string to Literal
        if self.command_goto == "END":
            self.command_goto = END

        # Ensure at least one execution target is set
        if (
            self.engine is None
            and self.engine_name is None
            and self.callable_func is None
            and self.tools is None
            and self.schemas is None
            # and self.node_type is not NodeType.VALIDATION
        ):
            raise ValueError(
                "At least one of engine, engine_name, tools,schemas or callable_func must be set"
            )

        # Convert input_fields and output_fields to dictionaries if they're lists
        if isinstance(self.input_fields, list):
            self.input_fields = {field: field for field in self.input_fields}

        if isinstance(self.output_fields, list):
            self.output_fields = {field: field for field in self.output_fields}

        # Determine node type if not explicitly set
        if self.node_type is None:
            # Check node type specific options first
            if self.tools is not None:
                self.node_type = NodeType.TOOL
            elif self.validation_schemas is not None:
                self.node_type = NodeType.VALIDATION
            elif self.condition is not None and self.routes is not None:
                self.node_type = NodeType.BRANCH
            elif self.send_targets is not None:
                self.node_type = NodeType.SEND
            else:
                # Determine from engine/callable
                if self.engine is not None:
                    self.node_type = NodeType.ENGINE
                elif self.engine_name is not None:
                    self.node_type = NodeType.ENGINE
                elif self.callable_func is not None:
                    self.node_type = NodeType.CALLABLE
                else:
                    self.node_type = NodeType.CUSTOM

        # Auto-generate schema from engine if available
        if self.engine and not self.state_schema:
            # Try to get schema from SchemaComposer
            try:
                from haive.core.schema.schema_composer import SchemaComposer

                schema = SchemaComposer.from_components([self.engine])
                self.state_schema = schema.build()

                # Also derive input/output schemas if not set
                if not self.input_schema:
                    self.input_schema = schema.create_input_schema()
                if not self.output_schema:
                    self.output_schema = schema.create_output_schema()
            except Exception as e:
                logger.warning(f"Could not auto-generate schema from engine: {e}")

        # Extract input/output mappings from engine I/O schema if they exist
        if self.engine and not self.input_fields and not self.output_fields:
            try:
                engine_name = getattr(self.engine, "name", "default")

                # Check if state schema has engine I/O mappings
                if hasattr(self.state_schema, "__engine_io_mappings__"):
                    io_mappings = getattr(
                        self.state_schema, "__engine_io_mappings__", {}
                    )
                    if engine_name in io_mappings:
                        mapping = io_mappings[engine_name]

                        # Extract input fields
                        if "inputs" in mapping and not self.input_fields:
                            input_fields = mapping["inputs"]
                            # Create identity mapping
                            self.input_fields = {field: field for field in input_fields}

                        # Extract output fields
                        if "outputs" in mapping and not self.output_fields:
                            output_fields = mapping["outputs"]
                            # Create identity mapping
                            self.output_fields = {
                                field: field for field in output_fields
                            }
            except Exception as e:
                logger.warning(f"Could not extract I/O mappings from schema: {e}")

        return self

    def get_engine(self) -> Tuple[Optional[Engine], Optional[str]]:
        """
        Get the engine for this node, resolving from registry if needed.

        Returns:
            Tuple of (engine_instance, engine_id)
        """
        # If no engine or engine_name, return callable or None
        if self.engine is None and self.engine_name is None:
            return self.callable_func, None

        # Return direct engine if already set
        if self.engine is not None:
            engine_id = getattr(self.engine, "id", None)
            return self.engine, engine_id

        # Lookup engine by name in registry
        try:
            from haive.core.engine.base import EngineRegistry

            registry = EngineRegistry.get_instance()

            engine = registry.find(self.engine_name)
            if engine:
                engine_id = getattr(engine, "id", None)
                return engine, engine_id
        except ImportError:
            logger.warning(
                f"Could not import EngineRegistry to resolve engine: {self.engine_name}"
            )

        # Not found - return None
        return None, None

    def get_input_mapping(self) -> Dict[str, str]:
        """
        Get the input mapping for this node.

        Returns:
            Dictionary mapping state keys to node input keys
        """
        if self.input_fields:
            return dict(self.input_fields)
        return {}

    def get_output_mapping(self) -> Dict[str, str]:
        """
        Get the output mapping for this node.

        Returns:
            Dictionary mapping node output keys to state keys
        """
        if self.output_fields:
            return dict(self.output_fields)
        return {}
