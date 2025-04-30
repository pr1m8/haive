import json
import os
import sys

import pytest
from dotenv import dotenv_values

# Dynamically support local modules like haive.tak or langchain_textsplitters
sys.path.insert(0, os.getcwd())

from haive.haive.introspection.metadata import extract_metadata
from haive.haive.introspection.scanner import discover_classes

actual_env = dotenv_values(".env")
EXPORT_DIR = "introspection_outputs"
os.makedirs(EXPORT_DIR, exist_ok=True)

MODULES_TO_SCAN = [
    ("langchain_community.retrievers", "get_relevant_documents"),
    ("langchain_community.document_loaders", "load"),
    ("langchain_community.tools", "__call__"),
    ("haive.tak.tools", "__call__"),
    ("haive.tak.toolkits", "__call__"),
    # ("langchain_text_splitters", None),
]


@pytest.mark.parametrize("module_path, method_required", MODULES_TO_SCAN)
def test_discovery_and_metadata(module_path, method_required):
    print(f"\n🔍 Scanning: {module_path} ({method_required or 'all classes'})")
    classes = discover_classes(module_path, method_required=method_required)
    assert classes, f"No classes found in {module_path}"

    results = []
    for cls, mod in classes:
        tool_type = method_required or "class"
        meta = extract_metadata(cls, mod, actual_env, tool_type=tool_type)
        results.append(meta)
        assert "class_name" in meta
        assert isinstance(meta["arg_schema"], dict)
        assert isinstance(meta["docstring"], str)
        print(f"✅ {meta['class_name']} from {mod}")
        if meta.get("env_required"):
            print(
                f"🔐 Requires: {meta['env_required']}, missing: {meta['env_missing']}"
            )

    # Export results to JSON
    module_tag = module_path.replace(".", "_")
    output_path = os.path.join(EXPORT_DIR, f"{module_tag}_metadata.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n📦 Metadata exported to: {output_path}")
