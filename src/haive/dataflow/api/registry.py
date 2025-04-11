# src/haive/api/registry.py
import importlib
import inspect
import logging
import pkgutil
import traceback
from typing import Dict, Type, List, Optional, Any, Tuple
import sys
import os
from datetime import datetime
from src.haive.core.engine.agent.agent import Agent, AgentConfig, AGENT_REGISTRY

logger = logging.getLogger(__name__)

class AgentRegistryService:
    """Service that manages agent registration and discovery."""
    
    # Update AgentRegistryService initialization to include database

    def __init__(self):
        self.agent_configs: Dict[str, Dict[str, Any]] = {}
        self.instantiated_agents: Dict[str, Agent] = {}
        self.agent_errors: Dict[str, str] = {}  # Track errors for agents that failed to load
        self.default_persistence_type = "postgres"  # Default value
        self.db_connection = None
        
        # Try to load persistence types
        try:
            from src.haive.core.engine.agent.persistence.types import CheckpointerType
            self.default_persistence_type = CheckpointerType.postgres
        except ImportError:
            logger.warning("Could not import CheckpointerType, using default persistence type")
        
        # Try to set up database connection
        try:
            self._setup_database()
        except Exception as e:
            logger.warning(f"Could not set up database connection: {e}")

    def _setup_database(self):
        """Set up the database connection and schema."""
        from src.api.api.db import DatabaseManager
        
        # Get database parameters from environment or config
        try:
            import os
            db_params = {
                'dbname': os.getenv('DB_NAME', 'postgres'),
                'user': os.getenv('DB_USER', 'postgres'),
                'password': os.getenv('DB_PASSWORD', 'postgres'),
                'host': os.getenv('DB_HOST', 'localhost'),
                'port': os.getenv('DB_PORT', '5432')
            }
            
            self.db = DatabaseManager(db_params)
            if self.db.connect():
                # Create schema and tables
                if self.db.create_schema() and self.db.create_tables():
                    logger.info("Database setup completed successfully")
                    self.db_connection = True
                else:
                    logger.warning("Failed to create schema or tables")
                    self.db_connection = False
            else:
                logger.warning("Failed to connect to database")
                self.db_connection = False
        except Exception as e:
            logger.warning(f"Database setup error: {e}")
            self.db_connection = False

    # Add method to register agent in database
    def _register_agent_in_db(self, name: str, config_class: Type[AgentConfig], agent_type: str):
        """Register an agent configuration in the database."""
        if hasattr(self, 'db') and self.db_connection:
            try:
                self.db.register_agent_config(name, config_class, agent_type)
            except Exception as e:
                logger.warning(f"Failed to register agent {name} in database: {e}")
    
    
    def discover_agents(self, search_paths: List[str] = ["src.haive.agents", "src.haive.games", "src.haive.tak"]) -> None:
        """
        Automatically discover and register all agent configurations from multiple paths.
        
        Args:
            search_paths: List of package paths to search for agents
        """
        start_time = datetime.now()
        logger.info(f"=== Starting agent discovery at {start_time.strftime('%Y-%m-%d %H:%M:%S')} ===")
        logger.info(f"Search paths: {search_paths}")
        logger.info(f"Python path: {sys.path}")
        
        successfully_loaded = []
        failed_packages = []
        
        for package_path in search_paths:
            logger.info(f"Searching for agents in {package_path}...")
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
                            self.discover_agents([name])
                        except Exception as e:
                            failed_packages.append((name, str(e)))
                            logger.warning(f"Error discovering agents in {name}: {e}")
                            logger.debug(f"Traceback for {name}: {traceback.format_exc()}")
                    else:
                        try:
                            logger.debug(f"Importing module: {name}")
                            module = importlib.import_module(name)
                            logger.debug(f"Module loaded: {module.__name__} from {getattr(module, '__file__', 'unknown location')}")
                            
                            # Find all AgentConfig subclasses in the module
                            class_count = 0
                            agent_count = 0
                            
                            for class_name, obj in inspect.getmembers(module, inspect.isclass):
                                class_count += 1
                                try:
                                    if issubclass(obj, AgentConfig) and obj != AgentConfig:
                                        agent_count += 1
                                        agent_name = getattr(obj, "name", None) or class_name.replace("Config", "")
                                        logger.debug(f"Found AgentConfig subclass: {class_name} → {agent_name}")
                                        
                                        # Check if it's a game agent
                                        is_game = 'game' in module.__name__.lower() or hasattr(obj, 'is_game') and obj.is_game
                                        agent_type = "game" if is_game else "agent"
                                        
                                        self.register_agent_config(agent_name, obj, agent_type)
                                        successfully_loaded.append((agent_name, agent_type))
                                except (TypeError, Exception) as class_err:
                                    logger.debug(f"Error checking class {class_name}: {class_err}")
                            
                            logger.debug(f"Module {name} had {class_count} classes, {agent_count} agents")
                            
                        except (ImportError, AttributeError) as e:
                            failed_packages.append((name, str(e)))
                            logger.debug(f"Error importing module {name}: {e}")
                            logger.debug(f"Traceback for {name}: {traceback.format_exc()}")
            except ImportError as e:
                failed_packages.append((package_path, str(e)))
                logger.warning(f"Could not import package {package_path}: {e}")
                logger.debug(f"Traceback for {package_path}: {traceback.format_exc()}")
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Log summary in test-like format
        logger.info("=== Agent Discovery Results ===")
        logger.info(f"Duration: {duration:.2f} seconds")
        logger.info(f"Discovered: {len(successfully_loaded)} agents")
        logger.info(f"Failed packages: {len(failed_packages)}")
        
        if successfully_loaded:
            logger.info("Successfully loaded agents:")
            for agent_name, agent_type in successfully_loaded:
                logger.info(f"  ✓ {agent_name} ({agent_type})")
        
        if failed_packages:
            logger.warning("Failed packages:")
            for package_name, error in failed_packages:
                logger.warning(f"  ✗ {package_name}: {error}")
        
        logger.info(f"=== Agent discovery completed at {end_time.strftime('%Y-%m-%d %H:%M:%S')} ===")

    
    def register_agent_config(self, name: str, config_class: Type[AgentConfig], agent_type: str = "agent") -> None:
        """
        Register an agent configuration class.
        
        Args:
            name: Name of the agent
            config_class: Agent configuration class
            agent_type: Type of agent (e.g., 'agent', 'game')
        """
        try:
            self.agent_configs[name] = {
                'class': config_class,
                'type': agent_type
            }
            logger.info(f"Registered agent configuration: {name} (type: {agent_type})")
            
            # If we have database connectivity, also register in the database
            if hasattr(self, 'db_connection') and self.db_connection:
                self._register_agent_in_db(name, config_class, agent_type)
            
            # Clear any previous errors for this agent
            if name in self.agent_errors:
                del self.agent_errors[name]
        except Exception as e:
            error_msg = f"Error registering agent {name}: {str(e)}"
            self.agent_errors[name] = error_msg
            logger.error(error_msg)
            logger.debug(f"Traceback for registering {name}: {traceback.format_exc()}")
    
    # Update get_agent_config to handle the new structure
    def get_agent_config(self, name: str) -> Optional[Type[AgentConfig]]:
        """Get agent configuration class by name."""
        agent_info = self.agent_configs.get(name)
        if agent_info:
            return agent_info['class']
        return None

    # Add method to get agent type
    def get_agent_type(self, name: str) -> Optional[str]:
        """Get agent type by name."""
        agent_info = self.agent_configs.get(name)
        if agent_info:
            return agent_info['type']
        return None
    
    def list_available_agents(self) -> List[str]:
        """List all available agent configurations."""
        return list(self.agent_configs.keys())
    
    def list_failed_agents(self) -> Dict[str, str]:
        """List agents that failed to register with their error messages."""
        return self.agent_errors
    
    def get_or_create_agent(self, 
                           name: str, 
                           thread_id: Optional[str] = None,
                           **config_kwargs) -> Tuple[Optional[Agent], Optional[str]]:
        """
        Get a previously instantiated agent or create a new one.
        Returns the agent and an error message if there was a problem.
        
        Args:
            name: Agent name
            thread_id: Optional thread ID for persistence
            **config_kwargs: Configuration parameters for agent creation
            
        Returns:
            Tuple of (agent, error_message)
        """
        # Check if agent has a known error
        if name in self.agent_errors:
            return None, self.agent_errors[name]
        
        # Create unique agent identifier if config parameters were provided
        agent_key = name
        if config_kwargs:
            # Use a simple hash of config values to create a unique key
            config_str = str(sorted([(k, str(v)) for k, v in config_kwargs.items()]))
            import hashlib
            config_hash = hashlib.md5(config_str.encode()).hexdigest()[:8]
            agent_key = f"{name}_{config_hash}"
        
        # If agent already exists, return it
        if agent_key in self.instantiated_agents:
            agent = self.instantiated_agents[agent_key]
            
            # Update thread_id in agent's config if provided
            if thread_id and hasattr(agent.config, 'runnable_config'):
                try:
                    if "configurable" not in agent.config.runnable_config:
                        agent.config.runnable_config["configurable"] = {}
                    agent.config.runnable_config["configurable"]["thread_id"] = thread_id
                except Exception as e:
                    logger.warning(f"Error updating thread_id for agent {name}: {e}")
                
            return agent, None
        
        # Get the agent config class
        config_class = self.get_agent_config(name)
        if not config_class:
            error_msg = f"No agent configuration found with name: {name}"
            logger.error(error_msg)
            return None, error_msg
        
        try:
            # Create agent config with provided parameters
            agent_config = config_class(**config_kwargs)
            
            # Set thread_id if provided
            if thread_id and hasattr(agent_config, 'runnable_config'):
                if "configurable" not in agent_config.runnable_config:
                    agent_config.runnable_config["configurable"] = {}
                agent_config.runnable_config["configurable"]["thread_id"] = thread_id
            
            # Ensure persistence is configured
            self._configure_persistence(agent_config)
            
            # Build and store the agent
            agent = agent_config.build_agent()
            if agent is None:
                raise ValueError(f"build_agent() returned None for {name}")
                
            self.instantiated_agents[agent_key] = agent
            return agent, None
        except Exception as e:
            error_msg = f"Error creating agent {name}: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg)
            return None, error_msg
    
    def _configure_persistence(self, agent_config: AgentConfig) -> None:
        """Configure persistence for an agent config if needed."""
        try:
            if not hasattr(agent_config, 'persistence') or agent_config.persistence is None:
                # Try to import the persistence module
                try:
                    from src.haive.core.engine.agent.persistence import load_checkpointer_config
                    
                    # Load the checkpointer config
                    agent_config.persistence = load_checkpointer_config(self.default_persistence_type)
                except ImportError:
                    # Fall back to memory persistence
                    from langgraph.checkpoint.memory import MemorySaver
                    agent_config.persistence = MemorySaver()
        except Exception as e:
            logger.warning(f"Error configuring persistence: {e}, using defaults")

# Singleton instance
agent_registry = AgentRegistryService()