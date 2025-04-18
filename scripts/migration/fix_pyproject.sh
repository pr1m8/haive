#!/bin/bash
# Fix all the pyproject.toml files

for pkg in packages/*; do
	if [[ -d ${pkg} ]]; then
		echo "Fixing ${pkg}/pyproject.toml"

		# Replace newlines in dependencies with actual newlines
		sed -i 's/\\n/\n/g' "${pkg}/pyproject.toml"

		echo "Fixed ${pkg}/pyproject.toml"
	fi
done
