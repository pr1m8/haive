#!/bin/bash

# Script to update documentation for all haive packages
# Applies the same improvements made to haive-core

echo "🚀 Updating documentation for all haive packages..."

# Define packages to update
PACKAGES=(
    "haive-agents"
    "haive-tools"
    "haive-mcp"
    "haive-games"
    "haive-dataflow"
    "haive-prebuilt"
    "haive-hap"
)

# Base directory
BASE_DIR="/home/will/Projects/haive/packages"

for PACKAGE in "${PACKAGES[@]}"; do
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📦 Processing $PACKAGE..."
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    DOCS_DIR="$BASE_DIR/$PACKAGE/docs"
    
    # Check if package and docs exist
    if [ ! -d "$BASE_DIR/$PACKAGE" ]; then
        echo "⚠️  Package $PACKAGE not found, skipping..."
        continue
    fi
    
    if [ ! -d "$DOCS_DIR/source" ]; then
        echo "⚠️  No docs/source directory for $PACKAGE, skipping..."
        continue
    fi
    
    # 1. Update conf.py with announcement bar and proper GitHub links
    CONF_FILE="$DOCS_DIR/source/conf.py"
    if [ -f "$CONF_FILE" ]; then
        echo "  ✏️  Updating conf.py..."
        
        # Check if html_theme_options exists
        if grep -q "html_theme_options" "$CONF_FILE"; then
            # Update existing html_theme_options
            python3 - "$CONF_FILE" "$PACKAGE" <<'EOF'
import sys
import re

conf_file = sys.argv[1]
package_name = sys.argv[2]

with open(conf_file, 'r') as f:
    content = f.read()

# Add announcement bar if not present
if 'announcement' not in content:
    # Find html_theme_options
    pattern = r'(html_theme_options\s*=\s*\{[^}]*)'
    
    announcement = '''    "announcement": (
        '<div style="font-weight: 600;">'
        '🚀 <a href="https://github.com/pr1m8/''' + package_name + '''" target="_blank">Star us on GitHub</a> | '
        '<a href="https://discord.gg/haive" target="_blank">Join Discord</a> | '
        '<a href="https://docs.haive.io" target="_blank">Haive Central Docs</a>'
        '</div>'
    ),
'''
    
    def add_announcement(match):
        return match.group(1) + '\n' + announcement
    
    content = re.sub(pattern, add_announcement, content, count=1)

# Update GitHub references
content = content.replace('github.com/haive/', 'github.com/pr1m8/')
content = content.replace('"https://github.com/pr1m8/haive"', f'"https://github.com/pr1m8/{package_name}"')

# Add source repository settings if not present
if '"source_repository"' not in content and 'html_theme_options' in content:
    pattern = r'(html_theme_options\s*=\s*\{[^}]*)'
    
    source_settings = f'''    "source_repository": "https://github.com/pr1m8/{package_name}",
    "source_branch": "main",
    "source_directory": "docs/source/",
'''
    
    def add_source_settings(match):
        return match.group(1) + '\n' + source_settings
    
    content = re.sub(pattern, add_source_settings, content, count=1)

# Update footer icons
if '"footer_icons"' in content:
    # Update existing footer icons
    pattern = r'"footer_icons":\s*\[[^\]]*\]'
    replacement = '''"footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/pr1m8/''' + package_name + '''",
            "html": '<svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path></svg>',
            "class": "",
        },
        {
            "name": "Discord",
            "url": "https://discord.gg/haive",
            "html": '<svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16"><path d="M13.545 2.907a13.227 13.227 0 0 0-3.257-1.011.05.05 0 0 0-.052.025c-.141.25-.297.577-.406.833a12.19 12.19 0 0 0-3.658 0 8.258 8.258 0 0 0-.412-.833.051.051 0 0 0-.052-.025c-1.125.194-2.22.534-3.257 1.011a.041.041 0 0 0-.021.018C.356 6.024-.213 9.047.066 12.032c.001.014.01.028.021.037a13.276 13.276 0 0 0 3.995 2.02.05.05 0 0 0 .056-.019c.308-.42.582-.863.818-1.329a.05.05 0 0 0-.01-.059.051.051 0 0 0-.018-.011 8.875 8.875 0 0 1-1.248-.595.05.05 0 0 1-.02-.066.051.051 0 0 1 .015-.019c.084-.063.168-.129.248-.195a.05.05 0 0 1 .051-.007c2.619 1.196 5.454 1.196 8.041 0a.052.052 0 0 1 .053.007c.08.066.164.132.248.195a.051.051 0 0 1-.004.085 8.254 8.254 0 0 1-1.249.594.05.05 0 0 0-.03.03.052.052 0 0 0 .003.041c.24.465.515.909.817 1.329a.05.05 0 0 0 .056.019 13.235 13.235 0 0 0 4.001-2.02.049.049 0 0 0 .021-.037c.334-3.451-.559-6.449-2.366-9.106a.034.034 0 0 0-.02-.019Zm-8.198 7.307c-.789 0-1.438-.724-1.438-1.612 0-.889.637-1.613 1.438-1.613.807 0 1.45.73 1.438 1.613 0 .888-.637 1.612-1.438 1.612Zm5.316 0c-.788 0-1.438-.724-1.438-1.612 0-.889.637-1.613 1.438-1.613.807 0 1.451.73 1.438 1.613 0 .888-.631 1.612-1.438 1.612Z"></path></svg>',
            "class": "",
        },
        {
            "name": "Haive Docs",
            "url": "https://docs.haive.io",
            "html": '<svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16"><path d="M14 4.5V14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2h5.5L14 4.5zm-3 0A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V4.5h-2z"/></svg>',
            "class": "",
        },
    ]'''
    content = re.sub(pattern, replacement, content)

with open(conf_file, 'w') as f:
    f.write(content)

print(f"    ✅ Updated conf.py for {package_name}")
EOF
        fi
    fi
    
    # 2. Copy custom.css if haive-core has it
    if [ -f "$BASE_DIR/haive-core/docs/source/_static/custom.css" ]; then
        mkdir -p "$DOCS_DIR/source/_static"
        cp "$BASE_DIR/haive-core/docs/source/_static/custom.css" "$DOCS_DIR/source/_static/"
        echo "  ✅ Copied custom.css"
    fi
    
    # 3. Fix VectorStore imports in all .rst files
    echo "  🔧 Fixing VectorStore imports..."
    find "$DOCS_DIR/source" -name "*.rst" -type f -exec sed -i \
        -e 's/from haive\.core\.models\.vectorstore/from haive.core.engine.vectorstore/g' \
        -e 's/from haive\.core\.models\.embeddings/from haive.core.engine.embedding.providers/g' \
        {} \;
    
    # 4. Update GitHub references in all .rst files
    echo "  🔧 Updating GitHub references..."
    find "$DOCS_DIR/source" -name "*.rst" -type f -exec sed -i \
        -e "s|github.com/haive/$PACKAGE|github.com/pr1m8/$PACKAGE|g" \
        -e "s|github.com/haive/haive|github.com/pr1m8/$PACKAGE|g" \
        {} \;
    
    # 5. Create/update additional_resources.rst if it doesn't exist
    RESOURCES_FILE="$DOCS_DIR/source/additional_resources.rst"
    if [ ! -f "$RESOURCES_FILE" ]; then
        echo "  📄 Creating additional_resources.rst..."
        cat > "$RESOURCES_FILE" <<EORF
==================
Additional Resources
==================

External Links
--------------

.. grid:: 2 2 3 3
   :gutter: 2

   .. grid-item::
   
      **GitHub Repository**
      
      `pr1m8/$PACKAGE <https://github.com/pr1m8/$PACKAGE>`_
      
   .. grid-item::
   
      **Discord Community**
      
      `Join our Discord <https://discord.gg/haive>`_
      
   .. grid-item::
   
      **Haive Central Docs**
      
      `docs.haive.io <https://docs.haive.io>`_
      
   .. grid-item::
   
      **PyPI Package**
      
      `$PACKAGE on PyPI <https://pypi.org/project/$PACKAGE/>`_

Developer Resources
-------------------

.. dropdown:: Code Examples

   Find examples in the \`examples/\` directory of the GitHub repository.
   
   - Basic usage patterns
   - Advanced configurations
   - Integration examples

.. dropdown:: Contributing

   We welcome contributions! Please see our `Contributing Guide <https://github.com/pr1m8/$PACKAGE/blob/main/CONTRIBUTING.md>`_.

.. dropdown:: API Documentation

   Full API documentation is available in the :doc:\`api_reference\` section.

Related Haive Packages
----------------------

.. dropdown:: Haive Ecosystem

   - \`haive-core\` - Core framework foundation
   - \`haive-agents\` - Pre-built agent implementations  
   - \`haive-tools\` - Tool integrations
   - \`haive-mcp\` - Model Context Protocol support
   - \`haive-games\` - Game environments
   - \`haive-dataflow\` - Data processing pipelines
   - \`haive-prebuilt\` - Ready-to-use configurations
   - \`haive-hap\` - Haive Application Protocol

Support & Help
--------------

.. dropdown:: Getting Help

   - **Issues**: `Report bugs <https://github.com/pr1m8/$PACKAGE/issues>`_
   - **Discussions**: `GitHub Discussions <https://github.com/pr1m8/$PACKAGE/discussions>`_
   - **Discord**: `Join our community <https://discord.gg/haive>`_

License & Citation
------------------

.. dropdown:: License Information

   This project is licensed under the MIT License. See the LICENSE file for details.

.. dropdown:: Citation

   If you use this package in your research, please cite:
   
   .. code-block:: bibtex
   
      @software{$PACKAGE,
        title = {$PACKAGE},
        author = {Haive Team},
        url = {https://github.com/pr1m8/$PACKAGE},
        year = {2025}
      }
EORF
    fi
    
    # 6. Remove hero sections if they exist
    echo "  🧹 Removing hero sections..."
    for rst_file in "$DOCS_DIR/source"/*.rst; do
        if [ -f "$rst_file" ]; then
            # Remove hero section HTML
            sed -i '/<div class="hero-section">/,/<\/div>/d' "$rst_file"
        fi
    done
    
    echo "  ✅ Completed updates for $PACKAGE"
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ All packages updated successfully!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Next steps:"
echo "1. Build documentation for each package:"
echo "   cd packages/<package-name>"
echo "   poetry run sphinx-build -b html docs/source docs/build/html"
echo ""
echo "2. Or use the build_all_docs.sh script to build all at once"