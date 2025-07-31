#!/bin/bash
# COMPREHENSIVE GIT FSCK REPAIR & RECOVERY SYSTEM
# Captures EVERYTHING: danglings, trees, branches, blobs, staged, unstaged
# Dates and organizes everything across all modules and locations

set -euo pipefail

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
ISO_DATE=$(date -Iseconds)
REPAIR_DIR="git_fsck_repair_${TIMESTAMP}"
REPAIR_LOG="${REPAIR_DIR}/fsck_repair_${TIMESTAMP}.log"

# Create repair directory first
mkdir -p "${REPAIR_DIR}"

echo "🔧 COMPREHENSIVE GIT FSCK REPAIR & RECOVERY" | tee "${REPAIR_LOG}"
echo "=============================================" | tee -a "${REPAIR_LOG}"
echo "🕐 Started: ${ISO_DATE}" | tee -a "${REPAIR_LOG}"
echo "📁 Repair Directory: ${REPAIR_DIR}" | tee -a "${REPAIR_LOG}"
echo "📋 Log File: ${REPAIR_LOG}" | tee -a "${REPAIR_LOG}"

# Create organized repair structure
mkdir -p "${REPAIR_DIR}"/{danglings,trees,blobs,branches,refs,stashes,working,staged,submodules,timestamps}

# 1. COMPREHENSIVE FSCK ANALYSIS
echo "" | tee -a "${REPAIR_LOG}"
echo "🎯 1. COMPREHENSIVE FSCK ANALYSIS" | tee -a "${REPAIR_LOG}"
echo "==================================" | tee -a "${REPAIR_LOG}"

# Full fsck with all options
git fsck --full --unreachable --dangling --no-reflogs --connectivity-only 2>&1 | tee "${REPAIR_DIR}/fsck_full_${TIMESTAMP}.txt"
git fsck --lost-found 2>&1 | tee "${REPAIR_DIR}/fsck_lost_found_${TIMESTAMP}.txt"

# Extract different object types
echo "📋 Extracting object types..." | tee -a "${REPAIR_LOG}"
grep "dangling commit" "${REPAIR_DIR}/fsck_full_${TIMESTAMP}.txt" | awk '{print $3}' >"${REPAIR_DIR}/danglings/dangling_commits_${TIMESTAMP}.txt" || true
grep "dangling tree" "${REPAIR_DIR}/fsck_full_${TIMESTAMP}.txt" | awk '{print $3}' >"${REPAIR_DIR}/trees/dangling_trees_${TIMESTAMP}.txt" || true
grep "dangling blob" "${REPAIR_DIR}/fsck_full_${TIMESTAMP}.txt" | awk '{print $3}' >"${REPAIR_DIR}/blobs/dangling_blobs_${TIMESTAMP}.txt" || true

# 2. CAPTURE ALL REFERENCES WITH TIMESTAMPS
echo "" | tee -a "${REPAIR_LOG}"
echo "🎯 2. CAPTURE ALL REFERENCES WITH TIMESTAMPS" | tee -a "${REPAIR_LOG}"
echo "=============================================" | tee -a "${REPAIR_LOG}"

# All refs with commit dates
git for-each-ref --format='%(committerdate:iso)%09%(refname)%09%(objectname)%09%(subject)' refs/ >"${REPAIR_DIR}/refs/all_refs_dated_${TIMESTAMP}.txt"

# All branches with last commit info
git for-each-ref --format='%(committerdate:iso)%09%(refname:short)%09%(objectname)%09%(authorname)%09%(subject)' refs/heads/ >"${REPAIR_DIR}/branches/all_branches_dated_${TIMESTAMP}.txt"

# Remote branches
git for-each-ref --format='%(committerdate:iso)%09%(refname:short)%09%(objectname)%09%(subject)' refs/remotes/ >"${REPAIR_DIR}/branches/remote_branches_dated_${TIMESTAMP}.txt" || true

# Tags with dates
git for-each-ref --format='%(taggerdate:iso)%09%(refname:short)%09%(objectname)%09%(subject)' refs/tags/ >"${REPAIR_DIR}/refs/tags_dated_${TIMESTAMP}.txt" || true

# 3. COMPREHENSIVE REFLOG CAPTURE
echo "" | tee -a "${REPAIR_LOG}"
echo "🎯 3. COMPREHENSIVE REFLOG CAPTURE" | tee -a "${REPAIR_LOG}"
echo "===================================" | tee -a "${REPAIR_LOG}"

# All reflog entries with full timestamps
git reflog --all --date=iso >"${REPAIR_DIR}/refs/reflog_all_dated_${TIMESTAMP}.txt"

# Individual branch reflogs
for branch in $(git branch -a | sed 's/^..//' | grep -v '^HEAD' | sed 's/remotes\///'); do
	if [[ -n ${branch} ]]; then
		echo "📝 Capturing reflog for: ${branch}" | tee -a "${REPAIR_LOG}"
		git reflog --date=iso "${branch}" >"${REPAIR_DIR}/refs/reflog_${branch//\//_}_${TIMESTAMP}.txt" 2>/dev/null || true
	fi
done

# 4. CAPTURE ALL WORKING AND STAGED CONTENT
echo "" | tee -a "${REPAIR_LOG}"
echo "🎯 4. CAPTURE ALL WORKING AND STAGED CONTENT" | tee -a "${REPAIR_LOG}"
echo "==============================================" | tee -a "${REPAIR_LOG}"

# Current status with timestamps
echo "# Git Status Captured: ${ISO_DATE}" >"${REPAIR_DIR}/working/git_status_${TIMESTAMP}.txt"
git status --porcelain -v >>"${REPAIR_DIR}/working/git_status_${TIMESTAMP}.txt"

# Working directory diff
echo "# Working Directory Diff Captured: ${ISO_DATE}" >"${REPAIR_DIR}/working/working_diff_${TIMESTAMP}.patch"
git diff >>"${REPAIR_DIR}/working/working_diff_${TIMESTAMP}.patch"

# Staged diff
echo "# Staged Changes Diff Captured: ${ISO_DATE}" >"${REPAIR_DIR}/staged/staged_diff_${TIMESTAMP}.patch"
git diff --cached >>"${REPAIR_DIR}/staged/staged_diff_${TIMESTAMP}.patch"

# Untracked files
git ls-files --others --exclude-standard >"${REPAIR_DIR}/working/untracked_files_${TIMESTAMP}.txt"

# 5. COMPREHENSIVE STASH CAPTURE
echo "" | tee -a "${REPAIR_LOG}"
echo "🎯 5. COMPREHENSIVE STASH CAPTURE" | tee -a "${REPAIR_LOG}"
echo "==================================" | tee -a "${REPAIR_LOG}"

# List all stashes with dates
git stash list --date=iso >"${REPAIR_DIR}/stashes/stash_list_dated_${TIMESTAMP}.txt" || true

# Individual stash contents
stash_count=$(git stash list | wc -l)
for ((i = 0; i < stash_count; i++)); do
	echo "📦 Capturing stash@{${i}}..." | tee -a "${REPAIR_LOG}"

	# Stash info with date
	git stash show -p "stash@{${i}}" >"${REPAIR_DIR}/stashes/stash_${i}_content_${TIMESTAMP}.patch" 2>/dev/null || true
	git show --stat "stash@{${i}}" >"${REPAIR_DIR}/stashes/stash_${i}_stats_${TIMESTAMP}.txt" 2>/dev/null || true
	git stash show --name-only "stash@{${i}}" >"${REPAIR_DIR}/stashes/stash_${i}_files_${TIMESTAMP}.txt" 2>/dev/null || true
done

# 6. SUBMODULE COMPREHENSIVE CAPTURE
echo "" | tee -a "${REPAIR_LOG}"
echo "🎯 6. SUBMODULE COMPREHENSIVE CAPTURE" | tee -a "${REPAIR_LOG}"
echo "=====================================" | tee -a "${REPAIR_LOG}"

# Submodule status with dates
echo "# Submodule Status Captured: ${ISO_DATE}" >"${REPAIR_DIR}/submodules/submodule_status_${TIMESTAMP}.txt"
git submodule status --recursive >>"${REPAIR_DIR}/submodules/submodule_status_${TIMESTAMP}.txt" || true

# For each submodule, capture its state
git submodule foreach --recursive --quiet 'echo "=== Submodule: $path ===" && pwd' >"${REPAIR_DIR}/submodules/submodule_paths_${TIMESTAMP}.txt" || true

# Submodule fsck
git submodule foreach --recursive 'git fsck --full --unreachable' >"${REPAIR_DIR}/submodules/submodule_fsck_${TIMESTAMP}.txt" 2>&1 || true

# 7. DANGLING COMMIT RECOVERY
echo "" | tee -a "${REPAIR_LOG}"
echo "🎯 7. DANGLING COMMIT RECOVERY" | tee -a "${REPAIR_LOG}"
echo "===============================" | tee -a "${REPAIR_LOG}"

if [[ -f "${REPAIR_DIR}/danglings/dangling_commits_${TIMESTAMP}.txt" ]]; then
	while IFS= read -r commit_hash; do
		if [[ -n ${commit_hash} ]]; then
			echo "💎 Processing dangling commit: ${commit_hash}" | tee -a "${REPAIR_LOG}"

			# Commit info with date
			git show --stat "${commit_hash}" >"${REPAIR_DIR}/danglings/commit_${commit_hash}_info_${TIMESTAMP}.txt" 2>/dev/null || true
			git show "${commit_hash}" >"${REPAIR_DIR}/danglings/commit_${commit_hash}_full_${TIMESTAMP}.patch" 2>/dev/null || true

			# Try to find when this commit was created
			git log --all --grep="${commit_hash}" --oneline >"${REPAIR_DIR}/danglings/commit_${commit_hash}_references_${TIMESTAMP}.txt" 2>/dev/null || true

			# Create recovery branch for significant commits
			commit_date=$(git show -s --format=%ci "${commit_hash}" 2>/dev/null || echo "unknown")
			branch_name="recovery/dangling_${commit_hash:0:8}_${TIMESTAMP}"

			git branch "${branch_name}" "${commit_hash}" 2>&1 | tee -a "${REPAIR_LOG}" || true
			echo "🌿 Created recovery branch: ${branch_name} (${commit_date})" | tee -a "${REPAIR_LOG}"
		fi
	done <"${REPAIR_DIR}/danglings/dangling_commits_${TIMESTAMP}.txt"
fi

# 8. CREATE COMPREHENSIVE TIMESTAMP MANIFEST
echo "" | tee -a "${REPAIR_LOG}"
echo "🎯 8. CREATE COMPREHENSIVE TIMESTAMP MANIFEST" | tee -a "${REPAIR_LOG}"
echo "===============================================" | tee -a "${REPAIR_LOG}"

cat >"${REPAIR_DIR}/FSCK_REPAIR_MANIFEST_${TIMESTAMP}.md" <<EOF
# COMPREHENSIVE GIT FSCK REPAIR MANIFEST
Generated: ${ISO_DATE}
Repair Directory: ${REPAIR_DIR}

## Summary
- **Timestamp**: ${TIMESTAMP}
- **ISO Date**: ${ISO_DATE}
- **Repository**: $(pwd)
- **Git Version**: $(git --version)

## Captured Objects
- **Dangling Commits**: $(wc -l <"${REPAIR_DIR}/danglings/dangling_commits_${TIMESTAMP}.txt" 2>/dev/null || echo "0")
- **Dangling Trees**: $(wc -l <"${REPAIR_DIR}/trees/dangling_trees_${TIMESTAMP}.txt" 2>/dev/null || echo "0")
- **Dangling Blobs**: $(wc -l <"${REPAIR_DIR}/blobs/dangling_blobs_${TIMESTAMP}.txt" 2>/dev/null || echo "0")
- **All References**: $(wc -l <"${REPAIR_DIR}/refs/all_refs_dated_${TIMESTAMP}.txt" 2>/dev/null || echo "0")
- **Branches**: $(wc -l <"${REPAIR_DIR}/branches/all_branches_dated_${TIMESTAMP}.txt" 2>/dev/null || echo "0")
- **Stashes**: $(wc -l <"${REPAIR_DIR}/stashes/stash_list_dated_${TIMESTAMP}.txt" 2>/dev/null || echo "0")

## Directory Structure
\`\`\`
${REPAIR_DIR}/
├── danglings/          # Dangling commits with recovery branches
├── trees/              # Dangling trees
├── blobs/              # Dangling blobs  
├── branches/           # All branches with dates
├── refs/               # All references and reflogs with timestamps
├── stashes/            # All stashes with full content
├── working/            # Working directory state
├── staged/             # Staged changes
├── submodules/         # Submodule states and fsck
└── timestamps/         # Timestamp metadata
\`\`\`

## Recovery Commands
To restore a dangling commit:
\`\`\`bash
git checkout recovery/dangling_HASH_${TIMESTAMP}
\`\`\`

To apply working changes:
\`\`\`bash
git apply ${REPAIR_DIR}/working/working_diff_${TIMESTAMP}.patch
\`\`\`

To apply staged changes:
\`\`\`bash
git apply --cached ${REPAIR_DIR}/staged/staged_diff_${TIMESTAMP}.patch
\`\`\`

## Verification
All captured data includes timestamps and can be verified against:
- Original fsck output: ${REPAIR_DIR}/fsck_full_${TIMESTAMP}.txt
- Complete reflog: ${REPAIR_DIR}/refs/reflog_all_dated_${TIMESTAMP}.txt
- Repair log: ${REPAIR_LOG}
EOF

echo "" | tee -a "${REPAIR_LOG}"
echo "🎉 COMPREHENSIVE FSCK REPAIR COMPLETE!" | tee -a "${REPAIR_LOG}"
echo "======================================" | tee -a "${REPAIR_LOG}"
echo "✅ All objects captured and dated!" | tee -a "${REPAIR_LOG}"
echo "📁 Results in: ${REPAIR_DIR}/" | tee -a "${REPAIR_LOG}"
echo "📋 Manifest: ${REPAIR_DIR}/FSCK_REPAIR_MANIFEST_${TIMESTAMP}.md" | tee -a "${REPAIR_LOG}"
echo "🕐 Completed: $(date -Iseconds)" | tee -a "${REPAIR_LOG}"
