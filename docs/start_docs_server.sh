#!/bin/bash

# Documentation Server Management Script with Enhanced Logging and Error Handling
# Usage: ./start_docs_server.sh [start|stop|restart|status|build|autobuild|debug]

set -euo pipefail # Exit on error, undefined vars, pipe failures

DOCS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "${DOCS_DIR}")"
PID_FILE="${DOCS_DIR}/docs_server.pid"
LOG_FILE="${DOCS_DIR}/docs_server.log"
BUILD_LOG_FILE="${DOCS_DIR}/docs_build.log"
DEBUG_LOG_FILE="${DOCS_DIR}/docs_debug.log"
PORT=8003
HOST="0.0.0.0"

cd "${DOCS_DIR}"

# Logging functions
log_info() {
	echo "[INFO] $(date '+%Y-%m-%d %H:%M:%S'): $1" | tee -a "${DEBUG_LOG_FILE}"
}

log_error() {
	echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S'): $1" | tee -a "${DEBUG_LOG_FILE}" >&2
}

log_debug() {
	echo "[DEBUG] $(date '+%Y-%m-%d %H:%M:%S'): $1" >>"${DEBUG_LOG_FILE}"
}

# Error handling function
handle_error() {
	local exit_code=$1
	local line_number=$2
	local command="$3"

	log_error "Command failed with exit code ${exit_code} at line ${line_number}: ${command}"
	log_error "Working directory: $(pwd)"
	log_error "Environment: $(env | grep -E '(PATH|VIRTUAL_ENV|POETRY)' | head -5)"

	if [[ -f "${LOG_FILE}" ]]; then
		log_error "Last 10 lines of server log:"
		tail -n 10 "${LOG_FILE}" | while read -r line; do
			log_error "  ${line}"
		done
	fi

	cleanup_on_exit
	exit "$exit_code"
}

# Set up error handling
trap 'handle_error $? $LINENO "$BASH_COMMAND"' ERR

# Cleanup function
cleanup_on_exit() {
	log_debug "Cleanup function called"
	# Don't kill server on normal script exit, only on error
	if [[ "${CLEANUP_SERVER-}" = "true" ]]; then
		pkill -f "sphinx-autobuild.*--port ${PORT}" 2>/dev/null || true
	fi
}

# Pre-flight checks
check_environment() {
	log_info "Starting environment checks..."

	# Check if poetry is available
	if ! command -v poetry &>/dev/null; then
		log_error "Poetry not found in PATH"
		return 1
	fi
	log_info "✓ Poetry found: $(which poetry)"

	# Check if we're in a poetry project
	if [[ ! -f "../pyproject.toml" ]]; then
		log_error "Not in a poetry project (no pyproject.toml found)"
		return 1
	fi
	log_info "✓ Poetry project detected"

	# Check if sphinx-autobuild is installed
	if ! poetry run python -c "import sphinx_autobuild" 2>/dev/null; then
		log_error "sphinx-autobuild not installed"
		log_error "Run: poetry install --all-extras"
		return 1
	fi
	log_info "✓ sphinx-autobuild available"

	# Check if source directory exists
	if [[ ! -d "source" ]]; then
		log_error "Source directory not found"
		return 1
	fi
	log_info "✓ Source directory exists"

	# Check if conf.py exists
	if [[ ! -f "source/conf.py" ]]; then
		log_error "conf.py not found in source directory"
		return 1
	fi
	log_info "✓ conf.py found"

	# Check port availability
	if lsof -Pi :"$PORT" -sTCP:LISTEN -t >/dev/null 2>&1; then
		log_info "WARNING: Port ${PORT} is already in use"
		log_info "Attempting to kill existing processes..."
		pkill -f "sphinx-autobuild.*--port ${PORT}" 2>/dev/null || true
		sleep 2
		if lsof -Pi :"$PORT" -sTCP:LISTEN -t >/dev/null 2>&1; then
			log_error "Port ${PORT} still in use after cleanup"
			return 1
		fi
	fi
	log_info "✓ Por${ $PO}RT is available"

	log_info "All environment checks passed"
	return 0
}

start_server() {
	log_info "=== Starting Documentation Server ==="
	log_info "Time: $(date)"
	log_info "Working directory: $(pwd)"
	log_info "Log file: ${LOG_FILE}"
	log_info "PID file: ${PID_FILE}"
	log_info "Port: ${PORT}"
	log_info "Host: ${HOST}"

	# Check if server is already running
	if [[ -f "${PID_FILE}" ]]; then
		PID=$(cat "${PID_FILE}")
		if kill -0 "${PID}" 2>/dev/null; then
			log_info "Documentation server already running (PID: ${PID})"
			log_info "View at: http://localhost:${PORT}"
			return 0
		else
			log_info "Removing stale PID file..."
			rm -f "${PID_FILE}"
		fi
	fi

	# Run pre-flight checks
	if ! check_environment; then
		log_error "Environment checks failed"
		return 1
	fi

	log_info "=== Starting Sphinx Autobuild ==="

	# Initialize log file with header
	{
		echo "=== Documentation Server Log ==="
		echo "Started: $(date)"
		echo "Command: poetry run sphinx-autobuild source _build/html --port ${PORT} --host ${HOST}"
		echo "Working directory: $(pwd)"
		echo "Python path: $(poetry run python -c 'import sys; print(sys.path)')"
		echo "================================="
		echo ""
	} >"${LOG_FILE}"

	# Start the server with comprehensive logging
	log_info "Executing sphinx-autobuild command..."

	# Use a wrapper script for better error handling
	{
		echo "#!/bin/bash"
		echo "set -euo pipefail"
		echo "cd '${DOCS_DIR}'"
		echo 'exec poetry run sphinx-autobuild \'
		echo '    source _build/html \'
		echo "    --port '${PORT}' \\"
		echo "    --host '${HOST}' \\"
		echo "    --ignore '*.pyc' \\"
		echo "    --ignore '*.pyo' \\"
		echo "    --ignore '*~' \\"
		echo "    --ignore '.git/*' \\"
		echo "    --ignore '_build/*' \\"
		echo '    --watch ../packages \'
		echo '    --open-browser \'
		echo "    -j auto"
	} >"${DOCS_DIR}/sphinx_wrapper.sh"

	chmod +x "${DOCS_DIR}/sphinx_wrapper.sh"

	# Start the server
	nohup "${DOCS_DIR}/sphinx_wrapper.sh" >>"${LOG_FILE}" 2>&1 &
	SERVER_PID=$!
	echo "$SERVER_PID" >"${PID_FILE}"

	log_info "Server PID: ${SERVER_PID}"
	log_info "Waiting for server to start..."

	# Wait and check if server started successfully
	for i in {1..15}; do
		sleep 2
		if ! kill -0 "${SERVER_PID}" 2>/dev/null; then
			log_error "Server process died (attempt ${i}/15)"
			log_error "Last 20 lines of log:"
			tail -n 20 "${LOG_FILE}" | while read -r line; do
				log_error "  ${line}"
			done
			rm -f "${PID_FILE}"
			return 1
		fi

		# Check if server is responding
		if curl -s --connect-timeout 2 "http://localhost:${PORT}" >/dev/null 2>&1; then
			log_info "✓ Server responding on por${ $PO}RT"
			break
		elif [[ "$i" -eq 15 ]]; then
			log_info "WARNING: Server not responding after 30 seconds"
			log_info "This may be normal if Sphinx is still building..."
		fi
	done

	log_info "=== Server Started Successfully ==="
	log_info "PID: ${SERVER_PID}"
	log_info "URL: http://localhost:${PORT}"
	log_info "Logs: tail -f ${LOG_FILE}"
	log_info "Debug: tail -f ${DEBUG_LOG_FILE}"
	log_info "Stop: $0 stop"
	log_info "Status: $0 status"
	log_info "================================="

	# Clean up wrapper script
	rm -f "${DOCS_DIR}/sphinx_wrapper.sh"
}

stop_server() {
	log_info "=== Stopping Documentation Server ==="

	if [[ -f "${PID_FILE}" ]]; then
		PID=$(cat "${PID_FILE}")
		if kill -0 "${PID}" 2>/dev/null; then
			log_info "Stopping documentation server (PID: ${PID})..."
			kill "${PID}"

			# Wait for graceful shutdown
			for i in {1..10}; do
				if ! kill -0 "${PID}" 2>/dev/null; then
					log_info "Server stopped gracefully"
					break
				fi
				sleep 1
			done

			# Force kill if still running
			if kill -0 "${PID}" 2>/dev/null; then
				log_info "Force killing server..."
				kill -9 "${PID}" 2>/dev/null || true
			fi

			rm -f "${PID_FILE}"
		else
			log_info "Documentation server not running"
			rm -f "${PID_FILE}"
		fi
	else
		log_info "No PID file found"
	fi

	# Kill any lingering sphinx processes
	if pkill -f "sphinx-autobuild.*--port ${PORT}" 2>/dev/null; then
		log_info "Killed lingering sphinx processes"
	fi

	log_info "Documentation server stopped"
}

status_server() {
	log_info "=== Server Status Check ==="

	if [[ -f "${PID_FILE}" ]]; then
		PID=$(cat "${PID_FILE}")
		if kill -0 "${PID}" 2>/dev/null; then
			log_info "Documentation server is running (PID: ${PID})"
			log_info "View at: http://localhost:${PORT}"
			log_info "Logs: tail -f ${LOG_FILE}"
			log_info "Debug: tail -f ${DEBUG_LOG_FILE}"

			# Check if server is responding
			if curl -s --connect-timeout 2 "http://localhost:${PORT}" >/dev/null 2>&1; then
				log_info "✓ Server is responding"
			else
				log_info "⚠ Server process exists but not responding"
			fi
		else
			log_info "Documentation server not running (stale PID file)"
			rm -f "${PID_FILE}"
		fi
	else
		log_info "Documentation server not running"
	fi
}

restart_server() {
	log_info "=== Restarting Documentation Server ==="
	stop_server
	sleep 2
	start_server
}

build_docs() {
	log_info "=== Building Documentation ==="
	log_info "Build log: ${BUILD_LOG_FILE}"

	# Run pre-flight checks
	if ! check_environment; then
		log_error "Environment checks failed"
		return 1
	fi

	# Clean previous build
	log_info "Cleaning previous build..."
	rm -rf _build/

	# Build documentation with detailed logging
	log_info "Starting documentation build..."

	{
		echo "=== Documentation Build Log ==="
		echo "Started: $(date)"
		echo "Command: poetry run sphinx-build source _build/html -j auto"
		echo "Working directory: $(pwd)"
		echo "================================="
		echo ""
	} >"${BUILD_LOG_FILE}"

	if poetry run sphinx-build source _build/html -j auto >>"${BUILD_LOG_FILE}" 2>&1; then
		log_info "Documentation built successfully"
		log_info "Output: _build/html/index.html"
		log_info "View at: file://${DOCS_DIR}/_build/html/index.html"

		# Check if index.html was created
		if [[ -f "_build/html/index.html" ]]; then
			log_info "✓ Index file created successfully"
		else
			log_error "Index file not found after build"
			return 1
		fi
	else
		log_error "Documentation build failed"
		log_error "Check logs: cat ${BUILD_LOG_FILE}"
		log_error "Last 20 lines of build log:"
		tail -n 20 "${BUILD_LOG_FILE}" | while read -r line; do
			log_error "  ${line}"
		done
		return 1
	fi
}

autobuild_docs() {
	log_info "=== Starting Autobuild Mode ==="
	log_info "This will rebuild docs automatically when files change"
	log_info "Press Ctrl+C to stop"
	log_info "Build log: ${BUILD_LOG_FILE}"

	# Run pre-flight checks
	if ! check_environment; then
		log_error "Environment checks failed"
		return 1
	fi

	# Set up signal handling for clean exit
	trap 'log_info "Autobuild stopped by user"; exit 0' INT TERM

	# Run autobuild without server
	poetry run sphinx-autobuild \
		source _build/html \
		--ignore "*.pyc" \
		--ignore "*.pyo" \
		--ignore "*~" \
		--ignore ".git/*" \
		--ignore "_build/*" \
		--watch ../packages \
		--no-open-browser \
		-j auto 2>&1 | tee "${BUILD_LOG_FILE}"
}

debug_environment() {
	log_info "=== Debug Environment Information ==="

	echo "=== System Information ===" | tee -a "${DEBUG_LOG_FILE}"
	echo "Date: $(date)" | tee -a "${DEBUG_LOG_FILE}"
	echo "User: $(whoami)" | tee -a "${DEBUG_LOG_FILE}"
	echo "Working directory: $(pwd)" | tee -a "${DEBUG_LOG_FILE}"
	echo "Shell: ${SHELL}" | tee -a "${DEBUG_LOG_FILE}"
	echo "" | tee -a "${DEBUG_LOG_FILE}"

	echo "=== Python Environment ===" | tee -a "${DEBUG_LOG_FILE}"
	echo "Python version: $(python3 --version 2>&1)" | tee -a "${DEBUG_LOG_FILE}"
	echo "Python path: $(which python3)" | tee -a "${DEBUG_LOG_FILE}"
	echo "" | tee -a "${DEBUG_LOG_FILE}"

	echo "=== Poetry Environment ===" | tee -a "${DEBUG_LOG_FILE}"
	echo "Poetry version: $(poetry --version 2>&1)" | tee -a "${DEBUG_LOG_FILE}"
	echo "Poetry path: $(which poetry)" | tee -a "${DEBUG_LOG_FILE}"
	echo "Poetry env info:" | tee -a "${DEBUG_LOG_FILE}"
	poetry env info 2>&1 | tee -a "${DEBUG_LOG_FILE}"
	echo "" | tee -a "${DEBUG_LOG_FILE}"

	echo "=== Project Structure ===" | tee -a "${DEBUG_LOG_FILE}"
	echo "Project root: ${PROJECT_ROOT}" | tee -a "${DEBUG_LOG_FILE}"
	echo "Docs directory: ${DOCS_DIR}" | tee -a "${DEBUG_LOG_FILE}"
	echo "Source directory exists: $([[ -d source ]] && echo 'Yes' || echo 'No')" | tee -a "${DEBUG_LOG_FILE}"
	echo "conf.py exists: $([[ -f source/conf.py ]] && echo 'Yes' || echo 'No')" | tee -a "${DEBUG_LOG_FILE}"
	echo "" | tee -a "${DEBUG_LOG_FILE}"

	echo "=== Network Information ===" | tee -a "${DEBUG_LOG_FILE}"
	echo "Port ${PORT} in use: $(lsof -Pi :"$PORT" -sTCP:LISTEN -t >/dev/null 2>&1 && echo 'Yes' || echo 'No')" | tee -a "${DEBUG_LOG_FILE}"
	echo "Processes using port ${PORT}:" | tee -a "${DEBUG_LOG_FILE}"
	lsof -Pi :"$PORT" -sTCP:LISTEN 2>/dev/null | tee -a "${DEBUG_LOG_FILE}" || echo "None" | tee -a "${DEBUG_LOG_FILE}"
	echo "" | tee -a "${DEBUG_LOG_FILE}"

	echo "=== Sphinx Processes ===" | tee -a "${DEBUG_LOG_FILE}"
	ps aux | grep sphinx | grep -v grep | tee -a "${DEBUG_LOG_FILE}" || echo "None" | tee -a "${DEBUG_LOG_FILE}"
	echo "" | tee -a "${DEBUG_LOG_FILE}"

	echo "=== Recent Log Files ===" | tee -a "${DEBUG_LOG_FILE}"
	for logfile in "${LOG_FILE}" "${BUILD_LOG_FILE}" "${DEBUG_LOG_FILE}"; do
		if [[ -f "${logfile}" ]]; then
			echo "--- ${logfile} (last 5 lines) ---" | tee -a "${DEBUG_LOG_FILE}"
			tail -n 5 "${logfile}" | tee -a "${DEBUG_LOG_FILE}"
			echo "" | tee -a "${DEBUG_LOG_FILE}"
		fi
	done

	log_info "Debug information saved to: ${DEBUG_LOG_FILE}"
}

# Main command handler
case "${1:-help}" in
start)
	start_server
	;;
stop)
	stop_server
	;;
restart)
	restart_server
	;;
status)
	status_server
	;;
build)
	build_docs
	;;
autobuild)
	autobuild_docs
	;;
debug)
	debug_environment
	;;
*)
	echo "Usage: $0 {start|stop|restart|status|build|autobuild|debug}"
	echo ""
	echo "Commands:"
	echo "  start     - Start the documentation server with live reload"
	echo "  stop      - Stop the documentation server"
	echo "  restart   - Restart the documentation server"
	echo "  status    - Check server status"
	echo "  build     - Build documentation once (no server)"
	echo "  autobuild - Auto-rebuild docs on file changes (no server)"
	echo "  debug     - Show debug information about environment"
	echo ""
	echo "Server will be available at: http://localhost:${PORT}"
	echo "Static build output: _build/html/index.html"
	echo ""
	echo "Log files:"
	echo "  Server logs: ${LOG_FILE}"
	echo "  Build logs: ${BUILD_LOG_FILE}"
	echo "  Debug logs: ${DEBUG_LOG_FILE}"
	exit 1
	;;
esac
