#!/bin/bash
# Build docs with workarounds for the NoneType issue

echo "🔧 Building docs with workarounds..."

# Clean build directory
rm -rf docs/build/html

# Set environment to use minimal profile and single process
export SPHINX_PACKAGES=core
export SPHINX_PROFILE=minimal
export SPHINX_FAST_IMPORTS=1
export SPHINX_PARALLEL_JOBS=1 # Force single process

# Run sphinx-build with single job (-j 1)
echo "🚀 Running sphinx-build with -j 1 (single process)..."
poetry run sphinx-build -b html -j 1 -E docs/source docs/build/html 2>&1 | tee build_fixed.log

echo "✅ Build complete. Check build_fixed.log for details."
