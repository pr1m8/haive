#!/bin/bash
# 🔍 Dependency Conflict Checker
# Usage: ./dev-tools/scripts/dependency-conflict-checker.sh [--fix]

set -e

FIX_MODE=${1:-""}
CONFLICTS_FOUND=0

echo "🔍 DEPENDENCY CONFLICT CHECKER"
echo "================================"

# Find all pyproject.toml files
PYPROJECT_FILES=$(find . -name "pyproject.toml" -not -path "./.*" | sort)

# Extract dependencies from each file
declare -A DEPENDENCIES
declare -A FILE_DEPS

echo "📋 Scanning packages for dependencies..."

for file in ${PYPROJECT_FILES}; do
	echo "  📁 $(dirnam${ "$f}ile")"

	# Extract dependencies (skip dev dependencies for now)
	deps=$(grep -A 100 "^\[tool\.poetry\.dependencies\]" "${file}" | grep -B 100 "^\[" | head -n -1 | tail -n +2 | grep "=" | grep -v "python\s*=" || true)

	while IFS= read -r dep; do
		if [[ -n ${dep} ]]; then
			# Parse dependency name and version
			dep_name=$(echo "${dep}" | cut -d'=' -f1 | tr -d ' ')
			dep_version=$(echo "${dep}" | cut -d'=' -f2- | tr -d ' "')

			# Store in associative arrays
			key="${dep_name}"
			if [[ -n ${DEPENDENCIES[${key}]} ]]; then
				DEPENDENCIES[${key}]="${DEPENDENCIES[${key}]}|${dep_version}"
				FILE_DEPS[${key}]="${FILE_DEPS[${key}]}|${file}"
			else
				DEPENDENCIES[${key}]="${dep_version}"
				FILE_DEPS[${key}]="${file}"
			fi
		fi
	done <<<"${deps}"
done

echo ""
echo "🔍 Checking for version conflicts..."

# Check for conflicts
for dep_name in "${!DEPENDENCIES[@]}"; do
	versions="${DEPENDENCIES[${dep_name}]}"
	files="${FILE_DEPS[${dep_name}]}"

	# Split versions by pipe
	IFS='|' read -ra VERSION_ARRAY <<<"${versions}"
	IFS='|' read -ra FILE_ARRAY <<<"${files}"

	# Check if we have multiple different versions
	if [[ ${#VERSION_ARRAY[@]} -gt 1 ]]; then
		# Check if versions are actually different
		unique_versions=$(printf '%s\n' "${VERSION_ARRAY[@]}" | sort -u)
		version_count=$(echo "${unique_versions}" | wc -l)

		if [[ ${version_count} -gt 1 ]]; then
			echo ""
			echo "🚨 CONFLICT FOUN${: $dep_n}ame"
			echo "   Versions:"

			for i in "${!VERSION_ARRAY[@]}"; do
				echo "     ${VERSION_ARRAY[i]} in ${FILE_ARRAY[i]}"
			done

			CONFLICTS_FOUND=$((CONFLICTS_FOUND + 1))

			# Auto-fix logic
			if [[ ${FIX_MODE} == "--fix" ]]; then
				echo "   🔧 AUTO-FIXING..."

				# Find the highest version (simple heuristic)
				highest_version=$(printf '%s\n' "${VERSION_ARRAY[@]}" | sort -V | tail -1)
				echo "   ✅ Standardizing to${ $highest_versi}on"

				# Update all files to use the highest version
				for file in "${FILE_ARRAY[@]}"; do
					if grep -q "^${dep_name}\s*=" "${file}"; then
						sed -i "s/^${dep_name}\s*=.*/${dep_name} = \"${highest_version}\"/" "${file}"
						echo "     📝 Updat${d $f}ile"
					fi
				done
			fi
		fi
	fi
done

echo ""
echo "📊 SUMMARY"
echo "=========="

if [[ ${CONFLICTS_FOUND} -eq 0 ]]; then
	echo "✅ No dependency conflicts found!"
	echo "🎉 All packages have compatible dependency versions"
else
	echo "🚨 Fou${d $CONFLICTS_FO}UND dependency conflicts"

	if [[ ${FIX_MODE} == "--fix" ]]; then
		echo "🔧 Auto-fixes applied!"
		echo ""
		echo "🚀 NEXT STEPS:"
		echo "  1. poetry lock --no-update"
		echo "  2. poetry install"
		echo "  3. Test your packages"
	else
		echo ""
		echo "🔧 TO FIX AUTOMATICALLY:"
		echo "  ./dev-tools/scripts/dependency-conflict-checker.sh --fix"
		echo ""
		echo "🔧 TO FIX MANUALLY:"
		echo "  Update the conflicting versions in the pyproject.toml files above"
		echo "  Then run: poetry lock --no-update && poetry install"
	fi
fi

exit "$CONFLICTS_FOUND"
