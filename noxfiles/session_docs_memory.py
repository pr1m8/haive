"""Memory-aware documentation sessions for Haive.

This module provides memory-safe versions of documentation sessions that:
- Monitor memory usage during builds
- Adjust parallelism based on available resources
- Clean up resources between operations
- Provide progressive fallback under memory pressure
"""

# Import memory management
from memory_manager import get_memory_safe_sphinx_args, memory_manager
import nox

# Import base documentation sessions
from session_docs import (
    BUILD_DIR,
    PYTHON_VERSIONS,
    SOURCE_DIR,
    create_log_file,
    run_with_graceful_handling,
)


@nox.session(python=PYTHON_VERSIONS)
def docs_memory_safe(session):
    """Memory-safe documentation build with automatic resource management."""
    session.log("🧠 Running memory-safe documentation build...")

    # Check memory status
    memory_status = memory_manager.check_memory_status(session)

    # Create log file
    log_file = create_log_file(session, "docs_memory_safe")

    # Install dependencies
    session.log("📦 Installing documentation dependencies...")
    session.run("poetry", "install", "--with", "docs", external=True)

    # Get memory-safe arguments
    sphinx_args = get_memory_safe_sphinx_args(session)

    # Build command with memory-safe settings
    cmd = [
        "poetry",
        "run",
        "sphinx-build",
        *sphinx_args,
        "-v",
        str(SOURCE_DIR),
        str(BUILD_DIR),
    ]

    # Monitor memory during build
    with memory_manager.monitor_build(session, "Sphinx Build"):
        status = run_with_graceful_handling(session, cmd, log_file,
                                            "Memory-Safe Build")

    # Clean up if needed
    if memory_status in ["critical", "low"]:
        memory_manager.cleanup_memory(session)

    return status["success"]


@nox.session(python=PYTHON_VERSIONS)
def docs_fast_memory(session):
    """Fast documentation build with memory monitoring."""
    session.log("🚀 Running fast build with memory awareness...")

    # Check memory and adjust strategy
    memory_gb = memory_manager.get_memory_gb()

    if memory_gb < 2.0:
        session.log("⚠️  Low memory detected - switching to memory-safe mode")
        session.notify("docs_memory_safe")
        return

    # Otherwise run fast build with monitoring
    with memory_manager.monitor_build(session, "Fast Build"):
        # Import and run the original fast build
        from session_docs import docs_fast

        # Call the underlying function directly
        docs_fast.func(session)


@nox.session(python=PYTHON_VERSIONS)
def docs_monitor(session):
    """Monitor system resources and suggest optimal build strategy."""
    session.log("📊 System Resource Analysis")
    session.log("=" * 50)

    # Check memory
    memory_manager.check_memory_status(session)
    memory_gb = memory_manager.get_memory_gb()

    # Check CPU if available
    try:
        import psutil

        cpu_count = psutil.cpu_count()
        cpu_percent = psutil.cpu_percent(interval=1)
        session.log(f"🖥️  CPU: {cpu_count} cores, {cpu_percent:.1f}% usage")
    except BaseException:
        cpu_count = 4
        session.log("🖥️  CPU: Unable to detect (assuming 4 cores)")

    # Recommendations
    session.log("\n📋 Recommendations:")

    if memory_gb < 2.0:
        session.log("  🚨 Use 'nox -s docs_memory_safe' for safe building")
        session.log("  ⚠️  Close other applications to free memory")
    elif memory_gb < 4.0:
        session.log("  ⚠️  Use 'nox -s docs' with standard settings")
        session.log("  💡 Memory is limited, avoid parallel builds")
    else:
        session.log("  ✅ Use 'nox -s docs_fast' for fastest builds")
        session.log("  ✅ Parallel builds (-j auto) are safe")

    # Suggest cleanup if needed
    if memory_gb < 4.0:
        session.log("\n🧹 Cleanup suggestions:")
        session.log("  - Run 'nox -s docs_clean' to remove old builds")
        session.log("  - Clear browser cache and close unused tabs")
        session.log("  - Run 'docker system prune' if using Docker")


@nox.session(python=PYTHON_VERSIONS)
def docs_adaptive(session):
    """Adaptive documentation build that adjusts to system resources."""
    session.log("🤖 Adaptive documentation build starting...")

    # Check resources
    memory_manager.get_memory_gb()
    memory_status = memory_manager.check_memory_status(session)

    # Choose strategy based on resources
    if memory_status == "critical":
        session.log("🚨 Critical memory - using minimal build")
        # Single job, no autosummary
        import os

        os.environ["SPHINX_AUTOSUMMARY_GENERATE"] = "false"
        cmd_args = ["-j", "1"]
    elif memory_status == "low":
        session.log("⚠️  Low memory - using conservative build")
        cmd_args = ["-j", "2"]
    elif memory_status == "moderate":
        session.log("📊 Moderate resources - using balanced build")
        cmd_args = ["-j", "4"]
    else:
        session.log("✅ Good resources - using optimal build")
        cmd_args = ["-j", "auto"]

    # Create log file
    log_file = create_log_file(session, "docs_adaptive")

    # Install dependencies
    session.log("📦 Installing documentation dependencies...")
    session.run("poetry", "install", "--with", "docs", external=True)

    # Build with adaptive settings
    cmd = [
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "html",
        *cmd_args,
        "--keep-going",
        "-v",
        str(SOURCE_DIR),
        str(BUILD_DIR),
    ]

    # Monitor and build
    with memory_manager.monitor_build(session, "Adaptive Build"):
        status = run_with_graceful_handling(session, cmd, log_file,
                                            "Adaptive Build")

    # Report results
    if status["success"]:
        session.log("✅ Adaptive build completed successfully!")
        session.log(
            f"💾 Final memory: {memory_manager.get_memory_gb():.1f}GB available",
        )

    return status["success"]


# Create memory-aware versions of existing sessions
@nox.session(python=PYTHON_VERSIONS)
def docs_autobuild_memory(session):
    """Memory-aware auto-build with resource monitoring."""
    session.log("🔄 Starting memory-aware auto-build...")

    # Check if we have enough memory for autobuild
    if memory_manager.get_memory_gb() < 3.0:
        session.log("⚠️  Insufficient memory for auto-build")
        session.log("💡 Try 'nox -s docs_memory_safe' instead")
        return False

    # Monitor memory during autobuild
    session.log("📊 Memory monitoring active during auto-build")
    session.log("⚠️  Will show warnings if memory drops below 2GB")

    # Import and run original autobuild
    from session_docs import docs_autobuild

    # Wrap the original function
    with memory_manager.monitor_build(session, "Auto-build Server"):
        docs_autobuild.func(session)
