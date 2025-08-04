#!/bin/bash
# 🔄 Sync Package Configurations - Ensure consistent import management across all packages
# Usage: ./dev-tools/scripts/sync-package-configs.sh [--fix|--preview]

set -e

MODE=${1:-"--preview"}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m'

echo -e "${CYAN}🔄 PACKAGE CONFIGURATION SYNC - POLY REPO${NC}"
echo -e "${BLUE}🔧 Mod$${:} $M}ODE${NC}"
echo ""

# Define packages to sync
PACKAGES=(
	"packages/haive-core"
	"packages/haive-agents"
	"packages/haive-tools"
	"packages/haive-games"
	"packages/haive-dataflow"
	"packages/haive-mcp"
)

# Standard ruff configuration for all packages
RUFF_CONFIG='
# Ruff configuration for linting and formatting
[tool.ruff]
target-version = "py312"
line-length = 88

[tool.ruff.lint]
select = [
    "E", "W",      # pycodestyle errors and warnings
    "F",           # Pyflakes
    "I",           # isort
    "B",           # flake8-bugbear
    "C4",          # flake8-comprehensions
    "UP",          # pyupgrade
    "TID251",      # Banned relative imports -> absolute imports
    "TID252",      # Relative imports from parent modules
]
ignore = ["E501", "D100", "D104", "D107", "D203", "D213"]

[tool.ruff.lint.isort]
known-first-party = ["haive"]
force-sort-within-sections = true
lines-after-imports = 2

# AutoImport Configuration for Namespaced Poly Repo
[tool.autoimport]
disable_move_to_top = false
force_absolute_imports = true

exclude_dirs = [
    "docs",
    "tests/fixtures",
    "build",
    ".git",
    "__pycache__",
    ".trunk",
    ".cache"
]

[tool.autoimport.common_statements]
# Core haive imports
"haive.core" = "from haive import core"
"haive.agents" = "from haive import agents"
"haive.tools" = "from haive import tools"
"haive.games" = "from haive import games"
"haive.dataflow" = "from haive import dataflow"
"haive.mcp" = "from haive import mcp"

# Common Python patterns
"Path" = "from pathlib import Path"
"Optional" = "from typing import Optional"
"Union" = "from typing import Union"
"List" = "from typing import List"
"Dict" = "from typing import Dict"
"Any" = "from typing import Any"
"BaseModel" = "from pydantic import BaseModel"
"Field" = "from pydantic import Field"'

# Safety checkpoint
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
git stash push -m "CONFIG_SYNC_CHECKPOINT_${TIMESTAMP}" || echo "⚠️ No changes to stash"

echo -e "${PURPLE}🔍 ANALYZING PACKAGE CONFIGURATIONS...${NC}"
echo ""

# Check current status
for package in "${PACKAGES[@]}"; do
	if [[ -d "${package}" ]]; then
		CONFIG_FILE="${package}/pyproject.toml"
		if [[ -f "${CONFIG_FILE}" ]]; then
			HAS_RUFF=$(grep -q '\[tool\.ruff\]' "${CONFIG_FILE}" && echo "✅" || echo "❌")
			HAS_ISORT=$(grep -q '\[tool\.ruff\.lint\.isort\]' "${CONFIG_FILE}" && echo "✅" || echo "❌")
			HAS_TID251=$(grep -q "TID251" "${CONFIG_FILE}" && echo "✅" || echo "❌")
			HAS_AUTOIMPORT=$(grep -q '\[tool\.autoimport\]' "${CONFIG_FILE}" && echo "✅" || echo "❌")

			echo -e "${BLUE}📦 $(basena"${e $p}ack"age):${NC}"
			echo "  Ruff config: ${HAS_RUFF}"
			echo "  Import rules: ${HAS_ISORT}"
			echo "  Absolute imports (TID251): ${HAS_TID251}"
			echo "  AutoImport config: ${HAS_AUTOIMPORT}"
			echo ""
		else
			echo -e "${RED}❌ $(basenam"${ $pac}ka"ge): No pyproject.toml found${NC}"
			echo ""
		fi
	fi
done

if [[ "${MODE}" = "--fix" ]]; then
	echo -e "${PURPLE}🔧 APPLYING CONFIGURATION SYNC...${NC}"
	echo ""

	for package in "${PACKAGES[@]}"; do
		if [[ -d "${package}" ]]; then
			CONFIG_FILE="${package}/pyproject.toml"
			if [[ -f "${CONFIG_FILE}" ]]; then
				echo -e "${BLUE}🔄 Syncing $(basena"${e $p}ack"age)...${NC}"

				# Check if ruff config already exists
				if grep -q '\[tool\.ruff\]' "${CONFIG_FILE}"; then
					echo "  ⚠️ Ruff config exists, updating..."
					# Remove existing ruff sections to avoid conflicts
					python3 -c "
import re
import sys

with open('${CONFIG_FILE}', 'r') as f:
    content = f.read()

# Remove existing ruff and autoimport sections
content = re.sub(r'\\n\\[tool\\.ruff\\].*?(?=\\n\\[|$)', '', content, flags=re.DOTALL)
content = re.sub(r'\\n\\[tool\\.autoimport\\].*?(?=\\n\\[|$)', '', content, flags=re.DOTALL)

# Add new config at the end
content = content.rstrip() + '''
${RUFF_CONFIG}
'''

with open('${CONFIG_FILE}', 'w') as f:
    f.write(content)
"
				else
					echo "  ✅ Adding ruff config..."
					# Append ruff config to end of file
					echo "${RUFF_CONFIG}" >>"${CONFIG_FILE}"
				fi

				echo "  ✅ Configuration synced"
				echo ""
			fi
		fi
	done

	echo -e "${GREEN}🎉 CONFIGURATION SYNC COMPLETE!${NC}"
	echo ""
	echo -e "${YELLOW}📊 RESULTS:${NC}"
	echo "  • ✅ Synchronized ruff configuration across all packages"
	echo "  • ✅ Added TID251/TID252 rules for absolute import enforcement"
	echo "  • ✅ Configured autoimport for haive namespace"
	echo "  • ✅ Standardized isort settings"
	echo ""
	echo -e "${BLUE}🔍 Next steps:${NC}"
	echo "  1. Run 'task check-imports' to see import violations"
	echo "  2. Run 'task fix-imports-mcp' to fix haive-mcp imports"
	echo "  3. Run 'task fix-imports-dataflow' to fix haive-dataflow imports"
	echo ""

elif [[ "${MODE}" = "--preview" ]]; then
	echo -e "${YELLOW}👀 PREVIEW MODE - Would apply the following changes:${NC}"
	echo ""
	echo -e "${CYAN}🔧 CONFIGURATION TO APPLY TO ALL PACKAGES:${NC}"
	echo "  • ✅ Ruff linting with import enforcement"
	echo "  • ✅ TID251/TID252 rules for absolute imports"
	echo "  • ✅ AutoImport with haive namespace awareness"
	echo "  • ✅ Consistent isort configuration"
	echo "  • ✅ Standard line length (88 characters)"
	echo ""
	echo -e "${GREEN}Run with --fix to apply these changes${NC}"
fi

echo ""
echo -e "${CYAN}🚀 Package Configuration Sync Complete!${NC}"
echo -e "${BLUE}💡 All packages will have consistent import management${NC}"
