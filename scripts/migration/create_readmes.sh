#!/bin/bash

# Script to create README.md files in Haive packages
# Run this from your project root directory

# Define packages within packages/ directory
PACKAGES=(
	"haive-core"
	"haive-agents"
	"haive-dataflow"
	"haive-games"
	"haive-prebuilt"
	"haive-tools"
)

# Function to create a README file
create_readme() {
	local path=$1
	local name=$2

	# Check if README already exists
	if [ -f "$path" ]; then
		echo "README.md already exists at $path"
	else
		echo "Creating README.md at $path"

		# Create README with package-specific content
		cat >"$path" <<EOF_INNER
# ${name^}

Part of the Haive AI Framework.

## Description

${name^} provides functionality for building dynamic AI agents and workflows.

## Features

- Modular architecture
- Dynamic composition
- Serializable configurations
- Integration with LangChain and LangGraph

## Usage

\`\`\`python
from ${name//-/_} import ...
\`\`\`

## License

Proprietary
EOF_INNER

		echo "Created README.md at $path"
	fi
}

# Check for README.md in project root
if [ ! -f "README.md" ]; then
	echo "Creating README.md in project root"
	cat >"README.md" <<EOF_INNER
# Haive AI Framework

A modular, composable framework for building AI agents and workflows.

## Overview

Haive provides a sophisticated architecture for creating dynamic AI systems with:
- Engine-based component system
- Agent architecture
- Dynamic graph building
- Persistence and state management

## Packages

- haive-core: Core engine and component system
- haive-agents: Agent implementations and tools
- haive-dataflow: Data processing and transformation
- haive-games: Interactive agent games and simulations
- haive-prebuilt: Ready-to-use agent templates
- haive-tools: Development and debugging utilities

## License

Proprietary
EOF_INNER
	echo "Created README.md in project root"
fi

# Check for packages in packages/ directory
for package in "${PACKAGES[@]}"; do
	readme_path="packages/$package/README.md"
	create_readme "$readme_path" "$package"
done

echo "All README.md files have been created or already exist"
echo "Docker build should now proceed without README.md errors"
