#!/usr/bin/env python
"""Hybrid Tools and Toolkits Importer.

This script first identifies tools using your working approach, then imports them to the database.
"""
import importlib
import inspect
import logging
import os
import sys
import uuid
from datetime import datetime
from typing import List, Optional

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


def load_tools_from_module(module_path: str, tool_type: str) -> list[BaseTool]:
    """Load tools from a module using your working approach."""
    tools = []
    try:
        # Try to import the module
        logger.info(f"Loading module: {module_path}")
        module = importlib.import_module(module_path)

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
                    if not hasattr(tool, "metadata") or tool.metadata is None:
                        tool.metadata = {}
                    tool.metadata["tool_type"] = tool_type
                    tool.metadata["module_path"] = module_path
                tools.extend(obj)

            # Check for individual tool objects
            elif isinstance(obj, BaseTool):
                logger.info(f"Found individual tool '{name}' in {module_path}")
                if not hasattr(obj, "metadata") or obj.metadata is None:
                    obj.metadata = {}
                obj.metadata["tool_type"] = tool_type
                obj.metadata["module_path"] = module_path
                tools.append(obj)

    except Exception as e:
        logger.warning(f"Error loading module {module_path}: {e}")
        failed_modules.append((module_path, str(e)))
        return []

    return tools


def load_tools_from_directory(
    directory: str, module_prefix: str, tool_type: str
) -> list[BaseTool]:
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

            # Determine category
            category_name = determine_category_from_module_path(tool_module)
            category_id = get_or_create_category(category_name)

            # Create tool record
            tool_id = get_or_create_tool(
                name=tool_name, category_id=category_id, description=tool_description
            )

            if tool_id:
                imported_tools += 1

            # Determine toolkit name
            toolkit_name = None
            if "toolkit" in tool_type or (tool_module and "toolkits" in tool_module):
                # Try to extract toolkit name from module path
                if "toolkits" in tool_module:
                    parts = tool_module.split(".")
                    toolkit_index = (
                        parts.index("toolkits") if "toolkits" in parts else -1
                    )
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

    # Print failures if any
    if failed_modules:
        for module, error in failed_modules[:5]:
            pass")
        if len(failed_modules) > 5:
            pass


def main():
    """Main function to run the tool importer."""
    global all_tools

    logger.info("Starting tool import process")

    # First collect all tools using your working approach
    logger.info("Phase 1: Discovering tools...")

    # Load tools from individual tools directory
    tools_from_tools = load_tools_from_directory(TOOLS_PATH, "haive.tools", "tool")
    logger.info(f"Found {len(tools_from_tools)} tools in tools directory")
    all_tools.extend(tools_from_tools)

    # Load tools from toolkits directory
    tools_from_toolkits = load_tools_from_directory(
        TOOLKITS_PATH, "haive.toolkits", "toolkit"
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
