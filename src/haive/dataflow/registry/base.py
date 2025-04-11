"""Base registry system for Haive components.

This module provides the fundamental registry system that all specific registries inherit from.
It handles registration, discovery, database persistence, and retrieval of components.
"""

from typing import Dict, Any, Type, Callable, Optional, List, Union, TypeVar, Generic, Set
import importlib
import inspect
import logging
import pkgutil
import traceback
import os
import sys
import json
import time
import hashlib
from datetime import datetime
from pathlib import Path
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field

# Set up logging
logger = logging.getLogger(__name__)

# Type variable for registries
T = TypeVar('T')

# Try to import the Supabase client
try:
    from src.haive.dataflow.supabase.base import get_supabase_client
    SUPABASE_AVAILABLE = True
    logger.info("Supabase client available for registry persistence")
except ImportError:
    SUPABASE_AVAILABLE = False
    logger.info("Supabase client not available, using in-memory storage only")


class RegistryItem(BaseModel):
    """Base model for registry items with metadata."""
    name: str
    class_name: str
    module_path: str
    class_ref: Optional[Any] = None
    item_type: str = "component"
    description: str = ""
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Registry(Generic[T]):
    """Base class for component registries.
    
    This class provides the foundation for registering and retrieving
    components in a type-safe way with added features like:
    - Automatic component discovery
    - Metadata tracking
    - Supabase integration
    - Caching
    
    Attributes:
        entries (Dict[str, RegistryItem]): Registry entries
        _instance (Registry): Singleton instance
        _discovered (bool): Whether auto-discovery has run
        _supabase_client: Supabase client for persistence
    """
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one registry exists."""
        if cls._instance is None:
            cls._instance = super(Registry, cls).__new__(cls)
            cls._instance.entries = {}
            cls._instance._discovered = False
            cls._instance._disabled_discovery = False
            cls._instance._supabase_client = None
            
            # Try to set up Supabase if available
            if SUPABASE_AVAILABLE:
                cls._instance._setup_supabase()
                
        return cls._instance
        
    def _setup_supabase(self):
        """Set up the Supabase client."""
        try:
            self._supabase_client = get_supabase_client()
            logger.info("Connected to Supabase for registry persistence")
        except Exception as e:
            logger.warning(f"Supabase setup error: {e}")
            self._supabase_client = None
    
    def register(self, 
                name: Optional[str] = None, 
                item_type: str = "component",
                **metadata) -> Callable[[Type[T]], Type[T]]:
        """Register a component in the registry.
        
        Args:
            name: Optional custom name (defaults to class name in lowercase)
            item_type: Type of item (e.g., "game", "agent", "component", "tool", "toolkit")
            **metadata: Additional metadata to store with the registration
            
        Returns:
            Decorator function that registers the component
            
        Example:
            @registry.register(name="custom_name", author="John")
            class MyComponent:
                ...
        """
        def decorator(cls: Type[T]) -> Type[T]:
            # Determine the name to use
            item_name = name or cls.__name__.lower()
            
            # Remove common suffixes
            for suffix in ["game", "agent", "config", "engine", "tool", "toolkit"]:
                if item_name.endswith(suffix) and len(item_name) > len(suffix):
                    item_name = item_name[:-len(suffix)]
            
            # Create registry item
            registry_item = RegistryItem(
                name=item_name,
                class_name=cls.__name__,
                module_path=cls.__module__,
                class_ref=cls,
                item_type=item_type,
                description=cls.__doc__ or "",
                metadata=metadata
            )
            
            # Register item
            self.entries[item_name] = registry_item
            
            # Register in Supabase if available
            if self._supabase_client is not None:
                try:
                    self._register_in_supabase(registry_item)
                except Exception as e:
                    logger.warning(f"Failed to register {item_name} in Supabase: {e}")
            
            logger.info(f"Registered {item_type} {item_name} ({cls.__name__}) in {self.__class__.__name__}")
            
            return cls
        
        return decorator
    
    def _register_in_supabase(self, item: RegistryItem) -> None:
        """Register an item in Supabase."""
        if self._supabase_client is None:
            return
            
        try:
            # Convert class_ref to None for serialization and prepare data
            item_dict = item.model_dump(exclude={"class_ref"})
            
            # Convert datetime to string
            item_dict["timestamp"] = item_dict["timestamp"].isoformat()
            
            # Convert metadata to JSON string
            item_dict["metadata"] = json.dumps(item_dict["metadata"])
            
            # Upsert the item in Supabase
            table_name = f"{item.item_type}_registry"
            self._supabase_client.table(table_name).upsert(item_dict).execute()
                
        except Exception as e:
            logger.error(f"Error registering {item.name} in Supabase: {e}")
            logger.debug(traceback.format_exc())
    
    def get(self, name: str, load_if_missing: bool = True) -> Optional[Type[T]]:
        """Get a component class by name.
        
        Args:
            name: Name of the component to retrieve
            load_if_missing: Whether to try loading the class if not already loaded
            
        Returns:
            Component class if found, None otherwise
        """
        # Normalize name
        name = name.lower()
        
        # Check if we need to discover components
        if not self._discovered and not self._disabled_discovery:
            self.discover_components()
        
        # Try to get from registry
        item = self.entries.get(name)
        if item and item.class_ref:
            return item.class_ref
            
        # If we have metadata but no class, try loading
        if item and load_if_missing:
            try:
                module = importlib.import_module(item.module_path)
                cls = getattr(module, item.class_name)
                
                # Update the registry with the loaded class
                item.class_ref = cls
                return cls
            except (ImportError, AttributeError) as e:
                logger.error(f"Error loading {name}: {e}")
                return None
                
        # Try loading from Supabase
        if self._supabase_client is not None and load_if_missing:
            try:
                table_name = f"{self.get_item_type()}_registry"
                response = self._supabase_client.table(table_name).select("*").eq("name", name).execute()
                
                if response.data and len(response.data) > 0:
                    row = response.data[0]
                    try:
                        # Load the class
                        module = importlib.import_module(row["module_path"])
                        cls = getattr(module, row["class_name"])
                        
                        # Create registry item
                        item = RegistryItem(
                            name=row["name"],
                            class_name=row["class_name"],
                            module_path=row["module_path"],
                            class_ref=cls,
                            item_type=row["item_type"],
                            description=row["description"],
                            metadata=json.loads(row["metadata"]) if row["metadata"] else {}
                        )
                        
                        # Register item
                        self.entries[name] = item
                        
                        return cls
                    except (ImportError, AttributeError) as e:
                        logger.error(f"Error loading {name} from Supabase: {e}")
            except Exception as e:
                logger.error(f"Supabase error retrieving {name}: {e}")
        
        return None
    
    def create(self, name: str, *args, **kwargs) -> Optional[T]:
        """Create an instance of a component.
        
        Args:
            name: Name of the component to create
            *args: Positional arguments for the constructor
            **kwargs: Keyword arguments for the constructor
            
        Returns:
            Instance of the component if found, None otherwise
        """
        cls = self.get(name)
        if cls:
            try:
                return cls(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error creating {name}: {e}")
                logger.debug(traceback.format_exc())
                return None
        return None
    
    def get_metadata(self, name: str) -> Dict[str, Any]:
        """Get metadata for a registry item.
        
        Args:
            name: Name of the item
            
        Returns:
            Dictionary of metadata if found, empty dict otherwise
        """
        # Normalize name
        name = name.lower()
        
        # Check if we need to discover components
        if not self._discovered and not self._disabled_discovery:
            self.discover_components()
        
        # Try to get from registry
        item = self.entries.get(name)
        if item:
            return {
                "name": item.name,
                "class_name": item.class_name,
                "module_path": item.module_path,
                "item_type": item.item_type,
                "description": item.description,
                **item.metadata
            }
        
        # Try loading from Supabase
        if self._supabase_client is not None:
            try:
                table_name = f"{self.get_item_type()}_registry"
                response = self._supabase_client.table(table_name).select("*").eq("name", name).execute()
                
                if response.data and len(response.data) > 0:
                    row = response.data[0]
                    return {
                        "name": row["name"],
                        "class_name": row["class_name"],
                        "module_path": row["module_path"],
                        "item_type": row["item_type"],
                        "description": row["description"],
                        **(json.loads(row["metadata"]) if row["metadata"] else {})
                    }
            except Exception as e:
                logger.error(f"Supabase error retrieving metadata for {name}: {e}")
        
        return {}
    
    def list_items(self, item_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all registered items, optionally filtered by type.
        
        Args:
            item_type: Optional type filter
            
        Returns:
            List of item metadata dictionaries
        """
        # Check if we need to discover components
        if not self._discovered and not self._disabled_discovery:
            self.discover_components()
        
        # Set default item_type if none provided
        if item_type is None:
            item_type = self.get_item_type()
        
        # Filter items by type if needed
        items = []
        for name, item in self.entries.items():
            if item_type is None or item.item_type == item_type:
                items.append({
                    "name": item.name,
                    "class_name": item.class_name,
                    "module_path": item.module_path,
                    "item_type": item.item_type,
                    "description": item.description,
                    **item.metadata
                })
        
        # Try to load additional items from Supabase
        if self._supabase_client is not None:
            try:
                table_name = f"{item_type}_registry"
                response = self._supabase_client.table(table_name).select("*").execute()
                
                if response.data:
                    for row in response.data:
                        # Skip items we already have
                        if any(item["name"] == row["name"] for item in items):
                            continue
                            
                        items.append({
                            "name": row["name"],
                            "class_name": row["class_name"],
                            "module_path": row["module_path"],
                            "item_type": row["item_type"],
                            "description": row["description"],
                            **(json.loads(row["metadata"]) if row["metadata"] else {})
                        })
            except Exception as e:
                logger.error(f"Supabase error retrieving items: {e}")
        
        return items
    
    def list_names(self, item_type: Optional[str] = None) -> List[str]:
        """List all registered item names, optionally filtered by type.
        
        Args:
            item_type: Optional type filter
            
        Returns:
            List of item names
        """
        items = self.list_items(item_type)
        return [item["name"] for item in items]
    
    def discover_components(self, search_paths: Optional[List[str]] = None) -> None:
        """Discover components by scanning package paths.
        
        Args:
            search_paths: Optional list of package paths to search
        """
        if self._disabled_discovery:
            logger.info("Component discovery is disabled")
            return
            
        if self._discovered:
            logger.debug("Components already discovered")
            return
            
        start_time = datetime.now()
        logger.info(f"=== Starting component discovery at {start_time.strftime('%Y-%m-%d %H:%M:%S')} ===")
        
        # Default search paths if none provided
        if not search_paths:
            search_paths = self.get_default_search_paths()
        
        logger.info(f"Search paths: {search_paths}")
        
        successfully_loaded = []
        failed_packages = []
        
        for package_path in search_paths:
            logger.info(f"Searching for components in {package_path}...")
            try:
                package = importlib.import_module(package_path)
                logger.debug(f"Package loaded: {package.__name__} from {getattr(package, '__file__', 'unknown location')}")
                
                # Get the package path
                pkg_path = getattr(package, '__path__', [None])[0]
                if pkg_path:
                    logger.debug(f"Package directory: {pkg_path}")
                    logger.debug(f"Directory contents: {os.listdir(pkg_path) if os.path.exists(pkg_path) else 'Not available'}")
                
                for _, name, is_pkg in pkgutil.iter_modules(package.__path__, package.__name__ + '.'):
                    logger.debug(f"Found module/package: {name} (is_package={is_pkg})")
                    
                    if is_pkg:
                        # Recursively check subpackages
                        logger.debug(f"Recursively checking subpackage: {name}")
                        try:
                            self.discover_components([name])
                        except Exception as e:
                            failed_packages.append((name, str(e)))
                            logger.warning(f"Error discovering components in {name}: {e}")
                            logger.debug(f"Traceback for {name}: {traceback.format_exc()}")
                    else:
                        try:
                            logger.debug(f"Importing module: {name}")
                            module = importlib.import_module(name)
                            logger.debug(f"Module loaded: {module.__name__} from {getattr(module, '__file__', 'unknown location')}")
                            
                            # Process the module for components
                            self._process_module(module)
                            successfully_loaded.append(name)
                            
                        except (ImportError, AttributeError) as e:
                            failed_packages.append((name, str(e)))
                            logger.debug(f"Error importing module {name}: {e}")
                            logger.debug(f"Traceback for {name}: {traceback.format_exc()}")
            except ImportError as e:
                failed_packages.append((package_path, str(e)))
                logger.warning(f"Could not import package {package_path}: {e}")
                logger.debug(f"Traceback for {package_path}: {traceback.format_exc()}")
        
        # Mark as discovered
        self._discovered = True
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Log summary
        logger.info("=== Component Discovery Results ===")
        logger.info(f"Duration: {duration:.2f} seconds")
        logger.info(f"Discovered: {len(self.entries)} items")
        logger.info(f"Successfully loaded modules: {len(successfully_loaded)}")
        logger.info(f"Failed packages: {len(failed_packages)}")
        
        if failed_packages:
            logger.debug("Failed packages:")
            for package_name, error in failed_packages:
                logger.debug(f"  ✗ {package_name}: {error}")
        
        logger.info(f"=== Component discovery completed at {end_time.strftime('%Y-%m-%d %H:%M:%S')} ===")
    
    def get_default_search_paths(self) -> List[str]:
        """Get default search paths for component discovery.
        
        This method should be overridden by subclasses to provide
        specific search paths for their component types.
        
        Returns:
            List of package paths to search
        """
        return []
    
    def _process_module(self, module) -> None:
        """Process a module for components to register.
        
        This method should be overridden by subclasses to provide
        specific processing logic for their component types.
        
        Args:
            module: Module to process
        """
        pass
    
    def get_item_type(self) -> str:
        """Get the default item type for this registry.
        
        This method should be overridden by subclasses to provide
        the default item type for their registry.
        
        Returns:
            String representing the default item type
        """
        return "component"


# Simplified access to registry operations
def register(registry: Registry, name: Optional[str] = None, **kwargs):
    """Register a component in a registry."""
    return registry.register(name, **kwargs)

def get(registry: Registry, name: str):
    """Get a component from a registry."""
    return registry.get(name)

def create(registry: Registry, name: str, *args, **kwargs):
    """Create a component instance from a registry."""
    return registry.create(name, *args, **kwargs)
