#!/bin/bash
# cleanup.sh - Script to clean up project structure

# Create backup directory
BACKUP_DIR="backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

# Clean up caches
echo "Cleaning up cache directories..."
rm -rf .mypy_cache .pytest_cache __pycache__ .nox .history .ipynb_checkpoints

# Move log files to logs directory
echo "Organizing log files..."
mkdir -p logs
find . -maxdepth 1 -name "*.log" -exec mv {} logs/ \;

# Move notebooks to notebooks directory
echo "Organizing notebooks..."
mkdir -p notebooks
find . -maxdepth 1 -name "*.ipynb" -exec mv {} notebooks/ \;

# Move test files to tests directory
echo "Organizing test files..."
mkdir -p tests
find . -maxdepth 1 -name "test_*.py" -exec mv {} tests/ \;

# Archive data files
echo "Organizing data files..."
mkdir -p $BACKUP_DIR/data
find . -maxdepth 1 -name "*.json" -not -name "package.json" -not -name "poetry.json" -exec mv {} $BACKUP_DIR/data/ \;
find . -maxdepth 1 -name "*.db" -exec mv {} $BACKUP_DIR/data/ \;

# Backup archive files
echo "Backing up archives..."
mkdir -p $BACKUP_DIR/archives
find . -maxdepth 1 -name "*.tar.gz" -exec mv {} $BACKUP_DIR/archives/ \;

# Organize config files
echo "Organizing configuration files..."
mkdir -p config
if [ -f .env.example ]; then
  cp .env.example config/
fi

echo "Cleanup complete. Temporary files backed up to $BACKUP_DIR"
echo "You may want to review the backup directory before deleting it."