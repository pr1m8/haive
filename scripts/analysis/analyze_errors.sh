#!/bin/bash
# Simple runner for pyright error analysis

cd "$(dirname "$0")/../.."

echo "Running Pyright Error Analysis..."
echo "================================"

# Ensure we're in poetry environment
poetry run python scripts/analysis/pyright_error_analyzer.py

# Open the latest report if on a system with 'open' command
if command -v open &>/dev/null; then
	LATEST_REPORT=$(ls -t error_reports/*/error_analysis_summary.md 2>/dev/null | head -1)
	if [ -n "$LATEST_REPORT" ]; then
		echo
		echo "Opening report: $LATEST_REPORT"
		open "$LATEST_REPORT"
	fi
elif command -v xdg-open &>/dev/null; then
	LATEST_REPORT=$(ls -t error_reports/*/error_analysis_summary.md 2>/dev/null | head -1)
	if [ -n "$LATEST_REPORT" ]; then
		echo
		echo "Opening report: $LATEST_REPORT"
		xdg-open "$LATEST_REPORT"
	fi
fi
