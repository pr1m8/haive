#!/bin/bash
# Integrate all enhanced documentation components

echo "======================================================================="
echo "INTEGRATING ENHANCED DOCUMENTATION"
echo "======================================================================="

# Backup current files
echo "📦 Backing up current configuration..."
cp docs/source/conf.py docs/source/conf.py.backup_$(date +%Y%m%d_%H%M%S)
cp docs/source/index.rst docs/source/index.rst.backup_$(date +%Y%m%d_%H%M%S)

# Use the complete enhanced configuration
echo "🔧 Installing enhanced configuration..."
cp docs/source/conf_complete_enhanced.py docs/source/conf.py

# Create _static directory if it doesn't exist
mkdir -p docs/source/_static

# Create placeholder files for enhanced index
echo "📄 Creating placeholder documentation files..."

# Create guide structure
mkdir -p docs/source/guide/{agents,tools,multi_agent,state_management}
echo "User Guide\n==========\n\nComing soon..." >docs/source/guide/index.rst
echo "Agents Guide\n============\n\nComing soon..." >docs/source/guide/agents/index.rst
echo "Tools Guide\n===========\n\nComing soon..." >docs/source/guide/tools/index.rst
echo "Multi-Agent Guide\n=================\n\nComing soon..." >docs/source/guide/multi_agent/index.rst
echo "State Management\n================\n\nComing soon..." >docs/source/guide/state_management/index.rst
echo "Best Practices\n==============\n\nComing soon..." >docs/source/guide/best_practices.rst

# Create examples structure
mkdir -p docs/source/examples
echo "Examples\n========\n\nComing soon..." >docs/source/examples/index.rst
echo "Simple Agents\n=============\n\nComing soon..." >docs/source/examples/simple_agents.rst
echo "ReAct Agents\n============\n\nComing soon..." >docs/source/examples/react_agents.rst
echo "Multi-Agent Workflows\n====================\n\nComing soon..." >docs/source/examples/multi_agent_workflows.rst
echo "RAG Systems\n===========\n\nComing soon..." >docs/source/examples/rag_systems.rst
echo "Game Agents\n===========\n\nComing soon..." >docs/source/examples/game_agents.rst

# Create other sections
echo "Quick Start\n===========\n\nComing soon..." >docs/source/quickstart.rst
echo "Installation\n============\n\nComing soon..." >docs/source/installation.rst
echo "Concepts\n========\n\nComing soon..." >docs/source/concepts.rst
echo "First Agent\n===========\n\nComing soon..." >docs/source/first_agent.rst

# Create integrations
mkdir -p docs/source/integrations
echo "Integrations\n============\n\nComing soon..." >docs/source/integrations/index.rst

# Create MCP docs
mkdir -p docs/source/mcp
echo "MCP Documentation\n=================\n\nComing soon..." >docs/source/mcp/index.rst

# Create development docs
mkdir -p docs/source/development
echo "Contributing\n============\n\nComing soon..." >docs/source/development/contributing.rst
echo "Architecture\n============\n\nComing soon..." >docs/source/development/architecture.rst
echo "Testing\n=======\n\nComing soon..." >docs/source/development/testing.rst
echo "Plugins\n=======\n\nComing soon..." >docs/source/development/plugins.rst
echo "Changelog\n=========\n\nComing soon..." >docs/source/development/changelog.rst

# Create resources
mkdir -p docs/source/resources
echo "FAQ\n===\n\nComing soon..." >docs/source/resources/faq.rst
echo "Troubleshooting\n===============\n\nComing soon..." >docs/source/resources/troubleshooting.rst
echo "Performance\n===========\n\nComing soon..." >docs/source/resources/performance.rst
echo "Security\n========\n\nComing soon..." >docs/source/resources/security.rst
echo "Glossary\n========\n\nComing soon..." >docs/source/resources/glossary.rst

# Check if sphinx_design is available for enhanced index
if poetry run python -c "import sphinx_design" 2>/dev/null; then
	echo "✅ sphinx_design available - using enhanced index"
	cp docs/source/index_enhanced.rst docs/source/index.rst
else
	echo "⚠️  sphinx_design not available - keeping simple index"
	echo "   Run: poetry add --group docs sphinx-design"
fi

# Clean build directory
echo "🧹 Cleaning build directory..."
rm -rf docs/build/html

# Build documentation
echo ""
echo "🔨 Building enhanced documentation..."
echo "======================================================================="

poetry run sphinx-build -b html docs/source docs/build/html -v 2>&1 | tee enhanced_build.log

# Check results
if [ $? -eq 0 ]; then
	echo ""
	echo "✅ BUILD SUCCESSFUL!"
	echo ""
	echo "📊 Build Statistics:"
	echo "  - HTML files: $(find docs/build/html -name "*.html" | wc -l)"
	echo "  - API files: $(find docs/build/html/api -name "*.html" 2>/dev/null | wc -l || echo 0)"
	echo "  - Warnings: $(grep -c "WARNING:" enhanced_build.log || echo 0)"
	echo ""
	echo "🌐 View documentation at: file://$PWD/docs/build/html/index.html"
else
	echo ""
	echo "❌ BUILD FAILED - Check enhanced_build.log"
fi

echo ""
echo "======================================================================="
echo "📝 Notes:"
echo "  - Install missing extensions: poetry add --group docs <extension-name>"
echo "  - For all themes: poetry add --group docs pydata-sphinx-theme sphinx-book-theme"
echo "  - For diagrams: poetry add --group docs sphinxcontrib-mermaid"
echo "  - For enhanced features: poetry add --group docs sphinx-design sphinx-tabs"
echo "======================================================================="
