# src/haive/__init__.py
"""Haive - Agent Framework and Ecosystem."""

__version__ = "0.1.0"

# Import from submodules
try:
    from haive_core import *
except ImportError:
    pass

try:
    from haive_agents_dep import *
except ImportError:
    pass

try:
    from haive_games import *
except ImportError:
    pass

try:
    from haive_dataflow_dep import *
except ImportError:
    pass

try:
    from haive_prebuilt import *
except ImportError:
    pass

try:
    from haive_tools import *
except ImportError:
    pass
