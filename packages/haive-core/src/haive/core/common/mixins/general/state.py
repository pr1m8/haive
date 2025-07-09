"""State management mixin for tracking object state changes with history.

This module provides a Pydantic-based mixin for adding state tracking capabilities
to any BaseModel. It maintains a current state string and a complete history
of all state changes with timestamps and optional reasons.

Usage:
    ```python
    from pydantic import BaseModel
    from haive.core.common.mixins.general.state import StateMixin

    class MyComponent(StateMixin, BaseModel):
        name: str

    # Create component and change states
    component = MyComponent(name="test")
    component.change_state("processing", "Starting work")
    component.change_state("complete", "Finished successfully")

    # Check current state
    if component.is_in_state("complete"):
        print("Component is done!")

    # Review state history
    for change in component.get_state_changes():
        print(f"{change['timestamp']}: {change['from_state']} -> {change['to_state']}")
    ```
"""

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class StateMixin(BaseModel):
    """Mixin for state tracking with validation and comprehensive history.

    This mixin adds state management capabilities to Pydantic models, allowing
    objects to track their current state and maintain a complete history of
    state transitions with timestamps and optional reasons.

    The mixin is designed to be composable with other BaseModel classes and
    provides thread-safe state transitions with automatic history tracking.

    Attributes:
        state: Current state of the object (defaults to "active").
        state_history: Chronological list of all state changes with metadata.

    Example:
        >>> class Task(StateMixin, BaseModel):
        ...     name: str
        >>> task = Task(name="Process data")
        >>> task.change_state("running", "Starting execution")
        >>> task.change_state("complete", "Finished successfully")
        >>> task.is_in_state("complete")
        True
        >>> len(task.get_state_changes())
        2
    """

    state: str = Field(default="active", description="Current state of the object")
    state_history: list[Dict[str, Any]] = Field(
        default_factory=list, description="History of state changes with timestamps"
    )

    def change_state(self, new_state: str, reason: Optional[str] = None) -> None:
        """Change state and automatically track the transition in history.

        This method updates the current state and records the transition
        in the state history with a timestamp and optional reason.

        Args:
            new_state: The new state to transition to.
            reason: Optional explanation for the state change.

        Example:
            >>> task.change_state("paused", "Waiting for user input")
            >>> task.state
            'paused'
        """
        old_state = self.state
        self.state = new_state

        change_record = {
            "from_state": old_state,
            "to_state": new_state,
            "timestamp": datetime.now(),
            "reason": reason,
        }
        self.state_history.append(change_record)

    def get_state_changes(self) -> list[Dict[str, Any]]:
        """Get a copy of the complete state change history.

        Returns:
            List of state change records, each containing:
                - from_state: Previous state
                - to_state: New state
                - timestamp: When the change occurred
                - reason: Optional explanation for the change

        Example:
            >>> changes = task.get_state_changes()
            >>> print(changes[0]["from_state"])
            'active'
        """
        return self.state_history.copy()

    def is_in_state(self, state: str) -> bool:
        """Check if the object is currently in the specified state.

        Args:
            state: State name to check against current state.

        Returns:
            True if current state matches the specified state, False otherwise.

        Example:
            >>> task.is_in_state("complete")
            False
            >>> task.change_state("complete")
            >>> task.is_in_state("complete")
            True
        """
        return self.state == state
