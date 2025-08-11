#!/bin/bash
# Test Sphinx build with enhanced configuration

echo "======================================================================="
echo "SPHINX TEST BUILD WITH AUTODOC-PYDANTIC AND WARNING FIXES"
echo "======================================================================="

# Set up environment
export SPHINX_PACKAGES="all"
export PYTHONPATH="/home/will/Projects/haive/backend/haive/packages/haive-core/src:$PYTHONPATH"

# Clean previous build
echo "🧹 Cleaning previous build..."
rm -rf docs/build/test_build

# Create test build directory
mkdir -p docs/build/test_build

# Run sphinx build with test configuration
echo ""
echo "🔨 Running Sphinx build with test configuration..."
echo "======================================================================="

# Use the test configuration file
poetry run sphinx-build -b html \
	-c docs/source \
	-C "sys.path.insert(0, 'docs/source'); from conf_test_autodoc_pydantic import *" \
	docs/source \
	docs/build/test_build \
	-v \
	-W --keep-going \
	2>&1 | tee sphinx_test_build.log

# Check results
if [ $? -eq 0 ]; then
	echo ""
	echo "✅ BUILD SUCCESSFUL!"
else
	echo ""
	echo "❌ BUILD FAILED - Check sphinx_test_build.log for details"
fi

# Count warnings and errors
echo ""
echo "======================================================================="
echo "BUILD ANALYSIS"
echo "======================================================================="

# Count different types of warnings
echo "📊 Warning Summary:"
echo "  - Total warnings: $(grep -c "WARNING:" sphinx_test_build.log || echo 0)"
echo "  - Reference warnings: $(grep -c "reference target not found" sphinx_test_build.log || echo 0)"
echo "  - Duplicate warnings: $(grep -c "duplicate object description" sphinx_test_build.log || echo 0)"
echo "  - AutoAPI warnings: $(grep -c "autoapi" sphinx_test_build.log || echo 0)"

# Count generated files
echo ""
echo "📁 Generated Files:"
echo "  - Total HTML files: $(find docs/build/test_build -name "*.html" | wc -l)"
echo "  - API doc files: $(find docs/build/test_build/api -name "*.html" 2>/dev/null | wc -l || echo 0)"

# Show unique warning types
echo ""
echo "🔍 Unique Warning Types:"
grep "WARNING:" sphinx_test_build.log |
	sed 's/.*WARNING: //' |
	sed 's/ reference target not found:.*/: reference target not found/' |
	sed 's/ duplicate object description of.*/: duplicate object description/' |
	sort | uniq -c | sort -nr | head -20

# Check if autodoc-pydantic is available
echo ""
echo "📦 Extension Check:"
if poetry run python -c "import sphinxcontrib.autodoc_pydantic" 2>/dev/null; then
	echo "  ✅ autodoc-pydantic is installed"
else
	echo "  ❌ autodoc-pydantic NOT installed - run: poetry add --group docs autodoc-pydantic"
fi

echo ""
echo "======================================================================="
echo "Full build log saved to: sphinx_test_build.log"
echo "Test build output in: docs/build/test_build/"
echo "======================================================================="
