import logging
from typing import Any

from playwright.async_api import Page

# Set up logging
logger = logging.getLogger(__name__)


class StateWrapper:
    """A wrapper for state dictionaries that stores Page objects separately.
    This avoids serialization issues by keeping non-serializable objects
    outside the state dictionary.
    """

    def __init__(self):
        # Store global instances of non-serializable objects
        self._page_instance: Page | None = None
        self._other_objects: dict[str, Any] = {}

    def set_page(self, page: Page) -> None:
        """Store the Page object."""
        self._page_instance = page

    def get_page(self) -> Page | None:
        """Retrieve the stored Page object."""
        return self._page_instance

    def store_object(self, key: str, obj: Any) -> None:
        """Store any other non-serializable object."""
        self._other_objects[key] = obj

    def get_object(self, key: str) -> Any:
        """Retrieve a stored non-serializable object."""
        return self._other_objects.get(key)

    def prepare_input(self, state: dict[str, Any]) -> dict[str, Any]:
        """Prepare state for LangGraph by removing any Page objects.

        Args:
            state: The input state dictionary

        Returns:
            A new state dict with Page objects removed
        """
        # Make a copy to avoid modifying the original
        clean_state = state.copy()

        # Check for and remove page object
        if "page" in clean_state:
            # Store it for later retrieval
            self.set_page(clean_state["page"])
            # Remove from state
            del clean_state["page"]
            logger.debug("Removed Page object from state for serialization")

        return clean_state

    def inject_page(self, state: dict[str, Any]) -> dict[str, Any]:
        """Re-inject the Page object into a state dict.

        Args:
            state: The state dictionary to update

        Returns:
            Updated state with Page object added
        """
        if self._page_instance:
            # Make a copy with the page added
            updated_state = state.copy()
            updated_state["page"] = self._page_instance
            logger.debug("Re-injected Page object into state")
            return updated_state
        return state


# Create a global instance
state_wrapper = StateWrapper()
