"""
Core Registry System for Haive.

This module provides the central registry system for managing
LLM models, embeddings, and other entity types in the system.
"""

import os
import json
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Type, Union, Set
from enum import Enum, auto

# Set up logging
logger = logging.getLogger(__name__)


class EntityType(str, Enum):
    """Types of entities that can be registered."""
    LLM = "llm"
    LLM_PROVIDER = "llm_provider"
    EMBEDDING = "embedding"
    EMBEDDING_PROVIDER = "embedding_provider"
    AGENT = "agent"
    TOOL = "tool"
    WORKFLOW = "workflow"
    DATA_SOURCE = "data_source"
    CUSTOM = "custom"


class ConfigType(str, Enum):
    """Types of configuration that can be associated with entities."""
    INIT = "init"
    CONNECTION = "connection"
    SCHEMA = "schema"
    WORKFLOW = "workflow"
    CUSTOM = "custom"


class DependencyType(str, Enum):
    """Types of dependencies between entities."""
    REQUIRES = "requires"
    RECOMMENDS = "recommends"
    CONFLICTS = "conflicts"
    EXTENDS = "extends"


class ImportStatus(str, Enum):
    """Status of an import operation."""
    SUCCESS = "success"
    FAILURE = "failure"
    PARTIAL = "partial"
    SKIPPED = "skipped"


class RegistrySystem:
    """
    Core registry system for managing entities.
    
    The registry system is a centralized repository for tracking and
    managing entities such as LLM models, embeddings, agents, tools, etc.
    
    It provides both in-memory storage and database persistence via Supabase.
    """
    
    def __init__(self):
        """Initialize the registry system."""
        self._entities = {}
        self._configurations = {}
        self._dependencies = {}
        self._environment_vars = {}
        self._import_logs = []
        self._supabase = None
        
        # Try to initialize Supabase client
        try:
            # Import Supabase client
            from src.haive.dataflow.db.supabase import get_supabase_client
            self._supabase = get_supabase_client()
            logger.info("Supabase connection initialized for registry system")
            
            # Initialize registry schema if needed for backwards compatibility
            self._ensure_registry_schema()
            
            # Check for provider types in the new schema
            self._ensure_provider_types()
        except Exception as e:
            logger.warning(f"Could not initialize Supabase connection: {e}")
            logger.info("Registry system running in in-memory mode only")
    
    def _ensure_registry_schema(self):
        """Ensure the registry schema is properly set up for backward compatibility."""
        try:
            # Check if the registry schema exists
            schema_check = self._supabase.query("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'registry'").execute()
            
            if not schema_check.data or len(schema_check.data) == 0:
                # Create registry schema if it doesn't exist
                self._supabase.query("CREATE SCHEMA IF NOT EXISTS registry").execute()
                logger.info("Created registry schema for backward compatibility")
            
            # Check for required tables
            tables = [
                ("registry", "items", """
                    id UUID PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    type VARCHAR(50) NOT NULL,
                    description TEXT,
                    metadata JSONB,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                """),
                ("registry", "configurations", """
                    id UUID PRIMARY KEY,
                    registry_id UUID NOT NULL,
                    config_type VARCHAR(50) NOT NULL,
                    config_data JSONB,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                """),
                ("registry", "dependencies", """
                    id UUID PRIMARY KEY,
                    registry_id UUID NOT NULL,
                    dependent_id UUID NOT NULL,
                    dependency_type VARCHAR(50) NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                """),
                ("registry", "environment_vars", """
                    id UUID PRIMARY KEY,
                    var_name VARCHAR(255) NOT NULL,
                    provider_name VARCHAR(255) NOT NULL,
                    is_required BOOLEAN DEFAULT TRUE,
                    description TEXT,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                """),
                ("registry", "import_logs", """
                    id UUID PRIMARY KEY,
                    import_session VARCHAR(100) NOT NULL,
                    entity_name VARCHAR(255) NOT NULL,
                    entity_type VARCHAR(50) NOT NULL,
                    status VARCHAR(50) NOT NULL,
                    message TEXT,
                    traceback TEXT,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                """)
            ]
            
            for schema, table_name, columns in tables:
                # Check if table exists
                table_check = self._supabase.query(f"SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = '{schema}' AND tablename = '{table_name}'").execute()
                
                if not table_check.data or len(table_check.data) == 0:
                    # Create table
                    self._supabase.query(f"CREATE TABLE IF NOT EXISTS {schema}.{table_name} ({columns})").execute()
                    logger.info(f"Created table {schema}.{table_name} for backward compatibility")
                    
        except Exception as e:
            logger.error(f"Error ensuring registry schema: {e}")
    
    def _ensure_provider_types(self):
        """Ensure the provider types exist in the models schema."""
        try:
            # Check if provider_types table exists in models schema
            table_check = self._supabase.query("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'models' AND tablename = 'provider_types'").execute()
            
            if table_check.data and len(table_check.data) > 0:
                # Check if we have the basic provider types
                from src.haive.dataflow.db.supabase import table
                
                provider_types_response = table(self._supabase, "models.provider_types").select("*").execute()
                
                if not provider_types_response.data or len(provider_types_response.data) == 0:
                    # Create default provider types
                    provider_types = [
                        {
                            "name": "llm",
                            "display_name": "Large Language Model",
                            "description": "Provider of large language models",
                            "created_at": datetime.now().isoformat()
                        },
                        {
                            "name": "embedding",
                            "display_name": "Embedding Model",
                            "description": "Provider of embedding models",
                            "created_at": datetime.now().isoformat()
                        },
                        {
                            "name": "vectorstore",
                            "display_name": "Vector Database",
                            "description": "Provider of vector databases",
                            "created_at": datetime.now().isoformat()
                        }
                    ]
                    
                    for provider_type in provider_types:
                        table(self._supabase, "models.provider_types").insert(provider_type).execute()
                        
                    logger.info("Created default provider types in models schema")
                
        except Exception as e:
            logger.warning(f"Error ensuring provider types: {e}")
    
    def register_entity(
    self,
    name: str,
    entity_type: EntityType,
    description: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> str:
        """
        Register a new entity in the registry.
        
        Args:
            name: Name of the entity
            entity_type: Type of entity
            description: Optional description
            metadata: Optional metadata dictionary
            
        Returns:
            ID of the registered entity
        """
        # Generate a unique ID
        registry_id = str(uuid.uuid4())
        
        # Prepare entity data
        entity_data = {
            "id": registry_id,
            "name": name,
            "type": entity_type.value if isinstance(entity_type, EntityType) else entity_type,
            "description": description or "",
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat()
        }
        
        # Store in local registry
        self._entities[registry_id] = entity_data
        
        # Store in Supabase if available
        if self._supabase is not None:
            try:
                from src.haive.dataflow.db.supabase import table
                
                # Convert metadata to JSON string for storage if needed
                db_entity = dict(entity_data)
                if isinstance(db_entity.get("metadata"), dict):
                    db_entity["metadata"] = json.dumps(db_entity["metadata"])
                
                # Store in the new schema location based on entity type
                success = False
                
                if entity_type == EntityType.LLM_PROVIDER or entity_type == EntityType.LLM:
                    try:
                        # Get provider type ID for LLM
                        provider_type_response = self._get_or_create_provider_type("llm", "Large Language Model")
                        
                        if provider_type_response:
                            provider_type_id = provider_type_response.get("id")
                            
                            # Store provider information in models.providers
                            provider_data = {
                                "id": registry_id,  # Use same ID for consistency
                                "type_id": provider_type_id,
                                "name": name,
                                "display_name": name.replace('_', ' ').title(),
                                "description": description or f"LLM provider: {name}",
                                "is_available": metadata.get("is_available", False) if metadata else False,
                                "created_at": entity_data["created_at"],
                                "updated_at": entity_data["created_at"]
                            }
                            
                            response = table(self._supabase, "models.providers").insert(provider_data).execute()
                            if response.data:
                                success = True
                                logger.info(f"Stored LLM provider {name} in models.providers")
                                
                                # If we have metadata from LiteLLM, automatically register an environment variable
                                if metadata and metadata.get("import_source") == "litellm":
                                    env_var_name = f"{name.upper()}_API_KEY"
                                    
                                    # Check for common substitutions
                                    if name == "openai":
                                        env_var_name = "OPENAI_API_KEY"
                                    elif name == "anthropic":
                                        env_var_name = "ANTHROPIC_API_KEY"
                                    elif name == "huggingface":
                                        env_var_name = "HUGGING_FACE_API_KEY"
                                    elif name == "together_ai":
                                        env_var_name = "TOGETHER_API_KEY"
                                    elif name == "gemini":
                                        env_var_name = "GOOGLE_GENAI_API_KEY"
                                        
                                    self._register_environment_var(
                                        var_name=env_var_name,
                                        provider_name=name,
                                        is_required=True,
                                        description=f"API key for {name.title()} provider"
                                    )
                    except Exception as e:
                        logger.warning(f"Error storing {name} in models.providers: {e}")
                        
                elif entity_type == EntityType.EMBEDDING_PROVIDER or entity_type == EntityType.EMBEDDING:
                    try:
                        # Get provider type ID for embedding
                        provider_type_response = self._get_or_create_provider_type("embedding", "Embedding Model")
                        
                        if provider_type_response:
                            provider_type_id = provider_type_response.get("id")
                            
                            # Store provider information in models.providers
                            provider_data = {
                                "id": registry_id,  # Use same ID for consistency
                                "type_id": provider_type_id,
                                "name": name,
                                "display_name": name.replace('_', ' ').title(),
                                "description": description or f"Embedding provider: {name}",
                                "is_available": metadata.get("is_available", False) if metadata else False,
                                "created_at": entity_data["created_at"],
                                "updated_at": entity_data["created_at"]
                            }
                            
                            response = table(self._supabase, "models.providers").insert(provider_data).execute()
                            if response.data:
                                success = True
                                logger.info(f"Stored embedding provider {name} in models.providers")
                                
                                # Register environment variable for API key
                                env_var_name = f"{name.upper()}_API_KEY"
                                self._register_environment_var(
                                    var_name=env_var_name,
                                    provider_name=name,
                                    is_required=True,
                                    description=f"API key for {name.title()} embedding provider"
                                )
                    except Exception as e:
                        logger.warning(f"Error storing {name} in models.providers: {e}")
                
                # If not stored in the new schema location or it failed, try config.components
                if not success:
                    try:
                        # Get or create component type
                        component_type_id = self._get_or_create_component_type(
                            entity_type.value,
                            entity_type.value.replace('_', ' ').title()
                        )
                        
                        if component_type_id:
                            component_data = {
                                "id": registry_id,
                                "component_type_id": component_type_id,
                                "external_id": registry_id,
                                "name": name,
                                "display_name": name.replace('_', ' ').title(),
                                "description": description or f"{entity_type.value}: {name}",
                                "is_available": metadata.get("is_available", False) if metadata else False,
                                "extended_metadata": db_entity["metadata"],
                                "created_at": entity_data["created_at"],
                                "updated_at": entity_data["created_at"]
                            }
                            
                            response = table(self._supabase, "config.components").insert(component_data).execute()
                            if response.data:
                                success = True
                                logger.info(f"Stored {name} in config.components")
                    except Exception as e:
                        logger.warning(f"Error storing {name} in config.components: {e}")
                
                # Fall back to the old registry.items table if all else fails
                if not success:
                    try:
                        # Check if registry schema exists
                        self._ensure_registry_schema()
                        
                        # Insert into registry.items table
                        response = table(self._supabase, "registry.items").insert(db_entity).execute()
                        if response.data:
                            success = True
                            logger.info(f"Stored {name} in legacy registry.items")
                    except Exception as e:
                        logger.error(f"Error storing entity in legacy registry.items: {e}")
                
                if not success:
                    logger.warning(f"Failed to store {name} in any location")
                
            except Exception as e:
                logger.error(f"Error storing entity in database: {e}")
            
        logger.info(f"Registered entity: {name} ({entity_type}) with ID: {registry_id}")
        return registry_id

    def _get_or_create_provider_type(self, type_name, display_name):
        """Helper method to get or create a provider type."""
        try:
            from src.haive.dataflow.db.supabase import table
            
            # Check if the provider type exists
            response = table(self._supabase, "models.provider_types").select("*").eq("name", type_name).execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            
            # If not, create it
            provider_type_data = {
                "id": str(uuid.uuid4()),
                "name": type_name,
                "display_name": display_name,
                "description": f"Provider type for {display_name}",
                "created_at": datetime.now().isoformat()
            }
            
            create_response = table(self._supabase, "models.provider_types").insert(provider_type_data).execute()
            
            if create_response.data and len(create_response.data) > 0:
                return create_response.data[0]
            
            # If table API fails, try direct SQL
            create_query = """
            INSERT INTO models.provider_types (id, name, display_name, description, created_at)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING *
            """
            
            sql_response = self._supabase.query(create_query, {
                1: provider_type_data["id"],
                2: provider_type_data["name"],
                3: provider_type_data["display_name"],
                4: provider_type_data["description"],
                5: provider_type_data["created_at"]
            }).execute()
            
            if sql_response.data and len(sql_response.data) > 0:
                return sql_response.data[0]
            
        except Exception as e:
            logger.error(f"Error getting or creating provider type {type_name}: {e}")
        
        return None

    def _get_or_create_component_type(self, type_name, display_name):
        """Helper method to get or create a component type."""
        try:
            from src.haive.dataflow.db.supabase import table
            
            # Check if the component type exists
            response = table(self._supabase, "config.component_types").select("id").eq("name", type_name).execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]["id"]
            
            # If not, create it
            component_type_data = {
                "id": str(uuid.uuid4()),
                "name": type_name,
                "display_name": display_name,
                "description": f"Component type for {display_name}",
                "created_at": datetime.now().isoformat()
            }
            
            create_response = table(self._supabase, "config.component_types").insert(component_type_data).execute()
            
            if create_response.data and len(create_response.data) > 0:
                return create_response.data[0]["id"]
            
            # If table API fails, try direct SQL
            create_query = """
            INSERT INTO config.component_types (id, name, display_name, description, created_at)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id
            """
            
            sql_response = self._supabase.query(create_query, {
                1: component_type_data["id"],
                2: component_type_data["name"],
                3: component_type_data["display_name"],
                4: component_type_data["description"],
                5: component_type_data["created_at"]
            }).execute()
            
            if sql_response.data and len(sql_response.data) > 0:
                return sql_response.data[0]["id"]
            
        except Exception as e:
            logger.error(f"Error getting or creating component type {type_name}: {e}")
        
        return None
    
    def add_configuration(
        self,
        registry_id: str,
        config_type: ConfigType,
        config_data: Any
    ) -> Optional[str]:
        """
        Add a configuration to an entity.
        
        Args:
            registry_id: ID of the registered entity
            config_type: Type of configuration
            config_data: Configuration data
            
        Returns:
            ID of the configuration or None on failure
        """
        if registry_id not in self._entities:
            logger.error(f"Entity with ID {registry_id} not found.")
            return None
        
        # Generate a unique ID for the configuration
        config_id = str(uuid.uuid4())
        
        # Prepare configuration data
        config_record = {
            "id": config_id,
            "registry_id": registry_id,
            "config_type": config_type.value if isinstance(config_type, ConfigType) else config_type,
            "config_data": config_data,
            "created_at": datetime.now().isoformat()
        }
        
        # Store in local registry
        if registry_id not in self._configurations:
            self._configurations[registry_id] = {}
        
        self._configurations[registry_id][config_id] = config_record
        
        # Store in Supabase if available
        if self._supabase is not None:
            try:
                from src.haive.dataflow.db.supabase import table
                
                # Try to serialize the data
                try:
                    from src.utils.serialization import serialize_object
                except ImportError:
                    def serialize_object(obj):
                        """Simple serialization helper."""
                        if isinstance(obj, (dict, list, str, int, float, bool, type(None))):
                            return obj
                        return str(obj)
                
                # Prepare for database storage
                db_config = dict(config_record)
                db_config["config_data"] = serialize_object(config_data)
                
                # Insert into registry.configurations table
                table(self._supabase, "registry.configurations").insert(db_config).execute()
                
            except Exception as e:
                logger.error(f"Error storing configuration in database: {e}")
        
        return config_id
    
    def add_dependency(
        self,
        registry_id: str,
        dependent_id: str,
        dependency_type: DependencyType
    ) -> Optional[str]:
        """
        Add a dependency between two entities.
        
        Args:
            registry_id: ID of the entity that depends on another
            dependent_id: ID of the entity being depended on
            dependency_type: Type of dependency
            
        Returns:
            ID of the dependency or None on failure
        """
        if registry_id not in self._entities or dependent_id not in self._entities:
            logger.error(f"Entity not found: {registry_id} or {dependent_id}")
            return None
        
        # Generate a unique ID for the dependency
        dependency_id = str(uuid.uuid4())
        
        # Prepare dependency data
        dependency_record = {
            "id": dependency_id,
            "registry_id": registry_id,
            "dependent_id": dependent_id,
            "dependency_type": dependency_type.value if isinstance(dependency_type, DependencyType) else dependency_type,
            "created_at": datetime.now().isoformat()
        }
        
        # Store in local registry
        if registry_id not in self._dependencies:
            self._dependencies[registry_id] = {}
        
        self._dependencies[registry_id][dependency_id] = dependency_record
        
        # Store in Supabase if available
        if self._supabase is not None:
            try:
                from src.haive.dataflow.db.supabase import table
                
                # Insert into registry.dependencies table
                table(self._supabase, "registry.dependencies").insert(dependency_record).execute()
                
            except Exception as e:
                logger.error(f"Error storing dependency in database: {e}")
        
        return dependency_id
    
    def add_environment_var(
    self,
    var_name: str,
    provider_name: str,
    is_required: bool = True,
    description: Optional[str] = None
) -> Optional[str]:
        """
        Add an environment variable to the registry.
        
        Args:
            var_name: Name of the environment variable
            provider_name: Provider this environment variable is for
            is_required: Whether the environment variable is required
            description: Optional description
            
        Returns:
            ID of the environment variable entry or None on failure
        """
        return self._register_environment_var(var_name, provider_name, is_required, description)

    def _register_environment_var(
        self,
        var_name: str,
        provider_name: str,
        is_required: bool = True,
        description: Optional[str] = None
    ) -> Optional[str]:
        """
        Implementation method to register an environment variable.
        
        Args:
            var_name: Name of the environment variable
            provider_name: Provider this environment variable is for
            is_required: Whether the environment variable is required
            description: Optional description
            
        Returns:
            ID of the environment variable entry or None on failure
        """
        # Generate a unique ID for the environment variable
        env_var_id = str(uuid.uuid4())
        
        # Prepare environment variable data
        env_var_record = {
            "id": env_var_id,
            "var_name": var_name,
            "provider_name": provider_name,
            "is_required": is_required,
            "description": description or f"Environment variable {var_name} for {provider_name}",
            "created_at": datetime.now().isoformat()
        }
        
        # Store in local registry
        self._environment_vars[var_name] = env_var_record
        
        # Store in Supabase if available
        if self._supabase is not None:
            try:
                from src.haive.dataflow.db.supabase import table
                
                # Try to add to config.environment_variables (new schema)
                try:
                    # Format the display name
                    display_name = var_name.replace('_', ' ').title()
                    
                    # Check if environment variable already exists
                    env_var_response = table(self._supabase, "config.environment_variables").select("*").eq("name", var_name).execute()
                    
                    if not env_var_response.data or len(env_var_response.data) == 0:
                        # Create new environment variable
                        env_var_data = {
                            "id": env_var_id,
                            "name": var_name,
                            "display_name": display_name,
                            "description": description or f"Environment variable {var_name} for {provider_name}",
                            "is_secret": True,  # API keys are usually secret
                            "is_required": is_required,
                            "metadata": json.dumps({"provider_name": provider_name}),
                            "created_at": datetime.now().isoformat(),
                            "updated_at": datetime.now().isoformat()
                        }
                        
                        response = table(self._supabase, "config.environment_variables").insert(env_var_data).execute()
                        
                        if response.data and len(response.data) > 0:
                            logger.info(f"Added environment variable {var_name} to config.environment_variables")
                            
                            # Now try to create a component-environment mapping if we have the provider in components
                            try:
                                provider_response = table(self._supabase, "config.components").select("id").eq("name", provider_name).execute()
                                
                                if provider_response.data and len(provider_response.data) > 0:
                                    component_id = provider_response.data[0]["id"]
                                    
                                    mapping_data = {
                                        "id": str(uuid.uuid4()),
                                        "component_id": component_id,
                                        "env_var_id": env_var_id,
                                        "priority": 1,
                                        "is_detected": False,
                                        "created_at": datetime.now().isoformat(),
                                        "updated_at": datetime.now().isoformat()
                                    }
                                    
                                    table(self._supabase, "config.component_env_mappings").insert(mapping_data).execute()
                                    logger.info(f"Created component to environment mapping for {provider_name} and {var_name}")
                            except Exception as mapping_e:
                                logger.warning(f"Error creating component-environment mapping: {mapping_e}")
                                
                            return env_var_id
                    else:
                        # Update existing environment variable
                        existing_id = env_var_response.data[0]["id"]
                        env_var_data = {
                            "description": description or f"Environment variable {var_name} for {provider_name}",
                            "is_required": is_required,
                            "metadata": json.dumps({"provider_name": provider_name}),
                            "updated_at": datetime.now().isoformat()
                        }
                        
                        table(self._supabase, "config.environment_variables").update(env_var_data).eq("id", existing_id).execute()
                        logger.info(f"Updated environment variable {var_name} in config.environment_variables")
                        return existing_id
                        
                except Exception as e:
                    logger.warning(f"Error adding to config.environment_variables: {e}")
                
                # Try the legacy registry.environment_vars table
                try:
                    # Create table if it doesn't exist
                    self._ensure_registry_schema()
                    create_env_vars_table = """
                    CREATE TABLE IF NOT EXISTS registry.environment_vars (
                        id UUID PRIMARY KEY,
                        var_name VARCHAR(255) NOT NULL,
                        provider_name VARCHAR(255) NOT NULL,
                        is_required BOOLEAN DEFAULT TRUE,
                        description TEXT,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                    );
                    """
                    self._supabase.query(create_env_vars_table).execute()
                    
                    # Check if record already exists
                    response = table(self._supabase, "registry.environment_vars").select("*").eq("var_name", var_name).eq("provider_name", provider_name).execute()
                    
                    if response.data and len(response.data) > 0:
                        # Update existing record
                        existing_id = response.data[0]["id"]
                        table(self._supabase, "registry.environment_vars").update({
                            "is_required": is_required,
                            "description": description or f"Environment variable {var_name} for {provider_name}",
                            "updated_at": datetime.now().isoformat()
                        }).eq("id", existing_id).execute()
                        env_var_id = existing_id
                        logger.info(f"Updated environment variable {var_name} in registry.environment_vars")
                    else:
                        # Insert new record
                        response = table(self._supabase, "registry.environment_vars").insert(env_var_record).execute()
                        if response.data and len(response.data) > 0:
                            logger.info(f"Added environment variable {var_name} to registry.environment_vars")
                            return env_var_id
                except Exception as legacy_e:
                    logger.warning(f"Error adding to registry.environment_vars: {legacy_e}")
                    
            except Exception as e:
                logger.error(f"Error storing environment variable in database: {e}")
            
        return env_var_id

    def _ensure_registry_schema(self):
        """Ensure the registry schema is properly set up for backward compatibility."""
        try:
            # Check if the registry schema exists
            schema_check = self._supabase.query("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'registry'").execute()
            
            if not schema_check.data or len(schema_check.data) == 0:
                # Create registry schema if it doesn't exist
                self._supabase.query("CREATE SCHEMA IF NOT EXISTS registry").execute()
                logger.info("Created registry schema for backward compatibility")
            
            # Check for required tables
            tables = [
                ("registry", "items", """
                    id UUID PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    type VARCHAR(50) NOT NULL,
                    description TEXT,
                    metadata JSONB,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                """),
                ("registry", "configurations", """
                    id UUID PRIMARY KEY,
                    registry_id UUID NOT NULL,
                    config_type VARCHAR(50) NOT NULL,
                    config_data JSONB,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                """),
                ("registry", "dependencies", """
                    id UUID PRIMARY KEY,
                    registry_id UUID NOT NULL,
                    dependent_id UUID NOT NULL,
                    dependency_type VARCHAR(50) NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                """),
                ("registry", "environment_vars", """
                    id UUID PRIMARY KEY,
                    var_name VARCHAR(255) NOT NULL,
                    provider_name VARCHAR(255) NOT NULL,
                    is_required BOOLEAN DEFAULT TRUE,
                    description TEXT,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                """),
                ("registry", "import_logs", """
                    id UUID PRIMARY KEY,
                    import_session VARCHAR(100) NOT NULL,
                    entity_name VARCHAR(255) NOT NULL,
                    entity_type VARCHAR(50) NOT NULL,
                    status VARCHAR(50) NOT NULL,
                    message TEXT,
                    traceback TEXT,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                """)
            ]
            
            for schema, table_name, columns in tables:
                try:
                    # Check if table exists
                    table_check = self._supabase.query(f"SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = '{schema}' AND tablename = '{table_name}'").execute()
                    
                    if not table_check.data or len(table_check.data) == 0:
                        # Create table
                        self._supabase.query(f"CREATE TABLE IF NOT EXISTS {schema}.{table_name} ({columns})").execute()
                        logger.info(f"Created table {schema}.{table_name} for backward compatibility")
                except Exception as table_e:
                    logger.warning(f"Error checking/creating table {schema}.{table_name}: {table_e}")
                        
        except Exception as e:
            logger.error(f"Error ensuring registry schema: {e}")
    
    def add_import_log(
    self,
    import_session: str,
    entity_name: str,
    entity_type: str,
    status: ImportStatus,
    message: Optional[str] = None,
    traceback_str: Optional[str] = None
) -> None:
        """
        Add an import log entry.
        
        Args:
            import_session: Import session identifier
            entity_name: Name of the entity being imported
            entity_type: Type of entity
            status: Import status
            message: Optional message
            traceback_str: Optional traceback string
        """
        # Prepare import log data
        log_entry = {
            "id": str(uuid.uuid4()),
            "import_session": import_session,
            "entity_name": entity_name,
            "entity_type": entity_type,
            "status": status.value if isinstance(status, ImportStatus) else status,
            "message": message,
            "traceback": traceback_str,
            "created_at": datetime.now().isoformat()
        }
        
        # Store in local registry
        self._import_logs.append(log_entry)
        
        # Store in Supabase if available
        if self._supabase is not None:
            try:
                from src.haive.dataflow.db.supabase import table
                
                # Try to add to audit.import_logs (new schema)
                try:
                    response = table(self._supabase, "audit.import_logs").insert(log_entry).execute()
                    logger.info(f"Successfully logged import for {entity_name} to audit.import_logs")
                    return
                except Exception as e:
                    logger.warning(f"Error storing import log in audit.import_logs: {e}")
                    
                    # Check if it's a table not found error
                    if hasattr(e, 'code') and getattr(e, 'code') == '42P01' or str(e).find("does not exist") >= 0:
                        # Try to create the table
                        try:
                            create_table_query = """
                            CREATE TABLE IF NOT EXISTS audit.import_logs (
                                id UUID PRIMARY KEY,
                                import_session VARCHAR(100) NOT NULL,
                                entity_name VARCHAR(100) NOT NULL,
                                entity_type VARCHAR(50) NOT NULL,
                                status VARCHAR(50) NOT NULL,
                                message TEXT,
                                traceback TEXT,
                                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                            );
                            """
                            self._supabase.query(create_table_query).execute()
                            logger.info("Created audit.import_logs table")
                            
                            # Try inserting again after creating the table
                            response = table(self._supabase, "audit.import_logs").insert(log_entry).execute()
                            logger.info(f"Successfully logged import for {entity_name} after creating table")
                            return
                        except Exception as create_e:
                            logger.error(f"Error creating audit.import_logs table: {create_e}")
                
                # Fall back to direct query if table API fails
                try:
                    # Create a parameterized query
                    insert_query = """
                    INSERT INTO audit.import_logs (id, import_session, entity_name, entity_type, status, message, traceback, created_at)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                    """
                    self._supabase.query(insert_query, {
                        1: log_entry["id"],
                        2: log_entry["import_session"],
                        3: log_entry["entity_name"],
                        4: log_entry["entity_type"],
                        5: log_entry["status"],
                        6: log_entry["message"],
                        7: log_entry["traceback"],
                        8: log_entry["created_at"]
                    }).execute()
                    logger.info(f"Successfully logged import for {entity_name} using direct query")
                    return
                except Exception as query_e:
                    logger.error(f"Error with direct query to audit.import_logs: {query_e}")
                    
                    # As a last resort, try the old registry schema location
                    try:
                        # Try to ensure the old registry import_logs table exists
                        create_legacy_table_query = """
                        CREATE TABLE IF NOT EXISTS registry.import_logs (
                            id UUID PRIMARY KEY,
                            import_session VARCHAR(100) NOT NULL,
                            entity_name VARCHAR(100) NOT NULL,
                            entity_type VARCHAR(50) NOT NULL,
                            status VARCHAR(50) NOT NULL,
                            message TEXT,
                            traceback TEXT,
                            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                        );
                        """
                        self._supabase.query(create_legacy_table_query).execute()
                        
                        # Insert into legacy table
                        table(self._supabase, "registry.import_logs").insert(log_entry).execute()
                        logger.info(f"Successfully logged import for {entity_name} to legacy registry.import_logs table")
                    except Exception as legacy_e:
                        logger.warning(f"Error storing import log in legacy location: {legacy_e}")
                    
            except Exception as e:
                logger.error(f"Error storing import log in database: {e}")
    def get_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """
        Get an entity by ID.
        
        Args:
            entity_id: ID of the entity
            
        Returns:
            Entity data or None if not found
        """
        # Try local registry first
        if entity_id in self._entities:
            return self._entities[entity_id]
        
        # Try Supabase if available
        if self._supabase is not None:
            try:
                from src.haive.dataflow.db.supabase import table
                
                response = table(self._supabase, "registry.items").select("*").eq("id", entity_id).execute()
                
                if response.data and len(response.data) > 0:
                    return response.data[0]
                
            except Exception as e:
                logger.error(f"Error retrieving entity from database: {e}")
        
        return None
    
    def get_entities_by_type(self, entity_type: EntityType) -> List[Dict[str, Any]]:
        """
        Get all entities of a specific type.
        
        Args:
            entity_type: Type of entities to retrieve
            
        Returns:
            List of entity data
        """
        entity_type_value = entity_type.value if isinstance(entity_type, EntityType) else entity_type
        
        # Try Supabase if available
        if self._supabase is not None:
            try:
                from src.haive.dataflow.db.supabase import table
                
                response = table(self._supabase, "registry.items").select("*").eq("type", entity_type_value).execute()
                
                if response.data:
                    # Add provider availability info for providers
                    if entity_type_value in [EntityType.LLM_PROVIDER, EntityType.EMBEDDING_PROVIDER]:
                        for entity in response.data:
                            # Update availability based on environment variables
                            provider_name = entity.get("name")
                            env_vars = self.get_environment_vars(provider_name)
                            
                            # Check if required env vars are set
                            required_vars = [env for env in env_vars if env["is_required"]]
                            
                            if required_vars:
                                # Set availability based on required env vars
                                all_required_available = all(self.check_environment_var(env["var_name"]) for env in required_vars)
                                
                                # Update entity metadata
                                metadata = entity.get("metadata", {})
                                if isinstance(metadata, str):
                                    try:
                                        metadata = json.loads(metadata)
                                    except json.JSONDecodeError:
                                        metadata = {}
                                
                                metadata["is_available"] = all_required_available
                                entity["metadata"] = metadata
                                entity["is_available"] = all_required_available
                    
                    return response.data
                
            except Exception as e:
                logger.error(f"Error retrieving entities from database: {e}")
        
        # Fall back to local registry
        return [entity for entity in self._entities.values() if entity["type"] == entity_type_value]
    
    def get_environment_vars(self, provider_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get environment variables, optionally filtered by provider.
        
        Args:
            provider_name: Optional provider to filter by
            
        Returns:
            List of environment variable data
        """
        # Try Supabase if available
        if self._supabase is not None:
            try:
                from src.haive.dataflow.db.supabase import table
                
                # Try to use config.environment_variables first (new schema)
                try:
                    query = table(self._supabase, "config.environment_variables").select("*")
                    response = query.execute()
                    
                    if response.data:
                        # Process results to match expected format
                        results = []
                        
                        for env_var in response.data:
                            # Extract provider_name from metadata
                            metadata = env_var.get("metadata", {})
                            if isinstance(metadata, str):
                                try:
                                    metadata = json.loads(metadata)
                                except:
                                    metadata = {}
                                    
                            provider = metadata.get("provider_name")
                            
                            # Only include if provider matches (if filtering)
                            if provider_name and provider != provider_name:
                                continue
                                
                            # Convert to expected format
                            results.append({
                                "id": env_var.get("id"),
                                "var_name": env_var.get("name"),
                                "provider_name": provider,
                                "is_required": env_var.get("is_required", True),
                                "description": env_var.get("description", ""),
                                "created_at": env_var.get("created_at")
                            })
                            
                        return results
                except Exception as e:
                    logger.warning(f"Error using config.environment_variables: {e}")
                
                # Fall back to legacy table
                query = table(self._supabase, "registry.environment_vars").select("*")
                
                if provider_name:
                    query = query.eq("provider_name", provider_name)
                
                response = query.execute()
                
                if response.data:
                    return response.data
                
            except Exception as e:
                logger.error(f"Error retrieving environment variables from database: {e}")
        
        # Fall back to local registry
        if provider_name:
            return [var for var in self._environment_vars.values() if var["provider_name"] == provider_name]
        else:
            return list(self._environment_vars.values())
    
    def check_environment_var(self, var_name: str) -> bool:
        """
        Check if an environment variable is set.
        
        Args:
            var_name: Name of environment variable to check
            
        Returns:
            True if the environment variable is set, False otherwise
        """
        return os.getenv(var_name) is not None
    
    def get_available_providers(self, entity_type: Optional[EntityType] = None) -> List[Dict[str, Any]]:
        """
        Get all available providers.
        
        Args:
            entity_type: Optional entity type to filter providers by (e.g., LLM_PROVIDER)
            
        Returns:
            List of provider data with availability info
        """
        entity_type_value = entity_type.value if isinstance(entity_type, EntityType) else entity_type
        
        # First try to get providers from the models schema (new schema)
        if self._supabase is not None:
            try:
                from src.haive.dataflow.db.supabase import table
                
                # Try to query from models.providers
                provider_type = None
                if entity_type_value == EntityType.LLM_PROVIDER:
                    provider_type = "llm"
                elif entity_type_value == EntityType.EMBEDDING_PROVIDER:
                    provider_type = "embedding"
                
                if provider_type:
                    # First get the provider type ID
                    type_response = table(self._supabase, "models.provider_types").select("id").eq("name", provider_type).execute()
                    
                    if type_response.data and len(type_response.data) > 0:
                        provider_type_id = type_response.data[0]["id"]
                        
                        # Get providers of this type
                        providers_response = table(self._supabase, "models.providers").select("*").eq("type_id", provider_type_id).execute()
                        
                        if providers_response.data and len(providers_response.data) > 0:
                            providers = providers_response.data
                            
                            # Update availability based on environment variables
                            for provider in providers:
                                # Get environment variables for this provider
                                provider_name = provider["name"]
                                env_vars = self.get_environment_vars(provider_name)
                                
                                # Check if required env vars are set
                                required_vars = [env for env in env_vars if env["is_required"]]
                                
                                if required_vars:
                                    # Set availability based on required env vars
                                    all_required_available = all(self.check_environment_var(env["var_name"]) for env in required_vars)
                                    provider["is_available"] = all_required_available
                                else:
                                    # No required env vars, assume available
                                    provider["is_available"] = True
                                
                                # Add entity_type to match legacy format
                                provider["type"] = entity_type_value
                                
                                # Update provider availability in database
                                table(self._supabase, "models.providers").update({
                                    "is_available": provider["is_available"],
                                    "updated_at": datetime.now().isoformat()
                                }).eq("id", provider["id"]).execute()
                            
                            return providers
            except Exception as e:
                logger.warning(f"Error getting providers from models schema: {e}")
        
        # Get all providers (LLM_PROVIDER or EMBEDDING_PROVIDER) from legacy registry
        providers = []
        
        if entity_type_value:
            providers = self.get_entities_by_type(entity_type_value)
        else:
            # Get both types
            providers = (
                self.get_entities_by_type(EntityType.LLM_PROVIDER) + 
                self.get_entities_by_type(EntityType.EMBEDDING_PROVIDER)
            )
        
        # Check environment variables for each provider
        for provider in providers:
            # Get environment variables for this provider
            provider_name = provider["name"]
            env_vars = self.get_environment_vars(provider_name)
            
            # Check if required env vars are set
            required_vars = [env for env in env_vars if env["is_required"]]
            
            if required_vars:
                # Set availability based on required env vars
                all_required_available = all(self.check_environment_var(env["var_name"]) for env in required_vars)
                provider["is_available"] = all_required_available
            else:
                # No required env vars, assume available
                provider["is_available"] = True
        
        return providers
    
    def search_entities(
        self,
        query: str,
        entity_type: Optional[EntityType] = None,
        metadata_filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for entities based on a query.
        
        Args:
            query: Search query
            entity_type: Optional entity type to filter by
            metadata_filter: Optional metadata filter
            
        Returns:
            List of matching entities
        """
        entity_type_value = entity_type.value if isinstance(entity_type, EntityType) else entity_type
        
        # Try Supabase if available and has search capabilities
        if self._supabase is not None:
            try:
                from src.haive.dataflow.db.supabase import table
                
                # Build query
                base_query = table(self._supabase, "registry.items").select("*")
                
                # Apply type filter if specified
                if entity_type_value:
                    base_query = base_query.eq("type", entity_type_value)
                
                # Apply search query
                # This is basic filtering - in a real implementation, you might want to use
                # Postgres full-text search or a more sophisticated approach
                response = base_query.or_(f"name.ilike.%{query}%,description.ilike.%{query}%").execute()
                
                if response.data:
                    # Further filter by metadata if needed
                    if metadata_filter:
                        filtered_results = []
                        for entity in response.data:
                            entity_metadata = entity.get("metadata", {})
                            if isinstance(entity_metadata, str):
                                try:
                                    entity_metadata = json.loads(entity_metadata)
                                except:
                                    entity_metadata = {}
                            
                            # Check if all metadata filters match
                            metadata_matches = True
                            for key, value in metadata_filter.items():
                                if key not in entity_metadata or entity_metadata[key] != value:
                                    metadata_matches = False
                                    break
                            
                            if metadata_matches:
                                filtered_results.append(entity)
                        
                        return filtered_results
                    else:
                        return response.data
                
            except Exception as e:
                logger.error(f"Error searching entities in database: {e}")
        
        # Fall back to local search
        results = []
        for entity in self._entities.values():
            # Apply type filter if specified
            if entity_type_value and entity["type"] != entity_type_value:
                continue
            
            # Apply text search
            if (
                query.lower() in entity["name"].lower() or
                query.lower() in entity.get("description", "").lower()
            ):
                # Apply metadata filter if specified
                if metadata_filter:
                    entity_metadata = entity.get("metadata", {})
                    metadata_matches = True
                    for key, value in metadata_filter.items():
                        if key not in entity_metadata or entity_metadata[key] != value:
                            metadata_matches = False
                            break
                    
                    if metadata_matches:
                        results.append(entity)
                else:
                    results.append(entity)
        
        return results


# Create a singleton instance
registry_system = RegistrySystem()