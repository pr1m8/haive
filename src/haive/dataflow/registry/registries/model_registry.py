"""
Model Registry Client for Haive.

This module provides a client interface for working with the registry system
to access LLM and embedding models with dynamic environment variable detection.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional, Union, Tuple, Type
from pydantic import BaseModel, create_model, Field

# Import registry core
from src.haive.dataflow.registry.core import registry_system, EntityType
from src.haive.dataflow.db.supabase import get_supabase_client, table

# Set up logging
logger = logging.getLogger(__name__)


class ModelRegistry:
    """
    Client for working with registered LLM and embedding models.
    """
    
    def __init__(self):
        """Initialize the model registry client."""
        self._supabase = None
        try:
            self._supabase = get_supabase_client()
        except Exception as e:
            logger.warning(f"Could not initialize Supabase connection: {e}")
        
        # Scan environment variables on initialization
        self.update_provider_availability()
    
    def update_provider_availability(self):
        """
        Scan environment variables and update provider availability status.
        """
        # Get all registered environment variables
        env_vars = registry_system.get_environment_vars()
        
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
                # Query for available providers directly from models schema
                response = table(self._supabase, "models.providers").select("*").eq("is_available", True).execute()
                if response.data:
                    return response.data
            except Exception as e:
                logger.error(f"Error retrieving available LLM providers: {e}")
        
        # Fall back to registry system
        providers = registry_system.get_available_providers(EntityType.LLM_PROVIDER)
        return [p for p in providers if p.get("is_available", False)]
    
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
                # Query for available embedding providers
                # Look for providers that have embedding models
                embedding_providers_response = table(self._supabase, "models.providers").select("*").eq("is_available", True).execute()
                
                if embedding_providers_response.data:
                    # Filter to only providers with embedding models
                    embedding_providers = []
                    for provider in embedding_providers_response.data:
                        # Check if provider has embedding models
                        provider_id = provider.get("id")
                        if provider_id:
                            models_response = table(self._supabase, "models.embedding_models").select("id").eq("provider_id", provider_id).limit(1).execute()
                            if models_response.data and len(models_response.data) > 0:
                                embedding_providers.append(provider)
                    
                    return embedding_providers
            except Exception as e:
                logger.error(f"Error retrieving available embedding providers: {e}")
        
        # Fall back to registry system
        providers = registry_system.get_available_providers(EntityType.EMBEDDING_PROVIDER)
        return [p for p in providers if p.get("is_available", False)]
    
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
        
        if self._supabase:
            try:
                # Use direct database query for efficiency
                query = table(self._supabase, "models.llm_models").select("models.llm_models.*, models.providers.name as provider_name")
                
                # Join with providers to get provider name
                query = query.join("models.providers", "models.llm_models.provider_id", "models.providers.id")
                
                if provider:
                    query = query.eq("models.providers.name", provider)
                elif only_available and available_providers:
                    # Filter to only available providers
                    query = query.in_("models.providers.name", available_providers)
                
                response = query.execute()
                
                if response.data:
                    # Normalize each model's structure
                    for model in response.data:
                        # Add provider name
                        if "provider_name" in model and "provider" not in model:
                            model["provider"] = model["provider_name"]
                            
                        normalized_model = self.normalize_model_data(model)
                        results.append(normalized_model)
                    
                    return results
                    
            except Exception as e:
                logger.error(f"Error retrieving LLM models from database: {e}")
        
        # Fall back to registry system
        registry_models = registry_system.get_entities_by_type(EntityType.LLM)
        
        # Apply filtering
        if provider:
            registry_models = [
                m for m in registry_models 
                if (m.get("provider") == provider or 
                    m.get("metadata", {}).get("provider") == provider)
            ]
        elif only_available and available_providers:
            registry_models = [
                m for m in registry_models 
                if (m.get("provider") in available_providers or 
                    m.get("metadata", {}).get("provider") in available_providers)
            ]
        
        # Normalize each model's structure
        for model in registry_models:
            normalized_model = self.normalize_model_data(model)
            results.append(normalized_model)
        
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
        
        if self._supabase:
            try:
                # Use direct database query for efficiency
                query = table(self._supabase, "models.embedding_models").select("models.embedding_models.*, models.providers.name as provider_name")
                
                # Join with providers
                query = query.join("models.providers", "models.embedding_models.provider_id", "models.providers.id")
                
                if provider:
                    query = query.eq("models.providers.name", provider)
                elif only_available and available_providers:
                    # Filter to only available providers
                    query = query.in_("models.providers.name", available_providers)
                
                response = query.execute()
                
                if response.data:
                    # Normalize each model's structure
                    for model in response.data:
                        # Add provider name
                        if "provider_name" in model and "provider" not in model:
                            model["provider"] = model["provider_name"]
                            
                        normalized_model = self.normalize_model_data(model)
                        results.append(normalized_model)
                    
                    return results
                
            except Exception as e:
                logger.error(f"Error retrieving embedding models from database: {e}")
        
        # Fall back to registry system
        registry_models = registry_system.get_entities_by_type(EntityType.EMBEDDING)
        
        # Apply filtering
        if provider:
            registry_models = [
                m for m in registry_models 
                if (m.get("provider") == provider or 
                    m.get("metadata", {}).get("provider") == provider)
            ]
        elif only_available and available_providers:
            registry_models = [
                m for m in registry_models 
                if (m.get("provider") in available_providers or 
                    m.get("metadata", {}).get("provider") in available_providers)
            ]
        
        # Normalize each model's structure
        for model in registry_models:
            normalized_model = self.normalize_model_data(model)
            results.append(normalized_model)
        
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
        
        # Fall back to registry search
        entities = registry_system.search_entities("", entity_type=EntityType.LLM)
        for entity in entities:
            normalized = self.normalize_model_data(entity)
            
            # Check if this is the model we're looking for
            if normalized.get("model_id") == model_id:
                return normalized
                
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
        
        # Fall back to registry search
        entities = registry_system.search_entities("", entity_type=EntityType.EMBEDDING)
        for entity in entities:
            normalized = self.normalize_model_data(entity)
            
            # Check if this is the model we're looking for
            if normalized.get("model_id") == model_id:
                return normalized
                
        return None
        
    def detect_environment_variables(self):
        """
        Detect available environment variables for LLM and embedding providers.
        
        Returns:
            Dict mapping provider names to available environment variables
        """
        # Map of known provider environment variable patterns
        provider_env_patterns = {
            # Common patterns
            "azure": ["AZURE_", "OPENAI_API_"],
            "openai": ["OPENAI_", "OPENAI_API_"],
            "anthropic": ["ANTHROPIC_", "CLAUDE_"],
            "huggingface": ["HUGGING_FACE_", "HUGGINGFACE_", "HF_"],
            "cohere": ["COHERE_"],
            "gemini": ["GEMINI_", "GOOGLE_", "PALM_"],
            "mistralai": ["MISTRAL_"],
            "groq": ["GROQ_"],
            "together_ai": ["TOGETHER_", "TOGETHER_AI_"],
            "fireworks_ai": ["FIREWORKS_", "FIREWORKS_AI_"],
            "replicate": ["REPLICATE_"],
            "deepseek": ["DEEPSEEK_"],
            "ai21": ["AI21_"],
            "perplexity": ["PERPLEXITY_"]
        }
        
        # Find matching environment variables
        env_matches = {}
        for env_name in os.environ:
            if "API_KEY" in env_name or "TOKEN" in env_name:
                for provider, patterns in provider_env_patterns.items():
                    if any(env_name.startswith(pattern) for pattern in patterns):
                        if provider not in env_matches:
                            env_matches[provider] = []
                        env_matches[provider].append(env_name)
        
        # Register detected environment variables
        for provider, env_vars in env_matches.items():
            if env_vars:
                # Register the first variable found (prioritize API_KEY variables)
                api_key_vars = [var for var in env_vars if "API_KEY" in var]
                var_to_register = api_key_vars[0] if api_key_vars else env_vars[0]
                
                # Register the environment variable in config schema
                if self._supabase:
                    try:
                        # Check if variable already exists
                        env_var_response = table(self._supabase, "config.environment_variables").select("*").eq("name", var_to_register).execute()
                        
                        if not env_var_response.data or len(env_var_response.data) == 0:
                            # Create new environment variable
                            table(self._supabase, "config.environment_variables").insert({
                                "name": var_to_register,
                                "display_name": f"{provider.title()} API Key",
                                "description": f"API key for {provider.title()} provider (auto-detected)",
                                "is_secret": True,
                                "is_required": True,
                                "metadata": json.dumps({"provider_name": provider}),
                                "created_at": "NOW()",
                                "updated_at": "NOW()"
                            }).execute()
                    except Exception as e:
                        logger.error(f"Error registering environment variable: {e}")
                else:
                    # Register with registry system
                    registry_system.add_environment_var(
                        var_name=var_to_register,
                        provider_name=provider,
                        is_required=True,
                        description=f"API key for {provider.title()} provider (auto-detected)"
                    )
                
                logger.info(f"Auto-detected environment variable for {provider}: {var_to_register}")
        
        return env_matches