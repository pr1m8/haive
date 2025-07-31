#!/bin/bash

# Haive Docker Runner Script
# Usage: ./run.sh [command]

set -e

COMPOSE_FILE="docker-compose.yml"

function show_help() {
	echo "Haive Docker Runner"
	echo "Usage: $0 [command]"
	echo ""
	echo "Commands:"
	echo "  build       Build containers without starting"
	echo "  up          Build and start all services"
	echo "  down        Stop and remove containers"
	echo "  restart     Stop, rebuild, and start"
	echo "  logs        Show logs for all services"
	echo "  logs-app    Show logs for haive app only"
	echo "  shell       Open bash shell in haive container"
	echo "  clean       Clean Docker system (remove unused containers/images)"
	echo "  prune       Aggressive cleanup including build cache"
	echo "  status      Show container status"
	echo "  help        Show this help"
	echo ""
}

function docker_build() {
	echo "🔨 Building Docker containers..."
	docker compose -f "${COMPOSE_FILE}" build
}

function docker_up() {
	echo "🚀 Starting Haive services..."
	docker compose -f "${COMPOSE_FILE}" up --build -d
	echo "✅ Services started!"
	echo "📱 App: http://localhost:8000"
	echo "🗄️  Database Studio: http://localhost:54323"
}

function docker_down() {
	echo "🛑 Stopping services..."
	docker compose -f "${COMPOSE_FILE}" down
}

function docker_restart() {
	echo "🔄 Restarting services..."
	docker_down
	docker_up
}

function docker_logs() {
	docker compose -f "${COMPOSE_FILE}" logs -f
}

function docker_logs_app() {
	docker compose -f "${COMPOSE_FILE}" logs -f haive
}

function docker_shell() {
	docker compose -f "${COMPOSE_FILE}" exec haive bash
}

function docker_clean() {
	echo "🧹 Cleaning Docker system..."
	docker system prune -f
}

function docker_prune() {
	echo "🧹 Aggressive Docker cleanup..."
	docker system prune -af --volumes
}

function docker_status() {
	docker compose -f "${COMPOSE_FILE}" ps
}

# Main command handler
case "${1:-help}" in
"build")
	docker_build
	;;
"up")
	docker_up
	;;
"down")
	docker_down
	;;
"restart")
	docker_restart
	;;
"logs")
	docker_logs
	;;
"logs-app")
	docker_logs_app
	;;
"shell")
	docker_shell
	;;
"clean")
	docker_clean
	;;
"prune")
	docker_prune
	;;
"status")
	docker_status
	;;
"help" | *)
	show_help
	;;
esac
