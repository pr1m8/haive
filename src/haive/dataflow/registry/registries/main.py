#!/usr/bin/env python
"""
Test script for the LLM and Embedding model registry system.
"""

import json
import logging
import os
import traceback

from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("registry-test")

# Load environment variables from .env file
load_dotenv()
logger.info("Loaded environment variables from .env file")


def ensure_registry_schema(client):
    """Ensure the registry schema exists in database."""
    try:
        # Use the rpc method to execute SQL
        logger.info("Checking for models schema")
        result = client.rpc(
            "execute_sql",
            {
                "sql": "SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'models'"
            },
        ).execute()

        if not result.data or len(result.data) == 0:
            logger.info("Creating models schema...")
            client.rpc(
                "execute_sql", {"sql": "CREATE SCHEMA IF NOT EXISTS models"}
            ).execute()
            logger.info("Created models schema")

        return True
    except Exception as e:
        logger.exception(f"Error ensuring registry schema: {e}")
        traceback.print_exc()
        return False


def ensure_provider_types(client):
    """Ensure provider types exist in database."""
    try:

        # First run a simple check to see if the provider_types table exists
        check_sql = "SELECT to_regclass('models.provider_types')"
        check_result = client.rpc("execute_sql", {"sql": check_sql}).execute()

        # Create the table if it doesn't exist (to_regclass returns null for non-existent tables)
        if not check_result.data or check_result.data[0].get("to_regclass") is None:
            logger.info("Creating provider_types table...")

            # Split the CREATE TABLE statement into multiple simpler statements
            # PostgreSQL requires CREATE TABLE to be its own statement
            create_table_sql = """
                CREATE TABLE IF NOT EXISTS models.provider_types (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    name VARCHAR(50) NOT NULL UNIQUE,
                    display_name VARCHAR(100) NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                )
            """

            client.rpc("execute_sql", {"sql": create_table_sql}).execute()
            logger.info("Provider_types table created successfully")

        # Check if provider_types table has data using a simpler query
        provider_types_query = "SELECT * FROM models.provider_types"
        provider_types = client.rpc(
            "execute_sql", {"sql": provider_types_query}
        ).execute()

        # Ensure llm provider type exists
        llm_exists = False
        if provider_types.data:
            for item in provider_types.data:
                if item.get("name") == "llm":
                    llm_exists = True
                    break

        if not llm_exists:
            logger.info("Creating LLM provider type...")
            insert_llm_sql = """
                INSERT INTO models.provider_types (name, display_name, description, created_at)
                VALUES ('llm', 'LLM Provider', 'Provider for Large Language Models', NOW())
                ON CONFLICT (name) DO NOTHING
            """
            client.rpc("execute_sql", {"sql": insert_llm_sql}).execute()

        # Ensure embedding provider type exists
        embedding_exists = False
        if provider_types.data:
            for item in provider_types.data:
                if item.get("name") == "embedding":
                    embedding_exists = True
                    break

        if not embedding_exists:
            logger.info("Creating Embedding provider type...")
            insert_embedding_sql = """
                INSERT INTO models.provider_types (name, display_name, description, created_at)
                VALUES ('embedding', 'Embedding Provider', 'Provider for Embedding Models', NOW())
                ON CONFLICT (name) DO NOTHING
            """
            client.rpc("execute_sql", {"sql": insert_embedding_sql}).execute()

        logger.info("Provider types setup complete")
        return True
    except Exception as e:
        logger.exception(f"Error ensuring provider types: {e}")
        traceback.print_exc()
        return False


def main():
    """Main test function."""
    logger.info("Starting registry system test")

    # Import model registry
    try:
        # Check which API keys are set
        logger.info("🔑 Checking available API keys in environment:")
        providers = [
            ("OpenAI", "OPENAI_API_KEY"),
            ("Azure OpenAI", "AZURE_OPENAI_API_KEY"),
            ("Anthropic", "ANTHROPIC_API_KEY"),
            ("Google (Gemini)", "GOOGLE_API_KEY"),
            ("Mistral AI", "MISTRAL_API_KEY"),
            ("Cohere", "COHERE_API_KEY"),
            ("HuggingFace", "HUGGING_FACE_API_KEY"),
        ]

        for provider_name, env_var in providers:
            if os.getenv(env_var):
                logger.info(f"  ✅ {provider_name} API key found ({env_var})")
            else:
                logger.info(f"  ❌ {provider_name} API key not found ({env_var})")

        # Import model definitions first to show they're being accessed directly
        logger.info("\n📚 Importing model definitions directly from importers:")

        # Try to import embedding models data
        try:
            from src.haive.dataflow.registry.importers.embeddings_importer import (
                EMBEDDING_MODELS,
            )

            logger.info(
                f"  ✅ Found {len(EMBEDDING_MODELS)} embedding models in embeddings_importer"
            )

            # Show a sample of embedding models
            sample_size = min(3, len(EMBEDDING_MODELS))
            logger.info("  Sample of embedding models:")
            for i in range(sample_size):
                model = EMBEDDING_MODELS[i]
                logger.info(
                    f"    - {model['model_id']} ({model['dimensions']} dimensions, {model['provider']} provider)"
                )
        except ImportError:
            logger.warning("  ❌ Could not import embedding models data")

        # Try to import LiteLLM
        try:
            from src.haive.dataflow.registry.importers.litellm_importer import (
                import_llm_models,
            )

            logger.info(
                "  ✅ LiteLLM importer is available (imports models from GitHub)")"
            )
        except ImportError:
            logger.warning("  ❌ Could not import LiteLLM importer")

        # Now create model registry and test its functionality
        logger.info("\n🔍 Testing model registry client:")
        from src.haive.dataflow.registry.registries.model_registry import ModelRegistry

        # Create the model registry client
        client = ModelRegistry()
        logger.info("  ✅ Model Registry client initialized")

        # Try to detect environment variables
        env_vars = client.detect_environment_variables()
        logger.info(f"  Detected environment variables for: {list(env_vars.keys())}")

        # Update provider availability
        client.update_provider_availability()

        # Get available LLM providers
        llm_providers = client.get_available_llm_providers()
        logger.info(
            f"  Available LLM providers: {[p.get('name') for p in llm_providers]}"
        )

        # Get available embedding providers
        embed_providers = client.get_available_embedding_providers()
        logger.info(
            f"  Available embedding providers: {[p.get('name') for p in embed_providers]}"
        )

        # Get embedding models (from cache/importers, not just database)
        logger.info("\n📊 Getting models from Registry:")

        # Get embedding models (available and all)
        available_embed_models = client.get_embedding_models(only_available=True)
        all_embed_models = client.get_embedding_models()

        logger.info(
            f"  Found {len(available_embed_models)} available embedding models (out of {len(all_embed_models)} total)"
        )

        # Get LLM models (available and all)
        available_llm_models = client.get_llm_models(only_available=True)
        all_llm_models = client.get_llm_models()

        logger.info(
            f"  Found {len(available_llm_models)} available LLM models (out of {len(all_llm_models)} total)"
        )

        # Print sample model info for first available embedding model
        if available_embed_models:
            logger.info("\n📋 Sample embedding model details:")
            sample_embed = available_embed_models[0]
            logger.info(f"  Model ID: {sample_embed.get('model_id', 'Unknown')}")
            logger.info(f"  Provider: {sample_embed.get('provider', 'Unknown')}")
            logger.info(f"  Dimensions: {sample_embed.get('dimensions', 'Unknown')}")
            logger.info(
                f"  Max tokens: {sample_embed.get('max_input_tokens', 'Unknown')}"
            )
            logger.info(
                f"  Pricing: {sample_embed.get('pricing', {}).get('input_cost_per_token', 'Unknown')} per token"
            )

        # Print sample model info for first available LLM model
        if available_llm_models:
            logger.info("\n📋 Sample LLM model details:")
            sample_model = available_llm_models[0]
            logger.info(f"  Model ID: {sample_model.get('model_id', 'Unknown')}")
            logger.info(f"  Provider: {sample_model.get('provider', 'Unknown')}")
            logger.info(f"  Max tokens: {sample_model.get('max_tokens', 'Unknown')}")

            # Get full model details
            model_id = sample_model.get("model_id")
            if model_id:
                model_details = client.get_llm_model(model_id)
                if model_details and "capabilities" in model_details:
                    capabilities = model_details["capabilities"]
                    logger.info("  Capabilities:")
                    for cap, value in capabilities.items():
                        if (
                            cap != "id"
                            and cap != "model_id"
                            and cap != "created_at"
                            and cap != "updated_at"
                        ) and value:
                            logger.info(f"    - {cap}: {value}")

        logger.info("\n✅ Registry test completed")

    except ImportError as e:
        logger.error(f"Failed to import registry components: {e}")
        traceback.print_exc()
        logger.info("Make sure your Python path includes the project directory")
    except Exception as e:
        logger.error(f"Test failed with error: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
