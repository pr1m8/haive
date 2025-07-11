#!/bin/bash

# Simple docs server script
# Usage: ./serve.sh [port]

PORT=${1:-8003}
HOST="0.0.0.0"

echo "Starting documentation server..."
echo "Available at: http://localhost:${PORT}"
echo "Press Ctrl+C to stop"

poetry run sphinx-autobuild source _build/html \
	--port "${PORT}" \
	--host "${HOST}" \
	--ignore "*.pyc" \
	--ignore "*.pyo" \
	--ignore "*~" \
	--ignore ".git/*" \
	--ignore "_build/*" \
	--watch ../packages \
	--open-browser \
	-j auto
