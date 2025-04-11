"""
LiteLLM Importer for the Haive Registry System.

This module provides functionality for importing LLM models and providers
from LiteLLM's published model list.
"""

import logging
import os
import traceback
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional

# Try to import requests
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    
# Import registry models and utilities
from ..models import EntityType, ImportStatus, DependencyType
from ..core import registry_system  # Import the singleton instance
from ..serialization import serialize_object

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
            
            # Special cases
            if model_id.startswith("watsonx/"):
                provider = "watsonx"
            elif "claude" in model_id.lower() and provider == "openai":
                provider = "anthropic"
            
            # Use model name for inference if needed
            if not provider:
                for known_provider in ["openai", "anthropic", "azure", "google", "gemini", 
                                      "mistralai", "cohere", "llama", "replicate", "groq", 
                                      "together_ai", "fireworks_ai", "perplexity", "anyscale", 
                                      "deepseek", "watsonx", "bedrock", "huggingface", "ai21"]:
                    if known_provider in model_id.lower():
                        provider = known_provider
                        break
            
            if provider:
                providers.add(provider)
        
        # Check for environment variables to determine availability
        provider_availability = {}
        env_var_mapping = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "azure": "AZURE_OPENAI_API_KEY",
            "google": "GOOGLE_API_KEY",
            "gemini": "GEMINI_API_KEY",
            "mistralai": "MISTRAL_API_KEY",
            "cohere": "COHERE_API_KEY",
            "llama": "LLAMA_API_KEY",
            "replicate": "REPLICATE_API_KEY",
            "groq": "GROQ_API_KEY",
            "together_ai": "TOGETHER_AI_API_KEY",
            "fireworks_ai": "FIREWORKS_AI_API_KEY",
            "perplexity": "PERPLEXITY_API_KEY",
            "anyscale": "ANYSCALE_API_KEY",
            "deepseek": "DEEPSEEK_API_KEY",
            "watsonx": "WATSONX_API_KEY",
            "bedrock": "AWS_ACCESS_KEY_ID",
            "huggingface": "HUGGING_FACE_API_KEY",
            "ai21": "AI21_API_KEY"
        }
        
        # Register providers
        provider_ids = {}
        for provider in providers:
            try:
                env_var = env_var_mapping.get(provider)
                is_available = False
                if env_var:
                    is_available = os.getenv(env_var) is not None
                
                provider_availability[provider] = is_available
                
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
                
                # Add environment variable
                if env_var:
                    registry_system.add_environment_var(
                        registry_id=provider_id,
                        env_name=env_var,
                        is_required=True
                    )
                
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
        
        # Register models
        model_count = 0
        
        # Check if Supabase is available
        if registry_system._supabase is not None:
            # Register models via Supabase
            for model_id, model_info in model_data.items():
                # Skip the sample spec
                if model_id == "sample_spec":
                    continue
                
                try:
                    # Determine provider
                    litellm_provider = model_info.get("litellm_provider", "")
                    provider = litellm_provider.lower()
                    
                    # Special cases
                    if model_id.startswith("watsonx/"):
                        provider = "watsonx"
                    elif "claude" in model_id.lower() and provider == "openai":
                        provider = "anthropic"
                    
                    # Use model name for inference if needed
                    if not provider:
                        for known_provider in ["openai", "anthropic", "azure", "google", "gemini", 
                                            "mistralai", "cohere", "llama", "replicate", "groq", 
                                            "together_ai", "fireworks_ai", "perplexity", "anyscale", 
                                            "deepseek", "watsonx", "bedrock", "huggingface", "ai21"]:
                            if known_provider in model_id.lower():
                                provider = known_provider
                                break
                    
                    # Skip if no provider determined
                    if not provider:
                        logger.warning(f"Could not determine provider for model {model_id}")
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
                        "provider": provider,
                        "model_name": model_name,
                        "description": f"LLM model: {model_id}",
                        "mode": model_info.get("mode", ""),
                        "litellm_provider": litellm_provider,
                        "max_tokens": model_info.get("max_tokens", 0),
                        "max_input_tokens": model_info.get("max_input_tokens", 0),
                        "max_output_tokens": model_info.get("max_output_tokens", 0),
                        "deprecation_date": model_info.get("deprecation_date"),
                        "metadata": serialize_object({
                            "capabilities": capabilities,
                            "imported_at": datetime.now().isoformat(),
                            "import_source": "litellm"
                        }),
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat()
                    }
                    
                    # Insert or update model
                    response = registry_system._supabase.table("agents.llm_models").select("*").eq("model_id", model_id).execute()
                    
                    if response.data and len(response.data) > 0:
                        # Update existing model
                        model_id_pk = response.data[0]["id"]
                        registry_system._supabase.table("agents.llm_models").update(model_data).eq("id", model_id_pk).execute()
                    else:
                        # Insert new model
                        model_response = registry_system._supabase.table("agents.llm_models").insert(model_data).execute()
                        
                        if model_response.data and len(model_response.data) > 0:
                            model_id_pk = model_response.data[0]["id"]
                        else:
                            logger.warning(f"Failed to insert model {model_id}")
                            continue
                    
                    # Insert or update capabilities
                    capabilities_data = {
                        "model_id": model_id,
                        **capabilities,
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat()
                    }
                    
                    capabilities_response = registry_system._supabase.table("agents.llm_model_capabilities").select("*").eq("model_id", model_id).execute()
                    
                    if capabilities_response.data and len(capabilities_response.data) > 0:
                        # Update existing capabilities
                        capabilities_id = capabilities_response.data[0]["id"]
                        registry_system._supabase.table("agents.llm_model_capabilities").update(capabilities_data).eq("id", capabilities_id).execute()
                    else:
                        # Insert new capabilities
                        registry_system._supabase.table("agents.llm_model_capabilities").insert(capabilities_data).execute()
                    
                    # Insert or update pricing
                    pricing_data = {
                        "model_id": model_id,
                        **pricing,
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat()
                    }
                    
                    pricing_response = registry_system._supabase.table("agents.llm_pricing").select("*").eq("model_id", model_id).execute()
                    
                    if pricing_response.data and len(pricing_response.data) > 0:
                        # Update existing pricing
                        pricing_id = pricing_response.data[0]["id"]
                        registry_system._supabase.table("agents.llm_pricing").update(pricing_data).eq("id", pricing_id).execute()
                    else:
                        # Insert new pricing
                        registry_system._supabase.table("agents.llm_pricing").insert(pricing_data).execute()
                    
                    # Add search pricing if available
                    if "search_context_cost_per_query" in model_info:
                        search_pricing = {
                            "model_id": model_id,
                            "search_context_size_low": model_info.get("search_context_cost_per_query", {}).get("search_context_size_low", 0),
                            "search_context_size_medium": model_info.get("search_context_cost_per_query", {}).get("search_context_size_medium", 0),
                            "search_context_size_high": model_info.get("search_context_cost_per_query", {}).get("search_context_size_high", 0),
                            "created_at": datetime.now().isoformat(),
                            "updated_at": datetime.now().isoformat()
                        }
                        
                        search_pricing_response = registry_system._supabase.table("agents.llm_search_pricing").select("*").eq("model_id", model_id).execute()
                        
                        if search_pricing_response.data and len(search_pricing_response.data) > 0:
                            # Update existing search pricing
                            search_pricing_id = search_pricing_response.data[0]["id"]
                            registry_system._supabase.table("agents.llm_search_pricing").update(search_pricing).eq("id", search_pricing_id).execute()
                        else:
                            # Insert new search pricing
                            registry_system._supabase.table("agents.llm_search_pricing").insert(search_pricing).execute()
                    
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
                    # Determine provider
                    litellm_provider = model_info.get("litellm_provider", "")
                    provider = litellm_provider.lower()
                    
                    # Special cases and provider inference logic (same as above)
                    if model_id.startswith("watsonx/"):
                        provider = "watsonx"
                    elif "claude" in model_id.lower() and provider == "openai":
                        provider = "anthropic"
                    
                    # Use model name for inference if needed
                    if not provider:
                        for known_provider in ["openai", "anthropic", "azure", "google", "gemini", 
                                            "mistralai", "cohere", "llama", "replicate", "groq", 
                                            "together_ai", "fireworks_ai", "perplexity", "anyscale", 
                                            "deepseek", "watsonx", "bedrock", "huggingface", "ai21"]:
                            if known_provider in model_id.lower():
                                provider = known_provider
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
                            "mode": model_info.get("mode", ""),
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