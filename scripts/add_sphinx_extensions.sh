#!/bin/bash
# Script to add missing Sphinx extensions via poetry

echo "🚀 Adding missing Sphinx extensions to Haive documentation..."

# Core Extensions
echo "📦 Adding core Sphinx extensions..."
poetry add --group docs \
	sphinx-autosummary-accessors \
	sphinx-issues \
	sphinx-jsonschema \
	sphinx-pyproject \
	sphinx-paramlinks \
	sphinx-math-dollar \
	sphinxemoji

# Advanced Features
echo "📦 Adding advanced Sphinx features..."
poetry add --group docs \
	sphinx-copydir \
	sphinx-lint \
	sphinx-last-updated-by-git \
	sphinxext-rediraffe

# Visualization
echo "📦 Adding visualization extensions..."
poetry add --group docs \
	sphinxcontrib-plantuml \
	sphinxcontrib-drawio \
	sphinxcontrib-images \
	sphinxcontrib-seqdiag \
	sphinxcontrib-blockdiag

# Additional Quality
echo "📦 Adding additional quality tools..."
poetry add --group docs \
	sphinx-autodocgen \
	sphinxcontrib-fulltoc \
	sphinx-basic-ng

# External Tools
echo "📦 Adding external documentation tools..."
poetry add --group docs \
	sphinx-external-toc \
	sphinx-thebe

echo "✅ All extensions added successfully!"
