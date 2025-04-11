"""Database schema management for the Haive Registry System.

This module provides functions for creating and managing the database schema
for the registry system. It handles schema creation, migrations, and
upgrades as needed.
"""

import logging
import os
import time
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple

# Set up logging
logger = logging.getLogger(__name__)

# SQL script paths
SCHEMA_DIR = Path(__file__).parent / "sql"
SCHEMA_SQL_PATH = SCHEMA_DIR / "schema.sql"

# Ensure SQL directory exists
os.makedirs(SCHEMA_DIR, exist_ok=True)

# Try to import Supabase client
try:
    from src.haive.dataflow.db.supabase import get_supabase_client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    logger.warning("Supabase client not available, schema operations will be limited")


def create_schema_sql() -> str:
    """
    Generate the SQL schema definition for the registry system.
    
    Returns:
        SQL schema definition as a string
    """
    # The complete SQL schema definition
    schema_sql = """-- Haive Registry System Schema Definitions
-- For Supabase PostgreSQL Database

-- Create schemas
CREATE SCHEMA IF NOT EXISTS registry;
CREATE SCHEMA IF NOT EXISTS agents;
CREATE SCHEMA IF NOT EXISTS components;

-- Registry Items (core entity table)
CREATE TABLE IF NOT EXISTS registry.items (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  type TEXT NOT NULL, -- 'agent', 'tool', 'engine', 'game', etc.
  description TEXT,
  module_path TEXT,
  class_name TEXT,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  metadata JSONB DEFAULT '{}'::jsonb,
  UNIQUE (type, name)
);

-- Configurations (schema, prompts, etc.)
CREATE TABLE IF NOT EXISTS registry.configurations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  registry_id UUID REFERENCES registry.items(id) ON DELETE CASCADE,
  config_type TEXT NOT NULL, -- 'state_schema', 'input_schema', 'output_schema', 'prompt', 'engine', etc.
  config_data JSONB NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Graph Definitions
CREATE TABLE IF NOT EXISTS registry.graphs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  registry_id UUID REFERENCES registry.items(id) ON DELETE CASCADE,
  nodes JSONB NOT NULL,
  edges JSONB NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Dependencies
CREATE TABLE IF NOT EXISTS registry.dependencies (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  registry_id UUID REFERENCES registry.items(id) ON DELETE CASCADE,
  dependent_id UUID REFERENCES registry.items(id) ON DELETE CASCADE,
  dependency_type TEXT NOT NULL, -- 'requires', 'uses', 'extends'
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Environment Variables
CREATE TABLE IF NOT EXISTS registry.environment_vars (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  registry_id UUID REFERENCES registry.items(id) ON DELETE CASCADE,
  env_name TEXT NOT NULL,
  is_required BOOLEAN DEFAULT false,
  default_value TEXT,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Import Logs
CREATE TABLE IF NOT EXISTS registry.import_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  import_session TEXT NOT NULL,
  entity_name TEXT NOT NULL,
  entity_type TEXT NOT NULL,
  status TEXT NOT NULL, -- 'success', 'failure'
  message TEXT,
  traceback TEXT,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Embedding Model Configuration
CREATE TABLE IF NOT EXISTS components.embedding_models (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  provider TEXT NOT NULL, -- 'azure', 'huggingface', 'openai', 'cohere'
  model_name TEXT NOT NULL,
  description TEXT,
  config_data JSONB NOT NULL,
  is_default BOOLEAN DEFAULT false,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  UNIQUE (provider, model_name)
);

-- LLM Model Configuration
CREATE TABLE IF NOT EXISTS components.llm_models (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  provider TEXT NOT NULL, -- 'azure', 'anthropic', 'openai', etc.
  model_name TEXT NOT NULL,
  description TEXT,
  config_data JSONB NOT NULL, 
  is_default BOOLEAN DEFAULT false,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  UNIQUE (provider, model_name)
);

-- Engine Templates
CREATE TABLE IF NOT EXISTS components.engine_templates (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  engine_type TEXT NOT NULL, -- 'aug_llm', 'llm_config', etc.
  description TEXT,
  config_data JSONB NOT NULL,
  is_default BOOLEAN DEFAULT false,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  UNIQUE (name)
);

-- State Schema Templates
CREATE TABLE IF NOT EXISTS components.state_templates (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  schema_type TEXT NOT NULL, -- 'agent_state', 'game_state', etc.
  description TEXT,
  schema_data JSONB NOT NULL,
  is_default BOOLEAN DEFAULT false,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  UNIQUE (name)
);

-- Tool Catalog
CREATE TABLE IF NOT EXISTS components.tools (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  tool_type TEXT NOT NULL, -- 'function', 'api', 'llm', etc.
  description TEXT,
  module_path TEXT,
  class_name TEXT,
  schema_data JSONB, -- Input/output schema
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  UNIQUE (name)
);

-- Toolkit Catalog
CREATE TABLE IF NOT EXISTS components.toolkits (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  description TEXT,
  tools JSONB NOT NULL, -- List of tool references
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  UNIQUE (name)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_registry_items_type ON registry.items(type);
CREATE INDEX IF NOT EXISTS idx_configurations_registry_id ON registry.configurations(registry_id);
CREATE INDEX IF NOT EXISTS idx_configurations_type ON registry.configurations(config_type);
CREATE INDEX IF NOT EXISTS idx_graphs_registry_id ON registry.graphs(registry_id);
CREATE INDEX IF NOT EXISTS idx_dependencies_registry_id ON registry.dependencies(registry_id);
CREATE INDEX IF NOT EXISTS idx_dependencies_dependent_id ON registry.dependencies(dependent_id);
CREATE INDEX IF NOT EXISTS idx_env_vars_registry_id ON registry.environment_vars(registry_id);
CREATE INDEX IF NOT EXISTS idx_embedding_models_provider ON components.embedding_models(provider);
CREATE INDEX IF NOT EXISTS idx_llm_models_provider ON components.llm_models(provider);
"""
    
    # Write the schema to a file for reference
    with open(SCHEMA_SQL_PATH, 'w') as f:
        f.write(schema_sql)
    
    return schema_sql


def execute_schema_sql(client=None, schema_sql: Optional[str] = None) -> bool:
    """
    Execute the schema SQL to set up the database.
    
    Args:
        client: Optional Supabase client
        schema_sql: Optional schema SQL to execute
        
    Returns:
        True if successful, False otherwise
    """
    if not SUPABASE_AVAILABLE and client is None:
        logger.error("Supabase client not available and no client provided.")
        return False
    
    try:
        # Get or use provided client
        supabase = client or get_supabase_client()
        
        # Get schema SQL
        sql = schema_sql or create_schema_sql()
        
        # Split into individual statements
        statements = sql.split(';')
        
        # Execute each statement
        for stmt in statements:
            if stmt.strip():
                try:
                    # Execute the SQL statement using the Supabase client's rpc function
                    # This requires a corresponding PostgreSQL function to be set up
                    # that can execute arbitrary SQL
                    result = supabase.rpc(
                        'execute_sql', 
                        {'sql_statement': stmt}
                    ).execute()
                    
                    # Check for errors
                    if hasattr(result, 'error') and result.error:
                        logger.error(f"Error executing SQL: {result.error}")
                        return False
                except Exception as e:
                    logger.error(f"Error executing SQL statement: {e}")
                    logger.debug(f"Statement: {stmt}")
                    return False
        
        logger.info("Schema created successfully")
        return True
    except Exception as e:
        logger.error(f"Error executing schema SQL: {e}")
        return False


def check_schema_exists(client=None) -> bool:
    """
    Check if the registry schema exists.
    
    Args:
        client: Optional Supabase client
        
    Returns:
        True if the schema exists, False otherwise
    """
    if not SUPABASE_AVAILABLE and client is None:
        logger.error("Supabase client not available and no client provided.")
        return False
    
    try:
        # Get or use provided client
        supabase = client or get_supabase_client()
        
        # Check if the registry schema exists by querying the information_schema
        result = supabase.rpc(
            'execute_sql',
            {'sql_statement': "SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'registry'"}
        ).execute()
        
        # Check if we got any results
        if hasattr(result, 'data') and result.data and len(result.data) > 0:
            return True
        
        return False
    except Exception as e:
        logger.error(f"Error checking if schema exists: {e}")
        return False


def check_table_exists(table_name: str, schema: str = "registry", client=None) -> bool:
    """
    Check if a specific table exists.
    
    Args:
        table_name: Name of the table to check
        schema: Schema name
        client: Optional Supabase client
        
    Returns:
        True if the table exists, False otherwise
    """
    if not SUPABASE_AVAILABLE and client is None:
        logger.error("Supabase client not available and no client provided.")
        return False
    
    try:
        # Get or use provided client
        supabase = client or get_supabase_client()
        
        # Check if the table exists by querying the information_schema
        result = supabase.rpc(
            'execute_sql',
            {'sql_statement': f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema}' AND table_name = '{table_name}'"}
        ).execute()
        
        # Check if we got any results
        if hasattr(result, 'data') and result.data and len(result.data) > 0:
            return True
        
        return False
    except Exception as e:
        logger.error(f"Error checking if table {schema}.{table_name} exists: {e}")
        return False


def setup_schema(client=None) -> bool:
    """
    Set up the database schema for the registry system.
    
    Args:
        client: Optional Supabase client
        
    Returns:
        True if successful, False otherwise
    """
    if not SUPABASE_AVAILABLE and client is None:
        logger.error("Supabase client not available and no client provided.")
        return False
    
    try:
        # Get or use provided client
        supabase = client or get_supabase_client()
        
        # Check if schema already exists
        if check_schema_exists(supabase):
            logger.info("Registry schema already exists")
            
            # Check if all required tables exist
            required_tables = {
                "registry": ["items", "configurations", "graphs", "dependencies", "environment_vars", "import_logs"],
                "components": ["embedding_models", "llm_models", "engine_templates", "state_templates", "tools", "toolkits"]
            }
            
            all_tables_exist = True
            for schema, tables in required_tables.items():
                for table in tables:
                    if not check_table_exists(table, schema, supabase):
                        logger.warning(f"Table {schema}.{table} does not exist")
                        all_tables_exist = False
            
            if all_tables_exist:
                logger.info("All required tables exist")
                return True
            else:
                logger.info("Some tables are missing, creating schema")
        else:
            logger.info("Registry schema does not exist, creating it")
        
        # Create the schema
        return execute_schema_sql(supabase)
    except Exception as e:
        logger.error(f"Error setting up schema: {e}")
        return False


def setup_execute_sql_function(client=None) -> bool:
    """
    Set up the execute_sql function in the database.
    This function is needed to execute arbitrary SQL statements.
    
    Args:
        client: Optional Supabase client
        
    Returns:
        True if successful, False otherwise
    """
    if not SUPABASE_AVAILABLE and client is None:
        logger.error("Supabase client not available and no client provided.")
        return False
    
    try:
        # Get or use provided client
        supabase = client or get_supabase_client()
        
        # SQL to create the execute_sql function
        sql = """
        CREATE OR REPLACE FUNCTION execute_sql(sql_statement TEXT)
        RETURNS JSONB
        LANGUAGE plpgsql
        SECURITY DEFINER
        AS $$
        DECLARE
            result JSONB;
        BEGIN
            EXECUTE sql_statement;
            result := json_build_object('success', true)::JSONB;
            RETURN result;
        EXCEPTION WHEN OTHERS THEN
            result := json_build_object(
                'success', false,
                'error', SQLERRM,
                'detail', SQLSTATE
            )::JSONB;
            RETURN result;
        END;
        $$;

        -- Grant execute permission to authenticated users
        GRANT EXECUTE ON FUNCTION execute_sql TO authenticated;
        """
        
        # Execute the SQL
        try:
            # First check if the function already exists
            check_result = supabase.rpc(
                'execute_sql',
                {'sql_statement': "SELECT 1 FROM pg_proc WHERE proname = 'execute_sql'"}
            ).execute()
            
            if hasattr(check_result, 'data') and check_result.data and len(check_result.data) > 0:
                logger.info("execute_sql function already exists")
                return True
            
            # If not, create it
            result = supabase.rpc(
                'execute_sql',
                {'sql_statement': sql}
            ).execute()
            
            if hasattr(result, 'error') and result.error:
                # If we got an error that the function doesn't exist, we need to create it
                # using a different approach - this would require direct PostgreSQL access
                logger.error(f"Error creating execute_sql function: {result.error}")
                logger.warning("Unable to create execute_sql function. This may require direct database access.")
                return False
            
            logger.info("execute_sql function created successfully")
            return True
        except Exception as e:
            logger.error(f"Error creating execute_sql function: {e}")
            logger.warning("Unable to create execute_sql function. This may require direct database access.")
            return False
    except Exception as e:
        logger.error(f"Error setting up execute_sql function: {e}")
        return False


def initialize_database(client=None) -> bool:
    """
    Initialize the database for the registry system.
    
    Args:
        client: Optional Supabase client
        
    Returns:
        True if successful, False otherwise
    """
    if not SUPABASE_AVAILABLE and client is None:
        logger.error("Supabase client not available and no client provided.")
        return False
    
    try:
        # Get or use provided client
        supabase = client or get_supabase_client()
        
        # Set up execute_sql function
        if not setup_execute_sql_function(supabase):
            logger.warning("Failed to set up execute_sql function. Database operations may be limited.")
        
        # Set up schema
        return setup_schema(supabase)
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        return False


# Save the schema SQL to a file on import
create_schema_sql()