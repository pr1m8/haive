#!/bin/bash
# complete_git_backup.sh - Comprehensive Git repository backup script
# Save this in scripts/migration/

# Exit on any error, but not for submodule operations
set -e

# Configuration - adjust these paths
HAIVE_REPO_PATH="$(pwd)" # Assuming you run this from the haive directory
PARENT_DIR="$(dirname "${HAIVE_REPO_PATH}")"
BACKUP_ROOT="${PARENT_DIR}/haive_backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="${BACKUP_ROOT}/${TIMESTAMP}"

# Create backup directories
mkdir -p "${BACKUP_DIR}"
mkdir -p "${BACKUP_DIR}/git_bundles"
mkdir -p "${BACKUP_DIR}/working_files"
mkdir -p "${BACKUP_DIR}/submodules"
mkdir -p "${BACKUP_DIR}/history_mapping"

echo "====================================================="
echo "Creating comprehensive backup of haive repository"
echo "Backup location: ${BACKUP_DIR}"
echo "====================================================="

# Common exclusion pattern for rsync
EXCLUDE_PATTERN="--exclude=__pycache__/ --exclude=*.pyc --exclude=*.pyo --exclude=*.pyd --exclude=.pytest_cache/ --exclude=.coverage --exclude=htmlcov/ --exclude=.tox/ --exclude=.nox/ --exclude=.hypothesis/ --exclude=.mypy_cache/ --exclude=.venv/ --exclude=venv/ --exclude=*.egg-info/ --exclude=*.egg/ --exclude=*.so --exclude=dist/ --exclude=build/ --exclude=.ipynb_checkpoints/ --exclude=.DS_Store"

# 1. Back up the entire working directory excluding unwanted files
echo "Backing up entire working directory..."
rsync -a "${EXCLUDE_PATTERN}" --exclude ".git/objects" "${HAIVE_REPO_PATH}/" "${BACKUP_DIR}/working_files/"

# 2. Create a Git bundle containing the complete history
echo "Creating Git bundle with complete history..."
cd "${HAIVE_REPO_PATH}"
git bundle create "${BACKUP_DIR}/git_bundles/haive_complete.bundle" --all || {
	echo "Warning: Could not create complete bundle. Attempting to create branch-specific bundles..."
	git bundle create "${BACKUP_DIR}/git_bundles/haive_main.bundle" main || echo "Warning: Failed to bundle main branch"
	for branch in $(git branch --format='%(refname:short)' | grep -v main); do
		git bundle create "${BACKUP_DIR}/git_bundles/haive_${branch}.bundle" "${branch}" || echo "Warning: Failed to bundle ${branch} branch"
	done
}

# 3. Back up submodules individually, but don't fail if one fails
echo "Backing up submodules individually..."
git submodule foreach 'echo "Backing up submodule $name"; 
  mkdir -p '"${BACKUP_DIR}/submodules/"'$name; 
  rsync -a '"${EXCLUDE_PATTERN}"' --exclude ".git/objects" . '"${BACKUP_DIR}/submodules/"'$name/ || echo "Warning: rsync failed for $name"; 
  git bundle create '"${BACKUP_DIR}/submodules/"'$name/bundle.bundle --all || echo "Warning: Failed to create bundle for $name"'

# 4. Create a complete repository mirror, but don't include submodules
echo "Creating main repository mirror backup (without submodules)..."
git clone --mirror --no-local "${HAIVE_REPO_PATH}/.git" "${BACKUP_DIR}/haive_mirror.git" || echo "Warning: Failed to create mirror"

# 5. Backup individual files from the main repository
echo "Backing up main repository files directly..."
cd "${HAIVE_REPO_PATH}"
mkdir -p "${BACKUP_DIR}/main_repo_files"
for file in $(git ls-files); do
	# Create directory structure
	mkdir -p "${BACKUP_DIR}/main_repo_files/$(dirname "${file}")"
	# Copy file
	cp --parents "${file}" "${BACKUP_DIR}/main_repo_files/" || echo "Warning: Failed to copy ${file}"
done

# 6. Create history mapping directories for main repository only
echo "Creating directory structure mappings for history migration..."
mkdir -p "${BACKUP_DIR}/history_mapping/src_to_packages"

# Map the old structure to the new structure for each component
for component in core agents games dataflow prebuilt tools; do
	# If the old structure exists, copy files directly
	if [[ -d "${HAIVE_REPO_PATH}/src/haive/${component}" ]]; then
		echo "Copying files from src/haive/${component} to history mapping directory"
		mkdir -p "${BACKUP_DIR}/history_mapping/src_to_packages/${component}"
		rsync -a "${EXCLUDE_PATTERN}" "${HAIVE_REPO_PATH}/src/haive/${component}/" "${BACKUP_DIR}/history_mapping/src_to_packages/${component}/"
	fi
done

# 7. Create a tar.gz archive of everything for easy storage
echo "Creating compressed archive of the backup..."
cd "${BACKUP_ROOT}"
tar -czf "haive_full_backup_${TIMESTAMP}.tar.gz" "${TIMESTAMP}" || echo "Warning: Failed to create archive"

echo "====================================================="
echo "Backup completed with possible warnings! Check output above."
echo "====================================================="
echo "Backup location: ${BACKUP_DIR}"
echo "Compressed archive: ${BACKUP_ROOT}/haive_full_backup_${TIMESTAMP}.tar.gz"
echo ""
echo "To fix the corrupted submodule, you may need to:"
echo "1. Remove the problematic submodule: git submodule deinit packages/haive-agents"
echo "2. Remove it from .git/config: git rm --cached packages/haive-agents"
echo "3. Clone it fresh: git submodule add <url> packages/haive-agents"
echo "====================================================="

# Create a "latest" symlink to the most recent backup
ln -sf "${TIMESTAMP}" "${BACKUP_ROOT}/latest"
