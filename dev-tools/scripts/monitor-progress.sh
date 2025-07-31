#!/bin/bash
# 📊 Progress Monitor - Real-time Package Health Dashboard
# Usage: ./dev-tools/scripts/monitor-progress.sh [--watch]

set -e

WATCH_MODE=${1:-""}

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Package directories
PACKAGES=("haive-games" "haive-dataflow" "haive-mcp" "haive-agents" "haive-core")

# Function to get error count for a package
get_error_count() {
	local package=$1
	local src_dir="packages/${package}/src"

	if [[ -d "${src_dir}" ]]; then
		cd "packages/${package}"
		local errors=$(poetry run ruff check src/ --statistics 2>/dev/null | grep "Found" | grep -o '[0-9]*' | head -1 || echo "0")
		cd - >/dev/null
		echo "${errors}"
	else
		echo "N/A"
	fi
}

# Function to get specific error types
get_error_breakdown() {
	local package=$1
	local src_dir="packages/${package}/src"

	if [[ -d "${src_dir}" ]]; then
		cd "packages/${package}"

		local prints=$(poetry run ruff check src/ --select T201 2>/dev/null | wc -l || echo "0")
		local f_strings=$(poetry run ruff check src/ --select G004 2>/dev/null | wc -l || echo "0")
		local imports=$(poetry run ruff check src/ --select I001,F401 2>/dev/null | wc -l || echo "0")
		local docstrings=$(poetry run ruff check src/ --select D101,D102 2>/dev/null | wc -l || echo "0")
		local modernize=$(poetry run ruff check src/ --select UP006,UP007,UP035 2>/dev/null | wc -l || echo "0")

		cd - >/dev/null
		echo "${prints},${f_strings},${imports},${docstrings},${modernize}"
	else
		echo "0,0,0,0,0"
	fi
}

# Function to calculate improvement percentage
calculate_improvement() {
	local before=$1
	local after=$2

	if [[ "${before}" -eq 0 ]]; then
		echo "100"
	else
		echo $(((before - after) * 100 / before))
	fi
}

# Function to get git stash count (safety checkpoints)
get_stash_count() {
	git stash list | grep "SAFETY_CHECKPOINT\|TASKIPY_CHECKPOINT" | wc -l
}

# Function to display dashboard
display_dashboard() {
	clear
	echo -e "${CYAN}╔══════════════════════════════════════════════════════════════════╗${NC}"
	echo -e "${CYAN}║                    📊 HAIVE PROJECT HEALTH DASHBOARD              ║${NC}"
	echo -e "${CYAN}╚══════════════════════════════════════════════════════════════════╝${NC}"
	echo ""

	# Header
	printf "%-15s %-8s %-8s %-8s %-8s %-8s %-8s %-10s\n" \
		"PACKAGE" "TOTAL" "PRINTS" "LOGS" "IMPORTS" "DOCS" "MODERN" "STATUS"
	echo "────────────────────────────────────────────────────────────────────────────"

	local total_errors=0
	local total_packages=0

	for package in "${PACKAGES[@]}"; do
		if [[ -d "packages/${package}" ]]; then
			local errors=$(get_error_count "${package}")
			local breakdown=$(get_error_breakdown "${package}")

			IFS=',' read -r prints f_strings imports docstrings modernize <<<"${breakdown}"

			# Determine status color
			local status_color=${RED}
			local status="🚨 NEEDS WORK"

			if [[ "${errors}" != "N/A" ]]; then
				total_errors=$((total_errors + errors))
				total_packages=$((total_packages + 1))

				if [[ "${errors}" -lt 100 ]]; then
					status_color=${GREEN}
					status="✅ EXCELLENT"
				elif [[ "${errors}" -lt 500 ]]; then
					status_color=${YELLOW}
					status="⚠️ GOOD"
				elif [[ "${errors}" -lt 1000 ]]; then
					status_color=${RED}
					status="🔧 NEEDS WORK"
				else
					status_color=${PURPLE}
					status="🚨 CRITICAL"
				fi
			fi

			printf "%-15s %-8s %-8s %-8s %-8s %-8s %-8s " \
				"${package}" "${errors}" "${prints}" "${f_strings}" "${imports}" "${docstrings}" "${modernize}"
			echo -e "${status_color}${status}${NC}"
		fi
	done

	echo "────────────────────────────────────────────────────────────────────────────"

	# Summary statistics
	local avg_errors=0
	if [[ "${total_packages}" -gt 0 ]]; then
		avg_errors=$((total_errors / total_packages))
	fi

	echo ""
	echo -e "${BLUE}📈 SUMMARY STATISTICS:${NC}"
	echo "  🎯 Total Error$$$${: $}tot}al_}err}ors acro$$$$${${ }}$to}tal}_pa}cka}ges packages"
	echo "  📊 Average Errors per Packag$$$${${${}} $a}vg_}err}ors"
	echo "  🛡️ Safety Checkpoints Available: $(get_stash_count)"
	echo ""

	# Recommendations
	echo -e "${YELLOW}🚀 QUICK ACTIONS:${NC}"
	for package in "${PACKAGES[@]}"; do
		if [[ -d "packages/${package}" ]]; then
			local errors=$(get_error_count "${package}")
			if [[ "${errors}" != "N/A" ]] && [[ "${errors}" -gt 500 ]]; then
				echo "  💡 task fix-${package//-/} - F$${x $}err}ors errors $$${${${${}} $p}ack}age"
			fi
		fi
	done

	echo ""
	echo -e "${GREEN}💪 POWER COMMANDS:${NC}"
	echo "  🚀 task nuclear-fix     - Fix ALL packages at once"
	echo "  🎯 task safe-experiment - Quick fixes with rollback option"
	echo "  📊 task check-stats     - Detailed error analysis"

	echo ""
	echo -e "${CYAN}Last updated: $(date)${NC}"

	if [[ "${WATCH_MODE}" = "--watch" ]]; then
		echo ""
		echo -e "${YELLOW}⏱️ Watching for changes... (Ctrl+C to exit)${NC}"
	fi
}

# Main execution
if [[ "${WATCH_MODE}" = "--watch" ]]; then
	# Watch mode - update every 30 seconds
	while true; do
		display_dashboard
		sleep 30
	done
else
	# Single run
	display_dashboard
fi
