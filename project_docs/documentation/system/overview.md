# Documentation System Overview

## 🏗️ Architecture

### Documentation Stack

- **Generator**: Sphinx 8.2.3
- **Theme**: Furo (with custom showcase styling)
- **API Docs**: AutoAPI
- **Examples**: Sphinx Gallery
- **Build Tool**: Nox

### Key Components

#### 1. **Sphinx Configuration** (`docs/source/conf.py`)

- AutoAPI for automatic API documentation
- Sphinx Gallery for example galleries
- Enhanced Furo theme with showcase cards
- Custom CSS/JS for modern styling

#### 2. **Gallery System**

- Package-specific example directories
- Automatic gallery generation
- Showcase cards with visual appeal
- Runnable code examples

#### 3. **API Documentation**

- Automatic generation from source code
- No manual maintenance required
- Complete coverage of all packages
- Proper namespace handling

## 📁 Directory Structure

```
docs/
├── source/                    # Source RST/MD files
│   ├── conf.py               # Sphinx configuration
│   ├── index.rst             # Main documentation index
│   ├── gallery.rst           # Example gallery index
│   ├── _static/              # CSS/JS/Images
│   ├── _templates/           # Custom templates
│   ├── agents/               # Agent documentation
│   ├── games/                # Games documentation
│   ├── tools/                # Tools documentation
│   ├── mcp/                  # MCP documentation
│   └── api/                  # API reference (AutoAPI generated)
├── build/                     # Built HTML output
└── logs/                      # Build logs

packages/
├── haive-agents/examples/     # Agent examples
├── haive-tools/examples/      # Tool examples
├── haive-games/examples/      # Game examples
└── haive-mcp/examples/        # MCP examples
```

## 🔧 Build System

### Primary Build Command

```bash
nox -s docs
```

### Build Process

1. AutoAPI scans all packages
2. Generates API documentation
3. Sphinx Gallery processes examples
4. Furo theme applies styling
5. HTML output generated

### Build Options

- `nox -s docs` - Standard build
- `nox -s docs-3.12` - Specific Python version
- `nox -s serve` - Build and serve locally

## 🎨 Styling System

### CSS Files

- `custom.css` - Base customizations
- `furo-showcase.css` - Showcase card styling
- `haive-enhanced.css` - Enhanced visual styling
- `agent-visualization.css` - Agent-specific styling

### JavaScript

- `showcase-interactions.js` - Interactive showcase elements
- `enhanced-search.js` - Enhanced search functionality
- `agent-visualization.js` - Agent visualization features

## 📊 Current Metrics

### Build Health

- **Errors**: 3 (from 195)
- **Warnings**: 5 (from 475)
- **Success Rate**: 98%+
- **Build Time**: ~2 minutes

### Coverage

- **Packages**: 6/6 documented
- **Examples**: 4 gallery sections
- **API**: 100% automated coverage

## 🚀 Recent Improvements

1. **AutoAPI Integration** - Complete API automation
2. **Gallery System** - Package-specific examples
3. **Error Reduction** - 97% fewer errors
4. **Showcase Styling** - Modern, professional appearance
5. **Navigation** - Improved structure and flow

## 🔍 Troubleshooting

### Common Issues

#### 1. KeyError in AutoAPI

- **Cause**: Invalid file names
- **Solution**: Remove files with spaces/parentheses

#### 2. Import Errors

- **Cause**: Missing dependencies
- **Solution**: `poetry install --all-extras`

#### 3. Gallery Not Showing

- **Cause**: Wrong directory config
- **Solution**: Check `sphinx_gallery_conf`

### Debug Commands

```bash
# Check syntax errors
find packages -name "*.py" -exec python -m py_compile {} \;

# Test imports
poetry run python -c "import haive.agents"

# Quick build test
poetry run sphinx-build -b html docs/source docs/build/html -W
```

## 📚 Documentation Standards

### Docstring Format

- Google-style docstrings
- Complete parameter documentation
- Examples section when applicable
- Type hints in signatures

### File Organization

- Package documentation in package directories
- Examples with `_example.py` suffix
- RST files for manual content
- AutoAPI for code documentation

## 🎯 Future Enhancements

1. **Interactive Examples** - Live code execution
2. **Version Switcher** - Multiple version support
3. **Search Enhancement** - Better search indexing
4. **PDF Generation** - Offline documentation
5. **API Playground** - Interactive API testing
