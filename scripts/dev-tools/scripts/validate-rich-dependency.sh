#!/bin/bash
# Validates that rich dependency is consistent across all packages

echo "🔍 Validating rich dependency consistency..."

errors=0
expected_version="^14.1.0"

# Check root
root_version=""
if grep -q 'rich = ' pyproject.toml; then
	root_version=$(grep 'rich = ' pyproject.toml | head -1 | sed 's/.*rich = "\([^"]*\)".*/\1/')
fi

if [[ ${root_version} != "${expected_version}" ]]; then
	echo "❌ Root pyproject.toml has rich = \"${root_version}\", expected \"${expected_version}\""
	errors=$((errors + 1))
fi

# Check submodules
for dir in packages/*/; do
	if [[ -f "${dir}/pyproject.toml" ]] && grep -q "rich.*=" "${dir}/pyproject.toml"; then
		package_name=$(basename "${dir}")
		package_version=""
		if grep -q 'rich = ' "${dir}/pyproject.toml"; then
			package_version=$(grep 'rich = ' "${dir}/pyproject.toml" | head -1 | sed 's/.*rich = "\([^"]*\)".*/\1/')
		fi
		if [[ ${package_version} != "${expected_version}" ]]; then
			echo "❌ ${package_name} has rich = \"${package_version}\", expected \"${expected_version}\""
			errors=$((errors + 1))
		fi
	fi
done

if [[ ${errors} -eq 0 ]]; then
	echo "✅ All rich dependencies are consistent at version ${expected_version}"
	exit 0
else
	echo "❌ Found ${errors} inconsistent rich dependencies"
	echo "💡 Run: ./dev-tools/scripts/fix-rich-dependency-permanently.sh"
	exit 1
fi
