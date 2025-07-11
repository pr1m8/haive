"""Serialization mixin for Agent classes.

This mixin provides proper serialization support for Agent instances in LangGraph,
handling both pickle and msgpack serialization formats.
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class SerializationMixin:
    """Mixin for serializing and deserializing Agent instances.

    This mixin provides methods for handling serialization with both pickle and
    msgpack, focusing on addressing the specific needs of agents within LangGraph.

    LangGraph uses msgpack under the hood for serialization during graph execution.
    This mixin ensures agents can be properly serialized without errors.
    """

    def __getstate__(self) -> dict[str, Any]:
        """Prepare instance for pickling.

        Excludes non-serializable components like graph, compiled_graph,
        checkpointer, store, etc. and handles complex type objects.

        Returns:
            Dict containing serializable state.
        """
        # Start with the regular state dictionary
        state = self.__dict__.copy()

        # Remove non-serializable components
        for exclude_key in [
            "graph",
            "_compiled_graph",
            "checkpointer",
            "store",
            "_app",
            "config",
            "output_parser",
        ]:
            if exclude_key in state:
                state.pop(exclude_key)

        # Handle dynamically created schemas (which are picklable but cause issues with msgpack)
        for schema_key in ["input_schema", "output_schema", "config_schema"]:
            if schema_key in state and state[schema_key] is not None:
                # Store schema name and module for reconstruction
                schema = state[schema_key]
                state[f"_{schema_key}_name"] = getattr(schema, "__name__", str(schema))
                state[f"_{schema_key}_module"] = getattr(schema, "__module__", None)
                # Remove the actual schema
                state.pop(schema_key)

        # Handle structured_output_model (which is a Type object)
        if (
            "structured_output_model" in state
            and state["structured_output_model"] is not None
        ):
            model = state["structured_output_model"]
            state["_structured_output_model_name"] = getattr(
                model, "__name__", str(model)
            )
            state["_structured_output_model_module"] = getattr(
                model, "__module__", None
            )
            state.pop("structured_output_model")

        return state

    def __setstate__(self, state: dict[str, Any]) -> None:
        """Reconstruct instance after unpickling.

        Handles reconstruction of the state dictionary, rebuilding special fields
        like schemas and structured output models.

        Args:
            state: Dictionary containing serialized state.
        """
        # Create minimal instance to ensure we don't crash
        self.__dict__.update(state)

        # Rebuild graph when used (will be done by agent)
        self._graph_built = False

        # Schema restoration is typically handled by the invoke method
        # which will call setup_schemas() when needed

    def __reduce__(self) -> tuple:
        """Make agent picklable for both pickle and msgpack.

        This special method enables proper serialization with both pickle and msgpack.
        We return a tuple of (constructor, args, state) that can be used to reconstruct
        this object.

        Returns:
            Tuple of (constructor, empty args, state) for reconstruction.
        """
        # Get state dictionary using getstate
        state = self.__getstate__()

        # Return the class and empty args along with state
        return (self.__class__, (), state)

    def _serialize_for_msgpack(self) -> dict[str, Any]:
        """Create a msgpack-serializable representation of this object.

        This method is used for explicitly controlling what's serialized when
        msgpack is directly used (e.g., in checkpointing).

        Returns:
            Dict containing msgpack-serializable data.
        """
        # Get state using getstate
        state = self.__getstate__()

        # Add agent type info
        state["__agent_type__"] = self.__class__.__name__
        state["__agent_module__"] = self.__class__.__module__

        return state

    @classmethod
    def _deserialize_from_msgpack(cls, data: dict[str, Any]) -> "SerializationMixin":
        """Reconstruct an agent from msgpack-serialized data.

        Args:
            data: Serialized data dictionary from _serialize_for_msgpack.

        Returns:
            Reconstructed agent instance.
        """
        # Create a new instance of this class
        instance = cls.__new__(cls)

        # Initialize instance with empty state to avoid validation errors
        # that might occur in __init__
        instance.__dict__.update(
            {"_setup_complete": False, "_graph_built": False, "_is_compiled": False}
        )

        # Remove type information fields
        data.pop("__agent_type__", None)
        data.pop("__agent_module__", None)

        # Update instance with the data
        instance.__setstate__(data)

        return instance
