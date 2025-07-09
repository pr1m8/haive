"""
Reference classes for serializing callables and types.
"""

import importlib
import inspect
import logging
import uuid
from functools import partial
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    get_args,
    get_origin,
)

from pydantic import BaseModel, ConfigDict, Field

logger = logging.getLogger(__name__)

T = TypeVar("T")


class CallableReference(BaseModel):
    """
    Serializable reference to a callable.

    This class can store and resolve references to:
    - Module-level functions
    - Lambda functions
    - Methods
    - Partial functions
    - Directly passed callables
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    module_path: Optional[str] = None
    name: Optional[str] = None
    callable_type: str = "function"
    source_code: Optional[str] = None
    args: Optional[Tuple] = None
    kwargs: Optional[Dict[str, Any]] = None

    # Store function object in a non-serialized field
    # Using proper naming that Pydantic allows
    runtime_func: Optional[Callable] = Field(default=None, exclude=True)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def from_callable(cls, callable_obj: Callable) -> Optional["CallableReference"]:
        """Create reference from a callable."""
        if callable_obj is None:
            return None

        ref = cls()
        # Store the function directly for runtime use
        ref.runtime_func = callable_obj
        ref.module_path = getattr(callable_obj, "__module__", None)
        ref.name = getattr(callable_obj, "__name__", None)

        # Handle different callable types
        if inspect.isfunction(callable_obj):
            ref.callable_type = "function"
            # Special handling for lambda functions
            if callable_obj.__name__ == "<lambda>":
                ref.callable_type = "lambda"
                try:
                    source_code = inspect.getsource(callable_obj).strip()
                    # Clean source code to prevent tuple evaluation issues
                    source_code = source_code.rstrip(",;")
                    ref.source_code = source_code
                except (IOError, TypeError):
                    # If we can't get source, we'll rely on the direct reference
                    logger.debug(f"Could not get source for lambda: {callable_obj}")
                    pass
        elif inspect.ismethod(callable_obj):
            ref.callable_type = "method"
            # Try to get instance info
            if hasattr(callable_obj, "__self__"):
                ref.kwargs = {"instance_id": id(callable_obj.__self__)}
        elif callable_obj.__class__.__name__ == "partial":
            ref.callable_type = "partial"
            # Try to get info about the wrapped function
            wrapped_func = callable_obj.func
            ref.name = getattr(wrapped_func, "__name__", "partial_func")
            ref.module_path = getattr(wrapped_func, "__module__", None)
            # Store args and kwargs
            ref.args = callable_obj.args
            ref.kwargs = callable_obj.keywords
        else:
            ref.callable_type = callable_obj.__class__.__name__

        return ref

    def resolve(self) -> Optional[Callable]:
        """
        Resolve reference to a callable.

        Priority:
        1. Direct function reference if available
        2. Module/name resolution for regular functions
        3. Source code evaluation for lambdas
        4. Partial function reconstruction
        """
        # First priority: use directly stored function if available
        if self.runtime_func is not None:
            return self.runtime_func

        # Second priority: resolve by module and name
        if self.module_path and self.name and self.callable_type != "lambda":
            try:
                module = importlib.import_module(self.module_path)
                func = getattr(module, self.name)

                # Handle partial functions
                if self.callable_type == "partial":
                    args = self.args or ()
                    kwargs = self.kwargs or {}
                    return partial(func, *args, **kwargs)

                return func
            except Exception as e:
                logger.error(
                    f"Failed to resolve function {self.module_path}.{self.name}: {e}"
                )

        # Third priority: evaluate lambda source code
        if self.source_code and self.callable_type == "lambda":
            try:
                # Clean source code to prevent tuple issues
                source = self.source_code
                # Remove trailing comma/semicolon if present
                source = source.rstrip(",;")

                # SECURITY NOTE: Only use with trusted data
                # Using a local scope to evaluate lambda
                local_vars = {}
                exec("func = " + source, globals(), local_vars)
                return local_vars["func"]
            except Exception as e:
                logger.error(f"Failed to resolve lambda from source: {e}")

        # Last resort: dynamic import for specific cases
        if self.callable_type == "function" and self.module_path and self.name:
            try:
                # Try to dynamically import the module
                spec = importlib.util.find_spec(self.module_path)
                if spec:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    if hasattr(module, self.name):
                        return getattr(module, self.name)
            except Exception as e:
                logger.debug(
                    f"Failed dynamic import for {self.module_path}.{self.name}: {e}"
                )

        # Could not resolve
        logger.warning(
            f"Could not resolve callable reference: {self.module_path}.{self.name}"
        )
        return None


class TypeReference(BaseModel):
    """Reference to a type that can be serialized."""

    module_path: Optional[str] = None
    name: str
    is_generic: bool = False
    generic_args: Optional[List["TypeReference"]] = None
    generic_origin: Optional[str] = None

    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)

    @classmethod
    def from_type(cls, type_obj: Optional[Type]) -> Optional["TypeReference"]:
        """Create a TypeReference from a type object."""
        if type_obj is None:
            return None

        # Get basic type info
        ref = cls(
            name=getattr(type_obj, "__name__", str(type_obj)),
            module_path=getattr(type_obj, "__module__", None),
        )

        # Handle generic types (like List[str], Dict[str, int], etc.)
        origin = get_origin(type_obj)
        if origin is not None:
            ref.is_generic = True
            ref.generic_origin = getattr(origin, "__name__", str(origin))

            # Get generic arguments
            args = get_args(type_obj)
            if args:
                ref.generic_args = [cls.from_type(arg) for arg in args]

        return ref

    def resolve(self) -> Optional[Type]:
        """Resolve the reference back to a type."""
        if not self.module_path or not self.name:
            return None

        try:
            # Import the base module
            module = importlib.import_module(self.module_path)
            base_type = getattr(module, self.name)

            # If not generic, return the base type
            if not self.is_generic:
                return base_type

            # If generic, reconstruct with arguments
            if self.generic_origin and self.generic_args:
                # Import typing module for generic types
                import typing

                origin = getattr(typing, self.generic_origin, None)

                if origin:
                    # Resolve generic arguments
                    args = [arg.resolve() for arg in self.generic_args]
                    # Filter out None values
                    args = [arg for arg in args if arg is not None]

                    # Create generic type
                    if len(args) == 1:
                        return origin[args[0]]
                    elif len(args) > 1:
                        return origin[tuple(args)]

            # Fallback to base type
            return base_type

        except (ImportError, AttributeError) as e:
            logger.error(f"Error resolving type: {e}")
            return None
