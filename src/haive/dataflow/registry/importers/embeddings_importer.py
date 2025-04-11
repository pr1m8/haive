"""
Embedding Models Importer for the Haive Registry System.

This module provides functionality for importing embedding models
from various providers and registering them in the system.
"""

import logging
import os
import traceback
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional, Set, Tuple

# Import registry models and utilities
from ..core import registry_system, EntityType, ImportStatus, DependencyType
from ..serialization import serialize_object

# Set up logging
logger = logging.getLogger(__name__)

# Embedding model data
EMBEDDING_MODELS = [
    # Azure OpenAI embeddings
    {
        "model_id": "azure/text-embedding-ada-002",
        "model_name": "text-embedding-ada-002",
        "provider": "azure",
        "dimensions": 1536,
        "max_input_tokens": 8191,
        "supports_batch": True,
        "input_cost_per_token": 0.0000001,
        "description": "Azure OpenAI text-embedding-ada-002 model"
    },
    {
        "model_id": "azure/text-embedding-3-small",
        "model_name": "text-embedding-3-small",
        "provider": "azure",
        "dimensions": 1536,
        "max_input_tokens": 8191,
        "supports_batch": True,
        "input_cost_per_token": 0.00000002,
        "description": "Azure OpenAI text-embedding-3-small model"
    },
    {
        "model_id": "azure/text-embedding-3-large",
        "model_name": "text-embedding-3-large",
        "provider": "azure",
        "dimensions": 3072,
        "max_input_tokens": 8191,
        "supports_batch": True,
        "input_cost_per_token": 0.00000013,
        "description": "Azure OpenAI text-embedding-3-large model"
    },
    
    # HuggingFace embeddings
    {
        "model_id": "huggingface/all-MiniLM-L6-v2",
        "model_name": "all-MiniLM-L6-v2",
        "provider": "huggingface",
        "dimensions": 384,
        "max_input_tokens": 256,
        "supports_batch": True,
        "input_cost_per_token": 0.0,
        "description": "Sentence Transformers all-MiniLM-L6-v2 model"
    },
    {
        "model_id": "huggingface/all-mpnet-base-v2",
        "model_name": "all-mpnet-base-v2",
        "provider": "huggingface",
        "dimensions": 768,
        "max_input_tokens": 384,
        "supports_batch": True,
        "input_cost_per_token": 0.0,
        "description": "Sentence Transformers all-mpnet-base-v2 model"
    },
    {
        "model_id": "huggingface/bge-small-en-v1.5",
        "model_name": "bge-small-en-v1.5",
        "provider": "huggingface",
        "dimensions": 384,
        "max_input_tokens": 512,
        "supports_batch": True,
        "input_cost_per_token": 0.0,
        "description": "BAAI BGE Small English v1.5 model"
    },
    {
        "model_id": "huggingface/bge-large-en-v1.5",
        "model_name": "bge-large-en-v1.5",
        "provider": "huggingface",
        "dimensions": 1024,
        "max_input_tokens": 512,
        "supports_batch": True,
        "input_cost_per_token": 0.0,
        "description": "BAAI BGE Large English v1.5 model"
    },
    {
        "model_id": "huggingface/e5-small-v2",
        "model_name": "e5-small-v2",
        "provider": "huggingface",
        "dimensions": 384,
        "max_input_tokens": 512,
        "supports_batch": True,
        "input_cost_per_token": 0.0,
        "description": "E5 Small v2 model"
    },
    {
        "model_id": "huggingface/e5-base-v2",
        "model_name": "e5-base-v2",
        "provider": "huggingface",
        "dimensions": 768,
        "max_input_tokens": 512,
        "supports_batch": True,
        "input_cost_per_token": 0.0,
        "description": "E5 Base v2 model"
    },
    {
        "model_id": "huggingface/e5-large-v2",
        "model_name": "e5-large-v2",
        "provider": "huggingface",
        "dimensions": 1024,
        "max_input_tokens": 512,
        "supports_batch": True,
        "input_cost_per_token": 0.0,
        "description": "E5 Large v2 model"
    },
    {
        "model_id": "huggingface/instructor-large",
        "model_name": "instructor-large",
        "provider": "huggingface",
        "dimensions": 768,
        "max_input_tokens": 512,
        "supports_batch": True,
        "supports_query_mapping": True,
        "input_cost_per_token": 0.0,
        "description": "Instructor Large model supporting instruction-based embeddings"
    },
    {
        "model_id": "huggingface/instructor-xl",
        "model_name": "instructor-xl",
        "provider": "huggingface",
        "dimensions": 1024,
        "max_input_tokens": 512,
        "supports_batch": True,
        "supports_query_mapping": True,
        "input_cost_per_token": 0.0,
        "description": "Instructor XL model supporting instruction-based embeddings"
    },
    
    # OpenAI embeddings
    {
        "model_id": "openai/text-embedding-ada-002",
        "model_name": "text-embedding-ada-002",
        "provider": "openai",
        "dimensions": 1536,
        "max_input_tokens": 8191,
        "supports_batch": True,
        "input_cost_per_token": 0.0000001,
        "description": "OpenAI text-embedding-ada-002 model"
    },
    {
        "model_id": "openai/text-embedding-3-small",
        "model_name": "text-embedding-3-small",
        "provider": "openai",
        "dimensions": 1536,
        "max_input_tokens": 8191,
        "supports_batch": True,
        "input_cost_per_token": 0.00000002,
        "description": "OpenAI text-embedding-3-small model"
    },
    {
        "model_id": "openai/text-embedding-3-large",
        "model_name": "text-embedding-3-large",
        "provider": "openai",
        "dimensions": 3072,
        "max_input_tokens": 8191,
        "supports_batch": True,
        "input_cost_per_token": 0.00000013,
        "description": "OpenAI text-embedding-3-large model"
    },
    
    # Cohere embeddings
    {
        "model_id": "cohere/embed-english-v3.0",
        "model_name": "embed-english-v3.0",
        "provider": "cohere",
        "dimensions": 1024,
        "max_input_tokens": 512,
        "supports_batch": True,
        "supports_query_mapping": True,
        "input_cost_per_token": 0.00000010,
        "description": "Cohere Embed English v3.0 model"
    },
    {
        "model_id": "cohere/embed-english-light-v3.0",
        "model_name": "embed-english-light-v3.0",
        "provider": "cohere",
        "dimensions": 384,
        "max_input_tokens": 512,
        "supports_batch": True,
        "supports_query_mapping": True,
        "input_cost_per_token": 0.00000001,
        "description": "Cohere Embed English Light v3.0 model"
    },
    {
        "model_id": "cohere/embed-multilingual-v3.0",
        "model_name": "embed-multilingual-v3.0",
        "provider": "cohere",
        "dimensions": 1024,
        "max_input_tokens": 512,
        "supports_batch": True,
        "supports_query_mapping": True,
        "input_cost_per_token": 0.00000015,
        "description": "Cohere Embed Multilingual v3.0 model supporting 100+ languages"
    },
    {
        "model_id": "cohere/embed-multilingual-light-v3.0",
        "model_name": "embed-multilingual-light-v3.0",
        "provider": "cohere",
        "dimensions": 384,
        "max_input_tokens": 512,
        "supports_batch": True,
        "supports_query_mapping": True,
        "input_cost_per_token": 0.00000002,
        "description": "Cohere Embed Multilingual Light v3.0 model supporting 100+ languages"
    }
]

def import_embedding_models() -> bool:
    """
    Import embedding models into the registry.
    
    Returns:
        True if successful, False otherwise
    """
    import_session = str(uuid.uuid4())
    logger.info(f"Starting embedding models import with session {import_session}")
    
    try:
        # Extract unique providers
        providers = set(model["provider"] for model in EMBEDDING_MODELS)
        
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
                else:
                    # Convert provider name to uppercase and add _API_KEY suffix
                    env_var_mapping[provider] = f"{provider.upper()}_API_KEY"
        
        # Check which providers are available based on environment variables
        for provider, env_var in env_var_mapping.items():
            provider_availability[provider] = os.getenv(env_var) is not None
            logger.debug(f"Provider {provider}: using env var {env_var}, available: {provider_availability[provider]}")
        
        # Register providers and environment variables
        provider_ids = {}
        for provider in providers:
            try:
                env_var = env_var_mapping.get(provider)
                is_available = provider_availability.get(provider, False)
                
                # Register environment variable first
                if env_var:
                    registry_system.add_environment_var(
                        var_name=env_var,
                        provider_name=provider,
                        is_required=True,
                        description=f"API key for {provider.title()} embedding provider"
                    )
                
                # Register the provider
                provider_id = registry_system.register_entity(
                    name=provider,
                    entity_type=EntityType.EMBEDDING_PROVIDER,
                    description=f"Embedding provider: {provider}",
                    metadata={
                        "is_available": is_available,
                        "imported_at": datetime.now().isoformat(),
                        "import_source": "embedding_importer"
                    }
                )
                
                # Store in Supabase directly if available
                if registry_system._supabase is not None:
                    try:
                        from ..db.supabase import table
                        # Add or update provider with environment variable
                        provider_data = {
                            "name": provider,
                            "provider_type": provider,
                            "is_available": is_available,
                            "env_var": env_var,
                            "description": f"Embedding provider: {provider}",
                            "metadata": serialize_object({
                                "imported_at": datetime.now().isoformat(),
                                "import_source": "embedding_importer"
                            })
                        }
                        
                        # Check if provider already exists
                        response = table(registry_system._supabase, "agents.embedding_providers").select("*").eq("name", provider).execute()
                        
                        if response.data and len(response.data) > 0:
                            # Update existing
                            table(registry_system._supabase, "agents.embedding_providers").update(provider_data).eq("id", response.data[0]["id"]).execute()
                        else:
                            # Insert new
                            table(registry_system._supabase, "agents.embedding_providers").insert(provider_data).execute()
                    except Exception as e:
                        logger.error(f"Error storing provider in Supabase: {e}")
                
                provider_ids[provider] = provider_id
                
                # Log success
                registry_system.add_import_log(
                    import_session=import_session,
                    entity_name=provider,
                    entity_type="embedding_provider",
                    status=ImportStatus.SUCCESS,
                    message=f"Successfully imported provider {provider}"
                )
                
                logger.info(f"Registered embedding provider: {provider} (available: {is_available})")
                
            except Exception as e:
                error_tb = traceback.format_exc()
                logger.error(f"Error registering provider {provider}: {e}\n{error_tb}")
                
                registry_system.add_import_log(
                    import_session=import_session,
                    entity_name=provider,
                    entity_type="embedding_provider",
                    status=ImportStatus.FAILURE,
                    message=f"Failed to import provider {provider}: {e}",
                    traceback_str=error_tb
                )
        
        # Register models
        model_count = 0
        
        # Check if Supabase is available for direct DB access
        if registry_system._supabase is not None:
            # Register models via Supabase
            from ..db.supabase import table
            
            for model_info in EMBEDDING_MODELS:
                try:
                    model_id = model_info["model_id"]
                    provider = model_info["provider"]
                    model_name = model_info["model_name"]
                    
                    # Get provider ID
                    provider_id = provider_ids.get(provider)
                    
                    # Prepare model data
                    model_data = {
                        "model_id": model_id,
                        "provider_uuid": provider_id,
                        "provider": provider,
                        "model_name": model_name,
                        "dimensions": model_info.get("dimensions", 0),
                        "max_input_tokens": model_info.get("max_input_tokens", 0),
                        "supports_batch": model_info.get("supports_batch", True),
                        "supports_query_mapping": model_info.get("supports_query_mapping", False),
                        "description": model_info.get("description", f"Embedding model: {model_id}"),
                        "metadata": serialize_object({
                            "imported_at": datetime.now().isoformat(),
                            "import_source": "embedding_importer"
                        }),
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat()
                    }
                    
                    # Insert or update model
                    response = table(registry_system._supabase, "agents.embedding_models").select("*").eq("model_id", model_id).execute()
                    
                    if response.data and len(response.data) > 0:
                        # Update existing model
                        model_id_pk = response.data[0]["id"]
                        table(registry_system._supabase, "agents.embedding_models").update(model_data).eq("id", model_id_pk).execute()
                    else:
                        # Insert new model
                        model_response = table(registry_system._supabase, "agents.embedding_models").insert(model_data).execute()
                        
                        if model_response.data and len(model_response.data) > 0:
                            model_id_pk = model_response.data[0]["id"]
                        else:
                            logger.warning(f"Failed to insert model {model_id}")
                            continue
                    
                    # Insert or update pricing
                    pricing_data = {
                        "model_id": model_id,
                        "input_cost_per_token": model_info.get("input_cost_per_token", 0),
                        "batch_cost_per_token": model_info.get("batch_cost_per_token", model_info.get("input_cost_per_token", 0)),
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat()
                    }
                    
                    pricing_response = table(registry_system._supabase, "agents.embedding_pricing").select("*").eq("model_id", model_id).execute()
                    
                    if pricing_response.data and len(pricing_response.data) > 0:
                        # Update existing pricing
                        pricing_id = pricing_response.data[0]["id"]
                        table(registry_system._supabase, "agents.embedding_pricing").update(pricing_data).eq("id", pricing_id).execute()
                    else:
                        # Insert new pricing
                        table(registry_system._supabase, "agents.embedding_pricing").insert(pricing_data).execute()
                    
                    # Log success
                    registry_system.add_import_log(
                        import_session=import_session,
                        entity_name=model_id,
                        entity_type="embedding_model",
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
                        entity_type="embedding_model",
                        status=ImportStatus.FAILURE,
                        message=f"Failed to import model {model_id}: {e}",
                        traceback_str=error_tb
                    )
        else:
            # Register models via in-memory registry
            for model_info in EMBEDDING_MODELS:
                try:
                    model_id = model_info["model_id"]
                    provider = model_info["provider"]
                    model_name = model_info["model_name"]
                    
                    # Create unique entity name
                    entity_name = f"{provider}_{model_name.replace('-', '_')}"
                    
                    # Register the model as an entity
                    model_registration_id = registry_system.register_entity(
                        name=entity_name,
                        entity_type=EntityType.EMBEDDING,
                        description=model_info.get("description", f"Embedding model: {model_id}"),
                        metadata={
                            "model_id": model_id,
                            "provider": provider,
                            "dimensions": model_info.get("dimensions", 0),
                            "max_input_tokens": model_info.get("max_input_tokens", 0),
                            "supports_batch": model_info.get("supports_batch", True),
                            "supports_query_mapping": model_info.get("supports_query_mapping", False),
                            "pricing": {
                                "input_cost_per_token": model_info.get("input_cost_per_token", 0),
                                "batch_cost_per_token": model_info.get("batch_cost_per_token", model_info.get("input_cost_per_token", 0))
                            },
                            "imported_at": datetime.now().isoformat(),
                            "import_source": "embedding_importer"
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
                        entity_type="embedding_model",
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
                        entity_type="embedding_model",
                        status=ImportStatus.FAILURE,
                        message=f"Failed to import model {model_id}: {e}",
                        traceback_str=error_tb
                    )
        
        logger.info(f"Imported {len(provider_ids)} embedding providers and {model_count} embedding models")
        return True
        
    except Exception as e:
        error_tb = traceback.format_exc()
        logger.error(f"Error importing embedding models: {e}\n{error_tb}")
        return False