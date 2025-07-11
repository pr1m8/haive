import importlib
import inspect
from typing import Any, Literal, Optional

from pydantic import Field, field_validator, model_validator

from haive.core.graph.state_graph.base import SerializableModel


class FunctionReference(SerializableModel):
    """Reference to a callable object that can be serialized."""

    module_path: str | None = Field(
        default=None, description="Module containing the callable"
    )
    function_name: str | None = Field(default=None, description="Name of the callable")
    callable_type: Literal["function", "method", "class", "lambda", "unknown"] = Field(
        default="function", description="Type of callable"
    )
    source_code: str | None = Field(
        default=None, description="Source code if available"
    )

    __abstract__ = True  # Not registered directly

    @model_validator(mode="after")
    def ensure_valid_reference(self) -> "FunctionReference":
        """Ensure the reference is valid."""
        if not self.module_path and not self.function_name and not self.source_code:
            raise ValueError(
                "Function reference must have either module_path and function_name, or source_code"
            )
        return self

    @field_validator("callable_type")
    @classmethod
    def validate_callable_type(cls, v: str) -> str:
        """Validate callable type."""
        valid_types = ["function", "method", "class", "lambda", "unknown"]
        if v not in valid_types:
            raise ValueError(
                f"Invalid callable type: {v}. Must be one of {valid_types}"
            )
        return v

    @classmethod
    def from_callable(
        cls, callable_obj: Any, name: str | None = None
    ) -> Optional["FunctionReference"]:
        """Create a FunctionReference from a callable object."""
        if callable_obj is None:
            return None

        instance_name = name or getattr(callable_obj, "__name__", "unnamed_function")

        ref = cls(
            name=instance_name,
            module_path=getattr(callable_obj, "__module__", None),
            function_name=getattr(callable_obj, "__name__", None),
        )

        # Determine callable type
        if inspect.isfunction(callable_obj):
            ref.callable_type = "function"
            # Try to get source code
            try:
                ref.source_code = inspect.getsource(callable_obj)
            except (TypeError, OSError):
                pass
        elif inspect.ismethod(callable_obj):
            ref.callable_type = "method"
        elif inspect.isclass(callable_obj):
            ref.callable_type = "class"
        elif callable(callable_obj) and ref.function_name is None:
            ref.callable_type = "lambda"
            try:
                ref.source_code = inspect.getsource(callable_obj)
            except (TypeError, OSError):
                pass
        else:
            ref.callable_type = "unknown"

        return ref

    def resolve(self) -> Any | None:
        """Resolve the reference back to a callable."""
        # Resolve from module path and name
        if self.module_path and self.function_name:
            try:
                module = importlib.import_module(self.module_path)
                return getattr(module, self.function_name)
            except (ImportError, AttributeError):
                pass

        # Try to resolve from source code if available
        if self.source_code:
            try:
                namespace = {}
                exec(self.source_code, namespace)
                # For functions/classes, the name should be in the namespace
                if self.function_name and self.function_name in namespace:
                    return namespace[self.function_name]
                # For lambdas or unnamed functions
                for obj in namespace.values():
                    if callable(obj):
                        return obj
            except Exception:
                pass

        return None
