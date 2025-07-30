#!/bin/bash
# Real-time Documentation Build Script with Line-by-Line Output
# Created: 2025-07-29 16:45
# Purpose: Show full real-time output of documentation build process

set -e

echo "🚀 Starting Real-Time Documentation Build..."
echo "📅 $(date)"
echo "📁 Working directory: $(pwd)"
echo "==============================================="

# Ensure we're in the right directory
cd /home/will/Projects/haive/backend/haive

# Create logs directory
mkdir -p docs/logs

# Set log file with timestamp
LOG_FILE="docs/logs/realtime_build_$(date +%Y%m%d_%H%M%S).log"

echo "📝 Logging to: $LOG_FILE"
echo "==============================================="

# Function to log with timestamp
log_with_timestamp() {
	echo "[$(date +'%H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log_with_timestamp "🔍 Checking Poetry environment..."
poetry env info

log_with_timestamp "📦 Installing docs dependencies..."
poetry install --only docs --no-interaction

log_with_timestamp "🧹 Cleaning previous build..."
rm -rf docs/build/

log_with_timestamp "🔨 Starting Sphinx build with REAL-TIME output..."
echo "==============================================="

# Run sphinx-build with real-time output - NO BUFFERING
poetry run sphinx-build \
	-b html \
	-W --keep-going \
	-v \
	docs/source \
	docs/build/html \
	2>&1 | while IFS= read -r line; do
	echo "[$(date +'%H:%M:%S')] $line" | tee -a "$LOG_FILE"
done

BUILD_STATUS=${PIPESTATUS[0]}

if [ $BUILD_STATUS -eq 0 ]; then
	log_with_timestamp "✅ Documentation build SUCCESSFUL!"
	log_with_timestamp "🌐 View docs: file://$(pwd)/docs/build/html/index.html"
else
	log_with_timestamp "❌ Documentation build completed with warnings/errors (status: $BUILD_STATUS)"
	log_with_timestamp "🌐 Partial build available: file://$(pwd)/docs/build/html/index.html"
fi

log_with_timestamp "📋 Full build log saved: $LOG_FILE"
echo "==============================================="
echo "🏁 Build process complete!"
