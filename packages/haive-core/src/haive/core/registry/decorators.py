# src/haive/core/registry/decorators.py

import logging
from functools import wraps
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
)

logger = logging.getLogger(__name__)

T = TypeVar("T")
if TYPE_CHECKING:
    from haive.core.registry.base import AbstractRegistry


def register_component(
    registry_getter: Union[str, Callable[[], "AbstractRegistry"]] = None,
    component_type: Any = None,
    auto_register: bool = True,
    metadata: Optional[Dict[str, Any]] = None,
    extract_fields: Optional[List[str]] = None,
    transform: Optional[Callable[[Any], Any]] = None,
    registry_method: str = "register",
):
    """
    Universal decorator for registering components with any registry.

    Args:
        registry_getter: String name of registry or callable that returns the registry instance
        component_type: Optional component type to use for registration
        auto_register: Whether to automatically register instances on creation
        metadata: Additional metadata to attach during registration
        extract_fields: Specific fields to extract from the component
        transform: Function to transform component before registration
        registry_method: Name of registration method to call on registry

    Returns:
        Decorated class with registration capabilities
    """

    def decorator(cls: Type[T]) -> Type[T]:
        # Store original __init__
        original_init = cls.__init__

        @wraps(cls.__init__)
        def new_init(self, *args, **kwargs):
            # Call original init
            original_init(self, *args, **kwargs)

            # Auto-register if enabled
            if auto_register:
                try:
                    # Get the appropriate registry
                    registry = _get_registry(registry_getter)

                    # Prepare component for registration
                    reg_item = _prepare_component(
                        self, component_type, metadata, extract_fields, transform
                    )

                    # Register with the registry
                    register_fn = getattr(registry, registry_method)
                    register_fn(reg_item)

                    logger.debug(
                        f"Auto-registered {cls.__name__} with {registry.__class__.__name__}"
                    )
                except Exception as e:
                    logger.warning(f"Failed to auto-register {cls.__name__}: {e}")

            # REMOVED: return self - __init__ should not return anything

        # Replace __init__
        cls.__init__ = new_init

        # Add class method for explicit registration
        @classmethod
        def register_instance(cls, instance, custom_registry=None, **kwargs):
            """Register an instance with the appropriate registry."""
            registry = custom_registry or _get_registry(registry_getter)

            # Prepare component with any additional kwargs
            extra_metadata = {**(metadata or {}), **kwargs}
            reg_item = _prepare_component(
                instance, component_type, extra_metadata, extract_fields, transform
            )

            # Register with registry
            register_fn = getattr(registry, registry_method)
            return register_fn(reg_item)

        cls.register_instance = register_instance

        # Store registration info on class for inspection
        cls.__registry_info__ = {
            "auto_register": auto_register,
            "component_type": component_type,
            "metadata": metadata,
            "extract_fields": extract_fields,
        }

        return cls

    def _get_registry(registry_ref):
        """Helper function to get the registry instance."""
        from haive.core.registry.manager import RegistryManager

        # Default to RegistryManager instance
        if registry_ref is None:
            return RegistryManager.get_instance().get_registry()

        # If it's a string, treat as registry type
        if isinstance(registry_ref, str):
            return RegistryManager.get_instance().create_registry(registry_ref)

        # If it's callable, call to get registry
        if callable(registry_ref):
            return registry_ref()

        # If it's already a registry, return it
        if hasattr(registry_ref, "register"):
            return registry_ref

        # Fallback to default registry
        return RegistryManager.get_instance().get_registry()

    def _prepare_component(instance, comp_type, meta, fields, transform_fn):
        """Prepare component for registration with appropriate fields and metadata."""
        # Start with the instance itself as the registration target
        reg_item = instance

        # Apply transformation if specified
        if transform_fn is not None:
            reg_item = transform_fn(instance)

        # Extract specific fields if requested
        if fields is not None:
            # For Pydantic models
            if hasattr(instance, "model_dump"):
                data = instance.model_dump(include=set(fields))
                # Add metadata if provided
                if meta:
                    data["metadata"] = meta
                reg_item = data
            # For regular classes
            else:
                data = {
                    field: getattr(instance, field)
                    for field in fields
                    if hasattr(instance, field)
                }
                # Add metadata if provided
                if meta:
                    data["metadata"] = meta
                reg_item = data

        # Add metadata to Pydantic models if not extracting fields
        elif meta and hasattr(instance, "metadata") and fields is None:
            # Update instance metadata
            instance.metadata.update(meta)

        # Determine component type if needed
        if comp_type is None:
            # Check common attributes
            for attr in ["engine_type", "component_type", "type"]:
                if hasattr(instance, attr):
                    comp_type = getattr(instance, attr)
                    break

        # If we have a component type and it's not already attached
        if comp_type is not None:
            # If it's a dict, add component_type
            if isinstance(reg_item, dict):
                reg_item["component_type"] = comp_type
            # For objects with engine_type but not component_type
            elif hasattr(reg_item, "engine_type") and not hasattr(
                reg_item, "component_type"
            ):
                # This is fine - engine_type serves the same purpose
                pass
            # If it's an object without component_type, try to add it
            elif not hasattr(reg_item, "component_type"):
                try:
                    reg_item.component_type = comp_type
                except (AttributeError, TypeError):
                    # Can't modify the object, may be immutable
                    pass

        return reg_item

    return decorator
