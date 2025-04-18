#!/bin/bash
# Clean all pyproject.toml files

for pkg in packages/*; do
	if [[ -d ${pkg} ]]; then
		pkg_name=$(basename "${pkg}")
		echo "Cleaning ${pkg}/pyproject.toml"

		# Create a clean pyproject.toml
		cat >"${pkg}/pyproject.toml" <<EOT
[tool.poetry]
name = "${pkg_name}"
version = "0.1.0"
description = "${pkg_name} for Haive framework"
authors = ["pr1m8 <william.astley@algebraicwealth.com>"]
license = "MIT"
readme = "README.md"

[tool.poetry.dependencies]
python = ">=3.12,<3.13"
pydantic = "^2.10.6"
langchain = "^0.3.20"
langchain-core = "^0.3.44"
langgraph = "^0.3.5"

[tool.poetry.group.dev.dependencies]
pytest = "^8.3.5"
black = "^25.1.0"
isort = "^6.0.1"
mypy = "^1.15.0"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
EOT

		echo "Created clean pyproject.toml for ${pkg_name}"
	fi
done

# Now update the internal dependencies
sed -i 's/dependencies]/dependencies]\nhaive-core = {path = "..\/haive-core", develop = true}/g' packages/haive-agents/pyproject.toml
sed -i 's/dependencies]/dependencies]\nhaive-core = {path = "..\/haive-core", develop = true}/g' packages/haive-tools/pyproject.toml
sed -i 's/dependencies]/dependencies]\nhaive-core = {path = "..\/haive-core", develop = true}\nhaive-agents = {path = "..\/haive-agents", develop = true}/g' packages/haive-prebuilt/pyproject.toml
sed -i 's/dependencies]/dependencies]\nhaive-core = {path = "..\/haive-core", develop = true}/g' packages/haive-dataflow/pyproject.toml
sed -i 's/dependencies]/dependencies]\nhaive-core = {path = "..\/haive-core", develop = true}/g' packages/haive-games/pyproject.toml

echo "Updated internal dependencies"
