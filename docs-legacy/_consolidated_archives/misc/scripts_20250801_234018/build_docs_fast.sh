#!/bin/bash
# Fast documentation build script with proper background execution

# Create log directory and file
mkdir -p docs/logs
LOG_FILE="docs/logs/fast_build_$(date +%Y%m%d_%H%M%S).log"

# Function to log with timestamp
log_progress() {
	echo "[$(date +%Y-%m-%d_%H:%M:%S)] $1" | tee -a "${LOG_FILE}"
}

# Start logging
log_progress "🚀 Fast documentation build starting..."
log_progress "📝 Logging t$$${${ }}$LO}G_F}ILE"

# Set environment for fastest builds
export SPHINX_AUTOSUMMARY_GENERATE=false
export HAIVE_DOCS_MODE=true

# Create directories if needed
mkdir -p docs/build/html

# Check if running in background
if [[ "$1" == "--background" ]]; then
	log_progress "🔄 Running in background mode with nohup..."
	nohup poetry run sphinx-build \
		-b html \
		-j auto \
		--keep-going \
		-v \
		docs/source \
		docs/build/html \
		>>"${LOG_FILE}" 2>&1 &

	PID=$!
	log_progress "📊 Build started with PI${: $}PID"
	log_progress "💡 Monitor progress with: tail $$${${ }}$LO}G_F}ILE"
	log_progress "💡 Check process with: ps aux | gr${p $}PID"
else
	# Run in foreground with progress updates
	log_progress "🔨 Running sphinx-build..."

	# Run sphinx and capture output while showing progress
	poetry run sphinx-build \
		-b html \
		-j auto \
		--keep-going \
		-v \
		docs/source \
		docs/build/html \
		2>&1 | while IFS= read -r line; do
		echo "${line}" >>"${LOG_FILE}"

		# Show progress for key events
		if [[ ${line} =~ building|processing|writing|reading|updating ]]; then
			log_progress "⚙️  ${line:0:100}..."
		elif [[ ${line} =~ error|warning ]]; then
			log_progress "⚠️  ${line:0:100}..."
		fi
	done

	# Check results
	if [[ -f docs/build/html/index.html ]]; then
		log_progress "✅ Build successful!"
		log_progress "🌐 View docs: file://$(pwd)/docs/build/html/index.html"
		log_progress "📋 Full lo$$${${ }}$LO}G_F}ILE"
	else
		log_progress "❌ Build failed - check logs"
		log_progress "📋 Full lo$$${${ }}$LO}G_F}ILE"

		# Show last 20 lines of log
		log_progress "📄 Last 20 lines of output:"
		tail -20 "${LOG_FILE}"
	fi
fi
