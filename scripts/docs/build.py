#!/usr/bin/env python3
"""
Documentation build script.
Place in scripts/docs/build_docs.py
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import http.server
import socketserver
import threading
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

class DocsBuilder:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.docs_dir = self.project_root / "docs"
        self.build_dir = self.docs_dir / "_build" / "html"
        self.src_dir = self.project_root / "src"
        self.scripts_dir = self.docs_dir / "scripts"

    def setup_directories(self):
        """Create necessary directories."""
        dirs = [
            self.docs_dir / "_static",
            self.docs_dir / "_build",
            self.docs_dir / "_templates",
            self.docs_dir / "api" / "_autosummary",
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)

    def clean_build(self):
        """Clean previous build."""
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)

    def build_docs(self):
        """Build the documentation."""
        try:
            # Set up environment
            env = os.environ.copy()
            env["PYTHONPATH"] = f"{self.src_dir}:{env.get('PYTHONPATH', '')}"

            # Run Sphinx build
            cmd = [
                "sphinx-build",
                "-b", "html",
                str(self.docs_dir),
                str(self.build_dir)
            ]
            
            result = subprocess.run(
                cmd,
                env=env,
                check=True,
                capture_output=True,
                text=True
            )

            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Build failed: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"Error during build: {e}")
            return False

    def serve_docs(self):
        """Serve the documentation."""
        if not self.build_dir.exists():
            logger.error("Build directory not found! Run build first.")
            return False

        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=str(self.build_dir), **kwargs)

        try:
            port = 8000
            with socketserver.TCPServer(("", port), Handler) as httpd:
                logger.info(f"Serving documentation at http://localhost:{port}")
                httpd.serve_forever()
        except Exception as e:
            logger.error(f"Server error: {e}")
            return False

def build():
    """Build the documentation."""
    builder = DocsBuilder()
    builder.setup_directories()
    builder.clean_build()
    success = builder.build_docs()
    return 0 if success else 1

def serve():
    """Serve the documentation."""
    builder = DocsBuilder()
    builder.serve_docs()
    return 0

def main():
    """Main entry point."""
    command = sys.argv[1] if len(sys.argv) > 1 else "build"
    
    if command == "build":
        return build()
    elif command == "serve":
        return serve()
    elif command == "both":
        if build() == 0:
            return serve()
        return 1
    else:
        logger.error(f"Unknown command: {command}")
        return 1

if __name__ == "__main__":
    sys.exit(main())