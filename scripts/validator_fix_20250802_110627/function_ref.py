import contextlib
import importlib
import inspect
from typing import Any, Literal, Optional, Self

from haive.core.graph.state_graph.base import SerializableModel
from pydantic import Field, field_validator, model_validator


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
    __abstract__ = True

    @model_validator(mode="after")
    def ensure_valid_reference(self) -> Self:
        """Ensure the reference is valid."""
        if not self.module_path and (not self.function_name) and (not self.source_code):
            raise ValueError(
                "Function reference must have either module_path and function_name, or source_code"
            )
        return self

    @field_validator("callable_type")
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
        if inspect.isfunction(callable_obj):
            ref.callable_type = "function"
            with contextlib.suppress(TypeError, OSError):
                ref.source_code = inspect.getsource(callable_obj)
        elif inspect.ismethod(callable_obj):
            ref.callable_type = "method"
        elif inspect.isclass(callable_obj):
            ref.callable_type = "class"
        elif callable(callable_obj) and ref.function_name is None:
            ref.callable_type = "lambda"
            with contextlib.suppress(TypeError, OSError):
                ref.source_code = inspect.getsource(callable_obj)
        else:
            ref.callable_type = "unknown"
        return ref

    def resolve(self) -> Any | None:
        """Resolve the reference back to a callable."""
        if self.module_path and self.function_name:
            try:
                module = importlib.import_module(self.module_path)
                return getattr(module, self.function_name)
            except (ImportError, AttributeError):
                pass
        if self.source_code:
            try:
                namespace = {}
                exec(self.source_code, namespace)
                if self.function_name and self.function_name in namespace:
                    return namespace[self.function_name]
                for obj in namespace.values():
                    if callable(obj):
                        return obj
            except Exception:
                pass
        return None
