"""
Utilities for detecting whether a callable uses `pause_for_human(...)` to pause execution.

This wraps LangGraph's `interrupt(...)` signal and provides AST-based static analysis to detect
if a function or callable object may yield control for human input.
"""

import ast
import inspect
import textwrap
from functools import lru_cache
from typing import Any, Callable, TypeVar

from langgraph.types import interrupt

T = TypeVar("T")


def pause_for_human(payload: T) -> T:
    """
    Pause execution for human input and return a resume value of the same type.

    This is a wrapper around `langgraph.types.interrupt(...)` and should be used
    to signal an interruptible pause in a LangGraph node.

    Args:
        payload: The value to pass along with the interrupt signal.

    Returns:
        The same payload after human resumption.
    """
    return interrupt(payload)


class _PauseCallVisitor(ast.NodeVisitor):
    """
    AST visitor that detects calls to `pause_for_human(...)` within a function body.
    """

    def __init__(self) -> None:
        self.found = False

    def visit_Call(self, node: ast.Call) -> None:
        """
        Visit each call node to see if it's a call to `pause_for_human`.

        Supports both direct usage (`pause_for_human(...)`) and attribute access
        (`some_module.pause_for_human(...)`).
        """
        fn = node.func

        # Direct call: pause_for_human(...)
        if isinstance(fn, ast.Name) and fn.id == "pause_for_human":
            self.found = True
            return

        # Attribute call: module.pause_for_human(...)
        if isinstance(fn, ast.Attribute) and fn.attr == "pause_for_human":
            self.found = True
            return

        # Continue walking if not already found
        if not self.found:
            super().generic_visit(node)


@lru_cache(maxsize=256)
def uses_pause(fn: Callable[..., Any]) -> bool:
    """
    Detect whether a function contains a call to `pause_for_human(...)`.

    Args:
        fn: A top-level function or method object.

    Returns:
        True if the function body invokes `pause_for_human(...)`.
        False if the source cannot be retrieved or does not contain such a call.
    """
    try:
        src = inspect.getsource(fn)
    except (OSError, TypeError):
        # No source available (e.g., built-ins or C-extensions)
        return False

    src = textwrap.dedent(src)

    try:
        module = ast.parse(src)
    except SyntaxError:
        return False

    visitor = _PauseCallVisitor()
    visitor.visit(module)
    return visitor.found


def is_interruptible(obj: object) -> bool:
    """
    Determine whether an object will trigger an interrupt via `pause_for_human()`.

    Works for:
    - Plain functions and methods
    - Callable objects (e.g., classes with `__call__`)

    Args:
        obj: The object to test for interruptibility.

    Returns:
        True if the object contains or delegates to a function that uses `pause_for_human(...)`,
        False otherwise.
    """
    # Directly check plain functions
    if callable(obj) and not hasattr(obj, "__call__") and uses_pause(obj):
        return True

    # Check class __call__ method
    call_method = getattr(obj, "__call__", None)
    if callable(call_method):
        fn = getattr(obj.__class__, "__call__", None)
        if fn is not None:
            return uses_pause(fn)

    return False
