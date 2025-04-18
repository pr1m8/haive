# scripts/migration/detect_system_deps.sh
#!/bin/bash
# System dependency detection

set -e # Exit on any error

SOURCE_PATH=$1
if [[ -z ${SOURCE_PATH} ]]; then
	echo "Usage: $0 <source_path>"
	exit 1
fi

echo "Detecting system dependencies in ${SOURCE_PATH}..."

# Look for common indicators of system dependencies
declare -A DETECTED_DEPS

# OpenCV
if grep -r "cv2" "${SOURCE_PATH}" >/dev/null; then
	DETECTED_DEPS["opencv"]="libopencv-dev"
fi

# PyTorch with CUDA
if grep -r "torch.cuda" "${SOURCE_PATH}" >/dev/null; then
	DETECTED_DEPS["cuda"]="cuda-toolkit"
fi

# GraphViz
if grep -r "graphviz" "${SOURCE_PATH}" >/dev/null; then
	DETECTED_DEPS["graphviz"]="graphviz"
fi

# PostgreSQL
if grep -r "psycopg\|psycopg2" "${SOURCE_PATH}" >/dev/null; then
	DETECTED_DEPS["postgresql"]="libpq-dev"
fi

# XML processing
if grep -r "lxml" "${SOURCE_PATH}" >/dev/null; then
	DETECTED_DEPS["lxml"]="libxml2-dev libxslt-dev"
fi

# Image processing
if grep -r "Pillow\|PIL" "${SOURCE_PATH}" >/dev/null; then
	DETECTED_DEPS["pillow"]="libjpeg-dev libpng-dev"
fi

# Output detected dependencies
if [[ ${#DETECTED_DEPS[@]} -gt 0 ]]; then
	echo "Detected system dependencies:"
	for dep in "${!DETECTED_DEPS[@]}"; do
		echo "- ${dep}: ${DETECTED_DEPS[${dep}]}"
	done

	# Create system_requirements.txt file
	echo "# System dependencies detected by automated analysis" >"${SOURCE_PATH}/system_requirements.txt"
	echo "# Install these using your system's package manager" >>"${SOURCE_PATH}/system_requirements.txt"
	echo "" >>"${SOURCE_PATH}/system_requirements.txt"
	echo "## Ubuntu/Debian:" >>"${SOURCE_PATH}/system_requirements.txt"
	echo '# sudo apt-get install \' >>"${SOURCE_PATH}/system_requirements.txt"
	for dep in "${!DETECTED_DEPS[@]}"; do
		echo "#   ${DETECTED_DEPS[${dep}]} \\" >>"${SOURCE_PATH}/system_requirements.txt"
	done

	echo "" >>"${SOURCE_PATH}/system_requirements.txt"
	echo "## macOS:" >>"${SOURCE_PATH}/system_requirements.txt"
	echo '# brew install \' >>"${SOURCE_PATH}/system_requirements.txt"
	for dep in "${!DETECTED_DEPS[@]}"; do
		# Map apt package names to brew package names (simplistic mapping)
		BREW_PKG=$(echo "${DETECTED_DEPS[${dep}]}" | sed 's/lib\(.*\)-dev/\1/g' | sed 's/ lib.*//g')
		echo "#   ${BREW_PKG} \\" >>"${SOURCE_PATH}/system_requirements.txt"
	done

	echo "System requirements written to ${SOURCE_PATH}/system_requirements.txt"
else
	echo "No system dependencies detected."
fi
