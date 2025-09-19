#!/bin/bash
# Build versioned documentation for all packages
# Creates versioned folders in central docs/ location
# Usage: ./scripts/build_versioned_docs.sh [version] [--concurrent]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
VERSION=""
CONCURRENT=false
MAX_JOBS=4
DOCS_ROOT="docs"
BUILD_LOG="build_versioned_docs.log"

# Parse arguments
while [[ $# -gt 0 ]]; do
	case $1 in
	--concurrent)
		CONCURRENT=true
		shift
		;;
	--jobs)
		MAX_JOBS="$2"
		shift 2
		;;
	--help | -h)
		echo "Usage: $0 [version] [--concurrent] [--jobs N]"
		echo ""
		echo "Options:"
		echo "  version        Git tag version (e.g., v0.2.1). If not provided, uses latest git tag"
		echo "  --concurrent   Build packages in parallel (default: sequential)"
		echo "  --jobs N       Max parallel jobs when concurrent (default: 4)"
		echo "  --help         Show this help"
		echo ""
		echo "Examples:"
		echo "  $0                    # Build latest version sequentially"
		echo "  $0 v0.2.1            # Build specific version"
		echo "  $0 --concurrent      # Build latest version with parallel builds"
		echo "  $0 v0.1.0 --concurrent --jobs 2"
		exit 0
		;;
	*)
		if [[ -z $VERSION ]]; then
			VERSION="$1"
		else
			echo -e "${RED}❌ Unknown argument: $1${NC}"
			exit 1
		fi
		shift
		;;
	esac
done

# Functions
log() {
	echo -e "$1" | tee -a "$BUILD_LOG"
}

detect_version() {
	if [[ -z $VERSION ]]; then
		VERSION=$(git tag --list | sort -V | tail -1)
		if [[ -z $VERSION ]]; then
			log "${RED}❌ No git tags found. Please create a tag first: git tag v0.1.0${NC}"
			exit 1
		fi
		log "${BLUE}📋 Auto-detected version: $VERSION${NC}"
	else
		# Verify the version exists as a git tag
		if ! git tag --list | grep -q "^$VERSION$"; then
			log "${RED}❌ Version $VERSION not found in git tags${NC}"
			log "${YELLOW}💡 Available tags: $(git tag --list | tr '\n' ' ')${NC}"
			exit 1
		fi
		log "${BLUE}📋 Using specified version: $VERSION${NC}"
	fi
}

setup_directories() {
	log "${BLUE}📁 Setting up directory structure...${NC}"

	# Create main docs structure
	mkdir -p "$DOCS_ROOT/versions/$VERSION"
	mkdir -p "$DOCS_ROOT/assets"

	# Create latest symlink
	if [[ -L "$DOCS_ROOT/latest" ]]; then
		rm "$DOCS_ROOT/latest"
	fi
	ln -sf "versions/$VERSION" "$DOCS_ROOT/latest"

	log "${GREEN}✅ Directory structure created${NC}"
	log "   📂 $DOCS_ROOT/versions/$VERSION/"
	log "   🔗 $DOCS_ROOT/latest -> versions/$VERSION"
}

get_packages() {
	# Get all package directories
	find packages -name "haive-*" -type d -maxdepth 1 | sort
}

build_package() {
	local package_path=$1
	local package_name=$(basename "$package_path")
	local log_file="$DOCS_ROOT/versions/$VERSION/${package_name}_build.log"

	log "${BLUE}🔨 Building $package_name...${NC}"

	# Check if package has docs
	if [[ ! -d "$package_path/docs" ]]; then
		log "${YELLOW}⚠️  $package_name: No docs directory found, skipping${NC}"
		return 0
	fi

	# Build the package documentation
	(
		cd "$package_path/docs"

		# Clean previous build
		if [[ -d "build" ]]; then
			rm -rf build/*
		fi

		# Build with timeout
		timeout 600 poetry run sphinx-build -b html source build/html 2>&1 | tee "$log_file"

		if [[ ${PIPESTATUS[0]} -eq 0 ]]; then
			# Copy to versioned location
			target_dir="../../$DOCS_ROOT/versions/$VERSION/$package_name"
			mkdir -p "$target_dir"
			cp -r build/html/* "$target_dir/"

			# Get build stats
			build_size=$(du -sh "$target_dir" | cut -f1)
			html_count=$(find "$target_dir" -name "*.html" | wc -l)

			log "${GREEN}✅ $package_name: Built successfully${NC}"
			log "   📏 Size: $build_size"
			log "   📄 HTML files: $html_count"

			return 0
		else
			log "${RED}❌ $package_name: Build failed${NC}"
			return 1
		fi
	)
}

build_sequential() {
	local packages=($(get_packages))
	local total=${#packages[@]}
	local current=1
	local failed_packages=()

	log "${BLUE}🚀 Building $total packages sequentially...${NC}"

	for package_path in "${packages[@]}"; do
		local package_name=$(basename "$package_path")

		log ""
		log "=================================================================================="
		log "${BLUE}📦 Building $package_name ($current/$total)${NC}"
		log "=================================================================================="

		if build_package "$package_path"; then
			log "${GREEN}✅ $package_name completed${NC}"
		else
			log "${RED}❌ $package_name failed${NC}"
			failed_packages+=("$package_name")
		fi

		# Wait between builds to manage resources
		if [[ $current -lt $total ]]; then
			log "${YELLOW}⏸️  Waiting 3 seconds before next build...${NC}"
			sleep 3
		fi

		current=$((current + 1))
	done

	return ${#failed_packages[@]}
}

build_concurrent() {
	local packages=($(get_packages))
	local total=${#packages[@]}
	local failed_packages=()

	log "${BLUE}🚀 Building $total packages concurrently (max $MAX_JOBS jobs)...${NC}"

	# Create job control
	local job_count=0
	local pids=()

	for package_path in "${packages[@]}"; do
		local package_name=$(basename "$package_path")

		# Wait if we've reached max jobs
		while [[ $job_count -ge $MAX_JOBS ]]; do
			wait -n # Wait for any job to complete
			job_count=$((job_count - 1))
		done

		# Start build in background
		(
			if build_package "$package_path"; then
				echo "$package_name:SUCCESS" >>"$DOCS_ROOT/versions/$VERSION/build_results.tmp"
			else
				echo "$package_name:FAILED" >>"$DOCS_ROOT/versions/$VERSION/build_results.tmp"
			fi
		) &

		pids+=($!)
		job_count=$((job_count + 1))

		log "${BLUE}🏃 Started $package_name (job $job_count/$MAX_JOBS)${NC}"
	done

	# Wait for all jobs to complete
	log "${YELLOW}⏳ Waiting for all builds to complete...${NC}"
	wait

	# Check results
	if [[ -f "$DOCS_ROOT/versions/$VERSION/build_results.tmp" ]]; then
		while IFS=: read -r package status; do
			if [[ $status == "FAILED" ]]; then
				failed_packages+=("$package")
			fi
		done <"$DOCS_ROOT/versions/$VERSION/build_results.tmp"
		rm "$DOCS_ROOT/versions/$VERSION/build_results.tmp"
	fi

	return ${#failed_packages[@]}
}

create_version_index() {
	log "${BLUE}📄 Creating version index...${NC}"

	local index_file="$DOCS_ROOT/index.html"

	cat >"$index_file" <<'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Haive Documentation</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif; margin: 40px auto; max-width: 800px; line-height: 1.6; color: #333; }
        .header { text-align: center; margin-bottom: 40px; }
        .version-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px 0; }
        .version-card { border: 1px solid #ddd; border-radius: 8px; padding: 20px; transition: box-shadow 0.2s; }
        .version-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        .version-title { font-size: 1.2em; font-weight: bold; color: #2563eb; margin-bottom: 10px; }
        .package-list { list-style: none; padding: 0; }
        .package-list li { margin: 5px 0; }
        .package-list a { color: #059669; text-decoration: none; }
        .package-list a:hover { text-decoration: underline; }
        .latest-badge { background: #10b981; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.8em; margin-left: 8px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 Haive Framework Documentation</h1>
        <p>AI Agent Framework with Dynamic Tool Integration</p>
    </div>

    <div class="version-grid">
EOF

	# Add version cards
	for version_dir in $(ls -1d "$DOCS_ROOT/versions"/*/ 2>/dev/null | sort -Vr); do
		local version=$(basename "$version_dir")
		local is_latest=""

		# Check if this is the latest version
		if [[ "$(readlink "$DOCS_ROOT/latest")" == "versions/$version" ]]; then
			is_latest='<span class="latest-badge">Latest</span>'
		fi

		cat >>"$index_file" <<EOF
        <div class="version-card">
            <div class="version-title">$version $is_latest</div>
            <ul class="package-list">
EOF

		# Add package links
		for package_dir in $(ls -1d "$version_dir"/*/ 2>/dev/null | sort); do
			local package=$(basename "$package_dir")
			if [[ -f "$package_dir/index.html" ]]; then
				cat >>"$index_file" <<EOF
                <li><a href="versions/$version/$package/">📦 $package</a></li>
EOF
			fi
		done

		cat >>"$index_file" <<EOF
            </ul>
        </div>
EOF
	done

	cat >>"$index_file" <<'EOF'
    </div>

    <div style="text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; color: #666;">
        <p>🔗 <a href="latest/">Latest Documentation</a> | 📧 <a href="mailto:william.astley@algebraicwealth.com">Contact</a></p>
        <p style="font-size: 0.9em;">Built with ❤️ using Sphinx</p>
    </div>
</body>
</html>
EOF

	log "${GREEN}✅ Version index created: $index_file${NC}"
}

# Main execution
main() {
	# Initialize log
	echo "🚀 Haive Versioned Documentation Build" >"$BUILD_LOG"
	echo "⏰ Started: $(date)" >>"$BUILD_LOG"
	echo "===========================================" >>"$BUILD_LOG"

	log "${BLUE}🚀 Haive Versioned Documentation Build${NC}"
	log "${BLUE}⏰ Started: $(date)${NC}"
	log ""

	# Detect version
	detect_version

	# Setup directories
	setup_directories

	# Build packages
	local failed_count
	if [[ $CONCURRENT == "true" ]]; then
		build_concurrent
		failed_count=$?
	else
		build_sequential
		failed_count=$?
	fi

	# Create version index
	create_version_index

	# Final summary
	log ""
	log "=================================================================================="
	if [[ $failed_count -eq 0 ]]; then
		log "${GREEN}🎉 All packages built successfully!${NC}"
	else
		log "${YELLOW}⚠️  Build completed with $failed_count failures${NC}"
	fi
	log "${BLUE}📍 Documentation available at: $DOCS_ROOT/index.html${NC}"
	log "${BLUE}🔗 Latest docs: $DOCS_ROOT/latest/${NC}"
	log "${BLUE}⏰ Finished: $(date)${NC}"
	log "=================================================================================="

	# Show directory structure
	log ""
	log "${BLUE}📁 Directory structure:${NC}"
	tree "$DOCS_ROOT" -L 3 2>/dev/null || find "$DOCS_ROOT" -type d | head -20

	# Server instructions
	log ""
	log "${BLUE}🌐 To view documentation:${NC}"
	log "   cd $DOCS_ROOT && python -m http.server 8002"
	log "   Then open: http://localhost:8002"

	return $failed_count
}

# Run main function
main "$@"
