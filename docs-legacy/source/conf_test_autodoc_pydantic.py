"""Test Sphinx configuration with autodoc-pydantic and all warning fixes."""

from __future__ import annotations

import os
from pathlib import Path
import sys

# Path setup
project_root = Path(__file__).parent.parent.parent
packages_dir = project_root / "packages"
sys.path.insert(0, str(packages_dir / "haive-core/src"))

# Logging with detailed output
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("sphinx_config_test")

# =============================================================================
# PROJECT INFORMATION
# =============================================================================

project = "Haive AI Agent Framework"
copyright = "2024, Haive Team"
author = "Haive Team"
version = "1.0"
release = "1.0.0"

# =============================================================================
# GENERAL CONFIGURATION
# =============================================================================

templates_path = ["_templates"]
exclude_patterns = [
    "_build", 
    "Thumbs.db", 
    ".DS_Store",
    "agents/conversation/*.rst",
    "guides/agent_visualization.rst",
]
pygments_style = "sphinx"

# =============================================================================
# EXTENSIONS - INCLUDING AUTODOC-PYDANTIC
# =============================================================================

extensions = [
    # CRITICAL: AutoAPI MUST BE FIRST
    "autoapi.extension",
    
    # Core Sphinx extensions
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.mathjax",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.graphviz",
    
    # Markdown support
    "myst_parser",
    
    # Enhanced features
    "sphinx_copybutton",
    
    # PYDANTIC SUPPORT - Add this to handle Pydantic models properly
    # NOTE: You'll need to install: poetry add --group docs autodoc-pydantic
    # "sphinxcontrib.autodoc_pydantic",  # Uncomment after installing
]

# Verify AutoAPI is first
if extensions[0] != "autoapi.extension":
    raise RuntimeError(f"AutoAPI MUST be first extension, but got: {extensions[0]}")

logger.info(f"✅ AutoAPI confirmed at position 0 with {len(extensions)} total extensions")

# =============================================================================
# AUTOAPI CONFIGURATION - ALL PACKAGES WITH DEBUG
# =============================================================================

ALL_PACKAGES = {
    "core": str(packages_dir / "haive-core/src"),
    "agents": str(packages_dir / "haive-agents/src"), 
    "tools": str(packages_dir / "haive-tools/src"),
    "games": str(packages_dir / "haive-games/src"),
    "dataflow": str(packages_dir / "haive-dataflow/src"),
    "mcp": str(packages_dir / "haive-mcp/src"),
    "prebuilt": str(packages_dir / "haive-prebuilt/src"),
}

autoapi_type = "python"
autoapi_dirs = list(ALL_PACKAGES.values())

# AutoAPI settings
autoapi_root = "api"
autoapi_add_toctree_entry = True
autoapi_generate_api_docs = True
autoapi_python_class_content = "both"
autoapi_member_order = "bysource"
autoapi_keep_files = True
autoapi_python_use_implicit_namespaces = True

# Enhanced options for better debugging
autoapi_options = [
    "members",
    "undoc-members", 
    "show-inheritance",
    "special-members",
    "imported-members",
]

# Add file patterns to process
autoapi_file_patterns = ["*.py"]
autoapi_ignore = []

# =============================================================================
# AUTODOC-PYDANTIC CONFIGURATION (if installed)
# =============================================================================

# Check if autodoc-pydantic is available
try:
    import sphinxcontrib.autodoc_pydantic
    if "sphinxcontrib.autodoc_pydantic" not in extensions:
        extensions.append("sphinxcontrib.autodoc_pydantic")
    
    # Configure autodoc-pydantic
    autodoc_pydantic_model_show_json = False
    autodoc_pydantic_model_show_config_summary = True
    autodoc_pydantic_model_show_validator_members = True
    autodoc_pydantic_model_show_validator_summary = True
    autodoc_pydantic_field_list_validators = True
    autodoc_pydantic_field_show_constraints = True
    autodoc_pydantic_field_doc_policy = "both"  # Show both description and constraints
    autodoc_pydantic_settings_show_json = False
    
    logger.info("✅ autodoc-pydantic extension loaded and configured")
except ImportError:
    logger.warning("⚠️ autodoc-pydantic not installed - run: poetry add --group docs autodoc-pydantic")

# =============================================================================
# ENHANCED AUTOAPI SKIP MEMBER - HANDLE DUPLICATES
# =============================================================================

def autoapi_skip_member(app, what, name, obj, skip, options):
    """Enhanced skip member to prevent duplicate Pydantic documentation."""
    try:
        # Log what we're processing for debugging
        if what == "attribute" and "pydantic" in str(type(obj)).lower():
            logger.debug(f"Processing Pydantic attribute: {name}")
        
        # Skip duplicate Pydantic model internals
        pydantic_internals = [
            "__fields__", "__config__", "__validators__", "__root_validators__",
            "__pre_root_validators__", "__post_root_validators__",
            "__schema_cache__", "__module__", "__annotations__",
            "__pydantic_model__", "__pydantic_fields__", "__pydantic_config__",
            "__pydantic_complete__", "__pydantic_decorators__",
            "__pydantic_fields_set__", "__pydantic_extra__",
            "__pydantic_generic_metadata__", "__pydantic_parent_namespace__",
            "__pydantic_serializer__", "__pydantic_validator__",
            "model_fields", "model_config", "model_computed_fields",
        ]
        
        if what == "attribute" and any(name.endswith(internal) for internal in pydantic_internals):
            logger.debug(f"Skipping Pydantic internal: {name}")
            return True
        
        # Skip duplicate field documentation if autodoc-pydantic is handling it
        if what == "attribute" and "." in name:
            parts = name.split(".")
            if len(parts) >= 2:
                field_name = parts[-1]
                class_path = ".".join(parts[:-1])
                
                # Known Pydantic fields that get duplicated
                duplicate_prone_fields = [
                    "milestones", "risk_factors", "available_tools", 
                    "time_constraints", "constraints", "dependencies",
                    "metadata", "tags", "status", "created_at", "updated_at",
                ]
                
                if field_name in duplicate_prone_fields:
                    # Check if this looks like a Pydantic model
                    if any(keyword in class_path.lower() for keyword in ["model", "schema", "config", "plan", "task"]):
                        logger.debug(f"Skipping duplicate Pydantic field: {name}")
                        return True
        
        # Skip problematic imports that cause errors
        problematic_patterns = [
            'haive.core.schema.prebuilt.messages_state',
            'haive.core.schema.prebuilt.messages.messages_state',
            'haive.agents.base.agent',
            'haive.agents.base',
            'hyde.agent',
            'hyde.enhanced_agent',
            'get_summary',
            'BranchSpec',
            'AgentState',
            'SupervisorReactState',
            'ExtendedHuggingFaceDatasetLoader',
            'HuggingFaceModelCardLoader',
            'VectorStoreConfig',
            'Config',
        ]
        
        if any(pattern in str(name) for pattern in problematic_patterns):
            logger.warning(f"⚠️ Skipping problematic member: {name}")
            return True
        
        return skip
        
    except Exception as e:
        logger.warning(f"⚠️ Error in skip_member for {name}: {e}")
        return True

# =============================================================================
# COMPREHENSIVE NITPICK IGNORE - ALL WARNINGS
# =============================================================================

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
    
    # Typing module
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
    ("py:class", "Annotated"),
    ("py:class", "ClassVar"),
    ("py:class", "Final"),
    ("py:class", "TypeAlias"),
    
    # Pydantic types
    ("py:class", "BaseModel"),
    ("py:class", "Field"),
    ("py:class", "SecretStr"),
    ("py:class", "ConfigDict"),
    ("py:class", "ValidationError"),
    ("py:class", "validator"),
    ("py:class", "root_validator"),
    ("py:class", "PrivateAttr"),
    ("py:class", "BaseSettings"),
    ("py:class", "FieldInfo"),
    ("py:class", "ModelMetaclass"),
    
    # LangChain types - COMPREHENSIVE
    ("py:class", "langchain_core.runnables.RunnableConfig"),
    ("py:class", "langchain_core.runnables.Runnable"),
    ("py:class", "langchain_core.runnables.RunnablePassthrough"),
    ("py:class", "langchain_core.runnables.RunnableLambda"),
    ("py:class", "langchain_core.callbacks.CallbackManagerForLLMRun"),
    ("py:class", "langchain_core.callbacks.CallbackManager"),
    ("py:class", "langchain_core.callbacks.BaseCallbackHandler"),
    ("py:class", "langchain_core.language_models.BaseLanguageModel"),
    ("py:class", "langchain_core.language_models.BaseLLM"),
    ("py:class", "langchain_core.language_models.BaseMessage"),
    ("py:class", "langchain_core.messages.BaseMessage"),
    ("py:class", "langchain_core.messages.HumanMessage"),
    ("py:class", "langchain_core.messages.AIMessage"),
    ("py:class", "langchain_core.messages.SystemMessage"),
    ("py:class", "langchain_core.messages.ToolMessage"),
    ("py:class", "langchain_core.messages.FunctionMessage"),
    ("py:class", "langchain_core.documents.Document"),
    ("py:class", "langchain_core.tools.BaseTool"),
    ("py:class", "langchain_core.tools.Tool"),
    ("py:class", "langchain_core.tools.StructuredTool"),
    ("py:class", "langchain_core.prompts.ChatPromptTemplate"),
    ("py:class", "langchain_core.prompts.PromptTemplate"),
    ("py:class", "langchain_core.prompts.BasePromptTemplate"),
    ("py:class", "langchain_core.output_parsers.BaseOutputParser"),
    ("py:class", "langchain_core.retrievers.BaseRetriever"),
    ("py:class", "langchain_core.vectorstores.VectorStore"),
    
    # Haive internal references that might not be available
    ("py:class", "haive.core.engine.base.Engine"),
    ("py:class", "haive.core.engine.Engine"),
    ("py:obj", "haive.core.common.mixins.tool_route_mixin.ToolRouteMixin"),
    ("py:class", "haive.agents.wiki_writer.utils.update_editor"),
    ("py:class", "haive.core.schema.StateSchema"),
    ("py:class", "haive.core.schema.BaseSchema"),
    ("py:class", "haive.core.models.BaseModel"),
    
    # Generic type parameters
    ("py:class", "T"),
    ("py:class", "Agent"),
    ("py:class", "TIn"),
    ("py:class", "TOut"),
    ("py:class", "StateType"),
    ("py:class", "MessageType"),
    
    # Common libraries
    ("py:class", "numpy.ndarray"),
    ("py:class", "pandas.DataFrame"),
    ("py:class", "pandas.Series"),
    ("py:class", "pathlib.Path"),
    ("py:class", "datetime.datetime"),
    ("py:class", "datetime.date"),
    ("py:class", "datetime.time"),
    ("py:class", "datetime.timedelta"),
    
    # Async types
    ("py:class", "Awaitable"),
    ("py:class", "Coroutine"),
    ("py:class", "AsyncIterator"),
    ("py:class", "AsyncGenerator"),
    
    # Other common missing references
    ("py:class", "Logger"),
    ("py:class", "logging.Logger"),
    ("py:class", "Exception"),
    ("py:class", "BaseException"),
]

# =============================================================================
# ENHANCED INTERSPHINX MAPPING
# =============================================================================

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
    "langchain": ("https://python.langchain.com/docs/", None),
    "langchain_core": ("https://api.python.langchain.com/en/latest/", None),
    "langchain_community": ("https://api.python.langchain.com/en/latest/", None),
    "langchain_openai": ("https://api.python.langchain.com/en/latest/", None),
    # Note: OpenAI docs URL doesn't support intersphinx, would need custom inventory
    # "openai": ("https://platform.openai.com/docs/", None),
}

# =============================================================================
# AUTODOC CONFIGURATION
# =============================================================================

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
    "show-inheritance": True,
}

autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"
autodoc_typehints_format = "short"
autodoc_mock_imports = []

# Type aliases to help with resolution
autodoc_type_aliases = {
    "Agent": "haive.agents.base.Agent",
    "StateSchema": "haive.core.schema.StateSchema",
    "Engine": "haive.core.engine.Engine",
    "T": "TypeVar('T')",
}

# Enable better type hint resolution
python_use_unqualified_type_names = True
suppress_warnings = ["ref.python", "autoapi"]

# AutoSummary configuration
autosummary_generate = True
autosummary_imported_members = True

# =============================================================================
# HTML THEME CONFIGURATION - FURO
# =============================================================================

html_theme = "furo"
html_title = f"🤖 {project} Documentation"
html_short_title = "Haive"

html_theme_options = {
    "light_css_variables": {
        "color-background-primary": "#ffffff",
        "color-background-secondary": "#f8fafc",
        "color-background-border": "#e2e8f0",
        "color-background-hover": "#f1f5f9",
        "color-background-item": "#e2e8f0",
        "color-brand-primary": "#2563eb",
        "color-brand-content": "#2563eb",
        "color-foreground-primary": "#1f2937",
        "color-foreground-secondary": "#6b7280",
        "color-foreground-muted": "#9ca3af",
        "color-foreground-border": "#d1d5db",
        "color-sidebar-background": "#f8fafc",
        "color-sidebar-background-border": "#e2e8f0",
        "color-api-background": "#f8fafc",
        "color-api-background-hover": "#f1f5f9",
        "color-api-overall": "#6b7280",
        "color-api-name": "#1f2937",
        "color-api-pre-name": "#6b7280",
        "color-inline-code-background": "#f1f5f9",
        "color-inline-code-foreground": "#374151",
        "color-admonition-background": "#f8fafc",
        "color-search-background": "#ffffff",
        "color-search-foreground": "#1f2937",
        "color-search-border": "#d1d5db",
        "color-link": "#2563eb",
        "color-link-underline": "#2563eb",
        "color-link-hover": "#1d4ed8",
    },
    "dark_css_variables": {
        "color-background-primary": "#0f172a",
        "color-background-secondary": "#1e293b",
        "color-background-border": "#334155",
        "color-background-hover": "#475569",
        "color-background-item": "#334155",
        "color-brand-primary": "#60a5fa",
        "color-brand-content": "#60a5fa",
        "color-foreground-primary": "#f1f5f9",
        "color-foreground-secondary": "#cbd5e1",
        "color-foreground-muted": "#94a3b8",
        "color-foreground-border": "#64748b",
        "color-sidebar-background": "#1e293b",
        "color-sidebar-background-border": "#334155",
        "color-api-background": "#1e293b",
        "color-api-background-hover": "#475569",
        "color-api-overall": "#cbd5e1",
        "color-api-name": "#f1f5f9",
        "color-api-pre-name": "#cbd5e1",
        "color-inline-code-background": "#475569",
        "color-inline-code-foreground": "#e2e8f0",
        "color-admonition-background": "#1e293b",
        "color-search-background": "#0f172a",
        "color-search-foreground": "#f1f5f9",
        "color-search-border": "#334155",
        "color-link": "#60a5fa",
        "color-link-underline": "#60a5fa",
        "color-link-hover": "#93c5fd",
    },
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "top_of_page_buttons": ["view", "edit"],
    "source_repository": "https://github.com/will-astley/haive",
    "source_branch": "main", 
    "source_directory": "docs/source/",
}

html_static_path = ["_static"]
html_css_files = []
html_js_files = []

html_context = {
    "display_github": True,
    "github_user": "will-astley",
    "github_repo": "haive",
    "github_version": "main",
    "conf_py_path": "/docs/source/",
}

html_sidebars = {
    "**": [
        "sidebar/scroll-start.html",
        "sidebar/brand.html",
        "sidebar/search.html",
        "sidebar/navigation.html", 
        "sidebar/scroll-end.html",
    ],
}

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
# OTHER EXTENSION SETTINGS
# =============================================================================

# Napoleon settings
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

# Copy button
if "sphinx_copybutton" in extensions:
    copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
    copybutton_prompt_is_regexp = True
    copybutton_line_continuation_character = "\\"
    copybutton_here_doc_delimiter = "EOT"
    copybutton_selector = "div.highlight > pre"

# Graphviz
graphviz_output_format = "svg"

# Todo
todo_include_todos = True
todo_emit_warnings = False

# =============================================================================
# SETUP FUNCTION WITH MCP DOCS AND DEBUG OUTPUT
# =============================================================================

def setup(app):
    """Enhanced setup with MCP docs handling and comprehensive debugging."""
    
    # Connect autoapi skip member
    try:
        app.connect("autoapi-skip-member", autoapi_skip_member)
        logger.info("✅ AutoAPI skip member handler connected")
    except Exception as e:
        logger.error(f"❌ Failed to connect AutoAPI skip member: {e}")
    
    # Initialize autoapi_all_objects
    def init_autoapi_objects_builder_inited(app):
        """Initialize when builder is initialized."""
        try:
            if hasattr(app, 'env') and app.env and not hasattr(app.env, 'autoapi_all_objects'):
                app.env.autoapi_all_objects = {}
                logger.info("✅ Initialized autoapi_all_objects")
        except Exception as e:
            logger.error(f"❌ Failed to initialize autoapi_all_objects: {e}")
    
    # Fix toc_num_entries
    def fix_autoapi_toc_entries(app, env):
        """Fix AutoAPI compatibility with Sphinx 8.2.3."""
        if 'index' not in env.toc_num_entries:
            env.toc_num_entries['index'] = 0
            logger.info("🔧 Fixed missing toc_num_entries for index")
        
        for docname in env.all_docs:
            if docname not in env.toc_num_entries:
                env.toc_num_entries[docname] = 0
    
    # Handle MCP documentation
    def handle_mcp_docs(app, env):
        """Create TOC entries for MCP documentation."""
        import shutil
        from pathlib import Path
        
        mcp_docs_source = Path(packages_dir) / "haive-mcp/data/documentation"
        
        if mcp_docs_source.exists():
            # Log what we found
            rst_files = list(mcp_docs_source.rglob("*.rst"))
            md_files = list(mcp_docs_source.rglob("*.md"))
            logger.info(f"📚 Found MCP docs: {len(rst_files)} .rst files, {len(md_files)} .md files")
            
            # Create index file for MCP docs
            mcp_index_path = Path(app.srcdir) / "mcp_documentation.rst"
            if not mcp_index_path.exists():
                categories = sorted([d.name for d in (mcp_docs_source / "servers").iterdir() if d.is_dir()])
                
                with open(mcp_index_path, 'w') as f:
                    f.write("MCP Server Documentation\n")
                    f.write("========================\n\n")
                    f.write(".. toctree::\n")
                    f.write("   :maxdepth: 2\n")
                    f.write("   :caption: MCP Servers by Category\n\n")
                    
                    for category in categories:
                        f.write(f"   MCP {category.replace('-', ' ').title()} <../../packages/haive-mcp/data/documentation/servers/{category}/index>\n")
                
                logger.info(f"✅ Created MCP documentation index with {len(categories)} categories")
    
    # Debug output function
    def build_finished_handler(app, exception):
        """Output comprehensive build statistics."""
        if exception:
            logger.error(f"❌ Build failed with exception: {exception}")
            return
        
        build_dir = Path(app.outdir)
        
        # Count generated files
        html_files = list(build_dir.rglob("*.html"))
        api_files = list((build_dir / "api").rglob("*.html")) if (build_dir / "api").exists() else []
        
        logger.info("=" * 70)
        logger.info("BUILD STATISTICS")
        logger.info("=" * 70)
        logger.info(f"✅ Total HTML files generated: {len(html_files)}")
        logger.info(f"✅ API documentation files: {len(api_files)}")
        logger.info(f"✅ Build directory: {build_dir}")
        
        # Show sample of generated API files
        if api_files:
            logger.info("\n📁 Sample API files generated:")
            for f in api_files[:10]:
                logger.info(f"   - {f.relative_to(build_dir)}")
            if len(api_files) > 10:
                logger.info(f"   ... and {len(api_files) - 10} more")
        
        # Check for warnings in the log
        if hasattr(app, '_warning_count'):
            logger.info(f"\n⚠️ Total warnings: {app._warning_count}")
        
        logger.info("=" * 70)
    
    # Connect all handlers
    app.connect('builder-inited', init_autoapi_objects_builder_inited)
    app.connect('env-updated', fix_autoapi_toc_entries)
    app.connect('env-before-read-docs', handle_mcp_docs)
    app.connect('build-finished', build_finished_handler)
    
    # Track warnings
    original_warn = app.warn
    app._warning_count = 0
    
    def counting_warn(message, *args, **kwargs):
        app._warning_count += 1
        return original_warn(message, *args, **kwargs)
    
    app.warn = counting_warn
    
    logger.info("✅ All setup handlers connected")

# =============================================================================
# CONFIGURATION SUMMARY
# =============================================================================

logger.info("=" * 70)
logger.info("SPHINX TEST CONFIGURATION LOADED")
logger.info("=" * 70)
logger.info(f"📦 Extensions: {len(extensions)} total")
logger.info(f"🎨 Theme: {html_theme}")
logger.info(f"🔧 AutoAPI: Processing {len(autoapi_dirs)} packages")
logger.info(f"🚫 Nitpick ignores: {len(nitpick_ignore)} entries")
logger.info(f"🔗 Intersphinx: {len(intersphinx_mapping)} external docs")
logger.info("=" * 70)