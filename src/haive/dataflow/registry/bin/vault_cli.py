#!/usr/bin/env python
"""Fixed Vault CLI.

A command-line utility to manage vault secrets and model imports,
with proper schema mapping for Supabase.
"""

import argparse
import importlib.util
import logging
import os
import sys
from datetime import datetime
from typing import Any

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(
            f"vault_cli_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        ),
    ],
)
logger = logging.getLogger(__name__)

# Get the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))


def find_module_path(module_name):
    """Find and import a module from the given paths."""
    possible_paths = [
        os.path.join(script_dir, f"{module_name}.py"),
        os.path.join(script_dir, f"utils/{module_name}.py"),
        os.path.join(script_dir, f"../utils/{module_name}.py"),
        os.path.join(script_dir, f"bin/{module_name}.py"),
        os.path.join(script_dir, f"../bin/{module_name}.py"),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    return None


def import_module(module_name, module_path):
    """Import a module from a file path."""
    if not module_path:
        return None

    try:
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        logger.exception(f"Error importing {module_name} from {module_path}: {e}")
        return None


def execute_sql(sql: str) -> Any:
    """Execute SQL safely through Supabase RPC function."""
    try:
        # Import the sanitize_sql function if available
        try:
            from src.haive.dataflow.db.supabase import get_supabase_client, sanitize_sql

            # Sanitize SQL by removing trailing semicolons and whitespace
            sanitized_sql = sanitize_sql(sql)
        except ImportError:
            # Simple sanitization if the function isn't available
            sanitized_sql = sql.strip().rstrip(";").strip()
            from src.haive.dataflow.db.supabase import get_supabase_client

        # Get Supabase client and execute the query
        supabase = get_supabase_client()

        # Execute the SQL via the RPC function
        response = supabase.rpc("execute_sql", {"sql": sanitized_sql}).execute()

        # Check for errors in the response
        if hasattr(response, "error") and response.error:
            logger.error(f"SQL execution error: {response.error}")
            return None

        return response

    except Exception as e:
        logger.exception(f"Error executing SQL: {e}")
        return None


def ensure_vault_reference_column(table_name: str) -> bool:
    """Ensure the table has a vault_reference column for secret references.
    Uses table() helper function for proper schema resolution.

    Args:
        table_name: Full table name including schema

    Returns:
        True if column exists or was created, False otherwise
    """
    try:
        from src.haive.dataflow.db.supabase import (
            get_supabase_client,
            sanitize_sql,
        )

        supabase = get_supabase_client()

        schema, table_base = table_name.split(".")

        # First, check if the column exists by testing information_schema
        # This is more reliable than checking the table data
        check_sql = f"""
        SELECT column_name FROM information_schema.columns
        WHERE table_schema = '{schema}' AND table_name = '{table_base}'
        AND column_name = 'vault_secret_id'
        """
        check_result = supabase.rpc(
            "execute_sql", {"sql": sanitize_sql(check_sql)}
        ).execute()

        if check_result.data and len(check_result.data) > 0:
            logger.info(f"Column vault_secret_id already exists in {table_name}")
            return True

        # If we get here, column doesn't exist, so add it
        add_column_sql = f"""
        ALTER TABLE {table_name}
        ADD COLUMN IF NOT EXISTS vault_secret_id UUID REFERENCES vault.secrets(id)
        """

        result = supabase.rpc(
            "execute_sql", {"sql": sanitize_sql(add_column_sql)}
        ).execute()

        if hasattr(result, "error") and result.error:
            logger.error(f"Failed to add column to {table_name}: {result.error}")
            return False

        logger.info(f"Added vault_secret_id column to {table_name}")

        # If this is engines.engines, also add config_vault_refs column
        if table_name == "engines.engines":
            add_refs_sql = """
            ALTER TABLE engines.engines
            ADD COLUMN IF NOT EXISTS config_vault_refs JSONB DEFAULT '{}'::jsonb
            """

            refs_result = supabase.rpc(
                "execute_sql", {"sql": sanitize_sql(add_refs_sql)}
            ).execute()

            if hasattr(refs_result, "error") and refs_result.error:
                logger.error(
                    f"Failed to add config_vault_refs to engines.engines: {refs_result.error}"
                )
            else:
                logger.info("Added config_vault_refs column to engines.engines")

        return True

    except Exception as e:
        logger.exception(f"Error ensuring vault_reference column on {table_name}: {e}")
        logger.info(
            f"Please run this SQL in your database: ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS vault_secret_id UUID REFERENCES vault.secrets(id);"
        )
        return False


def run_migrate(args):
    """Run the vault migration."""
    logger.info("Starting vault migration...")

    # Find and import the vault migration script
    module_path = find_module_path("vault_migration_script")
    if module_path:
        migration_module = import_module("vault_migration_script", module_path)
        if migration_module and hasattr(migration_module, "main"):
            try:
                # Patch the module with our fixed functions
                migration_module.execute_sql = execute_sql
                migration_module.ensure_vault_reference_column = (
                    ensure_vault_reference_column
                )

                result = migration_module.main()
                return 0 if result in [0, None] else result
            except Exception as e:
                logger.exception(f"Error running migration: {e}")
                return 1
        else:
            logger.error("Could not find main function in vault migration module")
            return 1
    else:
        logger.error("Could not find vault_migration_script.py")
        return 1


def run_import(args):
    """Run the model import."""
    logger.info("Starting model import...")

    # Find and import the model importer script
    module_path = find_module_path("model_importer")
    if module_path:
        importer_module = import_module("model_importer", module_path)
        if importer_module and hasattr(importer_module, "main"):
            try:
                # Patch the module with our fixed execute_sql function if it uses it
                if hasattr(importer_module, "execute_sql"):
                    importer_module.execute_sql = execute_sql

                # Check for model type filtering
                if args.model_type == "llm" or args.skip_embeddings:
                    logger.info("Importing only LLM models")
                    if hasattr(importer_module, "import_llm_models"):
                        llm_count = importer_module.import_llm_models()
                        logger.info(f"Imported {llm_count} LLM models")
                        return 0 if llm_count > 0 else 1

                if args.model_type == "embedding" or args.skip_llm:
                    logger.info("Importing only embedding models")
                    if hasattr(importer_module, "import_embedding_models"):
                        embedding_count = importer_module.import_embedding_models()
                        logger.info(f"Imported {embedding_count} embedding models")
                        return 0 if embedding_count > 0 else 1

                # If no filtering, run the full import
                result = importer_module.main()
                return 0 if result > 0 else 1
            except Exception as e:
                logger.exception(f"Error running model import: {e}")
                return 1
        else:
            logger.error("Could not find main function in model importer module")
            return 1
    else:
        logger.error("Could not find model_importer.py")
        return 1


def run_verify(args):
    """Run the vault verification."""
    logger.info("Starting vault verification...")

    # Find and import the verification script
    module_path = find_module_path("verify_vault_secrets")
    if module_path:
        verify_module = import_module("verify_vault_secrets", module_path)
        if verify_module and hasattr(verify_module, "generate_report"):
            try:
                # Patch the module with our fixed execute_sql function if it uses it
                if hasattr(verify_module, "execute_sql"):
                    verify_module.execute_sql = execute_sql

                verify_module.generate_report()
                return 0
            except Exception as e:
                logger.exception(f"Error running vault verification: {e}")
                return 1
        else:
            logger.error(
                "Could not find generate_report function in verification module"
            )
            return 1
    else:
        logger.error("Could not find verify_vault_secrets.py")
        return 1


def add_columns(args):
    """Add the vault reference columns to the database tables using table() helper."""
    logger.info("Adding vault reference columns to database tables...")

    try:
        from src.haive.dataflow.db.supabase import get_supabase_client, sanitize_sql

        supabase = get_supabase_client()
    except ImportError:
        logger.exception(
            "Cannot import Supabase client. Make sure it's properly installed and configured."
        )
        return 1

    # Define the tables that need columns added
    tables = [
        "config.environment_variables",
        "config.component_env_mappings",
        "models.providers",
        "engines.engines",
    ]

    success = True

    # Add the columns to each table
    for table_name in tables:
        if ensure_vault_reference_column(table_name):
            logger.info(f"Successfully handled vault_secret_id column for {table_name}")
        else:
            success = False

    # Add the helper functions
    try:
        # Create get_vault_secret function
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

        result = supabase.rpc(
            "execute_sql", {"sql": sanitize_sql(secret_func_sql)}
        ).execute()

        if not hasattr(result, "error") or not result.error:
            logger.info("Created get_vault_secret function")
        else:
            logger.error(f"Failed to create get_vault_secret function: {result.error}")
            success = False

        # Create get_vault_secret_by_name function
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

        result = supabase.rpc(
            "execute_sql", {"sql": sanitize_sql(name_func_sql)}
        ).execute()

        if not hasattr(result, "error") or not result.error:
            logger.info("Created get_vault_secret_by_name function")
        else:
            logger.error(
                f"Failed to create get_vault_secret_by_name function: {result.error}"
            )
            success = False
    except Exception as e:
        logger.exception(f"Error creating vault helper functions: {e}")
        success = False

    return 0 if success else 1


def run_export(args):
    """Export secrets from the vault."""
    logger.info("Exporting vault secrets...")

    # Find and import the export script
    module_path = find_module_path("vault_export")
    if not module_path:
        # Try to create export functionality directly
        try:
            import json
            import os

            from src.haive.dataflow.db.supabase import get_supabase_client, table

            supabase = get_supabase_client()

            # Get all decrypted secrets
            response = table(supabase, "vault.decrypted_secrets").select("*").execute()

            if not response.data:
                logger.info("No secrets found in vault")
                return 1

            secrets = response.data
            logger.info(f"Found {len(secrets)} secrets in vault")

            # Create export directory
            export_dir = args.output_dir or "vault_export"
            os.makedirs(export_dir, exist_ok=True)

            # Export to file
            export_file = os.path.join(
                export_dir,
                f"vault_secrets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            )

            # Format secrets for export
            export_data = []
            for secret in secrets:
                export_data.append(
                    {
                        "name": secret["name"],
                        "description": secret["description"],
                        "value": secret["decrypted_secret"],
                        "created_at": secret["created_at"],
                        "updated_at": secret["updated_at"],
                    }
                )

            # Write to file
            with open(export_file, "w") as f:
                json.dump(export_data, f, indent=2)

            logger.info(f"Exported {len(export_data)} secrets to {export_file}")

            # Create .env file if requested
            if args.env_file:
                env_file = os.path.join(export_dir, ".env")
                with open(env_file, "w") as f:
                    for secret in secrets:
                        f.write(f'{secret["name"]}="{secret["decrypted_secret"]}"\n')
                logger.info(f"Created .env file at {env_file}")

            return 0

        except Exception as e:
            logger.exception(f"Error exporting vault secrets: {e}")
            return 1
    else:
        # Use the export script if found
        export_module = import_module("vault_export", module_path)
        if export_module and hasattr(export_module, "export_secrets"):
            try:
                export_module.export_secrets(
                    output_dir=args.output_dir, env_file=args.env_file
                )
                return 0
            except Exception as e:
                logger.exception(f"Error running vault export: {e}")
                return 1
        else:
            logger.error("Could not find export_secrets function in export module")
            return 1


def run_import_secrets(args):
    """Import secrets into the vault."""
    logger.info("Importing secrets into vault...")

    # Check if input file exists
    if not args.input_file or not os.path.exists(args.input_file):
        logger.error(f"Input file not found: {args.input_file}")
        return 1

    # Find and import the import script
    module_path = find_module_path("vault_import")
    if not module_path:
        # Try to create import functionality directly
        try:
            import json

            from src.haive.dataflow.db.supabase import get_supabase_client, table

            supabase = get_supabase_client()

            # Read the input file
            with open(args.input_file) as f:
                import_data = json.load(f)

            if not import_data:
                logger.error("No data found in import file")
                return 1

            logger.info(f"Found {len(import_data)} secrets in import file")

            # Import each secret
            imported_count = 0
            updated_count = 0

            for secret_data in import_data:
                try:
                    name = secret_data.get("name")
                    value = secret_data.get("value")
                    description = secret_data.get(
                        "description", f"Imported secret: {name}"
                    )

                    if not name or not value:
                        logger.warning("Skipping secret with missing name or value")
                        continue

                    # Check if secret already exists
                    response = (
                        table(supabase, "vault.secrets")
                        .select("id")
                        .eq("name", name)
                        .execute()
                    )

                    if response.data and len(response.data) > 0:
                        # Update existing secret if overwrite is enabled
                        if args.overwrite:
                            secret_id = response.data[0]["id"]

                            # Update the secret
                            update_response = (
                                table(supabase, "vault.secrets")
                                .update(
                                    {
                                        "description": description,
                                        "secret": value,
                                        "updated_at": datetime.now().isoformat(),
                                    }
                                )
                                .eq("id", secret_id)
                                .execute()
                            )

                            if update_response.data and len(update_response.data) > 0:
                                updated_count += 1
                                logger.info(f"Updated existing secret: {name}")
                            else:
                                logger.error(f"Failed to update secret: {name}")
                        else:
                            logger.info(f"Secret already exists (skipping): {name}")
                    else:
                        # Create new secret
                        insert_response = (
                            table(supabase, "vault.secrets")
                            .insert(
                                {
                                    "name": name,
                                    "description": description,
                                    "secret": value,
                                    "created_at": datetime.now().isoformat(),
                                }
                            )
                            .execute()
                        )

                        if insert_response.data and len(insert_response.data) > 0:
                            imported_count += 1
                            logger.info(f"Imported new secret: {name}")
                        else:
                            logger.error(f"Failed to import secret: {name}")

                except Exception as e:
                    logger.exception(f"Error importing secret: {e}")

            logger.info(
                f"Import completed: {imported_count} secrets imported, {updated_count} secrets updated"
            )
            return 0 if imported_count > 0 or updated_count > 0 else 1

        except Exception as e:
            logger.exception(f"Error importing vault secrets: {e}")
            return 1
    else:
        # Use the import script if found
        import_module = import_module("vault_import", module_path)
        if import_module and hasattr(import_module, "import_secrets"):
            try:
                import_module.import_secrets(
                    input_file=args.input_file, overwrite=args.overwrite
                )
                return 0
            except Exception as e:
                logger.exception(f"Error running vault import: {e}")
                return 1
        else:
            logger.error("Could not find import_secrets function in import module")
            return 1


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="Vault Management CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Migrate command
    migrate_parser = subparsers.add_parser(
        "migrate", help="Migrate API keys and secrets to vault"
    )
    migrate_parser.set_defaults(func=run_migrate)

    # Import command
    import_parser = subparsers.add_parser(
        "import-models", help="Import LLM and embedding models"
    )
    import_parser.add_argument(
        "--model-type",
        choices=["llm", "embedding", "all"],
        default="all",
        help="Type of models to import",
    )
    import_parser.add_argument(
        "--skip-llm", action="store_true", help="Skip LLM models"
    )
    import_parser.add_argument(
        "--skip-embeddings", action="store_true", help="Skip embedding models"
    )
    import_parser.set_defaults(func=run_import)

    # Verify command
    verify_parser = subparsers.add_parser("verify", help="Verify vault secrets")
    verify_parser.set_defaults(func=run_verify)

    # Add columns command
    columns_parser = subparsers.add_parser(
        "add-columns", help="Add vault reference columns to database tables"
    )
    columns_parser.set_defaults(func=add_columns)

    # Export command
    export_parser = subparsers.add_parser("export", help="Export secrets from vault")
    export_parser.add_argument("--output-dir", help="Directory to export secrets to")
    export_parser.add_argument(
        "--env-file", action="store_true", help="Create .env file from secrets"
    )
    export_parser.set_defaults(func=run_export)

    # Import secrets command
    import_secrets_parser = subparsers.add_parser(
        "import-secrets", help="Import secrets into vault"
    )
    import_secrets_parser.add_argument(
        "--input-file", required=True, help="JSON file containing secrets to import"
    )
    import_secrets_parser.add_argument(
        "--overwrite", action="store_true", help="Overwrite existing secrets"
    )
    import_secrets_parser.set_defaults(func=run_import_secrets)

    # Parse args and execute command
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    if hasattr(args, "func"):
        return args.func(args)
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
