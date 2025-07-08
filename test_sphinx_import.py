#!/usr/bin/env python3
"""Test what Sphinx autodoc does when importing haive.core.models.llm"""

import sys
import os

# Add the paths Sphinx would add
sys.path.insert(0, os.path.abspath('packages/haive-core/src'))
sys.path.insert(0, os.path.abspath('docs/source'))

# Import conf to set up mocking
print("=== Loading Sphinx conf.py ===")
try:
    os.chdir('docs')
    sys.path.insert(0, 'source')
    import conf
    print("✓ Conf loaded")
except Exception as e:
    print(f"✗ Failed to load conf: {e}")
    import traceback
    traceback.print_exc()

# Now try the import that's failing in Sphinx
print("\n=== Testing import with Sphinx environment ===")
try:
    import haive.core.models.llm
    print("✓ Import succeeded")
    print(f"LLMConfig: {haive.core.models.llm.LLMConfig}")
except Exception as e:
    print(f"✗ Import failed: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

# Test what autodoc would do
print("\n=== Testing autodoc-style import ===")
try:
    from sphinx.ext.autodoc.mock import mock
    from sphinx.util import inspect
    
    # This is what autodoc does
    obj = haive.core.models.llm.LLMConfig
    print(f"✓ Got object: {obj}")
    
except Exception as e:
    print(f"✗ Autodoc-style failed: {e}")
    import traceback
    traceback.print_exc()