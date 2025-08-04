"""Documentation sessions for Haive."""

import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

import nox

# Import shared environment utilities
from .env_utils import ensure_sphinx_available

# Configuration
PYTHON_VERSIONS = ["3.12"]
DOCS_DIR = Path("docs")
SOURCE_DIR = DOCS_DIR / "source"
BUILD_DIR = DOCS_DIR / "build" / "html"
LOGS_DIR = DOCS_DIR / "logs"
QUALITY_REPORTS_DIR = DOCS_DIR / "quality-reports"
PACKAGES_DIR = Path("packages")
PACKAGE_NAMES = [
    "haive-core",
    "haive-agents",
    "haive-tools",
    "haive-games",
    "haive-dataflow",
    "haive-mcp",
]

# Ensure directories exist
LOGS_DIR.mkdir(parents=True, exist_ok=True)
QUALITY_REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Reuse virtualenvs for speed
nox.options.reuse_existing_virtualenvs = True


def create_log_file(session, operation_name: str) -> Path:
    """Create a timestamped log file for the operation."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOGS_DIR / f"{operation_name}_{timestamp}.log"
    session.log(f"📝 Logging to: {log_file}")
    return log_file


def run_with_graceful_handling(
    session,
    cmd: list,
    log_file: Path,
    operation: str,
) -> dict:
    """Run command with proper error detection and detailed logging."""
    status = {
        "success": False,
        "warnings": 0,
        "errors": 0,
        "exit_code": None,
        "files_built": 0,
        "sphinx_errors": [],
        "output_lines": [],
    }

    try:
        session.log(f"🔧 Running: {' '.join(cmd)}")

        # Key patterns to detect in sphinx output
        error_patterns = [
            "error:",
            "exception:",
            "traceback",
            "fatal:",
            "failed:",
            "valueerror:",
            "attributeerror:",
            "importerror:",
            "modulenotfounderror:",
        ]

        warning_patterns = [
            "warning:",
            "warn:",
            "deprecated:",
        ]

        success_patterns = [
            "build succeeded",
            "pages written",
            "build finished",
        ]

        with open(log_file, "w") as f:
            f.write(f"=== {operation} ===\n")
            f.write(f"Command: {' '.join(cmd)}\n")
            f.write(f"Started: {datetime.now()}\n")
            f.write("=" * 80 + "\n\n")

            # Run with captured output
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                universal_newlines=True,
            )

            # Capture both stdout and stderr
            stdout_lines = []
            stderr_lines = []

            # Read stdout
            for line in process.stdout:
                stdout_lines.append(line)
                f.write(f"[STDOUT] {line}")
                f.flush()

                line_lower = line.lower().strip()
                status["output_lines"].append(line.strip())

                # Check for errors
                for pattern in error_patterns:
                    if pattern in line_lower:
                        status["errors"] += 1
                        status["sphinx_errors"].append(line.strip())
                        break

                # Check for warnings
                for pattern in warning_patterns:
                    if pattern in line_lower:
                        status["warnings"] += 1
                        break

                # Check for success indicators
                for pattern in success_patterns:
                    if pattern in line_lower:
                        # Extract number of files built if possible
                        import re

                        match = re.search(
                            r"(\d+)\s+(source files?|pages?|files?)\s+(written|built)",
                            line_lower,
                        )
                        if match:
                            status["files_built"] = int(match.group(1))

            # Read stderr
            for line in process.stderr:
                stderr_lines.append(line)
                f.write(f"[STDERR] {line}")
                f.flush()

                line_lower = line.lower().strip()
                # stderr often contains errors
                if line.strip():
                    status["errors"] += 1
                    status["sphinx_errors"].append(f"[STDERR] {line.strip()}")

            # Wait for process to complete
            exit_code = process.wait()
            status["exit_code"] = exit_code

            # Determine success based on exit code AND error detection
            # sphinx-build should return 0 on success, non-zero on failure
            if exit_code == 0 and status["errors"] == 0:
                status["success"] = True
            else:
                status["success"] = False

            f.write("\n" + "=" * 80 + "\n")
            f.write(f"Completed: {datetime.now()}\n")
            f.write(f"Exit Code: {exit_code}\n")
            f.write(f"Success: {status['success']}\n")
            f.write(f"Files Built: {status['files_built']}\n")
            f.write(f"Warnings: {status['warnings']}\n")
            f.write(f"Errors: {status['errors']}\n")

            if status["sphinx_errors"]:
                f.write("\nDetected Errors:\n")
                for error in status["sphinx_errors"]:
                    f.write(f"  - {error}\n")

        # Report results
        if status["success"] and status["files_built"] > 0:
            session.log(f"✅ {operation} completed successfully!")
            session.log(f"📄 Built {status['files_built']} files")
        elif status["exit_code"] == 0 and status["errors"] > 0:
            session.log(
                f"⚠️  {operation} completed with errors (sphinx didn't report failure)",
            )
            session.log(f"❌ Found {status['errors']} errors in output")
        else:
            session.log(
                f"❌ {operation} failed with exit code: {status['exit_code']}")

        session.log(
            f"📊 Warnings: {
                status['warnings']}, Errors: {
                status['errors']}, Files: {
                status['files_built']}",
        )

        # Show last few errors if any
        if status["sphinx_errors"] and len(status["sphinx_errors"]) > 0:
            session.log("🔴 Recent errors:")
            for error in status["sphinx_errors"][-3:]:  # Show last 3 errors
                session.log(f"   {error[:100]}...")

        return status

    except Exception as e:
        session.log(f"❌ {operation} failed with exception: {e}")
        status["errors"] += 1
        return status


@nox.session(python=PYTHON_VERSIONS)
def docs_fast(session):
    """Fast documentation build that continues on errors."""
    start_time = datetime.now()
    session.log("🚀 Running FAST documentation build (continues on errors)...")

    log_file = create_log_file(session, "docs_fast_build")

    # Ensure dependencies are ready using shared utilities
    if not ensure_sphinx_available(session):
        session.error("❌ Could not prepare Sphinx for documentation build")
        return

    # Fast build command
    cmd = [
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "html",
        "-j",
        "auto",  # Parallel
        "--keep-going",  # Continue on errors
        str(SOURCE_DIR),
        str(BUILD_DIR),
    ]

    # Run build with improved error handling
    status = run_with_graceful_handling(session, cmd, log_file,
                                        "Fast Sphinx Build")

    # Check actual results on disk
    if BUILD_DIR.exists():
        html_files = list(BUILD_DIR.glob("*.html"))
        actual_files_count = len(html_files)
    else:
        actual_files_count = 0

    # Report comprehensive results
    if status["success"] and actual_files_count > 0:
        session.log("✅ Build completed successfully!")
        session.log(f"📄 Found {actual_files_count} HTML files on disk")
        session.log(f"🌐 View docs: file://{BUILD_DIR.absolute()}/index.html")
    elif status["exit_code"] == 0 and status["errors"] > 0:
        session.log("⚠️  Build reported success but errors were detected!")
        session.log(
            f"📄 Found {actual_files_count} HTML files on disk (may be incomplete)",
        )
        if actual_files_count > 0:
            session.log(
                f"🌐 View docs (with caution): file://{BUILD_DIR.absolute()}/index.html",
            )
    else:
        session.log("❌ Build failed!")
        session.log(f"📄 Only {actual_files_count} HTML files were generated")

    # Show log file location for debugging
    session.log(f"📋 Full build log: {log_file}")

    elapsed = (datetime.now() - start_time).total_seconds()
    session.log(f"⏱️  Build completed in {elapsed:.1f}s")


@nox.session(python=PYTHON_VERSIONS)
def docs(session):
    """Standard sphinx-build with logging and --keep-going."""
    session.log("📚 Running standard documentation build...")

    log_file = create_log_file(session, "docs_build")

    # Install dependencies
    session.log("📦 Installing documentation dependencies...")
    session.run("poetry", "install", "--with", "docs", external=True)

    # Build command
    cmd = [
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "html",
        "--keep-going",
        "-v",
        str(SOURCE_DIR),
        str(BUILD_DIR),
    ]

    # Run with logging
    run_with_graceful_handling(session, cmd, log_file, "Sphinx Build")


@nox.session(python=PYTHON_VERSIONS)
def docs_full(session):
    """Full sphinx-build with autosummary regeneration (slower but
    complete)."""
    session.log("📚 Running FULL documentation build...")

    log_file = create_log_file(session, "docs_full_build")

    # Install dependencies
    session.run("poetry", "install", "--with", "docs", external=True)

    # Set environment for full regeneration
    os.environ["SPHINX_AUTOSUMMARY_GENERATE"] = "true"

    # Full build command
    cmd = [
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "html",
        "-E",  # Don't use cached environment
        "-a",  # Write all files
        "--keep-going",
        "-v",
        str(SOURCE_DIR),
        str(BUILD_DIR),
    ]

    run_with_graceful_handling(session, cmd, log_file, "Full Sphinx Build")


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

    log_file = create_log_file(session, "docs_autobuild")

    # Kill existing processes
    try:
        session.run("pkill", "-f", "sphinx-autobuild.*8003", external=True)
        session.log("🧹 Killed existing sphinx processes")
    except BaseException:
        pass

    # Install dependencies
    session.run("poetry", "install", "--with", "docs", external=True)

    session.log("🌐 Auto-build server will start at: http://localhost:8003")
    session.log("🔄 Documentation rebuilds automatically on file changes")

    # Autobuild command
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
        "packages",
        "--ignore",
        "*.pyc",
        "--ignore",
        "__pycache__/*",
        "--open-browser",
        "--delay",
        "1",
        "--keep-going",
        "-v",
    ]

    try:
        run_with_graceful_handling(session, cmd, log_file, "Auto-build Server")
    except KeyboardInterrupt:
        session.log("🛑 Auto-build server stopped by user")


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
    session.log("🔍 Analyzing recent build logs...")

    if not LOGS_DIR.exists():
        session.log("❌ No logs directory found. Run 'nox -s docs' first.")
        return

    log_files = list(LOGS_DIR.glob("docs_build_*.log"))
    if not log_files:
        session.log("❌ No build logs found.")
        return

    latest_log = max(log_files, key=lambda f: f.stat().st_mtime)
    session.log(f"📋 Analyzing: {latest_log}")

    with open(latest_log) as f:
        content = f.read()

    # Count issues
    issues = {
        "import_errors":
        content.count("ModuleNotFoundError") + content.count("ImportError"),
        "syntax_errors":
        content.count("SyntaxError"),
        "warnings":
        content.count("WARNING"),
        "file_not_found":
        content.count("FileNotFoundError"),
    }

    session.log("=" * 50)
    session.log("📊 ISSUE ANALYSIS")
    session.log("=" * 50)

    for issue_type, count in issues.items():
        if count > 0:
            icon = "🚨" if count > 10 else "⚠️"
            session.log(
                f"{icon} {issue_type.replace('_', ' ').title()}: {count}")

    session.log(f"📋 Full log: {latest_log}")


@nox.session(python=PYTHON_VERSIONS)
def docs_history(session):
    """Show build history and trends from log files."""
    session.log("📈 Analyzing build history...")

    if not LOGS_DIR.exists():
        session.log("❌ No logs directory found.")
        return

    log_files = list(LOGS_DIR.glob("docs_build_*.log"))
    if not log_files:
        session.log("❌ No build logs found.")
        return

    # Sort by modification time (newest first)
    log_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

    session.log("=" * 60)
    session.log("📊 BUILD HISTORY (last 10)")
    session.log("=" * 60)

    for i, log_file in enumerate(log_files[:10]):
        timestamp = log_file.stem.split("_")[-2:]
        date_str = timestamp[0]
        time_str = timestamp[1]
        formatted_time = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]} {time_str[:2]}:{time_str[2:4]}:{time_str[4:6]}"

        with open(log_file) as f:
            content = f.read()
            warnings = content.count("WARNING")
            errors = content.count("ERROR")

        status = "✅" if errors == 0 else "❌"
        session.log(
            f"{i + 1:2d}. {formatted_time} | {status} | ⚠️ {warnings:3d} | 🚨 {errors:3d}",
        )

    session.log("=" * 60)


@nox.session(python=PYTHON_VERSIONS)
def docs_logs(session):
    """List and manage documentation build logs."""
    session.log("📋 Documentation build logs management")

    if not LOGS_DIR.exists():
        session.log("❌ No logs directory found.")
        return

    all_logs = list(LOGS_DIR.glob("*.log"))

    session.log(f"📁 Total logs: {len(all_logs)}")

    # Calculate total size
    total_size = sum(f.stat().st_size for f in all_logs)
    size_mb = total_size / (1024 * 1024)
    session.log(f"💾 Total log size: {size_mb:.1f} MB")

    # Show recent logs
    recent_logs = sorted(all_logs,
                         key=lambda f: f.stat().st_mtime,
                         reverse=True)[:5]

    session.log("\n📋 Recent logs:")
    for log_file in recent_logs:
        size_kb = log_file.stat().st_size / 1024
        mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
        session.log(
            f"  📄 {log_file.name} ({size_kb:.1f} KB) - {mtime.strftime('%Y-%m-%d %H:%M:%S')}",
        )

    if len(all_logs) > 20:
        session.log(
            f"\n⚠️  You have {len(all_logs)} log files. Consider cleaning old logs.",
        )


@nox.session(python=PYTHON_VERSIONS)
def docs_quality(session):
    """Run documentation quality checks (doc8, codespell)."""
    session.log("🔍 Running documentation quality checks...")

    create_log_file(session, "docs_quality")

    # Install dependencies
    session.run("poetry", "install", "--only", "docs", external=True)

    # Run doc8
    session.log("📋 Running doc8 (RST linter)...")
    try:
        session.run("poetry", "run", "doc8", str(SOURCE_DIR), external=True)
        session.log("✅ doc8: No RST issues found")
    except Exception as e:
        session.log(f"⚠️  doc8 found issues: {e}")

    # Run codespell
    session.log("📝 Running codespell (typo checker)...")
    try:
        session.run("poetry",
                    "run",
                    "codespell",
                    str(SOURCE_DIR),
                    external=True)
        session.log("✅ codespell: No typos found")
    except Exception as e:
        session.log(f"⚠️  codespell found typos: {e}")


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
def docs_nitpicky(session):
    """Run Sphinx in nitpicky mode to catch all warnings and errors."""
    session.log(
        "🔍 Running Sphinx in nitpicky mode (all warnings are errors)...")

    log_file = create_log_file(session, "docs_nitpicky")

    # Ensure dependencies are ready
    if not ensure_sphinx_available(session):
        session.error("❌ Could not prepare Sphinx for nitpicky check")
        return None

    # Nitpicky mode command
    cmd = [
        "poetry",
        "run",
        "sphinx-build",
        "-n",  # Nitpicky mode
        "-W",  # Warnings are errors
        "-b",
        "gettext",  # Minimal builder for fast checking
        str(SOURCE_DIR),
        str(DOCS_DIR / "build" / "nitpicky"),
    ]

    # Run nitpicky check
    status = run_with_graceful_handling(session, cmd, log_file,
                                        "Nitpicky Check")

    if status["success"]:
        session.log("✅ All checks passed in nitpicky mode!")
    else:
        session.log(f"❌ Nitpicky check failed with {status['errors']} errors")
        session.log(
            "💡 Fix all warnings and errors before building documentation")

    return status["success"]


@nox.session(python=PYTHON_VERSIONS)
def docs_test(session):
    """Quick validation of conf.py syntax and imports."""
    session.log("🧪 Testing documentation configuration...")

    # Test 1: Compile conf.py
    session.log("📋 Checking conf.py syntax...")
    try:
        session.run(
            "python",
            "-m",
            "compileall",
            str(SOURCE_DIR / "conf.py"),
            external=True,
        )
        session.log("✅ conf.py syntax is valid")
    except Exception as e:
        session.log(f"❌ conf.py has syntax errors: {e}")
        return False

    # Test 2: Import conf.py
    session.log("📦 Testing conf.py imports...")
    try:
        session.run(
            "python",
            "-c",
            f"import sys; sys.path.insert(0, '{SOURCE_DIR}'); import conf",
            external=True,
        )
        session.log("✅ conf.py imports successfully")
    except Exception as e:
        session.log(f"❌ conf.py import failed: {e}")
        return False

    # Test 3: Run flake8 if available
    try:
        session.run("flake8", "--version", external=True, silent=True)
        session.log("🔍 Running flake8 on conf.py...")
        session.run(
            "flake8",
            str(SOURCE_DIR / "conf.py"),
            "--max-line-length=120",
            "--ignore=E501,W503",
            external=True,
        )
        session.log("✅ flake8 checks passed")
    except Exception:
        session.log("⚠️  flake8 not available, skipping style check")

    session.log("✅ All configuration tests passed!")
    return True


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

    status = run_with_graceful_handling(session, cmd, log_file,
                                        "Coverage Check")

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

    log_file = create_log_file(session, "docs_pdf")

    # Install dependencies
    session.run("poetry", "install", "--with", "docs", external=True)

    # First build HTML
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

    run_with_graceful_handling(session, cmd, log_file, "PDF Generation")
