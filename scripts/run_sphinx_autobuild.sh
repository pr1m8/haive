#!/bin/bash

# Sphinx Auto-build Runner
# This script starts sphinx-autobuild in the background with file watching

echo "=== Starting Sphinx Auto-build ==="
echo "Time: $(date)"

# Kill any existing sphinx processes
echo "Cleaning up existing processes..."
pkill -f sphinx-build 2>/dev/null
pkill -f sphinx-autobuild 2>/dev/null
lsof -ti :8003 | xargs kill -9 2>/dev/null
sleep 1

# Change to docs directory
cd /home/will/Projects/haive/backend/haive/docs || exit

# Start sphinx-autobuild
echo "Starting sphinx-autobuild on port 8003..."
nohup poetry run sphinx-autobuild \
	--port 8003 \
	--host 0.0.0.0 \
	--ignore "*.pyc" \
	--ignore "**/__pycache__" \
	--ignore "**/.git" \
	--ignore "**/tests" \
	source build/html \
	>/tmp/sphinx_autobuild.log 2>&1 &

# Get the process ID
PID=$!
echo "${PID}" >/tmp/sphinx_autobuild.pid

# Wait a moment for startup
sleep 3

# Check if it started successfully
if ps -p "${PID}" >/dev/null; then
	echo ""
	echo "✅ Sphinx auto-build started successfully!"
	echo "   PID: ${PID}"
	echo "   URL: http://localhost:8003"
	echo "   Logs: tail -f /tmp/sphinx_autobuild.log"
	echo ""
	echo "The server will:"
	echo "  - Watch for file changes in docs/source"
	echo "  - Auto-rebuild when files change"
	echo "  - Live-reload the browser"
	echo ""
	echo "To stop: kill ${PID}"
else
	echo "❌ Failed to start sphinx-autobuild"
	echo "Check logs: cat /tmp/sphinx_autobuild.log"
fi
