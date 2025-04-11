"""
LiteLLM Importer for the Haive Framework.

This module provides functionality for importing LLM models and providers
from LiteLLM's published model list.
"""

import logging
import os
import traceback
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional, Set

# Try to import requests
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    
# Import registry models and utilities
from src.haive.dataflow.registry.core import registry_system, EntityType, ImportStatus, DependencyType
from src.utils.serialization import serialize_object

# Set up logging
logger = logging.getLogger(__name__)

# LiteLLM model data URL
LITELLM_URL = "https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json"


def import_llm_models() -> bool:
    """
    Import LLM models from LiteLLM.
    
    Returns:
        True if successful, False otherwise
    """
    if not REQUESTS_AVAILABLE:
        logger.error("Requests module not available. Cannot import LLM models.")
        return False
    
    import_session = str(uuid.uuid4())
    logger.info(f"Starting LiteLLM import with session {import_session}")
    
    try:
        # Fetch the data
        response = requests.get(LITELLM_URL)
        response.raise_for_status()
        model_data = response.json()
        
        logger.info(f"Successfully fetched model data from LiteLLM ({len(model_data)} models)")
        
        # Extract unique providers
        providers = set()
        for model_id, model_info in model_data.items():
            # Skip the sample spec
            if model_id == "sample_spec":
                continue
            
            # Extract provider from model ID and litellm_provider
            litellm_provider = model_info.get("litellm_provider", "")
            
            # Determine provider (simplified version)
            provider = litellm_provider.lower()
            
            # Special cases for provider inference
            if model_id.startswith("watsonx/"):
                provider = "watsonx"
            elif "claude" in model_id.lower() and provider == "openai":
                provider = "anthropic"
            
            # Use model name for inference if needed
            if not provider:
                # Extract likely provider from model ID
                for part in model_id.lower().split('/'):
                    if part and part not in ['models', 'api']:
                        provider = part
                        break
                        
            if provider:
                providers.add(provider)
        
        # Get environment variable mappings dynamically
        provider_availability = {}
        env_var_mapping = {}
        
        # Check for existing environment variables in the system
        existing_env_vars = registry_system.get_environment_vars()
        for env_var in existing_env_vars:
            if env_var.get("provider_name") in providers:
                env_var_mapping[env_var.get("provider_name")] = env_var.get("var_name")
        
        # Fallback to common patterns if not found in registry
        for provider in providers:
            if provider not in env_var_mapping:
                # Generate likely environment variable name based on provider name
                if provider == "huggingface":
                    env_var_mapping[provider] = "HUGGING_FACE_API_KEY"
                elif provider == "together_ai":
                    env_var_mapping[provider] = "TOGETHER_API_KEY"
                elif provider == "fireworks_ai":
                    env_var_mapping[provider] = "FIREWORKS_API_KEY"
                elif provider == "anthropic":
                    env_var_mapping[provider] = "ANTHROPIC_API_KEY"
                elif provider == "openai":
                    env_var_mapping[provider] = "OPENAI_API_KEY"
                elif provider == "azure":
                    env_var_mapping[provider] = "AZURE_OPENAI_API_KEY"
                elif provider == "gemini":
                    env_var_mapping[provider] = "GOOGLE_GENAI_API_KEY"
                else:
                    # Convert provider name to uppercase and add _API_KEY suffix
                    env_var_mapping[provider] = f"{provider.upper()}_API_KEY"
        
        # Check which providers are available based on environment variables
        for provider, env_var in env_var_mapping.items():
            provider_availability[provider] = os.getenv(env_var) is not None
            logger.debug(f"Provider {provider}: using env var {env_var}, available: {provider_availability[provider]}")
        
        # Register providers
        provider_ids = {}
        for provider in providers:
            try:
                env_var = env_var_mapping.get(provider)
                is_available = provider_availability.get(provider, False)
                
                # Register env var if not already in system
                if env_var:
                    registry_system.add_environment_var(
                        var_name=env_var,
                        provider_name=provider,
                        is_required=True,
                        description=f"API key for {provider.title()} LLM provider"
                    )
                
                # Register the provider
                provider_id = registry_system.register_entity(
                    name=provider,
                    entity_type=EntityType.LLM_PROVIDER,
                    description=f"LLM provider: {provider}",
                    metadata={
                        "is_available": is_available,
                        "imported_at": datetime.now().isoformat(),
                        "import_source": "litellm"
                    }
                )
                
                # Store in database if available
                if registry_system._supabase is not None:
                    try:
                        from src.haive.dataflow.db.supabase import table
                        
                        # First check for provider type
                        type_response = registry_system._supabase.table("models.provider_types").select("id").eq("name", "llm").execute()
                        provider_type_id = None
                        
                        if type_response.data and len(type_response.data) > 0:
                            provider_type_id = type_response.data[0]["id"]
                        else:
                            # Create provider type
                            type_data = {
                                "name": "llm",
                                "display_name": "Language Model",
                                "description": "Provider of large language models",
                                "created_at": datetime.now().isoformat()
                            }
                            
                            type_insert = registry_system._supabase.table("models.provider_types").insert(type_data).execute()
                            if type_insert.data and len(type_insert.data) > 0:
                                provider_type_id = type_insert.data[0]["id"]
                        
                        # Add or update provider with environment variable
                        provider_data = {
                            "name": provider,
                            "display_name": provider.title(),
                            "description": f"LLM provider: {provider}",
                            "is_available": is_available,
                            "metadata": serialize_object({
                                "imported_at": datetime.now().isoformat(),
                                "import_source": "litellm"
                            })
                        }
                        
                        if provider_type_id:
                            provider_data["type_id"] = provider_type_id
                        
                        # Check if provider already exists
                        response = registry_system._supabase.table("models.providers").select("*").eq("name", provider).execute()
                        
                        if response.data and len(response.data) > 0:
                            # Update existing
                            registry_system._supabase.table("models.providers").update(provider_data).eq("id", response.data[0]["id"]).execute()
                        else:
                            # Insert new
                            registry_system._supabase.table("models.providers").insert(provider_data).execute()
                    except Exception as e:
                        logger.error(f"Error storing provider in database: {e}")
                
                provider_ids[provider] = provider_id
                
                # Log success
                registry_system.add_import_log(
                    import_session=import_session,
                    entity_name=provider,
                    entity_type="llm_provider",
                    status=ImportStatus.SUCCESS,
                    message=f"Successfully imported provider {provider}"
                )
                
                logger.info(f"Registered provider: {provider} (available: {is_available})")
                
            except Exception as e:
                error_tb = traceback.format_exc()
                logger.error(f"Error registering provider {provider}: {e}\n{error_tb}")
                
                registry_system.add_import_log(
                    import_session=import_session,
                    entity_name=provider,
                    entity_type="llm_provider",
                    status=ImportStatus.FAILURE,
                    message=f"Failed to import provider {provider}: {e}",
                    traceback_str=error_tb
                )
        
        # Register models via Supabase (if available) or in-memory registry
        model_count = 0
        
        if registry_system._supabase is not None:
            # Insert models via Supabase
            for model_id, model_info in model_data.items():
                # Skip the sample spec
                if model_id == "sample_spec":
                    continue
                
                try:
                    # Determine provider
                    litellm_provider = model_info.get("litellm_provider", "")
                    provider = litellm_provider.lower()
                    
                    # Special cases for provider inference
                    if model_id.startswith("watsonx/"):
                        provider = "watsonx"
                    elif "claude" in model_id.lower() and provider == "openai":
                        provider = "anthropic"
                    
                    # Use model name for inference if needed
                    if not provider:
                        # Extract likely provider from model ID
                        for part in model_id.lower().split('/'):
                            if part and part not in ['models', 'api']:
                                provider = part
                                break
                    
                    # Skip if no provider determined
                    if not provider:
                        logger.warning(f"Could not determine provider for model {model_id}")
                        continue
                    
                    # Get provider ID
                    provider_response = registry_system._supabase.table("models.providers").select("id").eq("name", provider).execute()
                    
                    provider_id = None
                    if provider_response.data and len(provider_response.data) > 0:
                        provider_id = provider_response.data[0]["id"]
                    else:
                        logger.warning(f"Provider {provider} not found in database, skipping model {model_id}")
                        continue
                    
                    # Extract model capabilities
                    capabilities = {
                        "supports_function_calling": model_info.get("supports_function_calling", False),
                        "supports_parallel_function_calling": model_info.get("supports_parallel_function_calling", False),
                        "supports_vision": model_info.get("supports_vision", False),
                        "supports_audio_input": model_info.get("supports_audio_input", False),
                        "supports_audio_output": model_info.get("supports_audio_output", False),
                        "supports_prompt_caching": model_info.get("supports_prompt_caching", False),
                        "supports_response_schema": model_info.get("supports_response_schema", False),
                        "supports_system_messages": model_info.get("supports_system_messages", False),
                        "supports_web_search": model_info.get("supports_web_search", False),
                        "supports_tool_choice": model_info.get("supports_tool_choice", False)
                    }
                    
                    # Extract pricing information
                    pricing = {
                        "input_cost_per_token": model_info.get("input_cost_per_token", 0),
                        "output_cost_per_token": model_info.get("output_cost_per_token", 0),
                        "input_cost_per_token_batches": model_info.get("input_cost_per_token_batches", 0),
                        "output_cost_per_token_batches": model_info.get("output_cost_per_token_batches", 0),
                        "input_cost_per_audio_token": model_info.get("input_cost_per_audio_token", 0),
                        "output_cost_per_audio_token": model_info.get("output_cost_per_audio_token", 0),
                        "cache_read_input_token_cost": model_info.get("cache_read_input_token_cost", 0)
                    }
                    
                    # Extract model name from model_id
                    model_name = model_id.split("/")[-1] if "/" in model_id else model_id
                    
                    # Prepare model data
                    model_data = {
                        "model_id": model_id,
                        "provider_id": provider_id,
                        "name": model_name,
                        "display_name": model_name.replace('-', ' ').replace('_', ' ').title(),
                        "description": f"LLM model: {model_id}",
                        "mode": model_info.get("mode", "chat"),
                        "litellm_provider": litellm_provider,
                        "max_tokens": model_info.get("max_tokens", 0),
                        "max_input_tokens": model_info.get("max_input_tokens", 0),
                        "max_output_tokens": model_info.get("max_output_tokens", 0),
                        "is_active": True,
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat()
                    }
                    
                    # Insert or update model
                    response = registry_system._supabase.table("models.llm_models").select("*").eq("model_id", model_id).execute()
                    
                    if response.data and len(response.data) > 0:
                        # Update existing model
                        model_id_pk = response.data[0]["id"]
                        registry_system._supabase.table("models.llm_models").update(model_data).eq("id", model_id_pk).execute()
                    else:
                        # Insert new model
                        model_response = registry_system._supabase.table("models.llm_models").insert(model_data).execute()
                        
                        if model_response.data and len(model_response.data) > 0:
                            model_id_pk = model_response.data[0]["id"]
                        else:
                            logger.warning(f"Failed to insert model {model_id}")
                            continue
                    
                    # Insert or update capabilities
                    capabilities_data = {
                        "model_id": model_id_pk,
                        "supports_function_calling": capabilities.get("supports_function_calling", False),
                        "supports_vision": capabilities.get("supports_vision", False),
                        "supports_system_messages": capabilities.get("supports_system_messages", False),
                        "capability_matrix": serialize_object(capabilities),
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat()
                    }
                    
                    capabilities_response = registry_system._supabase.table("models.llm_capabilities").select("*").eq("model_id", model_id_pk).execute()
                    
                    if capabilities_response.data and len(capabilities_response.data) > 0:
                        # Update existing capabilities
                        capabilities_id = capabilities_response.data[0]["id"]
                        registry_system._supabase.table("models.llm_capabilities").update(capabilities_data).eq("id", capabilities_id).execute()
                    else:
                        # Insert new capabilities
                        registry_system._supabase.table("models.llm_capabilities").insert(capabilities_data).execute()
                    
                    # Insert or update pricing
                    pricing_data = {
                        "model_id": model_id_pk,
                        "input_cost_per_token": pricing.get("input_cost_per_token", 0),
                        "output_cost_per_token": pricing.get("output_cost_per_token", 0),
                        "currency": "USD",
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat()
                    }
                    
                    pricing_response = registry_system._supabase.table("models.llm_pricing").select("*").eq("model_id", model_id_pk).execute()
                    
                    if pricing_response.data and len(pricing_response.data) > 0:
                        # Update existing pricing
                        pricing_id = pricing_response.data[0]["id"]
                        registry_system._supabase.table("models.llm_pricing").update(pricing_data).eq("id", pricing_id).execute()
                    else:
                        # Insert new pricing
                        registry_system._supabase.table("models.llm_pricing").insert(pricing_data).execute()
                    
                    # Add search pricing if available
                    if "search_context_cost_per_query" in model_info:
                        search_pricing = {
                            "model_id": model_id_pk,
                            "search_context_size_low": model_info.get("search_context_cost_per_query", {}).get("search_context_size_low", 0),
                            "search_context_size_medium": model_info.get("search_context_cost_per_query", {}).get("search_context_size_medium", 0),
                            "search_context_size_high": model_info.get("search_context_cost_per_query", {}).get("search_context_size_high", 0),
                            "created_at": datetime.now().isoformat(),
                            "updated_at": datetime.now().isoformat()
                        }
                        
                        # Use the correct models schema
                        registry_system._supabase.table("models.llm_search_pricing").insert(search_pricing).execute()
                    
                    # Log success
                    registry_system.add_import_log(
                        import_session=import_session,
                        entity_name=model_id,
                        entity_type="llm_model",
                        status=ImportStatus.SUCCESS,
                        message=f"Successfully imported model {model_id}"
                    )
                    
                    model_count += 1
                    
                except Exception as e:
                    error_tb = traceback.format_exc()
                    logger.error(f"Error registering model {model_id}: {e}\n{error_tb}")
                    
                    registry_system.add_import_log(
                        import_session=import_session,
                        entity_name=model_id,
                        entity_type="llm_model",
                        status=ImportStatus.FAILURE,
                        message=f"Failed to import model {model_id}: {e}",
                        traceback_str=error_tb
                    )
        else:
            # Register models via in-memory registry
            for model_id, model_info in model_data.items():
                # Skip the sample spec
                if model_id == "sample_spec":
                    continue
                
                try:
                    # Determine provider using same logic as above
                    litellm_provider = model_info.get("litellm_provider", "")
                    provider = litellm_provider.lower()
                    
                    if model_id.startswith("watsonx/"):
                        provider = "watsonx"
                    elif "claude" in model_id.lower() and provider == "openai":
                        provider = "anthropic"
                    
                    if not provider:
                        for part in model_id.lower().split('/'):
                            if part and part not in ['models', 'api']:
                                provider = part
                                break
                    
                    # Skip if no provider determined
                    if not provider:
                        logger.warning(f"Could not determine provider for model {model_id}")
                        continue
                    
                    # Extract capabilities and pricing (same as above)
                    capabilities = {
                        "supports_function_calling": model_info.get("supports_function_calling", False),
                        "supports_parallel_function_calling": model_info.get("supports_parallel_function_calling", False),
                        "supports_vision": model_info.get("supports_vision", False),
                        "supports_audio_input": model_info.get("supports_audio_input", False),
                        "supports_audio_output": model_info.get("supports_audio_output", False),
                        "supports_prompt_caching": model_info.get("supports_prompt_caching", False),
                        "supports_response_schema": model_info.get("supports_response_schema", False),
                        "supports_system_messages": model_info.get("supports_system_messages", False),
                        "supports_web_search": model_info.get("supports_web_search", False),
                        "supports_tool_choice": model_info.get("supports_tool_choice", False)
                    }
                    
                    pricing = {
                        "input_cost_per_token": model_info.get("input_cost_per_token", 0),
                        "output_cost_per_token": model_info.get("output_cost_per_token", 0),
                        "input_cost_per_token_batches": model_info.get("input_cost_per_token_batches", 0),
                        "output_cost_per_token_batches": model_info.get("output_cost_per_token_batches", 0),
                        "input_cost_per_audio_token": model_info.get("input_cost_per_audio_token", 0),
                        "output_cost_per_audio_token": model_info.get("output_cost_per_audio_token", 0),
                        "cache_read_input_token_cost": model_info.get("cache_read_input_token_cost", 0)
                    }
                    
                    # Extract model name and description (same as above)
                    model_name = model_id.split("/")[-1] if "/" in model_id else model_id
                    description = f"LLM model: {model_id}"
                    
                    if model_info.get("max_tokens"):
                        description += f", context window: {model_info.get('max_tokens')} tokens"
                    
                    # Create a unique entity name
                    entity_name = f"{provider}_{model_name.replace('-', '_')}"
                    
                    # Register the model as an entity
                    model_registration_id = registry_system.register_entity(
                        name=entity_name,
                        entity_type=EntityType.LLM,
                        description=description,
                        metadata={
                            "model_id": model_id,
                            "provider": provider,
                            "litellm_provider": litellm_provider,
                            "mode": model_info.get("mode", "chat"),
                            "max_tokens": model_info.get("max_tokens", 0),
                            "max_input_tokens": model_info.get("max_input_tokens", 0),
                            "max_output_tokens": model_info.get("max_output_tokens", 0),
                            "deprecation_date": model_info.get("deprecation_date"),
                            "capabilities": capabilities,
                            "pricing": pricing,
                            "search_pricing": model_info.get("search_context_cost_per_query", {}),
                            "imported_at": datetime.now().isoformat(),
                            "import_source": "litellm"
                        }
                    )
                    
                    # Add dependency to provider
                    provider_id = provider_ids.get(provider)
                    if provider_id:
                        registry_system.add_dependency(
                            registry_id=model_registration_id,
                            dependent_id=provider_id,
                            dependency_type=DependencyType.REQUIRES
                        )
                    
                    # Log success
                    registry_system.add_import_log(
                        import_session=import_session,
                        entity_name=model_id,
                        entity_type="llm_model",
                        status=ImportStatus.SUCCESS,
                        message=f"Successfully imported model {model_id}"
                    )
                    
                    model_count += 1
                    
                except Exception as e:
                    error_tb = traceback.format_exc()
                    logger.error(f"Error registering model {model_id}: {e}\n{error_tb}")
                    
                    registry_system.add_import_log(
                        import_session=import_session,
                        entity_name=model_id,
                        entity_type="llm_model",
                        status=ImportStatus.FAILURE,
                        message=f"Failed to import model {model_id}: {e}",
                        traceback_str=error_tb
                    )
        
        logger.info(f"Imported {len(provider_ids)} providers and {model_count} models")
        return True
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching LiteLLM model data: {e}")
        return False
    except Exception as e:
        error_tb = traceback.format_exc()
        logger.error(f"Error importing LLM models: {e}\n{error_tb}")
        return False