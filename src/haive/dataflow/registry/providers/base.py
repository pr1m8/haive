"""
Base provider class for the Haive Registry System.

This module defines the base provider class that all specific
entity providers inherit from.
"""

import logging
import importlib
import inspect
import os
import pkgutil
import traceback
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Set, Tuple, Type, Union
from datetime import datetime

# Import models
from src.haive.dataflow.registry.models import EntityType, ConfigType, DependencyType, ImportStatus
from src.haive.dataflow.registry.core import registry_system

# Set up logging
from src.haive.dataflow.registry.utils.logging import setup_discovery_logger
logger = setup_discovery_logger("providers")


class EntityProvider(ABC):
    """
    Base class for entity providers.
    
    Entity providers are responsible for discovering, registering, and managing
    specific types of entities in the registry system.
    """
    
    def __init__(self, entity_type: EntityType):
        """
        Initialize the entity provider.
        
        Args:
            entity_type: Type of entity this provider handles
        """
        self.entity_type = entity_type
        
    @abstractmethod
    def discover(self, module_paths: Optional[List[str]] = None) -> List[str]:
        """
        Discover and register entities.
        
        Args:
            module_paths: Optional list of module paths to search
            
        Returns:
            List of registered entity IDs
        """
        pass
    
    @abstractmethod
    def get_default_search_paths(self) -> List[str]:
        """
        Get default search paths for entity discovery.
        
        Returns:
            List of package paths to search
        """
        pass
    
    def discover_modules(self, base_path: str) -> List[str]:
        """
        Discover all modules under a base path.
        
        Args:
            base_path: Base module path
            
        Returns:
            List of discovered module paths
        """
        discovered_modules = []
        try:
            # Import the base module
            base_module = importlib.import_module(base_path)
            
            # Get the base module's file path
            if hasattr(base_module, "__path__"):
                base_dir = base_module.__path__[0]
            elif hasattr(base_module, "__file__"):
                base_dir = os.path.dirname(base_module.__file__)
            else:
                logger.warning(f"Could not determine path for {base_path}")
                return []
            
            # Walk through the package
            for loader, module_name, is_pkg in pkgutil.walk_packages([base_dir]):
                full_module_name = f"{base_path}.{module_name}"
                discovered_modules.append(full_module_name)
                
                # If it's a package, recursively discover submodules
                if is_pkg:
                    sub_modules = self.discover_modules(full_module_name)
                    discovered_modules.extend(sub_modules)
            
            return discovered_modules
        
        except ImportError as e:
            logger.error(f"Error importing base module {base_path}: {e}")
            return []
        except Exception as e:
            logger.error(f"Error discovering modules in {base_path}: {e}")
            return []
    
    def is_pydantic_model(self, obj: Any) -> bool:
        """
        Check if an object is a Pydantic model.
        
        Args:
            obj: Object to check
            
        Returns:
            True if it's a Pydantic model, False otherwise
        """
        try:
            from pydantic import BaseModel
            return inspect.isclass(obj) and issubclass(obj, BaseModel)
        except (ImportError, TypeError):
            return False
    
    def add_environment_vars(self, registry_id: str, env_vars: Dict[str, bool]) -> None:
        """
        Add environment variables to a registry entity.
        
        Args:
            registry_id: Registry entity ID
            env_vars: Dictionary mapping environment variable names to required flag
        """
        for env_name, is_required in env_vars.items():
            registry_system.add_environment_var(
                registry_id=registry_id,
                env_name=env_name,
                is_required=is_required
            )
    
    def add_dependency(self, registry_id: str, dependent_id: str, dependency_type: DependencyType) -> None:
        """
        Add a dependency between registry entities.
        
        Args:
            registry_id: ID of the entity that depends on another
            dependent_id: ID of the entity being depended on
            dependency_type: Type of dependency
        """
        registry_system.add_dependency(
            registry_id=registry_id,
            dependent_id=dependent_id,
            dependency_type=dependency_type
        )
    
    def add_configuration(self, registry_id: str, config_type: ConfigType, config_data: Any) -> None:
        """
        Add a configuration to a registry entity.
        
        Args:
            registry_id: Registry entity ID
            config_type: Type of configuration
            config_data: Configuration data
        """
        registry_system.add_configuration(
            registry_id=registry_id,
            config_type=config_type,
            config_data=config_data
        )
    
    def add_import_log(
        self, 
        import_session: str,
        entity_name: str,
        status: ImportStatus,
        message: Optional[str] = None,
        traceback_str: Optional[str] = None
    ) -> None:
        """
        Add an import log entry.
        
        Args:
            import_session: Import session identifier
            entity_name: Name of the entity being imported
            status: Import status
            message: Optional message
            traceback_str: Optional traceback string
        """
        registry_system.add_import_log(
            import_session=import_session,
            entity_name=entity_name,
            entity_type=self.entity_type,
            status=status,
            message=message,
            traceback_str=traceback_str
        )