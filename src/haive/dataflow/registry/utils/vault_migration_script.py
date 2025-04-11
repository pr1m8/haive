"""
Fixed Vault Reference Migration Script

This script migrates API keys and secrets to the vault schema,
using proper schema mapping with the existing table() helper function.
"""

import os
import uuid
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import Supabase client and helper functions
try:
    from src.haive.dataflow.db.supabase import get_supabase_client, table, sanitize_sql
    supabase = get_supabase_client()
except ImportError:
    logger.error("Cannot import Supabase client. Make sure it's properly installed and configured.")
    exit(1)


def execute_sql(sql: str) -> Any:
    """Execute SQL safely through Supabase RPC function."""
    try:
        # Sanitize SQL by removing trailing semicolons and whitespace
        sanitized_sql = sanitize_sql(sql)
        
        # Execute the SQL via the RPC function
        response = supabase.rpc("execute_sql", {"sql": sanitized_sql}).execute()
        
        # Check for errors in the response
        if hasattr(response, 'error') and response.error:
            logger.error(f"SQL execution error: {response.error}")
            return None
            
        return response
        
    except Exception as e:
        logger.error(f"Error executing SQL: {e}")
        return None


def ensure_vault_reference_column(table_name: str) -> bool:
    """
    Ensure the table has a vault_reference column for secret references.
    Uses table() helper function for proper schema resolution.
    
    Args:
        table_name: Full table name including schema
        
    Returns:
        True if column exists or was created, False otherwise
    """
    try:
        schema, table_base = table_name.split('.')
        
        # First, check if the column exists by testing information_schema
        # This is more reliable than checking the table data
        check_sql = f"""
        SELECT column_name FROM information_schema.columns
        WHERE table_schema = '{schema}' AND table_name = '{table_base}'
        AND column_name = 'vault_secret_id'
        """
        check_result = supabase.rpc("execute_sql", {"sql": sanitize_sql(check_sql)}).execute()
        
        if check_result.data and len(check_result.data) > 0:
            logger.info(f"Column vault_secret_id already exists in {table_name}")
            return True
        
        # If we get here, column doesn't exist, so add it
        add_column_sql = f"""
        ALTER TABLE {table_name} 
        ADD COLUMN IF NOT EXISTS vault_secret_id UUID REFERENCES vault.secrets(id)
        """
        
        result = supabase.rpc("execute_sql", {"sql": sanitize_sql(add_column_sql)}).execute()
        
        if hasattr(result, 'error') and result.error:
            logger.error(f"Failed to add column to {table_name}: {result.error}")
            return False
            
        logger.info(f"Added vault_secret_id column to {table_name}")
        
        # If this is engines.engines, also add config_vault_refs column
        if table_name == "engines.engines":
            add_refs_sql = """
            ALTER TABLE engines.engines 
            ADD COLUMN IF NOT EXISTS config_vault_refs JSONB DEFAULT '{}'::jsonb
            """
            
            refs_result = supabase.rpc("execute_sql", {"sql": sanitize_sql(add_refs_sql)}).execute()
            
            if hasattr(refs_result, 'error') and refs_result.error:
                logger.error(f"Failed to add config_vault_refs to engines.engines: {refs_result.error}")
            else:
                logger.info(f"Added config_vault_refs column to engines.engines")
            
        return True
        
    except Exception as e:
        logger.error(f"Error ensuring vault_reference column on {table_name}: {e}")
        logger.info(f"Please run this SQL in your database: ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS vault_secret_id UUID REFERENCES vault.secrets(id);")
        return False


def get_existing_vault_secrets() -> Dict[str, str]:
    """Get existing vault secrets to avoid duplicates."""
    try:
        # Query decrypted_secrets view to get names and IDs
        response = table(supabase, "vault.decrypted_secrets").select("id,name").execute()
        
        # Create a mapping of name to ID
        secrets_map = {}
        if response.data:
            for secret in response.data:
                secrets_map[secret['name']] = secret['id']
        
        return secrets_map
    except Exception as e:
        logger.error(f"Error fetching existing vault secrets: {e}")
        return {}


def create_vault_secret(name: str, description: str, value: Optional[str] = None) -> Optional[str]:
    """Create a new secret in the vault."""
    try:
        # If value is not provided, try to get from environment
        if value is None:
            value = os.getenv(name)
            if not value:
                logger.warning(f"No value found for secret {name} in environment")
                # Store placeholder for manual update later
                value = f"PLACEHOLDER: Set value for {name}"
        
        # Create the secret
        secret_data = {
            "name": name,
            "description": description,
            "secret": value,
            "created_at": datetime.now().isoformat()
        }
        
        response = table(supabase, "vault.secrets").insert(secret_data).execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]["id"]
        
        return None
    except Exception as e:
        logger.error(f"Error creating vault secret {name}: {e}")
        return None


def migrate_environment_variables() -> int:
    """
    Migrate config.environment_variables to use vault references.
    
    Returns:
        Number of environment variables migrated
    """
    try:
        # First check if environment_variables has the vault_secret_id column
        has_column = ensure_vault_reference_column("config.environment_variables")
        
        if not has_column:
            logger.warning("Cannot migrate environment variables without vault_secret_id column")
            logger.info("Please add the column manually and run the script again")
            return 0

        # Get existing vault secrets
        existing_secrets = get_existing_vault_secrets()
        logger.info(f"Found {len(existing_secrets)} existing secrets in vault")
        
        # Get all sensitive environment variables
        response = table(supabase, "config.environment_variables").select("*").eq("is_secret", True).execute()
        
        if not response.data:
            logger.info("No sensitive environment variables found")
            return 0
            
        env_vars = response.data
        logger.info(f"Found {len(env_vars)} sensitive environment variables")
        
        # Count of migrated variables
        migrated_count = 0
        
        # Process each environment variable
        for env_var in env_vars:
            try:
                env_name = env_var["name"]
                env_id = env_var["id"]
                
                # Skip if it already has a vault reference
                if env_var.get("vault_secret_id"):
                    logger.info(f"Environment variable {env_name} already has a vault reference")
                    continue
                    
                # Check if a secret already exists with this name
                if env_name in existing_secrets:
                    # Reference the existing secret
                    secret_id = existing_secrets[env_name]
                    logger.info(f"Using existing vault secret {env_name} ({secret_id})")
                else:
                    # Create new secret
                    description = env_var.get("description", f"API key for {env_name}")
                    # The secret value would be resolved from environment variables
                    secret_id = create_vault_secret(env_name, description)
                    
                    if not secret_id:
                        logger.error(f"Failed to create vault secret for {env_name}")
                        continue
                        
                    logger.info(f"Created new vault secret for {env_name} ({secret_id})")
                    # Update our existing secrets map
                    existing_secrets[env_name] = secret_id
                
                # Update the environment variable with the vault reference
                update_response = table(supabase, "config.environment_variables").update({
                    "vault_secret_id": secret_id,
                    "updated_at": datetime.now().isoformat()
                }).eq("id", env_id).execute()
                
                if update_response.data and len(update_response.data) > 0:
                    logger.info(f"Updated environment variable {env_name} to reference vault secret {secret_id}")
                    migrated_count += 1
                else:
                    logger.error(f"Failed to update environment variable {env_name}")
                
            except Exception as env_error:
                logger.error(f"Error processing environment variable: {env_error}")
            
        logger.info(f"Completed migration of {migrated_count} environment variables")
        return migrated_count
        
    except Exception as e:
        logger.error(f"Error migrating environment variables: {e}")
        return 0


def migrate_component_env_mappings() -> int:
    """
    Migrate component_env_mappings to include vault references.
    
    Returns:
        Number of mappings migrated
    """
    try:
        # First check if component_env_mappings has the vault_secret_id column
        has_column = ensure_vault_reference_column("config.component_env_mappings")
        
        if not has_column:
            logger.warning("Cannot migrate component environment mappings without vault_secret_id column")
            logger.info("Please add the column manually and run the script again")
            return 0

        # Get all component_env_mappings
        response = table(supabase, "config.component_env_mappings").select("*").execute()
        
        if not response.data:
            logger.info("No component environment mappings found")
            return 0
            
        mappings = response.data
        logger.info(f"Found {len(mappings)} component environment mappings")
        
        # Count of migrated mappings
        migrated_count = 0
        
        # Process each mapping
        for mapping in mappings:
            try:
                mapping_id = mapping["id"]
                
                # Skip if it already has a vault reference
                if mapping.get("vault_secret_id"):
                    continue
                    
                # Get the corresponding environment variable
                env_var_id = mapping.get("env_var_id")
                if not env_var_id:
                    logger.warning(f"No environment variable ID found for mapping {mapping_id}")
                    continue
                
                env_var_response = table(supabase, "config.environment_variables").select("name,vault_secret_id").eq("id", env_var_id).execute()
                
                if not env_var_response.data or len(env_var_response.data) == 0:
                    logger.warning(f"No environment variable found for mapping {mapping_id}")
                    continue
                    
                env_var = env_var_response.data[0]
                env_name = env_var.get("name")
                
                # Get the vault secret ID from the environment variable
                vault_secret_id = env_var.get("vault_secret_id")
                
                if not vault_secret_id:
                    logger.warning(f"Environment variable {env_name} has no vault reference")
                    continue
                    
                # Update the mapping with the vault reference
                update_response = table(supabase, "config.component_env_mappings").update({
                    "vault_secret_id": vault_secret_id,
                    "updated_at": datetime.now().isoformat()
                }).eq("id", mapping_id).execute()
                
                if update_response.data and len(update_response.data) > 0:
                    logger.info(f"Updated mapping {mapping_id} to reference vault secret {vault_secret_id}")
                    migrated_count += 1
                else:
                    logger.error(f"Failed to update mapping {mapping_id}")
                
            except Exception as mapping_error:
                logger.error(f"Error processing component env mapping: {mapping_error}")
            
        logger.info(f"Completed migration of {migrated_count} component environment mappings")
        return migrated_count
        
    except Exception as e:
        logger.error(f"Error migrating component environment mappings: {e}")
        return 0


def migrate_provider_api_keys() -> int:
    """
    Migrate provider API keys to vault references.
    
    Returns:
        Number of providers migrated
    """
    try:
        # First check if providers has the vault_secret_id column
        has_column = ensure_vault_reference_column("models.providers")
        
        if not has_column:
            logger.warning("Cannot migrate provider API keys without vault_secret_id column")
            logger.info("Please add the column manually and run the script again")
            return 0

        # Get existing vault secrets
        existing_secrets = get_existing_vault_secrets()
        
        # Get all providers
        response = table(supabase, "models.providers").select("*").execute()
        
        if not response.data:
            logger.info("No providers found")
            return 0
            
        providers = response.data
        logger.info(f"Found {len(providers)} providers")
        
        # Count of migrated providers
        migrated_count = 0
        
        # Process each provider
        for provider in providers:
            try:
                provider_id = provider["id"]
                provider_name = provider["name"]
                
                # Skip if it already has a vault reference
                if provider.get("vault_secret_id"):
                    continue
                    
                # Generate standard API key name
                api_key_name = f"{provider_name.upper()}_API_KEY"
                
                # Special cases
                if provider_name == "huggingface":
                    api_key_name = "HUGGING_FACE_API_KEY"
                elif provider_name == "google":
                    api_key_name = "GOOGLE_API_KEY"
                elif provider_name == "together_ai":
                    api_key_name = "TOGETHER_API_KEY"
                    
                # Check if a secret already exists with this name
                if api_key_name in existing_secrets:
                    # Reference the existing secret
                    secret_id = existing_secrets[api_key_name]
                    logger.info(f"Using existing vault secret {api_key_name} ({secret_id})")
                else:
                    # Create new secret
                    description = f"API key for {provider_name} provider"
                    # The secret value would be resolved from environment variables
                    secret_id = create_vault_secret(api_key_name, description)
                    
                    if not secret_id:
                        logger.error(f"Failed to create vault secret for {api_key_name}")
                        continue
                        
                    logger.info(f"Created new vault secret for {api_key_name} ({secret_id})")
                    # Update our existing secrets map
                    existing_secrets[api_key_name] = secret_id
                
                # Update the provider with the vault reference
                update_response = table(supabase, "models.providers").update({
                    "vault_secret_id": secret_id,
                    "updated_at": datetime.now().isoformat()
                }).eq("id", provider_id).execute()
                
                if update_response.data and len(update_response.data) > 0:
                    logger.info(f"Updated provider {provider_name} to reference vault secret {secret_id}")
                    migrated_count += 1
                else:
                    logger.error(f"Failed to update provider {provider_name}")
                
            except Exception as provider_error:
                logger.error(f"Error processing provider: {provider_error}")
            
        logger.info(f"Completed migration of {migrated_count} providers")
        return migrated_count
        
    except Exception as e:
        logger.error(f"Error migrating provider API keys: {e}")
        return 0


def migrate_engine_api_keys() -> int:
    """
    Migrate engine API keys to vault references.
    
    Returns:
        Number of engines with API keys migrated
    """
    try:
        # First check if engines has the vault_secret_id column
        has_column = ensure_vault_reference_column("engines.engines")
        
        if not has_column:
            logger.warning("Cannot migrate engine API keys without vault_secret_id column")
            logger.info("Please add the column manually and run the script again")
            return 0

        # Get existing vault secrets
        existing_secrets = get_existing_vault_secrets()
        
        # Get all engines
        response = table(supabase, "engines.engines").select("*").execute()
        
        if not response.data:
            logger.info("No engines found")
            return 0
            
        engines = response.data
        logger.info(f"Found {len(engines)} engines")
        
        # Count of engines with API keys
        migrated_count = 0
        
        # Process each engine
        for engine in engines:
            try:
                engine_id = engine["id"]
                engine_name = engine["name"]
                
                # Skip if it already has a vault reference
                if engine.get("vault_secret_id"):
                    continue
                    
                # Check if the engine config contains API keys
                config = engine.get("config", {})
                if isinstance(config, str):
                    try:
                        config = json.loads(config)
                    except:
                        config = {}
                        
                # Look for API keys in the config
                api_keys = {}
                
                # Common API key patterns
                api_key_patterns = ["api_key", "apiKey", "token", "secret"]
                
                # Recursively find API keys in the config
                def find_api_keys(obj, prefix=""):
                    if isinstance(obj, dict):
                        for key, value in obj.items():
                            # Check if this is an API key
                            if any(pattern in key.lower() for pattern in api_key_patterns) and isinstance(value, str):
                                api_keys[f"{prefix}{key}"] = value
                            # Recursively check nested objects
                            find_api_keys(value, f"{prefix}{key}.")
                            
                find_api_keys(config)
                
                if not api_keys:
                    logger.info(f"No API keys found in engine {engine_name}")
                    continue
                    
                logger.info(f"Found {len(api_keys)} API keys in engine {engine_name}")
                
                # Create vault secrets for each API key
                for key, value in api_keys.items():
                    # Generate a secret name
                    secret_name = f"{engine_name.upper()}_{key.upper().replace('.', '_')}"
                    
                    # Check if a secret already exists with this name
                    if secret_name in existing_secrets:
                        # Reference the existing secret
                        secret_id = existing_secrets[secret_name]
                        logger.info(f"Using existing vault secret {secret_name} ({secret_id})")
                    else:
                        # Create new secret
                        description = f"API key for {engine_name} engine: {key}"
                        secret_id = create_vault_secret(secret_name, description, value)
                        
                        if not secret_id:
                            logger.error(f"Failed to create vault secret for {secret_name}")
                            continue
                            
                        logger.info(f"Created new vault secret for {secret_name} ({secret_id})")
                        # Update our existing secrets map
                        existing_secrets[secret_name] = secret_id
                    
                    # Update the config to reference the vault secret
                    # Here we're adding a new field to track the vault reference
                    # In a real system, you'd modify the code that uses this config
                    # to resolve the vault reference at runtime
                    config_vault_refs = engine.get("config_vault_refs", {})
                    if isinstance(config_vault_refs, str):
                        try:
                            config_vault_refs = json.loads(config_vault_refs)
                        except:
                            config_vault_refs = {}
                            
                    config_vault_refs[key] = secret_id
                    
                    # Update the engine with the vault references
                    update_response = table(supabase, "engines.engines").update({
                        "config_vault_refs": json.dumps(config_vault_refs),
                        "updated_at": datetime.now().isoformat()
                    }).eq("id", engine_id).execute()
                    
                    if update_response.data and len(update_response.data) > 0:
                        logger.info(f"Updated engine {engine_name} to reference vault secret {secret_id} for key {key}")
                    else:
                        logger.error(f"Failed to update engine {engine_name}")
                
                migrated_count += 1
                
            except Exception as engine_error:
                logger.error(f"Error processing engine: {engine_error}")
            
        logger.info(f"Completed migration of {migrated_count} engines")
        return migrated_count
        
    except Exception as e:
        logger.error(f"Error migrating engine API keys: {e}")
        return 0


def add_vault_helper_functions() -> bool:
    """
    Add helper functions to resolve vault references.
    
    Returns:
        True if successful, False if SQL should be run manually
    """
    try:
        # Create the get_vault_secret function
        secret_func_sql = """
        CREATE OR REPLACE FUNCTION get_vault_secret(secret_id UUID)
        RETURNS TEXT
        LANGUAGE plpgsql
        SECURITY DEFINER
        AS $$
        DECLARE
            secret_value TEXT;
        BEGIN
            SELECT decrypted_secret INTO secret_value
            FROM vault.decrypted_secrets
            WHERE id = secret_id;
            
            RETURN secret_value;
        END;
        $$;
        """
        
        # Execute the SQL
        result = supabase.rpc("execute_sql", {"sql": sanitize_sql(secret_func_sql)}).execute()
        
        if hasattr(result, 'error') and result.error:
            logger.warning(f"Failed to create get_vault_secret function: {result.error}")
            return False
            
        # Create the get_vault_secret_by_name function
        name_func_sql = """
        CREATE OR REPLACE FUNCTION get_vault_secret_by_name(secret_name TEXT)
        RETURNS TEXT
        LANGUAGE plpgsql
        SECURITY DEFINER
        AS $$
        DECLARE
            secret_value TEXT;
        BEGIN
            SELECT decrypted_secret INTO secret_value
            FROM vault.decrypted_secrets
            WHERE name = secret_name;
            
            RETURN secret_value;
        END;
        $$;
        """
        
        # Execute the SQL
        result = supabase.rpc("execute_sql", {"sql": sanitize_sql(name_func_sql)}).execute()
        
        if hasattr(result, 'error') and result.error:
            logger.warning(f"Failed to create get_vault_secret_by_name function: {result.error}")
            return False
            
        logger.info("Successfully created vault helper functions")
        return True
        
    except Exception as e:
        logger.error(f"Error creating vault helper functions: {e}")
        
        # Print the SQL for manual execution
        logger.info("Please add the following helper functions to your database manually:")
        logger.info("""
        -- Function to get a secret value from vault
        CREATE OR REPLACE FUNCTION get_vault_secret(secret_id UUID)
        RETURNS TEXT
        LANGUAGE plpgsql
        SECURITY DEFINER
        AS $$
        DECLARE
            secret_value TEXT;
        BEGIN
            SELECT decrypted_secret INTO secret_value
            FROM vault.decrypted_secrets
            WHERE id = secret_id;
            
            RETURN secret_value;
        END;
        $$;
        
        -- Function to get a secret value by name
        CREATE OR REPLACE FUNCTION get_vault_secret_by_name(secret_name TEXT)
        RETURNS TEXT
        LANGUAGE plpgsql
        SECURITY DEFINER
        AS $$
        DECLARE
            secret_value TEXT;
        BEGIN
            SELECT decrypted_secret INTO secret_value
            FROM vault.decrypted_secrets
            WHERE name = secret_name;
            
            RETURN secret_value;
        END;
        $$;
        """)
        
        return False


def main():
    """Main function to run the migration."""
    logger.info("Starting vault reference migration...")
    
    # Track overall success
    success = True
    total_migrated = 0
    
    # 1. First, migrate environment variables
    logger.info("Migrating environment variables...")
    env_count = migrate_environment_variables()
    total_migrated += env_count
    
    # 2. Update component environment mappings
    logger.info("Migrating component environment mappings...")
    mapping_count = migrate_component_env_mappings()
    total_migrated += mapping_count
    
    # 3. Migrate provider API keys
    logger.info("Migrating provider API keys...")
    provider_count = migrate_provider_api_keys()
    total_migrated += provider_count
    
    # 4. Migrate engine API keys
    logger.info("Migrating engine API keys...")
    engine_count = migrate_engine_api_keys()
    total_migrated += engine_count
    
    # 5. Add helper functions for accessing vault secrets
    logger.info("Adding vault helper functions...")
    func_success = add_vault_helper_functions()
    
    if not func_success:
        success = False
    
    # Report results
    logger.info("Migration completed with the following results:")
    logger.info(f"Environment variables migrated: {env_count}")
    logger.info(f"Component environment mappings migrated: {mapping_count}")
    logger.info(f"Providers migrated: {provider_count}")
    logger.info(f"Engines migrated: {engine_count}")
    logger.info(f"Total items migrated: {total_migrated}")
    
    if success and total_migrated > 0:
        logger.info("Migration was SUCCESSFUL")
        return 0
    elif total_migrated > 0:
        logger.info("Migration was PARTIALLY SUCCESSFUL")
        return 1
    else:
        logger.warning("Migration did not complete successfully")
        return 2


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)