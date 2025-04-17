#!/bin/bash
# Initialize repositories for each package

set -e  # Exit on any error

ORG_NAME="pr1m8"  # Your GitHub organization name
PACKAGES_DIR="packages"

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo "GitHub CLI not found. Please install it with:"
    echo "  sudo apt install gh  # For Ubuntu/Debian"
    echo "  brew install gh      # For macOS"
    exit 1
fi

# Ensure GitHub CLI is authenticated
if ! gh auth status &> /dev/null; then
    echo "Please log in to GitHub CLI:"
    gh auth login
fi

# For each package directory
for pkg_dir in "$PACKAGES_DIR"/*; do
    if [ -d "$pkg_dir" ]; then
        pkg_name=$(basename "$pkg_dir")
        echo "Processing $pkg_name..."
        
        # Change to package directory
        cd "$pkg_dir"
        
        # Initialize git repository if not already initialized
        if [ ! -d ".git" ]; then
            git init
            git add .
            git commit -m "Initial commit from migration"
        fi
        
        # Check if repository exists
        if gh repo view "$ORG_NAME/$pkg_name" &> /dev/null; then
            echo "Repository $ORG_NAME/$pkg_name already exists"
            
            # Set up remote if not already set
            if ! git remote | grep -q "origin"; then
                git remote add origin "https://github.com/$ORG_NAME/$pkg_name.git"
            fi
            
            # Push to repository (might fail if histories don't match)
            echo "Attempting to push to existing repository..."
            if ! git push -u origin main --force; then
                echo "Direct push failed. You may need to manually sync repositories."
                echo "Consider cloning the repository and copying the files over."
            fi
        else
            # Create repository and push
            echo "Creating new repository $ORG_NAME/$pkg_name..."
            gh repo create "$ORG_NAME/$pkg_name" --private --source=. --push
        fi
        
        # Return to original directory
        cd - > /dev/null
        echo "Done with $pkg_name"
        echo "----------------------------"
    fi
done

echo "Repository setup complete."
echo "You can now continue with your development."