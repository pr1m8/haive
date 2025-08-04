"""Complete Sphinx configuration with all extensions and packages."""

import os
import sys
from pathlib import Path

# Add conf_modules to Python path for imports
conf_modules_dir = Path(__file__).parent / "conf_modules"
sys.path.insert(0, str(conf_modules_dir))

from extension_configs import (get_all_extension_configs,
                               get_conditional_configs)
from extensions import get_all_extensions, test_extension_compatibility
from import_diagnostics import get_autodoc_mock_imports_from_diagnosis
from memory import get_memory_safe_sphinx_config, monitor_sphinx_build

# =============================================================================
# PROJECT INFORMATION
# =============================================================================

# Get packages to build from environment (will be set later in the file)
_sphinx_packages = os.environ.get('SPHINX_PACKAGES', 'all')

# Update project name based on what we're building
if _sphinx_packages != 'all':
    pkg_names = [p.strip().replace('haive-', '') for p in _sphinx_packages.split(',')]
    project = f"Haive {', '.join(p.title() for p in pkg_names)}"
else:
    project = "Haive AI Agent Framework"

copyright = "2024, Haive Team"
author = "Haive Team"
version = "1.0"
release = "1.0.0"

# =============================================================================
# GENERAL CONFIGURATION
# =============================================================================

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
pygments_style = "sphinx"

# =============================================================================
# EXTENSIONS - IMPORTED FROM MODULAR STRUCTURE WITH TESTING
# =============================================================================

# Get build profile from environment (default: full)
SPHINX_PROFILE = os.environ.get('SPHINX_PROFILE', 'full')

# Control example execution (set SPHINX_DISABLE_EXAMPLES=1 to skip computational examples)
DISABLE_EXAMPLES = os.environ.get('SPHINX_DISABLE_EXAMPLES', '0').lower() in ('1', 'true', 'yes')

# Select extensions based on profile
if SPHINX_PROFILE == 'minimal':
    # Minimal set for fast builds
    extensions = [
        "sphinx.ext.autodoc",
        "sphinx.ext.napoleon",
        "sphinx.ext.viewcode",
        "sphinx.ext.intersphinx",
        "autoapi.extension",
        "myst_parser",
    ]
    print(f"🚀 Using MINIMAL profile ({len(extensions)} extensions)")
elif SPHINX_PROFILE == 'standard':
    # Standard set with common extensions
    from extensions import get_core_sphinx_extensions, get_autoapi_extensions, get_myst_extensions
    extensions = get_core_sphinx_extensions() + get_autoapi_extensions() + get_myst_extensions()
    # Add a few more useful ones
    extensions.extend([
        "sphinx_copybutton",
        "sphinx_design",
        "sphinx_autodoc_typehints",
    ])
    print(f"📚 Using STANDARD profile ({len(extensions)} extensions)")
else:
    # Full set with all extensions
    extensions = get_all_extensions()
    print(f"🎯 Using FULL profile ({len(extensions)} extensions)")

# Apply memory-safe configuration with extension optimization
memory_config = get_memory_safe_sphinx_config(extensions)
extensions = memory_config["extensions"]  # Use memory-optimized extensions
build_recommendations = memory_config["build_recommendations"]

# Remove sphinx_gallery if examples are disabled
if DISABLE_EXAMPLES:
    extensions = [ext for ext in extensions if not ext.startswith('sphinx_gallery')]
    print("🚫 Sphinx Gallery disabled via SPHINX_DISABLE_EXAMPLES")

# Get extension-specific configurations
extension_configs = get_all_extension_configs(extensions)
conditional_configs = get_conditional_configs(extensions)

# Apply all configurations to global namespace
globals().update(memory_config)
globals().update(extension_configs)
globals().update(conditional_configs)

# =============================================================================
# AUTOAPI CONFIGURATION - ALL PACKAGES
# =============================================================================

import os

# Get packages to build from environment (default: all)
SPHINX_PACKAGES = os.environ.get('SPHINX_PACKAGES', 'all')

# All available packages
ALL_PACKAGES = {
    "core": "../../packages/haive-core/src",
    "agents": "../../packages/haive-agents/src",
    "tools": "../../packages/haive-tools/src",
    "games": "../../packages/haive-games/src",
    "dataflow": "../../packages/haive-dataflow/src",
    "mcp": "../../packages/haive-mcp/src",
    "prebuilt": "../../packages/haive-prebuilt/src",
}

autoapi_type = "python"

# Determine which packages to build
if SPHINX_PACKAGES == 'all':
    autoapi_dirs = list(ALL_PACKAGES.values())
    print(f"📦 Building ALL packages ({len(autoapi_dirs)} total)")
else:
    # Build specific packages (comma-separated)
    requested_packages = [p.strip() for p in SPHINX_PACKAGES.split(',')]
    autoapi_dirs = []
    
    for pkg in requested_packages:
        # Support both 'core' and 'haive-core' formats
        pkg_name = pkg.replace('haive-', '') if pkg.startswith('haive-') else pkg
        
        if pkg_name in ALL_PACKAGES:
            autoapi_dirs.append(ALL_PACKAGES[pkg_name])
            print(f"📦 Adding package: haive-{pkg_name}")
        else:
            print(f"⚠️  Unknown package: {pkg}")
    
    if not autoapi_dirs:
        print("❌ No valid packages specified, defaulting to haive-core")
        autoapi_dirs = [ALL_PACKAGES["core"]]

# Automatically diagnose and configure mock imports
autodoc_mock_imports = get_autodoc_mock_imports_from_diagnosis(
    autoapi_dirs, str(Path(__file__).parent)
)
# Add additional mocks for problematic dependencies
autodoc_mock_imports.extend(
    [
        "google_search_results",
        "google-search-results",
        "serpapi",
        "agents",
        "langgraph_supervisor",
        "compiled_state_graph",
        "agent_types",
        "complex_rag",
        "usage_examples",
        "normalize_contents",
        "map_branch",
        "llm_compiler",
        "plan_and_execute",
        "web_nav",
        "SolvabilityStatus",
        "SimpleAgentConfig",
        "tool",
        "task_analysis",
        "react_agent2",
        "from_llms",
        "models",
        "base",
        "WebSource",
        "LocalSource",
        "TypeConverter",
        "Config",
        # Add missing imports from error logs
        "langchain_community.utilities.alpha_vantage",
        "langchain_community.tools",
        "langchain_community.vectorstores",
        "langchain_openai",
        "langgraph.checkpoint.memory",
        "langgraph.graph",
        "langgraph.prebuilt",
        "langgraph.types",
        # Games related
        "haive.games.framework",
        "haive.games.framework.base",
        "haive.games.framework.core",
        # MCP related  
        "mcp",
        "@modelcontextprotocol/sdk",
        # Tools related
        "alpha_vantage",
        "amadeus",
        "azure.cognitiveservices",
        "clickup",
        "financialdatasets",
        "fred",
        "jira",
        "slack_sdk",
        "stackexchange",
        "stripe",
        "twilio",
        "vbible",
        "yugioh",
        # Chain related
        "BranchSpec",
        "haive.agents.chain.declarative_chain",
        # Document loader related
        "examples.usage_examples",
        "normalize_contents",
        # React state related
        "haive.agents.react.state",
        "AgentState",
        # Meta agent related
        "haive.agents.archive.meta.agent",
        "get_summary",
        # Multi agent related
        "haive.agents.multi",
        "haive.agents.simple",
        # Memory related
        "unified_memory_api",
        # Hyde related
        "hyde",
        "hyde.agent",
        "hyde.agent_v2", 
        "hyde.enhanced_agent",
        "hyde.enhanced_agent_v2",
        # Supervisor related
        "langgraph_supervisor",
        "SupervisorReactState",
        # Missing usage examples
        "examples.usage_examples",
        # Missing functions and modules
        "should_refine",
        "kg_extraction_engine",
        "format_search_context",
        "extract_memory_items",
        "check_domain_relevance",
        # Memory modules
        "haive.agents.memory_reorganized.base.memory_models_standalone",
        "haive.agents.memory_reorganized.core.memory_state_original",
        "haive.agents.multi.simple",
        "agents",
        "episodic",
        "procedural", 
        "semantic",
        "react_v2",
        # Experiment modules
        "haive.agents.experiments.supervisor.base_supervisor",
        # Rag modules
        "haive.agents.rag.db_rag.graph_db.agent",
    ]
)

autoapi_root = "api"
autoapi_add_toctree_entry = False
autoapi_generate_api_docs = True
autoapi_python_class_content = "both"
autoapi_member_order = "bysource"
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "special-members",
    "imported-members",
]

# Skip patterns to avoid problematic files during documentation generation
autoapi_ignore = [
    # Skip ALL example and test files
    "**/examples/**/*.py",
    "**/example*.py",
    "**/*example*.py",
    "**/demos/**/*.py",
    "**/demo*.py",
    "**/test*.py",
    "**/tests/**/*.py",
    # Skip auto-generated example galleries and archives
    "**/auto_examples/**",
    "**/archive/**",
    "**/archives/**",
    "**/packages/*/archive/**",
    "**/packages/*/archives/**",
    # Skip app.py files that cause logger issues
    "**/app.py",
    "**/app/**/*.py",
    # Skip files with generic class patterns that cause TypeError
    "**/supervisor/dynamic_activation_supervisor.py",
    "**/multi/experiments/implementations/*.py",
    "**/research/reasoning_agent.py",
    "**/planning/planning_agent.py",
    "**/multi/base_multi_agent.py",
    "**/multi/enhanced_multi_agent_v3.py",
    "**/multi/enhanced_multi_agent_v4.py",
    "**/memory_v2/test_*.py",
    "**/discovery/semantic_discovery.py",
    "**/discovery/dynamic_tool_selector.py",
    "**/discovery/selection_strategies.py",
    # Skip problematic research and wiki-related agents
    "**/research/**/*.py",
    "**/tools/search/wikipedia_search.py",
    "**/tools/search/arxiv_search.py",
    "**/tools/search/semantic_search.py",
    "**/agents/research/**/*.py",
    "**/agents/document_processing/**/*.py",
    # Modules with missing core dependencies
    "**/agents/base/compiled_agent.py",
    "**/agents/base/universal_agent.py",
    "**/agents/archive/meta/**/*.py",
    # Modules with Pydantic validation errors
    "**/agents/memory_v2/**/*.py",
    # Modules with missing imports
    "**/agents/chain/**/*.py",
    "**/agents/conversation/base/example*.py",
    "**/agents/document_loader/examples/**/*.py",
    "**/agents/document_modifiers/kg/**/*.py",
    "**/agents/experiments/**/*.py",
    "**/agents/memory/models_dir/**/*.py",
    # Chain agent - BranchSpec issues
    "**/chain/**/*.py",
    # Long term memory - AgentState issues
    "**/agents/long_term_memory/**/*.py",
    # Archive meta - get_summary issues
    "**/agents/archive/**/*.py",
    # Multi-agent modules with various issues
    "**/agents/multi/archive/**/*.py",
    "**/agents/multi/enhanced_clean_multi_agent.py",
    # Tools with missing dependencies
    "**/tools/google/google_finance.py",
    "**/tools/google/google_jobs.py",
    "**/tools/google/google_scholar.py",
    "**/tools/google/google_trends.py",
    # Search tools with issues
    "**/tools/search/**/*.py",
    # Reasoning and wiki agents
    "**/agents/reasoning_and_critique/**/*.py",
    "**/agents/wiki_writer/**/*.py",
    # Hyde agents with import issues (complex dependencies)
    "**/agents/rag/hyde/**/*.py",
    "**/rag/hyde/**/*.py",
    # Conversation examples with generic type issues
    "**/agents/conversation/base/example*.py",
    # Experiment modules with generic type issues
    "**/agents/experiments/**/*.py",
    # Memory modules with complex issues
    "**/agents/memory/models_dir/**/*.py",
    "**/agents/memory/search/**/*.py",
    "**/agents/memory_reorganized/**/*.py",
    "**/agents/memory_v2/**/*.py",
    # Multi-agent archive with complex issues
    "**/agents/multi/archive/**/*.py",
    # React class modules with complex import issues
    "**/agents/react_class/**/*.py",
]


# Preprocessing hook to handle Agent[T] pattern
def autoapi_skip_member(app, what, name, obj, skip, options):
    """Skip or modify problematic members."""
    return skip


def force_load_lazy_imports():
    """Force load lazy imports before documentation generation."""
    import importlib
    import sys

    # Force load provider classes
    try:
        providers_module = importlib.import_module("haive.core.models.llm.providers")
        if hasattr(providers_module, "__all__"):
            for name in providers_module.__all__:
                try:
                    getattr(providers_module, name)
                except Exception:
                    pass
    except Exception as e:
        print(f"Could not preload providers: {e}")

    # Force load retriever/vectorstore configs
    try:
        retriever_module = importlib.import_module("haive.core.models.retriever")
        if hasattr(retriever_module, "__all__"):
            for name in retriever_module.__all__:
                try:
                    getattr(retriever_module, name)
                except Exception:
                    pass
    except Exception as e:
        print(f"Could not preload retrievers: {e}")

    try:
        vectorstore_module = importlib.import_module("haive.core.models.vectorstore")
        if hasattr(vectorstore_module, "__all__"):
            for name in vectorstore_module.__all__:
                try:
                    getattr(vectorstore_module, name)
                except Exception:
                    pass
    except Exception as e:
        print(f"Could not preload vectorstores: {e}")


# Call this before autoapi runs
force_load_lazy_imports()

# =============================================================================
# JSMATH CONFIGURATION
# =============================================================================
jsmath_path = "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS-MML_HTMLorMML"

# =============================================================================
# HTML THEME CONFIGURATION
# =============================================================================

html_theme = "furo"
html_title = f"{project} Documentation"
html_short_title = "Haive Docs"

html_theme_options = {
    "source_repository": "https://github.com/yourusername/haive/",
    "source_branch": "main",
    "source_directory": "docs/source/",
    "sidebar_hide_name": True,
    "light_css_variables": {
        "color-brand-primary": "#2563eb",
        "color-brand-content": "#2563eb",
    },
    "dark_css_variables": {
        "color-brand-primary": "#3b82f6",
        "color-brand-content": "#3b82f6",
    },
}

html_static_path = ["_static"]
html_css_files = [
    "custom.css",
    "enhanced-docs.css",
]
html_js_files = ["custom.js"]

# =============================================================================
# MYST CONFIGURATION
# =============================================================================

myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]

myst_heading_anchors = 3
myst_footnote_transition = True
myst_dmath_double_inline = True

# =============================================================================
# AUTODOC CONFIGURATION
# =============================================================================

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}

autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"
autosummary_generate = False  # Disabled to avoid logger issues

# Type hint configuration to handle generics
typehints_fully_qualified = False
autodoc_typehints_format = "short"
autodoc_type_aliases = {
    "Agent": "Agent",
    "T": "T",
}

# Enable better type hint resolution
python_use_unqualified_type_names = True

# Suppress type hint warnings for basic types
suppress_warnings = ["ref.python", "autosummary", "autoapi"]

# =============================================================================
# INTERSPHINX MAPPING
# =============================================================================

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
    "langchain": ("https://python.langchain.com/docs/", None),
    "langchain_core": ("https://api.python.langchain.com/en/latest/", None),
    "openai": ("https://platform.openai.com/docs/", None),
}

# Configure nitpicky mode exceptions for common missing references
nitpicky = True
nitpick_ignore = [
    # Basic Python types
    ("py:class", "str"),
    ("py:class", "int"),
    ("py:class", "bool"),
    ("py:class", "float"),
    ("py:class", "list"),
    ("py:class", "dict"),
    ("py:class", "tuple"),
    ("py:class", "set"),
    ("py:class", "bytes"),
    ("py:class", "None"),
    ("py:class", "type"),
    ("py:class", "object"),
    # Common typing module types
    ("py:class", "Any"),
    ("py:class", "List"),
    ("py:class", "Dict"),
    ("py:class", "Tuple"),
    ("py:class", "Set"),
    ("py:class", "Optional"),
    ("py:class", "Union"),
    ("py:class", "Callable"),
    ("py:class", "Type"),
    ("py:class", "TypeVar"),
    ("py:class", "Generic"),
    ("py:class", "Literal"),
    ("py:class", "Protocol"),
    ("py:class", "TypedDict"),
    # Pydantic types
    ("py:class", "BaseModel"),
    ("py:class", "Field"),
    ("py:class", "SecretStr"),
    ("py:class", "ConfigDict"),
    # LangChain types
    ("py:class", "Document"),
    ("py:class", "BaseMessage"),
    ("py:class", "HumanMessage"),
    ("py:class", "AIMessage"),
    ("py:class", "SystemMessage"),
    ("py:class", "ToolMessage"),
    # Generic type parameters
    ("py:class", "T"),
    ("py:class", "Agent"),
    ("py:class", "TIn"),
    ("py:class", "TOut"),
]

# Set up proper Python domain configuration
python_use_unqualified_type_names = True

# =============================================================================
# ENHANCED DOCUMENTATION FEATURES (Using 86+ Extensions)
# =============================================================================

# Napoleon settings for Google/NumPy style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# Enhanced template directory
templates_path = ["_templates"]

# Sphinx-design configuration
if "sphinx_design" in extensions:
    sd_fontawesome_latex = True

# Enhanced copybutton configuration
if "sphinx_copybutton" in extensions:
    copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
    copybutton_prompt_is_regexp = True
    copybutton_line_continuation_character = "\\"
    copybutton_here_doc_delimiter = "EOT"
    copybutton_selector = "div.highlight > pre"

# Enhanced diagrams
if "sphinxcontrib.mermaid" in extensions:
    mermaid_output_format = "svg"
    mermaid_init_js = """
    mermaid.initialize({
        startOnLoad: true,
        theme: 'default',
        themeVariables: {
            primaryColor: '#2563eb',
            primaryTextColor: '#1f2937',
            primaryBorderColor: '#1d4ed8',
            lineColor: '#374151'
        }
    });
    """

# Enhanced inheritance diagrams
graphviz_output_format = "svg"

# Todo extension settings
todo_include_todos = True
todo_emit_warnings = False

# External TOC
if "sphinx_external_toc" in extensions:
    external_toc_path = "_toc.yml"

# Sitemap
if "sphinx_sitemap" in extensions:
    html_baseurl = "https://haive.readthedocs.io/"
    sitemap_url_scheme = "{link}"

# =============================================================================
# CUSTOM EVENT HANDLERS
# =============================================================================


def setup(app):
    """Setup function for custom Sphinx configuration."""
    app.connect("autoapi-skip-member", autoapi_skip_member)


# =============================================================================
# CONFIGURATION SUMMARY
# =============================================================================

print("✅ COMPLETE Sphinx configuration loaded successfully!")
print(f"📦 Total extensions: {len(extensions)}")
print(f"🎨 Theme: {html_theme}")
print(f"📝 MyST enabled with {len(myst_enable_extensions)} extensions")
print("🔧 AutoAPI configured for all 7 Haive packages")
print(f"⚙️  Extension configs applied: {len(extension_configs)} settings")
print(f"🔄 Conditional configs: {len(conditional_configs)} optimizations")
print("🚀 Full documentation build with ALL extensions active!")
