#!/bin/bash
# Enable automatic source tracking for all Python scripts

echo "🚀 Haive Auto-Logging Setup"
echo "=========================="
echo ""
echo "This will enable automatic source tracking for all Python scripts."
echo ""

# Method 1: Shell alias (recommended)
echo "Method 1: Shell Alias (Recommended)"
echo "-----------------------------------"
echo "Add this line to your ~/.bashrc or ~/.zshrc:"
echo ""
echo "  alias python='python -m haive.core.logging.auto_wrapper'"
echo ""
echo "Or for a shorter alias:"
echo "  alias pytrack='python -m haive.core.logging.auto_wrapper'"
echo ""

# Method 2: Environment variable
echo "Method 2: Environment Variable"
echo "------------------------------"
echo "Add this to your shell profile:"
echo ""
echo "  export HAIVE_AUTO_LOGGING=1"
echo ""
echo "Then haive will auto-enable source tracking when imported."
echo ""

# Method 3: Python startup file
echo "Method 3: Python Startup File"
echo "-----------------------------"
echo "Create a file ~/.pythonrc with:"
echo ""
cat <<'EOF'
try:
    from haive.core.logging.quick_setup import setup_development_logging
    setup_development_logging()
    print("📍 Haive source tracking enabled automatically!")
except ImportError:
    pass
EOF
echo ""
echo "Then add to your shell profile:"
echo "  export PYTHONSTARTUP=~/.pythonrc"
echo ""

# Method 4: Site customize
echo "Method 4: Site-wide Configuration"
echo "---------------------------------"
echo "Copy sitecustomize.py to your Python site-packages:"
echo ""
echo "  cp $(dirname "$0")/../src/haive/core/logging/sitecustomize.py $(python -m site --user-site)/"
echo ""
echo "Then set: export HAIVE_TRACK_ALL=1"
echo ""

# Quick test
echo "Quick Test"
echo "----------"
echo "Try this command to test:"
echo ""
echo "  python -m haive.core.logging.auto_wrapper -c 'import logging; logging.info(\"test\"); print(\"hello\")'"
echo ""

# Add to current session
read -p "Would you like to enable Method 1 (alias) for this session? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
	alias python='python -m haive.core.logging.auto_wrapper'
	echo "✅ Alias enabled for this session!"
	echo "   Now any 'python' command will have source tracking."
fi
