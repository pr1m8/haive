#!/bin/bash

# Simple wrapper for documentation server
# Usage: ./docs-server.sh [start|stop|restart|status]

exec ./docs/start_docs_server.sh "$@"
