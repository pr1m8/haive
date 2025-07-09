#!/bin/bash

# Documentation Server Management Script
# Usage: ./start_docs_server.sh [start|stop|restart|status]

DOCS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$DOCS_DIR")"
PID_FILE="$DOCS_DIR/docs_server.pid"
LOG_FILE="$DOCS_DIR/docs_server.log"
PORT=8003
HOST="0.0.0.0"

cd "$DOCS_DIR"

start_server() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "Documentation server already running (PID: $PID)"
            echo "View at: http://localhost:$PORT"
            return 0
        else
            rm -f "$PID_FILE"
        fi
    fi

    echo "Starting documentation server..."
    echo "Log file: $LOG_FILE"
    
    # Kill any existing sphinx processes
    pkill -f "sphinx-autobuild.*--port $PORT" 2>/dev/null || true
    
    # Start the server
    nohup poetry run sphinx-autobuild \
        source _build/html \
        --port "$PORT" \
        --host "$HOST" \
        --ignore "*.pyc" \
        --ignore "*.pyo" \
        --ignore "*~" \
        --ignore ".git/*" \
        --ignore "_build/*" \
        --watch ../packages \
        --open-browser \
        -j auto \
        > "$LOG_FILE" 2>&1 &
    
    SERVER_PID=$!
    echo $SERVER_PID > "$PID_FILE"
    
    # Wait a moment to check if server started successfully
    sleep 2
    if kill -0 "$SERVER_PID" 2>/dev/null; then
        echo "Documentation server started successfully (PID: $SERVER_PID)"
        echo "View at: http://localhost:$PORT"
        echo "Logs: tail -f $LOG_FILE"
    else
        echo "Failed to start documentation server"
        echo "Check logs: cat $LOG_FILE"
        rm -f "$PID_FILE"
        return 1
    fi
}

stop_server() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "Stopping documentation server (PID: $PID)..."
            kill "$PID"
            rm -f "$PID_FILE"
            echo "Documentation server stopped"
        else
            echo "Documentation server not running"
            rm -f "$PID_FILE"
        fi
    else
        echo "No PID file found"
    fi
    
    # Kill any lingering sphinx processes
    pkill -f "sphinx-autobuild.*--port $PORT" 2>/dev/null || true
}

status_server() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "Documentation server is running (PID: $PID)"
            echo "View at: http://localhost:$PORT"
            echo "Logs: tail -f $LOG_FILE"
        else
            echo "Documentation server not running (stale PID file)"
            rm -f "$PID_FILE"
        fi
    else
        echo "Documentation server not running"
    fi
}

restart_server() {
    stop_server
    sleep 1
    start_server
}

case "$1" in
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
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the documentation server"
        echo "  stop    - Stop the documentation server"
        echo "  restart - Restart the documentation server"
        echo "  status  - Check server status"
        echo ""
        echo "Server will be available at: http://localhost:$PORT"
        exit 1
        ;;
esac