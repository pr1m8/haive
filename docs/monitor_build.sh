#!/bin/bash

# Monitor build progress
STATUS_FILE="/tmp/haive_docs_build.status"
LOG_FILE="/tmp/haive_docs_build.log"
PID_FILE="/tmp/haive_docs_build.pid"

while true; do
	clear
	echo "=== Haive Documentation Build Monitor ==="
	echo "Time: $(date)"
	echo ""

	# Check status
	if [[ -f "${STATUS_FILE}" ]]; then
		STATUS=$(cat "${STATUS_FILE}")
		case ${STATUS} in
		"STARTING")
			echo "📦 Status: BUILD IN PROGRESS..."
			;;
		"SUCCESS")
			echo "✅ Status: BUILD SUCCESSFUL!"
			echo ""
			echo "🌐 Documentation available at:"
			echo "   http://localhost:8002/api/haive/index.html"
			break
			;;
		"FAILED")
			echo "❌ Status: BUILD FAILED"
			echo ""
			echo "Check log: tail -20 ${LOG_FILE}"
			break
			;;
		"TIMEOUT")
			echo "⏱️ Status: BUILD TIMED OUT"
			break
			;;
		esac
	fi

	# Check if process is running
	if [[ -f "${PID_FILE}" ]]; then
		PID=$(cat "${PID_FILE}")
		if ps -p "${PID}" >/dev/null 2>&1; then
			echo "🔄 Process: Running (PI${: $}PID)"

			# Estimate progress by checking built files
			if [[ -d "docs/build/html" ]]; then
				HTML_COUNT=$(find docs/build/html -name "*.html" 2>/dev/null | wc -l)
				echo "📄 HTML files buil$$$${${${${${${${}} $H}TML}_CO}UNT"

				# Check if new structure exists
				if [[ -f "docs/build/html/api/haive/index.html" ]]; then
					echo "✅ New /api/haive/ structure detected!"
				fi
			fi
		else
			echo "⚠️ Process: Not running"
		fi
	fi

	echo ""
	echo "Last log entry:"
	tail -1 "${LOG_FILE}" 2>/dev/null || echo "No log available"

	echo ""
	echo "Press Ctrl+C to exit monitor"

	sleep 5
done
