#!/usr/bin/env python
"""Haive Vault CLI.

A command-line utility for managing vault secrets and model imports.

Usage:
    python haive_vault_cli.py [command] [options]

Commands:
    migrate     Migrate API keys and secrets to the vault
    import      Import LLM and embedding models
    verify      Verify vault secret references
    help        Show this help message
"""

import argparse
import logging
import os
import sys
from datetime import datetime

# Try to import tqdm for progress bars
try:
    from tqdm import tqdm

    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False
    print("tqdm not available. Install with 'pip install tqdm' for progress bars.")

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(
            f"haive_vault_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        ),
    ],
)
logger = logging.getLogger(__name__)


def run_migrate():
    """Run the migration script."""
    try:
        from src.haive.dataflow.registry.utils.vault_migration_script import (
            add_vault_helper_functions,
            migrate_component_env_mappings,
            migrate_engine_api_keys,
            migrate_env_vars_to_vault,
            migrate_provider_api_keys,
        )

        logger.info("Starting vault reference migration...")

        # 1. First, migrate environment variables
        logger.info("Migrating environment variables...")
        migrate_env_vars_to_vault()

        # 2. Update component environment mappings
        logger.info("Migrating component environment mappings...")
        migrate_component_env_mappings()

        # 3. Migrate provider API keys
        logger.info("Migrating provider API keys...")
        migrate_provider_api_keys()

        # 4. Migrate engine API keys
        logger.info("Migrating engine API keys...")
        migrate_engine_api_keys()

        # 5. Add helper functions for accessing vault secrets
        logger.info("Adding vault helper functions...")
        add_vault_helper_functions()

        logger.info("Migration completed successfully")

    except ImportError:
        logger.error(
            "Could not import vault migration script. Make sure it's in the current directory."
        )
        return 1
    except Exception as e:
        logger.error(f"Error during migration: {e}")
        return 1

    return 0


def run_import(
    model_type=None, skip_llm=False, skip_embeddings=False, no_progress=False
):
    """Run the model importer."""
    try:
        from src.haive.dataflow.registry.importers.litellm_importer import (
            import_embedding_models,
            import_llm_models,
            update_availability_status,
        )

        # Override TQDM_AVAILABLE if progress bars are explicitly disabled
        if no_progress and "TQDM_AVAILABLE" in globals():
            global TQDM_AVAILABLE
            orig_value = TQDM_AVAILABLE
            TQDM_AVAILABLE = False
            logger.info("Progress bars disabled by user request")

        logger.info("Starting model import process...")

        llm_count = 0
        embedding_count = 0

        # Import LLM models if not skipped
        if not skip_llm and (model_type is None or model_type.lower() == "llm"):
            llm_count = import_llm_models()

        # Import embedding models if not skipped
        if not skip_embeddings and (
            model_type is None or model_type.lower() == "embedding"
        ):
            embedding_count = import_embedding_models()

        # Update availability status
        update_availability_status()

        # Log the results
        logger.info(
            f"Import completed: {llm_count} LLM models and {embedding_count} embedding models imported"
        )

        # Restore original TQDM_AVAILABLE value if it was overridden
        if no_progress and "orig_value" in locals():
            global TQDM_AVAILABLE
            TQDM_AVAILABLE = orig_value

    except ImportError:
        logger.error(
            "Could not import unified importer script. Make sure it's in the current directory."
        )
        return 1
    except Exception as e:
        logger.error(f"Error during import: {e}")
        return 1

    return 0


def run_verify():
    """Run the verification script."""
    try:
        from src.haive.dataflow.registry.utils.vault_migration_script import (
            generate_report,
        )

        logger.info("Starting vault secret verification...")
        generate_report()
        logger.info("Verification complete")

    except ImportError:
        logger.error(
            "Could not import verification script. Make sure it's in the current directory."
        )
        return 1
    except Exception as e:
        logger.error(f"Error during verification: {e}")
        return 1

    return 0


def main():
    parser = argparse.ArgumentParser(description="Haive Vault CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Migrate command
    migrate_parser = subparsers.add_parser(
        "migrate", help="Migrate API keys and secrets to the vault"
    )

    # Import command
    import_parser = subparsers.add_parser(
        "import", help="Import LLM and embedding models"
    )
    import_parser.add_argument(
        "--model-type",
        choices=["llm", "embedding"],
        help="Type of models to import (default: both)",
    )
    import_parser.add_argument(
        "--skip-llm", action="store_true", help="Skip LLM model import"
    )
    import_parser.add_argument(
        "--skip-embeddings", action="store_true", help="Skip embedding model import"
    )
    import_parser.add_argument(
        "--no-progress", action="store_true", help="Disable progress bars"
    )

    # Verify command
    verify_parser = subparsers.add_parser(
        "verify", help="Verify vault secret references"
    )

    # Parse arguments
    args = parser.parse_args()

    # If no command provided, show help
    if not args.command:
        parser.print_help()
        return 0

    # Execute the appropriate command
    if args.command == "migrate":
        return run_migrate()
    elif args.command == "import":
        return run_import(
            args.model_type, args.skip_llm, args.skip_embeddings, args.no_progress
        )
    elif args.command == "verify":
        return run_verify()
    elif args.command == "help":
        parser.print_help()
        return 0
    else:
        logger.error(f"Unknown command: {args.command}")
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
