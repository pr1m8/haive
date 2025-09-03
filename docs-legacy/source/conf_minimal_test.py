"""MINIMAL conf.py to isolate the AutoAPI issue."""

import os
from pathlib import Path
import sys

# Basic project info
project = "Haive Test"
copyright = "2024, Test"
author = "Test"
version = "1.0"
release = "1.0.0"

# Add paths
project_root = Path(__file__).parent.parent.parent
packages_dir = project_root / "packages" 
sys.path.insert(0, str(packages_dir / "haive-core/src"))

# MINIMAL extensions - ONLY what's needed
extensions = [
    "autoapi.extension",
    "sphinx.ext.autodoc",
]

# AutoAPI - point to ONE package
autoapi_dirs = [str(packages_dir / "haive-core/src")]
autoapi_type = "python"
autoapi_root = "api"
autoapi_generate_api_docs = True
autoapi_add_toctree_entry = True

# NO MOCKS
autodoc_mock_imports = []

# NO IGNORES  
autoapi_ignore = []

# Basic HTML
html_theme = "alabaster"

print(f"✅ Minimal config loaded")
print(f"📂 AutoAPI dirs: {autoapi_dirs}")
print(f"📂 Checking path exists: {Path(autoapi_dirs[0]).exists()}")
print(f"🔍 Python files found: {len(list(Path(autoapi_dirs[0]).rglob('*.py')))}")