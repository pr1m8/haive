"""Clean Furo-based documentation builds."""

from __future__ import annotations

import os
from pathlib import Path

import nox

# Python versions to test
PYTHON_VERSIONS = ["3.12"]

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DOCS_DIR = PROJECT_ROOT / "docs" / "source"
BUILD_DIR = PROJECT_ROOT / "docs" / "builds"


@nox.session(name="docs-furo")
def docs_furo(session):
    """Build documentation with Furo theme + AutoAPI (original version).

    This includes proper API documentation with haive.core.* namespacing.

    Usage:
        nox -s docs-furo
    """
    # Environment variables for Furo + AutoAPI build
    env = {
        "SPHINX_PACKAGES": "core.engine",  # Just engine for speed
        "SPHINX_THEME": "furo",
        "SPHINX_INCLUDE_MCP_DOCS": "false",
        "SPHINX_INCLUDE_READMES": "false",
    }

    output_dir = BUILD_DIR / "furo_original"

    session.log("🎨 Building Furo + AutoAPI (Original)...")
    session.log("📦 Submodule: haive.core.engine (fast build)")
    session.log("🔧 Proper haive.core.* namespacing")

    # Use original Furo config from templates directory
    import shutil

    conf_backup = DOCS_DIR / "conf.py.backup"
    conf_furo = DOCS_DIR / "conf_templates" / "conf_furo.py"  # Original config
    conf_main = DOCS_DIR / "conf.py"

    # Backup original config
    if conf_main.exists():
        shutil.copy2(conf_main, conf_backup)
        session.log("📋 Backed up original conf.py")

    # Copy original Furo config as main config
    shutil.copy2(conf_furo, conf_main)
    session.log("🎨 Activated Original Furo configuration")

    try:
        # Run sphinx-build with original Furo config
        session.run(
            "poetry",
            "run",
            "sphinx-build",
            "-b",
            "html",
            str(DOCS_DIR),
            str(output_dir),
            "-v",  # Verbose to see what's happening
            env=env,
            external=True,
        )
    finally:
        # Restore original config
        if conf_backup.exists():
            shutil.copy2(conf_backup, conf_main)
            conf_backup.unlink()  # Clean up backup
            session.log("🔄 Restored original conf.py")

    session.log(f"✅ Original Furo build complete: {output_dir}")
    session.log(f"📄 View: file://{output_dir}/index.html")


@nox.session(name="docs-furo-enhanced")
def docs_furo_enhanced(session):
    """Build documentation with enhanced Furo theme + AutoAPI + TOC navigation.

    This version includes improved toctree navigation and Furo theme integration.

    Usage:
        nox -s docs-furo-enhanced
    """
    # Environment variables for enhanced Furo build
    env = {
        "SPHINX_PACKAGES": "core.engine",  # Just engine for speed
        "SPHINX_THEME": "furo",
        "SPHINX_INCLUDE_MCP_DOCS": "false",
        "SPHINX_INCLUDE_READMES": "false",
    }

    output_dir = BUILD_DIR / "furo_enhanced"

    session.log("🚀 Building Enhanced Furo + AutoAPI...")
    session.log("📦 Submodule: haive.core.engine (fast build)")
    session.log("🔧 Enhanced navigation with manual toctree")
    session.log("🎨 Improved Furo theme integration")

    # Use enhanced Furo + AutoAPI config from templates directory
    import shutil

    conf_backup = DOCS_DIR / "conf.py.backup"
    conf_furo_autoapi = (
        DOCS_DIR / "conf_templates" / "conf_furo_with_autoapi.py"
    )  # Enhanced config
    conf_main = DOCS_DIR / "conf.py"

    # Backup original config
    if conf_main.exists():
        shutil.copy2(conf_main, conf_backup)
        session.log("📋 Backed up original conf.py")

    # Copy enhanced Furo + AutoAPI config as main config
    shutil.copy2(conf_furo_autoapi, conf_main)
    session.log("🚀 Activated Enhanced Furo + AutoAPI configuration")

    try:
        # Run sphinx-build with enhanced Furo + AutoAPI config
        session.run(
            "poetry",
            "run",
            "sphinx-build",
            "-b",
            "html",
            str(DOCS_DIR),
            str(output_dir),
            "-v",  # Verbose to see what's happening
            env=env,
            external=True,
        )
    finally:
        # Restore original config
        if conf_backup.exists():
            shutil.copy2(conf_backup, conf_main)
            conf_backup.unlink()  # Clean up backup
            session.log("🔄 Restored original conf.py")

    session.log(f"✅ Enhanced Furo build complete: {output_dir}")
    session.log(f"📄 View: file://{output_dir}/index_furo.html")
    session.log("🎯 This version includes improved TOC navigation!")


@nox.session(name="docs-furo-minimal")
def docs_furo_minimal(session):
    """Ultra-minimal Furo build with NO AutoAPI.

    This tests just the Furo theme without any API generation.

    Usage:
        nox -s docs-furo-minimal
    """
    env = {
        "SPHINX_THEME": "furo",
        "SPHINX_INCLUDE_MCP_DOCS": "false",
        "SPHINX_INCLUDE_READMES": "false",
    }

    output_dir = BUILD_DIR / "furo_minimal"

    session.log("⚡ Ultra-minimal Furo build - NO AutoAPI")

    # Use ultra-minimal Furo config from templates directory
    import shutil

    conf_backup = DOCS_DIR / "conf.py.backup"
    conf_furo_minimal = DOCS_DIR / "conf_templates" / "conf_furo_minimal.py"
    conf_main = DOCS_DIR / "conf.py"

    # Backup and activate ultra-minimal Furo config
    if conf_main.exists():
        shutil.copy2(conf_main, conf_backup)
    shutil.copy2(conf_furo_minimal, conf_main)

    try:
        session.run(
            "poetry",
            "run",
            "sphinx-build",
            "-b",
            "html",
            str(DOCS_DIR),
            str(output_dir),
            "-v",  # Verbose to see what happens
            env=env,
            external=True,
        )
    finally:
        # Restore original config
        if conf_backup.exists():
            shutil.copy2(conf_backup, conf_main)
            conf_backup.unlink()

    session.log(f"✅ Ultra-minimal build complete: {output_dir}")
    session.log(f"📄 View: file://{output_dir}/index.html")


@nox.session(name="docs-furo-full")
def docs_furo_full(session):
    """Build documentation with full haive-core package.

    Usage:
        nox -s docs-furo-full
    """
    # Environment variables for full core build
    env = {
        "SPHINX_PACKAGES": "core",  # Full core package
        "SPHINX_THEME": "furo",
        "SPHINX_INCLUDE_MCP_DOCS": "false",
        "SPHINX_INCLUDE_READMES": "false",
    }

    output_dir = BUILD_DIR / "furo_full"

    session.log("🎨 Building Furo + AutoAPI (FULL CORE)...")
    session.log("📦 Package: haive-core (complete)")
    session.log("⚠️  This will take longer than the engine-only build")

    # Use Furo + AutoAPI config temporarily
    import shutil

    conf_backup = DOCS_DIR / "conf.py.backup"
    conf_furo_autoapi = DOCS_DIR / "conf_templates" / "conf_furo_with_autoapi.py"
    conf_main = DOCS_DIR / "conf.py"

    # Backup original config
    if conf_main.exists():
        shutil.copy2(conf_main, conf_backup)
        session.log("📋 Backed up original conf.py")

    # Copy Furo + AutoAPI config as main config
    shutil.copy2(conf_furo_autoapi, conf_main)
    session.log("🎨 Activated Furo + AutoAPI configuration")

    try:
        # Run sphinx-build with Furo + AutoAPI config
        session.run(
            "poetry",
            "run",
            "sphinx-build",
            "-b",
            "html",
            str(DOCS_DIR),
            str(output_dir),
            "-v",  # Verbose to see what's happening
            env=env,
            external=True,
        )
    finally:
        # Restore original config
        if conf_backup.exists():
            shutil.copy2(conf_backup, conf_main)
            conf_backup.unlink()  # Clean up backup
            session.log("🔄 Restored original conf.py")

    session.log(f"✅ Full Furo + AutoAPI build complete: {output_dir}")
    session.log(f"📄 View: file://{output_dir}/index.html")


@nox.session(name="docs-furo-serve")
def docs_furo_serve(session):
    """Build with Furo and serve locally.

    Usage:
        nox -s docs-furo-serve
    """
    import subprocess
    import time

    # First build - use fast engine-only build
    env = {
        "SPHINX_PACKAGES": "core.engine",
        "SPHINX_THEME": "furo",
        "SPHINX_INCLUDE_MCP_DOCS": "false",
        "SPHINX_INCLUDE_READMES": "false",
    }

    output_dir = BUILD_DIR / "furo"

    session.log("🎨 Building Furo documentation (engine only for speed)...")

    # Use Furo + AutoAPI config temporarily
    import shutil

    conf_backup = DOCS_DIR / "conf.py.backup"
    conf_furo_autoapi = DOCS_DIR / "conf_templates" / "conf_furo_with_autoapi.py"
    conf_main = DOCS_DIR / "conf.py"

    # Backup and activate Furo config
    if conf_main.exists():
        shutil.copy2(conf_main, conf_backup)
    shutil.copy2(conf_furo_autoapi, conf_main)

    try:
        session.run(
            "poetry",
            "run",
            "sphinx-build",
            "-b",
            "html",
            str(DOCS_DIR),
            str(output_dir),
            env=env,
            external=True,
        )
    finally:
        # Restore original config
        if conf_backup.exists():
            shutil.copy2(conf_backup, conf_main)
            conf_backup.unlink()

    # Serve
    session.log("🚀 Starting local server...")
    session.log(f"📄 Open: http://localhost:8003")

    try:
        subprocess.run(
            ["python", "-m", "http.server", "8003", "--directory", str(output_dir)],
            check=True,
        )
    except KeyboardInterrupt:
        session.log("👋 Server stopped")


@nox.session(name="docs-furo-fixed")
def docs_furo_fixed(session):
    """Build documentation with FIXED Furo + AutoAPI (no autosummary conflicts).

    This version uses a minimal extension set to avoid autosummary errors.

    Usage:
        nox -s docs-furo-fixed
    """
    # Environment variables for fixed Furo build
    env = {
        "SPHINX_PACKAGES": "core.engine",  # Just engine for speed
        "SPHINX_THEME": "furo",
        "SPHINX_INCLUDE_MCP_DOCS": "false",
        "SPHINX_INCLUDE_READMES": "false",
    }

    output_dir = BUILD_DIR / "furo_fixed"

    session.log("🚀 Building FIXED Furo + AutoAPI (no autosummary conflicts)...")
    session.log("📦 Submodule: haive.core.engine (fast build)")
    session.log("🔧 Minimal extensions to avoid conflicts")
    session.log("✅ No autosummary, no sphinx_automodapi")

    # Use fixed Furo config from templates directory
    import shutil

    conf_backup = DOCS_DIR / "conf.py.backup"
    conf_furo_fixed = (
        DOCS_DIR / "conf_templates" / "conf_furo_minimal_fixed.py"
    )  # Fixed config
    conf_main = DOCS_DIR / "conf.py"

    # Backup original config
    if conf_main.exists():
        shutil.copy2(conf_main, conf_backup)
        session.log("📋 Backed up original conf.py")

    # Copy fixed Furo config as main config
    shutil.copy2(conf_furo_fixed, conf_main)
    session.log("🚀 Activated FIXED Furo configuration")

    try:
        # Run sphinx-build with fixed Furo config
        session.run(
            "poetry",
            "run",
            "sphinx-build",
            "-b",
            "html",
            str(DOCS_DIR),
            str(output_dir),
            "-v",  # Verbose to see what's happening
            env=env,
            external=True,
        )
    finally:
        # Restore original config
        if conf_backup.exists():
            shutil.copy2(conf_backup, conf_main)
            conf_backup.unlink()  # Clean up backup
            session.log("🔄 Restored original conf.py")

    session.log(f"✅ FIXED Furo build complete: {output_dir}")
    session.log(f"📄 View: file://{output_dir}/index_furo.html")
    session.log("🎯 This version should have NO autosummary errors!")


@nox.session(name="docs-furo-core")
def docs_furo_core(session):
    """Build documentation for haive-core ONLY with Furo theme.

    This avoids all agent documentation that causes autosummary errors.

    Usage:
        nox -s docs-furo-core
    """
    # Environment variables for core-only build
    env = {
        "SPHINX_PACKAGES": "core",  # Just core package
        "SPHINX_THEME": "furo",
        "SPHINX_INCLUDE_MCP_DOCS": "false",
        "SPHINX_INCLUDE_READMES": "false",
    }

    output_dir = BUILD_DIR / "furo_core"

    session.log("🎯 Building haive-core ONLY documentation...")
    session.log("📦 Package: haive-core (no agents)")
    session.log("✅ Avoiding all autosummary conflicts")

    # Use core-only Furo config
    import shutil

    conf_backup = DOCS_DIR / "conf.py.backup"
    conf_furo_core = DOCS_DIR / "conf_templates" / "conf_furo_core_only.py"
    conf_main = DOCS_DIR / "conf.py"

    # Also need to update master_doc in the config
    index_backup = DOCS_DIR / "index.rst.backup"
    index_core = DOCS_DIR / "index_core_only.rst"
    index_main = DOCS_DIR / "index.rst"

    # Clean up API directory - move non-core stuff to backup
    api_dir = DOCS_DIR / "api"
    api_backup_dir = DOCS_DIR / "api_backup"
    api_backup_dir.mkdir(exist_ok=True)

    # Move non-core API directories
    for item in api_dir.iterdir():
        if item.is_dir() and item.name != "haive" and item.name != "api_backup":
            target = api_backup_dir / item.name
            if target.exists():
                shutil.rmtree(target)  # Remove if already exists
            shutil.move(str(item), str(target))
            session.log(f"📦 Moved {item.name} to backup")

    # Replace autosummary files with clean versions
    haive_index = api_dir / "haive" / "index.rst"
    haive_index_clean = api_dir / "haive" / "index_clean.rst"
    if haive_index_clean.exists():
        shutil.copy2(haive_index_clean, haive_index)
        session.log("📄 Using clean haive index without autosummary")

    api_index = api_dir / "index.rst"
    api_index_clean = api_dir / "index_core_only.rst"
    if api_index_clean.exists():
        shutil.copy2(api_index_clean, api_index)
        session.log("📄 Using clean API index for core only")

    # Backup original files
    if conf_main.exists():
        shutil.copy2(conf_main, conf_backup)
        session.log("📋 Backed up original conf.py")

    # Copy core-only config
    shutil.copy2(conf_furo_core, conf_main)
    session.log("🎯 Activated core-only Furo configuration")

    # Update the config to use core-only index
    with open(conf_main, "r") as f:
        config_content = f.read()
    config_content = config_content.replace(
        'master_doc = "index_furo_clean"', 'master_doc = "index_core_only"'
    )
    with open(conf_main, "w") as f:
        f.write(config_content)

    try:
        # Run sphinx-build with core-only config
        session.run(
            "poetry",
            "run",
            "sphinx-build",
            "-b",
            "html",
            str(DOCS_DIR),
            str(output_dir),
            "-v",  # Verbose to see what's happening
            env=env,
            external=True,
        )
    finally:
        # Restore original config
        if conf_backup.exists():
            shutil.copy2(conf_backup, conf_main)
            conf_backup.unlink()
            session.log("🔄 Restored original conf.py")

    session.log(f"✅ Core-only Furo build complete: {output_dir}")
    session.log(f"📄 View: file://{output_dir}/index_core_only.html")
    session.log("🎯 This build contains ONLY haive-core documentation!")


@nox.session(name="docs-furo-core-clean")
def docs_furo_core_clean(session):
    """Build haive-core documentation with CLEAN AutoAPI setup.

    This uses a fresh api_clean directory and avoids all agent-related files.

    Usage:
        nox -s docs-furo-core-clean
    """
    # Environment variables for clean core build
    env = {
        "SPHINX_PACKAGES": "core",
        "SPHINX_THEME": "furo",
        "SPHINX_INCLUDE_MCP_DOCS": "false",
        "SPHINX_INCLUDE_READMES": "false",
    }

    output_dir = BUILD_DIR / "furo_core_clean"

    session.log("🧹 Building CLEAN haive-core with AutoAPI...")
    session.log("📦 Package: haive-core (complete)")
    session.log("✅ Using fresh api_clean directory")
    session.log("🚫 Avoiding all agent-related files")

    # Clean up any existing API directories
    api_clean_dir = DOCS_DIR / "api_clean"
    if api_clean_dir.exists():
        import shutil

        shutil.rmtree(api_clean_dir)
        session.log("🗑️  Removed old api_clean directory")

    # Use clean core config
    import shutil

    conf_backup = DOCS_DIR / "conf.py.backup"
    conf_furo_clean = DOCS_DIR / "conf_templates" / "conf_furo_core_clean.py"
    conf_main = DOCS_DIR / "conf.py"

    # Backup original config
    if conf_main.exists():
        shutil.copy2(conf_main, conf_backup)
        session.log("📋 Backed up original conf.py")

    # Copy clean config
    shutil.copy2(conf_furo_clean, conf_main)
    session.log("🧹 Activated CLEAN core configuration")

    try:
        # Run sphinx-build with clean config
        session.run(
            "poetry",
            "run",
            "sphinx-build",
            "-b",
            "html",
            str(DOCS_DIR),
            str(output_dir),
            "-v",  # Verbose to see what's happening
            env=env,
            external=True,
        )
    finally:
        # Restore original config
        if conf_backup.exists():
            shutil.copy2(conf_backup, conf_main)
            conf_backup.unlink()
            session.log("🔄 Restored original conf.py")

    session.log(f"✅ CLEAN core build complete: {output_dir}")
    session.log(f"📄 View: file://{output_dir}/index_core_only.html")
    session.log("🎯 This build should have working AutoAPI without autosummary errors!")


@nox.session(name="docs-furo-test")
def docs_furo_test(session):
    """Ultra-minimal test build to isolate autosummary issues.

    This bypasses AutoAPI entirely to test if autosummary is the root cause.

    Usage:
        nox -s docs-furo-test
    """
    # Environment variables for test build
    env = {
        "SPHINX_THEME": "furo",
        "SPHINX_INCLUDE_MCP_DOCS": "false",
        "SPHINX_INCLUDE_READMES": "false",
    }

    output_dir = BUILD_DIR / "furo_test"

    session.log("🧪 Ultra-minimal test build (NO AutoAPI)...")
    session.log("✅ This will isolate autosummary issues")

    # Use ultra-minimal config
    import shutil

    conf_backup = DOCS_DIR / "conf.py.backup"
    conf_ultra_minimal = DOCS_DIR / "conf_templates" / "conf_ultra_minimal.py"
    conf_main = DOCS_DIR / "conf.py"

    # Backup original config
    if conf_main.exists():
        shutil.copy2(conf_main, conf_backup)
        session.log("📋 Backed up original conf.py")

    # Copy ultra-minimal config
    shutil.copy2(conf_ultra_minimal, conf_main)
    session.log("🧪 Activated ultra-minimal configuration (NO AutoAPI)")

    try:
        # Run sphinx-build with ultra-minimal config
        session.run(
            "poetry",
            "run",
            "sphinx-build",
            "-b",
            "html",
            str(DOCS_DIR),
            str(output_dir),
            "-v",  # Verbose to see what's happening
            env=env,
            external=True,
        )
    finally:
        # Restore original config
        if conf_backup.exists():
            shutil.copy2(conf_backup, conf_main)
            conf_backup.unlink()
            session.log("🔄 Restored original conf.py")

    session.log(f"✅ Ultra-minimal test build complete: {output_dir}")
    session.log(f"📄 View: file://{output_dir}/index_core_only.html")
    session.log("🎯 If this works, the issue is with AutoAPI or extensions!")


@nox.session(name="docs-furo-clean")
def docs_furo_clean(session):
    """Clean Furo build artifacts.

    Usage:
        nox -s docs-furo-clean
    """
    import shutil

    clean_dirs = [
        BUILD_DIR / "furo",
        BUILD_DIR / "furo_original",
        BUILD_DIR / "furo_enhanced",
        BUILD_DIR / "furo_minimal",
        BUILD_DIR / "furo_full",
        BUILD_DIR / "furo_test",
        DOCS_DIR / "api",  # Remove generated API files
    ]

    session.log("🧹 Cleaning Furo build artifacts...")

    for dir_path in clean_dirs:
        if dir_path.exists():
            shutil.rmtree(dir_path)
            session.log(f"  ✅ Removed: {dir_path}")

    session.log("✨ Furo build directories cleaned")
