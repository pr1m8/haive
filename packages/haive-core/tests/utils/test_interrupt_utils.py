"""
Tests for interrupt detection utilities in haive.core.utils.interrupt_utils:

- pause_for_human: raises LangGraph interrupt signal
- uses_pause: statically detects pause_for_human(...) via AST
- is_interruptible: checks functions and callables for pause usage

Includes test workarounds for LangGraph context and AST edge cases.
"""

from typing import Any
from unittest.mock import patch

import pytest

from haive.core.utils.interrupt_utils import (
    is_interruptible,
)
from haive.core.utils.interrupt_utils import pause_for_human as real_pause_for_human
from haive.core.utils.interrupt_utils import (
    uses_pause,
)

# === AST-compatible dummy function ===


# We define a local dummy pause_for_human to allow AST inspection.
def pause_for_human(x: Any) -> Any:
    """Dummy function to trigger AST name resolution."""
    return x


# === Local test functions for AST/interrupt detection ===


def function_without_pause() -> str:
    """Function with no interruption."""
    return "all good"


def function_with_pause() -> None:
    """Function that calls pause_for_human."""
    pause_for_human("pause here")


class CallableWithPause:
    """Callable class using pause_for_human in __call__."""

    def __call__(self) -> None:
        pause_for_human("interrupt")


class CallableWithoutPause:
    """Callable class with no interruption."""

    def __call__(self) -> str:
        return "continue"


# === Tests ===


def test_pause_for_human_runtime_error_outside_context() -> None:
    """
    pause_for_human should raise RuntimeError if called outside a LangGraph runnable context.
    """
    with pytest.raises(RuntimeError, match="get_config outside of a runnable context"):
        real_pause_for_human({"message": "pause now"})


def test_uses_pause_detects_function_with_pause() -> None:
    """
    uses_pause should return True for a function that calls pause_for_human.
    """
    assert uses_pause(function_with_pause) is True


def test_uses_pause_returns_false_for_function_without_pause() -> None:
    """
    uses_pause should return False for functions with no pause_for_human.
    """
    assert uses_pause(function_without_pause) is False


def test_is_interruptible_true_for_callable_with_pause() -> None:
    """
    is_interruptible should return True for callables using pause_for_human.
    """
    obj = CallableWithPause()
    assert is_interruptible(obj) is True


def test_is_interruptible_false_for_callable_without_pause() -> None:
    """
    is_interruptible should return False for callables with no pause usage.
    """
    obj = CallableWithoutPause()
    assert is_interruptible(obj) is False


def test_is_interruptible_returns_false_for_plain_function() -> None:
    """
    is_interruptible should return False for regular functions with no pause.
    """
    assert is_interruptible(function_without_pause) is False


def test_is_interruptible_returns_true_for_function_with_pause_via_patch() -> None:
    """
    Patch uses_pause to simulate interruptible function, since AST may fail to resolve pause_for_human.
    This ensures is_interruptible behaves correctly when pause usage is detected.
    """
    with patch("haive.core.utils.interrupt_utils.uses_pause", return_value=True):
        assert is_interruptible(function_with_pause) is True


def test_is_interruptible_safe_for_builtin_function() -> None:
    """
    is_interruptible should return False (not raise) for built-in functions.
    """
    assert is_interruptible(len) is False
