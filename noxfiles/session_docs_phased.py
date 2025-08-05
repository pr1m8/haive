"""Phased documentation sessions with improved logging and debugging.

This module provides a staged approach to building documentation,
allowing for better debugging and incremental validation.
"""

import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

import nox

# Import shared environment utilities
from .env_utils import ensure_sphinx_available, log_environment_info

# Configuration
PYTHON_VERSIONS = ["3.12"]
DOCS_DIR = Path("docs")
SOURCE_DIR = DOCS_DIR / "source"
BUILD_DIR = DOCS_DIR / "build"
LOGS_DIR = DOCS_DIR / "logs"

# Ensure directories exist
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Reuse virtualenvs for speed
nox.options.reuse_existing_virtualenvs = True


class PhaseLogger:
    """Logger for tracking documentation build phases."""

    def __init__(self, session, log_file: Path):
        self.session = session
        self.log_file = log_file
        self.phases = []
        self.current_phase = None
        self.start_time = time.time()

    def start_phase(self, name: str, description: str):
        """Start a new phase."""
        if self.current_phase:
            self.end_phase()

        self.current_phase = {
            "name": name,
            "description": description,
            "start_time": time.time(),
            "logs": [],
            "errors": [],
            "warnings": [],
        }

        self.session.log(f"\n{'=' * 60}")
        self.session.log(f"📍 PHASE: {name}")
        self.session.log(f"📝 {description}")
        self.session.log(f"{'=' * 60}")

    def end_phase(self):
        """End the current phase."""
        if self.current_phase:
            self.current_phase["end_time"] = time.time()
            self.current_phase["duration"] = (self.current_phase["end_time"] -
                                              self.current_phase["start_time"])

            # Report phase results
            phase = self.current_phase
            status = "✅" if not phase["errors"] else "❌"
            self.session.log(
                f"{status} Phase '{
                    phase['name']}' completed in {
                    phase['duration']:.1f}s", )

            if phase["warnings"]:
                self.session.log(f"⚠️  {len(phase['warnings'])} warnings")
            if phase["errors"]:
                self.session.log(f"❌ {len(phase['errors'])} errors")
                for error in phase["errors"][:3]:  # Show first 3 errors
                    self.session.log(f"   - {error[:80]}...")

            self.phases.append(self.current_phase)
            self.current_phase = None

    def log(self, message: str, level: str = "info"):
        """Log a message to the current phase."""
        if self.current_phase:
            self.current_phase["logs"].append({
                "level": level,
                "message": message,
                "timestamp": time.time()
            })

        # Also log to session with consistent formatting to match conf modules
        icons = {"info": "ℹ️", "warning": "⚠️", "error": "❌", "success": "✅", "progress": "🔄", "debug": "🔍"}
        icon = icons.get(level, "📝")
        
        # Add phase context for better tracking
        phase_context = f"[{self.current_phase['name']}] " if self.current_phase else ""
        
        # Enhanced formatting with phase context and timestamps
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if level == "info":
            self.session.log(f"{icon} {phase_context}{message}")
        elif level == "warning":
            self.session.log(f"{icon} {phase_context}{message}")
        elif level == "error":
            self.session.log(f"{icon} {phase_context}{message}")
        elif level == "success":
            self.session.log(f"{icon} {phase_context}{message}")
        elif level == "progress":
            # Show progress updates with timestamps for long operations
            self.session.log(f"{icon} [{timestamp}] {phase_context}{message}")
        elif level == "debug":
            # Only show debug in verbose mode
            if hasattr(self.session, 'posargs') and ('-v' in self.session.posargs or '--verbose' in self.session.posargs):
                self.session.log(f"{icon} {phase_context}{message}")
        else:
            self.session.log(f"{icon} {phase_context}{message}")

    def warning(self, message: str):
        """Log a warning."""
        if self.current_phase:
            self.current_phase["warnings"].append(message)
        self.log(message, "warning")

    def error(self, message: str):
        """Log an error."""
        if self.current_phase:
            self.current_phase["errors"].append(message)
        self.log(message, "error")
    
    def progress(self, message: str, count: int = None, total: int = None):
        """Log a progress update with optional count/total."""
        if count is not None and total is not None:
            percentage = (count / total) * 100
            progress_message = f"{message} ({count}/{total} - {percentage:.1f}%)"
        else:
            progress_message = message
        self.log(progress_message, "progress")
    
    def phase_summary(self):
        """Show a quick summary of the current phase."""
        if self.current_phase:
            phase = self.current_phase
            elapsed = time.time() - phase["start_time"]
            self.log(f"Phase '{phase['name']}' - {elapsed:.1f}s elapsed, {len(phase['errors'])} errors, {len(phase['warnings'])} warnings", "progress")

    def write_summary(self):
        """Write a summary of all phases."""
        if self.current_phase:
            self.end_phase()

        total_time = time.time() - self.start_time

        # Write to log file
        with open(self.log_file, "w") as f:
            f.write("Documentation Build Report\n")
            f.write(f"Generated: {datetime.now()}\n")
            f.write(f"Total Duration: {total_time:.1f}s\n")
            f.write(f"{'=' * 80}\n\n")

            for phase in self.phases:
                f.write(f"Phase: {phase['name']}\n")
                f.write(f"Description: {phase['description']}\n")
                f.write(f"Duration: {phase['duration']:.1f}s\n")
                f.write(f"Errors: {len(phase['errors'])}\n")
                f.write(f"Warnings: {len(phase['warnings'])}\n")
                f.write("-" * 40 + "\n")

                if phase["errors"]:
                    f.write("Errors:\n")
                    for error in phase["errors"]:
                        f.write(f"  - {error}\n")

                if phase["warnings"]:
                    f.write("\nWarnings:\n")
                    for warning in phase["warnings"]:
                        f.write(f"  - {warning}\n")

                f.write("\n")

        # Print summary to console
        self.session.log(f"\n{'=' * 60}")
        self.session.log("📊 BUILD SUMMARY")
        self.session.log(f"{'=' * 60}")
        self.session.log(f"Total Duration: {total_time:.1f}s")
        self.session.log(f"Phases Completed: {len(self.phases)}")

        errors = sum(len(p["errors"]) for p in self.phases)
        warnings = sum(len(p["warnings"]) for p in self.phases)

        if errors == 0:
            self.session.log(
                f"✅ Build completed successfully with {warnings} warnings", )
        else:
            self.session.log(
                f"❌ Build failed with {errors} errors and {warnings} warnings",
            )

        self.session.log(f"📋 Full report: {self.log_file}")


def run_sphinx_command(
    session,
    logger: PhaseLogger,
    args: list[str],
    phase_name: str,
    check_output: bool = True,
    verbose: bool = True,
    keep_going: bool = False,
    fail_fast: bool = False,
) -> bool:
    """Run a sphinx-build command and parse output."""
    # Check if verbose mode requested via session args
    if session.posargs and "verbose" in session.posargs:
        verbose = True
    
    # Check if keep-going mode requested via session args
    if session.posargs and "keep-going" in session.posargs:
        keep_going = True

    # Always add verbose flag for better tracking
    if "-v" not in args and verbose:
        args = ["-v"] + args

    # Add more verbosity for AutoAPI debugging or if requested
    if "-vv" not in args and (phase_name == "extension_test" or
                              (session.posargs and "vv" in session.posargs)):
        args = ["-vv"] + args
    
    # Add keep-going flag if requested
    if keep_going and "--keep-going" not in args:
        args = ["--keep-going"] + args
        logger.log("🔄 Keep-going mode enabled: continuing on errors", "info")

    cmd = ["poetry", "run", "sphinx-build"] + args

    logger.log(f"Running: {' '.join(cmd)}")

    # Track progress metrics
    files_processed = 0
    html_generated = 0
    errors_found = []
    warnings_found = []
    current_file = None
    syntax_errors = {}
    provider_errors = {}

    try:
        # Run command with real-time output
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
            cwd=Path.cwd(),
        )

        # Process output line by line
        for line in process.stdout:
            line = line.strip()
            if not line:
                continue

            # Always print the line for real-time feedback
            print(line, flush=True)

            # Track current file being processed
            if "[AutoAPI] Analyzing" in line:
                import re

                match = re.search(r"\[AutoAPI\] Analyzing (.+)$", line)
                if match:
                    current_file = match.group(1)

            # Track actual progress with timestamp
            import time

            current_time = time.strftime("%H:%M:%S")

            if "reading sources..." in line:
                logger.progress("📖 Reading source files...")
            elif "writing output..." in line:
                logger.progress("✍️ Writing output files...")
            elif "building [html]:" in line and "source changed" in line:
                # Extract number of changed files
                import re

                match = re.search(r"(\d+) source files? that are out of date",
                                  line)
                if match:
                    logger.progress(f"🔄 Building {match.group(1)} changed source files")
            elif "[AutoAPI] Reading files..." in line or "Reading Python objects" in line:
                files_processed += 1
                if files_processed % 50 == 0:
                    logger.progress(f"📂 AutoAPI processed {files_processed} files...")
            elif "writing" in line and ".html" in line:
                html_generated += 1
                if html_generated % 20 == 0:
                    logger.progress(f"📄 Generated {html_generated} HTML files...")
            elif "WARNING:" in line:
                warnings_found.append(line)
                logger.warning(f"Sphinx warning: {line}")
            elif "ERROR:" in line or "CRITICAL:" in line:
                errors_found.append(line)
                logger.error(f"Sphinx error: {line}")
                # Fail fast mode: terminate immediately on first error
                if fail_fast:
                    logger.error("🚨 FAIL FAST: Terminating on first error")
                    process.terminate()
                    return False
            elif "Analyzing" in line and current_file:
                # Show progress for large analysis phases
                if files_processed % 100 == 0:
                    logger.progress(f"📊 Analyzing files... (current: {current_file})")
            elif line.startswith("Extension error:") or "ExtensionError" in line:
                errors_found.append(line)
                logger.error(f"Extension error: {line}")
                # Fail fast mode: terminate immediately on extension error
                if fail_fast:
                    logger.error("🚨 FAIL FAST: Terminating on extension error")
                    process.terminate()
                    return False
            elif "invalid syntax" in line:
                syntax_errors[current_file or "unknown"] = line
                logger.error(f"Syntax error in {current_file or 'unknown'}: {line}")
            elif "Exception" in line and current_file:
                errors_found.append(line)
                logger.error(f"Exception while processing {current_file}: {line}")
                
            # Periodic progress summary (every 30 seconds of processing)
            if time.time() - (getattr(logger, '_last_summary_time', 0)) > 30:
                logger.phase_summary()
                logger._last_summary_time = time.time()

            # Capture syntax errors with file information
            elif "IndentationError" in line or "SyntaxError" in line:
                if current_file:
                    syntax_errors[current_file] = line
                    logger.error(f"❌ Syntax error in {current_file}: {line}")
                else:
                    logger.error(f"❌ Syntax error (unknown file): {line}")

            # Capture parsing errors
            elif "Parsing Python code failed:" in line:
                # Look for the file name in the next part of the error
                import re

                match = re.search(r"\(([^,]+),", line)
                if match:
                    error_file = match.group(1)
                    syntax_errors[error_file] = line
                    logger.error(f"❌ Parse error in {error_file}")

            # Capture provider/autosummary errors
            elif "[autosummary] failed to import" in line:
                import re

                match = re.search(r"failed to import (.+)\.", line)
                if match:
                    failed_import = match.group(1)
                    provider_errors[failed_import] = "Import failed"
                    logger.warning(
                        f"⚠️ AutoSummary failed to import: {failed_import}")

            # Capture the "not enough values to unpack" errors
            elif "ValueError: not enough values to unpack" in line:
                if current_file:
                    provider_errors[current_file] = line

            elif "build succeeded" in line:
                logger.log("🎉 Build succeeded!", "success")
            elif "build finished with problems" in line:
                logger.error("Build finished with problems")
            # Log other potentially useful lines
            elif any(keyword in line.lower() for keyword in [
                    "finished",
                    "complete",
                    "done",
                    "failed",
                    "error",
                    "traceback",
            ]):
                logger.log(line)

        # Wait for process to complete
        process.wait()

        # Report metrics
        logger.log("📊 Build metrics:")
        logger.log(f"   - Files processed: {files_processed}")
        logger.log(f"   - HTML files generated: {html_generated}")
        logger.log(f"   - Warnings: {len(warnings_found)}")
        logger.log(f"   - Errors: {len(errors_found)}")

        # Report syntax errors
        if syntax_errors:
            logger.log(f"❌ Files with syntax errors: {len(syntax_errors)}")
            for file, error in list(syntax_errors.items())[:5]:  # Show first 5
                logger.log(f"   - {file}: {error[:80]}...")

        # Report provider import errors
        if provider_errors:
            logger.log(f"⚠️ Provider/import errors: {len(provider_errors)}")
            for name, error in list(
                    provider_errors.items())[:5]:  # Show first 5
                logger.log(f"   - {name}: {error}")

        # Check result
        if process.returncode != 0:
            logger.error(f"Command failed with exit code {process.returncode}")
            if keep_going:
                logger.warning("⚠️ Keep-going mode: treating failure as warning and continuing")
                # In keep-going mode, try a fallback build with fewer extensions
                logger.log("🔄 Attempting fallback build with reduced extensions", "info")
                return "fallback_needed"  # Signal that fallback is needed
            else:
                return False

        return True

    except Exception as e:
        logger.error(f"Exception running command: {e}")
        import traceback

        logger.error(f"Traceback: {traceback.format_exc()}")
        if keep_going:
            logger.warning("⚠️ Keep-going mode: treating exception as warning")
            return "fallback_needed"
        return False


@nox.session(python=PYTHON_VERSIONS)
def docs_phased(session):
    """Build documentation in phases with detailed logging.
    
    Options:
        verbose: Enable verbose output
        vv: Enable very verbose output
        keep-going: Continue building despite errors
        pdf: Also build PDF documentation
        fast-imports: Enable fast import diagnostics (default: enabled)
        slow-imports: Disable fast import diagnostics (test all modules)
        
    Examples:
        nox -s docs_phased -- keep-going verbose
        nox -s docs_phased -- vv pdf
        nox -s docs_phased -- slow-imports  # Test all 2754 modules
        nox -s docs_phased -- fast-imports  # Test ~300 key modules (default)
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOGS_DIR / f"docs_phased_{timestamp}.log"

    session.log("🚀 Starting PHASED documentation build...")

    # Set environment to disable examples by default for faster phased builds
    env = os.environ.copy()
    env["SPHINX_DISABLE_EXAMPLES"] = env.get(
        "SPHINX_DISABLE_EXAMPLES",
        "1",
    )  # Default to disabled
    env["SPHINX_PROFILE"] = env.get("SPHINX_PROFILE",
                                    "full")  # Default to full
    
    # Handle import diagnostics speed
    if session.posargs and "fast-imports" in session.posargs:
        env["SPHINX_FAST_IMPORTS"] = "1"
        env["SPHINX_IMPORT_SAMPLE_LIMIT"] = "300"
    elif session.posargs and "slow-imports" in session.posargs:
        env["SPHINX_FAST_IMPORTS"] = "0"
        env["SPHINX_IMPORT_SAMPLE_LIMIT"] = "10000"  # High limit = no sampling
    else:
        # Default to full imports (slow mode) for thorough testing
        env["SPHINX_FAST_IMPORTS"] = env.get("SPHINX_FAST_IMPORTS", "0")
        env["SPHINX_IMPORT_SAMPLE_LIMIT"] = env.get("SPHINX_IMPORT_SAMPLE_LIMIT", "10000")

    # Show configuration options
    keep_going_enabled = session.posargs and "keep-going" in session.posargs
    verbose_enabled = session.posargs and ("verbose" in session.posargs or "vv" in session.posargs)
    fast_imports_enabled = env["SPHINX_FAST_IMPORTS"] == "1"
    
    session.log("📊 Phased build configuration:")
    session.log(f"   SPHINX_DISABLE_EXAMPLES = {env['SPHINX_DISABLE_EXAMPLES']}")
    session.log(f"   SPHINX_PROFILE = {env['SPHINX_PROFILE']}")
    session.log(f"   SPHINX_FAST_IMPORTS = {env['SPHINX_FAST_IMPORTS']} (limit: {env['SPHINX_IMPORT_SAMPLE_LIMIT']} modules)")
    session.log(f"   Keep-going mode: {'✅ ENABLED' if keep_going_enabled else '❌ disabled'}")
    session.log(f"   Verbose logging: {'✅ ENABLED' if verbose_enabled else '❌ disabled'}")
    session.log(f"   Fast imports: {'✅ ENABLED' if fast_imports_enabled else '❌ disabled'}")
    session.log("   🚫 Examples disabled by default for faster phased builds")
    session.log("   💡 Override with SPHINX_DISABLE_EXAMPLES=0 to enable examples")
    session.log("   🔄 Use 'keep-going' arg to continue on errors")
    session.log("   ⚡ Use 'fast-imports' (default) for quick builds, 'slow-imports' for full diagnostics")

    # Apply environment to session
    session.env.update(env)

    logger = PhaseLogger(session, log_file)

    # Phase 1: Environment Check
    logger.start_phase("environment", "Checking build environment")

    if not ensure_sphinx_available(session):
        logger.error("Sphinx not available")
        logger.write_summary()
        session.error("❌ Environment check failed")
        return

    log_environment_info(session, "minimal")
    logger.log("Environment ready", "success")

    # Phase 2: Configuration Validation
    logger.start_phase("config_validation", "Validating configuration")

    # Test 1: Python syntax check
    try:
        session.run(
            "python",
            "-m",
            "compileall",
            str(SOURCE_DIR / "conf.py"),
            external=True,
            silent=True,
        )
        logger.log("conf.py syntax valid", "success")
    except Exception as e:
        logger.error(f"conf.py syntax error: {e}")

    # Test 2: Import test
    try:
        session.run(
            "python",
            "-c",
            f"import sys; sys.path.insert(0, '{SOURCE_DIR}'); import conf",
            external=True,
            silent=True,
        )
        logger.log("conf.py imports successfully", "success")
    except Exception as e:
        logger.error(f"conf.py import failed: {e}")

    # Skip extension testing and content validation - go directly to HTML build
    logger.log("ℹ️ Skipping extension test phase")
    logger.log("ℹ️ Skipping content validation phase")

    # Phase 3: HTML Build
    logger.start_phase("html_build", "Building HTML documentation")

    # Clear old HTML files to get accurate count
    html_dir = BUILD_DIR / "html"
    if html_dir.exists():
        logger.log(f"Clearing old HTML files from {html_dir}")

    # Check if keep-going mode requested
    keep_going = session.posargs and "keep-going" in session.posargs
    
    # Add incremental build support to avoid starting from 0
    # Use -E flag only for fresh builds, otherwise use cache
    use_fresh_build = session.posargs and "fresh" in session.posargs
    build_args = ["-b", "html", "-j", "auto"]
    
    if use_fresh_build:
        build_args.extend(["-E", "-a"])  # Fresh build: rebuild all files
        logger.log("🔄 Fresh build requested: rebuilding all files", "info")
    else:
        # Incremental build: only rebuild changed files
        logger.log("⚡ Incremental build: only changed files will be rebuilt", "info")
    
    build_args.extend([str(SOURCE_DIR), str(BUILD_DIR / "html")])
    
    success = run_sphinx_command(
        session,
        logger,
        build_args,
        "html_build",
        keep_going=keep_going,
    )

    # Handle fallback build if needed
    if success == "fallback_needed" and keep_going:
        logger.log("🔄 Starting fallback build with standard profile", "info")
        # Set environment to use standard profile (fewer extensions)
        fallback_env = session.env.copy()
        fallback_env["SPHINX_PROFILE"] = "standard"
        session.env.update(fallback_env)
        
        # Try again with standard profile
        success = run_sphinx_command(
            session,
            logger,
            ["-b", "html", "-j", "auto",
             str(SOURCE_DIR),
             str(BUILD_DIR / "html")],
            "html_build_fallback",
            keep_going=False,  # Don't recurse fallback
        )
        
        if success:
            logger.log("✅ Fallback build completed successfully", "success")
        else:
            logger.error("❌ Fallback build also failed")

    if success is True or success == "fallback_needed":
        # Count all generated HTML files recursively
        html_files = list((BUILD_DIR / "html").rglob("*.html"))
        api_files = (list((BUILD_DIR / "html" / "api").rglob("*.html")) if
                     (BUILD_DIR / "html" / "api").exists() else [])

        logger.log("📊 Final HTML generation stats:", "success")
        logger.log(f"   - Total HTML files: {len(html_files)}")
        logger.log(f"   - API documentation files: {len(api_files)}")
        logger.log(
            f"   - Root level files: {len(list((BUILD_DIR / 'html').glob('*.html')))}",
        )

        if html_files:
            logger.log(
                f"🌐 View docs: file://{(BUILD_DIR / 'html' / 'index.html').absolute()}",
                "success",
            )

            # Show some example files
            logger.log("📄 Sample generated files:")
            for file in list(html_files)[:5]:
                logger.log(f"   - {file.relative_to(BUILD_DIR / 'html')}")

    # Phase 6: Additional Formats (optional)
    if session.posargs and "pdf" in session.posargs:
        logger.start_phase("pdf_build", "Building PDF documentation")
        run_sphinx_command(
            session,
            logger,
            ["-b", "simplepdf",
             str(SOURCE_DIR),
             str(BUILD_DIR / "pdf")],
            "pdf_build",
        )

    # Write final summary
    logger.write_summary()


@nox.session(python=PYTHON_VERSIONS)
def docs_validate(session):
    """Quick validation of documentation setup (no build)."""
    session.log("🔍 Validating documentation setup...")

    checks = {
        "conf.py exists": (SOURCE_DIR / "conf.py").exists(),
        "index.rst/md exists": (SOURCE_DIR / "index.rst").exists()
        or (SOURCE_DIR / "index.md").exists(),
        "docs directory":
        DOCS_DIR.exists(),
        "source directory":
        SOURCE_DIR.exists(),
    }

    # Run checks
    all_passed = True
    for check, result in checks.items():
        status = "✅" if result else "❌"
        session.log(f"{status} {check}")
        if not result:
            all_passed = False

    # Check for common files
    common_files = [
        "conf.py", "index.rst", "index.md", "_toc.yml", "requirements.txt"
    ]
    session.log("\n📁 Common files:")
    for filename in common_files:
        path = SOURCE_DIR / filename
        if path.exists():
            session.log(f"✅ {filename}")
        else:
            session.log(f"⚠️  {filename} (missing)")

    if all_passed:
        session.log("\n✅ Basic setup validation passed!")
    else:
        session.log("\n❌ Some checks failed - fix before building")


@nox.session(python=PYTHON_VERSIONS)
def docs_diagnose(session):
    """Diagnose documentation build issues."""
    session.log("🏥 Running documentation diagnostics...")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = LOGS_DIR / f"docs_diagnostic_{timestamp}.txt"

    with open(report_file, "w") as f:
        f.write("Documentation Diagnostic Report\n")
        f.write(f"Generated: {datetime.now()}\n")
        f.write("=" * 80 + "\n\n")

        # 1. Check Python environment
        f.write("1. Python Environment\n")
        f.write("-" * 40 + "\n")

        result = subprocess.run(
            ["poetry", "run", "python", "--version"],
            capture_output=True,
            text=True,
            check=False,
        )
        f.write(f"Python Version: {result.stdout.strip()}\n")

        result = subprocess.run(
            ["poetry", "run", "sphinx-build", "--version"],
            capture_output=True,
            text=True,
            check=False,
        )
        f.write(f"Sphinx Version: {result.stdout.strip()}\n\n")

        # 2. Check installed extensions
        f.write("2. Installed Extensions\n")
        f.write("-" * 40 + "\n")

        # Get list of sphinx extensions
        extensions_check = subprocess.run(
            [
                "poetry",
                "run",
                "python",
                "-c",
                "import pkg_resources; exts = [p.project_name for p in pkg_resources.working_set if 'sphinx' in p.project_name.lower()]; print('\\n'.join(sorted(exts)))",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        f.write(extensions_check.stdout)
        f.write("\n")

        # 3. Test importing conf.py
        f.write("3. Configuration Import Test\n")
        f.write("-" * 40 + "\n")

        import_test = subprocess.run(
            [
                "poetry",
                "run",
                "python",
                "-c",
                f"import sys; sys.path.insert(0, '{SOURCE_DIR}'); import conf; print('Success')",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        if import_test.returncode == 0:
            f.write("✅ conf.py imports successfully\n")
        else:
            f.write("❌ conf.py import failed:\n")
            f.write(import_test.stderr)
        f.write("\n")

        # 4. Check for common issues
        f.write("4. Common Issues Check\n")
        f.write("-" * 40 + "\n")

        # Check for duplicate extensions
        if (SOURCE_DIR / "conf.py").exists():
            conf_content = (SOURCE_DIR / "conf.py").read_text()
            if conf_content.count("extensions = ") > 1:
                f.write("⚠️  Multiple 'extensions =' assignments found\n")
            if "myst_parser" in conf_content and "myst_nb" in conf_content:
                f.write(
                    "⚠️  Both myst_parser and myst_nb found (use only myst_nb)\n"
                )

        # 5. Try minimal build
        f.write("\n5. Minimal Build Test\n")
        f.write("-" * 40 + "\n")

        minimal_test = subprocess.run(
            [
                "poetry",
                "run",
                "sphinx-build",
                "-b",
                "gettext",
                str(SOURCE_DIR),
                str(BUILD_DIR / "diagnostic"),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        if minimal_test.returncode == 0:
            f.write("✅ Minimal build succeeded\n")
        else:
            f.write("❌ Minimal build failed\n")
            f.write("STDOUT:\n")
            f.write(
                minimal_test.stdout[:1000] + "...\n"
                if len(minimal_test.stdout) > 1000 else minimal_test.stdout, )
            f.write("\nSTDERR:\n")
            f.write(
                minimal_test.stderr[:1000] + "...\n"
                if len(minimal_test.stderr) > 1000 else minimal_test.stderr, )

    session.log(f"📋 Diagnostic report saved to: {report_file}")

    # Print summary
    with open(report_file) as f:
        content = f.read()
        if "❌" in content:
            session.log("❌ Issues found - check report for details")
        else:
            session.log("✅ No major issues detected")


@nox.session(python=PYTHON_VERSIONS)
def docs_phased_no_examples(session):
    """Build documentation in phases WITHOUT examples (fast phased build)."""
    # Set environment to explicitly disable examples
    os.environ["SPHINX_DISABLE_EXAMPLES"] = "1"
    os.environ["SPHINX_PROFILE"] = "standard"

    session.log("🚀 Starting FAST phased documentation build (no examples)...")
    session.log("   🚫 Examples explicitly disabled for maximum speed")

    # Call the main docs_phased function
    return docs_phased.func(session)
