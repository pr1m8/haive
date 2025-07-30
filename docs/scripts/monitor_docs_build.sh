#!/bin/bash
# Monitor documentation build progress

# Find the most recent log file
LOG_FILE=$(ls -t docs/logs/fast_build_*.log 2>/dev/null | head -1)

if [ -z "$LOG_FILE" ]; then
	echo "❌ No build log found"
	exit 1
fi

echo "📊 Monitoring: $LOG_FILE"
echo "---"

# Function to show progress
show_progress() {
	local lines=$(wc -l <"$LOG_FILE")
	local errors=$(grep -c "ERROR\|error:" "$LOG_FILE" 2>/dev/null || echo 0)
	local warnings=$(grep -c "WARNING\|warning:" "$LOG_FILE" 2>/dev/null || echo 0)
	local current=$(grep -E "reading sources|writing output|building \[" "$LOG_FILE" | tail -1)

	# Count pages
	local total_pages=$(grep -c "reading sources\|writing output" "$LOG_FILE" 2>/dev/null || echo 0)
	local reading_pages=$(grep -c "reading sources" "$LOG_FILE" 2>/dev/null || echo 0)
	local writing_pages=$(grep -c "writing output" "$LOG_FILE" 2>/dev/null || echo 0)

	# Get current page being processed
	local current_page=""
	if [ -n "$current" ]; then
		# Extract just the page name from the progress line
		current_page=$(echo "$current" | sed -E 's/.*\] (.*)/\1/' | sed 's/\.\.\.//')
	fi

	echo "[$(date +%H:%M:%S)] Lines: $lines | Pages: $total_pages (R:$reading_pages W:$writing_pages) | Errors: $errors | Warnings: $warnings"
	if [ -n "$current" ]; then
		echo "Progress: ${current:0:60}..."
	fi
	if [ -n "$current_page" ]; then
		echo "Current Page: $current_page"
	fi
}

# Monitor mode
if [ "$1" == "--watch" ]; then
	echo "🔄 Watching for changes (Ctrl+C to stop)..."
	while true; do
		clear
		echo "📊 Build Progress Monitor"
		echo "========================"
		show_progress
		echo ""
		echo "Last 5 lines:"
		echo "-------------"
		tail -5 "$LOG_FILE"
		sleep 2
	done
else
	# One-time status
	show_progress
	echo ""
	echo "💡 Use '$0 --watch' for continuous monitoring"
	echo "💡 Use 'tail -f $LOG_FILE' for raw log stream"
fi
