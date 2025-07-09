# src/haive/core/graph/StateGraphEditor.py

import importlib
import logging
import uuid
from collections.abc import Callable
from typing import Any, Literal

from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, StateGraph
from pydantic import BaseModel, Field, field_validator, model_validator

from haive.core.engine.base import Engine
from haive.core.graph.graph_pattern_registry import register_graph_component

logger = logging.getLogger(__name__)

# Updated NodeConfig in src/haive/core/graph/StateGraphEditor.py

import logging

from pydantic import ConfigDict


class NodeConfig(BaseModel):
    """Configuration for a node in the graph."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    # Make engine accept callable functions as well
    engine: Engine | str | Callable | None = None
    command_goto: str | Literal["END"] | None = None
    input_mapping: dict[str, str] | None = None
    output_mapping: dict[str, str] | None = None
    runnable_config: RunnableConfig | None = None
    metadata: dict[str, Any] | None = None

    @field_validator("command_goto")
    def validate_command_goto(cls, v):
        if v == "END":
            return END
        return v


class EdgeConfig(BaseModel):
    """Configuration for an edge in the graph."""

    from_node: str | list[str]
    to_node: str

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    @field_validator("to_node")
    def validate_to_node(cls, v):
        if v == "END":
            return END
        return v


class BranchConfig(BaseModel):
    """Configuration for a conditional branch in the graph."""

    source_node: str
    condition: Callable | str
    destinations: dict[str, str]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    @field_validator("destinations")
    def validate_destinations(cls, destinations):
        validated = {}
        for key, value in destinations.items():
            if value == "END":
                validated[key] = END
            else:
                validated[key] = value
        return validated


class StateGraphEditor(BaseModel):
    """Editor for manipulating StateGraph instances.

    This component provides methods for adding/removing nodes and edges,
    as well as visualizing and modifying the graph structure.
    """

    name: str = Field(default_factory=lambda: f"graph_{uuid.uuid4().hex[:8]}")
    description: str | None = None
    state_schema: type[Any] | None = None
    input_schema: type[Any] | None = None
    output_schema: type[Any] | None = None

    nodes: dict[str, NodeConfig] = Field(default_factory=dict)
    edges: list[EdgeConfig] = Field(default_factory=list)
    branches: list[BranchConfig] = Field(default_factory=list)

    entry_point: str | None = None
    compiled: bool = False

    # Internal state
    state_graph: StateGraph | None = Field(default=None, exclude=True)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    @model_validator(mode="after")
    def validate_schemas(self):
        """Ensure schemas are set correctly."""
        if self.state_schema is None and (
            self.input_schema is not None or self.output_schema is not None
        ):
            if self.input_schema is not None:
                self.state_schema = self.input_schema
            elif self.output_schema is not None:
                self.state_schema = self.output_schema
        return self

    def initialize_graph(self) -> StateGraph:
        """Initialize the StateGraph instance with current configuration."""
        # Create with schemas if available
        if self.state_schema is not None:
            if self.input_schema is not None and self.output_schema is not None:
                self.state_graph = StateGraph(
                    self.state_schema,
                    input=self.input_schema,
                    output=self.output_schema,
                )
            else:
                self.state_graph = StateGraph(self.state_schema)
        else:
            # Create with default dict schema
            self.state_graph = StateGraph(dict)

        logger.info(f"Initialized StateGraph '{self.name}'")
        return self.state_graph

    def get_graph(self) -> StateGraph:
        """Get the current StateGraph instance, initializing if needed."""
        if self.state_graph is None:
            self.initialize_graph()
        return self.state_graph

    def add_node(
        self,
        name: str,
        engine: Engine | str | None = None,
        command_goto: str | Literal["END"] | None = None,
        input_mapping: dict[str, str] | None = None,
        output_mapping: dict[str, str] | None = None,
        runnable_config: RunnableConfig | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> "StateGraphEditor":
        """Add a node to the graph.

        Args:
            name: Name of the node
            engine: Engine configuration or callable function
            command_goto: Optional next node to go to
            input_mapping: Optional mapping from state keys to engine input keys
            output_mapping: Optional mapping from engine output keys to state keys
            runnable_config: Optional runtime configuration specific to this node
            metadata: Optional metadata for the node

        Returns:
            Self for chaining
        """
        # Add to node config
        self.nodes[name] = NodeConfig(
            name=name,
            engine=engine,
            command_goto=command_goto,
            input_mapping=input_mapping,
            output_mapping=output_mapping,
            runnable_config=runnable_config,
            metadata=metadata,
        )

        # Add to StateGraph if initialized
        if self.state_graph is not None:
            from haive.core.graph.NodeFactory import NodeFactory

            # Resolve engine if it's a string
            resolved_engine = engine
            if isinstance(engine, str):
                from haive.core.engine.base import EngineRegistry, EngineType

                registry = EngineRegistry.get_instance()
                for engine_type in EngineType:
                    found_engine = registry.get(engine_type, engine)
                    if found_engine:
                        resolved_engine = found_engine
                        break
                if resolved_engine == engine:  # Not found
                    logger.warning(
                        f"Engine '{engine}' not found in registry, using as-is"
                    )

            # Create node function
            if resolved_engine is not None:
                node_fn = NodeFactory.create_node_function(
                    config=resolved_engine,
                    command_goto=END if command_goto == "END" else command_goto,
                    input_mapping=input_mapping,
                    output_mapping=output_mapping,
                    runnable_config=runnable_config,
                )

                # Add to graph
                self.state_graph.add_node(name, node_fn)
                logger.info(f"Added node '{name}' to StateGraph")
            else:
                logger.warning(
                    f"Cannot add node '{name}' to StateGraph: No engine specified"
                )

        # Set as entry point if first node
        if self.entry_point is None:
            self.entry_point = name
            if self.state_graph is not None:
                self.state_graph.set_entry_point(name)
                logger.info(f"Set entry point to '{name}'")

        return self

    def add_edge(self, from_node: str | list[str], to_node: str) -> "StateGraphEditor":
        """Add an edge between nodes.

        Args:
            from_node: Source node name or list of source node names
            to_node: Target node name or END

        Returns:
            Self for chaining
        """
        # Add to edge config
        self.edges.append(EdgeConfig(from_node=from_node, to_node=to_node))

        # Add to StateGraph if initialized
        if self.state_graph is not None:
            if isinstance(from_node, str):
                self.state_graph.add_edge(
                    from_node, END if to_node == "END" else to_node
                )
                logger.info(f"Added edge from '{from_node}' to '{to_node}'")
            else:
                # Use sequential add_edge for multiple sources
                for node in from_node:
                    self.state_graph.add_edge(
                        node, END if to_node == "END" else to_node
                    )
                logger.info(f"Added edge from {from_node} to '{to_node}'")

        return self

    def add_conditional_edges(
        self, source_node: str, condition: Callable | str, destinations: dict[str, str]
    ) -> "StateGraphEditor":
        """Add conditional edges based on a condition function.

        Args:
            source_node: Source node name
            condition: Condition function or string reference
            destinations: Mapping from condition results to target nodes

        Returns:
            Self for chaining
        """
        # Validate destinations
        validated_destinations = {}
        for key, value in destinations.items():
            if value == "END":
                validated_destinations[key] = END
            else:
                validated_destinations[key] = value

        # Add to branch config
        self.branches.append(
            BranchConfig(
                source_node=source_node,
                condition=condition,
                destinations=validated_destinations,
            )
        )

        # Add to StateGraph if initialized
        if self.state_graph is not None:
            # Resolve condition if it's a string
            resolved_condition = condition
            if isinstance(condition, str):
                # Try to import from module
                try:
                    import importlib

                    module_path, func_name = condition.rsplit(".", 1)
                    module = importlib.import_module(module_path)
                    resolved_condition = getattr(module, func_name)
                except (ValueError, ImportError, AttributeError):
                    logger.warning(
                        f"Could not resolve condition '{condition}', using as-is"
                    )

            # Add to graph
            self.state_graph.add_conditional_edges(
                source_node, resolved_condition, validated_destinations
            )
            logger.info(f"Added conditional edges from '{source_node}'")

        return self

    def set_entry_point(self, node_name: str) -> "StateGraphEditor":
        """Set the entry point for the graph.

        Args:
            node_name: Name of the entry point node

        Returns:
            Self for chaining
        """
        self.entry_point = node_name

        # Update StateGraph if initialized
        if self.state_graph is not None:
            self.state_graph.set_entry_point(node_name)
            logger.info(f"Set entry point to '{node_name}'")

        return self

    def build_graph(self) -> StateGraph:
        """Build and return the StateGraph with all configured components.

        Returns:
            Built StateGraph instance
        """
        # Initialize graph if needed
        if self.state_graph is None:
            self.initialize_graph()

            graph = self.state_graph

        # Add nodes
        for name, node_config in self.nodes.items():
            if name not in graph.nodes:
                from haive.core.graph.NodeFactory import NodeFactory

                # Resolve engine if it's a string
                resolved_engine = node_config.engine
                if isinstance(resolved_engine, str):
                    from haive.core.engine.base import EngineRegistry, EngineType

                    registry = EngineRegistry.get_instance()
                    for engine_type in EngineType:
                        found_engine = registry.get(engine_type, resolved_engine)
                        if found_engine:
                            resolved_engine = found_engine
                            break

                # Create node function
                if resolved_engine is not None:
                    node_fn = NodeFactory.create_node_function(
                        config=resolved_engine,
                        command_goto=node_config.command_goto,
                        input_mapping=node_config.input_mapping,
                        output_mapping=node_config.output_mapping,
                        runnable_config=node_config.runnable_config,
                    )

                    # Add to graph
                    graph.add_node(name, node_fn)

        # Add edges
        for edge_config in self.edges:
            if isinstance(edge_config.from_node, str):
                graph.add_edge(edge_config.from_node, edge_config.to_node)
            else:
                for node in edge_config.from_node:
                    graph.add_edge(node, edge_config.to_node)

        # Add conditional edges
        for branch_config in self.branches:
            # Resolve condition if it's a string
            resolved_condition = branch_config.condition
            if isinstance(resolved_condition, str):
                # Try to import from module
                try:
                    import importlib

                    module_path, func_name = resolved_condition.rsplit(".", 1)
                    module = importlib.import_module(module_path)
                    resolved_condition = getattr(module, func_name)
                except (ValueError, ImportError, AttributeError):
                    logger.warning(
                        f"Could not resolve condition '{resolved_condition}', using as-is"
                    )
                    continue

            # Add to graph
            graph.add_conditional_edges(
                branch_config.source_node,
                resolved_condition,
                branch_config.destinations,
            )

        # Set entry point
        if self.entry_point:
            graph.set_entry_point(self.entry_point)

        return graph

    def compile(self, **kwargs) -> Any:
        """Compile the StateGraph.

        Args:
            **kwargs: Additional keyword arguments to pass to StateGraph.compile()

        Returns:
            Compiled graph instance
        """
        graph = self.build_graph()
        compiled_graph = graph.compile(**kwargs)
        self.compiled = True
        return compiled_graph

    def to_dict(self) -> dict[str, Any]:
        """Convert the editor configuration to a dictionary for serialization.

        Returns:
            Dictionary representation
        """
        result = {
            "name": self.name,
            "description": self.description,
            "state_schema": self.state_schema.__name__ if self.state_schema else None,
            "input_schema": self.input_schema.__name__ if self.input_schema else None,
            "output_schema": (
                self.output_schema.__name__ if self.output_schema else None
            ),
            "entry_point": self.entry_point,
            "compiled": self.compiled,
            "nodes": {},
            "edges": [],
            "branches": [],
        }

        # Convert nodes to serializable format
        for name, node in self.nodes.items():
            node_dict = node.model_dump()

            # Handle engine field (convert Engine to name if needed)
            if isinstance(node.engine, Engine):
                node_dict["engine"] = node.engine.name

            # Handle command_goto
            if node.command_goto == END:
                node_dict["command_goto"] = "END"

            result["nodes"][name] = node_dict

        # Convert edges to serializable format
        for edge in self.edges:
            edge_dict = edge.model_dump()

            # Handle END node
            if edge.to_node == END:
                edge_dict["to_node"] = "END"

            result["edges"].append(edge_dict)

        # Convert branches to serializable format
        for branch in self.branches:
            branch_dict = branch.model_dump()

            # Handle condition (convert callable to string if needed)
            if callable(branch.condition):
                module = branch.condition.__module__
                name = branch.condition.__name__
                branch_dict["condition"] = f"{module}.{name}"

            # Handle destinations with END
            for key, value in branch.destinations.items():
                if value == END:
                    branch_dict["destinations"][key] = "END"

            result["branches"].append(branch_dict)

        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "StateGraphEditor":
        """Create a StateGraphEditor from a dictionary.

        Args:
            data: Dictionary representation

        Returns:
            New StateGraphEditor instance
        """
        # Import schemas if provided
        schemas = {}
        for schema_key in ["state_schema", "input_schema", "output_schema"]:
            if data.get(schema_key):
                schema_name = data[schema_key]
                if isinstance(schema_name, str):
                    try:
                        # Try to find the schema class
                        module_path, class_name = schema_name.rsplit(".", 1)
                        module = importlib.import_module(module_path)
                        schemas[schema_key] = getattr(module, class_name)
                    except (ValueError, ImportError, AttributeError):
                        logger.warning(f"Could not import schema '{schema_name}'")

        # Create editor
        editor = cls(
            name=data.get("name", f"graph_{uuid.uuid4().hex[:8]}"),
            description=data.get("description"),
            state_schema=schemas.get("state_schema"),
            input_schema=schemas.get("input_schema"),
            output_schema=schemas.get("output_schema"),
            entry_point=data.get("entry_point"),
        )

        # Add nodes
        for name, node_dict in data.get("nodes", {}).items():
            # Handle command_goto string to END conversion
            if node_dict.get("command_goto") == "END":
                node_dict["command_goto"] = END

            # Create node config
            node_config = NodeConfig(**node_dict)
            editor.nodes[name] = node_config

        # Add edges
        for edge_dict in data.get("edges", []):
            # Handle to_node string to END conversion
            if edge_dict.get("to_node") == "END":
                edge_dict["to_node"] = END

            # Create edge config
            edge_config = EdgeConfig(**edge_dict)
            editor.edges.append(edge_config)

        # Add branches
        for branch_dict in data.get("branches", []):
            # Convert condition string to callable if possible
            if isinstance(branch_dict.get("condition"), str):
                condition_str = branch_dict["condition"]
                try:
                    module_path, func_name = condition_str.rsplit(".", 1)
                    module = importlib.import_module(module_path)
                    branch_dict["condition"] = getattr(module, func_name)
                except (ValueError, ImportError, AttributeError):
                    logger.warning(f"Could not resolve condition '{condition_str}'")

            # Handle destinations with END strings
            destinations = branch_dict.get("destinations", {})
            for key, value in destinations.items():
                if value == "END":
                    destinations[key] = END

            # Create branch config
            branch_config = BranchConfig(**branch_dict)
            editor.branches.append(branch_config)

        return editor

    def visualize(self, filename: str | None = None) -> None:
        """Visualize the graph structure.

        Args:
            filename: Optional filename to save the visualization
        """
        # Build graph if needed
        graph = self.build_graph()

        # Generate visualization
        try:
            from haive.core.utils.visualize_graph_utils import render_and_display_graph

            render_and_display_graph(graph, output_name=filename)
            logger.info(f"Graph visualization saved to {filename}")
        except ImportError:
            logger.warning("Cannot visualize graph: visualization utils not available")


# Register with registry
@register_graph_component("graph_editor", "StateGraphEditor", ["editor", "graph"])
class RegisteredStateGraphEditor(StateGraphEditor):
    """Registered version of StateGraphEditor."""
