#!/usr/bin/env python3
"""Wrapper script to debug AutoAPI file processing."""

from __future__ import annotations

import logging
from pathlib import Path
import sys

# Add packages to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("/tmp/autoapi_debug.log"),
        logging.StreamHandler()
    ],
)

logger = logging.getLogger(__name__)

# Monkey-patch autoapi to log file processing
try:
    from autoapi._parser import Parser

    original_parse_file = Parser.parse_file

    def logged_parse_file(self, file_path, condition=None):
        """Wrapper that logs which file is being parsed."""
        logger.info(f"AutoAPI parsing: {file_path}")
        try:
            result = original_parse_file(self, file_path, condition)
            logger.info(f"Successfully parsed: {file_path}")
            return result
        except Exception as e:
            logger.error(
                f"ERROR parsing {file_path}: {type(e).__name__}: {e!s}")
            raise

    # Replace the method
    Parser.parse_file = logged_parse_file
    logger.info("Successfully patched AutoAPI Parser")

except ImportError as e:
    logger.error(f"Failed to import autoapi: {e}")

# Now run sphinx-build with the patched parser
if __name__ == "__main__":
    logger.info("Starting sphinx-build with AutoAPI debugging")

    # Run sphinx-build
    from sphinx.cmd.build import main as sphinx_main

    # Pass through all arguments
    sys.exit(sphinx_main(sys.argv[1:]))
