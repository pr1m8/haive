#!/usr/bin/env python3
"""Capture type hint warnings from Sphinx build."""
from __future__ import annotations

import re
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path


def create_minimal_conf():
    """Create a minimal conf.py focused on type warnings."""

    minimal_conf = """
import sys
from pathlib import Path

# Add source paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Minimal extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "autoapi.extension",
]

# Project info
project = "Haive Test"
version = "1.0.0"

# AutoAPI configuration - just haive-core for speed
autoapi_dirs = ["packages/haive-core/src"]
autoapi_type = "python"
autoapi_root = "api"
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "special-members",
    "imported-members",
]

autoapi_ignore = [
    "*conftest*",
    "*test_*",
    "*/tests/*",
    "*__pycache__*",
]

# Type hint configuration
autodoc_typehints = "description"
typehints_fully_qualified = False
autodoc_typehints_format = "short"

# Enable nitpicky mode with minimal ignores to see what we need
nitpicky = True
nitpick_ignore = [
    # Only the most basic types
    ("py:class", "str"),
    ("py:class", "int"),
    ("py:class", "bool"),
    ("py:class", "dict"),
    ("py:class", "list"),
    ("py:class", "Any"),
]

# Minimal theme
html_theme = "alabaster"

# Suppress non-type warnings
suppress_warnings = ["autoapi.not_readable"]

# Intersphinx for basic Python types
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
"""

    return minimal_conf


def run_test_build():
    """Run a test build to capture type warnings."""

    # Create temp config
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.py',
        prefix='test_conf_',
        dir='docs/source',
        delete=False,
    ) as f:
        f.write(create_minimal_conf())
        temp_conf = f.name

    try:
        # Create temp build directory
        temp_build = Path('docs/build/type_test')
        temp_build.mkdir(parents=True, exist_ok=True)

        # Run build
        cmd = [
            'poetry',
            'run',
            'sphinx-build',
            '-b',
            'html',
            '-c',
            'docs/source',  # Config directory
            '-D',
            f"extensions.conf={Path(temp_conf).stem}",  # Use our config
            '-n',  # Nitpicky mode
            '-w',
            'type_warnings.log',  # Warning log
            '-E',  # Don't use cached environment
            '--keep-going',  # Continue on errors
            'docs/source',
            str(temp_build),
        ]

        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )

        return result.stdout + result.stderr, Path('type_warnings.log')

    finally:
        # Clean up
        Path(temp_conf).unlink(missing_ok=True)


def extract_type_warnings(text: str):
    """Extract type reference warnings from text."""

    patterns = [
        r'py:class reference target not found: (.+)',
        r'py:obj reference target not found: (.+)',
        r'py:attr reference target not found: (.+)',
        r'py:func reference target not found: (.+)',
        r'py:meth reference target not found: (.+)',
        r'py:mod reference target not found: (.+)',
        r'py:exc reference target not found: (.+)',
        r'py:data reference target not found: (.+)',
    ]

    warnings = defaultdict(set)

    for line in text.split('\n'):
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                ref_type = pattern.split()[0].replace('(', '').replace(')', '')
                target = match.group(1).strip()
                warnings[ref_type].add(target)

    return warnings


def categorize_references(warnings):
    """Categorize missing references by type/module."""

    categories = {
        'langchain_core': [],
        'langchain': [],
        'pydantic': [],
        'typing_extensions': [],
        'haive_internal': [],
        'external_libs': [],
        'generic_types': [],
        'unknown': [],
    }

    for ref_type, targets in warnings.items():
        for target in targets:
            clean_target = target.split('[')[0].strip()

            if 'langchain_core' in clean_target:
                categories['langchain_core'].append((ref_type, clean_target))
            elif 'langchain' in clean_target:
                categories['langchain'].append((ref_type, clean_target))
            elif 'pydantic' in clean_target:
                categories['pydantic'].append((ref_type, clean_target))
            elif 'typing_extensions' in clean_target:
                categories['typing_extensions'].append((ref_type, clean_target))
            elif clean_target.startswith('haive.'):
                categories['haive_internal'].append((ref_type, clean_target))
            elif (len(clean_target) == 1 and clean_target.isupper()) or any(
                x in clean_target for x in ['T', '~', 'TypeVar']
            ):
                categories['generic_types'].append((ref_type, clean_target))
            else:
                categories['external_libs'].append((ref_type, clean_target))

    return categories


def main():
    """Main function."""

    print('Running test build to capture type warnings...')

    try:
        output, log_file = run_test_build()

        # Read warnings
        warning_text = ''
        if log_file and log_file.exists():
            warning_text = log_file.read_text()
            log_file.unlink()  # Clean up

        # Also check output
        full_text = output + '\n' + warning_text

        # Extract warnings
        warnings = extract_type_warnings(full_text)

        if not warnings:
            print('No type reference warnings found.')
            print('This might mean:')
            print('1. All types are properly resolved')
            print('2. The build failed before generating warnings')
            print('3. Warnings are being suppressed')
            return

        # Show summary
        print('\n=== Type Reference Warnings Summary ===')
        total = sum(len(targets) for targets in warnings.values())
        print(f"Total unique missing references: {total}")

        for ref_type, targets in warnings.items():
            if targets:
                print(f"{ref_type}: {len(targets)} missing")

        # Categorize
        categories = categorize_references(warnings)

        print('\n=== By Category ===')
        for category, items in categories.items():
            if items:
                print(f"{category}: {len(items)} items")

        # Generate nitpick_ignore additions
        additions = []

        print('\n=== Suggested nitpick_ignore additions ===')
        for category, items in categories.items():
            if not items:
                continue

            print(f"\n# {category}")
            for ref_type, target in sorted(set(items)):
                addition = f'    ("{ref_type}", "{target}"),'
                print(addition)
                additions.append(addition)

        # Save to file
        if additions:
            output_file = Path('nitpick_ignore_additions.txt')
            output_file.write_text('\n'.join(additions))
            print(f"\nAdditions saved to: {output_file}")

    except subprocess.TimeoutExpired:
        print('Build timed out - this is common with full builds')
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
