"""Patch for viewcode to handle files with too few lines."""

import logging
from sphinx.ext import viewcode

logger = logging.getLogger(__name__)

# Store the original collect_pages function
_original_collect_pages = viewcode.collect_pages


def patched_collect_pages(app):
    """Patched version of viewcode.collect_pages that handles IndexError."""
    try:
        # Get the original generator
        for result in _original_collect_pages(app):
            yield result
    except IndexError as e:
        logger.warning(f"viewcode IndexError caught and handled: {e}")
        # Continue without the problematic file
        pass
    except Exception as e:
        logger.error(f"viewcode unexpected error: {e}")
        # Re-raise other errors
        raise


# Apply the patch
def patch_viewcode():
    """Apply the viewcode patch."""
    viewcode.collect_pages = patched_collect_pages
    logger.info("✅ Applied viewcode IndexError patch")