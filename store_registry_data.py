#!/usr/bin/env python
"""
Script to extract agent/component schema information and store it in Supabase.

This script demonstrates:
1. How to extract agent schemas and graphs
2. How to store this information in Supabase
3. How to retrieve the stored information
"""

import os
import logging
from dotenv import load_dotenv
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env
load_dotenv('.env')

# Import registry components
# Import AgentTypeRegistry directly
from src.haive.dataflow.registry.agent import AgentTypeRegistry
from src.haive.dataflow.registry import (
    ComponentRegistry,
    ToolRegistry,
    ToolkitRegistry,
    extract_agent_schema,
    extract_agent_graph,
    extract_component_schema,
    get_graph_branches
)

# Import database models and client
from src.haive.dataflow.registry.db import (
    registry_db,
    RegistrySchema,
    SchemaDefinition,
    AgentGraph
)

def setup_supabase():
    """Setup Supabase connection and verify it's working."""
    # Check if Supabase environment variables are set
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_ANON_KEY")
    
    if not supabase_url or not supabase_key:
        logger.error("Supabase URL or KEY not set in environment. Check your .env file.")
        return False
    
    logger.info(f"Supabase environment variables found: URL={supabase_url}")
    return True

def store_agent_data(agent_name):
    """Extract and store agent data in Supabase.
    
    Args:
        agent_name: Name of the agent to extract and store
        
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Processing agent: {agent_name}")
    
    try:
        # Get agent metadata - use AgentTypeRegistry instead of AgentRegistry
        metadata = AgentTypeRegistry.get_agent_metadata(agent_name)
        if not metadata:
            logger.warning(f"Agent {agent_name} not found")
            return False
        
        # Extract agent schema
        schema = extract_agent_schema(agent_name)
        
        # Extract agent graph
        graph = extract_agent_graph(agent_name)
        
        # 1. Store agent in registry
        registry_item = RegistrySchema(
            name=agent_name,
            class_name=metadata.get("class_name", ""),
            module_path=metadata.get("module_path", ""),
            item_type="agent",
            description=metadata.get("description", ""),
            timestamp=datetime.now(),
            metadata=metadata
        )
        
        registry_item_id = registry_db.upsert_registry_item(registry_item)
        if not registry_item_id:
            logger.error(f"Failed to store agent {agent_name} in registry")
            return False
            
        logger.info(f"Stored agent {agent_name} in registry with ID: {registry_item_id}")
        
        # 2. Store agent schemas
        if schema:
            if schema.input_schema:
                input_schema = SchemaDefinition(
                    registry_item_id=registry_item_id,
                    schema_type="input",
                    schema_json=schema.input_schema,
                    timestamp=datetime.now()
                )
                registry_db.upsert_schema_definition(input_schema)
                logger.info(f"Stored input schema for agent {agent_name}")
            
            if schema.output_schema:
                output_schema = SchemaDefinition(
                    registry_item_id=registry_item_id,
                    schema_type="output",
                    schema_json=schema.output_schema,
                    timestamp=datetime.now()
                )
                registry_db.upsert_schema_definition(output_schema)
                logger.info(f"Stored output schema for agent {agent_name}")
                
            if schema.state_schema:
                state_schema = SchemaDefinition(
                    registry_item_id=registry_item_id,
                    schema_type="state",
                    schema_json=schema.state_schema,
                    timestamp=datetime.now()
                )
                registry_db.upsert_schema_definition(state_schema)
                logger.info(f"Stored state schema for agent {agent_name}")
        
        # 3. Store agent graph
        if graph:
            agent_graph = AgentGraph(
                agent_id=registry_item_id,
                nodes=[node.dict() for node in graph.nodes],
                edges=[edge.dict() for edge in graph.edges],
                timestamp=datetime.now()
            )
            graph_id = registry_db.upsert_agent_graph(agent_graph)
            if graph_id:
                logger.info(f"Stored graph for agent {agent_name} with ID: {graph_id}")
            else:
                logger.warning(f"Failed to store graph for agent {agent_name}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error storing agent {agent_name}: {e}", exc_info=True)
        return False

def store_component_data(component_name):
    """Extract and store component data in Supabase.
    
    Args:
        component_name: Name of the component to extract and store
        
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Processing component: {component_name}")
    
    try:
        # Get component metadata
        metadata = ComponentRegistry.get_metadata(component_name)
        if not metadata:
            logger.warning(f"Component {component_name} not found")
            return False
        
        # Extract component schema
        schema = extract_component_schema(component_name)
        
        # 1. Store component in registry
        registry_item = RegistrySchema(
            name=component_name,
            class_name=metadata.get("class_name", ""),
            module_path=metadata.get("module_path", ""),
            item_type="component",
            description=metadata.get("description", ""),
            timestamp=datetime.now(),
            metadata=metadata
        )
        
        registry_item_id = registry_db.upsert_registry_item(registry_item)
        if not registry_item_id:
            logger.error(f"Failed to store component {component_name} in registry")
            return False
            
        logger.info(f"Stored component {component_name} in registry with ID: {registry_item_id}")
        
        # 2. Store component schemas
        if schema:
            if schema.input_schema:
                input_schema = SchemaDefinition(
                    registry_item_id=registry_item_id,
                    schema_type="input",
                    schema_json=schema.input_schema,
                    timestamp=datetime.now()
                )
                registry_db.upsert_schema_definition(input_schema)
                logger.info(f"Stored input schema for component {component_name}")
            
            if schema.output_schema:
                output_schema = SchemaDefinition(
                    registry_item_id=registry_item_id,
                    schema_type="output",
                    schema_json=schema.output_schema,
                    timestamp=datetime.now()
                )
                registry_db.upsert_schema_definition(output_schema)
                logger.info(f"Stored output schema for component {component_name}")
                
            if schema.state_schema:
                state_schema = SchemaDefinition(
                    registry_item_id=registry_item_id,
                    schema_type="state",
                    schema_json=schema.state_schema,
                    timestamp=datetime.now()
                )
                registry_db.upsert_schema_definition(state_schema)
                logger.info(f"Stored state schema for component {component_name}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error storing component {component_name}: {e}", exc_info=True)
        return False

def main():
    """Main execution function."""
    # Setup Supabase
    if not setup_supabase():
        return
    
    # Process agents
    logger.info("Storing agent information...")
    agents = AgentTypeRegistry.list_agents()
    for agent in agents:
        agent_name = agent.get("name")
        if agent_name:
            store_agent_data(agent_name)
    
    # Process components
    logger.info("Storing component information...")
    components = ComponentRegistry.list_components()
    for component in components:
        component_name = component.get("name")
        if component_name:
            store_component_data(component_name)
    
    logger.info("Data storage complete!")

if __name__ == "__main__":
    main() 