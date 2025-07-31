#!/bin/bash
# Safe validator inspector application script

set -e # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Safe Validator Inspector Application${NC}"
echo "====================================="

# Function to create safety branch
create_safety_branch() {
	local package=$1
	local branch_name="validator-safety-$(date +%Y%m%d-%H%M%S)"

	echo -e "${YELLOW}Creating safety branch for ${package}...${NC}"
	cd ../packages/"${package}"

	# Check for uncommitted changes
	if [[ -n $(git status --porcelain) ]]; then
		echo -e "${RED}WARNING: Uncommitted changes detected in ${package}${NC}"
		git status --short
		echo "Stashing changes..."
		git stash push -m "Pre-validator changes $(date)"
	fi

	# Create branch
	git checkout -b "${branch_name}"
	echo -e "${GREEN}Safety branch created: ${branch_name}${NC}"

	# Return branch name
	echo "${branch_name}"
}

# Function to preview changes
preview_changes() {
	local package=$1
	echo -e "${YELLOW}Previewing changes for ${package}...${NC}"

	cd /home/will/Projects/haive/backend/haive/scripts
	poetry run python -m validator_inspector_cli ../packages/"${package}" --preview >../validator_preview_"${package}".txt 2>&1

	echo "Preview saved to validator_preview_${package}.txt"
}

# Function to apply changes
apply_changes() {
	local package=$1
	local branch=$2

	echo -e "${YELLOW}Applying validator changes to ${package}...${NC}"

	cd /home/will/Projects/haive/backend/haive/scripts
	poetry run python -m validator_inspector_cli ../packages/"${package}" --apply

	# Check what changed
	cd ../packages/"${package}"
	if [[ -n $(git status --porcelain) ]]; then
		echo -e "${GREEN}Changes applied:${NC}"
		git status --short
		git diff --stat

		# Commit changes
		git add -A
		git commit -m "Apply validator inspector fixes

Safety branch: ${branch}
Applied using validator_inspector_cli
Changes can be reverted by switching back to previous branch"

		echo -e "${GREEN}Changes committed${NC}"
	else
		echo "No changes were made by validator"
	fi
}

# Function to test after changes
test_changes() {
	local package=$1
	echo -e "${YELLOW}Running tests for ${package}...${NC}"

	cd /home/will/Projects/haive/backend/haive
	poetry run pytest packages/"${package}"/tests/ -x --tb=short || {
		echo -e "${RED}Tests failed! You may want to revert.${NC}"
		return 1
	}

	echo -e "${GREEN}Tests passed!${NC}"
}

# Function to revert changes
revert_changes() {
	local package=$1
	local original_branch=$2

	echo -e "${YELLOW}Reverting changes in ${package}...${NC}"
	cd ../packages/"${package}"

	git checkout "${original_branch}"
	echo -e "${GREEN}Reverted to ${original_branch}${NC}"
}

# Main logic
PACKAGE=${1:-haive-core}

echo "Target package: ${PACKAGE}"
echo ""

# Get current branch
cd /home/will/Projects/haive/backend/haive/packages/"${PACKAGE}"
ORIGINAL_BRANCH=$(git branch --show-current)
echo "Current branch: ${ORIGINAL_BRANCH}"

# Create safety branch
SAFETY_BRANCH=$(create_safety_branch "${PACKAGE}")

# Preview changes
preview_changes "${PACKAGE}"

echo ""
echo -e "${YELLOW}Review the preview file: validator_preview_${PACKAGE}.txt${NC}"
echo "Press ENTER to apply changes, or Ctrl+C to abort"
read

# Apply changes
apply_changes "${PACKAGE}" "${SAFETY_BRANCH}"

# Option to test
echo ""
echo "Do you want to run tests? (y/n)"
read -n 1 -r
echo
if [[ ${REPLY} =~ ^[Yy]$ ]]; then
	test_changes "${PACKAGE}" || {
		echo ""
		echo -e "${RED}Tests failed. Do you want to revert? (y/n)${NC}"
		read -n 1 -r
		echo
		if [[ ${REPLY} =~ ^[Yy]$ ]]; then
			revert_changes "${PACKAGE}" "${ORIGINAL_BRANCH}"
		fi
	}
fi

echo ""
echo -e "${GREEN}Process complete!${NC}"
echo "You are now on branch: $(git branch --show-current)"
echo "To revert all changes: git checkout ${ORIGINAL_BRANCH}"
echo "To see what changed: git diff ${ORIGINAL_BRANCH}"
