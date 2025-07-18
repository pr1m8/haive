#!/bin/bash
# Documentation Versioning Script for Haive
# This script helps version control the built documentation using Git LFS

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
DOCS_SOURCE="docs/source"
DOCS_BUILD="docs/build"
DOCS_ARCHIVE="docs/archives"
GITIGNORE_FILE=".gitignore"
GITIGNORE_BACKUP=".gitignore.backup"

echo -e "${GREEN}🚀 Haive Documentation Versioning Setup${NC}"
echo "========================================"

# Function to check if Git LFS is installed
check_git_lfs() {
	if ! command -v git-lfs &>/dev/null; then
		echo -e "${RED}❌ Git LFS is not installed!${NC}"
		echo "Please install Git LFS first:"
		echo "  - macOS: brew install git-lfs"
		echo "  - Ubuntu/Debian: apt-get install git-lfs"
		echo "  - Other: https://git-lfs.github.com/"
		exit 1
	fi
	echo -e "${GREEN}✅ Git LFS is installed${NC}"
}

# Function to initialize Git LFS
init_git_lfs() {
	echo -e "${YELLOW}📦 Initializing Git LFS...${NC}"
	git lfs install
	echo -e "${GREEN}✅ Git LFS initialized${NC}"
}

# Function to temporarily remove docs/build from .gitignore
modify_gitignore() {
	echo -e "${YELLOW}📝 Modifying .gitignore...${NC}"

	# Backup current .gitignore
	cp "${GITIGNORE_FILE}" "${GITIGNORE_BACKUP}"

	# Remove docs/build/ from .gitignore
	sed -i.tmp '/^docs\/build\/$/d' "${GITIGNORE_FILE}"
	rm -f "${GITIGNORE_FILE}.tmp"

	echo -e "${GREEN}✅ Temporarily removed docs/build/ from .gitignore${NC}"
}

# Function to restore .gitignore
restore_gitignore() {
	if [[ -f "${GITIGNORE_BACKUP}" ]]; then
		echo -e "${YELLOW}🔄 Restoring .gitignore...${NC}"
		mv "${GITIGNORE_BACKUP}" "${GITIGNORE_FILE}"
		echo -e "${GREEN}✅ .gitignore restored${NC}"
	fi
}

# Function to build documentation
build_docs() {
	echo -e "${YELLOW}🔨 Building documentation...${NC}"
	nox -s docs
	echo -e "${GREEN}✅ Documentation built successfully${NC}"
}

# Function to create version tag
create_version_tag() {
	local version_tag="docs-v$(date +%Y%m%d-%H%M%S)"
	echo -e "${YELLOW}🏷️  Creating version tag: ${version_tag}${NC}"

	# Create archive directory if it doesn't exist
	mkdir -p "${DOCS_ARCHIVE}"

	# Archive current build
	if [[ -d "${DOCS_BUILD}" ]]; then
		tar -czf "${DOCS_ARCHIVE}/${version_tag}.tar.gz" -C "${DOCS_BUILD}" .
		echo -e "${GREEN}✅ Documentation archived t${ $DOCS_ARCHI}VE/${version_tag}.tar.gz${NC}"
	fi

	echo "${version_tag}"
}

# Function to track documentation with Git LFS
track_docs_with_lfs() {
	echo -e "${YELLOW}📂 Tracking documentation with Git LFS...${NC}"

	# Add built documentation to Git LFS tracking
	git add -f docs/build/
	git add .gitattributes

	echo -e "${GREEN}✅ Documentation added to Git LFS tracking${NC}"
}

# Function to commit documentation
commit_docs() {
	local version_tag=$1
	echo -e "${YELLOW}💾 Committing documentation...${NC}"

	git commit -m "docs: Add built documentation ${version_tag}

- Built documentation tracked with Git LFS
- Version: ${version_tag}
- Generated on: $(date)"

	echo -e "${GREEN}✅ Documentation committed${NC}"
}

# Main execution
main() {
	echo "This script will:"
	echo "1. Check Git LFS installation"
	echo "2. Build the documentation"
	echo "3. Temporarily modify .gitignore"
	echo "4. Add built docs to Git LFS"
	echo "5. Create a versioned commit"
	echo ""
	read -p "Continue? (y/n) " -n 1 -r
	echo ""

	if [[ ! ${REPLY} =~ ^[Yy]$ ]]; then
		echo "Aborted."
		exit 0
	fi

	# Run setup steps
	check_git_lfs
	init_git_lfs
	build_docs

	# Create version tag
	VERSION_TAG=$(create_version_tag)

	# Modify gitignore and track docs
	modify_gitignore
	track_docs_with_lfs

	# Commit changes
	commit_docs "${VERSION_TAG}"

	# Restore gitignore
	restore_gitignore

	echo ""
	echo -e "${GREEN}🎉 Documentation versioning complete!${NC}"
	echo -e "Version tag: ${YELLOW}${VERSION_TAG}${NC}"
	echo ""
	echo "Next steps:"
	echo "1. Push to remote: git push origin $(git branch --show-current)"
	echo "2. Push LFS objects: git lfs push --all origin"
	echo ""
	echo "To serve versioned docs locally:"
	echo "  python -m http.server 8003 --directory docs/build/html/"
}

# Handle cleanup on exit
trap restore_gitignore EXIT

# Run main function
main
