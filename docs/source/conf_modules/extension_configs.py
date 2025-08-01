"""Configuration settings for specific Sphinx extensions.

This module provides configuration dictionaries for extensions that require
special settings beyond just being included in the extensions list.
"""

from typing import Any


def get_mermaid_config() -> dict[str, Any]:
    """Configuration for Mermaid diagrams."""
    return {
        "mermaid_output_format": "svg",
        "mermaid_init_js": """
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
        """,
        "mermaid_verbose": True,
    }


def get_plantuml_config() -> dict[str, Any]:
    """Configuration for PlantUML diagrams."""
    return {
        "plantuml": "java -jar plantuml.jar",
        "plantuml_output_format": "svg",
        "plantuml_cache_path": "_build/plantuml_cache",
        "plantuml_batch_size": 1,
    }


def get_bibtex_config() -> dict[str, Any]:
    """Configuration for bibliography."""
    return {
        "bibtex_bibfiles": ["references.bib"],
        "bibtex_default_style": "alpha",
        "bibtex_reference_style": "author_year",
    }


def get_openapi_config() -> dict[str, Any]:
    """Configuration for OpenAPI documentation."""
    return {
        "openapi_spec_url": "/openapi.json",
        "openapi_title": "Haive API Documentation",
        "openapi_description": "Complete API reference for Haive AI Agent Framework",
    }


def get_httpdomain_config() -> dict[str, Any]:
    """Configuration for HTTP domain."""
    return {
        "http_index_ignore_prefixes": ["/internal/", "/debug/"],
        "http_index_shortname": "Haive API",
        "http_index_localname": "Haive AI Agent Framework API",
    }


def get_images_config() -> dict[str, Any]:
    """Configuration for image handling."""
    return {
        "images_config": {
            "override_image_directive": True,
            "default_image_width": "100%",
            "default_image_height": None,
            "default_show_title": True,
            "download": False,
        }
    }


def get_youtube_config() -> dict[str, Any]:
    """Configuration for YouTube embedding."""
    return {
        "youtube_cmd": ('youtube-dl -f "best[height<=480]" --get-url {url}'),
        "youtube_fix_responsive": True,
        "youtube_privacy_mode": True,
    }


def get_copybutton_config() -> dict[str, Any]:
    """Configuration for copy button."""
    return {
        "copybutton_prompt_text": r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: ",
        "copybutton_prompt_is_regexp": True,
        "copybutton_line_continuation_character": "\\",
        "copybutton_here_doc_delimiter": "EOT",
    }


def get_design_config() -> dict[str, Any]:
    """Configuration for sphinx-design."""
    return {
        "sd_fontawesome_latex": True,
        "sd_custom_directives": {
            "dropdown": {"inherit": "note"},
            "tab-set": {"inherit": "container"},
        },
    }


def get_external_toc_config() -> dict[str, Any]:
    """Configuration for external TOC."""
    return {
        "external_toc_path": "_toc.yml",
        "external_toc_exclude_missing": False,
    }


def get_sitemap_config() -> dict[str, Any]:
    """Configuration for sitemap generation."""
    return {
        "html_baseurl": "https://haive.readthedocs.io/",
        "sitemap_url_scheme": "{link}",
        "sitemap_locales": [None],
        "sitemap_filename": "sitemap.xml",
    }


def get_opengraph_config() -> dict[str, Any]:
    """Configuration for OpenGraph meta tags."""
    return {
        "ogp_site_url": "https://haive.readthedocs.io/",
        "ogp_site_name": "Haive AI Agent Framework",
        "ogp_description_length": 160,
        "ogp_type": "website",
        "ogp_image": "https://haive.readthedocs.io/_static/og-image.png",
        "ogp_custom_meta_tags": [
            '<meta name="twitter:card" content="summary_large_image">',
            '<meta name="twitter:site" content="@haive_ai">',
        ],
    }


def get_versioning_config() -> dict[str, Any]:
    """Configuration for documentation versioning."""
    return {
        "scv_root_ref": "main",
        "scv_sort": ("semver",),
        "scv_banner_greatest_tag": True,
        "scv_show_banner": True,
        "scv_banner_main_ref": "main",
    }


def get_rediraffe_config() -> dict[str, Any]:
    """Configuration for redirects."""
    return {
        "rediraffe_branch": "main",
        "rediraffe_redirects": {
            # Add redirects as needed
            "old-page.html": "new-page.html",
        },
    }


def get_fulltoc_config() -> dict[str, Any]:
    """Configuration for full table of contents."""
    return {
        "html_theme_options": {
            "sidebar_includehidden": True,
        }
    }


def get_autodoc_typehints_config() -> dict[str, Any]:
    """Configuration for sphinx-autodoc-typehints to handle generics."""
    return {
        # CRITICAL: Configure for Agent generic types - use 'signature' to bypass generic issues
        "autodoc_typehints": "signature",  # Keep types in signature to avoid generic expansion
        "typehints_formatter": "short",  # Use modern Python 3.9+ style
        "typehints_fully_qualified": False,  # Use short names
        "autodoc_typehints_description_target": "documented",
        "autodoc_type_aliases": {
            # Add aliases for complex generic types
            "InvokableEngine": "haive.core.engine.base.base.InvokableEngine",
            "BaseModel": "pydantic.BaseModel",
            "TIn": "typing.TypeVar",
            "TOut": "typing.TypeVar",
        },
        # Enhanced suppression for generic type issues
        "suppress_warnings": [
            "autodoc.import_object",
            "autodoc.type_comment",
            "autosummary",  # Suppress autosummary warnings about generics
        ],
        # Additional typehints settings to handle generics
        "typehints_defaults": "comma",
        "always_document_param_types": False,  # Don't force parameter type documentation
        "typehints_use_signature": True,  # Use signature for type info
        "simplify_optional_unions": True,  # Simplify complex union types
    }


def get_all_extension_configs(available_extensions: list[str]) -> dict[str, Any]:
    """Get all configuration for available extensions."""
    configs = {}

    # Map extensions to their config functions
    config_map = {
        "sphinxcontrib.mermaid": get_mermaid_config,
        "sphinxcontrib.plantuml": get_plantuml_config,
        "sphinxcontrib.bibtex": get_bibtex_config,
        "sphinxcontrib.openapi": get_openapi_config,
        "sphinxcontrib.httpdomain": get_httpdomain_config,
        "sphinxcontrib.images": get_images_config,
        "sphinxcontrib.youtube": get_youtube_config,
        "sphinx_copybutton": get_copybutton_config,
        "sphinx_design": get_design_config,
        "sphinx_external_toc": get_external_toc_config,
        "sphinx_sitemap": get_sitemap_config,
        "sphinxext.opengraph": get_opengraph_config,
        "sphinxcontrib.versioning": get_versioning_config,
        "sphinxext.rediraffe": get_rediraffe_config,
        "sphinxcontrib.fulltoc": get_fulltoc_config,
        "sphinxcontrib.autodoc_pydantic": get_autodoc_pydantic_config,
        "autodocsumm": get_autodocsumm_config,
        "sphinx_autodoc_typehints": get_autodoc_typehints_config,  # CRITICAL for generics
    }

    # Get configs for available extensions
    for ext in available_extensions:
        if ext in config_map:
            ext_config = config_map[ext]()
            configs.update(ext_config)

    return configs


def get_extension_dependencies() -> dict[str, list[str]]:
    """Get dependencies between extensions."""
    return {
        "sphinxcontrib.plantuml": ["plantuml"],  # Requires PlantUML Java
        "sphinxcontrib.mermaid": ["mermaid"],  # Requires mermaid-cli
        "sphinxcontrib.youtube": ["youtube-dl"],  # Requires youtube-dl
        "sphinx_gallery.gen_gallery": [
            "matplotlib",
            "pillow",
        ],  # For gallery generation
    }


def get_autodoc_pydantic_config() -> dict[str, Any]:
    """Configuration for autodoc-pydantic extension."""
    return {
        # Pydantic model settings
        "autodoc_pydantic_model_show_json_error_strategy": "coerce",
        "autodoc_pydantic_model_show_config_member": True,
        "autodoc_pydantic_model_show_config_summary": True,
        "autodoc_pydantic_model_show_validator_members": True,
        "autodoc_pydantic_model_show_validator_summary": True,
        "autodoc_pydantic_model_show_field_summary": True,
        "autodoc_pydantic_model_member_order": "bysource",
        "autodoc_pydantic_model_signature_prefix": "pydantic model",
        "autodoc_pydantic_model_undoc_members": True,
        # Pydantic field settings
        "autodoc_pydantic_field_list_validators": True,
        "autodoc_pydantic_field_doc_policy": "both",
        "autodoc_pydantic_field_show_constraints": True,
        "autodoc_pydantic_field_show_alias": True,
        "autodoc_pydantic_field_show_default": True,
        "autodoc_pydantic_field_show_required": True,
        "autodoc_pydantic_field_signature_prefix": "field",
        # Pydantic validator settings
        "autodoc_pydantic_validator_signature_prefix": "validator",
        "autodoc_pydantic_validator_replace_signature": True,
        "autodoc_pydantic_validator_list_fields": True,
        # Pydantic config settings
        "autodoc_pydantic_config_signature_prefix": "model config",
        "autodoc_pydantic_config_members": True,
    }


def get_autodocsumm_config() -> dict[str, Any]:
    """Configuration for autodocsumm extension."""
    return {
        # Autodocsumm settings
        "autodocsumm_generate": True,
        "autodocsumm_imported_members": True,
        "autodocsumm_member_order": "bysource",
        "autodocsumm_generate_overwrite": True,
        # Integration with autosummary
        "autosummary_generate": True,
        "autosummary_generate_overwrite": True,
        "autosummary_mock_imports": [],
        "autosummary_ignore_module_all": False,
        # Template customization
        "autodocsumm_class_header": "Class Summary",
        "autodocsumm_function_header": "Function Summary",
        "autodocsumm_attribute_header": "Attribute Summary",
    }


def get_conditional_configs(extensions: list[str]) -> dict[str, Any]:
    """Get configurations that depend on multiple extensions being present."""
    configs = {}

    # If both mermaid and plantuml are available, optimize for diagrams
    if "sphinxcontrib.mermaid" in extensions and "sphinxcontrib.plantuml" in extensions:
        configs.update(
            {
                "html_css_files": ["diagrams.css"],
                "html_js_files": ["diagram-utils.js"],
            }
        )

    # If versioning and sitemap are both available, enhance SEO
    if "sphinxcontrib.versioning" in extensions and "sphinx_sitemap" in extensions:
        configs.update(
            {
                "html_extra_path": ["robots.txt"],
            }
        )

    # If multiple API doc extensions available, create unified API section
    api_extensions = [
        "sphinxcontrib.openapi",
        "sphinxcontrib.redoc",
        "sphinxcontrib.httpdomain",
    ]
    if any(ext in extensions for ext in api_extensions):
        configs.update(
            {
                "html_theme_options": {
                    "navigation_with_keys": True,
                    "show_navbar_depth": 3,
                }
            }
        )

    # If Pydantic documentation extensions are available, optimize for Python APIs
    pydantic_extensions = ["sphinxcontrib.autodoc_pydantic", "autodocsumm"]
    if any(ext in extensions for ext in pydantic_extensions):
        configs.update(
            {
                # Enhanced autodoc settings for Pydantic models
                "autodoc_default_options": {
                    "members": True,
                    "member-order": "bysource",
                    "special-members": "__init__",
                    "undoc-members": True,
                    "exclude-members": "__weakref__",
                    "show-inheritance": True,
                },
                # Type hint improvements
                "autodoc_typehints": "description",
                "autodoc_typehints_description_target": "documented",
                "autodoc_typehints_format": "short",
                # Better class documentation
                "autoclass_content": "both",
                "autodoc_class_signature": "mixed",
            }
        )

    # If both Pydantic and autosummary extensions are available, create comprehensive API docs
    if "sphinxcontrib.autodoc_pydantic" in extensions and "autodocsumm" in extensions:
        configs.update(
            {
                # Enhanced navigation for complex APIs
                "html_theme_options": {
                    "collapse_navigation": False,
                    "sticky_navigation": True,
                    "navigation_depth": 4,
                    "includehidden": True,
                    "titles_only": False,
                },
                # Better TOC generation
                "toctree_show_hidden": True,
                "toctree_titles_only": False,
            }
        )

    return configs
