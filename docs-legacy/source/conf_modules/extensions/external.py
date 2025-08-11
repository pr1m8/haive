"""External integration extensions.

This module configures extensions for external integrations:
- Intersphinx: Cross-project references
- Open Graph: Social sharing metadata
- Sitemap: SEO sitemap generation
- GitHub integration: Issues, contributors
- YouTube: Video embedding
- API documentation: OpenAPI, HTTP domains
"""

from typing import Any


def get_config(
    enable_intersphinx: bool = True,
    enable_opengraph: bool = True,
    enable_sitemap: bool = True,
    enable_github: bool = True,
    enable_youtube: bool = True,
    enable_api_docs: bool = True,
    github_repo: str = "pr1m8/haive",
    base_url: str = "https://haive.readthedocs.io/",
) -> dict[str, Any]:
    """Get external integration extension configuration.

    Args:
        enable_intersphinx: Enable cross-project references
        enable_opengraph: Enable Open Graph social metadata
        enable_sitemap: Enable SEO sitemap generation
        enable_github: Enable GitHub integration (issues, contributors)
        enable_youtube: Enable YouTube video embedding
        enable_api_docs: Enable API documentation extensions
        github_repo: GitHub repository (format: "owner/repo")
        base_url: Base URL for the documentation site

    Returns:
        Dictionary with external integration configuration
    """
    config = {}
    extensions = []

    # Cross-project references
    if enable_intersphinx:
        extensions.append("sphinx.ext.intersphinx")
        config.update(_get_intersphinx_config())

    # Social sharing
    if enable_opengraph:
        extensions.append("sphinxext.opengraph")
        config.update(_get_opengraph_config(base_url))

    # SEO sitemap
    if enable_sitemap:
        # extensions.append("sphinx_sitemap")  # DISABLED: Incompatible with Sphinx 8.2.3
        config.update(_get_sitemap_config(base_url))

    # GitHub integration
    if enable_github:
        extensions.extend(
            [
                "sphinx_issues",  # GitHub issues integration
                "sphinx_contributors",  # Automatic contributor lists
            ],
        )
        config.update(_get_github_config(github_repo))

    # YouTube videos
    if enable_youtube:
        extensions.append("sphinxcontrib.youtube")

    # API documentation
    if enable_api_docs:
        extensions.extend(
            [
                "sphinxcontrib.openapi",  # OpenAPI/Swagger docs
                "sphinxcontrib.httpdomain",  # HTTP API documentation
            ],
        )

    config["extensions"] = extensions
    return config


def _get_intersphinx_config() -> dict[str, Any]:
    """Get Intersphinx configuration."""
    return {
        "intersphinx_mapping": {
            "python": ("https://docs.python.org/3", None),
            "langchain": ("https://python.langchain.com/", None),
            "pydantic": ("https://docs.pydantic.dev/", None),
            "numpy": ("https://numpy.org/doc/stable/", None),
            "pandas": ("https://pandas.pydata.org/docs/", None),
            "fastapi": ("https://fastapi.tiangolo.com/", None),
            "requests": ("https://requests.readthedocs.io/en/latest/", None),
            "sqlalchemy": ("https://docs.sqlalchemy.org/en/latest/", None),
        },
        "intersphinx_disabled_reftypes": ["*"],  # Disable all by default
    }


def _get_opengraph_config(base_url: str) -> dict[str, Any]:
    """Get Open Graph configuration."""
    return {
        "ogp_site_url": base_url,
        "ogp_description_length": 200,
        "ogp_image": "_static/haive-logo.png",
        "ogp_social_cards": {
            "enable": True,
            "image": "_static/haive-logo.png",
        },
        "ogp_type": "website",
        "ogp_site_name": "Haive AI Agent Framework",
    }


def _get_sitemap_config(base_url: str) -> dict[str, Any]:
    """Get sitemap configuration."""
    return {
        "sitemap_url_scheme": "{link}",
        "html_baseurl": base_url,  # Required for sitemap generation
    }


def _get_github_config(github_repo: str) -> dict[str, Any]:
    """Get GitHub integration configuration."""
    return {
        "issues_github_path": github_repo,
        "contributors_github_repo": github_repo,
        "contributors_file": "CONTRIBUTORS.md",
    }


def get_hover_config() -> dict[str, Any]:
    """Get hover tooltips configuration."""
    return {
        "hoverxref_auto_ref": True,  # Enable automatic hover references
        "hoverxref_domains": ["py"],  # Enable for Python domain
        "hoverxref_roles": ["ref", "class", "func", "meth", "attr", "exc", "data"],
    }


def get_needs_config() -> dict[str, Any]:
    """Get requirements management configuration."""
    return {
        "needs_types": [
            {
                "directive": "req",
                "title": "Requirement",
                "prefix": "R_",
                "color": "#BFD8D2",
                "style": "node",
            },
            {
                "directive": "spec",
                "title": "Specification",
                "prefix": "S_",
                "color": "#FEDCD2",
                "style": "node",
            },
            {
                "directive": "agent",
                "title": "Agent",
                "prefix": "A_",
                "color": "#667eea",
                "style": "node",
            },
            {
                "directive": "tool",
                "title": "Tool",
                "prefix": "T_",
                "color": "#764ba2",
                "style": "node",
            },
        ],
    }


def get_minimal_config() -> dict[str, Any]:
    """Get minimal external integration configuration."""
    return get_config(
        enable_intersphinx=True,
        enable_opengraph=False,
        enable_sitemap=False,
        enable_github=False,
        enable_youtube=False,
        enable_api_docs=False,
    )


def get_standard_config() -> dict[str, Any]:
    """Get standard external integration configuration."""
    return get_config(
        enable_intersphinx=True,
        enable_opengraph=True,
        enable_sitemap=True,
        enable_github=True,
        enable_youtube=False,
        enable_api_docs=True,
    )


def get_full_config() -> dict[str, Any]:
    """Get full external integration configuration."""
    config = get_config(
        enable_intersphinx=True,
        enable_opengraph=True,
        enable_sitemap=True,
        enable_github=True,
        enable_youtube=True,
        enable_api_docs=True,
    )

    # Add additional full-featured extensions
    config["extensions"].extend(
        [
            "hoverxref.extension",  # Hover tooltips
            "sphinx_needs",  # Requirements management
        ],
    )

    config.update(get_hover_config())
    config.update(get_needs_config())

    return config
