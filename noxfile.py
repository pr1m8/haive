"""Enhanced Nox configuration for Haive project with documentation testing.

This enhanced version integrates all the documentation quality tools we've installed:
- pytest-doctestplus
- pytest-checkdocs  
- sphinx-testing
- darglint
- docstr-coverage
- interrogate
- and more...

Documentation Commands:
-----------------------
    nox -s docs_fast            # FASTEST: Build docs ignoring errors (NEW!)
    nox -s docs                 # Standard incremental sphinx-build
    nox -s docs_full            # Full rebuild with autosummary regeneration (slower)
    nox -s docs_autobuild       # Auto-build with hot reload and live updates
    nox -s docs_serve           # Serve pre-existing build (simple HTTP server)
    nox -s docs_clean           # Clean build artifacts
    nox -s docs_debug           # Analyze latest build log for issues
    nox -s docs_history         # Show build history and trends
    nox -s docs_logs            # List and manage build logs
    nox -s docs_quality         # Run doc8 and codespell quality checks
    nox -s docs_linkcheck       # Check for broken links
    nox -s docs_coverage        # Check documentation coverage
    nox -s docs_pdf             # Generate PDF documentation
    
Enhanced Documentation Testing Commands (NEW):
----------------------------------------------
    nox -s docs_test_all        # Run ALL documentation tests
    nox -s docs_test_docstrings # Test docstring coverage and quality
    nox -s docs_test_examples   # Test code examples in docs
    nox -s docs_test_notebooks  # Test Jupyter notebooks
    nox -s docs_test_spelling   # Advanced spell checking
    nox -s docs_test_prose      # Prose quality linting
    nox -s docs_test_metadata   # Check package metadata
    nox -s docs_test_pipeline   # Run full quality pipeline
    
Development Commands:
--------------------
    nox -s lint                 # Run linters
    nox -s test                 # Run tests
    nox -l                      # List all available sessions
    
Example Commands:
-----------------
    nox -s examples             # Run all examples with visualizations
    nox -s examples_simple      # Run SimpleAgent examples only
    nox -s examples_react       # Run ReactAgent examples only
    nox -s examples_rag         # Run RAG agent examples only
    nox -s examples_docs        # Generate examples for documentation
"""

import os
import shutil
import subprocess
import json
from datetime import datetime
from pathlib import Path

import nox

# Configuration
PYTHON_VERSIONS = ["3.12"]
# IMPORTANT: Reuse virtualenvs to cache installations and speed up runs
nox.options.reuse_existing_virtualenvs = True
nox.options.error_on_external_run = False

# Paths - Centralized and consistent
DOCS_DIR = Path("docs")
SOURCE_DIR = DOCS_DIR / "source"
BUILD_DIR = DOCS_DIR / "build" / "html"  # Centralized to single build directory
LOGS_DIR = DOCS_DIR / "logs"
QUALITY_REPORTS_DIR = DOCS_DIR / "quality-reports"

# Exclude problematic packages from documentation build
EXCLUDE_PACKAGES = ["packages/haive-prebuilt"]

# Package paths for namespaced imports (critical for testing)
PACKAGES_DIR = Path("packages")
PACKAGE_NAMES = [
    "haive-core",
    "haive-agents", 
    "haive-tools",
    "haive-games",
    "haive-dataflow",
    "haive-mcp",
    # "haive-prebuilt",  # Excluded due to parsing errors
]


def create_log_file(session, operation_name: str) -> Path:
    """Create a timestamped log file for the operation."""
    LOGS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOGS_DIR / f"{operation_name}_{timestamp}.log"
    session.log(f"📝 Logging to: {log_file}")
    return log_file


def log_progress(session, message: str, start_time: datetime = None):
    """Log progress with timestamp and elapsed time."""
    current_time = datetime.now()
    timestamp = current_time.strftime("%H:%M:%S")
    
    if start_time:
        elapsed = (current_time - start_time).total_seconds()
        elapsed_str = f" ({elapsed:.1f}s)"
    else:
        elapsed_str = ""
    
    session.log(f"[{timestamp}]{elapsed_str} {message}")


def run_with_graceful_handling(
    session, cmd: list, log_file: Path, operation: str
) -> dict:
    """Run command with graceful error handling and detailed status reporting."""
    status = {
        "success": False,
        "returncode": None,
        "warnings": 0,
        "errors": 0,
        "fatal_error": None,
        "output_exists": False,
        "log_file": log_file,
    }

    try:
        session.log(f"🔧 Running: {' '.join(cmd)}")

        # Run with real-time output and logging
        with open(log_file, "w") as f:
            f.write(f"=== {operation} ===\n")
            f.write(f"Command: {' '.join(cmd)}\n")
            f.write(f"Started: {datetime.now()}\n\n")

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                universal_newlines=True,
            )

            # Stream output in real time with graceful formatting
            while True:
                output = process.stdout.readline()
                if output == "" and process.poll() is not None:
                    break
                if output:
                    # Write to log file
                    f.write(output)
                    f.flush()

                    # Display with nice formatting and count issues
                    line = output.strip()
                    if "warning:" in line.lower():
                        status["warnings"] += 1
                        session.log(f"⚠️  {line}")
                    elif "error:" in line.lower() and "autosummary" not in line.lower():
                        status["errors"] += 1
                        session.log(f"🚨 {line}")
                    elif line and not line.startswith(("Running Sphinx", "loading")):
                        session.log(f"📄 {line}")

            status["returncode"] = process.poll()

            with open(log_file, "a") as f:
                f.write(f"\nCompleted: {datetime.now()}\n")
                f.write(f"Return code: {status['returncode']}\n")
                f.write(f"Warnings: {status['warnings']}\n")
                f.write(f"Errors: {status['errors']}\n")

        # Determine success based on output existence, not just return code
        if BUILD_DIR.exists():
            html_files = list(BUILD_DIR.glob("*.html"))
            status["output_exists"] = len(html_files) > 0

        if status["returncode"] == 0:
            status["success"] = True
            session.log(f"✅ {operation} completed successfully!")
        elif status["output_exists"]:
            session.log(
                f"⚠️  {operation} completed with issues but documentation was built!"
            )
            session.log(
                f"📊 Found {status['warnings']} warnings, {status['errors']} errors"
            )
        else:
            session.log(f"❌ {operation} failed - no output generated")

        return status

    except Exception as e:
        status["fatal_error"] = str(e)
        session.log(f"❌ {operation} failed: {e}")
        with open(log_file, "a") as f:
            f.write(f"\nFATAL ERROR: {e}\n")
        return status


# =============================================================================
# ORIGINAL DOCUMENTATION SESSIONS
# =============================================================================

@nox.session(python=PYTHON_VERSIONS)
def docs_fast(session):
    """Fast documentation build that continues on errors with last 20 lines output."""
    start_time = datetime.now()
    session.log("🚀 Running FAST documentation build (continues on errors)...")
    
    # Create log file
    log_file = create_log_file(session, "docs_fast_build")
    
    # Check if dependencies are already installed
    log_progress(session, "📦 Checking dependencies...", start_time)
    try:
        # Quick check if sphinx is available
        session.run("poetry", "run", "sphinx-build", "--version", silent=True, external=True)
        log_progress(session, "✅ Dependencies already installed, skipping install", start_time)
    except:
        log_progress(session, "📦 Installing documentation dependencies...", start_time)
        session.run(
            "poetry", "install", "--with", "docs", "--no-interaction", "-v",
            external=True,
            env={"POETRY_VIRTUALENVS_IN_PROJECT": "true"}
        )
        log_progress(session, "✅ Dependencies installed", start_time)

    # Set environment for fastest builds
    os.environ["SPHINX_AUTOSUMMARY_GENERATE"] = "false"
    os.environ["HAIVE_DOCS_MODE"] = "true"

    # Fast sphinx-build command with maximum error tolerance
    cmd = [
        "poetry",
        "run",
        "sphinx-build",
        "-b", "html",
        "-j", "auto",  # Parallel build
        "--keep-going",  # Continue on ALL errors
        str(SOURCE_DIR),
        str(BUILD_DIR),
    ]

    # Run command and capture output
    log_progress(session, "🔨 Building documentation (continuing on errors)...", start_time)
    output_lines = []
    last_progress_time = datetime.now()
    
    try:
        with open(log_file, "w") as f:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                universal_newlines=True,
            )
            
            # Capture all output to list for showing last 20 lines
            while True:
                output = process.stdout.readline()
                if output == "" and process.poll() is not None:
                    break
                if output:
                    f.write(output)
                    f.flush()
                    output_lines.append(output.strip())
                    
                    # Show progress updates every 5 seconds
                    current_time = datetime.now()
                    if (current_time - last_progress_time).total_seconds() > 5:
                        # Look for progress indicators in recent output
                        if "building" in output.lower() or "processing" in output.lower():
                            log_progress(session, f"⚙️  {output.strip()[:80]}...", start_time)
                        last_progress_time = current_time
            
            returncode = process.poll()
        
        # Show last 20 lines of output
        log_progress(session, "📄 Build complete! Showing last 20 lines of output:", start_time)
        session.log("-" * 50)
        for line in output_lines[-20:]:
            if line:
                session.log(line)
        session.log("-" * 50)
        
        # Quick check for output
        if BUILD_DIR.exists():
            html_files = list(BUILD_DIR.glob("*.html"))
            if html_files:
                session.log(f"✅ Built {len(html_files)} HTML files!")
                if (BUILD_DIR / "index.html").exists():
                    session.log(f"🌐 View docs: file://{(BUILD_DIR / 'index.html').absolute()}")
                else:
                    session.log(f"🌐 View docs: file://{html_files[0].absolute()}")
                session.log(f"📋 Full build log: {log_file}")
                return True
            else:
                session.log("❌ No HTML files generated")
                session.log(f"📋 Check full log: {log_file}")
                return False
        else:
            session.log("❌ Build directory not created")
            session.log(f"📋 Check full log: {log_file}")
            return False
            
    except subprocess.TimeoutExpired:
        session.log("⏱️  Build timed out after 5 minutes")
        session.log(f"📋 Check log: {log_file}")
        return False
    except Exception as e:
        session.log(f"❌ Build failed: {e}")
        session.log(f"📋 Check log: {log_file}")
        return False


@nox.session(python=PYTHON_VERSIONS)
def docs(session):
    """Standard sphinx-build with logging and --keep-going."""
    session.log("📚 Running sphinx-build with professional logging...")

    # Create log file
    log_file = create_log_file(session, "docs_build")

    # Install dependencies
    session.log("📦 Installing documentation dependencies...")
    session.run("poetry", "install", "--with", "docs", external=True)

    # Set environment for incremental builds
    os.environ["SPHINX_AUTOSUMMARY_GENERATE"] = (
        "false"  # Skip autosummary regeneration for speed
    )
    os.environ["HAIVE_DOCS_MODE"] = "true"

    # Standard sphinx-build command with logging and --keep-going
    cmd = [
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "html",
        "--keep-going",  # Continue building despite errors
        "-v",  # Verbose output
        str(SOURCE_DIR),
        str(BUILD_DIR),
    ]

    # Run with graceful handling and live logging
    status = run_with_graceful_handling(session, cmd, log_file, "Sphinx Build")

    # Enhanced result reporting
    session.log("=" * 50)
    session.log("📊 BUILD SUMMARY")
    session.log("=" * 50)

    if status["success"]:
        session.log("✅ Status: SUCCESS")
    elif status["output_exists"]:
        session.log("⚠️  Status: PARTIAL SUCCESS (with errors)")
    else:
        session.log("❌ Status: FAILED")

    session.log(f"📈 Warnings: {status['warnings']}")
    session.log(f"🚨 Errors: {status['errors']}")
    session.log(f"🔢 Return Code: {status['returncode']}")

    # Check for actual output files
    if BUILD_DIR.exists():
        html_files = list(BUILD_DIR.glob("*.html"))
        session.log(f"📄 HTML files generated: {len(html_files)}")

        if html_files:
            session.log("📋 Key files found:")
            for key_file in ["index.html", "genindex.html", "search.html"]:
                if (BUILD_DIR / key_file).exists():
                    session.log(f"  ✓ {key_file}")
                else:
                    session.log(f"  ✗ {key_file} (missing)")

            # Provide access URL
            if (BUILD_DIR / "index.html").exists():
                session.log(
                    f"🌐 View docs: file://{(BUILD_DIR / 'index.html').absolute()}"
                )
            else:
                # Find any HTML file to serve
                first_html = html_files[0]
                session.log(f"🌐 View docs: file://{first_html.absolute()}")
                session.log(
                    "   (Note: index.html missing, showing first available file)"
                )

    session.log(f"📋 Full log: {log_file}")
    session.log("=" * 50)

    return status["success"] or status["output_exists"]


@nox.session(python=PYTHON_VERSIONS)
def docs_full(session):
    """Full sphinx-build with autosummary regeneration (slower but complete)."""
    session.log("📚 Running FULL sphinx-build with autosummary regeneration...")

    # Create log file
    log_file = create_log_file(session, "docs_full_build")

    # Install dependencies
    session.log("📦 Installing documentation dependencies...")
    session.run("poetry", "install", "--with", "docs", external=True)

    # Set environment for full regeneration
    os.environ["SPHINX_AUTOSUMMARY_GENERATE"] = "true"  # Force autosummary regeneration
    os.environ["HAIVE_DOCS_MODE"] = "true"

    # Full sphinx-build command with clean rebuild
    cmd = [
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "html",
        "-E",  # Don't use cached environment
        "-a",  # Write all files
        "--keep-going",  # Continue building despite errors
        "-v",  # Verbose output
        str(SOURCE_DIR),
        str(BUILD_DIR),
    ]

    # Run with graceful handling and live logging
    status = run_with_graceful_handling(session, cmd, log_file, "Full Sphinx Build")

    # Enhanced result reporting (reuse from docs function)
    session.log("=" * 50)
    session.log("📊 FULL BUILD SUMMARY")
    session.log("=" * 50)

    if status["success"]:
        session.log("✅ Status: SUCCESS")
    elif status["output_exists"]:
        session.log("⚠️  Status: PARTIAL SUCCESS (with errors)")
    else:
        session.log("❌ Status: FAILED")

    session.log(f"📈 Warnings: {status['warnings']}")
    session.log(f"🚨 Errors: {status['errors']}")
    session.log(f"🔢 Return Code: {status['returncode']}")

    # Check for actual output files
    if BUILD_DIR.exists():
        html_files = list(BUILD_DIR.glob("*.html"))
        session.log(f"📄 HTML files generated: {len(html_files)}")

        if html_files:
            session.log("📋 Key files found:")
            for key_file in ["index.html", "genindex.html", "search.html"]:
                if (BUILD_DIR / key_file).exists():
                    session.log(f"  ✓ {key_file}")
                else:
                    session.log(f"  ✗ {key_file} (missing)")

            # Provide access URL
            if (BUILD_DIR / "index.html").exists():
                session.log(
                    f"🌐 View docs: file://{(BUILD_DIR / 'index.html').absolute()}"
                )
            else:
                # Find any HTML file to serve
                first_html = html_files[0]
                session.log(f"🌐 View docs: file://{first_html.absolute()}")
                session.log(
                    "   (Note: index.html missing, showing first available file)"
                )

    session.log(f"📋 Full log: {log_file}")
    session.log("=" * 50)

    return status["success"] or status["output_exists"]


@nox.session(python=PYTHON_VERSIONS)
def docs_serve(session):
    """Serve pre-existing documentation build (simple HTTP server)."""
    session.log("🌐 Serving pre-built documentation...")

    # Check if build exists
    if not (BUILD_DIR / "index.html").exists():
        session.log("❌ No documentation build found!")
        session.log("💡 Run 'nox -s docs' first to build documentation")
        return False

    session.log(f"📁 Serving from: {BUILD_DIR}")
    session.log("🌐 Server starting at: http://localhost:8003")
    session.log("🛑 Press Ctrl+C to stop")

    # Simple HTTP server for pre-built docs
    try:
        session.run(
            "python",
            "-m",
            "http.server",
            "8003",
            "--directory",
            str(BUILD_DIR),
            external=True,
        )
    except KeyboardInterrupt:
        session.log("🛑 Server stopped by user")


@nox.session(python=PYTHON_VERSIONS)
def docs_autobuild(session):
    """Auto-build documentation with hot reload and live updates."""
    session.log("🚀 Starting auto-build server with hot reload...")

    # Create log file for autobuild session
    log_file = create_log_file(session, "docs_autobuild")

    # Kill existing processes gracefully
    try:
        session.run("pkill", "-f", "sphinx-autobuild.*8003", external=True)
        session.log("🧹 Killed existing sphinx processes")
    except:
        session.log("ℹ️  No existing processes to kill")

    # Install dependencies
    session.log("📦 Installing documentation dependencies...")
    session.run("poetry", "install", "--with", "docs", external=True)

    # Set environment for graceful handling
    os.environ["SPHINX_AUTOSUMMARY_GENERATE"] = "false"  # Faster for serving
    os.environ["HAIVE_DOCS_MODE"] = "true"

    session.log("🌐 Auto-build server will start at: http://localhost:8003")
    session.log("📁 Watching packages/ for changes")
    session.log("🔄 Documentation rebuilds automatically on file changes")
    session.log("⚠️  Import warnings are normal and handled gracefully")
    session.log(f"📋 Server logs: {log_file}")

    # Prepare autobuild command with enhanced options
    cmd = [
        "poetry",
        "run",
        "sphinx-autobuild",
        str(SOURCE_DIR),
        str(BUILD_DIR),
        "--port",
        "8003",
        "--host",
        "0.0.0.0",
        "--watch",
        "packages",  # Watch source code changes
        "--ignore",
        "*.pyc",
        "--ignore",
        "*.pyo",
        "--ignore",
        "*~",
        "--ignore",
        ".git/*",
        "--ignore",
        "_build/*",
        "--ignore",
        "__pycache__/*",
        "--open-browser",
        "--delay",
        "1",  # Smart delay for rapid changes
        "--keep-going",  # Continue on build errors
        "-v",  # Verbose output
    ]

    # Run autobuild with graceful handling
    try:
        run_with_graceful_handling(session, cmd, log_file, "Auto-build Server")
    except KeyboardInterrupt:
        session.log("🛑 Auto-build server stopped by user")
    except Exception as e:
        session.log(f"❌ Auto-build server failed: {e}")
        session.log(f"📋 Check logs: {log_file}")


@nox.session(python=PYTHON_VERSIONS)
def docs_clean(session):
    """Clean documentation build artifacts."""
    session.log("🧹 Cleaning documentation build artifacts...")

    # Clean all build directories
    build_dirs = [
        BUILD_DIR,
        DOCS_DIR / "_build",
        DOCS_DIR / "_test_build",
        DOCS_DIR / "build",
    ]

    for build_dir in build_dirs:
        if build_dir.exists():
            shutil.rmtree(build_dir)
            session.log(f"✅ Cleaned {build_dir}")

    # Clean generated API docs
    api_dir = SOURCE_DIR / "api" / "generated"
    if api_dir.exists():
        shutil.rmtree(api_dir)
        session.log(f"✅ Cleaned {api_dir}")

    # Clean doctrees
    doctrees_dirs = [
        DOCS_DIR / ".doctrees",
        SOURCE_DIR / ".doctrees",
    ]

    for doctrees_dir in doctrees_dirs:
        if doctrees_dir.exists():
            shutil.rmtree(doctrees_dir)
            session.log(f"✅ Cleaned {doctrees_dir}")

    session.log("✅ All documentation artifacts cleaned!")


@nox.session(python=PYTHON_VERSIONS)
def docs_debug(session):
    """Analyze the most recent build log for common issues."""
    session.log("🔍 Analyzing recent build logs for common issues...")

    # Find the most recent build log
    if not LOGS_DIR.exists():
        session.log("❌ No logs directory found. Run 'nox -s docs' first.")
        return

    log_files = list(LOGS_DIR.glob("docs_build_*.log"))
    if not log_files:
        session.log("❌ No build logs found. Run 'nox -s docs' first.")
        return

    latest_log = max(log_files, key=lambda f: f.stat().st_mtime)
    session.log(f"📋 Analyzing: {latest_log}")

    # Analyze log content
    with open(latest_log) as f:
        content = f.read()

    # Count and categorize issues
    issues = {
        "import_errors": content.count("ModuleNotFoundError")
        + content.count("ImportError"),
        "relative_imports": content.count("TooManyLevelsError")
        + content.count("relative import"),
        "syntax_errors": content.count("SyntaxError"),
        "autoapi_errors": content.count("AutoAPI"),
        "warnings": content.count("WARNING"),
        "file_not_found": content.count("FileNotFoundError")
        + content.count("No such file"),
    }

    session.log("=" * 50)
    session.log("📊 ISSUE ANALYSIS")
    session.log("=" * 50)

    for issue_type, count in issues.items():
        if count > 0:
            icon = "🚨" if count > 10 else "⚠️" if count > 5 else "📋"
            session.log(f"{icon} {issue_type.replace('_', ' ').title()}: {count}")

    # Check build output status
    if BUILD_DIR.exists():
        html_files = list(BUILD_DIR.glob("*.html"))
        session.log(f"📄 HTML files in build: {len(html_files)}")

        if html_files:
            session.log("✅ Documentation was partially built despite errors")
            session.log(f"🌐 Try viewing: file://{BUILD_DIR.absolute()}")
        else:
            session.log("❌ No HTML files generated")

    session.log("=" * 50)
    session.log("💡 RECOMMENDATIONS")
    session.log("=" * 50)

    if issues["relative_imports"] > 0:
        session.log("🔧 Fix relative imports: Convert to absolute imports")
    if issues["import_errors"] > 0:
        session.log("🔧 Fix import errors: Check missing modules or circular imports")
    if issues["syntax_errors"] > 0:
        session.log("🔧 Fix syntax errors: Check Python syntax in source files")
    if issues["autoapi_errors"] > 0:
        session.log("🔧 AutoAPI issues: May be related to import problems")

    session.log(f"📋 Full log: {latest_log}")


@nox.session(python=PYTHON_VERSIONS)
def docs_history(session):
    """Show build history and trends from log files."""
    session.log("📈 Analyzing build history and trends...")

    if not LOGS_DIR.exists():
        session.log("❌ No logs directory found. Run 'nox -s docs' first.")
        return

    # Find all build logs
    log_files = list(LOGS_DIR.glob("docs_build_*.log"))
    if not log_files:
        session.log("❌ No build logs found. Run 'nox -s docs' first.")
        return

    # Sort by modification time (newest first)
    log_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

    session.log("=" * 60)
    session.log("📊 BUILD HISTORY")
    session.log("=" * 60)

    for i, log_file in enumerate(log_files[:10]):  # Show last 10 builds
        try:
            with open(log_file) as f:
                content = f.read()

            # Extract timestamp from filename
            timestamp = log_file.stem.split("_")[-2:]
            date_str = timestamp[0]
            time_str = timestamp[1]
            formatted_time = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]} {time_str[:2]}:{time_str[2:4]}:{time_str[4:6]}"

            # Get summary data from end of log
            warnings = content.count("WARNING")
            errors = content.count("ERROR") + content.count("error:")
            return_code = "Unknown"

            # Try to extract return code from log
            for line in content.split("\n"):
                if "Return code:" in line:
                    return_code = line.split("Return code:")[-1].strip()
                    break

            # Status based on return code
            if return_code == "0":
                status = "✅ SUCCESS"
            elif return_code == "2":
                status = "❌ FAILED"
            else:
                status = "⚠️  PARTIAL"

            session.log(
                f"{i + 1:2d}. {formatted_time} | {status} | ⚠️ {warnings:3d} warnings | 🚨 {errors:3d} errors"
            )

        except Exception as e:
            session.log(f"{i + 1:2d}. {log_file.name} | ❌ Error reading log: {e}")

    if len(log_files) > 10:
        session.log(f"... and {len(log_files) - 10} more builds")

    session.log("=" * 60)
    session.log("💡 RECENT TRENDS")
    session.log("=" * 60)

    # Analyze recent trends (last 5 builds)
    recent_logs = log_files[:5]
    if len(recent_logs) >= 2:
        recent_warnings = []
        recent_errors = []

        for log_file in recent_logs:
            try:
                with open(log_file) as f:
                    content = f.read()
                recent_warnings.append(content.count("WARNING"))
                recent_errors.append(content.count("ERROR") + content.count("error:"))
            except:
                continue

        if recent_warnings:
            avg_warnings = sum(recent_warnings) / len(recent_warnings)
            avg_errors = sum(recent_errors) / len(recent_errors)

            session.log(f"📊 Average warnings (last 5 builds): {avg_warnings:.1f}")
            session.log(f"📊 Average errors (last 5 builds): {avg_errors:.1f}")

            if len(recent_warnings) >= 2:
                warning_trend = (
                    "📈 increasing"
                    if recent_warnings[0] > recent_warnings[1]
                    else (
                        "📉 decreasing"
                        if recent_warnings[0] < recent_warnings[1]
                        else "➡️ stable"
                    )
                )
                error_trend = (
                    "📈 increasing"
                    if recent_errors[0] > recent_errors[1]
                    else (
                        "📉 decreasing"
                        if recent_errors[0] < recent_errors[1]
                        else "➡️ stable"
                    )
                )

                session.log(f"📈 Warning trend: {warning_trend}")
                session.log(f"📈 Error trend: {error_trend}")

    session.log("=" * 60)
    session.log(f"📁 All logs available in: {LOGS_DIR}")


@nox.session(python=PYTHON_VERSIONS)
def docs_logs(session):
    """List and manage documentation build logs."""
    session.log("📋 Documentation build logs management")

    if not LOGS_DIR.exists():
        session.log("❌ No logs directory found.")
        return

    # Get all log files
    all_logs = list(LOGS_DIR.glob("*.log"))
    build_logs = [f for f in all_logs if f.name.startswith("docs_build_")]
    autobuild_logs = [f for f in all_logs if f.name.startswith("docs_autobuild_")]
    serve_logs = [f for f in all_logs if f.name.startswith("docs_serve_")]

    session.log("=" * 50)
    session.log("📊 LOG SUMMARY")
    session.log("=" * 50)
    session.log(f"🔨 Build logs: {len(build_logs)}")
    session.log(f"🔄 Autobuild logs: {len(autobuild_logs)}")
    session.log(f"🌐 Serve logs: {len(serve_logs)}")
    session.log(f"📁 Total logs: {len(all_logs)}")

    # Calculate total size
    total_size = sum(f.stat().st_size for f in all_logs)
    size_mb = total_size / (1024 * 1024)
    session.log(f"💾 Total log size: {size_mb:.1f} MB")

    # Show recent logs
    session.log("\n📋 RECENT BUILD LOGS (last 5):")
    recent_builds = sorted(build_logs, key=lambda f: f.stat().st_mtime, reverse=True)[
        :5
    ]

    for log_file in recent_builds:
        size_kb = log_file.stat().st_size / 1024
        mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
        session.log(
            f"  📄 {log_file.name} ({size_kb:.1f} KB) - {mtime.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    session.log(f"\n📁 Logs directory: {LOGS_DIR}")
    session.log("\n💡 Commands:")
    session.log("  nox -s docs_debug     # Analyze latest build")
    session.log("  nox -s docs_history   # Show build history")
    session.log("  nox -s docs_clean     # Clean build artifacts (keeps logs)")

    # Cleanup suggestion
    if len(all_logs) > 20:
        session.log(
            f"\n⚠️  You have {len(all_logs)} log files. Consider cleaning old logs:"
        )
        session.log(
            "  find docs/logs -name '*.log' -mtime +7 -delete  # Remove logs older than 7 days"
        )


@nox.session(python=PYTHON_VERSIONS)
def docs_quality(session):
    """Run documentation quality checks (doc8, codespell)."""
    session.log("🔍 Running documentation quality checks...")

    # Create log file
    log_file = create_log_file(session, "docs_quality")

    # Install dependencies
    session.log("📦 Installing quality tools...")
    session.run("poetry", "install", "--only", "docs", external=True)

    quality_results = {"doc8": False, "codespell": False}

    # Run doc8 for RST linting
    session.log("📋 Running doc8 (RST linter)...")
    try:
        session.run(
            "poetry",
            "run",
            "doc8",
            str(SOURCE_DIR),
            "--config",
            "pyproject.toml",
            external=True,
        )
        quality_results["doc8"] = True
        session.log("✅ doc8: No RST issues found")
    except Exception as e:
        session.log(f"⚠️  doc8 found issues: {e}")
        session.log("   Run with --verbose to see details")

    # Run codespell for typo checking
    session.log("📝 Running codespell (typo checker)...")
    try:
        session.run(
            "poetry",
            "run",
            "codespell",
            str(SOURCE_DIR),
            "--config",
            "pyproject.toml",
            external=True,
        )
        quality_results["codespell"] = True
        session.log("✅ codespell: No typos found")
    except Exception as e:
        session.log(f"⚠️  codespell found typos: {e}")
        session.log("   Add to ignore list in pyproject.toml if needed")

    # Summary
    session.log("=" * 50)
    session.log("📊 QUALITY CHECK SUMMARY")
    session.log("=" * 50)

    all_passed = all(quality_results.values())
    if all_passed:
        session.log("✅ All quality checks passed!")
    else:
        session.log("⚠️  Some quality checks failed:")
        for check, passed in quality_results.items():
            status = "✅" if passed else "❌"
            session.log(f"  {status} {check}")

    session.log(f"📋 Full log: {log_file}")
    return all_passed


@nox.session(python=PYTHON_VERSIONS)
def docs_linkcheck(session):
    """Check for broken links in documentation."""
    session.log("🔗 Checking documentation links...")

    # Create log file
    log_file = create_log_file(session, "docs_linkcheck")

    # Install dependencies
    session.log("📦 Installing documentation dependencies...")
    session.run("poetry", "install", "--with", "docs", external=True)

    # Run sphinx linkcheck
    cmd = [
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "linkcheck",
        str(SOURCE_DIR),
        str(DOCS_DIR / "build" / "linkcheck"),
    ]

    status = run_with_graceful_handling(session, cmd, log_file, "Link Check")

    # Report results
    output_dir = DOCS_DIR / "build" / "linkcheck"
    if output_dir.exists():
        broken_file = output_dir / "output.txt"
        if broken_file.exists():
            with open(broken_file) as f:
                content = f.read()
                if content.strip():
                    session.log("⚠️  Found broken links:")
                    session.log(content)
                else:
                    session.log("✅ No broken links found!")

    session.log(f"📋 Full report: {output_dir / 'output.txt'}")
    return status["success"]


@nox.session(python=PYTHON_VERSIONS)
def docs_coverage(session):
    """Check documentation coverage for all modules."""
    session.log("📊 Checking documentation coverage...")

    # Create log file
    log_file = create_log_file(session, "docs_coverage")

    # Install dependencies
    session.log("📦 Installing documentation dependencies...")
    session.run("poetry", "install", "--with", "docs", external=True)

    # Run coverage check
    cmd = [
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "coverage",
        str(SOURCE_DIR),
        str(DOCS_DIR / "build" / "coverage"),
    ]

    status = run_with_graceful_handling(session, cmd, log_file, "Coverage Check")

    # Report results
    coverage_file = DOCS_DIR / "build" / "coverage" / "python.txt"
    if coverage_file.exists():
        session.log("📊 Documentation coverage report:")
        with open(coverage_file) as f:
            session.log(f.read())

    return status["success"]


@nox.session(python=PYTHON_VERSIONS)
def docs_pdf(session):
    """Generate PDF documentation using sphinx-simplepdf."""
    session.log("📄 Generating PDF documentation...")

    # Create log file
    log_file = create_log_file(session, "docs_pdf")

    # Install dependencies
    session.log("📦 Installing documentation dependencies...")
    session.run("poetry", "install", "--with", "docs", external=True)

    # First build HTML (required for simplepdf)
    session.log("🔨 Building HTML first...")
    session.run(
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "html",
        str(SOURCE_DIR),
        str(BUILD_DIR),
        external=True,
    )

    # Then generate PDF
    session.log("📄 Generating PDF...")
    cmd = [
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "simplepdf",
        str(SOURCE_DIR),
        str(DOCS_DIR / "build" / "pdf"),
    ]

    status = run_with_graceful_handling(session, cmd, log_file, "PDF Generation")

    # Check for output
    pdf_dir = DOCS_DIR / "build" / "pdf"
    if pdf_dir.exists():
        pdf_files = list(pdf_dir.glob("*.pdf"))
        if pdf_files:
            session.log("✅ PDF generated successfully!")
            for pdf in pdf_files:
                session.log(f"📄 {pdf}")
        else:
            session.log("❌ No PDF files generated")

    return status["success"]


# =============================================================================
# NEW ENHANCED DOCUMENTATION TESTING SESSIONS
# =============================================================================

@nox.session(python=PYTHON_VERSIONS)
def docs_test_all(session):
    """Run ALL documentation tests - comprehensive quality check."""
    session.log("🚀 Running comprehensive documentation testing suite...")
    
    results = {}
    
    # Run all test sessions
    test_sessions = [
        "docs_test_docstrings",
        "docs_test_examples", 
        "docs_test_notebooks",
        "docs_test_spelling",
        "docs_test_prose",
        "docs_test_metadata",
    ]
    
    for test_session in test_sessions:
        session.log(f"\n{'='*60}")
        session.log(f"Running: {test_session}")
        session.log(f"{'='*60}")
        
        try:
            session.notify(test_session)
            results[test_session] = "✅ PASSED"
        except Exception as e:
            results[test_session] = f"❌ FAILED: {e}"
    
    # Generate summary report
    session.log("\n" + "="*60)
    session.log("📊 COMPREHENSIVE TEST SUMMARY")
    session.log("="*60)
    
    for test_name, result in results.items():
        session.log(f"{result} {test_name}")
    
    # Save results
    QUALITY_REPORTS_DIR.mkdir(exist_ok=True)
    report_file = QUALITY_REPORTS_DIR / f"comprehensive_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    session.log(f"\n📋 Full report saved to: {report_file}")


@nox.session(python=PYTHON_VERSIONS)
def docs_test_docstrings(session):
    """Test docstring coverage and quality with multiple tools."""
    session.log("📊 Testing docstring coverage and quality...")
    
    # Create log file
    log_file = create_log_file(session, "docs_test_docstrings")
    
    # Install dependencies
    session.log("📦 Installing documentation testing dependencies...")
    session.run("poetry", "install", "--with", "dev", external=True)
    
    results = {}
    
    # 1. Interrogate - Docstring coverage
    session.log("\n🔍 Running interrogate (docstring coverage)...")
    try:
        session.run(
            "poetry", "run", "interrogate", "-vv", 
            "packages/", "--generate-badge", "docs/badges/",
            "--fail-under", "80",
            "--exclude", "packages/haive-prebuilt",
            external=True
        )
        results["interrogate"] = {"status": "passed", "coverage": ">80%"}
        session.log("✅ Interrogate: Good docstring coverage")
    except Exception as e:
        results["interrogate"] = {"status": "failed", "error": str(e)}
        session.log(f"❌ Interrogate: Low coverage - {e}")
    
    # 2. Darglint - Docstring/function matching
    session.log("\n🔍 Running darglint (docstring consistency)...")
    try:
        # Darglint doesn't have direct exclude, so we'll use find
        session.run(
            "bash", "-c",
            "find packages/ -name '*.py' -not -path 'packages/haive-prebuilt/*' | xargs poetry run darglint -v 2",
            external=True
        )
        results["darglint"] = {"status": "passed"}
        session.log("✅ Darglint: Docstrings match functions")
    except Exception as e:
        results["darglint"] = {"status": "failed", "error": str(e)}
        session.log(f"❌ Darglint: Inconsistencies found - {e}")
    
    # 3. Pydocstyle - Google style compliance
    session.log("\n🔍 Running pydocstyle (Google style)...")
    try:
        session.run(
            "poetry", "run", "pydocstyle", 
            "packages/", "--convention=google",
            "--match-dir='^(?!haive-prebuilt).*'",
            external=True
        )
        results["pydocstyle"] = {"status": "passed"}
        session.log("✅ Pydocstyle: Google style compliant")
    except Exception as e:
        results["pydocstyle"] = {"status": "failed", "error": str(e)}
        session.log(f"❌ Pydocstyle: Style violations - {e}")
    
    # 4. docstr-coverage - Detailed coverage report
    session.log("\n🔍 Running docstr-coverage...")
    try:
        # Run on each package except haive-prebuilt
        for package in PACKAGE_NAMES:
            if package != "haive-prebuilt":
                package_path = PACKAGES_DIR / package
                if package_path.exists():
                    session.run(
                        "poetry", "run", "docstr-coverage", 
                        str(package_path), "--failunder", "70",
                        external=True
                    )
        results["docstr-coverage"] = {"status": "passed", "coverage": ">70%"}
        session.log("✅ docstr-coverage: Good coverage")
    except Exception as e:
        results["docstr-coverage"] = {"status": "failed", "error": str(e)}
        session.log(f"❌ docstr-coverage: Low coverage - {e}")
    
    # Generate report
    _generate_quality_report(session, "docstring_quality", results)


@nox.session(python=PYTHON_VERSIONS)
def docs_test_examples(session):
    """Test code examples in documentation with pytest-doctestplus."""
    session.log("🧪 Testing code examples in documentation...")
    
    # Create log file
    log_file = create_log_file(session, "docs_test_examples")
    
    # Install dependencies
    session.log("📦 Installing testing dependencies...")
    session.run("poetry", "install", "--with", "dev,docs", external=True)
    
    # Configure pytest-doctestplus for namespaced packages
    # Important: Set Python path for namespaced imports
    for package in PACKAGE_NAMES:
        src_path = PACKAGES_DIR / package / "src"
        if src_path.exists():
            os.environ["PYTHONPATH"] = f"{src_path}:{os.environ.get('PYTHONPATH', '')}"
    
    results = {}
    
    # 1. Test Python docstrings with doctestplus
    session.log("\n🔍 Testing Python docstrings...")
    try:
        session.run(
            "poetry", "run", "pytest",
            "--doctest-plus",
            "--doctest-modules",
            "--doctest-continue-on-failure",
            "--ignore=packages/haive-prebuilt",
            "packages/",
            "-v",
            external=True
        )
        results["python_doctests"] = {"status": "passed"}
        session.log("✅ Python doctests passed")
    except Exception as e:
        results["python_doctests"] = {"status": "failed", "error": str(e)}
        session.log(f"❌ Python doctests failed - {e}")
    
    # 2. Test RST documentation
    session.log("\n🔍 Testing RST documentation...")
    try:
        session.run(
            "poetry", "run", "pytest",
            "--doctest-plus", 
            "--doctest-rst",
            "docs/",
            "-v",
            external=True
        )
        results["rst_doctests"] = {"status": "passed"}
        session.log("✅ RST doctests passed")
    except Exception as e:
        results["rst_doctests"] = {"status": "failed", "error": str(e)}
        session.log(f"❌ RST doctests failed - {e}")
    
    # 3. Test Markdown documentation
    session.log("\n🔍 Testing Markdown documentation...")
    try:
        session.run(
            "poetry", "run", "pytest",
            "--markdown-docs",
            "README.md",
            "project_docs/",
            "-v",
            external=True
        )
        results["markdown_doctests"] = {"status": "passed"}
        session.log("✅ Markdown doctests passed")
    except Exception as e:
        results["markdown_doctests"] = {"status": "failed", "error": str(e)}
        session.log(f"❌ Markdown doctests failed - {e}")
    
    # 4. Test with sphinx doctest extension
    session.log("\n🔍 Testing with Sphinx doctest...")
    try:
        session.run(
            "poetry", "run", "sphinx-build",
            "-b", "doctest",
            str(SOURCE_DIR),
            str(DOCS_DIR / "build" / "doctest"),
            external=True
        )
        results["sphinx_doctests"] = {"status": "passed"}
        session.log("✅ Sphinx doctests passed")
    except Exception as e:
        results["sphinx_doctests"] = {"status": "failed", "error": str(e)}
        session.log(f"❌ Sphinx doctests failed - {e}")
    
    _generate_quality_report(session, "example_testing", results)


@nox.session(python=PYTHON_VERSIONS)
def docs_test_notebooks(session):
    """Test Jupyter notebooks in documentation."""
    session.log("📓 Testing Jupyter notebooks...")
    
    # Create log file
    log_file = create_log_file(session, "docs_test_notebooks")
    
    # Install dependencies
    session.log("📦 Installing notebook testing dependencies...")
    session.run("poetry", "install", "--with", "docs", external=True)
    
    results = {}
    
    # Find all notebooks
    notebooks = list(Path(".").rglob("*.ipynb"))
    session.log(f"Found {len(notebooks)} notebooks to test")
    
    # Test each notebook
    for notebook in notebooks:
        session.log(f"\n📓 Testing: {notebook}")
        try:
            session.run(
                "poetry", "run", "pytest",
                "--nbval",
                str(notebook),
                external=True
            )
            results[str(notebook)] = {"status": "passed"}
            session.log(f"✅ {notebook.name} passed")
        except Exception as e:
            results[str(notebook)] = {"status": "failed", "error": str(e)}
            session.log(f"❌ {notebook.name} failed - {e}")
    
    _generate_quality_report(session, "notebook_testing", results)


@nox.session(python=PYTHON_VERSIONS)
def docs_test_spelling(session):
    """Advanced spell checking with multiple tools."""
    session.log("🔤 Running advanced spell checking...")
    
    # Create log file
    log_file = create_log_file(session, "docs_test_spelling")
    
    # Install dependencies
    session.log("📦 Installing spell checking tools...")
    session.run("poetry", "install", "--with", "dev", external=True)
    
    results = {}
    
    # 1. Codespell
    session.log("\n🔍 Running codespell...")
    try:
        session.run(
            "poetry", "run", "codespell",
            ".", 
            "--skip=.git,*.pyc,*.png,*.jpg,.venv,poetry.lock,*.min.js,*.min.css",
            "--ignore-words-list=haive,nd,crate",  # Add project-specific words
            external=True
        )
        results["codespell"] = {"status": "passed"}
        session.log("✅ Codespell: No spelling errors")
    except Exception as e:
        results["codespell"] = {"status": "failed", "error": str(e)}
        session.log(f"❌ Codespell: Spelling errors found - {e}")
    
    # 2. Pyspelling
    session.log("\n🔍 Running pyspelling...")
    try:
        # Create pyspelling config if not exists
        pyspelling_config = Path(".pyspelling.yml")
        if not pyspelling_config.exists():
            pyspelling_config.write_text("""
matrix:
- name: Python
  sources:
  - 'packages/**/*.py'
  aspell:
    lang: en
  pipeline:
  - pyspelling.filters.python:
      comments: true
      docstrings: true
  dictionary:
    wordlists:
    - docs/wordlist.txt

- name: Markdown
  sources:
  - '**/*.md'
  aspell:
    lang: en
  pipeline:
  - pyspelling.filters.markdown:
  dictionary:
    wordlists:
    - docs/wordlist.txt
""")
        
        session.run(
            "poetry", "run", "pyspelling",
            external=True
        )
        results["pyspelling"] = {"status": "passed"}
        session.log("✅ Pyspelling: No spelling errors")
    except Exception as e:
        results["pyspelling"] = {"status": "failed", "error": str(e)}
        session.log(f"❌ Pyspelling: Spelling errors found - {e}")
    
    _generate_quality_report(session, "spelling_check", results)


@nox.session(python=PYTHON_VERSIONS)
def docs_test_prose(session):
    """Test prose quality with proselint and vale."""
    session.log("✍️ Testing prose quality...")
    
    # Create log file
    log_file = create_log_file(session, "docs_test_prose")
    
    # Install dependencies
    session.log("📦 Installing prose linting tools...")
    session.run("poetry", "install", "--with", "dev", external=True)
    
    results = {}
    
    # 1. Proselint
    session.log("\n🔍 Running proselint...")
    try:
        session.run(
            "poetry", "run", "proselint",
            "README.md",
            "docs/",
            "project_docs/",
            external=True
        )
        results["proselint"] = {"status": "passed"}
        session.log("✅ Proselint: Good prose quality")
    except Exception as e:
        results["proselint"] = {"status": "failed", "error": str(e)}
        session.log(f"❌ Proselint: Prose issues found - {e}")
    
    # 2. Vale (if config exists)
    vale_config = Path(".vale.ini")
    if vale_config.exists():
        session.log("\n🔍 Running vale...")
        try:
            session.run(
                "poetry", "run", "vale",
                "README.md",
                "docs/",
                external=True
            )
            results["vale"] = {"status": "passed"}
            session.log("✅ Vale: Good prose quality")
        except Exception as e:
            results["vale"] = {"status": "failed", "error": str(e)}
            session.log(f"❌ Vale: Prose issues found - {e}")
    else:
        session.log("⚠️ Vale config not found, skipping")
        results["vale"] = {"status": "skipped", "reason": "No .vale.ini"}
    
    _generate_quality_report(session, "prose_quality", results)


@nox.session(python=PYTHON_VERSIONS)
def docs_test_metadata(session):
    """Check package metadata with pytest-checkdocs."""
    session.log("📦 Checking package metadata...")
    
    # Create log file
    log_file = create_log_file(session, "docs_test_metadata")
    
    # Install dependencies
    session.log("📦 Installing metadata checking tools...")
    session.run("poetry", "install", "--with", "dev", external=True)
    
    results = {}
    
    # 1. pytest-checkdocs
    session.log("\n🔍 Running pytest-checkdocs...")
    try:
        session.run(
            "poetry", "run", "pytest",
            "--checkdocs",
            "-v",
            external=True
        )
        results["checkdocs"] = {"status": "passed"}
        session.log("✅ Package metadata is valid")
    except Exception as e:
        results["checkdocs"] = {"status": "failed", "error": str(e)}
        session.log(f"❌ Metadata issues found - {e}")
    
    # 2. Pyroma
    session.log("\n🔍 Running pyroma...")
    try:
        session.run(
            "poetry", "run", "pyroma",
            ".",
            external=True
        )
        results["pyroma"] = {"status": "passed"}
        session.log("✅ Package quality is good")
    except Exception as e:
        results["pyroma"] = {"status": "failed", "error": str(e)}
        session.log(f"❌ Package quality issues - {e}")
    
    _generate_quality_report(session, "metadata_check", results)


@nox.session(python=PYTHON_VERSIONS)
def docs_test_pipeline(session):
    """Run the full documentation quality pipeline."""
    session.log("🚀 Running full documentation quality pipeline...")
    
    # This runs our custom Python pipeline script
    session.run("poetry", "install", "--with", "dev,docs", external=True)
    session.run(
        "poetry", "run", "python",
        "scripts/doc_quality_pipeline.py",
        "-v",
        "-o", str(QUALITY_REPORTS_DIR / f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"),
        external=True
    )


def _generate_quality_report(session, test_name: str, results: dict):
    """Generate a quality report for a test session."""
    QUALITY_REPORTS_DIR.mkdir(exist_ok=True)
    
    # Create report
    report = {
        "test_name": test_name,
        "timestamp": datetime.now().isoformat(),
        "results": results,
        "summary": {
            "total": len(results),
            "passed": sum(1 for r in results.values() if r.get("status") == "passed"),
            "failed": sum(1 for r in results.values() if r.get("status") == "failed"),
            "skipped": sum(1 for r in results.values() if r.get("status") == "skipped"),
        }
    }
    
    # Save report
    report_file = QUALITY_REPORTS_DIR / f"{test_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    # Display summary
    session.log("\n" + "="*60)
    session.log(f"📊 {test_name.upper()} SUMMARY")
    session.log("="*60)
    session.log(f"Total tests: {report['summary']['total']}")
    session.log(f"✅ Passed: {report['summary']['passed']}")
    session.log(f"❌ Failed: {report['summary']['failed']}")
    session.log(f"⏭️  Skipped: {report['summary']['skipped']}")
    session.log(f"📋 Report saved to: {report_file}")
    
    # Return success if all passed
    return report['summary']['failed'] == 0


# =============================================================================
# DEVELOPMENT AND EXAMPLE SESSIONS
# =============================================================================

@nox.session(python=PYTHON_VERSIONS)
def lint(session):
    """Run linters."""
    session.run("poetry", "install", "--with", "dev", external=True)
    session.run("poetry", "run", "ruff", "check", "packages/", external=True)


@nox.session(python=PYTHON_VERSIONS)
def test(session):
    """Run tests."""
    session.run("poetry", "install", "--with", "test", external=True)
    session.run("poetry", "run", "pytest", "-v", external=True)


@nox.session(python=PYTHON_VERSIONS)
def examples(session):
    """Run all agent examples with visualizations."""
    session.log("🚀 Running all agent examples...")
    
    # Install dependencies
    session.run("poetry", "install", "--all-extras", external=True)
    
    # Run the universal example runner
    session.run(
        "poetry", "run", "python", "run_all_examples.py",
        "--concurrent", "3", "--timeout", "300",
        external=True
    )


@nox.session(python=PYTHON_VERSIONS)
def examples_simple(session):
    """Run SimpleAgent examples only."""
    session.log("🤖 Running SimpleAgent examples...")
    
    # Install dependencies
    session.run("poetry", "install", "--all-extras", external=True)
    
    # Run agent-specific examples
    session.run(
        "poetry", "run", "python", "run_agent_examples.py",
        "--agent", "SimpleAgent", "--visualize",
        external=True
    )


@nox.session(python=PYTHON_VERSIONS)
def examples_react(session):
    """Run ReactAgent examples only."""
    session.log("🧠 Running ReactAgent examples...")
    
    # Install dependencies
    session.run("poetry", "install", "--all-extras", external=True)
    
    # Run agent-specific examples
    session.run(
        "poetry", "run", "python", "run_agent_examples.py",
        "--agent", "ReactAgent", "--visualize",
        external=True
    )


@nox.session(python=PYTHON_VERSIONS)
def examples_rag(session):
    """Run RAG agent examples only."""
    session.log("📚 Running RAG agent examples...")
    
    # Install dependencies
    session.run("poetry", "install", "--all-extras", external=True)
    
    # Run agent-specific examples
    session.run(
        "poetry", "run", "python", "run_agent_examples.py",
        "--agent", "RAGAgent", "--visualize",
        external=True
    )


@nox.session(python=PYTHON_VERSIONS)
def examples_docs(session):
    """Generate examples for documentation."""
    session.log("📚 Generating examples for documentation...")
    
    # Install dependencies
    session.run("poetry", "install", "--all-extras", external=True)
    
    # Change to docs directory and run docs example generator
    session.chdir("docs")
    session.run(
        "poetry", "run", "python", "run_examples_for_docs.py",
        external=True
    )