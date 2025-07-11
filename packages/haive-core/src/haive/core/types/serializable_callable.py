from importlib import import_module
from typing import Any, Callable, Protocol, TypeVar, runtime_checkable

P = TypeVar("P")
R = TypeVar("R")


@runtime_checkable
class SerializableCallable(Protocol):
    """Protocol for callables that can be serialized to and from importable strings.

    Limitations:
    - Works only with top-level functions or class/static methods.
    - Lambdas, closures, and dynamically-defined functions are not supported.
    """

    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...

    @classmethod
    def is_serializable(cls, func: Callable[..., Any]) -> bool:
        if not callable(func):
            return False

        if not hasattr(func, "__module__") or not hasattr(func, "__qualname__"):
            return False

        if "<locals>" in func.__qualname__ or func.__module__ == "__main__":
            return False

        # Reject instance methods (bound methods)
        return not (hasattr(func, "__self__") and not isinstance(func.__self__, type))

    @classmethod
    def serialize(cls, func: Callable[P, R]) -> str:
        """Convert a callable to a string path.

        Example:
            my.module.my_function
            my.module.MyClass.static_method
        """
        if not cls.is_serializable(func):
            raise ValueError(
                f"Cannot serialize callable {func} — must be a global or class-level callable"
            )

        return f"{func.__module__}.{func.__qualname__}"

    @classmethod
    def deserialize(cls, path: str) -> Callable[..., Any]:
        """Convert an importable string path back into a callable.

        Supports nested attributes, e.g.:
            my.module.Class.method
        """
        try:
            module_path, _, attr_path = path.partition(".")
            module_parts = path.split(".")
            for i in range(len(module_parts), 0, -1):
                try:
                    module_name = ".".join(module_parts[:i])
                    attr_chain = module_parts[i:]
                    module = import_module(module_name)
                    break
                except ImportError:
                    continue
            else:
                raise ImportError(f"No importable module found in '{path}'")

            obj = module
            for attr in attr_chain:
                obj = getattr(obj, attr)

            if not callable(obj):
                raise TypeError(f"Resolved object '{path}' is not callable")
            return obj

        except Exception as e:
            raise ImportError(f"Failed to deserialize callable from '{path}': {e}")
