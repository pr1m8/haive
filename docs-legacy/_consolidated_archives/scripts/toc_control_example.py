"""TOC Control Examples for Haive Documentation."""

# 1. Hide from documentation completely
from __future__ import annotations


class _PrivateClass:  # Leading underscore = hidden
    pass


# 2. Include but control visibility
class PublicClass:
    """This appears in TOC."""

    def public_method(self):
        """This appears under the class."""

    def _private_method(self):
        """This is hidden from TOC."""


# 3. Control with autoapi_options in conf.py
# "undoc-members" - Include undocumented members
# "private-members" - Include _private members
# "special-members" - Include __special__ methods

# 4. Skip specific items with AutoAPI
# In conf.py:

# 5. Module-level control
__all__ = ["PublicClass"]  # Only exports listed items
