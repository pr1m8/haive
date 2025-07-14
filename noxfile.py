"""Nox configuration for Haive project.

Documentation Commands:
-----------------------
    nox -s docs                 # Build docs once with graceful error handling
    nox -s docs_serve           # Serve pre-existing build (simple HTTP server)
    nox -s docs_autobuild       # Auto-build with hot reload and live updates
    nox -s docs_clean           # Clean build artifacts

Development Commands:
--------------------
    nox -s lint                 # Run linters
    nox -s test                 # Run tests
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

# Paths
DOCS_DIR = Path("docs")
SOURCE_DIR = DOCS_DIR / "source"
BUILD_DIR = DOCS_DIR / "_build"
LOGS_DIR = DOCS_DIR / "logs"


def create_log_file(session, operation_name: str) -> Path:
    """Create a timestamped log file for the operation."""
    LOGS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOGS_DIR / f"{operation_name}_{timestamp}.log"
    session.log(f"📝 Logging to: {log_file}")
    return log_file


def run_with_graceful_handling(
    session, cmd: list, log_file: Path, operation: str
) -> bool:
    """Run command with graceful error handling and logging."""
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

                    # Display with nice formatting
                    line = output.strip()
                    if "warning:" in line.lower():
                        session.log(f"⚠️  {line}")
                    elif "error:" in line.lower() and "autosummary" not in line.lower():
                        session.log(f"🚨 {line}")
                    elif line and not line.startswith(("Running Sphinx", "loading")):
                        session.log(f"📄 {line}")

            returncode = process.poll()

            with open(log_file, "a") as f:
                f.write(f"\nCompleted: {datetime.now()}\n")
                f.write(f"Return code: {returncode}\n")

        if returncode == 0:
            session.log(f"✅ {operation} completed successfully!")
            return True
        session.log(f"⚠️  {operation} completed with issues (check logs for details)")
        session.log(f"📋 Full log: {log_file}")
        return False

    except Exception as e:
        session.log(f"❌ {operation} failed: {e}")
        with open(log_file, "a") as f:
            f.write(f"\nFATAL ERROR: {e}\n")
        return False


@nox.session(python=PYTHON_VERSIONS)
def docs(session):
    """Build documentation once with graceful error handling and detailed logging."""
    session.log("📚 Building documentation with graceful error handling...")

    # Create log file
    log_file = create_log_file(session, "docs_build")

    # Install dependencies
    session.log("📦 Installing dependencies...")
    session.run("poetry", "install", "--all-extras", external=True)

    # Set environment for graceful import handling
    os.environ["SPHINX_AUTOSUMMARY_GENERATE"] = "true"
    os.environ["HAIVE_DOCS_MODE"] = "true"

    # Prepare command with enhanced error handling
    cmd = [
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "html",  # HTML output
        "-E",  # Don't use saved environment, rebuild everything
        "-a",  # Write all files, not just new/changed ones
        "--keep-going",  # Continue building despite errors
        "-v",  # Verbose output
        str(SOURCE_DIR),
        str(BUILD_DIR / "html"),
    ]

    # Run with graceful handling and live logging
    success = run_with_graceful_handling(session, cmd, log_file, "Documentation Build")

    # Report results with helpful messaging
    if success:
        session.log(
            f"🌐 Documentation: file://{(BUILD_DIR / 'html' / 'index.html').absolute()}"
        )
    else:
        session.log(
            "⚠️  Build completed with issues (this is normal during development)"
        )
        if (BUILD_DIR / "html" / "index.html").exists():
            session.log(
                f"📄 Documentation still built: file://{(BUILD_DIR / 'html' / 'index.html').absolute()}"
            )
            session.log(
                "💡 Warnings/errors are expected during development - check the log for details"
            )
        else:
            session.log(
                "❌ Build failed completely - check the log for critical errors"
            )

    session.log(f"📋 Detailed build log: {log_file}")
    return success


@nox.session(python=PYTHON_VERSIONS)
def docs_serve(session):
    """Serve pre-existing documentation build (simple HTTP server)."""
    session.log("🌐 Serving pre-built documentation...")
    
    # Check if build exists
    if not (BUILD_DIR / "html" / "index.html").exists():
        session.log("❌ No documentation build found!")
        session.log("💡 Run 'nox -s docs' first to build documentation")
        return False
    
    session.log(f"📁 Serving from: {BUILD_DIR / 'html'}")
    session.log("🌐 Server starting at: http://localhost:8003")
    session.log("🛑 Press Ctrl+C to stop")
    
    # Simple HTTP server for pre-built docs
    try:
        session.run(
            "python", "-m", "http.server", "8003", 
            "--directory", str(BUILD_DIR / "html"),
            external=True
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
    session.log("📦 Installing dependencies...")
    session.run("poetry", "install", "--all-extras", external=True)

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
        str(BUILD_DIR / "html"),
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
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
        session.log(f"✅ Cleaned {BUILD_DIR}")

    # Clean generated API docs
    api_dir = SOURCE_DIR / "api" / "generated"
    if api_dir.exists():
        shutil.rmtree(api_dir)
        session.log(f"✅ Cleaned {api_dir}")


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
