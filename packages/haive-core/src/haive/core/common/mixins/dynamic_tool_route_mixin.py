"""Dynamic Tool Route Mixin with Recompilation Signaling.

This mixin extends ToolRouteMixin to provide callbacks when tool routes change,
enabling graphs to know when they need recompilation.
"""

import logging
from typing import Any, Callable, Dict, List, Optional, Set

from pydantic import Field, PrivateAttr

from haive.core.common.mixins.tool_route_mixin import ToolRouteMixin

logger = logging.getLogger(__name__)


class DynamicToolRouteMixin(ToolRouteMixin):
    """Extended tool route mixin that signals when routes change.

    This allows graphs and agents to register callbacks that get triggered
    when tool routes are added, updated, or removed, enabling dynamic
    recompilation of graphs when needed.
    """

    # Private attributes for change tracking
    _route_change_callbacks: list[Callable[[str, str, str | None], None]] = PrivateAttr(
        default_factory=list
    )
    _route_observers: dict[str, list[Callable]] = PrivateAttr(default_factory=dict)
    _pending_changes: set[str] = PrivateAttr(default_factory=set)

    def register_route_change_callback(
        self,
        callback: Callable[[str, str, str | None], None],
        callback_id: str | None = None,
    ) -> str:
        """Register a callback for tool route changes.

        Args:
            callback: Function called with (tool_name, action, old_route)
                     action can be 'added', 'updated', or 'removed'
            callback_id: Optional ID for the callback (for removal)

        Returns:
            Callback ID for later removal
        """
        self._route_change_callbacks.append(callback)
        callback_id = callback_id or f"callback_{len(self._route_change_callbacks)}"

        if callback_id not in self._route_observers:
            self._route_observers[callback_id] = []
        self._route_observers[callback_id].append(callback)

        logger.debug(f"Registered route change callback: {callback_id}")
        return callback_id

    def unregister_route_change_callback(self, callback_id: str) -> bool:
        """Remove a registered callback by ID."""
        if callback_id in self._route_observers:
            callbacks = self._route_observers.pop(callback_id)
            for cb in callbacks:
                if cb in self._route_change_callbacks:
                    self._route_change_callbacks.remove(cb)
            return True
        return False

    def _notify_route_change(
        self, tool_name: str, action: str, old_route: str | None = None
    ) -> None:
        """Notify all registered callbacks of a route change.

        Args:
            tool_name: Name of the tool that changed
            action: Type of change ('added', 'updated', 'removed')
            old_route: Previous route (for updates)
        """
        self._pending_changes.add(tool_name)

        for callback in self._route_change_callbacks:
            try:
                callback(tool_name, action, old_route)
            except Exception as e:
                logger.exception(f"Error in route change callback: {e}")

    def add_tool(
        self,
        tool: Any,
        route: str | None = None,
        metadata: dict[str, Any] | None = None,
        notify: bool = True,
    ) -> "DynamicToolRouteMixin":
        """Add a tool and optionally notify observers.

        Args:
            tool: Tool to add
            route: Route for the tool
            metadata: Tool metadata
            notify: Whether to notify observers (default: True)
        """
        # Call parent implementation
        super().add_tool(tool, route, metadata)

        # Notify observers if enabled
        if notify:
            tool_name = self._get_tool_name(tool)
            self._notify_route_change(tool_name, "added", None)

        return self

    def update_tool_route(
        self, tool_name: str, new_route: str, notify: bool = True
    ) -> "DynamicToolRouteMixin":
        """Update a tool's route and optionally notify observers.

        Args:
            tool_name: Name of tool to update
            new_route: New route for the tool
            notify: Whether to notify observers (default: True)
        """
        old_route = self.tool_routes.get(tool_name)

        # Call parent implementation
        super().update_tool_route(tool_name, new_route)

        # Notify observers if enabled
        if notify and old_route != new_route:
            self._notify_route_change(tool_name, "updated", old_route)

        return self

    def remove_tool(
        self, tool_name: str, notify: bool = True
    ) -> "DynamicToolRouteMixin":
        """Remove a tool and optionally notify observers.

        Args:
            tool_name: Name of tool to remove
            notify: Whether to notify observers (default: True)
        """
        old_route = self.tool_routes.get(tool_name)

        # Remove the tool
        if tool_name in self.tool_routes:
            del self.tool_routes[tool_name]
        if tool_name in self.tool_metadata:
            del self.tool_metadata[tool_name]
        if tool_name in self.tool_instances:
            del self.tool_instances[tool_name]

        # Notify observers if enabled
        if notify:
            self._notify_route_change(tool_name, "removed", old_route)

        return self

    def batch_update_tools(
        self, updates: list[dict[str, Any]], notify_once: bool = True
    ) -> "DynamicToolRouteMixin":
        """Perform multiple tool updates and notify once at the end.

        Args:
            updates: List of update operations
                    Each dict should have 'action', 'tool_name', and relevant params
            notify_once: If True, notifies once after all updates
        """
        # Disable notifications during batch update
        for update in updates:
            action = update.get("action")

            if action == "add":
                self.add_tool(
                    update["tool"],
                    update.get("route"),
                    update.get("metadata"),
                    notify=False,
                )
            elif action == "update":
                self.update_tool_route(
                    update["tool_name"], update["new_route"], notify=False
                )
            elif action == "remove":
                self.remove_tool(update["tool_name"], notify=False)

        # Notify once for all changes
        if notify_once and self._pending_changes:
            for tool_name in self._pending_changes:
                self._notify_route_change(tool_name, "batch_update", None)
            self._pending_changes.clear()

        return self

    def get_pending_changes(self) -> set[str]:
        """Get set of tools with pending changes."""
        return self._pending_changes.copy()

    def clear_pending_changes(self) -> None:
        """Clear the pending changes set."""
        self._pending_changes.clear()

    def has_pending_changes(self) -> bool:
        """Check if there are any pending changes."""
        return len(self._pending_changes) > 0
