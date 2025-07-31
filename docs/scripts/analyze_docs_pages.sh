#!/bin/bash
# Analyze documentation pages - errors, warnings, and areas with problems

# Find the most recent log file
LOG_FILE=${1:-$(ls -t docs/logs/fast_build_*.log 2>/dev/null | head -1)}

if [[ -z "${LOG_FILE}" ]]; then
	echo "❌ No build log found"
	echo "Usage: $0 [log_file]"
	exit 1
fi

echo "📊 Analyzin${: $LOG_F}ILE"
echo "="$(printf '%.0s=' {1..80})

# Function to analyze errors by area/page
analyze_errors_by_area() {
	echo -e "\n❌ ERRORS BY AREA/PAGE:"
	echo "======================"

	# Create temporary file for context analysis
	local temp_file=$(mktemp)

	# Extract error lines with context
	grep -n -B3 -A1 "ERROR\|ImportError\|failed to import\|cannot import\|ModuleNotFoundError" "${LOG_FILE}" >"${temp_file}"

	echo -e "\n📍 IMPORT ERRORS:"
	echo "------------------"
	while IFS= read -r line; do
		if [[ ${line} =~ ImportError|ModuleNotFoundError|cannot\ import|failed\ to\ import ]]; then
			# Find the page context (look back for reading sources line)
			local line_num=$(echo "${line}" | cut -d: -f1)
			local page_context=$(grep -B5 "^${line_num}:" "${temp_file}" | grep "reading sources" | tail -1)

			if [[ -n "${page_context}" ]]; then
				local page_name=$(echo "${page_context}" | sed -E 's/.*\] (.*)/\1/')
				echo "  �${� $page_n}ame"
				echo "     $(echo "${line}" | cut -d: -f2- | xargs)"
			else
				echo "  🔴 Unknown context"
				echo "     $(echo "${line}" | cut -d: -f2- | xargs)"
			fi
			echo ""
		fi
	done <"${temp_file}"

	echo -e "\n📍 OTHER ERRORS:"
	echo "----------------"
	grep -v "ImportError\|ModuleNotFoundError\|cannot import\|failed to import" "${temp_file}" |
		grep -E "ERROR|error:" | head -10 | while IFS= read -r line; do
		echo "  🔴 $(ech${ "$l}ine" | cut -d: -f2- | xargs)"
	done

	rm "${temp_file}"
}

# Function to analyze warnings by area
analyze_warnings_by_area() {
	echo -e "\n⚠️  WARNINGS BY AREA/PAGE:"
	echo "========================="

	# Count and categorize warnings
	local warning_temp=$(mktemp)
	grep -n -B2 -A1 "WARNING" "${LOG_FILE}" >"${warning_temp}"

	echo -e "\n📍 WARNING CATEGORIES:"
	echo "--------------------"

	# Extension warnings
	local ext_warnings=$(grep -c "extension.*has no setup" "${warning_temp}" 2>/dev/null || echo 0)
	echo "Extension setup warnings: ${ext_warnings}"

	# Import warnings
	local import_warnings=$(grep -c "failed to import" "${warning_temp}" 2>/dev/null || echo 0)
	echo "Import warnings: ${import_warnings}"

	# Viewcode warnings
	local viewcode_warnings=$(grep -c "viewcode" "${warning_temp}" 2>/dev/null || echo 0)
	echo "Viewcode warnings: ${viewcode_warnings}"

	# Configuration warnings
	local config_warnings=$(grep -c "configuration.*changed" "${warning_temp}" 2>/dev/null || echo 0)
	echo "Configuration warnings: ${config_warnings}"

	echo -e "\n📍 WARNINGS BY PAGE AREA:"
	echo "------------------------"

	# Extract warnings with page context
	while IFS= read -r line; do
		if [[ ${line} =~ WARNING ]]; then
			local line_num=$(echo "${line}" | cut -d: -f1)
			local page_context=$(grep -B3 "^${line_num}:" "${warning_temp}" | grep "reading sources\|writing output" | tail -1)

			if [[ -n "${page_context}" ]]; then
				local page_name=$(echo "${page_context}" | sed -E 's/.*\] (.*)/\1/' | sed 's/\.\.\.//')
				local warning_text=$(echo "${line}" | cut -d: -f2- | xargs)
				echo "  ⚠�${�  $page_}name: ${warning_text:0:60}..."
			fi
		fi
	done <"${warning_temp}" | sort | uniq -c | sort -rn | head -20

	rm "${warning_temp}"
}

# Function to analyze pages with most problems
analyze_problem_pages() {
	echo -e "\n🚨 PAGES WITH MOST PROBLEMS:"
	echo "==========================="

	# Create a comprehensive analysis
	local problem_temp=$(mktemp)

	# Get all error and warning lines with context
	grep -n -B5 -A1 "ERROR\|WARNING\|ImportError\|failed to import" "${LOG_FILE}" >"${problem_temp}"

	# Extract page names and count problems
	echo -e "\n📊 PROBLEM COUNT BY PAGE:"
	echo "------------------------"

	grep "reading sources\|writing output" "${problem_temp}" |
		sed -E 's/.*\] (.*)/\1/' |
		sed 's/\.\.\.//' |
		sort | uniq -c | sort -rn | head -20 |
		while read count page; do
			printf "%3d problems: %s\n" "${count}" "${page}"
		done

	rm "${problem_temp}"
}

# Function to show build progress and page statistics
show_page_statistics() {
	echo -e "\n📄 PAGE PROCESSING STATISTICS:"
	echo "=============================="

	local total_pages=$(grep -c "reading sources\|writing output" "${LOG_FILE}" 2>/dev/null || echo 0)
	local reading_pages=$(grep -c "reading sources" "${LOG_FILE}" 2>/dev/null || echo 0)
	local writing_pages=$(grep -c "writing output" "${LOG_FILE}" 2>/dev/null || echo 0)

	echo "Total pages processed: ${total_pages}"
	echo "Pages read: ${reading_pages}"
	echo "Pages written: ${writing_pages}"

	# Package breakdown
	echo -e "\n📦 PAGES BY PACKAGE:"
	echo "------------------"
	for package in haive-core haive-agents haive-tools haive-games haive-dataflow haive-mcp; do
		local count=$(grep -c "reading sources.*${package}\|writing output.*${package}" "${LOG_FILE}" 2>/dev/null || echo 0)
		printf "%-15s: %4d pages\n" "${package}" "${count}"
	done

	# Current status
	echo -e "\n📍 CURRENT STATUS:"
	echo "-----------------"
	local last_page=$(grep -E "reading sources|writing output|building \[" "${LOG_FILE}" | tail -1)
	local percent=$(echo "${last_page}" | grep -oE '\[ *[0-9]+%' | grep -oE '[0-9]+')

	if [[ -n "${percent}" ]]; then
		echo "Progress: ${percent}%"
	fi
	if [[ -n "${last_page}" ]]; then
		echo "Current: ${last_page:0:100}..."
	fi
}

# Run all analyses
show_page_statistics
analyze_errors_by_area
analyze_warnings_by_area
analyze_problem_pages

echo -e "\n💡 TIPS:"
echo "======="
echo "• Use 'grep -n \"page_name\${ $LOG_FI}LE' to find specific pages"
echo "• Use 'grep -A5 -B5 \"error_text\${ $LOG_FI}LE' for error context"
echo "• Use './scripts/monitor_docs_build.sh --watch' for live monitoring"
