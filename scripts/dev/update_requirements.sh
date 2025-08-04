#!/usr/bin/env bash
set -e

# Update Poetry requirements.txt and sync to docs folder
# This script is run as a pre-commit hook whenever pyproject.toml or poetry.lock changes

echo "📦 Updating requirements.txt from Poetry..."

# 1. Export production dependencies to requirements.txt (no hashes for better portability)
poetry export -f requirements.txt --without-hashes -o requirements.txt

# 2. Also export with dev dependencies for development docs
poetry export -f requirements.txt --without-hashes --with dev -o requirements-dev.txt

# 3. Create docs directory if it doesn't exist
mkdir -p docs

# 4. Copy both files to docs folder
cp requirements.txt docs/requirements.txt
cp requirements-dev.txt docs/requirements-dev.txt

# 5. Stage the updated docs files
git add docs/requirements.txt docs/requirements-dev.txt

echo "✅ Requirements files updated and staged in docs/"
echo "   - docs/requirements.txt (production)"
echo "   - docs/requirements-dev.txt (with dev dependencies)"
exit 0
