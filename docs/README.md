# Haive Documentation System

**Status**: ✅ Cleaned and Organized (August 2025)  
**Build System**: Sphinx + Nox with modular configuration  
**Theme**: Furo with custom enhancements

## 🏗️ Directory Structure

```
docs/
├── source/                     # 📝 SOURCE FILES (edit these)
│   ├── conf.py                # Main Sphinx configuration
│   ├── conf_modules/          # Modular config system
│   │   ├── extensions/        # Extension configurations
│   │   ├── themes/           # Theme settings
│   │   └── core/             # Core utilities
│   ├── _templates/           # Jinja2 templates
│   ├── _static/              # CSS, JS, images
│   ├── agents/               # Agent documentation
│   ├── games/                # Game documentation
│   ├── guides/               # User guides
│   └── *.rst, *.md          # Content files
├── build/                    # 🏗️ BUILD OUTPUT (generated)
│   ├── html/                # Built HTML documentation
│   ├── doctrees/            # Sphinx cache
│   └── _static/             # Processed static files
├── _consolidated_archives/   # 📦 ARCHIVED FILES
│   ├── logs/                # ~400+ old log files
│   ├── config_backups/      # Configuration backups
│   ├── reports/             # Analysis reports
│   └── scripts/             # Old Python scripts
├── *.md                     # Documentation guides
├── requirements*.txt        # Python dependencies
└── Makefile, make.bat      # Build tools
```

## 🚀 Quick Start

### Build Documentation

```bash
# Fast build (recommended for development)
nox -s docs_fast

# Full build with all features
nox -s docs

# Auto-rebuild on changes
nox -s docs_autobuild

# Clean build
nox -s docs_clean && nox -s docs
```

### Development Workflow

```bash
# 1. Edit source files in source/
vim source/agents/new_guide.rst

# 2. Build and preview
nox -s docs_fast
python -m http.server 8000 --directory build/html

# 3. View at http://localhost:8000
```

## 📁 What Goes Where

### ✏️ Edit These (SOURCE)

- `source/*.rst, *.md` - Documentation content
- `source/_static/` - Custom CSS, JS, images
- `source/_templates/` - HTML templates
- `source/conf.py` - Main configuration
- `source/conf_modules/` - Modular configurations

### 🚫 Don't Edit These (GENERATED)

- `build/` - Built documentation (auto-generated)
- `source/_build/` - Sphinx temporary files
- `source/__pycache__/` - Python cache

### 📦 Archived (REFERENCE ONLY)

- `_consolidated_archives/` - Old files for reference

## 🔧 Configuration System

The documentation uses a **modular configuration system**:

- **`conf.py`** - Main entry point, imports modules
- **`conf_modules/extensions/`** - Extension configs
- **`conf_modules/themes/`** - Theme configurations
- **`conf_modules/core/`** - Utilities and logging

### Key Features

- ✅ Automatic package discovery
- ✅ Enhanced error handling
- ✅ Structured logging
- ✅ Multiple build modes
- ✅ Template engine integration

## 🎨 Customization

### Adding Content

```bash
# Create new guide
cp source/_templates/guide_template.rst source/guides/my_guide.rst

# Add to navigation
echo "   guides/my_guide" >> source/index.rst
```

### Custom Styling

```bash
# Add CSS
echo "/* My styles */" >> source/_static/custom.css

# Add JavaScript
echo "// My scripts" >> source/_static/custom.js
```

## 🧪 Testing & Quality

### Available Commands

```bash
# Test build without errors
nox -s docs_test_pipeline

# Check documentation quality
nox -s docs_quality

# Validate links
nox -s docs_linkcheck

# Test examples
nox -s docs_test_examples
```

### Build Modes

- **`docs_fast`** - Quick build, continues on errors
- **`docs`** - Standard build with error checking
- **`docs_debug`** - Verbose build for troubleshooting
- **`docs_quality`** - Full quality checks

## 🐛 Troubleshooting

### Common Issues

**Build fails with import errors:**

```bash
# Check Python path and dependencies
poetry install --all-extras
nox -s docs_debug
```

**Missing static files:**

```bash
# Clear cache and rebuild
nox -s docs_clean
nox -s docs
```

### Logs Location

- Current logs: Stored in `_consolidated_archives/logs/`
- Session logs: `~/.nox/docs*/`

## 📚 Related Documentation

- **Main Project Hub**: `../CLAUDE.md` - Central project memory
- **Package Documentation**: `../packages/{name}/README.md`
- **Project Documentation**: `../project_docs/` - Development notes
- **Examples**: `../examples/` - Code examples

## 🔄 Recent Cleanup (August 2025)

- ✅ Consolidated ~400+ scattered log files
- ✅ Organized config backups and archives
- ✅ Fixed import order in conf.py
- ✅ Removed duplicate directories
- ✅ Verified build system compatibility
- ✅ Created clear source vs build separation

---

**Need help?** Check the troubleshooting section or run `nox -s docs_debug` for detailed output.
