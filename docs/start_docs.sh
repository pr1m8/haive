#!/bin/bash

# Haive Documentation Auto-build Script
# Starts sphinx-autobuild in the background and keeps it running

DOCS_DIR="/home/will/Projects/haive/backend/haive/docs"
PID_FILE="$DOCS_DIR/docs_server.pid"
LOG_FILE="$DOCS_DIR/docs_server.log"

# Function to start the docs server
start_docs() {
    echo "Starting Haive documentation server..."
    cd "$DOCS_DIR"
    
    # Kill any existing docs server
    if [ -f "$PID_FILE" ]; then
        OLD_PID=$(cat "$PID_FILE")
        if kill -0 "$OLD_PID" 2>/dev/null; then
            echo "Stopping existing docs server (PID: $OLD_PID)"
            kill "$OLD_PID"
            sleep 2
        fi
        rm -f "$PID_FILE"
    fi
    
    # Start new server in background
    nohup poetry run sphinx-autobuild source _build/html \
        --port 8003 \
        --host 0.0.0.0 \
        --ignore "*.pyc" \
        --watch ../packages \
        --open-browser \
        -j auto > "$LOG_FILE" 2>&1 &
    
    # Save PID
    echo $! > "$PID_FILE"
    
    echo "Documentation server started!"
    echo "- PID: $(cat "$PID_FILE")"
    echo "- URL: http://localhost:8003"
    echo "- Log: $LOG_FILE"
    echo "- To stop: $0 stop"
}

# Function to stop the docs server
stop_docs() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "Stopping docs server (PID: $PID)"
            kill "$PID"
            rm -f "$PID_FILE"
            echo "Documentation server stopped."
        else
            echo "Documentation server is not running."
            rm -f "$PID_FILE"
        fi
    else
        echo "No PID file found. Server may not be running."
    fi
}

# Function to check status
status_docs() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "Documentation server is running (PID: $PID)"
            echo "URL: http://localhost:8003"
            echo "Log: $LOG_FILE"
        else
            echo "Documentation server is not running (stale PID file)"
            rm -f "$PID_FILE"
        fi
    else
        echo "Documentation server is not running."
    fi
}

# Function to show logs
logs_docs() {
    if [ -f "$LOG_FILE" ]; then
        echo "=== Documentation Server Logs ==="
        tail -f "$LOG_FILE"
    else
        echo "No log file found at $LOG_FILE"
    fi
}

# Main script logic
case "${1:-start}" in
    start)
        start_docs
        ;;
    stop)
        stop_docs
        ;;
    restart)
        stop_docs
        sleep 2
        start_docs
        ;;
    status)
        status_docs
        ;;
    logs)
        logs_docs
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the documentation server (default)"
        echo "  stop    - Stop the documentation server"
        echo "  restart - Restart the documentation server"
        echo "  status  - Check server status"
        echo "  logs    - Show server logs (live tail)"
        echo ""
        echo "Server will run at: http://localhost:8003"
        exit 1
        ;;
esac