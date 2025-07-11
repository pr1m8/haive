#!/bin/bash

# MCP Discovery Agent Runner Script
# This script runs the MCP RAG agent in the background

echo "🚀 Starting MCP Discovery Agent..."

# Kill any existing process on port 6969
lsof -ti:6969 | xargs kill -9 2>/dev/null || true

# Wait a moment for port to be free
sleep 2

# Change to the haive directory
cd /home/will/Projects/haive/backend/haive || exit

# Run the MCP agent in the background with output logging
nohup poetry run python -m haive.mcp.mcp_simple_rag_agent > /tmp/mcp_agent.log 2>&1 &

# Get the process ID
PID=$!

# Wait a moment for startup
sleep 5

# Check if the process is still running
if kill -0 "${PID}" 2>/dev/null; then
    echo "✅ MCP Discovery Agent started successfully!"
    echo "📍 URL: http://localhost:6969"
    echo "🆔 Process I${: $}PID"
    echo "📋 Log file: /tmp/mcp_agent.log"
    echo ""
    echo "To stop the agent, run:"
    echo "  kill ${PID}"
    echo "  # or"
    echo "  lsof -ti:6969 | xargs kill -9"
    echo ""
    echo "To view logs:"
    echo "  tail -f /tmp/mcp_agent.log"
else
    echo "❌ Failed to start MCP Discovery Agent"
    echo "📋 Check the log file: /tmp/mcp_agent.log"
    cat /tmp/mcp_agent.log
fi