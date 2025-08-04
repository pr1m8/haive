#!/usr/bin/env python3
"""Sphinx Extensions Integration Script Automatically integrates all installed
Sphinx extensions into conf.py.

Created: 2025-07-29 17:00
Purpose: Smart integration of 100+ Sphinx extensions with proper import names
"""

from __future__ import annotations

import importlib
import json
from pathlib import Path
import re
import subprocess
import sys

# Configuration
CONF_PY_PATH = Path(
    '/home/will/Projects/haive/backend/haive/docs/source/conf.py')
EXTENSIONS_LOG = Path(
    '/home/will/Projects/haive/backend/haive/docs/logs/extensions_integration.log',
)
BACKUP_CONF = Path(
    '/home/will/Projects/haive/backend/haive/docs/source/conf_backup_integration.py',
)

# Known extension import name mappings (from our research)
IMPORT_NAME_MAPPINGS = {
    # Package name -> correct import name
    'sphinx-hoverxref': 'hoverxref.extension',
    'sphinx-notfound-page': 'notfound.extension',
    'sphinx-autoapi': 'autoapi.extension',
    'sphinxemoji': 'sphinxemoji.sphinxemoji',
    'sphinx-issues': 'sphinx_issues',  # underscore
    'sphinx-contributors': 'sphinx_contributors',  # underscore
    'sphinx-external-toc': 'sphinx_external_toc',  # underscore
    'sphinx-thebe': 'sphinx_thebe',
    'myst-nb': 'myst_nb',
    'sphinx-favicon': 'sphinx_favicon',
    'sphinx-last-updated-by-git': 'sphinx_last_updated_by_git',
    'sphinx-tippy': 'sphinx_tippy',
    'sphinx-paramlinks': 'sphinx_paramlinks',
    'sphinx-selective-exclude': 'sphinx_selective_exclude',
    'sphinxcontrib-drawio': 'sphinxcontrib.drawio',
    'sphinx-version-warning': 'sphinx_version_warning',
    'sphinx-substitution-extensions': 'sphinx_substitution_extensions',
    # Add more as discovered...
}

# Extensions to skip (not Sphinx extensions)
SKIP_EXTENSIONS = {
    'babel',
    'beautifulsoup4',
    'certifi',
    'charset-normalizer',
    'click',
    'colorama',
    'markdown',
    'markupsafe',
    'packaging',
    'pillow',
    'requests',
    'setuptools',
    'six',
    'urllib3',
    'wheel',
    'numexpr',
    'bottleneck',
    'mkdocs',
    'mkdocs-material',
    'mkdocs-autorefs',
    'mkdocstrings',
    'nbconvert',
    'nbformat',
    'notebook',
    'jupyter-client',
    'jupyter-core',
    'pydantic',
    'pydantic-core',
    'fastapi',
    'uvicorn',
    'langchain-core',
}


def log_message(message: str, also_print: bool = True):
    """Log message to file and optionally print."""
    EXTENSIONS_LOG.parent.mkdir(exist_ok=True)
    with open(EXTENSIONS_LOG, 'a') as f:
        f.write(f"{message}\n")
    if also_print:
        pass


def get_installed_packages() -> list[str]:
    """Get all installed packages from poetry."""
    try:
        result = subprocess.run(
            ['poetry', 'show', '--only', 'docs'],
            capture_output=True,
            text=True,
            check=True,
        )
        packages = []
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                package_name = line.split()[0]
                packages.append(package_name)
        return packages
    except subprocess.CalledProcessError as e:
        log_message(f"❌ Error getting packages: {e}")
        return []


def get_sphinx_extensions(packages: list[str]) -> list[str]:
    """Filter packages to get only Sphinx extensions."""
    sphinx_extensions = []

    for package in packages:
        # Skip known non-Sphinx packages
        if package.lower() in SKIP_EXTENSIONS:
            continue

        # Include packages that look like Sphinx extensions
        if any(pattern in package.lower()
               for pattern in ['sphinx', 'myst', 'autodoc', 'docutils']):
            sphinx_extensions.append(package)

    return sphinx_extensions


def guess_import_name(package_name: str) -> str:
    """Guess the correct import name for a package."""
    # Check our known mappings first
    if package_name in IMPORT_NAME_MAPPINGS:
        return IMPORT_NAME_MAPPINGS[package_name]

    # Apply common patterns
    import_name = package_name

    # Replace hyphens with underscores
    import_name = import_name.replace('-', '_')

    # Handle sphinxcontrib packages
    if import_name.startswith('sphinxcontrib_'):
        import_name = import_name.replace('sphinxcontrib_', 'sphinxcontrib.')

    return import_name


def test_extension_import(import_name: str) -> tuple[bool, str]:
    """Test if an extension can be imported."""
    try:
        # Try importing the main module
        main_module = import_name.split('.')[0]
        importlib.import_module(main_module)
        return True, '✅ Import successful'
    except ImportError as e:
        return False, f"❌ Import failed: {e}"
    except Exception as e:
        return False, f"❌ Other error: {e}"


def get_current_extensions() -> set[str]:
    """Get currently configured extensions from conf.py."""
    current_extensions = set()

    if not CONF_PY_PATH.exists():
        return current_extensions

    with open(CONF_PY_PATH) as f:
        content = f.read()

    # Find extensions = [...] block
    extensions_match = re.search(r'extensions\s*=\s*\[(.*?)\]', content,
                                 re.DOTALL)
    if extensions_match:
        extensions_text = extensions_match.group(1)
        # Extract quoted strings
        for match in re.finditer(r'"([^"]+)"', extensions_text):
            current_extensions.add(match.group(1))

    return current_extensions


def backup_conf_py():
    """Create backup of conf.py."""
    if CONF_PY_PATH.exists():
        import shutil

        shutil.copy2(CONF_PY_PATH, BACKUP_CONF)
        log_message(f"📋 Backup created: {BACKUP_CONF}")


def integrate_extensions():
    """Main integration function."""
    log_message('🚀 Starting Sphinx Extensions Integration')
    log_message('=' * 60)

    # Backup conf.py
    backup_conf_py()

    # Get installed packages
    log_message('📦 Getting installed packages...')
    packages = get_installed_packages()
    log_message(f"Found {len(packages)} total packages")

    # Filter to Sphinx extensions
    sphinx_packages = get_sphinx_extensions(packages)
    log_message(f"Found {len(sphinx_packages)} potential Sphinx extensions")

    # Get current extensions
    current_extensions = get_current_extensions()
    log_message(
        f"Currently have {len(current_extensions)} extensions configured")

    # Test each extension
    log_message('\n🔍 Testing extension imports...')
    log_message('-' * 40)

    working_extensions = []
    failed_extensions = []
    new_extensions = []

    for package in sphinx_packages:
        import_name = guess_import_name(package)
        success, message = test_extension_import(import_name)

        log_message(f"{package:30} -> {import_name:30} {message}")

        if success:
            working_extensions.append((package, import_name))
            if import_name not in current_extensions:
                new_extensions.append((package, import_name))
        else:
            failed_extensions.append((package, import_name, message))

    # Summary
    log_message('\n📊 Integration Summary')
    log_message('=' * 40)
    log_message(f"✅ Working extensions: {len(working_extensions)}")
    log_message(f"❌ Failed extensions: {len(failed_extensions)}")
    log_message(f"🆕 New extensions to add: {len(new_extensions)}")

    # Show new extensions to add
    if new_extensions:
        log_message('\n🆕 New Extensions Ready to Add:')
        log_message('-' * 40)
        for package, import_name in new_extensions:
            log_message(f"  '{import_name}',  # {package}")

    # Show failed extensions
    if failed_extensions:
        log_message('\n❌ Failed Extensions (need research):')
        log_message('-' * 40)
        for package, import_name, error in failed_extensions:
            log_message(f"  {package} -> {import_name}")
            log_message(f"    Error: {error}")

    # Generate conf.py addition
    if new_extensions:
        log_message('\n📝 Add to conf.py extensions list:')
        log_message('-' * 40)
        log_message('extensions.extend([')
        for package, import_name in new_extensions:
            log_message(f'    "{import_name}",  # {package}')
        log_message('])')

    # Save results to JSON for further processing
    results = {
        'working_extensions':
        working_extensions,
        'failed_extensions':
        [(pkg, imp, err) for pkg, imp, err in failed_extensions],
        'new_extensions':
        new_extensions,
        'current_extensions':
        list(current_extensions),
        'total_packages':
        len(packages),
        'sphinx_packages':
        len(sphinx_packages),
    }

    results_file = EXTENSIONS_LOG.parent / 'extension_integration_results.json'
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

    log_message(f"\n💾 Results saved to: {results_file}")
    log_message(f"📋 Full log saved to: {EXTENSIONS_LOG}")

    return results


if __name__ == '__main__':
    # Ensure we're in the right directory
    import os

    os.chdir('/home/will/Projects/haive/backend/haive')

    try:
        results = integrate_extensions()

        if results['new_extensions']:
            pass

    except Exception as e:
        log_message(f"💥 Fatal error: {e}")
        sys.exit(1)
