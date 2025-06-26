# Haive Documentation Consolidation Plan

## Overview
This plan outlines the steps to consolidate and organize the scattered documentation in the Haive project following Sphinx and Google documentation conventions.

## Current State Analysis
- Documentation is scattered across 12+ different directory patterns
- Mixed formats: .md, .rst, .py (examples), .ipynb
- No consistent structure or indexing
- Tests are mixed with source code instead of in `packages/haive-*/tests`

## Proposed Structure

### 1. Main Documentation Directory (`/docs`)
```
docs/
├── source/
│   ├── _static/          # CSS, JS, images
│   ├── _templates/       # Custom Sphinx templates
│   ├── _extensions/      # Haive Sphinx extensions
│   ├── api/             # Auto-generated API docs
│   │   ├── core/
│   │   ├── agents/
│   │   ├── tools/
│   │   ├── games/
│   │   ├── dataflow/
│   │   ├── prebuilt/
│   │   └── mcp/
│   ├── guides/          # User guides and tutorials
│   │   ├── getting_started.rst
│   │   ├── installation.rst
│   │   ├── quickstart.rst
│   │   ├── architecture.rst
│   │   ├── building_agents.rst
│   │   ├── custom_tools.rst
│   │   ├── state_management.rst
│   │   └── best_practices.rst
│   ├── examples/        # Code examples and notebooks
│   │   ├── agents/
│   │   ├── tools/
│   │   ├── games/
│   │   └── notebooks/
│   ├── reference/       # Technical reference
│   │   ├── changelog.rst
│   │   ├── migration_guides.rst
│   │   ├── troubleshooting.rst
│   │   └── glossary.rst
│   ├── development/     # Developer documentation
│   │   ├── contributing.rst
│   │   ├── testing.rst
│   │   ├── documentation_standards.rst
│   │   └── release_process.rst
│   └── index.rst        # Main entry point
├── build/               # Generated documentation
└── Makefile
```

### 2. Package Structure
Each package should follow this structure:
```
packages/haive-{package}/
├── src/
│   └── haive/
│       └── {package}/
│           ├── __init__.py      # Module docstring
│           ├── README.md        # Module overview
│           └── submodule/
│               ├── __init__.py  # Submodule docstring
│               └── README.md    # Submodule details
├── tests/                       # All tests here
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── examples/                    # Package examples
└── README.md                    # Package overview
```

## Action Items

### Phase 1: Setup and Structure (Immediate)
1. Create the proposed directory structure in `/docs/source`
2. Move all test files to `packages/haive-*/tests/`
3. Create template README.md for modules and submodules
4. Create template __init__.py with proper Google-style docstrings

### Phase 2: Content Migration (Week 1)
1. **Root Level Docs → Appropriate Locations**
   - TODO.md → `/docs/source/development/todo.rst`
   - AGENT_SCHEMA_COMPOSER_FIXES.md → `/docs/source/reference/technical/`
   - multi_agent_*.md → `/docs/source/reference/architecture/`
   
2. **Project Docs → Documentation**
   - `/project_docs/*` → `/docs/source/reference/` or `/docs/source/guides/`
   - `/personal_notes/*` → Remove or move to private location
   
3. **Notebooks → Examples**
   - Clean up untitled notebooks
   - Move to `/docs/source/examples/notebooks/` with descriptive names

### Phase 3: API Documentation (Week 2)
1. Generate module and submodule READMEs using templates
2. Update all __init__.py files with comprehensive docstrings
3. Configure Sphinx autodoc to generate API documentation
4. Create module overview pages linking to READMEs

### Phase 4: Content Enhancement (Week 3)
1. Convert key .md files to .rst for better Sphinx integration
2. Add cross-references between related documentation
3. Create comprehensive index and navigation
4. Add code examples from example.py files

### Phase 5: Cleanup and Validation (Week 4)
1. Remove duplicate documentation
2. Delete outdated content
3. Validate all internal links
4. Run documentation linting
5. Test build with `poetry run nox -s docs`

## Documentation Standards

### Module README Template
```markdown
# Module Name

Brief description of the module's purpose.

## Overview
Detailed explanation of what this module provides.

## Key Components
- Component 1: Description
- Component 2: Description

## Usage Examples
```python
# Example code
```

## API Reference
See the [API documentation](link) for detailed reference.

## See Also
- Related module 1
- Related module 2
```

### __init__.py Docstring Template
```python
"""Module name - Brief description.

This module provides [functionality description]. It is designed to
[purpose and use cases].

Key Features:
    * Feature 1: Description
    * Feature 2: Description
    * Feature 3: Description

Example:
    Basic usage example::

        from haive.module import Component
        
        component = Component()
        result = component.process(data)

Note:
    Any important notes about the module.

See Also:
    :mod:`haive.related_module`: Description of relationship
"""
```

## Build Commands
All documentation commands should use poetry:
- Build: `poetry run nox -s docs`
- Live reload: `poetry run nox -s docs-live`
- Clean: `poetry run nox -s docs-clean`
- Check: `poetry run nox -s docs-check`

## Success Metrics
- All documentation accessible from main index
- No scattered .md files outside of docs/
- All tests in `packages/haive-*/tests/`
- All modules have README.md and proper __init__.py docstrings
- Documentation builds without warnings
- Cross-references work correctly