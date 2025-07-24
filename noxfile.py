"""Nox configuration for Haive project.

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
    nox -l                      # List all available sessions

Development Commands:
--------------------
    nox -s lint                 # Run linters
    nox -s test                 # Run tests

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
from datetime import datetime
from pathlib import Path

import nox

# Configuration
PYTHON_VERSIONS = ["3.12"]
nox.options.reuse_existing_virtualenvs = True
nox.options.error_on_external_run = False

# Paths - Centralized and consistent
DOCS_DIR = Path("docs")
SOURCE_DIR = DOCS_DIR / "source"
BUILD_DIR = DOCS_DIR / "build" / "html"  # Centralized to single build directory
LOGS_DIR = DOCS_DIR / "logs"

# Exclude problematic packages from documentation build
EXCLUDE_PACKAGES = ["packages/haive-prebuilt"]


def create_log_file(session, operation_name: str) -> Path:
    """Create a timestamped log file for the operation."""
    LOGS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOGS_DIR / f"{operation_name}_{timestamp}.log"
    session.log(f"📝 Logging to: {log_file}")
    return log_file


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


@nox.session(python=PYTHON_VERSIONS)
def docs_fast(session):
    """Fast documentation build that continues on errors with last 20 lines output."""
    session.log("🚀 Running FAST documentation build (continues on errors)...")

    # Create log file
    log_file = create_log_file(session, "docs_fast_build")

    # Install dependencies (reuses cache from poetry)
    session.log("📦 Installing documentation dependencies...")
    session.run("poetry", "install", "--with", "docs", external=True)

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
    session.log("🔨 Building documentation (continuing on errors)...")
    output_lines = []
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
            
            returncode = process.poll()
        
        # Show last 20 lines of output
        session.log("📄 Last 20 lines of build output:")
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


# =============================================================================
# Example Runner Sessions
# =============================================================================

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
