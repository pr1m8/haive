"""AutoAPI debugging configuration and error handling.

This module provides enhanced debugging capabilities for AutoAPI to help
identify problematic files during documentation builds.
"""

from __future__ import annotations

from datetime import datetime
import logging
from pathlib import Path
import sys
import traceback
from typing import Any


class AutoAPIDebugger:
    """Centralized debugging for AutoAPI issues with graceful error.

    handling.
    """

    def __init__(self, log_dir: Path | None = None):
        """Initialize the debugger with a log directory."""
        self.log_dir = log_dir or Path(__file__).parent.parent / "logs"
        self.log_dir.mkdir(exist_ok=True)

        # Create timestamped run folder for this build
        self.run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.run_dir = self.log_dir / f"run_{self.run_timestamp}"
        self.run_dir.mkdir(exist_ok=True)

        # Create organized subfolders
        (self.run_dir / "errors").mkdir(exist_ok=True)
        (self.run_dir / "warnings").mkdir(exist_ok=True)
        (self.run_dir / "skipped").mkdir(exist_ok=True)
        (self.run_dir / "successful").mkdir(exist_ok=True)
        (self.run_dir / "by_package").mkdir(exist_ok=True)

        # Create separate log files for different types of issues
        self.error_log = self.run_dir / "errors" / "detailed_errors.log"
        self.skip_log = self.run_dir / "skipped" / "skipped_files.log"
        self.progress_log = self.run_dir / "build_progress.log"
        self.warnings_log = self.run_dir / "warnings" / "all_warnings.log"
        self.failed_imports_log = self.run_dir / "errors" / "failed_imports.log"
        self.package_summary_log = self.run_dir / "package_summary.log"

        # Track statistics with more detail
        self.stats = {
            "total_files": 0,
            "successful_files": 0,
            "failed_files": 0,
            "skipped_files": 0,
            "errors": [],
            "warnings": [],
            "failed_imports": {},  # package -> list of failed modules
            "package_stats": {},  # package -> {success: int, failed: int, skipped: int}
        }

        self._setup_logging()

    def _setup_logging(self):
        """Configure logging for AutoAPI."""
        # Configure AutoAPI logger
        self.logger = logging.getLogger("autoapi")
        self.logger.setLevel(logging.DEBUG)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
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
            f.write(f"\n{'=' * 80}\n")
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
            f.write(f"{'=' * 80}\n")

        # Also log to main logger
        self.logger.error(f"Error in {filepath}: {error}")

    def log_skip(self, filepath: str, reason: str):
        """Log when a file is skipped."""
        self.stats["skipped_files"] += 1

        with open(self.skip_log, "a") as f:
            f.write(
                f"{datetime.now():%Y-%m-%d %H:%M:%S} - SKIPPED: {filepath} - Reason: {reason}\n",
            )

        self.logger.info(f"Skipped {filepath}: {reason}")

    def log_progress(self, message: str, filepath: str | None = None):
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
        self._update_package_stats(filepath, "success")
        self.logger.debug(f"Successfully processed: {filepath}")

    def log_warning(self, filepath: str, warning: str, context: str = ""):
        """Log warnings with package tracking."""
        self.stats["warnings"].append(
            {
                "file": filepath,
                "warning": warning,
                "context": context,
                "timestamp": datetime.now().isoformat(),
            },
        )

        # Write to warnings log
        with open(self.warnings_log, "a") as f:
            f.write(f"\n{'=' * 80}\n")
            f.write(f"WARNING in file: {filepath}\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write(f"Context: {context}\n")
            f.write(f"Warning: {warning}\n")
            f.write(f"{'=' * 80}\n")

        self.logger.warning(f"Warning in {filepath}: {warning}")

    def log_failed_import(self, package: str, module: str, error: Exception):
        """Log failed imports by package."""
        if package not in self.stats["failed_imports"]:
            self.stats["failed_imports"][package] = []

        self.stats["failed_imports"][package].append(
            {
                "module": module,
                "error": str(error),
                "error_type": type(error).__name__,
                "timestamp": datetime.now().isoformat(),
            },
        )

        # Write to failed imports log
        with open(self.failed_imports_log, "a") as f:
            f.write(f"\n{'=' * 60}\n")
            f.write(f"FAILED IMPORT - Package: {package}\n")
            f.write(f"Module: {module}\n")
            f.write(f"Error: {type(error).__name__}: {error!s}\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write(f"{'=' * 60}\n")

        self.logger.error(f"Failed import in {package}: {module} - {error}")

    def _update_package_stats(self, filepath: str, status: str):
        """Update per-package statistics."""
        # Extract package name from filepath
        package = self._extract_package_name(filepath)
        if not package:
            return

        if package not in self.stats["package_stats"]:
            self.stats["package_stats"][package] = {
                "success": 0,
                "failed": 0,
                "skipped": 0,
                "warnings": 0,
            }

        self.stats["package_stats"][package][status] += 1

    def _extract_package_name(self, filepath: str) -> str:
        """Extract package name from file path."""
        try:
            if "/packages/" in filepath:
                parts = filepath.split("/packages/")
                if len(parts) > 1:
                    package_part = parts[1].split("/")[0]
                    return package_part
            return "unknown"
        except Exception:
            return "unknown"

    def create_graceful_import_wrapper(self, module_path: str):
        """Create a graceful import wrapper that handles failures."""

        def safe_import():
            try:
                return __import__(module_path)
            except ImportError as e:
                package = self._extract_package_name(module_path)
                self.log_failed_import(package, module_path, e)
                return None
            except Exception as e:
                package = self._extract_package_name(module_path)
                self.log_failed_import(package, module_path, e)
                return None

        return safe_import

    def write_summary(self):
        """Write comprehensive summary with package breakdowns."""
        # Main summary file
        summary_path = self.run_dir / "build_summary.log"

        with open(summary_path, "w") as f:
            f.write("🚀 AutoAPI Debug Summary - Graceful Error Handling\n")
            f.write("=" * 60 + "\n")
            f.write(f"Run ID: {self.run_timestamp}\n")
            f.write(f"Generated at: {datetime.now():%Y-%m-%d %H:%M:%S}\n\n")

            # Overall Statistics
            f.write("📊 Overall Statistics:\n")
            f.write(f"  Total files processed: {self.stats['total_files']}\n")
            f.write(f"  ✅ Successful: {self.stats['successful_files']}\n")
            f.write(f"  ❌ Failed: {self.stats['failed_files']}\n")
            f.write(f"  ⏭️  Skipped: {self.stats['skipped_files']}\n")
            f.write(f"  ⚠️  Warnings: {len(self.stats['warnings'])}\n")
            f.write(f"  📦 Packages with failed imports: {len(self.stats['failed_imports'])}\n\n")

            # Package Statistics
            f.write("📦 Per-Package Statistics:\n")
            for package, stats in self.stats["package_stats"].items():
                total = sum(stats.values())
                success_rate = (stats["success"] / total * 100) if total > 0 else 0
                f.write(f"  {package}:\n")
                f.write(f"    ✅ Success: {stats['success']}\n")
                f.write(f"    ❌ Failed: {stats['failed']}\n")
                f.write(f"    ⏭️ Skipped: {stats['skipped']}\n")
                f.write(f"    ⚠️ Warnings: {stats['warnings']}\n")
                f.write(f"    📈 Success Rate: {success_rate:.1f}%\n\n")

            # Failed Imports Summary
            if self.stats["failed_imports"]:
                f.write("🚫 Failed Imports by Package:\n")
                for package, failures in self.stats["failed_imports"].items():
                    f.write(f"  {package} ({len(failures)} failures):\n")
                    for failure in failures[:5]:  # Show first 5
                        f.write(f"    - {failure['module']}: {failure['error_type']}\n")
                    if len(failures) > 5:
                        f.write(f"    ... and {len(failures) - 5} more\n")
                    f.write("\n")

            # Recent Errors
            if self.stats["errors"]:
                f.write("🔥 Recent Errors:\n")
                for error in self.stats["errors"][-10:]:  # Last 10 errors
                    f.write(f"  📁 {error['file']}\n")
                    f.write(f"     {error['error_type']}: {error['error_message'][:100]}...\n\n")

        # Write package summaries to separate files
        self._write_package_summaries()

        # Create index file pointing to all logs
        self._write_log_index()

        print(f"\n📊 AutoAPI Debug Summary written to: {summary_path}", file=sys.stderr)
        print(f"📁 Full logs available in: {self.run_dir}", file=sys.stderr)
        print(f"📋 Log index: {self.run_dir}/log_index.html", file=sys.stderr)

    def _write_package_summaries(self):
        """Write individual summaries for each package."""
        for package, failures in self.stats["failed_imports"].items():
            package_file = self.run_dir / "by_package" / f"{package}_summary.log"
            with open(package_file, "w") as f:
                f.write(f"Package: {package}\n")
                f.write("=" * 40 + "\n\n")

                stats = self.stats["package_stats"].get(package, {})
                f.write("Statistics:\n")
                for key, value in stats.items():
                    f.write(f"  {key.capitalize()}: {value}\n")
                f.write("\n")

                f.write("Failed Imports:\n")
                for failure in failures:
                    f.write(f"  Module: {failure['module']}\n")
                    f.write(f"  Error: {failure['error_type']}: {failure['error']}\n")
                    f.write(f"  Time: {failure['timestamp']}\n")
                    f.write("-" * 40 + "\n")

    def _write_log_index(self):
        """Create an HTML index of all log files."""
        index_file = self.run_dir / "log_index.html"
        with open(index_file, "w") as f:
            f.write(f"""<!DOCTYPE html>
<html>
<head>
    <title>AutoAPI Debug Logs - {self.run_timestamp}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .log-section {{ margin: 20px 0; }}
        .log-link {{ display: block; margin: 5px 0; padding: 5px; background: #f0f0f0; }}
        .stats {{ background: #e8f4f8; padding: 10px; border-radius: 5px; }}
    </style>
</head>
<body>
    <h1>🚀 AutoAPI Debug Logs</h1>
    <p><strong>Run ID:</strong> {self.run_timestamp}</p>
    <p><strong>Generated:</strong> {datetime.now():%Y-%m-%d %H:%M:%S}</p>

    <div class="stats">
        <h3>📊 Quick Stats</h3>
        <p>✅ Successful: {self.stats["successful_files"]}</p>
        <p>❌ Failed: {self.stats["failed_files"]}</p>
        <p>⏭️ Skipped: {self.stats["skipped_files"]}</p>
        <p>⚠️ Warnings: {len(self.stats["warnings"])}</p>
    </div>

    <div class="log-section">
        <h3>📋 Main Logs</h3>
        <a href="build_summary.log" class="log-link">📊 Build Summary</a>
        <a href="build_progress.log" class="log-link">📈 Build Progress</a>
        <a href="package_summary.log" class="log-link">📦 Package Summary</a>
    </div>

    <div class="log-section">
        <h3>🚫 Errors & Issues</h3>
        <a href="errors/detailed_errors.log" class="log-link">🔥 Detailed Errors</a>
        <a href="errors/failed_imports.log" class="log-link">📥 Failed Imports</a>
    </div>

    <div class="log-section">
        <h3>⚠️ Warnings & Skipped</h3>
        <a href="warnings/all_warnings.log" class="log-link">⚠️ All Warnings</a>
        <a href="skipped/skipped_files.log" class="log-link">⏭️ Skipped Files</a>
    </div>

    <div class="log-section">
        <h3>📦 By Package</h3>""")

            for package in self.stats["package_stats"].keys():
                f.write(
                    f'        <a href="by_package/{package}_summary.log" class="log-link">📦 {package}</a>\n',
                )

            f.write("""    </div>
</body>
</html>""")


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
            f"=== AutoAPI Debugging Started at {datetime.now():%Y-%m-%d %H:%M:%S} ===",
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
                    f"[{timestamp}] Parsing: {rel_path}",
                    filepath=path,
                )

            try:
                result = _original_parse_file(self, path)
                if "/haive/packages/" in str(path):
                    debugger.log_success(str(path))
                return result
            except Exception as e:
                # Extract package for organized logging
                package = debugger._extract_package_name(str(path))

                # Check if this is a critical error that should stop the build
                is_critical = any(
                    critical in str(e).lower()
                    for critical in [
                        "syntaxerror",
                        "indentationerror",
                        "tabError",
                    ]
                )

                if is_critical:
                    # Log as error and re-raise to stop build
                    debugger.log_error(str(path), e, context="Parser.parse_file - CRITICAL")
                    debugger._update_package_stats(str(path), "failed")
                    raise
                # Log as warning and try to continue gracefully
                warning_msg = f"Parse failed (non-critical): {type(e).__name__}: {e!s}"
                debugger.log_warning(str(path), warning_msg, "Parser.parse_file - GRACEFUL")
                debugger.log_failed_import(package, str(path), e)
                debugger._update_package_stats(str(path), "skipped")

                # Return None to skip this file gracefully
                return None

        def debug_parse(self, node):
            """Wrapped parse method to track AST parsing."""
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            file_info = f" (file: {current_file['path']})" if current_file["path"] else ""
            debugger.logger.debug(
                f"[{timestamp}] Parsing AST node: {type(node).__name__}{file_info}",
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
                    file_path,
                    e,
                    context="Parser._parse_file (internal)",
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
                raise

        def debug_get_full_import_name(from_node, name):
            """Wrapped get_full_import_name with graceful error handling."""
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            try:
                module_file = getattr(from_node.root(), "file", "unknown")
                # Only log for project files - reduce verbosity
                if (
                    "/haive/packages/" in str(module_file)
                    and debugger.stats["total_files"] % 100 == 0
                ):
                    debugger.logger.debug(
                        f"[{timestamp}] Resolving import '{name}' in {module_file}",
                    )
                return _original_get_full_import_name(from_node, name)
            except Exception as e:
                module_file = getattr(
                    from_node.root(),
                    "file",
                    current_file.get("path", "unknown"),
                )

                # Extract package name for organized logging
                package = debugger._extract_package_name(str(module_file))

                # Log as failed import with package tracking
                debugger.log_failed_import(package, name, e)

                # Update package stats
                debugger._update_package_stats(str(module_file), "failed")

                # Log as warning instead of stopping build
                warning_msg = f"Import resolution failed: '{name}' - {type(e).__name__}: {e!s}"
                debugger.log_warning(str(module_file), warning_msg, "get_full_import_name")

                # Return a safe dummy value to continue processing gracefully
                return f"ERROR_IMPORT_{name}"

        def debug_load(self, patterns=None, dirs=None, **kwargs):
            """Wrapped load method to track overall progress and phases."""
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]

            debugger.log_progress(
                f"[{timestamp}] Starting AutoAPI load process - Dirs: {dirs}",
            )

            # Log directories being processed
            if dirs:
                for i, d in enumerate(dirs, 1):
                    rel_dir = str(d).replace(
                        "/home/will/Projects/haive/backend/haive/",
                        "",
                    )
                    debugger.log_progress(f"  Processing directory: {d}")

            # Track phases
            current_phase = {"phase": "INITIALIZATION", "start_time": datetime.now()}

            def update_phase(new_phase):
                elapsed = (datetime.now() - current_phase["start_time"]).total_seconds()
                timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                current_phase["phase"] = new_phase
                current_phase["start_time"] = datetime.now()
                debugger.log_progress(
                    f"PHASE CHANGE: {current_phase['phase']} -> {new_phase}",
                )

            files_processed = 0
            files_parsed = 0

            # Store original methods to intercept various phases
            (self.create_mapper if hasattr(self, "create_mapper") else None)
            (self.read_files if hasattr(self, "read_files") else None)
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
                            if isinstance(file_path, str | Path):
                                rel_path = str(file_path).replace(
                                    "/home/will/Projects/haive/backend/haive/",
                                    "",
                                )
                            else:
                                rel_path = str(file_path)
                            elapsed = (datetime.now() - discovery_start).total_seconds()

                        # Show every 10th file in debug log
                        if files_processed % 10 == 0:
                            debugger.log_progress(
                                f"[{current_phase['phase']}] File #{files_processed}: {file_path}",
                            )

                        yield file_path

                    # Log the last file processed before any error
                    if last_file:
                        debugger.log_progress(
                            f"[{current_phase['phase']}] Last file: {last_file}",
                        )
                        update_phase("FILE_PARSING")

                self.find_files = counting_find_files

                # Intercept parser methods to track parsing phase
                if hasattr(Parser, "parse_file"):
                    original_parser_parse = Parser.parse_file

                    def tracking_parse_file(parser_self, path):
                        nonlocal files_parsed
                        files_parsed += 1

                        if files_parsed == 1 and current_phase["phase"] != "FILE_PARSING":
                            update_phase("FILE_PARSING")

                        if files_parsed % 20 == 0:
                            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                            rel_path = str(path).replace(
                                "/home/will/Projects/haive/backend/haive/",
                                "",
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

                debugger.log_progress(
                    f"AutoAPI load completed - Discovered: {files_processed}, Parsed: {files_parsed}",
                )
                debugger.write_summary()
                return result

            except Exception:
                timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]

                debugger.log_progress(
                    f"AutoAPI FAILED in phase {current_phase['phase']} - Discovered: {
                        files_processed
                    }, Parsed: {files_parsed}",
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

        debugger.log_progress("AutoAPI debugging patches applied successfully")

    except ImportError:
        import traceback

        traceback.print_exc()


def configure_autoapi_debugging(app: Any) -> dict[str, Any]:
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
            "Preparing Jinja environment",
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
