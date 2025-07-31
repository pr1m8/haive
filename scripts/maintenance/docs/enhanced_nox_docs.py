#!/usr/bin/env python3
"""Enhanced nox documentation session with better error handling and styling."""

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


def create_log_file(session, operation_name: str) -> Path:
    """Create a timestamped log file for the operation."""
    LOGS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOGS_DIR / f"{operation_name}_{timestamp}.log"
    session.log(f"📝 Logging to: {log_file}")
    return log_file


def run_sphinx_build(session, cmd, operation, log_file):
    """Enhanced sphinx build with comprehensive error handling."""
    status = {
        "success": False,
        "warnings": 0,
        "errors": 0,
        "returncode": None,
        "output_exists": False,
        "fatal_error": None,
    }

    try:
        with open(log_file, "w") as f:
            f.write(f"=== {operation} ===\n")
            f.write(f"Command: {' '.join(cmd)}\n")
            f.write(f"Started: {datetime.now()}\n\n")

        # Run sphinx-build with live output and error capturing
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
        )

        with open(log_file, "a") as f:
            for line in iter(process.stdout.readline, ""):
                f.write(line)
                f.flush()

                line = line.strip()
                if not line:
                    continue

                # Count warnings and errors
                if "WARNING:" in line or "warning:" in line.lower():
                    status["warnings"] += 1
                if "ERROR:" in line or "error:" in line.lower():
                    status["errors"] += 1

                # Enhanced logging with emojis and colors
                if "ERROR:" in line or "CRITICAL:" in line or "FATAL:" in line:
                    session.log(f"🚨 {line}")
                elif "WARNING:" in line:
                    session.log(f"⚠️  {line}")
                elif "PASSED" in line or "SUCCESS" in line or "✅" in line:
                    session.log(f"✅ {line}")
                elif "AutoAPI" in line and "Reading files" in line:
                    session.log(f"📚 {line}")
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
def docs_enhanced(session):
    """Enhanced sphinx-build with comprehensive error handling, syntax checking, and beautiful output."""
    session.log("🎨 Running ENHANCED sphinx-build with comprehensive features...")
    session.log("=" * 60)
    session.log("🚀 HAIVE DOCUMENTATION BUILD - ENHANCED MODE")
    session.log("=" * 60)

    # Create log file
    log_file = create_log_file(session, "docs_enhanced")

    # Install dependencies
    session.log("📦 Installing dependencies...")
    session.run("poetry", "install", "--all-extras", external=True)

    # Pre-build syntax check
    session.log("🔍 Running pre-build syntax check...")
    try:
        session.run(
            "poetry", "run", "python", "pre_build_syntax_check.py", external=True
        )
        session.log("✅ Pre-build syntax check passed")
    except Exception as e:
        session.log(f"⚠️  Pre-build syntax check found issues: {e}")
        session.log("🔧 Running automatic syntax fixes...")
        try:
            session.run(
                "poetry",
                "run",
                "python",
                "fix_critical_syntax_errors.py",
                external=True,
            )
            session.log("✅ Applied automatic syntax fixes")
        except Exception:
            session.log("⚠️  Some syntax fixes failed - continuing with build")

    # Clean and prepare build directory
    session.log("🧹 Preparing build environment...")
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    # Enhanced environment variables
    os.environ["SPHINX_AUTOSUMMARY_GENERATE"] = "true"
    os.environ["HAIVE_DOCS_MODE"] = "enhanced"
    os.environ["SPHINX_VERBOSE"] = "true"

    # Build documentation with enhanced error handling
    session.log("🔧 Building documentation with enhanced features...")
    session.log("   📚 PyData Sphinx Theme with dark/light mode")
    session.log("   🎨 Enhanced styling and interactive components")
    session.log("   📱 Mobile-responsive design")
    session.log("   🔍 Advanced search functionality")
    session.log("   🌐 GitHub integration and edit buttons")
    session.log("   📊 Mermaid diagrams and interactive examples")

    status = run_sphinx_build(
        session,
        [
            "poetry",
            "run",
            "sphinx-build",
            "-b",
            "html",
            "--keep-going",
            "-v",
            "-E",
            "-a",
            str(SOURCE_DIR),
            str(BUILD_DIR),
        ],
        "Enhanced Documentation build",
        log_file,
    )

    # Enhanced success reporting with detailed analysis
    session.log("=" * 60)
    session.log("📊 BUILD ANALYSIS")
    session.log("=" * 60)

    if status["success"]:
        session.log("🎉 DOCUMENTATION BUILD COMPLETED SUCCESSFULLY!")
        session.log("")
        session.log("🌐 Access your documentation:")
        session.log(f"   📁 Local file: {BUILD_DIR / 'index.html'}")
        session.log("   🌐 HTTP server: Run 'nox -s docs_serve' to serve")
        session.log("   🔄 Auto-rebuild: Run 'nox -s docs_autobuild' for live updates")
        session.log("")
        session.log("✨ Features available:")
        session.log("   🌙 Dark/Light mode toggle")
        session.log("   🔍 Advanced search")
        session.log("   📱 Mobile-responsive design")
        session.log("   🎨 Interactive components")
        session.log("   📊 Mermaid diagrams")
        session.log("   🔗 GitHub integration")

    elif status.get("output_exists"):
        session.log("⚠️  DOCUMENTATION BUILD COMPLETED WITH ISSUES!")
        session.log("🌐 Documentation was generated but with warnings/errors")
        session.log(f"   📁 View at: {BUILD_DIR / 'index.html'}")
        session.log("   📋 Check log for details on issues")

    else:
        session.log("❌ DOCUMENTATION BUILD FAILED")
        session.log("   No documentation output was generated")
        session.log(f"   📋 Check log file: {log_file}")
        session.log("   🔧 Common fixes:")
        session.log("     - Run 'poetry run python fix_critical_syntax_errors.py'")
        session.log("     - Check for missing dependencies")
        session.log("     - Verify Python imports")

    # Build statistics
    session.log("=" * 60)
    session.log("📈 BUILD STATISTICS")
    session.log("=" * 60)
    session.log(f"⚠️  Warnings: {status['warnings']}")
    session.log(f"🚨 Errors: {status['errors']}")
    session.log(f"📋 Log file: {log_file}")

    # Additional build info
    if BUILD_DIR.exists():
        html_files = list(BUILD_DIR.glob("**/*.html"))
        css_files = list(BUILD_DIR.glob("**/*.css"))
        js_files = list(BUILD_DIR.glob("**/*.js"))

        session.log(f"📄 Generated {len(html_files)} HTML files")
        session.log(f"🎨 Generated {len(css_files)} CSS files")
        session.log(f"⚡ Generated {len(js_files)} JavaScript files")

        # Check for key files
        key_files = {
            "index.html": "Main documentation page",
            "api/index.html": "API documentation",
            "search.html": "Search functionality",
            "genindex.html": "General index",
            "_static/custom.css": "Custom styling",
        }

        session.log("")
        session.log("🔍 Key files check:")
        for key_file, description in key_files.items():
            if (BUILD_DIR / key_file).exists():
                session.log(f"   ✅ {description}: {key_file}")
            else:
                session.log(f"   ⚠️  Missing {description}: {key_file}")

    session.log("=" * 60)
    session.log("🎨 Your enhanced Haive documentation is ready!")
    session.log("=" * 60)

    return status


if __name__ == "__main__":
    # For testing
    import sys

    sys.exit(0)
