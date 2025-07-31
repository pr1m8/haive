"""Documentation sessions for Haive."""

import json
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

import nox

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
    session, cmd: list, log_file: Path, operation: str
) -> dict:
    """Run command with graceful error handling."""
    status = {
        "success": False,
        "warnings": 0,
        "errors": 0,
    }

    try:
        session.log(f"🔧 Running: {' '.join(cmd)}")

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

            while True:
                output = process.stdout.readline()
                if output == "" and process.poll() is not None:
                    break
                if output:
                    f.write(output)
                    f.flush()

                    line = output.strip()
                    if "warning:" in line.lower():
                        status["warnings"] += 1
                    elif "error:" in line.lower():
                        status["errors"] += 1

            status["success"] = process.poll() == 0

            f.write(f"\nCompleted: {datetime.now()}\n")
            f.write(f"Warnings: {status['warnings']}\n")
            f.write(f"Errors: {status['errors']}\n")

        if status["success"]:
            session.log(f"✅ {operation} completed successfully!")
        else:
            session.log(f"❌ {operation} failed")

        session.log(f"📊 Warnings: {status['warnings']}, Errors: {status['errors']}")

        return status

    except Exception as e:
        session.log(f"❌ {operation} failed: {e}")
        return status


@nox.session(python=PYTHON_VERSIONS)
def docs_fast(session):
    """Fast documentation build that continues on errors."""
    start_time = datetime.now()
    session.log("🚀 Running FAST documentation build (continues on errors)...")

    log_file = create_log_file(session, "docs_fast_build")

    # Quick dependency check
    try:
        session.run(
            "poetry", "run", "sphinx-build", "--version", silent=True, external=True
        )
        session.log("✅ Dependencies already installed")
    except:
        session.log("📦 Installing documentation dependencies...")
        session.run(
            "poetry", "install", "--with", "docs", "--no-interaction", external=True
        )

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

    # Run with output capture
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

            while True:
                output = process.stdout.readline()
                if output == "" and process.poll() is not None:
                    break
                if output:
                    f.write(output)
                    f.flush()
                    output_lines.append(output.strip())

            process.poll()

        # Show last 20 lines
        session.log("📄 Last 20 lines of output:")
        session.log("-" * 50)
        for line in output_lines[-20:]:
            if line:
                session.log(line)
        session.log("-" * 50)

        # Check results
        if BUILD_DIR.exists():
            html_files = list(BUILD_DIR.glob("*.html"))
            if html_files:
                session.log(f"✅ Built {len(html_files)} HTML files!")
                session.log(f"🌐 View docs: file://{BUILD_DIR.absolute()}/index.html")
            else:
                session.log("❌ No HTML files generated")

        elapsed = (datetime.now() - start_time).total_seconds()
        session.log(f"⏱️  Build completed in {elapsed:.1f}s")

    except Exception as e:
        session.log(f"❌ Build failed: {e}")
        session.log(f"📋 Check log: {log_file}")


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
    """Full sphinx-build with autosummary regeneration (slower but complete)."""
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
    except:
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
        "import_errors": content.count("ModuleNotFoundError")
        + content.count("ImportError"),
        "syntax_errors": content.count("SyntaxError"),
        "warnings": content.count("WARNING"),
        "file_not_found": content.count("FileNotFoundError"),
    }

    session.log("=" * 50)
    session.log("📊 ISSUE ANALYSIS")
    session.log("=" * 50)

    for issue_type, count in issues.items():
        if count > 0:
            icon = "🚨" if count > 10 else "⚠️"
            session.log(f"{icon} {issue_type.replace('_', ' ').title()}: {count}")

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
            f"{i+1:2d}. {formatted_time} | {status} | ⚠️ {warnings:3d} | 🚨 {errors:3d}"
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
    recent_logs = sorted(all_logs, key=lambda f: f.stat().st_mtime, reverse=True)[:5]

    session.log("\n📋 Recent logs:")
    for log_file in recent_logs:
        size_kb = log_file.stat().st_size / 1024
        mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
        session.log(
            f"  📄 {log_file.name} ({size_kb:.1f} KB) - {mtime.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    if len(all_logs) > 20:
        session.log(
            f"\n⚠️  You have {len(all_logs)} log files. Consider cleaning old logs."
        )


@nox.session(python=PYTHON_VERSIONS)
def docs_quality(session):
    """Run documentation quality checks (doc8, codespell)."""
    session.log("🔍 Running documentation quality checks...")

    log_file = create_log_file(session, "docs_quality")

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
        session.run("poetry", "run", "codespell", str(SOURCE_DIR), external=True)
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
