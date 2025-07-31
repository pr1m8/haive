#!/bin/bash
# UNIVERSAL PRE-COMMIT CAPTURE SYSTEM
# Captures EVERYTHING across all modules, branches, staged, unstaged, etc.

set -euo pipefail

# Comprehensive timestamp system
CAPTURE_DATE=$(date +%Y-%m-%d)
CAPTURE_TIME=$(date +%H-%M-%S)
CAPTURE_TIMESTAMP=$(date +%Y%m%d_%H%M%S)
CAPTURE_ISO=$(date -Iseconds)
CAPTURE_EPOCH=$(date +%s)

# Create comprehensive capture directory with full dating
CAPTURE_BASE="universal_capture/${CAPTURE_DATE}/${CAPTURE_TIME}"
mkdir -p "${CAPTURE_BASE}"

# Logging with timestamps
CAPTURE_LOG="${CAPTURE_BASE}/capture_log_${CAPTURE_TIMESTAMP}.txt"

log_with_timestamp() {
    echo "[$(date -Iseconds)] $*" | tee -a "${CAPTURE_LOG}"
}

log_with_timestamp "🔄 UNIVERSAL PRE-COMMIT CAPTURE SYSTEM"
log_with_timestamp "============================================="
log_with_timestamp "Capture Date: ${CAPTURE_DATE}"
log_with_timestamp "Capture Time: ${CAPTURE_TIME}"
log_with_timestamp "ISO Timestamp: ${CAPTURE_ISO}"
log_with_timestamp "Epoch: ${CAPTURE_EPOCH}"
log_with_timestamp "Base Directory: ${CAPTURE_BASE}"

# 1. CAPTURE ALL GIT STATE ACROSS ALL BRANCHES
log_with_timestamp ""
log_with_timestamp "🎯 1. CAPTURING ALL GIT STATE"
log_with_timestamp "==============================="

mkdir -p "${CAPTURE_BASE}/git_state"

# Current state snapshot
log_with_timestamp "📸 Capturing current git state..."
git status --porcelain > "${CAPTURE_BASE}/git_state/status_${CAPTURE_TIMESTAMP}.txt"
git branch -a > "${CAPTURE_BASE}/git_state/all_branches_${CAPTURE_TIMESTAMP}.txt"
git tag > "${CAPTURE_BASE}/git_state/all_tags_${CAPTURE_TIMESTAMP}.txt"
git stash list > "${CAPTURE_BASE}/git_state/stash_list_${CAPTURE_TIMESTAMP}.txt"
git reflog --all --date=iso > "${CAPTURE_BASE}/git_state/reflog_${CAPTURE_TIMESTAMP}.txt"

# Current commit info with full details
git log --oneline -20 > "${CAPTURE_BASE}/git_state/recent_commits_${CAPTURE_TIMESTAMP}.txt"
git show --stat HEAD > "${CAPTURE_BASE}/git_state/current_commit_${CAPTURE_TIMESTAMP}.txt"

# 2. CAPTURE ALL STAGED WORK
log_with_timestamp ""
log_with_timestamp "🎯 2. CAPTURING ALL STAGED WORK"
log_with_timestamp "================================"

mkdir -p "${CAPTURE_BASE}/staged"

if git diff --cached --quiet; then
    log_with_timestamp "ℹ️  No staged changes found"
    echo "No staged changes at ${CAPTURE_ISO}" > "${CAPTURE_BASE}/staged/no_staged_changes_${CAPTURE_TIMESTAMP}.txt"
else
    log_with_timestamp "📦 Capturing staged changes..."
    git diff --cached > "${CAPTURE_BASE}/staged/staged_diff_${CAPTURE_TIMESTAMP}.patch"
    git diff --cached --name-only > "${CAPTURE_BASE}/staged/staged_files_${CAPTURE_TIMESTAMP}.txt"
    git diff --cached --stat > "${CAPTURE_BASE}/staged/staged_stats_${CAPTURE_TIMESTAMP}.txt"
fi

# 3. CAPTURE ALL UNSTAGED WORK
log_with_timestamp ""
log_with_timestamp "🎯 3. CAPTURING ALL UNSTAGED WORK"
log_with_timestamp "=================================="

mkdir -p "${CAPTURE_BASE}/unstaged"

if git diff --quiet; then
    log_with_timestamp "ℹ️  No unstaged changes found"
    echo "No unstaged changes at ${CAPTURE_ISO}" > "${CAPTURE_BASE}/unstaged/no_unstaged_changes_${CAPTURE_TIMESTAMP}.txt"
else
    log_with_timestamp "🔧 Capturing unstaged changes..."
    git diff > "${CAPTURE_BASE}/unstaged/unstaged_diff_${CAPTURE_TIMESTAMP}.patch"
    git diff --name-only > "${CAPTURE_BASE}/unstaged/unstaged_files_${CAPTURE_TIMESTAMP}.txt"
    git diff --stat > "${CAPTURE_BASE}/unstaged/unstaged_stats_${CAPTURE_TIMESTAMP}.txt"
fi

# 4. CAPTURE ALL UNTRACKED FILES
log_with_timestamp ""
log_with_timestamp "🎯 4. CAPTURING ALL UNTRACKED FILES"
log_with_timestamp "==================================="

mkdir -p "${CAPTURE_BASE}/untracked"

untracked_files=$(git ls-files --others --exclude-standard)
if [[ -z "${untracked_files}" ]]; then
    log_with_timestamp "ℹ️  No untracked files found"
    echo "No untracked files at ${CAPTURE_ISO}" > "${CAPTURE_BASE}/untracked/no_untracked_files_${CAPTURE_TIMESTAMP}.txt"
else
    log_with_timestamp "📁 Capturing untracked files..."
    git ls-files --others --exclude-standard > "${CAPTURE_BASE}/untracked/untracked_list_${CAPTURE_TIMESTAMP}.txt"
    
    # Create dated archive of all untracked files
    tar -czf "${CAPTURE_BASE}/untracked/untracked_archive_${CAPTURE_TIMESTAMP}.tar.gz" \
        --files-from="${CAPTURE_BASE}/untracked/untracked_list_${CAPTURE_TIMESTAMP}.txt" 2>/dev/null || true
    
    # Copy untracked files preserving structure
    mkdir -p "${CAPTURE_BASE}/untracked/files"
    while IFS= read -r file; do
        if [[ -f "${file}" ]]; then
            target_dir="${CAPTURE_BASE}/untracked/files/$(dirname "${file}")"
            mkdir -p "${target_dir}"
            cp "${file}" "${target_dir}/" 2>/dev/null || true
        fi
    done < "${CAPTURE_BASE}/untracked/untracked_list_${CAPTURE_TIMESTAMP}.txt"
fi

# 5. CAPTURE ALL SUBMODULE STATES
log_with_timestamp ""
log_with_timestamp "🎯 5. CAPTURING ALL SUBMODULE STATES"
log_with_timestamp "====================================="

mkdir -p "${CAPTURE_BASE}/submodules"

if [[ -f .gitmodules ]]; then
    log_with_timestamp "📦 Capturing submodule states..."
    git submodule status > "${CAPTURE_BASE}/submodules/submodule_status_${CAPTURE_TIMESTAMP}.txt"
    git submodule foreach 'echo "=== $name ===" && git status --porcelain' > "${CAPTURE_BASE}/submodules/submodule_changes_${CAPTURE_TIMESTAMP}.txt"
    git submodule foreach 'echo "=== $name ===" && git branch -a' > "${CAPTURE_BASE}/submodules/submodule_branches_${CAPTURE_TIMESTAMP}.txt"
    cp .gitmodules "${CAPTURE_BASE}/submodules/gitmodules_${CAPTURE_TIMESTAMP}.txt"
    
    # Capture each submodule's individual state
    git submodule foreach --quiet 'mkdir -p "'"${CAPTURE_BASE}"'/submodules/$name" && git status --porcelain > "'"${CAPTURE_BASE}"'/submodules/$name/status_'"${CAPTURE_TIMESTAMP}"'.txt" && git log --oneline -10 > "'"${CAPTURE_BASE}"'/submodules/$name/recent_commits_'"${CAPTURE_TIMESTAMP}"'.txt"'
else
    log_with_timestamp "ℹ️  No submodules found"
    echo "No submodules at ${CAPTURE_ISO}" > "${CAPTURE_BASE}/submodules/no_submodules_${CAPTURE_TIMESTAMP}.txt"
fi

# 6. CAPTURE ALL STASHES
log_with_timestamp ""
log_with_timestamp "🎯 6. CAPTURING ALL STASHES"
log_with_timestamp "==========================="

mkdir -p "${CAPTURE_BASE}/stashes"

stash_count=$(git stash list | wc -l)
if [[ ${stash_count} -eq 0 ]]; then
    log_with_timestamp "ℹ️  No stashes found"
    echo "No stashes at ${CAPTURE_ISO}" > "${CAPTURE_BASE}/stashes/no_stashes_${CAPTURE_TIMESTAMP}.txt"
else
    log_with_timestamp "📚 Capturing ${stash_count} stashes..."
    git stash list > "${CAPTURE_BASE}/stashes/stash_list_${CAPTURE_TIMESTAMP}.txt"
    
    # Capture each stash individually
    for i in $(seq 0 $((stash_count - 1))); do
        if git stash show stash@{${i}} >/dev/null 2>&1; then
            git stash show -p stash@{${i}} > "${CAPTURE_BASE}/stashes/stash_${i}_${CAPTURE_TIMESTAMP}.patch" 2>/dev/null || true
            git stash show --name-only stash@{${i}} > "${CAPTURE_BASE}/stashes/stash_${i}_files_${CAPTURE_TIMESTAMP}.txt" 2>/dev/null || true
        fi
    done
fi

# 7. CAPTURE ALL BRANCHES AND THEIR STATES
log_with_timestamp ""
log_with_timestamp "🎯 7. CAPTURING ALL BRANCH STATES"
log_with_timestamp "=================================="

mkdir -p "${CAPTURE_BASE}/branches"

current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "detached")
echo "Current branch: ${current_branch} at ${CAPTURE_ISO}" > "${CAPTURE_BASE}/branches/current_branch_${CAPTURE_TIMESTAMP}.txt"

# Capture state of all branches
git for-each-ref --format='%(refname:short) %(objectname) %(committerdate:iso)' refs/heads/ > "${CAPTURE_BASE}/branches/all_local_branches_${CAPTURE_TIMESTAMP}.txt"
git for-each-ref --format='%(refname:short) %(objectname) %(committerdate:iso)' refs/remotes/ > "${CAPTURE_BASE}/branches/all_remote_branches_${CAPTURE_TIMESTAMP}.txt"

# 8. CAPTURE WORKING DIRECTORY SNAPSHOT
log_with_timestamp ""
log_with_timestamp "🎯 8. CAPTURING WORKING DIRECTORY SNAPSHOT"
log_with_timestamp "==========================================="

mkdir -p "${CAPTURE_BASE}/workspace"

# File tree with timestamps
find . -type f -not -path './.git/*' -not -path './universal_capture/*' -printf '%T@ %p\n' | sort -n > "${CAPTURE_BASE}/workspace/file_tree_with_timestamps_${CAPTURE_TIMESTAMP}.txt"

# Directory structure
tree -a -I '.git|universal_capture' > "${CAPTURE_BASE}/workspace/directory_tree_${CAPTURE_TIMESTAMP}.txt" 2>/dev/null || find . -type d -not -path './.git/*' -not -path './universal_capture/*' > "${CAPTURE_BASE}/workspace/directories_${CAPTURE_TIMESTAMP}.txt"

# File counts and sizes
find . -type f -not -path './.git/*' -not -path './universal_capture/*' | wc -l > "${CAPTURE_BASE}/workspace/file_count_${CAPTURE_TIMESTAMP}.txt"
du -sh . > "${CAPTURE_BASE}/workspace/total_size_${CAPTURE_TIMESTAMP}.txt"

# 9. CREATE COMPREHENSIVE MANIFEST
log_with_timestamp ""
log_with_timestamp "🎯 9. CREATING COMPREHENSIVE MANIFEST"
log_with_timestamp "======================================"

cat > "${CAPTURE_BASE}/CAPTURE_MANIFEST_${CAPTURE_TIMESTAMP}.md" << EOF
# UNIVERSAL PRE-COMMIT CAPTURE MANIFEST

**Generated:** ${CAPTURE_ISO}
**Date:** ${CAPTURE_DATE}
**Time:** ${CAPTURE_TIME}
**Epoch:** ${CAPTURE_EPOCH}
**Directory:** ${CAPTURE_BASE}

## Capture Summary

- **Git Status:** $(git status --porcelain | wc -l) modified files
- **Staged Changes:** $(git diff --cached --name-only | wc -l) files
- **Unstaged Changes:** $(git diff --name-only | wc -l) files
- **Untracked Files:** $(git ls-files --others --exclude-standard | wc -l) files
- **Stashes:** ${stash_count} stashes
- **Current Branch:** ${current_branch}
- **Submodules:** $(test -f .gitmodules && git submodule status | wc -l || echo 0) submodules

## Directory Structure

\`\`\`
${CAPTURE_BASE}/
├── git_state/           # Git status, branches, commits, reflog
├── staged/              # All staged changes with diffs
├── unstaged/            # All unstaged changes with diffs
├── untracked/           # All untracked files (archived and copied)
├── submodules/          # Submodule states and changes
├── stashes/             # All stashes (individual patches)
├── branches/            # All branch states and commits
├── workspace/           # Working directory snapshot
└── CAPTURE_MANIFEST_${CAPTURE_TIMESTAMP}.md
\`\`\`

## Usage

This capture contains a complete snapshot of your repository state at ${CAPTURE_ISO}.
All files are timestamped with ${CAPTURE_TIMESTAMP} for precise identification.

To restore any component:
1. Check the relevant subdirectory
2. Apply patches using: \`git apply <patch_file>\`
3. Review manifests for detailed information

EOF

log_with_timestamp ""
log_with_timestamp "🎉 UNIVERSAL CAPTURE COMPLETE!"
log_with_timestamp "==============================="
log_with_timestamp "✅ Captured ALL repository state"
log_with_timestamp "✅ All files timestamped: ${CAPTURE_TIMESTAMP}"
log_with_timestamp "✅ Complete manifest created"
log_with_timestamp "📂 Capture location: ${CAPTURE_BASE}"
log_with_timestamp "📋 Manifest: ${CAPTURE_BASE}/CAPTURE_MANIFEST_${CAPTURE_TIMESTAMP}.md"
log_with_timestamp "📝 Log file: ${CAPTURE_LOG}"

# Create quick access summary
echo "Last capture: ${CAPTURE_ISO} in ${CAPTURE_BASE}" > universal_capture/LAST_CAPTURE.txt 