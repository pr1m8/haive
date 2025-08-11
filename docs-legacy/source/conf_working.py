"""EXACT COPY of the working isolated config."""
import sys
sys.path.insert(0, '/home/will/Projects/haive/backend/haive/packages/haive-core/src')

project = 'Test'
extensions = ['autoapi.extension']
autoapi_dirs = ['/home/will/Projects/haive/backend/haive/packages/haive-core/src']
autoapi_type = 'python'
autoapi_root = 'api'
html_theme = 'alabaster'
autodoc_mock_imports = []
autoapi_ignore = []

print("🔥 WORKING CONFIG LOADED")