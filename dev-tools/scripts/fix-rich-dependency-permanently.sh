#!/bin/bash

# 🔧 Permanent Rich Dependency Fixer
# Fixes the rich version conflict that keeps reverting in pyproject.toml

set -euo pipefail

echo "🔧 Fixing Rich Dependency Conflict Permanently..."

# Create backup
cp pyproject.toml pyproject.toml.backup.$(date +%Y%m%d_%H%M%S)

# Fix the root pyproject.toml
echo "📝 Updating root pyproject.toml..."
sed -i 's/rich = "\^13\.9\.4"/rich = "^14.1.0"/' pyproject.toml

# Verify the change
if grep -q 'rich = "\^14\.1\.0"' pyproject.toml; then
    echo "✅ Root pyproject.toml updated successfully"
else
    echo "❌ Failed to update root pyproject.toml"
    exit 1
fi

# Check all submodule pyproject.toml files for rich dependencies
echo "🔍 Checking submodule rich dependencies..."
for dir in packages/*/; do
    if [[ -f "$dir/pyproject.toml" ]]; then
        package_name=$(basename "$dir")
        if grep -q "rich.*=" "$dir/pyproject.toml"; then
            current_version=$(grep "rich.*=" "$dir/pyproject.toml" | head -1)
            echo "📦 $package_name: $current_version"
            
            # Update to 14.1.0 if different
            if ! grep -q 'rich = "\^14\.1\.0"' "$dir/pyproject.toml"; then
                echo "   📝 Updating $package_name to rich ^14.1.0..."
                sed -i 's/rich = "[^"]*"/rich = "^14.1.0"/' "$dir/pyproject.toml"
            fi
        else
            echo "📦 $package_name: No rich dependency"
        fi
    fi
done

# Remove all poetry.lock files to force clean resolution
echo "🧹 Removing stale lock files..."
find . -name "poetry.lock" -not -path "./.git/*" -delete

# Regenerate lock file
echo "🔄 Regenerating poetry.lock..."
if poetry lock; then
    echo "✅ Poetry lock successful!"
else
    echo "❌ Poetry lock failed - checking for remaining conflicts..."
    exit 1
fi

# Test the installation
echo "🧪 Testing installation..."
if poetry install --dry-run >/dev/null 2>&1; then
    echo "✅ Installation test passed!"
else
    echo "⚠️  Installation test failed - check dependencies"
fi

# Create a validation script to prevent future reverts
cat > dev-tools/scripts/validate-rich-dependency.sh << 'EOF'
#!/bin/bash
# Validates that rich dependency is consistent across all packages

echo "🔍 Validating rich dependency consistency..."

errors=0
expected_version="^14.1.0"

# Check root
root_version=$(grep 'rich = ' pyproject.toml | head -1 | sed 's/.*rich = "\([^"]*\)".*/\1/')
if [[ "$root_version" != "$expected_version" ]]; then
    echo "❌ Root pyproject.toml has rich = \"$root_version\", expected \"$expected_version\""
    errors=$((errors + 1))
fi

# Check submodules
for dir in packages/*/; do
    if [[ -f "$dir/pyproject.toml" ]] && grep -q "rich.*=" "$dir/pyproject.toml"; then
        package_name=$(basename "$dir")
        package_version=$(grep 'rich = ' "$dir/pyproject.toml" | head -1 | sed 's/.*rich = "\([^"]*\)".*/\1/')
        if [[ "$package_version" != "$expected_version" ]]; then
            echo "❌ $package_name has rich = \"$package_version\", expected \"$expected_version\""
            errors=$((errors + 1))
        fi
    fi
done

if [[ $errors -eq 0 ]]; then
    echo "✅ All rich dependencies are consistent at version $expected_version"
    exit 0
else
    echo "❌ Found $errors inconsistent rich dependencies"
    echo "💡 Run: ./dev-tools/scripts/fix-rich-dependency-permanently.sh"
    exit 1
fi
EOF

chmod +x dev-tools/scripts/validate-rich-dependency.sh

echo "🎉 Rich dependency fix complete!"
echo "📝 Run './dev-tools/scripts/validate-rich-dependency.sh' to check consistency"
echo "🔄 If this happens again, run this script to fix it permanently" 