#!/bin/bash
# complete_git_backup.sh - Comprehensive Git repository backup script
# Save this in scripts/migration/

# Exit on any error
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
git bundle create "${BACKUP_DIR}/git_bundles/haive_complete.bundle" --all

# 3. Back up submodules individually
echo "Backing up submodules individually..."
git submodule foreach --recursive 'echo "Backing up submodule $name";
  mkdir -p '"${BACKUP_DIR}/submodules/"'$name;
  rsync -a '"${EXCLUDE_PATTERN}"' --exclude ".git/objects" . '"${BACKUP_DIR}/submodules/"'$name/;
  git bundle create '"${BACKUP_DIR}/submodules/"'$name/bundle.bundle --all'

# 4. Create a complete repository mirror
echo "Creating full Git mirror backup..."
git clone --mirror "${HAIVE_REPO_PATH}" "${BACKUP_DIR}/haive_mirror.git"

# 5. Create history mapping directories to facilitate migration
echo "Creating directory structure mappings for history migration..."
mkdir -p "${BACKUP_DIR}/history_mapping/src_to_packages"

# Map the old structure to the new structure for each component
for component in core agents games dataflow prebuilt tools; do
	# Create directory for this component
	mkdir -p "${BACKUP_DIR}/history_mapping/src_to_packages/${component}"

	# If the old structure exists, extract its history
	if [[ -d "${HAIVE_REPO_PATH}/src/haive/${component}" ]]; then
		echo "Extracting history for src/haive/${component} -> packages/haive-${component}"

		# Create a temporary directory for extraction
		mkdir -p "${BACKUP_DIR}/history_mapping/src_to_packages/${component}/extract"
		cd "${BACKUP_DIR}/history_mapping/src_to_packages/${component}/extract"

		# Clone the repository and extract just the history for this component
		git clone "${BACKUP_DIR}/haive_mirror.git" .
		git filter-repo --path "src/haive/${component}/" --path-rename "src/haive/${component}/":"src/haive_${component}/" --force

		# Create a bundle file with the extracted history
		git bundle create "../${component}-history.bundle" --all

		# Clean up extraction directory
		cd ..
		rm -rf extract
	fi
done

# 6. Create a tar.gz archive of everything for easy storage
echo "Creating compressed archive of the backup..."
cd "${BACKUP_ROOT}"
tar -czf "haive_full_backup_${TIMESTAMP}.tar.gz" "${TIMESTAMP}"

# 7. Back up one level above haive as well
echo "Creating backup one level above haive..."
cd "${PARENT_DIR}"
# Exclude large files/dirs but include other important files
tar -czf "${BACKUP_DIR}/parent_dir_backup.tar.gz" \
	--exclude="*/node_modules" \
	--exclude="*/__pycache__" \
	--exclude="*.pyc" \
	--exclude="*.pyo" \
	--exclude="*.pyd" \
	--exclude="*/.pytest_cache" \
	--exclude="*/.git/objects" \
	--exclude="*/venv" \
	--exclude="*/.venv" \
	--exclude="*/.ipynb_checkpoints" \
	--exclude="*/dist" \
	--exclude="*/build" \
	--exclude="*.egg-info" \
	--exclude="*.egg" \
	--exclude="*.so" \
	.

echo "====================================================="
echo "Backup completed successfully!"
echo "====================================================="
echo "Full backup: ${BACKUP_DIR}"
echo "Compressed archive: ${BACKUP_ROOT}/haive_full_backup_${TIMESTAMP}.tar.gz"
echo ""
echo "The backup includes:"
echo "1. Working files in: ${BACKUP_DIR}/working_files/"
echo "2. Complete Git history in: ${BACKUP_DIR}/git_bundles/haive_complete.bundle"
echo "3. Submodule backups in: ${BACKUP_DIR}/submodules/"
echo "4. Repository mirror in: ${BACKUP_DIR}/haive_mirror.git"
echo "5. History mappings for migration in: ${BACKUP_DIR}/history_mapping/"
echo ""
echo "To restore from bundle:"
echo "  mkdir restore_temp"
echo "  cd restore_temp"
echo "  git clone \"${BACKUP_DIR}/git_bundles/haive_complete.bundle\" -b main haive_restored"
echo ""
echo "To restore from mirror:"
echo "  git clone \"${BACKUP_DIR}/haive_mirror.git\" haive_restored"
echo "====================================================="

# Optional: Create a "latest" symlink to the most recent backup
ln -sf "${TIMESTAMP}" "${BACKUP_ROOT}/latest"
