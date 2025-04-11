#!/usr/bin/env python
"""
Fixed LiteLLM Importer Module

This module imports LLM and embedding models from LiteLLM data and
other sources into Supabase, properly handling all models without limits.
"""

import os
import sys
import requests
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Import Supabase client and helpers
try:
    from src.haive.dataflow.db.supabase import get_supabase_client, table
    supabase = get_supabase_client()
    logger.info("Successfully imported Supabase client and helpers")
except ImportError as e:
    logger.error(f"Error importing Supabase client: {e}")
    logger.error("Make sure src.haive.dataflow.db.supabase is in your Python path")
    sys.exit(1)

# Define constants
LITELLM_URL = "https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json"

def get_or_create_provider_type(type_name: str, display_name: str) -> Optional[str]:
    """Get or create a provider type and return its ID."""
    try:
        # Check if provider type exists - use explicit schema reference
        response = table(supabase, "models.provider_types").select("id").eq("name", type_name).execute()
        
        if response.data and len(response.data) > 0:
            logger.info(f"Found existing provider type: {type_name}")
            return response.data[0]["id"]
        
        # Create new provider type with explicit schema reference
        provider_type_data = {
            "name": type_name,
            "display_name": display_name,
            "description": f"Provider type for {display_name.lower()}",
            "created_at": datetime.now().isoformat()
        }
        
        response = table(supabase, "models.provider_types").insert(provider_type_data).execute()
        
        if response.data and len(response.data) > 0:
            logger.info(f"Created new provider type: {type_name}")
            return response.data[0]["id"]
            
        return None
    except Exception as e:
        logger.error(f"Error getting or creating provider type {type_name}: {e}")
        return None

def get_or_create_provider(provider_name: str, provider_type: str) -> Optional[Dict[str, Any]]:
    """Get or create a provider and return its data."""
    try:
        # Get the provider type ID
        provider_type_id = get_or_create_provider_type(
            provider_type, 
            "Large Language Models" if provider_type == "llm" else "Embedding Models"
        )
        
        if not provider_type_id:
            logger.error(f"Failed to get or create provider type {provider_type}")
            return None
        
        # Check if the provider exists - use explicit schema reference
        response = table(supabase, "models.providers").select("*").eq("name", provider_name).execute()
        
        if response.data and len(response.data) > 0:
            logger.info(f"Found existing provider: {provider_name}")
            return response.data[0]
        
        # Generate API key name
        api_key_name = f"{provider_name.upper()}_API_KEY"
        
        # Special cases
        if provider_name == "huggingface":
            api_key_name = "HUGGING_FACE_API_KEY"
        elif provider_name == "google":
            api_key_name = "GOOGLE_API_KEY"
        elif provider_name == "together_ai":
            api_key_name = "TOGETHER_API_KEY"
        
        # Check if there's a vault secret for this API key
        vault_secret_id = None
        try:
            # Check vault.secrets table
            secret_response = table(supabase, "vault.secrets").select("id").eq("name", api_key_name).execute()
            if secret_response.data and len(secret_response.data) > 0:
                vault_secret_id = secret_response.data[0]["id"]
                logger.info(f"Found vault secret for {api_key_name}")
        except Exception as e:
            logger.warning(f"Could not check vault secrets: {e}")
        
        # Create new provider with explicit schema reference
        provider_data = {
            "type_id": provider_type_id,
            "name": provider_name,
            "display_name": provider_name.replace('_', ' ').title(),
            "description": f"{provider_type.upper()} provider: {provider_name}",
            "is_available": os.getenv(api_key_name) is not None,
            "vault_secret_id": vault_secret_id,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        response = table(supabase, "models.providers").insert(provider_data).execute()
        
        if response.data and len(response.data) > 0:
            logger.info(f"Created new provider: {provider_name}")
            return response.data[0]
            
        return None
    except Exception as e:
        logger.error(f"Error getting or creating provider {provider_name}: {e}")
        return None

def import_llm_models() -> int:
    """Import LLM models from LiteLLM. Returns the number of models imported."""
    try:
        # Fetch the data
        response = requests.get(LITELLM_URL)
        response.raise_for_status()
        model_data = response.json()
        
        logger.info(f"Successfully fetched model data from LiteLLM ({len(model_data)} models)")
        
        # Skip the sample spec
        if "sample_spec" in model_data:
            del model_data["sample_spec"]
        
        # Extract unique providers and track imported models
        providers_processed = set()
        models_imported = 0
        
        # Process each model - removed counter/limit to process all models
        for model_id, model_info in model_data.items():
            try:
                # Determine provider
                litellm_provider = model_info.get("litellm_provider", "")
                provider = litellm_provider.lower()
                
                # Apply special case rules
                if model_id.startswith("watsonx/"):
                    provider = "watsonx"
                elif "claude" in model_id.lower() and provider == "openai":
                    provider = "anthropic"
                
                # Use model name for inference if needed
                if not provider:
                    for part in model_id.lower().split('/'):
                        if part and part not in ['models', 'api']:
                            provider = part
                            break
                
                # Skip if provider couldn't be determined
                if not provider:
                    logger.warning(f"Could not determine provider for {model_id} - skipping")
                    continue
                
                # Get or create the provider
                provider_data = get_or_create_provider(provider, "llm")
                
                if not provider_data:
                    logger.error(f"Failed to get or create provider {provider}")
                    continue
                
                provider_id = provider_data["id"]
                providers_processed.add(provider)
                
                # Extract model capabilities
                capabilities = {
                    "supports_function_calling": model_info.get("supports_function_calling", False),
                    "supports_vision": model_info.get("supports_vision", False),
                    "supports_system_messages": model_info.get("supports_system_messages", False)
                }
                
                # Extract pricing information
                pricing = {
                    "input_cost_per_token": model_info.get("input_cost_per_token", 0),
                    "output_cost_per_token": model_info.get("output_cost_per_token", 0)
                }
                
                # Extract model name from model_id
                model_name = model_id.split("/")[-1] if "/" in model_id else model_id
                
                # Check if the model already exists - use explicit schema reference
                response = table(supabase, "models.llm_models").select("id").eq("model_id", model_id).execute()
                
                model_data = {
                    "provider_id": provider_id,
                    "model_id": model_id,
                    "name": model_name,
                    "display_name": model_name.replace('-', ' ').replace('_', ' ').title(),
                    "litellm_provider": litellm_provider,
                    "mode": model_info.get("mode", "chat"),
                    "max_tokens": model_info.get("max_tokens", 0),
                    "max_input_tokens": model_info.get("max_input_tokens", 0),
                    "max_output_tokens": model_info.get("max_output_tokens", 0),
                    "description": f"LLM model: {model_id}",
                    "is_active": True,
                    "updated_at": datetime.now().isoformat()
                }
                
                if response.data and len(response.data) > 0:
                    # Update existing model
                    model_pk = response.data[0]["id"]
                    table(supabase, "models.llm_models").update(model_data).eq("id", model_pk).execute()
                    logger.info(f"Updated existing model: {model_id}")
                else:
                    # Add created_at for new models
                    model_data["created_at"] = datetime.now().isoformat()
                    
                    # Insert new model
                    model_response = table(supabase, "models.llm_models").insert(model_data).execute()
                    
                    if not model_response.data or len(model_response.data) == 0:
                        logger.error(f"Failed to insert model {model_id}")
                        continue
                        
                    model_pk = model_response.data[0]["id"]
                    logger.info(f"Created new model: {model_id}")
                
                # Handle capabilities - use explicit schema reference
                capabilities_data = {
                    "model_id": model_pk,
                    "supports_function_calling": capabilities["supports_function_calling"],
                    "supports_vision": capabilities["supports_vision"],
                    "supports_system_messages": capabilities["supports_system_messages"],
                    "capability_matrix": json.dumps(capabilities),
                    "updated_at": datetime.now().isoformat()
                }
                
                # Check if capabilities record exists
                capabilities_response = table(supabase, "models.llm_capabilities").select("id").eq("model_id", model_pk).execute()
                
                if capabilities_response.data and len(capabilities_response.data) > 0:
                    # Update existing capabilities
                    capabilities_id = capabilities_response.data[0]["id"]
                    table(supabase, "models.llm_capabilities").update(capabilities_data).eq("id", capabilities_id).execute()
                else:
                    # Add created_at for new entries
                    capabilities_data["created_at"] = datetime.now().isoformat()
                    
                    # Insert new capabilities
                    table(supabase, "models.llm_capabilities").insert(capabilities_data).execute()
                
                # Handle pricing - use explicit schema reference
                pricing_data = {
                    "model_id": model_pk,
                    "input_cost_per_token": pricing["input_cost_per_token"],
                    "output_cost_per_token": pricing["output_cost_per_token"],
                    "currency": "USD",
                    "updated_at": datetime.now().isoformat()
                }
                
                # Check if pricing record exists
                pricing_response = table(supabase, "models.llm_pricing").select("id").eq("model_id", model_pk).execute()
                
                if pricing_response.data and len(pricing_response.data) > 0:
                    # Update existing pricing
                    pricing_id = pricing_response.data[0]["id"]
                    table(supabase, "models.llm_pricing").update(pricing_data).eq("id", pricing_id).execute()
                else:
                    # Add created_at for new entries
                    pricing_data["created_at"] = datetime.now().isoformat()
                    
                    # Insert new pricing
                    table(supabase, "models.llm_pricing").insert(pricing_data).execute()
                
                # Count as imported
                models_imported += 1
                
                # Log progress occasionally
                if models_imported % 50 == 0:
                    logger.info(f"Imported {models_imported} LLM models so far...")
                
            except Exception as e:
                logger.error(f"Error processing model {model_id}: {e}")
        
        logger.info(f"LLM import completed: {models_imported} models imported from {len(providers_processed)} providers")
        return models_imported
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching LiteLLM model data: {e}")
        return 0
    except Exception as e:
        logger.error(f"Error importing LLM models: {e}")
        return 0

def import_from_env() -> List[Dict[str, Any]]:
    """
    Extract embedding models from environment variables.
    Look for vars like OPENAI_EMBEDDING_MODEL, AZURE_EMBEDDING_MODEL, etc.
    """
    embedding_models = []
    
    # Look for common embedding model environment variables
    env_vars = {
        "OPENAI_EMBEDDING_MODEL": "openai",
        "OPENAI_EMBEDDING_DIMENSIONS": "openai",
        "AZURE_EMBEDDING_MODEL": "azure",
        "AZURE_EMBEDDING_DIMENSIONS": "azure",
        "COHERE_EMBEDDING_MODEL": "cohere",
        "COHERE_EMBEDDING_DIMENSIONS": "cohere",
        "HF_EMBEDDING_MODEL": "huggingface",
        "HUGGINGFACE_EMBEDDING_MODEL": "huggingface",
    }
    
    # Map of providers to their base models
    provider_defaults = {
        "openai": {
            "default_model": "text-embedding-3-small",
            "dimensions": 1536,
            "max_input_tokens": 8191
        },
        "azure": {
            "default_model": "text-embedding-ada-002",
            "dimensions": 1536,
            "max_input_tokens": 8191
        },
        "cohere": {
            "default_model": "embed-english-v3.0",
            "dimensions": 1024,
            "max_input_tokens": 512
        },
        "huggingface": {
            "default_model": "all-MiniLM-L6-v2",
            "dimensions": 384,
            "max_input_tokens": 256
        }
    }
    
    # Process environment variables
    for env_name, provider in env_vars.items():
        env_value = os.getenv(env_name)
        if env_value:
            # If it's a dimensions variable, skip (we'll use it with the model)
            if "DIMENSIONS" in env_name:
                continue
                
            # Get dimensions if available
            dimensions_var = f"{env_name.split('_MODEL')[0]}_DIMENSIONS"
            dimensions = os.getenv(dimensions_var)
            
            # Get model name and format model_id
            model_name = env_value
            if not model_name.startswith(provider + "/"):
                model_id = f"{provider}/{model_name}"
            else:
                model_id = model_name
                model_name = model_name.split("/")[1]
            
            # Use default dimensions if not specified
            if not dimensions and provider in provider_defaults:
                dimensions = provider_defaults[provider]["dimensions"]
            else:
                try:
                    dimensions = int(dimensions)
                except (TypeError, ValueError):
                    # If dimensions is not a valid integer, use default
                    dimensions = provider_defaults.get(provider, {}).get("dimensions", 1536)
            
            # Get max tokens from defaults or use a reasonable default
            max_tokens = provider_defaults.get(provider, {}).get("max_input_tokens", 8191)
            
            # Add to embedding models
            embedding_models.append({
                "model_id": model_id,
                "model_name": model_name,
                "provider": provider,
                "dimensions": dimensions,
                "max_input_tokens": max_tokens,
                "supports_batch": True,
                "supports_query_mapping": provider == "cohere",
                "input_cost_per_token": 0.0000001 if provider == "openai" else 0.0,
                "description": f"{provider.capitalize()} embedding model: {model_name}"
            })
    
    # Add default embedding models if none found in environment
    if not embedding_models:
        # Add standard embedding models
        embedding_models = [
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
            }
        ]
    
    return embedding_models

def import_embedding_models() -> int:
    """Import embedding models. Returns the number of models imported."""
    try:
        # Get embedding models from environment or use defaults
        embedding_models = import_from_env()
        
        # Track imported models and providers
        providers_processed = set()
        models_imported = 0
        
        # Process each model
        for model_info in embedding_models:
            try:
                model_id = model_info["model_id"]
                provider_name = model_info["provider"]
                model_name = model_info["model_name"]
                
                # Get or create the provider
                provider_data = get_or_create_provider(provider_name, "embedding")
                
                if not provider_data:
                    logger.error(f"Failed to get or create provider {provider_name}")
                    continue
                
                provider_id = provider_data["id"]
                providers_processed.add(provider_name)
                
                # Check if the model already exists - use explicit schema reference
                response = table(supabase, "models.embedding_models").select("id").eq("model_id", model_id).execute()
                
                model_data = {
                    "provider_id": provider_id,
                    "model_id": model_id,
                    "name": model_name,
                    "display_name": model_name.replace('-', ' ').replace('_', ' ').title(),
                    "dimensions": model_info.get("dimensions", 0),
                    "max_input_tokens": model_info.get("max_input_tokens", 0),
                    "supports_batch": model_info.get("supports_batch", True),
                    "supports_query_mapping": model_info.get("supports_query_mapping", False),
                    "description": model_info.get("description", f"Embedding model: {model_id}"),
                    "is_active": True,
                    "updated_at": datetime.now().isoformat()
                }
                
                if response.data and len(response.data) > 0:
                    # Update existing model
                    model_pk = response.data[0]["id"]
                    table(supabase, "models.embedding_models").update(model_data).eq("id", model_pk).execute()
                    logger.info(f"Updated existing embedding model: {model_id}")
                else:
                    # Add created_at for new models
                    model_data["created_at"] = datetime.now().isoformat()
                    
                    # Insert new model
                    model_response = table(supabase, "models.embedding_models").insert(model_data).execute()
                    
                    if not model_response.data or len(model_response.data) == 0:
                        logger.error(f"Failed to insert embedding model {model_id}")
                        continue
                        
                    model_pk = model_response.data[0]["id"]
                    logger.info(f"Created new embedding model: {model_id}")
                
                # Handle pricing - use explicit schema reference
                pricing_data = {
                    "model_id": model_pk,
                    "input_cost_per_token": model_info.get("input_cost_per_token", 0),
                    "batch_cost_per_token": model_info.get("batch_cost_per_token", model_info.get("input_cost_per_token", 0)),
                    "currency": "USD",
                    "updated_at": datetime.now().isoformat()
                }
                
                # Check if pricing record exists
                pricing_response = table(supabase, "models.embedding_pricing").select("id").eq("model_id", model_pk).execute()
                
                if pricing_response.data and len(pricing_response.data) > 0:
                    # Update existing pricing
                    pricing_id = pricing_response.data[0]["id"]
                    table(supabase, "models.embedding_pricing").update(pricing_data).eq("id", pricing_id).execute()
                else:
                    # Add created_at for new entries
                    pricing_data["created_at"] = datetime.now().isoformat()
                    
                    # Insert new pricing
                    table(supabase, "models.embedding_pricing").insert(pricing_data).execute()
                
                # Count as imported
                models_imported += 1
                
            except Exception as e:
                logger.error(f"Error processing embedding model {model_info.get('model_id')}: {e}")
        
        logger.info(f"Embedding import completed: {models_imported} models imported from {len(providers_processed)} providers")
        return models_imported
        
    except Exception as e:
        logger.error(f"Error importing embedding models: {e}")
        return 0

def add_import_log(entity_name: str, entity_type: str, status: str, message: str) -> None:
    """Add an import log entry to the audit.import_logs table."""
    try:
        # Generate import session ID
        import_session = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create log entry
        log_data = {
            "import_session": import_session,
            "entity_name": entity_name,
            "entity_type": entity_type,
            "status": status,
            "message": message,
            "created_at": datetime.now().isoformat()
        }
        
        # Insert the log with explicit schema reference
        table(supabase, "audit.import_logs").insert(log_data).execute()
        logger.info(f"Added import log for {entity_name}")
        
    except Exception as e:
        logger.error(f"Error adding import log: {e}")

def main():
    """Main function to run the import."""
    logger.info("Starting model import process...")
    
    # Import LLM models
    llm_count = import_llm_models()
    
    # Import embedding models
    embedding_count = import_embedding_models()
    
    # Log the results
    logger.info(f"Import completed: {llm_count} LLM models and {embedding_count} embedding models imported")
    
    # Record in audit log
    add_import_log(
        entity_name="model_import",
        entity_type="batch_import",
        status="success",
        message=f"Successfully imported {llm_count} LLM models and {embedding_count} embedding models"
    )
    
    return llm_count + embedding_count

if __name__ == "__main__":
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="Import LLM and embedding models to Supabase")
    parser.add_argument("--model-type", choices=["llm", "embedding", "all"], default="all", help="Type of models to import")
    args = parser.parse_args()
    
    # Run appropriate import based on arguments
    if args.model_type == "llm":
        llm_count = import_llm_models()
        logger.info(f"Imported {llm_count} LLM models")
        sys.exit(0 if llm_count > 0 else 1)
    elif args.model_type == "embedding":
        embedding_count = import_embedding_models()
        logger.info(f"Imported {embedding_count} embedding models")
        sys.exit(0 if embedding_count > 0 else 1)
    else:
        total = main()
        sys.exit(0 if total > 0 else 1)