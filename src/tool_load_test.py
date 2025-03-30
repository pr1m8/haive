import os
import sys
import importlib
import inspect
import uuid
import argparse
from typing import List, Tuple
from langchain_core.tools import BaseTool
from langchain_core.documents import Document

# --- CONFIG ---
BASE_PATH = "/home/will/Projects/haive/backend/haive/src"
TOOLS_PATH = os.path.join(BASE_PATH, "haive", "tools")
TOOLKITS_PATH = os.path.join(BASE_PATH, "haive", "toolkits")

# Add BASE_PATH to PYTHONPATH
sys.path.insert(0, BASE_PATH)

# --- State ---
failed_modules = []  # Track failed imports


def load_tools_from_module(module_path: str, tool_type: str) -> List[BaseTool]:
    tools = []
    try:
        module = importlib.import_module(module_path)

        for name, obj in inspect.getmembers(module):
            if isinstance(obj, list) and all(isinstance(item, BaseTool) for item in obj):
                for tool in obj:
                    if not hasattr(tool, "metadata") or tool.metadata is None:
                        tool.metadata = {}
                    tool.metadata["tool_type"] = tool_type
                tools.extend(obj)

    except Exception as e:
        failed_modules.append((module_path, str(e)))
        return []

    return tools


def load_tools_from_directory(directory: str, module_prefix: str, tool_type: str) -> List[BaseTool]:
    tools = []
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".py") and filename != "__init__.py":
                relative_path = os.path.relpath(root, BASE_PATH)
                module_base = relative_path.replace(os.sep, ".")
                module_name = filename[:-3]
                module_path = (
                    f"{module_prefix}.{module_name}"
                    if module_base == module_prefix
                    else f"{module_base}.{module_name}"
                )
                tools.extend(load_tools_from_module(module_path, tool_type))
    return tools


def create_tool_documents(tools: List[BaseTool]) -> List[Document]:
    return [
        Document(
            page_content=tool.description,
            id=str(uuid.uuid4()),
            metadata={
                "tool_name": tool.name,
                "tool_type": tool.metadata.get("tool_type", "unknown")
            }
        )
        for tool in tools
    ]


def print_documents(documents: List[Document]):
    print("📄 Documents:")
    for doc in documents:
        print(f"- ID: {doc.id}")
        print(f"  Name: {doc.metadata['tool_name']}")
        print(f"  Type: {doc.metadata['tool_type']}")
        print(f"  Preview: {doc.page_content[:80]}...\n")


def print_failures():
    if failed_modules:
        print(f"\n⚠️ {len(failed_modules)} modules failed to load:")
        for path, error in failed_modules:
            print(f"  ❌ {path}: {error}")
    else:
        print("\n✅ No import errors!")


def main():
    parser = argparse.ArgumentParser(description="Tool Loader")
    parser.add_argument("--clean", action="store_true", help="Print only successfully loaded tools")
    args = parser.parse_args()

    print("🔍 Scanning for tools...\n")

    all_tools = []
    all_tools += load_tools_from_directory(TOOLS_PATH, "haive.tools", "tool")
    all_tools += load_tools_from_directory(TOOLKITS_PATH, "haive.toolkits", "toolkit")

    print(f"\n✅ Loaded {len(all_tools)} tools total.")
    print_failures()

    documents = create_tool_documents(all_tools)

    if args.clean:
        print("\n✨ Showing only clean tools:\n")
        print_documents(documents)
    else:
        print("\n📦 Full toolset including failed modules:\n")
        print_documents(documents)


if __name__ == "__main__":
    main()
