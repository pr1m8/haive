import sys
from pathlib import Path

# Set up paths
project_root = Path(__file__).parent.parent
packages_dir = project_root / "packages"

# Add to Python path
sys.path.insert(0, str(packages_dir / "haive-core/src"))

# MINIMAL configuration - just AutoAPI
extensions = ["autoapi.extension"]
autoapi_type = "python"
autoapi_dirs = [str(packages_dir / "haive-core/src")]
autoapi_root = "api"
autoapi_add_toctree_entry = True
autoapi_generate_api_docs = True

# Basic required settings
project = "Minimal Haive Test"
html_theme = "furo"
