# COMPREHENSIVE GIT FSCK REPAIR MANIFEST
Generated: 2025-07-29T21:30:07-04:00
Repair Directory: git_fsck_repair_20250729_213007

## Summary
- **Timestamp**: 20250729_213007
- **ISO Date**: 2025-07-29T21:30:07-04:00
- **Repository**: /home/will/Projects/haive/backend/haive
- **Git Version**: git version 2.43.0

## Captured Objects
- **Dangling Commits**: 0
- **Dangling Trees**: 0
- **Dangling Blobs**: 0
- **All References**: 297
- **Branches**: 44
- **Stashes**: 31

## Directory Structure
```
git_fsck_repair_20250729_213007/
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
```

## Recovery Commands
To restore a dangling commit:
```bash
git checkout recovery/dangling_HASH_20250729_213007
```

To apply working changes:
```bash
git apply git_fsck_repair_20250729_213007/working/working_diff_20250729_213007.patch
```

To apply staged changes:
```bash
git apply --cached git_fsck_repair_20250729_213007/staged/staged_diff_20250729_213007.patch
```

## Verification
All captured data includes timestamps and can be verified against:
- Original fsck output: git_fsck_repair_20250729_213007/fsck_full_20250729_213007.txt
- Complete reflog: git_fsck_repair_20250729_213007/refs/reflog_all_dated_20250729_213007.txt
- Repair log: git_fsck_repair_20250729_213007/fsck_repair_20250729_213007.log
