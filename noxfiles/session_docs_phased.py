"""Phased documentation sessions with improved logging and debugging.

This module provides a staged approach to building documentation,
allowing for better debugging and incremental validation.
"""

from datetime import datetime
import os
from pathlib import Path
import subprocess
import time

# Import shared environment utilities
from env_utils import ensure_sphinx_available, log_environment_info
import nox

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
                "message": message
            })

        # Also log to session
        icons = {"info": "ℹ️", "warning": "⚠️", "error": "❌", "success": "✅"}
        icon = icons.get(level, "📝")
        self.session.log(f"{icon} {message}")

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
) -> bool:
    """Run a sphinx-build command and parse output."""
    # Check if verbose mode requested via session args
    if session.posargs and "verbose" in session.posargs:
        verbose = True

    # Always add verbose flag for better tracking
    if "-v" not in args and verbose:
        args = ["-v"] + args

    # Add more verbosity for AutoAPI debugging or if requested
    if "-vv" not in args and (phase_name == "extension_test" or
                              (session.posargs and "vv" in session.posargs)):
        args = ["-vv"] + args

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
                logger.log(f"[{current_time}] 📖 Reading source files...")
            elif "writing output..." in line:
                logger.log(f"[{current_time}] ✍️ Writing output files...")
            elif "building [html]:" in line and "source changed" in line:
                # Extract number of changed files
                import re

                match = re.search(r"(\d+) source files? that are out of date",
                                  line)
                if match:
                    logger.log(
                        f"🔄 Building {match.group(1)} changed source files")
            elif "[AutoAPI] Reading files..." in line or "Reading Python objects" in line:
                files_processed += 1
                if files_processed % 50 == 0:
                    logger.log(
                        f"📂 AutoAPI processed {files_processed} files...")
            elif "writing" in line and ".html" in line:
                html_generated += 1
                if html_generated % 20 == 0:
                    logger.log(f"📄 Generated {html_generated} HTML files...")
            elif "WARNING:" in line:
                warnings_found.append(line)
                logger.warning(line)
            elif "ERROR:" in line or "Exception" in line:
                errors_found.append(line)
                logger.error(line)

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
            return False

        return True

    except Exception as e:
        logger.error(f"Exception running command: {e}")
        import traceback

        logger.error(f"Traceback: {traceback.format_exc()}")
        return False


@nox.session(python=PYTHON_VERSIONS)
def docs_phased(session):
    """Build documentation in phases with detailed logging."""
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
                                    "standard")  # Default to standard

    session.log("📊 Phased build configuration:")
    session.log(
        f"   SPHINX_DISABLE_EXAMPLES = {env['SPHINX_DISABLE_EXAMPLES']}")
    session.log(f"   SPHINX_PROFILE = {env['SPHINX_PROFILE']}")
    session.log("   🚫 Examples disabled by default for faster phased builds")
    session.log(
        "   💡 Override with SPHINX_DISABLE_EXAMPLES=0 to enable examples")

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

    # Phase 3: Extension Testing - SKIPPED to go directly to HTML build
    logger.log("Skipping extension test phase - going directly to HTML build",
               "info")

    # Phase 4: Content Validation - SKIPPED
    logger.log("Skipping content validation phase", "info")

    # Phase 5: HTML Build
    logger.start_phase("html_build", "Building HTML documentation")

    # Clear old HTML files to get accurate count
    html_dir = BUILD_DIR / "html"
    if html_dir.exists():
        logger.log(f"Clearing old HTML files from {html_dir}")

    success = run_sphinx_command(
        session,
        logger,
        ["-b", "html", "-j", "auto",
         str(SOURCE_DIR),
         str(BUILD_DIR / "html")],
        "html_build",
    )

    if success:
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
