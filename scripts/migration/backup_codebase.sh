# scripts/migration/backup_codebase.sh
#!/bin/bash
# Create a backup of the codebase before migration

# Get current timestamp for the backup filename
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="haive_backup_${TIMESTAMP}.tar.gz"

# Create the backup
echo "Creating backup of the codebase..."
tar -czf "${BACKUP_NAME}" \
    --exclude="*/__pycache__" \
    --exclude="*.pyc" \
    --exclude=".venv" \
    --exclude=".git" \
    --exclude="*.tar.gz" \
    src/ tests/ pyproject.toml README.md

# Verify the backup was created successfully
if [ -f "${BACKUP_NAME}" ]; then
    BACKUP_SIZE=$(du -h "${BACKUP_NAME}" | cut -f1)
    echo "Backup created successfully: ${BACKUP_NAME} (${BACKUP_SIZE})"
    echo "To restore: tar -xzf ${BACKUP_NAME}"
else
    echo "Error: Backup creation failed"
    exit 1
fi