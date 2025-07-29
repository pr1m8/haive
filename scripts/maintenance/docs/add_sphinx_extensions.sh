#!/bin/bash
# Add all possible Sphinx extensions for world-class documentation

set -e

echo "🚀 Installing comprehensive Sphinx extensions for Haive..."
echo "================================================"

# Core documentation quality
echo "📊 Installing documentation quality tools..."
poetry add --group dev \
	darglint \
	docstr-coverage \
	docformatter \
	pydocstyle \
	rstcheck-core \
	interrogate \
	doc8 \
	flake8-docstrings \
	flake8-rst-docstrings \
	pyroma ||
	true

# Spell checking and prose
echo "🔤 Installing spell checking and prose tools..."
poetry add --group dev \
	codespell \
	pyspelling \
	proselint \
	vale ||
	true

# Testing documentation
echo "🧪 Installing documentation testing tools..."
poetry add --group dev \
	pytest-doctestplus \
	pytest-checkdocs \
	sphinx-testing \
	pytest-markdown-docs ||
	true

# Core Sphinx extensions
echo "🎨 Installing core Sphinx extensions..."
poetry add --group docs \
	sphinx-autodoc-typehints \
	autodoc-pydantic \
	autodocsumm \
	sphinx-autosummary-accessors \
	sphinx-autoapi \
	sphinx-autodocgen \
	sphinx-napoleon \
	sphinxcontrib-fulltoc ||
	true

# UI/UX enhancements
echo "💎 Installing UI/UX enhancement extensions..."
poetry add --group docs \
	sphinx-design \
	sphinx-tabs \
	sphinx-togglebutton \
	sphinx-inline-tabs \
	sphinx-copybutton \
	sphinx-codeautolink \
	sphinx-prompt \
	sphinx-tippy \
	sphinx-hoverxref \
	sphinxemoji ||
	true

# Visualization and media
echo "📊 Installing visualization extensions..."
poetry add --group docs \
	sphinxcontrib-mermaid \
	sphinxcontrib-plantuml \
	sphinxcontrib-drawio \
	sphinxcontrib-youtube \
	sphinxcontrib-images \
	sphinxcontrib-seqdiag \
	sphinxcontrib-blockdiag ||
	true

# API and code documentation
echo "🔌 Installing API documentation extensions..."
poetry add --group docs \
	sphinxcontrib-openapi \
	sphinxcontrib-httpdomain \
	sphinx-click \
	sphinx-argparse \
	sphinx-jsonschema ||
	true

# Navigation and discovery
echo "🗺️ Installing navigation extensions..."
poetry add --group docs \
	sphinx-sitemap \
	sphinx-search \
	readthedocs-sphinx-search \
	sphinx-autobuild \
	sphinx-multiversion ||
	true

# Advanced features
echo "🚀 Installing advanced feature extensions..."
poetry add --group docs \
	myst-parser \
	myst-nb \
	jupyter-book \
	nbsphinx \
	sphinx-gallery \
	sphinx-last-updated-by-git \
	sphinxext-opengraph \
	sphinx-needs \
	sphinx-external-toc \
	sphinx-thebe ||
	true

# Themes
echo "🎨 Installing additional themes..."
poetry add --group docs \
	pydata-sphinx-theme \
	sphinx-modern-theme \
	sphinx-typlog-theme \
	sphinx-basic-ng ||
	true

# Development tools
echo "🔧 Installing development extensions..."
poetry add --group docs \
	sphinx-lint \
	sphinx-pyproject \
	sphinx-version-warning \
	sphinx-notfound-page \
	sphinx-favicon \
	sphinx-contributors \
	sphinx-intl \
	sphinx-git ||
	true

# Specialized extensions
echo "🎯 Installing specialized extensions..."
poetry add --group docs \
	sphinx-jinja \
	sphinx-examples \
	sphinx-removed-in \
	sphinx-selective-exclude \
	sphinx-substitution-extensions \
	sphinx-paramlinks \
	sphinx-math-dollar \
	sphinxext-rediraffe ||
	true

# Educational extensions
echo "📚 Installing educational extensions..."
poetry add --group docs \
	sphinx-exercise \
	sphinx-proof \
	sphinx-revealjs ||
	true

# Alternative documentation systems (for comparison/migration)
echo "📦 Installing alternative documentation systems..."
poetry add --group docs \
	mkdocs \
	mkdocs-material \
	mkdocstrings \
	pdoc ||
	true

echo ""
echo "✅ Installation complete!"
echo ""
echo "📝 Next steps:"
echo "1. Update docs/source/conf.py with the new extensions"
echo "2. Run: poetry run python scripts/doc_quality_pipeline.py"
echo "3. Build docs: poetry run sphinx-build -b html docs/source docs/build/html"
echo "4. View docs: python -m http.server 8000 --directory docs/build/html"
