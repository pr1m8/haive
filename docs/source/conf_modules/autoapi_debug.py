"""AutoAPI debugging configuration and error handling.

This module provides enhanced debugging capabilities for AutoAPI to help identify
problematic files during documentation builds.
"""

import logging
import os
import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


class AutoAPIDebugger:
    """Centralized debugging for AutoAPI issues."""

    def __init__(self, log_dir: Optional[Path] = None):
        """Initialize the debugger with a log directory."""
        self.log_dir = log_dir or Path(__file__).parent.parent / "logs"
        self.log_dir.mkdir(exist_ok=True)

        # Create separate log files for different types of issues
        self.error_log = (
            self.log_dir / f"autoapi_errors_{datetime.now():%Y%m%d_%H%M%S}.log"
        )
        self.skip_log = self.log_dir / "autoapi_skipped_files.log"
        self.progress_log = self.log_dir / "autoapi_progress.log"

        # Track statistics
        self.stats = {
            "total_files": 0,
            "successful_files": 0,
            "failed_files": 0,
            "skipped_files": 0,
            "errors": [],
        }

        self._setup_logging()

    def _setup_logging(self):
        """Configure logging for AutoAPI."""
        # Configure AutoAPI logger
        self.logger = logging.getLogger("autoapi")
        self.logger.setLevel(logging.DEBUG)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # File handler for all AutoAPI logs
        fh = logging.FileHandler(self.log_dir / "autoapi_debug.log")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        # Console handler for errors only
        ch = logging.StreamHandler(sys.stderr)
        ch.setLevel(logging.ERROR)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def log_error(self, filepath: str, error: Exception, context: str = ""):
        """Log an error with full details."""
        self.stats["failed_files"] += 1
        error_entry = {
            "file": filepath,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context,
            "timestamp": datetime.now().isoformat(),
        }
        self.stats["errors"].append(error_entry)

        # Write detailed error to log
        with open(self.error_log, "a") as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"ERROR in file: {filepath}\n")
            f.write(f"Timestamp: {error_entry['timestamp']}\n")
            f.write(f"Context: {context}\n")
            f.write(f"Error Type: {error_entry['error_type']}\n")
            f.write(f"Error Message: {error_entry['error_message']}\n")

            # Add more details for specific error types
            if hasattr(error, "lineno"):
                f.write(f"Line Number: {error.lineno}\n")
            if hasattr(error, "node"):
                f.write(f"AST Node: {error.node}\n")

            f.write(f"\nTraceback:\n{traceback.format_exc()}\n")
            f.write(f"{'='*80}\n")

        # Also log to main logger
        self.logger.error(f"Error in {filepath}: {error}")

    def log_skip(self, filepath: str, reason: str):
        """Log when a file is skipped."""
        self.stats["skipped_files"] += 1

        with open(self.skip_log, "a") as f:
            f.write(
                f"{datetime.now():%Y-%m-%d %H:%M:%S} - SKIPPED: {filepath} - Reason: {reason}\n"
            )

        self.logger.info(f"Skipped {filepath}: {reason}")

    def log_progress(self, message: str, filepath: Optional[str] = None):
        """Log progress messages."""
        self.stats["total_files"] += 1 if filepath else 0

        with open(self.progress_log, "a") as f:
            f.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} - {message}\n")
            if filepath:
                f.write(f"  File: {filepath}\n")

        self.logger.debug(message)

    def log_success(self, filepath: str):
        """Log successful file processing."""
        self.stats["successful_files"] += 1
        self.logger.debug(f"Successfully processed: {filepath}")

    def write_summary(self):
        """Write a summary of the debugging session."""
        summary_path = self.log_dir / "autoapi_summary.log"

        with open(summary_path, "w") as f:
            f.write("AutoAPI Debug Summary\n")
            f.write("=" * 50 + "\n")
            f.write(f"Generated at: {datetime.now():%Y-%m-%d %H:%M:%S}\n\n")

            f.write("Statistics:\n")
            f.write(f"  Total files processed: {self.stats['total_files']}\n")
            f.write(f"  Successful: {self.stats['successful_files']}\n")
            f.write(f"  Failed: {self.stats['failed_files']}\n")
            f.write(f"  Skipped: {self.stats['skipped_files']}\n\n")

            if self.stats["errors"]:
                f.write("Failed Files:\n")
                for error in self.stats["errors"]:
                    f.write(f"\n  File: {error['file']}\n")
                    f.write(
                        f"  Error: {error['error_type']} - {error['error_message']}\n"
                    )
                    f.write(f"  Time: {error['timestamp']}\n")

        print(f"\n📊 AutoAPI Debug Summary written to: {summary_path}", file=sys.stderr)


# Global debugger instance
_debugger = None


def get_debugger() -> AutoAPIDebugger:
    """Get or create the global debugger instance."""
    global _debugger
    if _debugger is None:
        _debugger = AutoAPIDebugger()
    return _debugger


def patch_autoapi_for_debugging():
    """Monkey-patch AutoAPI classes to add debugging."""
    try:
        import autoapi._astroid_utils
        from autoapi._mapper import Mapper
        from autoapi._parser import Parser

        debugger = get_debugger()

        # Write initial log entry with timestamp
        debugger.log_progress(
            f"=== AutoAPI Debugging Started at {datetime.now():%Y-%m-%d %H:%M:%S} ==="
        )

        # Store original methods
        _original_parse_file = Parser.parse_file
        _original_parse = Parser.parse
        _original_read_file = Mapper.read_file
        _original_load = Mapper.load
        _original_parse_file_with_return = Parser._parse_file
        _original_get_full_import_name = autoapi._astroid_utils.get_full_import_name

        # Track file being processed
        current_file = {"path": None}

        def debug_parse_file(self, path):
            """Wrapped parse_file with error logging."""
            current_file["path"] = path
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]

            # Show relative path for readability
            rel_path = str(path).replace("/home/will/Projects/haive/backend/haive/", "")

            # Only log parsing of actual project files (not dependencies)
            if "/haive/packages/" in str(path):
                debugger.log_progress(
                    f"[{timestamp}] Parsing: {rel_path}", filepath=path
                )

            try:
                result = _original_parse_file(self, path)
                if "/haive/packages/" in str(path):
                    debugger.log_success(path)
                return result
            except Exception as e:
                debugger.log_error(path, e, context="Parser.parse_file")

                # Show VERY prominent error message
                print(f"\n{'='*120}", file=sys.stderr)
                print(f"🚨 PARSING ERROR FOUND", file=sys.stderr)
                print(f"{'='*120}", file=sys.stderr)
                print(f"⏰ Time: {timestamp}", file=sys.stderr)
                print(f"📁 File: {rel_path}", file=sys.stderr)
                print(f"📍 Full path: {path}", file=sys.stderr)
                print(f"⚠️  Error type: {type(e).__name__}", file=sys.stderr)
                print(f"💬 Error message: {str(e)}", file=sys.stderr)

                # Show the actual file contents
                try:
                    with open(path, "r") as f:
                        lines = f.readlines()
                        print(f"\n📝 File contents:", file=sys.stderr)
                        for i, line in enumerate(lines, 1):
                            if i <= 30:  # Show first 30 lines
                                if "import" in line or "from" in line:
                                    print(
                                        f"   {i:2d} ➤ {line.rstrip()}", file=sys.stderr
                                    )
                                else:
                                    print(
                                        f"   {i:2d}   {line.rstrip()}", file=sys.stderr
                                    )
                            elif i == 31:
                                print(
                                    f"   ... (file continues for {len(lines)} total lines)",
                                    file=sys.stderr,
                                )
                                break
                except Exception as read_error:
                    print(f"   (Could not read file: {read_error})", file=sys.stderr)

                # If it's an import error, try to provide more context
                if (
                    "import" in str(e).lower()
                    or "TooManyLevelsError" in type(e).__name__
                ):
                    print(f"\n🔍 IMPORT ANALYSIS:", file=sys.stderr)
                    print(
                        f"   This appears to be a relative import issue",
                        file=sys.stderr,
                    )
                    print(
                        f"   Look for imports with '..' or multiple dots",
                        file=sys.stderr,
                    )
                    print(
                        f"   These indicate relative imports that may be invalid",
                        file=sys.stderr,
                    )

                print(f"\n🛑 BUILD FAILED ON THIS FILE", file=sys.stderr)
                print(f"{'='*120}\n", file=sys.stderr)
                raise

        def debug_parse(self, node):
            """Wrapped parse method to track AST parsing."""
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            file_info = (
                f" (file: {current_file['path']})" if current_file["path"] else ""
            )
            debugger.logger.debug(
                f"[{timestamp}] Parsing AST node: {type(node).__name__}{file_info}"
            )
            try:
                return _original_parse(self, node)
            except Exception as e:
                debugger.log_error(
                    current_file.get("path", "unknown"),
                    e,
                    context=f"Parser.parse - Node type: {type(node).__name__}",
                )
                raise

        def debug_parse_file_internal(self, file_path, condition):
            """Wrapped _parse_file to catch internal parsing errors."""
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            debugger.logger.debug(f"[{timestamp}] Internal parse_file: {file_path}")
            try:
                return _original_parse_file_with_return(self, file_path, condition)
            except Exception as e:
                debugger.log_error(
                    file_path, e, context="Parser._parse_file (internal)"
                )
                raise

        def debug_read_file(self, path=None, **kwargs):
            """Wrapped read_file with error logging."""
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            debugger.log_progress(f"[{timestamp}] Reading file: {path}", filepath=path)
            try:
                result = _original_read_file(self, path=path, **kwargs)
                return result
            except Exception as e:
                debugger.log_error(path, e, context="Mapper.read_file")
                print(f"\n❌ ERROR at {timestamp} reading: {path}", file=sys.stderr)
                raise

        def debug_get_full_import_name(from_node, name):
            """Wrapped get_full_import_name to catch import resolution errors."""
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            try:
                module_file = getattr(from_node.root(), "file", "unknown")
                # Only log for project files - but reduce verbosity
                if (
                    "/haive/packages/" in str(module_file)
                    and debugger.stats["total_files"] % 100 == 0
                ):
                    debugger.logger.debug(
                        f"[{timestamp}] Resolving import '{name}' in {module_file}"
                    )
                return _original_get_full_import_name(from_node, name)
            except Exception as e:
                module_file = getattr(
                    from_node.root(), "file", current_file.get("path", "unknown")
                )
                rel_path = str(module_file).replace(
                    "/home/will/Projects/haive/backend/haive/", ""
                )

                # STOP EVERYTHING AND SHOW THE ERROR PROMINENTLY
                print(f"\n{'='*120}", file=sys.stderr)
                print(f"🚨 CRITICAL ERROR FOUND - STOPPING BUILD", file=sys.stderr)
                print(f"{'='*120}", file=sys.stderr)
                print(f"⏰ Time: {timestamp}", file=sys.stderr)
                print(f"📁 File with error: {rel_path}", file=sys.stderr)
                print(f"📍 Full path: {module_file}", file=sys.stderr)
                print(f"📦 Failed import: '{name}'", file=sys.stderr)
                print(f"⚠️  Error type: {type(e).__name__}", file=sys.stderr)
                print(f"💬 Error message: {str(e)}", file=sys.stderr)

                # Show file contents around the problematic import
                try:
                    with open(module_file, "r") as f:
                        lines = f.readlines()
                        print(f"\n📝 File contents (first 20 lines):", file=sys.stderr)
                        for i, line in enumerate(lines[:20], 1):
                            if "import" in line:
                                print(
                                    f"   {i:2d} ➤ {line.rstrip()}", file=sys.stderr
                                )  # Highlight import lines
                            else:
                                print(f"   {i:2d}   {line.rstrip()}", file=sys.stderr)
                except Exception:
                    print(f"   (Could not read file contents)", file=sys.stderr)

                if (
                    "TooManyLevelsError" in str(e)
                    or "TooManyLevelsError" in type(e).__name__
                ):
                    print(
                        f"\n🔍 DIAGNOSIS: Relative import with too many levels",
                        file=sys.stderr,
                    )
                    print(
                        f"   This means the file has a relative import like 'from .. import X'",
                        file=sys.stderr,
                    )
                    print(
                        f"   but there's no parent package to import from.",
                        file=sys.stderr,
                    )
                    print(
                        f"   Look for lines with '..' or multiple '.' in import statements.",
                        file=sys.stderr,
                    )

                print(
                    f"\n🛑 BUILD STOPPED - Fix this file and try again", file=sys.stderr
                )
                print(f"{'='*120}\n", file=sys.stderr)

                # Log to file as well
                debugger.log_error(
                    module_file,
                    e,
                    context=f"get_full_import_name - Import: '{name}' - BUILD STOPPED",
                )

                # Don't re-raise - let's try to continue and see if there are more errors
                # But mark this prominently
                print(f"⚠️  CONTINUING BUILD TO FIND MORE ERRORS...", file=sys.stderr)

                # Return a dummy value to continue processing
                return f"ERROR_IMPORT_{name}"

        def debug_load(self, patterns=None, dirs=None, **kwargs):
            """Wrapped load method to track overall progress and phases."""
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]

            print(f"\n{'='*80}", file=sys.stderr)
            print(f"🚀 AUTOAPI STARTING at {timestamp}", file=sys.stderr)
            print(
                f"📂 Directories to process: {len(dirs) if dirs else 0}",
                file=sys.stderr,
            )

            debugger.log_progress(
                f"[{timestamp}] Starting AutoAPI load process - Dirs: {dirs}"
            )

            # Log directories being processed
            if dirs:
                for i, d in enumerate(dirs, 1):
                    rel_dir = str(d).replace(
                        "/home/will/Projects/haive/backend/haive/", ""
                    )
                    print(f"   {i}. {rel_dir}", file=sys.stderr)
                    debugger.log_progress(f"  Processing directory: {d}")

            print(f"{'='*80}\n", file=sys.stderr)

            # Track phases
            current_phase = {"phase": "INITIALIZATION", "start_time": datetime.now()}

            def update_phase(new_phase):
                elapsed = (datetime.now() - current_phase["start_time"]).total_seconds()
                timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                print(
                    f"[{timestamp}] ✅ Completed phase: {current_phase['phase'].upper()} ({elapsed:.1f}s)",
                    file=sys.stderr,
                )
                current_phase["phase"] = new_phase
                current_phase["start_time"] = datetime.now()
                print(
                    f"[{timestamp}] 📍 Starting phase: {new_phase.upper()}",
                    file=sys.stderr,
                )
                debugger.log_progress(
                    f"PHASE CHANGE: {current_phase['phase']} -> {new_phase}"
                )

            files_processed = 0
            files_parsed = 0

            # Store original methods to intercept various phases
            original_create_mapper = (
                self.create_mapper if hasattr(self, "create_mapper") else None
            )
            original_read_files = (
                self.read_files if hasattr(self, "read_files") else None
            )
            original_map = self.map if hasattr(self, "map") else None
            original_create_objects = (
                self.create_objects if hasattr(self, "create_objects") else None
            )

            try:
                # Phase 1: File Discovery
                update_phase("FILE_DISCOVERY")

                # Intercept file processing
                original_find_files = self.find_files

                def counting_find_files(*args, **kwargs):
                    nonlocal files_processed
                    last_file = None
                    discovery_start = datetime.now()

                    for file_path in original_find_files(*args, **kwargs):
                        files_processed += 1
                        last_file = file_path

                        # Show progress every 50 files with more detail
                        if files_processed % 50 == 0:
                            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                            # Extract relative path for readability
                            if isinstance(file_path, (str, Path)):
                                rel_path = str(file_path).replace(
                                    "/home/will/Projects/haive/backend/haive/", ""
                                )
                            else:
                                rel_path = str(file_path)
                            elapsed = (datetime.now() - discovery_start).total_seconds()
                            print(
                                f"[{timestamp}] 📂 Phase: {current_phase['phase']} | Files: {files_processed} | Current: {rel_path} | Elapsed: {elapsed:.1f}s",
                                file=sys.stderr,
                            )

                        # Show every 10th file in debug log
                        if files_processed % 10 == 0:
                            debugger.log_progress(
                                f"[{current_phase['phase']}] File #{files_processed}: {file_path}"
                            )

                        yield file_path

                    # Log the last file processed before any error
                    if last_file:
                        debugger.log_progress(
                            f"[{current_phase['phase']}] Last file: {last_file}"
                        )
                        update_phase("FILE_PARSING")

                self.find_files = counting_find_files

                # Intercept parser methods to track parsing phase
                if hasattr(Parser, "parse_file"):
                    original_parser_parse = Parser.parse_file

                    def tracking_parse_file(parser_self, path):
                        nonlocal files_parsed
                        files_parsed += 1

                        if (
                            files_parsed == 1
                            and current_phase["phase"] != "FILE_PARSING"
                        ):
                            update_phase("FILE_PARSING")

                        if files_parsed % 20 == 0:
                            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                            rel_path = str(path).replace(
                                "/home/will/Projects/haive/backend/haive/", ""
                            )
                            print(
                                f"[{timestamp}] 🔍 Phase: {current_phase['phase']} | Parsed: {files_parsed}/{files_processed} | Current: {rel_path}",
                                file=sys.stderr,
                            )

                        return original_parser_parse(parser_self, path)

                    Parser.parse_file = tracking_parse_file

                # Track when moving to object creation phase
                if original_create_objects:

                    def tracking_create_objects(*args, **kwargs):
                        update_phase("OBJECT_CREATION")
                        return original_create_objects(*args, **kwargs)

                    self.create_objects = tracking_create_objects

                # Track mapping phase
                if original_map:

                    def tracking_map(*args, **kwargs):
                        update_phase("MAPPING")
                        return original_map(*args, **kwargs)

                    self.map = tracking_map

                # Execute the original load
                result = _original_load(self, patterns=patterns, dirs=dirs, **kwargs)

                # Final phase
                update_phase("RENDERING")

                timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                print(
                    f"\n[{timestamp}] ✅ AUTOAPI COMPLETED SUCCESSFULLY",
                    file=sys.stderr,
                )
                print(f"   Total files discovered: {files_processed}", file=sys.stderr)
                print(f"   Total files parsed: {files_parsed}", file=sys.stderr)

                debugger.log_progress(
                    f"AutoAPI load completed - Discovered: {files_processed}, Parsed: {files_parsed}"
                )
                debugger.write_summary()
                return result

            except Exception as e:
                timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                print(f"\n[{timestamp}] ❌ AUTOAPI FAILED", file=sys.stderr)
                print(f"   Phase: {current_phase['phase']}", file=sys.stderr)
                print(f"   Files discovered: {files_processed}", file=sys.stderr)
                print(f"   Files parsed: {files_parsed}", file=sys.stderr)
                print(f"   Error: {type(e).__name__}: {str(e)}", file=sys.stderr)

                debugger.log_progress(
                    f"AutoAPI FAILED in phase {current_phase['phase']} - Discovered: {files_processed}, Parsed: {files_parsed}"
                )
                debugger.write_summary()
                raise

        # Apply patches
        Parser.parse_file = debug_parse_file
        Parser.parse = debug_parse
        Parser._parse_file = debug_parse_file_internal
        Mapper.read_file = debug_read_file
        Mapper.load = debug_load
        autoapi._astroid_utils.get_full_import_name = debug_get_full_import_name

        print(
            f"✅ AutoAPI debug patches installed at {datetime.now():%Y-%m-%d %H:%M:%S}",
            file=sys.stderr,
        )
        print(f"📁 Debug logs will be written to: {debugger.log_dir}", file=sys.stderr)
        debugger.log_progress("AutoAPI debugging patches applied successfully")

    except ImportError as e:
        print(f"⚠️  Could not patch AutoAPI for debugging: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()


def configure_autoapi_debugging(app: Any) -> Dict[str, Any]:
    """Configure AutoAPI with debugging options.

    Args:
        app: Sphinx application instance

    Returns:
        Dictionary of AutoAPI configuration options
    """
    debugger = get_debugger()

    # Patch AutoAPI for better error tracking
    patch_autoapi_for_debugging()

    # Return additional configuration options
    return {
        # More verbose output
        "autoapi_python_use_implicit_namespaces": False,
        # Keep generated files for inspection
        "autoapi_keep_files": True,
        # Add event handlers
        "autoapi_prepare_jinja_env": lambda jinja_env: debugger.log_progress(
            "Preparing Jinja environment"
        ),
    }


def setup_debugging_hooks(app: Any):
    """Setup Sphinx event hooks for AutoAPI debugging."""
    debugger = get_debugger()

    def on_autoapi_skip_member(app, what, name, obj, skip, options):
        """Log when AutoAPI skips a member."""
        if skip:
            debugger.log_skip(name, f"Skipped {what}")
        return skip

    def on_builder_inited(app):
        """Log when builder is initialized."""
        debugger.log_progress("Sphinx builder initialized")

    def on_build_finished(app, exception):
        """Log when build is finished."""
        if exception:
            debugger.log_progress(f"Build finished with exception: {exception}")
        else:
            debugger.log_progress("Build finished successfully")
        debugger.write_summary()

    # Connect event handlers
    app.connect("autoapi-skip-member", on_autoapi_skip_member)
    app.connect("builder-inited", on_builder_inited)
    app.connect("build-finished", on_build_finished)

    # Log initial setup
    debugger.log_progress("AutoAPI debugging hooks configured")
    print(
        f"✅ AutoAPI debugging enabled - logs in: {debugger.log_dir}", file=sys.stderr
    )
