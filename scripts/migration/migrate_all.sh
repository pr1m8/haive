# scripts/migration/migrate_all.sh
#!/bin/bash
# Master migration script

set -e # Exit on any error

# Configuration
COMPONENTS=(
	# Core infrastructure
	"core:haive-core"

	# Agents groups
	"agents/simple:haive-agents"
	"agents/react:haive-agents"
	"agents/rag:haive-agents"
	"agents/planning:haive-agents"
	"agents/reasoning_and_critique:haive-agents"
	"agents/document_agents:haive-agents"
	"agents/research:haive-agents"
	"agents/supervisor:haive-agents"
	"agents/web_nav:haive-agents"
	"agents/coding:haive-agents"

	# Games
	"games:haive-games"
	"games/framework:haive-games"

	# Tools
	"tak:haive-tools"

	# Prebuilt agents
	"prebuilt/simple:haive-prebuilt"
	"prebuilt/react:haive-prebuilt"
	"prebuilt/misc:haive-prebuilt"

	# Dataflow
	"dataflow:haive-dataflow"
	"dataflow/registry:haive-dataflow"
	"dataflow/api:haive-dataflow"
)

# Create main directory structure
mkdir -p packages
for pkg in "haive-core" "haive-agents" "haive-games" "haive-tools" "haive-prebuilt" "haive-dataflow"; do
	mkdir -p "packages/${pkg}/src/${pkg//-/_}"
	mkdir -p "packages/${pkg}/tests"
	mkdir -p "packages/${pkg}/docs"
	echo "Created package structure for ${pkg}"
done

# Create backup
./scripts/migration/backup_codebase.sh

# Migrate each component
for comp in "${COMPONENTS[@]}"; do
	src=$(echo "${comp}" | cut -d: -f1)
	pkg=$(echo "${comp}" | cut -d: -f2)
	echo "=== Migrating ${src} to ${pkg} ==="
	./scripts/migration/auto_migrate.sh "${src}" "${pkg}"

	# Detect system dependencies
	./scripts/migration/detect_system_deps.sh "packages/${pkg}"

	# Generate setup.py for setuptools compatibility
	python3 ./scripts/migration/generate_setup.py "packages/${pkg}/pyproject.toml"

	echo
done

# Run deep import refactoring on all packages
echo "Running deep import refactoring..."
for pkg in "haive-core" "haive-agents" "haive-games" "haive-tools" "haive-prebuilt" "haive-dataflow"; do
	python3 ./scripts/migration/deep_import_refactor.py "packages/${pkg}"
done

# Create workspace pyproject.toml for development
cat >"packages/pyproject.toml" <<EOF
[tool.poetry]
name = "haive-workspace"
version = "0.1.0"
description = "Workspace for Haive packages"
authors = ["0rac130fD31phi <william.astley@algebraicwealth.com>"]
license = "MIT"

[tool.poetry.dependencies]
python = ">=3.12,<3.13"
haive-core = {path = "./haive-core", develop = true}
haive-agents = {path = "./haive-agents", develop = true}
haive-games = {path = "./haive-games", develop = true}
haive-tools = {path = "./haive-tools", develop = true}
haive-prebuilt = {path = "./haive-prebuilt", develop = true}
haive-dataflow = {path = "./haive-dataflow", develop = true}

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
EOF

echo "Migration complete. Making scripts executable..."

# Make all scripts executable
chmod +x scripts/migration/*.sh

echo "Migration workflow completed."
echo
echo "To set up Git submodules:"
echo "./scripts/migration/setup_submodules.sh"
echo
echo "To install the workspace and all packages in development mode:"
echo "cd packages && poetry install"
echo
echo "To run tests for all packages:"
echo "cd packages && poetry run pytest"
