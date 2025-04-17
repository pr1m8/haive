# scripts/migration/auto_migrate.sh
#!/bin/bash
# Automated package migration script

set -e  # Exit on any error

# Configuration
SOURCE_ROOT="src/haive"
PACKAGE_ROOT="packages"
DEFAULT_AUTHOR="0rac130fD31phi <william.astley@algebraicwealth.com>"
DEFAULT_VERSION="0.1.0"
LICENSE="MIT"

# Command line processing
COMPONENT=$1
TARGET_PACKAGE=$2

if [ -z "$COMPONENT" ] || [ -z "$TARGET_PACKAGE" ]; then
    echo "Usage: $0 <component_path> <target_package>"
    echo "Example: $0 core haive-core"
    echo "Example: $0 agents/simple haive-agents"
    exit 1
fi

SOURCE_PATH="${SOURCE_ROOT}/${COMPONENT}"
TARGET_PATH="${PACKAGE_ROOT}/${TARGET_PACKAGE}/src/${TARGET_PACKAGE//-/_}"
COMPONENT_NAME=$(basename "$COMPONENT")

# Check if source exists
if [ ! -d "$SOURCE_PATH" ]; then
    echo "Error: Source path $SOURCE_PATH does not exist"
    exit 1
fi

# Create target directories
mkdir -p "$TARGET_PATH"
mkdir -p "${PACKAGE_ROOT}/${TARGET_PACKAGE}/tests"
mkdir -p "${PACKAGE_ROOT}/${TARGET_PACKAGE}/docs"

echo "Migrating $SOURCE_PATH to $TARGET_PATH"

# Copy files
cp -r "$SOURCE_PATH"/* "$TARGET_PATH"/
echo "Files copied successfully"

# Dependency mapping from the main Poetry file
declare -A DEPENDENCY_MAP
DEPENDENCY_MAP=(
    ["langchain"]="langchain = \\.^0.3.20\\."
    ["langchain_core"]="langchain-core = \\.^0.3.44\\."
    ["langchain_community"]="langchain-community = \\.^0.3.20\\."
    ["langchain_experimental"]="langchain-experimental = \\.^0.3.4\\."
    ["pydantic"]="pydantic = \\.^2.10.6\\."
    ["numpy"]="numpy = \\.^1.24.0\\."
    ["pandas"]="pandas = \\.^2.2.3\\."
    ["matplotlib"]="matplotlib = \\.^3.10.0\\."
    ["networkx"]="networkx = \\.^3.4.2\\."
    ["psycopg"]="psycopg = \\.^3.2.6\\.\\.psycopg-pool = \\.^3.2.6\\."
    ["langgraph"]="langgraph = \\.^0.3.5\\."
    ["faiss"]="faiss-gpu-cu12 = { version = \\.^1.10.0\\., extras = [\\.fix-cuda\\.] }"
    ["anthropic"]="langchain-anthropic = \\.^0.3.10\\."
    ["openai"]="langchain-openai = \\.<=0.3.6\\."
)

# Auto-detect Python dependencies
echo "Detecting dependencies..."
# Look for imports in Python files
IMPORTS=$(grep -r -E "^(import|from) [a-zA-Z0-9_.]+" "$TARGET_PATH" | sed -E 's/^.*?(import|from) ([a-zA-Z0-9_.]+).*/\\./' | sort | uniq)

# Generate dependency list for pyproject.toml
POETRY_DEPS="python = \\.>=3.12,<3.13\\."

for imp in $IMPORTS; do
    # Get the root package name
    ROOT_PKG=$(echo "$imp" | cut -d. -f1)
    
    # Skip standard library and relative imports
    if [[ "$ROOT_PKG" == "os" || "$ROOT_PKG" == "sys" || "$ROOT_PKG" == "typing" || 
          "$ROOT_PKG" == "abc" || "$ROOT_PKG" == "enum" || "$ROOT_PKG" == "json" || 
          "$ROOT_PKG" == "time" || "$ROOT_PKG" == "datetime" || "$ROOT_PKG" == "logging" || 
          "$ROOT_PKG" == "uuid" || "$ROOT_PKG" == "collections" || "$ROOT_PKG" == "functools" ||
          "$ROOT_PKG" == "copy" || "$ROOT_PKG" == "pathlib" || "$ROOT_PKG" == "re" ||
          "$ROOT_PKG" == "." || "$ROOT_PKG" == "src" ]]; then
        continue
    fi
    
    # Check if we have this in our dependency map
    if [[ -n "${DEPENDENCY_MAP[$ROOT_PKG]}" ]]; then
        if [[ ! $POETRY_DEPS =~ $ROOT_PKG ]]; then
            POETRY_DEPS="$POETRY_DEPS\\.${DEPENDENCY_MAP[$ROOT_PKG]}"
        fi
    else
        # For unknown dependencies, add with a wildcard version
        if [[ ! $POETRY_DEPS =~ $ROOT_PKG ]]; then
            # Replace underscores with hyphens for package name
            PKG_NAME=$(echo "$ROOT_PKG" | tr '_' '-')
            POETRY_DEPS="$POETRY_DEPS\\.$PKG_NAME = \\.*\\."
        fi
    fi
done

# Check for haive internal dependencies
if grep -q "from src.haive.core" "$TARGET_PATH"/* 2>/dev/null; then
    POETRY_DEPS="$POETRY_DEPS\\.haive-core = {path = \\.../haive-core\\., develop = true}"
    echo "Detected dependency on haive-core"
fi

if grep -q "from src.haive.agents" "$TARGET_PATH"/* 2>/dev/null; then
    POETRY_DEPS="$POETRY_DEPS\\.haive-agents = {path = \\.../haive-agents\\., develop = true}"
    echo "Detected dependency on haive-agents"
fi

if grep -q "from src.haive.games" "$TARGET_PATH"/* 2>/dev/null; then
    POETRY_DEPS="$POETRY_DEPS\\.haive-games = {path = \\.../haive-games\\., develop = true}"
    echo "Detected dependency on haive-games"
fi

if grep -q "from src.haive.tak" "$TARGET_PATH"/* 2>/dev/null; then
    POETRY_DEPS="$POETRY_DEPS\\.haive-tools = {path = \\.../haive-tools\\., develop = true}"
    echo "Detected dependency on haive-tools"
fi

if grep -q "from src.haive.prebuilt" "$TARGET_PATH"/* 2>/dev/null; then
    POETRY_DEPS="$POETRY_DEPS\\.haive-prebuilt = {path = \\.../haive-prebuilt\\., develop = true}"
    echo "Detected dependency on haive-prebuilt"
fi

if grep -q "from src.haive.dataflow" "$TARGET_PATH"/* 2>/dev/null; then
    POETRY_DEPS="$POETRY_DEPS\\.haive-dataflow = {path = \\.../haive-dataflow\\., develop = true}"
    echo "Detected dependency on haive-dataflow"
fi

# Generate pyproject.toml if it doesn't exist
if [ ! -f "${PACKAGE_ROOT}/${TARGET_PACKAGE}/pyproject.toml" ]; then
    cat > "${PACKAGE_ROOT}/${TARGET_PACKAGE}/pyproject.toml" << EOF
[tool.poetry]
name = "${TARGET_PACKAGE}"
version = "${DEFAULT_VERSION}"
description = "$(echo "$TARGET_PACKAGE" | sed 's/-/ /g') for Haive framework"
authors = ["${DEFAULT_AUTHOR}"]
license = "${LICENSE}"
readme = "README.md"

[tool.poetry.dependencies]
$POETRY_DEPS

[tool.poetry.group.dev.dependencies]
pytest = "^8.3.5"
black = "^25.1.0"
isort = "^6.0.1"
mypy = "^1.15.0"
pre-commit = "^4.1.0"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
EOF
    echo "Generated pyproject.toml"
fi

# Create README.md if it doesn't exist
if [ ! -f "${PACKAGE_ROOT}/${TARGET_PACKAGE}/README.md" ]; then
    cat > "${PACKAGE_ROOT}/${TARGET_PACKAGE}/README.md" << EOF
# ${TARGET_PACKAGE}

$(echo "$TARGET_PACKAGE" | sed 's/-/ /g' | sed -E 's/\\.\\./\\.&/g') for the Haive framework.

## Installation

\\.\\.\\.bash
pip install ${TARGET_PACKAGE}
\\.\\.\\.

## Usage

\\.\\.\\.python
from ${TARGET_PACKAGE//-/_} import *

# Your code here
\\.\\.\\.

## License

MIT
EOF
    echo "Created README.md"
fi

# Create __init__.py if it doesn't exist
if [ ! -f "${TARGET_PATH}/__init__.py" ]; then
    cat > "${TARGET_PATH}/__init__.py" << EOF
"""${TARGET_PACKAGE} package for Haive framework."""

__version__ = "${DEFAULT_VERSION}"
EOF
    echo "Created __init__.py"
fi

# Refactor imports
echo "Refactoring imports..."
python3 - << EOF
import os
import re
from pathlib import Path

def refactor_imports(file_path):
    """Refactor imports in a Python file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Replace imports
    replacements = [
        (r'from src\\.haive\\.core', r'from haive_core'),
        (r'import src\\.haive\\.core', r'import haive_core'),
        (r'from src\\.haive\\.agents', r'from haive_agents'),
        (r'import src\\.haive\\.agents', r'import haive_agents'),
        (r'from src\\.haive\\.games', r'from haive_games'),
        (r'import src\\.haive\\.games', r'import haive_games'),
        (r'from src\\.haive\\.tak', r'from haive_tools'),
        (r'import src\\.haive\\.tak', r'import haive_tools'),
        (r'from src\\.haive\\.prebuilt', r'from haive_prebuilt'),
        (r'import src\\.haive\\.prebuilt', r'import haive_prebuilt'),
        (r'from src\\.haive\\.dataflow', r'from haive_dataflow'),
        (r'import src\\.haive\\.dataflow', r'import haive_dataflow')
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    # For the specific package being migrated, handle relative imports
    target_pkg = "${TARGET_PACKAGE}".replace("-", "_")
    component = "${COMPONENT}".replace("/", ".")
    if component != "core" and component != "agents" and component != "games" and component != "tak" and component != "prebuilt" and component != "dataflow":
        content = re.sub(f'from src\\.haive\\.{component}', f'from {target_pkg}', content)
        content = re.sub(f'import src\\.haive\\.{component}', f'import {target_pkg}', content)
    
    with open(file_path, 'w') as f:
        f.write(content)

# Process all Python files
for path in Path("${TARGET_PATH}").rglob("*.py"):
    refactor_imports(path)
EOF

echo "Creating basic test file..."
mkdir -p "${PACKAGE_ROOT}/${TARGET_PACKAGE}/tests"
cat > "${PACKAGE_ROOT}/${TARGET_PACKAGE}/tests/test_basic.py" << EOF
"""Basic tests for ${TARGET_PACKAGE}."""

import ${TARGET_PACKAGE//-/_}

def test_import():
    """Test that the package can be imported."""
    assert ${TARGET_PACKAGE//-/_}
EOF

echo "Migration of $COMPONENT to $TARGET_PACKAGE complete"
echo "Next steps:"
echo "1. Install the package in development mode: cd ${PACKAGE_ROOT}/${TARGET_PACKAGE} && pip install -e ."
echo "2. Run tests to verify functionality"
echo "3. Check imports and dependencies in pyproject.toml"