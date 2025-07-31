#!/bin/bash
# Comprehensive Recovery and Cataloging System
# Saves EVERYTHING across all modules, branches, stashes, dangling objects

set -euo pipefail

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RECOVERY_DIR="recovery_catalog/${TIMESTAMP}"
mkdir -p "${RECOVERY_DIR}"

echo "🔄 COMPREHENSIVE RECOVERY SYSTEM"
echo "================================="
echo "Recovery Directory: ${RECOVERY_DIR}"
echo "Timestamp: ${TIMESTAMP}"

# 1. Save current uncommitted work
echo "📦 1. Saving Current Uncommitted Work..."
mkdir -p "${RECOVERY_DIR}/current_work"
git status --porcelain >"${RECOVERY_DIR}/current_work/git_status.txt"
git diff >"${RECOVERY_DIR}/current_work/working_diff.patch" || true
git diff --staged >"${RECOVERY_DIR}/current_work/staged_diff.patch" || true

# Copy all untracked files
echo "📁 Copying untracked files..."
git ls-files --others --exclude-standard | while read -r file; do
	if [[ -f ${file} ]]; then
		mkdir -p "${RECOVERY_DIR}/current_work/untracked/$(dirname "${file}")"
		cp "${file}" "${RECOVERY_DIR}/current_work/untracked/${file}"
	fi
done

# 2. Save all stashes with metadata
echo "💾 2. Saving All Stashes..."
mkdir -p "${RECOVERY_DIR}/stashes"
git stash list --date=iso >"${RECOVERY_DIR}/stashes/stash_list.txt"

# Export each stash
stash_count=$(git stash list | wc -l)
for i in $(seq 0 $((stash_count - 1))); do
	echo "Saving stash@{${i}}..."
	git stash show -p "stash@{${i}}" >"${RECOVERY_DIR}/stashes/stash_${i}.patch" 2>/dev/null || true
	git show --name-only "stash@{${i}}" >"${RECOVERY_DIR}/stashes/stash_${i}_files.txt" 2>/dev/null || true
done

# 3. Save all branches and references
echo "🌿 3. Saving All Branches and References..."
mkdir -p "${RECOVERY_DIR}/refs"
git for-each-ref --sort=committerdate --format='%(committerdate:iso) %(refname) %(objectname) %(subject)' >"${RECOVERY_DIR}/refs/all_refs.txt"
git branch -a >"${RECOVERY_DIR}/refs/all_branches.txt"
git tag -l >"${RECOVERY_DIR}/refs/all_tags.txt"

# 4. Save dangling objects
echo "🔍 4. Cataloging Dangling Objects..."
mkdir -p "${RECOVERY_DIR}/dangling"
git fsck --full --unreachable --dangling >"${RECOVERY_DIR}/dangling/fsck_output.txt" 2>&1

# Extract dangling commits and save them
grep "unreachable commit" "${RECOVERY_DIR}/dangling/fsck_output.txt" | awk '{print $3}' >"${RECOVERY_DIR}/dangling/dangling_commits.txt" || true
grep "dangling commit" "${RECOVERY_DIR}/dangling/fsck_output.txt" | awk '{print $3}' >>"${RECOVERY_DIR}/dangling/dangling_commits.txt" || true

# Save each dangling commit
if [[ -f "${RECOVERY_DIR}/dangling/dangling_commits.txt" ]]; then
	while read -r commit; do
		if [[ -n ${commit} ]]; then
			echo "Saving dangling commit: ${commit}"
			git show --name-only "${commit}" >"${RECOVERY_DIR}/dangling/commit_${commit}_files.txt" 2>/dev/null || true
			git show "${commit}" >"${RECOVERY_DIR}/dangling/commit_${commit}.patch" 2>/dev/null || true
		fi
	done <"${RECOVERY_DIR}/dangling/dangling_commits.txt"
fi

# 5. Save submodule states
echo "📂 5. Saving Submodule States..."
mkdir -p "${RECOVERY_DIR}/submodules"
git submodule status >"${RECOVERY_DIR}/submodules/submodule_status.txt"

# For each submodule, save its state
git submodule foreach --quiet 'echo "=== $name ===" && pwd' >"${RECOVERY_DIR}/submodules/submodule_paths.txt"
git submodule foreach '
    module_name=$(basename $(pwd))
    echo "Processing submodule: $module_name"
    
    # Save current status
    git status --porcelain > "../${RECOVERY_DIR}/submodules/${module_name}_status.txt" || true
    git diff > "../${RECOVERY_DIR}/submodules/${module_name}_diff.patch" || true
    git diff --staged > "../${RECOVERY_DIR}/submodules/${module_name}_staged.patch" || true
    
    # Save recent commits
    git log --oneline -20 > "../${RECOVERY_DIR}/submodules/${module_name}_recent_commits.txt" || true
    
    # Save local branches
    git branch -a > "../${RECOVERY_DIR}/submodules/${module_name}_branches.txt" || true
' || true

# 6. Create searchable index
echo "🔍 6. Creating Searchable Index..."
mkdir -p "${RECOVERY_DIR}/search_index"

# Index all noxfile content
echo "Indexing noxfile content..."
find . -name "noxfile*.py" -exec basename {} \; >"${RECOVERY_DIR}/search_index/noxfiles_found.txt"
find . -name "noxfile*.py" -exec grep -l "docs_rich\|rich.*docs" {} \; >"${RECOVERY_DIR}/search_index/noxfiles_with_rich.txt" 2>/dev/null || true

# Search through all recovered content for docs_rich
echo "Searching for docs_rich across all content..."
grep -r "docs_rich" "${RECOVERY_DIR}/" >"${RECOVERY_DIR}/search_index/docs_rich_matches.txt" 2>/dev/null || true
grep -r "rich.*docs\|docs.*rich" "${RECOVERY_DIR}/" >"${RECOVERY_DIR}/search_index/rich_docs_matches.txt" 2>/dev/null || true

# 7. Create recovery manifest
echo "📋 7. Creating Recovery Manifest..."
cat >"${RECOVERY_DIR}/RECOVERY_MANIFEST.md" <<EOF
# Comprehensive Recovery Catalog
Generated: ${TIMESTAMP}

## Contents

### Current Work (${RECOVERY_DIR}/current_work/)
- git_status.txt - Current git status
- working_diff.patch - Uncommitted changes
- staged_diff.patch - Staged changes  
- untracked/ - All untracked files

### Stashes (${RECOVERY_DIR}/stashes/)
- stash_list.txt - Complete stash list
- stash_N.patch - Individual stash contents
- stash_N_files.txt - Files in each stash

### References (${RECOVERY_DIR}/refs/)
- all_refs.txt - All git references with timestamps
- all_branches.txt - All branches
- all_tags.txt - All tags

### Dangling Objects (${RECOVERY_DIR}/dangling/)
- fsck_output.txt - Complete git fsck output
- dangling_commits.txt - List of dangling commits
- commit_HASH.patch - Individual dangling commits

### Submodules (${RECOVERY_DIR}/submodules/)
- submodule_status.txt - Current submodule status
- MODULE_NAME_* - Individual submodule states

### Search Index (${RECOVERY_DIR}/search_index/)
- docs_rich_matches.txt - All docs_rich references found
- rich_docs_matches.txt - All rich/docs combinations
- noxfiles_*.txt - Noxfile locations and content

## Usage

To search for docs_rich session:
\`\`\`bash
grep -r "docs_rich" ${RECOVERY_DIR}/
\`\`\`

To restore a specific stash:
\`\`\`bash
git apply ${RECOVERY_DIR}/stashes/stash_N.patch
\`\`\`

To view a dangling commit:
\`\`\`bash
cat ${RECOVERY_DIR}/dangling/commit_HASH.patch
\`\`\`
EOF

echo "✅ RECOVERY COMPLETE!"
echo "📁 Everything saved to: ${RECOVERY_DIR}"
echo "📋 See ${RECOVERY_DIR}/RECOVERY_MANIFEST.md for details"
echo ""
echo "🔍 Quick search for docs_rich:"
if [[ -f "${RECOVERY_DIR}/search_index/docs_rich_matches.txt" ]]; then
	echo "Found $(wc -l <"${RECOVERY_DIR}/search_index/docs_rich_matches.txt" || echo 0) matches for docs_rich"
fi
