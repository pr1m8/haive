"""
Model Registry Client for Haive.

This module provides a client interface for working with the registry system
to access LLM and embedding models with dynamic environment variable detection.
"""

import os
import json
import logging
import inspect
from typing import Dict, Any, List, Optional, Union, Tuple, Type, Set
from pydantic import BaseModel, create_model, Field

# Import supabase client utilities
from src.haive.dataflow.db.supabase import get_supabase_client, table

# Import LLM core models for environment variable inspection
try:
    from src.haive.core.models.llm.base import SecureConfigMixin, LLMConfig
    from src.haive.core.models.llm.provider_types import LLMProvider
    CORE_LLM_AVAILABLE = True
except ImportError:
    CORE_LLM_AVAILABLE = False
    logging.warning("Core LLM models not available - some functionality will be limited")

# Set up logging
logger = logging.getLogger(__name__)


class ModelRegistry:
    """
    Client for working with registered LLM and embedding models.
    """
    
    def __init__(self):
        """Initialize the model registry client."""
        self._supabase = None
        self._llm_models_cache = []
        self._embedding_models_cache = []
        
        try:
            self._supabase = get_supabase_client()
            logger.info("✅ Initialized Supabase connection for model registry")
        except Exception as e:
            logger.warning(f"Could not initialize Supabase connection: {e}")
            import traceback
            logger.debug(f"Supabase init error traceback: {traceback.format_exc()}")
        
        # Load model data from importers
        self._load_model_data()
        
        # Scan environment variables on initialization
        self.update_provider_availability()
    
    def _load_model_data(self):
        """Load model data from importers."""
        # Try to import embedding models data
        try:
            from src.haive.dataflow.registry.importers.embeddings_importer import EMBEDDING_MODELS
            logger.info(f"Loaded {len(EMBEDDING_MODELS)} embedding models from embeddings_importer")
            self._embedding_models_cache = EMBEDDING_MODELS
        except ImportError:
            logger.warning("Could not import embedding models data")
        
        # Try to load LLM models data
        try:
            # LiteLLM importer doesn't have a static list like embedding_importer
            # Instead it fetches from GitHub, so we'll need to use this data
            # differently. For now, we'll rely on the database for LLM models.
            pass
        except ImportError:
            logger.warning("Could not import LLM models data")
    
    def update_provider_availability(self):
        """
        Scan environment variables and update provider availability status.
        """
        # Get all required environment variables by scanning the core LLM implementations
        env_vars = self.get_required_environment_vars()
        
        # Check which ones are available in the current environment
        available_vars = []
        for env_var in env_vars:
            var_name = env_var.get("var_name")
            if var_name and os.getenv(var_name):
                available_vars.append(var_name)
                logger.debug(f"Environment variable found: {var_name}")
        
        # Update provider availability in the database
        if self._supabase:
            try:
                # Update LLM providers in models schema
                llm_providers = table(self._supabase, "models.providers").select("*").execute()
                if llm_providers.data:
                    for provider in llm_providers.data:
                        # Check if any env vars for this provider
                        provider_name = provider.get("name")
                        matching_env_vars = [var for var in env_vars if var.get("provider_name") == provider_name]
                        
                        env_var_names = [var.get("var_name") for var in matching_env_vars]
                        is_available = any(env_name in available_vars for env_name in env_var_names if env_name)
                        
                        # Update provider status
                        table(self._supabase, "models.providers").update({
                            "is_available": is_available,
                            "updated_at": "NOW()"
                        }).eq("id", provider["id"]).execute()
                
                logger.info("Provider availability updated based on environment variables")
                
            except Exception as e:
                logger.error(f"Error updating provider availability: {e}")
    
    def get_required_environment_vars(self) -> List[Dict[str, Any]]:
        """
        Scan source code to detect environment variables used by LLM providers.
        
        Returns:
            List of environment variables with provider mapping
        """
        env_vars = []
        
        # If core LLM models aren't available, return empty list
        if not CORE_LLM_AVAILABLE:
            logger.warning("Core LLM models not available - cannot detect environment variables")
            return env_vars
            
        # Get the LLMProvider enum values
        provider_values = {e.value: e.name for e in LLMProvider}
        
        # Extract all subclasses of LLMConfig to find environment variable usage
        llm_config_classes = self._get_llm_config_subclasses()
        
        # Extra handling for specific environment variables that might be missed
        special_mappings = {
            "GEMINI": ["GOOGLE_API_KEY", "GEMINI_API_KEY"],  # Check both possible env vars for Gemini
            "MISTRALAI": ["MISTRAL_API_KEY"],
            "OPENAI": ["OPENAI_API_KEY"],
            "AZURE": ["AZURE_OPENAI_API_KEY"],
            "ANTHROPIC": ["ANTHROPIC_API_KEY", "CLAUDE_API_KEY"]
        }
        
        # Check each class for environment variable references
        for cls in llm_config_classes:
            provider_value = None
            provider_name = None
            
            # Try to get the provider value from the class
            try:
                provider_attr = getattr(cls, 'provider', None)
                if provider_attr and hasattr(provider_attr, 'value'):
                    provider_value = provider_attr.value
                    provider_name = provider_value
            except Exception:
                pass
                
            if not provider_name:
                continue
                
            # Look through class attributes to find SecretStr fields with default_factory
            for attr_name, attr_value in cls.__annotations__.items():
                if attr_name == 'api_key':
                    # Try to find the default_factory lambda that references os.getenv
                    field_info = cls.__fields__[attr_name] if hasattr(cls, '__fields__') else None
                    if field_info and hasattr(field_info, 'default_factory'):
                        default_factory = field_info.default_factory
                        source_code = inspect.getsource(default_factory)
                        
                        # Extract environment variable names using a simple approach
                        # Looking for patterns like: os.getenv("ENV_VAR_NAME", "")
                        import re
                        env_var_matches = re.findall(r'os\.getenv\(["\']([A-Z0-9_]+)["\']', source_code)
                        
                        for env_var_name in env_var_matches:
                            env_vars.append({
                                "var_name": env_var_name,
                                "provider_name": provider_name,
                                "is_required": True,
                                "description": f"API key for {provider_name.title()} provider"
                            })
                            logger.debug(f"Detected environment variable: {env_var_name} for provider {provider_name}")
        
        # Add special mappings for providers that might be missed
        for provider, env_var_names in special_mappings.items():
            provider_lower = provider.lower()
            
            # Check if we already have this provider in our env vars
            has_provider = any(var.get("provider_name", "").lower() == provider_lower for var in env_vars)
            
            # If not found or provider is Gemini (we want to ensure both env vars are checked)
            if not has_provider or provider_lower == "gemini":
                for env_var_name in env_var_names:
                    # Check if this specific env var is already registered
                    has_var = any(var.get("var_name") == env_var_name for var in env_vars)
                    if not has_var:
                        env_vars.append({
                            "var_name": env_var_name,
                            "provider_name": provider_lower,
                            "is_required": True,
                            "description": f"API key for {provider.title()} provider"
                        })
                        logger.debug(f"Added special mapping: {env_var_name} for provider {provider_lower}")
        
        # If we couldn't extract any from the code, fall back to secure config mixin mapping
        if not env_vars and hasattr(SecureConfigMixin, '_validate_api_key'):
            # Extract environment variable mapping from the secure config mixin
            source_code = inspect.getsource(SecureConfigMixin._validate_api_key)
            
            # Extract the env_key_map dictionary
            import re
            env_map_match = re.search(r'env_key_map\s*=\s*{([^}]+)}', source_code, re.DOTALL)
            
            if env_map_match:
                env_map_str = env_map_match.group(1)
                
                # Parse the environment variable mapping
                provider_env_pairs = re.findall(r'["\']([a-z0-9_]+)["\']:\s*["\']([A-Z0-9_]+)["\']', env_map_str)
                
                for provider_name, env_var_name in provider_env_pairs:
                    env_vars.append({
                        "var_name": env_var_name,
                        "provider_name": provider_name,
                        "is_required": True,
                        "description": f"API key for {provider_name.title()} provider"
                    })
                    logger.debug(f"Extracted environment variable from SecureConfigMixin: {env_var_name} for provider {provider_name}")
        
        # Check existing environment variables to see which ones are set
        # This is helpful for debugging and may catch variables not found by code analysis
        for env_name in os.environ:
            if any(term in env_name for term in ["API_KEY", "TOKEN", "SECRET"]):
                # Try to match to a provider
                provider_match = None
                
                # Common provider patterns in env var names
                patterns = {
                    "openai": ["OPENAI"],
                    "anthropic": ["ANTHROPIC", "CLAUDE"],
                    "gemini": ["GEMINI", "GOOGLE"],
                    "mistralai": ["MISTRAL"],
                    "azure": ["AZURE"],
                    "deepseek": ["DEEPSEEK"],
                    "groq": ["GROQ"],
                    "cohere": ["COHERE"],
                    "fireworks_ai": ["FIREWORKS"],
                    "together_ai": ["TOGETHER"],
                    "replicate": ["REPLICATE"]
                }
                
                for provider, prefixes in patterns.items():
                    if any(env_name.startswith(prefix) for prefix in prefixes):
                        provider_match = provider
                        break
                
                if provider_match:
                    # Check if we already have this environment variable
                    has_var = any(var.get("var_name") == env_name for var in env_vars)
                    if not has_var:
                        env_vars.append({
                            "var_name": env_name,
                            "provider_name": provider_match,
                            "is_required": True,
                            "description": f"API key for {provider_match.title()} provider (auto-detected)"
                        })
                        logger.debug(f"Auto-detected environment variable: {env_name} for provider {provider_match}")
                    
        # Register these environment variables in config
        if self._supabase and env_vars:
            self._register_environment_vars_in_vault(env_vars)
                    
        return env_vars
    
    def _get_llm_config_subclasses(self) -> List[Type]:
        """Get all subclasses of LLMConfig"""
        if not CORE_LLM_AVAILABLE:
            return []
            
        def get_all_subclasses(cls):
            all_subclasses = []
            for subclass in cls.__subclasses__():
                all_subclasses.append(subclass)
                all_subclasses.extend(get_all_subclasses(subclass))
            return all_subclasses
            
        return get_all_subclasses(LLMConfig)
        
    def _register_environment_vars_in_vault(self, env_vars: List[Dict[str, Any]]):
        """
        Register detected environment variables in the config table.
        Also securely store actual values in the vault schema if present.
        """
        try:
            # For each env var, register or update in config.environment_variables
            for env_var in env_vars:
                var_name = env_var.get("var_name")
                if not var_name:
                    continue
                    
                # Check if this env var already exists
                existing_vars = table(self._supabase, "config.environment_variables").select("*").eq("name", var_name).execute()
                
                env_var_id = None
                if existing_vars.data and len(existing_vars.data) > 0:
                    env_var_id = existing_vars.data[0].get("id")
                else:
                    # Create new entry using only columns that exist in the schema
                    insert_result = table(self._supabase, "config.environment_variables").insert({
                        "name": var_name,
                        "display_name": f"{env_var.get('provider_name', '').title()} API Key",
                        "description": env_var.get("description", "API key for provider"),
                        "is_secret": True,
                        "is_required": env_var.get("is_required", True),
                        "created_at": "NOW()",
                        "updated_at": "NOW()"
                    }).execute()
                    
                    if insert_result.data and len(insert_result.data) > 0:
                        env_var_id = insert_result.data[0].get("id")
                    
                    logger.info(f"Registered environment variable: {var_name}")

                # Create or update provider entry if needed
                provider_name = env_var.get("provider_name")
                if provider_name:
                    # Check if provider exists
                    provider_response = table(self._supabase, "models.providers").select("*").eq("name", provider_name).execute()
                    
                    provider_id = None
                    if provider_response.data and len(provider_response.data) > 0:
                        provider_id = provider_response.data[0].get("id")
                        # Update is_available
                        is_available = bool(os.getenv(var_name))
                        table(self._supabase, "models.providers").update({
                            "is_available": is_available,
                            "updated_at": "NOW()"
                        }).eq("id", provider_id).execute()
                    else:
                        # Get or create provider type
                        provider_type_response = table(self._supabase, "models.provider_types").select("*").eq("name", "llm").execute()
                        provider_type_id = None
                        
                        if provider_type_response.data and len(provider_type_response.data) > 0:
                            provider_type_id = provider_type_response.data[0].get("id")
                        else:
                            # Create provider type if not exists
                            provider_type_insert = table(self._supabase, "models.provider_types").insert({
                                "name": "llm",
                                "display_name": "LLM Provider",
                                "description": "Provider for Large Language Models",
                                "created_at": "NOW()"
                            }).execute()
                            
                            if provider_type_insert.data and len(provider_type_insert.data) > 0:
                                provider_type_id = provider_type_insert.data[0].get("id")
                        
                        if provider_type_id:
                            # Create provider
                            provider_insert = table(self._supabase, "models.providers").insert({
                                "type_id": provider_type_id,
                                "name": provider_name,
                                "display_name": provider_name.title(),
                                "description": f"Provider for {provider_name.title()} models",
                                "is_available": bool(os.getenv(var_name)),
                                "created_at": "NOW()",
                                "updated_at": "NOW()"
                            }).execute()
                            
                            if provider_insert.data and len(provider_insert.data) > 0:
                                provider_id = provider_insert.data[0].get("id")
                    
                    # Store the actual value in vault if available (for current user)
                    if env_var_id and provider_id:
                        self._store_secret_in_vault(env_var_id, var_name, provider_id)
                    
        except Exception as e:
            logger.error(f"Error registering environment variables: {e}")
            
    def _store_secret_in_vault(self, env_var_id: str, var_name: str, provider_id: str = None):
        """
        Securely store the secret value in the vault schema.
        
        Args:
            env_var_id: ID of the environment variable
            var_name: Name of the environment variable
            provider_id: Optional provider ID
        """
        # Only store if the value is available in the environment
        value = os.getenv(var_name)
        if not value:
            return
            
        try:
            # Check if the vault.user_env_secrets table exists
            try:
                current_user_id = self._get_current_user_id()
                if not current_user_id:
                    return
                    
                # Check if entry already exists
                existing = table(self._supabase, "vault.user_env_secrets").select("id").eq("user_id", current_user_id).eq("env_var_id", env_var_id).execute()
                
                if existing.data and len(existing.data) > 0:
                    # Update existing entry
                    table(self._supabase, "vault.user_env_secrets").update({
                        "secret_value": value,  # This should be encrypted by Supabase Vault
                        "updated_at": "NOW()"
                    }).eq("id", existing.data[0].get("id")).execute()
                    logger.info(f"Updated secret value for {var_name} in vault")
                else:
                    # Create new entry
                    table(self._supabase, "vault.user_env_secrets").insert({
                        "user_id": current_user_id,
                        "env_var_id": env_var_id,
                        "secret_value": value,  # This should be encrypted by Supabase Vault
                        "created_at": "NOW()",
                        "updated_at": "NOW()"
                    }).execute()
                    logger.info(f"Stored secret value for {var_name} in vault")
                    
                # If we have a provider ID, also store in team_env_secrets for the default team
                if provider_id:
                    default_team_id = self._get_default_team_id(current_user_id)
                    if default_team_id:
                        # Check if entry already exists
                        existing_team = table(self._supabase, "vault.team_env_secrets").select("id").eq("team_id", default_team_id).eq("env_var_id", env_var_id).execute()
                        
                        if existing_team.data and len(existing_team.data) > 0:
                            # Update existing entry
                            table(self._supabase, "vault.team_env_secrets").update({
                                "secret_value": value,
                                "updated_at": "NOW()"
                            }).eq("id", existing_team.data[0].get("id")).execute()
                        else:
                            # Create new entry
                            table(self._supabase, "vault.team_env_secrets").insert({
                                "team_id": default_team_id,
                                "env_var_id": env_var_id,
                                "secret_value": value,
                                "created_by": current_user_id,
                                "created_at": "NOW()",
                                "updated_at": "NOW()"
                            }).execute()
                
            except Exception as e:
                if "relation" in str(e) and "does not exist" in str(e):
                    logger.warning(f"Vault tables don't exist: {e}")
                else:
                    raise
                    
        except Exception as e:
            logger.error(f"Error storing secret in vault: {e}")
    
    def _get_current_user_id(self) -> Optional[str]:
        """Get the current authenticated user ID."""
        if not self._supabase:
            return None
            
        try:
            # Get current user info
            response = self._supabase.auth.get_user()
            if response and hasattr(response, 'user') and response.user:
                return response.user.id
        except Exception as e:
            logger.warning(f"Could not get current user ID: {e}")
            
        return None
        
    def _get_default_team_id(self, user_id: str) -> Optional[str]:
        """Get the default team ID for a user."""
        if not self._supabase or not user_id:
            return None
            
        try:
            # Try to find a team where the user is an owner or admin
            team_response = table(self._supabase, "public.team_members").select("team_id").eq("user_id", user_id).in_("role", ["owner", "admin"]).limit(1).execute()
            
            if team_response.data and len(team_response.data) > 0:
                return team_response.data[0].get("team_id")
        except Exception as e:
            logger.warning(f"Could not get default team ID: {e}")
            
        return None
        
    def get_secret_from_vault(self, var_name: str) -> Optional[str]:
        """
        Get a secret value from the vault.
        
        Args:
            var_name: Name of the environment variable
            
        Returns:
            Secret value or None if not found
        """
        # First try from environment
        env_value = os.getenv(var_name)
        if env_value:
            return env_value
            
        if not self._supabase:
            return None
            
        try:
            # Get the environment variable ID
            env_var_response = table(self._supabase, "config.environment_variables").select("id").eq("name", var_name).execute()
            
            if not env_var_response.data or len(env_var_response.data) == 0:
                return None
                
            env_var_id = env_var_response.data[0].get("id")
            current_user_id = self._get_current_user_id()
            
            if not current_user_id:
                return None
                
            # Try to get from user secrets
            user_secret_response = table(self._supabase, "vault.user_env_secrets").select("secret_value").eq("user_id", current_user_id).eq("env_var_id", env_var_id).execute()
            
            if user_secret_response.data and len(user_secret_response.data) > 0:
                return user_secret_response.data[0].get("secret_value")
                
            # Try to get from team secrets
            default_team_id = self._get_default_team_id(current_user_id)
            
            if default_team_id:
                team_secret_response = table(self._supabase, "vault.team_env_secrets").select("secret_value").eq("team_id", default_team_id).eq("env_var_id", env_var_id).execute()
                
                if team_secret_response.data and len(team_secret_response.data) > 0:
                    return team_secret_response.data[0].get("secret_value")
                    
        except Exception as e:
            logger.error(f"Error getting secret from vault: {e}")
            
        return None
    
    def get_available_llm_providers(self) -> List[Dict[str, Any]]:
        """
        Get all available LLM providers.
        
        Returns:
            List of available LLM providers
        """
        # Always run an availability check to ensure it's up to date
        self.update_provider_availability()
        
        if self._supabase:
            try:
                # Query for available providers directly from models schema using RPC
                # This approach should be more reliable than the table method
                sql = "SELECT * FROM models.providers WHERE is_available = true"
                response = self._supabase.rpc("execute_sql", {"sql": sql}).execute()
                
                if response.data:
                    return response.data
                    
            except Exception as e:
                logger.error(f"Error retrieving available LLM providers using RPC: {e}")
                
                # Try the table method as a fallback
                try:
                    from src.haive.dataflow.db.supabase import table
                    response = table(self._supabase, "models.providers").select("*").eq("is_available", True).execute()
                    if response.data:
                        return response.data
                except Exception as table_e:
                    logger.error(f"Error retrieving providers with table method: {table_e}")
        
        # Fall back to environment variable detection
        env_vars = self.get_required_environment_vars()
        available_providers = set()
        
        for var in env_vars:
            if os.getenv(var.get("var_name")):
                available_providers.add(var.get("provider_name"))
        
        return [{"name": p, "is_available": True} for p in available_providers]
    
    def get_available_embedding_providers(self) -> List[Dict[str, Any]]:
        """
        Get all available embedding providers.
        
        Returns:
            List of available embedding providers
        """
        # Always run an availability check to ensure it's up to date
        self.update_provider_availability()
        
        if self._supabase:
            try:
                # Query for available embedding providers using RPC
                sql = """
                SELECT p.* 
                FROM models.providers p
                JOIN models.provider_types pt ON p.type_id = pt.id
                WHERE p.is_available = true AND pt.name = 'embedding'
                """
                response = self._supabase.rpc("execute_sql", {"sql": sql}).execute()
                
                if response.data:
                    return response.data
                    
            except Exception as e:
                logger.error(f"Error retrieving available embedding providers using RPC: {e}")
                
                # Try the table method as a fallback
                try:
                    from src.haive.dataflow.db.supabase import table
                    # Get providers that have embedding models
                    embedding_providers = []
                    
                    # First get available providers
                    providers_response = table(self._supabase, "models.providers").select("*").eq("is_available", True).execute()
                    
                    if providers_response.data:
                        # Filter to only providers with embedding models
                        for provider in providers_response.data:
                            # Check if provider has embedding models
                            provider_id = provider.get("id")
                            if provider_id:
                                models_response = table(self._supabase, "models.embedding_models").select("id").eq("provider_id", provider_id).limit(1).execute()
                                if models_response.data and len(models_response.data) > 0:
                                    embedding_providers.append(provider)
                        
                        return embedding_providers
                except Exception as table_e:
                    logger.error(f"Error retrieving embedding providers with table method: {table_e}")
        
        # Fall back to environment variable detection
        env_vars = self.get_required_environment_vars()
        available_providers = set()
        
        for var in env_vars:
            if os.getenv(var.get("var_name")):
                available_providers.add(var.get("provider_name"))
        
        return [{"name": p, "is_available": True} for p in available_providers]
    
    def normalize_model_data(self, model: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize model data to ensure consistent field access.
        
        Args:
            model: Model data to normalize
            
        Returns:
            Normalized model data
        """
        # Create a copy to avoid modifying the original
        normalized = dict(model)
        
        # Extract metadata and ensure it's a dictionary
        metadata = normalized.get("metadata", {})
        if isinstance(metadata, str):
            try:
                metadata = json.loads(metadata)
            except:
                metadata = {}
        
        normalized["metadata"] = metadata
        
        # Ensure all important fields are at the top level
        key_fields = [
            "model_id", "provider", "model_name", "max_tokens", 
            "dimensions", "max_input_tokens", "deprecation_date"
        ]
        
        # Copy important fields from metadata to top level if not already present
        for field in key_fields:
            if field not in normalized and field in metadata:
                normalized[field] = metadata[field]
        
        # Also copy key nested structures if they exist
        for nested_field in ["capabilities", "pricing"]:
            if nested_field in metadata and nested_field not in normalized:
                normalized[nested_field] = metadata[nested_field]
        
        return normalized
    
    def get_llm_models(self, provider: Optional[str] = None, only_available: bool = False) -> List[Dict[str, Any]]:
        """
        Get all LLM models, optionally filtered by provider.
        
        Args:
            provider: Optional provider name to filter by
            only_available: If True, only return models from available providers
            
        Returns:
            List of LLM model data
        """
        # Get available providers if filtering by availability
        available_providers = []
        if only_available:
            available_providers = [p["name"] for p in self.get_available_llm_providers()]
        
        results = []
        
        # First try to get models from database
        if self._supabase:
            try:
                logger.debug(f"Fetching LLM models with provider={provider}, only_available={only_available}")
                
                # Build SQL query with proper filtering
                where_clause = ""
                if provider:
                    where_clause = f"WHERE p.name = '{provider.replace('\'', '\'\'')}'"
                elif only_available and available_providers:
                    # Format provider names for SQL IN clause with proper escaping
                    provider_names = "', '".join([p.replace("'", "''") for p in available_providers])
                    where_clause = f"WHERE p.name IN ('{provider_names}')"
                
                # Use a simpler joined query that should work with RPC
                sql = f"""
                SELECT m.*, p.name as provider_name
                FROM models.llm_models m
                JOIN models.providers p ON m.provider_id = p.id
                {where_clause}
                """
                
                logger.debug(f"Executing SQL: {sql}")
                
                # Execute SQL via RPC
                response = self._supabase.rpc("execute_sql", {"sql": sql}).execute()
                
                if response.data:
                    # Normalize each model's structure
                    for model in response.data:
                        # Add provider name
                        if "provider_name" in model and "provider" not in model:
                            model["provider"] = model["provider_name"]
                            
                        normalized_model = self.normalize_model_data(model)
                        results.append(normalized_model)
                    
                    if results:
                        return results
                    
            except Exception as e:
                logger.error(f"Error retrieving LLM models from database: {e}")
                import traceback
                logger.debug(f"Get models error traceback: {traceback.format_exc()}")
        
        # If database query didn't return results, try to import models directly
        if not results:
            try:
                # Try to run the litellm import
                from src.haive.dataflow.registry.importers.litellm_importer import import_llm_models
                
                # Run the import if needed (this will populate the database)
                import_success = import_llm_models()
                if import_success:
                    logger.info("Successfully imported LLM models from LiteLLM")
                    
                    # Retry database query after import
                    if self._supabase:
                        try:
                            sql = f"""
                            SELECT m.*, p.name as provider_name
                            FROM models.llm_models m
                            JOIN models.providers p ON m.provider_id = p.id
                            """
                            response = self._supabase.rpc("execute_sql", {"sql": sql}).execute()
                            
                            if response.data:
                                for model in response.data:
                                    if "provider_name" in model and "provider" not in model:
                                        model["provider"] = model["provider_name"]
                                    
                                    # Apply filters
                                    if provider and model.get("provider") != provider:
                                        continue
                                    
                                    if only_available and model.get("provider") not in available_providers:
                                        continue
                                    
                                    normalized_model = self.normalize_model_data(model)
                                    results.append(normalized_model)
                        except Exception as e:
                            logger.error(f"Error retrieving models after import: {e}")
            except Exception as import_e:
                logger.error(f"Error importing LLM models: {import_e}")
        
        return results
    
    def get_embedding_models(self, provider: Optional[str] = None, only_available: bool = False) -> List[Dict[str, Any]]:
        """
        Get all embedding models, optionally filtered by provider.
        
        Args:
            provider: Optional provider name to filter by
            only_available: If True, only return models from available providers
            
        Returns:
            List of embedding model data
        """
        # Get available providers if filtering by availability
        available_providers = []
        if only_available:
            available_providers = [p["name"] for p in self.get_available_embedding_providers()]
        
        results = []
        
        # First try to get from database
        if self._supabase:
            try:
                logger.debug(f"Fetching embedding models with provider={provider}, only_available={only_available}")
                
                # Build SQL query with proper filtering
                where_clause = ""
                if provider:
                    where_clause = f"WHERE p.name = '{provider.replace('\'', '\'\'')}'"
                elif only_available and available_providers:
                    # Format provider names for SQL IN clause with proper escaping
                    provider_names = "', '".join([p.replace("'", "''") for p in available_providers])
                    where_clause = f"WHERE p.name IN ('{provider_names}')"
                
                # Use a simpler joined query that should work with RPC
                sql = f"""
                SELECT m.*, p.name as provider_name
                FROM models.embedding_models m
                JOIN models.providers p ON m.provider_id = p.id
                {where_clause}
                """
                
                logger.debug(f"Executing SQL: {sql}")
                
                # Execute SQL via RPC
                response = self._supabase.rpc("execute_sql", {"sql": sql}).execute()
                
                if response.data:
                    # Normalize each model's structure
                    for model in response.data:
                        # Add provider name
                        if "provider_name" in model and "provider" not in model:
                            model["provider"] = model["provider_name"]
                            
                        normalized_model = self.normalize_model_data(model)
                        results.append(normalized_model)
                    
                    if results:
                        return results
                
            except Exception as e:
                logger.error(f"Error retrieving embedding models from database: {e}")
                import traceback
                logger.debug(f"Get embedding models error traceback: {traceback.format_exc()}")
        
        # If database doesn't have data, use the cached embedding models from the importer
        if not results and self._embedding_models_cache:
            for model in self._embedding_models_cache:
                model_provider = model.get("provider")
                
                # Apply filtering
                if provider and model_provider != provider:
                    continue
                
                if only_available and model_provider not in available_providers:
                    continue
                
                # Create normalized model data
                model_data = {
                    "model_id": model.get("model_id"),
                    "provider": model_provider,
                    "name": model.get("model_name"),
                    "display_name": model.get("model_name").replace("-", " ").title(),
                    "description": model.get("description"),
                    "dimensions": model.get("dimensions"),
                    "max_input_tokens": model.get("max_input_tokens"),
                    "supports_batch": model.get("supports_batch", True),
                    "supports_query_mapping": model.get("supports_query_mapping", False),
                    "pricing": {
                        "input_cost_per_token": model.get("input_cost_per_token", 0)
                    }
                }
                
                results.append(model_data)
        
        # If still no results and we can import, try to import
        if not results and not self._embedding_models_cache:
            try:
                # Run embedding models importer
                from src.haive.dataflow.registry.importers.embeddings_importer import import_embedding_models, EMBEDDING_MODELS
                
                # Cache the models list
                self._embedding_models_cache = EMBEDDING_MODELS
                
                # Run the import
                import_success = import_embedding_models()
                if import_success:
                    logger.info("Successfully imported embedding models")
                    
                    # Use the cached models now
                    for model in self._embedding_models_cache:
                        model_provider = model.get("provider")
                        
                        # Apply filtering
                        if provider and model_provider != provider:
                            continue
                        
                        if only_available and model_provider not in available_providers:
                            continue
                        
                        # Create normalized model data
                        model_data = {
                            "model_id": model.get("model_id"),
                            "provider": model_provider,
                            "name": model.get("model_name"),
                            "display_name": model.get("model_name").replace("-", " ").title(),
                            "description": model.get("description"),
                            "dimensions": model.get("dimensions"),
                            "max_input_tokens": model.get("max_input_tokens"),
                            "supports_batch": model.get("supports_batch", True),
                            "supports_query_mapping": model.get("supports_query_mapping", False),
                            "pricing": {
                                "input_cost_per_token": model.get("input_cost_per_token", 0)
                            }
                        }
                        
                        results.append(model_data)
            except Exception as import_e:
                logger.error(f"Error importing embedding models: {import_e}")
        
        return results
    
    def get_llm_model(self, model_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific LLM model by ID.
        
        Args:
            model_id: ID of the model
            
        Returns:
            Model data or None if not found
        """
        if self._supabase:
            try:
                response = table(self._supabase, "models.llm_models").select("*").eq("model_id", model_id).execute()
                
                if response.data and len(response.data) > 0:
                    model = response.data[0]
                    model_db_id = model.get("id")
                    
                    # Get provider
                    provider_id = model.get("provider_id")
                    if provider_id:
                        provider_response = table(self._supabase, "models.providers").select("*").eq("id", provider_id).execute()
                        if provider_response.data and len(provider_response.data) > 0:
                            provider_data = provider_response.data[0]
                            model["provider"] = provider_data.get("name")
                            model["is_available"] = provider_data.get("is_available", False)
                    
                    # Get capabilities
                    if model_db_id:
                        capabilities_response = table(
                            self._supabase, 
                            "models.llm_capabilities"
                        ).select("*").eq("model_id", model_db_id).execute()
                        
                        if capabilities_response.data and len(capabilities_response.data) > 0:
                            model["capabilities"] = capabilities_response.data[0]
                    
                    # Get pricing
                    if model_db_id:
                        pricing_response = table(
                            self._supabase, 
                            "models.llm_pricing"
                        ).select("*").eq("model_id", model_db_id).execute()
                        
                        if pricing_response.data and len(pricing_response.data) > 0:
                            model["pricing"] = pricing_response.data[0]
                    
                    return self.normalize_model_data(model)
                
            except Exception as e:
                logger.error(f"Error retrieving LLM model from database: {e}")
        
        # Fall back to checking core LLM models
        if CORE_LLM_AVAILABLE:
            # Parse model_id to get provider and model name
            parts = model_id.split("/")
            if len(parts) == 2:
                provider_val, model_name = parts
                
                # Look for matching LLM config class
                llm_config_classes = self._get_llm_config_subclasses()
                
                for cls in llm_config_classes:
                    try:
                        # Check if this is the class we're looking for
                        provider_attr = getattr(cls, 'provider', None)
                        if not provider_attr or not hasattr(provider_attr, 'value'):
                            continue
                            
                        provider_value = provider_attr.value
                        
                        # Skip if provider doesn't match
                        if provider_value.lower() != provider_val.lower():
                            continue
                            
                        cls_name = cls.__name__.replace("LLMConfig", "").lower()
                        
                        # Skip if model name doesn't match
                        if cls_name != model_name.lower():
                            continue
                            
                        # We found a match - create a model entry
                        model_data = {
                            "model_id": model_id,
                            "provider": provider_value,
                            "name": cls.__name__.replace("LLMConfig", ""),
                            "display_name": cls.__name__.replace("LLMConfig", ""),
                            "description": cls.__doc__ or f"Configuration for {cls.__name__.replace('LLMConfig', '')} models"
                        }
                        
                        return model_data
                    except Exception as e:
                        continue
        
        return None
        
    def get_embedding_model(self, model_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific embedding model by ID.
        
        Args:
            model_id: ID of the model
            
        Returns:
            Model data or None if not found
        """
        if self._supabase:
            try:
                response = table(self._supabase, "models.embedding_models").select("*").eq("model_id", model_id).execute()
                
                if response.data and len(response.data) > 0:
                    model = response.data[0]
                    model_db_id = model.get("id")
                    
                    # Get provider
                    provider_id = model.get("provider_id")
                    if provider_id:
                        provider_response = table(self._supabase, "models.providers").select("*").eq("id", provider_id).execute()
                        if provider_response.data and len(provider_response.data) > 0:
                            provider_data = provider_response.data[0]
                            model["provider"] = provider_data.get("name")
                            model["is_available"] = provider_data.get("is_available", False)
                    
                    # Get pricing
                    if model_db_id:
                        pricing_response = table(
                            self._supabase, 
                            "models.embedding_pricing"
                        ).select("*").eq("model_id", model_db_id).execute()
                        
                        if pricing_response.data and len(pricing_response.data) > 0:
                            model["pricing"] = pricing_response.data[0]
                    
                    return self.normalize_model_data(model)
                
            except Exception as e:
                logger.error(f"Error retrieving embedding model from database: {e}")
        
        return None
        
    def detect_environment_variables(self):
        """
        Detect available environment variables for LLM and embedding providers.
        
        Returns:
            Dict mapping provider names to available environment variables
        """
        # Get required environment variables from source code
        env_vars = self.get_required_environment_vars()
        
        # Check which ones are set in the current environment
        env_matches = {}
        
        for env_var in env_vars:
            var_name = env_var.get("var_name")
            provider_name = env_var.get("provider_name")
            
            if not var_name or not provider_name:
                continue
                
            if os.getenv(var_name):
                if provider_name not in env_matches:
                    env_matches[provider_name] = []
                env_matches[provider_name].append(var_name)
        
        # If enabled, store these in vault schema
        if self._supabase and env_matches:
            self._register_environment_vars_in_vault(env_vars)
        
        logger.info(f"Detected environment variables for: {list(env_matches.keys())}")
        return env_matches