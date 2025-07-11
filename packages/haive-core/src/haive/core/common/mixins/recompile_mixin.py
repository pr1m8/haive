"""Recompilation mixin for agents and engines that need dynamic recompilation.

This mixin provides standardized recompilation tracking and management
for components that can be dynamically updated (agents, engines, graphs).
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Set

from pydantic import Field

logger = logging.getLogger(__name__)


class RecompileMixin:
    """Mixin that adds recompilation tracking to agents and engines.

    This mixin provides:
    - Recompilation need tracking
    - Recompilation history
    - Reason logging for recompilation events
    - Automatic recompilation status management

    Components that inherit from this mixin can track when they need
    to be recompiled due to changes in tools, schemas, or other
    configuration updates.

    Example:
        ```python
        from haive.core.mixins.recompile_mixin import RecompileMixin
        from haive.agents.base.agent import Agent

        class MyAgent(Agent, RecompileMixin):
            def update_tools(self, new_tools):
                self.tools = new_tools
                self.mark_for_recompile("Tools updated")

            def compile_if_needed(self):
                if self.needs_recompile:
                    self.rebuild_graph()
                    self.resolve_recompile()
        ```
    """

    # Recompilation state
    needs_recompile: bool = Field(
        default=False, description="Whether this component needs recompilation"
    )

    recompile_reasons: list[str] = Field(
        default_factory=list, description="List of reasons why recompilation is needed"
    )

    recompile_count: int = Field(
        default=0, description="Total number of recompilations performed"
    )

    recompile_history: list[dict[str, Any]] = Field(
        default_factory=list, description="History of recompilation events"
    )

    # Automatic recompilation settings
    auto_recompile: bool = Field(
        default=False, description="Whether to automatically recompile when needed"
    )

    recompile_threshold: int = Field(
        default=10,
        description="Maximum number of pending reasons before forced recompile",
    )

    def mark_for_recompile(self, reason: str) -> None:
        """Mark this component as needing recompilation.

        Args:
            reason: Description of why recompilation is needed
        """
        if not self.needs_recompile:
            self.needs_recompile = True
            logger.info(
                f"Component {getattr(self, 'name', 'unnamed')} marked for recompile: {reason}"
            )

        # Add reason if not already present
        if reason not in self.recompile_reasons:
            self.recompile_reasons.append(reason)

        # Add to history
        self.recompile_history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "reason": reason,
                "action": "marked_for_recompile",
                "resolved": False,
            }
        )

        # Check if we should auto-recompile
        if (
            self.auto_recompile
            or len(self.recompile_reasons) >= self.recompile_threshold
        ):
            logger.warning(
                f"Component has {len(self.recompile_reasons)} pending reasons, forcing recompile"
            )
            self._trigger_auto_recompile()

    def resolve_recompile(self, success: bool = True) -> None:
        """Mark recompilation as resolved.

        Args:
            success: Whether the recompilation was successful
        """
        if not self.needs_recompile:
            logger.warning("resolve_recompile called but no recompilation was needed")
            return

        # Update state
        self.needs_recompile = False
        resolved_reasons = self.recompile_reasons.copy()
        self.recompile_reasons.clear()

        if success:
            self.recompile_count += 1
            logger.info(
                f"Component {getattr(self, 'name', 'unnamed')} recompilation resolved successfully"
            )
        else:
            logger.error(
                f"Component {getattr(self, 'name', 'unnamed')} recompilation failed"
            )

        # Update history
        self.recompile_history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "action": "resolved_recompile",
                "success": success,
                "resolved_reasons": resolved_reasons,
                "recompile_count": self.recompile_count,
            }
        )

        # Mark previous entries as resolved
        for entry in self.recompile_history:
            if entry.get("action") == "marked_for_recompile" and not entry.get(
                "resolved"
            ):
                entry["resolved"] = True
                entry["resolved_at"] = datetime.now().isoformat()

    def get_recompile_status(self) -> dict[str, Any]:
        """Get current recompilation status.

        Returns:
            Dictionary with recompilation status information
        """
        return {
            "needs_recompile": self.needs_recompile,
            "pending_reasons": self.recompile_reasons,
            "reason_count": len(self.recompile_reasons),
            "total_recompiles": self.recompile_count,
            "auto_recompile": self.auto_recompile,
            "last_recompile": self._get_last_recompile_timestamp(),
        }

    def clear_recompile_history(self, keep_recent: int = 10) -> None:
        """Clear recompilation history, optionally keeping recent entries.

        Args:
            keep_recent: Number of recent entries to keep (0 = clear all)
        """
        if keep_recent > 0:
            self.recompile_history = self.recompile_history[-keep_recent:]
        else:
            self.recompile_history.clear()

        logger.info(
            f"Recompilation history cleared, kept {len(self.recompile_history)} recent entries"
        )

    def force_recompile(self, reason: str = "Manual force recompile") -> None:
        """Force immediate recompilation regardless of current state.

        Args:
            reason: Reason for forcing recompilation
        """
        self.mark_for_recompile(reason)
        self._trigger_auto_recompile()

    def _trigger_auto_recompile(self) -> None:
        """Trigger automatic recompilation if supported.

        This method should be overridden by subclasses to implement
        actual recompilation logic.
        """
        logger.info(
            "Auto-recompile triggered - override _trigger_auto_recompile() to implement"
        )

        # Default behavior: just resolve the recompile
        # Subclasses should override this with actual recompilation logic
        self.resolve_recompile(success=True)

    def _get_last_recompile_timestamp(self) -> str | None:
        """Get timestamp of last successful recompilation."""
        for entry in reversed(self.recompile_history):
            if entry.get("action") == "resolved_recompile" and entry.get("success"):
                return entry.get("timestamp")
        return None

    def add_recompile_trigger(self, condition_func: callable, reason: str) -> None:
        """Add a condition that triggers recompilation.

        Args:
            condition_func: Function that returns True if recompilation needed
            reason: Reason to log if condition is met
        """
        if condition_func():
            self.mark_for_recompile(reason)

    def check_recompile_conditions(self) -> bool:
        """Check if any recompilation conditions are met.

        This method should be overridden by subclasses to implement
        specific recompilation condition checking.

        Returns:
            True if recompilation is needed
        """
        return self.needs_recompile
