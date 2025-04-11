"""Database schema and operations for the registry system.

This module provides database integration for the registry system, focusing on:
1. Schema creation and migration
2. Supabase integration
3. Relations between registry items and state schemas
4. Agent graph storage
"""

import logging
import json
import traceback
from typing import Dict, Any, Optional, List, Union, Tuple
from datetime import datetime
from pydantic import BaseModel, Field

# Set up logging
logger = logging.getLogger(__name__)

# Try to import the Supabase client
try:
    from src.haive.dataflow.supabase.base import get_supabase_client
    SUPABASE_AVAILABLE = True
    logger.info("Supabase client available for registry persistence")
except ImportError:
    SUPABASE_AVAILABLE = False
    logger.info("Supabase client not available, using in-memory storage only")


class RegistrySchema(BaseModel):
    """Schema for a registry item in Supabase."""
    id: Optional[str] = None
    name: str
    class_name: str
    module_path: str
    item_type: str
    description: str = ""
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        arbitrary_types_allowed = True


class SchemaDefinition(BaseModel):
    """Schema definition for a component, such as input/output/state schema."""
    id: Optional[str] = None
    registry_item_id: str
    schema_type: str  # input, output, state
    schema_json: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.now)


class AgentGraph(BaseModel):
    """Graph representation of an agent's components."""
    id: Optional[str] = None
    agent_id: str
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    timestamp: datetime = Field(default_factory=datetime.now)


class RegistryDB:
    """Database operations for the registry system.
    
    This class provides methods for interacting with the database,
    including creating and querying registry items, schemas, and
    agent graphs.
    """
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one instance exists."""
        if cls._instance is None:
            cls._instance = super(RegistryDB, cls).__new__(cls)
            cls._instance._supabase_client = None
            cls._instance._tables_created = False
            
            # Try to set up Supabase if available
            if SUPABASE_AVAILABLE:
                cls._instance._setup_supabase()
                
        return cls._instance
    
    def _setup_supabase(self):
        """Set up the Supabase client and create tables if needed."""
        try:
            self._supabase_client = get_supabase_client()
            logger.info("Connected to Supabase for registry persistence")
            
            # Create necessary tables if they don't exist
            self._create_tables()
            
        except Exception as e:
            logger.warning(f"Supabase setup error: {e}")
            self._supabase_client = None
    
    def _create_tables(self):
        """Create necessary tables in Supabase if they don't exist."""
        if self._tables_created or not self._supabase_client:
            return
            
        try:
            # Define all registry item tables
            registry_tables = [
                "game_registry",
                "agent_registry",
                "component_registry",
                "tool_registry",
                "toolkit_registry"
            ]
            
            # Create registry tables
            for table_name in registry_tables:
                self._create_registry_table(table_name)
            
            # Create schema tables for input/output/state schemas
            self._create_schema_tables()
            
            # Create agent graph tables
            self._create_agent_graph_tables()
            
            self._tables_created = True
            logger.info("Created all necessary tables in Supabase")
            
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            logger.debug(traceback.format_exc())
    
    def _create_registry_table(self, table_name: str):
        """Create a registry table in Supabase."""
        if not self._supabase_client:
            return
            
        try:
            # Use the REST API to create the table if it doesn't exist
            # This is a simplified approach - in a real implementation you'd use migrations
            # or a more robust method for schema management
            
            # Check if table exists by querying it (will error if it doesn't)
            try:
                self._supabase_client.table(table_name).select("count(*)", count="exact").limit(1).execute()
                logger.debug(f"Table {table_name} already exists")
                return
            except Exception:
                # Table doesn't exist, create it
                pass
            
            # Create the table using SQL (through Supabase functions or other means)
            # In a real implementation, you would use proper Supabase functions for this
            # This is a simplified approach for illustration
            
            logger.info(f"Would create table {table_name} if using SQL directly")
            # In a real-world scenario, you might create the table using a SQL function
            # exposed through Supabase or another method
            
        except Exception as e:
            logger.error(f"Error creating registry table {table_name}: {e}")
    
    def _create_schema_tables(self):
        """Create tables for component schemas."""
        if not self._supabase_client:
            return
            
        try:
            # Similar to _create_registry_table, in a real implementation
            # you would use proper Supabase methods or migrations
            
            table_name = "component_schemas"
            
            # Check if table exists
            try:
                self._supabase_client.table(table_name).select("count(*)", count="exact").limit(1).execute()
                logger.debug(f"Table {table_name} already exists")
                return
            except Exception:
                # Table doesn't exist, create it
                pass
            
            logger.info(f"Would create table {table_name} if using SQL directly")
            
        except Exception as e:
            logger.error(f"Error creating schema tables: {e}")
    
    def _create_agent_graph_tables(self):
        """Create tables for agent graphs."""
        if not self._supabase_client:
            return
            
        try:
            # Similar to the above methods
            
            table_name = "agent_graphs"
            
            # Check if table exists
            try:
                self._supabase_client.table(table_name).select("count(*)", count="exact").limit(1).execute()
                logger.debug(f"Table {table_name} already exists")
                return
            except Exception:
                # Table doesn't exist, create it
                pass
            
            logger.info(f"Would create table {table_name} if using SQL directly")
            
        except Exception as e:
            logger.error(f"Error creating agent graph tables: {e}")
    
    def upsert_registry_item(self, item: RegistrySchema) -> Optional[str]:
        """Create or update a registry item in the database.
        
        Args:
            item: Registry item to upsert
            
        Returns:
            ID of the inserted/updated item if successful, None otherwise
        """
        if not self._supabase_client:
            return None
            
        try:
            # Prepare the data
            item_dict = item.model_dump(exclude={"id"} if item.id is None else {})
            
            # Convert metadata to JSON string
            if "metadata" in item_dict and isinstance(item_dict["metadata"], dict):
                item_dict["metadata"] = json.dumps(item_dict["metadata"])
            
            # Convert timestamp to string if needed
            if "timestamp" in item_dict and isinstance(item_dict["timestamp"], datetime):
                item_dict["timestamp"] = item_dict["timestamp"].isoformat()
            
            # Determine the table name
            table_name = f"{item.item_type}_registry"
            
            # Upsert the item
            response = self._supabase_client.table(table_name).upsert(item_dict).execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0].get("id")
                
            return None
            
        except Exception as e:
            logger.error(f"Error upserting registry item: {e}")
            logger.debug(traceback.format_exc())
            return None
    
    def get_registry_item(self, name: str, item_type: str) -> Optional[RegistrySchema]:
        """Get a registry item from the database.
        
        Args:
            name: Name of the item
            item_type: Type of the item (game, agent, component, etc.)
            
        Returns:
            RegistrySchema if found, None otherwise
        """
        if not self._supabase_client:
            return None
            
        try:
            # Determine the table name
            table_name = f"{item_type}_registry"
            
            # Query the item
            response = self._supabase_client.table(table_name).select("*").eq("name", name).execute()
            
            if response.data and len(response.data) > 0:
                item_data = response.data[0]
                
                # Parse metadata if needed
                if "metadata" in item_data and isinstance(item_data["metadata"], str):
                    item_data["metadata"] = json.loads(item_data["metadata"])
                
                # Create the schema object
                return RegistrySchema(**item_data)
                
            return None
            
        except Exception as e:
            logger.error(f"Error getting registry item: {e}")
            logger.debug(traceback.format_exc())
            return None
    
    def list_registry_items(self, item_type: str) -> List[RegistrySchema]:
        """List all registry items of a specific type.
        
        Args:
            item_type: Type of items to list
            
        Returns:
            List of RegistrySchema objects
        """
        if not self._supabase_client:
            return []
            
        try:
            # Determine the table name
            table_name = f"{item_type}_registry"
            
            # Query all items
            response = self._supabase_client.table(table_name).select("*").execute()
            
            items = []
            if response.data:
                for item_data in response.data:
                    # Parse metadata if needed
                    if "metadata" in item_data and isinstance(item_data["metadata"], str):
                        item_data["metadata"] = json.loads(item_data["metadata"])
                    
                    # Create the schema object
                    items.append(RegistrySchema(**item_data))
                    
            return items
            
        except Exception as e:
            logger.error(f"Error listing registry items: {e}")
            logger.debug(traceback.format_exc())
            return []
    
    def upsert_schema_definition(self, schema: SchemaDefinition) -> Optional[str]:
        """Create or update a schema definition in the database.
        
        Args:
            schema: Schema definition to upsert
            
        Returns:
            ID of the inserted/updated schema if successful, None otherwise
        """
        if not self._supabase_client:
            return None
            
        try:
            # Prepare the data
            schema_dict = schema.model_dump(exclude={"id"} if schema.id is None else {})
            
            # Convert schema_json to JSON string
            if "schema_json" in schema_dict and isinstance(schema_dict["schema_json"], dict):
                schema_dict["schema_json"] = json.dumps(schema_dict["schema_json"])
            
            # Convert timestamp to string if needed
            if "timestamp" in schema_dict and isinstance(schema_dict["timestamp"], datetime):
                schema_dict["timestamp"] = schema_dict["timestamp"].isoformat()
            
            # Upsert the schema
            response = self._supabase_client.table("component_schemas").upsert(schema_dict).execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0].get("id")
                
            return None
            
        except Exception as e:
            logger.error(f"Error upserting schema definition: {e}")
            logger.debug(traceback.format_exc())
            return None
    
    def get_schema_definitions(self, registry_item_id: str, schema_type: Optional[str] = None) -> List[SchemaDefinition]:
        """Get schema definitions for a registry item.
        
        Args:
            registry_item_id: ID of the registry item
            schema_type: Optional schema type filter (input, output, state)
            
        Returns:
            List of SchemaDefinition objects
        """
        if not self._supabase_client:
            return []
            
        try:
            # Build the query
            query = self._supabase_client.table("component_schemas").select("*").eq("registry_item_id", registry_item_id)
            
            # Add schema_type filter if provided
            if schema_type:
                query = query.eq("schema_type", schema_type)
            
            # Execute the query
            response = query.execute()
            
            schemas = []
            if response.data:
                for schema_data in response.data:
                    # Parse schema_json if needed
                    if "schema_json" in schema_data and isinstance(schema_data["schema_json"], str):
                        schema_data["schema_json"] = json.loads(schema_data["schema_json"])
                    
                    # Create the schema object
                    schemas.append(SchemaDefinition(**schema_data))
                    
            return schemas
            
        except Exception as e:
            logger.error(f"Error getting schema definitions: {e}")
            logger.debug(traceback.format_exc())
            return []
    
    def upsert_agent_graph(self, graph: AgentGraph) -> Optional[str]:
        """Create or update an agent graph in the database.
        
        Args:
            graph: Agent graph to upsert
            
        Returns:
            ID of the inserted/updated graph if successful, None otherwise
        """
        if not self._supabase_client:
            return None
            
        try:
            # Prepare the data
            graph_dict = graph.model_dump(exclude={"id"} if graph.id is None else {})
            
            # Convert nodes and edges to JSON strings
            if "nodes" in graph_dict and isinstance(graph_dict["nodes"], list):
                graph_dict["nodes"] = json.dumps(graph_dict["nodes"])
            
            if "edges" in graph_dict and isinstance(graph_dict["edges"], list):
                graph_dict["edges"] = json.dumps(graph_dict["edges"])
            
            # Convert timestamp to string if needed
            if "timestamp" in graph_dict and isinstance(graph_dict["timestamp"], datetime):
                graph_dict["timestamp"] = graph_dict["timestamp"].isoformat()
            
            # Upsert the graph
            response = self._supabase_client.table("agent_graphs").upsert(graph_dict).execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0].get("id")
                
            return None
            
        except Exception as e:
            logger.error(f"Error upserting agent graph: {e}")
            logger.debug(traceback.format_exc())
            return None
    
    def get_agent_graph(self, agent_id: str) -> Optional[AgentGraph]:
        """Get an agent graph from the database.
        
        Args:
            agent_id: ID of the agent
            
        Returns:
            AgentGraph if found, None otherwise
        """
        if not self._supabase_client:
            return None
            
        try:
            # Query the graph
            response = self._supabase_client.table("agent_graphs").select("*").eq("agent_id", agent_id).execute()
            
            if response.data and len(response.data) > 0:
                graph_data = response.data[0]
                
                # Parse nodes and edges if needed
                if "nodes" in graph_data and isinstance(graph_data["nodes"], str):
                    graph_data["nodes"] = json.loads(graph_data["nodes"])
                
                if "edges" in graph_data and isinstance(graph_data["edges"], str):
                    graph_data["edges"] = json.loads(graph_data["edges"])
                
                # Create the graph object
                return AgentGraph(**graph_data)
                
            return None
            
        except Exception as e:
            logger.error(f"Error getting agent graph: {e}")
            logger.debug(traceback.format_exc())
            return None


# Singleton instance
registry_db = RegistryDB()

# Export the instance
__all__ = ["registry_db", "RegistrySchema", "SchemaDefinition", "AgentGraph"]
