"""AutoAPI-only configuration to debug why it's not generating files."""

project = "AutoAPI Debug Test"
copyright = "2024, Haive Team"
author = "Haive Team"
version = "1.0"
release = "1.0.0"

# Only AutoAPI extension
extensions = [
    "autoapi.extension",
]

# Basic settings
templates_path = ["_templates"]
exclude_patterns = ["_build"]
html_theme = "alabaster"

# AutoAPI configuration
autoapi_type = "python"
autoapi_dirs = ["../../packages/haive-core/src"]
autoapi_root = "api"
autoapi_add_toctree_entry = True
autoapi_generate_api_docs = True
autoapi_keep_files = True
autoapi_python_class_content = "both"
autoapi_member_order = "bysource"

# Debug output
print("🔧 AutoAPI-only configuration loaded")
print(f"📦 AutoAPI dirs: {autoapi_dirs}")
print(f"🎯 Extensions: {extensions}")

# Mock imports (minimal set)
try:
    autodoc_mock_imports = [
        # Core dependencies that might not be available during doc build
        "langchain_core",
        "langchain_community", 
        "pydantic",
        "numpy",
        "pandas",
    ]
except Exception as e:
    print(f"⚠️ Warning setting mock imports: {e}")
    autodoc_mock_imports = []