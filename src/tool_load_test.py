#!/usr/bin/env python
"""Hybrid Tools and Toolkits Importer.

This script first identifies tools using your working approach, then imports them to the database.
"""
import importlib
import inspect
import json
import logging
import os
import re
import sys
import uuid
from datetime import datetime
from typing import Dict, List, Optional

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Check for langchain dependencies
try:
    from langchain_core.documents import Document
    from langchain_core.tools import BaseTool
except ImportError:
    logger.exception(
        "langchain_core not found. Please install it with: pip install langchain-core"
    )
    sys.exit(1)

# Import Supabase client
try:
    from src.haive.dataflow.db.supabase import get_supabase_client, table

    supabase = get_supabase_client()
    logger.info("Successfully imported Supabase client and helpers")
except ImportError as e:
    logger.exception(f"Error importing Supabase client: {e}")
    sys.exit(1)

# --- CONFIG (using your actual paths) ---
BASE_PATH = "/home/will/Projects/haive/backend/haive/src"
TOOLS_PATH = os.path.join(BASE_PATH, "haive", "tak", "tools")
TOOLKITS_PATH = os.path.join(BASE_PATH, "haive", "tak", "toolkits")

# Add BASE_PATH to PYTHONPATH
sys.path.insert(0, os.path.dirname(BASE_PATH))

# --- State ---
failed_modules = []  # Track failed imports
all_tools = []  # All successfully loaded tools
tool_cache = {}
toolkit_cache = {}
category_cache = {}


def detect_environment_variables(source_code: str) -> list[str]:
    """Detect potential environment variables in source code.

    Args:
        source_code: String containing source code

    Returns:
        List of potential environment variable names
    """
    if not source_code:
        return []

    # Common patterns for environment variables
    patterns = [
        r'os\.environ\.get\(["\']([A-Za-z0-9_]+)["\']',  # os.environ.get('VAR_NAME')
        r'os\.getenv\(["\']([A-Za-z0-9_]+)["\']',  # os.getenv('VAR_NAME')
        r'os\.environ\[["\']([A-Za-z0-9_]+)["\']',  # os.environ['VAR_NAME']
        r'getenv\(["\']([A-Za-z0-9_]+)["\']',  # getenv('VAR_NAME')
        r'ENV\[["\']([A-Za-z0-9_]+)["\']',  # ENV['VAR_NAME']
        r'env\.["\']([A-Za-z0-9_]+)["\']',  # env.'VAR_NAME'
        r'config\[["\']([A-Za-z0-9_]+)["\']',  # config['VAR_NAME']
        r'dotenv\.get\(["\']([A-Za-z0-9_]+)["\']',  # dotenv.get('VAR_NAME')
        r"\.env\.([A-Z][A-Z0-9_]+)",  # .env.API_KEY
        r'["\']([A-Z][A-Z0-9_]+_(?:KEY|TOKEN|SECRET|PASSWORD|ID|URL|URI|ENDPOINT|CREDENTIALS))["\']',  # 'API_KEY'
    ]

    env_vars = set()
    for pattern in patterns:
        matches = re.findall(pattern, source_code)
        env_vars.update(matches)

    return list(env_vars)


def get_source_code(obj) -> str:
    """Extract source code from an object if possible."""
    try:
        return inspect.getsource(obj)
    except (TypeError, OSError):
        if hasattr(obj, "__wrapped__"):
            try:
                return inspect.getsource(obj.__wrapped__)
            except (TypeError, OSError):
                pass
        return ""


def get_module_source_code(module) -> str:
    """Get the source code of an entire module if possible."""
    try:
        return inspect.getsource(module)
    except (TypeError, OSError):
        # Try to get path and read file
        try:
            if hasattr(module, "__file__"):
                with open(module.__file__) as f:
                    return f.read()
        except Exception:
            pass
        return ""


def extract_schema_json(tool: BaseTool) -> dict:
    """Extract args schema from tool as JSON if possible."""
    if not hasattr(tool, "args_schema"):
        return None

    try:
        # Try new Pydantic V2 method first
        if hasattr(tool.args_schema, "model_json_schema"):
            return tool.args_schema.model_json_schema()
        # Fall back to older Pydantic V1 method
        if hasattr(tool.args_schema, "schema"):
            return tool.args_schema.schema()
        # Another possible method
        elif hasattr(tool.args_schema, "schema_json"):
            json_str = tool.args_schema.schema_json()
            if isinstance(json_str, str):
                return json.loads(json_str)
            return json_str
    except Exception as e:
        logger.warning(f"Error extracting schema from {tool.name}: {e}")

    return None


def load_tools_from_module(module_path: str, tool_type: str) -> List[BaseTool]:
    """Load tools from a module using your working approach."""
    tools = []
    try:
        # Try to import the module
        logger.info(f"Loading module: {module_path}")
        module = importlib.import_module(module_path)

        # Get module source code for environment variable detection
        module_source = get_module_source_code(module)
        module_env_vars = detect_environment_variables(module_source)

        if module_env_vars:
            logger.info(
                f"Module {module_path} may require environment variables: {', '.join(module_env_vars)}"
            )

        # Look for tools in the module
        for name, obj in inspect.getmembers(module):
            # Check for lists of tools (common pattern)
            if isinstance(obj, list) and all(
                isinstance(item, BaseTool) for item in obj
            ):
                logger.info(
                    f"Found tool list '{name}' in {module_path} with {len(obj)} tools"
                )
                for tool in obj:
                    # Set up metadata
                    if not hasattr(tool, "metadata") or tool.metadata is None:
                        tool.metadata = {}

                    # Add important metadata
                    tool.metadata["tool_type"] = tool_type
                    tool.metadata["module_path"] = module_path
                    tool.metadata["module_env_vars"] = module_env_vars

                    # Extract specific tool source code for additional env vars
                    tool_source = get_source_code(tool)
                    tool_env_vars = detect_environment_variables(tool_source)
                    if tool_env_vars:
                        tool.metadata["tool_env_vars"] = tool_env_vars

                    # Extract schema
                    try:
                        schema_json = extract_schema_json(tool)
                        if schema_json:
                            tool.metadata["args_schema_json"] = schema_json
                    except Exception as e:
                        logger.warning(
                            f"Error extracting schema for tool {tool.name}: {e}"
                        )

                    tools.append(tool)

            # Check for individual tool objects
            elif isinstance(obj, BaseTool):
                logger.info(f"Found individual tool '{name}' in {module_path}")
                if not hasattr(obj, "metadata") or obj.metadata is None:
                    obj.metadata = {}

                # Add important metadata
                obj.metadata["tool_type"] = tool_type
                obj.metadata["module_path"] = module_path
                obj.metadata["module_env_vars"] = module_env_vars

                # Extract specific tool source code for additional env vars
                tool_source = get_source_code(obj)
                tool_env_vars = detect_environment_variables(tool_source)
                if tool_env_vars:
                    obj.metadata["tool_env_vars"] = tool_env_vars

                # Extract schema
                try:
                    schema_json = extract_schema_json(obj)
                    if schema_json:
                        obj.metadata["args_schema_json"] = schema_json
                except Exception as e:
                    logger.warning(f"Error extracting schema for tool {obj.name}: {e}")

                tools.append(obj)

    except Exception as e:
        logger.warning(f"Error loading module {module_path}: {e}")
        failed_modules.append((module_path, str(e)))
        return []

    return tools


def load_tools_from_directory(
    directory: str, module_prefix: str, tool_type: str
) -> List[BaseTool]:
    """Load tools from a directory using your working approach."""
    tools = []
    logger.info(f"Scanning directory: {directory}")
    logger.info(f"Using module prefix: {module_prefix}")

    if not os.path.exists(directory):
        logger.warning(f"Directory not found: {directory}")
        return []

    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".py") and filename != "__init__.py":
                # This path conversion logic matches your working script
                relative_path = os.path.relpath(root, BASE_PATH)
                module_base = relative_path.replace(os.sep, ".")
                module_name = filename[:-3]
                module_path = (
                    f"{module_prefix}.{module_name}"
                    if module_base == module_prefix
                    else f"{module_base}.{module_name}"
                )

                # Append to tools list
                new_tools = load_tools_from_module(module_path, tool_type)
                if new_tools:
                    logger.info(f"Found {len(new_tools)} tools in {module_path}")
                    tools.extend(new_tools)

    return tools


def get_or_create_category(name: str, display_name: str | None = None) -> str:
    """Get or create a tool category."""
    # Check cache first
    if name in category_cache:
        return category_cache[name]

    # Default display name if not provided
    if not display_name:
        display_name = name.replace("_", " ").title()

    try:
        # Check if category exists
        response = (
            table(supabase, "tools.categories").select("id").eq("name", name).execute()
        )

        if response.data and len(response.data) > 0:
            category_id = response.data[0]["id"]
            category_cache[name] = category_id
            return category_id

        # Create new category
        category_data = {
            "name": name,
            "display_name": display_name,
            "created_at": datetime.now().isoformat(),
        }

        response = table(supabase, "tools.categories").insert(category_data).execute()

        if response.data and len(response.data) > 0:
            category_id = response.data[0]["id"]
            category_cache[name] = category_id
            return category_id

        raise Exception(f"Failed to create category: {name}")

    except Exception as e:
        logger.exception(f"Error getting or creating category {name}: {e}")
        # Return a default category ID to continue processing
        return str(uuid.uuid4())


def get_or_create_toolkit(
    name: str, display_name: str | None = None, description: str | None = None
) -> str:
    """Get or create a toolkit."""
    # Check cache first
    if name in toolkit_cache:
        return toolkit_cache[name]

    # Default display name if not provided
    if not display_name:
        display_name = name.replace("_", " ").title()

    try:
        # Check if toolkit exists
        response = (
            table(supabase, "tools.toolkits").select("id").eq("name", name).execute()
        )

        if response.data and len(response.data) > 0:
            toolkit_id = response.data[0]["id"]

            # Update existing toolkit
            update_data = {
                "display_name": display_name,
                "updated_at": datetime.now().isoformat(),
            }

            if description:
                update_data["description"] = description

            table(supabase, "tools.toolkits").update(update_data).eq(
                "id", toolkit_id
            ).execute()

            toolkit_cache[name] = toolkit_id
            return toolkit_id

        # Create new toolkit
        toolkit_data = {
            "name": name,
            "display_name": display_name,
            "is_public": True,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

        if description:
            toolkit_data["description"] = description

        response = table(supabase, "tools.toolkits").insert(toolkit_data).execute()

        if response.data and len(response.data) > 0:
            toolkit_id = response.data[0]["id"]
            toolkit_cache[name] = toolkit_id
            return toolkit_id

        raise Exception(f"Failed to create toolkit: {name}")

    except Exception as e:
        logger.exception(f"Error getting or creating toolkit {name}: {e}")
        # Return a UUID to continue processing
        return str(uuid.uuid4())


def get_or_create_tool(
    name: str,
    category_id: str,
    display_name: str | None = None,
    description: str | None = None,
    input_schema: Dict | None = None,
    source_code: str | None = None,
) -> str:
    """Get or create a tool."""
    # Check cache first
    if name in tool_cache:
        return tool_cache[name]

    # Default display name if not provided
    if not display_name:
        display_name = name.replace("_", " ").title()

    try:
        # Check if tool exists
        response = (
            table(supabase, "tools.tools").select("id").eq("name", name).execute()
        )

        if response.data and len(response.data) > 0:
            tool_id = response.data[0]["id"]

            # Update existing tool
            update_data = {
                "display_name": display_name,
                "category_id": category_id,
                "updated_at": datetime.now().isoformat(),
            }

            if description:
                update_data["description"] = description

            if input_schema:
                update_data["input_schema"] = json.dumps(input_schema)

            if source_code:
                update_data["source_code"] = source_code

            table(supabase, "tools.tools").update(update_data).eq(
                "id", tool_id
            ).execute()

            tool_cache[name] = tool_id
            return tool_id

        # Create new tool
        tool_data = {
            "name": name,
            "display_name": display_name,
            "category_id": category_id,
            "is_public": True,
            "is_experimental": False,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

        if description:
            tool_data["description"] = description

        if input_schema:
            tool_data["input_schema"] = json.dumps(input_schema)

        if source_code:
            tool_data["source_code"] = source_code

        response = table(supabase, "tools.tools").insert(tool_data).execute()

        if response.data and len(response.data) > 0:
            tool_id = response.data[0]["id"]
            tool_cache[name] = tool_id
            return tool_id

        raise Exception(f"Failed to create tool: {name}")

    except Exception as e:
        logger.exception(f"Error getting or creating tool {name}: {e}")
        # Return a UUID to continue processing
        return str(uuid.uuid4())


def register_environment_variables(tool_id: str, env_vars: List[str]) -> None:
    """Register environment variables for a tool."""
    if not env_vars:
        return

    try:
        # Get environment variable IDs or create them
        env_var_ids = []
        for env_name in env_vars:
            # Check if environment variable exists
            response = (
                table(supabase, "config.environment_variables")
                .select("id")
                .eq("name", env_name)
                .execute()
            )

            if response.data and len(response.data) > 0:
                env_var_ids.append(response.data[0]["id"])
            else:
                # Create new environment variable
                env_data = {
                    "name": env_name,
                    "description": f"Auto-detected for {env_name}",
                    "required": True,
                    "created_at": datetime.now().isoformat(),
                }

                response = (
                    table(supabase, "config.environment_variables")
                    .insert(env_data)
                    .execute()
                )

                if response.data and len(response.data) > 0:
                    env_var_ids.append(response.data[0]["id"])

        # Get tool as component
        response = (
            table(supabase, "config.components")
            .select("id")
            .eq("component_id", tool_id)
            .eq("component_type", "TOOL")
            .execute()
        )

        component_id = None
        if response.data and len(response.data) > 0:
            component_id = response.data[0]["id"]
        else:
            # Create component reference
            component_data = {
                "component_id": tool_id,
                "component_type": "TOOL",
                "created_at": datetime.now().isoformat(),
            }

            response = (
                table(supabase, "config.components").insert(component_data).execute()
            )

            if response.data and len(response.data) > 0:
                component_id = response.data[0]["id"]

        # Link environment variables to component
        if component_id:
            for env_var_id in env_var_ids:
                # Check if mapping already exists
                response = (
                    table(supabase, "config.component_env_mappings")
                    .select("id")
                    .eq("component_id", component_id)
                    .eq("env_var_id", env_var_id)
                    .execute()
                )

                if response.data and len(response.data) > 0:
                    continue

                # Create new mapping
                mapping_data = {
                    "component_id": component_id,
                    "env_var_id": env_var_id,
                    "created_at": datetime.now().isoformat(),
                }

                table(supabase, "config.component_env_mappings").insert(
                    mapping_data
                ).execute()

    except Exception as e:
        logger.exception(f"Error registering environment variables for tool {tool_id}: {e}")


def link_tool_to_toolkit(tool_id: str, toolkit_id: str) -> bool:
    """Link a tool to a toolkit."""
    try:
        # Check if link already exists
        response = (
            table(supabase, "tools.toolkit_tools")
            .select("id")
            .eq("toolkit_id", toolkit_id)
            .eq("tool_id", tool_id)
            .execute()
        )

        if response.data and len(response.data) > 0:
            # Link already exists
            return True

        # Create new link
        link_data = {
            "toolkit_id": toolkit_id,
            "tool_id": tool_id,
            "created_at": datetime.now().isoformat(),
        }

        response = table(supabase, "tools.toolkit_tools").insert(link_data).execute()

        return response.data is not None and len(response.data) > 0

    except Exception as e:
        logger.exception(f"Error linking tool {tool_id} to toolkit {toolkit_id}: {e}")
        return False


def determine_category_from_module_path(module_path: str) -> str:
    """Determine a category name from a module path."""
    if not module_path:
        return "general"

    # Split the path into parts
    parts = module_path.split(".")

    # For tools directly in the tools directory
    if len(parts) >= 2 and parts[-2] == "tools":
        return "general"

    # For tools in subdirectories of tools
    if len(parts) >= 3 and parts[-3] == "tools":
        return parts[-2]  # Use the parent directory name

    # For toolkits
    if len(parts) >= 2 and parts[-2] == "toolkits":
        return parts[-1].replace("_toolkit", "")

    # Default to the second-to-last part of the path
    if len(parts) >= 2:
        return parts[-2]

    return "general"


def import_tools_to_database():
    """Import the discovered tools into the database."""
    imported_tools = 0
    imported_toolkits = set()
    toolkit_tools = {}  # Maps toolkit names to list of tool IDs

    # Process each tool
    for tool in all_tools:
        try:
            # Get tool info
            tool_name = tool.name
            tool_description = tool.description
            tool_module = tool.metadata.get("module_path", "")
            tool_type = tool.metadata.get("tool_type", "general")

            # Get environment variables
            module_env_vars = tool.metadata.get("module_env_vars", [])
            tool_env_vars = tool.metadata.get("tool_env_vars", [])
            all_env_vars = list(set(module_env_vars + tool_env_vars))

            # Get source code
            source_code = get_source_code(tool)

            # Get args schema
            input_schema = tool.metadata.get("args_schema_json")

            # Determine category
            category_name = determine_category_from_module_path(tool_module)
            category_id = get_or_create_category(category_name)

            # Create tool record
            tool_id = get_or_create_tool(
                name=tool_name,
                category_id=category_id,
                description=tool_description,
                input_schema=input_schema,
                source_code=source_code,
            )

            if tool_id:
                imported_tools += 1

                # Register environment variables
                if all_env_vars:
                    register_environment_variables(tool_id, all_env_vars)

            # Determine toolkit name
            toolkit_name = None
            if "toolkit" in tool_type or (tool_module and "toolkits" in tool_module):
                # Try to extract toolkit name from module path
                if "toolkits" in tool_module:
                    parts = tool_module.split(".")
                    toolkit_index = -1
                    for i, part in enumerate(parts):
                        if part == "toolkits":
                            toolkit_index = i
                            break

                    if toolkit_index >= 0 and toolkit_index + 1 < len(parts):
                        toolkit_name = parts[toolkit_index + 1]
                        if toolkit_name.endswith("_toolkit"):
                            toolkit_name = toolkit_name[:-8]  # Remove _toolkit suffix

            # Link to toolkit if applicable
            if toolkit_name:
                if toolkit_name not in toolkit_tools:
                    toolkit_tools[toolkit_name] = []

                toolkit_tools[toolkit_name].append(tool_id)
                imported_toolkits.add(toolkit_name)

        except Exception as e:
            logger.exception(
                f"Error importing tool {getattr(tool, 'name', 'unknown')}: {e}"
            )

    # Create toolkits and link tools
    for toolkit_name, tool_ids in toolkit_tools.items():
        try:
            # Create toolkit
            toolkit_id = get_or_create_toolkit(
                name=toolkit_name, display_name=toolkit_name.replace("_", " ").title()
            )

            # Link tools to toolkit
            for tool_id in tool_ids:
                link_tool_to_toolkit(tool_id, toolkit_id)

        except Exception as e:
            logger.exception(f"Error creating toolkit {toolkit_name}: {e}")

    logger.info(
        f"Imported {imported_tools} tools into {len(imported_toolkits)} toolkits"
    )


def print_tool_stats():
    """Print statistics about discovered tools."""
    # Categorize tools by module
    tools_by_module = {}
    for tool in all_tools:
        module = tool.metadata.get("module_path", "unknown")
        if module not in tools_by_module:
            tools_by_module[module] = []
        tools_by_module[module].append(tool)

    # Print summary

    # Print top 10 modules with most tools
    sorted_modules = sorted(
        tools_by_module.items(), key=lambda x: len(x[1]), reverse=True
    )
    for module, tools in sorted_modules[:10]:
        pass")

    # Count tools with env vars
    tools_with_env_vars = sum(
        1
        for tool in all_tools
        if tool.metadata.get("module_env_vars") or tool.metadata.get("tool_env_vars")
    )
    print(f"\n🔑 {tools_with_env_vars} tools require environment variables")

    # Count tools with schemas
    tools_with_schemas = sum(
        1 for tool in all_tools if tool.metadata.get("args_schema_json")
    )

    # Print failures if any
    if failed_modules:
        print(f"\n⚠️ {len(failed_modules)} modules failed to load:")
        for module, error in failed_modules[:5]:
            print(f"  ❌ {module}: {error}")
        if len(failed_modules) > 5:
            pass
    print("\n")


def main():
    """Main function to run the tool importer."""
    global all_tools

    logger.info("Starting tool import process")

    # First collect all tools using your working approach
    logger.info("Phase 1: Discovering tools...")

    # Load tools from individual tools directory
    tools_from_tools = load_tools_from_directory(TOOLS_PATH, "haive.tak.tools", "tool")
    logger.info(f"Found {len(tools_from_tools)} tools in tools directory")
    all_tools.extend(tools_from_tools)

    # Load tools from toolkits directory
    tools_from_toolkits = load_tools_from_directory(
        TOOLKITS_PATH, "haive.tak.toolkits", "toolkit"
    )
    logger.info(f"Found {len(tools_from_toolkits)} tools in toolkits directory")
    all_tools.extend(tools_from_toolkits)

    # Print summary of discovered tools
    print_tool_stats()

    # Stop here if no tools found
    if not all_tools:
        logger.error("No tools discovered, exiting")
        return

    # Next import to database
    logger.info("Phase 2: Importing to database...")

    # Test database connection
    try:
        table(supabase, "tools.categories").select("id").limit(1).execute()
        logger.info("Database connection successful")
    except Exception as e:
        logger.exception(f"Database connection error: {e}")
        logger.exception("Skipping database import phase")
        return

    # Import to database
    import_tools_to_database()

    logger.info("Tool import process completed")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        passr")
    except Exception as e:
        import traceback

        traceback.print_exc()
