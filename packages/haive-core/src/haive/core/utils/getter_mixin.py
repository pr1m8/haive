"""
Collection utilities for Haive Core - GetterMixin.

This module includes powerful retrieval and filtering utilities
for collection classes.
"""

from typing import Any, Callable, Generic, List, Optional, Type, TypeVar

T = TypeVar('T')

class GetterMixin(Generic[T]):
    """
    A mixin providing rich lookup and filtering capabilities for collections.
    
    This mixin can be added to any collection class that implements
    _get_items() to provide powerful querying capabilities.
    """
    
    def _get_items(self) -> List[T]:
        """
        Get all items from the collection.
        
        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement _get_items()")
    
    def get_by_attr(self, attr_name: str, value: Any, default: Optional[T] = None) -> Optional[T]:
        """
        Get first item where attribute equals value.
        
        Args:
            attr_name: Attribute name to check
            value: Value to match
            default: Default value if not found
            
        Returns:
            First matching item or default
        """
        for item in self._get_items():
            if self._has_attr_value(item, attr_name, value):
                return item
        return default
    
    def get_all_by_attr(self, attr_name: str, value: Any) -> List[T]:
        """
        Get all items where attribute equals value.
        
        Args:
            attr_name: Attribute name to check
            value: Value to match
            
        Returns:
            List of matching items
        """
        return [item for item in self._get_items() if self._has_attr_value(item, attr_name, value)]
    
    def filter(self, **kwargs) -> List[T]:
        """
        Filter items by multiple attribute criteria.
        
        Args:
            **kwargs: Field name and value pairs to match
            
        Returns:
            List of matching items
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
        """
        Find first item matching a custom predicate function.
        
        Args:
            predicate: Function that takes item and returns boolean
            
        Returns:
            First matching item or None
        """
        for item in self._get_items():
            if predicate(item):
                return item
        return None
    
    def find_all(self, predicate: Callable[[T], bool]) -> List[T]:
        """
        Find all items matching a custom predicate function.
        
        Args:
            predicate: Function that takes item and returns boolean
            
        Returns:
            List of matching items
        """
        return [item for item in self._get_items() if predicate(item)]
    
    def get_by_type(self, type_cls: Type) -> List[T]:
        """
        Get all items of specified type.
        
        Args:
            type_cls: Type to match
            
        Returns:
            List of matching items
        """
        return [item for item in self._get_items() if isinstance(item, type_cls)]
    
    def field_values(self, field_name: str) -> List[Any]:
        """
        Get all values for a specific field across items.
        
        Args:
            field_name: Field name to collect
            
        Returns:
            List of field values
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
        """
        Get first item matching criteria.
        
        Args:
            **kwargs: Field name and value pairs to match
            
        Returns:
            First matching item or None
        """
        results = self.filter(**kwargs)
        return results[0] if results else None
    
    def _has_attr_value(self, item: Any, attr: str, value: Any) -> bool:
        """
        Check if item has attribute with specified value.
        
        Args:
            item: Item to check
            attr: Attribute name
            value: Value to match
            
        Returns:
            True if attribute matches value
        """
        if isinstance(item, dict):
            return attr in item and item[attr] == value
        return hasattr(item, attr) and getattr(item, attr) == value
"""