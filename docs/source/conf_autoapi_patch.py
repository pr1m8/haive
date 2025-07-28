"""
Patch for AutoAPI autosummary issues.
This module patches the autoapisummary directive to handle missing objects gracefully.
"""

import logging
from sphinx.ext.autosummary import Autosummary
from autoapi.directives import AutoapiSummary

logger = logging.getLogger(__name__)

# Store the original get_items method
_original_get_items = AutoapiSummary.get_items

def patched_get_items(self, names):
    """Patched version of get_items that handles missing objects gracefully."""
    try:
        return _original_get_items(self, names)
    except KeyError as e:
        logger.warning(f"AutoAPI: Could not find object {e}. Skipping autosummary.")
        # Return empty list to skip this autosummary
        return []
    except Exception as e:
        logger.warning(f"AutoAPI: Error in autosummary: {e}. Skipping.")
        return []

# Apply the patch
AutoapiSummary.get_items = patched_get_items
logger.info("Applied AutoAPI autosummary patch")