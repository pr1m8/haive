#!/bin/bash
# Quick rebuild script that runs in background

cd /home/will/Projects/haive/backend/haive/docs || exit

# Kill any existing build processes
pkill -f "sphinx-build" 2>/dev/null

# Run build in background with minimal output
nohup poetry run sphinx-build -b html source build/html -q >/tmp/sphinx_rebuild.log 2>&1 &

echo "✅ Rebuild started in background (PID: $!)"
echo "📋 Check progress: tail -f /tmp/sphinx_rebuild.log"
