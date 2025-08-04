"""Content enhancement extensions.

This module configures extensions that enhance content presentation:
- Design elements (cards, grids, badges)
- Interactive elements (tabs, toggles, buttons)
- Copy functionality and code highlighting
- Math support and emojis
"""

from __future__ import annotations

from typing import Any


def get_config(
    enable_design: bool = True,
    enable_interactive: bool = True,
    enable_copybutton: bool = True,
    enable_math: bool = True,
    enable_emoji: bool = True,
) -> dict[str, Any]:
    """Get content enhancement extension configuration.

    Args:
        enable_design: Enable sphinx-design (cards, grids, badges)
        enable_interactive: Enable interactive elements (tabs, toggles)
        enable_copybutton: Enable copy button for code blocks
        enable_math: Enable math support with $ syntax
        enable_emoji: Enable emoji support in documentation

    Returns:
        Dictionary with enhancement configuration
    """
    config = {}
    extensions = []

    # Design and layout
    if enable_design:
        extensions.append("sphinx_design")

    # Interactive content
    if enable_interactive:
        extensions.extend(
            [
                "sphinx_tabs.tabs",  # Tabbed content sections
                "sphinx_inline_tabs",  # Inline tabbed content
                "sphinx_togglebutton",  # Collapsible sections
            ], )

    # Code enhancements
    if enable_copybutton:
        extensions.append("sphinx_copybutton")
        config.update(_get_copybutton_config())

    # Math support
    if enable_math:
        extensions.append("sphinx_math_dollar")  # LaTeX math with $ syntax

    # Emoji support
    if enable_emoji:
        extensions.append("sphinxemoji.sphinxemoji")

    # Additional enhancement extensions
    extensions.extend(
        [
            "sphinx_exec_directive",  # Execute Python code in docs
            "sphinx_prompt",  # Terminal prompt styling
            "sphinx_substitution_extensions",  # Advanced text substitutions
            "sphinx_removed_in",  # Deprecation notices
        ], )

    config["extensions"] = extensions
    return config


def _get_copybutton_config() -> dict[str, Any]:
    """Get copy button configuration."""
    return {
        "copybutton_prompt_text":
        (r">>> |\\.\\.\\. |\\$ |In \\[\\d*\\]: | {2,5}\\.\\.\\.: | {5,8}: "),
        "copybutton_prompt_is_regexp":
        True,
        "copybutton_exclude":
        ".linenos, .gp",
    }


def get_tabs_config() -> dict[str, Any]:
    """Get additional tabs configuration if needed."""
    return {
        # sphinx-tabs works out of the box
        # Add custom configurations here if needed
    }


def get_design_config() -> dict[str, Any]:
    """Get sphinx-design configuration."""
    return {
        # sphinx-design works out of the box
        # Add custom configurations here if needed
    }


def get_minimal_config() -> dict[str, Any]:
    """Get minimal enhancement configuration."""
    return get_config(
        enable_design=False,
        enable_interactive=False,
        enable_math=False,
        enable_emoji=False,
    )


def get_standard_config() -> dict[str, Any]:
    """Get standard enhancement configuration."""
    return get_config(
        enable_design=True,
        enable_interactive=True,
        enable_copybutton=True,
        enable_math=False,
        enable_emoji=False,
    )


def get_full_config() -> dict[str, Any]:
    """Get full enhancement configuration."""
    return get_config(
        enable_design=True,
        enable_interactive=True,
        enable_copybutton=True,
        enable_math=True,
        enable_emoji=True,
    )
