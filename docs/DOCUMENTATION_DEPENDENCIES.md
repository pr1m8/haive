# Documentation Dependencies Guide

**Project:** PyAutoDoc Multi-Version Documentation Testing  
**Created:** 2025-01-08 16:00:00 UTC  
**Total Dependencies:** 150+ packages  
**Purpose:** Comprehensive testing of Sphinx documentation features

---

## 📋 Table of Contents

1. [Core Sphinx Framework](#core-sphinx-framework)
2. [Themes](#themes)
3. [Multi-Version & Versioning](#multi-version--versioning)
4. [API Documentation](#api-documentation)
5. [Content & Markup](#content--markup)
6. [Interactive Elements](#interactive-elements)
7. [Diagrams & Visualizations](#diagrams--visualizations)
8. [External Integrations](#external-integrations)
9. [Development & Quality](#development--quality)
10. [Testing Notes](#testing-notes)

---

## 🎯 Core Sphinx Framework

### Base System

```toml
sphinx = "8.2.3"                    # Core Sphinx documentation generator
sphinxcontrib-jquery = "^4.1"       # jQuery support for themes
sphinx-autobuild = "^2024.10.3"     # Live reload during development
```

**@core-framework**: Essential Sphinx infrastructure  
**Status**: ✅ Working  
**Notes**: Latest stable Sphinx version with jQuery compatibility

---

## 🎨 Themes

### Primary Themes

```toml
furo = "^2024.8.6"                  # Modern, clean theme (current default)
sphinx-rtd-theme = "^3.0.2"         # Read the Docs theme
pydata-sphinx-theme = "^0.16.1"     # PyData community theme
sphinx-book-theme = "*"             # Jupyter Book theme (implied by myst-nb)
```

### Alternative Themes

```toml
sphinx-modern-theme = "^1.0.5"      # Modern minimalist theme
sphinx-basic-ng = "^1.0.0b2"        # Next-gen basic theme
sphinx-typlog-theme = "^0.8.0"      # Typography-focused theme
```

**@themes @testing**: Multi-theme compatibility testing  
**Status**: 🚧 Need to test each theme  
**Next**: Create theme comparison matrix

### Theme Testing Plan

- [ ] **Furo**: Test all features (current)
- [ ] **PyData**: Scientific/data science styling
- [ ] **RTD**: Classic Read the Docs look
- [ ] **Book**: Jupyter Book integration
- [ ] **Modern**: Minimalist design
- [ ] **Typlog**: Typography focus

---

## 📚 Multi-Version & Versioning

### Multi-Version Systems

```toml
sphinx-multiversion = "^0.2.4"      # Git-based multi-version docs
sphinxcontrib-versioning = "^2.2.1" # Alternative versioning approach
sphinx-versions = "^1.1.3"          # Version management utilities
sphinx-polyversion = "^1.1.0"       # Polyglot version handling
sphinx-versioning = "^0.1.5"        # Additional versioning tools
```

### Version-Related Features

```toml
sphinx-version-warning = "^1.1.2"   # Warn about outdated versions
sphinx-last-updated-by-git = "^0.3.8" # Git-based last updated info
```

**@multiversion @git-integration**: Version control integration  
**Status**: 🚧 Primary focus - need to configure  
**Priority**: HIGH

### Multi-Version Strategy

```markdown
Planned Version Structure:
├── latest/ # Main branch (development)
├── stable/ # Latest stable release  
├── v1.0.0/ # Tagged releases
├── v0.9.0/  
└── dev/ # Feature branches

Features to Test:

- Cross-version linking
- Version dropdown navigation
- Automated version detection
- Branch-based documentation
```

---

## 🤖 API Documentation

### Auto-Generation

```toml
sphinx-autoapi = "^3.6.0"           # Automatic API documentation (current)
sphinx-autodoc2 = "^0.5.0"          # Alternative autodoc implementation
sphinx-autosummary-accessors = "^2025.3.1" # Enhanced autosummary
autodocsumm = "^0.2.14"             # Summary tables
```

### Specialized Documentation

```toml
autodoc-pydantic = "^2.2.0"         # Pydantic model documentation (active)
enum-tools = "^0.13.0"              # Enhanced enum documentation (active)
sphinx-toolbox = "^3.8.1"           # Required by enum-tools (active)
erdantic = "^1.0.6"                 # Entity relationship diagrams (active)
```

### Auto-Generation Tools

```toml
sphinx-autodocgen = "^1.4"          # Generate autodoc files
sphinx-automagicdoc = "^0.0.2"      # Magic autodoc generation
sphinx-autofixture = "^0.4.1"       # Auto-fixture documentation
sphinx-autorun = "^2.0.0"           # Auto-run code examples
sphinx-autoissues = "^0.0.1"        # Auto-link to issues
sphinx-autoindex = "^0.1.5"         # Auto-generate indices
sphinx-autopackagesummary = "^1.3"  # Package summary generation
sphinx-autopages = "^0.0.3"         # Auto-generate pages
sphinx-automodapi = "^0.20.0"       # Auto-document modules
```

**@api-docs @automation**: Automated documentation generation  
**Status**: ✅ Core features working  
**Next**: Test all auto-generation tools

---

## 📝 Content & Markup

### Markdown & MyST

```toml
myst-parser = "^4.0.1"              # Markdown support (MyST)
myst-nb = "^1.3.0"                  # Jupyter notebook integration
sphinx-markdown = "^1.0.2"          # Additional markdown features
```

### Enhanced Markup

```toml
sphinx-design = "^0.6.1"            # Modern design elements (cards, grids)
sphinx-tabs = "^3.4.5"              # Tabbed content (version fixed for compatibility)
sphinx-inline-tabs = "^2023.4.21"   # Inline tabbed content
sphinx-togglebutton = "^0.3.2"      # Collapsible sections (active)
sphinx-copybutton = "^0.5.2"        # Copy code button (active)
```

### Content Organization

```toml
sphinxcontrib-fulltoc = "^1.2.0"    # Full table of contents
sphinx-external-toc = "^1.0.1"      # External TOC definition
sphinx-tagtoctree = "^1.0.0"        # Tag-based TOC
sphinx-treeview = "^1.1.1"          # Tree view navigation
```

**@content @markup**: Content presentation and organization  
**Status**: ✅ Basic features working  
**Next**: Test advanced design elements

---

## 🎛️ Interactive Elements

### User Interface

```toml
sphinx-prompt = "^1.10.0"           # Command prompt styling
sphinx-btn = "^0.1.2"               # Button elements
sphinx-carousel = "^1.2.0"          # Image carousels
sphinx-collapse = "^0.1.3"          # Collapsible content
sphinx-toggleprompt = "^0.6.0"      # Toggle command prompts
```

### Feedback & Social

```toml
sphinx-feedback = "^0.1.0"          # User feedback forms
sphinx-comments = "^0.0.3"          # Comment system integration
sphinx-disqus = "^1.3.0"            # Disqus comments
sphinx-social = "^0.0.0"            # Social media integration
```

### Navigation Enhancements

```toml
sphinx-tippy = "^0.4.3"             # Tooltip system
sphinx-hoverxref = "^1.4.2"         # Hover cross-references
sphinx-codeautolink = "^0.15.0"     # Automatic code linking
sphinxext-rediraffe = "^0.2.7"      # Redirect management
```

**@interactive @ux**: User experience enhancements  
**Status**: 🚧 Need to test interactive features

---

## 📊 Diagrams & Visualizations

### Diagram Generation

```toml
sphinxcontrib-mermaid = "^1.0.0"    # Mermaid diagrams (active)
sphinxcontrib-plantuml = "^0.30"    # PlantUML diagrams (active)
sphinx-diagrams = "^0.4.0"          # Python diagrams library
sphinxcontrib-drawio = "^0.0.17"    # Draw.io integration
```

### Specialized Diagrams

```toml
sphinxcontrib-seqdiag = "^3.0.0"    # Sequence diagrams
sphinxcontrib-blockdiag = "^3.0.0"  # Block diagrams
sphinx-mindmap = "^0.5.2"           # Mind maps
sphinx-timeline = "^0.2.1"          # Timeline visualization
sphinx-uml = "^0.3.2"               # UML diagrams
sphinx-charts = "^0.2.1"            # Chart generation
sphinx-visualized = "^0.4.0"        # Data visualization
```

### Mathematical Content

```toml
sphinx-math-dollar = "^1.2.1"       # Dollar-sign math notation
sphinx-proof = "^0.2.1"             # Mathematical proofs
sphinx-exercise = "^1.0.1"          # Exercise formatting
```

**@diagrams @visualization**: Visual content generation  
**Status**: 🚧 Testing needed for all diagram types

### Diagram Testing Plan

```markdown
Diagram Types to Test:

- [x] Graphviz inheritance diagrams (working)
- [x] Mermaid flowcharts (configured)
- [x] PlantUML class diagrams (configured)
- [ ] Sequence diagrams
- [ ] Block diagrams
- [ ] Mind maps
- [ ] Timeline visualizations
- [ ] Mathematical proofs
```

---

## 🌐 External Integrations

### Documentation Platforms

```toml
readthedocs-sphinx-search = "^0.3.2" # RTD search integration
sphinx-notfound-page = "^1.1.0"      # Custom 404 pages
sphinx-sitemap = "^2.6.0"            # SEO sitemap (active)
sphinxext-opengraph = "^0.10.0"      # Open Graph metadata
```

### API & Schema Documentation

```toml
sphinxcontrib-openapi = "^0.8.4"     # OpenAPI/Swagger docs
sphinxcontrib-httpdomain = "^1.8.1"  # HTTP API documentation
sphinx-jsonschema = "^1.19.1"        # JSON Schema docs
sphinx-apischema = "^0.1"            # API schema documentation
```

### Code Integration

```toml
sphinxcontrib-programoutput = "^0.18" # Program output inclusion
sphinx-exec-directive = "^0.6"       # Execute code in docs
sphinx-pyscript = "^0.1.0"           # PyScript integration
jupyter-cache = "^1.0.1"             # Jupyter execution caching
sphinx-thebe = "^0.3.1"              # Live code execution
sphinx-thebelab = "^0.0.6"           # ThebeLab integration
```

### Media & Assets

```toml
sphinxcontrib-images = "^1.0.1"      # Image gallery
sphinxcontrib-video = "^0.4.1"       # Video embedding
sphinxcontrib-youtube = "^1.4.1"     # YouTube integration
sphinx-galleria = "^2.1.0"           # Photo galleries
sphinx-favicon = "^1.0.1"            # Favicon management
sphinxemoji = "^0.3.1"               # Emoji support
sphinx-fasvg = "^2.0.2"              # SVG icon integration
```

**@integration @external**: Third-party service integration  
**Status**: 🚧 Need to test external services

---

## 🔧 Development & Quality

### Code Quality

```toml
doc8 = "^1.1.2"                     # Documentation linting
codespell = "^2.4.1"                # Spell checking
sphinx-lint = "^1.0.0"              # Sphinx-specific linting
darglint2 = "^1.8.2"                # Docstring linting
sphinx-spelling = "^8.0.1"          # Advanced spell checking
pyenchant = "^3.2.2"                # Spell checking backend
```

### Development Tools

```toml
sphinx-testing = "^1.0.1"           # Testing utilities
pytest-doctestplus = "^1.4.0"       # Enhanced doctest
sphinx-debuginfo = "^0.2.2.post1"   # Debug information
sphinx-cache = "^0.0.1"             # Build caching
sphinx-watch = "^0.1.2"             # File watching
```

### CLI & Project Tools

```toml
sphinx-argparse = "^0.5.2"          # Argparse documentation
sphinx-click = "^6.0.0"             # Click command documentation
sphinx-cmd = "^0.5.0"               # Command line tools
sphinx-pyproject = "^0.3.0"         # pyproject.toml integration
```

**@development @quality**: Development workflow and code quality  
**Status**: 🚧 Need to configure linting pipeline

---

## 📄 Alternative Documentation Tools

### Other Generators (Comparison)

```toml
mkdocs = "^1.6.1"                   # MkDocs static site generator
mkdocs-material = "^9.6.16"         # Material Design theme for MkDocs
mkdocstrings = "^0.30.0"            # MkDocs API documentation
pdoc = "^15.0.4"                    # Simple API documentation
pydoctor = "^25.4.0"                # API documentation generator
```

**@comparison @alternatives**: Documentation tool comparison  
**Status**: 📋 For testing against Sphinx  
**Purpose**: Benchmark Sphinx features against alternatives

---

## 🎪 Specialized & Experimental

### Presentation & Publishing

```toml
sphinx-revealjs = "^3.2.0"          # Reveal.js presentations
sphinx-pdf-generate = "^0.0.4"      # PDF generation
sphinx-simplepdf = "^1.6.0"         # Simple PDF output
sphinx-reports = "^0.9.7"           # Report generation
sphinx-desktop = "^20240301"        # Desktop app generation
```

### Project Management

```toml
sphinx-needs = "^5.1.0"             # Requirements management
sphinx-issues = "^5.0.1"            # Issue tracking integration
sphinx-contributors = "^0.2.7"      # Contributor documentation
sphinx-changelog = "^1.6.0"         # Changelog generation
sphinx-git = "^11.0.0"              # Git integration
```

### Experimental Features

```toml
sphinx-me = "^0.3"                  # Personal documentation
sphinx-dust = "^1.2.4"              # Dust template system
sphinx-collections = "^0.2.0"       # Content collections
sphinx-combine = "^2024.12.30.1"    # Content combination
sphinx-variations = "^1.0.5"        # Content variations
sphinx-multiproject = "^1.0.0"      # Multi-project documentation
```

### Utility Extensions

```toml
sphinx-substitution-extensions = "^2025.6.6" # Text substitutions
sphinx-paramlinks = "^0.6.0"                 # Parameter linking
sphinx-removed-in = "^0.2.3"                 # Deprecation notices
sphinx-selective-exclude = "^1.0.3"          # Conditional inclusion
sphinx-reredirects = "^1.0.0"                # Redirect handling
sphinx-tags = "^0.4"                         # Content tagging
sphinx-toml = "^0.0.4"                       # TOML configuration
sphinx-sql = "^1.3.5"                        # SQL documentation
sphinx-typesafe = "^0.3"                     # Type safety checks
sphinx-tsegsearch = "^1.2"                   # Search segmentation
sphinx-intl = "^2.3.1"                       # Internationalization
sphinx-jinja2 = "^0.0.1"                     # Jinja2 integration
sphinx-jinja = "^2.0.2"                      # Alternative Jinja2
```

**@experimental @utilities**: Advanced and experimental features  
**Status**: 📋 For advanced testing scenarios

---

## 🧪 Testing Strategy

### Phase 1: Core Features ✅ COMPLETED

- [x] Basic Sphinx build
- [x] AutoAPI generation
- [x] Pydantic model documentation
- [x] Enum documentation with enum-tools
- [x] Theme compatibility (Furo)

### Phase 2: Multi-Version 🚧 CURRENT

- [ ] sphinx-multiversion configuration
- [ ] Git branch/tag detection
- [ ] Version navigation
- [ ] Cross-version linking
- [ ] Version comparison

### Phase 3: Theme Testing 📋 PLANNED

- [ ] Furo (baseline)
- [ ] PyData Sphinx Theme
- [ ] Read the Docs Theme
- [ ] Sphinx Book Theme
- [ ] Modern themes

### Phase 4: Interactive Features 📋 PLANNED

- [ ] Tabs and toggles
- [ ] Copy buttons
- [ ] Search functionality
- [ ] Interactive diagrams
- [ ] Live code execution

### Phase 5: Advanced Features 📋 FUTURE

- [ ] PDF generation
- [ ] Presentation mode
- [ ] Multi-language support
- [ ] External API integration
- [ ] Performance optimization

---

## 📊 Compatibility Matrix

| Feature Category  | Furo | PyData | RTD | Book | Status          |
| ----------------- | ---- | ------ | --- | ---- | --------------- |
| **Core Features** |
| AutoAPI           | ✅   | ?      | ?   | ?    | Testing needed  |
| Pydantic Models   | ✅   | ?      | ?   | ?    | Working in Furo |
| Enum Tools        | ✅   | ?      | ?   | ?    | Working in Furo |
| **Interactive**   |
| Toggle Buttons    | ✅   | ?      | ?   | ?    | Working in Furo |
| Copy Buttons      | ✅   | ?      | ?   | ?    | Working in Furo |
| Tabs              | ✅   | ?      | ?   | ?    | Need to test    |
| **Diagrams**      |
| Mermaid           | ✅   | ?      | ?   | ?    | Configured      |
| PlantUML          | ✅   | ?      | ?   | ?    | Configured      |
| Graphviz          | ✅   | ?      | ?   | ?    | Working         |
| **Multi-Version** |
| Version Dropdown  | ?    | ?      | ?   | ?    | Not tested      |
| Cross-linking     | ?    | ?      | ?   | ?    | Not implemented |

---

## 📝 Configuration Notes

### Extension Loading Strategy

```python
# Modular approach in conf_modules/extensions.py
optional_extensions = []

# Check for each extension and add if available
try:
    import myst_parser
    optional_extensions.append("myst_parser")
except ImportError:
    print("Warning: myst_parser not installed")

# This pattern repeated for all ~150 extensions
```

### Priority Loading Order

1. **Core Sphinx** (`sphinx`, `autodoc`, `napoleon`)
2. **API Generation** (`autoapi`, `autodoc-pydantic`)
3. **Content** (`myst-parser`, `sphinx-design`)
4. **Interactive** (`togglebutton`, `copybutton`, `tabs`)
5. **Diagrams** (`mermaid`, `plantuml`, `graphviz`)
6. **Multi-Version** (`sphinx-multiversion`)
7. **Themes** (`furo`, `pydata-sphinx-theme`, etc.)
8. **Experimental** (remaining extensions)

### Performance Considerations

```markdown
With 150+ extensions:

- Build time: Expect 2-5x slower builds
- Memory usage: High RAM requirements
- Dependency conflicts: Potential version issues
- Load order: Critical for stability

Optimization strategies:

- Conditional loading based on build type
- Profile builds to identify slow extensions
- Use caching where possible
- Consider build matrix for testing
```

---

## 🚀 Next Actions

### Immediate (Today)

- [ ] **@multiversion**: Configure sphinx-multiversion
- [ ] **@testing**: Test current build with all dependencies
- [ ] **@documentation**: Document which extensions are actually loaded
- [ ] **@performance**: Measure build time with full dependency set

### Short Term (This Week)

- [ ] **@themes**: Test top 5 themes with current content
- [ ] **@interactive**: Validate tabs, toggles, copy buttons
- [ ] **@diagrams**: Test Mermaid, PlantUML, sequence diagrams
- [ ] **@quality**: Set up linting pipeline with doc8, codespell

### Medium Term (Next Weeks)

- [ ] **@optimization**: Profile and optimize build performance
- [ ] **@comparison**: Create theme/feature comparison dashboard
- [ ] **@automation**: GitHub Actions for multi-theme builds
- [ ] **@advanced**: Test experimental features

---

**@dependencies @comprehensive**: Full dependency analysis complete  
**Total Count**: ~150 documentation-related packages  
**Status**: Installation complete, testing phase beginning  
**Next Update**: After sphinx-multiversion configuration
