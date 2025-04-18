#!/bin/bash
# Script to update all haive packages and repositories

set -e  # Exit on error

MAIN_DIR="$HOME/Projects/haive/backend/haive"
cd "$MAIN_DIR"

# List of all packages
PACKAGES=(
  "haive-core"
  "haive-agents"
  "haive-games"
  "haive-dataflow"
  "haive-prebuilt"
  "haive-tools"
)

echo "==== Starting package updates ===="

# Process each package
for pkg in "${PACKAGES[@]}"; do
  echo -e "\n\n==== Processing $pkg ===="
  cd "$MAIN_DIR/packages/$pkg"
  
  # Check and fix package structure if needed
  if [ ! -d "$pkg" ] && [ ! -d "${pkg//-/_}" ] && [ ! -d "src" ]; then
    echo "Creating proper package structure for $pkg..."
    pkg_dir="${pkg//-/_}"
    mkdir -p "$pkg_dir"
    touch "$pkg_dir/__init__.py"
    
    # Update pyproject.toml to include the package
    if ! grep -q "packages" pyproject.toml; then
      echo "Updating pyproject.toml to specify package location..."
      # Insert packages section before [build-system]
      sed -i "/\[build-system\]/i \[tool.poetry\]\npackages = [{include = \"$pkg_dir\"}]\n" pyproject.toml
    fi
  fi
  
  if [ "$pkg" == "haive-core" ]; then
    echo "Special handling for haive-core..."
    # Try to fix potential torch issues in lock file
    rm -f poetry.lock
    poetry lock  || echo "Lock file creation failed, continuing anyway"
    echo "Updating dependencies"
  else
    echo "Running poetry lock..."
    poetry lock  || echo "Lock failed, continuing anyway"
  fi
  
  echo "Running poetry install..."
  poetry install --no-root || echo "Install failed, continuing anyway"
  
  echo "Committing changes..."
  git add .
  git commit -m "Update dependencies for $pkg" || echo "No changes to commit"
  
  echo "Pushing to origin/main..."
  git push origin main || echo "Push failed, continuing anyway"
  
  echo "==== Completed $pkg ===="
done

# Process main repository
echo -e "\n\n==== Processing main repository ===="
cd "$MAIN_DIR"

# Fix dependency references in main pyproject.toml
echo "Checking main repository dependencies..."
for pkg in "${PACKAGES[@]}"; do
  pkg_path="packages/$pkg"
  if grep -q "path = \"../.*$pkg\"" pyproject.toml; then
    echo "Fixing path reference for $pkg..."
    sed -i "s|path = \"../.*$pkg\"|path = \"$pkg_path\"|g" pyproject.toml
  fi
done

echo "Running poetry lock for main repo..."
poetry lock --no-update || echo "Lock failed, continuing anyway"

echo "Running poetry install for main repo..."
poetry install --extras cpu --no-root || echo "Install failed, continuing anyway"

echo "Committing changes in main repo..."
git add .
git commit -m "Update all dependencies and submodule references" || echo "No changes to commit"

echo "Pushing main repo to origin/main..."
git push origin main || echo "Push failed, continuing anyway"

echo -e "\n\n==== Starting Docker build ===="
docker build -t haive:latest .

echo -e "\n\n==== All updates completed! ===="
echo "You can now run your Docker container with: docker run -p 8000:8000 haive:latest"