"""Collection utility mixin providing flexible query capabilities.

This module provides a mixin class that adds powerful filtering and lookup
capabilities to collection classes. It enables attribute-based lookups,
type filtering, predicate-based searches, and more.

Usage:
    ```python
    from typing import List
    from haive.core.common.mixins import GetterMixin

    class UserCollection(GetterMixin[User]):
        def __init__(self, users: List[User]):
            self._users = users

        def _get_items(self) -> List[User]:
            return self._users

    # Create collection
    users = UserCollection([
        User(id="1", name="Alice", role="admin"),
        User(id="2", name="Bob", role="user"),
        User(id="3", name="Charlie", role="user")
    ])

    # Find all users with role="user"
    user_role_users = users.get_all_by_attr("role", "user")

    # Find first admin
    admin = users.get_by_attr("role", "admin")

    # Get all usernames
    names = users.field_values("name")
    ```
"""

from typing import Any, Callable, Generic, List, Optional, Type, TypeVar

T = TypeVar("T")


class GetterMixin(Generic[T]):
    """A mixin providing rich lookup and filtering capabilities for collections.

    This mixin can be added to any collection class that implements
    _get_items() to provide powerful querying capabilities. It works with
    both dictionary-like objects and objects with attributes.

    The mixin is generic over type T, which represents the type of items
    in the collection. This enables proper type hinting when using the
    mixin's methods.

    Attributes:
        None directly, but requires subclasses to implement _get_items()
    """

    def _get_items(self) -> List[T]:
        """Get all items from the collection.

        This method must be implemented by subclasses to provide access
        to the underlying collection of items.

        Returns:
            A list of items of type T.

        Raises:
            NotImplementedError: If not implemented by subclass.
        """
        raise NotImplementedError("Subclasses must implement _get_items()")

    def get_by_attr(
        self, attr_name: str, value: Any, default: Optional[T] = None
    ) -> Optional[T]:
        """Get first item where attribute equals value.

        This method finds the first item in the collection where the
        specified attribute matches the given value.

        Args:
            attr_name: Attribute name to check.
            value: Value to match.
            default: Default value if not found.

        Returns:
            First matching item or default if none found.
        """
        for item in self._get_items():
            if self._has_attr_value(item, attr_name, value):
                return item
        return default

    def get_all_by_attr(self, attr_name: str, value: Any) -> List[T]:
        """Get all items where attribute equals value.

        This method finds all items in the collection where the
        specified attribute matches the given value.

        Args:
            attr_name: Attribute name to check.
            value: Value to match.

        Returns:
            List of matching items (empty list if none found).
        """
        return [
            item
            for item in self._get_items()
            if self._has_attr_value(item, attr_name, value)
        ]

    def filter(self, **kwargs) -> List[T]:
        """Filter items by multiple attribute criteria.

        This method finds all items that match all of the specified
        attribute criteria (logical AND of all criteria).

        Args:
            **kwargs: Field name and value pairs to match.

        Returns:
            List of matching items (empty list if none found).

        Example:
            ```python
            # Find all admin users with status='active'
            active_admins = collection.filter(role="admin", status="active")
            ```
        """
        results = []
        for item in self._get_items():
            match = True
            for attr, value in kwargs.items():
                if not self._has_attr_value(item, attr, value):
                    match = False
                    break
            if match:
                results.append(item)
        return results

    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        """Find first item matching a custom predicate function.

        This method finds the first item for which the predicate
        function returns True.

        Args:
            predicate: Function that takes an item and returns a boolean.

        Returns:
            First matching item or None if none found.

        Example:
            ```python
            # Find first user with name longer than 10 characters
            user = users.find(lambda u: len(u.name) > 10)
            ```
        """
        for item in self._get_items():
            if predicate(item):
                return item
        return None

    def find_all(self, predicate: Callable[[T], bool]) -> List[T]:
        """Find all items matching a custom predicate function.

        This method finds all items for which the predicate
        function returns True.

        Args:
            predicate: Function that takes an item and returns a boolean.

        Returns:
            List of matching items (empty list if none found).

        Example:
            ```python
            # Find all premium users with subscription expiring in 7 days
            from datetime import datetime, timedelta
            next_week = datetime.now() + timedelta(days=7)
            expiring = users.find_all(
                lambda u: u.is_premium and u.expires_at.date() == next_week.date()
            )
            ```
        """
        return [item for item in self._get_items() if predicate(item)]

    def get_by_type(self, type_cls: Type) -> List[T]:
        """Get all items of specified type.

        This method finds all items that are instances of the specified type.

        Args:
            type_cls: Type to match.

        Returns:
            List of matching items (empty list if none found).

        Example:
            ```python
            # Get all TextMessage instances
            text_messages = messages.get_by_type(TextMessage)
            ```
        """
        return [item for item in self._get_items() if isinstance(item, type_cls)]

    def field_values(self, field_name: str) -> List[Any]:
        """Get all values for a specific field across items.

        This method collects the values of a specific field or attribute
        from all items in the collection.

        Args:
            field_name: Field name to collect.

        Returns:
            List of field values (None for items where field doesn't exist).

        Example:
            ```python
            # Get all user IDs
            user_ids = users.field_values("id")
            ```
        """
        results = []
        for item in self._get_items():
            if isinstance(item, dict) and field_name in item:
                results.append(item[field_name])
            elif hasattr(item, field_name):
                value = getattr(item, field_name)
                results.append(value)
            else:
                results.append(None)
        return results

    def first(self, **kwargs) -> Optional[T]:
        """Get first item matching criteria.

        This is a convenience method that combines filter() with
        returning the first result only.

        Args:
            **kwargs: Field name and value pairs to match.

        Returns:
            First matching item or None if none found.

        Example:
            ```python
            # Find first active admin user
            admin = users.first(role="admin", status="active")
            ```
        """
        results = self.filter(**kwargs)
        return results[0] if results else None

    def _has_attr_value(self, item: Any, attr: str, value: Any) -> bool:
        """Check if item has attribute with specified value.

        This internal helper method handles both dictionary-style items
        and object-style items with attributes.

        Args:
            item: Item to check.
            attr: Attribute name.
            value: Value to match.

        Returns:
            True if attribute matches value, False otherwise.
        """
        if isinstance(item, dict):
            return attr in item and item[attr] == value
        return hasattr(item, attr) and getattr(item, attr) == value
