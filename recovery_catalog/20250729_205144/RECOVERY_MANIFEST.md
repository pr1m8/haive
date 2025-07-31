# Comprehensive Recovery Catalog

Generated: 20250729_205144

## Contents

### Current Work (recovery_catalog/20250729_205144/current_work/)

- git_status.txt - Current git status
- working_diff.patch - Uncommitted changes
- staged_diff.patch - Staged changes
- untracked/ - All untracked files

### Stashes (recovery_catalog/20250729_205144/stashes/)

- stash_list.txt - Complete stash list
- stash_N.patch - Individual stash contents
- stash_N_files.txt - Files in each stash

### References (recovery_catalog/20250729_205144/refs/)

- all_refs.txt - All git references with timestamps
- all_branches.txt - All branches
- all_tags.txt - All tags

### Dangling Objects (recovery_catalog/20250729_205144/dangling/)

- fsck_output.txt - Complete git fsck output
- dangling_commits.txt - List of dangling commits
- commit_HASH.patch - Individual dangling commits

### Submodules (recovery_catalog/20250729_205144/submodules/)

- submodule_status.txt - Current submodule status
- MODULE*NAME*\* - Individual submodule states

### Search Index (recovery_catalog/20250729_205144/search_index/)

- docs_rich_matches.txt - All docs_rich references found
- rich_docs_matches.txt - All rich/docs combinations
- noxfiles\_\*.txt - Noxfile locations and content

## Usage

To search for docs_rich session:

```bash
grep -r "docs_rich" recovery_catalog/20250729_205144/
```

To restore a specific stash:

```bash
git apply recovery_catalog/20250729_205144/stashes/stash_N.patch
```

To view a dangling commit:

```bash
cat recovery_catalog/20250729_205144/dangling/commit_HASH.patch
```
