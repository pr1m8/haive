#!/usr/bin/env python3
"""Test what Sphinx autodoc does when importing haive.core.models.llm."""

import os
import sys

# Add the paths Sphinx would add
sys.path.insert(0, os.path.abspath("packages/haive-core/src"))
sys.path.insert(0, os.path.abspath("docs/source"))

# Import conf to set up mocking
try:
    os.chdir("docs")
    sys.path.insert(0, "source")

except Exception:
    import traceback

    traceback.print_exc()

# Now try the import that's failing in Sphinx
try:
    import haive.core.models.llm

except Exception:
    import traceback

    traceback.print_exc()

# Test what autodoc would do
try:

    # This is what autodoc does
    obj = haive.core.models.llm.LLMConfig

except Exception:
    import traceback

    traceback.print_exc()
