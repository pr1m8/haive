#!/usr/bin/env python3
"""
Watch source files and automatically rebuild documentation when changes are detected.
Keeps API documentation in sync with code changes.
"""

import logging
import subprocess
import sys
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class DocsBuildHandler(FileSystemEventHandler):
    """Handle file system events and trigger doc rebuilds."""

    def __init__(self, build_command, debounce_seconds=2):
        self.build_command = build_command
        self.debounce_seconds = debounce_seconds
        self.last_modified = 0
        self.pending_build = False

    def on_modified(self, event):
        if event.is_directory:
            return

        # Only watch Python and RST/MD files
        if not any(event.src_path.endswith(ext) for ext in [".py", ".rst", ".md"]):
            return

        # Ignore build directory changes
        if "docs/build" in event.src_path or "__pycache__" in event.src_path:
            return

        current_time = time.time()
        self.last_modified = current_time

        if not self.pending_build:
            self.pending_build = True
            logger.info(f"Change detected in {event.src_path}")

            # Wait for debounce period
            time.sleep(self.debounce_seconds)

            # Check if any more changes happened during debounce
            if current_time == self.last_modified:
                self.build_docs()
                self.pending_build = False

    def build_docs(self):
        """Run the documentation build command."""
        logger.info("Rebuilding documentation...")

        try:
            # Run build command
            result = subprocess.run(
                self.build_command, shell=True, capture_output=True, text=True
            )

            if result.returncode == 0:
                logger.info("✅ Documentation rebuilt successfully!")
            else:
                logger.error(f"❌ Build failed with code {result.returncode}")
                if result.stderr:
                    logger.error(f"Error output:\n{result.stderr}")

        except Exception as e:
            logger.error(f"Failed to build docs: {e}")


def main():
    """Main entry point for docs watcher."""

    # Parse command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--fast":
        # Fast build without API regeneration
        build_command = "poetry run sphinx-build -b html docs/source docs/build/html -D autoapi_generate_api_docs=0"
        logger.info("Using fast build mode (no API regeneration)")
    else:
        # Full build with API regeneration
        build_command = "poetry run sphinx-build -b html docs/source docs/build/html"
        logger.info("Using full build mode (with API regeneration)")

    # Add live reload option
    if len(sys.argv) > 1 and sys.argv[-1] == "--serve":
        build_command += " && python -m http.server 8003 --directory docs/build/html"
        logger.info("Will serve docs at http://localhost:8003 after build")

    # Paths to watch
    watch_paths = [
        Path("docs/source"),
        Path("packages/haive-core/src"),
        Path("packages/haive-agents/src"),
        Path("packages/haive-tools/src"),
        Path("packages/haive-games/src"),
        Path("packages/haive-mcp/src"),
        Path("packages/haive-dataflow/src"),
        Path("packages/haive-prebuilt/src"),
    ]

    # Create event handler and observer
    event_handler = DocsBuildHandler(build_command)
    observer = Observer()

    # Add watchers for each path
    for path in watch_paths:
        if path.exists():
            observer.schedule(event_handler, str(path), recursive=True)
            logger.info(f"Watching {path}")
        else:
            logger.warning(f"Path {path} does not exist, skipping")

    # Initial build
    logger.info("Running initial documentation build...")
    event_handler.build_docs()

    # Start watching
    observer.start()
    logger.info("👀 Watching for changes... Press Ctrl+C to stop")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("Stopping docs watcher...")

    observer.join()


if __name__ == "__main__":
    main()
