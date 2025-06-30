# docs/source/conf.py
"""Sphinx configuration for Haive documentation.

This configuration handles:
- Poetry monorepo structure with multiple packages
- Autosummary generation for API documentation
- Custom templates and styling
- Agent run capture and display
- README integration
"""

from datetime import datetime
import logging
from pathlib import Path
import sys
from typing import Any
import warnings


# Suppress warnings
warnings.filterwarnings("ignore")

# -- Path setup --------------------------------------------------------------
# Get workspace root (docs/source/conf.py -> workspace root)
workspace_root = Path(__file__).resolve().parents[2]
docs_root = Path(__file__).resolve().parent.parent  # docs directory
source_root = Path(__file__).resolve().parent  # source directory

# Create necessary directories
build_dir = docs_root / "build"
build_dir.mkdir(exist_ok=True)

# Configure logging
log_file = build_dir / "sphinx-import-errors.log"
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(str(log_file), mode="w"), logging.StreamHandler()],
)

# -- Path setup for Poetry monorepo ------------------------------------------
# CRITICAL: Add all package paths to sys.path for Poetry monorepo structure
packages_dir = workspace_root / "packages"
package_names = [
    "haive-core",
    "haive-agents",
    "haive-tools",
    "haive-games",
    "haive-dataflow",
    "haive-prebuilt",
    "haive-mcp",
]

# Add each package's src directory to Python path
for package_name in package_names:
    package_path = packages_dir / package_name / "src"
    if package_path.exists():
        sys.path.insert(0, str(package_path))
        logging.info(f"Added to path: {package_path}")
    else:
        logging.warning(f"Package path not found: {package_path}")

# Also add the main src if it exists
main_src = workspace_root / "src"
if main_src.exists():
    sys.path.insert(0, str(main_src))

# Add specific fixes for problematic package paths
dataflow_path = packages_dir / "haive-dataflow" / "src"
if dataflow_path.exists():
    sys.path.insert(0, str(dataflow_path))
    logging.info(f"Added dataflow path: {dataflow_path}")

# Add core haive path if it exists
core_haive_path = workspace_root / "src" / "haive"
if core_haive_path.exists():
    sys.path.insert(0, str(workspace_root / "src"))
    logging.info(f"Added core haive path: {workspace_root / 'src'}")

# -- Project information -----------------------------------------------------
project = "Haive"
copyright = f"2025-{datetime.now().year}, William R. Astley"
author = "William R. Astley"
release = "1.0.0"
version = "1.0"

# Add extensions directory to path
sys.path.insert(0, str(source_root / "_extensions"))

# -- General configuration ---------------------------------------------------
extensions = [
    # Sphinx built-in
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.graphviz",
    "sphinx.ext.ifconfig",
    # Third-party extensions
    "sphinx_copybutton",
    "sphinx_tabs.tabs",
    "sphinx_design",
    "myst_parser",
    "sphinxcontrib.mermaid",
    "sphinx_togglebutton",
    # Custom Haive extensions
    "haive_sphinx_ext",
]

# Template paths
templates_path = ["_templates"]

# -- Autodoc configuration ---------------------------------------------------
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "special-members": "__init__",
    "member-order": "bysource",
    "exclude-members": "__weakref__,__dict__,__module__,__annotations__",
}
autodoc_typehints = "description"
autodoc_typehints_format = "short"
autodoc_inherit_docstrings = True
autodoc_type_aliases = {
    "BaseMessage": "langchain_core.messages.BaseMessage",
    "ToolMessage": "langchain_core.messages.ToolMessage",
}

# Mock imports for external dependencies
autodoc_mock_imports = [
    # LangChain and related
    "langchain",
    "langchain_core",
    "langchain_community",
    "langchain_openai",
    "langgraph",
    "langsmith",
    # Databases
    "neo4j",
    "sqlalchemy",
    "psycopg2",
    "chromadb",
    "faiss",
    "pinecone",
    "weaviate",
    "qdrant_client",
    "elasticsearch",
    "supabase",
    # Data science
    "networkx",
    "numpy",
    "pandas",
    "matplotlib",
    "scipy",
    "torch",
    "transformers",
    "sklearn",
    "scikit-learn",
    "tensorflow",
    "nltk",
    "spacy",
    # LLM providers
    "openai",
    "anthropic",
    "deepseek",
    "mistral",
    "deepinfra",
    "together",
    "replicate",
    "groq",
    "cohere",
    "ai21",
    # UI and visualization
    "textual",
    "rich",
    "gradio",
    "streamlit",
    "dash",
    "plotly",
    # Web and APIs
    "beautifulsoup4",
    "bs4",
    "requests",
    "httpx",
    "aiohttp",
    "PIL",
    "pillow",
    # Development tools
    "jira",
    "github",
    "gitlab",
    "boto3",
    "slack_sdk",
    "pytest",
    # Core dependencies
    "pydantic",
    "pydantic_core",
    "typing_extensions",
    # Additional
    "msgpack",
    "ujson",
    "orjson",
    "python-dotenv",
    "click",
    "typer",
    "tqdm",
    "tenacity",
    "backoff",
    "wrapt",
    "decorator",
    # Haive-specific missing modules
    "haive.tools.base",
    "haive.tools.content",
    "haive.tools.general",
    "haive.tools.google",
    "haive.tools.search",
    "haive.tools.utility",
]

# Modules to skip in autosummary due to import issues
autosummary_skip_modules = [
    # Modules with external service dependencies
    "haive.tools.toolkits.gradio_toolkit",
    "haive.dataflow.db.supabase",
    "haive.core.persistence.supabase_config",
    # Modules with ML dependencies that may cause import issues
    "haive.core.models.embeddings.base",
    "haive.core.engine.embedding.base",
    # Chess game modules (require python-chess)
    "haive.games.chess",
    "haive.games.chess.agent",
    "haive.games.chess.base",
    "haive.games.chess.components",
    # Modules with incomplete implementations
    "haive.agents.multi.base",
    "haive.core.engine.document.universal_loader",
    "haive.core.engine.document.engine",
    "haive.core.engine.retriever.retriever",
    "haive.core.engine.vectorstore.vectorstore",
    # Conversation modules (now fixed but keeping for safety)
    "haive.agents.conversation.social_media",
    # Non-existent modules that were incorrectly listed
    # 'haive.tools.base',      # Removed - doesn't exist
    # 'haive.tools.content',   # Removed - doesn't exist
    # 'haive.tools.general',   # Removed - doesn't exist
    # 'haive.tools.google',    # Removed - doesn't exist
    # 'haive.tools.search',    # Removed - doesn't exist
    # 'haive.tools.utility',   # Removed - doesn't exist
]

# -- Autosummary configuration -----------------------------------------------
# Keep autosummary disabled until modules are fixed (manual docs work fine)
autosummary_generate = False
autosummary_imported_members = False  # Don't document imported members
autosummary_ignore_module_all = False  # Respect __all__
autosummary_generate_overwrite = True  # Always regenerate

# Use a single generated directory to avoid conflicts
autosummary_generate_dir = "generated"

# Custom context for templates
autosummary_context = {
    "beta_status": True,
    "show_module_structure": True,
}

# -- MyST (Markdown) configuration -------------------------------------------
myst_enable_extensions = [
    "deflist",
    "tasklist",
    "html_image",
    "colon_fence",
    "smartquotes",
    "replacements",
    "linkify",
    "strikethrough",
]

# Support both RST and Markdown
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# Master document
master_doc = "index"

# -- Options for HTML output -------------------------------------------------
html_theme = "furo"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_js_files = ["custom.js"]

html_title = "Haive Documentation"
html_short_title = "Haive"
html_copy_source = True
html_show_sourcelink = True

# Theme options
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#2962ff",
        "color-brand-content": "#2962ff",
        "color-api-background": "#F5F5F5",
        "color-api-background-hover": "#EEEEEE",
    },
    "dark_css_variables": {
        "color-brand-primary": "#4fc3f7",
        "color-brand-content": "#4fc3f7",
        "color-api-background": "#1A1A1A",
        "color-api-background-hover": "#2A2A2A",
    },
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "announcement": "📚 This documentation is in BETA and under active development",
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/will-astley/haive",
            "html": "",
            "class": "fa fa-github",
        },
    ],
    "source_repository": "https://github.com/will-astley/haive/",
    "source_branch": "main",
    "source_directory": "docs/",
}

# -- Copy button configuration -----------------------------------------------
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True
copybutton_line_continuation_character = "\\"

# -- Mermaid configuration ---------------------------------------------------
mermaid_version = "10.6.1"

# -- Graphviz configuration --------------------------------------------------
graphviz_output_format = "svg"

# -- Intersphinx configuration -----------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
    "langchain_core": (
        "https://api.python.langchain.com/en/latest/langchain_core/",
        None,
    ),
    "langchain_community": (
        "https://api.python.langchain.com/en/latest/langchain_community/",
        None,
    ),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
}

# -- Napoleon settings (Google docstrings) -----------------------------------
# Enhanced Google-style docstring configuration for better documentation
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_use_keyword = True
napoleon_preprocess_types = True
napoleon_type_aliases = {
    "BaseMessage": "langchain_core.messages.BaseMessage",
    "ToolMessage": "langchain_core.messages.ToolMessage",
    "Dict": "typing.Dict",
    "List": "typing.List",
    "Optional": "typing.Optional",
    "Union": "typing.Union",
    "Any": "typing.Any",
}
napoleon_attr_annotations = True

# -- Todo extension ----------------------------------------------------------
todo_include_todos = True

# -- Haive Extension Configuration -------------------------------------------
haive_agent_showcase = True  # Enable automatic agent showcase generation
haive_readme_discovery = True  # Enable README discovery and integration
haive_agent_runs_dir = "resources/agent_runs"  # Directory for agent run captures

# -- Suppress warnings -------------------------------------------------------
suppress_warnings = [
    "app.add_node",
    "app.add_directive",
    "app.add_role",
    "autosummary",
    "autosummary.import_cycle",
    "autosummary.missing_attribute",
    "autodoc",
    "autodoc.import_object",
    "ref.citation",
    "ref.footnote",
    "misc.highlighting_failure",
]

# -- Exclude patterns --------------------------------------------------------
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**/.git",
    "**/node_modules",
    "**/__pycache__",
    "**/test_*.py",
    "**/tests/**",
    "**/testing/**",
    "**/*_test.py",
    "**/example.py",
    "**/examples/**",
    "**/ui.py",
    "**/ui/**",
    "**/demo.py",
    "**/demos/**",
    "**/*.ipynb",
    "**/*.egg-info/**",
    "generated/**",  # Exclude generated directory from source
]

# -- Custom module filtering -------------------------------------------------
# Track problematic modules
SKIP_MODULES: set[str] = set()
PROCESSED_MODULES: set[str] = set()


def load_skip_list() -> set[str]:
    """Load list of modules to skip from previous builds."""
    skip_file = build_dir / "skip_modules.txt"
    if skip_file.exists():
        with open(skip_file) as f:
            return {line.strip() for line in f if line.strip()}
    return set()


def save_skip_list() -> None:
    """Save list of problematic modules."""
    skip_file = build_dir / "skip_modules.txt"
    with open(skip_file, "w") as f:
        for module in sorted(SKIP_MODULES):
            f.write(f"{module}\n")


# Load previous skip list
SKIP_MODULES = load_skip_list()


def is_valid_module(module_name: str) -> bool:
    """Check if a module should be documented."""
    if module_name in SKIP_MODULES:
        return False

    # Skip test/example/ui modules
    problematic_patterns = [
        "test",
        "tests",
        "testing",
        "_test",
        "example",
        "examples",
        "demo",
        "demos",
        "ui",
        "_ui",
        "gui",
        "__pycache__",
        "experimental",
        "deprecated",
        ".ipynb_checkpoints",
        "tmp",
        "temp",
    ]

    parts = module_name.split(".")
    for part in parts:
        part_lower = part.lower()
        if any(pattern in part_lower for pattern in problematic_patterns):
            SKIP_MODULES.add(module_name)
            return False

    return True


# -- Event handlers ----------------------------------------------------------


def source_read_handler(app, docname: str, source: list[str]) -> None:
    """Process source files before parsing."""
    # Skip problematic documents
    if any(skip in docname for skip in ["example", "test", "ui", "demo"]):
        source[
            0
        ] = f"""
.. note::

   This is an example/test file. Please see the source code for implementation details.
   
   File: ``{docname}``
"""


def process_docstring(
    app, what: str, name: str, obj: Any, options: dict, lines: list[str]
) -> None:
    """Process docstrings to enhance formatting."""
    if not lines:
        return

    # Add beta notice
    if what in ("class", "module") and getattr(
        app.config, "autosummary_context", {}
    ).get("beta_status"):
        beta_notice = [
            "",
            ".. note::",
            "   This API is in BETA and may change in future versions.",
            "",
        ]
        if not any("beta" in line.lower() for line in lines):
            lines.extend(beta_notice)

    # Make parameter names bold
    for i, line in enumerate(lines):
        if line.strip().startswith(":param "):
            parts = line.split(":")
            if len(parts) >= 3:
                param_part = parts[1]  # "param name"
                param_split = param_part.split(" ", 1)
                if len(param_split) == 2:
                    param_name = param_split[1]
                    lines[i] = line.replace(
                        f":param {param_name}:", f":param **{param_name}**:"
                    )


def autodoc_skip_member(
    app, what: str, name: str, obj: Any, skip: bool, options: dict
) -> bool | None:
    """Skip certain members from documentation."""
    # Skip test methods
    if name.startswith("test_") or name.endswith("_test"):
        return True

    # Skip private members unless explicitly included
    if name.startswith("_") and not name.startswith("__"):
        return True

    # Skip certain special methods
    if name in ["__weakref__", "__dict__", "__module__", "__annotations__"]:
        return True

    # Skip modules in our skip list
    module_name = getattr(obj, "__module__", "")
    if any(skip_mod in module_name for skip_mod in autosummary_skip_modules):
        return True

    return skip


def autosummary_skip_module(
    app, what: str, name: str, obj: Any, options: dict, lines: list[str]
) -> None:
    """Skip modules that are in our skip list."""
    return name in autosummary_skip_modules


def build_finished_handler(app, exception: Exception | None) -> None:
    """Handle build completion."""
    save_skip_list()

    # Log summary
    logging.info("=" * 80)
    logging.info("Build Summary")
    logging.info("=" * 80)
    logging.info(f"Processed {len(PROCESSED_MODULES)} modules successfully")
    logging.info(f"Skipped {len(SKIP_MODULES)} problematic modules")

    if exception:
        logging.error(f"Build failed with exception: {exception}")

    # Write detailed summary
    summary_file = build_dir / "build_summary.txt"
    with open(summary_file, "w") as f:
        f.write("Haive Documentation Build Summary\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Build time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Processed modules: {len(PROCESSED_MODULES)}\n")
        f.write(f"Skipped modules: {len(SKIP_MODULES)}\n\n")

        if SKIP_MODULES:
            f.write("Skipped modules:\n")
            for module in sorted(SKIP_MODULES):
                f.write(f"  - {module}\n")


# -- Setup function ----------------------------------------------------------


def setup(app):
    """Custom Sphinx application setup."""
    # Ensure directories exist
    for dir_name in ["_static", "_templates", "_templates/autosummary"]:
        dir_path = source_root / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)

    # Create single generated directory for autosummary
    generated_dir = source_root / "generated"
    generated_dir.mkdir(exist_ok=True)

    # Create CSS file if missing
    css_file = source_root / "_static" / "custom.css"
    if not css_file.exists():
        css_content = """
/* Haive Documentation Custom CSS */

/* Agent run output styling */
.agent-run-output {
    background-color: var(--color-api-background);
    border: 1px solid var(--color-api-background-hover);
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
    overflow-x: auto;
}

.agent-run-output .run-header {
    font-weight: bold;
    margin-bottom: 0.5rem;
    color: var(--color-brand-primary);
}

.agent-run-output .run-content {
    font-family: monospace;
    white-space: pre-wrap;
    font-size: 0.9em;
}

/* Pagination controls */
.pagination-controls {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    margin: 1rem 0;
}

.pagination-controls button {
    background-color: var(--color-brand-primary);
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
}

.pagination-controls button:hover {
    opacity: 0.8;
}

.pagination-controls button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* Graph visualization */
.agent-graph {
    text-align: center;
    margin: 2rem 0;
}

.agent-graph img {
    max-width: 100%;
    height: auto;
    border: 1px solid var(--color-api-background-hover);
    border-radius: 8px;
}

/* Beta notice styling */
.beta-notice {
    background-color: #fff3cd;
    border: 1px solid #ffeaa7;
    border-radius: 4px;
    padding: 0.75rem 1rem;
    margin: 1rem 0;
}

.dark .beta-notice {
    background-color: #3e3e17;
    border-color: #5a5a26;
}
"""
        css_file.write_text(css_content)

    # Create JS file if missing
    js_file = source_root / "_static" / "custom.js"
    if not js_file.exists():
        js_content = """
// Haive Documentation Custom JavaScript

console.log('Haive documentation loaded!');

// Agent run output pagination
document.addEventListener('DOMContentLoaded', function() {
    // Initialize pagination for agent run outputs
    const runOutputs = document.querySelectorAll('.agent-run-output[data-paginated="true"]');
    
    runOutputs.forEach(output => {
        const content = output.querySelector('.run-content');
        const pageSize = parseInt(output.dataset.pageSize || '50');
        const lines = content.textContent.split('\\n');
        
        let currentPage = 0;
        const totalPages = Math.ceil(lines.length / pageSize);
        
        function showPage(page) {
            const start = page * pageSize;
            const end = start + pageSize;
            const pageLines = lines.slice(start, end);
            content.textContent = pageLines.join('\\n');

            // Update controls
            const prevBtn = output.querySelector('.prev-page');
            const nextBtn = output.querySelector('.next-page');
            const pageInfo = output.querySelector('.page-info');

            if (prevBtn) prevBtn.disabled = page === 0;
            if (nextBtn) nextBtn.disabled = page === totalPages - 1;
            if (pageInfo) pageInfo.textContent = `Page ${page + 1} of ${totalPages}`;
        }

        // Add pagination controls
        if (totalPages > 1) {
            const controls = document.createElement('div');
            controls.className = 'pagination-controls';
            controls.innerHTML = `
                <button class="prev-page">Previous</button>
                <span class="page-info">Page 1 of ${totalPages}</span>
                <button class="next-page">Next</button>
            `;

            output.appendChild(controls);

            controls.querySelector('.prev-page').addEventListener('click', () => {
                if (currentPage > 0) {
                    currentPage--;
                    showPage(currentPage);
                }
            });

            controls.querySelector('.next-page').addEventListener('click', () => {
                if (currentPage < totalPages - 1) {
                    currentPage++;
                    showPage(currentPage);
                }
            });

            // Show first page
            showPage(0);
        }
    });
});

// Smooth scrolling for internal links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
"""
        js_file.write_text(js_content)

    # Connect event handlers
    app.connect("source-read", source_read_handler)
    app.connect("autodoc-process-docstring", process_docstring)
    app.connect("autodoc-skip-member", autodoc_skip_member)
    app.connect("build-finished", build_finished_handler)

    # Add configuration values
    app.add_config_value("haive_skip_modules", SKIP_MODULES, "env")
    app.add_config_value("haive_capture_runs", True, "env")
    app.add_config_value("haive_readme_discovery", True, "env")

    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
