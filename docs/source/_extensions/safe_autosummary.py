"""Safe autosummary extension that handles import errors gracefully."""

import logging

from sphinx.ext.autosummary import Autosummary as BaseAutosummary
from sphinx.ext.autosummary import ImportExceptionGroup
from sphinx.ext.autosummary.generate import generate_autosummary_docs

logger = logging.getLogger(__name__)


class SafeAutosummary(BaseAutosummary):
    """Autosummary that continues on import errors."""

    def run(self):
        """Run the directive, catching import errors."""
        try:
            return super().run()
        except ImportExceptionGroup as e:
            # Log the errors but continue
            logger.warning(f"Import errors in autosummary: {e}")
            # Return empty content
            return []
        except Exception as e:
            logger.warning(f"Error in autosummary: {e}")
            return []


def safe_import_by_name(name, prefixes=None):
    """Import by name but return None on failure instead of raising."""
    from sphinx.ext.autosummary import import_by_name

    try:
        return import_by_name(name, prefixes)
    except Exception as e:
        logger.debug(f"Failed to import {name}: {e}")
        return None, None, None


def setup(app):
    """Setup the safe autosummary extension."""
    # Replace the standard autosummary directive
    app.add_directive("autosummary", SafeAutosummary, override=True)

    # Patch the import function
    import sphinx.ext.autosummary

    sphinx.ext.autosummary.import_by_name = safe_import_by_name

    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
