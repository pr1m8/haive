"""
Agent provider for the Haive Registry System.

This module implements the agent provider that handles discovery and registration
of agent components.
"""

import inspect
import uuid
import traceback
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple, Type, Union

# Import provider base class
from src.haive.dataflow.registry.providers.base import EntityProvider

# Import models
from src.haive.dataflow.registry.models import EntityType, ConfigType, DependencyType, ImportStatus
from src.haive.dataflow.registry.core import registry_system
from src.haive.dataflow.registry.serialization import serialize_object

# Set up logging
from src.haive.dataflow.registry.utils.logging import setup_discovery_logger
logger = setup_discovery_logger("agents")


class AgentProvider(EntityProvider):
    """
    Provider for agent components.
    
    This provider handles discovery and registration of agent configurations,
    including their state schemas, engines, and other components.
    """
    
    def __init__(self):
        """Initialize the agent provider."""
        super().__init__(EntityType.AGENT)
    
    def get_default_search_paths(self) -> List[str]:
        """
        Get default search paths for agent discovery.
        
        Returns:
            List of package paths to search
        """
        return ["src.haive.agents"]
    
    def discover(self, module_paths: Optional[List[str]] = None) -> List[str]:
        """
        Discover and register agents.
        
        Args:
            module_paths: Optional list of module paths to search
            
        Returns:
            List of registered agent IDs
        """
        # Use default module paths if none provided
        if module_paths is None:
            module_paths = self.get_default_search_paths()
        
        registered_ids = []
        import_session = str(uuid.uuid4())
        logger.info(f"Starting agent discovery with session {import_session}")
        
        for base_path in module_paths:
            logger.info(f"Discovering agents in {base_path}")
            
            # Discover all modules
            modules = self.discover_modules(base_path)
            for module_name in modules:
                try:
                    # Import the module
                    module = __import__(module_name, fromlist=["*"])
                    
                    # Look for classes that might be agent configs
                    for name, obj in inspect.getmembers(module):
                        # Skip if it's not a class
                        if not inspect.isclass(obj):
                            continue
                        
                        # Check if it's an agent config
                        is_agent_config = False
                        
                        # Check class name and inheritance
                        if name.endswith("Config") or name.endswith("AgentConfig"):
                            # Check inheritance - look for AgentConfig in mro
                            for base in obj.__mro__:
                                if base.__name__ in ["AgentConfig"]:
                                    is_agent_config = True
                                    break
                        
                        # Check for specific attributes that suggest it's an agent config
                        if hasattr(obj, "build_agent") or hasattr(obj, "agent_class"):
                            is_agent_config = True
                        
                        # Register if it's an agent config
                        if is_agent_config:
                            logger.info(f"Found agent config: {name} in {module_name}")
                            
                            # Try to instantiate the config
                            try:
                                instance = None
                                if hasattr(obj, "default") and callable(obj.default):
                                    instance = obj.default()
                                else:
                                    # Try to instantiate with no args
                                    instance = obj()
                                
                                # Get a better name
                                agent_name = instance.name if hasattr(instance, "name") else name
                                
                                # Register the agent
                                agent_id = registry_system.register_entity(
                                    name=agent_name,
                                    entity_type=EntityType.AGENT,
                                    description=instance.__doc__ if instance.__doc__ else f"{agent_name} agent configuration",
                                    module_path=module_name,
                                    class_name=name,
                                    metadata={
                                        "discovered_at": datetime.now().isoformat(),
                                        "type_hint": "agent_config"
                                    }
                                )
                                
                                # Register configurations if available
                                try:
                                    # State schema
                                    if hasattr(instance, "state_schema"):
                                        self.add_configuration(
                                            registry_id=agent_id,
                                            config_type=ConfigType.STATE_SCHEMA,
                                            config_data=instance.state_schema
                                        )
                                    
                                    # Input schema
                                    if hasattr(instance, "input_schema"):
                                        self.add_configuration(
                                            registry_id=agent_id,
                                            config_type=ConfigType.INPUT_SCHEMA,
                                            config_data=instance.input_schema
                                        )
                                    
                                    # Output schema
                                    if hasattr(instance, "output_schema"):
                                        self.add_configuration(
                                            registry_id=agent_id,
                                            config_type=ConfigType.OUTPUT_SCHEMA,
                                            config_data=instance.output_schema
                                        )
                                    
                                    # Engine
                                    if hasattr(instance, "engine"):
                                        # Register the engine
                                        if hasattr(instance.engine, "name"):
                                            engine_name = instance.engine.name
                                        else:
                                            engine_name = f"{agent_name}_engine"
                                        
                                        # Get the engine type
                                        if hasattr(instance.engine, "llm_config"):
                                            engine_type = "aug_llm"
                                        else:
                                            engine_type = "llm_config"
                                        
                                        # Register the engine
                                        engine_id = registry_system.register_entity(
                                            name=engine_name,
                                            entity_type=EntityType.ENGINE,
                                            description=f"Engine for {agent_name}",
                                            module_path=module_name,
                                            class_name=instance.engine.__class__.__name__,
                                            metadata={
                                                "discovered_at": datetime.now().isoformat(),
                                                "type_hint": engine_type
                                            }
                                        )
                                        
                                        # Add dependency
                                        self.add_dependency(
                                            registry_id=agent_id,
                                            dependent_id=engine_id,
                                            dependency_type=DependencyType.REQUIRES
                                        )
                                        
                                        # Add configuration
                                        self.add_configuration(
                                            registry_id=agent_id,
                                            config_type=ConfigType.ENGINE,
                                            config_data=instance.engine
                                        )
                                        
                                        # If it's an AugLLMConfig, extract its components
                                        if engine_type == "aug_llm":
                                            # Extract prompt template
                                            if hasattr(instance.engine, "prompt_template"):
                                                prompt_id = registry_system.register_entity(
                                                    name=f"{agent_name}_prompt",
                                                    entity_type=EntityType.PROMPT_TEMPLATE,
                                                    description=f"Prompt for {agent_name}",
                                                    module_path=module_name,
                                                    class_name=instance.engine.prompt_template.__class__.__name__,
                                                    metadata={
                                                        "discovered_at": datetime.now().isoformat(),
                                                        "type_hint": "prompt_template"
                                                    }
                                                )
                                                
                                                # Add dependency
                                                self.add_dependency(
                                                    registry_id=engine_id,
                                                    dependent_id=prompt_id,
                                                    dependency_type=DependencyType.REQUIRES
                                                )
                                                
                                                # Add configuration
                                                self.add_configuration(
                                                    registry_id=engine_id,
                                                    config_type=ConfigType.PROMPT,
                                                    config_data=instance.engine.prompt_template
                                                )
                                            
                                            # Extract structured output model
                                            if hasattr(instance.engine, "structured_output_model"):
                                                output_id = registry_system.register_entity(
                                                    name=f"{agent_name}_output_model",
                                                    entity_type=EntityType.STATE_SCHEMA,
                                                    description=f"Output model for {agent_name}",
                                                    module_path=module_name,
                                                    class_name=instance.engine.structured_output_model.__name__,
                                                    metadata={
                                                        "discovered_at": datetime.now().isoformat(),
                                                        "type_hint": "structured_output_model"
                                                    }
                                                )
                                                
                                                # Add dependency
                                                self.add_dependency(
                                                    registry_id=engine_id,
                                                    dependent_id=output_id,
                                                    dependency_type=DependencyType.REQUIRES
                                                )
                                                
                                                # Add configuration
                                                self.add_configuration(
                                                    registry_id=engine_id,
                                                    config_type=ConfigType.OUTPUT_SCHEMA,
                                                    config_data=instance.engine.structured_output_model
                                                )
                                            
                                            # Extract tools
                                            if hasattr(instance.engine, "tools") and instance.engine.tools:
                                                # Register the tools
                                                tool_ids = []
                                                for i, tool in enumerate(instance.engine.tools):
                                                    if hasattr(tool, "name"):
                                                        tool_name = tool.name
                                                    else:
                                                        tool_name = f"{agent_name}_tool_{i}"
                                                    
                                                    # Register the tool
                                                    tool_id = registry_system.register_entity(
                                                        name=tool_name,
                                                        entity_type=EntityType.TOOL,
                                                        description=getattr(tool, "description", f"Tool for {agent_name}"),
                                                        module_path=module_name,
                                                        class_name=tool.__class__.__name__,
                                                        metadata={
                                                            "discovered_at": datetime.now().isoformat(),
                                                            "type_hint": "tool"
                                                        }
                                                    )
                                                    
                                                    tool_ids.append(tool_id)
                                                
                                                # Add dependencies
                                                for tool_id in tool_ids:
                                                    self.add_dependency(
                                                        registry_id=engine_id,
                                                        dependent_id=tool_id,
                                                        dependency_type=DependencyType.USES
                                                    )
                                                
                                                # Add configuration
                                                self.add_configuration(
                                                    registry_id=engine_id,
                                                    config_type=ConfigType.TOOLS,
                                                    config_data=instance.engine.tools
                                                )
                                    
                                    # Additional engines
                                    if hasattr(instance, "engines") and instance.engines:
                                        for engine_name, engine in instance.engines.items():
                                            # Register the engine
                                            engine_id = registry_system.register_entity(
                                                name=engine_name,
                                                entity_type=EntityType.ENGINE,
                                                description=f"Engine {engine_name} for {agent_name}",
                                                module_path=module_name,
                                                class_name=engine.__class__.__name__,
                                                metadata={
                                                    "discovered_at": datetime.now().isoformat(),
                                                    "type_hint": "engine"
                                                }
                                            )
                                            
                                            # Add dependency
                                            self.add_dependency(
                                                registry_id=agent_id,
                                                dependent_id=engine_id,
                                                dependency_type=DependencyType.USES
                                            )
                                    
                                    # Persistence configuration
                                    if hasattr(instance, "persistence"):
                                        self.add_configuration(
                                            registry_id=agent_id,
                                            config_type=ConfigType.PERSISTENCE,
                                            config_data=instance.persistence
                                        )
                                    
                                    # Check for agent settings
                                    if hasattr(instance, "agent_settings") and instance.agent_settings:
                                        for key, value in instance.agent_settings.items():
                                            registry_system.update_entity(
                                                registry_id=agent_id,
                                                metadata={key: value}
                                            )
                                
                                except Exception as e:
                                    err_tb = traceback.format_exc()
                                    logger.error(f"Error registering configurations for {agent_name}: {e}\n{err_tb}")
                                
                                # Add to registered IDs
                                registered_ids.append(agent_id)
                                
                                # Log success
                                self.add_import_log(
                                    import_session=import_session,
                                    entity_name=agent_name,
                                    status=ImportStatus.SUCCESS,
                                    message=f"Successfully registered agent {agent_name} from {module_name}"
                                )
                                
                            except Exception as e:
                                # Log error
                                err_tb = traceback.format_exc()
                                logger.error(f"Error registering agent {name} from {module_name}: {e}\n{err_tb}")
                                
                                self.add_import_log(
                                    import_session=import_session,
                                    entity_name=name,
                                    status=ImportStatus.FAILURE,
                                    message=f"Failed to register agent {name} from {module_name}: {e}",
                                    traceback_str=err_tb
                                )
                
                except Exception as e:
                    err_tb = traceback.format_exc()
                    logger.error(f"Error processing module {module_name}: {e}\n{err_tb}")
        
        logger.info(f"Discovered {len(registered_ids)} agents")
        return registered_ids


# Create singleton instance
agent_provider = AgentProvider()