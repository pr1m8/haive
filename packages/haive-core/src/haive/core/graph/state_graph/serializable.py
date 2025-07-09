"""
Serialization support for BaseGraph.

This module provides serialization and deserialization utilities for BaseGraph,
enabling graphs to be stored, loaded, and exchanged with minimal information loss.
"""

import importlib
import json
import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, ConfigDict, Field

from haive.core.graph.common.references import CallableReference
from haive.core.utils.serialization import ensure_json_serializable

# Get logger
logger = logging.getLogger(__name__)


# Type references
class TypeReference(BaseModel):
    """Reference to a type that can be serialized."""

    module_path: Optional[str] = None
    name: str
    is_generic: bool = False
    generic_params: Optional[List["TypeReference"]] = None

    model_config = ConfigDict(extra="allow")

    @classmethod
    def from_type(cls, type_obj):
        if type_obj is None:
            return None

        ref = cls(
            name=getattr(type_obj, "__name__", str(type_obj)),
            module_path=getattr(type_obj, "__module__", None),
        )

        # TODO: Add support for complex generic types
        return ref

    def resolve(self):
        """Resolve the reference back to a type."""
        if not self.module_path or not self.name:
            return None

        try:
            module = importlib.import_module(self.module_path)
            return getattr(module, self.name)
        except (ImportError, AttributeError) as e:
            logger.warning(f"Error resolving type: {e}")
            return None


# Node serialization
class SerializableNode(BaseModel):
    """Serializable representation of a Node."""

    id: str
    name: str
    node_type: str

    # Configuration
    input_mapping: Optional[Dict[str, str]] = None
    output_mapping: Optional[Dict[str, str]] = None
    command_goto: Optional[Union[str, List[str]]] = None
    retry_policy: Optional[Dict[str, Any]] = None

    # Metadata
    description: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: Optional[str] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)


# Branch serialization
class SerializableBranch(BaseModel):
    """Serializable representation of a Branch."""

    id: str
    name: str
    source_node: str
    mode: Optional[str] = None

    # Core branch fields
    key: Optional[str] = None
    value: Optional[Any] = None
    comparison: Optional[str] = None
    default: Optional[str] = None
    allow_none: Optional[bool] = None
    message_key: Optional[str] = None

    # Function references
    function_ref: Optional[CallableReference] = None
    condition_ref: Optional[CallableReference] = None

    # Routing information
    destinations: Dict[str, str] = Field(default_factory=dict)

    # Advanced branch features
    send_mappings: Optional[List[Dict[str, Any]]] = None
    send_generators: Optional[List[Dict[str, Any]]] = None
    dynamic_mapping: Optional[Dict[str, Any]] = None

    # Chain branches - these need special handling
    chain_branches_ids: Optional[List[str]] = None
    true_branch_id: Optional[str] = None
    false_branch_id: Optional[str] = None

    # Metadata
    description: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(arbitrary_types_allowed=True)


class SerializableGraph(BaseModel):
    """Serializable representation of the BaseGraph."""

    # Basic identification
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None

    # Graph structure
    nodes: Dict[str, SerializableNode] = Field(default_factory=dict)

    # Edges stored as lists for easier serialization
    direct_edges: List[Tuple[str, str]] = Field(default_factory=list)

    # Branches
    branches: Dict[str, SerializableBranch] = Field(default_factory=dict)

    # Schema reference
    state_schema: Optional[TypeReference] = None

    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: str
    updated_at: str

    # Configuration
    config: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def from_graph(cls, graph):
        """Create a serializable representation from a BaseGraph."""
        from haive.core.graph.state_graph.base_graph import BaseGraph

        if not isinstance(graph, BaseGraph):
            raise TypeError("Expected a BaseGraph instance")

        # Initialize basic fields
        serializable = cls(
            id=graph.id,
            name=graph.name,
            description=graph.description,
            metadata=graph.metadata.copy(),
            created_at=graph.created_at.isoformat(),
            updated_at=graph.updated_at.isoformat(),
        )

        # Convert schema if present
        if graph.state_schema:
            serializable.state_schema = TypeReference.from_type(graph.state_schema)

        # Convert nodes
        for name, node in graph.nodes.items():
            serializable.nodes[name] = SerializableNode(
                id=node.id,
                name=node.name,
                node_type=node.node_type.value,
                input_mapping=node.input_mapping,
                output_mapping=node.output_mapping,
                command_goto=node.command_goto,
                retry_policy=node.retry_policy._asdict() if node.retry_policy else None,
                description=node.description,
                metadata=node.metadata.copy(),
                created_at=node.created_at.isoformat() if node.created_at else None,
            )

        # Convert direct edges
        for edge in graph.edges:
            serializable.direct_edges.append(edge)

        # Convert branches
        for branch_id, branch in graph.branches.items():
            # Basic properties all branches have
            branch_data = {
                "id": branch.id,
                "name": branch.name,
                "source_node": branch.source_node,
                "default": getattr(branch, "default", "END"),
                "description": getattr(branch, "description", None),
                "metadata": getattr(branch, "metadata", {}).copy(),
            }

            # Add mode
            if hasattr(branch, "mode"):
                mode = branch.mode
                branch_data["mode"] = (
                    mode.value if hasattr(mode, "value") else str(mode)
                )

            # Add standard fields that most branches have
            if hasattr(branch, "key"):
                branch_data["key"] = branch.key
            if hasattr(branch, "value"):
                branch_data["value"] = branch.value
            if hasattr(branch, "comparison"):
                comp = branch.comparison
                branch_data["comparison"] = (
                    comp.value if hasattr(comp, "value") else str(comp)
                )
            if hasattr(branch, "allow_none"):
                branch_data["allow_none"] = branch.allow_none
            if hasattr(branch, "message_key"):
                branch_data["message_key"] = branch.message_key

            # Handle destinations/routes
            if hasattr(branch, "destinations"):
                # Convert any non-string keys to strings
                destinations = {}
                for k, v in branch.destinations.items():
                    destinations[str(k)] = v
                branch_data["destinations"] = destinations

            # Handle function references
            if hasattr(branch, "function_ref"):
                branch_data["function_ref"] = branch.function_ref
            elif hasattr(branch, "function") and callable(branch.function):
                branch_data["function_ref"] = CallableReference.from_callable(
                    branch.function
                )

            if hasattr(branch, "condition_ref"):
                branch_data["condition_ref"] = branch.condition_ref
            elif hasattr(branch, "condition") and callable(branch.condition):
                branch_data["condition_ref"] = CallableReference.from_callable(
                    branch.condition
                )

            # Handle advanced branch features
            if hasattr(branch, "send_mappings") and branch.send_mappings:
                # Simplified serialization of send mappings
                branch_data["send_mappings"] = [
                    {
                        "condition": m.condition if hasattr(m, "condition") else None,
                        "node": m.node if hasattr(m, "node") else None,
                        "fields": m.fields if hasattr(m, "fields") else {},
                    }
                    for m in branch.send_mappings
                ]

            if hasattr(branch, "send_generators") and branch.send_generators:
                # Simplified serialization of send generators
                branch_data["send_generators"] = [
                    {
                        "collection_field": (
                            g.collection_field
                            if hasattr(g, "collection_field")
                            else None
                        ),
                        "target_node": (
                            g.target_node if hasattr(g, "target_node") else None
                        ),
                        "item_field": (
                            g.item_field if hasattr(g, "item_field") else None
                        ),
                    }
                    for g in branch.send_generators
                ]

            # Handle dynamic mapping - this part is fixed to correctly map key to field
            if hasattr(branch, "dynamic_mapping") and branch.dynamic_mapping:
                # Serialize dynamic mapping - The important fix: use key for field
                mapping = branch.dynamic_mapping
                branch_data["dynamic_mapping"] = {
                    "field": mapping.key,  # Store the key attribute under 'field' key
                    "mappings": (
                        mapping.mappings if hasattr(mapping, "mappings") else {}
                    ),
                    "default_node": (
                        mapping.default_node
                        if hasattr(mapping, "default_node")
                        else "END"
                    ),
                }

            # Handle chain branches
            if hasattr(branch, "chain_branches") and branch.chain_branches:
                # Store IDs instead of actual objects
                branch_data["chain_branches_ids"] = []
                for chain_branch in branch.chain_branches:
                    # Use ID if it exists in our branches
                    for bid, b in graph.branches.items():
                        if b is chain_branch:
                            branch_data["chain_branches_ids"].append(bid)
                            break

            # Handle true/false branches
            if hasattr(branch, "true_branch"):
                true_branch = branch.true_branch
                if isinstance(true_branch, str):
                    branch_data["true_branch_id"] = true_branch  # Direct node name
                elif hasattr(true_branch, "id"):
                    branch_data["true_branch_id"] = true_branch.id

            if hasattr(branch, "false_branch"):
                false_branch = branch.false_branch
                if isinstance(false_branch, str):
                    branch_data["false_branch_id"] = false_branch  # Direct node name
                elif hasattr(false_branch, "id"):
                    branch_data["false_branch_id"] = false_branch.id

            # Create serializable branch
            serializable.branches[branch_id] = SerializableBranch(**branch_data)

        return serializable

    def to_graph(self):
        """Convert serializable representation back to a BaseGraph."""
        from haive.core.graph.branches import BranchMode, ComparisonType
        from haive.core.graph.state_graph.base_graph import BaseGraph, Node, NodeType

        # Create basic graph
        graph = BaseGraph(
            id=self.id,
            name=self.name,
            description=self.description,
            metadata=self.metadata.copy(),
        )

        # Set timestamps
        try:
            graph.created_at = datetime.fromisoformat(self.created_at)
            graph.updated_at = datetime.fromisoformat(self.updated_at)
        except (ValueError, TypeError):
            # Use current time if iso format parsing fails
            now = datetime.now()
            graph.created_at = now
            graph.updated_at = now

        # Resolve schema if present
        if self.state_schema:
            graph.state_schema = self.state_schema.resolve()

        # Add nodes
        for name, node_data in self.nodes.items():
            try:
                # Convert string node_type to enum
                node_type = NodeType(node_data.node_type)

                # Create the node
                node = Node(
                    id=node_data.id,
                    name=node_data.name,
                    node_type=node_type,
                    input_mapping=node_data.input_mapping,
                    output_mapping=node_data.output_mapping,
                    command_goto=node_data.command_goto,
                    retry_policy=node_data.retry_policy,  # TODO: Convert dict to RetryPolicy
                    description=node_data.description,
                    metadata=node_data.metadata.copy(),
                )

                # Parse created_at
                if node_data.created_at:
                    try:
                        node.created_at = datetime.fromisoformat(node_data.created_at)
                    except (ValueError, TypeError):
                        node.created_at = datetime.now()

                # Add to graph
                graph.nodes[name] = node

            except Exception as e:
                logger.error(f"Error reconstructing node {name}: {e}")

        # Add direct edges
        for source, target in self.direct_edges:
            graph.edges.append((source, target))

        # First pass to create all branches (without references to other branches)
        temp_branches = {}
        for branch_id, branch_data in self.branches.items():
            try:
                # Resolve function reference if available
                function = None
                if branch_data.function_ref:
                    function = branch_data.function_ref.resolve()

                # Resolve condition reference if available
                if branch_data.condition_ref:
                    branch_data.condition_ref.resolve()

                # Convert comparison enum
                comparison = branch_data.comparison
                if comparison and not isinstance(comparison, ComparisonType):
                    try:
                        comparison = ComparisonType(comparison)
                    except (ValueError, TypeError):
                        pass  # Keep as string if not an enum value

                # Convert mode enum
                mode = branch_data.mode
                if mode and not isinstance(mode, BranchMode):
                    try:
                        mode = BranchMode(mode)
                    except (ValueError, TypeError):
                        pass  # Keep as string if not an enum value

                # Create dynamic mapping if provided - Fixed to correctly map field to key
                dynamic_mapping = None
                if branch_data.dynamic_mapping:
                    # The important fix: use field for key
                    dynamic_mapping = DynamicMapping(
                        key=branch_data.dynamic_mapping.get(
                            "field"
                        ),  # Map 'field' to 'key'
                        mappings=branch_data.dynamic_mapping.get("mappings", {}),
                        default_node=branch_data.dynamic_mapping.get(
                            "default_node", "END"
                        ),
                    )

                # Create send mappings if provided
                send_mappings = []
                if branch_data.send_mappings:
                    for mapping_data in branch_data.send_mappings:
                        mapping = SendMapping(
                            condition=mapping_data.get("condition"),
                            node=mapping_data.get("node"),
                            fields=mapping_data.get("fields", {}),
                        )
                        send_mappings.append(mapping)

                # Create send generators if provided
                send_generators = []
                if branch_data.send_generators:
                    for generator_data in branch_data.send_generators:
                        generator = SendGenerator(
                            collection_field=generator_data.get("collection_field"),
                            target_node=generator_data.get("target_node"),
                            item_field=generator_data.get("item_field"),
                        )
                        send_generators.append(generator)

                # Convert string keys in destinations to proper types (bool/int)
                destinations = {}
                if branch_data.destinations:
                    for k, v in branch_data.destinations.items():
                        # Try to convert string keys back to original types
                        if k.lower() == "true":
                            destinations[True] = v
                        elif k.lower() == "false":
                            destinations[False] = v
                        else:
                            try:
                                # Try as number
                                num = int(k)
                                destinations[num] = v
                            except ValueError:
                                # Keep as string
                                destinations[k] = v

                # Create branch with available data
                branch = Branch(
                    id=branch_data.id,
                    name=branch_data.name,
                    source_node=branch_data.source_node,
                    key=branch_data.key,
                    value=branch_data.value,
                    comparison=comparison,
                    function=function,
                    function_ref=branch_data.function_ref,
                    destinations=destinations,
                    default=branch_data.default or "END",
                    allow_none=branch_data.allow_none or False,
                    message_key=branch_data.message_key or "messages",
                    mode=mode or BranchMode.DIRECT,
                    # Dynamic mapping
                    dynamic_mapping=dynamic_mapping,
                    # Send mapping
                    send_mappings=send_mappings,
                    send_generators=send_generators,
                    # For condition branches
                    condition_ref=branch_data.condition_ref,
                )

                # Store for second pass linking
                temp_branches[branch_id] = branch

                # Add to graph
                graph.branches[branch_id] = branch

            except Exception as e:
                logger.error(f"Error reconstructing branch {branch_id}: {e}")

        # Second pass to link branches to each other
        for branch_id, branch_data in self.branches.items():
            if branch_id not in temp_branches:
                continue

            branch = temp_branches[branch_id]

            # Link chain branches
            if branch_data.chain_branches_ids:
                branch.chain_branches = []
                for chain_id in branch_data.chain_branches_ids:
                    if chain_id in temp_branches:
                        branch.chain_branches.append(temp_branches[chain_id])

            # Link true/false branches
            if branch_data.true_branch_id:
                if branch_data.true_branch_id in temp_branches:
                    branch.true_branch = temp_branches[branch_data.true_branch_id]
                else:
                    # Might be a node name
                    branch.true_branch = branch_data.true_branch_id

            if branch_data.false_branch_id:
                if branch_data.false_branch_id in temp_branches:
                    branch.false_branch = temp_branches[branch_data.false_branch_id]
                else:
                    # Might be a node name
                    branch.false_branch = branch_data.false_branch_id

        return graph

    def to_dict(self):
        """Convert to a dictionary for serialization."""
        return self.model_dump()

    @classmethod
    def from_dict(cls, data):
        """Create from a dictionary."""
        return cls.model_validate(data)

    # @classmethod
    def to_json(cls, **kwargs):
        """Convert to JSON string."""
        # First convert to a dict
        data = cls.to_dict()

        # Ensure all data is JSON serializable (handle functions, etc.)
        serializable_data = ensure_json_serializable(data)

        # Convert to JSON string
        return json.dumps(serializable_data, **kwargs)

    @classmethod
    def from_json(cls, json_str):
        """Create from JSON string."""
        return cls.model_validate_json(json_str)
