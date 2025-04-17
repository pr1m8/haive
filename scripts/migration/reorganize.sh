#!/bin/bash
# scripts/migrations/reorganize.sh

# Create necessary directories
mkdir -p data
mkdir -p examples/notebooks
mkdir -p docs/reports
mkdir -p config/certs
mkdir -p scripts/migrations
mkdir -p backup

# Move notebooks to examples/notebooks
echo "Moving notebooks..."
mv BaseAgent.ipynb examples/notebooks/
mv SequentialAgent.ipynb examples/notebooks/
mv notebooks/*.ipynb examples/notebooks/ 2>/dev/null || true

# Move reports to docs/reports
echo "Moving reports..."
mv scancode-report.html docs/reports/
mv reports/* docs/reports/ 2>/dev/null || true
rmdir reports 2>/dev/null || true

# Move certs to config/certs
echo "Moving certificates..."
mv certs/* config/certs/ 2>/dev/null || true
rmdir certs 2>/dev/null || true

# Move test files to tests
echo "Moving test files..."
mv test_monopoly.py tests/
mv test_monopoly_config.py tests/

# Move data files to data directory
echo "Moving data files..."
mv agent_analysis.json data/
mv output_file.json data/
mv Chinook.db data/
mv *.db data/ 2>/dev/null || true

# Backup archive files
echo "Archiving large files..."
mkdir -p backup/archives
mv *.tar.gz backup/archives/ 2>/dev/null || true

# Cleanup temp files
echo "Cleaning up logs..."
mkdir -p logs
mv *.log logs/ 2>/dev/null || true
mv debug_simple_agent.log logs/ 2>/dev/null || true
mv poker_debug.log logs/ 2>/dev/null || true
mv poker_test.log logs/ 2>/dev/null || true

# Clean registry scripts 
echo "Organizing scripts..."
mkdir -p scripts/tools
mv check_registry_data.py scripts/tools/
mv store_registry_data.py scripts/tools/

# Remove empty directories
echo "Cleaning empty directories..."
find . -type d -empty -delete 2>/dev/null || true

echo "Reorganization complete!"