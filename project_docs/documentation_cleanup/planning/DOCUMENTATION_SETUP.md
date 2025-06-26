# Haive Documentation Setup

This document provides an overview of the documentation tools and standards we've set up for the Haive framework.

## Documentation Structure

We've organized the documentation as follows:

1. **Documentation Guides in Sphinx**:
   - `/docs/source/guides/documentation/index.rst` - Main documentation guide
   - `/docs/source/guides/documentation/docstring_standards.rst` - Google-style docstring standards
   - `/docs/source/guides/documentation/documentation_tools.rst` - Documentation tools guide
   - `/docs/source/guides/documentation/module_readmes.rst` - Guide for module READMEs
   - `/docs/source/guides/documentation/documentation_process.rst` - Documentation workflow

2. **Automated Documentation Tools**:
   - `/scripts/doc_tools/add_docstrings.py` - Script to automatically add docstrings
   - `/scripts/doc_tools/templates/` - Templates for consistent documentation

## Using the Documentation Tools

The main tool is `add_docstrings.py`, which can:

1. Add Google-style docstrings to modules, classes, and functions
2. Create README.md files for modules
3. Support dry-run mode to preview changes

To use it:

```bash
# From the project root
python scripts/doc_tools/add_docstrings.py --path packages/haive-games/src/haive/games/chess
```

## Documentation Standards

We've established standards for:

1. **Module-level docstrings**: Overview, examples, and typical usage
2. **Class docstrings**: Purpose, attributes, and examples
3. **Function docstrings**: Purpose, parameters, return values, and examples
4. **Module READMEs**: Comprehensive documentation of module functionality

## Integration with Sphinx

The documentation is fully integrated with the Sphinx documentation system:

```bash
# Build documentation
nox -s docs

# Live documentation server
nox -s docs-live
```

## Next Steps

1. Run the docstring generation tools on key packages
2. Review and enhance the generated documentation
3. Build the Sphinx documentation to verify integration
4. Add more detailed examples to key modules

## Resources

- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Sphinx Documentation](https://www.sphinx-doc.org/en/master/)
- [Napoleon Extension](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html)
