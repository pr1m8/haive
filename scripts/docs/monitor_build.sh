#!/bin/bash
# Monitor the build in real-time

# Find the latest log file
LOG_DIR="docs/source/logs/build"
mkdir -p $LOG_DIR

# Start the build in background
echo "Starting build..."
nox -s docs_fast >/tmp/nox_output.log 2>&1 &
NOX_PID=$!

# Wait a moment for log file to be created
sleep 2

# Find the newest log file
LATEST_LOG=$(ls -t $LOG_DIR/sphinx_build_*.log 2>/dev/null | head -1)

if [ -z "$LATEST_LOG" ]; then
	echo "No log file found, showing nox output:"
	tail -f /tmp/nox_output.log &
	TAIL_PID=$!
else
	echo "Monitoring log: $LATEST_LOG"
	tail -f "$LATEST_LOG" &
	TAIL_PID=$!
fi

# Wait for nox to complete
wait $NOX_PID
EXIT_CODE=$?

# Kill tail
kill $TAIL_PID 2>/dev/null

echo "Build completed with exit code: $EXIT_CODE"

# Show final results
echo "=== Final Build Summary ==="
if [ -f /tmp/nox_output.log ]; then
	grep -E "(HTML files|generated|Built|failed|error)" /tmp/nox_output.log | tail -20
fi

# Count HTML files
HTML_COUNT=$(find docs/build -name "*.html" 2>/dev/null | wc -l)
echo "Total HTML files generated: $HTML_COUNT"
