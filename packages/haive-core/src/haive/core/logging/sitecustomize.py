"""
Site-wide Python customization for automatic logging with source tracking.

To use this file:
1. Copy it to your Python site-packages directory as 'sitecustomize.py'
2. Or add its directory to PYTHONPATH
3. Or use it with PYTHONSTARTUP environment variable

This will automatically enable source tracking for ALL Python scripts!
"""

import os
import sys

# Only activate if explicitly enabled
if os.getenv("HAIVE_AUTO_LOGGING") or os.getenv("HAIVE_TRACK_ALL"):
    try:
        # Enable source tracking for all logging
        from haive.core.logging.auto_config import enable_source_tracking
        from haive.core.logging.quick_setup import setup_development_logging

        # Use development setup by default (shows sources, hides noise)
        setup_development_logging()

        # Add startup message
        print("🚀 Haive logging auto-enabled with source tracking!"g!")
        print(f"   Running: {sys.argv[0]}")
        print("   All logs and prints will show their source location\n")

    except ImportError:
        # Haive not installed, skip
        pass
