#!/bin/bash
# Documentation Publishing Script for Haive
# This script builds docs and publishes them to a version-controlled directory

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
DOCS_BUILD="docs/build/html"
DOCS_PUBLISHED="docs/published"
DOCS_VERSIONS="docs/versions"
CURRENT_LINK="${DOCS_PUBLISHED}/current"

echo -e "${BLUE}📚 Haive Documentation Publisher${NC}"
echo "================================="

# Function to check dependencies
check_dependencies() {
    echo -e "${YELLOW}🔍 Checking dependencies...${NC}"

    # Check Git LFS
    if ! command -v git-lfs &> /dev/null; then
        echo -e "${RED}❌ Git LFS is not installed!${NC}"
        echo "Please install Git LFS:"
        echo "  brew install git-lfs  # macOS"
        echo "  apt install git-lfs   # Ubuntu/Debian"
        exit 1
    fi

    # Check if Git LFS is initialized
    if ! git lfs env &> /dev/null; then
        echo -e "${YELLOW}Initializing Git LFS...${NC}"
        git lfs install
    fi

    echo -e "${GREEN}✅ All dependencies satisfied${NC}"
}

# Function to build documentation
build_docs() {
    echo -e "${YELLOW}🔨 Building documentation...${NC}"

    # Run nox to build docs
    if nox -s docs; then
        echo -e "${GREEN}✅ Documentation built successfully${NC}"
    else
        echo -e "${RED}❌ Documentation build failed${NC}"
        exit 1
    fi
}

# Function to create version identifier
get_version() {
    # Try to get version from git tag or commit
    local git_tag=$(git describe --tags --exact-match 2>/dev/null || echo "")
    local git_commit=$(git rev-parse --short HEAD)
    local timestamp=$(date +%Y%m%d-%H%M%S)

    if [[ -n "${git_tag}" ]]; then
        echo "${git_tag}"
    else
        echo "dev-${git_commit}-${timestamp}"
    fi
}

# Function to publish documentation
publish_docs() {
    local version=$1
    echo -e "${YELLOW}📤 Publishing documentation version: ${version}${NC}"

    # Create directories
    mkdir -p "${DOCS_PUBLISHED}"
    mkdir -p "${DOCS_VERSIONS}"

    # Copy built docs to versioned directory
    local version_dir="${DOCS_VERSIONS}/${version}"
    echo -e "${BLUE}Copying to ${version_dir}...${NC}"

    rm -rf "${version_dir}"
    cp -r "${DOCS_BUILD}" "${version_dir}"

    # Update current symlink
    rm -f "${CURRENT_LINK}"
    ln -s "../versions/${version}" "${CURRENT_LINK}"

    # Create a README for the published directory
    cat > "${DOCS_PUBLISHED}/README.md" << EOF
# Published Documentation

This directory contains version-controlled documentation builds.

## Current Version
The \`current\` symlink points to the latest published version.

## Versions
All versions are stored in the \`versions/\` directory.

### Viewing Documentation
To view the current documentation locally:
\`\`\`bash
python -m http.server 8003 --directory docs/published/current/
\`\`\`

### Version History
- **${version}** - Published on $(date)
EOF

    echo -e "${GREEN}✅ Documentation published t${ $version_d}ir${NC}"
}

# Function to stage files for Git LFS
stage_for_lfs() {
    local version=$1
    echo -e "${YELLOW}📦 Staging documentation for Git LFS...${NC}"

    # Add the published docs to git
    git add -f "${DOCS_PUBLISHED}/README.md"
    git add -f "${DOCS_VERSIONS}/${version}"
    git add -f "${CURRENT_LINK}"
    git add .gitattributes

    echo -e "${GREEN}✅ Files staged for commit${NC}"
}

# Function to create commit
create_commit() {
    local version=$1
    echo -e "${YELLOW}💾 Creating commit...${NC}"

    local commit_msg="docs: Publish documentation ${version}

- Built and published documentation
- Version: ${version}
- Date: $(date)
- Files tracked with Git LFS"

    git commit -m "${commit_msg}" || {
        echo -e "${YELLOW}No changes to commit${NC}"
        return 0
    }

    echo -e "${GREEN}✅ Documentation committed${NC}"
}

# Function to show summary
show_summary() {
    local version=$1
    echo ""
    echo -e "${GREEN}🎉 Documentation published successfully!${NC}"
    echo ""
    echo "Version: ${YELLOW}${version}${NC}"
    echo "Location: ${BLUE}${DOCS_VERSIONS}/${version}${NC}"
    echo ""
    echo "To view locally:"
    echo -e "  ${YELLOW}python -m http.server 8003 --directory ${DOCS_PUBLISHED}/current/${NC}"
    echo ""
    echo "To push to remote:"
    echo -e "  ${YELLOW}git push origin $(git branch --show-current)${NC}"
    echo -e "  ${YELLOW}git lfs push --all origin${NC}"
}

# Main execution
main() {
    echo "This will build and publish the documentation with Git LFS."
    echo ""
    read -p "Continue? (y/n) " -n 1 -r
    echo ""

    if [[ ! ${REPLY} =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 0
    fi

    # Run steps
    check_dependencies
    build_docs

    # Get version
    VERSION=$(get_version)

    # Publish and commit
    publish_docs "${VERSION}"
    stage_for_lfs "${VERSION}"
    create_commit "${VERSION}"

    # Show summary
    show_summary "${VERSION}"
}

# Run main function
main
