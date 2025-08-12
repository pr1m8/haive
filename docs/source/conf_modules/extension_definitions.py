"""Extension definitions organized by category.

This module defines all available Sphinx extensions with their configurations
and dependencies in a clean, manageable way.
"""

from .extension_manager import ExtensionSpec, create_extension_spec


# Configuration functions for complex extensions
def configure_sphinx_gallery():
    """Configuration for sphinx-gallery."""
    return {
        "sphinx_gallery_conf": {
            "examples_dirs": ["../examples"],
            "gallery_dirs": ["auto_examples"],
            "plot_gallery": True,
            "download_all_examples": False,
        }
    }


def configure_nbsphinx():
    """Configuration for nbsphinx."""
    return {
        "nbsphinx_execute": "auto",
        "nbsphinx_timeout": 300,
        "nbsphinx_allow_errors": False,
    }


def configure_myst_parser():
    """Configuration for MyST parser."""
    return {
        "myst_enable_extensions": [
            "deflist",
            "tasklist",
            "html_image",
            "colon_fence",
            "smartquotes",
            "replacements",
            "linkify",
            "strikethrough",
        ],
        "myst_heading_anchors": 3,
    }


def configure_intersphinx():
    """Configuration for intersphinx."""
    return {
        "intersphinx_mapping": {
            "python": ("https://docs.python.org/3", None),
            "pydantic": ("https://docs.pydantic.dev/latest", None),
            "sphinx": ("https://www.sphinx-doc.org/en/master", None),
        }
    }


def configure_plantuml():
    """Configuration for PlantUML."""
    return {
        "plantuml_output_format": "svg",
        "plantuml": "plantuml",  # Assumes plantuml is in PATH
    }


def configure_autodoc_pydantic():
    """Configuration for autodoc-pydantic."""
    return {
        "autodoc_pydantic_model_show_json": True,
        "autodoc_pydantic_model_show_config_summary": True,
        "autodoc_pydantic_model_show_validator_summary": True,
        "autodoc_pydantic_model_show_field_summary": True,
        "autodoc_pydantic_model_show_validator_members": True,
        "autodoc_pydantic_field_list_validators": True,
        "autodoc_pydantic_field_show_constraints": True,
        "autodoc_pydantic_model_erdantic_figure": True,
    }


# Core Sphinx Extensions (highest priority)
CORE_EXTENSIONS = [
    create_extension_spec(
        "sphinx.ext.autodoc",
        package="sphinx",
        module_check="sphinx.ext.autodoc",
        description="Generate documentation from docstrings",
        category="core",
        priority=1,
    ),
    create_extension_spec(
        "sphinx.ext.napoleon",
        package="sphinx",
        module_check="sphinx.ext.napoleon",
        description="Google/NumPy docstring support",
        category="core",
        priority=2,
    ),
    create_extension_spec(
        "sphinx.ext.viewcode",
        package="sphinx",
        module_check="sphinx.ext.viewcode",
        description="Link to highlighted source code",
        category="core",
        priority=3,
    ),
    create_extension_spec(
        "sphinx.ext.intersphinx",
        package="sphinx",
        module_check="sphinx.ext.intersphinx",
        description="Cross-project linking",
        category="core",
        priority=4,
        config_func=configure_intersphinx,
    ),
    create_extension_spec(
        "sphinx.ext.autosummary",
        package="sphinx",
        module_check="sphinx.ext.autosummary",
        description="Generate summary tables",
        category="core",
        priority=5,
    ),
]

# API Documentation Extensions
API_EXTENSIONS = [
    create_extension_spec(
        "autoapi.extension",
        package="sphinx-autoapi",
        module_check="autoapi",
        description="Automatic API documentation generation",
        category="api",
        priority=10,
        config_vars={
            "autoapi_type": "python",
            "autoapi_dirs": ["../../../src"],
            "autoapi_template_dir": "_autoapi_templates",
            "autoapi_add_toctree_entry": True,
            "autoapi_generate_api_docs": True,
            "autoapi_keep_files": True,
        },
    ),
    create_extension_spec(
        "sphinxcontrib.autodoc_pydantic",
        package="autodoc-pydantic",
        module_check="sphinxcontrib.autodoc_pydantic",
        description="Enhanced Pydantic model documentation",
        category="api",
        priority=11,
        config_func=configure_autodoc_pydantic,
    ),
    create_extension_spec(
        "enum_tools.autoenum",
        package="enum-tools",
        module_check="enum_tools",
        description="Enhanced enum documentation",
        category="api",
        priority=12,
        requires=["sphinx-toolbox"],  # enum-tools requires sphinx-toolbox
    ),
    create_extension_spec(
        "sphinx_autodoc_typehints",
        package="sphinx-autodoc-typehints",
        module_check="sphinx_autodoc_typehints",
        description="Type hints in documentation",
        category="api",
        priority=13,
        config_vars={
            "typehints_fully_qualified": False,
            "typehints_use_signature": True,
        },
    ),
]

# Content and Markup Extensions
CONTENT_EXTENSIONS = [
    create_extension_spec(
        "myst_parser",
        package="myst-parser",
        module_check="myst_parser",
        description="Markdown support with MyST",
        category="content",
        priority=20,
        config_func=configure_myst_parser,
    ),
    create_extension_spec(
        "sphinx_design",
        package="sphinx-design",
        module_check="sphinx_design",
        description="Modern design elements (cards, grids)",
        category="content",
        priority=21,
    ),
    create_extension_spec(
        "sphinx_tabs.tabs",
        package="sphinx-tabs",
        module_check="sphinx_tabs",
        description="Tabbed content",
        category="content",
        priority=22,
        config_vars={"sphinx_tabs_disable_tab_closing": True},
    ),
    create_extension_spec(
        "sphinx_togglebutton",
        package="sphinx-togglebutton",
        module_check="sphinx_togglebutton",
        description="Collapsible content sections",
        category="content",
        priority=23,
        config_vars={
            "togglebutton_hint": "Click to show",
            "togglebutton_hint_hide": "Click to hide",
        },
    ),
    create_extension_spec(
        "sphinx_copybutton",
        package="sphinx-copybutton",
        module_check="sphinx_copybutton",
        description="Copy code button",
        category="content",
        priority=24,
        config_vars={
            "copybutton_prompt_text": r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: ",
            "copybutton_prompt_is_regexp": True,
        },
    ),
]

# Diagram and Visualization Extensions
DIAGRAM_EXTENSIONS = [
    create_extension_spec(
        "sphinx.ext.graphviz",
        package="sphinx",
        module_check="sphinx.ext.graphviz",
        description="Graphviz diagrams",
        category="diagrams",
        priority=30,
    ),
    create_extension_spec(
        "sphinxcontrib.mermaid",
        package="sphinxcontrib-mermaid",
        module_check="sphinxcontrib.mermaid",
        description="Mermaid diagrams",
        category="diagrams",
        priority=31,
        config_vars={"mermaid_params": ["--theme", "neutral"]},
    ),
    create_extension_spec(
        "sphinxcontrib.plantuml",
        package="sphinxcontrib-plantuml",
        module_check="sphinxcontrib.plantuml",
        description="PlantUML diagrams",
        category="diagrams",
        priority=32,
        config_func=configure_plantuml,
    ),
    create_extension_spec(
        "sphinxcontrib.seqdiag",
        package="sphinxcontrib-seqdiag",
        module_check="sphinxcontrib.seqdiag",
        description="Sequence diagrams",
        category="diagrams",
        priority=33,
    ),
    create_extension_spec(
        "sphinxcontrib.blockdiag",
        package="sphinxcontrib-blockdiag",
        module_check="sphinxcontrib.blockdiag",
        description="Block diagrams",
        category="diagrams",
        priority=34,
    ),
]

# Code Execution Extensions
EXECUTION_EXTENSIONS = [
    create_extension_spec(
        "sphinx_exec_code",
        package="sphinx-exec-code",
        module_check="sphinx_exec_code",
        description="Execute Python code blocks",
        category="execution",
        priority=40,
    ),
    create_extension_spec(
        "sphinxcontrib.programoutput",
        package="sphinxcontrib-programoutput",
        module_check="sphinxcontrib.programoutput",
        description="Execute shell commands",
        category="execution",
        priority=41,
    ),
    create_extension_spec(
        "sphinx_runpython",
        package="sphinx-runpython",
        module_check="sphinx_runpython",
        description="Run Python snippets inline",
        category="execution",
        priority=42,
    ),
    create_extension_spec(
        "sphinx_gallery.gen_gallery",
        package="sphinx-gallery",
        module_check="sphinx_gallery",
        description="Execute scripts and generate galleries",
        category="execution",
        priority=43,
        config_func=configure_sphinx_gallery,
    ),
    create_extension_spec(
        "nbsphinx",
        package="nbsphinx",
        module_check="nbsphinx",
        description="Jupyter notebook integration",
        category="execution",
        priority=44,
        config_func=configure_nbsphinx,
    ),
]

# Multi-Version Extensions
VERSIONING_EXTENSIONS = [
    create_extension_spec(
        "sphinx_multiversion",
        package="sphinx-multiversion",
        module_check="sphinx_multiversion",
        description="Git-based multi-version documentation",
        category="versioning",
        priority=50,
    ),
    create_extension_spec(
        "sphinx_last_updated_by_git",
        package="sphinx-last-updated-by-git",
        module_check="sphinx_last_updated_by_git",
        description="Git-based last updated timestamps",
        category="versioning",
        priority=51,
    ),
    create_extension_spec(
        "sphinx_version_warning",
        package="sphinx-version-warning",
        module_check="sphinx_version_warning",
        description="Version deprecation warnings",
        category="versioning",
        priority=52,
    ),
]

# Utility Extensions
UTILITY_EXTENSIONS = [
    create_extension_spec(
        "sphinx_sitemap",
        package="sphinx-sitemap",
        module_check="sphinx_sitemap",
        description="SEO sitemap generation",
        category="utility",
        priority=60,
        config_vars={"html_baseurl": "https://pyautodoc.readthedocs.io/"},
    ),
    create_extension_spec(
        "sphinx_codeautolink",
        package="sphinx-codeautolink",
        module_check="sphinx_codeautolink",
        description="Automatic code linking",
        category="utility",
        priority=61,
        config_vars={
            "codeautolink_autodoc_inject": True,
            "codeautolink_concat_default": True,
        },
    ),
]

# Development Extensions (disabled by default)
DEVELOPMENT_EXTENSIONS = [
    create_extension_spec(
        "sphinx_autobuild",
        package="sphinx-autobuild",
        module_check="sphinx_autobuild",
        description="Live reload during development",
        category="development",
        priority=90,
        enabled_by_default=False,  # Only for dev
    ),
]

# All extension categories
ALL_EXTENSION_GROUPS = {
    "core": CORE_EXTENSIONS,
    "api": API_EXTENSIONS,
    "content": CONTENT_EXTENSIONS,
    "diagrams": DIAGRAM_EXTENSIONS,
    "execution": EXECUTION_EXTENSIONS,
    "versioning": VERSIONING_EXTENSIONS,
    "utility": UTILITY_EXTENSIONS,
    "development": DEVELOPMENT_EXTENSIONS,
}

# Predefined extension sets for common use cases
EXTENSION_SETS = {
    "minimal": ["core"],
    "standard": ["core", "api", "content"],
    "full": ["core", "api", "content", "diagrams", "utility"],
    "development": ["core", "api", "content", "utility", "development"],
    "execution": ["core", "api", "content", "execution"],
    "versioning": ["core", "api", "content", "versioning"],
    "everything": list(ALL_EXTENSION_GROUPS.keys()),
}
