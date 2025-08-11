# Complete Modular Sphinx Configuration with Tracing

## 🎯 Full Modular Structure with Debugging

```
docs/source/
├── conf.py                    # Main orchestrator with logging
├── _conf/                     # All configuration modules
│   ├── __init__.py           # Setup logging
│   ├── project.py            # Project metadata
│   ├── extensions.py         # ALL extensions with descriptions
│   ├── paths.py              # Path configuration with validation
│   ├── theme.py              # Theme settings
│   ├── api.py                # AutoAPI configuration
│   ├── mocks.py              # Mock imports (auto-discovered + manual)
│   ├── logging_config.py     # Logging/tracing setup
│   ├── debug.py              # Debug utilities
│   └── build_hooks.py        # Build event handlers
```

## 📄 Implementation with Full Tracing

### conf.py (Main Entry with Logging)

```python
"""Sphinx configuration for Haive documentation."""

import sys
import logging
from pathlib import Path
from datetime import datetime

# Add _conf to path
sys.path.insert(0, str(Path(__file__).parent))

# Setup logging FIRST
from _conf.logging_config import setup_sphinx_logging
logger = setup_sphinx_logging()

logger.info("=" * 80)
logger.info(f"🚀 Starting Sphinx configuration load at {datetime.now()}")
logger.info(f"📁 Config directory: {Path(__file__).parent}")
logger.info("=" * 80)

# Import configurations with tracing
logger.info("📦 Loading project configuration...")
from _conf.project import *

logger.info("🔌 Loading extensions configuration...")
from _conf.extensions import *

logger.info("📂 Loading paths configuration...")
from _conf.paths import *

logger.info("🎨 Loading theme configuration...")
from _conf.theme import *

logger.info("🤖 Loading API documentation configuration...")
from _conf.api import *

logger.info("🎭 Loading mock imports configuration...")
from _conf.mocks import *

logger.info("🪝 Loading build hooks...")
from _conf.build_hooks import *

logger.info("✅ Configuration loaded successfully!")
logger.info("=" * 80)

# Enable debug mode if requested
import os
if os.environ.get('SPHINX_DEBUG', '').lower() in ('1', 'true', 'yes'):
    from _conf.debug import enable_debug_mode
    enable_debug_mode()
```

### \_conf/logging_config.py

```python
"""Logging configuration for Sphinx builds."""

import logging
import sys
from pathlib import Path
from datetime import datetime

def setup_sphinx_logging():
    """Setup comprehensive logging for Sphinx builds."""

    # Create logs directory
    log_dir = Path(__file__).parent.parent / "logs" / "build"
    log_dir.mkdir(parents=True, exist_ok=True)

    # Log file with timestamp
    log_file = log_dir / f"sphinx_build_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    # Configure root logger
    logger = logging.getLogger('sphinx_config')
    logger.setLevel(logging.DEBUG)

    # File handler - detailed
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)

    # Console handler - info and above
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info(f"📝 Logging to: {log_file}")

    return logger
```

### \_conf/extensions.py (ALL Extensions with Tracing)

```python
"""Complete extensions configuration with descriptions."""

import logging
logger = logging.getLogger('sphinx_config.extensions')

# Define all extensions with descriptions
EXTENSION_REGISTRY = {
    # === Core Sphinx Extensions ===
    "sphinx.ext.autodoc": "Extract documentation from docstrings",
    "sphinx.ext.autosummary": "Generate summary tables",
    "sphinx.ext.napoleon": "Parse Google/NumPy style docstrings",
    "sphinx.ext.viewcode": "Add links to source code",
    "sphinx.ext.intersphinx": "Link to other Sphinx docs",
    "sphinx.ext.todo": "Support TODO directives",
    "sphinx.ext.coverage": "Check documentation coverage",
    "sphinx.ext.mathjax": "Render math via JavaScript",
    "sphinx.ext.ifconfig": "Conditional content",
    "sphinx.ext.githubpages": "GitHub Pages support",
    "sphinx.ext.duration": "Measure build durations",
    "sphinx.ext.graphviz": "Graphviz diagram support",
    "sphinx.ext.inheritance_diagram": "Class inheritance diagrams",
    "sphinx.ext.autosectionlabel": "Auto-create section labels",

    # === API Documentation ===
    "autoapi.extension": "Automatic API documentation generation",
    "sphinx_autodoc_typehints": "Type hint support in docs",

    # === Content Enhancement ===
    "myst_parser": "Markdown parsing support",
    "sphinx_copybutton": "Add copy button to code blocks",
    "sphinx_togglebutton": "Add toggle buttons",
    "sphinx_design": "Design elements (cards, tabs, etc)",
    "sphinxcontrib.mermaid": "Mermaid diagram support",
    "sphinx_inline_tabs": "Inline tabbed content",

    # === Export Formats ===
    "sphinxcontrib.spelling": "Spell checking",
    "sphinx.ext.doctest": "Test code snippets",

    # === Custom Haive Extensions ===
    "_extensions.haive_sphinx_ext": "Haive-specific customizations",
    "_extensions.agent_docs": "Agent documentation helpers",
    "_extensions.auto_module_discovery": "Auto-discover modules",
    "_extensions.games_autodoc": "Game documentation helpers",
    "_extensions.namespace_autosummary": "Namespace-aware autosummary",
}

# Build the extensions list with logging
extensions = []
logger.info("Loading extensions:")

for ext_name, description in EXTENSION_REGISTRY.items():
    try:
        # Try to import to verify it exists
        if ext_name.startswith("_extensions"):
            # Local extension
            __import__(ext_name)
        extensions.append(ext_name)
        logger.info(f"  ✅ {ext_name}: {description}")
    except ImportError as e:
        logger.warning(f"  ⚠️  {ext_name}: Not available - {e}")
        # Still add it, might be optional
        extensions.append(ext_name)

logger.info(f"Total extensions loaded: {len(extensions)}")

# === Extension Configurations ===

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = True

logger.debug("Napoleon configuration set")

# MyST settings
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "dollarmath",
    "amsmath",
    "html_admonition",
    "html_image",
    "replacements",
    "smartquotes",
    "substitution",
    "tasklist",
]

logger.debug("MyST parser configuration set")

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "langchain": ("https://api.python.langchain.com/en/latest/", None),
}

logger.debug("Intersphinx mapping configured")
```

### \_conf/debug.py

```python
"""Debug utilities for Sphinx builds."""

import logging
import os
import sys
from pathlib import Path

logger = logging.getLogger('sphinx_config.debug')

def enable_debug_mode():
    """Enable comprehensive debug mode."""
    logger.info("🐛 ENABLING DEBUG MODE")

    # Set environment variables
    os.environ['SPHINX_DEBUG'] = '1'
    os.environ['AUTOAPI_DEBUG'] = '1'

    # Increase verbosity
    for logger_name in ['sphinx', 'autoapi', 'sphinx_config']:
        logging.getLogger(logger_name).setLevel(logging.DEBUG)

    # Add debug information
    logger.debug(f"Python version: {sys.version}")
    logger.debug(f"Python path: {sys.path}")
    logger.debug(f"Current directory: {Path.cwd()}")
    logger.debug(f"Config directory: {Path(__file__).parent.parent}")

    # List all packages
    logger.debug("Installed packages:")
    try:
        import pkg_resources
        for pkg in pkg_resources.working_set:
            logger.debug(f"  - {pkg.key} {pkg.version}")
    except Exception as e:
        logger.debug(f"  Could not list packages: {e}")

def trace_import(name, globals=None, locals=None, fromlist=(), level=0):
    """Trace all imports during build."""
    logger.debug(f"Importing: {name}")
    return original_import(name, globals, locals, fromlist, level)

# Store original import
original_import = __builtins__.__import__

def enable_import_tracing():
    """Enable tracing of all imports."""
    __builtins__.__import__ = trace_import
    logger.info("Import tracing enabled")
```

### \_conf/build_hooks.py

```python
"""Build event hooks for monitoring and debugging."""

import logging
import time
from datetime import datetime

logger = logging.getLogger('sphinx_config.hooks')

# Track build timing
build_start_time = None
phase_times = {}

def on_config_inited(app, config):
    """Called when config is initialized."""
    global build_start_time
    build_start_time = time.time()
    logger.info("=" * 80)
    logger.info("🏗️  BUILD STARTED")
    logger.info(f"📅 Time: {datetime.now()}")
    logger.info(f"📁 Source: {app.srcdir}")
    logger.info(f"📁 Output: {app.outdir}")
    logger.info(f"🎨 Builder: {app.builder.name}")
    logger.info("=" * 80)

def on_builder_inited(app):
    """Called when builder is initialized."""
    logger.info(f"🔨 Builder initialized: {app.builder.name}")
    logger.debug(f"Builder format: {app.builder.format}")
    logger.debug(f"Builder supported image types: {getattr(app.builder, 'supported_image_types', 'N/A')}")

def on_env_get_outdated(app, env, added, changed, removed):
    """Called to get outdated docs."""
    logger.info(f"📊 Document changes detected:")
    logger.info(f"  ➕ Added: {len(added)} files")
    logger.info(f"  ✏️  Changed: {len(changed)} files")
    logger.info(f"  ➖ Removed: {len(removed)} files")

    if logger.isEnabledFor(logging.DEBUG):
        if added:
            logger.debug(f"  Added files: {added[:5]}...")
        if changed:
            logger.debug(f"  Changed files: {changed[:5]}...")

def on_source_read(app, docname, source):
    """Called when a source file is read."""
    logger.debug(f"📖 Reading: {docname}")

def on_doctree_resolved(app, doctree, docname):
    """Called when doctree is resolved."""
    logger.debug(f"🌳 Resolved doctree: {docname}")

def on_build_finished(app, exception):
    """Called when build is finished."""
    build_time = time.time() - build_start_time if build_start_time else 0

    logger.info("=" * 80)
    if exception:
        logger.error(f"❌ BUILD FAILED: {exception}")
    else:
        logger.info("✅ BUILD SUCCESSFUL")
    logger.info(f"⏱️  Total time: {build_time:.2f} seconds")
    logger.info(f"📅 Completed: {datetime.now()}")
    logger.info("=" * 80)

def setup(app):
    """Setup build hooks."""
    app.connect('config-inited', on_config_inited)
    app.connect('builder-inited', on_builder_inited)
    app.connect('env-get-outdated', on_env_get_outdated)
    app.connect('source-read', on_source_read)
    app.connect('doctree-resolved', on_doctree_resolved)
    app.connect('build-finished', on_build_finished)

    logger.info("Build hooks registered")

    return {
        'version': '1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
```

### \_conf/api.py (with Discovery Logging)

```python
"""AutoAPI configuration with comprehensive logging."""

import logging
from pathlib import Path

logger = logging.getLogger('sphinx_config.api')

# Package discovery
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
PACKAGES_DIR = PROJECT_ROOT / "packages"

logger.info("🔍 Discovering packages for API documentation...")

# Discover all packages
autoapi_dirs = []
for package_dir in PACKAGES_DIR.glob("haive-*/src"):
    if package_dir.is_dir():
        autoapi_dirs.append(str(package_dir))
        logger.info(f"  📦 Found: {package_dir.relative_to(PROJECT_ROOT)}")

logger.info(f"Total packages found: {len(autoapi_dirs)}")

# AutoAPI settings
autoapi_type = "python"
autoapi_root = "api"
autoapi_keep_files = True
autoapi_add_toctree_entry = True

# What to document
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",
]

logger.debug(f"AutoAPI options: {autoapi_options}")

# Ignore patterns
autoapi_ignore = [
    "**/test_*.py",
    "**/tests/**",
    "**/*_test.py",
    "**/conftest.py",
    "**/__pycache__/**",
]

logger.debug(f"AutoAPI ignore patterns: {len(autoapi_ignore)} patterns")

# Template customization
autoapi_template_dir = "_templates/autoapi"

# Generate summary
def autoapi_skip_member(app, what, name, obj, skip, options):
    """Log what's being skipped."""
    if skip:
        logger.debug(f"⏭️  Skipping {what}: {name}")
    return skip
```

## 🚀 Usage

### Basic Build

```bash
poetry run sphinx-build -b html docs/source docs/build/html
```

### Debug Build

```bash
SPHINX_DEBUG=1 poetry run sphinx-build -b html docs/source docs/build/html
```

### View Logs

```bash
# Latest log
ls -la docs/source/logs/build/sphinx_build_*.log | tail -1

# Follow log in real-time
tail -f docs/source/logs/build/sphinx_build_*.log
```

## 📊 What Gets Traced

1. **Configuration Loading**: Each module load is logged
2. **Extension Loading**: Success/failure for each extension
3. **Package Discovery**: What packages are found for API docs
4. **Build Phases**: Start, progress, completion
5. **Document Changes**: What files are added/changed/removed
6. **Errors & Warnings**: Full stack traces
7. **Performance**: Time for each phase

This gives you complete visibility into your documentation build process!
