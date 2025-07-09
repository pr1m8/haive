# haive/agents/base/mixins/hooks_mixin.py

"""Enhanced hooks mixin for the Haive framework.

Provides a flexible hooks system that can be used by both single and multi agents,
with support for different hook points and graph-aware modifications.
"""

import logging
from collections.abc import Callable
from typing import Any, Generic, TypeVar

from pydantic import PrivateAttr

from haive.agents.base.types import HookContext, HookPoint, TState

logger = logging.getLogger(__name__)

# Type for hook results
T = TypeVar("T")


class HooksMixin(Generic[TState]):
    """Mixin that provides comprehensive hooks functionality.

    This mixin is generic over the state type, allowing hooks to be
    type-safe with respect to the agent's state schema.
    """

    # Private storage for hooks
    _hooks: dict[HookPoint, list[dict[str, Any]]] = PrivateAttr(default_factory=dict)
    _hook_enabled: bool = PrivateAttr(default=True)
    _hook_results: dict[str, Any] = PrivateAttr(default_factory=dict)

    def __init__(self, **kwargs):
        """Initialize hooks storage."""
        super().__init__(**kwargs)
        self._hooks = {point: [] for point in HookPoint}
        self._hook_enabled = True
        self._hook_results = {}

        # Auto-register decorated hooks
        self._auto_register_hooks()

    def _auto_register_hooks(self):
        """Automatically register methods decorated with @hook."""
        for attr_name in dir(self):
            if attr_name.startswith("_"):
                continue

            try:
                attr = getattr(self, attr_name)
                if hasattr(attr, "_hook_metadata"):
                    metadata = attr._hook_metadata
                    self.register_hook(
                        point=metadata["point"],
                        hook=attr,
                        priority=metadata.get("priority", 0),
                        name=metadata.get("name", attr_name),
                        graph_aware=metadata.get("graph_aware", False),
                    )
            except Exception as e:
                logger.debug(f"Error checking {attr_name} for hooks: {e}")

    def register_hook(
        self,
        point: HookPoint,
        hook: Callable,
        priority: int = 0,
        name: str | None = None,
        graph_aware: bool = False,
        condition: Callable[["HooksMixin", HookContext[TState]], bool] | None = None,
    ) -> None:
        """Register a hook with enhanced capabilities.

        Args:
            point: Hook point to register at
            hook: Hook function to call
            priority: Execution priority (higher = earlier)
            name: Optional hook name
            graph_aware: Whether hook needs graph context
            condition: Optional condition function
        """
        hook_entry = {
            "function": hook,
            "priority": priority,
            "name": name or getattr(hook, "__name__", f"hook_{id(hook)}"),
            "graph_aware": graph_aware,
            "condition": condition,
        }

        # Insert maintaining priority order
        hooks = self._hooks.setdefault(point, [])
        insert_idx = len(hooks)

        for i, existing in enumerate(hooks):
            if existing["priority"] < priority:
                insert_idx = i
                break

        hooks.insert(insert_idx, hook_entry)

        logger.debug(
            f"Registered {'graph-aware ' if graph_aware else ''}hook "
            f"'{hook_entry['name']}' at {point.value} with priority {priority}"
        )

    def run_hooks(
        self,
        point: HookPoint,
        *args,
        context: HookContext[TState] | None = None,
        **kwargs,
    ) -> Any:
        """Run hooks for a specific point with enhanced context.

        Returns:
            Last non-None result from hooks, or None
        """
        if not self._hook_enabled:
            return None

        # Create context if needed
        if context is None:
            context = HookContext[TState](
                hook_point=point,
                agent_id=getattr(self, "id", "unknown"),
                agent_type=self.__class__.__name__,
                state_type=getattr(self, "state_schema", None),
            )

        hooks = self._hooks.get(point, [])
        result = None

        for hook_entry in hooks:
            # Check condition if present
            if hook_entry["condition"]:
                try:
                    if not hook_entry["condition"](self, context):
                        continue
                except Exception as e:
                    logger.error(f"Hook condition error: {e}")
                    continue

            # Run hook
            try:
                hook_func = hook_entry["function"]
                hook_name = hook_entry["name"]

                logger.debug(f"Running hook '{hook_name}' at {point.value}")

                # Call with appropriate arguments
                if hook_entry["graph_aware"]:
                    # Graph-aware hooks get special treatment
                    hook_result = hook_func(self, *args, context=context, **kwargs)
                else:
                    # Regular hooks
                    hook_result = hook_func(self, *args, context=context, **kwargs)

                # Store result
                if hook_result is not None:
                    result = hook_result
                    self._hook_results[f"{point.value}:{hook_name}"] = hook_result

            except Exception as e:
                logger.error(f"Hook '{hook_entry['name']}' error at {point.value}: {e}")
                if logger.isEnabledFor(logging.DEBUG):
                    logger.exception("Full hook error:")

        return result

    def get_hook_result(self, point: HookPoint, hook_name: str) -> Any:
        """Get stored result from a previous hook execution."""
        key = f"{point.value}:{hook_name}"
        return self._hook_results.get(key)

    def clear_hook_results(self):
        """Clear all stored hook results."""
        self._hook_results.clear()

    def unregister_hook(
        self, point: HookPoint, hook: Callable | str | None = None
    ) -> None:
        """Unregister one or all hooks at a point."""
        if point not in self._hooks:
            return

        if hook is None:
            self._hooks[point] = []
        else:
            hooks = self._hooks[point]
            if isinstance(hook, str):
                self._hooks[point] = [h for h in hooks if h["name"] != hook]
            else:
                self._hooks[point] = [h for h in hooks if h["function"] is not hook]

    def enable_hooks(self) -> None:
        """Enable hook execution."""
        self._hook_enabled = True

    def disable_hooks(self) -> None:
        """Disable hook execution."""
        self._hook_enabled = False

    def list_hooks(self) -> dict[str, list[dict[str, Any]]]:
        """List all registered hooks with metadata."""
        return {
            point.value: [
                {
                    "name": h["name"],
                    "priority": h["priority"],
                    "graph_aware": h["graph_aware"],
                    "has_condition": h["condition"] is not None,
                }
                for h in hooks
            ]
            for point, hooks in self._hooks.items()
            if hooks
        }


# Hook decorator
def hook(
    point: HookPoint,
    priority: int = 0,
    name: str | None = None,
    graph_aware: bool = False,
    condition: Callable | None = None,
):
    """Decorator for marking methods as hooks.

    Usage:
        @hook(HookPoint.AFTER_GRAPH_BUILD, priority=10)
        def add_output_parser(self, graph, context):
            # Modify graph
            return graph
    """

    def decorator(func: Callable) -> Callable:
        func._hook_metadata = {
            "point": point,
            "priority": priority,
            "name": name or func.__name__,
            "graph_aware": graph_aware,
            "condition": condition,
        }
        return func

    return decorator
