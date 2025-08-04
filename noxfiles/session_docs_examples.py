"""Documentation sessions with example execution control for Haive."""
from __future__ import annotations

import os
import shutil
from datetime import datetime

import nox
from env_utils import ensure_sphinx_available
from session_docs import BUILD_DIR
from session_docs import create_log_file
from session_docs import PYTHON_VERSIONS
from session_docs import run_with_graceful_handling
from session_docs import SOURCE_DIR

# Import shared environment utilities
# Import shared utilities from the main docs sessions

# Reuse virtualenvs for speed
nox.options.reuse_existing_virtualenvs = True


@nox.session(python=PYTHON_VERSIONS)
def docs_no_examples(session):
    """Fast documentation build WITHOUT example execution (non-.

    computational).
    """
    start_time = datetime.now()
    session.log("🚀 Running FAST documentation build WITHOUT examples...")
    session.log(
        "   This build skips example execution for faster, non-computational builds",
    )

    log_file = create_log_file(session, "docs_no_examples")

    # Ensure dependencies are ready
    if not ensure_sphinx_available(session):
        session.error("❌ Could not prepare Sphinx for documentation build")
        return None

    # Set environment to disable examples
    env = os.environ.copy()
    env["SPHINX_DISABLE_EXAMPLES"] = "1"
    env["SPHINX_PROFILE"] = "standard"  # Use standard profile for good balance

    session.log("📊 Environment configuration:")
    session.log(
        f"   SPHINX_DISABLE_EXAMPLES = {env['SPHINX_DISABLE_EXAMPLES']}")
    session.log(f"   SPHINX_PROFILE = {env['SPHINX_PROFILE']}")
    session.log("   🚫 Sphinx Gallery execution DISABLED")
    session.log("   ⚡ Examples will be documented but not executed")

    # Build command
    cmd = [
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "html",
        "-j",
        "auto",  # Parallel
        "--keep-going",  # Continue on errors
        "-v",
        str(SOURCE_DIR),
        str(BUILD_DIR),
    ]

    # Run build with environment variables
    session.env.update(env)
    status = run_with_graceful_handling(
        session,
        cmd,
        log_file,
        "No-Examples Sphinx Build",
    )

    # Check actual results
    if BUILD_DIR.exists():
        html_files = list(BUILD_DIR.glob("*.html"))
        actual_files_count = len(html_files)
    else:
        actual_files_count = 0

    # Report results
    elapsed = (datetime.now() - start_time).total_seconds()

    if status["success"] and actual_files_count > 0:
        session.log(f"✅ Fast build completed successfully in {elapsed:.1f}s!")
        session.log(f"📄 Generated {actual_files_count} HTML files")
        session.log("🚫 Examples were skipped - no computational overhead")
        session.log(f"🌐 View docs: file://{BUILD_DIR.absolute()}/index.html")
    else:
        session.log(f"❌ Build failed after {elapsed:.1f}s")
        session.log(f"📄 Only {actual_files_count} HTML files were generated")

    session.log(f"📋 Full build log: {log_file}")
    return status["success"]


@nox.session(python=PYTHON_VERSIONS)
def docs_with_examples(session):
    """Documentation build WITH example execution (computational)."""
    start_time = datetime.now()
    session.log("🐌 Running documentation build WITH examples...")
    session.log("   This build executes examples and may take longer")

    log_file = create_log_file(session, "docs_with_examples")

    # Ensure dependencies are ready
    if not ensure_sphinx_available(session):
        session.error("❌ Could not prepare Sphinx for documentation build")
        return None

    # Set environment to enable examples
    env = os.environ.copy()
    env["SPHINX_DISABLE_EXAMPLES"] = "0"
    env["SPHINX_PROFILE"] = "full"  # Use full profile for examples

    session.log("📊 Environment configuration:")
    session.log(
        f"   SPHINX_DISABLE_EXAMPLES = {env['SPHINX_DISABLE_EXAMPLES']}")
    session.log(f"   SPHINX_PROFILE = {env['SPHINX_PROFILE']}")
    session.log("   ✅ Sphinx Gallery execution ENABLED")
    session.log("   🔄 Examples will be executed (computational overhead)")

    # Build command with longer timeout for examples
    cmd = [
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "html",
        "--keep-going",  # Continue on errors
        "-v",
        str(SOURCE_DIR),
        str(BUILD_DIR),
    ]

    # Run build with environment variables
    session.env.update(env)
    status = run_with_graceful_handling(
        session,
        cmd,
        log_file,
        "With-Examples Sphinx Build",
    )

    # Check actual results
    if BUILD_DIR.exists():
        html_files = list(BUILD_DIR.glob("*.html"))
        actual_files_count = len(html_files)

        # Check for generated examples
        auto_examples_dir = BUILD_DIR / "auto_examples"
        example_files = (list(auto_examples_dir.rglob("*.html"))
                         if auto_examples_dir.exists() else [])
    else:
        actual_files_count = 0
        example_files = []

    # Report results
    elapsed = (datetime.now() - start_time).total_seconds()

    if status["success"] and actual_files_count > 0:
        session.log(f"✅ Full build completed successfully in {elapsed:.1f}s!")
        session.log(f"📄 Generated {actual_files_count} HTML files")
        session.log(f"🎯 Generated {len(example_files)} example pages")
        session.log("✅ Examples were executed and included")
        session.log(f"🌐 View docs: file://{BUILD_DIR.absolute()}/index.html")
    else:
        session.log(f"❌ Build failed after {elapsed:.1f}s")
        session.log(f"📄 Only {actual_files_count} HTML files were generated")

    session.log(f"📋 Full build log: {log_file}")
    return status["success"]


@nox.session(python=PYTHON_VERSIONS)
def docs_compare_examples(session):
    """Compare build times and results with and without example execution."""
    session.log(
        "🏁 Comparing documentation builds with and without examples...")

    # Build without examples
    session.log("\n" + "=" * 60)
    session.log("Phase 1: Building WITHOUT examples")
    session.log("=" * 60)

    start_time = datetime.now()
    success_no_examples = docs_no_examples.func(session)
    time_no_examples = (datetime.now() - start_time).total_seconds()

    # Count files without examples
    if BUILD_DIR.exists():
        files_no_examples = len(list(BUILD_DIR.glob("*.html")))
    else:
        files_no_examples = 0

    # Clean for next build
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)

    # Build with examples
    session.log("\n" + "=" * 60)
    session.log("Phase 2: Building WITH examples")
    session.log("=" * 60)

    start_time = datetime.now()
    success_with_examples = docs_with_examples.func(session)
    time_with_examples = (datetime.now() - start_time).total_seconds()

    # Count files with examples
    if BUILD_DIR.exists():
        files_with_examples = len(list(BUILD_DIR.glob("*.html")))
        auto_examples_dir = BUILD_DIR / "auto_examples"
        example_files = (len(list(auto_examples_dir.rglob("*.html")))
                         if auto_examples_dir.exists() else 0)
    else:
        files_with_examples = 0
        example_files = 0

    # Report comparison
    session.log("\n" + "=" * 80)
    session.log("📊 BUILD COMPARISON RESULTS")
    session.log("=" * 80)

    session.log("🚫 WITHOUT Examples:")
    session.log(f"   ⏱️  Time: {time_no_examples:.1f}s")
    session.log(f"   📄 Files: {files_no_examples}")
    session.log(f"   ✅ Success: {success_no_examples}")

    session.log("\n✅ WITH Examples:")
    session.log(f"   ⏱️  Time: {time_with_examples:.1f}s")
    session.log(f"   📄 Files: {files_with_examples}")
    session.log(f"   🎯 Example pages: {example_files}")
    session.log(f"   ✅ Success: {success_with_examples}")

    # Calculate improvements
    if time_with_examples > 0:
        time_savings = time_with_examples - time_no_examples
        percent_faster = (time_savings / time_with_examples) * 100
        session.log("\n💡 Performance Comparison:")
        session.log(
            f"   ⚡ Time saved: {time_savings:.1f}s ({percent_faster:.1f}% faster)",
        )
        session.log(
            f"   📊 Speed multiplier: {time_with_examples / time_no_examples:.1f}x",
        )

    # Recommendations
    session.log("\n🎯 Recommendations:")
    session.log(
        f"   - For development: Use 'nox -s docs_no_examples' ({time_no_examples:.1f}s)",
    )
    session.log(
        "   - For CI/testing: Use 'nox -s docs_no_examples' (fast feedback)")
    session.log(
        "   - For production: Use 'nox -s docs_with_examples' (complete docs)")
    session.log(
        "   - For preview: Use 'nox -s docs_no_examples' then 'nox -s docs_serve'",
    )


@nox.session(python=PYTHON_VERSIONS)
def docs_minimal_no_examples(session):
    """Ultra-fast minimal documentation build without examples."""
    start_time = datetime.now()
    session.log("⚡ Running MINIMAL documentation build (fastest possible)...")

    log_file = create_log_file(session, "docs_minimal_no_examples")

    # Ensure dependencies are ready
    if not ensure_sphinx_available(session):
        session.error("❌ Could not prepare Sphinx for documentation build")
        return None

    # Set environment for minimal build
    env = os.environ.copy()
    env["SPHINX_DISABLE_EXAMPLES"] = "1"
    env["SPHINX_PROFILE"] = "minimal"  # Minimal profile

    session.log("📊 Ultra-minimal configuration:")
    session.log(
        f"   SPHINX_DISABLE_EXAMPLES = {env['SPHINX_DISABLE_EXAMPLES']}")
    session.log(f"   SPHINX_PROFILE = {env['SPHINX_PROFILE']}")
    session.log("   ⚡ Minimal extensions only")
    session.log("   🚫 No examples, no gallery, no heavy processing")

    # Minimal build command
    cmd = [
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "html",
        "-j",
        "auto",  # Parallel
        "-q",  # Quiet mode
        str(SOURCE_DIR),
        str(BUILD_DIR),
    ]

    # Run build
    session.env.update(env)
    status = run_with_graceful_handling(session, cmd, log_file,
                                        "Minimal Build")

    elapsed = (datetime.now() - start_time).total_seconds()

    if status["success"]:
        files_count = len(list(
            BUILD_DIR.glob("*.html"))) if BUILD_DIR.exists() else 0
        session.log(f"⚡ Ultra-fast build completed in {elapsed:.1f}s!")
        session.log(f"📄 Generated {files_count} HTML files")
        session.log(f"🌐 View docs: file://{BUILD_DIR.absolute()}/index.html")
    else:
        session.log(f"❌ Minimal build failed after {elapsed:.1f}s")

    session.log(f"📋 Full build log: {log_file}")
    return status["success"]


@nox.session(python=PYTHON_VERSIONS)
def docs_autobuild_no_examples(session):
    """Auto-build documentation server without example execution."""
    session.log("🚀 Starting auto-build server WITHOUT examples...")
    session.log("   Fast rebuilds on file changes - no computational overhead")

    log_file = create_log_file(session, "docs_autobuild_no_examples")

    # Kill existing processes
    try:
        session.run("pkill", "-f", "sphinx-autobuild.*8004", external=True)
        session.log("🧹 Killed existing sphinx processes")
    except BaseException:
        pass

    # Install dependencies
    session.run("poetry", "install", "--with", "docs", external=True)

    # Set environment to disable examples
    env = os.environ.copy()
    env["SPHINX_DISABLE_EXAMPLES"] = "1"
    env["SPHINX_PROFILE"] = "standard"

    session.log("🌐 Auto-build server will start at: http://localhost:8004")
    session.log("🔄 Documentation rebuilds automatically on file changes")
    session.log("🚫 Examples are disabled for faster rebuilds")

    # Autobuild command
    cmd = [
        "poetry",
        "run",
        "sphinx-autobuild",
        str(SOURCE_DIR),
        str(BUILD_DIR),
        "--port",
        "8004",  # Different port from regular autobuild
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
    ]

    try:
        # Run with environment variables
        session.env.update(env)
        run_with_graceful_handling(
            session,
            cmd,
            log_file,
            "Auto-build Server (No Examples)",
        )
    except KeyboardInterrupt:
        session.log("🛑 Auto-build server stopped by user")


@nox.session(python=PYTHON_VERSIONS)
def docs_dev(session):
    """Alias for docs_no_examples - convenient for development."""
    session.log("🛠️  Development documentation build (no examples)...")
    return docs_no_examples.func(session)


@nox.session(python=PYTHON_VERSIONS)
def docs_prod(session):
    """Alias for docs_with_examples - for production builds."""
    session.log("🏭 Production documentation build (with examples)...")
    return docs_with_examples.func(session)
