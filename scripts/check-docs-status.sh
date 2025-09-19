#!/bin/bash
# check-docs-status.sh - Check documentation sync status and health across all haive packages
# Usage: ./scripts/check-docs-status.sh [reference_package]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Default reference package (what we compare against)
REFERENCE_PACKAGE="${1:-haive-core}"

# Base directory
BASE_DIR="/home/will/Projects/haive/packages"

# Package list - auto-detect from directories
PACKAGES=($(find "$BASE_DIR" -maxdepth 1 -name "haive-*" -type d -exec basename {} \;))

echo -e "${BLUE}📊 Documentation Sync Status Check${NC}"
echo -e "${BLUE}Reference package: ${REFERENCE_PACKAGE}${NC}"
echo ""

# Verify reference package exists
REFERENCE_DOCS="$BASE_DIR/$REFERENCE_PACKAGE/docs/source"
if [[ ! -d $REFERENCE_DOCS ]]; then
	echo -e "${RED}❌ Reference package docs not found: $REFERENCE_DOCS${NC}"
	exit 1
fi

# Global status counters
TOTAL_PACKAGES=0
SYNCED_PACKAGES=0
PARTIAL_PACKAGES=0
MISSING_PACKAGES=0
ISSUES_FOUND=0

# Arrays to track issues
declare -a CONF_ISSUES=()
declare -a STATIC_ISSUES=()
declare -a TEMPLATE_ISSUES=()
declare -a MISSING_DOCS=()

# Function to check file similarity (ignoring project-specific content)
check_file_similarity() {
	local ref_file="$1"
	local target_file="$2"
	local package="$3"

	if [[ ! -f $ref_file ]]; then
		return 2 # Reference file doesn't exist
	fi

	if [[ ! -f $target_file ]]; then
		return 1 # Target file doesn't exist
	fi

	# Create temp files with project names normalized
	local temp_ref=$(mktemp)
	local temp_target=$(mktemp)

	# Normalize project names for comparison
	sed "s/$REFERENCE_PACKAGE/PACKAGE_NAME/g" "$ref_file" |
		sed "s|github.com/pr1m8/$REFERENCE_PACKAGE|github.com/pr1m8/PACKAGE_NAME|g" >"$temp_ref"

	sed "s/$package/PACKAGE_NAME/g" "$target_file" |
		sed "s|github.com/pr1m8/$package|github.com/pr1m8/PACKAGE_NAME|g" >"$temp_target"

	# Compare normalized files
	if diff -q "$temp_ref" "$temp_target" >/dev/null 2>&1; then
		local result=0 # Files are essentially the same
	else
		local result=1 # Files differ
	fi

	# Cleanup
	rm -f "$temp_ref" "$temp_target"
	return $result
}

# Function to check essential static files
check_essential_static() {
	local ref_static="$1"
	local target_static="$2"
	local package="$3"
	local issues=""

	for file in custom.css tippy-enhancements.css favicon.ico logo.png; do
		if [[ -f "$ref_static/$file" ]]; then
			if [[ ! -f "$target_static/$file" ]]; then
				issues="$issues missing:$file"
			elif ! check_file_similarity "$ref_static/$file" "$target_static/$file" "$package"; then
				issues="$issues differs:$file"
			fi
		fi
	done

	# Check for unwanted files
	for unwanted in purple-theme.css purple-theme-enhanced.css code-purple-theme.css; do
		if [[ -f "$target_static/$unwanted" ]]; then
			issues="$issues unwanted:$unwanted"
		fi
	done

	echo "$issues"
}

# Function to check package documentation status
check_package_status() {
	local package="$1"
	local target_docs="$BASE_DIR/$package/docs/source"

	echo -e "${CYAN}📦 Checking $package...${NC}"

	# Skip if it's the reference package
	if [[ $package == "$REFERENCE_PACKAGE" ]]; then
		echo -e "   ${BLUE}ℹ️  Reference package${NC}"
		((SYNCED_PACKAGES++))
		return 0
	fi

	# Check if docs directory exists
	if [[ ! -d $target_docs ]]; then
		echo -e "   ${RED}❌ No docs directory${NC}"
		MISSING_DOCS+=("$package")
		((MISSING_PACKAGES++))
		return 1
	fi

	local status="✅"
	local issues=0
	local details=""

	# 1. Check conf.py
	if ! check_file_similarity "$REFERENCE_DOCS/conf.py" "$target_docs/conf.py" "$package"; then
		status="⚠️"
		details="$details conf.py-differs"
		CONF_ISSUES+=("$package")
		((issues++))
	elif [[ ! -f "$target_docs/conf.py" ]]; then
		status="❌"
		details="$details conf.py-missing"
		CONF_ISSUES+=("$package")
		((issues++))
	fi

	# 2. Check _static files
	local static_issues=""
	if [[ -d "$REFERENCE_DOCS/_static" ]]; then
		if [[ -d "$target_docs/_static" ]]; then
			static_issues=$(check_essential_static "$REFERENCE_DOCS/_static" "$target_docs/_static" "$package")
			if [[ -n $static_issues ]]; then
				status="⚠️"
				details="$details static:($static_issues)"
				STATIC_ISSUES+=("$package: $static_issues")
				((issues++))
			fi
		else
			status="❌"
			details="$details static-missing"
			STATIC_ISSUES+=("$package: directory missing")
			((issues++))
		fi
	fi

	# 3. Check _templates
	if [[ -d "$REFERENCE_DOCS/_templates" ]]; then
		if [[ ! -d "$target_docs/_templates" ]]; then
			status="❌"
			details="$details templates-missing"
			TEMPLATE_ISSUES+=("$package: directory missing")
			((issues++))
		else
			# Check if templates are reasonably similar (count files)
			local ref_count=$(find "$REFERENCE_DOCS/_templates" -type f | wc -l)
			local target_count=$(find "$target_docs/_templates" -type f | wc -l)

			if [[ $target_count -lt $((ref_count - 1)) ]]; then
				status="⚠️"
				details="$details templates-incomplete"
				TEMPLATE_ISSUES+=("$package: $target_count/$ref_count files")
				((issues++))
			fi
		fi
	fi

	# 4. Try a quick build test (optional, can be slow)
	# Commented out for speed, uncomment if you want build testing
	# if command -v sphinx-build >/dev/null 2>&1; then
	#     if ! (cd "$BASE_DIR/$package" && timeout 30s sphinx-build -q -b html docs/source /tmp/test_build_$package >/dev/null 2>&1); then
	#         status="⚠️"
	#         details="$details build-fails"
	#         ((issues++))
	#     fi
	#     rm -rf /tmp/test_build_$package 2>/dev/null || true
	# fi

	# Update counters
	if [[ $issues -eq 0 ]]; then
		echo -e "   ${GREEN}$status Fully synced${NC}"
		((SYNCED_PACKAGES++))
	elif [[ $issues -le 2 ]]; then
		echo -e "   ${YELLOW}$status Partially synced${NC} ${details}"
		((PARTIAL_PACKAGES++))
	else
		echo -e "   ${RED}$status Major issues${NC} ${details}"
		((ISSUES_FOUND++))
	fi

	((TOTAL_PACKAGES++))
}

# Check all packages
echo -e "${BLUE}📋 Found packages: ${PACKAGES[*]}${NC}"
echo ""

for package in "${PACKAGES[@]}"; do
	check_package_status "$package"
done

echo ""
echo -e "${PURPLE}📊 Summary Report${NC}"
echo "============================================="
printf "%-20s %3d\n" "Total packages:" $((${#PACKAGES[@]}))
printf "%-20s %3d\n" "Fully synced:" $SYNCED_PACKAGES
printf "%-20s %3d\n" "Partially synced:" $PARTIAL_PACKAGES
printf "%-20s %3d\n" "Major issues:" $ISSUES_FOUND
printf "%-20s %3d\n" "Missing docs:" $MISSING_PACKAGES
echo ""

# Detailed issue breakdown
if [[ ${#CONF_ISSUES[@]} -gt 0 ]]; then
	echo -e "${YELLOW}⚠️  conf.py Issues:${NC}"
	for issue in "${CONF_ISSUES[@]}"; do
		echo "   • $issue"
	done
	echo ""
fi

if [[ ${#STATIC_ISSUES[@]} -gt 0 ]]; then
	echo -e "${YELLOW}⚠️  _static Issues:${NC}"
	for issue in "${STATIC_ISSUES[@]}"; do
		echo "   • $issue"
	done
	echo ""
fi

if [[ ${#TEMPLATE_ISSUES[@]} -gt 0 ]]; then
	echo -e "${YELLOW}⚠️  _templates Issues:${NC}"
	for issue in "${TEMPLATE_ISSUES[@]}"; do
		echo "   • $issue"
	done
	echo ""
fi

if [[ ${#MISSING_DOCS[@]} -gt 0 ]]; then
	echo -e "${RED}❌ Missing Documentation:${NC}"
	for package in "${MISSING_DOCS[@]}"; do
		echo "   • $package (no docs/source directory)"
	done
	echo ""
fi

# Overall health score
TOTAL_POSSIBLE=$((${#PACKAGES[@]}))
HEALTH_SCORE=$(((SYNCED_PACKAGES * 100) / TOTAL_POSSIBLE))

echo -e "${BLUE}🎯 Overall Health Score: ${HEALTH_SCORE}%${NC}"

if [[ $HEALTH_SCORE -ge 90 ]]; then
	echo -e "${GREEN}🎉 Excellent! Documentation is well synchronized.${NC}"
	EXIT_CODE=0
elif [[ $HEALTH_SCORE -ge 70 ]]; then
	echo -e "${YELLOW}👍 Good! Minor sync issues to address.${NC}"
	EXIT_CODE=0
elif [[ $HEALTH_SCORE -ge 50 ]]; then
	echo -e "${YELLOW}⚠️  Fair. Consider running sync-docs-config.sh${NC}"
	EXIT_CODE=1
else
	echo -e "${RED}🚨 Poor. Documentation sync needed urgently!${NC}"
	EXIT_CODE=2
fi

echo ""
echo -e "${CYAN}💡 Recommendations:${NC}"

if [[ $ISSUES_FOUND -gt 0 || $PARTIAL_PACKAGES -gt 0 ]]; then
	echo -e "   ${BLUE}1. Run sync script:${NC} ./scripts/sync-docs-config.sh"
fi

if [[ ${#MISSING_DOCS[@]} -gt 0 ]]; then
	echo -e "   ${BLUE}2. Initialize missing docs:${NC} Create docs/source directories"
fi

if [[ $HEALTH_SCORE -lt 90 ]]; then
	echo -e "   ${BLUE}3. Re-check after fixes:${NC} ./scripts/check-docs-status.sh"
fi

echo -e "   ${BLUE}4. Build test:${NC} cd packages/[package] && poetry run sphinx-build docs/source docs/build"

exit $EXIT_CODE
