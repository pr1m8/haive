"""Diagram and visualization extensions.

This module configures extensions for creating diagrams and visualizations:
- Mermaid diagrams (flowcharts, sequence diagrams)
- PlantUML diagrams (UML, system design)
- Block diagrams (architecture)
- Sequence diagrams (API flows)
- Image galleries and thumbnails
"""

from __future__ import annotations

from typing import Any


def get_config(
    enable_mermaid: bool = True,
    enable_plantuml: bool = True,
    enable_blockdiag: bool = True,
    enable_seqdiag: bool = True,
    enable_images: bool = True,
) -> dict[str, Any]:
    """Get diagram and visualization extension configuration.

    Args:
        enable_mermaid: Enable Mermaid diagrams
        enable_plantuml: Enable PlantUML diagrams
        enable_blockdiag: Enable block diagrams
        enable_seqdiag: Enable sequence diagrams
        enable_images: Enable image galleries and thumbnails

    Returns:
        Dictionary with diagram configuration
    """
    config = {}
    extensions = []

    # Mermaid diagrams
    if enable_mermaid:
        extensions.append("sphinxcontrib.mermaid")
        config.update(_get_mermaid_config())

    # PlantUML diagrams
    if enable_plantuml:
        extensions.append("sphinxcontrib.plantuml")
        config.update(_get_plantuml_config())

    # Block diagrams
    if enable_blockdiag:
        extensions.append("sphinxcontrib.blockdiag")

    # Sequence diagrams
    if enable_seqdiag:
        extensions.append("sphinxcontrib.seqdiag")

    # Image enhancements
    if enable_images:
        extensions.append("sphinxcontrib.images")
        config.update(_get_images_config())

    config["extensions"] = extensions
    return config


def _get_mermaid_config() -> dict[str, Any]:
    """Get Mermaid diagram configuration."""
    return {
        "mermaid_version": "10.6.1",
        "mermaid_init_js": """
mermaid.initialize({
    startOnLoad: true,
    theme: 'default',
    themeVariables: {
        primaryColor: '#0066cc',
        primaryTextColor: '#ffffff',
        primaryBorderColor: '#0066cc',
        lineColor: '#666666',
        secondaryColor: '#f0f0f0',
        tertiaryColor: '#ffffff'
    }
});
""",
    }


def _get_plantuml_config() -> dict[str, Any]:
    """Get PlantUML diagram configuration."""
    return {
        # PlantUML server (use local if available, otherwise remote)
        "plantuml": "java -jar plantuml.jar",
        # Alternative: use online server
        "plantuml_output_format": "svg",
        "plantuml_epstopdf": "epstopdf",
    }


def _get_images_config() -> dict[str, Any]:
    """Get image gallery configuration."""
    return {
        "images_config": {
            "override_image_directive": False,
            "show_caption": True,
            "download": True,
        },
    }


def get_blockdiag_config() -> dict[str, Any]:
    """Get block diagram configuration."""
    return {
        "blockdiag_html_image_format": "SVG",
        "blockdiag_fontpath": None,  # Use system default
    }


def get_seqdiag_config() -> dict[str, Any]:
    """Get sequence diagram configuration."""
    return {
        "seqdiag_html_image_format": "SVG",
        "seqdiag_fontpath": None,  # Use system default
    }


def get_minimal_config() -> dict[str, Any]:
    """Get minimal diagram configuration."""
    return get_config(
        enable_mermaid=True,
        enable_plantuml=False,
        enable_blockdiag=False,
        enable_seqdiag=False,
        enable_images=False,
    )


def get_standard_config() -> dict[str, Any]:
    """Get standard diagram configuration."""
    return get_config(
        enable_mermaid=True,
        enable_plantuml=True,
        enable_blockdiag=False,
        enable_seqdiag=False,
        enable_images=True,
    )


def get_full_config() -> dict[str, Any]:
    """Get full diagram configuration."""
    return get_config(
        enable_mermaid=True,
        enable_plantuml=True,
        enable_blockdiag=True,
        enable_seqdiag=True,
        enable_images=True,
    )
