#!/bin/bash

# Auto-build documentation with background support and timeout
BUILD_DIR="/tmp/haive_docs_build"
LOG_FILE="/tmp/haive_docs_build.log"
PID_FILE="/tmp/haive_docs_build.pid"
STATUS_FILE="/tmp/haive_docs_build.status"

# Function to get timestamp
timestamp() {
	date '+%Y-%m-%d %H:%M:%S'
}

# Function to cleanup old processes
cleanup_old_build() {
	if [[ -f "${PID_FILE}" ]]; then
		OLD_PID=$(cat "${PID_FILE}")
		if ps -p "${OLD_PID}" >/dev/null 2>&1; then
			echo "[$(timestamp)] Killing existing build (PID: ${OLD_PID})"
			kill -9 "${OLD_PID}" 2>/dev/null
			sleep 1
		fi
	fi
}

# Start build
echo "[$(timestamp)] Starting Haive documentation auto-build..." >"${LOG_FILE}"
echo "STARTING" >"${STATUS_FILE}"

cd /home/will/Projects/haive/backend/haive || exit

# Cleanup old build
cleanup_old_build

# Clean build directory
echo "[$(timestamp)] Cleaning build directory..." >>"${LOG_FILE}"
rm -rf docs/build/html
mkdir -p docs/build/html

# Run build in background with timeout
echo "[$(timestamp)] Starting background build with 15 minute timeout..." >>"${LOG_FILE}"
nohup bash -c "
    timeout 900 poetry run sphinx-build -b html docs/source docs/build/html -j auto -q >> '${LOG_FILE}' 2>&1
    BUILD_EXIT=\$?

    if [ \$BUILD_EXIT -eq 0 ]; then
        echo '[$(timestamp)] ✅ Build completed successfully!' >>${'$LOG_FI}LE'
        echo 'SUCCESS' > '${STATUS_FILE}'

        # Start server if not running
        if ! lsof -ti :8002 > /dev/null 2>&1; then
            echo '[$(timestamp)] Starting documentation server on port 8002...' >> '${LOG_FILE}'
            cd docs/build/html
            nohup python -m http.server 8002 > /dev/null 2>&1 &
            echo \$! > /tmp/doc_server.pid
            echo '[$(timestamp)] Server started at http://localhost:8002' >> '${LOG_FILE}'
        fi

        # Log key URLs
        echo '[$(timestamp)] 🌐 Key URLs:' >${ '$LOG_F}ILE'
        echo '  - Main: http://localhost:8002/api/haive/index.html' >> '${LOG_FILE}'
        echo '  - Core: http://localhost:8002/api/haive/core/index.html' >> '${LOG_FILE}'
        echo '  - Engine: http://localhost:8002/api/haive/core/engine/index.html' >> '${LOG_FILE}'

    elif [ \$BUILD_EXIT -eq 124 ]; then
        echo '[$(timestamp)] ⏱️ Build timed out after 15 minutes!' ${> '$LOG_}FILE'
        echo 'TIMEOUT' > '${STATUS_FILE}'
    else
        echo '[$(timestamp)] ❌ Build failed with exit code \$BUILD_EXIT' >>${'$LOG_FI}LE'
        echo 'FAILED' > '${STATUS_FILE}'
    fi

    rm -f '${PID_FILE}'
" >/dev/null 2>&1 &

BUILD_PID=$!
echo "$BUILD_PID" >"${PID_FILE}"

echo "[$(timestamp)] Build started in background (PID: ${BUILD_PID})"
echo "[$(timestamp)] Log file: ${LOG_FILE}"
echo "[$(timestamp)] Status file: ${STATUS_FILE}"
echo ""
echo "Monitor with:"
echo "  - Status: cat ${STATUS_FILE}"
echo "  - Progress: tail -f ${LOG_FILE}"
echo "  - Check build: ps -p ${BUILD_PID}"
