#!/usr/bin/env python
"""
Test script for the LLM and Embedding model registry system.
"""

import os
import logging
import json
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("registry-test")

# Load environment variables from .env file
load_dotenv()

def main():
    """Main test function."""
    logger.info("Starting registry system test")
    
    # Import registry components
    try:
        from src.haive.dataflow.registry.core import registry_system
        from src.haive.dataflow.registry.models import EntityType
        
        # Import LiteLLM models
        logger.info("Importing LLM models from LiteLLM...")
        from src.haive.dataflow.registry.importers.litellm_importer import import_llm_models
        
        import_success = import_llm_models()
        if import_success:
            logger.info("✅ Successfully imported LLM models")
        else:
            logger.error("❌ Failed to import LLM models")
        
        # Import embedding models
        logger.info("Importing embedding models...")
        from src.haive.dataflow.registry.importers.embeddings_importer import import_embedding_models
        
        embed_success = import_embedding_models()
        if embed_success:
            logger.info("✅ Successfully imported embedding models")
        else:
            logger.error("❌ Failed to import embedding models")
            
        # Test the model registry client
        logger.info("Testing model registry client...")
        from src.haive.dataflow.registry.registries.model_registry import ModelRegistry
        
        client = ModelRegistry()
        
        # Try to detect environment variables
        env_vars = client.detect_environment_variables()
        logger.info(f"Detected environment variables for: {list(env_vars.keys())}")
        
        # Update provider availability
        client.update_provider_availability()
        
        # Get available LLM providers
        llm_providers = client.get_available_llm_providers()
        logger.info(f"Available LLM providers: {[p['name'] for p in llm_providers]}")
        
        # Get available embedding providers
        embed_providers = client.get_available_embedding_providers()
        logger.info(f"Available embedding providers: {[p['name'] for p in embed_providers]}")
        
        # Get LLM models for available providers
        available_llm_models = client.get_llm_models(only_available=True)
        logger.info(f"Found {len(available_llm_models)} available LLM models")
        
        # Get embedding models for available providers
        available_embed_models = client.get_embedding_models(only_available=True)
        logger.info(f"Found {len(available_embed_models)} available embedding models")
        
        # Print sample model info for first available model
        if available_llm_models:
            sample_model = available_llm_models[0]
            print(sample_model)
            logger.info(f"Sample LLM model: {sample_model['model_id']}")
            logger.info(f"  Provider: {sample_model['provider']}")
            logger.info(f"  Max tokens: {sample_model['max_tokens']}")
            
            # Get full model details
            model_details = client.get_llm_model(sample_model['model_id'])
            if model_details and 'capabilities' in model_details:
                capabilities = model_details['capabilities']
                logger.info("  Capabilities:")
                for cap, value in capabilities.items():
                    if cap != 'id' and cap != 'model_id' and cap != 'created_at' and cap != 'updated_at':
                        if value:
                            logger.info(f"    - {cap}: {value}")
            
        # Print sample model info for first available embedding model
        if available_embed_models:
            sample_embed = available_embed_models[0]
            logger.info(f"Sample embedding model: {sample_embed['model_id']}")
            logger.info(f"  Provider: {sample_embed['provider']}")
            logger.info(f"  Dimensions: {sample_embed['dimensions']}")
            
        logger.info("Registry test completed")
        
    except ImportError as e:
        logger.error(f"Failed to import registry components: {e}")
        logger.info("Make sure your Python path includes the project directory")
    except Exception as e:
        logger.error(f"Test failed with error: {e}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main()