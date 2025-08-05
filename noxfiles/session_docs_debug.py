"""Debug session for documentation build with enhanced logging."""

import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import nox

# Configuration
PYTHON_VERSIONS = ["3.12"]
DOCS_DIR = Path("docs")
SOURCE_DIR = DOCS_DIR / "source"
BUILD_DIR = DOCS_DIR / "build"
LOGS_DIR = DOCS_DIR / "logs"
DEBUG_DIR = LOGS_DIR / "debug"

# Ensure directories exist
DEBUG_DIR.mkdir(parents=True, exist_ok=True)

# Reuse virtualenvs for speed
nox.options.reuse_existing_virtualenvs = True


class DebugLogger:
    """Enhanced logger for debugging documentation builds."""

    def __init__(self, session, debug_file: Path):
        self.session = session
        self.debug_file = debug_file
        self.start_time = time.time()
        self.checkpoints = []
        self.errors = []
        self.warnings = []
        self.info_messages = []
        self.file_operations = []

        # Open debug file
        self.debug_handle = open(debug_file, "w")
        self.write_header()

    def write_header(self):
        """Write debug log header."""
        self.debug_handle.write("=" * 80 + "\n")
        self.debug_handle.write("SPHINX BUILD DEBUG LOG\n")
        self.debug_handle.write(f"Started: {datetime.now()}\n")
        self.debug_handle.write(f"Python: {sys.version}\n")
        self.debug_handle.write(f"Working Directory: {Path.cwd()}\n")
        self.debug_handle.write("=" * 80 + "\n\n")
        self.debug_handle.flush()

    def checkpoint(self, name: str, data: dict = None):
        """Record a checkpoint with optional data."""
        elapsed = time.time() - self.start_time
        checkpoint_data = {
            "name": name,
            "time": elapsed,
            "timestamp": datetime.now().isoformat(),
            "data": data or {},
        }
        self.checkpoints.append(checkpoint_data)

        # Write to session log
        self.session.log(f"🔍 CHECKPOINT [{elapsed:.1f}s]: {name}")
        if data:
            for key, value in data.items():
                self.session.log(f"   {key}: {value}")

        # Write to debug file
        self.debug_handle.write(f"\n[{elapsed:.1f}s] CHECKPOINT: {name}\n")
        if data:
            self.debug_handle.write(json.dumps(data, indent=2) + "\n")
        self.debug_handle.flush()

    def log_command(self, cmd: list[str], cwd: str = None):
        """Log command execution."""
        self.debug_handle.write(f"\n🔧 COMMAND: {' '.join(cmd)}\n")
        if cwd:
            self.debug_handle.write(f"   CWD: {cwd}\n")
        self.debug_handle.flush()

    def log_output(self, line: str, level: str = "info"):
        """Log command output with classification."""
        # Classify the line
        if any(
            err in line.lower() for err in ["error", "exception", "traceback", "failed"]
        ):
            level = "error"
            self.errors.append(line)
        elif any(warn in line.lower() for warn in ["warning", "warn", "deprecated"]):
            level = "warning"
            self.warnings.append(line)
        elif any(
            info in line.lower()
            for info in ["writing", "building", "reading", "processing"]
        ):
            level = "progress"

        # Color coding for session
        colors = {
            "error": "31",  # Red
            "warning": "33",  # Yellow
            "progress": "32",  # Green
            "info": "0",  # Default
        }
        color = colors.get(level, "0")

        # Write to session with color
        if level in ["error", "warning", "progress"]:
            self.session.log(f"\033[{color}m{line}\033[0m")

        # Write to debug file
        self.debug_handle.write(f"[{level.upper()}] {line}\n")
        self.debug_handle.flush()

    def track_file_operation(self, operation: str, path: str, success: bool = True):
        """Track file operations."""
        self.file_operations.append(
            {
                "operation": operation,
                "path": path,
                "success": success,
                "time": time.time() - self.start_time,
            }
        )

        status = "✅" if success else "❌"
        self.session.log(f"{status} {operation}: {path}")
        self.debug_handle.write(
            f"\nFILE_OP: {operation} {path} - {'SUCCESS' if success else 'FAILED'}\n"
        )
        self.debug_handle.flush()

    def analyze_state(self):
        """Analyze current build state."""
        state = {
            "html_files": 0,
            "source_files": 0,
            "build_exists": False,
            "errors_count": len(self.errors),
            "warnings_count": len(self.warnings),
        }

        # Check source files
        if SOURCE_DIR.exists():
            state["source_files"] = len(list(SOURCE_DIR.rglob("*.rst"))) + len(
                list(SOURCE_DIR.rglob("*.md"))
            )

        # Check build directory
        if BUILD_DIR.exists():
            state["build_exists"] = True
            html_dir = BUILD_DIR / "html"
            if html_dir.exists():
                state["html_files"] = len(list(html_dir.rglob("*.html")))

        self.checkpoint("STATE_ANALYSIS", state)
        return state

    def close(self):
        """Close debug log with summary."""
        total_time = time.time() - self.start_time

        # Write summary
        self.debug_handle.write("\n" + "=" * 80 + "\n")
        self.debug_handle.write("BUILD SUMMARY\n")
        self.debug_handle.write("=" * 80 + "\n")
        self.debug_handle.write(f"Total Time: {total_time:.1f}s\n")
        self.debug_handle.write(f"Checkpoints: {len(self.checkpoints)}\n")
        self.debug_handle.write(f"Errors: {len(self.errors)}\n")
        self.debug_handle.write(f"Warnings: {len(self.warnings)}\n")
        self.debug_handle.write(f"File Operations: {len(self.file_operations)}\n")

        # Final state
        final_state = self.analyze_state()
        self.debug_handle.write(f"\nFinal State:\n")
        self.debug_handle.write(json.dumps(final_state, indent=2) + "\n")

        self.debug_handle.close()

        # Print summary to session
        self.session.log("\n" + "=" * 60)
        self.session.log("📊 DEBUG SUMMARY")
        self.session.log("=" * 60)
        self.session.log(f"⏱️  Total Time: {total_time:.1f}s")
        self.session.log(f"❌ Errors: {len(self.errors)}")
        self.session.log(f"⚠️  Warnings: {len(self.warnings)}")
        self.session.log(f"📄 HTML Files Generated: {final_state['html_files']}")
        self.session.log(f"📝 Debug Log: {self.debug_file}")


@nox.session(python=PYTHON_VERSIONS)
def docs_debug_enhanced(session):
    """Debug documentation build with comprehensive logging.

    This session provides detailed debugging information to understand
    why the documentation build is not generating HTML files.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    debug_file = DEBUG_DIR / f"sphinx_debug_{timestamp}.log"

    session.log("🐛 Starting DEBUG documentation build...")
    session.log(f"📝 Debug log: {debug_file}")

    # Create debug logger
    logger = DebugLogger(session, debug_file)

    # Check environment
    logger.checkpoint("ENVIRONMENT_CHECK")

    # Install dependencies
    logger.checkpoint("INSTALL_START")
    session.install(".[docs]")  # Install with docs extras
    logger.checkpoint("INSTALL_COMPLETE")

    # Verify Sphinx installation
    logger.checkpoint("VERIFY_SPHINX")
    result = subprocess.run(
        ["poetry", "run", "sphinx-build", "--version"], capture_output=True, text=True
    )
    logger.checkpoint("SPHINX_VERSION", {"version": result.stdout.strip()})

    # Check source directory
    logger.checkpoint("CHECK_SOURCE")
    source_files = list(SOURCE_DIR.rglob("*.rst")) + list(SOURCE_DIR.rglob("*.md"))
    logger.checkpoint(
        "SOURCE_FILES",
        {
            "count": len(source_files),
            "rst_files": len(list(SOURCE_DIR.rglob("*.rst"))),
            "md_files": len(list(SOURCE_DIR.rglob("*.md"))),
        },
    )

    # Test conf.py import
    logger.checkpoint("TEST_CONF_IMPORT")
    test_import = subprocess.run(
        [
            "poetry",
            "run",
            "python",
            "-c",
            f"import sys; sys.path.insert(0, '{SOURCE_DIR}'); import conf; print('OK')",
        ],
        capture_output=True,
        text=True,
    )
    logger.checkpoint(
        "CONF_IMPORT_RESULT",
        {
            "success": test_import.returncode == 0,
            "stdout": test_import.stdout,
            "stderr": test_import.stderr,
        },
    )

    # Clear build directory
    logger.checkpoint("CLEAR_BUILD")
    if BUILD_DIR.exists():
        import shutil

        shutil.rmtree(BUILD_DIR)
        logger.track_file_operation("REMOVED", str(BUILD_DIR))
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    logger.track_file_operation("CREATED", str(BUILD_DIR))

    # Run Sphinx build with detailed output capture
    logger.checkpoint("SPHINX_BUILD_START")

    cmd = [
        "poetry",
        "run",
        "sphinx-build",
        "-v",  # Verbose
        "-T",  # Show full traceback
        "-E",  # Force rebuild
        "-a",  # Write all files
        "-b",
        "html",
        str(SOURCE_DIR),
        str(BUILD_DIR / "html"),
    ]

    # Set minimal environment
    env = os.environ.copy()
    env["SPHINX_PROFILE"] = "minimal"
    env["SPHINX_DISABLE_EXAMPLES"] = "1"

    logger.log_command(cmd)
    logger.checkpoint("EXECUTING_SPHINX")

    # Run with real-time output capture
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env=env,
    )

    # Process output line by line
    line_count = 0
    for line in process.stdout:
        line = line.strip()
        if line:
            line_count += 1
            logger.log_output(line)

            # Track specific events
            if "reading sources..." in line:
                logger.checkpoint("READING_SOURCES")
            elif "building [html]:" in line:
                logger.checkpoint("BUILDING_HTML")
            elif "writing output..." in line:
                logger.checkpoint("WRITING_OUTPUT")
            elif "build succeeded" in line:
                logger.checkpoint("BUILD_SUCCEEDED")
            elif "build finished with problems" in line:
                logger.checkpoint("BUILD_FAILED")

    process.wait()
    logger.checkpoint(
        "SPHINX_BUILD_COMPLETE",
        {"exit_code": process.returncode, "lines_processed": line_count},
    )

    # Analyze results
    logger.checkpoint("ANALYZE_RESULTS")

    # Check for HTML files
    html_files = (
        list((BUILD_DIR / "html").rglob("*.html"))
        if (BUILD_DIR / "html").exists()
        else []
    )
    logger.checkpoint(
        "HTML_FILES_CHECK",
        {
            "count": len(html_files),
            "files": [
                str(f.relative_to(BUILD_DIR)) for f in html_files[:10]
            ],  # First 10
        },
    )

    # Check for other output files
    all_files = list(BUILD_DIR.rglob("*")) if BUILD_DIR.exists() else []
    file_types = {}
    for f in all_files:
        if f.is_file():
            ext = f.suffix or "no_extension"
            file_types[ext] = file_types.get(ext, 0) + 1

    logger.checkpoint(
        "ALL_OUTPUT_FILES", {"total": len(all_files), "by_type": file_types}
    )

    # Check for specific error patterns
    if logger.errors:
        logger.checkpoint(
            "ERROR_ANALYSIS",
            {"count": len(logger.errors), "first_errors": logger.errors[:5]},
        )

    # Close and summarize
    logger.close()

    # Final verdict
    if html_files:
        session.log(f"\n✅ SUCCESS: Generated {len(html_files)} HTML files!")
        session.log(
            f"🌐 View at: file://{(BUILD_DIR / 'html' / 'index.html').absolute()}"
        )
    else:
        session.log("\n❌ FAILED: No HTML files generated!")
        session.log(f"📋 Check debug log for details: {debug_file}")

        # Print key errors
        if logger.errors:
            session.log("\n🚨 Key Errors:")
            for error in logger.errors[:3]:
                session.log(f"  - {error}")


@nox.session(python=PYTHON_VERSIONS)
def docs_minimal_test(session):
    """Test minimal Sphinx build with step-by-step debugging."""
    session.log("🧪 Testing minimal Sphinx configuration...")

    # Create temporary test directory
    test_dir = Path("docs/test_minimal")
    test_dir.mkdir(parents=True, exist_ok=True)

    # Create minimal conf.py
    minimal_conf = test_dir / "conf.py"
    minimal_conf.write_text(
        """
project = "Test"
extensions = []
    """
    )

    # Create minimal index.rst
    minimal_index = test_dir / "index.rst"
    minimal_index.write_text(
        """
Test Documentation
==================

This is a test.
    """
    )

    # Test build
    session.log("📦 Building minimal test documentation...")
    result = session.run(
        "sphinx-build",
        "-b",
        "html",
        str(test_dir),
        str(test_dir / "_build"),
        external=True,
        success_codes=[0, 1, 2],
    )

    # Check results
    html_files = list((test_dir / "_build").rglob("*.html"))
    session.log(f"📄 Generated {len(html_files)} HTML files")

    # Clean up
    import shutil

    shutil.rmtree(test_dir)

    if html_files:
        session.log("✅ Minimal Sphinx build works!")
    else:
        session.log("❌ Even minimal Sphinx build fails!")
