"""Environment and dependency management utilities for nox sessions.

This module provides reusable utilities for:
- Poetry dependency management
- Environment validation
- Lock file synchronization
- Graceful error handling for dependency issues
"""
from __future__ import annotations

import subprocess
from datetime import datetime
from pathlib import Path


def ensure_poetry_sync(session,
                       group: str = "docs",
                       log_prefix: str = "📦") -> bool:
    """Ensure poetry lock file is synced and dependencies can be installed.

    Args:
        session: Nox session object
        group: Poetry dependency group to install (e.g., "docs", "test", "dev")
        log_prefix: Emoji prefix for log messages

    Returns:
        bool: True if dependencies are ready, False if there were issues
    """
    session.log(f"{log_prefix} Checking poetry environment sync...")

    # Step 1: Check if lock file is in sync with pyproject.toml
    try:
        session.run("poetry", "check", "--lock", external=True, silent=True)
        session.log("✅ Poetry lock file is in sync")
    except Exception:
        session.log("🔄 Poetry lock file out of sync, updating...")
        try:
            session.run("poetry", "lock", "--no-update", external=True)
            session.log("✅ Poetry lock file updated")
        except Exception as e:
            session.log(f"❌ Failed to update lock file: {e}")
            session.log(
                "💡 Try running 'poetry lock' manually to fix dependency issues",
            )
            return False

    # Step 2: Try to install dependencies with sync
    try:
        session.log(f"{log_prefix} Installing {group} dependencies...")
        session.run(
            "poetry",
            "install",
            "--with",
            group,
            "--no-interaction",
            "--sync",  # Ensure installed packages match lock file exactly
            external=True,
        )
        session.log("✅ Dependencies installed successfully with --sync")
        return True
    except Exception as e:
        session.log(f"⚠️  Failed to install with --sync: {str(e)[:100]}...")
        session.log("🔧 Trying fallback installation methods...")

        # Step 3: Fallback - try without sync
        try:
            session.log(
                f"{log_prefix} Attempting installation without --sync...")
            session.run(
                "poetry",
                "install",
                "--with",
                group,
                "--no-interaction",
                external=True,
            )
            session.log("✅ Dependencies installed with fallback method")
            return True
        except Exception as fallback_error:
            session.log(
                f"❌ Fallback installation also failed: {str(fallback_error)[:100]}...",
            )

            # Step 4: Last resort - try without problematic optional dependencies
            try:
                session.log(f"{log_prefix} Attempting minimal installation...")
                session.run(
                    "poetry",
                    "install",
                    "--only",
                    group,  # Only install the specific group, skip others
                    "--no-interaction",
                    external=True,
                )
                session.log(
                    "⚠️  Minimal dependencies installed (some features may be unavailable)", )
                return True
            except Exception:
                session.log("❌ All installation methods failed")
                session.log("💡 Manual steps to fix:")
                session.log("   1. Run 'poetry lock' to fix lock file")
                session.log(
                    "   2. Check for conflicting dependencies in pyproject.toml",
                )
                session.log("   3. Consider removing problematic packages")
                return False


def check_tool_available(
    session,
    tool_name: str,
    version_flag: str = "--version",
) -> bool:
    """Check if a tool is available in the current environment.

    Args:
        session: Nox session object
        tool_name: Name of the tool/command to check
        version_flag: Flag to use for version check (default: --version)

    Returns:
        bool: True if tool is available, False otherwise
    """
    try:
        session.run(
            "poetry",
            "run",
            tool_name,
            version_flag,
            silent=True,
            external=True,
        )
        return True
    except Exception:
        return False


def ensure_sphinx_available(session) -> bool:
    """Ensure Sphinx is available for documentation builds.

    Args:
        session: Nox session object

    Returns:
        bool: True if Sphinx is ready, False if unavailable
    """
    session.log("🔍 Checking Sphinx availability...")

    if check_tool_available(session, "sphinx-build"):
        session.log("✅ Sphinx is available")
        return True
    session.log(
        "❌ Sphinx not available, attempting to install docs dependencies...", )
    if ensure_poetry_sync(session, group="docs"):
        # Check again after installation
        if check_tool_available(session, "sphinx-build"):
            session.log("✅ Sphinx is now available")
            return True
        session.log("❌ Sphinx still not available after installation")
        return False
    session.log("❌ Failed to install dependencies for Sphinx")
    return False


def get_dependency_info(session) -> dict:
    """Get information about current dependency state.

    Args:
        session: Nox session object

    Returns:
        dict: Information about poetry environment
    """
    info = {
        "lock_sync": False,
        "docs_installed": False,
        "sphinx_available": False,
        "poetry_env": None,
    }

    try:
        # Check lock sync
        session.run("poetry", "check", "--lock", external=True, silent=True)
        info["lock_sync"] = True
    except Exception:
        pass

    try:
        # Check if docs dependencies are installed
        result = session.run(
            "poetry",
            "show",
            "--with",
            "docs",
            external=True,
            silent=True,
        )
        info["docs_installed"] = True
    except Exception:
        pass

    # Check Sphinx availability
    info["sphinx_available"] = check_tool_available(session, "sphinx-build")

    try:
        # Get poetry env info
        result = subprocess.run(
            ["poetry", "env", "info", "--path"],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
            check=False,
        )
        if result.returncode == 0:
            info["poetry_env"] = result.stdout.strip()
    except Exception:
        pass

    return info


def create_dependency_report(session, operation: str = "build") -> str:
    """Create a dependency status report.

    Args:
        session: Nox session object
        operation: Name of operation being performed

    Returns:
        str: Formatted dependency report
    """
    info = get_dependency_info(session)

    report = f"""
=== Dependency Status Report for {operation} ===
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Lock file sync: {"✅" if info["lock_sync"] else "❌"}
Docs dependencies: {"✅" if info["docs_installed"] else "❌"}
Sphinx available: {"✅" if info["sphinx_available"] else "❌"}
Poetry environment: {info["poetry_env"] or "Unknown"}

Recommendations:
"""

    if not info["lock_sync"]:
        report += "- Run 'poetry lock' to sync lock file\n"
    if not info["docs_installed"]:
        report += "- Run 'poetry install --with docs' to install documentation dependencies\n"
    if not info["sphinx_available"]:
        report += "- Check Sphinx installation in poetry environment\n"

    return report


def log_environment_info(session, log_level: str = "info"):
    """Log current environment information for debugging.

    Args:
        session: Nox session object
        log_level: Level of detail ("minimal", "info", "verbose")
    """
    if log_level == "minimal":
        info = get_dependency_info(session)
        session.log(
            f"🔧 Environment: Lock={'✅' if info['lock_sync'] else '❌'} "
            f"Docs={'✅' if info['docs_installed'] else '❌'} "
            f"Sphinx={'✅' if info['sphinx_available'] else '❌'}", )
    elif log_level in ["info", "verbose"]:
        report = create_dependency_report(session)
        session.log(report)
