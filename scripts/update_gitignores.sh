#!/bin/bash

# Script to update .gitignore files in all packages with standard documentation patterns

DOCS_PATTERNS='
# === Documentation build artifacts ===
docs/build/
docs/_build/
docs/logs/
docs/autoapi/
docs/source/_autosummary/
docs/source/_autoapi_templates/
docs/source/_build/
docs/source/api/
docs/_build/html/
docs/build/html/
*.rst~
.doctrees/
_build/
_static/
_templates/
'

# Function to update gitignore if patterns don't exist
update_gitignore() {
    local gitignore_file=$1
    
    # Check if docs patterns already exist
    if ! grep -q "Documentation build artifacts\|docs/build/\|docs/_build/" "$gitignore_file"; then
        echo "Updating $gitignore_file with documentation patterns..."
        echo "$DOCS_PATTERNS" >> "$gitignore_file"
    else
        echo "$gitignore_file already has documentation patterns"
    fi
}

# Update each package's .gitignore
for pkg_gitignore in packages/*/.gitignore; do
    if [ -f "$pkg_gitignore" ]; then
        update_gitignore "$pkg_gitignore"
    fi
done

echo "Done updating .gitignore files"