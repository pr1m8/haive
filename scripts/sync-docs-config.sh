#!/bin/bash
# sync-docs-config.sh - Sync documentation configuration across all haive packages
# Usage: ./scripts/sync-docs-config.sh [source_package]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default source package (the "golden" config)
SOURCE_PACKAGE="${1:-haive-core}"

# Base directory
BASE_DIR="/home/will/Projects/haive/packages"

# Package list - auto-detect from directories
PACKAGES=($(find "$BASE_DIR" -maxdepth 1 -name "haive-*" -type d -exec basename {} \;))

echo -e "${BLUE}🔄 Syncing documentation configuration across haive packages${NC}"
echo -e "${BLUE}Source package: ${SOURCE_PACKAGE}${NC}"
echo ""

# Verify source package exists and has docs
SOURCE_DOCS="$BASE_DIR/$SOURCE_PACKAGE/docs/source"
if [[ ! -d $SOURCE_DOCS ]]; then
	echo -e "${RED}❌ Source package docs not found: $SOURCE_DOCS${NC}"
	exit 1
fi

if [[ ! -f "$SOURCE_DOCS/conf.py" ]]; then
	echo -e "${RED}❌ Source conf.py not found: $SOURCE_DOCS/conf.py${NC}"
	exit 1
fi

echo -e "${GREEN}✅ Source configuration found${NC}"
echo ""

# Function to sync configuration for a package
sync_package() {
	local package="$1"
	local target_docs="$BASE_DIR/$package/docs/source"

	echo -e "${YELLOW}📦 Processing $package...${NC}"

	# Skip if no docs directory
	if [[ ! -d $target_docs ]]; then
		echo -e "   ${YELLOW}⚠️  No docs directory, skipping${NC}"
		return
	fi

	# Skip if it's the source package
	if [[ $package == "$SOURCE_PACKAGE" ]]; then
		echo -e "   ${BLUE}ℹ️  Source package, skipping${NC}"
		return
	fi

	echo -e "   ${BLUE}🔄 Syncing configuration...${NC}"

	# 1. Copy conf.py and customize
	cp "$SOURCE_DOCS/conf.py" "$target_docs/conf.py"

	# 2. Update project name
	sed -i "s/project = \"$SOURCE_PACKAGE\"/project = \"$package\"/" "$target_docs/conf.py"

	# 3. Update GitHub URLs - handle both cases
	if [[ $SOURCE_PACKAGE == "haive-core" ]]; then
		# Replace haive-core with the target package
		sed -i "s|github.com/pr1m8/haive-core|github.com/pr1m8/$package|g" "$target_docs/conf.py"
	else
		# Replace source package with target package
		sed -i "s|github.com/pr1m8/$SOURCE_PACKAGE|github.com/pr1m8/$package|g" "$target_docs/conf.py"
	fi

	# 4. Sync _static files (only the ones actually used)
	if [[ -d "$SOURCE_DOCS/_static" ]]; then
		mkdir -p "$target_docs/_static"

		# Copy only essential files
		for file in custom.css tippy-enhancements.css favicon.ico logo.png; do
			if [[ -f "$SOURCE_DOCS/_static/$file" ]]; then
				cp "$SOURCE_DOCS/_static/$file" "$target_docs/_static/"
				echo -e "   ${GREEN}📄 Copied $file${NC}"
			fi
		done

		# Clean up any unused CSS files in target
		for unused in purple-theme.css purple-theme-enhanced.css code-purple-theme.css; do
			if [[ -f "$target_docs/_static/$unused" ]]; then
				rm "$target_docs/_static/$unused"
				echo -e "   ${YELLOW}🗑️  Removed unused $unused${NC}"
			fi
		done
	fi

	# 5. Sync _templates directory (if it exists)
	if [[ -d "$SOURCE_DOCS/_templates" ]]; then
		echo -e "   ${BLUE}📋 Syncing templates...${NC}"

		# Remove existing templates directory and copy fresh
		rm -rf "$target_docs/_templates"
		cp -r "$SOURCE_DOCS/_templates" "$target_docs/_templates"

		# Clean up any build artifacts in templates
		find "$target_docs/_templates" -name "*.backup" -type d -exec rm -rf {} + 2>/dev/null || true
		find "$target_docs/_templates" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

		echo -e "   ${GREEN}📋 Templates synced${NC}"
	fi

	echo -e "   ${GREEN}✅ $package configuration synced${NC}"
	echo ""
}

# Sync all packages
echo -e "${BLUE}📋 Found packages: ${PACKAGES[*]}${NC}"
echo ""

for package in "${PACKAGES[@]}"; do
	sync_package "$package"
done

echo -e "${GREEN}🎉 Documentation configuration sync complete!${NC}"
echo ""
echo -e "${BLUE}📝 Summary:${NC}"
echo -e "   • Source: $SOURCE_PACKAGE"
echo -e "   • Synced: conf.py + _static files + _templates"
echo -e "   • Updated: project names and GitHub URLs"
echo -e "   • Cleaned: unused CSS files and build artifacts"
echo ""
echo -e "${YELLOW}💡 Next steps:${NC}"
echo -e "   • Review changes in each package"
echo -e "   • Test documentation builds"
echo -e "   • Commit changes if satisfied"
